#!/usr/bin/env python3
"""
One test that asserts all three representations stay in sync with
data/model.json - the single source of truth.

Runnable two ways:
  python3 data/test_sync.py     # plain, no deps
  pytest data/test_sync.py

The core guarantee: every generated file (diagram/train_tree.json,
squiggle/base_model.squiggle, squiggle/nodes/*.squiggle) is byte-identical to
what data/generate.py would produce right now. So any number changed anywhere
but model.json makes this fail - drift cannot land silently. On top of that we
check the shared invariants the generator does not (orgs referenced by name
actually exist; allocate.py reads the same slate).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import model as M          # noqa: E402
import generate            # noqa: E402


def test_generated_files_are_current():
    """diagram + squiggle files match the generator output (no manual drift)."""
    stale = []
    for path, content in generate.targets().items():
        rel = os.path.relpath(path, ROOT)
        current = open(path).read() if os.path.exists(path) else None
        if current != content:
            stale.append(rel)
    assert not stale, ("stale generated files (run `python3 data/generate.py`): "
                       + ", ".join(stale))


def test_top_picks_reference_real_orgs():
    names = {o["name"] for o in M.ORGS}
    for s in M.STOPS:
        assert s["top_pick"] in names, f'{s["id"]} top_pick {s["top_pick"]!r} not in slate'


def test_allocate_uses_the_canonical_slate():
    """allocate.py ranks exactly the model's orgs - same names, no extra copy."""
    import allocate
    _, ew, _ = allocate.allocate(allocate.STOPS_BY_SHORT["inverts"], 1.0, 1.0)
    assert set(ew) == {o["name"] for o in M.ORGS}


def test_circles_are_monotone_down_each_branch():
    """A child's moral circle contains its parent's - the circle only grows
    (until an override stop, which invalidates every assumption but keeps the
    inherited weights, so it does not shrink the circle either)."""
    for e in M.EDGES:
        parent = set(M.circle(e["from"]))
        child = set(M.circle(e["to"]))
        assert parent <= child, f'{e["to"]} drops a domain its parent {e["from"]} counted'


def test_edge_parents_match_stop_parents():
    """Every edge from->to agrees with the child stop's declared `parent`, so the
    Squiggle import chain and the diagram edges describe the same tree."""
    for e in M.EDGES:
        assert M.stop_by_id(e["to"])["parent"] == e["from"], \
            f'{e["to"]} parent != edge source {e["from"]}'


def test_resolved_coeffs_have_the_full_schema():
    """Every stop resolves to a coeff record with exactly the default keys, so no
    `sets` delta introduces an unknown coefficient the base model won't read."""
    keys = set(M.COEFF_DEFAULTS)
    for s in M.STOPS:
        assert set(M.resolved_coeffs(s)) == keys, f'{s["id"]} coeffs != schema'


def test_soup_kitchen_botec_is_positive():
    """The worked soup-kitchen BOTEC nets out positive (its counterfactual bank
    value is < 1), so the parochial root has a real winner."""
    lo, hi = M.org_daly_per_usd(M.org_by_name("Local soup kitchen"))
    assert 0 < lo <= hi


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} checks passed - model.json, diagram and squiggle are in sync")


if __name__ == "__main__":
    main()
