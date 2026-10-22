#!/usr/bin/env python3
"""INTERFACE PROOF for roster_builder_c2v006 (root ruling A173 on OI-A1, ruling (a)): classifier A's own record
checks, run on the records the builders write over the synthetic test fixtures.

Usage: python3 -I -B interface_proof_c2v006.py --out FILE      (FILE must not exist; written by exclusive create)

What it does (read-only on every input; the only file written is --out):
  1. Loads classifier_a_c4v004.py (e92aa30e) from its verified bytes as a module (exec of the bytes; no bytecode is
     written, nothing of the module is run except the two checker methods below and their helpers). It never runs
     classify_bundle and opens no file through classifier A except the pinned list and rosters of item 2.
  2. Gate list: for every FULL build that the c2v006 record run RUN1 wrote (test_records_c2v006/RUN1/work/out/*/
     GATE_STATUS_LIST.json, synthetic fixtures), classifier A's Run.check_gate_list over that list and the build's six
     rosters (read through A's own sha-verified read_pinned). The same for every FULL build of the c2v005 record run
     RUN1 (test_records_c2v005/RUN1), and for each c2v005 list with only "schema": "GATE_STATUS_LIST_C4V001" added
     (in memory), which isolates the mismatch to the key.
  3. Gate list agreement: on one c2v006 list (case X01), variants (as written; no schema; wrong schema strings; an
     extra key) through c2v006's and c2v005's _a_gate_list_problem and through classifier A's check_gate_list.
  4. TSR flag record: classifier A's Run.check_tsr on ROOT_TSR_FLAG_RECORD_V003 (written by c2v006 tsr-record) and on
     V002 (c2v005's record), and on in-memory variants of V003, with in-memory synthetic stand-ins for the other
     carriers check_tsr reads (the compare document, the TSR support record, the freeze manifest's input_files),
     built from classifier A's own constants so that only the flag record can fire. The compare, N1 and node files
     the records pin are not opened. c2v006's tsr_record_v003 is run in memory on V001 and must give V003's bytes.
No NGC3198 target, observed, velocity or sigma file, no slots file and no query manifest is opened.
"""
import hashlib
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.realpath(__file__))
FOLDER = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2'
PINS = {
    'classifier_a': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/build_c4v004/'
                     'classifier_a_c4v004.py', 'e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0'),
    'builder_c2v006': (FOLDER + '/roster_builder_c2v006.py',
                       '0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2'),
    'builder_c2v005': (FOLDER + '/roster_builder_c2v005.py',
                       '653ced76513d3415d8d4904a73bf1c2dc6d316a053be4f89029611c80ffc9075'),
    'tsr_v003': (FOLDER + '/ROOT_TSR_FLAG_RECORD_V003.json',
                 '7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070'),
    'tsr_v002': (FOLDER + '/ROOT_TSR_FLAG_RECORD_V002.json',
                 'c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0'),
    'tsr_v001': (FOLDER + '/ROOT_TSR_FLAG_RECORD_V001.json',
                 '61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc'),
    'test_record_c2v006_run1': (FOLDER + '/test_records_c2v006/RUN1/TEST_RECORD.json',
                                '1896a0d885bd7c182f86446709430e2ab0d2245915994f018dc66ac9c69c71d1'),
    'test_record_c2v005_run1': (FOLDER + '/test_records_c2v005/RUN1/TEST_RECORD.json',
                                'dbabe47228bf45ae43313b46e3cfa16f7e4686365a077f6464319faa0cb1847e'),
}
OUT_DIRS = {'c2v006': FOLDER + '/test_records_c2v006/RUN1/work/out',
            'c2v005': FOLDER + '/test_records_c2v005/RUN1/work/out'}
SYN_SHA = '0' * 64


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_pinned_bytes(key):
    path, want = PINS[key]
    with open(path, 'rb') as f:
        raw = f.read()
    if sha(raw) != want:
        raise SystemExit('PIN_MISMATCH: %s' % key)
    return raw


def load_module(key, name):
    raw = read_pinned_bytes(key)
    mod = types.ModuleType(name)
    mod.__file__ = os.path.realpath(PINS[key][0])
    exec(compile(raw, mod.__file__, 'exec'), mod.__dict__)
    return mod


def pin_of(path):
    with open(path, 'rb') as f:
        return {'path': os.path.realpath(path), 'sha256': sha(f.read())}


def stop_summary(run):
    return sorted({'%s|%s' % (k[0], d) for k, v in run.stops.items() for d in (v['detail'] or {''})})


def a_gate_check(A, gl_doc, rosters, gl_load_err=None):
    """classifier A's own check_gate_list on an in-memory list and the build's loaded rosters."""
    run = A.Run('/synthetic/interface_proof_bundle.json')
    run.docs = {'gate_status_list': gl_doc}
    run.load_err = {'gate_status_list': gl_load_err}
    run.rosters = rosters
    run.gate_list_out = None
    run.check_gate_list()
    return run


def load_build(A, out_dir):
    """The build's list (through A's read_pinned, sha-verified) and its six rosters (A's read_pinned)."""
    run = A.Run('/synthetic/interface_proof_bundle.json')
    gl_doc, gl_err = run.read_pinned(pin_of(os.path.join(out_dir, 'GATE_STATUS_LIST.json')))
    with open(os.path.join(out_dir, 'ROSTER_PINS.json'), 'rb') as f:
        rpins = json.loads(f.read())['row_registration_rosters']
    rosters = {}
    for name, spec in sorted(rpins.items()):
        doc, err = run.read_pinned(spec)
        rosters[name] = (doc, err, spec['sha256'])
    return gl_doc, gl_err, rosters


def gate_lists(A, label):
    root = OUT_DIRS[label]
    res = []
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        if not os.path.isfile(os.path.join(d, 'GATE_STATUS_LIST.json')):
            continue
        gl_doc, gl_err, rosters = load_build(A, d)
        run = a_gate_check(A, gl_doc, rosters, gl_err)
        entry = {'build': name, 'list_keys': sorted(gl_doc) if isinstance(gl_doc, dict) else None,
                 'list_sha256': pin_of(os.path.join(d, 'GATE_STATUS_LIST.json'))['sha256'],
                 'a_stops': stop_summary(run),
                 'a_gate_list_defect': any(k[0] == 'GATE_STATUS_LIST_DEFECT' for k in run.stops),
                 'a_gate_list_out_is_the_list': run.gate_list_out == (gl_doc or {}).get('gates')}
        if label == 'c2v005':
            run2 = a_gate_check(A, dict(gl_doc, schema='GATE_STATUS_LIST_C4V001'), rosters)
            entry['with_schema_added_a_stops'] = stop_summary(run2)
            entry['with_schema_added_a_gate_list_defect'] = any(
                k[0] == 'GATE_STATUS_LIST_DEFECT' for k in run2.stops)
        res.append(entry)
    return res


def gate_agreement(A, B6, B5):
    d = os.path.join(OUT_DIRS['c2v006'], [n for n in sorted(os.listdir(OUT_DIRS['c2v006'])) if n.startswith('x01_')][0])
    gl, _err, rosters = load_build(A, d)
    variants = {
        'as_written_by_c2v006': dict(gl),
        'no_schema_(c2v005_form)': {k: v for k, v in gl.items() if k != 'schema'},
        'schema_GATE_STATUS_LIST_C4V002': dict(gl, schema='GATE_STATUS_LIST_C4V002'),
        'schema_lower_case': dict(gl, schema='gate_status_list_c4v001'),
        'schema_TSR_FLAG_RECORD_C4V001': dict(gl, schema='TSR_FLAG_RECORD_C4V001'),
        'schema_null': dict(gl, schema=None),
        'extra_key': dict(gl, builder='roster_builder_c2v006'),
        'schema_only_no_gates': {'schema': 'GATE_STATUS_LIST_C4V001'},
    }
    rows = []
    for name, v in variants.items():
        try:
            b6 = B6._a_gate_list_problem(v)
        except (KeyError, TypeError) as exc:
            b6 = 'EXCEPTION %s' % type(exc).__name__
        try:
            b5 = B5._a_gate_list_problem(v)
        except (KeyError, TypeError) as exc:
            b5 = 'EXCEPTION %s' % type(exc).__name__
        run = a_gate_check(A, v, rosters)
        a_ok = not any(k[0] == 'GATE_STATUS_LIST_DEFECT' for k in run.stops)
        rows.append({'variant': name, 'a_accepts': a_ok, 'c2v006_accepts': b6 is None, 'c2v005_accepts': b5 is None,
                     'c2v006_agrees_with_a': (b6 is None) == a_ok, 'c2v005_agrees_with_a': (b5 is None) == a_ok})
    return {'build': os.path.basename(d), 'rows': rows}


def a_tsr_check(A, rec_doc, rec_sha, load_err=None):
    """classifier A's own check_tsr on a flag record, with synthetic stand-ins for the other carriers it reads (from
    A's own constants: compare 6f095f64 with failing TRUNCATION_SHAPE ring 15 only, the support record's ring 15
    bounds, a manifest whose input_files pins the four shas)."""
    ring = {'ordinal': A.FAILING_RING_ORDINAL, 'classification': 'TRUNCATION_SHAPE', 'R_kpc': 10.4,
            'synthetic': True}
    compare = {'schema': 'NGC_NTEST_COMPARE_C2V002', 'failing_TRUNCATION_SHAPE_rings': [dict(ring)],
               'failing_non_TRUNCATION_SHAPE_rings': [], 'n_route_ab_gate': 'OPEN'}
    support = {'schema': 'UNT_ROOT_TSR_SUPPORT_CX3V001', 'mode': 'synthetic', 'target_free': True,
               'before_target_access': True, 'point_key': 'synthetic',
               'slots_pin': {'path': '/synthetic/slots.json', 'sha256': SYN_SHA},
               'ntest_compare_pin': {'path': '/synthetic/compare.json', 'sha256': A.COMPARE_SHA},
               'rule_id': 'synthetic',
               'rings': [{'native_ring': dict(ring), 'lower_kpc': A.SUPPORT_LOWER_KPC,
                          'upper_kpc': A.SUPPORT_UPPER_KPC, 'lower_inclusive': False, 'upper_inclusive': False}]}
    manifest = {'pins': {'input_files': [{'path': '/synthetic/%d.json' % i, 'sha256': s} for i, s in
                                         enumerate((A.COMPARE_SHA, A.N1_SHA, A.NODE_SHA, rec_sha))]}}
    run = A.Run('/synthetic/interface_proof_bundle.json')
    run.b = {'inputs': {'ntest_compare': {'path': '/synthetic/compare.json', 'sha256': A.COMPARE_SHA},
                        'tsr_flag_record': {'path': '/synthetic/flag.json', 'sha256': rec_sha}}}
    run.docs = {'ntest_compare': compare, 'tsr_flag_record': rec_doc, 'tsr_support_record': support,
                'freeze_manifest': manifest}
    run.load_err = {'tsr_flag_record': load_err}
    run.check_tsr()
    return run


def tsr_part(A, B6):
    out = {}
    v3_raw, v2_raw, v1_raw = read_pinned_bytes('tsr_v003'), read_pinned_bytes('tsr_v002'), read_pinned_bytes('tsr_v001')
    v3, v2 = A.strict_loads(v3_raw), A.strict_loads(v2_raw)
    out['c2v006_tsr_record_v003_on_V001_gives_V003_bytes'] = B6.tsr_record_v003(
        {'path': PINS['tsr_v001'][0], 'sha256': sha(v1_raw)}) == v3_raw
    out['V003_is_V002_plus_schema'] = v3 == dict(v2, schema='TSR_FLAG_RECORD_C4V001')
    rows = []
    variants = [('V003_as_written_by_c2v006_tsr_record', v3, PINS['tsr_v003'][1]),
                ('V002_c2v005_record_no_schema', v2, PINS['tsr_v002'][1])]
    for name, doc in (('V003_schema_UNT_ROOT_TSR_FLAG_RECORD_C2V001',
                       dict(v3, schema='UNT_ROOT_TSR_FLAG_RECORD_C2V001')),
                      ('V003_schema_lower_case', dict(v3, schema='tsr_flag_record_c4v001')),
                      ('V003_schema_null', dict(v3, schema=None)),
                      ('V003_extra_key_rule_id', dict(v3, rule_id='M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001'))):
        variants.append((name, doc, sha(json.dumps(doc, sort_keys=True).encode())))
    for name, doc, s in variants:
        run = a_tsr_check(A, doc, s)
        rows.append({'record': name, 'a_stops': stop_summary(run),
                     'a_tsr_flag_table_mismatch': any(k[0] == 'TSR_FLAG_TABLE_MISMATCH' for k in run.stops)})
    out['a_check_tsr'] = rows
    return out


def main(argv):
    if len(argv) != 2 or argv[0] != '--out':
        print(__doc__)
        return 2
    out_path = os.path.abspath(argv[1])
    A = load_module('classifier_a', 'classifier_a_c4v004_readonly')
    B6 = load_module('builder_c2v006', 'roster_builder_c2v006_readonly')
    B5 = load_module('builder_c2v005', 'roster_builder_c2v005_readonly')
    for k in ('test_record_c2v006_run1', 'test_record_c2v005_run1'):
        read_pinned_bytes(k)
    g6, g5 = gate_lists(A, 'c2v006'), gate_lists(A, 'c2v005')
    agree = gate_agreement(A, B6, B5)
    tsr = tsr_part(A, B6)
    by = {r['record']: r for r in tsr['a_check_tsr']}
    checks = {
        'G1_every_c2v006_list_accepted_by_A_no_stop_at_all': bool(g6) and all(not e['a_stops'] for e in g6),
        'G2_every_c2v006_list_echoed_by_A_as_the_list': bool(g6) and all(e['a_gate_list_out_is_the_list'] for e in g6),
        'G3_every_c2v005_list_refused_by_A_GATE_STATUS_LIST_DEFECT': bool(g5) and all(
            e['a_gate_list_defect'] for e in g5),
        'G4_every_c2v005_list_plus_schema_accepted_by_A_no_stop_at_all': bool(g5) and all(
            not e['with_schema_added_a_stops'] for e in g5),
        'G5_c2v006_checker_agrees_with_A_on_every_variant': all(r['c2v006_agrees_with_a'] for r in agree['rows']),
        'G6_c2v005_checker_disagrees_with_A_on_the_honest_and_c2v005_forms': [
            r['variant'] for r in agree['rows'] if not r['c2v005_agrees_with_a']] == [
            'as_written_by_c2v006', 'no_schema_(c2v005_form)'],
        'T1_c2v006_tsr_record_reproduces_V003': tsr['c2v006_tsr_record_v003_on_V001_gives_V003_bytes'],
        'T2_V003_is_V002_plus_schema': tsr['V003_is_V002_plus_schema'],
        'T3_V003_accepted_by_A_no_stop_at_all': by['V003_as_written_by_c2v006_tsr_record']['a_stops'] == [],
        'T4_V002_refused_by_A_TSR_FLAG_TABLE_MISMATCH': by['V002_c2v005_record_no_schema']['a_tsr_flag_table_mismatch'],
        'T5_V003_variants_refused_by_A': all(r['a_tsr_flag_table_mismatch'] for r in tsr['a_check_tsr'][2:]),
    }
    record = {'schema': 'INTERFACE_PROOF_RUNBOOK_V002_C2V006',
              'pins': {k: {'path': v[0], 'sha256': v[1]} for k, v in sorted(PINS.items())},
              'proof_script': pin_of(os.path.realpath(__file__)), 'python': sys.version.split()[0],
              'gate_lists_c2v006_run1': g6, 'gate_lists_c2v005_run1': g5, 'gate_list_agreement': agree,
              'tsr_flag_record': tsr, 'checks': checks,
              'verdict': 'PASS' if all(v is True for v in checks.values()) else 'FAIL',
              'n_lists': {'c2v006': len(g6), 'c2v005': len(g5)}}
    raw = (json.dumps(record, indent=1, sort_keys=True) + '\n').encode()
    with open(out_path, 'xb') as f:
        f.write(raw)
    print(json.dumps({'verdict': record['verdict'], 'checks': checks, 'n_lists': record['n_lists'],
                      'sha256': sha(raw)}, indent=1))
    return 0 if record['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
