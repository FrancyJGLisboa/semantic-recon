# The Registry Layer (multiple contracts)

<!-- Generated from references/full-pack.txt (pack v2.4) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
12b. THE REGISTRY LAYER  (only once you hold more than one contract)
======================================================================

Everything before this section produces ONE contract. This section is about
what appears the moment two of them describe overlapping facts, and it is not
producible by either contract, because the question it answers is above both.

Do not build this speculatively. It is worth writing when, and only when, two
registered contracts can answer the same question.

----------------------------------------------------------------------
12b.1 WHY NEITHER CONTRACT CAN DECIDE
----------------------------------------------------------------------

Two systems covering one domain will disclose different things. Not more or
less — DIFFERENT. One names the model and hides when it ran; the other names
the run and hides which cell answered. Each is complete on its own terms and
neither is complete for a merged series, which inherits the INTERSECTION of
what they disclose. That intersection is routinely empty.

So a merged value is not an average of two partial provenances. It is a value
with no provenance at all, wearing the confidence of two systems that agreed.

And they often do agree. That is the trap: agreement reads as permission to
mix, and it is the weakest possible evidence for it. Two systems can agree
because they share an upstream model, at one location, on one day, and diverge
elsewhere by an order of magnitude more than the agreement suggested.

----------------------------------------------------------------------
12b.2 THE RULE
----------------------------------------------------------------------

CAPABILITY DECIDES WHERE CAPABILITY CAN DECIDE. EVERYTHING ELSE ESCALATES.

  exactly one contract CAN answer   -> rule for it, and say why the others cannot
  several can, operator declared    -> rule for the declared one, list the rest
  several can, nobody declared      -> REFUSE. That decision is the operator's.
  none can                          -> REFUSE, and say so as a finding

The third row is the whole design. A registry that guesses a preference is
worse than one that refuses, because a guessed preference is indistinguishable
from a policy: it will be inherited, cited, and defended by agents that have no
idea a human never made it.

So the preference table SHIPS EMPTY, and a test asserts that it does. A row in
it must be a decision somebody made. Capability rows are derived from evidence;
preference rows are not derivable at all.

----------------------------------------------------------------------
12b.3 THE CAPABILITY TABLE
----------------------------------------------------------------------

One row per contract, one column per thing that decides who can answer:
coverage in time, horizon, which provenance fields exist, which dimensions can
be pinned, unit vocabulary.

Every cell MUST cite the claim id in that contract which established it. A
capability table assembled from impressions is a preference table in disguise.

Write the "no" cells with the same care as the "yes" cells. They are what
produces a CAPABILITY ruling, and a ruling that names why the other contracts
cannot answer is auditable in a way that "we chose X" never is.

----------------------------------------------------------------------
12b.4 COMPARE IS ALLOWED. MERGE IS NOT.
----------------------------------------------------------------------

Provide a comparison that returns every candidate side by side, each with its
own provenance and an explicit note of which half it is missing. It must not
reduce them to one number, and there should be no function that does.

Provide a merge function ONLY so that the attempt fails by name, and give it
NO OVERRIDE. Not the one your contracts use internally, not a force flag.

This is a deliberate asymmetry with section 8.1, where overrides are permitted
through explicit named arguments. Mixing sources INSIDE one contract is a
labelled choice that contract is competent to offer about material it owns.
Choosing between contracts is not a choice either of them may make, so there is
nothing for an override to unlock. An override here would be a contract
granting itself authority it does not have.

----------------------------------------------------------------------
12b.5 HOOKS INTO THE REST OF THE PACK
----------------------------------------------------------------------

TARGET PROFILER (section 1b)
  The collision check already compares slugs. Extend it: when a registered
  contract answers questions about the SAME SUBJECT, that is not a slug
  collision and must not be discriminated away — it is an authority overlap.
  Record it in TARGET.md and flag it for this layer.

DOWNSTREAM BOOTSTRAP (section 11)
  Step 0 becomes: consult the registry's arbiter BEFORE loading a contract. An
  agent that picks by reading the index and choosing is the failure this layer
  prevents.

THE CONTRACTS THEMSELVES
  Each keeps its foreign-data guard. The arbiter decides who answers; the
  guards ensure that nothing crosses even if the arbiter is bypassed. Two
  independent mechanisms, because the arbiter is advisory to code that does not
  call it and the guards are not.

REGISTRY-G1 passes only if:
- Every capability cell cites the claim that established it.
- The preference table is empty, or every row in it names who decided and when.
- A test asserts the preference table cannot be populated by inference.
- Comparison preserves per-contract provenance and cannot reduce to one value.
- The merge path takes no override, proven by a test that passes every override
  the contracts themselves accept.
- A question that NO contract can answer produces a refusal that says so,
  rather than the closest available answer.
```
