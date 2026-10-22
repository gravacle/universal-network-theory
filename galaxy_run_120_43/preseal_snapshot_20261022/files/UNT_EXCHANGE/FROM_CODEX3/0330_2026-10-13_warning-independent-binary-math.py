"""SOURCE ONLY, root executes. Stdlib NPY/IEEE754 interpretation, no NumPy.
Complete dyadic dots use integer units2^-1074, not producer Fraction-per-product.
"""
import ast
from array import array
from fractions import Fraction as Q
import hashlib
import math
import mmap
from pathlib import Path
import struct
import sys

CELLS = ((0, 0), (0, 1), (1, 0), (1, 1), (127, 10430), (127, 10431))


def need(ok, why):
    if not ok:
        raise ValueError(why)


class Npy:
    def __init__(self, path, shape, dtype):
        self.path = Path(path)
        self.stream = self.path.open('rb')
        self.data = mmap.mmap(self.stream.fileno(), 0, access=mmap.ACCESS_READ)
        need(self.data[:6] == b'\x93NUMPY', 'literal NPY magic')
        version = tuple(self.data[6:8])
        need(version in ((1, 0), (2, 0), (3, 0)), 'bounded standard NPY version')
        width = 2 if version == (1, 0) else 4
        length = int.from_bytes(self.data[8:8+width], 'little')
        self.offset = 8+width+length
        need(0 < length <= 4096 and self.data[self.offset-1:self.offset] == b'\n', 'whole bounded NPY header')
        header = ast.literal_eval(self.data[8+width:self.offset].decode('utf8' if version == (3, 0) else 'latin1'))
        need(type(header) is dict and set(header) == {'descr', 'fortran_order', 'shape'}, 'closed NPY header')
        need(header['descr'] == dtype and header['shape'] == shape and type(header['fortran_order']) is bool,
             'literal complete NPY dtype and shape')
        self.shape, self.dtype, self.fortran = shape, dtype, header['fortran_order']
        self.itemsize = {'<c16': 16, '<f8': 8}[dtype]
        self.nbytes = math.prod(shape)*self.itemsize
        need(len(self.data) == self.offset+self.nbytes, 'complete NPY data with no suffix')

    def meta(self):
        strides = [0]*len(self.shape)
        stride = self.itemsize
        order = range(len(self.shape)) if self.fortran else range(len(self.shape)-1, -1, -1)
        for i in order:
            strides[i] = stride
            stride *= self.shape[i]
        return {'shape': list(self.shape), 'dtype': self.dtype, 'strides': strides,
                'C_contiguous': not self.fortran or len(self.shape) == 1,
                'F_contiguous': self.fortran or len(self.shape) == 1, 'nbytes': self.nbytes}

    def position(self, i, j):
        need(len(self.shape) == 2 and 0 <= i < self.shape[0] and 0 <= j < self.shape[1], 'complete coordinate')
        index = j*self.shape[0]+i if self.fortran else i*self.shape[1]+j
        return self.offset+16*index

    def complex_bits(self, i, j):
        return struct.unpack_from('<QQ', self.data, self.position(i, j))

    def scan(self, guard, bound=None):
        h = hashlib.sha256()
        for pos in range(self.offset, len(self.data), 1 << 20):
            chunk = self.data[pos:min(pos+(1 << 20), len(self.data))]
            h.update(chunk)
            values = array('d')
            values.frombytes(chunk)
            if sys.byteorder != 'little':
                values.byteswap()
            need(all(map(math.isfinite, values)), 'every full array scalar finite')
            if bound is not None:
                need(max(values) <= bound and min(values) >= -bound, 'every full input component bounded')
            guard()
        return h.hexdigest()

    def close(self):
        self.data.close()
        self.stream.close()


def units(bits):
    sign = -1 if bits >> 63 else 1
    exponent, mantissa = (bits >> 52) & 2047, bits & ((1 << 52)-1)
    need(exponent < 2047, 'finite exact IEEE754 input')
    return sign*(mantissa if exponent == 0 else ((1 << 52)+mantissa) << (exponent-1))


def exact_value(bits):
    return Q(units(bits), 1 << 1074)


def verify_left(V, left, guard):
    # Full logical transpose/conjugation identity, including every signed zero.
    need(V.shape == (10432, 10432) and left.shape == (128, 10432), 'complete actual left shape')
    for k in range(10432):
        for i in range(128):
            r, s = V.complex_bits(k, i)
            need(left.complex_bits(i, k) == (r, s ^ (1 << 63)), 'every actual left operand bit')
        if k % 128 == 0:
            guard()


def tiny(pre, result, kind):
    matrices = [((1, 0), (0, 0), (0, 0), (1, 0)),
                ((0, 0), (0, 0), (0, 0), (0, 0)),
                ((1, 0), (0, 1), (0, -1), (1, 0))]
    desired = matrices[kind]
    need(len(pre) == len(result) == 64, 'all four Gaussian operand/result entries')
    operand = [tuple(map(exact_value, z)) for z in struct.iter_unpack('<QQ', pre)]
    actual = [tuple(map(exact_value, z)) for z in struct.iter_unpack('<QQ', result)]
    need(operand == list(desired), 'all exact tiny operand entries')
    expected = []
    for i in range(2):
        for j in range(2):
            re = im = 0
            for k in range(2):
                a, b = desired[2*i+k]
                c, d = desired[2*k+j]
                re += a*c-b*d
                im += a*d+b*c
            expected.append((Q(re), Q(im)))
    need(actual == expected, 'all nine complete exact dyadic tiny products')
    # Raw hex is retained by outer receipt. Equality here concerns exact
    # dyadic values: signed zero differences are not nonzero numeric errors.


def six_cells(V, products, guard):
    answer = []
    n = 10432
    for i, j in CELLS:
        real_sum = imag_sum = absolute_real = absolute_imag = 0
        for k in range(n):
            a, b = (units(v) for v in V.complex_bits(k, i))
            c, d = (units(v) for v in V.complex_bits(k, j))
            ac, bd, ad, bc = a*c, b*d, a*d, b*c
            real_sum += ac+bd
            imag_sum += ad-bc
            absolute_real += abs(ac)+abs(bd)
            absolute_imag += abs(ad)+abs(bc)
            if k % 256 == 0:
                guard()
        rr, ii, ar, ai = (Q(v, 1 << 2148) for v in (real_sum, imag_sum, absolute_real, absolute_imag))
        # Algebraically rearranged depth2n envelope; no Accelerate model claim.
        gamma = Q(2*n, (1 << 53)-2*n)
        eta = Q(4*n*(1 << 53), ((1 << 53)-2*n)*(1 << 1074))
        br, bi = gamma*ar+eta, gamma*ai+eta
        comparisons = []
        for label, product in zip(('MAPPED_ORIGINAL', 'FULL_C_COPY'), products):
            vr, vi = (exact_value(v) for v in product.complex_bits(i, j))
            comparisons.append({'case': label, 'actual_binary64_as_rational': [str(vr), str(vi)],
                'signed_error': [str(vr-rr), str(vi-ii)],
                'within_stated_scalar_model_envelope': abs(vr-rr) <= br and abs(vi-ii) <= bi})
        answer.append({'cell': [i, j], 'all_summands': n,
            'exact_binary64_input_dot': [str(rr), str(ii)],
            'sum_absolute_real_products': str(ar), 'sum_absolute_imag_products': str(ai),
            'stated_scalar_model_error_envelope': [str(br), str(bi)], 'all_two_actual_products': comparisons})
    return {'schema': 'SIX_COMPLETE_BINARY64_DOTS_V001', 'cells': answer,
            'model': 'SEPARATE_RN_BINARY64_REAL_PRODUCTS_AND_SEQUENTIAL_SUM; GAMMA_2N; ABS_UNDERFLOW_ALLOWANCE4N*2^-1074',
            'model_applies_to_unchecked_Accelerate': False, 'unselected_cells_certified': False}
