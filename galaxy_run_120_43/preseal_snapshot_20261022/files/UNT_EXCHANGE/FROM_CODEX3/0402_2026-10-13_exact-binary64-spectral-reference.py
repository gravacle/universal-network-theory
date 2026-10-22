"""SOURCE ONLY: exact W55/lambda48 reconstruction, without NumPy or float arithmetic.
Root caller authenticates complete original files before/after this module's use.
No dense reference file is written. RAM W=16*n*n bytes, E=8*n bytes;
read-only original mmap pages are also charged to the root process RSS cap.
This module establishes reference conversion only, not spectral certification.
"""
import ast
from array import array
import hashlib
import mmap
from pathlib import Path
import struct
import sys


def need(ok, why):
    if not ok:
        raise ValueError(why)


def scaled_binary64(bits, scale, floor=False):
    """Return exact scaled integer: truncate, or floor including negative tails."""
    need(type(bits) is int and 0 <= bits < 1 << 64, 'binary64 bits')
    need(type(scale) is int and 0 <= scale <= 128, 'binary scale')
    sign = bits >> 63
    exp = (bits >> 52) & 2047
    mantissa = bits & ((1 << 52)-1)
    need(exp != 2047, 'nonfinite binary64 reference')
    if exp:
        mantissa |= 1 << 52
        power = exp - 1075 + scale
    else:
        power = -1074 + scale
    if power >= 0:
        integer, tail = mantissa << power, False
    else:
        integer = mantissa >> (-power)
        tail = mantissa != integer << (-power)
    if sign:
        return -integer - int(floor and tail)
    return integer


class OriginalArray:
    def __init__(self, pin, dtype, shape, guard):
        need(set(pin) == {'path', 'sha256', 'bytes'}, 'complete original pin')
        self.path = Path(pin['path'])
        need(self.path.is_absolute() and self.path.resolve() == self.path and
             self.path.is_file() and not self.path.is_symlink(), 'plain original array')
        self.file = self.path.open('rb')
        self.mapping = None
        try:
            need(self.file.seek(0, 2) == pin['bytes'], 'complete original size')
            self.file.seek(0)
            digest = hashlib.sha256()
            while True:
                block = self.file.read(1 << 20)
                if not block:
                    break
                digest.update(block)
                guard()
            need(digest.hexdigest() == pin['sha256'], 'complete original hash')
            self.mapping = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)
            m = self.mapping
            need(m[:6] == b'\x93NUMPY', 'NPY magic')
            version = tuple(m[6:8])
            need(version in ((1, 0), (2, 0), (3, 0)), 'NPY version')
            size_bytes = 2 if version == (1, 0) else 4
            length = int.from_bytes(m[8:8+size_bytes], 'little')
            start = 8 + size_bytes
            need(0 < length <= 65536 and start+length <= len(m), 'NPY header length')
            raw = m[start:start+length]
            need(raw.endswith(b'\n'), 'NPY header terminator')
            header = ast.literal_eval(raw.decode('utf-8' if version == (3, 0) else 'latin1').strip())
            need(type(header) is dict and set(header) == {'descr', 'fortran_order', 'shape'}, 'NPY closed header')
            need(header['descr'] in ('<'+dtype, '>'+dtype), 'explicit binary64 dtype/endian')
            need(type(header['fortran_order']) is bool and type(header['shape']) is tuple and
                 all(type(x) is int for x in header['shape']) and header['shape'] == shape, 'NPY exact shape/order')
            self.offset = start + length
            count = 1
            for d in shape:
                count *= d
            itemsize = 16 if dtype == 'c16' else 8
            need(dtype in ('c16', 'f8') and len(m) == self.offset + count*itemsize, 'complete NPY payload')
            self.header = header
            self.unpack = struct.Struct(header['descr'][0]+'Q').unpack_from
            self.pin = dict(pin)
        except BaseException:
            self.close()
            raise

    def bits(self, index):
        return self.unpack(self.mapping, self.offset + 8*index)[0]

    def rehash(self, guard):
        self.file.seek(0)
        digest = hashlib.sha256()
        size = 0
        while True:
            block = self.file.read(1 << 20)
            if not block:
                break
            size += len(block)
            digest.update(block)
            guard()
        need(size == self.pin['bytes'] and digest.hexdigest() == self.pin['sha256'], 'closing complete original hash')

    def close(self):
        if self.mapping is not None:
            self.mapping.close()
            self.mapping = None
        self.file.close()


def reconstruct(v_pin, e_pin, n, guard, progress):
    """Fully pinned originals -> new exact references, both retained by caller in RAM.

    Progress callback is documentary; exceptions abort conversion. Every original
    scalar is visited, finite/range checked and converted. Original E order is
    checked exactly by its scale-free dyadic ordering, before lambda flooring.
    """
    need(type(n) is int and 1 <= n <= 10432, 'reference dimension')
    need(array('q').itemsize == 8 and sys.byteorder in ('little', 'big'), 'signed64 reference storage')
    v = OriginalArray(v_pin, 'c16', (n, n), guard)
    try:
        e = OriginalArray(e_pin, 'f8', (n,), guard)
        try:
            w = array('q', [0]) * (2*n*n)
            lambdas = array('q', [0]) * n
            columns = []
            previous = None
            max_lambda = 0
            # Normalize signed zero in ordering; positive/negative finite IEEE
            # words are monotone under this exact integer key transformation.
            for j in range(n):
                bits = e.bits(j)
                absolute = bits & ((1 << 63)-1)
                need((absolute >> 52) != 2047, 'finite original energy')
                key = 0 if absolute == 0 else (-absolute if bits >> 63 else absolute)
                need(previous is None or key >= previous, 'complete original energy ordering')
                previous = key
                value = scaled_binary64(bits, 48, floor=True)
                need(abs(value) <= 20*(1 << 48), 'lambda48 declared bound')
                lambdas[j] = value
                max_lambda = max(max_lambda, abs(value))
            for j in range(n):
                maximum, l1, nonzero = 0, 0, 0
                for i in range(n):
                    source_index = j*n+i if v.header['fortran_order'] else i*n+j
                    for component in (0, 1):
                        bits = v.bits(2*source_index+component)
                        absolute = bits & ((1 << 63)-1)
                        need(absolute <= 0x4000000000000000, 'finite original component bounded by two')
                        value = scaled_binary64(bits, 55)
                        need(abs(value) <= 1 << 56, 'W55 bound')
                        w[2*(j*n+i)+component] = value
                        maximum = max(maximum, abs(value))
                        l1 += abs(value)
                        nonzero += int(value != 0)
                    if i % 256 == 0:
                        guard()
                record = {'column': j, 'max_abs_integer_component': maximum,
                          'component_l1_integer': l1, 'nonzero_integer_components': nonzero}
                columns.append(record)
                progress(record)
            v.rehash(guard)
            e.rehash(guard)
            return w, lambdas, {
                'schema': 'EXACT_W55_LAMBDA48_REFERENCE_V001',
                'dimension': n, 'original_vectors': dict(v_pin), 'original_values': dict(e_pin),
                'original_vector_header': v.header, 'original_value_header': e.header,
                'vector_rule': 'each binary64 component scaled by 2^55 and truncated toward zero',
                'value_rule': 'each binary64 value scaled by 2^48 and floored toward negative infinity',
                'layout': 'column-major interleaved signed64 real,imag in memory',
                'dense_reference_storage': 'RAM only; fully reconstructible from complete pinned immutable originals',
                'dense_reference_bytes': 16*n*n, 'lambda_reference_bytes': 8*n,
                'original_mmap_bytes': v_pin['bytes']+e_pin['bytes'],
                'lambda_integers': list(lambdas), 'lambda_max_abs_integer': max_lambda,
                'columns': columns, 'original_arrays_rehashed_after_conversion': True,
                'no_spectral_certificate_from_conversion_alone': True}
        finally:
            e.close()
    finally:
        v.close()
