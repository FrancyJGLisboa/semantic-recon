# Operating Principles, Claim + Evidence Standards, Completion

<!-- Generated from references/full-pack.txt (pack v2.3) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
13. OPERATING PRINCIPLES
======================================================================

LLM / AGENT RESPONSIBILITY
- user intent
- natural-language interpretation
- hypothesis formation
- choosing among semantically valid alternatives
- explanation
- anomaly investigation
- ambiguity detection
- escalation when policy is missing

DETERMINISTIC CODE RESPONSIBILITY
- access and authentication plumbing
- pagination, retry, rate limiting
- normalization and unit conversion
- joins, deduplication, revision handling
- aggregation and metric calculation
- validation and REFUSAL
- provenance tracking
- contract enforcement
- freshness and drift detection

SEMANTIC CONTRACT RESPONSIBILITY
- meaning, grain, relationships
- authority and temporal semantics
- business rules, constraints, exclusions
- allowable and forbidden transformations
- known traps
- task-shaped playbooks
- unresolved questions

Governing principle:
Move every rule as far down this list as it can go.
Code that refuses beats prose that explains.
Prose that is read beats prose that is complete.


======================================================================
14. CLAIM CLASSIFICATION STANDARD
======================================================================

Status:

DISCOVERED   directly demonstrated from documentation, metadata, schema, data,
             or deterministic system behavior
INFERRED     strongly supported by evidence, not logically guaranteed
DECLARED     supplied by a human, policy owner, or authoritative governance source
UNRESOLVED   cannot be reliably determined from available evidence

Blast radius (NEW in v2.0, and the field that should drive your priorities):

SILENT_WRONG  a violation produces a plausible but incorrect result with no error.
              Highest priority for red-teaming and for a validator.
LOUD_FAIL     a violation raises an error or returns obvious garbage.
              Lower priority. The system already protects itself.
COSMETIC      a violation affects labels, formatting, or presentation only.

Structured form:

claim:
  contract_id:          which system this claim belongs to; never omit
  id:
  description:
  value:
  status:               DISCOVERED | INFERRED | DECLARED | UNRESOLVED
  confidence:
  blast_radius:         SILENT_WRONG | LOUD_FAIL | COSMETIC
  scope:
  source:
  evidence:
  counterevidence:
  exceptions:
  enforced_by:          the validator or test that makes this rule active
  falsification_attempted:  yes/no + what was tried
  verified_by:
  last_verified_at:
  max_age:              how long this claim may be trusted without re-verification

A claim with blast_radius SILENT_WRONG and enforced_by empty is a defect.
Either write the validator or downgrade the claim to UNRESOLVED.


======================================================================
15. EVIDENCE STANDARD
======================================================================

For every high-impact rule, preserve enough to reproduce the conclusion without
the original agent:

- the exact operation and parameters used
- environment, version, or dataset identifier
- timestamp
- sample size and rows/records examined
- the observed consistency rate, not a binary verdict
- every observed exception
- documentation reference where one exists
- the code path and test case that now encode it
- the falsification attempt that was performed
- confidence, status, blast_radius

Never replace evidence with a prose summary alone.
Never delete a counterexample after the rule is corrected. The counterexample is
the reason the rule is correct now, and it is the regression test.


======================================================================
16. COMPLETION CRITERIA
======================================================================

The run is complete only when:

- CONTRACT_ID was derived by the Target Profiler, collision-checked, frozen, and
  stamped in folder, files, namespace, and INDEX.md.
- TARGET.md is filled and scope was respected.
- Holdout questions were frozen before discovery.
- Access is verified, including failure paths.
- Structure is profiled with real sample sizes.
- Entities, grains, measures, and dimensions are mapped.
- Relationships are tested for fan-out.
- Temporal semantics are separated and probed for leakage.
- Business rules are classified, and unresolved ones are enforceable.
- Every SILENT_WRONG claim has been red-teamed and has an enforcer.
- Deterministic logic lives in code, with tests.
- validate_query() refuses all eight refusal classes, proven by tests.
- TRAPS.md exists, ordered by blast radius, each trap regression-tested.
- PLAYBOOKS.md covers every category A and B holdout question.
- AGENT_INSTRUCTIONS.md is self-sufficient, routed, and within its size cap.
- contract_health.py reports freshness and drift.
- Provenance is preserved end to end.
- A clean-room audit against the frozen holdout set has been performed.
- Final status is PASS or PASS_WITH_UNRESOLVED_ITEMS.

Final sanity check, to be answered honestly by the Orchestrator:

  If a future agent reads only AGENT_INSTRUCTIONS.md, calls only the code, and
  ignores every other file, does it still get correct results and correct
  refusals?

  If no, the contract is documentation. It is not a contract.
```
