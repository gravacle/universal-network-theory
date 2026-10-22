"""Exact-enumeration fixtures for owned_worm_loop_whole_path_c2v001.py (synthetic explicit states only).

Never imports the native operator or sampler; never samples.  Usage:
  python3 -I -B worm_loop_fixture_c2v001.py <module_sha256> <output_json>
The output file is created exclusively ('x').  Sections:
  F1 pure-walk proposal symmetry (exact Fractions): every closed walk's reverse walk regenerates the
     same loop with the identical integer branching product, is produced by grow_walk itself under
     scripted choices, reverse(reverse) = identity, and the aggregated proposal kernel is symmetric
     Q(a->b) = Q(b->a); graphs: Q3 (4-cycles, all 4096 incidence words), honeycomb 2x3 (sectors) and
     3x3 (dimer sector) tori and the L=2 periodic diamond (ice sector subset, walk level).
  F2 end-to-end exact kernel of move() by exhaustive scripted-RNG enumeration against the toy
     target on closed path sets (no events, flip pair, hop pair, Birth/reverse, mixed): detailed
     balance pi(a)T(a,b) = pi(b)T(b,a), rows sum to one, every output path independently valid,
     input never mutated, and T equal to an independently coded oracle kernel.
  F3 forward + reverse log MH = 0 (exact) and the reverse move returns the original path.
  F4 event replay accounting, F5 guards / no resampling, F6 interruption atomicity at every
     budget checkpoint of an accepted eventful proposal.
  F7 mutants (wrong reverse probability, missing branching factor, one-dwell-only flip, one-dwell
     flip with guards removed) must be caught; a symmetric-omission control must pass.
  F8 the literal walk rule (LOOKAHEAD = False, in-memory one-constant variant): F1 (Q3, honeycomb
     3x3) and F2 (sector cases) repeated; both rules must pass.
"""
import copy
import hashlib
import importlib.util
import json
import math
import sys
import time
import types
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE / 'owned_worm_loop_whole_path_c2v001.py'
TOY = HERE / 'worm_fixture_toy_c2v001.py'


def load_source(src, name):
    mod = types.ModuleType(name)
    mod.__file__ = '<' + name + '>'
    exec(compile(src, name, 'exec'), mod.__dict__)
    return mod


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = None  # toy library module


class NeedChoice(Exception):
    def __init__(self, n):
        Exception.__init__(self, n)
        self.n = n


class ScriptRNG:
    def __init__(self, prefix, uniform=0.0):
        self.prefix, self.i, self.ns = list(prefix), 0, []
        self.uniform, self.random_calls = uniform, 0

    def integers(self, low, high):
        n = high - low
        if self.i < len(self.prefix):
            v = self.prefix[self.i]
            assert 0 <= v < n, (v, n)
            self.i += 1
            self.ns.append(n)
            return low + v
        raise NeedChoice(n)

    def random(self):
        self.random_calls += 1
        return self.uniform


def prod(xs):
    p = 1
    for x in xs:
        p *= x
    return p


def bits(x):
    i = 0
    while x:
        if x & 1:
            yield i
        x >>= 1
        i += 1


def other(e, v):
    return e[1] if v == e[0] else e[0]


LOOK = {'value': True}  # set from the module under test; the oracle re-implements the rule


def own_candidates(colouring, v, colour, visited=(), lookahead=None):
    """Independent re-implementation of the walk's candidate rule (sorted edge labels)."""
    lookahead = LOOK['value'] if lookahead is None else lookahead
    out = []
    for e in sorted(colouring):
        if v not in e or colouring[e] != colour:
            continue
        w = other(e, v)
        if lookahead and w not in visited and not any(
                w in f and colouring[f] == 1 - colour for f in colouring):
            continue
        out.append(e)
    return out


def reverse_prefix(roster, colouring_rev, start, rev_edges):
    """Independent: scripted choice indices that make grow_walk generate rev_edges."""
    prefix = [list(roster).index(start)]
    v, need, seen = start, 1, {start}
    for e in rev_edges:
        prefix.append(own_candidates(colouring_rev, v, need, seen).index(e))
        v = other(e, v)
        seen.add(v)
        need ^= 1
    return prefix


def subsets_with_degrees(edges, target):
    """All edge subsets whose degree at every vertex equals target[v] (recursive)."""
    edges = sorted(edges)
    out = []
    remaining = {}
    for a, b in edges:
        remaining[a] = remaining.get(a, 0) + 1
        remaining[b] = remaining.get(b, 0) + 1
    need = dict(target)

    def rec(i, chosen):
        if i == len(edges):
            if all(v == 0 for v in need.values()):
                out.append(frozenset(chosen))
            return
        a, b = edges[i]
        remaining[a] -= 1
        remaining[b] -= 1
        if need[a] > 0 and need[b] > 0:
            need[a] -= 1
            need[b] -= 1
            chosen.append(edges[i])
            if need[a] <= remaining[a] and need[b] <= remaining[b]:
                rec(i + 1, chosen)
            chosen.pop()
            need[a] += 1
            need[b] += 1
        if need[a] <= remaining[a] and need[b] <= remaining[b]:
            rec(i + 1, chosen)
        remaining[a] += 1
        remaining[b] += 1
    rec(0, [])
    return out


def degree_vector(vertices, inc):
    d = {v: 0 for v in vertices}
    for a, b in inc:
        d[a] += 1
        d[b] += 1
    return tuple(d[v] for v in vertices)


# ======================== F1: pure walk symmetry =============================================
def walk_dfs_prefixed(mod, colouring, roster):
    out, stack = [], [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        try:
            w = mod.grow_walk(colouring, roster, lambda n: rng.integers(0, n), mod.MAX_WALK_STEPS)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        out.append((Fraction(1, prod(rng.ns)), w, prefix))
    return out


def walk_dfs(mod, colouring, roster):
    out, stack = [], [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        try:
            w = mod.grow_walk(colouring, roster, lambda n: rng.integers(0, n), mod.MAX_WALK_STEPS)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        out.append((Fraction(1, prod(rng.ns)), w))
    return out


def f1_graph(mod, name, vertices, edges, states, roster, shift=None, periods=None, aggregate=True):
    t0 = time.time()
    n_walks = n_closed = 0
    lengths, wind = {}, {'winding': 0, 'contractible': 0}
    Q = {}
    state_set = set(states)
    for inc in states:
        colouring = {e: (1 if e in inc else 0) for e in edges}
        row = {}
        walks = walk_dfs(mod, colouring, roster)
        assert sum(p for p, _ in walks) == 1, name
        for p, w in walks:
            n_walks += 1
            if w['status'] != 'closed':
                continue
            n_closed += 1
            ew, c = w['edges'], w['closure']
            loop = ew[c:]
            assert mod.loop_contract(colouring, loop)
            assert w['branch_product'] == prod(w['counts'])
            assert p == Fraction(1, len(roster) * w['branch_product'])
            assert mod.walk_branch_product(colouring, roster, w['start'], ew, mod.MAX_WALK_STEPS) == w['branch_product']
            new_inc = frozenset(set(inc) ^ set(loop))
            col_rev = {e: (1 if e in new_inc else 0) for e in edges}
            rev = mod.reverse_edges(ew, c)
            assert mod.reverse_edges(rev, c) == list(ew)
            assert mod.walk_branch_product(col_rev, roster, w['start'], rev, mod.MAX_WALK_STEPS) == w['branch_product']
            rng = ScriptRNG(reverse_prefix(roster, col_rev, w['start'], rev))
            w2 = mod.grow_walk(col_rev, roster, lambda n: rng.integers(0, n), mod.MAX_WALK_STEPS)
            assert w2['status'] == 'closed' and w2['edges'] == rev and w2['closure'] == c
            assert w2['branch_product'] == w['branch_product']
            lengths[len(loop)] = lengths.get(len(loop), 0) + 1
            if shift is not None:
                v, seq = w['closure_vertex'], []
                for e in loop:
                    seq.append((v, e))
                    v = other(e, v)
                assert v == w['closure_vertex']
                wv = T.winding(seq, shift, periods)
                wind['winding' if any(wv) else 'contractible'] += 1
            if aggregate:
                row[new_inc] = row.get(new_inc, Fraction(0)) + p
        if aggregate:
            assert all(b in state_set for b in row), name
            Q[inc] = row
    pairs = 0
    if aggregate:
        for a, row in Q.items():
            for b, q in row.items():
                if b != a:
                    assert Q[b].get(a, Fraction(0)) == q, (name, 'asymmetric proposal kernel')
                    pairs += 1
    res = {'graph': name, 'vertices': len(vertices), 'edges': len(edges), 'states': len(states),
           'walks_enumerated': n_walks, 'closed_walks': n_closed,
           'aggregate_symmetric_ordered_pairs': pairs if aggregate else 'walk_level_only',
           'closed_loop_length_counts': {str(k): v for k, v in sorted(lengths.items())},
           'seconds': round(time.time() - t0, 2)}
    if shift is not None:
        res['closed_walk_loops_by_winding'] = wind
    return res


def section_f1(mod):
    out = []
    A, B, edges, _ = T.cube_q3()
    allstates = []
    for m in range(1 << len(edges)):
        allstates.append(frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1))
    out.append(f1_graph(mod, 'Q3_cube_all_4096', A + B, sorted(edges), allstates, A + B))
    A, B, edges, shift, per = T.honeycomb_torus(2, 3)
    V = A + B
    sectors = {}
    for m in range(1 << len(edges)):
        inc = frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1)
        sectors.setdefault(degree_vector(V, inc), []).append(inc)
    ones, twos = tuple([1] * len(V)), tuple([2] * len(V))
    mixed = sorted((dv for dv in sectors if 0 in dv and 3 in dv), key=lambda dv: (-len(sectors[dv]), dv))[0]
    chosen = sectors[ones] + sectors[twos] + sectors[mixed]
    out.append(f1_graph(mod, 'honeycomb_2x3_torus_d1_d2_and_largest_defect_sector', V, sorted(edges),
                        chosen, V, shift, per))
    out[-1]['defect_sector_degree_vector'] = list(mixed)
    A, B, edges, shift, per = T.honeycomb_torus(3, 3)
    V = A + B
    dimers = subsets_with_degrees(edges, {v: 1 for v in V})
    out.append(f1_graph(mod, 'honeycomb_3x3_torus_dimer_sector', V, sorted(edges), dimers, V, shift, per))
    A, B, edges, shift, per = T.diamond_torus(2)
    V = A + B
    ice = sorted(subsets_with_degrees(edges, {v: 2 for v in V}), key=lambda s: sorted(s))
    sub = ice[::max(1, len(ice) // 24)][:24]
    r = f1_graph(mod, 'diamond_L2_torus_ice_sector_subset', V, sorted(edges), sub, V, shift, per, aggregate=False)
    r['ice_sector_size'] = len(ice)
    out.append(r)
    return out


# ======================== F2: end-to-end exact kernel =========================================
def path_sig(path):
    return T.path_signature(path)


def module_row(mod, toy, run, path, roster, legal=None, counters=None):
    """Exact kernel row of mod.move from `path` by exhaustive scripted choices."""
    row, flags = {}, {'invalid_output_path': 0, 'left_closed_set': 0, 'exceptions': []}
    sig_a = path_sig(path)
    snapshot = copy.deepcopy(path)
    stack = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        diag = {'sweeps_completed': 0}
        try:
            new, status = mod.move(run, path, rng, diag, toy, roster, toy.state_labels)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        except T.ToyStop as exc:
            flags['exceptions'].append(exc.status + ': ' + exc.message)
            continue
        if counters is not None:
            for k, v in diag.items():
                if isinstance(v, int) and not isinstance(v, bool):
                    counters[k] = counters.get(k, 0) + v
        p = 1.0 / prod(rng.ns)
        if status == 'changed':
            lr = diag['worm_loop_last_proposal']['log_mh_ratio']
            assert rng.random_calls == (1 if lr < 0 else 0)
            a = 1.0 if lr >= 0 else math.exp(lr)
            if not T.validate_path(toy, run, new):
                flags['invalid_output_path'] += 1
            sig_b = path_sig(new)
            row[sig_b] = row.get(sig_b, 0.) + p * a
            row[sig_a] = row.get(sig_a, 0.) + p * (1. - a)
            if legal is not None:
                legal.append((prefix, new, lr))
        else:
            assert status == 'rejected' and new is path
            row[sig_a] = row.get(sig_a, 0.) + p
    assert path == snapshot, 'input path mutated'
    return row, flags


def oracle_row(toy, run, path, roster, max_steps):
    """Independent kernel: own eligibility (key bits), own walks, own reverse count, own flips."""
    keys = [s['key'] for s in path['segments']]
    common, varying = keys[0][1], 0
    for k in keys:
        common &= k[1]
        varying |= k[2] ^ keys[0][2]
    colour = {toy.universe[c]: (keys[0][2] >> c) & 1 for c in bits(common & ~varying)}
    lw_a = T.log_weight(toy, run, path)
    sig_a = path_sig(path)
    row = {}

    def add(sig, p):
        row[sig] = row.get(sig, 0.) + p

    def closed(start, seq, c, p, counts):
        loop = seq[c:]
        mask = sum(1 << toy.code[e] for e in loop)
        flipped = dict(colour)
        for e in loop:
            flipped[e] ^= 1
        v, need, rp, seen = start, 1, 1, {start}
        rev = seq[:c] + seq[c:][::-1]
        for i, e in enumerate(rev):
            cands = own_candidates(flipped, v, need, seen)
            assert e in cands
            rp *= len(cands)
            v = other(e, v)
            assert (v in seen) == (i == len(rev) - 1)
            seen.add(v)
            need ^= 1
        newkeys = [(k[0], k[1], k[2] ^ mask) + k[3:] for k in keys]
        events = []
        for i, ev in enumerate(path['events']):
            ch = toy._unique_mark(run, toy.channels(newkeys[i]), ev['kind'], ev['owner'], 'oracle')
            if ch is None or ch['target'] != newkeys[i + 1]:
                add(sig_a, p)
                return
            events.append({'kind': ev['kind'], 'owner': ev['owner'], 'W': ch['W']})
        new = {'segments': [toy._segment_core(run, k) for k in newkeys], 'events': events,
               'times': list(path['times'])}
        lr = math.log(prod(counts)) - math.log(rp) + T.log_weight(toy, run, new) - lw_a
        a = 1.0 if lr >= 0 else math.exp(lr)
        add(path_sig(new), p * a)
        add(sig_a, p * (1 - a))

    def rec(v, need, seq, pos, p, start, counts):
        cands = own_candidates(colour, v, need, pos)
        if not cands:
            add(sig_a, p)
            return
        for e in cands:
            w = other(e, v)
            s2, p2, c2 = seq + [e], p / len(cands), counts + [len(cands)]
            if w in pos:
                closed(start, s2, pos[w], p2, c2)
            elif len(s2) >= max_steps:
                add(sig_a, p2)
            else:
                pos2 = dict(pos)
                pos2[w] = len(s2)
                rec(w, need ^ 1, s2, pos2, p2, start, c2)
    for start in roster:
        rec(start, 1, [], {start: 0}, 1.0 / len(roster), start, [])
    return row


def toy_cases(full_q3_events=False):
    """(name, toy, roster, skeleton, times, list of x0 keys).

    full_q3_events: eventful Q3 cases start from ALL 4096 incidence words (filtered by skeleton
    validity) instead of the selected degree sectors."""
    cases = []
    A, B, edges, births = T.cube_q3()
    V = A + B
    toy = T.Toy(A=A, B=B, base_edges=edges, births=births)
    by_dv = {}
    for m in range(1 << len(edges)):
        inc = frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1)
        by_dv.setdefault(degree_vector(V, inc), []).append(inc)
    ones, twos = tuple([1] * 8), tuple([2] * 8)
    mixed = sorted((dv for dv in by_dv if 3 in dv and (0 in dv or 1 in dv) and len(by_dv[dv]) >= 2),
                   key=lambda dv: (-len(by_dv[dv]), dv))[:3]
    sector = by_dv[ones] + by_dv[twos] + [s for dv in mixed for s in by_dv[dv]]

    def key(inc, p=()):
        m = sum(1 << toy.code[e] for e in inc)
        return (0, toy.base_mask, m, sum(1 << toy.vid[v] for v in p), 0, 0, 0)
    cut = births[0]['cut']
    fl = ('flip', ('flip', ('edge', (2, 7))))
    hp = ('hop', ('hop', ('edge', (0, 6))))
    bi = ('birth', ('birth', 0, tuple(cut)))
    br = ('birth_rev', ('birth', 0, tuple(cut)))
    xs = [key(s) for s in sector]
    ev = [s for dv in sorted(by_dv) for s in by_dv[dv]] if full_q3_events else sector
    xe = [key(s) for s in ev]
    tag = '_all4096' if full_q3_events else ''
    cases.append(('Q3_no_events', toy, V, [], [], xs))
    cases.append(('Q3_flip_pair' + tag, toy, V, [fl, fl], [.3, .7], xe))
    cases.append(('Q3_hop_pair' + tag, toy, V, [hp, hp], [.35, .8], [key(s, (0,)) for s in ev]))
    cases.append(('Q3_birth_reverse' + tag, toy, V, [bi, br], [.25, .6], xe))
    cases.append(('Q3_birth_flip_flip_reverse' + tag, toy, V, [bi, fl, fl, br], [.2, .4, .55, .8], xe))
    A, B, edges, shift, per = T.honeycomb_torus(2, 3)
    V = A + B
    toyh = T.Toy(A=A, B=B, base_edges=edges)
    secs = subsets_with_degrees(edges, {v: 1 for v in V}) + subsets_with_degrees(edges, {v: 2 for v in V})

    def keyh(inc, p=()):
        return (0, toyh.base_mask, sum(1 << toyh.code[e] for e in inc), sum(1 << toyh.vid[v] for v in p), 0, 0, 0)
    e0 = sorted(edges)[0]
    cases.append(('honeycomb_2x3_no_events', toyh, V, [], [], [keyh(s) for s in secs]))
    cases.append(('honeycomb_2x3_flip_pair', toyh, V, [('flip', ('flip', ('edge', e0)))] * 2, [.4, .9],
                  [keyh(s) for s in secs]))
    cases.append(('honeycomb_2x3_hop_pair', toyh, V, [('hop', ('hop', ('edge', e0)))] * 2, [.15, .5],
                  [keyh(s, (e0[0],)) for s in secs]))
    return cases


def run_case(mod, name, toy, roster, skeleton, times, xs, with_oracle=True, with_reverse=False):
    run = T.make_run()
    run['context'] = toy.context
    paths = []
    for x in xs:
        p = T.build_path(toy, run, x, skeleton, times)
        if p is not None:
            paths.append(p)
    index = {path_sig(p): i for i, p in enumerate(paths)}
    lw = [T.log_weight(toy, run, p) for p in paths]
    rows, legal_all, counters = [], [], {}
    flags = {'invalid_output_path': 0, 'left_closed_set': 0, 'exceptions': 0, 'oracle_mismatch': 0,
             'db_violation': 0, 'row_sum_error': 0}
    max_db, max_oracle = 0., 0.
    exc_messages = set()
    for p in paths:
        legal = []
        row, f = module_row(mod, toy, run, p, roster, legal, counters)
        flags['invalid_output_path'] += f['invalid_output_path']
        flags['exceptions'] += len(f['exceptions'])
        exc_messages.update(f['exceptions'])
        for sig in row:
            if sig not in index:
                flags['left_closed_set'] += 1
        if abs(math.fsum(row.values()) - 1.) > 1e-12 and not f['exceptions']:
            flags['row_sum_error'] += 1
        rows.append(row)
        legal_all.append(legal)
        if with_oracle:
            orow = oracle_row(toy, run, p, roster, mod.MAX_WALK_STEPS if hasattr(mod, 'MAX_WALK_STEPS') else 1024)
            for sig in set(row) | set(orow):
                d = abs(row.get(sig, 0.) - orow.get(sig, 0.))
                max_oracle = max(max_oracle, d)
                if d > 1e-12:
                    flags['oracle_mismatch'] += 1
    m = max(lw) if lw else 0.
    pairs = moved = metropolis_partial = 0
    for i, row in enumerate(rows):
        for sig, t in row.items():
            j = index.get(sig)
            if j is None or j == i:
                continue
            pairs += 1
            tij = t
            tji = rows[j].get(path_sig(paths[i]), 0.)
            lhs, rhs = math.exp(lw[i] - m) * tij, math.exp(lw[j] - m) * tji
            d = abs(lhs - rhs) / max(lhs, rhs, 1e-300)
            max_db = max(max_db, d)
            if d > 1e-10:
                flags['db_violation'] += 1
            moved += 1
    lr_stats = {'negative': 0, 'zero': 0, 'positive': 0}
    for legal in legal_all:
        for _, _, lr in legal:
            lr_stats['negative' if lr < 0 else ('zero' if lr == 0 else 'positive')] += 1
    rev = None
    if with_reverse:
        rev = reverse_checks(mod, toy, run, paths, legal_all, roster)
    caught = any(flags[k] for k in flags)
    res = {'case': name, 'paths_in_closed_set': len(paths), 'events_per_path': len(skeleton),
           'offdiagonal_transitions': moved, 'max_relative_detailed_balance_error': max_db,
           'max_abs_oracle_kernel_difference': max_oracle, 'legal_proposal_log_mh_signs': lr_stats,
           'flags': flags, 'any_flag': caught,
           'move_counters_summed_over_enumeration': {k: v for k, v in sorted(counters.items())
                                                     if k.startswith('worm_loop_') and 'measurement' not in k}}
    if exc_messages:
        res['exception_messages'] = sorted(exc_messages)[:5]
    if rev is not None:
        res['forward_reverse'] = rev
    return res


def reverse_checks(mod, toy, run, paths, legal_all, roster):
    n, max_sum, all_exact = 0, 0., True
    for p, legal in zip(paths, legal_all):
        labels = [dict(toy.state_labels(context=toy.context, state=s['key'])) for s in p['segments']]
        colouring = mod.eligible_colouring(labels)
        for prefix, new, lr in legal:
            rng = ScriptRNG(prefix)
            w = mod.grow_walk(colouring, roster, lambda k: rng.integers(0, k), mod.MAX_WALK_STEPS)
            nl = [dict(toy.state_labels(context=toy.context, state=s['key'])) for s in new['segments']]
            col_rev = mod.eligible_colouring(nl)
            rev = mod.reverse_edges(w['edges'], w['closure'])
            pre = reverse_prefix(roster, col_rev, w['start'], rev)
            diag = {'sweeps_completed': 0}
            back, status = mod.move(run, new, ScriptRNG(pre), diag, toy, roster, toy.state_labels)
            assert status == 'changed', 'reverse proposal not legal'
            assert path_sig(back) == path_sig(p), 'reverse move does not restore the path'
            lr2 = diag['worm_loop_last_proposal']['log_mh_ratio']
            s = lr + lr2
            all_exact = all_exact and s == 0.0
            max_sum = max(max_sum, abs(s))
            n += 1
    return {'legal_proposals_reversed': n, 'max_abs_forward_plus_reverse_log_mh': max_sum,
            'all_exactly_zero': all_exact}


def section_f2(mod):
    out = []
    for name, toy, roster, sk, times, xs in toy_cases(full_q3_events=True):
        r = run_case(mod, name, toy, roster, sk, times, xs, with_oracle=True, with_reverse=True)
        assert not r['any_flag'], (name, r['flags'])
        assert r['max_relative_detailed_balance_error'] < 1e-10
        assert r['forward_reverse']['all_exactly_zero']
        out.append(r)
    return out


# ======================== F5 guards / F4 replay / F6 interruption =============================
def expect_stop(fn, status=None):
    try:
        fn()
    except T.ToyStop as exc:
        if status is not None and exc.status != status:
            raise AssertionError(('wrong stop status', exc.status, exc.message))
        return exc
    raise AssertionError('expected a stop')


def q3_toy(**kw):
    A, B, edges, births = T.cube_q3()
    toy = T.Toy(A=A, B=B, base_edges=edges, births=births, **kw)
    run = T.make_run()
    run['context'] = toy.context
    return toy, run, A + B, edges, births


def q3_key(toy, inc, p=()):
    return (0, toy.base_mask, sum(1 << toy.code[e] for e in inc), sum(1 << toy.vid[v] for v in p), 0, 0, 0)


def find_legal_prefix(mod, toy, run, path, roster, want_events=True):
    stack = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        try:
            new, status = mod.move(run, path, rng, {'sweeps_completed': 0}, toy, roster, toy.state_labels)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        if status == 'changed':
            return prefix, new
    return None, None


def section_guards(mod):
    res = {}
    toy, run, V, edges, births = q3_toy()
    sec2 = subsets_with_degrees(edges, {v: 2 for v in V})
    inc = sorted(sec2, key=sorted)[0]
    cut = births[0]['cut']
    bi = ('birth', ('birth', 0, tuple(cut)))
    br = ('birth_rev', ('birth', 0, tuple(cut)))
    fl = ('flip', ('flip', ('edge', (2, 7))))
    # an eventful Birth/flip/flip/reverse path with an accepted worm move that changes an event W
    eventful = None
    for m in range(1 << len(edges)):
        s = frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1)
        p = T.build_path(toy, run, q3_key(toy, s), [bi, fl, fl, br], [.2, .4, .55, .8])
        if p is None:
            continue
        prefix, new = find_legal_prefix(mod, toy, run, p, V)
        if prefix is not None and any(a['W'] != b['W'] for a, b in zip(p['events'], new['events'])):
            eventful = p
            break
    assert eventful is not None
    simple = T.build_path(toy, run, q3_key(toy, inc), [], [])
    d = lambda: {'sweeps_completed': 0}

    # g1 malformed
    bad = copy.deepcopy(eventful)
    bad['times'] = bad['times'][:-1]
    expect_stop(lambda: mod.move(run, bad, ScriptRNG([0] * 50), d(), toy, V, toy.state_labels), 'failed')
    res['malformed_path_fails'] = True
    # g2 event cap
    run2 = dict(run)
    run2['caps'] = {'max_events_per_path': 3}
    expect_stop(lambda: mod.move(run2, eventful, ScriptRNG([0] * 50), d(), toy, V, toy.state_labels), 'incomplete')
    res['event_cap_terminal'] = True
    # g3 not closed
    bad = copy.deepcopy(simple)
    bad['segments'] = [simple['segments'][0], toy._segment_core(run, q3_key(toy, sorted(sec2, key=sorted)[1]))]
    bad['events'] = [dict(kind='flip', owner=('flip', ('edge', (2, 7))), W=1.)]
    bad['times'] = [.5]
    expect_stop(lambda: mod.move(run, bad, ScriptRNG([0] * 50), d(), toy, V, toy.state_labels), 'failed')
    res['unclosed_path_fails'] = True
    # g4 bad roster
    for roster in (list(V), V + (V[0],), ()):
        expect_stop(lambda: mod.move(run, simple, ScriptRNG([0] * 50), d(), toy, roster, toy.state_labels), 'failed')
    res['bad_roster_fails'] = True
    # g5 empty start: vertex with no occupied eligible edge, no resampling
    s0 = frozenset([(1, 6), (1, 7)])  # vertex 0 unoccupied everywhere
    p0 = T.build_path(toy, run, q3_key(toy, s0), [], [])
    rng = ScriptRNG([V.index(0)])
    dd = d()
    out, status = mod.move(run, p0, rng, dd, toy, V, toy.state_labels)
    assert status == 'rejected' and out is p0 and dd['worm_loop_empty_start'] == 1 and rng.ns == [8]
    res['empty_start_self_loop_one_draw'] = True
    # g6 dead end (rule-agnostic): find a scripted walk that dead-ends; one draw per choice, no resampling
    found = None
    for m in range(1 << len(edges)):
        sd = frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1)
        col = {e: (1 if e in sd else 0) for e in edges}
        for p_, w_ in [(x[2], x[1]) for x in walk_dfs_prefixed(mod, col, V)]:
            if w_['status'] == 'dead_end':
                found = (sd, p_)
                break
        if found:
            break
    assert found is not None
    p1 = T.build_path(toy, run, q3_key(toy, found[0]), [], [])
    rng = ScriptRNG(found[1])
    dd = d()
    out, status = mod.move(run, p1, rng, dd, toy, V, toy.state_labels)
    assert status == 'rejected' and out is p1 and dd['worm_loop_dead_end'] == 1 and len(rng.ns) == len(found[1])
    res['dead_end_self_loop_no_resampling'] = True
    # g7 length cap (module copy with cap 3)
    capped = load_source(MODULE.read_text().replace('MAX_WALK_STEPS = 1024', 'MAX_WALK_STEPS = 3', 1), 'worm_capped')
    stack, seen = [[]], set()
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        dd = d()
        try:
            out, status = capped.move(run, simple, rng, dd, toy, V, toy.state_labels)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        seen.update(k for k in dd if k.endswith('length_cap'))
        assert status == 'rejected'  # an 8-cycle 2-factor has no closure within 3 steps
    assert 'worm_loop_length_cap' in seen
    res['length_cap_self_loop'] = True
    # g8 stored W mismatch
    bad = copy.deepcopy(eventful)
    bad['events'][1]['W'] *= 1.0000001
    prefix, _ = find_legal_prefix(mod, toy, run, eventful, V)
    expect_stop(lambda: mod.move(run, bad, ScriptRNG(prefix), d(), toy, V, toy.state_labels), 'failed')
    res['stored_rate_mismatch_fails'] = True
    # g9 transformed replay guard: hop on an occupied eligible loop edge
    hp = ('hop', ('hop', ('edge', (0, 6))))
    found = False
    for s in sorted(sec2, key=sorted):
        if (0, 6) not in s:
            continue
        ph = T.build_path(toy, run, q3_key(toy, s, (0,)), [hp, hp], [.35, .8])
        if ph is None:
            continue
        stack = [[]]
        while stack and not found:
            prefix = stack.pop()
            rng = ScriptRNG(prefix)
            dd = d()
            try:
                out, status = mod.move(run, ph, rng, dd, toy, V, toy.state_labels)
            except NeedChoice as nc:
                stack.extend(prefix + [j] for j in range(nc.n))
                continue
            if dd.get('worm_loop_event_replay_guard_or_target'):
                assert status == 'rejected' and out is ph
                found = True
        if found:
            break
    assert found
    res['transformed_event_guard_self_loop'] = True
    # g10 missing native flip witness
    toyz, runz, V, edges, births = q3_toy(zero_h=[(0, 5)])
    s = [x for x in sorted(sec2, key=sorted) if (0, 5) in x][0]
    pz = T.build_path(toyz, runz, q3_key(toyz, s), [], [])
    caught = False
    stack = [[]]
    while stack:
        prefix = stack.pop()
        try:
            mod.move(runz, pz, ScriptRNG(prefix), d(), toyz, V, toyz.state_labels)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
        except T.ToyStop as exc:
            assert exc.status == 'failed' and 'native positive-rate flip' in exc.message
            caught = True
            break
    assert caught
    res['missing_native_flip_witness_fails'] = True
    # g11 key contract (resource component changed by canonicalisation)
    toyw, runw, V, edges, births = q3_toy(wrong_key=True)
    pw = {'segments': [dict(s) for s in simple['segments']], 'events': [], 'times': []}
    caught = False
    stack = [[]]
    while stack:
        prefix = stack.pop()
        try:
            mod.move(runw, pw, ScriptRNG(prefix), d(), toyw, V, toyw.state_labels)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
        except T.ToyStop as exc:
            assert exc.status == 'failed' and 'key contract' in exc.message
            caught = True
            break
    assert caught
    res['whole_path_key_contract_fails'] = True
    # g12 budget propagation from the first checkpoint
    toy.trigger, toy.checkpoints = 1, 0
    exc = expect_stop(lambda: mod.move(run, simple, ScriptRNG([0] * 50), d(), toy, V, toy.state_labels), 'incomplete')
    assert isinstance(exc, T.ToyBudgetStop)
    toy.trigger = None
    res['budget_stop_propagates'] = True
    # F4 replay: accepted eventful move carries the transformed native W
    prefix, new = find_legal_prefix(mod, toy, run, eventful, V)
    assert T.validate_path(toy, run, new)
    changed_w = sum(1 for a, b in zip(eventful['events'], new['events']) if a['W'] != b['W'])
    res['F4_replayed_events_valid_with_transformed_W'] = {'events': len(new['events']),
                                                          'events_with_changed_W': changed_w}
    # F6 interruption atomicity at every checkpoint of an accepted eventful proposal
    toy.trigger, toy.checkpoints, toy.checkpoint_log = None, 0, []
    dd0 = d()
    full, status = mod.move(run, eventful, ScriptRNG(prefix), dd0, toy, V, toy.state_labels)
    assert status == 'changed'
    n_checks = toy.checkpoints
    log = list(toy.checkpoint_log)
    assert log[-1] == 'before worm-loop atomic commit'
    snapshot = copy.deepcopy(eventful)
    for t in range(1, n_checks + 1):
        toy.trigger, toy.checkpoints = t, 0
        dd = d()
        exc = expect_stop(lambda: mod.move(run, eventful, ScriptRNG(prefix), dd, toy, V, toy.state_labels), 'incomplete')
        assert isinstance(exc, T.ToyBudgetStop)
        assert eventful == snapshot
        assert not any('read_integral' in k or 'accepted' in k for k in dd)
    toy.trigger = None
    res['F6_interruption'] = {'checkpoints_in_accepted_eventful_move': n_checks,
                              'every_checkpoint_interrupted': True, 'input_path_unchanged': True,
                              'no_read_integral_or_accepted_counter_written': True,
                              'last_checkpoint': log[-1], 'checkpoint_kinds': sorted(set(log))}
    return res


# ======================== F7 mutants =========================================================
REV_CALL = ("    reverse_product = walk_branch_product(reverse_colouring, owner_roster, start,\n"
            "                                          reverse_edges(edges, closure), MAX_WALK_STEPS)\n")
MUTANTS = {
    'M1_wrong_reverse_probability_same_orientation': [
        (REV_CALL, "    reverse_product = _mutant_same_orientation(reverse_colouring, start, edges)\n"),
        ("def move(", "def _mutant_same_orientation(colouring, start, edges):\n"
                      "    inc = incidence_lists(colouring)\n    v, p = start, 1\n"
                      "    for e in edges:\n        p *= len(inc[v][colouring[e]])\n        v = _other(e, v)\n"
                      "    return p\n\n\ndef move(")],
    'M2_missing_start_branching_factor_forward': [
        ("    forward_product = walk['branch_product']\n",
         "    forward_product = walk['branch_product'] // walk['counts'][0]\n"),
        ("MAX_WALK_STEPS) != forward_product:", "MAX_WALK_STEPS) != forward_product * walk['counts'][0]:")],
    'M3_one_dwell_only_flip': [
        ("        new_occupied = occupied ^ loopset\n",
         "        new_occupied = occupied ^ loopset if (old is segs[0] or old is segs[-1]) else occupied\n"),
        ("                (old['key'][2] ^ new_key[2]) != mask):", "                False):"),
        ("        fail('Eligible coloured graph is not invariant up to the loop flip')", "        pass")],
    'M3b_one_dwell_only_flip_guards_removed': [
        ("        new_occupied = occupied ^ loopset\n",
         "        new_occupied = occupied ^ loopset if (old is segs[0] or old is segs[-1]) else occupied\n"),
        ("                (old['key'][2] ^ new_key[2]) != mask):", "                False):"),
        ("        fail('Eligible coloured graph is not invariant up to the loop flip')", "        pass"),
        ("    if reverse_product is None:\n        return reject('reverse_walk_impossible')",
         "    if reverse_product is None:\n        reverse_product = forward_product"),
        ("        if after is None or not sampler._keys_equal(run, sampler._target_key(run, after), transformed[i+1]['key']):",
         "        if after is None:")],
    'CONTROL_symmetric_omission_of_start_factor': [
        ("    forward_product = walk['branch_product']\n",
         "    forward_product = walk['branch_product'] // walk['counts'][0]\n"),
        ("MAX_WALK_STEPS) != forward_product:", "MAX_WALK_STEPS) != forward_product * walk['counts'][0]:"),
        ("    walk_term = math.log(forward_product) - math.log(reverse_product)\n",
         "    reverse_product //= len(_step_candidates(incidence_lists(reverse_colouring), start, 1, {start: 0}, LOOKAHEAD))\n"
         "    walk_term = math.log(forward_product) - math.log(reverse_product)\n")],
}


def mutant_source(src, edits):
    for old, new in edits:
        assert src.count(old) == 1, ('mutation anchor not unique', old[:60])
        src = src.replace(old, new)
    return src


def section_f7(src):
    out = {}
    names = ('Q3_no_events', 'Q3_flip_pair', 'Q3_birth_reverse', 'Q3_birth_flip_flip_reverse',
             'honeycomb_2x3_no_events', 'honeycomb_2x3_flip_pair')
    cases = [c for c in toy_cases() if c[0] in names]
    for mname, edits in MUTANTS.items():
        msrc = mutant_source(src, edits)
        mod = load_source(msrc, mname)
        per = []
        for name, toy, roster, sk, times, xs in cases:
            r = run_case(mod, name, toy, roster, sk, times, xs, with_oracle=True)
            per.append({'case': name, 'flags': r['flags'],
                        'max_relative_detailed_balance_error': r['max_relative_detailed_balance_error'],
                        'max_abs_oracle_kernel_difference': r['max_abs_oracle_kernel_difference']})
        caught = any(any(v for v in p['flags'].values()) for p in per)
        out[mname] = {'mutated_source_sha256': hashlib.sha256(msrc.encode()).hexdigest(),
                      'caught': caught, 'cases': per,
                      'detected_by': sorted({k for p in per for k, v in p['flags'].items() if v})}
    for k, v in out.items():
        if k.startswith('CONTROL'):
            assert not v['caught'], ('control mutant should pass', v)
        else:
            assert v['caught'], ('mutant not caught', k)
    return out


def section_literal_variant(src):
    """Same F1 (Q3 all states, honeycomb 3x3 dimers) and F2 cases with LOOKAHEAD = False."""
    vsrc = src.replace('LOOKAHEAD = True  #', 'LOOKAHEAD = False  #', 1)
    assert vsrc != src
    mod = load_source(vsrc, 'worm_literal_rule')
    LOOK['value'] = False
    try:
        out = {'variant_source_sha256': hashlib.sha256(vsrc.encode()).hexdigest(), 'F1': [], 'F2': []}
        A, B, edges, _ = T.cube_q3()
        allstates = [frozenset(e for i, e in enumerate(sorted(edges)) if (m >> i) & 1) for m in range(1 << len(edges))]
        out['F1'].append(f1_graph(mod, 'Q3_cube_all_4096', A + B, sorted(edges), allstates, A + B))
        A, B, edges, shift, per = T.honeycomb_torus(3, 3)
        V = A + B
        out['F1'].append(f1_graph(mod, 'honeycomb_3x3_torus_dimer_sector', V, sorted(edges),
                                  subsets_with_degrees(edges, {v: 1 for v in V}), V, shift, per))
        for name, toy, roster, sk, times, xs in toy_cases():
            r = run_case(mod, name, toy, roster, sk, times, xs, with_oracle=True, with_reverse=True)
            assert not r['any_flag'] and r['forward_reverse']['all_exactly_zero'], (name, r['flags'])
            out['F2'].append({k: r[k] for k in ('case', 'paths_in_closed_set', 'offdiagonal_transitions',
                              'max_relative_detailed_balance_error', 'max_abs_oracle_kernel_difference',
                              'flags', 'forward_reverse')})
    finally:
        LOOK['value'] = True
    return out


def main():
    global T
    expected, out_path = sys.argv[1], Path(sys.argv[2])
    src_bytes = MODULE.read_bytes()
    actual = hashlib.sha256(src_bytes).hexdigest()
    assert actual == expected, 'module bytes differ from the declared pin'
    T = load_file(TOY, 'worm_fixture_toy')
    mod = load_file(MODULE, 'worm_module_under_test')
    assert mod.LOOKAHEAD is True
    LOOK['value'] = True
    t0 = time.time()
    result = {'scope': 'Synthetic explicit states and exact enumeration only; no native operator, sampler or '
                       'production state; toy target deliberately not loop-invariant.',
              'module': {'path': str(MODULE), 'sha256': actual},
              'toy_library': {'path': str(TOY), 'sha256': hashlib.sha256(TOY.read_bytes()).hexdigest()},
              'fixture': {'path': str(Path(__file__).resolve()),
                          'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    result['F1_pure_walk_proposal_symmetry'] = section_f1(mod)
    result['F2_F3_end_to_end_exact_kernel'] = section_f2(mod)
    result['F4_F5_F6_guards_replay_interruption'] = section_guards(mod)
    result['F7_mutants'] = section_f7(src_bytes.decode())
    result['F8_literal_rule_variant_LOOKAHEAD_False'] = section_literal_variant(src_bytes.decode())
    result['all_assertions_passed'] = True
    result['seconds'] = round(time.time() - t0, 1)
    with out_path.open('x') as f:
        json.dump(result, f, indent=1, sort_keys=False)
        f.write('\n')
    print(json.dumps({'ok': True, 'seconds': result['seconds'], 'out': str(out_path)}))


if __name__ == '__main__':
    main()
