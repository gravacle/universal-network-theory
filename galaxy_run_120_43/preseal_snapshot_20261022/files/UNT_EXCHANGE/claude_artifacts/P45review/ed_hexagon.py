"""ED normalization check of the ring amplitude on the 64-state flip cube of one flippable
hexagon (environment frozen). Lowest two eigenvalues split by 2K + O(h^8).
Claude, P45 review."""
import numpy as np
from fractions import Fraction as F
sig = [1, -1, 1, -1, 1, -1]
def run(Ud, alpha, h):
    A = 2 * Ud
    H = np.zeros((64, 64))
    for S in range(64):
        tot = sum(A + alpha * sig[i] for i in range(6) if S >> i & 1)
        tot += sum(2 * Ud * sig[i] * sig[(i + 1) % 6] for i in range(6) if S >> i & 1 and S >> ((i + 1) % 6) & 1)
        H[S, S] = tot
        for i in range(6):
            H[S, S ^ (1 << i)] = -h
    w = np.linalg.eigvalsh(H)
    return w[0], w[1]
T = {0.0: 252.0, 0.25: 89792708608/330812181}
for alpha in (0.0, 0.25):
    for h in (0.08, 0.04, 0.02):
        e0, e1 = run(1.0, alpha, h)
        K = h**6 * T[alpha] / 2**5
        print(f"alpha={alpha} h={h}: split/(2K) = {(e1-e0)/(2*K):.8f}")
