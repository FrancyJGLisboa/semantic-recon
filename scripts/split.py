#!/usr/bin/env python3
"""Re-split references/full-pack.txt into the per-phase reference files.

full-pack.txt is the single source of truth. Edit it, then run this.
Files under references/ are generated; editing them directly is lost on the
next split.

    python3 scripts/split.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, 'references', 'full-pack.txt')

# (output path, header the section starts at, title)
SECTIONS = [
    ('references/vocabulary.md',                 '0. TARGET PROFILE',                   'Target Profile + Vocabulary Mapping'),
    ('references/identity.md',                   '0.1a CONTRACT_ID DERIVATION',         'CONTRACT_ID Derivation + Identity Discipline'),
    ('references/structure.md',                  '0.2 TYPE-SPECIFIC',                   'Type-Specific Probes + Output Structure'),
    ('references/agents/00-orchestrator.md',     '1. ORCHESTRATOR PROMPT',              'Orchestrator'),
    ('references/agents/01-target-profiler.md',  '1b. TARGET PROFILER PROMPT',          'Target Profiler (runs first)'),
    ('references/agents/02-holdout-author.md',   '2. HOLDOUT QUESTION AUTHOR',          'Holdout Question Author'),
    ('references/agents/03-access-explorer.md',  '3. ACCESS EXPLORER PROMPT',           'Access Explorer'),
    ('references/agents/04-schema-analyst.md',   '4. SCHEMA AND METADATA ANALYST',      'Schema and Metadata Analyst'),
    ('references/agents/05-semantic-analyst.md', '5. SEMANTIC AND ONTOLOGY ANALYST',    'Semantic and Ontology Analyst'),
    ('references/agents/06-business-analyst.md', '6. BUSINESS CONTRACT ANALYST',        'Business Contract Analyst'),
    ('references/agents/07-red-team.md',         '7. ADVERSARIAL VALIDATOR',            'Adversarial Validator / Semantic Red Team'),
    ('references/agents/08-implementation.md',   '8. REFERENCE IMPLEMENTATION ENGINEER','Reference Implementation Engineer'),
    ('references/agents/09-compiler.md',         '9. CONTRACT COMPILER PROMPT',         'Contract Compiler'),
    ('references/agents/10-auditor.md',          '10. INDEPENDENT FINAL AUDITOR',       'Independent Final Auditor'),
    ('references/downstream.md',                 '11. DOWNSTREAM PRODUCTION AGENT',     'Downstream Bootstrap + Contract Refresh'),
    ('references/registry.md',                   '12b. THE REGISTRY LAYER',             'The Registry Layer (multiple contracts)'),
    ('references/standards.md',                  '13. OPERATING PRINCIPLES',            'Operating Principles, Claim + Evidence Standards, Completion'),
]
END = 'END OF PROMPT PACK'


def main():
    lines = open(PACK, encoding='utf-8').read().split('\n')

    def find(prefix):
        for i, line in enumerate(lines):
            if line.startswith(prefix):
                return i
        sys.exit(f"section header not found in full-pack.txt: {prefix!r}")

    starts = [find(h) for _, h, _ in SECTIONS] + [find(END)]

    version = next((l.split(':', 1)[1].strip() for l in lines[:10]
                    if l.startswith('Version:')), 'unknown')

    for i, (path, _, title) in enumerate(SECTIONS):
        lo, hi = starts[i], starts[i + 1]
        # exclude the ==== rule that belongs to the next section's header
        while hi > lo and lines[hi - 1].startswith('===='):
            hi -= 1
        body = '\n'.join(lines[lo:hi]).strip('\n')
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(
                f"# {title}\n\n"
                f"<!-- Generated from references/full-pack.txt (pack v{version}) "
                f"by scripts/split.py. Do not edit; edit the pack and re-split. -->\n\n"
                f"```\n{body}\n```\n"
            )
        print(f"{hi - lo:5d}  {path}")

    print(f"\nsplit pack v{version} into {len(SECTIONS)} files")


if __name__ == '__main__':
    main()
