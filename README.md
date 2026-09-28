# Security Assistant — FastHTML

One Python application serves the Sentinel interface and JSON endpoints. FastHTML replaces the previous FastAPI web layer; the existing LangGraph, Ollama, Chroma, and SQLAlchemy services run directly in the same process.

## Run on Windows

Use Python 3.11 (the existing environment is `backend/.venv`). From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Only when backend/.env does not already exist:
Copy-Item backend/.env.example backend/.env
python main.py
```

Or use the existing environment after installing the root requirements into it:

```powershell
.\backend\.venv\Scripts\python.exe main.py
```

Open http://127.0.0.1:8000. `HOST` and `PORT` override the local bind address and port. There is no separate frontend or FastAPI server.

## Connections

Keep your database and model configuration in `backend/.env`. Set `DATABASE_URL` (a read-only database account), `OLLAMA_HOST`, `OLLAMA_LLM_MODEL`, and `OLLAMA_EMBED_MODEL`. Existing credentials are preserved. Default local models:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

Index the schema from the root after configuring the services:

```powershell
python -m backend.scripts.index_schema
```

The UI starts without live services. Dashboard counts and AI answers require the corresponding database/model connections. Knowledge-document ingestion is not implemented by the existing pipeline; knowledge requests retain its `knowledge_not_found` behavior.

## Interface

The frontend matches the supplied `sentinel-chat-ui.zip`: its exact stylesheet and SVG assets are served locally, while `backend/app/web_ui.py` builds the page with FastHTML components. JavaScript handles browser interactions; no Node server, React build, or external frontend CDN is required.

- Dark purple desktop layout and responsive mobile sidebar.
- Chat with loading state, stop-waiting control, clarification replies, errors, and retry.
- Conversation search, rename/delete, JSON export, and optional browser-local persistence (up to 50 saved conversations).
- Twelve starter prompts plus count prompts and Data Explorer cards generated from the configured allowed tables (currently 39).
- Result filtering, ten-row pagination, CSV export, copied answers/SQL, source labels, and query details when returned by the backend.
- Light/dark theme, connection information, keyboard shortcuts, and settings to disable or clear saved history.

Conversation history, including result rows, is stored in this browser by default, matching the reference. Turn off **Remember conversations** in Settings to remove saved history. Backend context retains the last three completed requests, bounded result previews, and pending clarifications for one hour. Follow-ups are resolved by the intent model without keyword matching. Context is process-local and is lost on restart; multiple workers require shared storage. **Stop waiting** cancels the browser request, not necessarily the running model/database work.

The connection pill checks the application's `/health` endpoint; it does not prove database/model readiness. The data explorer describes supported domains rather than displaying live database counts. JavaScript is required for interactive features.

Set a strong `SESSION_SECRET` in `backend/.env` for stable signed sessions. Without it, FastHTML stores a generated local secret in the ignored `.sesskey` file. Authentication is not included; the server binds to localhost by default.

## Routes and structure

- `GET /` and `GET /chat`: Sentinel interface (`/chat?question=...` prefills the composer).
- `GET /static/sentinel/...`: local styles, browser interactions, and favicon.
- `GET /health`: process health/configuration.
- `POST /ask`: JSON endpoint accepting `question` and optional `conversation_id`; validation errors use HTTP 422 and pipeline errors use HTTP 500.

`main.py` is the entry point. `backend/app/main.py` owns the FastHTML app and request orchestration; `backend/app/web_ui.py` contains the page components. `static/sentinel/` holds the reference design assets and browser interaction code. The graph, nodes, database service, prompts, schema catalog, and security policy remain under `backend/`. Root `requirements.txt` is the authoritative dependency list.

The expanded SQL schema supports 39 operational tables. See [schema expansion and future table setup](backend/docs/SCHEMA_EXPANSION.md) for exclusions, protected columns, unresolved relationships, and indexing instructions. Adding configured tables also updates the Data Explorer on page reload; no hardcoded frontend cards are required.

Schema retrieval runs before query planning. Above 0.75 intent confidence, it uses identified tables; otherwise vector retrieval supplies fallback candidates. Unique shortest verified join paths add intermediate tables within `TOP_TABLES`; ambiguous paths are not guessed. The planner receives only retrieved table schemas, their verified relationships, and the retrieval glossary. Plans referencing tables outside that context fail explicitly. Intent receives only allowed table names and descriptions. SQL generation uses the same retrieved schemas.

## Universal entity/value resolution

Database questions now pass through a deterministic value-resolution stage before query planning. It is **table-agnostic**: it searches policy-approved searchable columns across the complete configured catalog, rather than hard-coding names such as `guards.first_name`. Exact matches are preferred, followed by prefix/contains matching. Candidate values are ranked using the requested target tables and the verified relationship graph. If multiple materially plausible records remain, the assistant asks for clarification instead of guessing.

Resolved evidence (`resolved_table`, `resolved_column`, `matched_value`, match type and confidence) is carried into the query plan and SQL-generation prompt. Protected columns remain excluded by the existing security policy. See [universal entity resolution](backend/docs/ENTITY_RESOLUTION.md).

Configuration: `ENABLE_ENTITY_RESOLUTION`, `ENTITY_RESOLUTION_COLUMNS_LIMIT`, and `ENTITY_RESOLUTION_MATCHES_PER_COLUMN`.

## Tests

```powershell
python -m pytest -q
```

Tests cover the existing pipeline, FastHTML markup, local asset serving, response statuses, and input validation with external services stubbed where appropriate. Browser interaction logic also has dependency-free Node tests (Node is needed only to run these tests):

```powershell
node --test tests/sentinel_client.test.mjs
```

These tests use a DOM stub; they do not replace visual browser verification. Live end-to-end model and database verification is separate:

```powershell
python -m backend.scripts.evaluate
```

Generated queries return at most 20 rows, enforced by SQL validation and result fetching. Smaller requested limits are preserved; counts and aggregates still use all matching records. `DEFAULT_ROW_LIMIT` and `MAX_ROW_LIMIT` can lower this cap but cannot raise it above 20.

Partial clarification replies are merged by the existing intent call. Pending context keeps the original request, established details, unresolved questions and up to four clarification exchanges. Set `BUSINESS_TIMEZONE` to your business IANA timezone to resolve relative dates; otherwise the assistant asks when the date/timezone matters.
