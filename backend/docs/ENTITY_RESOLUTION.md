# Universal Entity / Value Resolution

The database workflow now contains a deterministic entity-resolution stage between intent understanding and query planning.

## Flow

```text
User question
    |
    v
Intent + task understanding (LLM)
    |
    v
Universal entity/value resolver (deterministic)
    |
    +--> resolved entity evidence
    |
    +--> ambiguous -> clarification
    |
    v
Query planner (LLM)
    |
    v
Schema retrieval -> SQL generation -> validation -> execute -> answer
```

## What it does

- Searches policy-approved, searchable columns across the whole catalog rather than hard-coding a table such as `guards`.
- Uses exact matching first, then prefix/contains matching.
- Classifies columns from table/column/description/type metadata into generic semantic types such as `person_name`, `site_name`, `customer_name`, `identifier`, `status`, `email` and `phone`.
- Uses the verified relationship graph and the intent's target tables to rank candidates.
- Treats multiple materially plausible entity records as ambiguous and asks the user to clarify instead of guessing.
- Never searches blocked columns or blocked tables.
- Sends the resolved table, column and matched value to the planner and SQL generator as deterministic evidence.

## Security model

The resolver is downstream of the existing security projection in `live_or_static_catalog()` and `security_policy.json`. It therefore cannot reintroduce protected columns such as passwords, tokens, passport/license fields, bank details or other blocked fields.

## Performance

`ENTITY_RESOLUTION_COLUMNS_LIMIT` bounds the number of searchable columns considered per request. `ENTITY_RESOLUTION_MATCHES_PER_COLUMN` bounds matches returned from each column. Exact matching is attempted before broader matching so common identifier/name lookups usually finish in one database pass.

For large production databases, this component can later be backed by a dedicated normalized value index without changing its public state contract.
