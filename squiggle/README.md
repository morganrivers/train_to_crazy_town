# Squiggle models — the shared logic per node

Each get-off point links to a [Squiggle](https://www.squiggle-language.com)
model. They share one base model; a node sets its own moral assumptions. The
decision rule never changes — every node ranks the same donation slate by
expected welfare-adjusted DALYs averted per dollar (`wDALY/$`). Only the
assumptions change, so the winner changes down the train.

## Layout

- **`base_model.squiggle`** — the shared logic. Defines the fixed slate, the root
  coefficient record (`export defaults`), the soup-kitchen worked BOTEC, and
  `export evaluate(c)`, which ranks the slate under a coefficient record `c`.
  Three blocks (between the `GENERATED SOUP KITCHEN BOTEC`, `GENERATED SLATE` and
  `GENERATED DEFAULTS` markers) are generated from
  [`../data/model.json`](../data/model.json); the `evaluate` logic around them is
  hand-written.
- **`nodes/*.squiggle`** — one model per stop, **generated** from
  `../data/model.json`, forming an **import chain**. Each node does
  `import "hub:morganrivers/base_model" as base` **and** imports its parent node
  (`import "hub:morganrivers/<parent-id>" as parent`), then builds its own
  coefficients by merging a one-line delta onto the parent's:
  `export coeffs = Dict.merge(parent.coeffs, { w_farmed: 1 })`. The root starts
  from `base.defaults`. Finally `ranking = base.evaluate(coeffs)`.

So a branch that adds one crucial consideration is one `Dict.merge` line
different from its parent. The `override` coefficient replaces the whole result:
`"boltzmann"` sets every charity to one equal pleasant thought, `"antirealist"`
makes every charity negative.

These files are generated: edit `../data/model.json` and run
`python3 ../data/generate.py`, don't hand-edit the `.squiggle` files. Changing
one number (e.g. `neuron_exponent` in the `s3_inverts` `sets`) flips the
ranking — the instability the project shows. `../data/test_sync.py` fails if a
generated file drifts from the model.

Numbers are placeholder order-of-magnitude estimates (`lo to hi` = lognormal 90%
CI) traceable to published work: GiveWell CEAs; Rethink Priorities / Fischer
welfare ranges; invertebrate and x-risk estimates. The soup kitchen is a worked
BOTEC whose agreed value is imported unchanged by every node below the root.

## Run

```bash
cd squiggle
npm install
node run.mjs                             # every node
node run.mjs nodes/s3_inverts.squiggle   # one node
```

`run.mjs` maps every Hub import name (`hub:morganrivers/base_model` and
`hub:morganrivers/<node-id>`) to the local file through a custom linker, so the
import chain resolves on disk and the same files publish to Squiggle Hub
unchanged. The same linker feeds the `@quri/squiggle-components` React player.

## Where the diagram links point

Each node in the diagram links to its model's **source file here on GitHub**
(`squiggle/nodes/<node-id>.squiggle`) — a reliable target that needs no account,
shows the real model with its comments, and runs locally with `node run.mjs`
(above).

To get the interactive calculator instead, publish the models to
[Squiggle Hub](https://squigglehub.org) under your own account (`base_model`
plus one per node id) and repoint the links by setting the hub owner in
`diagram/build_diagram.py` — the files import `hub:<owner>/base_model`, so they
publish unchanged.
