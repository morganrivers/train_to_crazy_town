#!/usr/bin/env python3
"""
Bottom-line allocator for the train to crazy town.

Prints, for each donation org: its expected cost-effectiveness (as a multiple of
GiveWell top charities) and its share of a portfolio, under a single
WORLDVIEW-DIVERSIFICATION coefficient.

The orgs and the worldview tree are NOT defined here — worldviews are composed
from the numbered assumption files in assumptions/ (the single source of truth
shared with the diagram and the generated Squiggle models). Each worldview is a
chain of assumptions; its per-org expected values come from running the chain's
Python, the same computation the generated Squiggle model performs.

  --center W           worldview you lean toward, by id (see --list), e.g. w1_2_5
  --diversification D  0 = go all-in on the center worldview's single winner
                       (pure EV-max); higher = spread credence across worldviews
                       by how many assumptions they differ in, funding the best
                       org in each.
  --animal-weight M    extra multiplier on animal/invertebrate orgs (default 1;
                       sweep it to watch the ranking flip).
  --list               list the worldviews and exit.

  python3 allocate.py
  python3 allocate.py --center w1_2_5 --diversification 2
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assumptions import worldviews as W  # noqa: E402

VIEWS = W.worldviews()
BY_ID = {w["id"]: w for w in VIEWS}
SLATE = W.slate()
ANIMAL_ORGS = {o["name"] for o in SLATE if o["animal"]}
BASELINE_ORG = "GiveWell top charity (AMF)"
NOTHING = "— nothing (ranking flat)"


def expected_values(view, animal_weight):
    """{org name: E[wDALY/$]} under one worldview, with the CLI animal-weight
    sweep applied on top of the chain's own coefficients."""
    return {name: ev * (animal_weight if name in ANIMAL_ORGS else 1.0)
            for name, ev in view["evs"].items()}


def champion(view, animal_weight):
    """The worldview's best buy, or None when its ranking is flat (overrides)."""
    ev = expected_values(view, animal_weight)
    if min(ev.values()) == max(ev.values()):
        return None
    return max(ev, key=ev.get)


def credences(center, diversification):
    """Credence over worldviews, peaked on the center, falling off with how many
    assumptions two worldviews disagree about (symmetric set difference)."""
    def distance(w):
        return len(set(w["numbers"]) ^ set(center["numbers"]))
    if diversification <= 0:
        return {w["id"]: (1.0 if w is center else 0.0) for w in VIEWS}
    raw = {w["id"]: math.exp(-distance(w) / diversification) for w in VIEWS}
    z = sum(raw.values())
    return {wid: raw[wid] / z for wid in raw}


def allocate(center, diversification, animal_weight):
    cred = credences(center, diversification)
    alloc = {org["name"]: 0.0 for org in SLATE}
    alloc[NOTHING] = 0.0
    ew = {org["name"]: 0.0 for org in SLATE}
    for w in VIEWS:
        best = champion(w, animal_weight)
        alloc[best if best is not None else NOTHING] += cred[w["id"]]
        ev = expected_values(w, animal_weight)
        for name in ew:
            ew[name] += cred[w["id"]] * ev[name]
    return cred, ew, alloc


def main():
    ap = argparse.ArgumentParser(description="Worldview-diversified donation allocator.")
    ap.add_argument("--center", default="w1_2", choices=sorted(BY_ID),
                    metavar="WORLDVIEW",
                    help="worldview you lean toward, by id (default w1_2; see --list)")
    ap.add_argument("--diversification", type=float, default=1.0,
                    help="0 = all-in on the center worldview's winner; higher = diversify")
    ap.add_argument("--animal-weight", type=float, default=1.0,
                    help="extra multiplier on animal/invertebrate orgs (default 1)")
    ap.add_argument("--list", action="store_true", help="list worldviews and exit")
    args = ap.parse_args()

    if args.list:
        print("\nworldviews (id = accepted assumptions; stop = craziest one) -> champion:")
        for w in VIEWS:
            best = champion(w, 1.0) or NOTHING
            print(f"  {w['id']:<16} stop {w['stop']}  {w['file']:<60} -> {best}")
        print()
        return

    center = BY_ID[args.center]
    cred, ew, alloc = allocate(center, args.diversification, args.animal_weight)
    baseline = max(ew[BASELINE_ORG], 1e-30)

    print(f"\ncenter: {args.center} ({center['file']})")
    print(f"diversification: {args.diversification}   animal-weight: {args.animal_weight}\n")
    print("credence over worldviews:")
    for w in VIEWS:
        c = cred[w["id"]]
        if c < 0.005:
            continue
        bar = "#" * int(round(c * 40))
        print(f"  {w['id']:<16} stop {w['stop']} {c*100:5.1f}%  {bar}")

    print("\n{:<34}{:>16}{:>13}".format("org", "x GiveWell (E)", "allocation"))
    print("-" * 63)
    order = sorted(alloc, key=lambda n: alloc[n], reverse=True)
    for name in order:
        x = "" if name == NOTHING else f"{ew[name] / baseline:16.4g}"
        print("{:<34}{:>16}{:>12.1f}%".format(name, x, alloc[name] * 100))

    top = max(alloc, key=alloc.get)
    print(f"\nsuggestion: {top}  ({alloc[top]*100:.0f}% of the portfolio)\n")


if __name__ == "__main__":
    main()
