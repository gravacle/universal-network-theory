"""SOURCE ONLY. Independent certificate of the entire UNTRUSTED saved proposal.
Common-denominator Gaussian integer powers/actions, no Code2 math or Decimal.
Frozen native tau1/512,K32,den560,I80; arbitrary fully authenticated I80 center.
Inherited L2 bound must come from the actual accepted predecessor, externally
authenticated. Root executes with one owned whole-chunk guard.
"""
from fractions import Fraction as Q
from math import factorial

S = 1 << 80


def need(ok, why):
    if not ok:
        raise ValueError(why)


def wire(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): wire(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [wire(v) for v in value]
    return value


def upward(q):
    """Rational bisection for smallest128-bit upward root, no isqrt oracle."""
    need(q >= 0, 'nonnegative complete norm squared')
    p, d = q.numerator << 256, q.denominator
    low, high = 0, 1
    while high*high*d < p:
        high <<= 1
    while low < high:
        mid = (low+high)//2
        if mid*mid*d < p:
            low = mid+1
        else:
            high = mid
    need(low*low*d >= p and (low == 0 or (low-1)**2*d < p), 'complete outward root minimality')
    return Q(low, 1 << 128)


def vector(v, n):
    need(type(v) is list and len(v) == n and all(type(z) is list and len(z) == 2
         and all(type(x) is int for x in z) for z in v), 'whole Gaussian integer vector')
    return [(a, b) for a, b in v]


def square(v):
    return sum(a*a+b*b for a, b in v)


def h_action(rows, x, guard):
    out = []
    for i, row in enumerate(rows):
        re = im = 0
        for j, a, b in row:
            u, v = x[j]
            re += a*u-b*v
            im += a*v+b*u
        out.append((re, im))
        if i%256 == 0:
            guard()
    return out


def combine(V, c, guard):
    out = []
    for i in range(len(V[0])):
        re = im = 0
        for j, (a, b) in enumerate(c):
            u, v = V[j][i]
            re += a*u-b*v
            im += a*v+b*u
        out.append((re, im))
        if i%256 == 0:
            guard()
    return out


def small(T, c):
    out = []
    for row in T:
        re = im = 0
        for (a, b), (u, v) in zip(row, c):
            re += a*u-b*v
            im += a*v+b*u
        out.append((re, im))
    return out


def reconstruct(rows, center, candidate, guard, input_L2_error):
    n, K, denom, t = 10432, 32, 560, Q(1, 512)
    need(len(rows) == n, 'whole native dimension')
    error = Q(input_L2_error)
    need(0 <= error < Q(1, 1 << 51), 'actual native inherited error within strict cumulative cap')
    x = vector(center, n)
    need(set(candidate) == {'basis_I80', 'projected_H_I80', 'initial_coeff_I80', 'candidate_scope'}
         and candidate['candidate_scope'] == 'UNTRUSTED_DECIMAL80_TWO_PASS_KRYLOV; ONLY_FULL_EXACT_DEFECT_CAN_CERTIFY',
         'entire saved untrusted candidate wire')
    m = len(candidate['basis_I80'])
    need(1 <= m <= 16 and len(candidate['projected_H_I80']) == m, 'frozen maximal16 candidate columns')
    V = [vector(v, n) for v in candidate['basis_I80']]
    T = [vector(v, m) for v in candidate['projected_H_I80']]
    c = vector(candidate['initial_coeff_I80'], m)
    need(all(T[i][j] == (T[j][i][0], -T[j][i][1]) for i in range(m) for j in range(m)), 'whole exact projected Hermiticity')
    # Rows are independently constructed by0336, with exact full-domain/H
    # authentication performed before this arithmetic function is invoked.
    basis_squared = []
    residual_denominator = denom*S*S
    for j in range(m):
        hv = h_action(rows, V[j], guard)
        vt = combine(V, [T[i][j] for i in range(m)], guard)
        residual = [(S*a-denom*u, S*b-denom*v) for (a, b), (u, v) in zip(hv, vt)]
        basis_squared.append(Q(square(residual), residual_denominator**2))
        guard()
    W = combine(V, c, guard)
    difference = [(S*a-u, S*b-v) for (a, b), (u, v) in zip(x, W)]
    initial_squared = Q(square(difference), S**4)
    projected = []
    defects = []
    integrated = Q(0)
    common = factorial(K)*512**K*S**(K+2)
    polynomial = [(0, 0) for _ in range(n)]
    for k in range(K+1):
        coefficient_denominator = S**(k+1)
        projected.append([(Q(a, coefficient_denominator), Q(b, coefficient_denominator)) for a, b in c])
        factor = (factorial(K)//factorial(k))*512**(K-k)*S**(K-k)
        for i, (a, b) in enumerate(W):
            if k%4 == 1:
                a, b = b, -a
            elif k%4 == 2:
                a, b = -a, -b
            elif k%4 == 3:
                a, b = -b, a
            u, v = polynomial[i]
            polynomial[i] = u+factor*a, v+factor*b
        hw = h_action(rows, W, guard)
        if k < K:
            next_c = small(T, c)
            next_W = combine(V, next_c, guard)
            residual = [(S*a-denom*u, S*b-denom*v) for (a, b), (u, v) in zip(hw, next_W)]
            residual_denominator = denom*S**(k+3)
            squared = Q(square(residual), residual_denominator**2)
        else:
            squared = Q(square(hw), (denom*S**(K+2))**2)
        upper = upward(squared)
        integral_factor = t**(k+1)/factorial(k+1)
        integrated += upper*integral_factor
        defects.append({'power': k, 'complete_defect_norm_squared': squared,
                        'norm_upper': upper, 'integral_factor': integral_factor})
        if k < K:
            c, W = next_c, next_W
            actual_denominator = S**(k+2)
        else:
            actual_denominator = coefficient_denominator
        for pair in c:
            for value in pair:
                z = Q(value, actual_denominator)
                need(max(z.numerator.bit_length(), z.denominator.bit_length()) <= 32768, 'same declared full projected-power bit cap')
        guard()
    def trunc(numerator):
        return (1 if numerator >= 0 else -1)*(abs(numerator)*S//common)
    endpoint = [[trunc(a), trunc(b)] for a, b in polynomial]
    round_num = [(a*S-u*common, b*S-v*common) for (a, b), (u, v) in zip(polynomial, endpoint)]
    rounding_squared = Q(square(round_num), (common*S)**2)
    initial = upward(initial_squared)
    rounding = upward(rounding_squared)
    added = initial+integrated+rounding
    total = error+added
    return wire({'schema': 'CERTIFIED_KRYLOV_POLYNOMIAL_DEFECT_V001', 'dimension': n,
        'basis_columns': m, 'degree': K, 'tau': t, 'input_L2_error': error,
        'initial_projection_defect_squared': initial_squared, 'initial_projection_error_upper': initial,
        'all_basis_residual_norm_squared': basis_squared, 'all_projected_powers': projected,
        'all_polynomial_defect_terms': defects, 'integrated_defect_upper': integrated,
        'endpoint_quantization_norm_squared': rounding_squared, 'endpoint_quantization_error_upper': rounding,
        'step_added_L2_error': added, 'accumulated_L2_error': total, 'endpoint_I80': endpoint,
        'step_target_2_minus_64_met': added <= Q(1, 1 << 64),
        'original_cumulative_cap_2_minus_51_met': total < Q(1, 1 << 51),
        'arithmetic': 'FULL_EXACT_RATIONAL_WITH_INTEGER_OUTWARD_SQRT',
        'orthogonality_or_backend_flags_trusted': False, 'exact_input_error_and_H_ancestry_authenticated_here': False,
        'native_N2_validation_completed': False, 'physical_release': False})
