#!/usr/bin/env python3
"""
render_diagram.py — render the train-to-crazy-town tree straight to PNG + SVG.

Reads the same train_tree.json that build_diagram.py uses and lays the tree out
top-to-bottom with Graphviz (root = least crazy, at the top), colouring each stop
on the craziness gradient and banding it into a "STOP k" cluster. Unlike
build_diagram.py (which emits an editable .drawio for draw.io to render), this
writes the raster/vector images directly, so it needs nothing but Graphviz `dot`
on PATH — no draw.io app, no Electron.

The two outputs are committed to the repo and linked from the README via their
raw.githubusercontent URLs, so the images never depend on GitHub Pages being
enabled.

Usage:  python render_diagram.py [train_tree.json] [out_basename]
        # writes <out_basename>.png and <out_basename>.svg (default: train_tree)
Requires Graphviz `dot` on PATH.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from squiggle_playground import playground_url

HERE = os.path.dirname(__file__)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'train_tree')

# (fill, stroke/border, font) per stop — the craziness gradient shared with
# build_diagram.py (calm slate at the top → hot red → override violet). A
# worldview's stop is its craziest accepted assumption, 0..9.
STOP_STYLE = [
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


def esc(s):
    """Escape a string for a Graphviz double-quoted label."""
    return str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


def node_label(n):
    """Worldview headline (latest assumption + accepted chain), its argmax
    donation target, and the figure(s) who articulate the latest assumption —
    same composition build_diagram.py bakes into draw.io."""
    figs = ', '.join(n.get('figures', []))
    label = n['lbl'] + '\n→ ' + n.get('top_pick', '?')
    if figs:
        label += '\n(' + figs + ')'
    return label


def main():
    G = json.load(open(SRC))
    nodes = [n for n in G['nodes'] if not n.get('id', '').startswith('_')]
    edges = G['edges']
    stops = sorted({n['stop'] for n in nodes})

    dot = [
        'digraph T{',
        '  rankdir=TB; bgcolor="white"; splines=polyline;',
        '  nodesep=0.5; ranksep=0.8; pad=0.3;',
        '  node[shape=box, style="rounded,filled", fontname="Helvetica",'
        ' fontsize=11, margin="0.14,0.08"];',
        '  edge[fontname="Helvetica", fontsize=9, color="#9aa6b3",'
        ' fontcolor="#5b6675"];',
    ]

    # One dashed "STOP k" band per stop, enclosing every node at that depth.
    for s in stops:
        fill, stroke, _ = STOP_STYLE[min(s, len(STOP_STYLE) - 1)]
        dot.append(f'  subgraph cluster_stop{s} {{')
        dot.append(f'    label="STOP {s}"; labeljust="l"; fontname="Helvetica-Bold";')
        dot.append(f'    fontsize=13; fontcolor="{stroke}"; color="{stroke}";')
        dot.append('    style="dashed,rounded"; penwidth=2;')
        for n in nodes:
            if n['stop'] == s:
                fill, stroke, font = STOP_STYLE[min(n['stop'], len(STOP_STYLE) - 1)]
                # Same temporary-playground link the .drawio uses, so the SVG is
                # clickable too (opens the node's model, editable, no account).
                url = playground_url(n)
                href = f' URL="{esc(url)}", target="_blank"' if url else ''
                dot.append(
                    f'    "{n["id"]}"[label="{esc(node_label(n))}",'
                    f' fillcolor="{fill}", color="{stroke}", fontcolor="{font}"{href}];')
        # keep every worldview that rides to the same stop on one visual band
        same = [n['id'] for n in nodes if n['stop'] == s]
        if len(same) > 1:
            dot.append('    {rank=same; ' + ' '.join(f'"{i}"' for i in same) + ';}')
        dot.append('  }')

    for e in edges:
        style = 'dashed' if e.get('kind') == 'override' else 'solid'
        color = '#c0392b' if e.get('kind') == 'override' else '#9aa6b3'
        label = f', label="{esc(e["label"])}"' if e.get('label') else ''
        dot.append(f'  "{e["from"]}" -> "{e["to"]}"'
                   f'[style={style}, color="{color}"{label}];')

    dot.append('}')
    src = '\n'.join(dot)

    for fmt in ('png', 'svg'):
        out = f'{OUT}.{fmt}'
        p = subprocess.run(['dot', f'-T{fmt}', '-o', out],
                           input=src, text=True, capture_output=True)
        if p.returncode != 0:
            sys.stderr.write(p.stderr)
            sys.exit(p.returncode)
        print(f'wrote {out}')


if __name__ == '__main__':
    main()
