"""Native explicit-state checks of the worm move's operator binding (operator V003, L=4 binding).

No sampler, no worker, no sampling of the target: only the operator's public functions on a few
EXPLICIT states (the registered seed, states born from it by actual native Birth channels, and a
two-dwell Birth/reverse explicit path).  Checks:
  N1 label-route whole-loop flip (state_labels -> toggled 'occupied' -> canonical_state_key) equals
     the sequential composition of the actual native positive-rate flip marks, changes only the
     incidence component, by popcount = loop length;
  N2 raw diagonal sum and the uniform-lapse sampler-form sum  sum_X d_X (1 + sum_alpha w_alphaX)
     are bit-identical after an alternating loop (degrees, n_e count preserved), while the
     incidence reads change; a non-alternating single-edge flip does change the diagonal;
  N3 native event replay on an explicit Birth/reverse path after a worm flip on its eligible graph;
  N4 explicit-state proposal statistics of grow_walk (fixed fixture RNG 467, NOT the pilot seed) on
     the seed, a born state and a defect-laden born state (64 native single-edge flips, RNG 4672):
     closure fraction, loop/tail lengths, winding vs contractible, exact reverse-product equality.
Usage: python3 -I -B worm_loop_native_explicit_check_c2v001.py <worm_module_sha256> <output_json>
"""
import hashlib
import importlib.util
import json
import math
import sys
import time
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


def load(name, path, sha):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, path
    spec = importlib.util.spec_from_file_location('native_check_' + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    worm_sha, out_path = sys.argv[1], Path(sys.argv[2])
    wpath = HERE / 'owned_worm_loop_whole_path_c2v001.py'
    worm = load('worm', wpath, worm_sha)
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
    calls = {'palette_channels': 0}

    def owner_of(v):
        return ad.label_metadata(v, L=L)[4]

    def channels(key, owners):
        calls['palette_channels'] += 1
        return op.palette_channels(context=ctx, state=key, palette_owners=sorted(set(owners)))

    def native_flip(key, e):
        hits = [r for r in channels(key, [owner_of(e[0]), owner_of(e[1])])
                if r.kind == 'flip' and r.owner_id == ('flip', ('edge', e)) and r.amplitude != 0]
        assert len(hits) == 1, ('native flip mark', e, len(hits))
        return op.canonical_state_key(context=ctx, state=hits[0].target_state)

    def labels(key):
        return dict(op.state_labels(context=ctx, state=key))

    def label_flip(key, loop):
        lab = labels(key)
        lab['occupied'] = tuple(sorted(set(map(tuple, lab['occupied'])) ^ set(loop)))
        return op.canonical_state_key(context=ctx, state=lab)

    def diag_sums(key):
        recs = op.diagonal_terms(context=ctx, state=key)
        raw = math.fsum(complex(r.amplitude).real for r in recs)
        lapse = math.fsum(complex(r.amplitude).real * math.fsum([1.] + [float(w) for w in r.energy_weights])
                          for r in recs if complex(r.amplitude) != 0)
        return raw, lapse

    def reads(key):
        return np.asarray(op.read_rows(context=ctx, state=key)['values'], dtype=np.float64)

    def winding(loop, w0):
        v, tot = w0, [0, 0, 0]
        for e in loop:
            w = e[1] if v == e[0] else e[0]
            cv, cw = ad.label_metadata(v, L=L)[1], ad.label_metadata(w, L=L)[1]
            for i in range(3):
                tot[i] += (cw[i] - cv[i] + L // 2) % L - L // 2
            v = w
        assert v == w0 and all(t % L == 0 for t in tot), tot
        return tuple(t // L for t in tot)

    def walk_stats(key, n, seed, label):
        lab = labels(key)
        col = worm.eligible_colouring([lab])
        rng = np.random.default_rng(seed)
        status, lengths, tails, wnd, ratio_ok = {}, [], [], {'winding': 0, 'contractible': 0}, 0
        examples = []
        for _ in range(n):
            w = worm.grow_walk(col, roster, lambda k: int(rng.integers(0, k)), worm.MAX_WALK_STEPS)
            status[w['status']] = status.get(w['status'], 0) + 1
            if w['status'] != 'closed':
                continue
            loop = w['edges'][w['closure']:]
            assert worm.loop_contract(col, loop)
            col2 = {e: c ^ (1 if e in set(loop) else 0) for e, c in col.items()}
            rp = worm.walk_branch_product(col2, roster, w['start'], worm.reverse_edges(w['edges'], w['closure']),
                                          worm.MAX_WALK_STEPS)
            ratio_ok += rp == w['branch_product']
            lengths.append(len(loop))
            tails.append(w['closure'])
            wnd['winding' if any(winding(loop, w['closure_vertex'])) else 'contractible'] += 1
            if len(examples) < 3:
                examples.append(loop)
        ls = np.asarray(lengths)
        deg = {}
        occ = set(map(tuple, lab['occupied']))
        for e in lab['edges']:
            for v in e:
                deg.setdefault(v, 0)
        for a, b in occ:
            deg[a] += 1
            deg[b] += 1
        return {'state': label, 'walks': n, 'status_counts': status, 'eligible_edges': len(col),
                'present_vertices': len(deg), 'active_slots': len(lab['slots']),
                'U_sum_d_minus_2_sq': int(sum((d - 2) ** 2 for d in deg.values())),
                'loop_length_mean': float(ls.mean()) if ls.size else None,
                'loop_length_quantiles_10_50_90_max': [float(x) for x in np.quantile(ls, [.1, .5, .9, 1.])] if ls.size else None,
                'loop_length_4_fraction': float(np.mean(ls == 4)) if ls.size else None,
                'tail_length_mean': float(np.mean(tails)) if tails else None,
                'closed_loops_by_winding': wnd, 'reverse_product_equal_forward': ratio_ok,
                'closed': int(ls.size)}, examples

    out = {'scope': 'Operator V003 public functions on explicit L=4 states only; no sampler, no sampling, '
                    'no worker. N4 statistics are explicit-state proposal statistics under fixture RNG 467, '
                    'not predictions of the pilot.',
           'pins': {k: {'path': str(p), 'sha256': s} for k, (p, s) in PINS.items()},
           'worm_module': {'path': str(wpath), 'sha256': worm_sha}, 'TRIAL': dict(fr.TRIAL)}
    key0 = op.canonical_state_key(context=ctx, state=binding['seed_state'])
    # Born states by actual native Birth channels from the seed, distinct owners in roster order.
    born, births_applied = key0, []
    for o in roster:
        if len(births_applied) >= 12:
            break
        recs = [r for r in channels(born, [o]) if r.kind == 'birth' and r.amplitude != 0]
        if recs:
            born = op.canonical_state_key(context=ctx, state=recs[0].target_state)
            births_applied.append({'owner': o, 'birth_owner_id': repr(recs[0].owner_id)[:200]})
    out['born_state'] = {'births_applied': len(births_applied), 'owners': [b['owner'] for b in births_applied]}

    # Defect-laden explicit state: native single-edge flips of 64 uniformly chosen current edges.
    defected = born
    frng = np.random.default_rng(4672)
    for _ in range(64):
        edges_now = sorted(map(tuple, labels(defected)['edges']))
        defected = native_flip(defected, edges_now[int(frng.integers(0, len(edges_now)))])
    n1 = []
    n2 = []
    stats = []
    for label, key in (('seed', key0), ('born_from_seed_by_native_births', born),
                       ('born_plus_64_native_single_edge_flips', defected)):
        st, examples = walk_stats(key, 4000, 467, label)
        stats.append(st)
        raw0, lap0 = diag_sums(key)
        r0 = reads(key)
        for loop in examples[:2]:
            k_label = label_flip(key, loop)
            k_seq = key
            for e in loop:
                k_seq = native_flip(k_seq, e)
            mask = key[2] ^ k_label[2]
            n1.append({'state': label, 'loop_length': len(loop), 'label_route_equals_native_sequence': k_label == k_seq,
                       'only_incidence_changed': all(k_label[j] == key[j] for j in (0, 1, 3, 4, 5, 6)),
                       'popcount_mask_equals_length': bin(mask).count('1') == len(loop)})
            raw1, lap1 = diag_sums(k_label)
            r1 = reads(k_label)
            n2.append({'state': label, 'loop_length': len(loop), 'raw_diagonal_identical': raw1 == raw0,
                       'uniform_lapse_sampler_form_identical': lap1 == lap0,
                       'raw_diagonal_change': raw1 - raw0, 'reads_changed': int(np.sum(r1 != r0)),
                       'max_abs_read_change': float(np.max(np.abs(r1 - r0)))})
        # control: single-edge flip (not alternating) changes the diagonal
        e = sorted(map(tuple, labels(key)['occupied']))[0]
        k1 = native_flip(key, e)
        raw1, lap1 = diag_sums(k1)
        n2.append({'state': label, 'control_single_occupied_edge_flip_raw_diagonal_change': raw1 - raw0,
                   'control_changes_diagonal': raw1 != raw0})
    out['N1_label_route_vs_native_flips'] = n1
    out['N2_diagonal_invariance_and_read_change'] = n2
    out['N4_explicit_state_walk_statistics'] = stats
    # N3: explicit Birth/reverse path seed -> born1 -> seed; worm flip on its eligible graph.
    o = births_applied[0]['owner'] if births_applied else None
    n3 = {'available': o is not None}
    if o is not None:
        recs = [r for r in channels(key0, [o]) if r.kind == 'birth' and r.amplitude != 0]
        b = recs[0]
        x1 = op.canonical_state_key(context=ctx, state=b.target_state)
        rev = [r for r in channels(x1, [o]) if r.kind == 'birth_rev' and r.owner_id == b.owner_id
               and op.canonical_state_key(context=ctx, state=r.target_state) == key0]
        col = worm.eligible_colouring([labels(key0), labels(x1), labels(key0)])
        rng = np.random.default_rng(4671)
        tried = replay_ok = 0
        details = []
        for _ in range(200):
            w = worm.grow_walk(col, roster, lambda k: int(rng.integers(0, k)), worm.MAX_WALK_STEPS)
            if w['status'] != 'closed':
                continue
            loop = w['edges'][w['closure']:]
            y0, y1 = label_flip(key0, loop), label_flip(x1, loop)
            fwd = [r for r in channels(y0, [o]) if r.kind == 'birth' and r.owner_id == b.owner_id]
            ok = (len(fwd) == 1 and op.canonical_state_key(context=ctx, state=fwd[0].target_state) == y1)
            bk = [r for r in channels(y1, [o]) if r.kind == 'birth_rev' and r.owner_id == b.owner_id]
            ok_rev = (len(bk) == 1 and op.canonical_state_key(context=ctx, state=bk[0].target_state) == y0)
            tried += 1
            replay_ok += ok and ok_rev
            if len(details) < 3:
                details.append({'loop_length': len(loop), 'forward_birth_replays_to_transformed': ok,
                                'reverse_replays_to_transformed': ok_rev,
                                'W_amplitude_equal': (abs(fwd[0].amplitude) == abs(b.amplitude)) if fwd else None})
            if tried >= 10:
                break
        n3.update({'birth_owner': o, 'reverse_present_on_original': len(rev) == 1,
                   'eligible_edges_across_three_dwells': len(col),
                   'graph_edges_reference': len(labels(key0)['edges']),
                   'loops_tried': tried, 'loops_with_exact_native_replay_both_events': replay_ok,
                   'examples': details})
    out['N3_native_birth_reverse_replay'] = n3
    out['palette_channel_calls'] = calls['palette_channels']
    out['seconds'] = round(time.time() - t0, 1)
    with out_path.open('x') as f:
        json.dump(out, f, indent=1)
        f.write('\n')
    print(json.dumps({'ok': True, 'seconds': out['seconds']}))


if __name__ == '__main__':
    main()
