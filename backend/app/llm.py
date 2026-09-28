from __future__ import annotations
import json
from typing import Any, TypeVar, Type

from ollama import Client
from pydantic import BaseModel, ValidationError

from .config import settings
from .catalog import prompt
from .tracing import log_llm_payload, model_call

T = TypeVar("T", bound=BaseModel)


def make_client(host: str, api_key: str = "") -> Client:
    return Client(
        host=host,
        headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
        timeout=settings.ollama_timeout_seconds,
    )


_client = make_client(settings.ollama_native_host, settings.ollama_api_key.get_secret_value())
# Do not forward the cloud credential to a separate embedding service.
_embed_client = make_client(settings.embedding_host, settings.ollama_embed_api_key.get_secret_value())


def _json_candidates(content: str) -> list[Any]:
    """Extract direct, fenced, or embedded JSON objects from a model response."""
    text = content.strip().lstrip("\ufeff")
    candidates = [text]
    if "```" in text:
        for block in text.split("```")[1::2]:
            block = block.strip()
            if block.lower().startswith("json"):
                block = block[4:].lstrip(": \r\n")
            candidates.append(block)

    # A model can add a short sentence before or after the object. Decode every
    # balanced JSON object start without trusting arbitrary text as JSON.
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        candidates.append(value)

    result = []
    for candidate in candidates:
        if isinstance(candidate, (dict, list)):
            value = candidate
        else:
            try:
                value = json.loads(candidate)
            except (TypeError, json.JSONDecodeError):
                continue
        if value not in result:
            result.append(value)
    return result


def _parse_structured(model_cls: Type[T], content: str) -> T:
    errors = []
    for value in _json_candidates(content):
        try:
            return model_cls.model_validate(value)
        except ValidationError as exc:
            errors.append(str(exc).splitlines()[0])
    detail = errors[0] if errors else "no JSON object found"
    raise ValueError(f"Invalid {model_cls.__name__} response: {detail}")


def structured_chat(model_cls: Type[T], system: str, user: str, temperature: float = 0.0) -> T:
    schema = model_cls.model_json_schema()
    cloud = settings.ollama_direct_cloud or settings.ollama_llm_model.endswith((":cloud", "-cloud"))
    instruction = system + prompt("structured_output_instruction", schema=json.dumps(schema))
    messages = [{"role": "system", "content": instruction}, {"role": "user", "content": user}]
    last_error = ""
    for attempt in range(2):
        log_llm_payload(
            f"LLM INPUT ({model_cls.__name__}, attempt {attempt + 1}) | Messages sent:",
            compact_json(messages),
        )
        with model_call("LLM", f"{model_cls.__name__}, attempt {attempt + 1}"): 
            response = _client.chat(
                model=settings.ollama_chat_model,
                messages=messages,
                options={"temperature": temperature},
                **({} if cloud else {"format": schema}),
            )
        content = (response.message.content or "").strip()
        if not content:
            log_llm_payload("LLM response diagnostic", compact_json({
                "model": settings.ollama_chat_model,
                "done_reason": getattr(response, "done_reason", None),
                "has_thinking": bool(getattr(response.message, "thinking", None)),
                "error": "Empty final content; thinking is not used as an answer.",
            }))
        log_llm_payload(
            f"LLM OUTPUT ({model_cls.__name__}, attempt {attempt + 1}) | Raw response:",
            content,
        )
        try:
            parsed = _parse_structured(model_cls, content)
            log_llm_payload(
                f"LLM OUTPUT ({model_cls.__name__}, attempt {attempt + 1}) | Parsed response:",
                compact_json(parsed.model_dump()),
            )
            return parsed
        except ValueError as exc:
            last_error = str(exc)
            if attempt == 0:
                if content:
                    messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": prompt("structured_retry_user")})
    raise ValueError(f"Ollama returned invalid structured JSON after two attempts: {last_error}") from None


def text_chat(system: str, user: str, temperature: float = 0.0) -> str:
    log_llm_payload("LLM INPUT (Final answer) | System prompt:", system)
    log_llm_payload("LLM INPUT (Final answer) | User prompt:", user)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for attempt in range(2):
        if attempt:
            messages.append({"role": "user", "content": prompt("final_answer_retry_user")})
            log_llm_payload("LLM INPUT (Final answer retry) | Messages sent:", compact_json(messages))
        with model_call("LLM", f"Final answer, attempt {attempt + 1}"):
            response = _client.chat(
                model=settings.ollama_chat_model,
                messages=messages,
                options={"temperature": temperature},
            )
        content = (response.message.content or "").strip()
        log_llm_payload(f"LLM OUTPUT (Final answer, attempt {attempt + 1}) | Raw response:", content)
        if content:
            return content
    raise ValueError("Ollama returned empty final answer content after two attempts.")


def embed_texts(texts: list[str]) -> list[list[float]]:
    with model_call("Embedding", f"{len(texts)} texts"):
        response = _embed_client.embed(model=settings.ollama_embed_model, input=texts)
    return response.embeddings


def compact_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
