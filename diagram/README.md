# `diagram/` — drawing the tree

Graph-generation code mirroring the Graphviz→draw.io setup in
`morganrivers/iati_webapp` (`docs/diagram/`). Everything here renders
`train_tree.json`, which is **generated from `../assumptions/` by
`../generate.py`** — do not hand-edit it.

## Files

- **`train_tree.json`** — the worldview graph. Nodes are worldviews with a
  `top_pick`, a `squiggle` model path, their accepted assumption numbers, and
  the public `figures` who most prominently articulate the latest assumption.
  Edges add one assumption each; `kind: "override"` marks the dashed-red edges
  into the flat terminal worldviews. Its `pages` field is the render layout
  (see `partition.py`).
- **`partition.py`** — cuts the tree into bounded, clickable **pages** so it
  stays readable as it grows. Greedy largest-chunk-first: a subtree big enough
  for its own page (`≥ min_page`, `≤ max_page`; defaults 8/25, override with
  `DIAGRAM_MIN_PAGE`/`DIAGRAM_MAX_PAGE`) is split off, and on its parent page it
  becomes a single collapsed boundary. Taking the largest fitting chunk first
  keeps pages balanced; the `min_page` floor (and a soft-overflow fallback)
  avoids fragmenting into tiny pages. `generate.py` bakes the result into
  `train_tree.json`; run `python3 partition.py` to print the page layout.
- **`graph_common.py`** — shared primitives: Graphviz `dot` run + plain-format
  parse, coordinate transform, node/edge/band/mxfile emission.
- **`build_diagram.py`** — reads the JSON, lays each page top→bottom with
  Graphviz (root = least crazy, at the top), bands each stop (a node's band =
  its craziest accepted assumption, STOP 0–11, on a 12-colour craziness
  gradient), and writes one editable `.drawio` per page: `train_tree.drawio`
  (root) plus `train_tree__<subtree-root-id>.drawio`. A collapsed boundary is a
  `▼ N more worldviews` node linking to its subtree's page. Prints the public
  read-only draw.io view link for the root page. Requires Graphviz `dot`.
- **`render_diagram.py`** — renders each page to PNG + SVG directly with
  Graphviz (no draw.io app needed): `train_tree.{png,svg}` plus
  `train_tree__<id>.{png,svg}`. All are committed and linked from the top-level
  README via raw.githubusercontent URLs, so they never depend on GitHub Pages.
  Collapsed boundaries in the SVG hyperlink to their subtree page's viewer.
- **`squiggle_playground.py`** — turns a worldview's generated Squiggle model
  into a temporary, no-account playground link. The models are standalone, so
  the whole file is packed into the URL's `#code=` hash
  (`JSON → deflate → base64 → urlencode`, byte-for-byte Squiggle's own
  `playground.ts` encoding). Both the `.drawio` and the SVG carry these links,
  so clicking a node opens its model live and editable; nothing is persisted
  to any account. Run it directly for a per-node link listing + roundtrip
  self-test.

## Regenerating

```bash
python3 ../generate.py           # recompose worldviews -> train_tree.json (+ pages) + models
python3 build_diagram.py         # one editable .drawio per page + printed view link
python3 render_diagram.py        # one PNG + SVG per page
python3 partition.py             # print the page layout (sizes, collapse points)
```

The committed `.drawio` is served read-only by draw.io straight from its raw
GitHub URL (the `#U` hash link `build_diagram.py` prints); override the git ref
in the link with `DIAGRAM_REF=<branch>`. Keep the ref a plain branch name —
draw.io re-parses `raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`
URLs into its GitHub handler, and a `refs/heads/` prefix makes that parse fail
with "File not found".

## CI (`.github/workflows/diagram.yml`)

On every change to `assumptions/` or `diagram/`, the GitHub Action looks at the
assumptions layout, runs the Python chain for each worldview
(`generate.py --check` fails if any committed generated file has drifted),
rebuilds the `.drawio` and the PNG/SVG, asserts the render is a valid image,
and (from the default branch) publishes the images to GitHub Pages at
`https://morganrivers.github.io/train_to_crazy_town/` (needs the one-time
Settings → Pages → Source = "GitHub Actions" setup; the committed raw-URL
images work regardless).
