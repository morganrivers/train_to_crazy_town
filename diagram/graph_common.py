"""
graph_common.py — shared primitives for laying the crazy-town worldview tree out
with Graphviz `dot` and baking the result into an editable draw.io diagram.

Adapted from the draw.io generators in morganrivers/iati_webapp
(docs/diagram/drawio_common.py): same Graphviz-run + plain-format parse, pixel
coordinate transform, and node/edge/group-box/mxfile emission. Kept here as a
single source of truth so build_diagram.py only has to define the tree's own
stop-banding, colours, and (later) the per-node Guesstimate links.

Node dicts use the schema documented in train_tree.json. Edge dicts use:
from, to, flip (label), kind.
"""
import subprocess, collections, html, os, urllib.parse
from squiggle_playground import playground_url

S = 72.0  # Graphviz points-per-inch → draw.io pixel scale

# ---- single source of layout truth ------------------------------------------
# build_diagram.py (editable .drawio) and render_diagram.py (direct PNG/SVG)
# both feed Graphviz the SAME DOT layout via layout_dot() below, so a node sits
# at the same place in the image and in the .drawio it links to. Only the DRAWING
# stage differs (Graphviz draws the image; draw.io draws the .drawio), so the two
# match structurally without needing draw.io/Electron in CI.

# Craziness gradient (calm slate at the top → hot red → override violet), one
# (fill, stroke, font) hex triple per stop; a worldview's stop is its craziest
# accepted assumption, 0..11. Both renderers derive their colours from this.
GRADIENT = [
    ('#dfe7ef', '#6b7f96', '#1b2733'),   # 0 slate (parochial)
    ('#cfe6cf', '#5a9367', '#1e3a24'),   # 1 green (all humans)
    ('#e6e2c0', '#b0a04a', '#3a3410'),   # 2 olive (animals)
    ('#f2e3b3', '#c9a72a', '#57450e'),   # 3 gold (future, discounted)
    ('#f6e0c0', '#c9932a', '#5a3f10'),   # 4 amber (no discounting)
    ('#f5d3b8', '#cc7a33', '#5a300e'),   # 5 orange (RP animals)
    ('#f2ccc0', '#c96a4a', '#5a2410'),   # 6 clay (suffering)
    ('#eec2a8', '#c65a2e', '#5a2a10'),   # 7 terracotta (meat-eater)
    ('#e9b0a0', '#b8402a', '#511810'),   # 8 rust (net-negative lives)
    ('#eeb3b3', '#c0392b', '#5a1410'),   # 9 red (simulation)
    ('#d7c6e6', '#6a3fa0', '#2c1650'),   # 10 violet (anti-realism)
    ('#c9b3dd', '#4a2a78', '#201040'),   # 11 dark violet (Boltzmann)
]
EDGE_COL = '#9aa6b3'
OVERRIDE_COL = '#c0392b'

# Child-page links use the draw.io viewer + raw-GitHub pattern. Keep REF a plain
# branch name: draw.io re-parses raw.githubusercontent.com/<user>/<repo>/<branch>
# /<path> into its GitHub handler, and extra segments make it read the branch as
# "refs" (File not found).
REPO = 'morganrivers/train_to_crazy_town'
REF = os.environ.get('DIAGRAM_REF', 'main')


def stop_style(s):
    """(fill, stroke, font) hex for a stop, clamped to the gradient's range."""
    return GRADIENT[min(s, len(GRADIENT) - 1)]


def viewer_url(basename):
    """Public read-only draw.io viewer URL for a committed <basename>.drawio."""
    raw = f'https://raw.githubusercontent.com/{REPO}/{REF}/diagram/{basename}.drawio'
    return 'https://viewer.diagrams.net/?lightbox=1&nav=1&chrome=0#U' + urllib.parse.quote(raw, safe='')


def esc(s):
    return html.escape(str(s), quote=True)


def dot_esc(s):
    """Escape a string for a Graphviz double-quoted label."""
    return str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


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
    """Winner + runner-up: each org's lives-saved-equivalent per $1000 and the
    confidence (P it is actually the best buy) the full distributions give."""
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


def compose_label(n, collapsed):
    """The worldview's multi-line label: headline + best-buy/runner-up figures,
    then either a `▼ N more worldviews` fold badge (collapsed boundary) or the
    associated figures. Identical text in both renderers, so node sizes match."""
    lines = [n['lbl']] + pick_lines(n)
    if n['id'] in collapsed:
        lines.append(f"▼ {collapsed[n['id']]['count']} more worldviews")
    else:
        figs = ', '.join(n.get('figures', []))
        if figs:
            lines.append('(' + figs + ')')
    return '\n'.join(lines)


def node_size(label):
    """Fixed (w, h) in px for a node box, sized to hold `label` at 11px."""
    lines = label.split('\n')
    maxc = max(len(x) for x in lines)
    return max(150, int(maxc * 7.2) + 28), len(lines) * 16 + 28


def node_link(n, collapsed):
    """The clickable URL for a node: its Squiggle playground, or (for a collapsed
    boundary) the draw.io viewer of the subtree page it stands for."""
    if n['id'] in collapsed:
        return viewer_url(collapsed[n['id']]['child'])
    return playground_url(n)


def _edge_dot_attr(e):
    """Layout-and-draw attributes for one edge. Only the label affects Graphviz
    layout; colour/style are honoured when Graphviz draws the image and ignored
    by the -Tplain parse build_diagram uses."""
    style = 'dashed' if e.get('kind') == 'override' else 'solid'
    color = OVERRIDE_COL if e.get('kind') == 'override' else EDGE_COL
    label = f', label="{dot_esc(e["label"])}"' if e.get('label') else ''
    return f'style={style}, color="{color}"{label}'


def layout_dot(nodes, edges, collapsed, node_style, ranksep=0.8):
    """Assemble the DOT source that fixes the tree's layout, shared by both
    renderers. `nodes` are this page's node dicts, `edges` its edges, `collapsed`
    its boundary map (id -> {count, child}). `node_style(n, label)` returns the
    per-node drawing attributes (label/colour/href for the image; `label=""` for
    the geometry-only .drawio pass); layout_dot prepends each node's fixed
    width/height so both passes get byte-identical positions.

    Bands are drawn as `STOP k` clusters (with rank=same) AND enforced top-to-
    bottom by invisible funnel nodes, so the ordering is robust even on a page
    whose stops are not directly edge-connected."""
    stops = sorted({n['stop'] for n in nodes})
    by_stop = {s: [n for n in nodes if n['stop'] == s] for s in stops}
    dot = [
        'digraph T{',
        '  rankdir=TB; bgcolor="white"; splines=polyline;',
        f'  nodesep=0.5; ranksep={ranksep}; pad=0.3;',
        '  node[shape=box, fixedsize=true, fontname="Helvetica", fontsize=11,'
        ' style="rounded,filled", margin="0.14,0.08"];',
        '  edge[fontname="Helvetica", fontsize=9, color="%s", fontcolor="#5b6675"];' % EDGE_COL,
    ]
    for s in stops:
        stroke = stop_style(s)[1]
        dot.append(f'  subgraph cluster_stop{s} {{')
        dot.append(f'    label="STOP {s}"; labeljust="l"; fontname="Helvetica-Bold";')
        dot.append(f'    fontsize=13; fontcolor="{stroke}"; color="{stroke}";')
        dot.append('    style="dashed,rounded"; penwidth=2;')
        for n in by_stop[s]:
            label = compose_label(n, collapsed)
            w, h = node_size(label)
            dims = f'width={max(w, 70) / 72.0:.3f}, height={max(h, 30) / 72.0:.3f}'
            # peripheries/penwidth grow a collapsed boundary's footprint, so they
            # must be applied in BOTH passes (they affect layout) — unlike colour
            # or dash style, which each renderer adds in node_style.
            geo = dims + (', peripheries=2, penwidth=2.4' if n['id'] in collapsed else '')
            dot.append(f'    "{n["id"]}"[{geo}, {node_style(n, label)}];')
        same = [n['id'] for n in by_stop[s]]
        if len(same) > 1:
            dot.append('    {rank=same; ' + ' '.join(f'"{i}"' for i in same) + ';}')
        dot.append('  }')
    for i in range(len(stops) - 1):
        z = f'__z{i}'
        dot.append(f'  "{z}"[style=invis, width=0.01, height=0.01, label=""];')
        for n in by_stop[stops[i]]:
            dot.append(f'  "{n["id"]}" -> "{z}"[style=invis];')
        for n in by_stop[stops[i + 1]]:
            dot.append(f'  "{z}" -> "{n["id"]}"[style=invis];')
    ids = {n['id'] for n in nodes}
    for e in edges:
        if e['from'] not in ids or e['to'] not in ids:
            continue
        dot.append(f'  "{e["from"]}" -> "{e["to"]}"[{_edge_dot_attr(e)}];')
    dot.append('}')
    return dot


def lblh(s):
    """Node label with newlines turned into draw.io <br> (HTML-escaped)."""
    return '&lt;br&gt;'.join(esc(x) for x in str(s).split('\n'))


def run_dot(dot_lines):
    """Run Graphviz `dot -Tplain` on the assembled DOT source; return
    (pos, H, edgepts): node centre positions, graph height, per-edge polylines.
    Requires Graphviz `dot` on PATH."""
    plain = subprocess.run(['dot', '-Tplain'], input='\n'.join(dot_lines),
                           capture_output=True, text=True).stdout
    pos = {}
    H = 0.0
    edgepts = collections.defaultdict(list)
    for line in plain.splitlines():
        t = line.split()
        if not t:
            continue
        if t[0] == 'graph':
            H = float(t[3])
        elif t[0] == 'node':
            pos[t[1]] = (float(t[2]), float(t[3]))
        elif t[0] == 'edge':
            n = int(t[3]); c = t[4:4 + 2 * n]
            edgepts[(t[1], t[2])].append([(float(c[2 * i]), float(c[2 * i + 1])) for i in range(n)])
    return pos, H, edgepts


def transforms(H):
    """Return (X, Y) functions mapping Graphviz coords → draw.io pixel coords."""
    return (lambda x: x * S), (lambda y: (H - y) * S)


def decl(n):
    """Fixed-size Graphviz node declaration (label drawn later by draw.io)."""
    return f'"{n["id"]}"[width={max(n["w"],70)/72.0:.3f},height={max(n["h"],30)/72.0:.3f},label=""];'


def node_rect(n, pos, X, Y):
    cx, cy = X(pos[n['id']][0]), Y(pos[n['id']][1])
    return (cx - n['w'] / 2, cy - n['h'] / 2, cx + n['w'] / 2, cy + n['h'] / 2)


GROUP_BOX = ('rounded=1;html=1;dashed=1;dashPattern=6 4;strokeWidth=2;fillColor=none;'
             'verticalAlign=top;align=left;spacingLeft=12;spacingTop=6;fontStyle=1;fontSize=13;')


def group_box(nodes, ids, pos, X, Y, idkey, label, col, cells, pad=22, ptop=30):
    """Append a dotted container box (behind the nodes) enclosing `ids`; return
    its (x0,y0,x1,y1) rect, or None if none of the ids were laid out. Used to
    band the tree by stop / craziness level."""
    ns = [n for n in nodes if n['id'] in ids and n['id'] in pos]
    if not ns:
        return None
    rs = [node_rect(n, pos, X, Y) for n in ns]
    x0 = min(r[0] for r in rs) - pad; y0 = min(r[1] for r in rs) - ptop
    x1 = max(r[2] for r in rs) + pad; y1 = max(r[3] for r in rs) + pad
    st = GROUP_BOX + f'strokeColor={col};fontColor={col};'
    cells.append(f'<mxCell id="{idkey}" value="{esc(label)}" style="{st}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" as="geometry"/></mxCell>')
    return (x0, y0, x1, y1)


def emit_node(n, style, pos, X, Y):
    """Emit one node as a labelled draw.io <object> (with hover tooltip). If the
    node dict carries a 'link' key it becomes the clickable URL for that cell —
    this is the slot the per-node Guesstimate model URL plugs into (see
    build_diagram.guesstimate_link)."""
    x = X(pos[n['id']][0]) - n['w'] / 2
    y = Y(pos[n['id']][1]) - n['h'] / 2
    tip = (f'&lt;b&gt;{esc(n["file"])}&lt;/b&gt;&lt;br&gt;&lt;br&gt;' if n.get('file') else '') + esc(n.get('desc', ''))
    link_attr = f' link="{esc(n["link"])}"' if n.get('link') else ''
    return (f'<object label="{lblh(n["lbl"])}" tooltip="{tip}"{link_attr} id="{n["id"]}">'
            f'<mxCell style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{max(n["w"],70):.0f}" height="{max(n["h"],30):.0f}" as="geometry"/></mxCell></object>')


def emit_edges(edges, edgepts, X, Y, ebase, ek):
    """Emit every edge with Graphviz routing waypoints; `ek` maps edge kind →
    extra style. Returns a list of mxCell strings."""
    out = []
    used = collections.defaultdict(int)
    for i, e in enumerate(edges):
        st = ebase + ek.get(e.get('kind'), '')
        key = (e['from'], e['to']); wp = ''
        if edgepts[key]:
            idx = min(used[key], len(edgepts[key]) - 1); used[key] += 1
            raw = edgepts[key][idx]
            pts = raw[1:-1] if len(raw) > 2 else []
            if pts:
                wp = '<Array as="points">' + ''.join(f'<mxPoint x="{X(px):.0f}" y="{Y(py):.0f}"/>' for px, py in pts) + '</Array>'
        geom = f'<mxGeometry relative="1" as="geometry">{wp}</mxGeometry>'
        val = f' value="{esc(e["label"])}"' if e.get('label') else ''
        out.append(f'<mxCell id="e{i}"{val} style="{st}" edge="1" parent="1" source="{e["from"]}" target="{e["to"]}">'
                   f'{geom}</mxCell>')
    return out


def wrap_mxfile(cells, name, dia_id, page_w=1600, page_h=2400):
    """Wrap emitted cells (already ordered back→front) in the mxfile envelope."""
    return (f'<mxfile host="app.diagrams.net" type="device"><diagram name="{name}" id="{dia_id}">'
            '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
            f'fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0"><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(cells) + '</root></mxGraphModel></diagram></mxfile>')
