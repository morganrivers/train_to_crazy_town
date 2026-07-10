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
  - a prelude of **named parameter distributions** — every genuinely uncertain
    moral parameter the chain applies (discounts, probabilities, multipliers),
    each cited, each editable live in the playground;
  - `scored` — per org, `dist` (its full wDALY/$ distribution: direct-effect
    BOTEC × the chain's moral coefficient, with externalities riding the same
    direct-effect draw) and `wdalyPerUsd` (the exact analytic mean of `dist`);
  - `ranking` — the slate, best first, sorted by `wdalyPerUsd`;
  - `worldviewEv` — **the expected value of that worldview**: what its best buy
    achieves per dollar.

  Distributions are built with the symbolic constructors
  (`Sym.lognormal({p5, p95})`, `Sym.beta`, `Sym.uniform`) rather than
  `lo to hi`, because the runtime samples `to`-built distributions even inside
  `mean()` — which under-estimates heavy-tailed means several-fold — while
  symbolic means are analytic. Uncertain terms are independent by
  construction, so each expectation factorises exactly, and `node run.mjs`
  prints rankings that equal the Python side's `expected_values()` to float
  precision.

These files are generated: edit the assumption files and run
`python3 ../generate.py`, don't hand-edit the `.squiggle` files.
`../test_worldviews.py` (run in CI) fails if a generated file drifts.

Numbers are order-of-magnitude estimates (`Sym.lognormal({p5, p95})` = a
lognormal stated by its two-sided 90% CI) calibrated to published work and
cited on each org in
`../assumptions/0_parochial.py`: GiveWell CEAs; Rethink Priorities / Fischer
welfare ranges; Vasco Grilo's animal-welfare cost-effectiveness analyses;
Denkenberger & Pearce and Linch's x-risk bar for the far-future orgs. The
calibration is chosen so the animals-matter-a-lot worldview (`w1_2_5`)
reproduces Grilo's published DALY/$ figures — shrimp welfare ~64,000× GiveWell,
humane pesticides ~24,000×, chicken campaigns ~460× — and the GiveWell (AMF)
baseline reproduces his ~0.00994 DALY/$. The soup kitchen is a worked BOTEC
whose agreed value is carried unchanged into every worldview.

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
