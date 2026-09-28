> The web layer is now FastHTML. Start the single app from the project root with `python main.py`; see [the root README](../README.md) for current setup and routes. This document describes the preserved query pipeline.

# s_demo Text-to-SQL - Google Cloud article approach

This project implements a guarded natural-language -> SQL -> database result -> natural-language pipeline for the supplied `s_demo` database export.

## Queryable database scope

The new SQL export contains 43 tables; 39 operational tables are configured for querying.
See [schema expansion](docs/SCHEMA_EXPANSION.md) for the full scope and update workflow.
The following original table rules remain:

- `auth_sessions` - excluded (authentication/session infrastructure and token material)
- `conversations` - excluded by requirement
- `threads` - excluded by requirement
- `customers` - included
- `guards` - included
- `sites` - included
- `users` - included, but `password` is blocked

Sensitive guard identity-document columns (`guard_passport`, `license_number`) are also blocked from model-generated output by default.

The new `client_ai_conversations`, `finance_integrations`, and `roles` tables are excluded.
Banking/tax details, emergency contacts, private HR narratives and protected document
metadata are also blocked by `domain/security_policy.json`.

> The fallback catalog uses CREATE TABLE definitions plus owner-confirmed `business_schema` relationships. The dump declares no foreign keys; the 39 policy-permitted business joins work without database constraints. `scripts/index_schema.py` introspects the live schema and indexes permitted relationships. Unlisted ID-like names are not treated as verified joins. `users.role_type` remains numeric and named-role filters require a confirmed mapping.

## Architecture

The workflow includes a universal deterministic entity/value resolver between intent understanding and query planning. This resolves real database values across all policy-approved tables and uses the verified relationship graph to disambiguate candidates before SQL generation. See [ENTITY_RESOLUTION.md](docs/ENTITY_RESOLUTION.md).

The flow follows the techniques described in Google's "Getting AI to write good SQL: Text-to-SQL techniques explained":

```text
User question
   |
   v
Multi-stage semantic retrieval
   |-- table vectors
   |-- column vectors constrained by table hits
   |-- similar validated SQL examples
   |-- safe categorical value sampling (optional)
   v
Intent + ambiguity / answerability gate
   |---- clarification required --> ask user
   |---- out of scope -----------> stop
   v
Structured SQL plan
   v
Self-consistency SQL generation (N candidates)
   v
Deterministic AST/security validation (sqlglot)
   v
Database EXPLAIN dry-run
   |---- failure --> error-guided SQL repair --> validate again
   v
Consensus candidate selection
   v
Read-only execution
   v
Grounded result-to-text answer
```

Article techniques represented here:

- **Business-specific context**: semantic schema catalog + business glossary.
- **Intelligent retrieval/ranking**: separate table and column vector indexes using Ollama embeddings + Chroma.
- **In-context learning**: retrieves similar validated SQL examples.
- **Data linking/sampling**: optional distinct-value sampling for a strict safe-column whitelist.
- **Semantic layer**: `domain/business_glossary.json` maps ordinary terms to schema concepts and records ambiguities.
- **Intent disambiguation**: the LLM must ask a follow-up instead of guessing when semantics are missing.
- **Dialect awareness**: `SQL_DIALECT` is passed to generation and sqlglot parsing.
- **Validation and reprompting**: AST policy checks plus database `EXPLAIN`; exact errors are used for repair.
- **Self-consistency**: multiple candidates are generated and normalized; matching valid SQL gets consensus preference.
- **Evaluation**: `eval/cases.json` and `scripts/evaluate.py` provide a starting regression suite.

## Technology

- Python 3.11+
- FastHTML
- LangGraph
- Ollama
- `qwen2.5-coder:7b` by default for planning/SQL/answering
- `nomic-embed-text` for embeddings
- ChromaDB for local vector search
- SQLAlchemy for DB connectivity/introspection
- sqlglot for deterministic SQL parsing and safety validation
- MySQL default because the supplied export was produced by phpMyAdmin; PostgreSQL is also supported by changing the URL/dialect and driver.

## 1. Create a read-only database user

Do **not** point an LLM-driven query service at a privileged database account. Create an account that can only `SELECT` the allowed business tables.

For MySQL, adapt this example to your environment:

```sql
CREATE USER 'text2sql_ro'@'%' IDENTIFIED BY 'change-me';
GRANT SELECT ON s_demo.customers TO 'text2sql_ro'@'%';
GRANT SELECT ON s_demo.guards TO 'text2sql_ro'@'%';
GRANT SELECT ON s_demo.sites TO 'text2sql_ro'@'%';
GRANT SELECT ON s_demo.users TO 'text2sql_ro'@'%';
FLUSH PRIVILEGES;
```

The app blocks `users.password` in its AST validator, but DB least privilege remains the primary control. For stronger protection, expose database views that omit sensitive columns and grant the service account access only to those views.

## 2. Install Ollama models

```bash
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

For a lower-resource machine, set `OLLAMA_LLM_MODEL` in `.env` to a smaller instruction/coder model you have installed. SQL accuracy should be evaluated before production use.

## 3. Install the project

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env     # Windows
# cp .env.example .env     # Linux/macOS
```

Edit `.env`:

```env
DATABASE_URL=mysql+pymysql://text2sql_ro:change-me@127.0.0.1:3306/s_demo
SQL_DIALECT=mysql
```

For PostgreSQL, for example:

```env
DATABASE_URL=postgresql+psycopg://text2sql_ro:change-me@127.0.0.1:5432/s_demo
SQL_DIALECT=postgres
```

## 4. Inspect and index the live schema

```bash
python -m backend.scripts.inspect_schema
python -m backend.scripts.index_schema
```

The indexing step embeds only the allowlisted tables/columns. `conversations`, `threads`, `auth_sessions`, `users.password`, `guards.guard_passport`, and `guards.license_number` are excluded/blocked by policy.

## 5. Run the API

```bash
python main.py  # from the project root
```

Open the assistant at `http://127.0.0.1:8000/chat`.

Example request:

```json
POST /ask
{
  "question": "How many guards are in the system?"
}
```

Typical response shape:

```json
{
  "status": "ok",
  "answer": "There are 3 guards in the system.",
  "sql": "SELECT COUNT(*) AS guard_count FROM guards LIMIT 100",
  "columns": ["guard_count"],
  "rows": [{"guard_count": 3}],
  "retrieved_tables": ["guards"]
}
```

A question such as `Show active guards` is intentionally expected to trigger clarification until your business glossary defines what value of `guards.status` means active. This avoids learning business semantics from accidental sample values.

## 6. Evaluation

Run deterministic unit tests:

```bash
pytest -q
```

Run end-to-end evaluation after Ollama and the database are available:

```bash
python -m backend.scripts.evaluate
```

Add production questions to `eval/cases.json`. Track at minimum:

- table retrieval recall
- column retrieval recall
- clarification accuracy
- SQL parse/guard pass rate
- EXPLAIN pass rate
- execution accuracy
- result correctness
- sensitive-data violations (target: zero)
- average LLM calls/latency

## LLM-call behavior

For an ordinary successful request with the defaults:

1. One intent/disambiguation call
2. One planning call
3. Three SQL candidate calls (`SQL_CANDIDATES=3`)
4. Optional repair calls only if all candidates fail validation/dry-run
5. One final result-to-text call

Embedding calls are model inference but are not generative LLM chat calls. Retrieval, sqlglot validation, EXPLAIN and execution are deterministic/non-generative stages.

To reduce latency, set `SQL_CANDIDATES=1`. To maximize reliability, keep 2-3 candidates and measure the trade-off on your own evaluation set.

## Important production hardening

1. Use a **read-only DB user** and preferably safe database views.
2. Keep blocked tables/columns enforced in both DB privileges and `domain/security_policy.json`.
3. Confirm the exact live schema; the uploaded PDF is not DDL.
4. Define business semantics such as status values explicitly in `business_glossary.json` instead of letting the model infer them.
5. Add verified join/business rules when your real schema contains assignment/relationship tables.
6. Put API authentication/rate limits in front of `/ask` before deployment.
7. Log prompt/SQL/validation outcomes without logging passwords, tokens or restricted PII.
8. Continuously run the evaluation suite whenever the model, prompt, schema or business rules change.
