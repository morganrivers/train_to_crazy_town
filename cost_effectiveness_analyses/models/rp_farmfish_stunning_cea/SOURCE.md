# Rethink Priorities — Farmed finfish stunning CEA (vendored snapshot)

Prospective cost-effectiveness analysis of a farmed-finfish stunning
intervention in Europe (electrical stunning corporate commitments).

- **Upstream repo:** https://github.com/rethinkpriorities/farmfish_stunning_cea
- **Commit vendored:** `c0d58a8c4f8f1bee215a002f671895241a52b45d`
- **Retrieved:** 2026-07-19
- **License:** MIT (Copyright (c) 2024 Rethink Priorities) — see `LICENSE`
- **EA Forum write-up (Vasco Grilo linkpost):**
  https://forum.effectivealtruism.org/posts/hXH2KbPK29zxKBRGC/linkpost-prospective-cost-effectiveness-of-farmed-fish

## What is included here

Only the **source** of the model is vendored, to keep the snapshot small:

- `2_code/` — the R + Quarto model. Read in dependency order:
  - `b_fish_assumptions.R` — species / production parameters
  - `c_model_assumptions.R` — intervention + pain-track assumptions
  - `a_functions.R` — the calculation functions
  - `*.qmd` — the report documents that render the results
- `UPSTREAM_README.md`, `LICENSE`

The large `1_input_data/`, `3_intermediate_data/`, `4_charts/` and rendered
`*.html` reports were **not** vendored (they are regenerable from the code, and
keep this directory lightweight). Clone the upstream repo for the full artifact.

## Relation to this repo's framework

This is a worked, per-org direct-effect CEA in a beneficiary's own welfare
units (fish welfare-adjusted suffering averted per unit spent) — structurally
the same object as a `botecs/*.py` entry here.
