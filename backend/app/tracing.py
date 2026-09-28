"""Request-scoped terminal timing; never prints prompts, credentials or rows."""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from time import perf_counter
from uuid import uuid4
from threading import RLock


@dataclass
class RequestTrace:
    request_id: str
    steps: int = 0
    llm_calls: int = 0
    embedding_calls: int = 0
    status: str = "error"


_request: ContextVar[RequestTrace | None] = ContextVar("request_trace", default=None)
_step: ContextVar[int | None] = ContextVar("trace_step", default=None)
_progress: dict[str, dict[str, object]] = {}
_progress_lock = RLock()


USER_STEP_MESSAGES = {
    "Resolve conversation context": ("Preparing your request", "Using this conversation's relevant context."),
    "Analyze intent": ("Understanding your question", "Identifying the information you need."),
    "Resolve entities": ("Matching requested records", "Checking relevant names and values."),
    "Retrieve": ("Finding relevant data", "Selecting the parts of your data needed for this question."),
    "Make plan": ("Preparing the data request", "Choosing the relevant fields and verified connections."),
    "Generate": ("Preparing a safe data request", "Applying your question to the selected data."),
    "Validate": ("Checking the data request", "Verifying it is safe and valid."),
    "Repair": ("Refining the data request", "Correcting a request that could not be verified."),
    "Execute": ("Retrieving results", "Reading the requested data."),
    "Build answer": ("Preparing your answer", "Summarizing the verified results."),
}


def publish_progress(request_id: str, title: str, detail: str, *, complete: bool = False) -> None:
    with _progress_lock:
        _progress[request_id] = {"title": title, "detail": detail, "complete": complete}


def get_progress(request_id: str) -> dict[str, object] | None:
    with _progress_lock:
        value = _progress.get(request_id)
        return dict(value) if value else None


def emit(trace, message):
    print(f"[Request {trace.request_id}] {message}", flush=True)


def log_llm_payload(label: str, payload: str):
    """Print application-visible LLM inputs and outputs for request debugging."""
    trace = _request.get()
    if trace is None:
        return
    emit(trace, f"{label}\n{payload}")


@contextmanager
def request_trace(request_id: str | None = None):
    trace = RequestTrace(request_id or uuid4().hex[:8])
    token = _request.set(trace)
    started = perf_counter()
    emit(trace, "START | Processing question")
    try:
        yield trace
    finally:
        emit(trace, f"END | Status: {trace.status} | Steps: {trace.steps} | "
             f"LLM calls: {trace.llm_calls} | Embedding calls: {trace.embedding_calls} | "
             f"Total request processing time: {perf_counter() - started:.3f}s")
        publish_progress(trace.request_id, "Finishing up", "Your response is ready.", complete=True)
        _request.reset(token)


def traced_step(name, llm):
    def decorate(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            trace = _request.get()
            if trace is None:
                return fn(*args, **kwargs)
            trace.steps += 1
            number = trace.steps
            token = _step.set(number)
            calls_before = trace.llm_calls
            embeddings_before = trace.embedding_calls
            started = perf_counter()
            outcome = "ERROR"
            emit(trace, f"Step {number}: {name} | START | LLM call: {llm}")
            title, detail = USER_STEP_MESSAGES.get(name, ("Working on your request", "Processing your question."))
            publish_progress(trace.request_id, title, detail)
            try:
                result = fn(*args, **kwargs)
                outcome = "ERROR" if isinstance(result, dict) and result.get("status") == "error" else "DONE"
                return result
            finally:
                calls = trace.llm_calls - calls_before
                emit(trace, f"Step {number}: {name} | {outcome} | "
                     f"LLM call: {'Yes' if calls else 'No'} ({calls}) | "
                     f"Embedding calls: {trace.embedding_calls - embeddings_before} | "
                     f"Response time: {perf_counter() - started:.3f}s")
                _step.reset(token)
        return wrapped
    return decorate


@contextmanager
def model_call(kind, purpose):
    trace = _request.get()
    if trace is None:
        yield
        return
    if kind == "LLM":
        trace.llm_calls += 1
        number = trace.llm_calls
    else:
        trace.embedding_calls += 1
        number = trace.embedding_calls
    label = f"Step {_step.get()}: {kind} call {number} ({purpose})"
    started = perf_counter()
    outcome = "ERROR"
    emit(trace, f"{label} | START")
    try:
        yield
        outcome = "DONE"
    finally:
        emit(trace, f"{label} | {outcome} | Response time: {perf_counter() - started:.3f}s")
