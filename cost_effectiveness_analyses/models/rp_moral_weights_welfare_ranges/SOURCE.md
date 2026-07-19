# Rethink Priorities — Moral Weight Project welfare ranges (published results)

The species welfare-range estimates from Rethink Priorities' Moral Weight
Project (Fischer et al.). These are the numbers this repo's framework already
uses (e.g. the shrimp welfare range ≈ 0.031 behind the Shrimp Welfare Project
and humane-pesticide BOTECs).

- **Upstream repo:** https://github.com/rethinkpriorities/public_moral_weight_and_sentience
- **Commit vendored:** `eca3901ae0257b286c35af7a91dc405679f1164f`
- **Retrieved:** 2026-07-19
- **License:** none stated upstream. Only the **summary-statistics CSVs**
  (published research *results / data*, a few hundred bytes each) are mirrored
  here for convenience, with attribution. For the model **code** (the
  `wr_simulate.py` / `wr_models.ipynb` Monte-Carlo, ~120 MB of simulation
  outputs) clone the upstream repo — see `../../fetch.sh`.
- **Research area page:**
  https://rethinkpriorities.org/research-area/welfare-range-estimates/

## What is included here

Each CSV is one modelling variant's welfare ranges by species
(mean, 5th / 50th / 95th percentile), for the eleven species RP scored:
pigs, chickens, octopuses, bees, carp, salmon, crayfish, shrimp, crabs,
black soldier flies (bsf), silkworms.

The headline "mixture" / "adjusted" variants are the ones most commonly cited.
Different variants correspond to different judgment calls about which
welfare-relevant proxies to count and how to handle probability of sentience;
picking among them is exactly the kind of moral fork this repo models.

## Related

- Updated Moral Weight Project (distributional sentience):
  https://github.com/rethinkpriorities/updated_moral_weights
- Nuño Sempere's Bayesian adjustment (two-envelope critique), already cited in
  this repo's README:
  https://nunosempere.com/blog/2023/02/19/bayesian-adjustment-to-rethink-priorities-welfare-range-estimates/
