"""botecs/ — the empirical axis: one worked derivation per org's direct effect.

Importing this package registers every botec into `BOTECS` (id -> Botec). The
moral assumption chain (assumptions/*.py) reads these by id and never redefines
them: empirical magnitudes are shared and improved in one place, moral premises
are what fork into worldviews. See botecs/base.py for the contract and the
provenance taxonomy.
"""
from botecs.base import (  # noqa: F401
    Botec, Factor, BOTECS, register, get,
    lognormal_mean, uniform_mean, standard_normal, Z90,
    PROVENANCE_KINDS, _sq_num, _sym_lognormal,
    ordered_factor_names, render_botec,
)

# Import order is irrelevant to results (registration is idempotent by id), but
# grouping keeps the shared future factor defined before its consumers.
from botecs import future        # noqa: F401,E402  (defines the shared factor)
from botecs import near_term     # noqa: F401,E402
from botecs import allfed        # noqa: F401,E402
from botecs import ai_xrisk      # noqa: F401,E402


def all_botecs():
    """Every registered botec, in a stable order for generation."""
    return [BOTECS[i] for i in sorted(BOTECS)]
