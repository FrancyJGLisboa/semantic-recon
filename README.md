# semantic-recon

**Better conditions for building AI agents with expertise on a system.**

A portable agent skill that probes an API, MCP server, database, or codebase —
by running it, not by reading about it — and compiles what it finds into a
**data contract**: a folder whose code refuses the operations that are silently
wrong, each refusal carrying the counterexample that proved it.

An agent built on that contract inherits the limits without having to learn
them.

Installs into **Claude Code**, **Codex CLI** and **Copilot CLI**; all three read
the same `<config>/skills/<name>/SKILL.md` layout, so one source serves them all.

## In plain language

AI assistants can use real systems now — a database, an internal API, a weather
service. The risk is not that they crash. It is that they hand you a number
that is wrong and looks completely fine.

A real example. Ask a public weather service how much rain fell in Tokyo
yesterday. The answer is **4.1 mm** or **1.2 mm** depending on one setting most
people never touch. No error either way; both look like *the* answer. And if you
check whether that setting matters by looking at temperature instead of rain,
temperature comes back **identical** both ways — so you conclude it is
cosmetic, and from then on you are confidently wrong about rain.

Nobody hid that. It is the kind of thing that is obvious to whoever built the
service and invisible to everyone else. Every real system has a handful.

This tool sends an AI to poke at a system for an hour — try things, break
things, write down what surprised it, with the actual numbers — and turns every
surprise into a tripwire in code. After that, any AI working with that system
hits the tripwire instead of the wrong answer, **without having read anything.**

It is the difference between a new hire and a senior colleague. The senior does
not know more facts; they know where the landmines are and stop you before you
step on one.

We tested it the obvious way: a small weather app with **zero safety checks
written into it** was stopped five times by the tool's output, and reached
correct code in two rounds of following the error messages — including for a
reason its author never knew.

## What changes

Same question, same code, same API. The difference is whether a contract exists.

**Without**
```
>>> forecast(52.52, 13.41)
2026-09-01: 22.2 °C
```
Which of five models answered? Unknown. Which grid cell — you asked for one and
got another a kilometre away? Unknown. Comparable to the figure you stored
yesterday? No way to tell. **Nothing is wrong on the screen.**

**With**
```
>>> forecast(52.52, 13.41)
REFUSED: a forecast request with no explicit model
INSTEAD: pass models='icon_seamless' …

2026-09-01: 22.2 °C
— forecast · icon_seamless · grid 52.5200,13.4200 (38 m) · tz Europe/Berlin
```
Stopped before the ambiguous call, told exactly how to fix it, and the answer
names what produced it. **You did not have to know any of that.**

That is the whole trade. You spend an hour once. After that, correctness on this
system stops depending on whether the next person happens to know the five
things that matter.

## What this rests on

The pack has been run end to end twice, against two public weather APIs.
Everything claimed here comes from those runs, and the boundaries are stated
because a project about evidence has to meet its own standard.

**Established**

- Two contracts built and audited clean-room against questions frozen *before*
  discovery began: **20 of 22** and **17 of 17** correct, zero wrong answers.
- Six falsified assumptions in the first run, four in the second. Each keeps a
  measured counterexample in `evidence/`.
- A weather skill written with **zero refusal logic of its own** inherited five
  refusals from its contract and reached correct code in two rounds of doing
  what the refusal messages said.
- 64 tests across the two contracts and the registry.
- The skill loads in Claude Code.

**Not established**

- Loading in Codex CLI or Copilot CLI. The layout matches and the installer
  places the skill correctly, but nobody has invoked it there.
- Anything about non-API targets. The `DATABASE`, `MCP_SERVER` and `CODEBASE`
  vocabularies are written and unexercised.
- Any general claim about agent behaviour. What was measured is one skill
  inheriting refusals it did not write.

## The thesis

A contract is not successful because it is complete.
It is successful because it **changes the behavior of the agent that consults it.**

Most "document the system for the AI" efforts produce a beautiful folder nobody
reads at decision time. This pack optimizes for the opposite: what an agent
under context pressure actually loads, and what fails loudly when it does the
wrong thing anyway.

That produces a few opinionated choices:

- **Code that refuses beats prose that explains.** `validate_query()` is a hard
  gate with eight refusal classes, not a helper. If a downstream agent can
  produce a silently wrong result without an exception firing, that is a defect
  in the code layer, not a documentation gap.
- **The exam is written before the studying.** Holdout questions are frozen
  before any discovery runs, so the final clean-room audit cannot grade itself
  on questions the contract happens to answer.
- **Triage by blast radius, not by confidence.** A high-confidence
  `SILENT_WRONG` claim — one that returns a plausible number with no error — is
  the most dangerous object in the contract. A `LOUD_FAIL` claim already
  protects itself.
- **Nothing is verified until someone tried to break it.** A dedicated red-team
  phase must attempt falsification before any rule is promoted, and every
  falsified assumption becomes a documented trap with the wrong value shown
  next to the right one.
- **Identity travels with the content.** Agents quote fragments, not paths, so
  every artifact carries its contract id. Data from one contract reaching
  another contract's functions raises.

## Targets

`DATA_API` · `DATABASE` · `MCP_SERVER` · `CODEBASE`

A vocabulary table binds the pack's abstract terms — entity, measure, grain,
authority, temporal, forbidden operation — to each target type, so the same
phases run whether you are mapping a REST API, a Postgres schema, an MCP
server, or a repository.

Use it when the same system will be used repeatedly, by agents, and being
silently wrong is expensive. Do not use it for a one-off query.

**New here?** → **[francyjglisboa.github.io/semantic-recon](https://francyjglisboa.github.io/semantic-recon/)**
walks the whole path: install, the prompt, what comes out, and how to use it,
with real output from a real run. The same text lives in
[GETTING-STARTED.md](GETTING-STARTED.md) if you would rather read it here.

## Install

```bash
git clone https://github.com/FrancyJGLisboa/semantic-recon.git
cd semantic-recon
./scripts/install.sh
```

The installer detects which agent CLIs are present and symlinks into each:

```
Claude Code    ~/.claude/skills/semantic-recon
Codex CLI      ~/.codex/skills/semantic-recon
Copilot CLI    ~/.copilot/skills/semantic-recon
```

Symlinking keeps the clone as the single source of truth — pull, and all three
CLIs see the change with no reinstall. `--copy` installs copies instead;
`--uninstall` removes them.

## Three ways to use what came out

Ranked by how little you have to do.

**1 · Paste the bootstrap into any agent** — *no code.*
Ten lines from `references/downstream.md`. The agent reads the routing table,
calls the contract's functions instead of the API, and reports refusals instead
of guessing. Works in any assistant that can read a folder.

**2 · Import the code into what you are building** — *one import.*
The refusals stop being advice and become structural: they fire whether or not
anyone read the documentation.

```python
from data_contract_open_meteo.code import client, series

res = client.query({"product": "forecast", "latitude": 52.52, "longitude": 13.41,
                    "daily": "temperature_2m_max", "timezone": "UTC",
                    "models": "icon_seamless", "forecast_days": 3})
print(series.format_with_provenance(res[0]["daily"]["temperature_2m_max"]))
```

Leave out `models` and it refuses, naming the 1.7 °C spread between models and
the exact call that fixes it.

**3 · Point another agent at the folder and let it build** — *the leverage.*
This is where it compounds. Build five things on one contract and all five
inherit the same traps, without any of their authors learning them.

> **The third way, measured.** We wrote a weather skill with **zero refusal
> logic of its own** — no checks, no validation, nothing about models or
> timezones. Its contract stopped it five times. Two rounds of following the
> messages and it was correct, including for a reason its author never knew:
> two models resolve to different grid cells.

Anything a person will read goes through `format_with_provenance()`. It is the
only formatter a contract ships, and it cannot omit the source.

## What lands on disk

```
~/contracts/
├── INDEX.md                          registry; agents read this first
└── data_contract_<slug>/
    ├── AGENT_INSTRUCTIONS.md         self-sufficient; assume it is all that's read
    ├── PLAYBOOKS.md                  recipes by question shape, not by concept
    ├── TRAPS.md                      wrong value next to right value
    ├── UNCERTAINTIES.md              questions only a human can answer
    ├── code/validators.py            the gate that refuses
    ├── code/contract_health.py       staleness and drift
    ├── tests/                        every trap is a regression test
    └── evidence/                     holdout questions, counterexamples, provenance
```

Plus the semantic layer: entities, metrics, dimensions, relationships, temporal
semantics, business rules, authority policy.

## Docs

| page | what it covers |
|---|---|
| [Walkthrough](https://francyjglisboa.github.io/semantic-recon/) | install → prompt → artifacts → using them |
| [How it works](https://francyjglisboa.github.io/semantic-recon/concepts.html) | the consult-time path, the sealed pipeline, the claim triage grid, where a rule should live |

Page fragments live in `docs/src/`; `docs/*.html` is generated by
`scripts/build-docs.py`. `GETTING-STARTED.md` is the canonical text for the
walkthrough — if it and the page disagree, the Markdown is right.

## Layout

```
SKILL.md                     router; the only file loaded every invocation
references/
  full-pack.txt              source of truth — the entire pack
  vocabulary.md              target profile + term binding per target type
  identity.md                slug derivation + identity discipline
  structure.md               per-type probes + output folder layout
  standards.md               claim classification, blast radius, evidence
  downstream.md              consuming-agent bootstrap + refresh runs
  agents/00..10              one file per phase, read on entry
templates/                   registry seed, credential injection pattern
docs/src/                    page fragments; docs/*.html is generated
scripts/install.sh           install into every CLI found
scripts/split.py             regenerate references/ from full-pack.txt
scripts/build-docs.py        regenerate docs/*.html from docs/src/
```

Splitting the pack is not cosmetic. `SKILL.md` loads on every invocation; the
phase files load only when the run reaches that phase.

## Editing

`references/*.md` are **generated**. Edit `references/full-pack.txt`, then:

```bash
python3 scripts/split.py        # references/ from full-pack.txt
python3 scripts/build-docs.py   # docs/*.html from docs/src/
python3 scripts/check-docs.py   # fails if the walkthrough's two surfaces drift
```

Editing a generated file directly loses your change on the next build.

Enable the pre-commit hook once per clone:

```bash
git config core.hooksPath .githooks
```

It refuses a commit that would publish a stale generated file, or let the
walkthrough's two surfaces drift. It regenerates to detect staleness, so a
stale file is already fixed in your working tree by the time it tells you —
but it will not stage it for you.

`GETTING-STARTED.md` and `docs/src/index.html` tell the same story to different
readers and neither can be generated from the other without degrading it, so
they cannot share a source. `check-docs.py` compares their section headings and
fails on any difference that has not been declared, with a reason, in its
`EXPECTED_DIFFERENCES` table. When you cannot prevent a divergence, make it
loud — the same move the contracts make.

## License

MIT
