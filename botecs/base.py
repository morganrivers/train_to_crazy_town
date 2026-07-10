"""botecs/base.py — the empirical axis of the model.

The train has TWO axes that must never multiply into each other:

  * MORAL assumptions (assumptions/*.py) are combinatorial by design — who
    counts, how much, under what discount. That is the ladder, and forking it
    is what produces the 73+ worldviews.
  * EMPIRICAL magnitudes (this package) are NOT combinatorial. There is one
    true P(nuclear war), one true chicken-years-per-dollar. Disagreement about
    them is resolved by IMPROVING A SHARED DERIVATION, not by forking a
    worldview. Every worldview reads the same botec; editing a factor here
    propagates to all of them at once — which is what "objective" means
    operationally.

A `Botec` is a worked derivation of one org's direct effect on its primary
beneficiary, in that beneficiary's own welfare units, BEFORE any moral
weighting (the chain's `coefficient` supplies the circle, welfare range and
discount). It is a multilinear form: a sum of product-`terms` over named,
independent `Factor`s. Because the factors are independent and each appears at
most once per term, both the mean AND the variance are closed-form — so a
worldview model can show a single moment-matched lognormal SUMMARY (mean exact,
variance exact) and link to the full derivation, instead of inlining every
factor into all 73 models.

Provenance is tracked per factor, not buried in prose, so the survey-anchored
guesses that drive the biggest EV levers are a greppable, machine-checkable
list (see PROVENANCE.md, generated). The taxonomy:

  worked-internal   — computed here from parts, each itself sourced
  worked-external   — a bottom line imported from a published, fully worked
                      model (GiveWell CEA, a Grilo/Saulius post); the mechanism
                      is public and checkable, we import its endpoint
  empirical-anchor  — a measured/counted quantity (FAOSTAT head counts, neuron
                      counts, present population)
  expert-judgment   — an elicited or stipulated number with NO derivation
                      (forecaster aggregates, conference-survey ranges); the
                      weak points we most want to replace with mechanisms
"""
import math

__all__ = [
    "Z90", "PROVENANCE_KINDS", "Factor", "Botec", "BOTECS", "register", "get",
    "lognormal_mean", "uniform_mean", "standard_normal",
    "ordered_factor_names", "render_botec", "_sq_num", "_sym_lognormal",
]

Z90 = 1.6448536269514722  # Phi^-1(0.95): the normal deviate of a two-sided 90% CI

PROVENANCE_KINDS = ("worked-internal", "worked-external", "empirical-anchor",
                    "expert-judgment")


# ---- factors: a named uncertain (or pinned) quantity, with its moments -------
class Factor:
    """One named, independent quantity in a botec. Carries enough to (a) return
    its exact first and second moments, (b) sample from it reproducibly, and
    (c) render itself as Squiggle source — plus its provenance and source.

    kind / params:
      lognormal        (lo, hi)  — two-sided 90% CI
      point            (p,)      — pinned scalar, no uncertainty
      one_minus_uniform(a, b)    — 1 - U[a, b]  (a bounded fraction, e.g. a
                                   counterfactual-discount that has no tail)
      beta             (a, b)    — a probability in [0, 1]
    """

    def __init__(self, name, kind, params, provenance, comment, source=None,
                 shared=False):
        assert provenance in PROVENANCE_KINDS, provenance
        self.name = name
        self.kind = kind
        self.params = tuple(params)
        self.provenance = provenance
        self.comment = comment
        self.source = source
        self.shared = shared  # drawn ONCE per world-state, shared across botecs

    # -- moments (exact) --
    def m1(self):
        k, p = self.kind, self.params
        if k == "lognormal":
            mu, sig = _lognormal_mu_sigma(*p)
            return math.exp(mu + sig * sig / 2)
        if k == "point":
            return float(p[0])
        if k == "one_minus_uniform":
            return 1.0 - (p[0] + p[1]) / 2
        if k == "beta":
            return p[0] / (p[0] + p[1])
        raise ValueError(k)

    def m2(self):
        k, p = self.kind, self.params
        if k == "lognormal":
            mu, sig = _lognormal_mu_sigma(*p)
            return math.exp(2 * mu + 2 * sig * sig)
        if k == "point":
            return float(p[0]) ** 2
        if k == "one_minus_uniform":
            eu = (p[0] + p[1]) / 2
            eu2 = (p[0] * p[0] + p[0] * p[1] + p[1] * p[1]) / 3
            return 1.0 - 2 * eu + eu2
        if k == "beta":
            a, b = p
            return a * (a + 1) / ((a + b) * (a + b + 1))
        raise ValueError(k)

    def moment(self, power):
        return self.m1() if power == 1 else self.m2()

    # -- sampling (reproducible; uses only rng.random() via standard_normal) --
    def sample(self, rng):
        k, p = self.kind, self.params
        if k == "point":
            return float(p[0])
        if k == "lognormal":
            mu, sig = _lognormal_mu_sigma(*p)
            return math.exp(mu + sig * standard_normal(rng))
        if k == "one_minus_uniform":
            return 1.0 - (p[0] + (p[1] - p[0]) * rng.random())
        if k == "beta":
            a, b, u = p[0], p[1], rng.random()
            if a == 1:
                return 1.0 - (1.0 - u) ** (1.0 / b)
            if b == 1:
                return u ** (1.0 / a)
            raise NotImplementedError("only beta(1, b) / beta(a, 1) sample stably")
        raise ValueError(k)

    # -- Squiggle source for this factor's distribution --
    def squiggle_rhs(self):
        k, p = self.kind, self.params
        if k == "lognormal":
            return _sym_lognormal(*p)
        if k == "point":
            return _sq_num(p[0])
        if k == "one_minus_uniform":
            return f"1 - Sym.uniform({_sq_num(p[0])}, {_sq_num(p[1])})"
        if k == "beta":
            return f"Sym.beta({_sq_num(p[0])}, {_sq_num(p[1])})"
        raise ValueError(k)

    def is_point(self):
        return self.kind == "point"


class Botec:
    """A worked derivation: value = sum over `terms` of the product of the
    factors named in each term. `factors` maps name -> Factor. Every factor is
    independent and appears at most once per term, so mean and variance are
    closed-form."""

    def __init__(self, id, terms, factors, doc, source_url=None,
                 units="wDALY-equivalent per $ (beneficiary's own welfare units)"):
        self.id = id
        self.terms = [tuple(t) for t in terms]
        self.factors = factors
        self.doc = doc
        self.source_url = source_url
        self.units = units
        seen = {n for t in self.terms for n in t}
        missing = seen - set(factors)
        assert not missing, f"{id}: terms reference undefined factors {missing}"

    def mean(self):
        total = 0.0
        for term in self.terms:
            prod = 1.0
            for name in term:
                prod *= self.factors[name].m1()
            total += prod
        return total

    def second_moment(self):
        """E[value^2] for the multilinear form: sum over ordered pairs of terms
        of E[term_i * term_j]. A factor in both terms enters at power 2 (its
        m2), a factor in one enters at power 1 (its m1); independence factorises
        the expectation."""
        total = 0.0
        for ti in self.terms:
            si = set(ti)
            for tj in self.terms:
                sj = set(tj)
                e = 1.0
                for name in si | sj:
                    power = (name in si) + (name in sj)
                    e *= self.factors[name].moment(power)
                total += e
        return total

    def variance(self):
        m = self.mean()
        return max(self.second_moment() - m * m, 0.0)

    def summary_lognormal(self):
        """(p5, p95) of the lognormal whose mean and variance EQUAL this botec's
        — the moment-matched summary a worldview model displays in place of the
        full derivation. Exact in mean and variance; for a single lognormal or a
        pure product of lognormals it reproduces the true distribution exactly,
        for a sum it is a shape approximation with the right first two moments.
        Returns None for a degenerate (zero-variance) botec."""
        # A one-factor lognormal botec IS a lognormal; return its CI verbatim so
        # the summary reads as the input rather than an exp/log round-trip of it.
        if len(self.terms) == 1 and len(self.terms[0]) == 1:
            only = self.factors[self.terms[0][0]]
            if only.kind == "lognormal":
                return only.params
        m, v = self.mean(), self.variance()
        if m <= 0 or v <= 0:
            return None
        sig2 = math.log(1.0 + v / (m * m))
        sig = math.sqrt(sig2)
        mu = math.log(m) - sig2 / 2
        return (math.exp(mu - Z90 * sig), math.exp(mu + Z90 * sig))

    # -- sampling: one draw of the whole botec, honouring shared factors --
    def sample(self, rng, shared_draws):
        """One draw. `shared_draws` maps a shared factor's name to its
        already-drawn value for this world-state (so futureDalysAtStake is the
        SAME for ALLFED and AI safety in a given Monte-Carlo iteration). Each
        non-shared factor is drawn once here and reused across the botec's
        terms."""
        draw = {}
        for name, f in self.factors.items():
            draw[name] = shared_draws[name] if (f.shared and name in shared_draws) \
                else f.sample(rng)
        total = 0.0
        for term in self.terms:
            prod = 1.0
            for name in term:
                prod *= draw[name]
            total += prod
        return total

    def shared_factor_specs(self):
        """{name: Factor} for factors flagged shared — drawn once per world-state
        by the confidence Monte-Carlo."""
        return {n: f for n, f in self.factors.items() if f.shared}

    # -- Squiggle: the standalone, full-derivation model for this botec --
    def expr_str(self, wrap_mean=False):
        def ref(name):
            f = self.factors[name]
            if wrap_mean and not f.is_point():
                return f"mean({name})"
            return name
        return " + ".join(" * ".join(ref(n) for n in term) for term in self.terms)


# ---- registry ----------------------------------------------------------------
BOTECS = {}


def register(botec):
    assert botec.id not in BOTECS, f"duplicate botec id {botec.id}"
    BOTECS[botec.id] = botec
    return botec


def get(botec_id):
    return BOTECS[botec_id]


# ---- shared math (one implementation, reused by the moral-factor machinery) ---
def _lognormal_mu_sigma(lo, hi):
    if lo == hi:
        return math.log(lo), 0.0
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return mu, sigma


def lognormal_mean(lo, hi):
    """E[X] for the lognormal whose two-sided 90% CI is [lo, hi] — exactly what
    Squiggle's mean(Sym.lognormal({p5: lo, p95: hi})) returns."""
    if lo == hi:
        return float(lo)
    mu, sigma = _lognormal_mu_sigma(lo, hi)
    return math.exp(mu + sigma * sigma / 2)


def uniform_mean(lo, hi):
    return (lo + hi) / 2


def standard_normal(rng):
    """One N(0,1) draw via Box-Muller using ONLY rng.random() (the Mersenne
    Twister core, identical across CPython versions), so the confidence
    Monte-Carlo baked into generated files is byte-reproducible in CI."""
    u1 = rng.random() or 1e-300
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


# ---- Squiggle number / distribution formatting -------------------------------
def _sq_num(x):
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return repr(x)


def _sym_lognormal(lo, hi):
    """Squiggle source for the lognormal whose two-sided 90% CI is [lo, hi] — the
    SYMBOLIC constructor, so every mean() stays analytic (a `to`-built
    distribution samples its mean and biases heavy tails low)."""
    return f"Sym.lognormal({{p5: {_sq_num(lo)}, p95: {_sq_num(hi)}}})"


def ordered_factor_names(botec):
    """Factor names in reading order — first appearance across the terms."""
    out = []
    for term in botec.terms:
        for name in term:
            if name not in out:
                out.append(name)
    return out


def render_botec(botec):
    """The standalone, full-derivation Squiggle model for one botec: every
    factor as a named distribution tagged with its provenance, the value
    expression, its exact analytic mean, and the moment-matched summary that
    worldview models display in its place."""
    b = botec
    lines = [f"// === botec: {b.id} — full derivation ===",
             f"// {b.doc}",
             f"// units: {b.units}"]
    if b.source_url:
        lines.append(f"// source: {b.source_url}")
    lines += [
        "// Each factor is independent and tagged [provenance]: worked-internal /",
        "// worked-external (imported endpoint of a public model) / empirical-anchor",
        "// (a measured count) / expert-judgment (elicited, no derivation — the weak",
        "// points). Worldview models show only the moment-matched summary at the",
        "// bottom and link here; edit the mechanism in botecs/*.py, not this file.",
        "// GENERATED by generate.py.",
        "",
    ]
    for name in ordered_factor_names(b):
        f = b.factors[name]
        src = f"  ({f.source})" if f.source else ""
        lines.append(f"{name} = {f.squiggle_rhs()}  "
                     f"// [{f.provenance}] {f.comment}{src}")
    lines += [
        "",
        f"{b.id}DalyPerUsd = {b.expr_str()}",
        f"{b.id}DalyPerUsdMean = {b.expr_str(wrap_mean=True)}  "
        f"// exact analytic mean (factors independent, so E factorises per term)",
    ]
    summ = b.summary_lognormal()
    if summ is not None:
        lines.append(
            f"{b.id}DalyPerUsdSummary = {_sym_lognormal(*summ)}  "
            f"// moment-matched lognormal: same mean AND variance as the botec — "
            f"what worldview models display")
    return "\n".join(lines) + "\n"
