# Type-Specific Probes + Output Structure

<!-- Generated from references/full-pack.txt (pack v2.2) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
0.2 TYPE-SPECIFIC MANDATORY PROBES
----------------------------------------------------------------------

DATA_API
- pagination, rate limits, error taxonomy, partial results, filter syntax
- whether metadata endpoints exist and whether they agree with live responses

DATABASE
- information_schema / catalog dump, actual constraints vs declared constraints
- row counts and cardinality per table, indexes, what a full scan costs
- soft-delete columns, tenancy columns, and whether every query MUST filter them
- which views are materialized and how stale they are

MCP_SERVER
- full tools/list, resources/list, prompts/list with complete JSON schemas
- for EVERY tool: is it read-only or does it mutate? is it idempotent?
- what the tool returns on empty result vs error vs partial
- argument coercion behavior: what does it do with a wrong type or extra field
- whether tool results are truncated, and at what size
- ordering/statefulness: does tool B require tool A to have run first

CODEBASE
- entrypoints, build, test, and run commands, each actually executed once
- the public surface vs the internal surface, and how the boundary is enforced
- invariants asserted in tests (tests are the executable spec — read them first)
- what breaks silently vs loudly when a rule is violated
- the 5 files a new contributor must read, and why


======================================================================
0.3 TARGET OUTPUT STRUCTURE
======================================================================

data_contract_<CONTRACT_ID>/      e.g. data_contract_usda_quickstats/
├── TARGET.md                     <- section 0 block, filled; CONTRACT_ID first
├── .contract_id                  <- one line, the slug; machine-readable anchor
├── README.md
├── AGENT_INSTRUCTIONS.md         <- the ONE file a downstream agent must read
├── PLAYBOOKS.md                  <- NEW: task-shaped recipes
├── TRAPS.md                      <- NEW: wrong answers with the wrong value shown
├── ACCESS.md
├── SOURCES.md
├── ENTITIES.md
├── METRICS.md
├── DIMENSIONS.md
├── RELATIONSHIPS.md
├── TEMPORAL_SEMANTICS.md
├── BUSINESS_RULES.md
├── AUTHORITY_POLICY.md
├── UNCERTAINTIES.md
├── CHANGELOG.md
├── examples/
│   ├── example_queries.md
│   └── example_responses.md
├── code/
│   ├── client.py
│   ├── queries.py
│   ├── validators.py             <- validate_query() lives here; it is a GATE
│   ├── normalization.py
│   └── contract_health.py        <- NEW: staleness + smoke test
├── tests/
│   ├── test_access.py
│   ├── test_schema.py
│   ├── test_metrics.py
│   ├── test_relationships.py
│   ├── test_temporal_semantics.py
│   ├── test_business_rules.py
│   ├── test_traps.py             <- NEW: each trap is a regression test
│   └── test_validators.py        <- NEW: the gate must itself be tested
└── evidence/
    ├── holdout_questions.md      <- NEW: frozen BEFORE discovery
    ├── observations.jsonl
    ├── schema_profile.json
    ├── key_candidates.yaml
    ├── hypotheses.yaml
    ├── counterexamples.yaml
    └── provenance.yaml
```
