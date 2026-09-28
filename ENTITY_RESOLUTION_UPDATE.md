# Entity Resolution Update

This distribution adds a universal, table-agnostic database value resolver.

Main changes:
- `backend/app/entity_resolver.py` — generic value resolution across policy-approved tables.
- `backend/app/database.py` — parameterized exact/prefix/contains value lookup.
- `backend/app/graph.py` — resolver inserted between intent and database planning; ambiguity routes to clarification.
- `backend/app/models.py` — resolved entity evidence carried in `QueryPlan`.
- `backend/app/nodes/plan.py` — planner receives deterministic resolution evidence.
- `backend/admin/prompts.json` — planner/SQL generator instructed to preserve resolved evidence.
- `backend/app/config.py` — resolver feature flags and bounds.
- `backend/tests/test_entity_resolution.py` — resolver and security regression tests.
- `backend/docs/ENTITY_RESOLUTION.md` — design and security documentation.
- `database/s_demo.sql` — supplied database dump included for reference.

Secrets and local virtual environments are intentionally excluded from this distribution. Copy `backend/.env.example` to `backend/.env` and configure the database/model credentials locally.
