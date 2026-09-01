# Downstream Bootstrap + Contract Refresh

<!-- Generated from references/full-pack.txt (pack v2.4) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
11. DOWNSTREAM PRODUCTION AGENT BOOTSTRAP PROMPT
======================================================================

Paste this into any agent that will use the target system.

Before querying this system:

0.  Confirm which contract you need. If the registry has an arbiter (section
    12b), ASK IT — do not read the index and choose. Picking by hand is the
    failure that layer exists to prevent, and the arbiter will refuse rather
    than guess when the choice is a preference nobody declared. Load exactly
    one contract. If your task spans systems, load each separately and never
    let a rule from one govern the other. A fragment with no CONTRACT header is
    unattributed: do not act on it.
1.  Run <CONTRACT_DIR>/code/contract_health.report(). If it returns EXPIRED or
    DRIFT_DETECTED, state that before answering and do not present results as
    verified.
2.  Read <CONTRACT_DIR>/AGENT_INSTRUCTIONS.md. Use its routing table.
3.  If your task matches a playbook in PLAYBOOKS.md, follow that playbook.
4.  Call functions under <CONTRACT_DIR>/code/. Do not reach the target directly.
5.  Do not reimplement any deterministic operation the code already provides.
6.  Route every request through validate_query().
7.  If a validator refuses, do not bypass it. Report the refusal and its reason.
    Bypass only on an explicit user instruction, and state exactly what is being
    bypassed and what could go wrong.
8.  Before returning any number, check TRAPS.md for your operation shape.
9.  If your interpretation touches an item in UNCERTAINTIES.md, do not choose
    silently. Surface the ambiguity and ask.
10. Preserve provenance in every substantive answer: source, version, as-of time,
    and the claim status that governs it.
11. Never present an INFERRED rule as a guaranteed fact.
12. Never override a DECLARED policy with your own inference.
13. If the contract and the live system disagree, stop, report the discrepancy,
    and do not produce a confident answer.
14. Prefer explicit uncertainty or refusal over an unsupported assumption.
15. If you had to work around the contract to complete a task, record it. That is
    a contract defect and it feeds the next refresh.


======================================================================
12. RE-RUN / CONTRACT REFRESH PROMPT
======================================================================

You are running Semantic Contract Refresh.

Read .contract_id first. Do NOT re-derive the slug and do NOT let the Target
Profiler mint a new one. A refresh that forks the identity produces two partial
contracts for one system, and downstream agents will load whichever they find.

Detect whether access, structure, semantics, business rules, or the reference
implementation changed since the last verified contract.

1. Run contract_health.smoke_test() first. It is cheap and often sufficient to
   decide whether a full re-run is needed.
2. Re-run the reconnaissance agents whose domain the smoke test flagged.
3. Do NOT regenerate holdout_questions.md. Reuse the frozen set. Add new
   questions only for genuinely new capabilities, and mark them as added.
4. Produce a semantic diff.

Example:

  Contract v1.7 -> v1.8
  + new operation: get_regional_breakdown
  ~ unit metadata changed on measure M
  ~ pagination behavior changed on /records
  ! historical values for entity E were revised
  ! source-precedence rule requires policy review
  - deprecated: /legacy/records

Classify every change:

NON_BREAKING
POTENTIALLY_BREAKING
BREAKING
POLICY_REVIEW_REQUIRED

Do not overwrite the verified contract until:
- affected tests pass
- affected semantic rules are revalidated
- counterexamples are re-run
- the holdout set is re-answered at the previous score or better
- the Independent Final Auditor issues PASS or PASS_WITH_UNRESOLVED_ITEMS

Append to <CONTRACT_DIR>/CHANGELOG.md. Never rewrite history there.
Update last_verified_at on every claim you actually re-verified, and only those.
```
