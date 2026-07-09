#!/usr/bin/env python3
"""
Build an editable draw.io diagram of the *train to crazy town* worldview tree
from train_tree.json (generated from assumptions/ by generate.py), using
Graphviz for a top-to-bottom layered layout (root = least crazy, at the top).
Mirrors the setup in morganrivers/iati_webapp
(docs/diagram/build_webapp_drawio.py): all layout/emit machinery is shared via
graph_common.py; this script only defines the tree's stop bands, the
craziness-gradient colours, and the per-node Squiggle playground links.

Each node is a WORLDVIEW (a chain of assumptions); each edge adds exactly one
assumption. A node's band ("STOP k") is its craziest accepted assumption — how
far down the line that worldview rides.

Usage:  python build_diagram.py [train_tree.json] [out.drawio]
Requires Graphviz 'dot' on PATH.
"""
import json, sys, os
from graph_common import (run_dot, transforms, decl, emit_node, emit_edges,
                          group_box, wrap_mxfile, esc)
from squiggle_playground import playground_url

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), 'train_tree.drawio')

G = json.load(open(SRC))
nodes = [n for n in G['nodes'] if not n.get('id', '').startswith('_')]
edges = G['edges']


# ---------- per-node model links --------------------------------------------
# Each node opens its Squiggle model in a TEMPORARY playground link: clicking a
# node loads the model live and editable, with no Squiggle Hub account. The
# generated worldview models are standalone (the assumption chain is composed in
# Python before the Squiggle is rendered), so the whole file rides in the link's
# #code= hash. See squiggle_playground.py for the encoding (identical to
# Squiggle's own playground.ts).
# NOTE: keep REF a plain branch name (no refs/heads/ prefix). draw.io's viewer
# recognises raw.githubusercontent.com/<user>/<repo>/<branch>/<path> URLs and
# re-parses them into its GitHub handler; extra path segments make it read the
# branch as "refs" and fail with "File not found".
REPO = 'morganrivers/train_to_crazy_town'
REF = os.environ.get('DIAGRAM_REF', 'main')

for n in nodes:
    link = playground_url(n)
    if link:
        n['link'] = link


# ---------- node sizing (label-driven, so Graphviz reserves real footprint) --
def size(n):
    lines = n['lbl'].split('\n')
    maxc = max(len(x) for x in lines)
    w = max(150, int(maxc * 7.2) + 28)
    h = len(lines) * 16 + 28
    return w, h


# Compose the node label: worldview headline (latest assumption + accepted
# chain), its argmax donation target, and the public figure(s) who most
# prominently articulate the latest assumption.
for n in nodes:
    figs = ', '.join(n.get('figures', []))
    n['lbl'] = n['lbl'] + '\n→ ' + n.get('top_pick', '?') + ('\n(' + figs + ')' if figs else '')
    n['w'], n['h'] = size(n)


# ---------- craziness gradient (calm slate at the top → hot at the bottom) ---
# Colour encodes how far down the train a worldview rides: its craziest
# accepted assumption, 0 (parochial) to 9 (Boltzmann brain).
STOP_STYLE = [
    'fillColor=#dfe7ef;strokeColor=#6b7f96;fontColor=#1b2733;',   # 0 slate (parochial)
    'fillColor=#cfe6cf;strokeColor=#5a9367;fontColor=#1e3a24;',   # 1 green (all humans)
    'fillColor=#e6e2c0;strokeColor=#b0a04a;fontColor=#3a3410;',   # 2 olive (animals)
    'fillColor=#f2e3b3;strokeColor=#c9a72a;fontColor=#57450e;',   # 3 gold (future, discounted)
    'fillColor=#f6e0c0;strokeColor=#c9932a;fontColor=#5a3f10;',   # 4 amber (no discounting)
    'fillColor=#f5d3b8;strokeColor=#cc7a33;fontColor=#5a300e;',   # 5 orange (RP animals)
    'fillColor=#f2ccc0;strokeColor=#c96a4a;fontColor=#5a2410;',   # 6 clay (suffering)
    'fillColor=#eeb3b3;strokeColor=#c0392b;fontColor=#5a1410;',   # 7 red (simulation)
    'fillColor=#d7c6e6;strokeColor=#6a3fa0;fontColor=#2c1650;',   # 8 violet (anti-realism)
    'fillColor=#c9b3dd;strokeColor=#4a2a78;fontColor=#201040;',   # 9 dark violet (Boltzmann)
]
NODE_BASE = 'rounded=1;whiteSpace=wrap;html=1;fontSize=11;'
def node_style(n):
    return NODE_BASE + STOP_STYLE[min(n['stop'], len(STOP_STYLE) - 1)]

EBASE = 'edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;strokeColor=#9aa6b3;fontSize=9;fontColor=#5b6675;'
EK = {'expand': 'strokeColor=#8a5fb0;', 'override': 'strokeColor=#c0392b;dashed=1;'}


# ---------- layout via Graphviz ---------------------------------------------
dot = ['digraph T{', 'rankdir=TB;', 'splines=polyline;', 'nodesep=0.5;', 'ranksep=0.9;',
       'node[shape=box,fixedsize=true];']
for n in nodes:
    dot.append(decl(n))
for e in edges:
    dot.append(f'"{e["from"]}"->"{e["to"]}";')
# Force clean stop bands: every node at stop k ranks above every node at stop
# k+1 (same invisible-funnel trick as the iati_webapp generator).
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
pos, H, edgepts = run_dot(dot)
X, Y = transforms(H)

bg = []   # stop-band boxes (behind)
mid = []  # edges
fg = []   # nodes (front)

# one dotted band per stop, labelled with how far down the train it is
STOP_COL = ['#6b7f96', '#5a9367', '#b0a04a', '#c9a72a', '#c9932a',
            '#cc7a33', '#c96a4a', '#c0392b', '#6a3fa0', '#4a2a78']
for s in stops:
    col = STOP_COL[min(s, len(STOP_COL) - 1)]
    group_box(nodes, set(by_stop[s]), pos, X, Y, f'band_{s}',
              f'STOP {s}', col, bg)

for n in nodes:
    if n['id'] in pos:
        fg.append(emit_node(n, node_style(n), pos, X, Y))
mid = emit_edges(edges, edgepts, X, Y, EBASE, EK)

xml = wrap_mxfile(bg + mid + fg, 'Train to crazy town', 'train-to-crazy-town')
open(OUT, 'w').write(xml)
print('wrote %s: nodes=%d edges=%d bytes=%d' % (OUT, len(pos), len(edges), len(xml)))


# ---------- public "anyone can view" draw.io link ---------------------------
# The repo is public, so draw.io can open the committed .drawio straight from its
# raw GitHub URL via the #U hash (chrome=0 => read-only viewer, no account). This
# is the link "auto-populated by repo code": it points at whatever this build
# just committed. Override the ref via DIAGRAM_REF (defaults to main).
import urllib.parse
raw = f'https://raw.githubusercontent.com/{REPO}/{REF}/diagram/{os.path.basename(OUT)}'
view = 'https://viewer.diagrams.net/?lightbox=1&nav=1&chrome=0#U' + urllib.parse.quote(raw, safe='')
print('view (read-only, public): ' + view)
