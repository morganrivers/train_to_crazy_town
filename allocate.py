#!/usr/bin/env python3
"""
Bottom-line allocator for the train to crazy town.

Prints, for each donation org: its expected welfare-adjusted DALYs per dollar
(wDALY/$) and the share of a portfolio it should get, under a single
WORLDVIEW-DIVERSIFICATION coefficient.

The coefficient models how Open Phil actually diversifies: you are uncertain
which stop on the train is the right place to get off, so you hold credence
across the worldviews (stops) and fund the best org in each, weighted by that
credence.

  --center C          the stop you lean toward (0..5)
  --diversification D  0 = go all-in on the center worldview's single winner
                       (pure EV-max); higher = spread credence across worldviews,
                       so orgs that win under more worldviews accumulate share.

  python3 allocate.py                          # defaults
  python3 allocate.py --center 4 --diversification 2

The slate numbers and worldview assumption vectors mirror
squiggle/base_model.squiggle and squiggle/nodes/*.squiggle -- keep them in sync.
Numbers are placeholder order-of-magnitude estimates.
"""
import argparse
import math

HUMAN_NEURONS = 8.6e10

# name, domain, (lo, hi) = daly/$ 90% CI, representative neurons
SLATE = [
    ("Local Rotary Club",           "local_human",   (0.0002, 0.002),  HUMAN_NEURONS),
    ("GiveDirectly",                "global_human",  (0.005, 0.02),    HUMAN_NEURONS),
    ("GiveWell (AMF)",              "global_human",  (0.02, 0.1),      HUMAN_NEURONS),
    ("AIM / Charity Entrep.",       "global_human",  (0.05, 0.3),      HUMAN_NEURONS),
    ("The Humane League",           "farmed_animal", (1, 30),          2.2e8),
    ("Shrimp Welfare Project",      "invertebrate",  (10, 5000),       1e5),
    ("ALLFED",                      "future_human",  (0.01, 100),      HUMAN_NEURONS),
    ("AI safety (Redwood Research)", "xrisk_future", (0.001, 1e6),     HUMAN_NEURONS),
]

# stop -> moral assumption vector (mirror of squiggle/nodes/*.squiggle)
WORLDVIEWS = {
    0: dict(w_local=1, w_global=0, w_farmed=0, w_invert=0, w_future=0, w_xrisk=0, neuron_exponent=0,   accept_tiny_prob=False),
    1: dict(w_local=1, w_global=1, w_farmed=0, w_invert=0, w_future=0, w_xrisk=0, neuron_exponent=0,   accept_tiny_prob=False),
    2: dict(w_local=1, w_global=1, w_farmed=1, w_invert=0, w_future=0, w_xrisk=0, neuron_exponent=0.5, accept_tiny_prob=False),
    3: dict(w_local=1, w_global=1, w_farmed=1, w_invert=1, w_future=0, w_xrisk=0, neuron_exponent=0.4, accept_tiny_prob=False),
    4: dict(w_local=1, w_global=1, w_farmed=1, w_invert=1, w_future=1, w_xrisk=0, neuron_exponent=0.4, accept_tiny_prob=False),
    5: dict(w_local=1, w_global=1, w_farmed=1, w_invert=1, w_future=1, w_xrisk=1, neuron_exponent=0.4, accept_tiny_prob=True),
}
STOP_NAME = {0: "parochial", 1: "all humans", 2: "farmed animals",
             3: "invertebrates", 4: "future people", 5: "astronomical"}

DOMAIN_KEY = {"local_human": "w_local", "global_human": "w_global",
              "farmed_animal": "w_farmed", "invertebrate": "w_invert",
              "future_human": "w_future", "xrisk_future": "w_xrisk"}

Z90 = 1.6448536269514722  # standard normal 95th percentile


def lognormal_mean(lo, hi):
    """Mean of the lognormal with a 90% CI of [lo, hi] (matches Squiggle `lo to hi`)."""
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return math.exp(mu + sigma * sigma / 2)


def welfare_range(a, domain, neurons):
    if domain in ("farmed_animal", "invertebrate"):
        return (neurons / HUMAN_NEURONS) ** a["neuron_exponent"]
    return 1.0


def wdaly_per_usd(a):
    """Expected wDALY/$ per org under one worldview's assumptions."""
    out = {}
    for name, domain, ci, neurons in SLATE:
        base = lognormal_mean(*ci)
        fanaticism = 1e-6 if (domain == "xrisk_future" and not a["accept_tiny_prob"]) else 1.0
        out[name] = base * welfare_range(a, domain, neurons) * a[DOMAIN_KEY[domain]] * fanaticism
    return out


def champion(a):
    """The single best org (pure EV-max) under one worldview."""
    evs = wdaly_per_usd(a)
    return max(evs, key=evs.get)


def credences(center, diversification):
    """Credence over worldviews: peaked on `center`, widened by `diversification`.
    0 -> all on center; large -> approaches uniform across worldviews."""
    stops = sorted(WORLDVIEWS)
    if diversification <= 0:
        return {w: (1.0 if w == center else 0.0) for w in stops}
    raw = {w: math.exp(-abs(w - center) / diversification) for w in stops}
    z = sum(raw.values())
    return {w: raw[w] / z for w in stops}


def allocate(center, diversification):
    stops = sorted(WORLDVIEWS)
    cred = credences(center, diversification)
    # Worldview-diversified portfolio: each worldview funds its champion,
    # weighted by that worldview's credence.
    alloc = {name: 0.0 for name, *_ in SLATE}
    for w in stops:
        alloc[champion(WORLDVIEWS[w])] += cred[w]
    # Credence-weighted wDALY/$ per org (expectation over worldviews).
    ew = {name: 0.0 for name, *_ in SLATE}
    for w in stops:
        evs = wdaly_per_usd(WORLDVIEWS[w])
        for name in ew:
            ew[name] += cred[w] * evs[name]
    return cred, ew, alloc


def main():
    ap = argparse.ArgumentParser(description="Worldview-diversified donation allocator.")
    ap.add_argument("--center", type=int, default=3, choices=range(6),
                    help="worldview you lean toward, 0..5 (default 3, invertebrates)")
    ap.add_argument("--diversification", type=float, default=1.0,
                    help="0 = all-in on the center worldview's winner; higher = diversify across worldviews")
    args = ap.parse_args()

    cred, ew, alloc = allocate(args.center, args.diversification)

    print(f"\ncenter worldview: {args.center} ({STOP_NAME[args.center]})   "
          f"diversification: {args.diversification}\n")

    print("credence over worldviews:")
    for w in sorted(WORLDVIEWS):
        bar = "#" * int(round(cred[w] * 40))
        print(f"  stop {w} {STOP_NAME[w]:<15} {cred[w]*100:5.1f}%  {bar}")

    print("\n{:<28}{:>16}{:>14}".format("org", "wDALY/$ (E)", "allocation"))
    print("-" * 58)
    for name in sorted(alloc, key=lambda n: alloc[n], reverse=True):
        print("{:<28}{:>16.4g}{:>13.1f}%".format(name, ew[name], alloc[name] * 100))

    top = max(alloc, key=alloc.get)
    print(f"\nsuggestion: {top}  ({alloc[top]*100:.0f}% of the portfolio)\n")


if __name__ == "__main__":
    main()
