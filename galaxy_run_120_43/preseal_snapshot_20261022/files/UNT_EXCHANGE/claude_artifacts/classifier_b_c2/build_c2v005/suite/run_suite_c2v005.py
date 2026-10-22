"""Run classifier B's own suite (c2v005; the c2v004 runner with the c2v005 library; c2v004 was the c2v003 runner with the c2v004 library; c2v003 was the c2v002 runner
with the c2v003 seams and library): build every case, run it twice, check hand specs and the schema.

usage: run_suite_c2v005.py --classifier CLS.py --schema SCHEMA.json --defs DEFS_MODULE_PATH --cases DIR --results OUT.json
Every file is created exclusively.  Cases are built once (into --cases); pass 1 and pass 2 each load a fresh
classifier module instance and must give byte-identical outputs.  Seam cases (see suite_lib) run in-process with
COMPARE_SHA / STAGE0_SUCCESSOR_SHA256 set to the synthetic stand-ins, and every case with PHASE1_TOOL_SHA256 set to
the suite's PHASE1_SEAM; each seam case is also run unpatched, where a score-mode
output must carry TSR_FLAG_TABLE_MISMATCH.  Unpatched cases are also run through the CLI in a subprocess, whose bytes
must equal the in-process bytes.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ABSENT = object()


def load_module(path, tag):
    spec = importlib.util.spec_from_file_location('clsb_' + tag, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def get(o, path):
    cur = o
    for seg in path.split('/'):
        try:
            if seg.startswith('R='):
                cur = next(r for r in cur['readings'] if r['reading'] == seg[2:])
            elif seg.startswith('A='):
                cur = next(a for a in cur['alternatives'] if a['name'] == seg[2:])
            elif seg.startswith('row='):
                cur = next(r for r in cur['rows'] if r['id'] == seg[4:])
            elif seg == '#codes':
                cur = sorted({s['code'] for s in cur['stops']})
            elif seg == '#details':
                cur = [d for s in cur['stops'] for d in s['detail']]
            elif isinstance(cur, list):
                cur = cur[int(seg)]
            else:
                cur = cur[seg]
        except (KeyError, IndexError, StopIteration, TypeError, ValueError):
            return ABSENT
    return cur


def check(o, exp, json_eq):
    fails = []
    for path, want in exp:
        got = get(o, path)
        if want == '#absent':
            ok = got is ABSENT
        elif isinstance(want, str) and want.startswith('has:'):
            needle = want[4:]
            ok = got is not ABSENT and (any(needle in x for x in got) if isinstance(got, list) and path.endswith('#details')
                                        else needle in got)
        else:
            ok = got is not ABSENT and json_eq(got, want)
        if not ok:
            fails.append({'path': path, 'want': want, 'got': '#absent' if got is ABSENT else got})
    return fails


def prefix_only(sha):
    return sha[:8] + ''.join('0' if ch != '0' else '1' for ch in sha[8:])


def run_case(mod, bundle, ctx, seam, seam_succ=True, p1_table=None):
    saved = (mod.COMPARE_SHA, mod.STAGE0_SUCCESSOR_SHA256, mod.PHASE1_TOOL_SHA256)
    try:
        if p1_table is not None:
            mod.PHASE1_TOOL_SHA256 = dict(p1_table)
        if seam:
            mod.COMPARE_SHA = ctx['compare_sha']
            if 'succ_sha' in ctx and seam_succ:
                mod.STAGE0_SUCCESSOR_SHA256 = (prefix_only(ctx['succ_sha']) if seam_succ == 'PREFIX_ONLY'
                                               else ctx['succ_sha'])
        return mod.classify_bundle(bundle)
    finally:
        mod.COMPARE_SHA, mod.STAGE0_SUCCESSOR_SHA256, mod.PHASE1_TOOL_SHA256 = saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--classifier', required=True)
    ap.add_argument('--schema', required=True)
    ap.add_argument('--defs', required=True)
    ap.add_argument('--cases', required=True)
    ap.add_argument('--results', required=True)
    ap.add_argument('--python', default=sys.executable)
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(a.defs)))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from jsonschema_mini_c2v001 import Validator, json_eq
    defs = load_module(a.defs, 'defs')
    import suite_lib_c2v005 as lib
    V = Validator(json.load(open(a.schema)))
    os.makedirs(a.cases, exist_ok=False)
    built = []
    for c in defs.CASES:
        s = lib.Spec(c['phase'], successor=c['successor'], mode=c['mode'])
        exp = c['fn'](s)
        d = os.path.join(a.cases, c['id'])
        bundle, ctx = s.build(d)
        with open(os.path.join(d, 'EXPECT_SPEC.json'), 'x') as f:
            json.dump({'id': c['id'], 'class': c['class'], 'clause': c['clause'], 'seam': c['seam'],
                       'seam_succ': c.get('seam_succ', True), 'p1_seam': c.get('p1_seam', True),
                       'expect': exp}, f, indent=1, sort_keys=True, default=str)
        built.append((c, exp, bundle, ctx))
    results = {'schema': 'CLASSIFIER_B_SUITE_RESULTS_C2V005', 'classifier': a.classifier,
               'retired': getattr(defs, 'RETIRED', {}),
               'classifier_sha256': hashlib.sha256(open(a.classifier, 'rb').read()).hexdigest(),
               'schema_file_sha256': hashlib.sha256(open(a.schema, 'rb').read()).hexdigest(),
               'defs_sha256': hashlib.sha256(open(a.defs, 'rb').read()).hexdigest(), 'cases': []}
    outs = {}
    for pass_no in (1, 2):
        mod = load_module(a.classifier, 'pass%d' % pass_no)
        for c, exp, bundle, ctx in built:
            out = run_case(mod, bundle, ctx, c['seam'], c.get('seam_succ', True),
                           lib.PHASE1_SEAM if c.get('p1_seam', True) else None)
            outs.setdefault(c['id'], []).append(out)
            if pass_no == 1:
                with open(os.path.join(os.path.dirname(bundle), 'OUTPUT.json'), 'xb') as f:
                    f.write(out)
    mod = load_module(a.classifier, 'unpatched')
    n_ok = 0
    for c, exp, bundle, ctx in built:
        o1, o2 = outs[c['id']]
        o = json.loads(o1)
        errs = V.errors(o)
        fails = check(o, exp, json_eq)
        rec = {'id': c['id'], 'class': c['class'], 'clause': c['clause'], 'seam': c['seam'],
               'output_sha256': hashlib.sha256(o1).hexdigest(), 'pass2_byte_equal': o1 == o2,
               'schema_errors': errs[:5], 'spec_failures': fails}
        unp = run_case(mod, bundle, ctx, False)
        out_path = os.path.join(os.path.dirname(bundle), 'OUTPUT_CLI_UNPATCHED.json')
        p = subprocess.run([a.python, '-I', '-B', a.classifier, bundle, out_path], capture_output=True)
        rec['cli_exit'] = p.returncode
        rec['cli_byte_equal'] = p.returncode == 0 and open(out_path, 'rb').read() == unp
        if c['seam']:
            ou = json.loads(unp)
            if ou.get('mode') == 'score' and 'stops' in ou:
                rec['unpatched_tsr_stop'] = any(s['code'] == 'TSR_FLAG_TABLE_MISMATCH' for s in ou['stops'])
            elif ou.get('mode') == 'prescore' and 'stops' in ou:
                rec['unpatched_tsr_stop'] = any(s['code'] == 'TSR_FLAG_TABLE_MISMATCH' for s in ou['stops'])
            else:
                rec['unpatched_tsr_stop'] = 'n/a (%s)' % (ou.get('status') or ou.get('reason'))
        ok = (rec['pass2_byte_equal'] and not errs and not fails and rec.get('unpatched_tsr_stop', True) is not False
              and rec.get('cli_byte_equal', True))
        rec['pass'] = ok
        n_ok += ok
        results['cases'].append(rec)
    results['n_cases'] = len(built)
    results['n_pass'] = n_ok
    with open(a.results, 'x') as f:
        json.dump(results, f, indent=1, sort_keys=True, default=str)
    print('cases %d pass %d' % (len(built), n_ok))
    for r in results['cases']:
        if not r['pass']:
            print('FAIL', r['id'], json.dumps({k: r[k] for k in r if k in ('schema_errors', 'spec_failures',
                                                                           'pass2_byte_equal', 'unpatched_tsr_stop',
                                                                           'cli_byte_equal')}, default=str)[:1500])


if __name__ == '__main__':
    main()
