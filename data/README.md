# `data/` — the single source of truth

Every number in this project lives here, in [`model.json`](model.json), and
nowhere else. The three representations are read from it or generated from it, so
they cannot drift apart:

```
                    data/model.json
                   (orgs · stops · edges · constants)
                          │
        ┌─────────────────┼───────────────────────────┐
        │ reads           │ generates                  │ generates
        ▼                 ▼                            ▼
   allocate.py    diagram/train_tree.json      squiggle/base_model.squiggle
   (portfolio)    → build_diagram.py → .drawio  squiggle/nodes/*.squiggle
```

## Files

- **`model.json`** — canonical data:
  - `orgs` — the donation slate. Each org has a `domain`, an `x_givewell`
    cost-effectiveness multiple (with a `source` tag and, where published, a
    `source_url`) for the allocator, and a `daly_per_usd` `[lo, hi]` BOTEC +
    representative `neurons` for the Squiggle models. Animal/invertebrate
    `x_givewell` figures are copied from published EA Forum CEAs; human, future
    and x-risk figures are illustrative placeholders.
  - `stops` — the worldview/branch tree. Each stop declares its moral `circle`
    (the list of domains it counts — the Squiggle per-domain weights are derived
    from this), the `neuron_exponent`, the `accept_tiny_prob` and `count_soil`
    flags, its `figures`, `label`, `desc`, and the illustrative `top_pick`.
  - `edges` — the crucial-consideration flips. The tree forks at `s3_inverts`
    into a soil-animal branch (**A**) and a longtermist branch (**F**).
- **`model.py`** — loader shared by `allocate.py`, `generate.py` and the test.
- **`generate.py`** — regenerates the derived files from `model.json`.
- **`test_sync.py`** — asserts every derived file is byte-identical to what
  `generate.py` would produce, plus the shared invariants (top-picks reference
  real orgs; circles only grow down each branch; the allocator uses the same
  slate). CI runs this on every push and PR (`.github/workflows/sync.yml`).

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
