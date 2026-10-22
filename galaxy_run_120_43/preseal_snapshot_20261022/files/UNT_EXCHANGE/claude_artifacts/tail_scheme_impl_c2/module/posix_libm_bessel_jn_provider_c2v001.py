"""INERT explicit installed POSIX libm J0/J1/Jn provider for the UV-tail library (TAIL_SCHEME_DESIGN_V002 sec 3.3).

Successor pattern of posix_libm_bessel_j0_provider_v001 (c7c93416): construction resolves the libm symbols but
never evaluates them; actual calls evaluate each UNIQUE exact float argument once per call (np.unique), no series,
interpolant, recurrence, fallback or claimed floating-point error bound. Dependencies: stdlib + NumPy only.

  create_provider() -> provider with .j0(x), .j1(x), .jn(n, x), .custody(), .counts
  n is a Python int (0 <= n <= 100000); x is any real finite float64 array; the result has x's shape, float64.
"""
import ctypes
import ctypes.util
import hashlib
import math
import os
import platform
import numpy as np

SCHEMA = 'POSIX_LIBM_BESSEL_JN_PROVIDER_C2V001'


class _Provider:
    def __init__(self):
        path = ctypes.util.find_library('m')
        if not path:
            raise RuntimeError('POSIX libm not discoverable; no Bessel fallback installed')
        try:
            lib = ctypes.CDLL(path)
            f0 = lib.j0; f0.argtypes = [ctypes.c_double]; f0.restype = ctypes.c_double
            f1 = lib.j1; f1.argtypes = [ctypes.c_double]; f1.restype = ctypes.c_double
            fn = lib.jn; fn.argtypes = [ctypes.c_int, ctypes.c_double]; fn.restype = ctypes.c_double
        except (OSError, AttributeError) as exc:
            raise RuntimeError('Installed POSIX libm j0/j1/jn symbols unavailable: ' + str(exc)) from exc
        self._f0, self._f1, self._fn = f0, f1, fn
        self._u0 = np.frompyfunc(f0, 1, 1)
        self._u1 = np.frompyfunc(f1, 1, 1)
        self._un = np.frompyfunc(fn, 2, 1)
        image = None

        class DlInfo(ctypes.Structure):
            _fields_ = [('dli_fname', ctypes.c_char_p), ('dli_fbase', ctypes.c_void_p),
                        ('dli_sname', ctypes.c_char_p), ('dli_saddr', ctypes.c_void_p)]
        try:
            system = ctypes.CDLL(None)
            locate = system.dladdr
            locate.argtypes = [ctypes.c_void_p, ctypes.POINTER(DlInfo)]
            locate.restype = ctypes.c_int
            info = DlInfo()
            if locate(ctypes.cast(fn, ctypes.c_void_p), ctypes.byref(info)) and info.dli_fname:
                image = info.dli_fname.decode('utf-8')
        except (OSError, AttributeError, UnicodeError):
            pass
        file_sha = None; file_note = None
        for cand in (path, image):
            if cand and os.path.isfile(cand):
                with open(cand, 'rb') as fh:
                    file_sha = hashlib.sha256(fh.read()).hexdigest()
                file_note = 'sha256 of the bytes of ' + cand
                break
        if file_sha is None:
            file_note = ('no regular file at the resolved library path or symbol image (macOS dyld shared cache); '
                         'sha256 not computable from bytes, recorded as null')
        self._custody = dict(schema=SCHEMA, provider='POSIX libm j0/j1/jn', lookup='ctypes.util.find_library(m)',
                             resolved_library_path=path, loaded_library_name=lib._name, symbol_image_path=image,
                             image_resolution='dladdr' if image is not None else 'unavailable; resolved library retained',
                             library_file_sha256=file_sha, library_file_sha256_note=file_note,
                             platform=platform.platform(), machine=platform.machine(),
                             signatures=['double j0(double)', 'double j1(double)', 'double jn(int,double)'],
                             exact_argument_reuse='per call (np.unique); no persistent cache',
                             scope='Installed compiled Bessel implementation; no series, interpolant, recurrence, download or claimed analytic floating-point error bound')
        self.counts = {'j0': 0, 'j1': 0, 'jn': 0}

    @staticmethod
    def _args(x):
        a = np.asarray(x)
        if np.iscomplexobj(a):
            raise ValueError('Real Bessel arguments required')
        a = np.asarray(a, dtype=np.float64)
        if not np.all(np.isfinite(a)):
            raise ValueError('Finite Bessel arguments required')
        return a

    def _eval(self, ufunc, a, key, *lead):
        unique, inverse = np.unique(a.ravel(), return_inverse=True)
        if len(unique) == 0:
            return np.zeros(a.shape)
        vals = np.asarray(ufunc(*lead, unique) if lead else ufunc(unique), dtype=np.float64)
        self.counts[key] += int(len(unique))
        if not np.all(np.isfinite(vals)):
            raise ValueError('POSIX libm Bessel returned a nonfinite value')
        return vals[inverse].reshape(a.shape)

    def j0(self, x):
        return self._eval(self._u0, self._args(x), 'j0')

    def j1(self, x):
        return self._eval(self._u1, self._args(x), 'j1')

    def jn(self, n, x):
        if type(n) is not int or n < 0 or n > 100000:
            raise ValueError('Integer order 0 <= n <= 100000 required')
        a = self._args(x)
        if n == 0:
            return self.j0(a)
        if n == 1:
            return self.j1(a)
        return self._eval(self._un, a, 'jn', n)

    def custody(self):
        return dict(self._custody, counts=dict(self.counts))


def create_provider():
    return _Provider()
