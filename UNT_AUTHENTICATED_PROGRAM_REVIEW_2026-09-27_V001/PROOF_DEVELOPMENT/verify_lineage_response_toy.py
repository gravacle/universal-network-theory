#!/usr/bin/env python3
"""Exact classical-diagonal example for LINEAGE_RESPONSE_LEMMA_V001.

This is not an UNT calculation or verification of all quantum directions.
The four entries use order (S,C)=(0,0),(0,1),(1,0),(1,1).
"""

from fractions import Fraction as F
from itertools import product


STATES = tuple(product(range(2), repeat=2))


def marginals(vector):
    return tuple(
        tuple(sum(vector[i] for i, state in enumerate(STATES) if state[axis] == bit)
              for bit in range(2))
        for axis in range(2)
    )


def output(vector, readout):
    return tuple(sum(vector[i] for i, state in enumerate(STATES)
                     if readout(*state) == bit) for bit in range(2))


def distance(left, right):
    return sum(abs(a - b) for a, b in zip(left, right)) / 2


def main():
    actual = (F(1, 2), F(0), F(0), F(1, 2))
    sm, cm = marginals(actual)
    comparator = tuple(sm[s] * cm[c] for s, c in STATES)
    correlation = tuple(a - b for a, b in zip(actual, comparator))
    assert sum(actual) == sum(comparator) == 1
    assert min(actual) >= 0 and min(comparator) >= 0
    assert marginals(actual) == marginals(comparator)
    assert marginals(correlation) == ((0, 0), (0, 0))

    # Reversible common map (s,c) -> (s,c XOR s), followed by tracing out s.
    permutation = tuple((s, c ^ s) for s, c in STATES)
    assert set(permutation) == set(STATES)
    xor = lambda s, c: c ^ s
    out_actual, out_product = output(actual, xor), output(comparator, xor)
    assert out_actual == (1, 0)
    assert out_product == (F(1, 2), F(1, 2))
    assert distance(out_actual, out_product) == F(1, 2)
    assert output(correlation, xor) == (F(1, 2), F(-1, 2))
    assert distance(out_actual, out_product) <= distance(actual, comparator)

    # All two-by-two diagonal matrices with zero row/column sums are
    # a*(1,-1,-1,1). Verify sufficiency on this complete diagonal basis.
    basis = (F(1), F(-1), F(-1), F(1))
    assert marginals(basis) == ((0, 0), (0, 0))
    assert correlation == tuple(value / 4 for value in basis)
    assert output(basis, lambda s, c: c) == (0, 0)  # identity continuation
    assert output(basis, lambda s, c: s) == (0, 0)  # lineage copy to carrier
    assert output(basis, xor) == (2, -2)

    # Independent exact nullspace characterization from row/column equations.
    for a, b, c, d in product(range(-2, 3), repeat=4):
        v = tuple(map(F, (a, b, c, d)))
        zero_marginals = marginals(v) == ((0, 0), (0, 0))
        is_basis_multiple = v == tuple(F(a) * value for value in basis)
        assert zero_marginals == is_basis_multiple

    # Pullback of Z=(+1,-1) under XOR has pure correlation parity,
    # whereas identity/copy pullbacks are local carrier/lineage functions.
    pullback = tuple(F(1 if xor(s, c) == 0 else -1) for s, c in STATES)
    score = sum(o * g for o, g in zip(pullback, correlation))
    assert score == 1
    assert abs(score) / 2 == distance(out_actual, out_product)
    print("PASS exact rational diagonal toy: equal marginals; reversible common "
          "XOR response Delta=1/2; diagonal correlation-kernel census; "
          "identity/copy sufficiency; dual witness normalization.")
    print("Scope: one classical diagonal sector; no UNT or all-quantum replay.")


if __name__ == "__main__":
    main()
