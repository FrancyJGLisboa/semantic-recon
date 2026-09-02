# Scope

The shortest document here on purpose. A scope statement that rambles has
already failed.

## The one sentence

**It maps how one external system actually behaves, and compiles what it found
into refusals that fire in code.**

## The term is already taken, and means the opposite

In most of the industry a *data contract* is a **producer-side agreement**: the
team publishing the data commits to a schema, and the commitment is enforced
when they write.

This is the **consumer-side inverse**. Nobody agreed to anything. The producer
may not know you exist. What you get is a reconstruction, built by probing,
of how the system behaves — and refusals that protect you from the parts of
that behaviour nobody wrote down.

If you have a real producer-side contract, use it. This is for everything else,
which is most things.

## In scope

| | |
|---|---|
| One external system's observed semantics | what it returns, not what its docs promise |
| The gap between the two | where documentation and behaviour disagree |
| Refusals in code | the operations that are silently wrong, made to fail |
| Evidence | the counterexample and the numbers behind every rule |
| What nobody can answer | unresolved items, escalated rather than guessed |
| Routing between contracts | once you hold more than one |

## Out of scope, and these are the ones people assume

**Not data quality.** It found a 100× parse error in a real pipeline, and it
found it by comparing two columns the publisher had already provided. It does
not profile for anomalies, does not do statistical QA, does not monitor. Had
that pipeline stored only the parsed number, it would have found nothing.

**Not a data catalog.** No lineage, no org-wide discovery, no search. The
registry is a routing table with a handful of rows.

**Not ETL.** It does not move, transform, or store data. It describes how to
read someone else's.

**Not monitoring.** `contract_health` is a smoke test you run before trusting a
contract. There is no alerting, no history, no dashboard.

**Not a schema registry.** No versioned schemas, no compatibility checking, no
enforcement at write time. It has no authority over the producer.

**Not testing your code.** It tests your understanding of somebody else's data,
which is a layer most projects have no tests for at all.

**Not your business logic.** It describes an external system's semantics and
should stay out of what you do with them.

**Not a replacement for reading the docs.** It is what remains after them.

## Where a single contract stops

- **Observed behaviour, dated.** Every claim is tied to when and how it was
  observed. Behaviour changes; the contract says when it was last true.
- **Within a call budget.** Coverage is bounded by what the operator paid for,
  and `OUT_OF_SCOPE` in every `TARGET.md` says what was deliberately not mapped.
- **Unresolved stays unresolved.** Questions only a human or the vendor can
  answer are enforced as refusals, not resolved by inference. A contract with
  open items is correct and conservative, and that is the intended state.

## The pieces, and what each is for

| piece | scope |
|---|---|
| the pack | the method — eleven gated phases |
| the skill | the method, executable, in three CLIs |
| a contract | one system |
| the registry | which contract answers, when you have several |
| the ledger | whether the refusals are changing anything |

## What has actually been exercised

Five contracts across two of the five target types: three `DATA_API`, two
`DATA_FILE`. `DATABASE`, `MCP_SERVER` and `CODEBASE` have vocabularies and
probe lists and have never touched a real system.

Loading is confirmed in Claude Code only.

Nothing here has been used by anyone but its author.
