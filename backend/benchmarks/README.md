# 50-question benchmark

Run from this copy project folder:

```powershell
C:\Python314\python.exe -B benchmarks/run_50.py
```

The runner targets the project folder that contains this `benchmarks` directory
and invokes its `ask()` handler directly in a fresh process per question. This captures the same
Python print logs used by the API without depending on another terminal's output.
It exercises live Ollama and database connections, but does not measure HTTP latency
or conversation follow-ups. The restricted-action questions test rejection behavior.

Each dated run folder contains:

- `all_questions.txt`: combined logs, appended and flushed after every completed
  question. It includes every question, expected status, numbered step and
  model-call logs, durations, complete response, and verdict.
- `results.json`: incremental status results and wall times, updated per question.

`all_questions.txt` is written after every question, not only after all 50 finish.
Each completed question update is flushed to disk with `fsync`. A 180-second
per-question timeout is recorded as a failure and the run continues. Wall time
includes process startup; the step logs separately report pipeline request time.

PASS means the response status matches the expected status, not that every SQL
query or answer is semantically correct. Empty query results can be valid.
Expected clarifications follow this project's current glossary, where the
meaning of active/inactive is still undefined. All 50 requests are independent.

Logs contain database results and debug information: keep them local/private.
The two initial incomplete runs on 2026-09-16 record a sandbox permission failure
and a Chroma runtime mismatch. The complete run uses Python 3.14 and Chroma 1.5.9.
