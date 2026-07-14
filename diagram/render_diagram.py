#!/usr/bin/env python3
"""
render_diagram.py — render the train-to-crazy-town tree straight to PNG + SVG.

Reads the same train_tree.json that build_diagram.py uses and lays the tree out
with Graphviz via the SHARED layout in graph_common.layout_dot (root = least
crazy, at the top), so a node sits in the same place here as in the editable
.drawio that build_diagram.py emits. This pass hands the shared DOT to
`dot -Tpng/-Tsvg`, letting Graphviz both lay out and draw it, so it needs
nothing but Graphviz `dot` on PATH — no draw.io app, no Electron.

The tree is cut into bounded, clickable PAGES (train_tree.json's `pages`); this
renders one PNG + SVG per page. The root page keeps the given basename; each
collapsed subtree gets `<basename>__<subtree-root-id>.{png,svg}`. A collapsed
boundary node is drawn with a `▼ N more worldviews` badge and hyperlinks to its
subtree page's draw.io viewer, so the SVG is a navigable, zoom-in map. The root
PNG + SVG are committed and linked from the README via raw.githubusercontent
URLs, so the images never depend on GitHub Pages being enabled.

Usage:  python render_diagram.py [train_tree.json] [out_basename]
        # writes <out_basename>.png/.svg plus <out_basename>__<id>.png/.svg
Requires Graphviz `dot` on PATH.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graph_common import layout_dot, stop_style, node_link, dot_esc

HERE = os.path.dirname(__file__)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'train_tree.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'train_tree')
OUTDIR = os.path.dirname(OUT) or '.'
BASE = os.path.basename(OUT)


def node_style(collapsed):
    """Per-node Graphviz drawing attributes for the image: colour from the stop
    gradient, the clickable link, and a double dashed border for a collapsed
    boundary. Returns a closure over this page's collapsed-boundary map."""
    def style(n, label):
        fill, stroke, font = stop_style(n['stop'])
        url = node_link(n, collapsed)
        href = f' URL="{dot_esc(url)}", target="_blank"' if url else ''
        extra = ', style="rounded,filled,dashed"' if n['id'] in collapsed else ''
        return (f'label="{dot_esc(label)}", fillcolor="{fill}",'
                f' color="{stroke}", fontcolor="{font}"{href}{extra}')
    return style


def render_page(page, nodes_by_id, edges):
    nodes = [nodes_by_id[i] for i in page['nodes']]
    src = '\n'.join(layout_dot(nodes, edges, page['collapsed'], node_style(page['collapsed'])))

    basename = BASE if page['is_root'] else page['id']
    for fmt in ('png', 'svg'):
        out = os.path.join(OUTDIR, f'{basename}.{fmt}')
        p = subprocess.run(['dot', f'-T{fmt}', '-o', out],
                           input=src, text=True, capture_output=True)
        if p.returncode != 0:
            sys.stderr.write(p.stderr)
            sys.exit(p.returncode)
        print(f'wrote {out}')


def main():
    G = json.load(open(SRC))
    nodes_by_id = {n['id']: n for n in G['nodes'] if not n.get('id', '').startswith('_')}
    for page in G['pages']:
        render_page(page, nodes_by_id, G['edges'])


if __name__ == '__main__':
    main()
