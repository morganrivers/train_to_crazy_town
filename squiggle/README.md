# Squiggle models — one standalone model per worldview

Each node of the tree links to a [Squiggle](https://www.squiggle-language.com)
model. The decision rule never changes — every worldview ranks the same donation
slate by expected welfare-adjusted DALYs averted per dollar (`wDALY/$`). What
changes is the chain of assumptions behind it, and the models here are that
chain's *output*.

## Layout

- **`worldviews/*.squiggle`** — one model per worldview, **generated** by
  running the Python assumption chain in [`../assumptions/`](../assumptions/)
  (`python3 ../generate.py`). A worldview `w1_2_5` is the composition of
  assumption files `1_far_away_humans.py`, `2_animals_somewhat.py` and
  `5_animals_matter_a_lot.py` on top of the parochial base; the composed
  chain's `squiggle()` renders the model. Each file is **standalone** — no
  imports, no base model — because the composition already happened in Python.
  Every model exports:
  - `scored` — each org's `E[wDALY/$]`: its direct-effect BOTEC times the moral
    coefficient the assumption chain puts on it;
  - `ranking` — the slate, best first;
  - `worldviewEv` — **the expected value of that worldview**: what its best buy
    achieves per dollar.

These files are generated: edit the assumption files and run
`python3 ../generate.py`, don't hand-edit the `.squiggle` files.
`../test_worldviews.py` (run in CI) fails if a generated file drifts.

Numbers are placeholder order-of-magnitude estimates (`lo to hi` = lognormal 90%
CI) traceable to published work: GiveWell CEAs; Rethink Priorities / Fischer
welfare ranges; invertebrate and x-risk estimates (source URLs sit on each org
in `../assumptions/0_parochial.py`). The soup kitchen is a worked BOTEC whose
agreed value is carried unchanged into every worldview.

## Run

```bash
cd squiggle
npm install
node run.mjs                              # every worldview
node run.mjs worldviews/w1_2_5.squiggle   # one worldview
```

Because the models are standalone, `run.mjs` needs no import linker — and the
same files can be pasted into the playground or published to
[Squiggle Hub](https://squigglehub.org) unchanged.

## Where the diagram links point

Each node in the diagram links to a **temporary Squiggle playground** — clicking
it opens that worldview's model live and editable, with no account.
`diagram/squiggle_playground.py` packs the model file into the playground URL
hash (`#code=<deflate+base64>`, byte-for-byte Squiggle's own `playground.ts`
encoding). Nothing is persisted to any account — the whole model travels in the
link.
