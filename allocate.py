#!/usr/bin/env python3
"""
Bottom-line allocator for the train to crazy town.

Prints, for each donation org: its cost-effectiveness (as a multiple of GiveWell
top charities) and its share of a portfolio, under a single
WORLDVIEW-DIVERSIFICATION coefficient.

The tree now forks. A shared trunk (local -> all humans -> farmed animals ->
invertebrates) splits into:
  - branch A (biological micro-minds): counting wild animals and soil animals,
    where the sign of the effect on ~10^19 soil nematodes swamps everything and
    even reverses which human charities look good;
  - branch F (longtermist): accepting the astronomical-waste argument and
    tiny-probability x-risk bets.
(The digital-minds / AI-sentience branch is intentionally left out: there are no
comparable published cost-effectiveness estimates to copy, so it is not
fabricated.)

Cost-effectiveness numbers for the animal and invertebrate orgs are copied from
published EA Forum cost-effectiveness analyses (cited inline). Human, future and
x-risk numbers are illustrative placeholders, marked below.

  --center W          worldview you lean toward (see --list)
  --diversification D  0 = go all-in on the center worldview's single winner
                       (pure EV-max); higher = spread credence across worldviews
                       by depth, funding the best org in each.
  --animal-weight M    multiplier on animal/invertebrate moral weight (default 1
                       = RP-median; sweep it to watch the ranking flip).
  --list               list the worldviews and exit.

  python3 allocate.py
  python3 allocate.py --center soil_nematodes --diversification 2
"""
import argparse
import math

# --- donation slate: cost-effectiveness as a MULTIPLE of GiveWell top charities.
# Animal / invertebrate figures are copied from published EA Forum analyses:
#   The Humane League (corporate campaigns for chicken welfare): 1.51e3x
#     https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken
#   Shrimp Welfare Project (Humane Slaughter Initiative): 639 DALY/$ = 6.43e4x
#     https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane
#   Wild insects (paying farmers to use humane pesticides): 236 DALY/$ = 2.37e4x
#     https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane
# Human numbers (Rotary, GiveDirectly, AIM) and future/x-risk numbers are
# illustrative placeholders, not from those analyses.
# name, domain, x_givewell (multiple of GiveWell top charities), source_tag
SLATE = [
    ("Local Rotary Club",               "local",       0.01,    "placeholder"),
    ("GiveDirectly",                    "global",      0.1,     "placeholder"),
    ("GiveWell (AMF)",                  "global",      1.0,     "baseline"),
    ("AIM / Charity Entrep.",           "global",      2.0,     "placeholder"),
    ("The Humane League",               "farmed",      1.51e3,  "published"),
    ("Shrimp Welfare Project",          "invert",      6.43e4,  "published"),
    ("Wild insects (humane pesticides)", "wild_invert", 2.37e4, "published"),
    ("ALLFED",                          "future",      3.0,     "placeholder"),
    ("AI safety (Redwood Research)",    "xrisk",       5.0,     "placeholder"),
]

# Counting soil animals, GiveWell top charities' cropland effect works out to
# ~1.11 kQALY/$ ~= 1.74x the SWP Humane Slaughter Initiative -- so on branch A
# the "normal" human charity leaps to ~1.11e5x GiveWell's own direct value, and
# its SIGN is uncertain (it could be net-negative for soil nematodes).
#   https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane
SOIL_X_GIVEWELL = 1.11e5

ANIMAL_DOMAINS = {"farmed", "invert", "wild_invert"}
FANATICAL_MULT = 1e6  # placeholder multiplier x-risk claims once tiny-prob bets are accepted

# worldview -> (depth, branch, in-circle domains, flags)
WORLDVIEWS = {
    "parochial":      (0, "trunk", {"local"},                                            {}),
    "all_humans":     (1, "trunk", {"local", "global"},                                  {}),
    "farmed":         (2, "trunk", {"local", "global", "farmed"},                        {}),
    "invertebrates":  (3, "trunk", {"local", "global", "farmed", "invert"},              {}),
    "soil_nematodes": (4, "A",     {"local", "global", "farmed", "invert", "wild_invert"},
                       {"count_soil": True}),
    "astronomical":   (4, "F",     {"local", "global", "farmed", "invert", "wild_invert",
                                    "future", "xrisk"}, {"accept_tiny_prob": True}),
}


def cost_effectiveness(worldview, animal_weight):
    """x-GiveWell cost-effectiveness of each org under one worldview."""
    _, _, circle, flags = WORLDVIEWS[worldview]
    out = {}
    for name, domain, x, _tag in SLATE:
        if domain not in circle:
            out[name] = 0.0
            continue
        v = x
        if domain in ANIMAL_DOMAINS:
            v *= animal_weight
        if name == "GiveWell (AMF)" and flags.get("count_soil"):
            v = SOIL_X_GIVEWELL          # soil-animal reversal (sign uncertain)
        if domain == "xrisk":
            v *= FANATICAL_MULT if flags.get("accept_tiny_prob") else 1e-6
        out[name] = v
    return out


def champion(worldview, animal_weight):
    ce = cost_effectiveness(worldview, animal_weight)
    return max(ce, key=ce.get)


def credences(center, diversification):
    """Credence over worldviews, peaked on the center's depth, widened by
    diversification; worldviews at the same depth share that depth's credence."""
    center_depth = WORLDVIEWS[center][0]
    if diversification <= 0:
        return {w: (1.0 if w == center else 0.0) for w in WORLDVIEWS}
    raw = {w: math.exp(-abs(WORLDVIEWS[w][0] - center_depth) / diversification)
           for w in WORLDVIEWS}
    z = sum(raw.values())
    return {w: raw[w] / z for w in WORLDVIEWS}


def allocate(center, diversification, animal_weight):
    cred = credences(center, diversification)
    alloc = {name: 0.0 for name, *_ in SLATE}
    for w in WORLDVIEWS:
        alloc[champion(w, animal_weight)] += cred[w]
    ew = {name: 0.0 for name, *_ in SLATE}
    for w in WORLDVIEWS:
        ce = cost_effectiveness(w, animal_weight)
        for name in ew:
            ew[name] += cred[w] * ce[name]
    return cred, ew, alloc


def main():
    ap = argparse.ArgumentParser(description="Worldview-diversified donation allocator.")
    ap.add_argument("--center", default="invertebrates", choices=list(WORLDVIEWS),
                    help="worldview you lean toward (default invertebrates)")
    ap.add_argument("--diversification", type=float, default=1.0,
                    help="0 = all-in on the center worldview's winner; higher = diversify across worldviews")
    ap.add_argument("--animal-weight", type=float, default=1.0,
                    help="multiplier on animal/invertebrate moral weight (default 1 = RP-median)")
    ap.add_argument("--list", action="store_true", help="list worldviews and exit")
    args = ap.parse_args()

    if args.list:
        print("\nworldviews (depth / branch -> champion at default animal weight):")
        for w, (d, b, _c, _f) in WORLDVIEWS.items():
            print(f"  {w:<15} depth {d} branch {b:<5} -> {champion(w, 1.0)}")
        print()
        return

    cred, ew, alloc = allocate(args.center, args.diversification, args.animal_weight)

    print(f"\ncenter: {args.center}   diversification: {args.diversification}   "
          f"animal-weight: {args.animal_weight}\n")
    print("credence over worldviews:")
    for w, (d, b, _c, _f) in WORLDVIEWS.items():
        bar = "#" * int(round(cred[w] * 40))
        print(f"  {w:<15} d{d} {b:<5} {cred[w]*100:5.1f}%  {bar}")

    print("\n{:<34}{:>16}{:>13}".format("org", "x GiveWell (E)", "allocation"))
    print("-" * 63)
    for name in sorted(alloc, key=lambda n: alloc[n], reverse=True):
        print("{:<34}{:>16.4g}{:>12.1f}%".format(name, ew[name], alloc[name] * 100))

    top = max(alloc, key=alloc.get)
    print(f"\nsuggestion: {top}  ({alloc[top]*100:.0f}% of the portfolio)\n")


if __name__ == "__main__":
    main()
