"""Fixture for owned_worm_committed_capture_durability_v002.py (observer only; no sampling).

D1 exact key packing round trip (toy keys and 36864-bit ints; operator V003 L=4 seed and a born key
   from actual native Birth channels on explicit states).
D2 census / U / degree histogram / time means against an independent computation.
D3 synthetic observer integration with fake base/statistics: 2 chains x 20 committed rows, 16-row
   flush plus final flush, V001 row fields retained, reference fields aligned with measurement ids,
   decode equals the staged keys, worm_counters lookup, commit-tuple mismatch detected.
Usage: python3 -I -B durability_v002_fixture_v001.py <durability_sha256> <output_json>
The integration directory <output stem>_integration_run/ is created exclusively next to the output.
"""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'owned_worm_committed_capture_durability_v002.py'
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
OP = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py'),
      'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07')
AD = (UPC / 'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py',
      '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77')
FR = (UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py',
      '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7')


def load(name, path, sha=None):
    if sha is not None:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, path
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    expected, out_path = sys.argv[1], Path(sys.argv[2])
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == expected
    m = load('durability_v002_under_test', SOURCE)
    T = load('toy', HERE / 'worm_fixture_toy_c2v001.py')
    res = {'durability': {'path': str(SOURCE), 'sha256': expected}}
    # D1 packing
    big = [(0, 2 ** 36863 + 12345, 2 ** 36000 + 1, 0, 7, 2 ** 383, 2 ** 256 - 1),
           (5, 1, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0)]
    kb, kn, ks = m.encode_keys(big)
    assert m.decode_keys(kb, kn) == big and kb.dtype == np.uint8 and kb.shape[1] == 7
    assert all(bytes(ks[i]) == hashlib.sha256(','.join(format(v, 'x') for v in k).encode()).digest() for i, k in enumerate(big))
    op = load('op', *OP)
    ad = load('ad', *AD)
    fr = load('fr', *FR)
    binding = ad.build_inputs(L=4, coefficients=dict(fr.TRIAL), port_cache_entries=4096)
    reg = binding['registration']
    frame = tuple(tuple(v / 2. for v in p) for p in ad.PROTOTYPES4)
    reg['port_vectors'] = {'A': frame, 'B': tuple(tuple(-v for v in r) for r in frame)}
    reg['whitening'] = tuple(tuple(ad.W if i == j else 0. for j in range(3)) for i in range(3))
    reg['max_cached_graphs'] = 4
    ctx = ad.bind_context(operator_module=op, binding=binding)
    seed = op.canonical_state_key(context=ctx, state=binding['seed_state'])
    born = seed
    for o in tuple(binding['graph0']['A'])[:6]:
        recs = [r for r in op.palette_channels(context=ctx, state=born, palette_owners=[o]) if r.kind == 'birth']
        if recs:
            born = op.canonical_state_key(context=ctx, state=recs[0].target_state)
    kb, kn, ks = m.encode_keys([seed, born])
    assert m.decode_keys(kb, kn) == [seed, born] and born != seed
    res['D1_key_packing'] = {'synthetic_large_ints_exact': True, 'native_seed_and_born_keys_exact': True,
                             'native_key_field_bytes': kn.tolist(), 'packed_width_bytes': int(kb.shape[2])}
    # D2 census against an independent computation on native labels
    for key in (seed, born):
        lab = dict(op.state_labels(context=ctx, state=key))
        got = m.census(lab, 2.)
        deg = {}
        for a, b in lab['edges']:
            deg.setdefault(a, 0)
            deg.setdefault(b, 0)
        for a, b in lab['occupied']:
            deg[a] += 1
            deg[b] += 1
        hist = np.bincount(list(deg.values()), minlength=5).tolist()
        assert got == (len(lab['slots']), float(sum((d - 2) ** 2 for d in deg.values())), hist,
                       len(lab['occupied']), len(deg))
    res['D2_native_census'] = {'seed': list(m.census(dict(op.state_labels(context=ctx, state=seed)), 2.)),
                               'born': list(m.census(dict(op.state_labels(context=ctx, state=born)), 2.))}
    # D3 integration with fakes and the toy labels
    A, B, edges, births = T.cube_q3()
    toy = T.Toy(A=A, B=B, base_edges=edges, births=births)
    run = {'beta': 1., 'context': toy.context}

    class Base:
        def _measure(self, run, path):
            return (np.arange(3.) + len(path['times']), np.eye(2), np.ones(4), len(path['events']))

        def _measure_allk(self, run, path):
            return (np.zeros(5), np.zeros(2), np.ones(9))

    class Sampler:
        _BASE = Base()

    class Stats:
        def capture(self, **kw):
            return np.full(6, 2.)

    sink = []
    prepared = {'arguments': {'progress_sink': lambda *, record: sink.append(record)},
                'reweighting_capture_record': {'synthetic': True}, 'counters': {'c': 1},
                'mixture_counters': {}, 'worm_binding': {'counters': {'worm_loop_attempts': 7}}}
    directory = out_path.parent / (out_path.stem + '_integration_run') / 'committed_capture'
    directory.parent.mkdir(exist_ok=False)
    stats = Stats()
    obs = m.DurableCapture(directory=directory, sampler=Sampler, statistics=stats, prepared=prepared,
                           clean=lambda v: json.loads(json.dumps(v, default=str)), pins={'synthetic': 'pins'},
                           state_labels=toy.state_labels, dstar=2.)
    obs.install()
    staged = []
    rng = np.random.default_rng(0)
    cut = births[0]['cut']
    for c in (0, 1):
        for n in range(1, 21):
            while True:
                inc = frozenset(e for e in sorted(edges) if rng.random() < .5)
                x0 = (0, toy.base_mask, sum(1 << toy.code[e] for e in inc), 0, 0, 0, 0)
                path = T.build_path(toy, run, x0, [('birth', ('birth', 0, tuple(cut))), ('birth_rev', ('birth', 0, tuple(cut)))], [.3, .7])
                if path is not None:
                    break
            Sampler._BASE._measure(run, path)
            Sampler._BASE._measure_allk(run, path)
            stats.capture(metadata={'m': 1})
            staged.append((c, n - 1, path))
            prepared['arguments']['progress_sink'](record={'event': 'sweep', 'chain': c, 'measurements_committed': n})
    obs.close()
    blocks = sorted(directory.glob('block_*.npz'))
    rows = {}
    for f in blocks:
        with np.load(f, allow_pickle=False) as z:
            keys = m.decode_keys(z['reference_key_bytes'], z['reference_key_nbytes'])
            for i in range(len(keys)):
                rows[(int(z['chain_id'][i]), int(z['measurement_id'][i]))] = {
                    'key': keys[i], 'slots': int(z['reference_active_slots'][i]), 'U': float(z['reference_U'][i]),
                    'tU': float(z['time_mean_U'][i]), 'tS': float(z['time_mean_active_slots'][i]),
                    'fields': sorted(z.files)}
    assert len(rows) == 40 and len(blocks) == 3
    for c, i, path in staged:
        r = rows[(c, i)]
        assert r['key'] == path['segments'][0]['key']
        labs = [dict(toy.state_labels(context=toy.context, state=s['key'])) for s in path['segments']]
        cs = [m.census(l, 2.) for l in labs]
        ends = [0., .3, .7, 1.]
        assert r['slots'] == cs[0][0] and r['U'] == cs[0][1]
        assert abs(r['tU'] - math.fsum((ends[j + 1] - ends[j]) * cs[j][1] for j in range(3))) < 1e-15
        assert abs(r['tS'] - .4) < 1e-15  # Birth active on the middle dwell [.3,.7)
    meta = json.loads((directory / 'block_000000.json').read_text())
    assert meta['worm_counters'] == {'worm_loop_attempts': 7} and meta['rows'] == 16
    v001_fields = {'chain_id', 'measurement_id', 'score', 'contact', 'reads', 'events', 'score_cells',
                   'allk_contacts', 'background', 'features'}
    assert v001_fields <= set(rows[(0, 0)]['fields'])
    # commit-tuple mismatch: a committed measurement without the staged reference
    obs2 = m.DurableCapture.__new__(m.DurableCapture)
    obs2.pending = {'measure': (1, 2, 3, 4), 'allk': (1, 2, 3), 'raw': np.zeros(1)}
    obs2.last_ids = {}
    obs2.rows = []
    obs2.original_progress = lambda *, record: None
    try:
        obs2.progress(record={'event': 'sweep', 'chain': 0, 'measurements_committed': 1})
        raise AssertionError('mismatch not detected')
    except ValueError as exc:
        assert 'commit tuple' in str(exc)
    res['D3_integration'] = {'rows': 40, 'blocks': len(blocks), 'fields': rows[(0, 0)]['fields'],
                             'reference_keys_exact': True, 'census_and_time_means_exact': True,
                             'v001_fields_retained': True, 'worm_counters_lookup': True,
                             'commit_tuple_mismatch_detected': True, 'directory': str(directory)}
    with out_path.open('x') as f:
        json.dump(res, f, indent=1)
        f.write('\n')
    print(json.dumps({'ok': True}))


if __name__ == '__main__':
    main()
