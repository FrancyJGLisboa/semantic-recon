# Changelog

## 2.2
- Section 8.3: the enforcement compliance pass runs twice — against the target
  system, and against the contract's own code. Names five recurring bypass
  classes: caller-asserted labels, opt-in validators, provenance-losing
  returns, injected environment, and constants measured once.
- `ENFORCEMENT-G1` now fails on an empty pass-2 enumeration, and forbids any
  "no further bypass exists" claim unless both passes are documented.
- Found by running the pack against a live API: three attempts against the
  target's surface passed the gate while four bypasses through the contract's
  own code were still open.
- Normalization now strips trailing TLDs, so a system named after its domain
  does not fork the slug (`Open-Meteo.com` -> `open_meteo`, not `open_meteo_com`).

## 2.1
- `CONTRACT_ID` is derived by the Target Profiler, not supplied by the operator.
  Deterministic normalization means the same system always yields the same slug.
- New Target Profiler phase (previously a role with no prompt). Runs first,
  costs at most 3 operations, blocks the run until identity and scope are fixed.
- Contract folders are slug-scoped (`data_contract_<id>/`). Identity is carried
  in the folder name, the Python package, every file header, and a central
  registry, so a fragment quoted out of context still names its system.
- Eighth refusal class in `validate_query()`: `ForeignContractData`, the
  cross-system guard.
- `IDENTITY-G1` gate; the auditor must reproduce the slug from its derivation
  record.
- Packaged as a portable skill for Claude Code, Codex CLI, and Copilot CLI.
  Split into per-phase reference files so only the router loads every invocation.

## 2.0
- `TARGET PROFILE` block and vocabulary mapping. The pack adapts to
  `DATA_API` / `DATABASE` / `MCP_SERVER` / `CODEBASE` instead of assuming a
  data API.
- Holdout Question Author. Evaluation questions frozen before discovery so the
  final auditor cannot grade itself.
- `validate_query()` promoted from helper to hard enforcement gate.
- New artifacts: `PLAYBOOKS.md`, `TRAPS.md`, `CHANGELOG.md`,
  `contract_health.py`.
- `AGENT_INSTRUCTIONS.md` made self-sufficient, with a routing table and a size
  cap, on the assumption it is the only file read.
- `blast_radius` on every claim, driving red-team priority.
- Downstream agents must check freshness and drift before trusting a contract.

## 1.0
- Initial eight-role pack for credentialed data APIs.
