"""Native explicit-state checks of the c2v002 Birth-residence binding (operator V003, L=4 binding).

No V006 sampler, no worker, no sampling of the target.  Explicit states only: the registered
seed, a state born from it by 12 actual native Birth channels, a SATURATED state (native Births
applied owner by owner in roster order until no owner has a Birth channel; the pilot rows had
120-128 of 128 slots active), and that saturated state after 64 native single-edge flips.
  C1 union-palette partition: ONE operator palette_channels call over all 128 original owners,
     Birth/reverse records with owner_id[0] == 'birth' partitioned by owner_id[1], equals for
     EVERY owner the per-owner palette_channels Birth/reverse records (V001's roster) and the
     primitive_channels partition, as multisets of (kind, owner_id, target key, amplitude,
     energy_weights); every Birth owner_id[1] is a roster label.  Reports |S(x)|, the V001
     empty-owner fraction 1 - |S(x)|/128 and timings.
  C2 module run on explicit native closed paths through a NATIVE-STATE SHIM of the sampler API
     (operator calls; W = |amplitude| and D = raw diagonal sum, which equal the sampler's values
     for TRIAL's uniform lapse 1; NOT the V006 sampler): fixed fixture RNG 1702 (not the pilot
     seed), outcomes counted; every changed proposal is reversed with scripted choices, must
     restore the path exactly with forward + reverse log MH == 0.0.
Usage: python3 -I -B birth_residence_native_explicit_check_c2v002.py <module_sha256> <output_json>
"""
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PINS = {
    'operator': (X / 'owned_retained_response_0405/owned_parent_operator_v003.py',
                 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07'),
    'adapter': (UPC / 'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py',
                '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77'),
    'family_recipe': (UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py',
                      '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7'),
}
L = 4
BK = ('birth', 'birth_rev')


def load(name, path, sha):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, path
    spec = importlib.util.spec_from_file_location('birth_native_check_' + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ShimStop(Exception):
    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status, self.stage, self.message = status, stage, message


class NativeShim:
    """Sampler-API subset used by the Birth module, built directly on operator V003 calls."""
    _Stop = ShimStop

    def __init__(self, op, ctx, group):
        self.op, self.ctx, self.group = op, ctx, group
        self.palette_calls = 0
        self.palette_seconds = 0.

    def _budget_check(self, run, phase, what):
        pass

    def _record_groups(self, run, kind, owner):
        if kind in BK and owner[0] == 'birth':
            return frozenset((self.group[owner[1]],))
        raise ShimStop('failed', run['stage'], 'shim classifies Birth marks only')

    def _palette_channels(self, run, state, groups):
        t = time.time()
        recs = self.op.palette_channels(context=self.ctx, state=state, palette_owners=sorted(groups))
        self.palette_seconds += time.time() - t
        self.palette_calls += 1
        cs = []
        for r in recs:
            if r.kind == 'diag' or complex(r.amplitude) == 0:
                continue
            cs.append({'kind': r.kind, 'owner': r.owner_id, 'target': r.target_state,
                       'W': abs(complex(r.amplitude)), 'key': None, 'has_key': False})
        return cs, math.fsum(c['W'] for c in cs)

    def _unique_mark(self, run, channels, kind, owner, where):
        hits = [c for c in channels if c['kind'] == kind and c['owner'] == owner]
        if len(hits) > 1:
            raise ShimStop('failed', run['stage'], where + ': duplicate')
        return hits[0] if hits else None

    def _state_key(self, run, state):
        return self.op.canonical_state_key(context=self.ctx, state=state)

    def _target_key(self, run, ch):
        if not ch['has_key']:
            ch['key'], ch['has_key'] = self._state_key(run, ch['target']), True
        return ch['key']

    def _segment_core(self, run, state):
        key = self._state_key(run, state)
        recs = self.op.diagonal_terms(context=self.ctx, state=key)
        D = math.fsum(complex(r.amplitude).real for r in recs)
        row = np.asarray(self.op.read_rows(context=self.ctx, state=key)['values'], dtype=np.float64)
        return {'state': key, 'key': key, 'D': D, 'r': None, 'row': row}

    def _event_from_channel(self, run, ch):
        return {'kind': ch['kind'], 'owner': ch['owner'], 'W': ch['W']}

    def _keys_equal(self, run, a, b):
        return a == b

    def _check_times(self, run, times, horizon):
        prev = 0.
        for t in times:
            assert prev < t < horizon
            prev = t


class ScriptRNG:
    def __init__(self, prefix):
        self.prefix, self.i = list(prefix), 0

    def integers(self, low, high):
        v = self.prefix[self.i]
        self.i += 1
        assert 0 <= v < high - low
        return low + v

    def random(self):
        return 0.0


class RecordingRNG:
    def __init__(self, rng):
        self.rng, self.draws = rng, []

    def integers(self, low, high):
        v = int(self.rng.integers(low, high))
        self.draws.append(v - low)
        return v

    def random(self):
        return float(self.rng.random())


def main():
    sha, out_path = sys.argv[1], Path(sys.argv[2])
    mpath = HERE / 'owned_worldline_birth_residence_transport_c2v002.py'
    mod = load('module', mpath, sha)
    op = load('operator', *PINS['operator'])
    ad = load('adapter', *PINS['adapter'])
    fr = load('family_recipe', *PINS['family_recipe'])
    t0 = time.time()
    binding = ad.build_inputs(L=L, coefficients=dict(fr.TRIAL), port_cache_entries=4096)
    reg = binding['registration']
    frame = tuple(tuple(v / 2. for v in p) for p in ad.PROTOTYPES4)
    reg['port_vectors'] = {'A': frame, 'B': tuple(tuple(-v for v in r) for r in frame)}
    reg['whitening'] = tuple(tuple(ad.W if i == j else 0. for j in range(3)) for i in range(3))
    reg['max_cached_graphs'] = 4
    ctx = ad.bind_context(operator_module=op, binding=binding)
    roster = tuple(binding['graph0']['A']) + tuple(binding['graph0']['B'])
    rset = set(roster)
    g0 = binding['graph0']
    group = {o: o for o in roster}  # the V004 sampler's permanent group map (originals and slots)
    for o in roster:
        for lab in g0['slots'][o]:
            group[lab] = o

    def ident(r):
        return (r.kind, r.owner_id, op.canonical_state_key(context=ctx, state=r.target_state),
                complex(r.amplitude), tuple(float(w) for w in r.energy_weights))

    def births(recs):
        return [r for r in recs if r.kind in BK and r.owner_id[0] == 'birth']

    def labels(key):
        return dict(op.state_labels(context=ctx, state=key))

    def nb(key, o):
        return [r for r in births(op.palette_channels(context=ctx, state=key, palette_owners=[o]))
                if r.kind == 'birth' and complex(r.amplitude) != 0]

    key0 = op.canonical_state_key(context=ctx, state=binding['seed_state'])
    born = key0
    for o in roster[:12]:
        recs = nb(born, o)
        if recs:
            born = op.canonical_state_key(context=ctx, state=recs[0].target_state)
    sat, applied = key0, 0
    progress = True
    while progress:
        progress = False
        for o in roster:
            recs = nb(sat, o)
            if recs:
                sat = op.canonical_state_key(context=ctx, state=recs[0].target_state)
                applied += 1
                progress = True
    frng = np.random.default_rng(17021)
    defect = sat
    for _ in range(64):
        es = sorted(map(tuple, labels(defect)['edges']))
        e = es[int(frng.integers(0, len(es)))]
        hits = [r for r in op.palette_channels(context=ctx, state=defect, palette_owners=sorted({group[e[0]], group[e[1]]}))
                if r.kind == 'flip' and r.owner_id == ('flip', ('edge', e)) and complex(r.amplitude) != 0]
        assert len(hits) == 1
        defect = op.canonical_state_key(context=ctx, state=hits[0].target_state)
    states = [('seed', key0), ('born_12_native_births', born), ('saturated_native_births', sat),
              ('saturated_plus_64_native_single_edge_flips', defect)]
    out = {'scope': 'Operator V003 public functions on explicit L=4 states; C2 uses a native-state shim of '
                    'the sampler API (not the V006 sampler); fixture RNG 1702 is not the pilot seed. No sampling '
                    'of the target, no worker.',
           'pins': {k: {'path': str(p), 'sha256': s} for k, (p, s) in PINS.items()},
           'module': {'path': str(mpath), 'sha256': sha}, 'saturated_births_applied': applied}
    c1 = []
    for label, key in states:
        lab = labels(key)
        t = time.time()
        union = op.palette_channels(context=ctx, state=key, palette_owners=list(roster))
        t_union = time.time() - t
        t = time.time()
        full = op.primitive_channels(context=ctx, state=key)
        t_full = time.time() - t
        part_u, part_f, outside = {}, {}, 0
        for src, part in ((union, part_u), (full, part_f)):
            for r in births(src):
                if r.owner_id[1] not in rset:
                    outside += 1
                    continue
                part.setdefault(r.owner_id[1], []).append(ident(r))
        mismatches, t_per = 0, 0.
        for o in roster:
            t = time.time()
            per = op.palette_channels(context=ctx, state=key, palette_owners=[o])
            t_per += time.time() - t
            want = Counter(ident(r) for r in births(per) if r.owner_id[1] == o)
            if Counter(part_u.get(o, [])) != want or Counter(part_f.get(o, [])) != want:
                mismatches += 1
        bearing = [o for o in roster if any(x[3] != 0 for x in part_u.get(o, []))]
        kinds = {}
        for o in bearing:
            for x in part_u[o]:
                if x[3] != 0:
                    kinds[x[0]] = kinds.get(x[0], 0) + 1
        c1.append({'state': label, 'active_slots': len(lab['slots']), 'present_edges': len(lab['edges']),
                   'owners_with_birth_mark_S': len(bearing),
                   'v001_empty_owner_fraction': 1. - len(bearing) / len(roster),
                   'birth_marks_by_kind': kinds,
                   'owners_whose_union_partition_differs_from_per_owner_or_full': mismatches,
                   'birth_records_with_owner_outside_roster': outside,
                   'seconds_union_call': round(t_union, 4), 'seconds_full_primitive_call': round(t_full, 4),
                   'seconds_128_per_owner_calls': round(t_per, 4)})
        assert mismatches == 0 and outside == 0
    out['C1_union_partition_equals_per_owner_rosters'] = c1
    # C2 module on explicit native closed paths through the shim
    shim = NativeShim(op, ctx, group)
    run = {'beta': 1., 'stage': 'native explicit', 'caps': {'max_events_per_path': 10000},
           'burn_in_sweeps': 0, 'group': group}
    rng = np.random.default_rng(1702)
    c2 = []
    for label, key in states:
        seg0 = shim._segment_core(run, key)
        paths = [('no_events', {'segments': [seg0], 'events': [], 'times': []})]
        o = next((o for o in roster if nb(key, o)), None)
        if o is not None:
            b = nb(key, o)[0]
            x1 = op.canonical_state_key(context=ctx, state=b.target_state)
            back = [r for r in op.palette_channels(context=ctx, state=x1, palette_owners=[o])
                    if r.kind == 'birth_rev' and r.owner_id == b.owner_id]
            if len(back) == 1 and op.canonical_state_key(context=ctx, state=back[0].target_state) == key:
                paths.append(('birth_reverse_owner_' + str(o), {
                    'segments': [seg0, shim._segment_core(run, x1), seg0],
                    'events': [{'kind': 'birth', 'owner': b.owner_id, 'W': abs(complex(b.amplitude))},
                               {'kind': 'birth_rev', 'owner': b.owner_id, 'W': abs(complex(back[0].amplitude))}],
                    'times': [.3, .7]}))
        for pname, path in paths:
            outcomes, reversed_ok, sums, owner_counts = {}, 0, [], []
            for _ in range(6):
                rr = RecordingRNG(rng)
                diag = {'sweeps_completed': 0}
                new, status = mod.move(run, path, rr, diag, shim, roster)
                reasons = [k[len('birth_residence_'):] for k in diag if k.startswith('birth_residence_')
                           and k[len('birth_residence_'):] in ('no_channel_bearing_owner', 'dwell_guard',
                           'inverse_guard', 'inverse_canonical_target', 'event_replay_guard_or_target', 'metropolis')]
                tag = status if status == 'changed' else 'rejected:' + ','.join(reasons)
                outcomes[tag] = outcomes.get(tag, 0) + 1
                lp = diag.get('birth_residence_last_proposal')
                if lp is not None:
                    owner_counts.append([lp['forward_owner_count'], lp['reverse_owner_count']])
                if status != 'changed':
                    continue
                inv = 'birth_rev' if lp['kind'] == 'birth' else 'birth'
                y = new['segments'][0]['key']
                cs, _ = shim._palette_channels(run, y, frozenset(group[x] for x in roster))
                Sy = [x for x in roster if any(c['kind'] in BK and c['owner'][0] == 'birth' and c['owner'][1] == x for c in cs)]
                Ry = [c for c in cs if c['kind'] in BK and c['owner'][0] == 'birth' and c['owner'][1] == lp['original_owner']]
                fwd_owner = None
                xs, _ = shim._palette_channels(run, path['segments'][0]['key'], frozenset(group[x] for x in roster))
                Rx = [c for c in xs if c['kind'] in BK and c['owner'][0] == 'birth' and c['owner'][1] == lp['original_owner']]
                fwd_owner = Rx[rr.draws[1]]['owner']
                pre = [Sy.index(lp['original_owner']),
                       [i for i, c in enumerate(Ry) if c['kind'] == inv and c['owner'] == fwd_owner][0]]
                d2 = {'sweeps_completed': 0}
                back_path, st2 = mod.move(run, new, ScriptRNG(pre), d2, shim, roster)
                same = (st2 == 'changed' and [s['key'] for s in back_path['segments']] == [s['key'] for s in path['segments']]
                        and [(e['kind'], e['owner'], e['W']) for e in back_path['events']] ==
                        [(e['kind'], e['owner'], e['W']) for e in path['events']])
                s = lp['log_mh_ratio'] + d2['birth_residence_last_proposal']['log_mh_ratio']
                reversed_ok += same and s == 0.0
                sums.append(s)
                assert same and s == 0.0, (label, pname, s)
            c2.append({'state': label, 'path': pname, 'attempts': 6, 'outcomes': outcomes,
                       'forward_reverse_owner_counts': owner_counts,
                       'changed_reversed_exactly_with_zero_log_mh_sum': reversed_ok,
                       'max_abs_forward_plus_reverse_log_mh': max(map(abs, sums)) if sums else None})
    out['C2_module_on_native_explicit_paths_via_shim'] = c2
    out['shim_palette_calls'] = shim.palette_calls
    out['shim_palette_seconds'] = round(shim.palette_seconds, 2)
    out['seconds'] = round(time.time() - t0, 1)
    with out_path.open('x') as f:
        json.dump(out, f, indent=1, default=repr)
        f.write('\n')
    print(json.dumps({'ok': True, 'seconds': out['seconds']}))


if __name__ == '__main__':
    main()
