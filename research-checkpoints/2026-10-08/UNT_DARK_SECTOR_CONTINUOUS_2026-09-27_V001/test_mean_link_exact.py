#!/usr/bin/env python3
"""Exact rational derivative check, no numerical evolution or physical fitting."""
import importlib.util
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
PRIOR = Path(__file__).resolve().parent.parent / 'UNT_DARK_SECTOR_MECHANISM_START_2026-09-27_V001/test_exact_screen.py'
spec = importlib.util.spec_from_file_location('rational_matrices', PRIOR)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def comm(a, b):
    return m.add(m.mm(a, b), m.scale(-1, m.mm(b, a)))


class MeanLinkExact(unittest.TestCase):
    def test_derivatives_and_purity(self):
        count = 0
        left = [[F(1), F(0)], [F(0), F(0)]]
        hb = [[F(2), F(-1)], [F(-1), F(5)]]
        diagonal = [[F(1,3), F(0)], [F(0), F(-2,3)]]
        for p in (F(0), F(1,4), F(1,2), F(3,4), F(1)):
            coherences = (F(0),) if p in (0,1) else (F(0), F(1,8), F(-1,8))
            for coherence in coherences:
                rb = [[1-p, coherence], [coherence, p]]
                self.assertGreaterEqual(p*(1-p)-coherence**2, 0)
                rho = m.kron(rb, left)
                for hopping in (F(0), F(1,2), F(2)):
                    h = m.add(m.add(m.kron(hb,m.I), m.kron(m.I,diagonal)),
                              m.scale(-hopping,m.kron(m.Q,m.X)))
                    # Reduced first derivative = -i*K, second coefficient = S.
                    k = m.reduce_second(comm(h,rho))
                    s = m.scale(F(-1,2),m.reduce_second(comm(h,comm(h,rho))))
                    self.assertEqual(k[1][0], -hopping*p)
                    self.assertEqual(s[1][1], hopping**2*p)
                    coherent_h = m.add(diagonal,m.scale(-hopping*p,m.X))
                    coherent_s = m.scale(F(-1,2),comm(coherent_h,comm(coherent_h,left)))
                    self.assertEqual(coherent_s[1][1], hopping**2*p**2)
                    self.assertEqual(s[1][1]-coherent_s[1][1], hopping**2*p*(1-p))
                    purity_t2 = -m.tr(m.mm(k,k))+2*m.tr(m.mm(left,s))
                    self.assertEqual(purity_t2,-2*hopping**2*p*(1-p))
                    count += 1
        self.assertEqual(count, 33)
        print('33 rational state/coupling cases: derivative, probability, gap, purity exact')


if __name__ == '__main__':
    unittest.main(verbosity=2)
