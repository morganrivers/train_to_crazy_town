# Squiggle models — the shared logic per node

Each get-off point links to a [Squiggle](https://www.squiggle-language.com)
model. They share one base model; a node sets its own moral assumptions. The
decision rule never changes — every node ranks the same donation slate by
expected welfare-adjusted DALYs averted per dollar (`wDALY/$`). Only the
assumptions change, so the winner changes down the train.

## Layout

- **`base_model.squiggle`** — the shared logic. Defines the `wDALY/$` formula and
  `export evaluate(assumptions)`, which ranks the slate under a given assumption
  record. Its `slate = [...]` block (between the `GENERATED SLATE` markers) is
  generated from [`../data/model.json`](../data/model.json); the logic around it
  is hand-written.
- **`nodes/*.squiggle`** — one model per stop, **generated** from
  `../data/model.json`. Each does `import "hub:morganrivers/base_model" as base`
  and passes its own `assumptions` (moral weight per domain — derived from the
  stop's moral circle — plus the animal `neuron_exponent` and the
  `accept_tiny_prob` switch) to `base.evaluate`.

These files are generated: edit `../data/model.json` and run
`python3 ../data/generate.py`, don't hand-edit the `.squiggle` files. Changing
one number (e.g. `neuron_exponent` for `s3_inverts` in `model.json`) flips the
ranking — the instability the project shows. `../data/test_sync.py` fails if a
generated file drifts from the model.

Numbers are placeholder order-of-magnitude estimates (`lo to hi` = lognormal 90%
CI) traceable to published work: GiveWell CEAs; Rethink Priorities / Fischer
welfare ranges; invertebrate and x-risk estimates.

## Run

```bash
cd squiggle
npm install
node run.mjs                             # every node
node run.mjs nodes/s3_inverts.squiggle   # one node
```

`run.mjs` maps the Hub import name `hub:morganrivers/base_model` to the local
`base_model.squiggle` through a custom linker, so the same files publish to
Squiggle Hub unchanged and run here on disk. The same linker feeds the
`@quri/squiggle-components` React player.

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
