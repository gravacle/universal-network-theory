"""batched_engine_adapter_c3v001 -- Module D of dispatch 0463 (Claude3 lane, V001).

Thin, versioned adapter that lets the frozen 0462 calibration-region engine
(``calibration_region_engine_c3v001.py``, untouched) consume a batched
``forward_many(thetas=[...])`` callable (dispatch 0463 Module C) while the
engine itself keeps calling a scalar ``forward(theta)``.

Mechanism: a theta-keyed cache sits between the engine and ``forward_many``.
Points the engine is known to request next (the seed, the first-attempt
central-difference Jacobian stencil, the Halton design points) are computed
here with the engine's own pinned helpers and fetched in one batch each; the
engine then runs through the cached forward and finds every prefetched point
already present.  Anything not foreseeable (halved Jacobian steps after an
invalid side, repair, march and bisection points) is fetched sequentially,
one theta per ``forward_many`` call, and cached as well.

Conventions (INTERFACE_0463_V001 / INTERFACE_0462_V001):
  * inert at import; keyword-only arguments without defaults;
  * every public function returns a dict with at least ``ok`` and ``reasons``
    and fails closed on anticipated bad input (no raise);
  * numpy only (no scipy); no numpy object escapes;
  * the 0462 engine module is passed in by the caller (``engine``) and its
    file bytes must hash to the pinned ``engine_sha256`` or the adapter
    refuses to use it;
  * no file is written, no process/thread is spawned, no NGC3198 data is read.
"""

import hashlib
import json
import math

import numpy as np

__all__ = [
    'make_cache',
    'make_cached_forward',
    'prefetch',
    'jacobian_stencil',
    'design_points',
    'run_calibration_region_batched',
]

MODULE_NAME = 'batched_engine_adapter_c3v001'
ADAPTER_VERSION = 'c3v001'
# SHA256 (bytes) of calibration_region_engine_c3v001.py this adapter version was written against
# and self-tested with.  It is informative only: the enforced pin is the ``engine_sha256`` kwarg.
ENGINE_SHA256_VALIDATED = 'f5613832fcb6e452b4490d56453cce37fb8846e802442407e794f80a6ec84e0b'
# Engine attributes this adapter relies on (all pinned through the engine file hash).
REQUIRED_ENGINE_ATTRS = (
    'run_calibration_region', 'make_coordinate_spec', 'load_observation_region', 'to_natural',
    '_check_spec', '_check_unit_vector', '_check_identifiability', '_x_of', '_floats',
    '_first_primes', '_radical_inverse', '_inside_box', '_nonneg_int', '_positive_float', '_finite_float',
)
STATS_KEYS = (
    'forward_calls',            # scalar forward(theta) calls received from the engine
    'cache_hits',               # of those, served from the cache
    'cache_misses',             # of those, not in the cache
    'sequential_fallbacks',     # misses that triggered forward_many(thetas=[theta])
    'fallback_failures',        # fallbacks that produced no forward-style verdict (not cached)
    'invalid_theta',            # forward(theta) calls with a theta the adapter could not key
    'forward_many_calls',       # every forward_many invocation (batches + fallbacks)
    'batch_calls',              # forward_many invocations made by prefetch
    'batch_thetas_requested',   # unique uncached thetas sent in prefetch batches
    'batch_thetas_fetched',     # of those, stored in the cache
)
PURPOSE_SEED_STENCIL = 'seed_and_jacobian_stencil'
PURPOSE_DESIGN = 'halton_design'


# --------------------------------------------------------------------------
# small helpers (duplicated from the engine where the engine's own are private
# and their exact semantics matter for byte-identical behaviour)
# --------------------------------------------------------------------------

def _canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _is_bool(x):
    return isinstance(x, (bool, np.bool_))


def _is_number(x):
    return (not _is_bool(x)) and isinstance(x, (int, float, np.integer, np.floating))


def _finite_float(x):
    if not _is_number(x):
        return None
    try:
        v = float(x)
    except Exception:
        return None
    if not math.isfinite(v):
        return None
    return v


def _is_int(x):
    return (not _is_bool(x)) and isinstance(x, (int, np.integer))


def _is_true(x):
    # identical to the engine's rule: only the bool True (or numpy True) counts
    return x is True or (isinstance(x, np.bool_) and bool(x))


def _is_hex64(s):
    if not isinstance(s, str) or len(s) != 64:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in s)


def _init_stats(stats):
    for key in STATS_KEYS:
        if not _is_int(stats.get(key)):
            stats[key] = 0


def _snapshot(stats):
    return {key: int(stats.get(key, 0)) for key in STATS_KEYS}


def _delta(after, before):
    return {key: int(after[key]) - int(before[key]) for key in STATS_KEYS}


def _theta_key(theta):
    """(reasons, key, clean_theta). clean_theta has str keys and plain finite floats."""
    if not isinstance(theta, dict) or not theta:
        return ['theta must be a non-empty dict {coordinate_name: float}'], None, None
    clean = {}
    for k, v in theta.items():
        if not isinstance(k, str) or not k:
            return ['theta keys must be non-empty str'], None, None
        fv = _finite_float(v)
        if fv is None:
            return [f'theta[{k!r}] must be a finite number'], None, None
        clean[k] = fv
    try:
        key = _canonical_json(clean)
    except Exception as exc:  # cannot happen for finite floats; fail closed anyway
        return [f'theta is not canonically serialisable: {type(exc).__name__}: {exc}'], None, None
    return [], key, clean


def _sanitize_result(raw):
    """Plain forward-style copy of a per-theta forward_many entry; None if it is not a dict.

    The copy is chosen so that the engine's own sanitiser/classifier give exactly the same
    verdict on the copy as on the raw dict (same validity rule, same finite-float rule).
    """
    if not isinstance(raw, dict):
        return None
    speeds = raw.get('speeds_km_s')
    clean_speeds = None
    if isinstance(speeds, dict):
        clean_speeds = {str(k): _finite_float(v) for k, v in speeds.items()}
    rsn = raw.get('reasons')
    clean_reasons = [str(r) for r in rsn] if isinstance(rsn, (list, tuple)) else []
    out = {'speeds_km_s': clean_speeds, 'valid': bool(_is_true(raw.get('valid'))), 'reasons': clean_reasons}
    prov = raw.get('provenance')
    if isinstance(prov, dict):
        try:
            out['provenance'] = json.loads(_canonical_json(prov))
        except Exception:
            out['provenance'] = {'note': 'provenance dropped by the adapter: not JSON-serialisable'}
    return out


def _copy_result(res):
    out = {
        'speeds_km_s': (dict(res['speeds_km_s']) if isinstance(res.get('speeds_km_s'), dict) else None),
        'valid': bool(res.get('valid')),
        'reasons': list(res.get('reasons', [])),
    }
    if 'provenance' in res:
        out['provenance'] = json.loads(json.dumps(res['provenance']))
    return out


def _invalid_result(reasons):
    return {'speeds_km_s': None, 'valid': False, 'reasons': list(reasons)}


def _call_forward_many(forward_many, clean_thetas):
    """Call forward_many once. Returns {ok, results: [sanitized|None], forward_many_ok,
    forward_many_reasons, exception, reasons}. ok iff every entry is a forward-style dict."""
    rec = {'ok': False, 'results': [None] * len(clean_thetas), 'forward_many_ok': None,
           'forward_many_reasons': [], 'exception': None, 'reasons': []}
    try:
        raw = forward_many(thetas=[dict(t) for t in clean_thetas])
    except Exception as exc:
        rec['exception'] = f'{type(exc).__name__}: {exc}'
        rec['reasons'].append('forward_many raised an exception')
        return rec
    if not isinstance(raw, dict):
        rec['reasons'].append('forward_many did not return a dict')
        return rec
    rec['forward_many_ok'] = bool(_is_true(raw.get('ok')))
    fr = raw.get('reasons')
    rec['forward_many_reasons'] = [str(r) for r in fr] if isinstance(fr, (list, tuple)) else []
    results = raw.get('results')
    if not isinstance(results, (list, tuple)) or len(results) != len(clean_thetas):
        rec['reasons'].append(f"forward_many 'results' must be a list of length {len(clean_thetas)}")
        return rec
    missing = []
    for i, entry in enumerate(results):
        san = _sanitize_result(entry)
        rec['results'][i] = san
        if san is None:
            missing.append(i)
    if missing:
        rec['reasons'].append(f'forward_many returned no forward-style dict for result index(es) {missing}')
        return rec
    if not rec['forward_many_ok']:
        rec['reasons'].append('note: forward_many reported ok=False but returned a forward-style verdict '
                              'for every theta; the verdicts are used as returned')
    rec['ok'] = True
    return rec


def _verify_engine(engine, engine_sha256):
    """(reasons, info); info = {file, sha256, matches_validated_hash} when the pinned engine is usable."""
    if engine is None or not hasattr(engine, '__file__'):
        return ['engine must be an imported module object with a __file__ attribute'], None
    if not _is_hex64(engine_sha256):
        return ['engine_sha256 must be a 64-character hexadecimal str'], None
    path = getattr(engine, '__file__', None)
    if not isinstance(path, str) or not path:
        return ['engine.__file__ must be a non-empty str path'], None
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
    except Exception as exc:
        return [f'cannot read engine file {path!r}: {type(exc).__name__}: {exc}'], None
    actual = hashlib.sha256(raw).hexdigest()
    if actual != engine_sha256.lower():
        return [f'engine file SHA256 mismatch: file {path!r} hashes to {actual}, pinned engine_sha256 is '
                f'{engine_sha256.lower()}; refusing to use this engine'], None
    missing = [a for a in REQUIRED_ENGINE_ATTRS if not callable(getattr(engine, a, None))]
    if missing:
        return [f'engine module lacks required callable attribute(s) {missing}'], None
    return [], {'file': path, 'sha256': actual, 'matches_validated_hash': (actual == ENGINE_SHA256_VALIDATED)}


def _logged_u(engine, u_array):
    """The unit point exactly as the engine's _evaluate_point records it and converts it."""
    return engine._floats(np.clip(np.asarray(u_array, dtype=float), 0.0, 1.0))


def _theta_at(engine, spec, u_array):
    """(u_list, theta) for the point the engine would hand to forward at u_array, or (u_list, None)
    when the engine's unit-to-natural conversion fails (then the engine does not call forward)."""
    u_list = _logged_u(engine, u_array)
    nat = engine.to_natural(spec=spec, u=u_list)
    if not _is_true(nat.get('ok')):
        return u_list, None
    return u_list, dict(nat['theta_natural'])


def _stencil_impl(engine, spec, info, uu, rel_step, min_step):
    """First-attempt central-difference stencil in the engine's request order.

    uu: numpy array from engine._check_unit_vector. min_step None = no column skip rule.
    """
    n = info['n']
    u_points, thetas, per_column, conv_failed = [], [], [], []
    for j in range(n):
        h = float(rel_step)
        h_p = min(h, 1.0 - float(uu[j]))
        h_m = min(h, float(uu[j]))
        col = {'column': j, 'name': info['varying'][j], 'nominal_step': h, 'plus_step': float(h_p),
               'minus_step': float(h_m), 'plus_point_index': None, 'minus_point_index': None,
               'skipped_below_min_step': False}
        if min_step is not None and (h_p + h_m) < float(min_step):
            col['skipped_below_min_step'] = True
            per_column.append(col)
            continue
        if h_p > 0.0:
            up = uu.copy()
            up[j] = float(uu[j]) + h_p
            u_list, theta = _theta_at(engine, spec, up)
            if theta is None:
                conv_failed.append({'column': j, 'side': 'plus', 'u': u_list})
            else:
                col['plus_point_index'] = len(u_points)
                u_points.append(u_list)
                thetas.append(theta)
        if h_m > 0.0:
            um = uu.copy()
            um[j] = float(uu[j]) - h_m
            u_list, theta = _theta_at(engine, spec, um)
            if theta is None:
                conv_failed.append({'column': j, 'side': 'minus', 'u': u_list})
            else:
                col['minus_point_index'] = len(u_points)
                u_points.append(u_list)
                thetas.append(theta)
        per_column.append(col)
    return u_points, thetas, per_column, conv_failed


def _boundary_side(boundary, k, side):
    """Boundary value for identified direction k (int or str key), finite float >= 0, else None."""
    entry = None
    if isinstance(boundary, dict):
        if k in boundary:
            entry = boundary[k]
        elif str(k) in boundary:
            entry = boundary[str(k)]
    if not isinstance(entry, dict):
        return None
    v = _finite_float(entry.get(side))
    if v is None or v < 0.0:
        return None
    return v


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------

def make_cache():
    """A fresh, empty theta-keyed cache: {theta_key: {'theta', 'result', 'source'}}."""
    return {'ok': True, 'cache': {}, 'schema': 'BATCHED_ADAPTER_CACHE_C3V001', 'reasons': []}


def make_cached_forward(*, forward_many, cache, stats):
    """A scalar forward(theta) that serves from cache and falls back to forward_many(thetas=[theta]).

    stats (dict) is updated in place with the counters in STATS_KEYS. The returned forward never
    raises: an adapter-level failure returns a forward-style dict with valid False and reasons
    starting with 'adapter:'; such a failure is NOT cached (the replay then exposes it).
    """
    out = {'ok': False, 'forward': None, 'reasons': []}
    reasons = out['reasons']
    if not callable(forward_many):
        reasons.append('forward_many must be callable')
    if not isinstance(cache, dict):
        reasons.append('cache must be a dict (from make_cache)')
    if not isinstance(stats, dict):
        reasons.append('stats must be a dict (updated in place)')
    if reasons:
        return out
    _init_stats(stats)

    def forward(theta):
        stats['forward_calls'] += 1
        rs, key, clean = _theta_key(theta)
        if rs:
            stats['invalid_theta'] += 1
            return _invalid_result(['adapter: theta rejected: ' + '; '.join(rs)])
        hit = cache.get(key)
        if isinstance(hit, dict) and isinstance(hit.get('result'), dict):
            stats['cache_hits'] += 1
            return _copy_result(hit['result'])
        stats['cache_misses'] += 1
        stats['sequential_fallbacks'] += 1
        stats['forward_many_calls'] += 1
        rec = _call_forward_many(forward_many, [clean])
        if rec['ok']:
            res = rec['results'][0]
            cache[key] = {'theta': dict(clean), 'result': res, 'source': 'sequential_fallback'}
            return _copy_result(res)
        stats['fallback_failures'] += 1
        rs2 = ['adapter: sequential forward_many fallback produced no verdict; not cached']
        rs2.extend(rec['reasons'])
        if rec['exception']:
            rs2.append(f'exception: {rec["exception"]}')
        return _invalid_result(rs2)

    out['forward'] = forward
    out['ok'] = True
    return out


def prefetch(*, forward_many, cache, thetas, stats):
    """Fetch every not-yet-cached theta in ONE forward_many call and store the results.

    requested = len(thetas); already_cached = thetas found in the cache before the call;
    fetched = unique uncached thetas stored. ok iff every uncached theta received a forward-style
    verdict. Nothing is fetched if any theta is malformed (fail closed before calling forward_many).
    """
    out = {'ok': False, 'requested': 0, 'fetched': 0, 'already_cached': 0, 'n_unique_uncached': 0,
           'n_not_fetched': 0, 'forward_many_called': False, 'forward_many_ok': None,
           'forward_many_reasons': [], 'exception': None, 'reasons': []}
    reasons = out['reasons']
    if not callable(forward_many):
        reasons.append('forward_many must be callable')
    if not isinstance(cache, dict):
        reasons.append('cache must be a dict (from make_cache)')
    if not isinstance(stats, dict):
        reasons.append('stats must be a dict (updated in place)')
    if not isinstance(thetas, (list, tuple)):
        reasons.append('thetas must be a list of theta dicts')
    if reasons:
        return out
    _init_stats(stats)
    out['requested'] = len(thetas)
    keys, cleans, seen = [], [], set()
    already = 0
    for i, th in enumerate(thetas):
        rs, key, clean = _theta_key(th)
        if rs:
            reasons.append(f'thetas[{i}] rejected: ' + '; '.join(rs))
            continue
        hit = cache.get(key)
        if isinstance(hit, dict) and isinstance(hit.get('result'), dict):
            already += 1
            continue
        if key in seen:
            continue
        seen.add(key)
        keys.append(key)
        cleans.append(clean)
    out['already_cached'] = already
    if reasons:
        reasons.append('nothing fetched: malformed theta in the request')
        return out
    out['n_unique_uncached'] = len(keys)
    if not keys:
        out['ok'] = True
        return out
    out['forward_many_called'] = True
    stats['forward_many_calls'] += 1
    stats['batch_calls'] += 1
    stats['batch_thetas_requested'] += len(keys)
    rec = _call_forward_many(forward_many, cleans)
    out['forward_many_ok'] = rec['forward_many_ok']
    out['forward_many_reasons'] = rec['forward_many_reasons']
    out['exception'] = rec['exception']
    fetched = 0
    for key, clean, res in zip(keys, cleans, rec['results']):
        if res is None:
            continue
        cache[key] = {'theta': dict(clean), 'result': res, 'source': 'batch'}
        fetched += 1
    out['fetched'] = fetched
    out['n_not_fetched'] = len(keys) - fetched
    stats['batch_thetas_fetched'] += fetched
    reasons.extend(rec['reasons'])
    out['ok'] = bool(rec['ok'] and fetched == len(keys))
    return out


def jacobian_stencil(*, engine, spec, u0, rel_step, engine_sha256):
    """The first-attempt central-difference points of the pinned 0462 engine at u0.

    Reproduces finite_difference_jacobian's first attempt: for each varying coordinate j, plus side
    u0 + min(rel_step, 1 - u0_j) e_j (if that step is > 0), then minus side u0 - min(rel_step, u0_j) e_j
    (if > 0), in the engine's request order; every point is clipped and converted with the engine's
    own helpers. Halved steps after an invalid side are not predicted here (sequential cache misses).
    The seed point itself is returned separately as seed_u / seed_theta.
    Note: the engine's column-skip rule (clipped plus+minus < min_step) needs min_step, which this
    signature does not carry; it is applied inside run_calibration_region_batched and can only
    trigger when rel_step > 1.
    """
    out = {'ok': False, 'u_points': [], 'thetas': [], 'seed_u': None, 'seed_theta': None, 'u0_used': None,
           'per_column': [], 'conversion_failed': [], 'n_points': 0, 'varying_names': [],
           'engine_sha256': None, 'reasons': []}
    reasons = out['reasons']
    rs, einfo = _verify_engine(engine, engine_sha256)
    if rs:
        reasons.extend(rs)
        return out
    out['engine_sha256'] = einfo['sha256']
    rs, info = engine._check_spec(spec)
    if rs:
        reasons.extend(['spec rejected by the engine: ' + r for r in rs])
        return out
    reasons.extend(engine._positive_float(rel_step, 'rel_step'))
    rs, uu = engine._check_unit_vector(u0, info['n'], 'u0')
    reasons.extend(rs)
    if reasons:
        return out
    try:
        seed_u, seed_theta = _theta_at(engine, spec, uu)
        u_points, thetas, per_column, conv_failed = _stencil_impl(engine, spec, info, uu, float(rel_step), None)
    except Exception as exc:  # fail closed
        reasons.append(f'internal error while building the stencil: {type(exc).__name__}: {exc}')
        return out
    if seed_theta is None:
        reasons.append('seed point fails the engine unit-to-natural conversion; the engine would not call forward')
        return out
    out.update({'ok': True, 'u_points': u_points, 'thetas': thetas, 'seed_u': seed_u, 'seed_theta': seed_theta,
                'u0_used': engine._floats(uu), 'per_column': per_column, 'conversion_failed': conv_failed,
                'n_points': len(u_points), 'varying_names': list(info['varying'])})
    return out


def design_points(*, engine, spec, exploration, identifiability, design_count, rng_seed, engine_sha256):
    """The Halton design points of the pinned 0462 engine's exploration stage 4, in request order.

    From exploration (a COMPLETE-or-later run, design evaluated or not): the first admitted point a
    (admitted point with log_index == first_admitted_log_index) and boundary[k] = {minus, plus} per
    identified direction k; from identifiability: right_vectors and identified. Then, exactly as the
    engine: bases = _first_primes(len(identified)), first_index = rng_seed + 1, and for
    jj in range(design_count): idx = first_index + jj, p = a + sum_k t_k V[k] with
    t_k = -minus + _radical_inverse(idx, base_k) * (minus + plus); p outside [0,1]^n (engine tolerance)
    is skipped and counted. Budget is not applied here (see run_calibration_region_batched).
    """
    out = {'ok': False, 'u_points': [], 'thetas': [], 'skipped_outside_box': 0, 'halton_indices': [],
           'bases': [], 'first_index': None, 'n_points': 0, 'anchor_u': None, 'anchor_log_index': None,
           'identified': [], 'conversion_failed': [], 'engine_sha256': None, 'reasons': []}
    reasons = out['reasons']
    rs, einfo = _verify_engine(engine, engine_sha256)
    if rs:
        reasons.extend(rs)
        return out
    out['engine_sha256'] = einfo['sha256']
    rs, info = engine._check_spec(spec)
    if rs:
        reasons.extend(['spec rejected by the engine: ' + r for r in rs])
        return out
    reasons.extend(engine._nonneg_int(design_count, 'design_count'))
    reasons.extend(engine._nonneg_int(rng_seed, 'rng_seed'))
    if reasons:
        return out
    n = info['n']
    # identifiability: validated with the engine's own checker (needs the row count)
    m = None
    if isinstance(identifiability, dict):
        rid = identifiability.get('row_ids')
        if isinstance(rid, list) and rid:
            m = len(rid)
        else:
            S = identifiability.get('scaled_jacobian')
            if isinstance(S, list):
                m = len(S)
    if m is None:
        reasons.append('identifiability must be the ok=True dict from identifiability_report (row count unknown)')
        return out
    rs, idn = engine._check_identifiability(identifiability, n, m)
    if rs:
        reasons.extend(['identifiability rejected by the engine: ' + r for r in rs])
        return out
    ident = idn['identified']
    V = idn['V']
    # exploration: anchor (first admitted point) and boundary per identified direction
    if not isinstance(exploration, dict):
        reasons.append('exploration must be the dict returned by the engine exploration stage')
        return out
    fal = exploration.get('first_admitted_log_index')
    if not _is_int(fal):
        reasons.append('exploration.first_admitted_log_index is not an int: no first admitted point '
                       '(exploration did not reach the design stage)')
        return out
    pts = exploration.get('admitted_points')
    if not isinstance(pts, list):
        reasons.append('exploration.admitted_points must be a list')
        return out
    matches = [p for p in pts if isinstance(p, dict) and p.get('log_index') == fal]
    if len(matches) != 1:
        reasons.append(f'expected exactly one admitted point with log_index == {fal}, found {len(matches)}')
        return out
    rs, a_arr = engine._check_unit_vector(matches[0].get('u'), n, 'first admitted point u')
    if rs:
        reasons.extend(rs)
        return out
    a = np.array(list(matches[0]['u']), dtype=float)  # exactly as the engine: np.array(first['u'])
    width = {}
    boundary = exploration.get('boundary')
    for k in ident:
        bm = _boundary_side(boundary, int(k), 'minus')
        bp = _boundary_side(boundary, int(k), 'plus')
        if bm is None or bp is None:
            reasons.append(f'exploration.boundary[{k}] minus/plus not determined (march stage incomplete)')
            continue
        width[int(k)] = (bm, bp)
    if reasons:
        return out
    out['anchor_u'] = engine._floats(a)
    out['anchor_log_index'] = int(fal)
    out['identified'] = [int(k) for k in ident]
    try:
        m_id = len(ident)
        bases = engine._first_primes(m_id)
        first_index = int(rng_seed) + 1
        out['bases'] = [int(b) for b in bases]
        out['first_index'] = first_index
        if m_id == 0:
            reasons.append('note: no identified direction; the engine evaluates no design point')
            out['ok'] = True
            return out
        u_points, thetas, indices, conv_failed = [], [], [], []
        skipped = 0
        for jj in range(int(design_count)):
            idx = first_index + jj
            p = a.copy()
            for pos, k in enumerate(ident):
                h = engine._radical_inverse(idx, bases[pos])
                bm, bp = width[int(k)]
                t_k = -bm + h * (bm + bp)
                p = p + t_k * V[k]
            if not engine._inside_box(p):
                skipped += 1
                continue
            u_list, theta = _theta_at(engine, spec, p)
            if theta is None:
                conv_failed.append({'halton_index': int(idx), 'u': u_list})
                continue
            u_points.append(u_list)
            thetas.append(theta)
            indices.append(int(idx))
    except Exception as exc:  # fail closed
        reasons.append(f'internal error while building the design: {type(exc).__name__}: {exc}')
        return out
    out.update({'ok': True, 'u_points': u_points, 'thetas': thetas, 'skipped_outside_box': int(skipped),
                'halton_indices': indices, 'n_points': len(u_points), 'conversion_failed': conv_failed})
    return out


def run_calibration_region_batched(*, engine, forward_many, cache, stats, engine_sha256, coordinates,
                                   observation_region_path, observation_region_sha256, u_seed, budget,
                                   rel_step, min_step, max_halvings, null_tolerance, repair_iterations,
                                   max_repair_step, march_step, bisection_steps, design_count, rng_seed):
    """Run the pinned 0462 engine's run_calibration_region with batched prefetching.

    1. prefetch the seed and the first-attempt Jacobian stencil (one forward_many call);
    2. engine.run_calibration_region(forward=cached forward, ..., design_count=0);
       a status other than COMPLETE makes the batching layer ok=False: steps 3-4 are skipped (stage 4
       was not reached) and step 5 still runs from the cache so engine_result equals a sequential run;
    3. compute the Halton design points exactly as the engine's stage 4 would, from that run;
    4. prefetch them (one forward_many call);
    5. rerun engine.run_calibration_region with the requested design_count; the replay of stages 1-3
       and of the design must make no new forward_many call (replay_new_calls == 0, else ok=False).
    engine_result is the step-5 output. ok is the batching layer's verdict: True iff every prefetch
    delivered, replay_new_calls == 0 and the engine finished COMPLETE. All counters in 'batching' are
    deltas for this call; the caller's stats dict accumulates across calls.
    """
    out = {
        'ok': False, 'engine_result': None, 'engine_file': None, 'engine_sha256': None,
        'batching': {
            'batches': [], 'cache_hits': 0, 'cache_misses': 0, 'sequential_fallbacks': 0,
            'fallback_failures': 0, 'replay_new_calls': 0, 'replay_performed': False,
            'forward_calls': 0, 'forward_many_calls': 0, 'stencil': None, 'design': None,
            'step2': None, 'step5': None, 'stats_delta': None,
        },
        'warnings': [], 'module': MODULE_NAME, 'adapter_version': ADAPTER_VERSION, 'reasons': [],
    }
    reasons = out['reasons']
    bat = out['batching']
    rs, einfo = _verify_engine(engine, engine_sha256)
    if rs:
        reasons.extend(rs)
        return out
    out['engine_file'] = einfo['file']
    out['engine_sha256'] = einfo['sha256']
    if not einfo['matches_validated_hash']:
        out['warnings'].append(f'engine hash {einfo["sha256"]} differs from the hash this adapter version was '
                               f'validated against ({ENGINE_SHA256_VALIDATED}); the pin you passed is honoured')
    if not callable(forward_many):
        reasons.append('forward_many must be callable')
    if not isinstance(cache, dict):
        reasons.append('cache must be a dict (from make_cache)')
    if not isinstance(stats, dict):
        reasons.append('stats must be a dict (updated in place)')
    if reasons:
        return out
    # the engine's own parameter checks, applied before anything is fetched
    reasons.extend(engine._nonneg_int(budget, 'budget'))
    reasons.extend(engine._positive_float(rel_step, 'rel_step'))
    reasons.extend(engine._positive_float(min_step, 'min_step'))
    reasons.extend(engine._nonneg_int(max_halvings, 'max_halvings'))
    tol = engine._finite_float(null_tolerance)
    if tol is None or not (0.0 <= tol <= 1.0):
        reasons.append('null_tolerance must be a finite number in [0, 1]')
    reasons.extend(engine._nonneg_int(repair_iterations, 'repair_iterations'))
    reasons.extend(engine._positive_float(max_repair_step, 'max_repair_step'))
    reasons.extend(engine._positive_float(march_step, 'march_step'))
    reasons.extend(engine._nonneg_int(bisection_steps, 'bisection_steps'))
    reasons.extend(engine._nonneg_int(design_count, 'design_count'))
    reasons.extend(engine._nonneg_int(rng_seed, 'rng_seed'))
    if not reasons and not (float(min_step) <= float(rel_step)):
        reasons.append('min_step must not exceed rel_step')
    if reasons:
        reasons.append('engine parameters rejected; nothing fetched, engine not run')
        return out
    region = engine.load_observation_region(path=observation_region_path, expected_sha256=observation_region_sha256)
    if not _is_true(region.get('ok')):
        reasons.append('observation region failed to load; nothing fetched, engine not run')
        reasons.extend(region.get('reasons', []))
        return out
    spec = engine.make_coordinate_spec(coordinates=coordinates)
    if not _is_true(spec.get('ok')):
        reasons.append('coordinate specification invalid; nothing fetched, engine not run')
        reasons.extend(spec.get('reasons', []))
        return out
    rs, info = engine._check_spec(spec)
    if rs:
        reasons.extend(rs)
        return out
    n = info['n']
    # seed point exactly as run_calibration_region derives it
    try:
        trial_u = []
        for nm in spec['varying_names']:
            tr = spec['transforms'][nm]
            x_lo, x_hi = engine._x_of(tr, spec['lower'][nm]), engine._x_of(tr, spec['upper'][nm])
            trial_u.append((engine._x_of(tr, spec['trial_values'][nm]) - x_lo) / (x_hi - x_lo))
        if u_seed is None:
            seed_list = list(trial_u)
        else:
            us = u_seed.tolist() if isinstance(u_seed, np.ndarray) else u_seed
            if not isinstance(us, (list, tuple)) or len(us) != n:
                reasons.append(f'u_seed must be None or a list of length {n} over the varying coordinates')
                return out
            seed_list = [trial_u[j] if x is None else x for j, x in enumerate(us)]
        rs, u0 = engine._check_unit_vector(seed_list, n, 'u_seed')
        if rs:
            reasons.extend(rs)
            return out
        # finite_difference_jacobian re-checks _floats(u0): identical values
        rs, uu = engine._check_unit_vector(engine._floats(u0), n, 'u0')
        if rs:
            reasons.extend(rs)
            return out
        seed_u, seed_theta = _theta_at(engine, spec, uu)
        if seed_theta is None:
            reasons.append('seed point fails the engine unit-to-natural conversion; nothing fetched, engine not run')
            return out
        u_points, thetas, per_column, conv_failed = _stencil_impl(engine, spec, info, uu, float(rel_step),
                                                                   float(min_step))
    except Exception as exc:  # fail closed
        reasons.append(f'internal error while preparing the stencil: {type(exc).__name__}: {exc}')
        return out
    # the engine checks the budget before every evaluation: seed first, then the stencil in order
    ordered = [seed_theta] + list(thetas)
    to_fetch = ordered[:int(budget)]
    bat['stencil'] = {'seed_u': seed_u, 'n_stencil_points': len(u_points), 'per_column': per_column,
                      'conversion_failed': conv_failed, 'n_prefetched': len(to_fetch),
                      'n_truncated_by_budget': len(ordered) - len(to_fetch)}

    fwd = make_cached_forward(forward_many=forward_many, cache=cache, stats=stats)
    if not fwd['ok']:
        reasons.extend(fwd['reasons'])
        return out
    forward = fwd['forward']
    _init_stats(stats)
    s_start = _snapshot(stats)

    def batch_record(purpose, pf):
        rec = {'purpose': purpose, 'n_requested': int(pf['requested']), 'n_fetched': int(pf['fetched']),
               'n_already_cached': int(pf['already_cached']), 'n_unique_uncached': int(pf['n_unique_uncached']),
               'forward_many_called': bool(pf['forward_many_called']), 'forward_many_ok': pf['forward_many_ok'],
               'ok': bool(pf['ok']), 'reasons': list(pf['reasons'])}
        bat['batches'].append(rec)
        return rec

    def finish(ok):
        s_end = _snapshot(stats)
        d = _delta(s_end, s_start)
        bat['stats_delta'] = d
        bat['cache_hits'] = d['cache_hits']
        bat['cache_misses'] = d['cache_misses']
        bat['sequential_fallbacks'] = d['sequential_fallbacks']
        bat['fallback_failures'] = d['fallback_failures']
        bat['forward_calls'] = d['forward_calls']
        bat['forward_many_calls'] = d['forward_many_calls']
        out['ok'] = bool(ok)
        return out

    def engine_kwargs(dc):
        return dict(forward=forward, coordinates=coordinates, observation_region_path=observation_region_path,
                    observation_region_sha256=observation_region_sha256, u_seed=u_seed, budget=budget,
                    rel_step=rel_step, min_step=min_step, max_halvings=max_halvings, null_tolerance=null_tolerance,
                    repair_iterations=repair_iterations, max_repair_step=max_repair_step, march_step=march_step,
                    bisection_steps=bisection_steps, design_count=dc, rng_seed=rng_seed)

    # ---- (1) seed + stencil batch ---------------------------------------------------------
    pf1 = prefetch(forward_many=forward_many, cache=cache, thetas=to_fetch, stats=stats)
    batch_record(PURPOSE_SEED_STENCIL, pf1)
    if not pf1['ok']:
        reasons.append('seed/stencil prefetch did not deliver a verdict for every point; engine not run '
                       '(fetched verdicts stay in the cache; re-invoke to fetch only the missing ones)')
        reasons.extend(pf1['reasons'])
        return finish(False)

    # ---- (2) engine with design_count=0 -----------------------------------------------------
    s2 = _snapshot(stats)
    try:
        res2 = engine.run_calibration_region(**engine_kwargs(0))
    except Exception as exc:  # the engine does not raise by contract; fail closed if it does
        reasons.append(f'engine raised during the design_count=0 run: {type(exc).__name__}: {exc}')
        return finish(False)
    d2 = _delta(_snapshot(stats), s2)
    bat['step2'] = {'status': res2.get('status'), 'ok': bool(_is_true(res2.get('ok'))),
                    'evaluations_used': res2.get('evaluations_used'), 'forward_calls': d2['forward_calls'],
                    'cache_hits': d2['cache_hits'], 'sequential_fallbacks': d2['sequential_fallbacks'],
                    'fallback_failures': d2['fallback_failures']}
    out['engine_result'] = res2
    if d2['fallback_failures'] > 0:
        reasons.append(f'{d2["fallback_failures"]} sequential fallback(s) produced no verdict during the '
                       f'design_count=0 run; the engine result contains adapter-level invalid evaluations '
                       f'(reasons prefixed "adapter:"); design prefetch and replay not performed')
        return finish(False)
    step2_complete = (res2.get('status') == 'COMPLETE')
    if not step2_complete:
        # Batching layer fails (ok=False). The design cannot be computed (stage 4 was not reached), so
        # the design prefetch is skipped; the engine is still rerun with the requested design_count so
        # that engine_result is the byte-identical equivalent of a sequential run (the rerun fails at
        # the same place from the cache alone; replay_new_calls is measured and must be 0).
        reasons.append(f'engine status {res2.get("status")!r} (not COMPLETE) in the design_count=0 run; '
                       f'design prefetch skipped; engine rerun with the requested design_count from the cache')
        reasons.extend(str(r) for r in res2.get('reasons', []))
    else:
        # ---- (3) design points exactly as stage 4 --------------------------------------------
        dp = design_points(engine=engine, spec=res2['spec'], exploration=res2['exploration'],
                           identifiability=res2['identifiability'], design_count=design_count,
                           rng_seed=rng_seed, engine_sha256=engine_sha256)
        if not dp['ok']:
            reasons.append('design points could not be computed from the design_count=0 run; '
                           'replay not performed (the design_count=0 engine result is returned)')
            reasons.extend(dp['reasons'])
            return finish(False)
        remaining = int(budget) - int(res2.get('evaluations_used', 0))
        design_thetas = list(dp['thetas'])[:max(0, remaining)]
        bat['design'] = {'design_count_requested': int(design_count), 'n_inside_box': int(dp['n_points']),
                         'skipped_outside_box': int(dp['skipped_outside_box']), 'bases': dp['bases'],
                         'first_index': dp['first_index'], 'identified': dp['identified'],
                         'anchor_log_index': dp['anchor_log_index'], 'halton_indices': dp['halton_indices'],
                         'n_prefetched': len(design_thetas),
                         'n_truncated_by_budget': int(dp['n_points']) - len(design_thetas),
                         'notes': [r for r in dp['reasons']]}

        # ---- (4) design batch ---------------------------------------------------------------
        pf2 = prefetch(forward_many=forward_many, cache=cache, thetas=design_thetas, stats=stats)
        batch_record(PURPOSE_DESIGN, pf2)
        if not pf2['ok']:
            reasons.append('design prefetch did not deliver a verdict for every point; replay not performed '
                           '(the design_count=0 engine result is returned)')
            reasons.extend(pf2['reasons'])
            return finish(False)

    # ---- (5) full run: replay of stages 1-3 + design, all from the cache ---------------------
    s5 = _snapshot(stats)
    try:
        res5 = engine.run_calibration_region(**engine_kwargs(design_count))
    except Exception as exc:
        reasons.append(f'engine raised during the full run: {type(exc).__name__}: {exc}')
        return finish(False)
    d5 = _delta(_snapshot(stats), s5)
    bat['replay_performed'] = True
    bat['replay_new_calls'] = int(d5['sequential_fallbacks'])
    bat['step5'] = {'status': res5.get('status'), 'ok': bool(_is_true(res5.get('ok'))),
                    'evaluations_used': res5.get('evaluations_used'), 'forward_calls': d5['forward_calls'],
                    'cache_hits': d5['cache_hits'], 'sequential_fallbacks': d5['sequential_fallbacks'],
                    'fallback_failures': d5['fallback_failures']}
    out['engine_result'] = res5
    ok = step2_complete
    if d5['sequential_fallbacks'] != 0:
        ok = False
        reasons.append(f'replay mismatch: the full run requested {d5["sequential_fallbacks"]} point(s) that were '
                       f'not prefetched or cached (replay_new_calls must be 0)')
    if d5['fallback_failures'] != 0:
        ok = False
        reasons.append(f'{d5["fallback_failures"]} sequential fallback(s) produced no verdict during the full run')
    if step2_complete and (res5.get('status') != 'COMPLETE' or not _is_true(res5.get('ok'))):
        ok = False
        reasons.append(f'engine status {res5.get("status")!r} in the full run')
        reasons.extend(str(r) for r in res5.get('reasons', []))
    if d5['forward_calls'] != d5['cache_hits'] + d5['sequential_fallbacks']:
        ok = False
        reasons.append('internal accounting mismatch in the full run')
    return finish(ok)
