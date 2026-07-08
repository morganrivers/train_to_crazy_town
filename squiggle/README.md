# Squiggle models — the shared logic per node

Each get-off point links to a [Squiggle](https://www.squiggle-language.com)
model. They share one base model; a node sets its own moral assumptions. The
decision rule never changes — every node ranks the same donation slate by
expected welfare-adjusted DALYs averted per dollar (`wDALY/$`). Only the
assumptions change, so the winner changes down the train.

## Layout

- **`base_model.squiggle`** — the shared logic. Defines the fixed donation
  slate, the `wDALY/$` formula, and `export evaluate(assumptions)`, which ranks
  the slate under a given assumption record.
- **`nodes/*.squiggle`** — one model per stop. Each does
  `import "hub:morganrivers/base_model" as base` and passes its own `assumptions`
  (moral weight per domain, the animal `neuron_exponent`, the `accept_tiny_prob`
  switch) to `base.evaluate`.

Editing one number (e.g. `neuron_exponent` in `nodes/s3_inverts.squiggle`) flips
the ranking — the instability the project shows.

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

## Hub

The models live on Squiggle Hub under `morganrivers` (`base_model` and one per
node id). Each node's diagram link points to
`https://squigglehub.org/models/morganrivers/<node-id>`.
