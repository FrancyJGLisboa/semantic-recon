# Changelog

## 2.5
- Section 12b.2: the registry's other job is proving that NO contract can answer
  a question, with reasons — something no single contract can do, because a
  contract only knows itself.
- `subject` is required on every contract row and every question, and gates
  candidacy before capability. Inferring it is the same mistake as inferring a
  preference.
- The capability table's first column is `subject`, and inapplicable cells are
  written "n/a" with a reason rather than left blank, because a blank reads as
  "no".
- `REGISTRY-G1` now requires tests for a subject-less question and for a
  question nothing can answer.
- Found by registering a third contract on a different domain. While every
  contract shared a subject the arbiter only appeared to work; the gap surfaced
  as failing tests, which is the good case only because the tests existed.
  **Two contracts in one domain do not test a registry.**

## 2.4
- Section 12b, the registry layer: what appears once two contracts describe
  overlapping facts, and why neither of them can produce it. Capability decides
  where capability can decide; an undeclared preference is escalated, never
  guessed, because a guessed preference is indistinguishable from a policy.
- Comparison preserves per-contract provenance; merging takes no override at
  all — a deliberate asymmetry with the named overrides of section 8.1.
- `REGISTRY-G1`. Hooks into the Target Profiler's collision check (subject
  overlap is not a slug collision) and the downstream bootstrap (consult the
  arbiter before loading a contract).
- Found by running the pack a second time, on a system chosen because it
  overlapped the first. The two agreed within 0.2 C and hid different halves of
  the provenance.

## 2.3
- Section 8.3 gains class (f), human-facing output. A gate can force a caller to
  pass a model and still not force it to say which one answered; every rule
  enforced in the data structure evaporates when a number is rendered into prose
  without its origin. The contract must own that rendering and ship no formatter
  that can omit provenance.
- `ENFORCEMENT-G1` now requires a test enumerating the public formatters.
- Found the same way as 2.2: a skill built on a finished contract inherited
  every refusal correctly, then printed `22.2 °C` with no source attached.

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
