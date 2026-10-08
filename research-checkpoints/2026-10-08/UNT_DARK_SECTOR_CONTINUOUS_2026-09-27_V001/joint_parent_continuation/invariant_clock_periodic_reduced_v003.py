"""Exact paired cosine/sine arithmetic, without an RHS parity projection.

V001/V002 and their failed receipts remain unchanged. This evaluates the
same odd-N trigonometric interpolant using independent half-grid cosine
and sine sums. BOTH parity sectors are represented by dx; no physical mode
is discarded. Basis values are stored in exact reflected pairs to avoid
last-bit symmetry leakage amplified by the constrained canonical operator.
Only from_full removes floating representation error from the already
declared reflection-symmetric preparation; callers must measure that
change against the saved initial data and qualify reconstructed momenta.
No state, charge, shear, or RHS is projected during evolution.
"""
import numpy as np
from invariant_clock_periodic_reduced_v001 import Reduced as Parent


class Reduced(Parent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        M = self.n//2
        phase = 2*np.pi*np.arange(M+1)/self.n
        self.ch = np.cos(self.nm[:, None]*phase)
        self.sh = np.sin(self.nm[:, None]*phase)
        self.sh[:, 0] = 0.
        self.sh[0] = 0.
        self.cosine = np.concatenate((self.ch, self.ch[:, 1:][:, ::-1]), axis=1)
        all_sine = np.concatenate((self.sh, -self.sh[:, 1:][:, ::-1]), axis=1)
        self.sine = all_sine[1:]
        self.dxcos = -self.k*self.nm[:, None]*all_sine
        self.core.dx = self.dx

    def dx(self, f):
        f = np.asarray(f)
        if f.shape != (self.n,) or np.iscomplexobj(f) or not np.all(np.isfinite(f)):
            raise ValueError('finite real grid required')
        even = (f+f[self.mirror])/2
        odd = (f-f[self.mirror])/2
        even = even-np.mean(even)
        M = self.n//2
        ae = 2*(even[0]+2*self.ch[1:, 1:]@even[1:M+1])/self.n
        ao = 4*(self.sh[1:, 1:]@odd[1:M+1])/self.n
        dh_even = (self.k*self.nm[1:]*ao)@self.ch[1:]
        dh_odd = -(self.k*self.nm[1:]*ae)@self.sh[1:]
        return (np.r_[dh_even, dh_even[1:][::-1]]
                + np.r_[dh_odd, -dh_odd[1:][::-1]])

    def from_full(self, x, z, piT):
        raw = super().from_full(x, z, piT)
        signs = np.array([1, 1, -1, 1, 1, 1, -1, 1])[:, None]
        paired = (raw+signs*raw[:, self.mirror])/2
        self.initial_pairing_change = paired-raw
        return paired
