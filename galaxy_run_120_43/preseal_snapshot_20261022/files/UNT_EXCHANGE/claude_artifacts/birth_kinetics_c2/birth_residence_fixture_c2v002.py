"""Exact-enumeration fixtures for owned_worldline_birth_residence_transport_c2v002.py.

Synthetic explicit states only (birth_fixture_toy_c2v002.py); never imports the native operator or
sampler; never samples.  Usage:
  python3 -I -B birth_residence_fixture_c2v002.py <module_sha256> <output_json>
The output file is created exclusively ('x').  Sections:
  F1 end-to-end exact kernel of move() by exhaustive scripted-RNG enumeration on closed path sets
     (all valid reference states x0 for each event skeleton): detailed balance
     pi(a)T(a,b) = pi(b)T(b,a), rows sum to one, every output path independently valid, input never
     mutated, T equal to an independently coded oracle kernel.  The toy has owners without any Birth
     mark (owner 3 always; others by state) and the channel-bearing count changes across moves;
     both are counted.
  F2 forward + reverse log MH = 0 exactly and the reverse move restores the original path.
  F3 guards / self loops / contract failures, F4 event replay carries the transformed W,
  F5 interruption atomicity at every budget checkpoint of an accepted eventful proposal.
  F6 mutants (missing owner-count correction; counting all roster owners; counting owners with any
     mark; V001 all-owner selection with the c2v002 correction) must be caught; controls (the
     reviewed V001 transport itself, which is exact for its own proposal, and a per-owner
     enumeration variant of c2v002 with the identical kernel) must pass.
  F7 exact self-loop probability for lack of an owner, V001 against c2v002, on the toy states.
"""
import copy
import hashlib
import importlib.util
import json
import math
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE / 'owned_worldline_birth_residence_transport_c2v002.py'
TOY = HERE / 'birth_fixture_toy_c2v002.py'
V001 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
            'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py')
V001_SHA = '6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8'
BIRTH_KINDS = ('birth', 'birth_rev')
T = None


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


def new_diag():
    return {'sweeps_completed': 0}


# ---------------- independent toy-side quantities (never the module) ------------------------
def own_marks(toy, key):
    return [c for c in toy.channels(key) if c['kind'] in BIRTH_KINDS]


def own_bearing(toy, key, roster):
    marks = own_marks(toy, key)
    return [o for o in roster if any(c['owner'][1] == o for c in marks)]


def own_roster(toy, key, o):
    return [c for c in own_marks(toy, key) if c['owner'][1] == o]


def own_mark(toy, key, kind, owner):
    hits = [c for c in toy.channels(key) if c['kind'] == kind and c['owner'] == owner]
    assert len(hits) <= 1
    return hits[0] if hits else None


def oracle_row(toy, run, path, roster, selection='bearing'):
    """Independent kernel of the c2v002 proposal (selection='bearing') from the toy definitions."""
    keys = [s['key'] for s in path['segments']]
    sig_a = T.path_signature(path)
    lw_a = T.log_weight(toy, run, path)
    row = {}

    def add(sig, p):
        row[sig] = row.get(sig, 0.) + p
    S = own_bearing(toy, keys[0], roster)
    if not S:
        add(sig_a, 1.)
        return row
    for o in S:
        R = own_roster(toy, keys[0], o)
        for c in R:
            p = 1. / (len(S) * len(R))
            inv = 'birth_rev' if c['kind'] == 'birth' else 'birth'
            newkeys, ok = [], True
            for kx in keys:
                m = own_mark(toy, kx, c['kind'], c['owner'])
                if m is None:
                    ok = False
                    break
                b = own_mark(toy, m['target'], inv, c['owner'])
                if b is None or b['target'] != kx:
                    ok = False
                    break
                newkeys.append(m['target'])
            events = []
            if ok:
                for i, ev in enumerate(path['events']):
                    m = own_mark(toy, newkeys[i], ev['kind'], ev['owner'])
                    if m is None or m['target'] != newkeys[i + 1]:
                        ok = False
                        break
                    events.append({'kind': ev['kind'], 'owner': ev['owner'], 'W': m['W']})
            if not ok:
                add(sig_a, p)
                continue
            new = {'segments': [{'key': k} for k in newkeys], 'events': events, 'times': list(path['times'])}
            Sy = own_bearing(toy, newkeys[0], roster)
            Ry = own_roster(toy, newkeys[0], o)
            lr = (math.log(len(S) * len(R)) - math.log(len(Sy) * len(Ry)) +
                  T.log_weight(toy, run, new) - lw_a)
            a = 1.0 if lr >= 0 else math.exp(lr)
            add(T.path_signature(new), p * a)
            add(sig_a, p * (1 - a))
    return row


def module_row(mod, toy, run, path, roster, legal=None, counters=None):
    row, flags = {}, {'invalid_output_path': 0, 'exceptions': []}
    sig_a = T.path_signature(path)
    snapshot = copy.deepcopy(path)
    stack = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix)
        diag = new_diag()
        try:
            new, status = mod.move(run, path, rng, diag, toy, roster)
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
            lp = diag['birth_residence_last_proposal']
            lr = lp['log_mh_ratio']
            assert rng.random_calls == (1 if lr < 0 else 0)
            a = 1.0 if lr >= 0 else math.exp(lr)
            if not T.validate_path(toy, run, new):
                flags['invalid_output_path'] += 1
            sig_b = T.path_signature(new)
            row[sig_b] = row.get(sig_b, 0.) + p * a
            row[sig_a] = row.get(sig_a, 0.) + p * (1. - a)
            if legal is not None:
                legal.append((prefix, new, lr, lp))
        else:
            assert status == 'rejected' and new is path
            row[sig_a] = row.get(sig_a, 0.) + p
    assert path == snapshot, 'input path mutated'
    return row, flags


SKELETONS = {
    'no_events': ([], []),
    'flip_e0_pair': ([('flip', ('flip', ('edge', (0, 1))))] * 2, [.3, .7]),
    'flip_e1_pair': ([('flip', ('flip', ('edge', (2, 4))))] * 2, [.25, .6]),
    'birth_owner2_reverse': ([('birth', ('birth', 2, 0)), ('birth_rev', ('birth', 2, 0))], [.2, .55]),
    'birth_owner1_flip_e0_flip_e0_reverse': ([('birth', ('birth', 1, 0)), ('flip', ('flip', ('edge', (0, 1)))),
                                              ('flip', ('flip', ('edge', (0, 1)))), ('birth_rev', ('birth', 1, 0))],
                                             [.15, .35, .6, .85]),
    'reverse_owner0_site1_then_birth': ([('birth_rev', ('birth', 0, 1)), ('birth', ('birth', 0, 1))], [.4, .9]),
}


def run_case(mod, name, roster=None, with_oracle=True, with_reverse=False, toy_kw=None):
    toy = T.Toy(**(toy_kw or {}))
    run = T.make_run()
    roster = T.OWNERS if roster is None else roster
    skeleton, times = SKELETONS[name]
    paths = [p for p in (T.build_path(toy, run, x, skeleton, times) for x in toy.all_keys()) if p is not None]
    index = {T.path_signature(p): i for i, p in enumerate(paths)}
    lw = [T.log_weight(toy, run, p) for p in paths]
    rows, legal_all, counters = [], [], {}
    flags = {'invalid_output_path': 0, 'left_closed_set': 0, 'exceptions': 0, 'oracle_mismatch': 0,
             'db_violation': 0, 'row_sum_error': 0}
    max_db = max_oracle = 0.
    exc_messages = set()
    owners_without = owners_with = 0
    for p in paths:
        legal = []
        row, f = module_row(mod, toy, run, p, roster, legal, counters)
        flags['invalid_output_path'] += f['invalid_output_path']
        flags['exceptions'] += len(f['exceptions'])
        exc_messages.update(f['exceptions'])
        flags['left_closed_set'] += sum(1 for sig in row if sig not in index)
        if abs(math.fsum(row.values()) - 1.) > 1e-12 and not f['exceptions']:
            flags['row_sum_error'] += 1
        rows.append(row)
        legal_all.append(legal)
        nb = len(own_bearing(toy, p['segments'][0]['key'], roster))
        owners_with += nb
        owners_without += len(roster) - nb
        if with_oracle:
            orow = oracle_row(toy, run, p, roster)
            for sig in set(row) | set(orow):
                d = abs(row.get(sig, 0.) - orow.get(sig, 0.))
                max_oracle = max(max_oracle, d)
                if d > 1e-12:
                    flags['oracle_mismatch'] += 1
    m = max(lw)
    moved = 0
    for i, row in enumerate(rows):
        for sig, t in row.items():
            j = index.get(sig)
            if j is None or j == i:
                continue
            tji = rows[j].get(T.path_signature(paths[i]), 0.)
            lhs, rhs = math.exp(lw[i] - m) * t, math.exp(lw[j] - m) * tji
            d = abs(lhs - rhs) / max(lhs, rhs, 1e-300)
            max_db = max(max_db, d)
            if d > 1e-10:
                flags['db_violation'] += 1
            moved += 1
    nonunit = sum(1 for legal in legal_all for _, _, _, lp in legal
                  if lp.get('forward_owner_count', 0) != lp.get('reverse_owner_count', 0))
    signs = {'negative': 0, 'zero': 0, 'positive': 0}
    for legal in legal_all:
        for _, _, lr, _ in legal:
            signs['negative' if lr < 0 else ('zero' if lr == 0 else 'positive')] += 1
    res = {'case': name, 'roster': list(roster), 'paths_in_closed_set': len(paths), 'events_per_path': len(skeleton),
           'offdiagonal_transitions': moved, 'max_relative_detailed_balance_error': max_db,
           'max_abs_oracle_kernel_difference': max_oracle if with_oracle else None,
           'legal_proposals': sum(len(x) for x in legal_all),
           'legal_proposals_with_changed_channel_bearing_count': nonunit,
           'legal_proposal_log_mh_signs': signs,
           'reference_owner_slots_without_birth_mark': owners_without,
           'reference_owner_slots_with_birth_mark': owners_with,
           'reference_states_without_any_channel_bearing_owner': sum(
               1 for p in paths if not own_bearing(toy, p['segments'][0]['key'], roster)),
           'flags': flags, 'any_flag': any(flags.values()),
           'move_counters_summed_over_enumeration': {k: v for k, v in sorted(counters.items())
                                                     if k.startswith('birth_residence_') and 'measurement' not in k}}
    if exc_messages:
        res['exception_messages'] = sorted(exc_messages)[:5]
    if with_reverse:
        res['forward_reverse'] = reverse_checks(mod, toy, run, paths, legal_all, roster)
    return res


def reverse_prefix(toy, run, key, roster, owner, kind):
    """Independent scripted choices making the module propose (kind, owner) at `key`.

    Index of the owner in the channel-bearing roster-order list and of the mark in the union
    palette order of the toy (the module's documented ordering)."""
    S = own_bearing(toy, key, roster)
    union = frozenset(run['group'][o] for o in roster)
    cs, _ = toy._palette_channels(run, key, union)
    R = [c for c in cs if c['kind'] in BIRTH_KINDS and c['owner'][0] == 'birth' and c['owner'][1] == owner[1]]
    return [S.index(owner[1]), [i for i, c in enumerate(R) if c['kind'] == kind and c['owner'] == owner][0]]


def reverse_checks(mod, toy, run, paths, legal_all, roster):
    n, max_sum, all_exact = 0, 0., True
    for p, legal in zip(paths, legal_all):
        for prefix, new, lr, lp in legal:
            inv = 'birth_rev' if lp['kind'] == 'birth' else 'birth'
            # owner_id of the chosen mark, recovered independently from the scripted choices
            S = own_bearing(toy, p['segments'][0]['key'], roster)
            o = S[prefix[0]]
            union = frozenset(run['group'][x] for x in roster)
            cs, _ = toy._palette_channels(run, p['segments'][0]['key'], union)
            R = [c for c in cs if c['kind'] in BIRTH_KINDS and c['owner'][0] == 'birth' and c['owner'][1] == o]
            owner = R[prefix[1]]['owner']
            assert R[prefix[1]]['kind'] == lp['kind'] and o == lp['original_owner']
            pre = reverse_prefix(toy, run, new['segments'][0]['key'], roster, owner, inv)
            diag = new_diag()
            back, status = mod.move(run, new, ScriptRNG(pre), diag, toy, roster)
            assert status == 'changed', 'reverse proposal not legal'
            assert T.path_signature(back) == T.path_signature(p), 'reverse move does not restore the path'
            lr2 = diag['birth_residence_last_proposal']['log_mh_ratio']
            s = lr + lr2
            all_exact = all_exact and s == 0.0
            max_sum = max(max_sum, abs(s))
            n += 1
    return {'legal_proposals_reversed': n, 'max_abs_forward_plus_reverse_log_mh': max_sum,
            'all_exactly_zero': all_exact}


def section_f1_f2(mod):
    out = []
    for name in SKELETONS:
        r = run_case(mod, name, with_oracle=True, with_reverse=True)
        assert not r['any_flag'], (name, r['flags'], r.get('exception_messages'))
        assert r['max_relative_detailed_balance_error'] < 1e-10
        assert r['forward_reverse']['all_exactly_zero']
        out.append(r)
    # restricted fixed roster (3, 4): owner 3 never bears a mark, owner 4 only with incidence bit 0
    # and an open gate, so reference states with an EMPTY channel-bearing set occur (self loops)
    for name in ('no_events', 'flip_e0_pair', 'birth_owner2_reverse'):
        r = run_case(mod, name, roster=(3, 4), with_oracle=True, with_reverse=True)
        assert not r['any_flag'], (name, r['flags'], r.get('exception_messages'))
        assert r['max_relative_detailed_balance_error'] < 1e-10
        assert r['forward_reverse']['all_exactly_zero']
        out.append(r)
    assert sum(r['legal_proposals_with_changed_channel_bearing_count'] for r in out) > 0
    assert all(r['reference_owner_slots_without_birth_mark'] > 0 for r in out)
    assert sum(r['reference_states_without_any_channel_bearing_owner'] for r in out) > 0
    return out


# ---------------- F3 guards, F4 replay, F5 interruption ----------------------------------------
def expect_stop(fn, status=None, contains=None):
    try:
        fn()
    except T.ToyStop as exc:
        if status is not None and exc.status != status:
            raise AssertionError(('wrong stop status', exc.status, exc.message))
        if contains is not None and contains not in exc.message:
            raise AssertionError(('wrong stop message', exc.message))
        return exc
    raise AssertionError('expected a stop')


def enumerate_until(mod, toy, run, path, roster, pred, uniform=0.0):
    """Exhaustive scripted enumeration; returns (prefix, diag, outcome) of the first hit of pred."""
    stack = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptRNG(prefix, uniform)
        diag = new_diag()
        try:
            out = mod.move(run, path, rng, diag, toy, roster)
        except NeedChoice as nc:
            stack.extend(prefix + [j] for j in range(nc.n))
            continue
        except T.ToyStop as exc:
            out = exc
        if pred(out, diag):
            return prefix, diag, out
    return None


def paths_of(toy, run, name):
    sk, times = SKELETONS[name]
    return [p for p in (T.build_path(toy, run, x, sk, times) for x in toy.all_keys()) if p is not None]


def section_guards(mod):
    res = {}
    toy = T.Toy()
    run = T.make_run()
    R = T.OWNERS
    simple = paths_of(toy, run, 'no_events')
    eventful = paths_of(toy, run, 'birth_owner1_flip_e0_flip_e0_reverse')
    # g1 malformed / g2 event cap / g3 unclosed
    bad = copy.deepcopy(eventful[0])
    bad['times'] = bad['times'][:-1]
    expect_stop(lambda: mod.move(run, bad, ScriptRNG([0] * 9), new_diag(), toy, R), 'failed', 'Malformed')
    run2 = dict(run)
    run2['caps'] = {'max_events_per_path': 3}
    expect_stop(lambda: mod.move(run2, eventful[0], ScriptRNG([0] * 9), new_diag(), toy, R), 'incomplete')
    bad = copy.deepcopy(simple[0])
    other = toy._segment_core(run, simple[1]['segments'][0]['key'])
    bad['segments'] = [simple[0]['segments'][0], other]
    bad['events'] = [{'kind': 'flip', 'owner': ('flip', ('edge', (0, 1))), 'W': 1.}]
    bad['times'] = [.5]
    expect_stop(lambda: mod.move(run, bad, ScriptRNG([0] * 9), new_diag(), toy, R), 'failed', 'not closed')
    res['malformed_event_cap_unclosed'] = True
    # g4 bad rosters (list, duplicate, empty, unknown label)
    for roster in (list(R), R + (R[0],), (), R + (7,)):
        expect_stop(lambda: mod.move(run, simple[0], ScriptRNG([0] * 9), new_diag(), toy, roster), 'failed')
    res['bad_roster_fails'] = True
    # g5 no channel-bearing owner: self loop with ZERO draws
    empty = [p for p in simple if not own_bearing(toy, p['segments'][0]['key'], (3, 4))]
    full = [p for p in simple if own_bearing(toy, p['segments'][0]['key'], R)]
    assert empty
    for pe in empty:
        rng, dd = ScriptRNG([]), new_diag()
        out, st = mod.move(run, pe, rng, dd, toy, (3, 4))
        assert st == 'rejected' and out is pe and rng.ns == [] and dd['birth_residence_no_channel_bearing_owner'] == 1
    # owners without marks are never drawn: every scripted first draw has n = |S(x)| < |roster|
    for p in full:
        S = own_bearing(toy, p['segments'][0]['key'], R)
        rng = ScriptRNG([0, 0])
        try:
            mod.move(run, p, rng, new_diag(), toy, R)
        except NeedChoice:
            pass
        assert rng.ns[0] == len(S) and 3 not in S
    res['no_channel_bearing_owner_self_loop_zero_draws'] = {'roster_3_4_states_with_empty_S': len(empty),
                                                           'first_draw_over_bearing_owners_only': len(full)}
    # g6 dwell guard, inverse guard, event replay guard reached on the fixture toy (self loops)
    reached = {}
    for name in SKELETONS:
        for p in paths_of(toy, run, name):
            for reason in ('dwell_guard', 'inverse_guard', 'event_replay_guard_or_target', 'metropolis'):
                if reason in reached:
                    continue
                hit = enumerate_until(mod, toy, run, p, R,
                                      lambda o, d, r=reason: d.get('birth_residence_' + r),
                                      uniform=1. - 2. ** -40 if reason == 'metropolis' else 0.)
                if hit:
                    assert hit[2][1] == 'rejected' and hit[2][0] is p
                    reached[reason] = name
    assert set(reached) == {'dwell_guard', 'inverse_guard', 'event_replay_guard_or_target', 'metropolis'}, reached
    res['self_loop_reasons_reached'] = reached
    # g7 inverse canonical target (toy flag: reverse targets a different key)
    toyw = T.Toy(rev_wrong_target=True)
    hit = None
    for p in paths_of(toyw, run, 'no_events'):
        hit = enumerate_until(mod, toyw, run, p, R, lambda o, d: d.get('birth_residence_inverse_canonical_target'))
        if hit:
            break
    assert hit and hit[2][1] == 'rejected'
    res['inverse_canonical_target_self_loop'] = True
    # g8 stored W mismatch (terminal)
    p = eventful[0]
    pre = enumerate_until(mod, toy, run, p, R, lambda o, d: d.get('birth_residence_legal_transport'))[0]
    bad = copy.deepcopy(p)
    bad['events'][1]['W'] *= 1.0000001
    expect_stop(lambda: mod.move(run, bad, ScriptRNG(pre), new_diag(), toy, R), 'failed', 'Stored primitive')
    res['stored_rate_mismatch_fails'] = True
    # g9 union/per-owner contract: skewed W, dropped reverse marks, owner outside roster (terminal)
    for kw, text in (({'union_W_skew': True}, 'Union roster mark differs'),
                     ({'union_drop_rev': True}, 'Union roster reverse mark differs'),
                     ({'union_outside_owner': True}, 'outside the fixed original roster')):
        tz = T.Toy(**kw)
        found = False
        for pz in paths_of(tz, run, 'no_events'):
            hit = enumerate_until(mod, tz, run, pz, R, lambda o, d: isinstance(o, T.ToyStop))
            if hit:
                assert hit[2].status == 'failed' and text in hit[2].message, (kw, hit[2].message)
                found = True
                break
        assert found, kw
    res['union_vs_per_owner_contract_failures'] = ['W skew', 'reverse mark missing', 'owner outside roster']
    # g10 budget stop propagates from the first checkpoint
    toy.trigger, toy.checkpoints = 1, 0
    exc = expect_stop(lambda: mod.move(run, simple[0], ScriptRNG([0] * 9), new_diag(), toy, R), 'incomplete')
    assert isinstance(exc, T.ToyBudgetStop)
    toy.trigger = None
    res['budget_stop_propagates'] = True
    # F4 replay: an accepted eventful move whose replayed event W changed
    best = None
    for p in eventful:
        hit = enumerate_until(mod, toy, run, p, R, lambda o, d: isinstance(o, tuple) and o[1] == 'changed' and
                              any(a['W'] != b['W'] for a, b in zip(p['events'], o[0]['events'])))
        if hit:
            best = (p, hit)
            break
    assert best
    p, (prefix, dd, (new, st)) = best
    assert T.validate_path(toy, run, new)
    res['F4_replayed_events_valid_with_transformed_W'] = {
        'events': len(new['events']),
        'events_with_changed_W': sum(1 for a, b in zip(p['events'], new['events']) if a['W'] != b['W'])}
    # F5 interruption atomicity at every checkpoint of this accepted eventful proposal
    toy.trigger, toy.checkpoints, toy.checkpoint_log = None, 0, []
    full_out, st = mod.move(run, p, ScriptRNG(prefix), new_diag(), toy, R)
    assert st == 'changed'
    n_checks, log = toy.checkpoints, list(toy.checkpoint_log)
    assert log[-1] == 'before Birth residence atomic commit'
    snapshot = copy.deepcopy(p)
    for t in range(1, n_checks + 1):
        toy.trigger, toy.checkpoints = t, 0
        dd = new_diag()
        exc = expect_stop(lambda: mod.move(run, p, ScriptRNG(prefix), dd, toy, R), 'incomplete')
        assert isinstance(exc, T.ToyBudgetStop)
        assert p == snapshot
        assert not any('read_integral' in k or 'accepted' in k or 'donor' in k for k in dd), sorted(dd)
    toy.trigger = None
    res['F5_interruption'] = {'checkpoints_in_accepted_eventful_move': n_checks,
                              'every_checkpoint_interrupted': True, 'input_path_unchanged': True,
                              'no_read_integral_accepted_or_donor_diagnostic_written': True,
                              'last_checkpoint': log[-1], 'checkpoint_kinds': sorted(set(log))}
    return res


# ---------------- F6 mutants and controls ----------------------------------------------------
OWNER_TERM = "    owner_term = math.log(len(old_bearing)) - math.log(len(new_bearing))\n"
ANY_HELPER = ("def _any_owner_count(sampler, run, state, roster):\n"
              "    groups = frozenset(run['group'][o] for o in roster)\n"
              "    cs, _ = sampler._palette_channels(run, state, groups)\n"
              "    hit = set()\n"
              "    for ch in cs:\n"
              "        hit |= set(sampler._record_groups(run, ch['kind'], ch['owner']))\n"
              "    return sum(1 for o in roster if run['group'][o] in hit)\n\n\ndef move(")
MUTANTS = {
    'M1_missing_owner_count_correction': [(OWNER_TERM, "    owner_term = 0.0\n")],
    'M2a_counting_all_roster_owners': [
        (OWNER_TERM, "    owner_term = math.log(len(owner_roster)) - math.log(len(owner_roster))\n")],
    'M2b_counting_all_owners_with_any_mark': [
        (OWNER_TERM, "    owner_term = (math.log(_any_owner_count(sampler, run, segs[0]['state'], owner_roster))\n"
                     "                  - math.log(_any_owner_count(sampler, run, transformed[0]['state'], owner_roster)))\n"),
        ("def move(", ANY_HELPER)],
    'M3_v001_all_owner_selection_with_c2v002_correction': [
        ("    original_owner = old_bearing[int(rng.integers(0, len(old_bearing)))]\n"
         "    old_roster = old_rosters[original_owner]\n",
         "    original_owner = owner_roster[int(rng.integers(0, len(owner_roster)))]\n"
         "    old_roster = old_rosters.get(original_owner, [])\n"
         "    if not old_roster:\n        return reject('no_channel_bearing_owner')\n")],
    'CONTROL_per_owner_enumeration_same_kernel': [
        ("        cs, _ = sampler._palette_channels(run, state, union_groups)\n",
         "        cs = [c for o in owner_roster for c in sampler._palette_channels(run, state, frozenset((run['group'][o],)))[0]\n"
         "              if c['kind'] in ('birth', 'birth_rev') and c['owner'][0] == 'birth' and c['owner'][1] == o]\n")],
}


def mutant_source(src, edits):
    for old, new in edits:
        assert src.count(old) == 1, ('mutation anchor not unique', old[:60])
        src = src.replace(old, new)
    return src


def section_mutants(src):
    out = {}
    names = list(SKELETONS)
    variants = {k: (mutant_source(src, e), True) for k, e in MUTANTS.items()}
    v001_src = V001.read_text()
    assert hashlib.sha256(v001_src.encode()).hexdigest() == V001_SHA
    variants['CONTROL_reviewed_v001_transport_own_proposal'] = (v001_src, False)
    for mname, (msrc, oracle) in variants.items():
        mod = load_source(msrc, mname)
        per = []
        for name in names:
            r = run_case(mod, name, with_oracle=oracle)
            per.append({'case': name, 'flags': r['flags'],
                        'max_relative_detailed_balance_error': r['max_relative_detailed_balance_error'],
                        'max_abs_oracle_kernel_difference': r['max_abs_oracle_kernel_difference']})
        caught = any(any(v for v in p['flags'].values()) for p in per)
        out[mname] = {'source_sha256': hashlib.sha256(msrc.encode()).hexdigest(), 'caught': caught,
                      'oracle_compared': oracle,
                      'detected_by': sorted({k for p in per for k, v in p['flags'].items() if v}),
                      'max_relative_detailed_balance_error': max(p['max_relative_detailed_balance_error'] for p in per),
                      'cases': per}
    for k, v in out.items():
        if k.startswith('CONTROL'):
            assert not v['caught'], ('control should pass', k, v['detected_by'])
        else:
            assert v['caught'] and 'db_violation' in v['detected_by'], ('mutant not caught by detailed balance', k)
    return out


# ---------------- F7 exact no-owner self-loop probability -------------------------------------
def section_waste(mod):
    v001 = load_source(V001.read_text(), 'v001_for_waste')
    toy = T.Toy()
    run = T.make_run()
    res = {}
    for label, m, key in (('v001', v001, 'birth_residence_empty_reference_owner'),
                          ('c2v002', mod, 'birth_residence_no_channel_bearing_owner')):
        tot = 0.
        legal = 0.
        paths = paths_of(toy, run, 'no_events')
        for p in paths:
            stack = [[]]
            while stack:
                prefix = stack.pop()
                rng = ScriptRNG(prefix)
                d = new_diag()
                try:
                    m.move(run, p, rng, d, toy, T.OWNERS)
                except NeedChoice as nc:
                    stack.extend(prefix + [j] for j in range(nc.n))
                    continue
                w = 1. / prod(rng.ns) / len(paths)
                if d.get(key):
                    tot += w
                if d.get('birth_residence_legal_transport'):
                    legal += w
        res[label] = {'probability_no_owner_self_loop_uniform_over_states': tot,
                      'probability_legal_transport_uniform_over_states': legal}
    return res


def main():
    global T
    expected, out_path = sys.argv[1], Path(sys.argv[2])
    src_bytes = MODULE.read_bytes()
    actual = hashlib.sha256(src_bytes).hexdigest()
    assert actual == expected, 'module bytes differ from the declared pin'
    T = load_file(TOY, 'birth_fixture_toy')
    mod = load_file(MODULE, 'birth_c2v002_under_test')
    assert mod.MODULE_VERSION == 'birth_residence_c2v002'
    t0 = time.time()
    result = {'scope': 'Synthetic explicit states and exact enumeration only; no native operator, sampler or '
                       'production state; toy target deliberately not Birth-invariant.',
              'module': {'path': str(MODULE), 'sha256': actual},
              'toy_library': {'path': str(TOY), 'sha256': hashlib.sha256(TOY.read_bytes()).hexdigest()},
              'reviewed_v001': {'path': str(V001), 'sha256': V001_SHA},
              'fixture': {'path': str(Path(__file__).resolve()),
                          'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    result['F1_F2_exact_kernel_and_forward_reverse'] = section_f1_f2(mod)
    result['F3_F4_F5_guards_replay_interruption'] = section_guards(mod)
    result['F6_mutants_and_controls'] = section_mutants(src_bytes.decode())
    result['F7_no_owner_self_loop_probability'] = section_waste(mod)
    result['all_assertions_passed'] = True
    result['seconds'] = round(time.time() - t0, 1)
    with out_path.open('x') as f:
        json.dump(result, f, indent=1)
        f.write('\n')
    print(json.dumps({'ok': True, 'seconds': result['seconds'], 'out': str(out_path)}))


if __name__ == '__main__':
    main()
