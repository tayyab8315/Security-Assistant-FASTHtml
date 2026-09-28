# Source database interpretation

The uploaded `s_demo_DB.zip` contains a PDF export of database `s_demo` with seven tables:

| Table | AI-queryable? | Reason |
|---|---:|---|
| `customers` | Yes | Business/customer data |
| `guards` | Yes | Business/guard data |
| `sites` | Yes | Business/site data |
| `users` | Yes, restricted | Business/application users; `password` is blocked |
| `conversations` | No | Explicitly excluded conversation data |
| `threads` | No | Explicitly excluded conversation metadata |
| `auth_sessions` | No | Authentication/session token infrastructure |

The source PDF is a **data dump**, not full DDL. Therefore this project does not invent data types or foreign-key joins from sample values. At setup time, `python -m scripts.index_schema` uses SQLAlchemy inspection against the real database to retrieve exact columns, types and declared foreign keys, then indexes only the allowlisted schema.

## Default sensitive-column policy

- `users.password` - blocked
- `guards.guard_passport` - blocked
- `guards.license_number` - blocked
- all columns of excluded tables - inaccessible

Adjust `domain/security_policy.json` only after a deliberate security review.
