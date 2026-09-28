# Expanded operational schema

The configuration now covers 39 of the 42 tables in the supplied `s_demo.sql`.
CREATE TABLE definitions and owner-confirmed business relationships were used; the dump was not executed or imported.
The existing four tables retain their configuration pattern and include their new columns.

## Scope

Enabled domains include scheduling, guard availability, attendance, timesheets,
patrols, incidents, hazards, emergency/welfare checks, compliance metadata, training,
HR employment metadata, payroll, contracts, customer/supplier invoices, purchasing,
rates, subcontractors, visitors, vehicles, form metadata and recorded business insights.

The new `client_ai_conversations`, `finance_integrations`, and `roles` tables are
excluded, along with the previous conversation/session exclusions. Protected columns
include passwords, identity-document numbers, banking/tax details, emergency contacts,
private request/review narratives, compliance notes, document/media names and URLs,
visitor pass numbers and form-definition JSON. `security_policy.json` is authoritative.
SQL validation enforces these blocks through aliases and subqueries as well as direct references.

Operational contacts, payroll amounts, location records and other allowed business
data remain queryable. Existing application authentication and access boundaries are unchanged.

## Known schema ambiguities

- The dump has no FOREIGN KEY declarations. The catalog records owner-confirmed
  business relationships after removing obsolete shift links. These are semantic
  join rules, not database constraints. Other relationships still require confirmation.
- `guard_availabilities` stores dated windows in nullable `start_at`/`end_at` DATETIME columns. Its unique `(guard_id, day_of_week)` key still permits only one row per guard/weekday; do not assume recurring weekly availability or unrestricted date history.
- `guard_requests`, `leave_requests`, and `shift_swap_requests` are separate sources.
  Their synchronization and deduplication rules are unknown.
- `shift_assignments` is the authoritative source of guard assignments.
  `shifts.guard_id` is obsolete and blocked. `shifts.site_id` remains the approved
  link to `sites.id`: guard -> shift_assignments -> shifts -> sites.
  Unassigned shifts have no matching `shift_assignments` row.
- `users.role_type` is INT in this dump. The old text-based admin-role example was
  removed. Named-role filters require a verified numeric mapping.
- Enum literals are documented from DDL. Defaults do not establish numeric status
  meanings, currencies, timezones, rating scales or accounting formulas.

## Business relationship verification

Each supplied relationship was checked against the SQL dump and live column metadata.
All endpoint types match and all parent keys are unique. `verified_by: business_schema`
records the owner's confirmation of meaning; metadata checks alone cannot prove business meaning.
The catalog uses child/reference -> parent/key direction. Unique child keys make
`guard_compliance.guard_id`, `welfare_checkins.guard_id`, and `attendance.shift_id`
one-to-one (at most one child per parent); other supplied edges are many-to-one.
Nullability and missing parent rows are still possible without foreign-key enforcement.

Customer-to-contract queries traverse `customers -> sites -> client_contracts`.
No direct customer-name join was added. `users.role_id -> roles.id` and
`client_ai_conversations.user_id -> users.user_id` are documented but excluded from
runtime prompts/index relationships because their endpoints are restricted.

Read-only integrity checks found 30 orphan references in `shift_assignments.guard_id`,
30 in `shifts.guard_id`, and 3 in `timesheets.shift_id` at verification time.
No rows were repaired. See [the timestamped verification report](relationship_verification.json)
for aggregate results, nullability and scope. Use LEFT JOIN when all base records must
be preserved, and do not treat missing parent data as a replacement identity.

The supplied list does not confirm every ID-like column. For example,
`timesheets.guard_id`,
`guard_requests.target_shift_id`, and shift-swap requester/target guard IDs still have
no approved join rule. Only `shift_assignments` is authoritative for guard assignments;
the historical verification report does not authorize obsolete shift columns.

## Updating tables in future

1. Update `domain/security_policy.json` to allow tables and protect sensitive fields.
2. Update `admin/schema_catalog.json` with descriptions and actual column names.
3. Add business meanings to `domain/business_glossary.json` and verified SQL examples
   to `admin/examples.json`. Do not derive business rules from guessed ID relationships.
4. Ensure the connected database actually contains the tables and the read-only account
   can inspect/query them. The catalog does not create tables or import a dump.
5. With the application stopped and the embedding service available, run from the root:

   ```powershell
   .\backend\.venv\Scripts\python.exe -m backend.scripts.index_schema
   .\backend\.venv\Scripts\python.exe main.py
   ```

6. Check the printed indexed table names. Live introspection excludes missing tables;
   if the database is unreachable the application uses the static fallback catalog.
7. Run `python -m pytest -q` and `node --test tests/sentinel_client.test.mjs`.
   The optional `python -m backend.scripts.evaluate` performs live model/database checks.

The Data Explorer and additional count prompts now derive from the configured table
list on page load. Future table additions do not need hardcoded JavaScript cards.
This is a configured scope display, not proof of live database availability.
Rebuild the index after schema changes and restart running workers to refresh cached
collection handles. The default index path is `backend/admin/admin_schemas` unless
`ADMIN_SCHEMAS_PATH` overrides it.
