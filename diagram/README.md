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
  into the flat terminal worldviews.
- **`graph_common.py`** — shared primitives: Graphviz `dot` run + plain-format
  parse, coordinate transform, node/edge/band/mxfile emission.
- **`build_diagram.py`** — reads the JSON, lays the tree top→bottom with
  Graphviz (root = least crazy, at the top), bands each stop (a node's band =
  its craziest accepted assumption, STOP 0–11, on a 12-colour craziness
  gradient), writes the editable `train_tree.drawio`, and prints the public
  read-only draw.io view link. Requires Graphviz `dot` on PATH.
- **`render_diagram.py`** — renders `train_tree.json` → `train_tree.png` +
  `train_tree.svg` directly with Graphviz (no draw.io app needed). Both images
  are committed and linked from the top-level README via their
  raw.githubusercontent URLs, so they never depend on GitHub Pages.
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
python3 ../generate.py           # recompose worldviews -> train_tree.json + models
python3 build_diagram.py         # editable .drawio + printed view link
python3 render_diagram.py        # train_tree.png + train_tree.svg
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
