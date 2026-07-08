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
    """A child's moral circle contains its parent's - the circle only grows."""
    by_id = {s["id"]: s for s in M.STOPS}
    for e in M.EDGES:
        parent, child = set(by_id[e["from"]]["circle"]), set(by_id[e["to"]]["circle"])
        assert parent <= child, f'{e["to"]} drops a domain its parent {e["from"]} counted'


def test_squiggle_stops_have_full_assumptions():
    """Every stop that claims a Squiggle model has all six domain weights defined."""
    for s in M.squiggle_stops():
        w = M.weights_from_circle(s["circle"])
        assert set(w) == {f"w_{d}" for d in M.SQUIGGLE_WEIGHT_DOMAINS}


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} checks passed - model.json, diagram and squiggle are in sync")


if __name__ == "__main__":
    main()
