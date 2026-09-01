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

## Use

```
/semantic-recon
```

or describe the task in words: *"build a data contract for this MCP server"*,
*"make agents SME on this database"*.

Two fields are always yours to supply, because they are decisions rather than
discoveries:

| Field | Why you |
|---|---|
| `BLAST_RADIUS_OF_MISUSE` | Only you know what breaks in your business if an agent gets this system wrong |
| `OUT_OF_SCOPE` | Only you know where this run should stop |

Everything else the skill determines, **including the contract's name.** The
Target Profiler derives a slug from what the system calls itself, using
deterministic normalization: the same asserted name always yields the same
result. Two runs can still read that name from different surfaces, so a
collision check against the registry catches the rest.

Phase 1 costs at most three operations and returns the proposed slug with its
derivation. Confirm there before spending a call budget.

## What you get

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
python3 scripts/split.py
```

Editing the generated files directly loses your change on the next split.

## License

MIT
