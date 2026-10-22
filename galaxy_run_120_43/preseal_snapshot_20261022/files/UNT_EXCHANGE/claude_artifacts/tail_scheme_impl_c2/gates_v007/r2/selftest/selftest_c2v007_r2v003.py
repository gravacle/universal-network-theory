"""c2v007 selftest driver (Claude2 gates_v007).  Synthetic trees only; no real run is read.
Runs every suite as its own process (python3 -I -B, single-thread BLAS) under each driver selection r4 and r5, parses each harness's
own results file, and judges EVERY row against the c2v007 expectation table expect_c2v007.json (selftest/):
  MUST_PASS   verdict PASS_BITWISE_EQUAL;
  MUST_FAIL   verdict FAIL and EVERY listed owner check failing, and no COMPARATOR_EXCEPTION unless listed: a MUST_FAIL that fails
              for an unrelated reason is a selftest FAIL (Codex2 0447 S2 / selftest_audit SHOULD_FIX);
  MUST_REFUSE no report and a refusal naming the listed reason (or, for subprocess suites, a non-zero exit with no report);
  UNIT_TRUE   the unit predicate holds.
Each table row carries the c2v006 expectation and, where c2v007 changes it, the reason code (BUILD.md lists the codes).
Suites: A (Codex2 c2v005 review: whole-gate 9 + duplicate NPZ 2), B (Codex2 c2v005 review: structural 23, invocation 24), CD (c2v006 own
canaries C+D 75), X (Codex2 c2v006 review: counterexamples whole-gate 20, structural 25, invocation 24; source-audit probes 9 + ledger 4;
A73 probe 47 predicates), K (the c2v006 workflow's checker CK002: 69 canaries + 5 SF regressions), E (own c2v007 canaries and units),
S (driver-process units: N6 checker tool, A71 inventory, source checks).
  python3 -I -B selftest_c2v007.py --comparator C --ported DIR --fill FILL --out DIR [--observe]
"""
import argparse
import ast
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
HERE = Path(__file__).resolve().parent
G7 = HERE.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd, env_extra, log, timeout=3600):
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    env.update(env_extra)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = 'TIMEOUT', str(e.stdout)[-2000:], str(e.stderr)[-2000:]
    with open(log, 'x') as f:
        f.write('$ %s\n--- rc %s\n--- stdout\n%s\n--- stderr\n%s\n' % (' '.join(cmd), rc, so[-60000:], se[-20000:]))
    return rc


def jl(p):
    return json.loads(Path(p).read_bytes())


def rows_whole(path):  # Codex2 whole-gate harnesses (RESULTS.json rows: name, actual_pass, failing)
    out = []
    for r in jl(path)['rows']:
        rp = (r.get('report') or {}).get('path')
        rep = jl(rp) if rp and Path(rp).is_file() else {}
        out.append({'case': r['name'], 'verdict': rep.get('verdict', 'NO_REPORT'), 'failing': rep.get('failing') or [], 'report': rp})
    return out


def rows_struct(path):
    return [{'case': r['case'], 'verdict': r.get('verdict') or 'NO_REPORT', 'failing': r.get('failing') or [],
             'exception': (r.get('exception') or {}).get('message') if isinstance(r.get('exception'), dict) else r.get('exception')}
            for r in jl(path)['cases']]


def rows_inv(path):
    return [{'case': r['name'], 'verdict': r.get('actual') or 'NO_REPORT', 'failing': r.get('failing') or [], 'exception': r.get('exception')}
            for r in jl(path)['rows']]


def rows_cd(path):
    return [{'case': r['case'], 'verdict': r['verdict'], 'failing': r.get('failing') or [], 'exception': r.get('exception')} for r in jl(path)['rows']]


def rows_a71(path):
    j = jl(path)
    out = [{'case': r['name'], 'verdict': r.get('actual'), 'failing': r.get('failing') or [], 'exception': r.get('exception')} for r in j['rows']]
    out += [{'case': 'UNIT_' + u['name'], 'unit_value': u['pass'], 'detail': u.get('detail')} for u in j['unit_observations']]
    return out


def rows_ledger(path):
    return [{'case': r['case'], 'verdict': r['verdict'], 'failing': r.get('failing') or []} for r in jl(path)['rows']]


def rows_a73(path):
    return [{'case': '%s %s' % (r['item'], r['name']), 'unit_value': r['pass'], 'detail': r.get('detail')} for r in jl(path)['rows']]


def rows_ck(path):
    out = []
    for r in jl(path)['rows']:
        lg = Path(path).parent / r['case'] / 'RUN.log'
        tail = lg.read_text(errors='replace')[-1500:] if lg.is_file() else ''
        out.append({'case': r['case'], 'verdict': r.get('verdict'), 'failing': r.get('failing') or [], 'exception': tail})
    return out


def rows_e(path):
    return [dict(r, case=r['case']) for r in jl(path)['rows']]


def judge(row, exp):
    """True when the observed row meets the c2v007 expectation."""
    kind = exp['expect']
    v, f = row.get('verdict'), set(row.get('failing') or [])
    if kind == 'MUST_PASS':
        return v == 'PASS_BITWISE_EQUAL' and not f
    if kind == 'MUST_FAIL':
        own = set(exp.get('owners') or [])
        if exp.get('only') is not None and sorted(f) != sorted(exp['only']):
            return False
        return v == 'FAIL' and bool(own) and own <= f and ('COMPARATOR_EXCEPTION' not in f or 'COMPARATOR_EXCEPTION' in own)
    if kind == 'MUST_REFUSE':
        return v in ('REFUSED', 'NO_REPORT', None) and (exp.get('refuse') is None or exp['refuse'] in str(row.get('exception') or ''))
    if kind == 'MUST_NOT_PASS':
        return v != 'PASS_BITWISE_EQUAL'
    if kind == 'UNIT_TRUE':
        return row.get('unit_value') is True
    if kind == 'UNIT_FALSE':
        return row.get('unit_value') is False
    return False


def s2_fault_probes():
    import types
    source = Path(__file__).read_bytes()
    fn = next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    start = next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='roster' for t in n.targets))
    end = next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rep' for t in n.targets))
    code = compile(ast.fix_missing_locations(ast.Module(body=fn.body[start:end],type_ignores=[])),str(__file__),'exec')
    roster={'OWN|r5':{'one':{'expect':'MUST_PASS'},'two':{'expect':'MUST_FAIL','owners':['RA_IDENTITY']}}}
    result=[]
    for name in ('positive','contradictory_pass','omitted','duplicate','child_exit1','timeout','missing_suite','extra_suite','wrong_owner','exception','empty'):
        obs={('OWN','r5'):{'rc':0,'rows':[{'case':'one','verdict':'PASS_BITWISE_EQUAL','failing':[]},{'case':'two','verdict':'FAIL','failing':['RA_IDENTITY']}]}}
        o=obs[('OWN','r5')]
        if name=='contradictory_pass':o['rows'][0]['failing']=['RESULT']
        if name=='omitted':o['rows'].pop()
        if name=='duplicate':o['rows'][1]=dict(o['rows'][0])
        if name=='child_exit1':o['rc']=1
        if name=='timeout':o['rc']='TIMEOUT'
        if name=='missing_suite':obs.clear()
        if name=='extra_suite':obs[('OTHER','r5')]=o
        if name=='wrong_owner':o['rows'][1]['failing']=['RESULT']
        if name=='exception':o['rows'][1]['failing']=['RA_IDENTITY','COMPARATOR_EXCEPTION']
        if name=='empty':o['rows']=[]
        env=dict(obs=obs,units={},judge=judge,sha=lambda p:'same',C='inert',S='same',a=types.SimpleNamespace(observe=False),HERE=HERE,jl=lambda p:{'suites':roster},want=lambda x:True)
        exec(code,env)
        want_v='PASS' if name=='positive' else 'FAIL'
        result.append({'case':name,'expect':'MUST_PASS' if name=='positive' else 'MUST_FAIL','actual':env['verdict'],'ok':env['verdict']==want_v})
    return {'value':all(r['ok'] for r in result),'detail':result}


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--comparator', required=True)
    ap.add_argument('--ported', required=True)
    ap.add_argument('--fill', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--observe', action='store_true')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    C = str(Path(a.comparator).resolve())
    S = sha(C)
    P = Path(a.ported).resolve()
    port_rec = jl(P / 'PORT_C2V007.json')
    for name, v in port_rec['ported'].items():
        if sha(P / name) != v['port_sha256']:
            raise SystemExit('ported file changed since porting: %s' % name)
    FIX = P / 'invocation_canaries_cx2v003_port_c2v007.py'
    FS = sha(FIX)
    EXPECT = jl(HERE / 'expect_c2v007.json') if not a.observe else {}
    env0 = {'C2V007_CMP': C, 'C2V007_CMP_SHA': S, 'C2V007_FILL_SHA': sha(a.fill)}
    obs = {}
    only = set(x for x in a.only.split(',') if x)
    if only - {'A','B','CD','X','K','E','S'}: raise SystemExit('UNKNOWN_SUITE')

    def want(s):
        return not only or s in only
    for drv in ('r4', 'r5'):
        e = dict(env0, C2V007_DRIVER=drv)
        if want('A'):
            for tag, script in (('A_whole_gate', 'test_whole_gate_edge_cases_cx2v001_port_c2v007.py'), ('A_duplicate_npz', 'test_duplicate_npz_members_cx2v001_port_c2v007.py')):
                d = out / ('%s_%s' % (tag, drv))
                rc = run([PY, '-I', '-B', str(P / script), C, S, str(d), drv], e, str(out / ('%s_%s.log' % (tag, drv))))
                obs[(tag, drv)] = {'rc': rc, 'rows': rows_whole(d / 'RESULTS.json') if (d / 'RESULTS.json').is_file() else []}
        if want('B'):
            d = out / ('B_structural_%s' % drv)
            d.mkdir()
            rc = run([PY, '-I', '-B', str(P / 'run_structural_canaries_cx2v002_port_c2v007.py'), '--comparator', C, '--sha256', S, '--driver', drv],
                     dict(e, C2V007_PORT_OUT=str(d)), str(out / ('B_structural_%s.log' % drv)))
            rs = sorted(d.glob('run_*/STRUCTURAL_RESULTS.json'))
            obs[('B_structural', drv)] = {'rc': rc, 'rows': rows_struct(rs[-1]) if rs else []}
            d = out / ('B_invocation_%s' % drv)
            rc = run([PY, '-I', '-B', str(P / 'invocation_canaries_cx2v003_port_c2v007.py'), '--comparator', C, '--sha256', S, '--out', str(d), '--driver', drv],
                     e, str(out / ('B_invocation_%s.log' % drv)))
            obs[('B_invocation', drv)] = {'rc': rc, 'rows': rows_inv(d / 'RESULT.json') if (d / 'RESULT.json').is_file() else []}
        if want('CD'):
            d = out / ('CD_canaries_c2v006_%s' % drv)
            rc = run([PY, '-I', '-B', str(P / 'canaries_c2v006_port_c2v007.py'), '--comparator', C, '--sha256', S, '--driver', drv, '--out', str(d)],
                     e, str(out / ('CD_canaries_c2v006_%s.log' % drv)))
            obs[('CD', drv)] = {'rc': rc, 'rows': rows_cd(d / 'CANARIES_C2V006.json') if (d / 'CANARIES_C2V006.json').is_file() else []}
        if want('X'):
            d = out / ('X_whole_gate_%s' % drv)
            d.mkdir()
            rc = run([PY, '-I', '-B', str(P / 'test_whole_gate_counterexamples_cx2v002_port_c2v007.py'), '--driver', drv],
                     dict(e, C2V007_PORT_OUT=str(d)), str(out / ('X_whole_gate_%s.log' % drv)))
            rj = d / ('whole_gate_%s_v001' % drv) / 'RESULTS.json'
            obs[('X_whole_gate', drv)] = {'rc': rc, 'rows': rows_whole(rj) if rj.is_file() else []}
            d = out / ('X_structural_%s' % drv)
            d.mkdir()
            rc = run([PY, '-I', '-B', str(P / 'run_structural_canaries_cx2v003_port_c2v007.py'), '--comparator', C, '--sha256', S, '--driver', drv],
                     dict(e, C2V007_PORT_OUT=str(d)), str(out / ('X_structural_%s.log' % drv)))
            rs = sorted(d.glob('run_*/STRUCTURAL_RESULTS.json'))
            obs[('X_structural', drv)] = {'rc': rc, 'rows': rows_struct(rs[-1]) if rs else []}
            d = out / ('X_invocation_%s' % drv)
            d.mkdir()
            rc = run([PY, '-I', '-B', str(P / 'invocation_canaries_cx2v004_port_c2v007.py'), '--comparator', C, '--sha256', S, '--out', str(d / 'run'), '--driver', drv],
                     dict(e, C2V007_PORT_OUT=str(d)), str(out / ('X_invocation_%s.log' % drv)))
            obs[('X_invocation', drv)] = {'rc': rc, 'rows': rows_inv(d / 'run/RESULT.json') if (d / 'run/RESULT.json').is_file() else []}
            d = out / ('X_a71_probes_%s' % drv)
            rc = run([PY, '-I', '-B', str(P / 'probe_a71_store_cx2v001_port_c2v007.py'), '--date-u', 'selftest', '--out', str(d)], e,
                     str(out / ('X_a71_probes_%s.log' % drv)))
            obs[('X_a71_probes', drv)] = {'rc': rc, 'rows': rows_a71(d / 'RESULTS_CX2V001.json') if (d / 'RESULTS_CX2V001.json').is_file() else []}
            d = out / ('X_ledger_%s' % drv)
            d.mkdir()
            rc = run([PY, '-I', '-B', str(P / 'probe_ledger_alias_cx2v001_port_c2v007.py'), '--date-u', 'selftest'], dict(e, C2V007_PORT_OUT=str(d)),
                     str(out / ('X_ledger_%s.log' % drv)))
            rj = d / 'ledger_v001/RESULTS_LEDGER_CX2V001.json'
            obs[('X_ledger', drv)] = {'rc': rc, 'rows': rows_ledger(rj) if rj.is_file() else []}
        if want('E'):
            d = out / ('E_canaries_c2v007_%s' % drv)
            rc = run([PY, '-I', '-B', str(HERE / 'canaries_c2v007_r2v002.py'), '--comparator', C, '--sha256', S, '--fixture', str(FIX), '--fixture-sha256', FS,
                      '--fill', a.fill, '--driver', drv, '--out', str(d)], e, str(out / ('E_canaries_c2v007_%s.log' % drv)))
            obs[('E', drv)] = {'rc': rc, 'rows': rows_e(d / 'CANARIES_C2V007.json') if (d / 'CANARIES_C2V007.json').is_file() else []}
    if want('X'):
        d = out / 'X_a73'
        d.mkdir()
        rc = run([PY, '-I', '-B', str(P / 'probe_a73_cx2v001_port_c2v007.py')], dict(env0, C2V007_PORT_OUT=str(d)), str(out / 'X_a73.log'))
        rs = sorted(d.glob('run_*/A73_RESULTS.json'))
        obs[('X_a73', 'r4r5')] = {'rc': rc, 'rows': rows_a73(rs[-1]) if rs else []}
    if want('K'):
        for tag, script in (('K_ck002', 'canaries_c2v006_ck002_port_c2v007.py'), ('K_regress', 'regress_ck001_sf_ck002_port_c2v007.py')):
            d = out / tag
            rc = run([PY, '-I', '-B', str(P / script), 'all', str(d)], env0, str(out / ('%s.log' % tag)), timeout=7200)
            for drv in ('r4', 'r5'):
                rj = sorted(glob.glob(str(d / drv / 'CANARIES_CK002_*.json')))
                obs[(tag, drv)] = {'rc': rc, 'rows': rows_ck(rj[-1]) if rj else []}
    # ---------------- S: driver-process units
    units = {}
    if want('S'):
        tool = G7 / 'tools/a71_inventory_c2v007.py'
        p = subprocess.run([PY, '-I', '-B', str(tool), '--comparator', C, '--check', '--out', str(out / 'A71_SITES_C2V007.json')], capture_output=True, text=True)
        units['S_a71_inventory_no_untagged_site'] = {'value': p.returncode == 0, 'detail': p.stdout.strip().splitlines()[-1] if p.stdout else p.stderr[-400:]}
        src = Path(C).read_text()
        tree = ast.parse(src)
        fn = {n.name: ast.get_source_segment(src, n) for n in tree.body if isinstance(n, ast.FunctionDef)}
        units['S_load_cm_and_driver_exec_hashed_bytes'] = {'value': all('exec(compile(raw' in fn[k] and 'spec_from_file_location' not in fn[k]
                                                                        for k in ('load_cm', 'load_driver')), 'detail': None}
        units['S_no_argparse_in_comparator'] = {'value': 'import argparse' not in src and 'ArgumentParser' not in src, 'detail': 'strict CLI (SF-ARGV)'}
        units['S_no_dollar_anchor_in_regexes'] = {'value': not any(isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.endswith('$')
                                                                   for n in ast.walk(tree) if isinstance(n, ast.Constant)), 'detail': 'fullmatch only (0446)'}
        units['S_no_backslash_d_in_regexes'] = {'value': '\\d' not in src, 'detail': 'ASCII [0-9] (CK002 N1)'}
        units['S_no_log_skip'] = {'value': 'LOG_NAMES' not in src, 'detail': 'no file is skipped by name (A76)'}
        # N6 checker tool on synthetic receipts and reports (subprocess; this process has no fixture hook)
        td = Path(tempfile.mkdtemp(dir=str(out), prefix='S_n6_'))
        n6 = G7 / 'tools/r5_gate_check_c2v007.py'
        res = {}
        good = {'schema': 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001', 'status': 'FINISHED', 'driver_status': 'COMPLETED', 'exit_code': 0, 'stop_reason': None,
                'retries': 0, 'pins': {'driver': {'sha256': 'd' * 64}}}
        var = {'GOOD': {}, 'FAILED_STATUS': {'status': 'FAILED'}, 'RUNNING': {'status': 'RUNNING'}, 'EXIT_1': {'exit_code': 1}, 'EXIT_TRUE': {'exit_code': True},
               'STOPPED': {'stop_reason': 'wall_cap'}, 'RETRIED': {'retries': 1}, 'WRONG_DRIVER': {'pins': {'driver': {'sha256': 'e' * 64}}}}
        for k, ch in var.items():
            (td / k).mkdir()
            (td / k / 'result.json').write_bytes(b'{"r": 1}')
            rc_ = dict(good, **ch)
            rc_['result'] = {'path': str(td / k / 'result.json'), 'sha256': hashlib.sha256(b'{"r": 1}').hexdigest()}
            (td / (k + '.receipt.json')).write_bytes(json.dumps(rc_).encode())
        (td / 'DUPKEY').mkdir()
        (td / 'DUPKEY.receipt.json').write_bytes(b'{"status": "FAILED", "status": "FINISHED"}')
        (td / 'MISSING').mkdir()
        (td / 'LINKED').mkdir()
        (td / 'LINKED.receipt.json').symlink_to(td / 'GOOD.receipt.json')
        for k in list(var) + ['DUPKEY', 'MISSING', 'LINKED']:
            res[k] = subprocess.run([PY, '-I', '-B', str(n6), 'receipts', '--ext', str(td), '--driver-sha', 'd' * 64, k], capture_output=True, text=True).returncode
        okrep = {'schema': 'RUN_IDENTITY_COMPARE_C2V007', 'gate': 'Z2', 'driver_selected': 'r5', 'verdict': 'PASS_BITWISE_EQUAL', 'failing': [],
                 'comparator': {'sha256': 'c' * 64}, 'comparator_sha256_at_end': 'c' * 64}
        (td / 'REP.json').write_bytes(json.dumps(okrep).encode())
        (td / 'BAD.json').write_bytes(json.dumps(dict(okrep, verdict='FAIL', failing=['RESULT'])).encode())
        (td / 'OTHERCMP.json').write_bytes(json.dumps(dict(okrep, comparator={'sha256': 'f' * 64})).encode())
        for k, item in (('V_GOOD', 'Z2=%s=0' % (td / 'REP.json')), ('V_FAIL', 'Z2=%s=0' % (td / 'BAD.json')), ('V_EXIT1', 'Z2=%s=1' % (td / 'REP.json')),
                        ('V_OTHER_COMPARATOR', 'Z2=%s=0' % (td / 'OTHERCMP.json')), ('V_WRONG_GATE', 'B0P_RERUN=%s=0' % (td / 'REP.json')),
                        ('V_MISSING', 'Z2=%s=0' % (td / 'NONE.json'))):
            res[k] = subprocess.run([PY, '-I', '-B', str(n6), 'verdicts', '--comparator-sha', 'c' * 64, '--driver', 'r5', item], capture_output=True, text=True).returncode
        wantrc = {k: (0 if k in ('GOOD', 'V_GOOD') else 1) for k in res}
        units['S_n6_receipt_and_verdict_checker'] = {'value': res == wantrc, 'detail': {'exit_codes': res, 'expected': wantrc}}
        # the R5 command script: order of checks (source; not run)
        sh = G7 / 'R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2.sh'
        txt = sh.read_text() if sh.is_file() else ''
        i_rc, i_cmp = txt.find('r5_gate_check_c2v007.py receipts'), txt.find('run_identity_compare_c2v007.py --gate')
        i_v, i_w = txt.find('r5_gate_check_c2v007.py verdicts'), txt.find('write_identity_records_c2v007_r2.py --driver')
        sc = {'present': bool(txt), 'receipts_before_any_comparison': 0 <= i_rc < i_cmp, 'verdicts_after_comparisons': i_cmp < i_v,
              'records_after_verdicts': i_v < i_w, 'each_pid_waited': txt.count('wait $') >= 3, 'nonzero_exit_on_failure': txt.count('exit 1') >= 3,
              'comparator_pinned': S in txt}
        units['S_n6_r5_command_script'] = {'value': all(sc.values()), 'detail': sc}
    if want('S'):
        units['S2_accounting_fault_probes'] = s2_fault_probes()
    # ---------------- judging; immutable expected case multiset, not observations as authority
    roster = jl(HERE / 'EXPECTED_CASES_R2_V002.json')['suites']
    table, breaches, counts = [], [], {}
    expected_suites = {k for k in roster if want(k.split('|')[0].split('_')[0])}
    actual_suites = {suite+'|'+drv for suite,drv in obs}
    if actual_suites != expected_suites:
        breaches.append({'kind':'SUITE_SET_DEFECT','missing':sorted(expected_suites-actual_suites),'extra':sorted(actual_suites-expected_suites)})
    for (suite,drv),o in obs.items():
        expected = roster.get(suite+'|'+drv,{})
        names = [r.get('case') for r in o['rows']]
        if len(names)!=len(set(names)) or set(names)!=set(expected):
            breaches.append({'kind':'CASE_MULTISET_DEFECT','suite':suite,'driver':drv,'missing':sorted(set(expected)-set(names)),'extra':sorted(set(names)-set(expected)),'duplicate':len(names)!=len(set(names))})
    for (suite, drv), o in sorted(obs.items()):
        for r in o['rows']:
            key = '%s|%s' % (suite, r['case'])
            exp = roster.get(suite+'|'+drv,{}).get(r['case'])
            if suite == 'E' and exp and exp['expect'] == 'UNIT_TRUE':
                ok = r.get('kind') == 'UNIT' and r.get('ok') is True
            else:
                ok = judge(r, exp) if exp else False
                if suite == 'E':
                    ok = ok and r.get('ok') is True and (r.get('extra_check') is None or r['extra_check'][0] is True)
            row = {'suite': suite, 'driver': drv, 'case': r['case'], 'verdict': r.get('verdict'), 'failing': r.get('failing'),
                   'unit_value': r.get('unit_value'), 'expectation': exp, 'ok': ok, 'exception':r.get('exception')}
            table.append(row)
            c = counts.setdefault(suite, {'n': 0, 'ok': 0})
            c['n'] += 1
            c['ok'] += bool(ok)
            if not ok:
                breaches.append({'suite': suite, 'driver': drv, 'case': r['case'], 'verdict': r.get('verdict'), 'failing': r.get('failing'),
                                 'unit_value': r.get('unit_value'), 'expectation': exp, 'exception': str(r.get('exception'))[:300]})
    for k, u in units.items():
        counts.setdefault('S', {'n': 0, 'ok': 0})
        counts['S']['n'] += 1
        counts['S']['ok'] += bool(u['value'])
        if not u['value']:
            breaches.append({'suite': 'S', 'case': k, 'detail': u['detail']})
    rc_bad = {'%s_%s' % k: v['rc'] for k, v in obs.items() if v['rc'] != 0 or not v['rows']}
    verdict = 'PASS' if not breaches and not rc_bad and sha(C) == S and not a.observe else ('OBSERVED' if a.observe else 'FAIL')
    rep = {'schema': 'SELFTEST_C2V007_V001', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'comparator': {'path': C, 'sha256': S, 'sha256_at_end': sha(C)}, 'harness': {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)},
           'case_roster': {'path':str(HERE/'EXPECTED_CASES_R2_V002.json'),'sha256':sha(HERE/'EXPECTED_CASES_R2_V002.json')},
           'expect_table': {'path': str(HERE / 'expect_c2v007.json'), 'sha256': sha(HERE / 'expect_c2v007.json') if (HERE / 'expect_c2v007.json').is_file() else None},
           'ported': {'dir': str(P), 'record_sha256': sha(P / 'PORT_C2V007.json')}, 'fixture_sha256': FS, 'fill_sha256': sha(a.fill),
           'counts': counts, 'units': units, 'suite_return_codes': {'%s_%s' % k: v['rc'] for k, v in obs.items()}, 'suites_with_bad_rc_or_no_rows': rc_bad,
           'breaches': breaches, 'rows': table, 'verdict': verdict}
    with open(out / 'SELFTEST_C2V007.json', 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({'verdict': verdict, 'counts': counts, 'n_breaches': len(breaches), 'bad_rc': rc_bad}, indent=1))

    return 0 if verdict == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
