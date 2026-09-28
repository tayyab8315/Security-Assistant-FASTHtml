# Tests

Run `python -m pytest -q` from the project root for the pipeline and FastHTML HTTP/markup tests in `backend/tests`.

Run `node --test tests/sentinel_client.test.mjs` for dependency-free browser interaction logic tests (DOM stub): clarification IDs, HTTP error envelopes, escaping, history, prompts, tables, settings, and themes. Node is only a test tool, not an application runtime dependency.

The Sentinel frontend is implemented in `backend/app/web_ui.py` and `static/sentinel/`. Browser layout and interaction should also be checked manually at desktop and mobile sizes.
