"""Independent saved-only acceptance; root executes after natural closure.

No scientific implementation is imported, no history is propagated, and no
Hamiltonian, background, atomic or transfer equation is evaluated. Only
sealed metadata, saved-state differences and serialized transfer arithmetic
are checked. Pending final pins prohibit execution.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import time

BASE = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
PARENT = 'INVARIANT_CLOCK_JOINT_V003_RECOMBINATION_TRANSFER_V001'
STEM = PARENT + '_SAVED_AUDIT_V001'
SOURCE = BASE / 'invariant_clock_joint_v003_recombination_transfer_v001.py'
PROTOCOL = BASE / (PARENT + '.md')
RESULT = BASE / (PARENT + '_RESULT.json')
RECEIPT = BASE / (PARENT + '_RECEIPT.json')
CAL = BASE / 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
CP = BASE / (PARENT + '_CHECKPOINTS')
MANIFEST = BASE / (PARENT + '_MANIFEST.json')
JOURNAL = BASE / (PARENT + '_JOURNAL.jsonl')
OUT = BASE / (STEM + '.json')
MD = BASE / (STEM + '.md')
AUDIT_RECEIPT = BASE / (STEM + '_RECEIPT.json')
ERROR = BASE / (STEM + '_ERROR.json')
PINS = {
    SOURCE: 'cedbd2b46a07b8886b622976261b86e54015f43d7c7f54dd08122ca5823352a2',
    PROTOCOL: '57e38ca36b6adc2488cfa460f147aa04384b6899c4a500639afba14307820b87',
    CAL: 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f',
    RESULT: 'b4779aec64441f1729ecfbe037e378b9c0daf6d32bbef4639c083ede31be6ec1',
    RECEIPT: '60a13bf4ff8fc5cbf68c77c9eba9637fa300e4b8dade7a0ec5595abc18a0eb58',
}
TRIALS = [('COARSE', 4096, 16, 48, 1e-7, 'half', 1),
          ('FINE', 8192, 16, 48, 1e-7, 'half', 1),
          ('START', 8192, 16, 48, 5e-8, 'half', 1),
          ('HIERARCHY', 8192, 20, 64, 1e-7, 'half', 1),
          ('ATOMIC', 8192, 16, 48, 1e-7, 'default', 1),
          ('THIN', 8192, 16, 48, 1e-7, 'half', 2)]
COUNT = 0
MAX_SERIAL_ERROR = 0.
INPUTS = {}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def check(ok, name):
    global COUNT
    COUNT += 1
    if not ok:
        raise AssertionError(name)


def close(got, expected, name):
    global MAX_SERIAL_ERROR
    check(math.isfinite(got) and math.isfinite(expected), name + ': finite')
    error = abs(got - expected) / max(abs(got), abs(expected), 1e-30)
    MAX_SERIAL_ERROR = max(MAX_SERIAL_ERROR, error)
    check(error <= 1e-11, name + ': serialized arithmetic')


def finite(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            finite(value)
    elif isinstance(obj, list):
        for value in obj:
            finite(value)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        check(math.isfinite(obj), 'finite saved scalar')


def read(path):
    return json.loads(Path(path).read_text())


def atomic(path, obj, markdown=False):
    if path.exists():
        raise FileExistsError(str(path))
    tmp = path.with_name(path.name + '.TMP_' + str(os.getpid()))
    with tmp.open('x') as stream:
        stream.write(obj if markdown else json.dumps(obj, indent=2, allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    if path.exists():
        raise FileExistsError(str(path))
    os.rename(tmp, path)
    path.chmod(0o444)


def names(lg, ln):
    return ['Psi', 'db', 'V', 'F', 'Uc', 'B', 'Zh', 'dg', 'slip', 'dn', 'Un'] + [
        'fg' + str(l) for l in range(2, lg + 1)] + [
        'fn' + str(l) for l in range(2, ln + 1)] + [
        'pol' + str(l) for l in range(lg + 1)]


def saved_error(left, right, selected=None, endpoint=False):
    if selected is None:
        selected = [n for n in left['names'] if n in right['names'] and
                    not (left['dust'] and n in ('B', 'Zh'))]
    li = [left['names'].index(n) for n in selected]
    ri = [right['names'].index(n) for n in selected]
    aa, bb = left['snapshots'], right['snapshots']
    if not endpoint:
        check(len(aa) == len(bb), 'comparison snapshot census')
        for a, b in zip(aa, bb):
            close(a['a'], b['a'], 'paired saved epoch')
    values = {}
    for n, i, j in zip(selected, li, ri):
        scale = max(max(abs(b['state'][j]) for b in bb), 1e-30)
        delta = abs(aa[-1]['state'][i] - bb[-1]['state'][j]) if endpoint else max(
            abs(a['state'][i] - b['state'][j]) for a, b in zip(aa, bb))
        values[n] = delta / scale
    limiting = max(selected, key=lambda n: values[n])
    return dict(error=values[limiting], limiting_state=limiting, per_state=values)


def main():
    began = time.monotonic()
    for path, expected in PINS.items():
        check(sha(path) == expected, 'direct pin ' + path.name)
    result, receipt, cal = read(RESULT), read(RECEIPT), read(CAL)
    finite(result)
    expected_inputs = {}
    tree = ast.parse(SOURCE.read_text())
    direct = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in n.targets))
    check(len(direct) == 23 and len(cal['hashes']) == 18, 'complete direct/inherited census')
    for name, value in direct.items():
        expected_inputs[str(BASE / name)] = value
    expected_inputs.update({str(SOURCE): PINS[SOURCE], str(PROTOCOL): PINS[PROTOCOL]})
    for path, value in cal['hashes'].items():
        check(path not in expected_inputs or expected_inputs[path] == value, 'nonconflicting inherited pin')
        expected_inputs[path] = value
    check(result['input_sha256'] == receipt['input_sha256'] == expected_inputs, 'complete input map')
    INPUTS.update(expected_inputs)
    for path, value in INPUTS.items():
        check(sha(path) == value, 'actual input seal')
    check(result['source_sha256'] == receipt['source_sha256'] == PINS[SOURCE], 'source identity')
    check(result['protocol_sha256'] == receipt['protocol_sha256'] == PINS[PROTOCOL], 'protocol identity')
    check(result['gauss_function_span_sha256'] == '53faaa3ad155bae52ac092c3c072e3eb61f863402760a161478cff26b62af8d0', 'exact function custody')
    check(result['charged_helper_scope'] == 'Only exact gauss_step loaded; no legacy D0/calibration initialization', 'helper scope')
    check(result['fixed'] == cal['fixed'] and result['selected_calibration'] == cal['selected'], 'same complete calibration')
    check(result['k_Mpc_inverse'] == .01, 'fixed physical k')
    check(cal['all_controls_passed'] and len(cal['controls']) == 149 and cal['fitted_freedoms'] == 2, 'accepted parent calibration')
    check(all(c['passed'] for c in cal['controls']), 'every parent numerical control')
    normalization = []
    for row in cal['rows']:
        close(result['radiation_omega'], row['omega_radiation'], 'same measured-temperature radiation')
        for kind in ('default', 'half'):
            invocation = row['invocations'][kind]
            raw_path = BASE / invocation['output_path']
            check(sha(raw_path) == invocation['output_sha256'] == INPUTS[str(raw_path)], 'four final atomic history seals')
            raw = read(raw_path)
            check(raw['status'] == 'COMPLETE_ATOMIC_HISTORY_ONLY' and raw['zero_injection'], 'saved atomic scope')
            check(raw['omega_b'] == cal['selected']['physical_omega_b'] and raw['YHe_atomic'] == cal['selected']['YHe'] and raw['Hcal_km_s_Mpc'] == cal['selected']['Hunit'], 'same atomic tuple')
            normalization.append((raw['nH0_cm3'] * 1e6, 1 + 2 * raw['fHe']))
            if row['kind'] == 'CANDIDATE' and kind == 'half':
                close(result['high_z_join_relative_jump'], normalization[-1][1] / raw['rows'][-1][1] - 1, 'actual high-z join jump')
    check(len(set(normalization)) == 1, 'common four-history normalization')
    close(result['nH0_m_inverse3'], normalization[0][0], 'HYREC hydrogen normalization')
    close(result['fully_ionized_xe'], normalization[0][1], 'HYREC helium high-z extension')
    manifest = read(MANIFEST)
    check(manifest == dict(stem=PARENT, input_sha256=INPUTS, input_map_sha256=digest(INPUTS),
                           k_Mpc_inverse=.01, trials=[list(t) for t in TRIALS], seed=1e-5, end_a=1/801), 'manifest exact specification')
    check(receipt['manifest_sha256'] == sha(MANIFEST), 'manifest receipt pin')
    events = [json.loads(line) for line in JOURNAL.read_text().splitlines()]
    check(receipt['journal_sha256'] == sha(JOURNAL) and receipt['event_count'] == len(events), 'journal receipt')
    check(events[0]['stage'] == 'started' and events[-1]['stage'] == 'completed', 'natural completed journal')
    check(sum(e['stage'] == 'started' for e in events) == 1 and sum(e['stage'] == 'completed' for e in events) == 1, 'unique endpoints')
    for i, e in enumerate(events):
        check(e['index'] == i and e['pid'] > 0 and e['input_map_sha256'] == digest(INPUTS), 'journal identity')
        check(e['stage'] in ('started', 'resumed', 'trial_complete', 'completed'), 'journal allowed stage')
        check(e['previous_sha256'] == (digest(events[i-1]) if i else None), 'journal append chain')
    check(events[0]['manifest_sha256'] == sha(MANIFEST), 'initial start manifest')
    check(receipt['initial_pid'] == events[0]['pid'] and receipt['closing_pid'] == events[-1]['pid'], 'owner PIDs')
    trial_events = [e for e in events if e['stage'] == 'trial_complete']
    expected_files = {branch + '_' + t[0] + suffix for branch in ('KX', 'REF')
                      for t in TRIALS for suffix in ('.json', '.COMMIT.json')}
    check({p.name for p in CP.iterdir()} == expected_files, 'exact 24 committed checkpoint files')
    check(len(trial_events) == receipt['checkpoint_count'] == 12, '12 trial commits')
    actual_cp = {p.name: sha(p) for p in CP.iterdir()}
    check(result['checkpoint_sha256'] == actual_cp, 'complete payload/COMMIT seals')
    histories = {}
    astar = 1 / (1 + cal['rows'][0]['observables']['zstar'])
    for branch, dust in [('KX', False), ('REF', True)]:
        for trial, steps, lg, ln, ai, atomic_kind, thin in TRIALS:
            identity = dict(branch=branch, dust=dust, trial=trial, steps=steps, lg=lg, ln=ln,
                            ai=ai, atomic=atomic_kind, thin=thin, k_Mpc_inverse=.01,
                            seed=1e-5, visibility_a=astar, end_a=1/801)
            name = branch + '_' + trial
            payload, commit = read(CP/(name+'.json')), read(CP/(name+'.COMMIT.json'))
            check(set(payload) == {'identity', 'input_sha256', 'history'}, 'checkpoint envelope')
            check(payload['identity'] == identity and payload['input_sha256'] == INPUTS, 'full checkpoint source/spec')
            check(commit == dict(status='COMMITTED', filename=name+'.json', sha256=actual_cp[name+'.json'],
                                 identity=identity, input_map_sha256=digest(INPUTS)), 'COMMIT full schema')
            ee = [e for e in trial_events if e['name'] == name]
            check(len(ee) == 1 and ee[0]['sha256'] == actual_cp[name+'.json'] and ee[0]['commit_sha256'] == actual_cp[name+'.COMMIT.json'], 'unique journal commit')
            h = payload['history']; histories[branch, trial] = h
            finite(h)
            check(h['names'] == names(lg, ln) and h['lg'] == lg and h['ln'] == ln and h['steps'] == steps and h['ai'] == ai and h['dust'] == dust, 'history specification')
            ss = h['snapshots']
            check(len(ss) == (68 if trial == 'START' else 67), 'frozen snapshot census')
            check(all(a['a'] < b['a'] for a, b in zip(ss, ss[1:])), 'strict saved time order')
            close(ss[0]['a'], ai, 'initial age'); close(ss[-1]['a'], 1/801, 'final age')
            check(all(len(z['state']) == len(h['names']) for z in ss), 'full saved-state dimensions')
            check(all(set(z['transfer']) == {'monopole_plus_lapse', 'photon_velocity', 'baryon_velocity', 'Weyl', 'photon_quadrupole', 'polarization_source', 'baryon_density', 'clock_density'} for z in ss), 'all eight saved transfers')
            close(h['maximum_constraint'], max(z['constraint'] for z in ss), 'sampled constraint maximum')
    rows = result['rows']
    check([x['kind'] for x in rows] == ['KX', 'REF'], 'two ordered branches')
    expected_controls = {}
    for row, dust in zip(rows, [False, True]):
        branch = row['kind']; hh = {t[0]:histories[branch, t[0]] for t in TRIALS}
        check(row['dust'] == dust and row['k_Mpc_inverse'] == .01, 'row branch spec')
        common = [n for n in names(16,48) if n in names(16,48)[:11] or
                  (n.startswith(('fg','fn')) and int(n[2:]) <= 4) or
                  (n.startswith('pol') and int(n[3:]) <= 4)]
        if dust: common = [n for n in common if n not in ('B','Zh')]
        computed = dict(time=saved_error(hh['COARSE'],hh['FINE']),
                        start=saved_error(hh['FINE'],hh['START'],endpoint=True),
                        hierarchy=saved_error(hh['FINE'],hh['HIERARCHY'],common),
                        atomic=saved_error(hh['FINE'],hh['ATOMIC']),
                        interpolation=saved_error(hh['FINE'],hh['THIN']))
        check(set(row['errors']) == set(computed), 'five unchanged refinements')
        for tag, got in computed.items():
            saved=row['errors'][tag]; check(saved['limiting_state'] == got['limiting_state'], 'limiting full field')
            check(set(saved['per_state']) == set(got['per_state']), 'all compared fields')
            for key, value in got['per_state'].items(): close(saved['per_state'][key], value, 'per-state refinement')
            close(saved['error'], got['error'], 'refinement error');expected_controls[branch+'_'+tag]=(got['error'],1e-4)
        for t in TRIALS: expected_controls[branch+'_trajectory_constraint_'+t[0]]=(hh[t[0]]['maximum_constraint'],1e-6)
        for aa in (1e-7, 1/8001, astar, 1/801):
            for tag in ('constraint_identity_', 'physical_background_'): expected_controls[branch+'_'+tag+str(aa)]=(None,1e-10)
        for tag in ('radiation_tuple','physical_baryon_tuple'):expected_controls[('REFERENCE' if dust else 'CANDIDATE')+'_'+tag]=(None,1e-10)
        for key in ('linear_clock_margin_ratio','linear_spatial_ratio','cold_baryon_pressure_screen'):close(row[key],hh['FINE'][key],'descriptive diagnostic')
        for label,aa in [('visibility_peak',astar),('z800',1/801)]:check(row['selected'][label]==min(hh['FINE']['snapshots'],key=lambda z:abs(z['a']/aa-1)),'selected exact saved row')
    controls=result['controls'];check(len(controls)==len(expected_controls)==42 and result['check_count']==receipt['check_count']==42,'42 shared controls')
    check(len({c['name'] for c in controls})==42 and {c['name'] for c in controls}==set(expected_controls),'complete unique gate labels')
    for c in controls:
        error,tolerance=expected_controls[c['name']];check(c['tolerance']==tolerance,'unchanged acceptance threshold')
        check(c['error'] >= 0, 'nonnegative numerical error')
        check(c['passed']==(math.isfinite(c['error']) and c['error']<=tolerance),'exact pass disposition')
        if error is not None:close(c['error'],error,'direct saved-state gate')
    passed=all(c['passed'] for c in controls);status=('NUMERICALLY_QUALIFIED_' if passed else 'NUMERICALLY_UNQUALIFIED_')+'JOINT_V003_LINEAR_TRANSFER'
    check(result['status']==receipt['status']==events[-1]['status']==status,'qualification preserved')
    check(result['all_numerical_controls_passed']==receipt['all_numerical_controls_passed']==passed,'shared qualification flag')
    ca,hre=histories['KX','FINE'],histories['REF','FINE']
    targets=[('visibility_peak',astar),('z800',1/801)]+[(f'window_z{1/z["a"]-1:.3f}',z['a']) for z in ca['snapshots'] if 900<1/z['a']-1<1500 and abs(z['a']/astar-1)>1e-10]
    check([(c['epoch'],c['a']) for c in result['comparisons']]==targets,'complete epoch order/census')
    report_lines=[]
    def pick(branch,trial,aa):return min(histories[branch,trial]['snapshots'],key=lambda z:abs(z['a']/aa-1))['transfer']
    for q,(label,aa) in zip(result['comparisons'],targets):
        c,r=pick('KX','FINE',aa),pick('REF','FINE',aa);check(set(c)==set(r)==set(q['differences_per_curvature']),'all signed transfer fields')
        check(q['k_Mpc_inverse']==.01 and set(q['sensitivity_per_curvature'])=={'COARSE','START','HIERARCHY','ATOMIC','THIN'},'comparison arms')
        for n in c:
            close(q['candidate_per_curvature'][n],c[n]/1e-5,'candidate curvature normalization');close(q['reference_per_curvature'][n],r[n]/1e-5,'reference curvature normalization');delta=(c[n]-r[n])/1e-5;close(q['differences_per_curvature'][n],delta,'signed common-seed difference')
            for trial,ss in q['sensitivity_per_curvature'].items():
                cc,rr=pick('KX',trial,aa),pick('REF',trial,aa)
                close(ss['paired_difference_change'][n],(cc[n]-rr[n])/1e-5-delta,'paired refinement change');close(ss['candidate_transfer_change'][n],(cc[n]-c[n])/1e-5,'candidate refinement change');close(ss['reference_transfer_change'][n],(rr[n]-r[n])/1e-5,'reference refinement change')
            maximum=max(abs(ss['paired_difference_change'][n]) for ss in q['sensitivity_per_curvature'].values())
            report_lines.append(f'| {label} | {n} | {q["candidate_per_curvature"][n]:.12g} | {q["reference_per_curvature"][n]:.12g} | {delta:+.12g} | {maximum:.12g} |')
    parent_report=BASE/(PARENT+'_REPORT.md');text=parent_report.read_text()
    for line in report_lines:check(line in text,'every signed report row and max-refinement value')
    for row in rows:check('| '+row['kind']+' | '+' | '.join(f'{row["errors"][n]["error"]:.10g}' for n in ('time','start','hierarchy','atomic','interpolation'))+' |' in text,'report full numerical gates')
    check(receipt['result_sha256']==events[-1]['result_sha256']==sha(RESULT) and receipt['report_sha256']==events[-1]['report_sha256']==sha(parent_report),'final output receipt seals')
    check(events[-1]['check_count']==42,'final event control count')
    inherited=dict(old_recombination_76_of_76_at_different_Hunit=68.06502010698708,late_lensing_failed_gates=6,earlier_HYREC_scan_uncomputed=207,data_exposed=True,inherited_fitted_freedoms=2,additional_fitted_freedoms=0)
    check(result['inherited_qualifications']==receipt['inherited_qualifications']==inherited,'all prior successes/failures/exposure retained')
    old = read(BASE/'INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V002_RESULT.json')
    late = read(BASE/'INVARIANT_CLOCK_LATE_LENSING_V001_RESULT.json')
    panel = read(BASE/'hyrec_inputs_v001/HYREC_BAO_POINT10_PANEL_V001_RESULTS.json')
    partial = read(BASE/'hyrec_inputs_v001/HYREC_BAO_INTERVAL_SAVED_AUDIT_V003_RESULTS.json')
    check(len(old['controls']) == 76 and all(c['passed'] for c in old['controls']), 'actual old 76-control success')
    check(not late['all_numerical_controls_passed'] and sum(not c['passed'] for c in late['controls']) == 6, 'actual six late-lensing failures')
    known = set(partial['all125_summary']['cases']) | set(panel['copied_case_indices']) | set(panel['newly_scored_case_indices'])
    check(partial['histories'] == 335 and len(known) == 128 and 335 - len(known) == 207, 'actual unfinished scan count')
    check(not (BASE/(PARENT+'_ERROR.json')).exists(),'no producer ERROR')
    preserved={str(path):sha(path) for path in [*PINS,parent_report,MANIFEST,JOURNAL,*CP.iterdir()]}
    for path,value in INPUTS.items():check(sha(path)==value,'after-read input seal')
    audit=dict(status='SAVED_ONLY_ACCEPTANCE_PASSED',parent_status=status,parent_numerical_all_pass=passed,
               assertions=COUNT,max_serial_arithmetic_relative_error=MAX_SERIAL_ERROR,
               source_sha256=sha(Path(__file__)),input_sha256=INPUTS,parent_seals=preserved,
               branches=2,trial_count=12,checkpoint_files=24,controls=42,
               comparison_epochs=len(targets),signed_report_rows=len(report_lines),
               failed_parent_controls=[c['name'] for c in controls if not c['passed']],
               elapsed_seconds=time.monotonic()-began,
               scope='Independent saved-state difference/serialization acceptance; no equation evaluation, imports, atomic/calibration replay or trajectory propagation. Numerical qualification only; no observed CMB spectrum or likelihood.')
    note=f'# Independent saved-only joint V003 recombination acceptance\n\n{audit["status"]}; assertions {COUNT}; parent {status}.\n\nAll two branches, twelve trials, twenty-four payload/COMMIT files, forty-two frozen controls and {len(report_lines)} signed report rows retained. Maximum serialization error {MAX_SERIAL_ERROR:.12g}. All exact input/journal/output seals and old qualification/exposure records checked.\n\n{audit["scope"]}\n'
    atomic(OUT,audit);atomic(MD,note,markdown=True)
    rec=dict(status=audit['status'],assertions=COUNT,source_sha256=sha(Path(__file__)),result_sha256=sha(OUT),report_sha256=sha(MD),parent_status=status,parent_seals=preserved)
    atomic(AUDIT_RECEIPT,rec)
    for path,value in {**INPUTS,**preserved}.items():
        if sha(path)!=value:raise AssertionError('Post-output input changed: '+path)
    print(json.dumps(dict(status=audit['status'],assertions=COUNT,result_sha256=sha(OUT),receipt_sha256=sha(AUDIT_RECEIPT)),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if not args.execute:parser.error('Root authorization and --execute required; no output action')
    if any(value=='PENDING_NATURAL_CLOSURE' for value in PINS.values()):raise RuntimeError('Final natural-closure pins required before audit')
    for path in (OUT,MD,AUDIT_RECEIPT,ERROR):
        if path.exists():raise FileExistsError('Preserve existing audit evidence: '+str(path))
    try:main()
    except Exception as exc:
        atomic(ERROR,dict(status='AUDIT_INCOMPLETE',error=repr(exc),assertions=COUNT,source_sha256=sha(Path(__file__)),parent_pins={str(p):v for p,v in PINS.items()},input_sha256=INPUTS))
        raise
