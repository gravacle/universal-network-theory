"""SOURCE ONLY. Exact I80 decoding/quadratics and continuous-window enclosures.
Caller must authenticate complete original C150 archives, vector pins and L2
proofs. No file I/O, propagation, acceptance or author execution.
"""
from fractions import Fraction as F
import struct

SCALE = 1 << 80
TAU = F(1, 128)
HALFWIDTH = F(1, 4096)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def wire(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): wire(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [wire(v) for v in value]
    return value


def decode_vector(raw, dimension, point=False):
    need(type(raw) is bytes and len(raw) == 16+48*dimension, 'complete fixed-width vector bytes')
    need(raw[:8] == b'UNTI80V1' and struct.unpack('<II', raw[8:16]) == (dimension, 4), 'literal I80 full vector header')
    center = []
    for offset in range(16, len(raw), 48):
        a, b, c, d = [int.from_bytes(raw[offset+k:offset+k+12], 'little', signed=True)
                      for k in (0, 12, 24, 36)]
        need(a <= b and c <= d, 'ordered complete interval coordinates')
        if point:
            need(a == b and c == d, 'left vector is exact point center')
        center.append(((a+b)//2, (c+d)//2))
    return center


def signed_decision(interval, exact_null=False):
    lo, hi = map(F, interval)
    if exact_null:
        need(lo == hi == 0, 'literal zero operator expectation')
        return 'EXACT_OPERATOR_NULL'
    if lo > TAU:
        return 'POSITIVE_ABOVE_DECLARED_THRESHOLD'
    if hi < -TAU:
        return 'NEGATIVE_BELOW_DECLARED_THRESHOLD'
    if lo >= -TAU and hi <= TAU:
        return 'WITHIN_DECLARED_ZERO_TOLERANCE'
    return 'UNRESOLVED'


def evaluate(table, center, error, guard=lambda: None):
    n = table['active_dimension']
    need(type(n) is int and 1 <= n <= 10432 and len(center) == n, 'complete declared read dimension')
    need(all(len(z) == 2 and all(type(a) is int for a in z) for z in center), 'exact integer center')
    e = F(error)
    need(0 <= e < F(1, 1 << 51), 'original cumulative L2 error cap')
    need(F(table['E_bias']) == F(7, 4) and F(table['signed_bias_threshold']) == TAU
         and F(table['required_halfwidth']) == HALFWIDTH, 'frozen units and tolerances')
    masses = [r*r+s*s for r, s in center]
    delta = 2*e+e*e
    results = {}
    for name, definition in table['reads'].items():
        weights = definition['weights_numerator_over_14']
        norm = F(definition['operator_norm_upper'])
        lower, upper = map(F, definition['global_range'])
        need(len(weights) == n and all(type(w) is int for w in weights), 'complete exact read weights')
        need(0 <= norm <= 1 and -norm <= lower <= upper <= norm, 'proved read norm and range')
        need(all(lower <= F(w, 14) <= upper for w in weights), 'entire diagonal spectrum in declared range')
        value = F(sum(w*m for w, m in zip(weights, masses)), 14*SCALE*SCALE)
        allowance = norm*delta
        interval = [max(lower, value-allowance), min(upper, value+allowance)]
        need(interval[0] <= interval[1], 'normalized-reference interval nonempty')
        need((interval[1]-interval[0])/2 <= HALFWIDTH, 'fixed interval halfwidth')
        null = definition['exact_operator_null']
        need(type(null) is bool and null == (norm == 0), 'zero-operator scope')
        results[name] = {'center_expectation': value, 'interval': interval,
                         'vector_error_allowance': allowance, 'kind': definition['kind'],
                         'signed_read_decision': signed_decision(interval, null),
                         'unitary_bias_signature_eligible': definition['kind'] == 'UNITARY_SIGNED_COST_BIAS'}
        guard()
    return wire({'schema': 'P50_EXACT_SAVED_STATE_COST_READ_V001',
                 'center_norm_squared': F(sum(masses), SCALE*SCALE),
                 'original_L2_error': e, 'base_vector_error_allowance': delta,
                 'all_reads': results, 'center_renormalized': False,
                 'arithmetic': 'EXACT_INTEGER_GAUSSIAN_MASSES_AND_RATIONAL_DIAGONAL_WEIGHTS',
                 'full_input_error_proof_external': True, 'physical_mass_claim': False})


def exact_initial(M, table, packet, seed):
    need(seed in M.TYPES and table['active_dimension'] == 10432, 'original five native q11 seeds')
    ss = {tuple(s): i for i, s in enumerate(packet['active_states'])}
    ket = M.exact_kets()['11:'+seed]
    support = [(ss[state], r*r+s*s) for state, r, s in ket]
    need(sum(w for i, w in support) == 25, 'exact original normalization')
    results = {}
    for name, definition in table['reads'].items():
        weights = definition['weights_numerator_over_14']
        value = F(sum(weights[i]*mass for i, mass in support), 14*25)
        interval = [value, value]
        results[name] = {'exact_expectation': value, 'interval': interval,
                         'kind': definition['kind'],
                         'signed_read_decision': signed_decision(interval, definition['exact_operator_null'])}
    return wire({'schema': 'P50_EXACT_Q11_INITIAL_COST_READ_V001', 'seed': seed,
                 'time': F(0), 'all_reads': results, 'initial_state_not_physical_S1': True})


class Window:
    def __init__(self, table):
        self.table = table
        self.range_data = {}
        self.first = self.last = None
        self.max_gap = F(0)
        self.samples = 0

    def add(self, time, result):
        time = F(time)
        if self.last is not None:
            need(time > self.last, 'strict complete sample chronology')
            self.max_gap = max(self.max_gap, time-self.last)
        else:
            self.first = time
        self.last = time
        need(set(result['all_reads']) == set(self.table['reads']), 'every frozen read at every time')
        for name, row in result['all_reads'].items():
            lo, hi = map(F, row['interval'])
            if name not in self.range_data:
                self.range_data[name] = [lo, hi, lo, hi]
            else:
                a, b, c, d = self.range_data[name]
                self.range_data[name] = [min(a, lo), max(b, hi), max(c, lo), min(d, hi)]
        self.samples += 1

    def finish(self, start, end, expected_samples):
        need(self.first == F(start) and self.last == F(end) and self.samples == expected_samples,
             'complete declared time window and boundary samples')
        need(self.max_gap <= F(1, 512), 'frozen maximum sample gap')
        answers = {}
        for name, (minlo, maxhi, maxlo, minhi) in self.range_data.items():
            read = self.table['reads'][name]
            L = F(read['commutator_norm_upper'])
            need(L >= 0, 'nonnegative independently authenticated commutator bound')
            lower, upper = map(F, read['global_range'])
            interpolation = L*self.max_gap/2
            outer = [max(lower, minlo-interpolation), min(upper, maxhi+interpolation)]
            observed_lower = max(F(0), maxlo-minhi)
            width = outer[1]-outer[0]
            need(width >= observed_lower >= 0, 'consistent continuous range certificate')
            verdict = ('RESOLVED_VARIATION_ABOVE_THRESHOLD' if observed_lower > TAU else
                       'WITHIN_CONTINUOUS_WINDOW_TOLERANCE' if width <= TAU else 'UNRESOLVED')
            answers[name] = {'observed_range_lower': observed_lower,
                             'continuous_range_outer': outer,
                             'continuous_range_width_upper': width,
                             'between_sample_allowance': interpolation,
                             'verdict': verdict, 'kind': read['kind'],
                             'unitary_bias_signature_eligible': read['kind'] == 'UNITARY_SIGNED_COST_BIAS'}
        return wire({'schema': 'P50_COMPLETE_FINITE_WINDOW_COST_STABILITY_V001',
                     'start': self.first, 'end': self.last, 'samples': self.samples,
                     'max_gap': self.max_gap, 'threshold': TAU, 'all_reads': answers,
                     'continuous_interpolation_bound_included': True,
                     'physical_durability_or_mass_claim': False})
