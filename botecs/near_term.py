"""botecs/near_term.py — the non-astronomical slate: the derivations whose
bottom lines are imported from published, fully-worked models (GiveWell CEAs,
Grilo's and Saulius's forum analyses) or worked here from parts. Each is a
single lognormal 90% CI on the direct effect in the beneficiary's own welfare
units, except the soup kitchen, which is a worked product.

The CIs are calibrated so their lognormal MEANS reproduce the published figures
each entry cites — Grilo's ~0.00994 DALY/$ GiveWell baseline, and (at Rethink
Priorities welfare ranges) his ~460x / ~64k x / ~24k x multiples for chickens,
shrimp and wild insects. See assumptions/README.md "The metric and the slate".
"""
from botecs.base import Botec, Factor, register


def _single(id, lo, hi, provenance, comment, source_url, doc):
    """A one-factor botec: a lognormal 90% CI on the direct effect."""
    name = f"{id}DalyPerUsd"
    return register(Botec(
        id, terms=[(name,)],
        factors={name: Factor(name, "lognormal", (lo, hi), provenance, comment,
                              source=source_url)},
        doc=doc, source_url=source_url))


# Local soup kitchen — a worked subjective-wellbeing BOTEC, netted against the
# counterfactual of the money sitting in a bank.
register(Botec(
    "soup_kitchen",
    terms=[("soupKitchenPeopleHelpedPerUsd", "soupKitchenWellbeingGainDaly",
            "soupKitchenNetOfBank")],
    factors={
        "soupKitchenPeopleHelpedPerUsd": Factor(
            "soupKitchenPeopleHelpedPerUsd", "lognormal", (0.05, 0.5),
            "worked-internal", "people given a hot meal per dollar"),
        "soupKitchenWellbeingGainDaly": Factor(
            "soupKitchenWellbeingGainDaly", "lognormal", (0.001, 0.01),
            "worked-internal", "subjective-wellbeing gain per person, in DALYs"),
        "soupKitchenNetOfBank": Factor(
            "soupKitchenNetOfBank", "one_minus_uniform", (0.1, 0.5),
            "worked-internal",
            "share NOT counterfactually produced by the money sitting in a "
            "bank (mean 0.7); a bounded fraction, so uniform not lognormal"),
    },
    doc="Worked BOTEC: people made happier per dollar x their wellbeing gain, "
        "netted against the bank counterfactual. The parochial root's best buy; "
        "every worldview carries this agreed number unchanged.",
    source_url=None))

_single(
    "gd", 0.0004, 0.002, "worked-external",
    "GiveWell cash benchmark; CI mean 0.00101 DALY/$ = 0.10x the AMF entry",
    "https://www.givewell.org/international/technical/programs/cash-transfers",
    "GiveDirectly direct cash; ~1/10 of GiveWell top charities per dollar.")

_single(
    "amf", 0.0035, 0.021, "worked-external",
    "GiveWell CEA; CI mean 0.00994 DALY/$ reproduces Grilo's GiveWell baseline "
    "exactly — the 1x every other multiple is read against",
    "https://www.givewell.org/how-we-work/our-criteria/cost-effectiveness/cost-effectiveness-models",
    "GiveWell top charity (AMF); the 1x global-health baseline.")

_single(
    "aim", 0.001, 0.025, "expert-judgment",
    "AIM incubatees TARGET GiveWell-level cost-effectiveness with high "
    "early-stage variance; a heuristic range, not a worked CEA",
    "https://www.charityentrepreneurship.com/",
    "AIM / Charity Entrepreneurship; GiveWell-level target, higher variance.")

_single(
    "thl", 1.2, 47, "worked-external",
    "Saulius 9-120 chicken-years/$ x a reform's welfare delta; CI mean 14.0 x "
    "RP welfare range 0.332 = 4.6 DALY/$ ~ 460x GiveWell, Grilo's central multiple",
    "https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken",
    "The Humane League; corporate chicken campaigns (Saulius / Grilo).")

_single(
    "swp", 1200, 74000, "worked-external",
    "Grilo HSI 639 DALY/$ = 64.3k x GiveWell; CI mean 20668 x RP shrimp welfare "
    "range 0.031 = 641 DALY/$, reproducing his figure",
    "https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane",
    "Shrimp Welfare Project; Humane Slaughter Initiative (Grilo).")

_single(
    "wildbugs", 1600, 82000, "worked-external",
    "Grilo 236 DALY/$ = 23.7k x GiveWell (5.74M insects/$); CI mean 23427 x "
    "insect welfare range 0.01 = 234 DALY/$, reproducing his figure",
    "https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane",
    "Wild insects (humane pesticides); paying farmers for humane pesticides (Grilo).")
