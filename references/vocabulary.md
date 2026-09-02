# Target Profile + Vocabulary Mapping

<!-- Generated from references/full-pack.txt (pack v2.8) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
0. TARGET PROFILE  (FILL THIS BEFORE ANY AGENT RUNS)
======================================================================

This pack is target-agnostic. Nothing downstream is valid until this block is
filled in and written to <CONTRACT_DIR>/TARGET.md.

CONTRACT_ID:            DERIVED BY THE TARGET PROFILER, not supplied by the
                        operator. See section 0.1a. Short stable slug,
                        lowercase, [a-z0-9_], e.g. usda_quickstats.
                        The operator may override, but should not have to.
CONTRACT_DIR:           data_contract_<CONTRACT_ID>
                        Every path in this pack written as <CONTRACT_DIR>/ resolves
                        to this. Never use a bare "data_contract/".
TARGET_NAME:            human-readable name
TARGET_TYPE:            one of DATA_API | DATABASE | MCP_SERVER | CODEBASE
                        | DATA_FILE  (one or more URLs serving a dataset directly)
TARGET_LOCATION:        base URL, DSN, server command, repo path
CREDENTIALS_AVAILABLE:  yes/no + how they are injected (never the values)
WRITE_ACCESS:           read-only | read-write | unknown
BLAST_RADIUS_OF_MISUSE: what happens if a future agent gets this wrong
CALL_BUDGET:            max requests/queries/tool-calls this run may spend
TIME_BUDGET:
PRIMARY_CONSUMERS:      which agents/workflows will use the contract
OUT_OF_SCOPE:           explicitly what this run will NOT map

If TARGET_TYPE is unknown or the target is a hybrid (e.g. an MCP server fronting
a database), declare a PRIMARY type and list SECONDARY types. Run the primary
vocabulary; annotate secondary findings.

----------------------------------------------------------------------
0.1 VOCABULARY MAPPING
----------------------------------------------------------------------

Every agent prompt below uses abstract terms. Bind them using this table
according to TARGET_TYPE. Where an example in this pack is domain-flavored,
substitute the equivalent from your target's column.

CONCEPT        | DATA_API                | DATABASE                    | MCP_SERVER                      | CODEBASE                     | DATA_FILE
---------------+-------------------------+-----------------------------+---------------------------------+------------------------------
ACCESS         | auth scheme, base URL,  | DSN, driver, roles, grants, | transport, handshake, protocol  | build, install, entrypoints, | URL, content-type vs actual content, redirects, whether an error is loud
               | endpoints               | schemas, search_path        | version, capability negotiation | env config, run modes
ENTITY         | resource / dataset      | table / view / mat. view    | tool / resource / prompt        | module / service / domain object | the dataset the file holds
FIELD          | response field, param   | column                      | input+output schema property    | struct field, function param | a column - but the header may be compound, padded, or not on row 1
MEASURE        | metric / measure        | aggregate over a column     | what the tool RETURNS and means | computed value, emitted metric | a cell, which may carry a flag glued to the number
GRAIN          | one record = what?      | primary key grain           | one call = what unit of work?   | one invocation = what effect? | what one row is; often a compound key packed into one column
RELATIONSHIP   | join key, expansion     | FK, junction table          | tool chaining / composition     | call graph, import graph, DI | joins to code lists that live in another file entirely
CARDINALITY    | 1:1 / 1:N / N:M         | FK cardinality, fan-out     | N calls needed per outcome      | fan-out of a call | rows x period columns; wide vs long changes what a row means
TEMPORAL       | observation vs          | valid_time vs transaction   | statefulness, session scope,    | migrations, API versioning, | period as columns or as a row; breaks in series
               | publication vs revision | time, as_of, soft deletes   | cache TTL, idempotency window   | eventual consistency
AUTHORITY      | source precedence       | source of truth vs replica  | which server owns which fact    | which module owns which write | which URL governs when a 'latest' and a dated one both exist
               |                         | vs materialized view        | when servers overlap            | path
BUSINESS RULE  | source selection,       | constraints, triggers,      | idempotency, side effects,      | invariants, feature flags, | flag semantics, missing markers, rounding, what may be compared
               | suppression, vintages   | soft delete, tenancy        | rate limits, confirmation reqs  | permissions, guard clauses
FORBIDDEN OP   | join that fans out,     | cross-db join, unbounded    | destructive tool without        | writing to the DB bypassing | comparing across a break flag; dropping flags; treating a marker as 0
               | mixed vintages          | scan, lock escalation       | confirmation, non-idempotent    | the service layer
REVISION       | vintages, restatements  | updated_at, history tables  | protocol/tool version drift     | migrations, deprecated APIs | can a version be pinned? immutable URL, change-detection only, or neither
DISCOVERY      | metadata / catalog      | information_schema,         | tools/list, resources/list,     | README, ADRs, tests, types, | code lists, data dictionary, the structural metadata beside the file
  SURFACE      | endpoints, OpenAPI      | pg_catalog, EXPLAIN         | prompts/list, server info       | schemas, CI config

----------------------------------------------------------------------
```
