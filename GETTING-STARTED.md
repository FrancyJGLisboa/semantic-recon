# Getting started

Better conditions for building AI agents with expertise on a system: probe the
target by running it, compile what it does into refusals code enforces, and let
whatever you build on top inherit those limits without learning them.

End to end below, with output from a real run. The worked example is Open-Meteo,
a public weather API that needs no credentials, so you can reproduce every step
yourself.

---

## 1 · Install

```bash
git clone https://github.com/FrancyJGLisboa/semantic-recon.git
cd semantic-recon
./scripts/install.sh
```

```
Claude Code    linked  -> ~/.claude/skills/semantic-recon
Codex CLI      linked  -> ~/.codex/skills/semantic-recon
Copilot CLI    linked  -> ~/.copilot/skills/semantic-recon
registry       created -> ~/contracts/INDEX.md
```

The installer detects which agent CLIs are present and skips the rest. It
symlinks, so `git pull` updates all of them at once. Use `--copy` if you would
rather have independent copies, `--uninstall` to remove.

**Verify it loaded.** In Claude Code, type `/` and look for `semantic-recon`.
It appears without restarting. All three CLIs read the same skill layout, but
loading has only been confirmed in Claude Code — check yours before relying
on it.

---

## 2 · The prompt

Two fields are yours. Everything else the skill determines, **including the
contract's name** — you never pick a slug.

```
/semantic-recon

TARGET_TYPE:            DATA_API
TARGET_LOCATION:        https://api.open-meteo.com
BLAST_RADIUS_OF_MISUSE: Test run, no production consumer.
OUT_OF_SCOPE:           Everything except Forecast and Historical Archive.
CALL_BUDGET:            120
```

| field | why it has to be you |
|---|---|
| `BLAST_RADIUS_OF_MISUSE` | only you know what breaks in your business if an agent gets this wrong |
| `OUT_OF_SCOPE` | only you know where this run should stop |

`TARGET_TYPE` is one of `DATA_API`, `DATABASE`, `MCP_SERVER`, `CODEBASE`.

**With credentials**, add the variable name — never the value:

```bash
export MYSYSTEM_TOKEN="..."      # in your shell, not in the prompt
```
```
CREDENTIALS_AVAILABLE:  yes, via $MYSYSTEM_TOKEN
WRITE_ACCESS:           read-only
```

Use a read-only credential where the system offers one. The pack marks mutating
operations and will not run them without approval, but a read-only credential
makes that structural instead of behavioural.

---

## 3 · It stops after phase 1, on purpose

The first phase costs at most three operations and hands back a proposed name
with its derivation. Confirm before it spends the call budget.

```
contract_id_derivation:
  raw_name:            "Open-Meteo.com"
  source:              <title> of https://open-meteo.com/en/docs
  normalized_to:       open_meteo
  collision_checked:   yes — against ~/contracts/INDEX.md
  escalated_to_human:  no
```

The slug is derived deterministically: the same asserted name always normalizes
to the same result. Two runs can still read the name from different surfaces —
a page title one time, an OpenAPI `info.title` the next — so the collision check
against `INDEX.md` is what catches the rest. If you disagree with the name, say
so now. After this point it is frozen, and it appears in the folder name, the
Python package, and every file header.

Say `continue` and the remaining phases run: freeze the exam, explore access,
profile structure, map semantics, find the business rules, try to break every
claim, compile the code, compile the contract, and audit it clean-room.

---

## 4 · What you get

```
~/contracts/
├── INDEX.md                        which contract answers what
├── AUTHORITY.md                    appears only once two contracts overlap
└── data_contract_open_meteo/
    ├── AGENT_INSTRUCTIONS.md       ← start here. Written to be the only file read
    ├── PLAYBOOKS.md                recipes by question shape
    ├── TRAPS.md                    wrong value beside right value
    ├── UNCERTAINTIES.md            questions only a human can answer
    ├── AUTHORITY_POLICY.md         which value governs when several exist
    ├── ACCESS.md ENTITIES.md METRICS.md DIMENSIONS.md
    ├── RELATIONSHIPS.md TEMPORAL_SEMANTICS.md BUSINESS_RULES.md
    ├── code/                       client · validators · series · health
    ├── tests/                      every trap is a regression test
    └── evidence/                   frozen questions, observations, counterexamples, audit
```

**The reconstructible half** — `ENTITIES`, `METRICS`, `ACCESS`, `DIMENSIONS` —
a competent agent could rebuild most of it from the vendor's docs.

**The half that is the point** — `TRAPS`, `UNCERTAINTIES`, `AUTHORITY_POLICY`,
`counterexamples.yaml`, `validators.py`. None of it exists without having probed
the system, and each item carries the measurement that established it.

Open-Meteo does document some of this in prose. That is not the same as an agent
loading it at the moment it builds a request, which is the entire point: the
contract turns each one into a refusal that fires whether or not anybody read
anything. Five, from the real run:

- the two products return different values for the same past date, from
  different grid cells
- `timezone` changes the *value* of a daily aggregate, not its label — and not
  every variable equally, so a temperature spot-check says it does not matter
- an unknown query parameter returns **200** and is silently ignored, so a
  typo applies the default
- the historical archive is not all ERA5; the last ~5 days are filled from an
  unnamed source with no seam marker
- `best_match` is a per-location selection, never reported, with 1.7 °C of
  spread between models

---

## 5 · Reading the verdict

The audit ends in exactly one of three states.

| status | meaning |
|---|---|
| `PASS` | clean-room agent answered the frozen questions correctly, nothing unresolved |
| `PASS_WITH_UNRESOLVED_ITEMS` | correct, but some questions need a human or the vendor |
| `FAIL` | do not use it yet; the report says why |

`PASS_WITH_UNRESOLVED_ITEMS` is the normal outcome for a real system, and it is
not a defect. It means the contract will be **correct but conservative**: it
refuses where a fully-resolved contract would answer. Each unresolved item
carries a precise question and an owner. Answering them and re-running the
refresh is how the contract gets less conservative over time.

---

## 6 · Using it

Paste this into any agent that will touch the system:

```
Before querying this system:
1. Run contract_health.report(). If EXPIRED or DRIFT_DETECTED, say so first.
2. Read data_contract_<slug>/AGENT_INSTRUCTIONS.md and use its routing table.
3. Call functions under data_contract_<slug>/code/. Never reach the API directly.
4. If a validator refuses, report the refusal — do not bypass it.
5. Preserve provenance in every substantive answer.
```

The full block is in `references/downstream.md`.

**In code**, the contract does the refusing for you:

```python
from data_contract_open_meteo.code import client, series

res = client.query({"product": "forecast", "latitude": 52.52, "longitude": 13.41,
                    "daily": "temperature_2m_max", "timezone": "UTC",
                    "models": "icon_seamless", "forecast_days": 3})

print(series.format_with_provenance(res[0]["daily"]["temperature_2m_max"]))
# 2026-09-01: 22.2 °C
# 2026-09-02: 21.8 °C
# — source: forecast · icon_seamless · grid 52.5200,13.4200 (38 m) · tz GMT
```

Leave out `models` and it stops you:

```
REFUSED: a forecast request with no explicit model
WHY: best_match selects a model per location, never reports which, and the
     spread across models reached 1.7 C at a 3-day horizon (U-02, CE-06)
INSTEAD: pass models='icon_seamless' (or ecmwf_ifs025 / gfs_seamless), or pass
     allow_best_match=True for a single casual lookup you will label
```

Every refusal carries three things: what was refused, why in one sentence, and
the correct call ready to copy. Following the messages is how you converge on
correct usage. In the one test of this so far, a weather skill written with
**zero refusal logic of its own** was stopped five times, reached working code
in two rounds of following the messages, and inherited a fact its author never
knew — that two models resolve to different grid cells.

**Anything a person will read** goes through `format_with_provenance()`. It is
the only formatter the contract ships, and it cannot omit the source.

---

## 7 · A second system

Run the skill again. The Target Profiler checks for collisions against
`INDEX.md` on its own.

When two contracts can answer the same question, an arbiter appears above them
(`AUTHORITY.md`, `registry/authority.py`). Ask it rather than choosing:

```python
from registry import authority

authority.route({"date": date(2019, 3, 15)})
# <Ruling open_meteo by CAPABILITY: the only registered contract that can
#  answer: met_locationforecast does not serve dates before today>

authority.route({"date": date(2026, 9, 3)}, country="NO")
# REFUSED: choosing between met_locationforecast, open_meteo
# WHY: all of them can answer this, so capability does not decide, and no
#      operator preference is declared ...
```

Capability decides where it can. A preference nobody declared is escalated to
you, never guessed — a guessed preference is indistinguishable from a policy,
and will be inherited and defended by agents that have no idea you never made
it. Comparing two contracts is allowed; merging them is not, and takes no
override.

---

## 8 · Keeping it true

```python
from data_contract_open_meteo.code import contract_health
print(contract_health.report())
```
```
CONTRACT open_meteo — verified 2026-09-01 (0 days ago) — FRESH
smoke test: PASS
```

When it goes `STALE` or reports drift, run a refresh:

```
/semantic-recon refresh open_meteo
```

A refresh reads `.contract_id` and never re-derives the slug — that would fork
the contract. It re-runs only the phases the smoke test flagged, re-answers the
**same frozen questions** (never new ones), and produces a semantic diff before
anything is overwritten.

---

## When not to use this

Not for a one-off query. The cost is paid once and the protection is
distributed, so the return comes from repetition: build five things on one
contract and all five inherit the same traps and refusals without anyone
rediscovering them. For a single question, just call the API.

## What has and has not been shown

Run end to end twice, against two public weather APIs. Two contracts audited
clean-room against questions frozen before discovery: 20/22 and 17/17 correct,
zero wrong. 64 tests. Loading confirmed in Claude Code.

Not shown: loading in Codex or Copilot CLI, any target that is not a
`DATA_API`, or anything general about agent behaviour. What was measured is one
skill inheriting refusals it did not write.
