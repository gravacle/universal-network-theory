"""INERT installed POSIX libm integer-order Bessel J_n provider (UNT 0445, c2v001).

Wraps the system libm symbol `double jn(int, double)` through ctypes, following
the loading pattern of posix_libm_bessel_j0_provider_v001.py (read as text only):
ctypes.util.find_library('m') -> ctypes.CDLL -> explicit argtypes/restype ->
dladdr image record. Construction resolves symbols but never evaluates them.

Each call validates the integer order (declared range MIN_ORDER..MAX_ORDER) and
finite real arguments, then evaluates libm jn elementwise, once per unique exact
float64 argument, with an explicit bounded LRU cache keyed by (order, argument)
(max_cache_entries == 0 disables the cache). This module contains no Bessel
series, recurrence, interpolant, asymptotic form or J0 substitution of its own;
if libm jn is unavailable the factory returns a precise finding, never a
substitute provider. No scientific execution or I/O at import; dependencies are
stdlib (ctypes) and NumPy only. Floating-point error state is the caller's.
"""
import ctypes
import ctypes.util
import math
from collections import OrderedDict

import numpy as np

MIN_ORDER = 0
MAX_ORDER = 6
LIBRARY_POLICY_FIND_LIBRARY_M = 'posix_find_library_m'
READY = 'READY'
_MAX_EXACT_INTEGER = 2 ** 53


class _DlInfo(ctypes.Structure):
    _fields_ = [('dli_fname', ctypes.c_char_p), ('dli_fbase', ctypes.c_void_p),
                ('dli_sname', ctypes.c_char_p), ('dli_saddr', ctypes.c_void_p)]


def _symbol_image(function):
    """Return (image_path, symbol_name) via dladdr, or (None, None)."""
    try:
        system = ctypes.CDLL(None)
        locate = system.dladdr
        locate.argtypes = [ctypes.c_void_p, ctypes.POINTER(_DlInfo)]
        locate.restype = ctypes.c_int
        info = _DlInfo()
        if locate(ctypes.cast(function, ctypes.c_void_p), ctypes.byref(info)):
            image = info.dli_fname.decode('utf-8') if info.dli_fname else None
            name = info.dli_sname.decode('utf-8') if info.dli_sname else None
            return image, name
    except (OSError, AttributeError, UnicodeError):
        pass
    return None, None


def _validated_order(n):
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)):
        raise TypeError('Integer Bessel order required (bool, float, str and arrays rejected); got '
                        + type(n).__name__)
    order = int(n)
    if order < MIN_ORDER or order > MAX_ORDER:
        raise ValueError('Bessel order %d outside declared range %d..%d' % (order, MIN_ORDER, MAX_ORDER))
    return order


def _validated_arguments(x_array):
    a = np.asarray(x_array)
    kind = a.dtype.kind
    if kind == 'f':
        if a.dtype.itemsize > 8:
            raise TypeError('Extended-precision arguments would be rounded to float64; pass float64')
    elif kind in 'iu':
        if a.size and (np.any(a > _MAX_EXACT_INTEGER) or (kind == 'i' and np.any(a < -_MAX_EXACT_INTEGER))):
            raise ValueError('Integer arguments beyond 2**53 are not exactly representable in float64')
    else:
        raise TypeError('Real numeric Bessel arguments required; dtype %s rejected '
                        '(complex, bool, object and string inputs are not accepted)' % a.dtype)
    a = a.astype(np.float64)
    if not np.all(np.isfinite(a)):
        raise ValueError('Finite Bessel arguments required')
    return a


def create_jn_provider(*, library_policy, expected_library_path, max_cache_entries):
    """Resolve libm jn; return a fail-closed result dict.

    Required keyword arguments (no defaults):
      library_policy        -- must be 'posix_find_library_m' (ctypes.util.find_library('m')).
      expected_library_path -- None (record whatever is resolved) or the exact str the
                               lookup must return; any other resolution fails closed.
      max_cache_entries     -- int >= 0; 0 disables caching, otherwise LRU bound on
                               (order, argument) entries retained across calls.

    Returns dict(status, bessel_jn, metadata, finding). status == 'READY' only when
    jn was resolved; otherwise bessel_jn is None and finding states why. Invalid
    caller arguments raise TypeError/ValueError.
    """
    if not isinstance(library_policy, str) or library_policy != LIBRARY_POLICY_FIND_LIBRARY_M:
        raise ValueError("library_policy must be '%s'" % LIBRARY_POLICY_FIND_LIBRARY_M)
    if expected_library_path is not None and (not isinstance(expected_library_path, str)
                                              or not expected_library_path):
        raise TypeError('expected_library_path must be None or a nonempty str')
    if type(max_cache_entries) is not int or max_cache_entries < 0:
        raise ValueError('max_cache_entries must be a Python int >= 0 (0 disables the cache)')

    metadata = dict(
        provider='POSIX libm jn (integer order Bessel J_n)',
        library_policy=library_policy,
        lookup='ctypes.util.find_library(m)',
        expected_library_path=expected_library_path,
        resolved_library_path=None, loaded_library_name=None,
        symbol='jn', signature='double jn(int, double)',
        symbol_image_path=None, symbol_image_name=None, image_resolution='unavailable',
        j0_symbol_distinct=None,
        order_range=[MIN_ORDER, MAX_ORDER],
        max_cache_entries=max_cache_entries,
        cache_policy=('disabled' if max_cache_entries == 0 else
                      'LRU keyed by (order, float64 argument), bounded by max_cache_entries'),
        exact_argument_reuse='within a call: one libm evaluation per unique (order, argument)',
        signed_zero='-0.0 canonicalized to +0.0 before lookup/evaluation',
        output_invariants='finite, |J_n|<=1, J_0(0)==1, J_n(0)==0 for n>=1; violation raises',
        calls=0, evaluations=0, cache_hits=0, cache_evictions=0, cache_entries=0,
        scope=('Installed compiled libm jn evaluated elementwise; no series, recurrence, '
               'interpolant, asymptotic form, download, J0 substitution or claimed analytic '
               'floating-point error bound in this module'))

    def finding(status, text):
        return dict(status=status, bessel_jn=None, metadata=metadata, finding=text)

    try:
        path = ctypes.util.find_library('m')
    except (OSError, ValueError) as exc:
        return finding('LIBM_NOT_DISCOVERABLE', 'ctypes.util.find_library(m) raised: ' + repr(exc))
    if not path:
        return finding('LIBM_NOT_DISCOVERABLE',
                       'ctypes.util.find_library(m) returned %r; no Bessel fallback installed' % (path,))
    metadata['resolved_library_path'] = path
    if expected_library_path is not None and path != expected_library_path:
        return finding('LIBM_PATH_MISMATCH', 'find_library(m) resolved %r, expected %r'
                       % (path, expected_library_path))
    try:
        library = ctypes.CDLL(path)
    except OSError as exc:
        return finding('LIBM_LOAD_FAILED', 'ctypes.CDLL(%r) failed: %s' % (path, exc))
    metadata['loaded_library_name'] = getattr(library, '_name', None)
    try:
        function = library.jn
    except AttributeError as exc:
        return finding('LIBM_JN_SYMBOL_UNAVAILABLE',
                       'Installed libm %r exports no jn symbol: %s; no provider substituted' % (path, exc))
    function.argtypes = [ctypes.c_int, ctypes.c_double]
    function.restype = ctypes.c_double
    jn_address = ctypes.cast(function, ctypes.c_void_p).value
    try:
        j0_address = ctypes.cast(library.j0, ctypes.c_void_p).value
    except AttributeError:
        j0_address = None
    if j0_address is not None and j0_address == jn_address:
        return finding('LIBM_JN_ALIASES_J0', 'libm jn resolves to the j0 entry point; refused')
    metadata['j0_symbol_distinct'] = (None if j0_address is None else True)
    image, name = _symbol_image(function)
    metadata['symbol_image_path'] = image
    metadata['symbol_image_name'] = name
    metadata['image_resolution'] = 'dladdr' if image is not None else 'unavailable; resolved library retained'

    cache = OrderedDict()

    def bessel_jn(n, x_array):
        """J_n(x) for integer n in MIN_ORDER..MAX_ORDER and finite real x.

        Returns a new float64 ndarray of x_array's shape. Raises TypeError/ValueError
        on invalid input before any evaluation, RuntimeError if libm output violates
        an invariant. Cache holds only validated values; a failed call returns nothing.
        """
        order = _validated_order(n)
        x = _validated_arguments(x_array)
        metadata['calls'] += 1
        flat = x.reshape(-1) + 0.0
        unique, inverse = np.unique(flat, return_inverse=True)
        values = np.empty(unique.shape[0], dtype=np.float64)
        for i in range(unique.shape[0]):
            argument = float(unique[i])
            key = (order, argument)
            if max_cache_entries and key in cache:
                cache.move_to_end(key)
                values[i] = cache[key]
                metadata['cache_hits'] += 1
                continue
            value = float(function(order, argument))
            if not math.isfinite(value) or abs(value) > 1.0:
                raise RuntimeError('libm jn(%d, %r) returned %r (nonfinite or |J|>1)' % (order, argument, value))
            if argument == 0.0 and value != (1.0 if order == 0 else 0.0):
                raise RuntimeError('libm jn(%d, 0) returned %r, not the exact J_n(0)' % (order, value))
            metadata['evaluations'] += 1
            if max_cache_entries:
                cache[key] = value
                if len(cache) > max_cache_entries:
                    cache.popitem(last=False)
                    metadata['cache_evictions'] += 1
                metadata['cache_entries'] = len(cache)
            values[i] = value
        return values[inverse.reshape(-1)].reshape(x.shape)

    return dict(status=READY, bessel_jn=bessel_jn, metadata=metadata, finding=None)
