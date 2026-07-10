#!/usr/bin/env python3
"""
Build editable draw.io diagrams of the *train to crazy town* worldview tree from
train_tree.json (generated from assumptions/ by generate.py), using Graphviz for
a top-to-bottom layered layout (root = least crazy, at the top). Mirrors the
setup in morganrivers/iati_webapp (docs/diagram/build_webapp_drawio.py): all
layout/emit machinery is shared via graph_common.py.

Each node is a WORLDVIEW (a chain of assumptions); each edge adds exactly one
assumption. A node's band ("STOP k") is its craziest accepted assumption — how
far down the line that worldview rides.

The tree is cut into bounded, clickable PAGES (train_tree.json's `pages`, from
diagram/partition.py): each page is a subtree small enough to read, and a
subtree big enough for its own page is COLLAPSED on its parent page to a
`▼ N more worldviews` boundary node that links to that subtree's page. This
writes one .drawio per page: the root page keeps the given name, children get
`<root-basename>__<subtree-root-id>.drawio` beside it.

Usage:  python build_diagram.py [train_tree.json] [out.drawio]
Requires Graphviz 'dot' on PATH.
"""
import json, sys, os, urllib.parse
from graph_common import (run_dot, transforms, decl, emit_node, emit_edges,
                          group_box, wrap_mxfile)
from squiggle_playground import playground_url

HERE = os.path.dirname(__file__)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'train_tree.drawio')
OUTDIR = os.path.dirname(OUT) or '.'

G = json.load(open(SRC))
NODES = {n['id']: n for n in G['nodes'] if not n.get('id', '').startswith('_')}
EDGES = G['edges']
PAGES = G['pages']

# ---------- links: playground per node; child-page viewer per boundary --------
# Each node opens its Squiggle model in a TEMPORARY playground link (the model
# rides in the link's #code= hash; see squiggle_playground.py). A collapsed
# boundary instead links to the draw.io viewer of the subtree's own page.
# NOTE: keep REF a plain branch name (no refs/heads/ prefix) — draw.io re-parses
# raw.githubusercontent.com/<user>/<repo>/<branch>/<path> URLs into its GitHub
# handler, and extra segments make it read the branch as "refs" (File not found).
REPO = 'morganrivers/train_to_crazy_town'
REF = os.environ.get('DIAGRAM_REF', 'main')


def viewer_url(basename):
    raw = f'https://raw.githubusercontent.com/{REPO}/{REF}/diagram/{basename}.drawio'
    return 'https://viewer.diagrams.net/?lightbox=1&nav=1&chrome=0#U' + urllib.parse.quote(raw, safe='')


PLAY = {nid: playground_url(n) for nid, n in NODES.items()}

# ---------- craziness gradient (calm slate at the top → hot at the bottom) ----
# Colour encodes how far down the train a worldview rides: its craziest accepted
# assumption, 0 (parochial) to 11 (Boltzmann brain).
STOP_STYLE = [
    'fillColor=#dfe7ef;strokeColor=#6b7f96;fontColor=#1b2733;',   # 0 slate (parochial)
    'fillColor=#cfe6cf;strokeColor=#5a9367;fontColor=#1e3a24;',   # 1 green (all humans)
    'fillColor=#e6e2c0;strokeColor=#b0a04a;fontColor=#3a3410;',   # 2 olive (animals)
    'fillColor=#f2e3b3;strokeColor=#c9a72a;fontColor=#57450e;',   # 3 gold (future, discounted)
    'fillColor=#f6e0c0;strokeColor=#c9932a;fontColor=#5a3f10;',   # 4 amber (no discounting)
    'fillColor=#f5d3b8;strokeColor=#cc7a33;fontColor=#5a300e;',   # 5 orange (RP animals)
    'fillColor=#f2ccc0;strokeColor=#c96a4a;fontColor=#5a2410;',   # 6 clay (suffering)
    'fillColor=#eec2a8;strokeColor=#c65a2e;fontColor=#5a2a10;',   # 7 terracotta (meat-eater)
    'fillColor=#e9b0a0;strokeColor=#b8402a;fontColor=#511810;',   # 8 rust (net-negative lives)
    'fillColor=#eeb3b3;strokeColor=#c0392b;fontColor=#5a1410;',   # 9 red (simulation)
    'fillColor=#d7c6e6;strokeColor=#6a3fa0;fontColor=#2c1650;',   # 10 violet (anti-realism)
    'fillColor=#c9b3dd;strokeColor=#4a2a78;fontColor=#201040;',   # 11 dark violet (Boltzmann)
]
NODE_BASE = 'rounded=1;whiteSpace=wrap;html=1;fontSize=11;'
# A collapsed boundary gets a bold dashed border + fold hint so it reads as
# "there is more behind this — click to open its page".
COLLAPSE_EXTRA = 'dashed=1;dashPattern=8 4;strokeWidth=3;fontStyle=1;'
STOP_COL = ['#6b7f96', '#5a9367', '#b0a04a', '#c9a72a', '#c9932a', '#cc7a33',
            '#c96a4a', '#c65a2e', '#b8402a', '#c0392b', '#6a3fa0', '#4a2a78']

EBASE = 'edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;strokeColor=#9aa6b3;fontSize=9;fontColor=#5b6675;'
EK = {'expand': 'strokeColor=#8a5fb0;', 'override': 'strokeColor=#c0392b;dashed=1;'}


def size(n):
    lines = n['lbl'].split('\n')
    maxc = max(len(x) for x in lines)
    return max(150, int(maxc * 7.2) + 28), len(lines) * 16 + 28


def _fmt_lives(x):
    """Compact lives-saved-equivalent per $1000 (2.1e4 -> '21k', 0.33 -> '0.33')."""
    ax = abs(x)
    if ax >= 1000:
        return f"{x/1000:.0f}k"
    if ax >= 10:
        return f"{x:.0f}"
    if ax >= 1:
        return f"{x:.1f}"
    return f"{x:.2g}" if ax > 0 else "0"


def pick_lines(n):
    """The winner + runner-up lines: each org's lives-saved-equivalent per $1000
    and the confidence (P it is actually the best buy) the distributions give."""
    picks = n.get('picks') or []
    if not picks:                      # flat / override worldviews
        return ['→ ' + n.get('top_pick', '?')]
    w = picks[0]
    out = [f"→ {w['org']}",
           f"   {_fmt_lives(w['lives_per_1000usd'])} lives-eq/$1k · "
           f"{round(w['confidence']*100)}% best"]
    if len(picks) > 1:
        r = picks[1]
        out.append(f"   runner-up {r['org']} · {round(r['confidence']*100)}%")
    return out


def prepare(nid, collapsed):
    """A render-ready copy of a node for one page: compose its label + link.
    Collapsed boundaries advertise their hidden subtree and link to its page."""
    n = dict(NODES[nid])
    lines = [n['lbl']] + pick_lines(n)
    if nid in collapsed:
        c = collapsed[nid]
        lines.append(f"▼ {c['count']} more worldviews")
        n['link'] = viewer_url(c['child'])
        n['collapsed'] = True
    else:
        figs = ', '.join(n.get('figures', []))
        if figs:
            lines.append('(' + figs + ')')
        if PLAY.get(nid):
            n['link'] = PLAY[nid]
    n['lbl'] = '\n'.join(lines)
    n['w'], n['h'] = size(n)
    return n


def build_page(page):
    ids = set(page['nodes'])
    collapsed = page['collapsed']
    nodes = [prepare(nid, collapsed) for nid in page['nodes']]
    edges = [e for e in EDGES if e['from'] in ids and e['to'] in ids]

    # ---- layout via Graphviz (stop bands via the invisible-funnel trick) -----
    dot = ['digraph T{', 'rankdir=TB;', 'splines=polyline;', 'nodesep=0.5;', 'ranksep=0.9;',
           'node[shape=box,fixedsize=true];']
    for n in nodes:
        dot.append(decl(n))
    for e in edges:
        dot.append(f'"{e["from"]}"->"{e["to"]}";')
    stops = sorted({n['stop'] for n in nodes})
    by_stop = {s: [n['id'] for n in nodes if n['stop'] == s] for s in stops}
    for i in range(len(stops) - 1):
        z = f'__z{i}'
        dot.append(f'"{z}"[style=invis,width=0.01,height=0.01,label=""];')
        for nid in by_stop[stops[i]]:
            dot.append(f'"{nid}"->"{z}"[style=invis];')
        for nid in by_stop[stops[i + 1]]:
            dot.append(f'"{z}"->"{nid}"[style=invis];')
    dot.append('}')
    pos, Hgt, edgepts = run_dot(dot)
    X, Y = transforms(Hgt)

    bg, fg = [], []
    for s in stops:
        col = STOP_COL[min(s, len(STOP_COL) - 1)]
        group_box(nodes, set(by_stop[s]), pos, X, Y, f'band_{s}', f'STOP {s}', col, bg)
    for n in nodes:
        if n['id'] in pos:
            style = NODE_BASE + STOP_STYLE[min(n['stop'], len(STOP_STYLE) - 1)]
            if n.get('collapsed'):
                style += COLLAPSE_EXTRA
            fg.append(emit_node(n, style, pos, X, Y))
    mid = emit_edges(edges, edgepts, X, Y, EBASE, EK)

    title = 'Train to crazy town' + ('' if page['is_root'] else f' — {page["root"]} subtree')
    xml = wrap_mxfile(bg + mid + fg, title, page['id'])
    out = OUT if page['is_root'] else os.path.join(OUTDIR, page['id'] + '.drawio')
    open(out, 'w').write(xml)
    n_real = sum(1 for n in nodes if n['id'] in pos)
    print('wrote %s: nodes=%d edges=%d bytes=%d' % (os.path.basename(out), n_real, len(edges), len(xml)))
    return out


root_out = None
for page in PAGES:
    out = build_page(page)
    if page['is_root']:
        root_out = out

# ---------- public "anyone can view" draw.io link (root page) ----------------
# The repo is public, so draw.io opens the committed .drawio straight from its
# raw GitHub URL via the #U hash (chrome=0 => read-only viewer, no account).
print('view (read-only, public): ' + viewer_url(os.path.basename(root_out)[:-len('.drawio')]))
