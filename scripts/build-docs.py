#!/usr/bin/env python3
"""Wrap the page fragments in docs/src/ into standalone documents in docs/.

The fragments are also what gets published as Artifacts, which inject their own
<head>/<body>. docs/src/ is the single source; docs/*.html is generated. Edit
the fragment, then run this.

    python3 scripts/build-docs.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = os.path.join(ROOT, 'docs', 'src'), os.path.join(ROOT, 'docs')

PAGES = [
    ('index.html', True,
     'Better conditions for building AI agents with expertise on a system. '
     'Install to working code, walked through with output from a real run.'),
    ('concepts.html', False,
     'How the system works: the consult-time path, the sealed pipeline, the '
     'claim triage grid, and where a rule should live.'),
]

NAV = '''<nav class="sitenav">
  <a href="./" {i}>Walkthrough</a>
  <a href="./concepts.html" {c}>How it works</a>
  <a href="https://github.com/FrancyJGLisboa/semantic-recon">GitHub</a>
</nav>'''

NAVCSS = '''
.sitenav{position:sticky;top:0;z-index:10;display:flex;gap:1.5rem;align-items:center;
  padding:.85rem 26px;background:var(--paper);border-bottom:1px solid var(--rule);
  font-family:var(--mono);font-size:.72rem;letter-spacing:.09em;text-transform:uppercase}
.sitenav a{color:var(--muted);text-decoration:none;padding-bottom:2px;border-bottom:1px solid transparent}
.sitenav a:hover{color:var(--ink)}
.sitenav a[aria-current="page"]{color:var(--accent);border-bottom-color:var(--accent)}
.sitenav a:last-child{margin-left:auto}
.sitenav a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
'''

FAVICON = ('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 '
           'viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>'
           '\U0001F9ED</text></svg>')


def pack_version():
    """Read it from the pack itself. A version typed into a page is a claim
    that stops being true the moment the pack moves, and nothing would say so."""
    pack = os.path.join(ROOT, 'references', 'full-pack.txt')
    with open(pack, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('Version:'):
                return line.split(':', 1)[1].strip()
    sys.exit('no Version: line in references/full-pack.txt')


def build(name, is_index, desc):
    frag = open(os.path.join(SRC, name), encoding='utf-8').read()
    frag = frag.replace('{{PACK_VERSION}}', pack_version())
    m = re.search(r'<title>(.*?)</title>', frag)
    if not m:
        sys.exit('%s has no <title>' % name)
    title = m.group(1)
    frag = re.sub(r'<title>.*?</title>\s*', '', frag, count=1)
    frag = frag.replace('</style>', NAVCSS + '</style>', 1)
    nav = NAV.format(i='aria-current="page"' if is_index else '',
                     c='' if is_index else 'aria-current="page"')
    frag = frag.replace('<div class="wrap">', nav + '\n\n<div class="wrap">', 1)
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n'
           '<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<title>%s · semantic-recon</title>\n'
           '<meta name="description" content="%s">\n'
           '<meta property="og:title" content="%s">\n'
           '<meta property="og:description" content="%s">\n'
           '<meta property="og:type" content="website">\n'
           '<link rel="icon" href="%s">\n'
           '</head>\n<body>\n%s</body>\n</html>\n'
           % (title, desc, title, desc, FAVICON, frag))
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(doc)
    print('%-16s %6d bytes  title=%r' % (name, len(doc), title))


if __name__ == '__main__':
    for n, i, d in PAGES:
        build(n, i, d)
    print('\nbuilt %d pages from docs/src/ (pack v%s)'
          % (len(PAGES), pack_version()))
