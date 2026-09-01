# Contract Registry

Every contract produced by the Semantic Reconnaissance pack registers one row here.
A downstream agent reads this file FIRST to decide which contract to load.
A contract missing from this table is a contract agents will not find.

Status: IN_PROGRESS | PASS | PASS_WITH_UNRESOLVED_ITEMS | FAIL | STALE

| CONTRACT_ID | TARGET_TYPE | answers questions about | path | last_verified_at | status |
|-------------|-------------|-------------------------|------|------------------|--------|
| _(none yet)_ | | | | | |

## Rules

- CONTRACT_ID is derived by the Target Profiler (pack section 0.1a), never hand-picked.
- Before minting a new slug, the Profiler MUST read this file for collisions.
- A slug is frozen once written. Renames create a new row and leave the old one
  with an alias note; they never edit an existing CONTRACT_ID in place.
- Never load two contracts and let one contract's rules govern the other's data.
