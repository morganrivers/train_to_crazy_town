#!/usr/bin/env python3
"""
Bottom-line allocator for the train to crazy town.

Prints, for each donation org: its cost-effectiveness (as a multiple of GiveWell
top charities) and its share of a portfolio, under a single
WORLDVIEW-DIVERSIFICATION coefficient.

The orgs, their cost-effectiveness figures, and the worldview/branch tree are
NOT defined here - they are read from data/model.json, the single source of
truth shared with the diagram and the Squiggle models (see data/README.md).

The tree forks after the invertebrate stop into a soil-animal branch (A), where
the sign of the effect on ~10^19 soil nematodes swamps everything and even
reverses which human charities look good, and a longtermist branch (F), which
accepts the astronomical-waste argument and tiny-probability x-risk bets.

Cost-effectiveness numbers for the animal and invertebrate orgs are copied from
published EA Forum cost-effectiveness analyses (cited in data/model.json). Human,
future and x-risk numbers are illustrative placeholders.

  --center W          worldview you lean toward (see --list)
  --diversification D  0 = go all-in on the center worldview's single winner
                       (pure EV-max); higher = spread credence across worldviews
                       by depth, funding the best org in each.
  --animal-weight M    multiplier on animal/invertebrate moral weight (default 1
                       = RP-median; sweep it to watch the ranking flip).
  --list               list the worldviews and exit.

  python3 allocate.py
  python3 allocate.py --center soil --diversification 2
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
import model as M  # noqa: E402

ANIMAL_DOMAINS = M.ANIMAL_DOMAINS
SOIL_X_GIVEWELL = M.CONSTANTS["soil_x_givewell"]
FANATICAL_MULT = M.CONSTANTS["fanatical_mult"]
XRISK_REFUSED_MULT = M.CONSTANTS["xrisk_refused_mult"]

# Short CLI name per stop (drops the "sN_" ordering prefix), e.g. s4_soil -> soil.
def short(stop):
    return stop["id"].split("_", 1)[1]

STOPS_BY_SHORT = {short(s): s for s in M.STOPS}


def cost_effectiveness(stop, animal_weight):
    """x-GiveWell cost-effectiveness of each org under one worldview."""
    circle = set(stop["circle"])
    out = {}
    for org in M.ORGS:
        name, domain, x = org["name"], org["domain"], org["x_givewell"]
        if domain not in circle:
            out[name] = 0.0
            continue
        v = x
        if domain in ANIMAL_DOMAINS:
            v *= animal_weight
        if org["id"] == "amf" and stop["count_soil"]:
            v = SOIL_X_GIVEWELL          # soil-animal reversal (sign uncertain)
        if domain == "xrisk":
            v *= FANATICAL_MULT if stop["accept_tiny_prob"] else XRISK_REFUSED_MULT
        out[name] = v
    return out


def champion(stop, animal_weight):
    ce = cost_effectiveness(stop, animal_weight)
    return max(ce, key=ce.get)


def credences(center, diversification):
    """Credence over worldviews, peaked on the center's depth, widened by
    diversification; worldviews at the same depth share that depth's credence."""
    center_depth = center["stop"]
    if diversification <= 0:
        return {s["id"]: (1.0 if s is center else 0.0) for s in M.STOPS}
    raw = {s["id"]: math.exp(-abs(s["stop"] - center_depth) / diversification)
           for s in M.STOPS}
    z = sum(raw.values())
    return {sid: raw[sid] / z for sid in raw}


def allocate(center, diversification, animal_weight):
    cred = credences(center, diversification)
    alloc = {org["name"]: 0.0 for org in M.ORGS}
    for s in M.STOPS:
        alloc[champion(s, animal_weight)] += cred[s["id"]]
    ew = {org["name"]: 0.0 for org in M.ORGS}
    for s in M.STOPS:
        ce = cost_effectiveness(s, animal_weight)
        for name in ew:
            ew[name] += cred[s["id"]] * ce[name]
    return cred, ew, alloc


def main():
    ap = argparse.ArgumentParser(description="Worldview-diversified donation allocator.")
    ap.add_argument("--center", default="inverts", choices=list(STOPS_BY_SHORT),
                    help="worldview you lean toward (default inverts)")
    ap.add_argument("--diversification", type=float, default=1.0,
                    help="0 = all-in on the center worldview's winner; higher = diversify across worldviews")
    ap.add_argument("--animal-weight", type=float, default=1.0,
                    help="multiplier on animal/invertebrate moral weight (default 1 = RP-median)")
    ap.add_argument("--list", action="store_true", help="list worldviews and exit")
    args = ap.parse_args()

    if args.list:
        print("\nworldviews (depth / branch -> champion at default animal weight):")
        for name, s in STOPS_BY_SHORT.items():
            print(f"  {name:<12} depth {s['stop']} branch {s['branch']:<5} -> {champion(s, 1.0)}")
        print()
        return

    center = STOPS_BY_SHORT[args.center]
    cred, ew, alloc = allocate(center, args.diversification, args.animal_weight)

    print(f"\ncenter: {args.center}   diversification: {args.diversification}   "
          f"animal-weight: {args.animal_weight}\n")
    print("credence over worldviews:")
    for name, s in STOPS_BY_SHORT.items():
        c = cred[s["id"]]
        bar = "#" * int(round(c * 40))
        print(f"  {name:<12} d{s['stop']} {s['branch']:<5} {c*100:5.1f}%  {bar}")

    print("\n{:<34}{:>16}{:>13}".format("org", "x GiveWell (E)", "allocation"))
    print("-" * 63)
    for name in sorted(alloc, key=lambda n: alloc[n], reverse=True):
        print("{:<34}{:>16.4g}{:>12.1f}%".format(name, ew[name], alloc[name] * 100))

    top = max(alloc, key=alloc.get)
    print(f"\nsuggestion: {top}  ({alloc[top]*100:.0f}% of the portfolio)\n")


if __name__ == "__main__":
    main()
