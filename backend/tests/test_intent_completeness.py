import pytest
from backend.app.models import IntentUnderstanding
from backend.app.nodes.intent import reconcile_completeness
from backend.app.graph import route_intent


def decision(**changes):
    data = dict(intent='database_query', confidence=.95,
                required_tables=['guards', 'guard_availabilities'],
                resolved_question='Is Ashfaque available on 2026-09-25 after 10 PM?',
                task_complete=False, needs_clarification=False)
    data.update(changes)
    return IntentUnderstanding(**data)


def test_logged_contradiction_proceeds_to_database():
    result = reconcile_completeness(decision(), {'guards', 'guard_availabilities'})
    assert result.task_complete
    assert not result.needs_clarification
    assert route_intent({'intent': result.model_dump()}) == 'database'


@pytest.mark.parametrize('change', [
    {'needs_clarification': True},
    {'missing_required_context': True},
    {'missing_information': ['Which date?']},
    {'ambiguity': ['Multiple guards match']},
    {'clarification_question': 'Which guard?'},
    {'clarification_items': [{'kind': 'required_context', 'question': 'Which timezone?'}]},
])
def test_real_blockers_are_preserved_even_with_complete_flag(change):
    result = reconcile_completeness(decision(task_complete=True, **change), {'guards', 'guard_availabilities'})
    assert result.needs_clarification
    assert not result.task_complete
    assert route_intent({'intent': result.model_dump()}) == 'clarify'


@pytest.mark.parametrize('change', [
    {'confidence': .5}, {'required_tables': []}, {'required_tables': ['roles']},
    {'resolved_question': None}, {'intent': 'unsafe_request'},
])
def test_insufficient_evidence_does_not_override_incomplete(change):
    result = reconcile_completeness(decision(**change), {'guards', 'guard_availabilities'})
    assert not result.task_complete
