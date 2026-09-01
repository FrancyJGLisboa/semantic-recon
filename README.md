# semantic-recon

A portable agent skill that runs a multi-agent reconnaissance of a target
system and compiles a **data contract** — a folder that makes future AI agents
behave like a subject-matter expert on that system instead of rediscovering it,
badly, on every run.

Works in **Claude Code**, **Codex CLI**, and **Copilot CLI**. All three read the
same `<config>/skills/<name>/SKILL.md` layout, so one source installs to all of
them.

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

**New here? [GETTING-STARTED.md](GETTING-STARTED.md)** walks the whole path —
install, the prompt, what comes out, and how to use it — with real output from
a real run.

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
deterministic normalization, so two runs on one system never fork into two
contracts.

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
scripts/install.sh           install into every CLI found
scripts/split.py             regenerate references/ from full-pack.txt
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
