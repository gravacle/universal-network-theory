"""M1_check_v001 (dispatch 0457, Claude4 helper M1): exact finite-fiber detailed-balance check of the
whole-path admission residence transport.  Pure Python, single thread, no numpy, no project import.

Part A  independent reference kernel written from the M1 derivation (not from any author code) on tiny
        synthetic toy operators; exact detailed balance (DB) and invariance on every enumerated
        fixed-(k, times) fiber; mutants (sign / count / rate / time-density / target / selection /
        owner-format / inverse-guard / partial-transform).
Part B  the SAME exact-kernel harness applied to Claude3's frozen move (c3v001, hash-pinned, executed
        from source with no bytecode written) through a mock sampler that transcribes the used V004 API
        semantics; entrywise comparison with Part A, input immutability, outcome contract, budget
        interruption at every checkpoint, stored-event corruption, non-canonical state representation.

Toys are NOT the native operator.  'base' mimics V003 admission semantics (admit iff (p,s)=(0,0) ->
(1,1); admit_rev iff (1,1) -> (0,0); q kept; owner ('admission', ('vertex', v)); sector #p == #s);
other variants deliberately generalize (event W depending on s, multi-level admission, hard-core
exclusion, target-changing event, kappa_b = 0, a same-group non-original vertex) or are deliberately
NON-Hermitian / non-involutive ('edgeguard': admit_rev only if e = 0; 'lossy': admit_rev also toggles
q_v if e = 1) so that the per-dwell inverse guard becomes load-bearing.

Usage: python3 -I -B M1_check_v001.py  -> prints a JSON summary; exit status 0 iff every expectation holds.
"""
import sys
sys.dont_write_bytecode = True
import collections
import hashlib
import json
import math

C3_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_0456/'
           'admission_residence_transport_c3v001.py')
C3_SHA = '5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653'
BETA = 1.7
TIMES = {0: (), 2: (0.37, 1.06), 4: (0.15, 0.52, 0.97, 1.38),
         6: (0.11, 0.34, 0.62, 0.95, 1.21, 1.52)}   # odd k fibers are empty in these toys
ADM = ('admit', 'admit_rev')
INV = {'admit': 'admit_rev', 'admit_rev': 'admit'}
REL_TOL = 1e-11
Rec = collections.namedtuple('Rec', 'kind owner target W')

# ------------------------------------------------------------------------------------------------
# Toy operators
# ------------------------------------------------------------------------------------------------
CP = {'a': 0.41, 'b': -0.27, 'n': 0.33}
CS = {'a': -0.58, 'b': 0.36, 'n': -0.21}
CQ = {'a': 0.19, 'b': -0.44, 'n': 0.12}
CPD = {'a': 0.23, 'b': -0.31, 'n': 0.0}
CE, CES, CPQ, CSS = 0.52, -0.47, 0.29, 0.61
H, T = 0.83, 1.21
G = {'a': 0.67, 'b': 1.09, 'n': 0.74}
KAPPA = {'a': 0.91, 'b': 1.37, 'n': 0.58}


class Toy:
    def __init__(self, variant):
        self.variant = variant
        self.verts = ('a', 'b', 'n') if variant == 'newborn' else ('a', 'b')
        self.group = {'a': 'a', 'b': 'b'}
        if variant == 'newborn':
            self.group['n'] = 'a'          # same permanent group as original 'a', not an original
        self.smax = 2 if variant == 'ladder' else 1
        self.kappa = dict(KAPPA)
        if variant == 'kappa0':
            self.kappa['b'] = 0.0
        self._rec = {}

    def i(self, v, f):
        return 1 + 3 * self.verts.index(v) + 'psq'.index(f)

    def get(self, x, v, f):
        return x[self.i(v, f)]

    def put(self, x, **kw):
        y = list(x)
        for name, val in kw.items():
            if name == 'e':
                y[0] = val
            else:
                v, f = name.split('_')
                y[self.i(v, f)] = val
        return tuple(y)

    def states(self):
        out = []
        per = [(p, s, q) for p in (0, 1) for s in range(self.smax + 1) for q in (0, 1)]
        def rec(prefix, left):
            if not left:
                out.append(prefix)
                return
            for t in per:
                rec(prefix + t, left - 1)
        for e in (0, 1):
            rec((e,), len(self.verts))
        if self.variant != 'ladder':      # V003 declared sector: #carriers == #spent
            out = [x for x in out if sum(self.get(x, v, 'p') for v in self.verts)
                   == sum(self.get(x, v, 's') for v in self.verts)]
        return out

    def D(self, x):
        g = self.get
        terms = [CE * x[0], CES * x[0] * g(x, 'a', 's'), CPQ * g(x, 'a', 'p') * g(x, 'b', 'q'),
                 CSS * g(x, 'a', 's') * g(x, 'b', 's')]
        for v in self.verts:
            deg = x[0] if v in ('a', 'b') else 0
            terms += [CP[v] * g(x, v, 'p'), CS[v] * g(x, v, 's'), CQ[v] * g(x, v, 'q'),
                      CPD[v] * g(x, v, 'p') * deg]
        return math.fsum(terms)

    def row(self, x):
        g = self.get
        return (float(g(x, 'a', 's')), float(g(x, 'b', 's')),
                float(g(x, 'a', 'p') + g(x, 'b', 'q')), float(x[0] * g(x, 'a', 's')))

    def records(self, x):
        r = self._rec.get(x)
        if r is None:
            r = self._rec[x] = self._records(x)
        return r

    def _records(self, x):
        g, put, V = self.get, self.put, self.verts
        out = []
        sa, sb = g(x, 'a', 's'), g(x, 'b', 's')
        w = H * (1 + 0.3 * (sa + sb)) if self.variant == 'wdep' else H
        out.append(Rec('flip', ('flip', ('edge', ('a', 'b'))), put(x, e=1 - x[0]), w))
        pa, pb = g(x, 'a', 'p'), g(x, 'b', 'p')
        if x[0] == 1 and pa != pb:
            out.append(Rec('hop', ('hop', ('edge', ('a', 'b'))), put(x, a_p=pb, b_p=pa), T))
        for v in V:
            if g(x, v, 'p') == 1:
                tgt = put(x, **{v + '_q': 1 - g(x, v, 'q')})
                if self.variant == 'cond' and v == 'b' and sa >= 1:
                    tgt = put(tgt, e=1 - x[0])     # target depends on s_a (replay-target test)
                out.append(Rec('bind', ('bind', ('vertex', v)), tgt, G[v]))
        for v in V:
            kap = self.kappa[v]
            if kap == 0.0:
                continue                           # zero amplitude: no positive mark (V004 drops it)
            own = ('admission', ('vertex', v))
            p, s = g(x, v, 'p'), g(x, v, 's')
            if self.variant == 'ladder':
                if s < self.smax:
                    out.append(Rec('admit', own, put(x, **{v + '_s': s + 1}), kap))
                if s > 0:
                    out.append(Rec('admit_rev', own, put(x, **{v + '_s': s - 1}), kap))
            elif p == 0 and s == 0:
                if self.variant == 'hardcore' and any(g(x, u, 's') for u in V if u != v):
                    continue
                out.append(Rec('admit', own, put(x, **{v + '_p': 1, v + '_s': 1}), kap))
            elif p == 1 and s == 1:
                if self.variant == 'edgeguard' and x[0] == 1:
                    continue                       # deliberately missing reverse (non-Hermitian toy)
                tgt = put(x, **{v + '_p': 0, v + '_s': 0})
                if self.variant == 'lossy' and x[0] == 1:
                    tgt = put(tgt, **{v + '_q': 1 - g(x, v, 'q')})   # non-involutive inverse
                out.append(Rec('admit_rev', own, tgt, kap))
        return tuple(out)

    def find(self, x, kind, owner):
        hits = [r for r in self.records(x) if r.kind == kind and r.owner == owner]
        assert len(hits) <= 1
        return hits[0] if hits else None


def closed_paths(toy, k):
    res = []
    for x0 in toy.states():
        if k == 0:
            res.append(((x0,), ()))
            continue
        stack = [((x0,), ())]
        while stack:
            xs, ms = stack.pop()
            if len(ms) == k:
                if xs[-1] == x0:
                    res.append((xs, ms))
                continue
            for r in toy.records(xs[-1]):
                stack.append((xs + (r.target,), ms + ((r.kind, r.owner),)))
    return res


def dts(times):
    ends = (0.0,) + tuple(times) + (BETA,)
    return [ends[i + 1] - ends[i] for i in range(len(ends) - 1)]


def log_pi(toy, xs, ms, times):
    """Independent target: -sum_i dt_i D(x_i) + sum_events log W, zero weight if a mark is invalid."""
    terms = [-dt * toy.D(x) for dt, x in zip(dts(times), xs)]
    for i, (kind, owner) in enumerate(ms):
        r = toy.find(xs[i], kind, owner)
        if r is None or r.target != xs[i + 1]:
            return -math.inf
        terms.append(math.log(r.W))
    return math.fsum(terms)


# ------------------------------------------------------------------------------------------------
# Part A: reference kernel from the derivation, with mutants
# ------------------------------------------------------------------------------------------------
def adm_marks(toy, x, v, mode):
    recs = [r for r in toy.records(x) if r.kind in ADM]
    if mode == 'bare_owner':
        return [r for r in recs if r.owner == ('vertex', v)]
    if mode == 'group_filter':
        return [r for r in recs if toy.group[r.owner[1][1]] == toy.group[v]]
    return [r for r in recs if r.owner == ('admission', ('vertex', v))]


def transport(toy, xs, ms, times, v, m, mutant):
    """(new_xs, new_ms, logR) or (None, reason).  m is the chosen reference mark."""
    kind, owner, inv = m.kind, m.owner, INV[m.kind]
    ys = []
    for x in xs:
        r = toy.find(x, kind, owner)
        if r is None:
            if mutant == 'partial':
                ys.append(x)
                continue
            return None, 'dwell_guard'
        if mutant != 'no_inverse_check':
            b = toy.find(r.target, inv, owner)
            if b is None or b.target != x:
                return None, 'inverse_guard'
        ys.append(r.target)
    if ys[0] != ys[-1]:
        raise AssertionError('closure must hold for a class-function transform')
    new_ms, wterms = [], []
    for i, (k_i, o_i) in enumerate(ms):
        before = toy.find(xs[i], k_i, o_i)
        assert before is not None and before.target == xs[i + 1]
        after = toy.find(ys[i], k_i, o_i)
        if after is None:
            return None, 'replay'
        if mutant != 'no_target' and after.target != ys[i + 1]:
            return None, 'replay_target'
        new_ms.append((k_i, o_i))
        wterms.append(math.log(after.W) - math.log(before.W))
    mode = mutant if mutant in ('bare_owner', 'group_filter') else 'exact'
    fwd = adm_marks(toy, xs[0], v, mode)
    rev = adm_marks(toy, ys[0], v, mode)
    rsel = [r for r in rev if r.kind == inv and r.owner == owner]
    if len(rsel) != 1 or rsel[0].target != xs[0]:
        return None, 'reverse_selection'
    terms = []
    if mutant != 'count':
        terms += [math.log(len(fwd)), -math.log(len(rev))]
    sgn = 1.0 if mutant == 'sign' else -1.0
    d = dts(times)
    for i, (x, y) in enumerate(zip(xs, ys)):
        dt = d[(i + 1) % len(d)] if mutant == 'dt_shift' else d[i]
        terms.append(sgn * dt * (toy.D(y) - toy.D(x)))
    if mutant != 'event_W':
        terms += wterms
    if mutant == 'adm_W':
        terms.append(math.log(m.W))
    if mutant == 'insert_event':
        terms += [math.log(m.W), math.log(BETA), -math.log(len(ms) + 1)]
    return (tuple(ys), tuple(new_ms), math.fsum(terms)), None


def ref_kernel(toy, xs, ms, times, roster, mutant=None):
    """Off-diagonal transition probabilities {path_key: prob}; the rest is self-loop mass."""
    mode = mutant if mutant in ('bare_owner', 'group_filter') else 'exact'
    labels = []                                     # (prob of label, v, mark)
    if mutant == 'resample_guard':
        legal = []
        for v in roster:
            for m in adm_marks(toy, xs[0], v, mode):
                res, _ = transport(toy, xs, ms, times, v, m, None)
                if res is not None:
                    legal.append((v, m))
        labels = [(1.0 / len(legal), v, m) for v, m in legal]
    else:
        vs = list(roster)
        if mutant == 'eligible_only':
            vs = [v for v in roster if adm_marks(toy, xs[0], v, mode)]
        for v in vs:
            marks = adm_marks(toy, xs[0], v, mode)
            for m in marks:
                labels.append((1.0 / (len(vs) * len(marks)), v, m))
    K = {}
    for q, v, m in labels:
        res, _ = transport(toy, xs, ms, times, v, m, None if mutant == 'resample_guard' else mutant)
        if res is None:
            continue
        ys, nms, lr = res
        acc = 1.0 if lr >= 0 else math.exp(lr)
        key = (ys, nms)
        K[key] = K.get(key, 0.0) + q * acc
    return K


def db_report(fiber, kernels):
    """fiber: key -> logpi; kernels: key -> {key2: p}.  Exact pairwise DB and global balance."""
    n_off = viol = off_support = 0
    worst = 0.0
    inflow = collections.defaultdict(float)
    for key, row in kernels.items():
        for key2, p in row.items():
            if key2 == key:
                continue
            n_off += 1
            lp1 = fiber[key]
            lp2 = fiber.get(key2, -math.inf)
            if lp2 == -math.inf:
                off_support += 1
                viol += 1
                continue
            inflow[key2] += math.exp(lp1 - lp2) * p      # sum_w pi(w)K(w,w') / pi(w')
            back = kernels[key2].get(key, 0.0)
            if back == 0.0:
                viol += 1
                worst = max(worst, 1.0)
                continue
            rel = abs(math.expm1((lp2 + math.log(back)) - (lp1 + math.log(p))))
            worst = max(worst, rel)
            if rel > REL_TOL:
                viol += 1
    bal = 0.0
    for key, row in kernels.items():
        out = math.fsum(p for k2, p in row.items() if k2 != key)
        bal = max(bal, abs(inflow.get(key, 0.0) - out))
    return dict(offdiag=n_off, violations=viol, off_support=off_support,
                max_rel_db_error=worst, max_global_balance_error=bal)


def kernels_equal(K1, K2):
    worst = 0.0
    for key in set(K1) | set(K2):
        r1, r2 = K1.get(key, {}), K2.get(key, {})
        for k2 in set(r1) | set(r2):
            a, b = r1.get(k2, 0.0), r2.get(k2, 0.0)
            worst = max(worst, abs(a - b) / max(abs(a), abs(b), 1e-300))
    return worst


VARIANTS = {   # variant -> fibers k (fixed rooted times TIMES[k])
    'base': (0, 2, 4, 6), 'wdep': (0, 2, 4), 'hardcore': (0, 2, 4), 'cond': (0, 2, 4),
    'kappa0': (0, 2, 4), 'ladder': (0, 2, 4), 'newborn': (0, 2), 'edgeguard': (0, 2, 4),
    'lossy': (0, 2, 4),
}
ROSTER = ('a', 'b')     # frozen original-vertex roster (the toy 'n' is never in it)
MUTANTS = ('sign', 'count', 'adm_W', 'insert_event', 'event_W', 'dt_shift', 'no_target',
           'eligible_only', 'resample_guard', 'no_inverse_check', 'bare_owner', 'group_filter',
           'partial')


def build_fibers():
    out = {}
    for var, ks in VARIANTS.items():
        toy = Toy(var)
        for k in ks:
            paths = closed_paths(toy, k)
            fiber = {}
            for xs, ms in paths:
                lp = log_pi(toy, xs, ms, TIMES[k])
                assert lp > -math.inf
                fiber[(xs, ms)] = lp
            out[(var, k)] = (toy, fiber)
    return out


def part_a(fibers):
    res = {}
    ref = {}
    for (var, k), (toy, fiber) in fibers.items():
        K = {key: ref_kernel(toy, key[0], key[1], TIMES[k], ROSTER) for key in fiber}
        ref[(var, k)] = K
        res[f'{var}/k{k}/reference'] = dict(paths=len(fiber), **db_report(fiber, K))
        for mu in MUTANTS:
            Km = {key: ref_kernel(toy, key[0], key[1], TIMES[k], ROSTER, mu) for key in fiber}
            rep = db_report(fiber, Km)
            rep['max_rel_diff_vs_reference'] = kernels_equal(K, Km)
            res[f'{var}/k{k}/{mu}'] = rep
    return res, ref


def zero_event_checks(fibers):
    """k = 0: logR = log(Nf/Nr) - beta (D(y) - D(x)) exactly (no event, no amplitude factor)."""
    worst = 0.0
    n = 0
    for (var, k), (toy, fiber) in fibers.items():
        if k != 0:
            continue
        for (xs, ms) in fiber:
            for v in ROSTER:
                for m in adm_marks(toy, xs[0], v, 'exact'):
                    res, _ = transport(toy, xs, ms, (), v, m, None)
                    if res is None:
                        continue
                    ys, _, lr = res
                    nf = len(adm_marks(toy, xs[0], v, 'exact'))
                    nr = len(adm_marks(toy, ys[0], v, 'exact'))
                    want = math.log(nf / nr) - BETA * (toy.D(ys[0]) - toy.D(xs[0]))
                    worst = max(worst, abs(lr - want))
                    n += 1
    return dict(zero_event_transports=n, max_abs_logR_error=worst)


# ------------------------------------------------------------------------------------------------
# Part B: Claude3 c3v001 through a mock sampler (transcribed V004 semantics of the used API)
# ------------------------------------------------------------------------------------------------
class _Stop(Exception):
    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status, self.stage, self.message = status, stage, message


class _BudgetStop(_Stop):
    def __init__(self, stage, checkpoint):
        _Stop.__init__(self, 'incomplete', stage, 'INCOMPLETE_BUDGET at ' + checkpoint)


class Rep:
    """Non-canonical state representation (identity equality); its canonical key is .x."""
    __slots__ = ('x',)

    def __init__(self, x):
        self.x = x


def canon(state):
    return state.x if isinstance(state, Rep) else state


class MockSampler:
    _Stop = _Stop

    def __init__(self, toy):
        self.toy = toy

    def _budget_check(self, run, phase, what):
        hook = run['budget_hook']
        if hook is None:
            return
        run['counters']['budget_checks'] += 1
        stop = hook()
        if not isinstance(stop, bool):
            raise _Stop('failed', run['stage'], 'budget hook contract')
        if stop:
            raise _BudgetStop(run['stage'], f'{phase} {what}')

    def _record_groups(self, run, kind, owner_id):
        group = run['group']
        labels = None
        try:
            if kind in ('birth', 'birth_rev'):
                if owner_id[0] == 'birth':
                    labels = (owner_id[1],)
            elif kind in ('flip', 'hop'):
                tag, pair = owner_id[1]
                if tag == 'edge' and len(pair) == 2:
                    labels = (pair[0], pair[1])
            elif kind in ('bind', 'admit', 'admit_rev'):
                tag, vertex = owner_id[1]
                if tag == 'vertex':
                    labels = (vertex,)
            if labels is not None:
                return frozenset(group[lab] for lab in labels)
        except (TypeError, KeyError, IndexError, ValueError):
            pass
        raise _Stop('failed', run['stage'], f'unclassifiable owner {owner_id!r}')

    def _palette_channels(self, run, state, owners):
        x = canon(state)
        chans = []
        for r in self.toy.records(x):
            if self._record_groups(run, r.kind, r.owner).isdisjoint(owners):
                continue
            chans.append({'kind': r.kind, 'owner': r.owner, 'target': r.target, 'W': r.W,
                          'mult': 1.0, 'weights': {}, 'sig': None, 'key': None, 'has_key': False})
        return chans, math.fsum(c['W'] for c in chans)

    def _unique_mark(self, run, channels, kind, owner, where):
        hits = [c for c in channels if c['kind'] == kind and self._keys_equal(run, c['owner'], owner)]
        if len(hits) > 1:
            raise _Stop('failed', run['stage'], f'{where}: duplicate (kind, owner)')
        return hits[0] if hits else None

    def _segment_core(self, run, state):
        x = canon(state)
        return {'state': state, 'key': x, 'D': self.toy.D(x), 'r': None, 'Da': None,
                'row': self.toy.row(x), 'allk': None}

    def _target_key(self, run, ch):
        if not ch['has_key']:
            ch['key'] = canon(ch['target'])
            ch['has_key'] = True
        return ch['key']

    def _keys_equal(self, run, a, b):
        eq = a == b
        if isinstance(eq, bool):
            return eq
        raise _Stop('failed', run['stage'], 'keys not comparable')

    def _event_from_channel(self, run, ch):
        return {'kind': ch['kind'], 'owner': ch['owner'], 'W': ch['W'], 'rho': None}

    def _check_times(self, run, times, horizon):
        prev = 0.0
        for t in times:
            if not (t > prev and t < horizon):
                raise _Stop('failed', run['stage'], 'time coincidence')
            prev = t


class ScriptRNG:
    def __init__(self, ints, u=0.0):
        self.ints, self.u, self.calls = list(ints), u, []

    def integers(self, lo, hi):
        self.calls.append(('integers', lo, hi))
        v = self.ints.pop(0)
        assert lo <= v < hi
        return v

    def random(self):
        self.calls.append(('random',))
        return self.u


def load_c3():
    with open(C3_PATH, 'rb') as fh:
        src = fh.read()
    sha = hashlib.sha256(src).hexdigest()
    if sha != C3_SHA:
        raise SystemExit(f'c3v001 hash changed: {sha}')
    ns = {'__name__': 'c3v001_under_test', '__file__': C3_PATH}
    exec(compile(src, C3_PATH, 'exec'), ns)          # no import machinery, no bytecode cache
    return ns['move'], sha


def make_run(toy, hook=None):
    return {'stage': 'm1_toy', 'beta': BETA, 'caps': {'max_events_per_path': 16},
            'group': dict(toy.group), 'budget_hook': hook, 'counters': {'budget_checks': 0}}


def make_path(toy, ms_, run, xs, ms, times, rep=False):
    segs = [ms_._segment_core(run, Rep(x) if rep else x) for x in xs]
    evs = [{'kind': k_, 'owner': o_, 'W': toy.find(xs[i], k_, o_).W, 'rho': None}
           for i, (k_, o_) in enumerate(ms)]
    return {'segments': segs, 'events': evs, 'times': list(times)}


def snapshot(path):
    return (id(path), id(path['segments']), id(path['events']), id(path['times']),
            [(id(s), id(s['state']), s['key'], s['D'], tuple(s['row'])) for s in path['segments']],
            [(id(e), e['kind'], e['owner'], e['W']) for e in path['events']], list(path['times']))


def path_key(path):
    return (tuple(s['key'] for s in path['segments']),
            tuple((e['kind'], e['owner']) for e in path['events']))


def c3_kernel(move, toy, xs, ms, times, roster, stats, lr_log, rep=False):
    sam = MockSampler(toy)
    run = make_run(toy)
    path = make_path(toy, sam, run, xs, ms, times, rep)
    snap = snapshot(path)
    K = {}
    M = len(roster)
    for vi in range(M):
        rng = ScriptRNG([vi, 0])
        diag = {}
        out, oc = move(run, path, rng, diag, sam, roster)
        ints = [c for c in rng.calls if c[0] == 'integers']
        if len(ints) == 1:
            assert oc == 'rejected' and out is path
            stats['empty_reference'] += 1
            continue
        N = ints[1][2]
        for mj in range(N):
            rng = ScriptRNG([vi, mj])
            diag = {}
            out, oc = move(run, path, rng, diag, sam, roster)
            assert snapshot(path) == snap, 'input path mutated'
            if oc == 'rejected':
                assert out is path
                assert diag.get('admission_residence_metropolis', 0) == 0
                assert 'admission_residence_read_integral_change_sum' not in diag
                stats['guard_rejections'] += 1
                continue
            assert oc == 'changed' and out is not path
            assert out['segments'] is not path['segments'] and out['events'] is not path['events']
            assert out['times'] == list(times) and out['times'] is not path['times']
            assert len(out['events']) == len(ms) and len(out['segments']) == len(xs)
            lr = diag['admission_residence_last_proposal']['log_mh_ratio']
            key2 = path_key(out)
            res, _ = transport(toy, xs, ms, times, roster[vi],
                               adm_marks(toy, xs[0], roster[vi], 'exact')[mj], None)
            assert res is not None and (res[0], res[1]) == key2, 'c3 path differs from reference'
            lr_log.append(abs(lr - res[2]))
            acc = 1.0 if lr >= 0 else math.exp(lr)
            K[key2] = K.get(key2, 0.0) + acc / (M * N)
            stats['changed'] += 1
    return K


def interruption_and_contract_tests(move):
    """Budget stop at every checkpoint of selected changed proposals; corruption; roster; repr."""
    out = collections.Counter()
    for var in ('base', 'wdep', 'ladder', 'cond'):
        toy = Toy(var)
        for k in (0, 2, 4):
            chosen = 0
            for xs, ms in closed_paths(toy, k):
                if chosen >= 6:
                    break
                for vi, v in enumerate(ROSTER):
                    marks = adm_marks(toy, xs[0], v, 'exact')
                    for mj, m in enumerate(marks):
                        res, _ = transport(toy, xs, ms, TIMES[k], v, m, None)
                        if res is None:
                            continue
                        chosen += 1
                        sam = MockSampler(toy)
                        calls = [0]
                        def counting():
                            calls[0] += 1
                            return False
                        run = make_run(toy, counting)
                        path = make_path(toy, sam, run, xs, ms, TIMES[k])
                        rng0, d0 = ScriptRNG([vi, mj]), {}
                        o, oc = move(run, path, rng0, d0, sam, ROSTER)
                        assert oc == 'changed'
                        n_total = calls[0]
                        lr = d0['admission_residence_last_proposal']['log_mh_ratio']
                        n_random = sum(1 for c in rng0.calls if c[0] == 'random')
                        assert n_random == (1 if lr < 0 else 0)      # u drawn only when log MH < 0
                        if lr < 0:                    # accept iff u < exp(log MH), u ~ U[0, 1)
                            thr = math.exp(lr)
                            for u, want in ((thr * (1 - 1e-9), 'changed'), (thr * (1 + 1e-9), 'rejected')):
                                dd = {}
                                _, got = move(make_run(toy), path, ScriptRNG([vi, mj], u), dd, sam, ROSTER)
                                assert got == want
                                if want == 'rejected':
                                    assert dd.get('admission_residence_metropolis') == 1
                            out['metropolis_threshold_checked'] += 1
                        for n in range(1, n_total + 1):
                            c = [0]
                            def hook(c=c, n=n):
                                c[0] += 1
                                return c[0] == n
                            run = make_run(toy, hook)
                            path = make_path(toy, sam, run, xs, ms, TIMES[k])
                            snap = snapshot(path)
                            diag = {}
                            try:
                                move(run, path, ScriptRNG([vi, mj]), diag, sam, ROSTER)
                                raise AssertionError('budget stop not propagated')
                            except _Stop as exc:
                                assert exc.status == 'incomplete'
                            assert snapshot(path) == snap
                            assert 'admission_residence_read_integral_change_sum' not in diag
                            assert 'admission_residence_accepted_changed' not in diag
                            out['interruptions_checked'] += 1
                        if ms:                    # stored-event corruption -> hard failure
                            run = make_run(toy)
                            path = make_path(toy, sam, run, xs, ms, TIMES[k])
                            path['events'][0]['W'] *= (1 + 1e-9)
                            try:
                                move(run, path, ScriptRNG([vi, mj]), {}, sam, ROSTER)
                                raise AssertionError('corrupted stored W accepted')
                            except _Stop as exc:
                                assert exc.status == 'failed' and 'inconsistent' in exc.message
                            out['stored_event_corruptions_failed_closed'] += 1
                        # non-canonical representation of the original states: same outcome
                        run = make_run(toy)
                        p1 = make_path(toy, sam, run, xs, ms, TIMES[k])
                        p2 = make_path(toy, sam, run, xs, ms, TIMES[k], rep=True)
                        d1, d2 = {}, {}
                        o1, c1 = move(run, p1, ScriptRNG([vi, mj]), d1, sam, ROSTER)
                        o2, c2 = move(run, p2, ScriptRNG([vi, mj]), d2, sam, ROSTER)
                        assert c1 == c2 == 'changed' and path_key(o1) == path_key(o2)
                        assert d1['admission_residence_last_proposal'] == d2['admission_residence_last_proposal']
                        out['representation_invariant'] += 1
    toy = Toy('base')
    sam = MockSampler(toy)
    x0 = toy.states()[0]
    for bad, roster in (('list', list(ROSTER)), ('dup', ('a', 'a')), ('empty', ()),
                        ('unknown', ('a', 'zz')), ('nonoriginal', None)):
        run = make_run(toy)
        if bad == 'nonoriginal':
            run['group']['n2'] = 'a'
            roster = ('a', 'n2')
        path = make_path(toy, sam, run, (x0,), (), ())
        try:
            move(run, path, ScriptRNG([0, 0]), {}, sam, roster)
            raise AssertionError(f'roster {bad} accepted')
        except _Stop as exc:
            assert exc.status == 'failed'
        out['roster_misuse_failed_closed'] += 1
    run = make_run(toy)
    run['group'] = None
    path = make_path(toy, sam, make_run(toy), (x0,), (), ())
    try:
        move(run, path, ScriptRNG([0, 0]), {}, sam, ROSTER)
        raise AssertionError('missing group accepted')
    except _Stop as exc:
        assert exc.status == 'failed'
    out['no_group_failed_closed'] += 1
    return dict(out)


def part_b(fibers, ref):
    move, sha = load_c3()
    res = {'c3_sha256': sha}
    lr_err = []
    for (var, k), (toy, fiber) in fibers.items():
        stats = collections.Counter()
        Kc = {key: c3_kernel(move, toy, key[0], key[1], TIMES[k], ROSTER, stats, lr_err)
              for key in fiber}
        rep = db_report(fiber, Kc)
        rep['max_rel_diff_vs_reference'] = kernels_equal(ref[(var, k)], Kc)
        rep.update(stats)
        res[f'{var}/k{k}/c3v001'] = rep
    res['max_abs_logMH_diff_vs_reference'] = max(lr_err) if lr_err else None
    res['contract'] = interruption_and_contract_tests(move)
    return res


def expectations(a, b):
    """Return list of failed expectations (empty = all hold)."""
    bad = []
    def chk(cond, msg):
        if not cond:
            bad.append(msg)
    for name, r in a.items():
        var, kk, mu = name.split('/')
        if mu == 'reference' or mu in ('partial', 'group_filter', 'bare_owner'):
            chk(r['violations'] == 0, f'{name}: DB violated')
        if mu == 'reference':
            chk(r['offdiag'] > 0, f'{name}: reference inert')
        if mu == 'partial':
            chk(r['max_rel_diff_vs_reference'] <= REL_TOL, f'{name}: partial differs (boundary lemma)')
        if mu == 'bare_owner':
            chk(r['offdiag'] == 0, f'{name}: bare owner not inert')
    def anyviol(mu, variants):
        return any(a[f'{v}/k{k}/{mu}']['violations'] > 0 for v in variants for k in VARIANTS[v])
    for mu in ('sign', 'adm_W', 'insert_event', 'dt_shift'):
        chk(anyviol(mu, ('base',)), f'mutant {mu} not exposed on base')
    chk(anyviol('count', ('ladder',)), 'count mutant not exposed on ladder')
    chk(not anyviol('count', ('base',)), 'count mutant unexpectedly visible on base (N ratio 1)')
    chk(anyviol('event_W', ('wdep',)), 'event_W mutant not exposed on wdep')
    chk(not anyviol('event_W', ('base',)), 'event_W mutant unexpectedly visible on base')
    chk(anyviol('no_target', ('cond',)), 'no_target mutant not exposed on cond')
    chk(anyviol('eligible_only', ('hardcore',)), 'eligible_only not exposed on hardcore')
    chk(anyviol('resample_guard', ('hardcore',)), 'resample_guard not exposed on hardcore')
    chk(anyviol('no_inverse_check', ('edgeguard',)), 'no_inverse_check not exposed on edgeguard')
    chk(anyviol('no_inverse_check', ('lossy',)), 'no_inverse_check not exposed on lossy')
    chk(not anyviol('no_inverse_check', ('base', 'wdep', 'ladder', 'cond', 'hardcore')),
        'no_inverse_check unexpectedly visible on an involutive toy')
    chk(not anyviol('eligible_only', ('base',)) and not anyviol('resample_guard', ('base',)),
        'selection mutants unexpectedly visible on base')
    for name, r in b.items():
        if isinstance(r, dict) and name.endswith('c3v001'):
            chk(r['violations'] == 0, f'{name}: c3 DB violated')
            chk(r['max_rel_diff_vs_reference'] <= REL_TOL, f'{name}: c3 kernel differs from reference')
    chk(b['max_abs_logMH_diff_vs_reference'] is not None
        and b['max_abs_logMH_diff_vs_reference'] <= 1e-12, 'c3 logMH differs from reference')
    return bad


def main():
    fibers = build_fibers()
    a, ref = part_a(fibers)
    z = zero_event_checks(fibers)
    b = part_b(fibers, ref)
    bad = expectations(a, b)
    if z['max_abs_logR_error'] > 1e-12:
        bad.append('zero-event logR formula')
    matrix = {}
    for mu in ('reference',) + MUTANTS:
        matrix[mu] = {v: '%d/%d' % (sum(a[f'{v}/k{k}/{mu}']['violations'] for k in VARIANTS[v]),
                                     sum(a[f'{v}/k{k}/{mu}']['offdiag'] for k in VARIANTS[v]))
                      for v in VARIANTS}
    c3 = [r for n, r in b.items() if n.endswith('c3v001')]
    totals = dict(paths=sum(a[f'{v}/k{k}/reference']['paths'] for v in VARIANTS for k in VARIANTS[v]),
                  c3_changed_transitions=sum(r['changed'] for r in c3),
                  c3_db_violations=sum(r['violations'] for r in c3),
                  c3_max_rel_diff_vs_reference=max(r['max_rel_diff_vs_reference'] for r in c3),
                  c3_max_rel_db_error=max(r['max_rel_db_error'] for r in c3))
    summary = {'mutant_matrix_violations_over_offdiag': matrix, 'totals': totals,
               'part_a': a, 'zero_event': z, 'part_b': b, 'failed_expectations': bad,
               'verdict': 'ALL_EXPECTATIONS_HOLD' if not bad else 'EXPECTATION_FAILURES'}
    print(json.dumps(summary, indent=1, sort_keys=True, default=str))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
