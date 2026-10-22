# Claude4 converter (dispatch 0650, V006 A113 P6; A59, A67 N1, A81 RI-21): turn the raw output of the identity comparator slot
# c2v007r2 (run_identity_compare_c2v007.py 052da0fe, gate Z2, on the R5_V001 Z2 identity run) into seal tool 4's B7 input
#   {"schema": CUSTODY_SCHEMA, "identity_run": "Z2", "driver_sha256", "stages_total", "stages_successor", "verdict": "PASS",
#    "method", "evidence": [{path, sha256}], "note"}
# by exclusive create (open 'x'). It REFUSES (exit 2, nothing written) when any stage lacks its successor, the run is not Z2, the
# driver is not the driver slot, or any input is malformed. Root runs it (A113), since its inputs come from a UVT_* run comparison.
# What it reads: the comparator report (--report, pinned by --report-sha256), the Z2 identity gate record of record (pinned), that
# record's report of record (pinned by the record), the comparator source, the tokens file and the driver source (bytes hashed; the
# driver is read as AST only, never imported or executed). It never opens, lists or stats a run directory: run paths are compared as
# strings only.
# Successor rule (A59 replace mode, as the comparator's planned_script plans gate Z2, from the driver slot's own tables): a stage is
# a successor stage only when its request script (script_sha256) equals the planned script (planned_sha256) AND that script is
#   SCRIPTS_UVT[kind] for the eight UVT_TAIL_KINDS (and is not the base SCRIPTS[kind]);
#   RO1_ROUTE_A worker or worker_parallel for kind route_a (and not a base route-A worker);
#   AUX_UVT manifest_writer for kind route_a_tail_manifest.
# Any other kind has no successor in the driver and refuses. stages_total is the run's own stage set (STAGE_SET.order_new); every
# stage must carry its SCRIPT_CUSTODY row.
# usage (one flag each, exact spelling, no --flag=value):
#   python3 -I -B make_custody_record_c4v001.py --report R.json --report-sha256 H --identity-record B1.json
#       --identity-record-sha256 H --driver-sha256 H --out OUT.json [--dry-run]
import ast, hashlib, json, os, re, stat, sys
from pathlib import Path

TOOL4 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/build_seal_record_c4v004.py',
         '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41')
COMPARATOR = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py',
              '052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e')     # prereg r6 seal_slots.identity_comparator c2v007r2
REPORT_SCHEMA = 'RUN_IDENTITY_COMPARE_C2V007'
GATE_RECORD_SCHEMA = 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'
SCRIPT_CUSTODY_RULE_Z2 = 'A59: every new stage runs the driver-planned script for gate Z2, hashed from bytes'   # comparator L2346
Z2_HEAD = {'gate': 'Z2', 'tail_on': True, 'ro1_requirement': 'ARMED', 'declared_tail_off_records': False}        # comparator GATES['Z2']
ROW_KEYS = {'kind', 'script_sha256', 'planned_sha256', 'ok'}                                                    # comparator L2343
TABLES = ('SCRIPTS', 'SCRIPTS_UVT', 'RO1_ROUTE_A', 'AUX_UVT', 'PARALLEL_ROUTE_A', 'UVT_TAIL_KINDS')
MUTATORS = {'update', 'setdefault', 'pop', 'popitem', 'clear', '__setitem__', '__delitem__', 'append', 'extend', 'insert', 'remove'}
HEX64 = re.compile(r'[0-9a-f]{64}')
FLAGS_VALUE = ('--report', '--report-sha256', '--identity-record', '--identity-record-sha256', '--driver-sha256', '--out')
FLAGS_BOOL = ('--dry-run',)


class Refuse(Exception):
    def __init__(self, code, detail=''):
        super().__init__('%s: %s' % (code, detail))
        self.code = code


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise Refuse('JSON_DUPLICATE_KEY', repr(k)[:80])
        out[k] = v
    return out


def no_constant(c):
    raise Refuse('JSON_NON_FINITE_CONSTANT', c)


def regular_file_bytes(path, code):
    p = str(path)
    if not os.path.isabs(p):
        raise Refuse(code, 'not an absolute path: %s' % p)
    try:
        st = os.lstat(p)
    except OSError as e:
        raise Refuse(code, 'cannot stat %s (%s)' % (p, type(e).__name__))
    if not stat.S_ISREG(st.st_mode):
        raise Refuse(code, 'not a regular file (or a symlink): %s' % p)
    return Path(p).read_bytes()


def pinned(path, sha, code):
    raw = regular_file_bytes(path, code)
    got = sha_bytes(raw)
    if not (isinstance(sha, str) and HEX64.fullmatch(sha)) or got != sha:
        raise Refuse(code, '%s hashes to %s, pinned %r' % (path, got, sha))
    return raw


def strict_json(raw, code):
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=no_constant)
    except Refuse as e:
        raise Refuse(code, e.code)
    except (UnicodeDecodeError, ValueError) as e:
        raise Refuse(code, type(e).__name__)


def module_string(raw, name):
    vals = [n.value.value for n in ast.parse(raw.decode('utf-8')).body if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name and isinstance(n.value, ast.Constant)
            and isinstance(n.value.value, str)]
    if len(vals) != 1:
        raise Refuse('TOOL4_CONSTANT', name)
    return vals[0]


def driver_tables(raw):
    """the successor tables of the driver, read from its bytes as AST (no code executed); each table must be assigned exactly once at
    module level, as a literal, and never mutated anywhere in the module"""
    try:
        tree = ast.parse(raw.decode('utf-8'))
    except (UnicodeDecodeError, SyntaxError) as e:
        raise Refuse('DRIVER_NOT_PARSABLE', type(e).__name__)
    binds = {k: [] for k in TABLES}
    for node in ast.walk(tree):
        tgts = []
        if isinstance(node, (ast.Assign, ast.Delete)):
            tgts = node.targets
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            tgts = [node.target]
        for t in tgts:
            for n in ast.walk(t):
                if isinstance(n, ast.Name) and n.id in TABLES:
                    binds[n.id].append(node)
                if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id in TABLES:
                    raise Refuse('DRIVER_TABLES_NOT_STATIC', 'item assignment to %s at line %d' % (n.value.id, node.lineno))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) \
                and node.func.value.id in TABLES and node.func.attr in MUTATORS:
            raise Refuse('DRIVER_TABLES_NOT_STATIC', '%s.%s at line %d' % (node.func.value.id, node.func.attr, node.lineno))
        if isinstance(node, (ast.Global, ast.Nonlocal)) and set(node.names) & set(TABLES):
            raise Refuse('DRIVER_TABLES_NOT_STATIC', 'global rebinding at line %d' % node.lineno)
    out = {}
    for name in TABLES:
        nodes = binds[name]
        if len(nodes) != 1 or nodes[0] not in tree.body or not isinstance(nodes[0], ast.Assign) or len(nodes[0].targets) != 1 \
                or not isinstance(nodes[0].targets[0], ast.Name):
            raise Refuse('DRIVER_TABLES_NOT_STATIC', '%s is bound %d time(s), or not by one module-level assignment' % (name, len(nodes)))
        v = nodes[0].value
        if name == 'UVT_TAIL_KINDS':
            if not (isinstance(v, ast.Tuple) and v.elts and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in v.elts)):
                raise Refuse('DRIVER_TABLE_SHAPE', name)
            kinds = [e.value for e in v.elts]
            if len(set(kinds)) != len(kinds):
                raise Refuse('DRIVER_TABLE_SHAPE', '%s repeats a kind' % name)
            out[name] = tuple(kinds)
            continue
        if not isinstance(v, ast.Dict) or any(k is None for k in v.keys):
            raise Refuse('DRIVER_TABLE_SHAPE', name)
        tab = {}
        for k, e in zip(v.keys, v.values):
            if not (isinstance(k, ast.Constant) and isinstance(k.value, str)) or k.value in tab:
                raise Refuse('DRIVER_TABLE_SHAPE', '%s key at line %d' % (name, getattr(k, 'lineno', 0)))
            if not (isinstance(e, ast.Tuple) and len(e.elts) == 2 and isinstance(e.elts[1], ast.Constant)
                    and isinstance(e.elts[1].value, str) and HEX64.fullmatch(e.elts[1].value)):
                raise Refuse('DRIVER_TABLE_SHAPE', '%s[%s] is not (path, sha256)' % (name, k.value))
            tab[k.value] = e.elts[1].value
        out[name] = tab
    for kind in out['UVT_TAIL_KINDS']:
        if kind not in out['SCRIPTS_UVT'] or kind not in out['SCRIPTS']:
            raise Refuse('DRIVER_TABLE_SHAPE', 'UVT kind %s lacks SCRIPTS_UVT or SCRIPTS' % kind)
        if out['SCRIPTS_UVT'][kind] == out['SCRIPTS'][kind]:
            raise Refuse('DRIVER_TABLE_SHAPE', 'SCRIPTS_UVT[%s] is its base' % kind)
    for need, key in (('RO1_ROUTE_A', 'worker'), ('RO1_ROUTE_A', 'worker_parallel'), ('AUX_UVT', 'manifest_writer'), ('SCRIPTS', 'route_a'),
                      ('PARALLEL_ROUTE_A', 'worker')):
        if key not in out[need]:
            raise Refuse('DRIVER_TABLE_SHAPE', '%s lacks %s' % (need, key))
    return out


def classify(name, row, tabs):
    """the successor class of one SCRIPT_CUSTODY row, or Refuse"""
    if not (isinstance(row, dict) and set(row) == ROW_KEYS):
        raise Refuse('STAGE_ROW_MALFORMED', '%s: keys must be exactly %s' % (name, sorted(ROW_KEYS)))
    s, p, ok, kind = row['script_sha256'], row['planned_sha256'], row['ok'], row['kind']
    if ok is not True or not (isinstance(s, str) and HEX64.fullmatch(s)) or s != p:
        raise Refuse('STAGE_NOT_ON_ITS_PLANNED_SCRIPT', '%s (ok %r; ran %r; planned %r)' % (name, ok, s, p))
    if not isinstance(kind, str):
        raise Refuse('STAGE_KIND_HAS_NO_SUCCESSOR', '%s kind %r' % (name, kind))
    if kind in tabs['UVT_TAIL_KINDS']:
        if s != tabs['SCRIPTS_UVT'][kind] or s == tabs['SCRIPTS'][kind]:
            raise Refuse('STAGE_NOT_ON_ITS_SUCCESSOR', '%s kind %s ran %s; its successor SCRIPTS_UVT[%s] is %s' % (name, kind, s, kind, tabs['SCRIPTS_UVT'][kind]))
        return 'SCRIPTS_UVT'
    if kind == 'route_a':
        base = {tabs['SCRIPTS']['route_a'], tabs['PARALLEL_ROUTE_A']['worker']}
        if s not in (tabs['RO1_ROUTE_A']['worker'], tabs['RO1_ROUTE_A']['worker_parallel']) or s in base:
            raise Refuse('STAGE_NOT_ON_ITS_SUCCESSOR', '%s (route_a) ran %s, not an RO1 tail route-A worker of the driver slot' % (name, s))
        return 'RO1_ROUTE_A'
    if kind == 'route_a_tail_manifest':
        if s != tabs['AUX_UVT']['manifest_writer']:
            raise Refuse('STAGE_NOT_ON_ITS_SUCCESSOR', '%s (route_a_tail_manifest) ran %s, not AUX_UVT manifest_writer' % (name, s))
        return 'AUX_UVT_MANIFEST_WRITER'
    raise Refuse('STAGE_KIND_HAS_NO_SUCCESSOR', '%s kind %r: no successor exists in the driver for this kind' % (name, kind))


def check(report, ok, code, detail=''):
    if not ok:
        raise Refuse(code, detail)


def get_check(rep, name):
    c = (rep.get('checks') or {}).get(name) if isinstance(rep.get('checks'), dict) else None
    if not (isinstance(c, dict) and set(c) == {'pass', 'detail'} and isinstance(c['pass'], bool)):
        raise Refuse('CHECK_MISSING_OR_MALFORMED', name)
    if c['pass'] is not True:
        raise Refuse('CHECK_NOT_PASS', name)
    return c['detail']


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and os.path.isabs(x['path']) \
        and isinstance(x['sha256'], str) and bool(HEX64.fullmatch(x['sha256']))


def custody_view(rep):
    """the sections whose equality ties a re-run to the report of record"""
    keys = ('schema', 'gate', 'driver_selected', 'driver_pin', 'comparator', 'reference', 'new', 'tokens', 'verdict', 'failing')
    v = {k: rep.get(k) for k in keys}
    v['checks'] = {k: (rep.get('checks') or {}).get(k) for k in ('SCRIPT_CUSTODY', 'NEW_DRIVER_PIN', 'STAGE_SET')}
    return json.dumps(v, sort_keys=True)


def under(p, root):
    p, root = os.path.normpath(p), os.path.normpath(root)
    return p == root or p.startswith(root.rstrip('/') + '/')


def build(a):
    me = Path(__file__).resolve()
    me_raw = me.read_bytes()
    t4 = pinned(TOOL4[0], TOOL4[1], 'TOOL4_PIN')
    schema = module_string(t4, 'CUSTODY_SCHEMA')
    dsha = a['--driver-sha256']
    check(None, isinstance(dsha, str) and bool(HEX64.fullmatch(dsha)), 'DRIVER_SHA_FORMAT', repr(dsha)[:80])
    out = a['--out']
    check(None, os.path.isabs(out), 'OUT_NOT_ABSOLUTE', out)
    check(None, not os.path.lexists(out), 'OUT_EXISTS', out)
    check(None, os.path.isdir(os.path.dirname(out)), 'OUT_PARENT_MISSING', os.path.dirname(out))
    # ---- the comparator report (raw output)
    rraw = pinned(a['--report'], a['--report-sha256'], 'REPORT_PIN_MISMATCH')
    rep = strict_json(rraw, 'REPORT_JSON')
    check(rep, isinstance(rep, dict), 'REPORT_SHAPE', 'not a JSON object')
    check(rep, rep.get('schema') == REPORT_SCHEMA, 'REPORT_SCHEMA', repr(rep.get('schema'))[:80])
    check(rep, rep.get('gate') == 'Z2', 'RUN_NOT_Z2', repr(rep.get('gate'))[:40])
    for k, v in Z2_HEAD.items():
        check(rep, rep.get(k) == v and type(rep.get(k)) is type(v), 'RUN_NOT_Z2_SEMANTICS', '%s = %r' % (k, rep.get(k)))
    check(rep, rep.get('comparator') == {'path': COMPARATOR[0], 'sha256': COMPARATOR[1]} and rep.get('comparator_sha256_at_end') == COMPARATOR[1],
          'COMPARATOR_NOT_C2V007R2', repr(rep.get('comparator'))[:200])
    cmp_raw = pinned(COMPARATOR[0], COMPARATOR[1], 'COMPARATOR_NOT_C2V007R2')
    dp = rep.get('driver_pin')
    check(rep, isinstance(dp, list) and len(dp) == 2 and all(isinstance(x, str) for x in dp), 'REPORT_SHAPE', 'driver_pin')
    check(rep, dp[1] == dsha, 'DRIVER_NOT_THE_SLOT', 'the report ran driver %s; the driver slot is %s' % (dp[1], dsha))
    drv_raw = pinned(dp[0], dsha, 'DRIVER_BYTES_NOT_THE_SLOT')
    tabs = driver_tables(drv_raw)
    check(rep, rep.get('verdict') == 'PASS_BITWISE_EQUAL' and rep.get('failing') == [], 'COMPARISON_NOT_PASS',
          '%r, failing %r' % (rep.get('verdict'), rep.get('failing')))
    checks = rep.get('checks')
    check(rep, isinstance(checks, dict) and checks and all(isinstance(c, dict) and c.get('pass') is True for c in checks.values()),
          'COMPARISON_NOT_PASS', 'a check does not pass')
    tok = rep.get('tokens')
    check(rep, is_pin(tok), 'REPORT_SHAPE', 'tokens')
    tok_raw = pinned(tok['path'], tok['sha256'], 'TOKENS_PIN_MISMATCH')
    for k in ('new', 'reference'):
        check(rep, isinstance(rep.get(k), str) and os.path.isabs(rep[k]), 'REPORT_SHAPE', k)
    check(rep, not under(out, rep['new']) and not under(out, rep['reference']), 'OUT_INSIDE_A_COMPARED_RUN', out)
    ndp = get_check(rep, 'NEW_DRIVER_PIN')
    check(rep, isinstance(ndp, dict) and ndp.get('pin') == dp and ndp.get('start_json') == dp and ndp.get('result_json_driver_sha256') == dsha,
          'NEW_DRIVER_PIN_NOT_THE_SLOT', repr(ndp)[:300])
    sset = get_check(rep, 'STAGE_SET')
    order = sset.get('order_new') if isinstance(sset, dict) else None
    check(rep, isinstance(order, list) and order and all(isinstance(x, str) and x for x in order) and len(set(order)) == len(order)
          and sset.get('new_problems') == [], 'STAGE_SET_MALFORMED', 'order_new must be a non-empty list of distinct stage names, no problems')
    sc = get_check(rep, 'SCRIPT_CUSTODY')
    check(rep, isinstance(sc, dict) and sc.get('rule') == SCRIPT_CUSTODY_RULE_Z2, 'SCRIPT_CUSTODY_RULE', repr(sc.get('rule') if isinstance(sc, dict) else sc)[:200])
    check(rep, sc.get('violations') == [], 'SCRIPT_CUSTODY_VIOLATIONS', repr(sc.get('violations'))[:300])
    rows = sc.get('stages')
    check(rep, isinstance(rows, dict), 'SCRIPT_CUSTODY_MALFORMED', 'stages')
    missing, extra = [x for x in order if x not in rows], [x for x in rows if x not in order]
    check(rep, not missing, 'STAGE_WITHOUT_CUSTODY_ROW', ', '.join(missing))
    check(rep, not extra, 'CUSTODY_ROW_FOR_NO_STAGE', ', '.join(extra))
    classes = {}
    for name in order:
        cl = classify(name, rows[name], tabs)
        classes.setdefault(cl, []).append(name)
    n_succ = sum(len(v) for v in classes.values())
    check(rep, n_succ == len(order), 'STAGE_LACKS_ITS_SUCCESSOR', '%d of %d' % (n_succ, len(order)))
    # ---- the Z2 identity gate record of record, and its report of record
    rec_raw = pinned(a['--identity-record'], a['--identity-record-sha256'], 'RECORD_PIN_MISMATCH')
    rec = strict_json(rec_raw, 'RECORD_JSON')
    ic = rec.get('identity_comparison') if isinstance(rec, dict) else None
    run = rec.get('run') if isinstance(rec, dict) else None
    check(rec, isinstance(rec, dict) and rec.get('schema') == GATE_RECORD_SCHEMA and rec.get('gate') == 'B1' and rec.get('tail') == 'ON'
          and isinstance(ic, dict) and ic.get('gate') == 'Z2' and isinstance(run, dict), 'RECORD_NOT_THE_Z2_B1_RECORD', '')
    check(rec, ic.get('verdict') == 'PASS_BITWISE_EQUAL' and ic.get('failing') == [] and isinstance(ic.get('checks'), dict)
          and ic['checks'].get('SCRIPT_CUSTODY') is True and ic['checks'].get('NEW_DRIVER_PIN') is True, 'RECORD_COMPARISON_NOT_PASS', '')
    check(rec, rec.get('comparator') == {'path': COMPARATOR[0], 'sha256': COMPARATOR[1]}, 'RECORD_COMPARATOR_NOT_C2V007R2', '')
    check(rec, run.get('path') == rep['new'] and (rec.get('reference_run') or {}).get('path') == rep['reference'] and rec.get('tokens') == tok
          and ic.get('driver_selected') == rep.get('driver_selected'), 'NOT_THE_RECORDED_Z2_RUN',
          'the report compares %s against %s; the record names %s against %s' % (rep['new'], rep['reference'], run.get('path'),
                                                                                (rec.get('reference_run') or {}).get('path')))
    check(rec, run.get('driver_sha256') == dsha and (rec.get('a67_n1') or {}).get('identity_run_driver_sha256') == dsha,
          'RECORD_DRIVER_NOT_THE_SLOT', '')
    ror = ic.get('report')
    check(rec, is_pin(ror), 'RECORD_SHAPE', 'identity_comparison.report')
    same = os.path.normpath(ror['path']) == os.path.normpath(a['--report'])
    if same:
        check(rec, ror['sha256'] == a['--report-sha256'], 'REPORT_IS_NOT_THE_RECORDED_BYTES', '')
        ror_raw, ror_rep = rraw, rep
    else:
        ror_raw = pinned(ror['path'], ror['sha256'], 'REPORT_OF_RECORD_PIN_MISMATCH')
        ror_rep = strict_json(ror_raw, 'REPORT_OF_RECORD_JSON')
        check(rec, isinstance(ror_rep, dict) and custody_view(ror_rep) == custody_view(rep), 'RERUN_DIFFERS_FROM_THE_REPORT_OF_RECORD',
              'gate, driver, comparator, runs, tokens, verdict, SCRIPT_CUSTODY, NEW_DRIVER_PIN and STAGE_SET must equal the report of record')
    # ---- the record
    ev = [{'path': str(Path(a['--report'])), 'sha256': a['--report-sha256']},
          {'path': str(Path(a['--identity-record'])), 'sha256': a['--identity-record-sha256']}]
    if not same:
        ev.append({'path': ror['path'], 'sha256': ror['sha256']})
    ev += [{'path': COMPARATOR[0], 'sha256': COMPARATOR[1]}, {'path': tok['path'], 'sha256': tok['sha256']},
           {'path': dp[0], 'sha256': dsha}, {'path': str(me), 'sha256': sha_bytes(me_raw)}]
    breakdown = '; '.join('%s: %d stage(s) (%s)' % (k, len(v), ', '.join(v)) for k, v in sorted(classes.items()))
    method = ('A59 raw successor custody of the Z2 identity run, from the identity comparator slot c2v007r2 (%s, sha256 %s): its report %s '
              '(sha256 %s) compares the new run %s against %s with tokens %s (sha256 %s) on driver %s (sha256 %s) and reads %s with '
              'failing []; its SCRIPT_CUSTODY check (%s) passed with one row per stage of STAGE_SET.order_new and no violation, and '
              'NEW_DRIVER_PIN passed (start.json and result.json name the driver slot, A67 N1). This converter (%s, sha256 %s) re-read the '
              'driver slot bytes as AST (no driver code executed) and counted a stage as a successor stage only when the script it ran '
              'is the planned Z2 successor of its kind: SCRIPTS_UVT[kind] for the UVT tail kinds %s (never the base SCRIPTS[kind]), an '
              'RO1 tail route-A worker for route_a, the AUX_UVT manifest writer for route_a_tail_manifest; any other kind refuses. '
              'Cross-checked against the Z2 identity gate record of record %s (sha256 %s)%s.'
              % (COMPARATOR[0], COMPARATOR[1], a['--report'], a['--report-sha256'], rep['new'], rep['reference'], tok['path'], tok['sha256'],
                 dp[0], dsha, rep['verdict'], SCRIPT_CUSTODY_RULE_Z2, me.name, sha_bytes(me_raw), ', '.join(tabs['UVT_TAIL_KINDS']),
                 a['--identity-record'], a['--identity-record-sha256'],
                 ' (the converted report is that record\'s report of record)' if same else
                 ' and its report of record %s (sha256 %s), whose custody sections this re-run equals' % (ror['path'], ror['sha256'])))
    note = 'stages_total = %d = stages_successor. Stages by successor class: %s.' % (len(order), breakdown)
    obj = {'schema': schema, 'identity_run': 'Z2', 'driver_sha256': dsha, 'stages_total': len(order), 'stages_successor': n_succ,
           'verdict': 'PASS', 'method': method, 'evidence': ev, 'note': note}
    text = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    return obj, text


def parse_cli(argv):
    seen, a, i = set(), {}, 0
    while i < len(argv):
        f = argv[i]
        if f not in FLAGS_VALUE + FLAGS_BOOL:
            raise Refuse('CLI_ARGUMENT', 'not an exact flag (no abbreviation, no --flag=value, no positional): %r' % f[:80])
        if f in seen:
            raise Refuse('CLI_REPEATED_FLAG', f)
        seen.add(f)
        if f in FLAGS_BOOL:
            a[f], i = True, i + 1
            continue
        if i + 1 >= len(argv) or argv[i + 1].startswith('--'):
            raise Refuse('CLI_MISSING_VALUE', f)
        a[f], i = argv[i + 1], i + 2
    miss = [f for f in FLAGS_VALUE if f not in a]
    if miss:
        raise Refuse('CLI_MISSING_FLAG', ', '.join(miss))
    return a


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    try:
        a = parse_cli(argv)
        obj, text = build(a)
    except Refuse as e:
        print(json.dumps({'verdict': 'REFUSE', 'code': e.code, 'detail': str(e)[:600]}, sort_keys=True), file=sys.stderr)
        return 2
    except Exception as e:                                     # fail closed: a code, never a traceback, and nothing written
        print(json.dumps({'verdict': 'REFUSE', 'code': 'INTERNAL_EXCEPTION:%s' % type(e).__name__, 'detail': str(e)[:300]}, sort_keys=True),
              file=sys.stderr)
        return 2
    sha = sha_bytes(text.encode('utf-8'))
    if a.get('--dry-run'):
        sys.stdout.write(text)
        print(json.dumps({'verdict': 'DRY_RUN_PASS', 'sha256': sha, 'would_write': a['--out']}, sort_keys=True), file=sys.stderr)
        return 0
    try:
        with open(a['--out'], 'x', encoding='utf-8') as f:
            f.write(text)
    except OSError as e:
        print(json.dumps({'verdict': 'REFUSE', 'code': 'OUT_NOT_CREATED', 'detail': '%s: %s' % (type(e).__name__, str(e)[:200])}, sort_keys=True),
              file=sys.stderr)
        return 2
    got = sha_bytes(Path(a['--out']).read_bytes())
    print(json.dumps({'verdict': 'PASS' if got == sha else 'WRITTEN_BYTES_DIFFER', 'out': a['--out'], 'sha256': got}, sort_keys=True),
          file=sys.stderr)
    return 0 if got == sha else 3


if __name__ == '__main__':
    raise SystemExit(main())
