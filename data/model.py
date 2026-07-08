#!/usr/bin/env python3
"""
Loader for data/model.json - the single source of truth for the train to crazy
town. allocate.py, data/generate.py and data/test_sync.py all import this so the
orgs, the worldview/branch tree, and the assumption knobs are defined exactly
once.

The moral circle (`circle`, a list of domains) is the source; each Squiggle
per-domain weight `w_<domain>` is derived from it (1 if the domain is in the
node's circle, else 0). Nothing downstream carries its own copy of the numbers.
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
DOMAINS = MODEL["domains"]
ORGS = MODEL["orgs"]
STOPS = MODEL["stops"]
EDGES = MODEL["edges"]

ANIMAL_DOMAINS = {d for d, meta in DOMAINS.items() if meta["animal"]}


def org_by_name(name):
    for o in ORGS:
        if o["name"] == name:
            return o
    raise KeyError(name)


def stop_by_id(sid):
    for s in STOPS:
        if s["id"] == sid:
            return s
    raise KeyError(sid)


def squiggle_orgs():
    """Orgs that carry a `daly_per_usd` BOTEC, i.e. appear in the Squiggle slate."""
    return [o for o in ORGS if o.get("daly_per_usd") is not None]


def squiggle_stops():
    """Stops that have a Squiggle model (all except ones flagged `squiggle: false`)."""
    return [s for s in STOPS if s.get("squiggle", True)]


def weights_from_circle(circle):
    """Derive the six Squiggle per-domain weights from a moral circle."""
    return {f"w_{d}": (1 if d in circle else 0) for d in SQUIGGLE_WEIGHT_DOMAINS}
