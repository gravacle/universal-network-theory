"""SOURCE ONLY. Root-gated ctypes ABI for independently reviewed kernel0383.
No library is loaded at import. The root caller must authenticate compiler,
source, shared-library pin, runtime and full original input custody first.
All native calls retain complete PRE/RETURN via caller's durable event function.
Nonzero status discards all scientific buffer contents, retaining failure status.
"""
from array import array
import ctypes as C
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


I64, U64, U32, I32 = C.c_int64, C.c_uint64, C.c_uint32, C.c_int32
TICK = C.CFUNCTYPE(C.c_int, U64, U64)


class Kernel:
    def __init__(self, library_pin, authenticate, n, w, lambdas, guard, event, progress):
        need(type(n) is int and 1 <= n <= 10432, 'ABI dimension')
        need(type(w) is array and w.typecode == 'q' and w.itemsize == 8 and len(w) == 2*n*n, 'whole writable W array')
        need(type(lambdas) is array and lambdas.typecode == 'q' and lambdas.itemsize == 8 and len(lambdas) == n, 'whole lambda array')
        need(w is not lambdas, 'separate owned reference arrays')
        self.n, self.w, self.lambdas = n, w, lambdas
        # from_buffer retains exporter ownership; never resize either exporter.
        self.wp = (I64*len(w)).from_buffer(w)
        self.lp = (I64*n).from_buffer(lambdas)
        self.guard, self.event, self.progress = guard, event, progress
        self.exception = None
        self.serial = 0
        self.call_name = None
        self.callback = TICK(self._tick)
        authenticate(library_pin, retain=False)
        path = Path(library_pin['path'])
        need(path.is_absolute() and path.resolve() == path and not path.is_symlink(), 'literal gated library')
        self.library_pin = dict(library_pin)
        self.library = C.CDLL(str(path))
        self.gram_function = self.library.unt_exact_gram
        self.gram_function.argtypes = [U32, C.POINTER(I64), C.POINTER(U32), C.POINTER(U64), TICK]
        self.gram_function.restype = C.c_int
        self.residual_function = self.library.unt_exact_residual
        self.residual_function.argtypes = [U32, C.POINTER(I64), C.POINTER(I64), C.POINTER(U64),
                                         C.POINTER(U32), C.POINTER(I64), U64, C.POINTER(U32), C.POINTER(U64), TICK]
        self.residual_function.restype = C.c_int
        self.compression_function = self.library.unt_exact_compression
        self.compression_function.argtypes = [U32, C.POINTER(I64), C.POINTER(U32), U32, U32,
                                            C.POINTER(U64), C.POINTER(I32), TICK]
        self.compression_function.restype = C.c_int
        authenticate(library_pin, retain=False)

    def _tick(self, phase, count):
        try:
            self.guard()
            # Inner-loop ticks enforce limits but do not create millions of files.
            if phase in (0, 2, 4):
                self.progress({'call': self.call_name, 'phase': phase, 'count': count})
            return 0
        except BaseException as error:
            self.exception = error
            return 1

    def _begin(self, kind, detail):
        self.guard()
        self.exception = None
        self.call_name = '%06d_%s' % (self.serial, kind)
        self.serial += 1
        self.event(self.call_name+'_PRE', {'kernel': kind, 'dimension': self.n,
                  'library': self.library_pin, 'detail': detail})

    def _end(self, status, result):
        if status or self.exception is not None:
            self.event(self.call_name+'_RETURN', {'status': int(status), 'accepted_buffers': False,
                'callback_exception': None if self.exception is None else
                    {'type': type(self.exception).__name__, 'message': str(self.exception)}})
            if self.exception is not None:
                raise self.exception
            raise ValueError('exact compiled kernel refused, status '+str(status))
        self.guard()
        self.event(self.call_name+'_RETURN', {'status': 0, 'accepted_buffers': True, 'value': result})
        return result

    def gram(self):
        sums = (U32*(16*self.n))()
        meta = (U64*(3*self.n))()
        self._begin('GRAM', {'all_entries': self.n*self.n, 'squared_denominator': 1 << 220,
                            'output_uint32_limbs': 16*self.n, 'metadata_uint64': 3*self.n})
        status = self.gram_function(self.n, self.wp, sums, meta, self.callback)
        if status or self.exception is not None:
            return self._end(status, None)
        columns = [sum(int(sums[16*j+k]) << (32*k) for k in range(16)) for j in range(self.n)]
        metadata = [{'column': j, 'max_abs_integer_component': int(meta[3*j]),
                     'component_l1_integer': int(meta[3*j+1])+(int(meta[3*j+2]) << 64)} for j in range(self.n)]
        return self._end(status, {'squared_column_numerators': columns,
             'squared_total_numerator': sum(columns), 'squared_denominator': 1 << 220,
             'complete_column_metadata': metadata, 'complete_gram_entry_count': self.n*self.n,
             'signed128_global_dot_plus_diagonal_bound': 2*self.n*(1 << 112)+(1 << 110),
             'tighter_pair_component_bound_rule': 'min(max_j*L1_k,max_k*L1_j), every actual pair checked before diagonal subtraction',
             'all_squares_accumulator_bits': 512})

    def residual(self, rows):
        need(type(rows) is list and len(rows) == self.n, 'complete H rows')
        offsets, indices, entries, row_norms = [0], [], [], []
        for row in rows:
            need(type(row) is list, 'H row')
            previous, row_norm = -1, 0
            for term in row:
                need(type(term) is list and len(term) == 3 and all(type(x) is int for x in term), 'exact Gaussian integer H term')
                col, re, im = term
                need(previous < col < self.n and (re or im), 'unique sorted complete H row indices')
                need(max(abs(re), abs(im)) < 1 << 63, 'signed64 H entries')
                previous = col
                row_norm += abs(re)+abs(im)
                indices.append(col)
                entries.extend((re, im))
            need(row_norm <= 10207, 'declared H row bound')
            row_norms.append(row_norm)
            offsets.append(len(indices))
        need(len(indices) <= 64*self.n, 'declared CSR size')
        off = (U64*len(offsets))(*offsets)
        ix = (U32*max(1,len(indices)))(*indices)
        val = (I64*max(1,len(entries)))(*entries)
        sums, norms = (U32*(16*self.n))(), (U64*self.n)()
        self._begin('RESIDUAL', {'rows': rows, 'nnz': len(indices), 'denominator': 560*(1 << 103),
                                'squared_denominator': 560**2*(1 << 206)})
        status = self.residual_function(self.n, self.wp, self.lp, off, ix, val,
                                       len(indices), sums, norms, self.callback)
        if status or self.exception is not None:
            return self._end(status, None)
        need(list(norms) == row_norms, 'all native row bounds match ABI return')
        columns = [sum(int(sums[16*j+k]) << (32*k) for k in range(16)) for j in range(self.n)]
        return self._end(status, {'squared_column_numerators': columns,
             'squared_total_numerator': sum(columns), 'squared_denominator': 560**2*(1 << 206),
             'all_row_l1_integers': list(norms), 'complete_residual_entry_count': self.n*self.n,
             'signed128_component_bound': 10207*(1 << 56)*(1 << 48)+560*(1 << 56)*20*(1 << 48),
             'all_squares_accumulator_bits': 512})

    def compression(self, weights, first, rank, label, weights_reference):
        need(type(first) is int and type(rank) is int and 0 <= first < self.n and
             1 <= rank <= 16 and first+rank <= self.n, 'whole small cluster')
        need(type(weights) is list and len(weights) == self.n and
             all(type(x) is int and 0 <= x <= 4 for x in weights), 'complete exact read diagonal')
        need(type(weights_reference) is dict and set(weights_reference) == {'file', 'field'}, 'full retained diagonal reference')
        weight = (U32*self.n)(*weights)
        magnitudes, signs = (U64*(4*rank*rank))(), (I32*(2*rank*rank))()
        self._begin('COMPRESSION', {'first': first, 'rank': rank, 'read': label,
            'weights_reference': weights_reference, 'entry_denominator': 1 << 110,
            'weighted_partial_sum_bound': 'sum_i weight_i*(abs(Re W_ij)+abs(Im W_ij))*(abs(Re W_ik)+abs(Im W_ik)) < 2^127; checked for every pair before dot'})
        status = self.compression_function(self.n, self.wp, weight, first, rank,
                                          magnitudes, signs, self.callback)
        if status or self.exception is not None:
            return self._end(status, None)
        matrix = []
        for j in range(rank):
            row = []
            for k in range(rank):
                entry = []
                for z in (0, 1):
                    q = 2*(j*rank+k)+z
                    magnitude = int(magnitudes[2*q])+(int(magnitudes[2*q+1]) << 64)
                    sign = int(signs[q])
                    need(sign in (-1, 0, 1) and ((sign == 0) == (magnitude == 0)), 'canonical signed magnitude wire')
                    entry.append(sign*magnitude)
                row.append(entry)
            matrix.append(row)
        return self._end(status, {'first': first, 'rank': rank, 'read': label,
             'entry_denominator': 1 << 110, 'complete_gaussian_integer_matrix': matrix})
