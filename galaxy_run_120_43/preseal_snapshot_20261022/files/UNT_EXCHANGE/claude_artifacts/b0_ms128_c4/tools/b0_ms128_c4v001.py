"""Claude4 RI-31 (A113, dispatch 0650) harness b0_ms128_c4v001.  Gate B0 (A55 ruling 2, B0-EMPTY rule of A54): plan identity
of driver v010 r5 against r4 on the ten FILLED P128 / M_s 128 V007 specs of SPEC_REGISTRY_R5_MS128_CX1V004.json (c7023846).

Method of record: root's tail_scheme_impl_c2/driver_r5/gates/b0_r5_vs_r4_c2v001.py (857ccb8a), loaded INERT from its pinned
bytes (exec into a fresh module; its main() is never called).  declared_map, compare, apply, files and ENV are used unchanged.
Each dry run is ONE child process
    taskpolicy -b PY -I -B tools/run_fenced_c4st2.py DRIVER dry-run --spec SPEC --report-dir RD      (cwd = RD's parent)
with root's single-thread ENV, at most 4 children at once, inside the review fence tools/fence_c4v002.py (c993d34c; review
root = this folder; the runner fe904509 checks the fence sha and runs its selftests first).
Declared adaptations of root's main(), each forced by the fenced child:
  (1) the child is the fence runner under taskpolicy -b (root: plain driver under nice -n 10);
  (2) the runner appends one FENCE_C4ST2_SUMMARY line to stderr; the terminal stderr line used by the B0-EMPTY rule is the
      DRIVER's last stderr line: the last line of stderr.strip() after removing that trailing summary line (recorded apart);
  (3) the spec set is exactly the ten FILLED specs of c7023846 (not root's sets a-c), labelled by registry case;
  (4) task rule 4: a child that hits a fence refusal stops its spec (R5 is not run after a refused R4) and the spec is
      BLOCKED_FORBIDDEN_ACCESS (not counted, not passed); nothing is retried or worked around.
This parent installs its own audit-hook guard first: process creation only for the exact sanctioned child argvs; no delete;
no network; no write outside this folder; no open or listing of a run tree, a UVT_* component, the C5H name or
target/observed-velocity data.  It hashes pinned files, spawns the children, compares, and writes by exclusive create only.
usage: python3 -I -B b0_ms128_c4v001.py check|run STAMP        (STAMP = `date -u +%Y-%m-%dT%H:%M:%SZ` at launch)
"""
import concurrent.futures as cf
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
import types
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
HERE = Path(os.path.realpath(os.path.dirname(os.path.abspath(__file__))))
FOLDER = HERE.parent
OUT = FOLDER / 'out'
DRY = OUT / 'dry'
LOGS = OUT / 'logs'
RECORD = OUT / 'B0_R5_VS_R4_MS128_C4V001.json'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
LP = EX / 'v007_launch_packet_cx1'
B0_TOOL = (EX / 'tail_scheme_impl_c2/driver_r5/gates/b0_r5_vs_r4_c2v001.py', '857ccb8a49e11314c7534b1651bfd316b5eab156b2f26b8b148fea385ef4ce5c')
R5 = (EX / 'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
R4 = (EX / 'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py', 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b')
# map sha: pasted from shasum of the bytes (2026-10-19T03:13Z), re-verified here before and after declared_map reads it
MAP = (EX / 'tail_scheme_impl_c2/driver_r5/CASCADE_MAP_R5_C2V001.json', 'a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880')
REG = (LP / 'SPEC_REGISTRY_R5_MS128_CX1V004.json', 'c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90')
FENCE = (HERE / 'fence_c4v002.py', 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5')
RUNNER = (HERE / 'run_fenced_c4st2.py', 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25')
SEAL_TOOLS = EX / 'v007_final_prereg_c4/seal_tools_v004/tools'
FENCE_SRC = (SEAL_TOOLS / 'fence_c4v002.py', FENCE[1])
RUNNER_SRC = (SEAL_TOOLS / 'run_fenced_c4st2.py', RUNNER[1])
PROBE = HERE / 'fence_probe_c4v001.py'
BUILDS = (LP / 'BUILD_V007.md', LP / 'BUILD_V006.md', LP / 'BUILD_V005.md')
DRY_REC = (LP / 'DRY_R5_MS128_V004.json', 'ff60cd6b')  # prefix as dispatched; the full sha is taken from BUILD_V005's bytes
MAX_PROCS = 4
N_SPECS = 10
TASKPOLICY = '/usr/sbin/taskpolicy'
NICE = '/usr/bin/nice'
SUMMARY_PREFIX = 'FENCE_C4ST2_SUMMARY '
RUNNER_REFUSALS = ('REFUSED: the fence is not fence_c4v002', 'REFUSED: fence selftest failed', 'REFUSED: fence v002 exception probes failed')

# ----------------------------------------------------------------------------------------------- parent guard (audit hook)
RUNS_EXT = (
    '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
    '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
)
TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')
GUARD_BLOCKED = []
ALLOWED_ARGV = set()
SPAWNED = []
_F = str(FOLDER)
_PROC = {'os.system', 'os.exec', 'os.spawn', 'os.fork', 'os.forkpty', 'pty.spawn', 'os.startfile', 'os.kill', 'os.killpg',
         'signal.pthread_kill'}
_NET = {'socket.connect', 'socket.bind', 'socket.sendto', 'socket.sendmsg', 'socket.getaddrinfo', 'socket.gethostbyname',
        'urllib.Request', 'http.client.connect', 'ftplib.connect', 'smtplib.connect'}
_DEL = {'os.remove', 'os.rmdir', 'shutil.rmtree'}
_WRITE = {'os.mkdir': (0,), 'os.rename': (0, 1), 'os.symlink': (1,), 'os.link': (1,), 'os.truncate': (0,), 'os.chmod': (0,),
          'os.chown': (0,), 'os.utime': (0,), 'shutil.copyfile': (1,), 'shutil.copytree': (1,), 'shutil.move': (0, 1),
          'os.chflags': (0,), 'os.lchflags': (0,), 'os.setxattr': (0,), 'os.removexattr': (0,)}
_LIST = {'os.listdir', 'os.scandir', 'glob.glob', 'glob.glob/2'}


def _under(p, root):
    return p == root or p.startswith(root + os.sep)


def _p(x):
    if x is None or isinstance(x, int):
        return None
    if isinstance(x, bytes):
        return os.fsdecode(x)
    try:
        return os.fspath(x)
    except TypeError:
        return None


def _forbidden(p):
    lit = os.path.abspath(p)
    real = os.path.realpath(lit)
    if any(_under(q, r) for q in (lit, real) for r in RUNS_EXT):
        return 'real run tree'
    if _under(lit, _F) and _under(real, _F):
        return None  # my own outputs
    for q in (lit, real):
        low = q.casefold()
        parts = low.split(os.sep)
        if any(x.startswith('uvt_') for x in parts):
            base = q.split(os.sep)[-1]
            if not (base.startswith('uvt_') and base.endswith('.py') and not any(x.startswith('uvt_') for x in parts[:-1])):
                return 'UVT component'
        if 'kmax_a2f10_c5h_run_v001' in low:
            return 'C5H name'
        if any(w in low for w in TARGET_WORDS):
            return 'target word'
        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):
            return 'NGC3198 data'
    return None


def _inside(p):
    ap = os.path.abspath(p)
    real = os.path.join(os.path.realpath(os.path.dirname(ap)), os.path.basename(ap))
    return _under(ap, _F) and _under(real, _F)


def _refuse(ev, detail):
    GUARD_BLOCKED.append([ev, str(detail)[:400]])
    raise PermissionError('PARENT_GUARD_C4: %s %s' % (ev, detail))


def _hook(ev, args):
    if ev in ('subprocess.Popen', 'os.posix_spawn'):
        argv = tuple(str(a) for a in (args[1] or ()))
        if argv not in ALLOWED_ARGV:
            _refuse(ev, argv[:6])
        SPAWNED.append(ev)
        return
    if ev in _PROC or ev in _NET:
        _refuse(ev, args[:2] if isinstance(args, tuple) else args)
    if ev in _DEL:
        _refuse(ev, args[:1])
    if ev in _WRITE:
        for i in _WRITE[ev]:
            p = _p(args[i]) if len(args) > i else None
            if p is not None and not _inside(p):
                _refuse(ev, p)
        return
    if ev in _LIST:
        p = _p(args[0]) if args else None
        if p is not None:
            why = _forbidden(p)
            if why:
                _refuse('%s(%s)' % (ev, why), p)
        return
    if ev == 'open':
        p = _p(args[0])
        if p is None:
            return
        why = _forbidden(p)
        if why:
            _refuse('open(%s)' % why, p)
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else None
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
            (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
        if writing and not _inside(p):
            _refuse('open(write outside folder)', p)


sys.addaudithook(_hook)


# ----------------------------------------------------------------------------------------------- helpers
def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def write_x(p, text):
    with open(p, 'x', encoding='utf-8') as f:
        f.write(text)
    return [str(p), sha_f(p)]


def need(cond, msg):
    if not cond:
        raise SystemExit('PIN/PRECONDITION FAILED: ' + msg)


def verify_pins():
    out = {}
    for name, (p, s) in (('b0_tool', B0_TOOL), ('r5', R5), ('r4', R4), ('map', MAP), ('registry', REG), ('fence', FENCE),
                         ('runner', RUNNER), ('fence_source', FENCE_SRC), ('runner_source', RUNNER_SRC)):
        a = sha_f(p)
        need(a == s, '%s %s expected %s actual %s' % (name, p, s, a))
        out[name] = [str(p), a]
    need(Path(FENCE[0]).read_bytes() == Path(FENCE_SRC[0]).read_bytes(), 'fence copy not byte-identical')
    need(Path(RUNNER[0]).read_bytes() == Path(RUNNER_SRC[0]).read_bytes(), 'runner copy not byte-identical')
    out['probe'] = [str(PROBE), sha_f(PROBE)]
    out['harness'] = [str(Path(os.path.abspath(__file__))), sha_f(__file__)]
    return out


def load_b0_inert():
    raw = Path(B0_TOOL[0]).read_bytes()
    need(sha_b(raw) == B0_TOOL[1], 'b0 tool bytes at load')
    m = types.ModuleType('b0_r5_vs_r4_c2v001_inert')
    m.__file__ = str(B0_TOOL[0])
    exec(compile(raw, str(B0_TOOL[0]), 'exec'), m.__dict__)  # module level: imports + constants only; main() is never called
    need(str(m.R4[0]) == str(R4[0]) and m.R4[1] == R4[1], 'b0 tool R4 constant differs from the r4 pin')
    need(str(m.MAP) == str(MAP[0]), 'b0 tool MAP constant differs from the map pin')
    need(m.PY == PY, 'b0 tool PY differs')
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        need(m.ENV.get(k) == '1', 'b0 tool ENV %s' % k)
    need(not any(k.startswith('PYTHON') for k in m.ENV), 'b0 tool ENV carries PYTHON*')
    return m


def registry_jobs():
    reg = json.loads(Path(REG[0]).read_bytes())
    need(reg['driver'] == {'path': str(R5[0]), 'sha256': R5[1]}, 'registry driver pin is not r5 b5cc62af')
    other = {}
    for k in ('module', 'EPS', 'LO', 'fill_tool'):
        a = sha_f(reg[k]['path'])
        need(a == reg[k]['sha256'], 'registry %s pin %s' % (k, reg[k]['path']))
        other[k] = [reg[k]['path'], a]
    jobs = []
    for e in reg['specs']:
        need(e['P'] == 128, 'registry spec P != 128: %r' % e.get('case'))
        ent = {}
        for k in ('parent', 'template', 'filled'):
            a = sha_f(e[k]['path'])
            need(a == e[k]['sha256'], 'registry %s %s spec pin %s' % (e['case'], k, e[k]['path']))
            ent[k] = [e[k]['path'], a]
        sp = json.loads(Path(e['filled']['path']).read_bytes())
        uv = sp['numerics']['uv_tail']
        facts = {'galaxy': sp.get('galaxy'), 'label': sp.get('label'), 'M_s': uv['gas']['M_s'],
                 'eps_certificate_equals_registry_EPS': uv['eps_certificate'] == reg['EPS'],
                 'lo_certificate_equals_registry_LO': uv['lo_certificate'] == reg['LO']}
        jobs.append({'label': e['case'], 'spec': e['filled']['path'], 'spec_sha256': ent['filled'][1], 'registry_entry': ent,
                     'spec_facts': facts})
    need(len(jobs) == N_SPECS, 'registry has %d specs, not %d' % (len(jobs), N_SPECS))
    need(len({j['label'] for j in jobs}) == N_SPECS and len({j['spec'] for j in jobs}) == N_SPECS, 'labels/specs not unique')
    need(all(re.fullmatch(r'[A-Za-z0-9-]+', j['label']) for j in jobs), 'label charset')
    return jobs, other


def _sha_rows(text):
    return {p: s for s, p in re.findall(r'^([0-9a-f]{64})  (/.*?)\s*$', text, re.M)}


def build_chain():
    """BUILD_V007 pins BUILD_V006, which pins BUILD_V005, which pins DRY_R5_MS128_V004.json and every per-case
    DRYRUN_REPORT.json; every sha is checked from bytes and every path is taken from those records' bytes."""
    chain = []
    for a, b in zip(BUILDS, BUILDS[1:]):
        rows = _sha_rows(Path(a).read_bytes().decode())
        actual = sha_f(b)
        need(rows.get(str(b)) == actual, '%s does not pin %s at %s' % (a, b, actual))
        chain.append({'record': [str(a), sha_f(a)], 'pins': [str(b), actual]})
    r5rows = _sha_rows(Path(BUILDS[-1]).read_bytes().decode())
    dry_sha = r5rows.get(str(DRY_REC[0]))
    need(dry_sha is not None and dry_sha.startswith(DRY_REC[1]), 'BUILD_V005 does not pin %s (ff60cd6b)' % DRY_REC[0])
    need(sha_f(DRY_REC[0]) == dry_sha, 'DRY_R5_MS128_V004.json bytes differ from the BUILD_V005 pin')
    dj = json.loads(Path(DRY_REC[0]).read_bytes())
    need(dj['registry'] == {'path': str(REG[0]), 'sha256': REG[1]}, 'DRY record registry is not c7023846')
    need(dj['driver'] == {'path': str(R5[0]), 'sha256': R5[1]}, 'DRY record driver is not r5')
    dirs = {}
    for c in dj['checks']:
        rp, rs = c['report']['path'], c['report']['sha256']
        need(r5rows.get(rp) == rs, 'BUILD_V005 pin of %s' % rp)
        need(sha_f(rp) == rs, 'existing report bytes %s' % rp)
        dirs[c['case']] = {'dir': str(Path(rp).parent), 'report': [rp, rs], 'exit': c['exit'], 'executed_stages': c['executed_stages'],
                           'passed': c['passed']}
    return {'chain': chain, 'dry_record': [str(DRY_REC[0]), dry_sha], 'cases': dirs}


def child_argv(script_args):
    lead = [TASKPOLICY, '-b'] if os.path.exists(TASKPOLICY) else [NICE, '-n', '10']
    return lead + [PY, '-I', '-B', str(RUNNER[0])] + [str(a) for a in script_args]


def parse_stderr(err):
    lines = err.strip().splitlines()
    summary, body = None, lines
    if lines and lines[-1].startswith(SUMMARY_PREFIX):
        try:
            summary = json.loads(lines[-1][len(SUMMARY_PREFIX):])
        except ValueError:
            summary = {'unparsed': lines[-1][:600]}
        body = lines[:-1]
    text = '\n'.join(body).strip()
    tail = text.splitlines()[-1:] if text else []
    fence_lines = [x[:600] for x in lines if 'FENCE_C4:' in x]
    blocked_after = summary.get('blocked_after_selftest') if isinstance(summary, dict) else None
    runner_refused = [x[:600] for x in lines if x.startswith(RUNNER_REFUSALS)]
    return {'stderr_tail': tail, 'fence_summary': summary, 'fence_summary_present': summary is not None,
            'blocked_after_selftest': blocked_after, 'fence_refusal_lines': fence_lines,
            'fence_refused': bool(fence_lines) or bool(blocked_after), 'runner_refused': runner_refused}


def run_child(tag, script_args, cwd, log_stem):
    argv = child_argv(script_args)
    t0 = time.monotonic()
    started = utc()
    p = subprocess.run(argv, capture_output=True, text=True, errors='replace', env=ENV, cwd=str(cwd))
    secs = round(time.monotonic() - t0, 2)
    res = {'argv': argv, 'cwd': str(cwd), 'started_utc': started, 'exit': p.returncode, 'seconds': secs,
           'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr)}
    res.update(parse_stderr(p.stderr))
    if log_stem is not None:
        res['stderr_log'] = write_x(LOGS / (log_stem + '.stderr.txt'), p.stderr)
        res['stdout_log'] = write_x(LOGS / (log_stem + '.stdout.txt'), p.stdout)
    else:
        res['stdout_text'] = p.stdout[-400:]
        res['stderr_text_tail'] = p.stderr[-1600:]
    return res


def smoke_ok(s):
    f = s.get('fence_summary') or {}
    return (s['exit'] == 0 and isinstance(f, dict) and f.get('fence_sha256') == FENCE[1] and f.get('review_root') == str(FOLDER)
            and f.get('selftest_pass') == f.get('selftest_of') == 8
            and f.get('v002_exception_probes_pass') == f.get('v002_exception_probes_of') == 15
            and f.get('blocked_after_selftest') == [] and not s['fence_refusal_lines'] and not s['runner_refused'])


def rule_verdict(m, base, a, b, d4, d5):
    cmpd = m.compare(d4, d5, base)
    t4 = m.apply(base + [(str(d4), str(d5))], '\n'.join(a['stderr_tail']).encode()).decode()
    term_eq = t4 == '\n'.join(b['stderr_tail'])
    evidence = a['exit'] == 0 and b['exit'] == 0 and cmpd['reports_nonempty']
    if evidence:
        verdict = 'PASS_PLAN_IDENTICAL' if cmpd['identical'] else 'FAIL'
    elif a['exit'] != 0 and b['exit'] != 0 and a['exit'] == b['exit'] and term_eq and cmpd['identical']:
        verdict = 'NO_EVIDENCE_EQUAL_EARLY_FAILURE'
    else:
        verdict = 'FAIL'
    return cmpd, term_eq, evidence, verdict


def main():
    global ENV
    need(len(sys.argv) == 3 and sys.argv[1] in ('check', 'run'), 'usage: check|run STAMP')
    mode, stamp = sys.argv[1], sys.argv[2]
    need(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', stamp) is not None, 'STAMP format')
    pins = verify_pins()
    m = load_b0_inert()
    ENV = dict(m.ENV)
    base = m.declared_map(str(R5[0]), R5[1])
    need(sha_f(MAP[0]) == MAP[1], 'map bytes changed around declared_map')
    jobs, reg_other = registry_jobs()
    build = build_chain()
    need(sorted(build['cases']) == sorted(j['label'] for j in jobs), 'BUILD_V005 cases differ from the registry cases')
    for j in jobs:
        j['rd'] = {'R4': DRY / ('R4_' + j['label']), 'R5': DRY / ('R5_' + j['label'])}
        for tag, drv in (('R4', R4[0]), ('R5', R5[0])):
            ALLOWED_ARGV.add(tuple(child_argv([drv, 'dry-run', '--spec', j['spec'], '--report-dir', j['rd'][tag]])))
    ALLOWED_ARGV.add(tuple(child_argv([PROBE])))
    need(len(ALLOWED_ARGV) == 2 * N_SPECS + 1, 'sanctioned argv count')
    need(DRY.is_dir() and LOGS.is_dir(), 'out/dry and out/logs must exist')
    if mode == 'run':
        need(not RECORD.exists(), 'record exists')
        for j in jobs:
            for tag in ('R4', 'R5'):
                need(not j['rd'][tag].exists(), 'report dir exists: %s' % j['rd'][tag])
                for suf in ('.stderr.txt', '.stdout.txt'):
                    need(not (LOGS / ('%s_%s%s' % (tag, j['label'], suf))).exists(), 'log exists')
    smoke = run_child('SMOKE', [PROBE], DRY, 'FENCE_SMOKE_RUN_C4V001' if mode == 'run' else None)
    smoke['ok'] = smoke_ok(smoke)
    pre = {'mode': mode, 'stamp': stamp, 'pins': pins, 'declared_map_pairs': len(base), 'registry_other_pins': reg_other,
           'jobs': [[j['label'], j['spec'], j['spec_sha256'], j['spec_facts']] for j in jobs],
           'build_chain': build, 'sanctioned_argvs': len(ALLOWED_ARGV), 'smoke': smoke, 'guard_blocked': GUARD_BLOCKED,
           'example_child_argv': list(child_argv([R4[0], 'dry-run', '--spec', jobs[0]['spec'], '--report-dir', jobs[0]['rd']['R4']]))}
    if mode == 'check':
        print(json.dumps(pre, indent=1, default=str))
        return 0 if smoke['ok'] else 4
    need(smoke['ok'], 'fence smoke test failed: %s' % json.dumps(smoke, default=str)[:1500])

    # ---- the 20 sanctioned dry runs: per spec R4 then R5 (R5 skipped after a fence refusal or runner refusal of R4)
    def per_spec(j):
        a = run_child('R4', [R4[0], 'dry-run', '--spec', j['spec'], '--report-dir', j['rd']['R4']], DRY, 'R4_' + j['label'])
        if a['fence_refused'] or a['runner_refused']:
            return a, None
        b = run_child('R5', [R5[0], 'dry-run', '--spec', j['spec'], '--report-dir', j['rd']['R5']], DRY, 'R5_' + j['label'])
        return a, b
    runs = {}
    t_start = utc()
    with cf.ThreadPoolExecutor(max_workers=MAX_PROCS) as ex:
        fut = {ex.submit(per_spec, j): j['label'] for j in jobs}
        for f in cf.as_completed(fut):
            try:
                runs[fut[f]] = f.result()
            except Exception:
                runs[fut[f]] = ('EXCEPTION', traceback.format_exc()[-3000:])
    t_end = utc()

    rows = {}
    for j in jobs:
        n = j['label']
        row = {'label': n, 'spec': j['spec'], 'spec_sha256': j['spec_sha256'], 'spec_sha256_after': sha_f(j['spec']),
               'registry_entry': j['registry_entry'], 'spec_facts': j['spec_facts'],
               'report_dirs': {k: str(v) for k, v in j['rd'].items()}}
        r = runs.get(n)
        try:
            if r is None or r[0] == 'EXCEPTION':
                row.update(r4=None, r5=None, counted=False, verdict='ERROR', error=(r[1] if r else 'no result'))
            else:
                a, b = r
                row['r4'], row['r5'] = a, b
                blocked = [x for x in (a, b) if x is not None and x['fence_refused']]
                runner_bad = [x for x in (a, b) if x is not None and x['runner_refused']]
                if b is not None:
                    cmpd, term_eq, evidence, verdict = rule_verdict(m, base, a, b, j['rd']['R4'], j['rd']['R5'])
                    row.update(terminal_line_equal_after_T=term_eq, files=cmpd, rule_verdict=verdict)
                else:
                    evidence, verdict = False, None
                    row.update(terminal_line_equal_after_T=None, files=None, rule_verdict=None,
                               r5_not_run='spec stopped after the R4 child hit a fence/runner refusal (task rule 4)')
                if blocked:
                    row.update(counted=False, verdict='BLOCKED_FORBIDDEN_ACCESS',
                               refused=[{'side': 'R4' if x is a else 'R5', 'fence_refusal_lines': x['fence_refusal_lines'],
                                         'blocked_after_selftest': x['blocked_after_selftest']} for x in blocked])
                elif runner_bad:
                    row.update(counted=False, verdict='ERROR', error='fence runner refused: %s' % [x['runner_refused'] for x in runner_bad])
                else:
                    row.update(counted=evidence, verdict=verdict)
        except Exception:
            row.update(counted=False, verdict='ERROR', error=traceback.format_exc()[-3000:])
        rows[n] = row

    counted = [n for n, r in rows.items() if r['counted']]
    summ = {'specs': len(rows), 'counted_comparisons': len(counted),
            'pass_plan_identical': sorted(n for n in counted if rows[n]['verdict'] == 'PASS_PLAN_IDENTICAL'),
            'fail': sorted(n for n, r in rows.items() if r['verdict'] == 'FAIL'),
            'no_evidence_equal_early_failures': sorted(n for n, r in rows.items() if r['verdict'] == 'NO_EVIDENCE_EQUAL_EARLY_FAILURE'),
            'blocked_forbidden_access': sorted(n for n, r in rows.items() if r['verdict'] == 'BLOCKED_FORBIDDEN_ACCESS'),
            'error': sorted(n for n, r in rows.items() if r['verdict'] == 'ERROR')}
    summ['n_pass'] = len(summ['pass_plan_identical'])
    summ['n_no_evidence'] = len(summ['no_evidence_equal_early_failures'])
    summ['verdict_root_formula'] = 'PASS_PLAN_IDENTICAL' if not summ['fail'] and summ['n_pass'] == len(counted) else 'FAIL'
    if summ['fail']:
        summ['verdict_B0'] = 'FAIL'
    elif summ['blocked_forbidden_access']:
        summ['verdict_B0'] = 'BLOCKED_FORBIDDEN_ACCESS'
    elif summ['error']:
        summ['verdict_B0'] = 'ERROR'
    else:
        summ['verdict_B0'] = summ['verdict_root_formula']
    summ['all_specs_counted'] = len(counted) == N_SPECS
    fence_ok = {n: {side: (rows[n].get(side) or {}).get('blocked_after_selftest') for side in ('r4', 'r5')} for n in rows}
    summ['every_child_blocked_after_selftest_empty'] = all(v == [] for d in fence_ok.values() for v in d.values())
    summ['every_child_fence_selftest_8_of_8'] = all(
        isinstance((rows[n].get(side) or {}).get('fence_summary'), dict)
        and rows[n][side]['fence_summary'].get('selftest_pass') == 8 and rows[n][side]['fence_summary'].get('v002_exception_probes_pass') == 15
        for n in rows for side in ('r4', 'r5'))

    # ---- NOTE-level cross-check: fresh R5 reports vs the existing BUILD_V005-pinned r5 dry reports (dir substitution only)
    cross = {}
    for j in jobs:
        n = j['label']
        ex_dir = Path(build['cases'][n]['dir'])
        try:
            if rows[n].get('r5') is None or rows[n]['r5']['exit'] != 0:
                cross[n] = {'existing_dir': str(ex_dir), 'status': 'NOT_COMPARED (fresh R5 dry run did not complete)'}
                continue
            pinned = build['cases'][n]['report']
            need(sha_f(pinned[0]) == pinned[1], 'existing report changed: %s' % pinned[0])
            cx = m.compare(ex_dir, j['rd']['R5'], [])
            cross[n] = {'existing_dir': str(ex_dir), 'existing_report_pinned': pinned, 'fresh_dir': str(j['rd']['R5']),
                        'substitution': [str(ex_dir), str(j['rd']['R5'])],
                        'status': 'EQUAL' if cx['identical'] else 'DIFFER', 'compare': cx}
        except Exception:
            cross[n] = {'existing_dir': str(ex_dir), 'status': 'ERROR', 'error': traceback.format_exc()[-2000:]}

    after = {k: sha_f(p) == s for k, (p, s) in (('b0_tool', B0_TOOL), ('r5', R5), ('r4', R4), ('map', MAP), ('registry', REG),
                                                 ('fence', FENCE), ('runner', RUNNER))}
    rec = {
        'schema': 'B0_R5_VS_R4_MS128_C4V001',
        'label': 'TESTED: dry-run (plan only, executed_stages 0) of both drivers on each spec under the review fence; '
                 'compared on bytes with root\'s compare() after the declared map T',
        'task': 'RI-31 (A113, dispatch 0650, root entry A113 in V006): production M_s 128 r5 = r4 dry identity on the c7023846 set, '
                'B0-EMPTY rule (A55 ruling 2: every spec)',
        'stamp_launch_date_u': stamp, 'children_started_utc': t_start, 'children_finished_utc': t_end,
        'tool': pins['b0_tool'], 'tool_use': 'loaded INERT from its pinned bytes (exec into a fresh module; main() never called); '
                                             'declared_map, compare, apply, files and ENV used unchanged',
        'harness': pins['harness'], 'fence': pins['fence'], 'fence_source': pins['fence_source'], 'runner': pins['runner'],
        'runner_source': pins['runner_source'], 'fence_probe': pins['probe'], 'review_root': str(FOLDER),
        'r5': pins['r5'], 'r4': pins['r4'], 'declared_map': [str(MAP[0]), MAP[1], len(base)], 'registry': pins['registry'],
        'registry_other_pins_verified': reg_other, 'build_chain': build,
        'max_procs': MAX_PROCS, 'scheduler': 'per spec: R4 child, then R5 child (R5 not run after a fence/runner refusal of R4); '
                                             'at most %d specs, hence %d children, at once' % (MAX_PROCS, MAX_PROCS),
        'child_command': child_argv(['DRIVER', 'dry-run', '--spec', 'SPEC', '--report-dir', 'RD']), 'child_cwd': str(DRY),
        'child_env': 'root ENV: os.environ without PYTHON*, OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS_NUM_THREADS=1',
        'rule': 'B0-EMPTY (A54): counted iff both exit 0 and both DRYRUN_REPORT.json and DRYRUN_PLAN.txt are non-empty; '
                'equal early failures listed as no evidence',
        'rule_detail': 'counted comparisons PASS_PLAN_IDENTICAL iff compare() identical, else FAIL; uncounted with equal nonzero exit, '
                       'equal terminal stderr line after T and identical files -> NO_EVIDENCE_EQUAL_EARLY_FAILURE; any other -> FAIL; '
                       'verdict_B0 PASS_PLAN_IDENTICAL iff no FAIL and every counted comparison passes (root main())',
        'adaptations': [
            'child = fence runner run_fenced_c4st2.py (fe904509) under taskpolicy -b, not the bare driver under nice -n 10',
            'terminal stderr line = the driver\'s last stderr line: last line of stderr.strip() after removing the runner\'s '
            'trailing FENCE_C4ST2_SUMMARY line (that line is recorded per child as fence_summary)',
            'spec set = exactly the ten FILLED specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846), labels = registry case',
            'task rule 4: a fence refusal makes the spec BLOCKED_FORBIDDEN_ACCESS (not counted) and stops it; verdict_B0 is then '
            'BLOCKED_FORBIDDEN_ACCESS unless a FAIL exists'],
        'fence_smoke': smoke,
        'rows': rows,
        'summary': summ,
        'cross_check_note': {'level': 'NOTE (not part of the verdict)', 'method': 'compare(existing_dir, fresh R5 dir, base=[]): '
                             'only the report-dir substitution, plus compare()\'s own derived-hash fixpoint and plan hash prefixes',
                             'per_spec': cross,
                             'equal': sorted(n for n, c in cross.items() if c['status'] == 'EQUAL'),
                             'differ': sorted(n for n, c in cross.items() if c['status'] != 'EQUAL')},
        'pins_unchanged_after_runs': after,
        'parent_guard': {'blocked': GUARD_BLOCKED, 'spawn_events': len(SPAWNED), 'sanctioned_argvs': len(ALLOWED_ARGV)},
    }
    rec['written_utc'] = utc()
    with open(RECORD, 'x') as f:
        json.dump(rec, f, indent=1, default=str)
    print(json.dumps({'record': [str(RECORD), sha_f(RECORD)], 'summary': summ,
                      'cross_check': {'equal': rec['cross_check_note']['equal'], 'differ': rec['cross_check_note']['differ']},
                      'pins_unchanged_after_runs': after, 'guard_blocked': GUARD_BLOCKED}, indent=1))
    return 0


ENV = None
if __name__ == '__main__':
    sys.exit(main())
