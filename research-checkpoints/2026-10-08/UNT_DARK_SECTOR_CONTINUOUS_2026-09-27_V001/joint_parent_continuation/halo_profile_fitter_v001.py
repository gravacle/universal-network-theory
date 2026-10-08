"""Inert, NumPy-only descriptive NFW/ISO velocity-profile fitter.

No files are read or written and no fit runs on import.  The caller owns the
prospective input census, source authentication, tests and result publication.
The two halo parameters are A=v_halo(pivot)**2 >= 0 and scale>0.  These are
comparison profiles, not changes to the UNT law or the saved baryonic field.

Sources for the circular-speed shapes: Navarro, Frenk & White (1997), eq. 3,
https://arxiv.org/pdf/astro-ph/9611107 ; de Blok et al. (2008), eqs. 6--10,
https://arxiv.org/pdf/0810.2100 .  No concentration--mass prior is imposed.
"""

import math
from functools import lru_cache
import numpy as np


LOGSCALE_BOUNDS = (-20.0, 20.0)
AMPLITUDE_BISECTIONS = 96
GOLDEN_ITERATIONS = 80
CONFIG = {
    "logscale_bounds": list(LOGSCALE_BOUNDS),
    "amplitude_bisections": AMPLITUDE_BISECTIONS,
    "golden_iterations": GOLDEN_ITERATIONS,
    "required_comparison_grids": [257, 513],
    "small_x_series_threshold": 0.125,
    "nfw_series_terms": 18,
    "iso_series_terms": 10,
    "amplitude_upper_bound": "max(observed**2/shape) over positive-weight rows",
    "sampled_local_minimum_rule": "sse[i]<=sse[i-1] and sse[i]<=sse[i+1]",
    "velocity_residual_sign": "prediction minus observed",
}


def _model_name(model):
    name = str(model).upper()
    if name not in ("NFW", "ISO"):
        raise ValueError("model must be NFW or ISO")
    return name


def _vector(value, name):
    array = np.asarray(value, dtype=float)
    if array.ndim != 1 or not array.size or not np.all(np.isfinite(array)):
        raise ValueError(name + " must be a nonempty finite one-dimensional array")
    return array


def _fit_inputs(shape_values, baryon_v2, observed, weights):
    arrays = tuple(_vector(value, name) for value, name in (
        (shape_values, "shape"), (baryon_v2, "baryon_v2"),
        (observed, "observed"), (weights, "weights")))
    s, b, v, w = arrays
    if any(a.shape != s.shape for a in arrays):
        raise ValueError("all input arrays must have the same shape")
    if np.any(s <= 0) or np.any(b < 0) or np.any(v <= 0):
        raise ValueError("shape and observed must be positive; baryon_v2 nonnegative")
    if np.any(w < 0) or not np.any(w > 0):
        raise ValueError("weights must be nonnegative with at least one positive entry")
    return arrays


def _horner_and_derivative(x, coefficients):
    value = np.full_like(x, coefficients[-1])
    derivative = np.zeros_like(x)
    for coefficient in coefficients[-2::-1]:
        derivative = derivative*x + value
        value = value*x + coefficient
    return value, derivative


def _log_kernel_and_slope(model, logx):
    """Return log f(x) and d log f / d log x, retaining small-x powers.

    NFW: f=x sum_j (-1)^j (j+1)/(j+2) x^j.
    ISO: f=x^2 sum_j (-1)^j x^(2j)/(2j+3).
    Direct small differences are not used below x=1/8.  Logarithmic leading
    powers also avoid underflow when two tiny kernels are normalized.
    """
    logx = np.asarray(logx, dtype=float)
    value, slope = np.empty_like(logx), np.empty_like(logx)
    small = logx < math.log(0.125)
    x = np.exp(logx[small])
    if model == "NFW":
        coefficients = [(-1.0)**j*(j+1)/(j+2) for j in range(18)]
        p, dp = _horner_and_derivative(x, coefficients)
        value[small] = logx[small] + np.log(p)
        slope[small] = 1 + x*dp/p
        ell = logx[~small]
        fraction = 1/(1+np.exp(-ell))
        numerator = np.logaddexp(0, ell)-fraction
        value[~small] = np.log(numerator)-ell
        slope[~small] = fraction*fraction/numerator-1
    else:
        coefficients = [(-1.0)**j/(2*j+3) for j in range(10)]
        p, dp = _horner_and_derivative(x*x, coefficients)
        value[small] = 2*logx[small] + np.log(p)
        slope[small] = 2 + 2*x*x*dp/p
        ell = logx[~small]
        reciprocal = np.exp(-ell)
        # atan(x)=pi/2-atan(1/x); this branch has x>=1/8.
        ratio = (math.pi/2-np.arctan(reciprocal))*reciprocal
        kernel = 1-ratio
        value[~small] = np.log1p(-ratio)
        slope[~small] = 1/((1+reciprocal*reciprocal)*kernel)-1
    return value, slope


def _shape_and_derivative(model, radius, logscale, pivot):
    model = _model_name(model)
    radius = np.asarray(radius, dtype=float)
    pivot, logscale = float(pivot), float(logscale)
    if not math.isfinite(pivot) or pivot <= 0:
        raise ValueError("pivot must be finite and positive")
    if not np.all(np.isfinite(radius)) or np.any(radius <= 0):
        raise ValueError("all radii must be finite and positive")
    if math.isnan(logscale):
        raise ValueError("logscale must not be NaN")
    logr = np.log(radius)-math.log(pivot)
    if math.isinf(logscale):
        exponent = (-1 if logscale < 0 else 1) if model == "NFW" else (
            0 if logscale < 0 else 2)
        normalized = np.exp(exponent*logr)
        derivative = np.zeros_like(normalized)
    else:
        arguments = np.r_[np.ravel(logr-logscale), -logscale]
        logf, slope = _log_kernel_and_slope(model, arguments)
        normalized = np.exp(logf[:-1]-logf[-1]).reshape(radius.shape)
        derivative = normalized*(slope[-1]-slope[:-1].reshape(radius.shape))
    if not np.all(np.isfinite(normalized)) or np.any(normalized <= 0):
        raise ValueError("normalized shape is outside finite floating-point range")
    return normalized, derivative


def shape(model, radius, logscale, pivot):
    """Normalized halo speed-squared shape, equal to one at the pivot.

    scale=pivot*exp(logscale).  Scalar or array radii are accepted.  Explicit
    +/-inf logscale selects the exact scale limits, not a very large scale.
    """
    result, _ = _shape_and_derivative(model, radius, logscale, pivot)
    return float(result) if result.ndim == 0 else result


def _amplitude_fit(s, b, v, w):
    active = w > 0
    sa, ba, va, wa = s[active], b[active], v[active], w[active]

    def gradient(amplitude):
        velocity = np.sqrt(ba+amplitude*sa)
        if np.any(velocity == 0):
            return -math.inf  # observed>0 and positive active weights
        return float(np.dot(wa*sa, 1-va/velocity))

    at_zero = gradient(0.0)
    # Each model speed at this bound is >= its observed speed, since b>=0.
    upper = float(np.max((va*va)/sa))
    if not math.isfinite(upper) or upper <= 0:
        raise ValueError("amplitude bracket is outside finite floating-point range")
    lower, high = 0.0, upper
    iterations = 0
    if at_zero >= 0:
        amplitude = 0.0
        lower = high = 0.0
    else:
        for _ in range(AMPLITUDE_BISECTIONS):
            middle = lower+(high-lower)/2
            if gradient(middle) < 0:
                lower = middle
            else:
                high = middle
        iterations = AMPLITUDE_BISECTIONS
        amplitude = lower+(high-lower)/2
    prediction = np.sqrt(b+amplitude*s)
    residual = prediction-v  # signed actual velocity residual, not v^2 residual
    loss = float(np.dot(w, residual*residual))
    velocity_active = prediction[active]
    curvature = (math.inf if np.any(velocity_active == 0) else
                 float(np.dot(wa*sa*sa, va/(2*velocity_active**3))))
    if not math.isfinite(loss) or not np.all(np.isfinite(prediction)):
        raise ValueError("objective or prediction overflowed")
    bracket_gradients = [gradient(lower), gradient(high)]
    return {
        "amplitude": float(amplitude), "sse": loss,
        "amplitude_gradient": gradient(amplitude),
        "amplitude_curvature": curvature,
        "amplitude_boundary": bool(amplitude == 0),
        "derivative_at_zero": None if not math.isfinite(at_zero) else at_zero,
        "derivative_at_zero_is_negative_infinity": bool(at_zero == -math.inf),
        "initial_upper_amplitude": upper,
        "final_amplitude_bracket": [float(lower), float(high)],
        "final_bracket_gradients": [g if math.isfinite(g) else None
                                    for g in bracket_gradients],
        "final_bracket_negative_infinity": [g == -math.inf for g in bracket_gradients],
        "amplitude_bisections": iterations,
        "prediction": prediction.tolist(), "residual": residual.tolist(),
        "halo_v2": (amplitude*s).tolist(),
        "halo_velocity": np.sqrt(amplitude*s).tolist(),
    }


def optimize_amplitude(shape, baryon_v2, observed, weights):
    """Unique constrained velocity-SSE amplitude optimum for a fixed shape.

    J'(A)=sum w*s*(1-v/sqrt(b+A*s)), with strictly positive derivative of
    J' for positive observations and active weights.  The A=0 boundary is
    preserved; otherwise 96 bisections use the analytic, non-prior bracket.
    Zero-weight rows remain in returned predictions and residuals.
    """
    return _amplitude_fit(*_fit_inputs(shape, baryon_v2, observed, weights))


def profile_fit(model, r, b2, v, w, grid_count, pivot=None):
    """Profile amplitude, scan scale, and refine every sampled local bracket.

    The optional fixed pivot permits identical bounds across sample masks.
    Both finite bounds and both exact asymptotic profiles are candidates.
    Grid agreement must be assessed by the caller: this search is not a proof
    of global optimality between samples or outside the finite-scale window.
    A limiting-profile optimum is an infimum candidate, not a finite halo.
    No input filtering, source fitting, parameter priors or I/O occurs here.
    """
    model = _model_name(model)
    r = _vector(r, "r")
    if np.any(r <= 0):
        raise ValueError("radii must be positive")
    _, b2, v, w = _fit_inputs(np.ones_like(r), b2, v, w)
    if isinstance(grid_count, bool) or int(grid_count) != grid_count or grid_count < 3:
        raise ValueError("grid_count must be an integer >=3")
    grid_count = int(grid_count)
    pivot = float(np.median(r)) if pivot is None else float(pivot)
    if not math.isfinite(pivot) or pivot <= 0:
        raise ValueError("pivot must be finite and positive")
    # Bounded memoization prevents tied/flat profiles from retaining every
    # golden-section trial vector.  Grid and candidate records stay complete.
    @lru_cache(maxsize=128)
    def evaluate(t):
        t = float(t)
        s, ds = _shape_and_derivative(model, r, t, pivot)
        result = _amplitude_fit(s, b2, v, w)
        amplitude = result["amplitude"]
        if math.isinf(t):
            derivative, scale = None, None
        else:
            scale = pivot*math.exp(t)
            if not math.isfinite(scale) or scale <= 0:
                raise ValueError("scale is outside finite floating-point range")
            if amplitude == 0:
                derivative = 0.0
            else:
                active = w > 0
                prediction = np.asarray(result["prediction"])
                derivative = float(amplitude*np.dot(
                    w[active]*ds[active], 1-v[active]/prediction[active]))
        result.update({"logscale": None if math.isinf(t) else t,
                       "scale": scale, "logscale_gradient": derivative,
                       "shape": s.tolist()})
        return result

    grid = np.linspace(*LOGSCALE_BOUNDS, grid_count)
    grid_fits = [evaluate(t) for t in grid]
    grid_loss = np.array([item["sse"] for item in grid_fits])
    candidates = []

    def candidate(t, kind, **metadata):
        item = dict(evaluate(t))
        item.update({"kind": kind, **metadata})
        candidates.append(item)

    candidate(grid[0], "finite_lower_boundary")
    candidate(grid[-1], "finite_upper_boundary")
    candidate(-math.inf, "zero_scale_limit", limit_label="scale_to_zero")
    candidate(math.inf, "infinite_scale_limit", limit_label="scale_to_infinity")
    golden = (math.sqrt(5)-1)/2
    for index in range(1, grid_count-1):
        if grid_loss[index] > grid_loss[index-1] or grid_loss[index] > grid_loss[index+1]:
            continue
        left, right = float(grid[index-1]), float(grid[index+1])
        initial_bracket = [left, right]
        x1, x2 = right-golden*(right-left), left+golden*(right-left)
        f1, f2 = evaluate(x1)["sse"], evaluate(x2)["sse"]
        for _ in range(GOLDEN_ITERATIONS):
            if f1 <= f2:
                right, x2, f2 = x2, x1, f1
                x1 = right-golden*(right-left)
                f1 = evaluate(x1)["sse"]
            else:
                left, x1, f1 = x1, x2, f2
                x2 = left+golden*(right-left)
                f2 = evaluate(x2)["sse"]
        # Keep the sampled minimum itself; refinement must never discard it.
        choices = [float(grid[index]), left, right, x1, x2, (left+right)/2]
        best_t = min(choices, key=lambda t: evaluate(t)["sse"])
        candidate(best_t, "sampled_local_minimum",
                  grid_index=index, initial_logscale_bracket=initial_bracket,
                  final_logscale_bracket=[left, right],
                  sampled_sse=float(grid_loss[index]),
                  golden_iterations=GOLDEN_ITERATIONS)

    best_index = min(range(len(candidates)), key=lambda i: candidates[i]["sse"])
    selected = dict(candidates[best_index])
    equal_best = [i for i, item in enumerate(candidates)
                  if item["sse"] == selected["sse"]]
    selected["scale_unidentified_at_zero_amplitude"] = selected["amplitude_boundary"]
    grid_keys = ("logscale", "scale", "amplitude", "sse", "amplitude_gradient",
                 "logscale_gradient", "amplitude_boundary")
    return {
        "model": model, "pivot": pivot, "grid_count": grid_count,
        "logscale_bounds": list(LOGSCALE_BOUNDS),
        "amplitude_bisections": AMPLITUDE_BISECTIONS,
        "golden_iterations": GOLDEN_ITERATIONS,
        "selected_candidate_index": best_index,
        "exactly_equal_best_candidate_indices": equal_best,
        "selected": selected, "candidates": candidates,
        "grid_profiles": [{key: item[key] for key in grid_keys} for item in grid_fits],
        "sampled_local_bracket_count": len(candidates)-4,
        "sampled_grid_is_exactly_flat": bool(np.all(grid_loss == grid_loss[0])),
        "newtonian_sse": float(np.dot(w, (np.sqrt(b2)-v)**2)),
        "search_scope": "finite logscale grid/refinements plus exact limits; no global proof",
    }
