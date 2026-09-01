# The Registry Layer (multiple contracts)

<!-- Generated from references/full-pack.txt (pack v2.6) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
12b. THE REGISTRY LAYER  (only once you hold more than one contract)
======================================================================

Everything before this section produces ONE contract. This section is about
what appears the moment two of them describe overlapping facts, and it is not
producible by either contract, because the question it answers is above both.

Do not build this speculatively. It is worth writing once the registry holds a
second contract — whether or not it overlaps the first. Overlap is the obvious
reason; 12b.2 is the one that is easy to miss.

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
12b.2 THE OTHER REASON: PROVING THAT NOTHING CAN ANSWER
----------------------------------------------------------------------

Overlap is the obvious reason for this layer. The opposite case is the one that
gets missed, and it only appears once a contract joins on a different subject.

When registered contracts cover different domains, the arbiter's job is not to
choose between them. It is to state, WITH REASONS, that none of them can answer
the question:

  "when was the March 2019 forecast run?"
    -> REFUSED. Contract A exposes no run time; contract B has no history.

That is more useful than the closest available answer, and no single contract
can say it, because a contract only knows itself. Proving a question is
unanswerable is a service the registry provides and the contracts cannot.

SUBJECT IS REQUIRED, NOT OPTIONAL

This needs a `subject` on every contract row, not only on colliding ones, and
it needs every question to name one. A date alone does not say what is being
asked about: "1 March 2019" is a weather question or an agricultural question
depending on something the arbiter cannot see.

Gate on subject BEFORE capability. A contract excluded for covering the wrong
domain produces a clearer refusal than one excluded for lacking a field, and
the exclusion is certain rather than a judgement.

Refuse a question that names no subject. Inferring it from the wording is the
same mistake as inferring a preference (12b.3): the inference will be inherited,
cited, and defended by agents with no idea nobody made it.

TWO CONTRACTS IN ONE DOMAIN DO NOT TEST A REGISTRY

While every registered contract shares a subject, every question is implicitly
about that subject. `subject` looks optional. The arbiter appears to work. It is
not until a contract arrives from another domain that the gap shows — and it
shows up as failing tests rather than as a wrong answer, which is the good case
only because somebody wrote the tests first.

So add the subject field while you still have two contracts, before you can
demonstrate you need it. By the time you can demonstrate it, agents are already
relying on the arbiter.

----------------------------------------------------------------------
12b.3 THE RULE
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
12b.4 THE CAPABILITY TABLE
----------------------------------------------------------------------

One row per contract. The FIRST column is `subject`, because it decides
candidacy before any capability does. Then one column per thing that decides
who can answer: coverage in time, horizon, which provenance fields exist, which
dimensions can be pinned, unit vocabulary.

Where a column does not apply to a contract, write "n/a" and why, not a blank.
A blank reads as "no" and will exclude that contract from questions it could
have answered.

Every cell MUST cite the claim id in that contract which established it. A
capability table assembled from impressions is a preference table in disguise.

Write the "no" cells with the same care as the "yes" cells. They are what
produces a CAPABILITY ruling, and a ruling that names why the other contracts
cannot answer is auditable in a way that "we chose X" never is.

----------------------------------------------------------------------
12b.5 COMPARE IS ALLOWED. MERGE IS NOT.
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
12b.6 HOOKS INTO THE REST OF THE PACK
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
- Every contract row carries a `subject`, and routing gates on it before
  capability.
- A question naming no subject is refused, proven by a test.
- A question no registered contract can answer produces a refusal that names
  why each one was excluded, proven by a test.
- Every capability cell cites the claim that established it.
- The preference table is empty, or every row in it names who decided and when.
- A test asserts the preference table cannot be populated by inference.
- Comparison preserves per-contract provenance and cannot reduce to one value.
- The merge path takes no override, proven by a test that passes every override
  the contracts themselves accept.
- A question that NO contract can answer produces a refusal that says so,
  rather than the closest available answer.
```
