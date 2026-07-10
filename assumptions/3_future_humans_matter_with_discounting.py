"""Assumption 3 — future humans matter, with discounting.

Future people enter the circle, but a pure-time discount keeps them from
dominating. This assumption REDEFINES `moral_weight` (future humans enter the
circle), ADDS a new parameter `future_discount_ci`, and WRAPS
`uncertain_factors` so the discount multiplies every future-facing org — as a
full distribution in the generated model, and as its exact mean in the
Python-side ranking.
"""

NAME = "future_humans_matter_with_discounting"
LABEL = "Future humans count\n(discounted)"
EDGE_LABEL = "count future people, discounted"
FIGURES = ["Frank Ramsey", "Tyler Cowen"]
REQUIRES = ["far_away_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Future people are inside the circle, but with a positive pure-time "
    "discount rate — the moderate longtermist position. A modest discount is "
    "enough to keep present, measurable global health competitive with "
    "future-protecting work; remove it (the next assumption) and the "
    "astronomical numbers take over."
)

_present_only_moral_weight = moral_weight    # noqa: F821
_undiscounted_uncertain_factors = uncertain_factors  # noqa: F821

# The aggregate attenuation on far-future value from a positive pure-time
# preference compounded with catastrophe/extinction hazard over the horizon,
# as a 90% CI rather than a point. The anchors disagree by orders of
# magnitude, which is exactly why this is a distribution:
#   - Ramsey (1928, "A Mathematical Theory of Saving") and the Stern Review
#     (2006, delta ~= 0.1%/yr) argue the PURE rate should be ~0 — attenuation
#     driven only by catastrophe hazard (cf. Ord, The Precipice: ~1/6 per
#     century), keeping far-future value near the top of this CI;
#   - Nordhaus (2007, "A Review of the Stern Review", ~1.5%/yr) and Cowen's
#     discussion of positive rates compound to near-total attenuation over
#     centuries, the bottom of this CI.
# The CI's mean (~0.0097) preserves the moderate-longtermist compromise the
# old 0.01 point stood for: the far future counts, but does not dominate.
FUTURE_DISCOUNT_CI = (0.0012, 0.03)


def future_discount_ci():
    """NEW parameter: the aggregate pure-time + hazard attenuation on future
    people, a lognormal 90% CI. Even a heavy discount leaves them IN the
    circle — dropping it is a separate assumption."""
    return FUTURE_DISCOUNT_CI


def moral_weight(domain):
    """REDEFINED: future humans are inside the circle."""
    if domain == "future_human":
        return 1.0
    return _present_only_moral_weight(domain)


def uncertain_factors(org):
    """WRAPPED: future-facing value carries the discount — the full
    distribution in the model, its exact mean in the ranking."""
    fs = _undiscounted_uncertain_factors(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        fs.append(lognormal_factor(  # noqa: F821
            "futureDiscount", *future_discount_ci(),
            "pure-time + catastrophe attenuation on far-future value "
            "(Ramsey/Stern ~0%/yr vs Nordhaus ~1.5%/yr; 1 = no discount)"))
    return fs
