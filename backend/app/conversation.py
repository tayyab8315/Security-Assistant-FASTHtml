from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from threading import RLock
from time import monotonic
import json
import uuid


@dataclass
class Conversation:
    turns: list[dict] = field(default_factory=list)
    pending: dict | None = None
    updated: float = field(default_factory=monotonic)


class ConversationManager:
    """Bounded process-local context; use shared storage for multiple workers."""
    def __init__(self, ttl=3600, max_conversations=1000, max_turns=3):
        self._conversations: dict[str, Conversation] = {}
        self._lock = RLock()
        self.ttl, self.max_conversations, self.max_turns = ttl, max_conversations, max_turns

    def _get(self, cid):
        now = monotonic()
        self._conversations = {k: v for k, v in self._conversations.items()
                               if now - v.updated < self.ttl}
        return self._conversations.get(cid)

    def _ensure(self, cid):
        conversation = self._get(cid)
        if conversation is None:
            if len(self._conversations) >= self.max_conversations:
                oldest = min(self._conversations, key=lambda k: self._conversations[k].updated)
                del self._conversations[oldest]
            conversation = self._conversations[cid] = Conversation()
        conversation.updated = monotonic()
        return conversation

    def normalize(self, conversation_id: str | None, message: str) -> tuple[str, str]:
        cid = conversation_id or uuid.uuid4().hex
        pending = self.context(cid).get('pending_clarification')
        if not pending:
            return cid, message
        return cid, (f"Original request: {pending['original_question']}\n"
                     f"Clarification asked: {pending['clarification_question']}\n"
                     f"User clarification: {message}")

    def context(self, cid):
        with self._lock:
            conversation = self._get(cid)
            if conversation is None:
                return {}
            return deepcopy({'recent_turns': conversation.turns,
                             'pending_clarification': conversation.pending})

    def remember_clarification(self, conversation_id, original_question, clarification_question,
                               *, intent=None, message=None):
        intent = intent or {}
        with self._lock:
            conversation = self._ensure(conversation_id)
            previous = conversation.pending
            continuing = previous is not None and intent.get('clarification_relation') != 'new_request'
            exchanges = list(previous.get('exchanges', [])) if continuing else []
            if continuing and message:
                exchanges.append({'asked': previous['clarification_question'], 'reply': message[:4000]})
            details = intent.get('known_details') or (previous.get('known_details', []) if continuing else [])
            # Keep raw replies as evidence even if the model omits a known detail.
            conversation.pending = {
                'original_question': previous['original_question'] if continuing else original_question[:4000],
                'resolved_question': (intent.get('resolved_question') or original_question)[:4000],
                'known_details': [str(v)[:500] for v in details[:16]],
                'unresolved_questions': [str(v)[:500] for v in intent.get('missing_information', [])[:8]],
                'clarification_question': clarification_question[:4000],
                'exchanges': exchanges[-4:]}

    def remember_result(self, cid, message, state):
        # Only retain results already released by the validated query pipeline.
        rows = state.get('result_rows') or []
        turn = {'user_message': message[:4000],
                'resolved_question': state.get('question', message)[:4000],
                'intent': state.get('intent', {}).get('intent'),
                'plan': state.get('plan'), 'sql': state.get('selected_sql'),
                'resolved_entities': state.get('resolved_entities', []),
                'result_rows': rows[:10], 'result_count': len(rows),
                'results_truncated': len(rows) > 10}
        # Bound serialized context even for unusually large cells or plans.
        for key in ('result_rows', 'resolved_entities', 'plan', 'sql'):
            if len(json.dumps(turn, default=str)) <= 20000:
                break
            turn.pop(key, None)
            turn['results_truncated'] = True
        with self._lock:
            conversation = self._ensure(cid)
            conversation.pending = None
            conversation.turns = (conversation.turns + [deepcopy(turn)])[-self.max_turns:]

    def forget(self, conversation_id):
        with self._lock:
            self._conversations.pop(conversation_id, None)


manager = ConversationManager()
