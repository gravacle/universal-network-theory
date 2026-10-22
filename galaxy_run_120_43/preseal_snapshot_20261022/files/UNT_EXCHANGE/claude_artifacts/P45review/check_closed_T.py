"""Transcribed (not imported) P39 closed-form T(x) vs my 720-ordering enumeration. Claude."""
from fractions import Fraction as F
def T_closed(x):
    run3, pair_single, alternating = {}, {}, {}
    for s in (-1, 1):
        a = 1 + s * x
        run3[s] = 4 / ((1 - x * x) * a) + 1 / a ** 3
        pair_single[s] = (3 / (1 - x * x) + 1 / a ** 2) / (2 + s * x)
        alternating[s] = 1 / a ** 3
    ma = sum(run3.values()) + sum(pair_single.values())
    mo = sum(pair_single.values())
    ms = {s: (run3[s] + alternating[s] + 2 * pair_single[s]) / (2 * (1 + s * x)) for s in (-1, 1)}
    s5 = {s: (2 * ma + 2 * ms[s] + mo) / (1 + s * x) for s in (-1, 1)}
    return 3 * sum(s5.values())
enum = {F(0): F(252), F(1, 16): F(92255964626944, 359401303125), F(1, 8): F(89792708608, 330812181), F(1, 4): F(86523904, 253125)}
for x, v in enum.items():
    print(x, T_closed(x) == v, T_closed(x))
