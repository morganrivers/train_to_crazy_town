# Squiggle models — the shared logic per node

Each get-off point in the worldview tree links to a [Squiggle](https://www.squiggle-language.com)
model. They all share one base model; a node just dials in its own moral
assumptions. The decision rule never changes — every node ranks the **same**
donation slate by **expected welfare-adjusted DALYs averted per dollar
(`wDALY/$`)**. Only the assumptions change, so the winner changes down the train.

## Layout

- **`base_model.squiggle`** — the shared logic. Defines the fixed donation
  slate, the `wDALY/$` formula, and `export evaluate(assumptions)`, which ranks
  the slate under a given assumption record.
- **`nodes/*.squiggle`** — one tiny model per stop. Each does
  `import "../base_model.squiggle" as base` and passes its own `assumptions`
  (moral weight per domain, the animal `neuron_exponent`, the `accept_tiny_prob`
  fanaticism switch) to `base.evaluate`.

The assumption vectors expand the moral circle / turn up the knobs as you
descend: `s0` counts only local humans → `s5` counts everything and accepts
tiny-probability x-risk bets. Editing one number (e.g. `neuron_exponent` in
`nodes/s3_inverts.squiggle`) visibly flips the ranking — that is the instability
the whole project is about.

> **Numbers are placeholder BOTECs**, deliberately stubbed (order-of-magnitude,
> `lo to hi` = lognormal 90% CI). Replace them with sourced estimates (GiveWell
> CEAs; Rethink Priorities / Fischer welfare ranges; standard invertebrate and
> x-risk back-of-envelopes). The MVP *follows* existing work; it invents nothing.

## Run them from this repo

```bash
cd squiggle
npm install
node run.mjs                      # every node
node run.mjs nodes/s3_inverts.squiggle   # just one
```

`run.mjs` is the **load-Squiggle-directly-from-the-repo** path: it hands a
custom linker the local `base_model.squiggle`, so each node's relative `import`
resolves to the file on disk — no Squiggle Hub, no hosting. The same linker
pattern is what you'd give the `@quri/squiggle-components` React player to embed
these models in a web page.

## How the diagram links to a model

`diagram/build_diagram.py` turns each node's `squiggle` path (in
`train_tree.json`) into the node's clickable link. Two modes:

- **Default — raw GitHub link** to the `.squiggle` file. Works today, fully
  auto-populated from the repo; shows the model source.
- **Live model — Squiggle Hub.** Set `SQUIGGLE_HUB_OWNER=<you>` when running the
  build and links point at `https://squigglehub.org/models/<you>/<node-id>`
  instead — a running, editable model. To publish, copy each node's model to Hub
  and change its import to the Hub form, e.g.
  `import "hub:<you>/base_model" as base`. (Imports resolve *relatively* here and
  via a `hub:` linker on Hub; Hub does **not** import arbitrary GitHub URLs.)

## Open question (unchanged)

Guesstimate vs. Squiggle: we went with Squiggle precisely because it's *code* —
one shared `evaluate`, imported by every node, versioned in the repo — rather
than N hand-cloned Guesstimate canvases that drift. If you'd rather each node be
GUI-tweakable, Guesstimate is still an option for the leaf models; the link slot
in `build_diagram.py` is tool-agnostic.
