#!/usr/bin/env python3
"""
Loader for data/model.json - the single source of truth for the train to crazy
town. allocate.py, data/generate.py and data/test_sync.py all import this so the
orgs, the worldview/branch tree, and the assumption knobs are defined exactly
once.

The model is COMPOSITIONAL. Every stop carries a one-line `sets` delta; its
resolved coefficient record (`resolved_coeffs`) is its parent's resolved coeffs
- `coeff_defaults` at the root - with `sets` merged on top. That mirrors the
Squiggle side, where each node imports its PARENT and `Dict.merge`s the same
delta. The moral circle is DERIVED from the resolved coeffs (a domain is in the
circle iff its weight is positive), so nothing carries a second copy of it.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "model.json")

# Squiggle assumption records use exactly these six per-domain weights.
SQUIGGLE_WEIGHT_DOMAINS = ["local", "global", "farmed", "invert", "future", "xrisk"]


def load(path=MODEL_PATH):
    with open(path) as f:
        return json.load(f)


MODEL = load()
CONSTANTS = MODEL["constants"]
COEFF_DEFAULTS = MODEL["coeff_defaults"]
DOMAINS = MODEL["domains"]
ORGS = MODEL["orgs"]
STOPS = MODEL["stops"]
EDGES = MODEL["edges"]

ANIMAL_DOMAINS = {d for d, meta in DOMAINS.items() if meta["animal"]}
STOP_BY_ID = {s["id"]: s for s in STOPS}


def org_by_name(name):
    for o in ORGS:
        if o["name"] == name:
            return o
    raise KeyError(name)


def stop_by_id(sid):
    return STOP_BY_ID[sid]


# ---- soup-kitchen worked BOTEC ---------------------------------------------
def botec_daly_per_usd(botec):
    """[lo, hi] DALY/$ from a soup-kitchen-style BOTEC: people helped per dollar
    times their wellbeing gain, netted against the counterfactual of the money
    sitting in a bank (which still does `counterfactual_bank_value` as much good).
    Multiplying two lognormal 90% CIs endpoint-wise keeps the order of magnitude."""
    plo, phi = botec["people_helped_per_usd"]
    wlo, whi = botec["wellbeing_gain_daly"]
    keep = 1.0 - botec["counterfactual_bank_value"]
    return [plo * wlo * keep, phi * whi * keep]


def org_daly_per_usd(org):
    """The Squiggle slate BOTEC for an org, computing it from a `botec` block if
    present. Returns None for orgs with no BOTEC (they are not in the slate)."""
    if org.get("botec"):
        return botec_daly_per_usd(org["botec"])
    return org.get("daly_per_usd")


def squiggle_orgs():
    """Orgs that carry (or derive) a `daly_per_usd` BOTEC, i.e. appear in the slate."""
    return [o for o in ORGS if org_daly_per_usd(o) is not None]


def squiggle_stops():
    """Stops that have a Squiggle model (all except ones flagged `squiggle: false`)."""
    return [s for s in STOPS if s.get("squiggle", True)]


# ---- coefficient chain ------------------------------------------------------
def resolved_coeffs(stop):
    """This stop's full coefficient record: walk root->stop applying each `sets`
    delta over coeff_defaults (the same accumulation the Squiggle chain does)."""
    if isinstance(stop, str):
        stop = STOP_BY_ID[stop]
    chain = []
    s = stop
    while s is not None:
        chain.append(s)
        s = STOP_BY_ID.get(s["parent"]) if s.get("parent") else None
    coeffs = dict(COEFF_DEFAULTS)
    for s in reversed(chain):          # root first, so deeper deltas win
        coeffs.update(s.get("sets", {}))
    return coeffs


def circle_from_coeffs(coeffs):
    """Domains inside the moral circle: any of the six weight-domains with weight
    > 0, plus wild_invert when the soil reversal is switched on."""
    circle = [d for d in SQUIGGLE_WEIGHT_DOMAINS if coeffs.get(f"w_{d}", 0) > 0]
    if coeffs.get("count_soil"):
        circle.append("wild_invert")
    return circle


def circle(stop):
    return circle_from_coeffs(resolved_coeffs(stop))


def weights_from_coeffs(coeffs):
    """The six Squiggle per-domain weights, in canonical order, from a coeffs record."""
    return {f"w_{d}": coeffs.get(f"w_{d}", 0) for d in SQUIGGLE_WEIGHT_DOMAINS}
