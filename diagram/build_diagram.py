#!/usr/bin/env python3
"""
Build an editable draw.io diagram of the *train to crazy town* worldview tree
from train_tree.json, using Graphviz for a top-to-bottom layered layout (root =
least crazy, at the top). Mirrors the setup in morganrivers/iati_webapp
(docs/diagram/build_webapp_drawio.py): all layout/emit machinery is shared via
graph_common.py; this script only defines the tree's stop bands, the
craziness-gradient colours, and the (stubbed) per-node Guesstimate links.

Usage:  python build_diagram.py [train_tree.json] [out.drawio]
Requires Graphviz 'dot' on PATH.

Render step: this only writes the editable .drawio. Turning it into PNG/SVG is a
separate stub (render_diagram.py); those raster/vector outputs are .gitignored
and are NOT committed.
"""
import json, sys, os
from graph_common import (run_dot, transforms, decl, emit_node, emit_edges,
                          group_box, wrap_mxfile, esc)

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), 'train_tree.drawio')

G = json.load(open(SRC))
nodes = [n for n in G['nodes'] if not n.get('id', '').startswith('_')]
edges = G['edges']


# ---------- Guesstimate links (STUB) ----------------------------------------
# Each node will eventually link to its own Guesstimate model, all sharing one
# parameterised template (the "shared logic"): the same donation slate and the
# same E[welfare-adjusted DALY averted / $] formula, with this node's moral
# assumptions dialled in. For now train_tree.json carries `guesstimate: null` on
# every node; when the models exist, drop their URLs there (or resolve them from
# a slug here) and they become the node's clickable target.
#
# Open question for the design: is Guesstimate the right tool, or should the
# shared logic live in Squiggle / a notebook that we snapshot? Left undecided.
def guesstimate_link(n):
    """Return the node's Guesstimate model URL, or '' if not wired up yet."""
    return n.get('guesstimate') or ''  # TODO: point at the shared-logic model per node


for n in nodes:
    link = guesstimate_link(n)
    if link:
        n['link'] = link


# ---------- node sizing (label-driven, so Graphviz reserves real footprint) --
def size(n):
    lines = n['lbl'].split('\n')
    maxc = max(len(x) for x in lines)
    w = max(150, int(maxc * 7.2) + 28)
    h = len(lines) * 16 + 28
    return w, h


# Show the node's argmax donation target under the assumption label, and mark
# subgraph nodes so it is obvious where a child tree will open.
for n in nodes:
    tag = '  ▼' if n.get('subgraph') else ''   # ▼ = click to open sub-tree (TBD)
    n['lbl'] = n['lbl'] + '\n→ ' + n.get('top_pick', '?') + tag
    n['w'], n['h'] = size(n)


# ---------- craziness gradient (calm slate at the top → hot at the bottom) ---
# Colour encodes how far down the train a stop is. Later this can be replaced by
# a real instability metric (how much the ranking swings under a small
# perturbation of that stop's newest parameter).
STOP_STYLE = [
    'fillColor=#dfe7ef;strokeColor=#6b7f96;fontColor=#1b2733;',   # 0 slate
    'fillColor=#cfe6cf;strokeColor=#5a9367;fontColor=#1e3a24;',   # 1 green
    'fillColor=#e6e2c0;strokeColor=#b0a04a;fontColor=#3a3410;',   # 2 olive
    'fillColor=#f6e0c0;strokeColor=#c9932a;fontColor=#5a3f10;',   # 3 amber (first unstable)
    'fillColor=#f2ccc0;strokeColor=#c96a4a;fontColor=#5a2410;',   # 4 clay
    'fillColor=#eeb3b3;strokeColor=#c0392b;fontColor=#5a1410;',   # 5 red (crazy town)
]
NODE_BASE = 'rounded=1;whiteSpace=wrap;html=1;fontSize=11;'
def node_style(n):
    return NODE_BASE + STOP_STYLE[min(n['stop'], len(STOP_STYLE) - 1)]

EBASE = 'edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;strokeColor=#9aa6b3;fontSize=9;fontColor=#5b6675;'
EK = {'expand': 'strokeColor=#8a5fb0;', 'branch': 'strokeColor=#c0392b;dashed=1;'}


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
STOP_COL = ['#6b7f96', '#5a9367', '#b0a04a', '#c9932a', '#c96a4a', '#c0392b']
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
