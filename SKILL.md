---
name: semantic-recon
description: Run a multi-agent reconnaissance of a target system and compile a slug-scoped data_contract_<id>/ folder that makes future AI agents behave like an SME on it. Use when asked to map, learn, document, or build a contract for an API, MCP server, database, or codebase so other agents can use it correctly; when credentials for a system exist and its semantics must be discovered and verified; or on any invocation like /semantic-recon, "semantic orchestrator", "build a data contract", "make agents SME on this system", "refresh the contract". Enforces frozen holdout questions, blast-radius triage, adversarial falsification, and a validate_query gate that refuses rather than describes.
license: MIT
metadata:
  version: "2.2"
  pack: Semantic Reconnaissance Multi-Agent Prompt Pack
---

# Semantic Reconnaissance

Produce a verified, reusable contract that lets a future agent operate a target
system correctly without rediscovering it.

**The thesis.** A contract is not successful because it is complete. It is
successful because it changes the behavior of the agent that consults it.
Optimize for what an agent under context pressure actually reads and actually
runs, not for coverage of the artifact.

## When this applies

Target is one of: `DATA_API`, `DATABASE`, `MCP_SERVER`, `CODEBASE`.
The pack is target-agnostic; a vocabulary table binds its abstract terms to each.

Do not use this for a one-off query against a system. Use it when the same
system will be used repeatedly, by agents, and being silently wrong is expensive.

## Non-negotiables

1. **CONTRACT_ID is derived, never hand-picked.** The Target Profiler mints it
   from what the system calls itself, using deterministic normalization, so two
   runs on one system produce one slug. See `references/identity.md`.
2. **Holdout questions are frozen before discovery.** Otherwise the final audit
   grades itself. See `references/agents/02-holdout-author.md`.
3. **Triage by blast radius, not by confidence.** A high-confidence
   `SILENT_WRONG` claim is the most dangerous object in the contract; a
   `LOUD_FAIL` claim already protects itself.
4. **Code that refuses beats prose that explains.** If a downstream agent can
   produce a silently wrong result without any exception firing, that is a
   defect in the code layer, not a documentation gap. Attack the target AND
   your own code — a caller-asserted label, an opt-in validator, or a bare
   float handed back are all bypasses, and only the second pass finds them
   (section 8.3).
5. **Never persist, print, or document a credential.** Env injection only.
   Record the variable name in TARGET.md, never the value.
6. **Every artifact is stamped with CONTRACT_ID.** Agents quote content, not
   paths. An unattributed fragment is unusable, not probably-ours.

## Phases

Run in order. Each phase has its own gate; do not advance past a failed gate.
Read the reference file when you enter the phase, not before.

| # | Phase | Read | Gate |
|---|-------|------|------|
| 0 | Coordinate the whole run | `references/agents/00-orchestrator.md` | — |
| 1 | Derive the slug, fence the scope | `references/agents/01-target-profiler.md` | IDENTITY-G1 |
| 2 | Freeze the exam before studying | `references/agents/02-holdout-author.md` | HOLDOUT-G0 |
| 3 | How the system is reached | `references/agents/03-access-explorer.md` | ACCESS-G1 |
| 4 | Observable structure | `references/agents/04-schema-analyst.md` | SCHEMA-G1 |
| 5 | Meaning, grain, measures | `references/agents/05-semantic-analyst.md` | SEMANTICS-G1 |
| 6 | What is legitimate, not merely possible | `references/agents/06-business-analyst.md` | BUSINESS-G1 |
| 7 | Try to break every claim | `references/agents/07-red-team.md` | RELATIONSHIPS-G1, TEMPORAL-G1, TRAPS-G1, PROVENANCE-G1 |
| 8 | Compile rules into refusing code | `references/agents/08-implementation.md` | CODE-G1, ENFORCEMENT-G1 |
| 9 | Compile the operational contract | `references/agents/09-compiler.md` | PLAYBOOK-G1 |
| 10 | Clean-room audit vs frozen holdout | `references/agents/10-auditor.md` | FINAL-G1 |

Supporting references, read as needed:

- `references/vocabulary.md` — TARGET PROFILE block and the term-binding table
- `references/identity.md` — slug derivation and identity discipline
- `references/structure.md` — per-type mandatory probes, output folder layout
- `references/standards.md` — claim classification, blast radius, evidence rules
- `references/downstream.md` — bootstrap for consuming agents, refresh runs
- `references/full-pack.txt` — the entire pack in one file

## Start

1. Read `references/vocabulary.md` and fill the TARGET PROFILE block. Two fields
   are the operator's decision and must be asked if absent:
   `BLAST_RADIUS_OF_MISUSE` and `OUT_OF_SCOPE`. Everything else you determine.
2. Run phase 1 only. It costs at most 3 operations and returns a proposed slug
   with its derivation. Confirm before spending the call budget.
3. Proceed through the phases.

Contracts live in `~/contracts/<CONTRACT_DIR>/`, registered in
`~/contracts/INDEX.md`. Create the registry from `templates/INDEX.md` if absent.

## Refresh

An existing contract is refreshed, never re-derived. Read `.contract_id` first,
then follow the refresh procedure in `references/downstream.md`. A refresh that
mints a new slug forks the contract and downstream agents load whichever they
find first.

## Consuming a finished contract

Paste the bootstrap block from `references/downstream.md` into any agent that
will use the system. Its first instruction is to check `~/contracts/INDEX.md`
and load exactly one contract.
