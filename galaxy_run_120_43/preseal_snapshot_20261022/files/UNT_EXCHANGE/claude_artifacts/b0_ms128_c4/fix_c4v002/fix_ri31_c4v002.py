#!/usr/bin/env python3
"""fix_ri31_c4v002.py: Claude4 helper, dispatch 0650 (root entry A113 in V006), stage FIX (ri31).

Confirms refuter finding R31-S1 (SHOULD_FIX) from bytes, re-checks from bytes the facts behind the wording changes that
refuter notes R31-N2, R31-N3 and R31-N5 suggest, and writes successor files by exclusive create (open(p, 'x')).
It never overwrites or appends to a file. (PARTIAL.md is appended to by the shell, between steps.)

usage (python3 -I -B, with the four single-thread env vars set to 1):
  fix_ri31_c4v002.py dry --ts STAMP     every check; builds FIX_RI31_C4V002.json and README_B0_MS128_C4V002.md in
                                        memory and prints them; writes nothing
  fix_ri31_c4v002.py write --ts STAMP   the same checks, then writes both files by exclusive create
  fix_ri31_c4v002.py hashes --ts STAMP  writes HASHES_B0_MS128_C4V002.txt (exclusive create) over every other file; last
  fix_ri31_c4v002.py verify             read-only: re-hashes every HASHES_B0_MS128_C4V002 row, checks the inventory
STAMP is `date -u +%Y-%m-%dT%H:%M:%SZ`, taken immediately before the call.

No driver is imported or run. An audit hook refuses process creation, network use, deletes, renames and moves, any write
outside the folder, and any open or listing of a forbidden name: any runs_ext path, the C5H run name, a UVT_* component, a
target word (rotmod, vobs, massmodels, sparc) or NGC3198 non-.py data. It tests the literal path first, so a refused path
is never resolved or lstat'ed (cf. refuter R31-N4).
"""
import ast
import hashlib
import io
import json
import os
import re
import sys
import tokenize

FOLDER = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4'
FIXDIR = FOLDER + '/fix_c4v002'
SCRIPT = os.path.realpath(__file__)
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')

# pins: dispatch 0650 text (drivers, b0 tool, registry, fence, runner), the refuter's result (its three records),
# README V001 bytes (DRY_R5_MS128_V004 full sha; BUILD 16-hex prefixes, compared as prefixes only, never extended)
R4 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
      'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b')
R5 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
      'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
B0_TOOL = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/gates/b0_r5_vs_r4_c2v001.py',
           '857ccb8a49e11314c7534b1651bfd316b5eab156b2f26b8b148fea385ef4ce5c')
REGISTRY = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json',
            'c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90')
FENCE = (FOLDER + '/tools/fence_c4v002.py', 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5')
RUNNER = (FOLDER + '/tools/run_fenced_c4st2.py', 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25')
REF = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4_refute'
REFUTER = {
    'REFUTE_RI31.md': (REF + '/REFUTE_RI31.md', 'd853899a3308e3697d812f7ee4c1bd3898d4ca702fd1aa5f0d8ac59093048958'),
    'REFUTE_RI31_CHECKS_C4V001.json': (REF + '/REFUTE_RI31_CHECKS_C4V001.json',
                                       'fc943107f25c2333ef06ba9556ee07ce9f497d46e2367b8ebf7dfdfdcd61453c'),
    'HASHES_REFUTE_RI31_C4V001.txt': (REF + '/HASHES_REFUTE_RI31_C4V001.txt',
                                      '357a9a6a1673e432a43cb3bc7bf11bc93d832f2d4051e22ec99663c86e582c4d'),
}
PKT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1'
BUILDS = {'BUILD_V007.md': (PKT + '/BUILD_V007.md', '94bc05a5db1e6350'),
          'BUILD_V006.md': (PKT + '/BUILD_V006.md', 'fb9e6a4a19395f35'),
          'BUILD_V005.md': (PKT + '/BUILD_V005.md', '46bc5b5d23bb39e7')}
DRY_V004 = (PKT + '/DRY_R5_MS128_V004.json', 'ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed')

HASHES_V001 = FOLDER + '/HASHES_B0_MS128_C4V001.txt'
README_V001 = FOLDER + '/README_B0_MS128_C4V001.md'
RECORD_V001 = FOLDER + '/out/B0_R5_VS_R4_MS128_C4V001.json'
PARTIAL = FOLDER + '/PARTIAL.md'
PARTIAL_V001_LEN = 1322   # TESTED before the fix stage's first append: 1322 bytes, sha256 = its HASHES V001 row
OUT_FIX = FOLDER + '/FIX_RI31_C4V002.json'
OUT_README = FOLDER + '/README_B0_MS128_C4V002.md'
OUT_HASHES = FOLDER + '/HASHES_B0_MS128_C4V002.txt'
DEVIATION_PATH = ('/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/'
                  'scratchpad/explore_dry1.txt')   # disclosed: an exploratory dry-mode capture written outside the folder
SCHEMA_CALL = 'UNT_GALAXY_M0_FORWARD_CALL_C2V001'
DRY_SCHEMA = 'UNT_GALAXY_M0_FORWARD_DRYRUN_C2V001'
NGC_GUARD = "nspec.get('config') == 'NGC3198_C2V002'"
A2_PATH = 'CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json'

# ------------------------------------------------------------------------------------------------ guard (audit hook)
TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')   # equals fence_c4v002 TARGET_WORDS (checked from its bytes)
GUARD = {'refused': [], 'opens': 0, 'listings': 0, 'writes': []}
PROC_EVENTS = {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty',
               'pty.spawn', 'os.startfile', 'os.kill', 'os.killpg', 'signal.pthread_kill'}
NET_EVENTS = {'socket.connect', 'socket.bind', 'socket.sendto', 'socket.sendmsg', 'socket.getaddrinfo',
              'socket.gethostbyname', 'urllib.Request', 'http.client.connect', 'ftplib.connect', 'smtplib.connect'}
NO_EVENTS = {'os.remove', 'os.rmdir', 'shutil.rmtree', 'os.rename', 'shutil.move', 'os.truncate', 'os.symlink', 'os.link',
             'os.chmod', 'os.chown', 'os.utime', 'os.chflags', 'os.lchflags', 'os.setxattr', 'os.removexattr',
             'shutil.copyfile', 'shutil.copytree'}


def _p(x):
    if x is None or isinstance(x, int):
        return None
    try:
        return os.path.abspath(os.fsdecode(os.fspath(x)))
    except TypeError:
        return None


def _under(p, root):
    return p == root or p.startswith(root + os.sep)


def forbidden(p):
    low = p.casefold()
    if 'runs_ext' in low:
        return 'runs_ext'
    if 'kmax_a2f10_c5h_run_v001' in low:
        return 'C5H name'
    parts = p.split(os.sep)
    for i, x in enumerate(parts):
        if x.casefold().startswith('uvt_') and not (i == len(parts) - 1 and x.startswith('uvt_') and x.endswith('.py')):
            return 'UVT component'
    if any(w in low for w in TARGET_WORDS):
        return 'target word'
    if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):
        return 'NGC3198 data'
    return None


def _refuse(event, detail):
    GUARD['refused'].append([event, str(detail)])
    raise PermissionError('FIX_GUARD_C4V002: %s %s' % (event, detail))


def _hook(event, args):
    if event in PROC_EVENTS or event in NET_EVENTS or event in NO_EVENTS:
        _refuse(event, args[:1] if isinstance(args, tuple) else args)
    if event == 'os.mkdir':
        p = _p(args[0]) if args else None
        if p is None or not _under(p, FOLDER):
            _refuse(event, args[:1])
        return
    if event in ('os.listdir', 'os.scandir'):
        p = _p(args[0]) if args else None
        if p is None:
            return
        why = forbidden(p) or (None if _under(p, FOLDER) else 'outside folder')
        if why:
            _refuse('%s(%s)' % (event, why), p)
        GUARD['listings'] += 1
        return
    if event == 'open':
        p = _p(args[0]) if args else None
        if p is None:
            return
        why = forbidden(p)               # literal first: a refused path is never resolved
        if why:
            _refuse('open(%s)' % why, p)
        real = os.path.realpath(p)
        why = forbidden(real)
        if why:
            _refuse('open(real path %s)' % why, real)
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else None
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
            (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
        if writing:
            if not (_under(p, FOLDER) and _under(real, FOLDER)):
                _refuse('open(write outside folder)', p)
            GUARD['writes'].append(p)
        GUARD['opens'] += 1


def guard_summary():
    return {'refused': list(GUARD['refused']), 'opens_allowed': GUARD['opens'], 'listings_allowed': GUARD['listings'],
            'write_opens': list(GUARD['writes'])}


# ------------------------------------------------------------------------------------------------ helpers
def need(cond, msg):
    if not cond:
        raise SystemExit('FIX_C4V002 STOP: ' + msg)


def rb(p):
    with open(p, 'rb') as f:
        return f.read()


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def line_of(text, i):
    return text.count('\n', 0, i) + 1


# ------------------------------------------------------------------------------------------------ checks
def check_pins():
    pins = {}
    table = [('r4_driver', R4), ('r5_driver', R5), ('b0_tool', B0_TOOL), ('registry', REGISTRY),
             ('fence_copy', FENCE), ('runner_copy', RUNNER), ('dry_r5_ms128_v004', DRY_V004)]
    table += [('refuter_' + k, v) for k, v in REFUTER.items()]
    for name, (p, s) in table:
        got = sha_b(rb(p))
        need(got == s, 'pin %s differs: %s' % (name, got))
        pins[name] = {'path': p, 'sha256': got, 'equal_to_pin': True}
    for name, (p, pre) in BUILDS.items():
        got = sha_b(rb(p))
        need(got.startswith(pre), 'BUILD pin %s: %s does not start with the README V001 prefix %s' % (name, got, pre))
        pins[name] = {'path': p, 'sha256': got, 'readme_v001_prefix': pre, 'prefix_equal': True}
    fence_src = rb(FENCE[0])
    tw = None
    for node in ast.parse(fence_src).body:     # read by AST; the fence is NOT imported (that would install its hook)
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TARGET_WORDS' for t in node.targets):
            tw = tuple(ast.literal_eval(node.value))
    need(tw == TARGET_WORDS, 'fence TARGET_WORDS %r' % (tw,))
    fl = fence_src.decode('utf-8').split('\n')
    n4 = {'line_134': fl[133].strip(), 'line_135': fl[134].strip(), 'line_136': fl[135].strip(),
          'line_86': fl[85].strip()}
    need(n4['line_134'] == 'lit = os.path.abspath(p)' and n4['line_135'] == 'real = os.path.realpath(lit)'
         and n4['line_136'] == 'why = _forbidden_read(lit, real)' and n4['line_86'].startswith("if ('ngc3198' in low"),
         'fence lines 86 / 134-136 are not as cited: %r' % n4)
    rl = rb(RUNNER[0]).decode('utf-8').split('\n')
    se = [i + 1 for i, l in enumerate(rl) if l.strip().startswith('except SystemExit as e')]
    need(len(se) == 1, 'runner SystemExit handler')
    n7 = {'except_line': se[0], 'handler': [rl[se[0] - 1].strip(), rl[se[0]].strip()]}
    return pins, {'fence_TARGET_WORDS': list(tw), 'r31_n4_fence_lines': n4, 'r31_n7_runner_lines': n7}


def check_v001(mode):
    hb = rb(HASHES_V001)
    lines = hb.decode('utf-8').split('\n')
    need(lines[0].startswith('# HASHES_B0_MS128_C4V001: '), 'HASHES V001 header')
    rows = []
    for l in lines[1:]:
        if not l:
            continue
        s, p = l.split('  ', 1)
        need(re.fullmatch(r'[0-9a-f]{64}', s) is not None and p.startswith(FOLDER + '/'), 'bad V001 row %r' % l)
        rows.append((s, p))
    rowmap = dict((p, s) for s, p in rows)
    need(len(rowmap) == len(rows), 'duplicate V001 rows')
    equal, changed, partial = 0, [], None
    for s, p in rows:
        b = rb(p)
        if p == PARTIAL:
            pre = sha_b(b[:PARTIAL_V001_LEN])
            partial = {'path': p, 'v001_row_sha256': s, 'v001_len': PARTIAL_V001_LEN, 'len_now': len(b),
                       'sha256_now': sha_b(b), 'first_1322_bytes_sha256': pre,
                       'prefix_equals_v001_row': pre == s and len(b) >= PARTIAL_V001_LEN}
            need(partial['prefix_equals_v001_row'], 'PARTIAL.md: its V001 prefix changed')
        elif sha_b(b) == s:
            equal += 1
        else:
            changed.append(p)
    need(not changed, 'V001 files changed: %r' % changed)
    need(partial is not None, 'PARTIAL.md row missing from HASHES V001')
    news = {OUT_FIX, OUT_README, OUT_HASHES}
    unexpected, links, fixfiles, present = [], [], [], []
    for d, dirs, files in os.walk(FOLDER):
        for n in dirs + files:
            if os.path.islink(os.path.join(d, n)):
                links.append(os.path.join(d, n))
        for n in files:
            q = os.path.join(d, n)
            if q in rowmap or q == HASHES_V001:
                continue
            if _under(q, FIXDIR):
                fixfiles.append(q)
            elif q in news:
                present.append(q)
            else:
                unexpected.append(q)
    need(not links, 'symlinks in the folder: %r' % links)
    need(not unexpected, 'unexpected files: %r' % unexpected)
    expect_present = {'dry': [], 'write': [], 'hashes': sorted([OUT_FIX, OUT_README]),
                      'verify': sorted([OUT_FIX, OUT_README, OUT_HASHES])}[mode]
    need(sorted(present) == expect_present, 'mode %s: outputs present %r, expected %r' % (mode, present, expect_present))
    return {'hashes_v001': {'path': HASHES_V001, 'sha256': sha_b(hb), 'rows': len(rows)},
            'rows_equal': equal, 'rows_changed': changed, 'partial_md': partial,
            'fix_stage_files_present': sorted(fixfiles), 'unexpected_files': unexpected, 'symlinks': links}, rowmap


def check_record(rowmap):
    b = rb(RECORD_V001)
    need(sha_b(b) == rowmap[RECORD_V001], 'record V001 differs from its HASHES V001 row')
    r = json.loads(b)
    s = r['summary']
    need(r['schema'] == 'B0_R5_VS_R4_MS128_C4V001', 'record schema')
    need(s['verdict_B0'] == 'PASS_PLAN_IDENTICAL' and s['specs'] == 10 and s['counted_comparisons'] == 10
         and s['n_pass'] == 10 and not s['fail'] and not s['no_evidence_equal_early_failures']
         and not s['blocked_forbidden_access'] and not s['error'], 'record summary')
    low = b.decode('utf-8').casefold()
    phrases = ('neither driver', 'target-word', 'target word', 'forbidden tree', 'run-tree', 'run tree')
    hits = dict((ph, low.count(ph)) for ph in phrases)
    need(not any(hits.values()), 'the record contains a corrected phrase: %r' % hits)
    return r, {'path': RECORD_V001, 'sha256': sha_b(b), 'equals_hashes_v001_row': True, 'verdict_B0': s['verdict_B0'],
               'specs': s['specs'], 'counted_comparisons': s['counted_comparisons'], 'n_pass': s['n_pass'],
               'pass_plan_identical': s['pass_plan_identical'], 'fail': s['fail'],
               'no_evidence_equal_early_failures': s['no_evidence_equal_early_failures'],
               'blocked_forbidden_access': s['blocked_forbidden_access'], 'error': s['error'],
               'corrected_phrase_counts_in_record': hits}


def check_specs(record, rowmap):
    reg = json.loads(rb(REGISTRY[0]))
    cases = [e['case'] for e in reg['specs']]
    need(cases == list(record['rows']), 'registry cases differ from the record rows')
    out = {}
    for e in reg['specs']:
        c = e['case']
        p, s = e['filled']['path'], e['filled']['sha256']
        b = rb(p)
        need(sha_b(b) == s, 'spec %s sha' % c)
        row = record['rows'][c]
        need(row['spec'] == p and row['spec_sha256'] == s and row['verdict'] == 'PASS_PLAN_IDENTICAL', 'record row %s' % c)
        sp = json.loads(b)
        need(sp.get('schema') == SCHEMA_CALL and sp.get('galaxy') == 'DDO154', 'spec %s schema/galaxy' % c)
        reps = {}
        for side, drv in (('R4', R4), ('R5', R5)):
            rp = row['report_dirs'][side] + '/DRYRUN_REPORT.json'
            rbb = rb(rp)
            need(sha_b(rbb) == rowmap[rp], 'report %s %s differs from HASHES V001' % (side, c))
            rep = json.loads(rbb)
            ns = rep['normalized_spec']
            reps[side] = {'report_schema': rep['schema'], 'normalized_schema': ns.get('schema'),
                          'normalized_galaxy': ns.get('galaxy'), 'normalized_has_config_field': 'config' in ns,
                          'executed_stages': rep['executed_stages'], 'call_spec_sha256': rep.get('call_spec_sha256'),
                          'driver_sha256': rep.get('driver_sha256')}
            need(rep['schema'] == DRY_SCHEMA and ns.get('schema') == SCHEMA_CALL and ns.get('galaxy') == 'DDO154'
                 and 'config' not in ns and rep['executed_stages'] == 0 and rep.get('call_spec_sha256') == s
                 and rep.get('driver_sha256') == drv[1], 'report %s %s fields: %r' % (side, c, reps[side]))
        out[c] = {'filled_spec': [p, s], 'schema': sp['schema'], 'galaxy': sp['galaxy'], 'reports': reps,
                  'record_verdict': row['verdict']}
    return cases, out


def check_fence_logs(cases):
    names = ['FENCE_SMOKE_RUN_C4V001'] + ['%s_%s' % (side, c) for c in cases for side in ('R4', 'R5')]
    out = {}
    for n in names:
        t = rb(FOLDER + '/out/logs/%s.stderr.txt' % n).decode('utf-8')
        lines = [l for l in t.split('\n') if l.strip()]
        need(lines and lines[-1].startswith('FENCE_C4ST2_SUMMARY '), 'no fence summary in %s' % n)
        js = json.loads(lines[-1][len('FENCE_C4ST2_SUMMARY '):])
        ok = (js['fence_sha256'] == FENCE[1] and js['review_root'] == FOLDER and js['selftest_pass'] == 8
              and js['selftest_of'] == 8 and js['v002_exception_probes_pass'] == 15
              and js['v002_exception_probes_of'] == 15 and js['blocked_after_selftest'] == [])
        need(ok, 'fence summary %s: %r' % (n, js))
        out[n] = {'blocked_after_selftest': js['blocked_after_selftest'],
                  'selftest': '%d/%d' % (js['selftest_pass'], js['selftest_of']),
                  'probes': '%d/%d' % (js['v002_exception_probes_pass'], js['v002_exception_probes_of']),
                  'other_stderr_lines': len(lines) - 1}
    need(all(v['other_stderr_lines'] == 0 for k, v in out.items() if k != 'FENCE_SMOKE_RUN_C4V001'),
         'a driver stderr is not empty')
    return out


def analyze_driver(b):
    text = b.decode('utf-8')
    low = text.casefold()
    lines = text.split('\n')
    words = ('runs_ext', 'c5h', 'kmax_a2f10_c5h_run_v001') + TARGET_WORDS + ('ngc3198', 'ngc_3198')
    counts = dict((w, low.count(w)) for w in words)
    line_hits = dict((w, [i + 1 for i, l in enumerate(lines) if w in l.casefold()])
                     for w in ('runs_ext', 'c5h', 'kmax_a2f10_c5h_run_v001') + TARGET_WORDS)
    names = {tokenize.STRING: 'STRING', tokenize.COMMENT: 'COMMENT', tokenize.NAME: 'NAME'}
    if hasattr(tokenize, 'FSTRING_MIDDLE'):
        names[tokenize.FSTRING_MIDDLE] = 'FSTRING_MIDDLE'
    tokens, tok_count = [], dict((w, 0) for w in TARGET_WORDS)
    for t in tokenize.tokenize(io.BytesIO(b).readline):
        if t.type not in names:
            continue
        sl = t.string.casefold()
        ws = [w for w in TARGET_WORDS if w in sl]
        if not ws:
            continue
        for w in ws:
            tok_count[w] += sl.count(w)
        tokens.append({'token': names[t.type], 'lines': [t.start[0], t.end[0]], 'words': ws})
    tree = ast.parse(b)
    parent = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            parent[ch] = node

    def enclosing(node):
        n = parent.get(node)
        while n is not None and not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            n = parent.get(n)
        return n.name if n is not None else '<module>'

    def role(node):
        par = parent.get(node)
        if isinstance(par, ast.Expr):
            fn = parent.get(par)
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and fn.body \
                    and fn.body[0] is par:
                return 'docstring'
            return 'expression statement'
        if isinstance(par, ast.Subscript) and par.slice is node:
            return 'subscript key'
        if isinstance(par, ast.Tuple):
            gp = parent.get(par)
            if isinstance(gp, ast.Assign):
                return 'tuple element assigned to ' + ','.join(t.id for t in gp.targets if isinstance(t, ast.Name))
            return 'tuple element'
        if isinstance(par, ast.Dict):
            return 'dict key' if any(node is k for k in par.keys) else 'dict value'
        if isinstance(par, ast.Compare):
            return 'comparison operand'
        return type(par).__name__

    def path_literal(v):
        return re.search(r'\s', v) is None and ('/' in v or re.fullmatch(r'[\w.%\-]+\.[A-Za-z0-9]{1,5}', v) is not None)

    def guard_of(node):
        ch, n = node, parent.get(node)
        while n is not None and not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if isinstance(n, ast.If) and any(ch is x for x in n.body):
                return ast.unparse(n.test)
            ch, n = n, parent.get(n)
        return None

    consts, ngc_paths, const_count = [], [], dict((w, 0) for w in TARGET_WORDS)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            vl = v.casefold()
            ws = [w for w in TARGET_WORDS if w in vl]
            if ws:
                for w in ws:
                    const_count[w] += vl.count(w)
                consts.append({'line': node.lineno, 'end_line': node.end_lineno, 'words': ws, 'role': role(node),
                               'enclosing': enclosing(node), 'path_literal': path_literal(v),
                               'value': v if len(v) <= 240 else v[:240] + '...'})
            if ('ngc3198' in vl or 'ngc_3198' in vl) and not vl.endswith('.py') and path_literal(v):
                ngc_paths.append({'line': node.lineno, 'value': v, 'enclosing': enclosing(node)})
    consts.sort(key=lambda x: x['line'])
    ngc_paths.sort(key=lambda x: (x['line'], x['value']))

    def refs(name):
        out = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == name and isinstance(node.ctx, ast.Load):
                par = parent.get(node)
                out.append({'line': node.lineno, 'enclosing': enclosing(node),
                            'call': isinstance(par, ast.Call) and par.func is node, 'guard': guard_of(node)})
            elif isinstance(node, ast.Attribute) and node.attr == name:
                out.append({'line': node.lineno, 'enclosing': enclosing(node), 'attribute': True})
            elif isinstance(node, ast.Constant) and node.value == name:
                out.append({'line': node.lineno, 'enclosing': enclosing(node), 'string': True})
        return sorted(out, key=lambda x: x['line'])

    chain_names = ('_VELOCITY_KEY_HINTS', '_key_scan', 'ngc_sources_summary', '_ngc_collect', 'ngc_dry_run',
                   'ngc_run_blocked', 'normalize_ngc_spec')
    chain = dict((n, refs(n)) for n in chain_names)
    defs = dict((n, [d.lineno for d in ast.walk(tree) if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef))
                     and d.name == n]) for n in chain_names[1:])
    defs['_VELOCITY_KEY_HINTS'] = [d.lineno for d in ast.walk(tree) if isinstance(d, ast.Assign)
                                   and any(isinstance(t, ast.Name) and t.id == '_VELOCITY_KEY_HINTS' for t in d.targets)]
    config_consts = sorted(({'line': node.lineno, 'enclosing': enclosing(node), 'role': role(node)}
                            for node in ast.walk(tree) if isinstance(node, ast.Constant) and node.value == 'NGC3198_C2V002'),
                           key=lambda x: x['line'])
    return {'n_lines': len(lines), 'counts': counts, 'line_hits': line_hits, 'tokens': tokens, 'token_count': tok_count,
            'const_count': const_count, 'consts': consts, 'chain': chain, 'defs': defs,
            'config_NGC3198_C2V002_constants': config_consts, 'ngc3198_non_py_path_literals': ngc_paths,
            'a2_anchor_result_path_lines': [i + 1 for i, l in enumerate(lines) if A2_PATH in l]}


def s1_facts(a):
    c = a['counts']
    ch = a['chain']
    plain = all(not r.get('string') and not r.get('attribute') for n in ch for r in ch[n])
    facts = {
        'no_runs_ext_c5h_kmax': c['runs_ext'] == 0 and c['c5h'] == 0 and c['kmax_a2f10_c5h_run_v001'] == 0,
        'massmodels_sparc_zero': c['massmodels'] == 0 and c['sparc'] == 0,
        'rotmod_2_vobs_1': c['rotmod'] == 2 and c['vobs'] == 1,
        'lines_4580_4596_4560': a['line_hits']['rotmod'] == [4580, 4596] and a['line_hits']['vobs'] == [4560],
        'all_in_string_tokens': all(t['token'] == 'STRING' for t in a['tokens'])
        and a['token_count'] == dict((w, c[w]) for w in TARGET_WORDS),
        'all_in_string_constants': a['const_count'] == dict((w, c[w]) for w in TARGET_WORDS),
        'no_path_literal': not any(x['path_literal'] for x in a['consts']),
        'roles': sorted((x['role'], x['enclosing']) for x in a['consts']) == sorted(
            [('docstring', 'ngc_sources_summary'), ('subscript key', 'ngc_sources_summary'),
             ('tuple element assigned to _VELOCITY_KEY_HINTS', '<module>')]),
        'single_definitions': all(len(v) == 1 for v in a['defs'].values()),
        'no_string_or_attribute_refs': plain,
        'hints_read_only_by_key_scan': [r['enclosing'] for r in ch['_VELOCITY_KEY_HINTS']] == ['_key_scan'],
        'key_scan_called_by_itself_and_ngc_sources_summary':
            sorted(set(r['enclosing'] for r in ch['_key_scan'])) == ['_key_scan', 'ngc_sources_summary'],
        'ngc_sources_summary_called_only_by_ngc_collect':
            [r['enclosing'] for r in ch['ngc_sources_summary']] == ['_ngc_collect'],
        'ngc_collect_called_only_by_ngc_dry_run_and_run_blocked':
            sorted(r['enclosing'] for r in ch['_ngc_collect']) == ['ngc_dry_run', 'ngc_run_blocked'],
        'ngc_dry_run_only_in_cmd_dry_run_under_guard':
            [(r['enclosing'], r.get('guard')) for r in ch['ngc_dry_run']] == [('cmd_dry_run', NGC_GUARD)],
        'ngc_run_blocked_only_in_cmd_run_under_guard':
            [(r['enclosing'], r.get('guard')) for r in ch['ngc_run_blocked']] == [('cmd_run', NGC_GUARD)],
        'a2_anchor_path_on_one_line': len(a['a2_anchor_result_path_lines']) == 1,
    }
    return facts


TOKCH = re.compile(r'[^\s"\'<>,;:()\[\]{}=\\]')


def out_scan(rowmap):
    files = sorted(p for p in rowmap if _under(p, FOLDER + '/out'))
    words = ('runs_ext', 'kmax_a2f10_c5h_run_v001', 'c5h', 'rotmod', 'vobs', 'massmodels', 'sparc', 'ngc3198',
             'ngc_3198', '/volumes', 'claude2/runs/')
    tot = dict.fromkeys(words, 0)
    nfiles = dict.fromkeys(words, 0)
    sparc_ok, sparc_bad = 0, []
    runs_tails, uvt_comps, uvt_files = {}, {}, 0
    for p in files:
        t = rb(p).decode('utf-8', errors='replace')
        for w in words:
            k = len(re.findall(re.escape(w), t, flags=re.I))
            tot[w] += k
            nfiles[w] += 1 if k else 0
        for m in re.finditer('sparc', t, flags=re.I):
            a, z = m.start(), m.end()
            while a > 0 and TOKCH.match(t[a - 1]):
                a -= 1
            while z < len(t) and TOKCH.match(t[z]):
                z += 1
            tok = t[a:z]
            if re.fullmatch(r'DDO154_SPARC12_\d+', tok, flags=re.I):
                sparc_ok += 1
            elif len(sparc_bad) < 20:
                sparc_bad.append([p, tok[:160]])
        for m in re.finditer(r'claude2/runs/([^\s"\'<>,;:()\[\]{}=\\]*)', t, flags=re.I):
            runs_tails[m.group(1)] = runs_tails.get(m.group(1), 0) + 1
        found = False
        for m in re.finditer(r'/(uvt_[^/\s"\'<>,;:()\[\]{}=\\]*)(/?)', t, flags=re.I):
            key = m.group(1) + m.group(2)
            uvt_comps[key] = uvt_comps.get(key, 0) + 1
            found = True
        uvt_files += 1 if found else 0
    return {'files_scanned': len(files), 'occurrences': tot, 'files_with': nfiles,
            'sparc_whole_row_ids': sparc_ok, 'sparc_other_tokens': sparc_bad,
            'claude2_runs_path_tails': runs_tails, 'uvt_path_components': uvt_comps, 'files_with_uvt_path': uvt_files}


def scan_facts(s):
    o = s['occurrences']
    return {
        'zero_forbidden_text': all(o[w] == 0 for w in ('runs_ext', 'kmax_a2f10_c5h_run_v001', 'c5h', 'rotmod', 'vobs',
                                                       'massmodels', 'ngc3198', 'ngc_3198', '/volumes')),
        'sparc_only_row_ids': s['sparc_whole_row_ids'] == o['sparc'] and not s['sparc_other_tokens'],
        'claude2_runs_only_a2_anchor': list(s['claude2_runs_path_tails']) == ['A2_ANCHOR_F10_RUN_V001/result.json'],
        'uvt_components_only_py_sources': bool(s['uvt_path_components']) and all(
            k.startswith('uvt_') and k.endswith('.py') for k in s['uvt_path_components']),
    }


def n5_check(cases):
    logs = {}
    for c in cases:
        p = PKT + '/P128/%s_DRY_R5_MS128_V004.log' % c
        b = rb(p)
        logs[c] = {'path': p, 'sha256': sha_b(b),
                   'equals_fresh_R5_stdout': b == rb(FOLDER + '/out/logs/R5_%s.stdout.txt' % c)}
    recs = dict((k, rb(v[0]).decode('utf-8', errors='replace')) for k, v in BUILDS.items())
    recs['DRY_R5_MS128_V004.json'] = rb(DRY_V004[0]).decode('utf-8', errors='replace')
    out = {}
    for k, t in recs.items():
        out[k] = {'log_name_mentions': len(re.findall(r'_DRY_R5_MS128_V004\.log', t)),
                  'dot_log_mentions': len(re.findall(r'\.log\b', t)),
                  'log_sha256_hits': sorted(c for c in cases if logs[c]['sha256'] in t),
                  'log_sha16_hits': sorted(c for c in cases if logs[c]['sha256'][:16] in t),
                  'log_sha8_hits': sorted(c for c in cases if logs[c]['sha256'][:8] in t)}
    return {'logs': logs, 'records': out}


def n5_facts(n):
    return {'logs_equal_fresh_R5_stdout': all(v['equals_fresh_R5_stdout'] for v in n['logs'].values()),
            'no_sha_pin_of_any_log': all(not v['log_sha256_hits'] and not v['log_sha16_hits'] and not v['log_sha8_hits']
                                         for v in n['records'].values()),
            'no_log_name_in_records': all(v['log_name_mentions'] == 0 for v in n['records'].values())}


# ------------------------------------------------------------------------------------------------ README V002 text
OLD_TITLE = '# B0 r5 = r4 dry identity on the production M_s 128 set (RI-31)\n'
OLD_HEADER = ('Claude4 helper, dispatch 0650, root entry A113 in V006. Folder '
              '`/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4`. README written 2026-10-19T03:30:50Z (date -u).')
OLD_SCAN = ('- Every file under `out/` was scanned after the run. None contains a run-tree, C5H, target-word '
            '(rotmod/Vobs/MassModels/SPARC), NGC3198 or UVT_* component path string.')
OLD_SCOPE = "Neither driver's source contains a runs_ext, C5H or target-word string."
OLD_LOGS = ('- Checked outside the record, after the run (TESTED): each fresh R5 stdout is byte-identical to '
            '`v007_launch_packet_cx1/P128/<case>_DRY_R5_MS128_V004.log` for all 10 cases, and T(r4 stdout) == r5 stdout '
            'for all 10.')
OLD_TESTED = ('- TESTED: the pin checks, the 20 fenced dry runs, the B0 verdict, the fence summaries, the parent-guard counts, '
              'the cross-check and the output scan, all run on bytes in this folder.')
OLD_FORMAL = ('- FORMAL: that the dry-run path launches nothing and has no source references to forbidden trees (from reading '
              'the driver source), and that the fence does not cover stat or listdir.')
OLD_FILES_HEAD = '\n## Files\n'
OLD_FILES = ('- `PARTIAL.md` (progress log), this README, and `HASHES_B0_MS128_C4V001.txt`, which is written last and lists '
             'every other file.')
OLD_PARTIAL_S1 = 'no runs_ext/C5H/target strings in either driver'


def apply_reps(text, reps):
    spans = []
    for tag, old, new in reps:
        need(text.count(old) == 1, 'README V001 text for %s occurs %d times' % (tag, text.count(old)))
        i = text.index(old)
        spans.append((i, i + len(old), new, tag))
    spans.sort()
    for (a1, z1, _n1, t1), (a2, z2, _n2, t2) in zip(spans, spans[1:]):
        need(z1 <= a2, 'overlapping replacements %s / %s' % (t1, t2))
    out, pos = [], 0
    for a, z, new, tag in spans:
        out.append(text[pos:a])
        out.append(new)
        pos = z
    out.append(text[pos:])
    return ''.join(out)


def build_readme(v1, ts, fix_sha, E):
    rec, v0 = E['record'], E['v001']
    a, scan, n5 = E['r5'], E['out_scan'], E['n5']
    uvt = ', '.join(sorted(scan['uvt_path_components']))
    runs_n = scan['claude2_runs_path_tails']['A2_ANCHOR_F10_RUN_V001/result.json']
    runs_files = scan['files_with']['claude2/runs/']
    n_ngc = len(a['ngc3198_non_py_path_literals'])
    new_title = '# B0 r5 = r4 dry identity on the production M_s 128 set (RI-31), README V002\n'
    new_header = (
        'Claude4 helper, dispatch 0650, root entry A113 in V006. Folder `%s`. README V001 was written '
        '2026-10-19T03:30:50Z. This successor, README V002, was written %s in the FIX stage (ri31). Both stamps are '
        'from date -u.\n'
        '\n'
        '## Successor note (FIX stage, V002)\n'
        '\n'
        '- Why V002 exists: the refuter (stage refute_ri31, `%s`, sha256 `%s`) reported 0 BLOCKING findings and 1 '
        'SHOULD_FIX, R31-S1. R31-S1 says that one FORMAL sentence of README V001 about the driver sources is false as '
        'worded. The fix stage confirmed R31-S1 from the driver bytes (TESTED). V002 corrects that sentence and the FORMAL '
        'label line that depends on it. The fix stage also re-checked from bytes the facts behind refuter notes R31-N2, '
        'R31-N3 and R31-N5 (TESTED), and V002 narrows the two TESTED sentences they concern.\n'
        '- What did not change: **verdict_B0 = PASS_PLAN_IDENTICAL**. The record of the verdict, '
        '`out/B0_R5_VS_R4_MS128_C4V001.json` (sha256 `%s`), is unchanged, and it contains none of the corrected sentences '
        '(TESTED). The fix stage ran no driver, dry run, child process or `--validity-only`.\n'
        '- Evidence: `FIX_RI31_C4V002.json` (sha256 `%s`), written by `fix_c4v002/fix_ri31_c4v002.py`.\n'
        '- Files: nothing of record was overwritten. %d of the %d rows of `HASHES_B0_MS128_C4V001.txt` re-hash equal '
        '(TESTED). The remaining row is the progress log `PARTIAL.md`. The dispatch has the fix stage append to it, and its '
        'first %d bytes still hash to the V001 row `%s` (TESTED). `HASHES_B0_MS128_C4V002.txt`, written last, covers the '
        'folder as it now stands.\n'
        '- Changed from V001 (each marked "V002" below): the out/ scan bullet (R31-N2, R31-N3), the Scope bullet '
        '(R31-S1), the .log cross-check bullet (R31-N5), a new TESTED label line, the FORMAL label line, a new section on '
        'the refuter notes, and the Files section. All other V001 text is unchanged, and its labels stand.\n'
        '- Disclosure (fix stage): one exploratory dry-mode run of an earlier draft of the fix script wrote its stdout '
        'outside this folder, to the session scratchpad: `%s` (sha256 `%s`). That is a literal deviation from "write only '
        'inside your own output folder". It touched no lane or root file. Every later fix-stage write is inside this folder.'
    ) % (FOLDER, ts, REFUTER['REFUTE_RI31.md'][0], REFUTER['REFUTE_RI31.md'][1], rec['sha256'], fix_sha,
         v0['rows_equal'], v0['hashes_v001']['rows'], PARTIAL_V001_LEN, v0['partial_md']['v001_row_sha256'],
         E['deviation']['path'], E['deviation']['sha256'])
    new_scan = (
        '- Every file under `out/` was scanned after the run. V002: the fix stage re-counted the text of the %d out/ files '
        'that HASHES V001 lists (TESTED). No file contains runs_ext, C5H, rotmod, Vobs, MassModels, NGC3198 or /Volumes. '
        'SPARC occurs %d times, each time as a whole non-path row id of the form DDO154_SPARC12_nn (R31-N3). The only path '
        'components that start with uvt_ are uvt_*.py source modules (%s). Correction (R31-N2): by "run-tree", V001 meant '
        'the two CLAUDE2 runs_ext roots. `out/` does contain one CLAUDE2 runs path, '
        '`.../CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json`, %d times in %d files. Both drivers pin that path (driver '
        'line %d). It is not under runs_ext, and it is neither a UVT_* path nor a C5H path.'
    ) % (scan['files_scanned'], scan['occurrences']['sparc'], uvt, runs_n, runs_files,
         a['a2_anchor_result_path_lines'][0])
    new_scope = (
        "V002 correction (R31-S1): V001 said here that neither driver's source contains a runs_ext, C5H or target-word "
        'string. That is false as worded. The corrected statement below is TESTED by byte count, tokenizer and AST over '
        'both driver files, with identical results for r4 and r5. runs_ext, C5H and KMAX_A2F10 occur 0 times in each '
        'driver, and so do MassModels and SPARC. rotmod occurs twice and vobs once, each time as non-path text inside a '
        'string literal. Line 4580 is in the docstring of ngc_sources_summary ("The rotmod .dat named in the manifest '
        'provenance is NOT opened."). Line 4596 is the manifest key \'rotmod_header\' in ngc_sources_summary. Line 4560 is '
        "the element 'vobs' of the key-name hint tuple _VELOCITY_KEY_HINTS, which only _key_scan reads. This is "
        'NGC3198-only code (FORMAL, read from the AST call graph, which is TESTED). _key_scan is called only by itself and '
        'by ngc_sources_summary. ngc_sources_summary is called only by _ngc_collect, and _ngc_collect only by ngc_dry_run '
        'and ngc_run_blocked. cmd_dry_run and cmd_run call those two only under `%s`. In all 20 fresh reports the '
        'normalized spec is galaxy DDO154 with no config field, and no file in out/ contains NGC3198 (both TESTED). So '
        'that branch was not taken (FORMAL inference). Each driver also contains %d NGC3198 non-.py path literals: galaxy '
        'configs and inputs, NGC3198 source and reduction files, a target-free query manifest, and one probe-file name '
        'pattern. The full list is in the fix record. The fence classes all of them as NGC3198 data. None of them was '
        'opened in any child (TESTED: every BLOCKED list is empty; FORMAL: the fence refuses every Python open of a '
        'non-.py NGC3198 path, fence line 86).'
    ) % (NGC_GUARD, n_ngc)
    if n5['facts']['no_log_name_in_records']:
        log_pin = 'are neither named nor pinned by sha in'
    else:
        log_pin = 'are not pinned by sha in'
    new_logs = OLD_LOGS + (
        ' V002 note (R31-N5): these .log files %s BUILD_V005, BUILD_V006, BUILD_V007 or DRY_R5_MS128_V004.json (TESTED in '
        'the fix stage). This line is therefore a comparison against unpinned files, and the verdict does not use it.'
    ) % log_pin
    new_tested = OLD_TESTED + (
        '\n- TESTED in the fix stage (V002): the R31-S1 byte, token and AST evidence for both drivers; the ten specs\' '
        'schema and galaxy; the normalized spec, driver sha and executed_stages of the 20 fresh reports; the 21 fence '
        'summaries in out/logs; the out/ re-count; the .log pin search; the refuter-file shas; and the integrity of the '
        'V001 files.')
    new_formal = (
        '- FORMAL: that the dry-run path launches nothing, and that the fence does not cover stat or listdir. V002 '
        'replaces V001\'s "has no source references to forbidden trees" with this: the driver code that holds target '
        'words is NGC3198-only and is not reached for these DDO154 specs. The drivers do contain target words as non-path '
        'text, and NGC3198 path literals (see Scope).')
    notes = (
        '\n## Refuter notes (V002)\n'
        '\n'
        '- R31-N1: the refuter re-derived PASS_PLAN_IDENTICAL from bytes. No action.\n'
        '- R31-N2, R31-N3 and R31-N5: re-checked from bytes and carried into the scan, Scope and .log bullets above.\n'
        '- R31-N4: in the fence, `_hook` runs `real = os.path.realpath(lit)` (fence line 135) before `_forbidden_read` '
        '(line 136). So, as the refuter says, the runs_ext probes in each fenced child also lstat the CLAUDE2 runs_ext root '
        'entry (line text TESTED, effect FORMAL). No C5H path and no UVT_* run output is touched. Changing this needs a new '
        'fence version, so no action here.\n'
        '- R31-N6: README V001 and HASHES V001 were written through a helper in the session scratchpad that was not kept, '
        'so their exclusive creation is UNTESTED. The fix-stage script is kept in `fix_c4v002/` and listed in HASHES V002. '
        'One fix-stage capture went outside the folder; see the disclosure in the successor note.\n'
        '- R31-N7: the runner\'s `except SystemExit` handler (runner line %d) keeps only an int exit code and drops a text '
        'message (FORMAL). Per the refuter, both drivers exit with int codes (FORMAL), and all 20 driver stderrs are empty '
        '(TESTED here). So it had no effect. No action.\n'
        '- R31-N8: per the refuter, the equal batch-1 timings are real. No action.\n'
    ) % E['aux']['r31_n7_runner_lines']['except_line']
    new_files = (
        '- `PARTIAL.md` (progress log; the fix-stage lines come after byte %d), `README_B0_MS128_C4V001.md` (V001, '
        'unchanged), this README V002, and `HASHES_B0_MS128_C4V001.txt` (the V001 state, unchanged).\n'
        '- V002, fix stage: `FIX_RI31_C4V002.json` (the fix record); `fix_c4v002/fix_ri31_c4v002.py` (the fix script, with '
        'modes dry, write, hashes and verify); `fix_c4v002/dry_stdout_c4v002.txt` and `fix_c4v002/write_stdout_c4v002.txt` '
        '(its captured output); and `HASHES_B0_MS128_C4V002.txt`, written last, which lists every other file in the folder.'
    ) % PARTIAL_V001_LEN
    reps = [('title', OLD_TITLE, new_title), ('header', OLD_HEADER, new_header), ('scan', OLD_SCAN, new_scan),
            ('scope', OLD_SCOPE, new_scope), ('logs', OLD_LOGS, new_logs), ('tested', OLD_TESTED, new_tested),
            ('formal', OLD_FORMAL, new_formal), ('notes', OLD_FILES_HEAD, notes + OLD_FILES_HEAD),
            ('files', OLD_FILES, new_files)]
    return apply_reps(v1, reps)


def v001_locations(v1, partial_prefix):
    locs = []
    for tag, old in (('scope_S1', OLD_SCOPE), ('formal_label_S1', 'has no source references to forbidden trees'),
                     ('scan_N2', OLD_SCAN), ('logs_N5', OLD_LOGS)):
        need(v1.count(old) == 1, 'README V001: %s found %d times' % (tag, v1.count(old)))
        locs.append({'tag': tag, 'file': README_V001, 'line': line_of(v1, v1.index(old)), 'text': old})
    need(partial_prefix.count(OLD_PARTIAL_S1) == 1, 'PARTIAL.md V001 prefix: S1 text')
    locs.append({'tag': 'partial_S1', 'file': PARTIAL + ' (first 1322 bytes, the V001 state)',
                 'line': line_of(partial_prefix, partial_prefix.index(OLD_PARTIAL_S1)), 'text': OLD_PARTIAL_S1})
    return locs


CITATION = ("Neither driver contains the string runs_ext or the C5H run name (0 each, r4 and r5). Target words occur only as "
            "non-path text in NGC3198-only code: rotmod twice (line 4580, docstring of ngc_sources_summary; line 4596, the "
            "manifest key 'rotmod_header') and vobs once (line 4560, _VELOCITY_KEY_HINTS, read only by _key_scan); "
            "MassModels and SPARC 0. That code is reached only under nspec.get('config') == 'NGC3198_C2V002', which none "
            "of the ten DDO154 specs takes. The drivers also hold NGC3198 non-.py path literals; none was opened in any of "
            "the 20 fenced children (every BLOCKED list empty).")


def gather(mode):
    E = {}
    E['pins'], E['aux'] = check_pins()
    E['v001'], rowmap = check_v001(mode)
    record, E['record'] = check_record(rowmap)
    E['cases'], E['specs'] = check_specs(record, rowmap)
    E['fence_logs'] = check_fence_logs(E['cases'])
    b4, b5 = rb(R4[0]), rb(R5[0])
    need(sha_b(b4) == R4[1] and sha_b(b5) == R5[1], 'drivers changed during the run')
    E['r4'], E['r5'] = analyze_driver(b4), analyze_driver(b5)
    E['r4_equals_r5'] = dict((k, E['r4'][k] == E['r5'][k]) for k in E['r4'])
    E['s1_facts'] = {'r4': s1_facts(E['r4']), 'r5': s1_facts(E['r5'])}
    E['out_scan'] = out_scan(rowmap)
    E['out_scan_facts'] = scan_facts(E['out_scan'])
    n5 = n5_check(E['cases'])
    n5['facts'] = n5_facts(n5)
    E['n5'] = n5
    v1b = rb(README_V001)
    need(sha_b(v1b) == rowmap[README_V001], 'README V001 differs from its HASHES V001 row')
    E['readme_v001'] = {'path': README_V001, 'sha256': sha_b(v1b)}
    E['v001_text'] = v1b.decode('utf-8')
    E['locations'] = v001_locations(E['v001_text'], rb(PARTIAL)[:PARTIAL_V001_LEN].decode('utf-8'))
    dv = rb(DEVIATION_PATH)
    E['deviation'] = {'what': ('stdout of one exploratory dry-mode run of an earlier draft of this script, written by the '
                               'shell to the session scratchpad, outside the folder (dry mode itself writes nothing)'),
                      'path': DEVIATION_PATH, 'sha256': sha_b(dv), 'bytes': len(dv),
                      'touched_lane_or_root_file': False, 'deleted_or_moved': False}
    return E


def verdict_ok(E):
    bad = []
    for side in ('r4', 'r5'):
        bad += ['s1:%s:%s' % (side, k) for k, v in E['s1_facts'][side].items() if not v]
    bad += ['r4_equals_r5:%s' % k for k, v in E['r4_equals_r5'].items() if not v]
    bad += ['out_scan:%s' % k for k, v in E['out_scan_facts'].items() if not v]
    bad += ['n5:%s' % k for k, v in E['n5']['facts'].items() if k != 'no_log_name_in_records' and not v]
    return bad


def build_fix(E, ts):
    a = E['r5']
    s1 = {
        'severity': 'SHOULD_FIX', 'status': 'CONFIRMED_FROM_BYTES',
        'claim_v001_locations': E['locations'][:2] + E['locations'][4:],
        'other_location_not_in_folder': "builder structured finding RI31-N4 (same wording, per the refuter)",
        'evidence_label': ('TESTED: byte counts, tokenizer and AST of both driver files, the ten specs, the 20 fresh '
                           'reports and the 21 fence summaries. FORMAL: what the call graph implies about reachability.'),
        'facts': E['s1_facts'],
        'driver_evidence': {'r4': {'path': R4[0], 'sha256': R4[1]}, 'r5': {'path': R5[0], 'sha256': R5[1]},
                            'r4_equals_r5': E['r4_equals_r5'], 'r5_analysis': a},
        'ten_specs': E['specs'],
        'fence_logs': E['fence_logs'],
        'citation_wording': CITATION,
        'fixed_in': ['README_B0_MS128_C4V002.md: Scope bullet and FORMAL label line (successor; V001 left unchanged)',
                     'PARTIAL.md: a correction line appended after this record is written'],
        'verdict_effect': ('none. verdict_B0 rests on root compare() and the B0-EMPTY rule over the 20 fenced dry runs; '
                           'the corrected sentence is a FORMAL coverage note.'),
    }
    findings = {
        'R31-S1': s1,
        'R31-N1': {'severity': 'NOTE', 'status': 'ACKNOWLEDGED', 'action': 'none (confirmation)'},
        'R31-N2': {'severity': 'NOTE', 'status': 'RE-CHECKED_TESTED',
                   'action': 'README V002 scan bullet: "no runs_ext path"; the CLAUDE2/runs A2 anchor result path is named',
                   'claim_v001_location': E['locations'][2], 'out_scan': E['out_scan'], 'facts': E['out_scan_facts']},
        'R31-N3': {'severity': 'NOTE', 'status': 'RE-CHECKED_TESTED',
                   'action': 'README V002 scan bullet names the DDO154_SPARC12_nn row ids',
                   'sparc_occurrences': E['out_scan']['occurrences']['sparc'],
                   'sparc_whole_row_ids': E['out_scan']['sparc_whole_row_ids']},
        'R31-N4': {'severity': 'NOTE', 'status': 'ACKNOWLEDGED (fence line text TESTED, effect FORMAL)',
                   'action': 'none here; needs a new fence version', 'fence_lines': E['aux']['r31_n4_fence_lines']},
        'R31-N5': {'severity': 'NOTE', 'status': 'RE-CHECKED_TESTED',
                   'action': 'README V002 calls the .log identity a comparison against unpinned files',
                   'claim_v001_location': E['locations'][3], 'n5': E['n5']},
        'R31-N6': {'severity': 'NOTE', 'status': 'ACKNOWLEDGED',
                   'action': 'the fix stage keeps its script under fix_c4v002/ (listed in HASHES V002)'},
        'R31-N7': {'severity': 'NOTE', 'status': 'ACKNOWLEDGED (runner line text TESTED, effect FORMAL)',
                   'action': 'none; needs a new pinned runner', 'runner_lines': E['aux']['r31_n7_runner_lines']},
        'R31-N8': {'severity': 'NOTE', 'status': 'ACKNOWLEDGED', 'action': 'none'},
    }
    return {
        'schema': 'FIX_RI31_C4V002',
        'stage': 'fix_ri31', 'dispatch': '0650', 'root_entry': 'A113 (V006)', 'lane': 'Claude4 helper',
        'written_utc': ts, 'written_utc_source': 'date -u, taken immediately before the write call',
        'folder': FOLDER,
        'script': {'path': SCRIPT, 'sha256': sha_b(rb(SCRIPT))},
        'interpreter': {'executable': sys.executable, 'version': sys.version.split()[0], 'isolated': sys.flags.isolated,
                        'dont_write_bytecode': sys.dont_write_bytecode,
                        'thread_env': dict((k, os.environ.get(k)) for k in THREAD_ENV)},
        'refuter': {'stage': 'refute_ri31', 'reported': '0 BLOCKING, 1 SHOULD_FIX (R31-S1), 8 NOTE; verdict CONFIRMED '
                    'PASS_PLAN_IDENTICAL (as given in the dispatch text)',
                    'files': dict((k, E['pins']['refuter_' + k]) for k in REFUTER)},
        'pins': E['pins'],
        'verdict_B0_unchanged': E['record'],
        'v001_integrity': E['v001'],
        'readme_v001': E['readme_v001'],
        'findings': findings,
        'successors': {'README_B0_MS128_C4V001.md': 'README_B0_MS128_C4V002.md (its sha256 is in HASHES_B0_MS128_C4V002)',
                       'HASHES_B0_MS128_C4V001.txt': 'HASHES_B0_MS128_C4V002.txt (written last)',
                       'out/B0_R5_VS_R4_MS128_C4V001.json': 'unchanged; no successor needed'},
        'deviations': [E['deviation']],
        'not_done': ['no driver import or run, no dry run, no child process, no --validity-only',
                     'no file overwritten, deleted or moved; no network; no write outside the folder except the one '
                     'disclosed in deviations',
                     'no recursive content search; contents read only from named files (pins, HASHES V001 rows, '
                     'registry specs, the ten .log files, BUILD_V005-7, DRY_R5_MS128_V004.json)'],
        'labels': {'TESTED': 'run on bytes in this script', 'FORMAL': 'source reading (reachability, fence and runner '
                   'effects)', 'UNTESTED': 'how README V001 / HASHES V001 were created (R31-N6)'},
        'guard_before_write': guard_summary(),
    }


def summary_for_print(E):
    return {'pins': dict((k, v['sha256']) for k, v in E['pins'].items()),
            'v001': {'hashes_v001': E['v001']['hashes_v001'], 'rows_equal': E['v001']['rows_equal'],
                     'partial_md': E['v001']['partial_md'], 'fix_stage_files': E['v001']['fix_stage_files_present']},
            'record': {k: E['record'][k] for k in ('sha256', 'verdict_B0', 'counted_comparisons', 'n_pass')},
            'specs': dict((c, [v['galaxy'], v['schema'], v['reports']['R4']['normalized_has_config_field'],
                               v['reports']['R5']['normalized_has_config_field']]) for c, v in E['specs'].items()),
            'fence_logs_ok': len(E['fence_logs']),
            's1_facts': E['s1_facts'], 'r4_equals_r5': E['r4_equals_r5'],
            'r5_counts': E['r5']['counts'], 'r5_line_hits': E['r5']['line_hits'], 'r5_tokens': E['r5']['tokens'],
            'r5_consts': E['r5']['consts'], 'r5_chain': E['r5']['chain'], 'r5_defs': E['r5']['defs'],
            'r5_config_consts': E['r5']['config_NGC3198_C2V002_constants'],
            'r5_ngc_paths': E['r5']['ngc3198_non_py_path_literals'],
            'r5_a2_lines': E['r5']['a2_anchor_result_path_lines'],
            'out_scan': E['out_scan'], 'out_scan_facts': E['out_scan_facts'],
            'n5': E['n5'], 'locations': E['locations'], 'aux': E['aux']}


def do_fix(mode, ts):
    E = gather(mode)
    print(json.dumps(summary_for_print(E), indent=1))
    bad = verdict_ok(E)
    need(not bad, 'facts behind the V002 wording do not hold: %r' % bad)
    fix = build_fix(E, ts)
    fix_bytes = (json.dumps(fix, indent=1, ensure_ascii=True) + '\n').encode('utf-8')
    fix_sha = sha_b(fix_bytes)
    readme_bytes = build_readme(E['v001_text'], ts, fix_sha, E).encode('utf-8')
    readme_sha = sha_b(readme_bytes)
    print('FIX_RECORD_SHA256 %s (%d bytes)' % (fix_sha, len(fix_bytes)))
    print('README_V002_SHA256 %s (%d bytes)' % (readme_sha, len(readme_bytes)))
    if mode == 'dry':
        print('----- README V002 (dry, not written) -----')
        print(readme_bytes.decode('utf-8'))
        print('DRY OK: nothing written. guard %s' % json.dumps(guard_summary()))
        return 0
    with open(OUT_FIX, 'xb') as f:
        f.write(fix_bytes)
    with open(OUT_README, 'xb') as f:
        f.write(readme_bytes)
    need(sha_b(rb(OUT_FIX)) == fix_sha and sha_b(rb(OUT_README)) == readme_sha, 'read-back mismatch')
    print('WROTE %s %s' % (fix_sha, OUT_FIX))
    print('WROTE %s %s' % (readme_sha, OUT_README))
    print('guard %s' % json.dumps(guard_summary()))
    return 0


def do_hashes(ts):
    v001, _rowmap = check_v001('hashes')
    files = []
    for d, dirs, fs in os.walk(FOLDER):
        for n in fs:
            q = os.path.join(d, n)
            if q != OUT_HASHES:
                files.append(q)
    files.sort()
    rows = [(sha_b(rb(q)), q) for q in files]
    header = ('# HASHES_B0_MS128_C4V002: sha256 of every file in %s except this file (written last, %s). Successor of '
              'HASHES_B0_MS128_C4V001.txt (sha256 %s), which still holds for the V001 state: every V001 row re-hashes '
              'equal except PARTIAL.md, which the fix stage appended to; its first %d bytes still hash to the V001 row.'
              % (FOLDER, ts, v001['hashes_v001']['sha256'], PARTIAL_V001_LEN))
    body = (header + '\n' + ''.join('%s  %s\n' % r for r in rows)).encode('utf-8')
    with open(OUT_HASHES, 'xb') as f:
        f.write(body)
    need(rb(OUT_HASHES) == body, 'read-back mismatch')
    print(json.dumps({'hashes_v002': OUT_HASHES, 'sha256': sha_b(body), 'rows': len(rows),
                      'v001_rows_equal': v001['rows_equal'], 'v001_rows': v001['hashes_v001']['rows'],
                      'partial_prefix_equals_v001_row': v001['partial_md']['prefix_equals_v001_row'],
                      'partial_md_now': [v001['partial_md']['len_now'], v001['partial_md']['sha256_now']],
                      'guard': guard_summary()}, indent=1))
    return 0


def do_verify():
    v001, _rowmap = check_v001('verify')
    lines = rb(OUT_HASHES).decode('utf-8').split('\n')
    need(lines[0].startswith('# HASHES_B0_MS128_C4V002: '), 'HASHES V002 header')
    rows = [l.split('  ', 1) for l in lines[1:] if l]
    bad = [p for s, p in rows if sha_b(rb(p)) != s]
    listed = set(p for s, p in rows)
    present = set()
    for d, dirs, fs in os.walk(FOLDER):
        for n in fs:
            present.add(os.path.join(d, n))
    missing = sorted(present - listed - {OUT_HASHES})
    extra = sorted(listed - present)
    print(json.dumps({'hashes_v002_sha256': sha_b(rb(OUT_HASHES)), 'rows': len(rows), 'rows_bad': bad,
                      'files_not_listed': missing, 'rows_without_file': extra, 'v001_rows_equal': v001['rows_equal'],
                      'partial_prefix_equals_v001_row': v001['partial_md']['prefix_equals_v001_row'],
                      'guard': guard_summary()}, indent=1))
    need(not bad and not missing and not extra, 'HASHES V002 does not verify')
    print('VERIFY OK')
    return 0


def main(argv):
    need(len(argv) >= 1 and argv[0] in ('dry', 'write', 'hashes', 'verify'), 'usage: dry|write|hashes --ts STAMP, verify')
    mode = argv[0]
    ts = None
    if mode != 'verify':
        need(len(argv) == 3 and argv[1] == '--ts' and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', argv[2]) is not None,
             'usage: %s --ts STAMP' % mode)
        ts = argv[2]
    need(SCRIPT == FIXDIR + '/fix_ri31_c4v002.py', 'script location %s' % SCRIPT)
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode, 'run with python3 -I -B')
    need(all(os.environ.get(k) == '1' for k in THREAD_ENV), 'single-thread env not set')
    sys.addaudithook(_hook)
    if mode == 'hashes':
        return do_hashes(ts)
    if mode == 'verify':
        return do_verify()
    return do_fix(mode, ts)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
