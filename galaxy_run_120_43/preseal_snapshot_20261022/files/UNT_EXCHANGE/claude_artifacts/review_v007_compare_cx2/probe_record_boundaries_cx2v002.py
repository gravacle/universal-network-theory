"""Raw synthetic record and blinded-mode probes; no scientific data or launches.
nice unavailable (sandbox); 0514 waiver
"""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
setup_source = (HERE / 'probe_compare_r5_cx2v001.py').read_bytes()
setup_tree = ast.parse(setup_source)
prefix = []
for node in setup_tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CHECKS' for t in node.targets):
        break
    prefix.append(node)
exec(compile(ast.Module(body=prefix, type_ignores=[]), str(HERE / 'probe_compare_r5_cx2v001.py') + ':setup_only', 'exec'))
for name in ('world', 'gate_eval', 'evaluate'):
    node = next(n for n in setup_tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(HERE / 'probe_compare_r5_cx2v001.py') + ':' + name, 'exec'))
V5 = ROOT / 'kmax_prereg_v005_c2/kmax_compare_c2v005.py'
INPUTS.append(V5)
ctx['C5M'] = load_source(V5, 'v005_source_adapter_review')
FIXOUT = HERE / 'synthetic_record_boundaries_v001'
FIXOUT.mkdir()
FILES = {}
def write_json(path, obj):
    raw = (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as out:
        out.write(raw)
    FILES[str(path)] = hashlib.sha256(raw).hexdigest()
    return FILES[str(path)]

raw_results = []
for attack in ('clean', 'duplicate_early_row', 'unknown_early_row', 'duplicate_last_row', 'missing_early_id', 'nonfinite_early_id'):
    R, IDR = world()
    original = R['C6T']
    raw = copy.deepcopy(original['result'])
    raw['rows'] = [{'id': i, 'speed_km_s': original['adapted']['rows'][i]} for i in ids]
    raw['passes'] = [{'pass': j+1, 'max_abs_change_km_s': .0005,
                      'rows': [{'id': i, 'speed_km_s': row[i]} for i in ids]} for j, row in enumerate(original['pass_rows'])]
    raw['identity'] = {'route_a': {'custody': {'identity_sha256': original['adapted']['route_a_identity_sha256']}}}
    raw['final_pass'] = len(raw['passes'])
    if attack.startswith('duplicate'):
        j = -1 if attack == 'duplicate_last_row' else 0
        raw['passes'][j]['rows'].insert(0, {'id': ids[0], 'speed_km_s': 999.})
    if attack == 'unknown_early_row':
        raw['passes'][0]['rows'].append({'id': 'UNKNOWN_SYNTHETIC', 'speed_km_s': 999.})
    if attack == 'missing_early_id':
        raw['passes'][0]['rows'].pop(0)
    if attack == 'nonfinite_early_id':
        raw['passes'][0]['rows'][0]['speed_km_s'] = None
    d = FIXOUT / attack
    d.mkdir()
    attempt = d / 'synthetic_attempt.json'
    apsha = write_json(attempt, {'result': {'uv_tail': original['uvt_record']}})
    raw['route_a_outcome'].update(result_path=str(attempt), result_sha256=apsha)
    rp = d / 'result.json'
    sha = write_json(rp, raw)
    write_json(d / 'finish.json', {'result_sha256': sha})
    write_json(d / 'start.json', {'normalized_spec': raw['normalized_spec']})
    write_json(Path(str(d) + '.receipt.json'), f['receipt_for'](sha, str(rp), raw['call_spec_sha256'], raw['driver_sha256']))
    run = M.read_run('C6T', d, ctx)
    R['C6T'] = run
    ev, _ = evaluate(R, IDR)
    raw_results.append({'attack': attack, 'reading': ev['decision']['outcome'], 'run_unreadable': run.get('unreadable'),
                        'read_codes': run.get('read_codes'), 'gap': run.get('pass_rows_gap'),
                        'valid_all': ev['validity']['C6T']['valid_all'],
                        'T1_H_status': (ev.get('tests') or {}).get('T1_H', {}).get('status')})

blind_results = []
for canary in ('SPEED612345678', 'SPEED61_2345678', 'SPEED61.2345678', 'SPEED6e7'):
    R, IDR = world()
    records = f['complete_records'](R, IDR, b0_c5h=True)
    records['EPS']['verdict'] = canary
    g = gate_eval(records, R, IDR)['EPS']
    rendered = json.dumps(M.blinded_gate(g), sort_keys=True)
    blind_results.append({'mode': 'gates-only serializer', 'canary': canary, 'leaked': canary in rendered, 'output': rendered})
    run = {'result': {'status': 'REFUSED', 'reasons': [canary]}, 'receipt': {}, 'spec_for_reading': {}}
    failure = M.classify_failure(run, ctx)
    v = {'label': 'C4T', 'present': True, 'valid_all': False, 'failed': ['V1'], 'reading': failure['class'],
         'V1_codes': failure['codes'], 'ro1': {}, 'uvt': {}}
    rendered = json.dumps(M.blinded_case(v), sort_keys=True)
    blind_results.append({'mode': 'validity-only serializer', 'canary': canary, 'leaked': canary in rendered, 'output': rendered})

report = {'schema': 'UNT_CX2_COMPARE_R5_BOUNDARY_PROBES_V001', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
          'priority_note': 'nice unavailable (sandbox); 0514 waiver', 'source_pins': PINS,
          'setup_script_sha256': hashlib.sha256(setup_source).hexdigest(), 'raw_reader_observations': raw_results,
          'blinding_observations': blind_results, 'synthetic_files': FILES,
          'max_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'source_stable_end': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() == s for p,s in PINS.items()},
          'limitations': ['Full scientific CLI not invoked; raw read_run and exact blinded serializers exercised',
                          'Packet V4/V5 are fixture assertions; actual scientific packet checks not executed'],
          'research_files_read': sorted(set(READS))}
write_json(HERE / 'BOUNDARY_RESULTS_CX2V001.json', report)
print(json.dumps({'raw_reader_observations': raw_results,
                  'leaks': [{'mode': x['mode'], 'canary': x['canary']} for x in blind_results if x['leaked']],
                  'max_rss_bytes_macos': report['max_rss_bytes_macos']}))
