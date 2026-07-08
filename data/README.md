# `data/` — the single source of truth

Every number in this project lives here, in [`model.json`](model.json), and
nowhere else. The three representations are read from it or generated from it, so
they cannot drift apart:

```
                    data/model.json
        (orgs · coeff_defaults · stops · edges · constants)
                          │
        ┌─────────────────┼───────────────────────────┐
        │ reads           │ generates                  │ generates
        ▼                 ▼                            ▼
   allocate.py    diagram/train_tree.json      squiggle/base_model.squiggle
   (portfolio)    → build_diagram.py → .drawio  squiggle/nodes/*.squiggle
```

## The model is compositional

Every stop carries a `coeffs` record. A stop's resolved coefficients are its
**parent's** coefficients (`coeff_defaults` at the root) with the one-line delta
in its `sets` merged on top. The Squiggle side does exactly this — each node
`import`s its parent node and `Dict.merge`s the same delta — so a branch that
adds one crucial consideration (a discount rate, a `P(nuclear war)`, an override)
is *one line different* from its parent. The mimicry down the tree is real and
deliberate; that is what lets the tree fan out combinatorially without
duplicating a calculation.

The moral circle is **derived** from the resolved coeffs (a domain is counted iff
its weight is positive), so it is not stored a second time.

## Files

- **`model.json`** — canonical data:
  - `coeff_defaults` — the root coefficient record every node starts from:
    per-domain weights `w_*`, `neuron_exponent`, `future_discount`,
    `catastrophe_mult`, `accept_tiny_prob`, `count_soil`, and `override`.
  - `orgs` — the donation slate. Each org has a `domain`, an `x_givewell`
    cost-effectiveness multiple (with a `source` tag and, where published, a
    `source_url`) for the allocator, and either a `daly_per_usd` `[lo, hi]` BOTEC
    or a structured `botec` block (the soup kitchen: people helped × wellbeing
    gain, netted against a bank-account counterfactual) + representative `neurons`
    for the Squiggle models. Animal/invertebrate `x_givewell` figures are copied
    from published EA Forum CEAs; human, future and x-risk figures are
    illustrative placeholders.
  - `stops` — the worldview/branch tree. Each stop declares its `parent`, the
    one-line `sets` delta it applies, its `figures`, `label`, `desc`, and the
    illustrative `top_pick`.
  - `edges` — the crucial-consideration flips. The tree forks at `s3_inverts`
    into a soil-animal branch (**A**) and a longtermist branch (**F**); forks
    again at `s4_future` into discount / nuclear / astronomical siblings; and ends
    past `s5_astro` in two `override` stops — a Boltzmann brain (**B**, every
    charity collapses to one equal pleasant thought) and moral anti-realism
    (**R**, every charity goes negative — better to be selfish).
- **`model.py`** — loader shared by `allocate.py`, `generate.py` and the test;
  owns `resolved_coeffs` (the parent chain) and the soup-kitchen BOTEC.
- **`generate.py`** — regenerates the derived files from `model.json`.
- **`test_sync.py`** — asserts every derived file is byte-identical to what
  `generate.py` would produce, plus the shared invariants (top-picks reference
  real orgs; circles only grow down each branch; edges agree with declared
  parents; every stop resolves to the full coeff schema; the allocator uses the
  same slate). CI runs this on every push and PR (`.github/workflows/sync.yml`).

## Workflow

```bash
# edit data/model.json, then:
python3 data/generate.py        # rewrite diagram + squiggle files
python3 data/test_sync.py       # assert everything is in sync
python3 diagram/build_diagram.py  # rebuild the committed .drawio (needs Graphviz)
```

`python3 data/generate.py --check` reports drift without writing (what CI uses).

## Two lenses, one input

`allocate.py` (x-GiveWell multiples) and the Squiggle models (`wDALY/$` BOTECs)
are deliberately **different valuation lenses over the same orgs and the same
tree**, so their computed winners can differ at a given stop (e.g. at the future
stop the allocator still favours shrimp welfare while the Squiggle model favours
ALLFED). That divergence is the point — it is not drift. What the single source
of truth guarantees is that both lenses rank the *same slate* under the *same
moral circles*; only the numbers each lens applies are its own.
