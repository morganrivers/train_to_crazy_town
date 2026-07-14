#!/usr/bin/env python3
"""
Build editable draw.io diagrams of the *train to crazy town* worldview tree from
train_tree.json (generated from assumptions/ by generate.py), using Graphviz for
a top-to-bottom layered layout (root = least crazy, at the top). Mirrors the
setup in morganrivers/iati_webapp (docs/diagram/build_webapp_drawio.py): all
layout/emit machinery is shared via graph_common.py.

The layout DOT is the SHARED graph_common.layout_dot, the exact same source
render_diagram.py feeds to Graphviz for the PNG/SVG — so every node lands in the
same place in the image and in the .drawio it links to. Here the layout is read
back with `dot -Tplain` and re-emitted as editable draw.io cells (node labels,
stop bands, edge routing) rather than drawn by Graphviz.

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
import json, sys, os
from graph_common import (run_dot, transforms, emit_node, emit_edges, group_box,
                          wrap_mxfile, layout_dot, stop_style, compose_label,
                          node_size, node_link, viewer_url)

HERE = os.path.dirname(__file__)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'train_tree.drawio')
OUTDIR = os.path.dirname(OUT) or '.'

G = json.load(open(SRC))
NODES = {n['id']: n for n in G['nodes'] if not n.get('id', '').startswith('_')}
EDGES = G['edges']
PAGES = G['pages']

# draw.io node/edge styling (the DRAWING stage; layout is shared upstream). The
# fill/stroke/font come from graph_common.stop_style so colours never drift from
# the image renderer.
NODE_BASE = 'rounded=1;whiteSpace=wrap;html=1;fontSize=11;'
# A collapsed boundary gets a bold dashed border + fold hint so it reads as
# "there is more behind this — click to open its page".
COLLAPSE_EXTRA = 'dashed=1;dashPattern=8 4;strokeWidth=3;fontStyle=1;'

EBASE = 'edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;strokeColor=#9aa6b3;fontSize=9;fontColor=#5b6675;'
EK = {'expand': 'strokeColor=#8a5fb0;', 'override': 'strokeColor=#c0392b;dashed=1;'}


def drawio_fill(s):
    """draw.io style fragment for a stop's colours, from the shared gradient."""
    fill, stroke, font = stop_style(s)
    return f'fillColor={fill};strokeColor={stroke};fontColor={font};'


def prepare(nid, collapsed):
    """A render-ready copy of a node for one page: its shared label + size + link.
    Collapsed boundaries advertise their hidden subtree and link to its page."""
    n = dict(NODES[nid])
    n['lbl'] = compose_label(n, collapsed)
    n['w'], n['h'] = node_size(n['lbl'])
    if nid in collapsed:
        n['collapsed'] = True
    link = node_link(n, collapsed)
    if link:
        n['link'] = link
    return n


def build_page(page):
    collapsed = page['collapsed']
    nodes = [prepare(nid, collapsed) for nid in page['nodes']]
    edges = [e for e in EDGES if e['from'] in set(page['nodes']) and e['to'] in set(page['nodes'])]

    # Layout via the SHARED DOT (geometry only: empty labels, sizes already fixed
    # by node_size), read back as coordinates and re-drawn as draw.io cells.
    dot = layout_dot(nodes, edges, collapsed, lambda n, label: 'label=""')
    pos, Hgt, edgepts = run_dot(dot)
    X, Y = transforms(Hgt)

    stops = sorted({n['stop'] for n in nodes})
    by_stop = {s: [n['id'] for n in nodes if n['stop'] == s] for s in stops}
    bg, fg = [], []
    for s in stops:
        col = stop_style(s)[1]
        group_box(nodes, set(by_stop[s]), pos, X, Y, f'band_{s}', f'STOP {s}', col, bg)
    for n in nodes:
        if n['id'] in pos:
            style = NODE_BASE + drawio_fill(n['stop'])
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
