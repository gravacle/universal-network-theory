"""cp1_registry_checks_c2v001: READ-ONLY checks used by cp1_registry_root_c2v001.zsh (CP-1 rho registration,
LO slot proofs c3v003, bundles and registry with registry_assembler_c3v004).

It never writes a file, never imports a producer or a tool, and never computes a physics number. Tool constants are
read from the pinned tool bytes by AST (no execution). Every file is read from bytes and its sha256 compared.
Output: one line on stdout, 'OK<TAB><value>' with exit 0, or 'FAIL<TAB><reason>' with exit 1.

Subcommands
  drafts   <dir> <final_dir>     the drafted inputs in <dir> (scratch staging or the final copies) are consistent with
                                 the tools and the CP-1 records; plus exact replicas of the tool checks that need no
                                 custody derivation (slot proof L199-219, L289-305; assembler L237-261, L293-309)
  slot     <stdout> <proof_path> <slot_out> <args_path> <args_sha> <key>
  bundle   <stdout> <bundle_path> <key> <eps_proof> <gq_proof> <lo_proof> <lo_proof_sha> <args_path> <args_sha>
  registry <stdout> <reg_out> <registration_path> <registration_sha> <approved_path> <approved_sha> <bundle=sha>...
"""
import ast
import copy
import glob
import hashlib
import json
import os
import sys

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LANE = ART + '/s4rc1_c3'
RUN = LANE + '/cp1_run_c3v004b'
COMMON_C3V004 = (LANE + '/build_c3v004/s4rc1_common_c3v004.py',
                 '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083')
SLOT_TOOL = (LANE + '/proof_side_c3v003/lo_slot_proof_c3v003.py',
             'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3')
ASSEMBLER = (LANE + '/build_c3v004/registry_assembler_c3v004.py',
             'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0')
C1_DRAFT = (LANE + '/build_c3v004/C1_DRAFT_APPROVED_PRODUCERS_C3V004.json',
            '8774699ccf5a93bce79e1bb0e4cb1a66bc60d092a55b5a40876b9c8541e06961')
REGISTRATION_NAME = 'RHO_REGISTRATION_CP1_C2V001.json'
APPROVED_NAME = 'APPROVED_PRODUCERS_CP1_REGISTRY_C2V001.json'
ARGS_KEYS = {'spec_ref', 'rho_ref', 'registered_rho_records', 'anchor_rho_pair', 'root_ruling_refs',
             'approved_producer_sha256'}
EPS_NUMERIC_SCHEMA = 'UNT_POINT_EPS_NUMERICAL_CX2V001'     # assembler L66
CUSTODY_KEYS = {'grid_sha256', 'background_sha256', 'geometry_sha256', 'modules_sha256', 'row_contract_sha256'}
REGISTRY_SCHEMA = 'S4RC1_C1_CERTIFICATE_REGISTRY_C3V003'   # assembler L61


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and is_sha(x['sha256'])


def read_raw(path, sha=None, label='file'):
    need(isinstance(path, str) and os.path.isabs(path), 'PATH_NOT_ABSOLUTE %s %r' % (label, path))
    need(os.path.realpath(path) == path, 'PATH_NOT_CANONICAL %s %s' % (label, path))
    need(os.path.isfile(path), 'FILE_MISSING %s %s' % (label, path))
    with open(path, 'rb') as f:
        raw = f.read()
    got = hashlib.sha256(raw).hexdigest()
    need(sha is None or got == sha, 'SHA_MISMATCH %s %s want %s got %s' % (label, path, sha, got))
    return raw, got


def read_json(path, sha=None, label='file'):
    raw, got = read_raw(path, sha, label)
    return json.loads(raw), got


def pin_of(path, label='file'):
    _, got = read_raw(path, None, label)
    return {'path': path, 'sha256': got}


def read_pin(pin, label):
    need(is_pin(pin), 'NOT_AN_EXACT_PIN %s %r' % (label, pin))
    return read_json(pin['path'], pin['sha256'], label)[0]


def _eval(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Tuple):
        return tuple(_eval(e, env) for e in node.elts)
    if isinstance(node, ast.List):
        return [_eval(e, env) for e in node.elts]
    if isinstance(node, ast.Dict):
        return {_eval(k, env): _eval(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _eval(node.left, env) + _eval(node.right, env)
    if isinstance(node, ast.Name) and node.id in env:
        return env[node.id]
    raise ValueError('unsupported')


def consts(pinned, names):
    """Module-level constants read by AST from the pinned bytes (never executed)."""
    raw, _ = read_raw(pinned[0], pinned[1], 'tool ' + os.path.basename(pinned[0]))
    env = {}
    for n in ast.parse(raw.decode('utf-8')).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                env[n.targets[0].id] = _eval(n.value, env)
            except ValueError:
                pass
    missing = [k for k in names if k not in env]
    need(not missing, 'TOOL_CONSTANTS_NOT_FOUND %s %r' % (pinned[0], missing))
    return {k: env[k] for k in names}


def table():
    c = consts(COMMON_C3V004, ['ART', 'POINTS', 'DRIVER_SHA', 'PINS', 'CANONICAL_APPROVED_PRODUCERS', 'PROOF_SCHEMA',
                               'BUNDLE_SCHEMA'])
    need(c['ART'] == ART, 'COMMON_ART_DIFFERS')
    rows = [dict(row=r[0], key=r[1], label=r[2], spec_path=ART + '/' + r[4], spec_sha256=r[5]) for r in c['POINTS']]
    need([r['row'] for r in rows] == list(range(1, 32)), 'POINT_TABLE_NOT_31_ROWS_IN_ORDER')
    return rows, c


def slot_consts():
    return consts(SLOT_TOOL, ['ROOT_RULINGS', 'ANCHOR_KEY', 'RHO_SCHEMA', 'RHO_GATE', 'RHO_VERDICT', 'RHO_COVERAGE',
                              'RHO_PARTITION', 'RESPONSE_SHA', 'RHO_COMPARE_KEYS', 'PROOF_SCHEMA', 'GATE',
                              'FORBIDDEN_PROOF_KEYS', 'SLOT_RULE', 'LO_ROUTE'])


def point_identity(spec, driver_sha):
    """common c3v004 point_identity (core a595c5c0 L233-238)."""
    n = copy.deepcopy(spec['numerics'])
    for k in ('eps_certificate', 'lo_certificate'):
        n['uv_tail'].pop(k, None)
    return {'driver_sha256': driver_sha, 'physical': spec['physical'], 'coefficients': spec['coefficients'],
            'numerics': n}


def point_dir(r):
    hits = glob.glob(RUN + '/P%02d_%s_*' % (r['row'], r['key'][:16]))
    want = RUN + '/P%02d_%s_%s_a1' % (r['row'], r['key'][:16], r['label'])
    need(hits == [want], 'POINT_DIR_NOT_UNIQUE row %d %r' % (r['row'], hits))
    return want


def names(r):
    k16 = r['key'][:16]
    return 'FILLED_SPEC_P%02d_%s.json' % (r['row'], k16), 'SLOT_ARGS_P%02d_%s.json' % (r['row'], k16)


def check_rho_record(rec, S, label):
    """Slot proof c3v003 check_rho_record L199-219 (the producer bytes are read here by sha)."""
    need(isinstance(rec, dict), label + ' RHO_RECORD_NOT_AN_OBJECT')
    need(rec.get('schema') == S['RHO_SCHEMA'] and rec.get('gate') == S['RHO_GATE'], label + ' RHO_SCHEMA_OR_GATE')
    need(rec.get('status') == 'TESTED' and rec.get('verdict') == S['RHO_VERDICT'], label + ' RHO_STATUS_OR_VERDICT')
    need(rec.get('settings') == 'registered' and rec.get('full_registered_search_executed') is True,
         label + ' RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH')
    need(rec.get('coverage_complete') is True and rec.get('required_coverage_inverse_kpc') == S['RHO_COVERAGE'],
         label + ' RHO_COVERAGE')
    need([s.get('range_inverse_kpc') for s in rec.get('shells') or [] if isinstance(s, dict)] == S['RHO_PARTITION'],
         label + ' RHO_PARTITION')
    p = rec.get('producer')
    need(is_pin(p) and p['sha256'] == S['RESPONSE_SHA'], label + ' RHO_PRODUCER_NOT_A1DCDEA8')
    read_raw(p['path'], p['sha256'], label + ' rho producer bytes')
    need(isinstance(rec.get('identity'), dict) and rec.get('point_sha256') == digest(rec['identity']),
         label + ' RHO_IDENTITY_POINT_SHA_INCONSISTENT')


def rho_bitwise_canonical(rec, S):
    """Slot proof c3v003 L183-191 (wrapper v002 10-key canonical comparison)."""
    return canonical({k: rec.get(k) for k in S['RHO_COMPARE_KEYS']})


def cmd_drafts(d, final_dir):
    rows, C = table()
    S = slot_consts()
    slot_pin = {'path': SLOT_TOOL[0], 'sha256': SLOT_TOOL[1]}
    c1 = read_json(C1_DRAFT[0], C1_DRAFT[1], 'C1 draft')[0]
    proposed = c1.get('proposed_approved_certificate_producers')
    canon = [{'path': C['PINS'][n][0], 'sha256': C['PINS'][n][1]} for n in C['CANONICAL_APPROVED_PRODUCERS']]
    need(proposed == canon, 'C1_DRAFT_LIST_NOT_THE_CANONICAL_THREE')
    need(slot_pin in proposed, 'SLOT_PRODUCER_NOT_IN_C1_DRAFT')
    for p in proposed:
        read_raw(p['path'], p['sha256'], 'approved producer')
    # Approved-producers input of registry_assembler_c3v004 load_approved (L198-207).
    appr = read_json(os.path.join(d, APPROVED_NAME), None, 'approved producers draft')[0]
    need(isinstance(appr, dict) and appr.get('approved_certificate_producers') == proposed,
         'APPROVED_FILE_LIST_DIFFERS_FROM_C1_DRAFT')
    need(appr.get('source_c1_draft') == {'path': C1_DRAFT[0], 'sha256': C1_DRAFT[1]}, 'APPROVED_FILE_SOURCE_PIN')
    approved = appr['approved_certificate_producers']
    # Registration list: slot rho = attempt a (every point), anchor pair = (a, b) (A199 item 2).
    reg = read_json(os.path.join(d, REGISTRATION_NAME), None, 'registration draft')[0]
    lst, pair = reg.get('registered_rho_records'), reg.get('anchor_rho_pair')
    need(isinstance(lst, list) and len(lst) == 32 and all(is_pin(p) for p in lst), 'REGISTRATION_NOT_32_EXACT_PINS')
    need(len({p['path'] for p in lst}) == 32 and len({p['sha256'] for p in lst}) == 32, 'REGISTRATION_DUPLICATES')
    need(rows[0]['key'] == S['ANCHOR_KEY'], 'TABLE_ROW1_NOT_THE_SLOT_ANCHOR_KEY')
    slot_rho, eps_num, csha_all, deps = {}, {}, {}, set()
    for r in rows:
        pdir = point_dir(r)
        k16 = r['key'][:16]
        rho_a = pin_of(pdir + '/RHO_NUMERIC_%s_a.json' % k16, 'rho a')
        need(lst[r['row'] - 1] == rho_a, 'REGISTRATION_ROW_%d_NOT_RHO_A' % r['row'])
        need(sorted(glob.glob(pdir + '/RHO_NUMERIC_*')) == sorted(
            [rho_a['path']] + ([pdir + '/RHO_NUMERIC_%s_b.json' % k16] if r['row'] == 1 else [])),
            'RHO_RECORD_SET_UNEXPECTED row %d' % r['row'])
        slot_rho[r['key']] = rho_a
        spec = read_json(r['spec_path'], r['spec_sha256'], 'registered spec')[0]
        ident = point_identity(spec, C['DRIVER_SHA'])
        need(digest(ident) == r['key'], 'SPEC_KEY_MISMATCH row %d' % r['row'])
        # EPS and GQ proofs (the files adapt-eps and the GQ stage wrote).
        eps_pin = pin_of(pdir + '/EPS_PROOF_%s.json' % k16, 'EPS proof')
        gq_pin = pin_of(pdir + '/GQ_PROOF_%s.json' % k16, 'GQ proof')
        eps = read_pin(eps_pin, 'EPS proof')
        gq = read_pin(gq_pin, 'GQ proof')
        for gate, doc in (('EPS', eps), ('GQ', gq)):                    # assembler _proof L210-217
            need(doc.get('schema') == C['PROOF_SCHEMA'] and doc.get('gate') == gate, gate + '_PROOF_SCHEMA_OR_GATE')
            need(doc.get('status') == 'TESTED' and doc.get('verdict') == 'PASS', gate + '_PROOF_NOT_TESTED_PASS')
        eslot = eps.get('driver_certificate')
        need(is_pin(eslot) and eslot == pin_of(pdir + '/EPS_NUMERIC_%s.json' % k16, 'EPS numeric'),
             'EPS_PROOF_SLOT_NOT_THIS_POINTS_EPS_NUMERIC row %d' % r['row'])
        eps_num[r['key']] = eslot
        eps_rec = read_pin(eslot, 'EPS numeric')
        rho = read_pin(rho_a, 'rho a')
        check_rho_record(rho, S, 'row %d rho a' % r['row'])
        need(rho.get('identity') == ident and rho.get('point_sha256') == r['key'], 'RHO_A_POINT_MISMATCH row %d' % r['row'])
        # assembler assemble_bundle L237-261 (all but the LO proof, which does not exist yet).
        need(eps_rec.get('schema') == EPS_NUMERIC_SCHEMA and eps_rec.get('identity') == ident, 'EPS_RECORD_SCHEMA_OR_POINT')
        need(eps_rec.get('settings') == 'registered' and eps_rec.get('full_registered_search_executed') is True,
             'SMOKE_OR_PARTIAL_EPS_RECORD')
        custody = eps_rec.get('custody')
        need(isinstance(custody, dict) and set(custody) == CUSTODY_KEYS, 'CUSTODY_FIVE_KEYS row %d' % r['row'])
        need(rho.get('custody') == custody, 'CUSTODY_MISMATCH_BETWEEN_SLOT_RECORDS row %d' % r['row'])
        csha = digest(custody)
        for gate, doc in (('EPS', eps), ('GQ', gq)):
            need(doc.get('point_sha256') == r['key'], gate + '_POINT_MISMATCH row %d' % r['row'])
            need(doc.get('custody_sha256') == csha, gate + '_CUSTODY_MISMATCH row %d' % r['row'])
            need(doc.get('producer') in approved, gate + '_PRODUCER_NOT_APPROVED row %d' % r['row'])
        need(gq.get('all_production_kperp_nodes') is True and gq.get('nodes_tested') == gq.get('production_nodes'),
             'PARTIAL_GQ_PROOF row %d' % r['row'])
        csha_all[r['key']] = csha
        deps.add(digest({'dependencies': eps_rec.get('dependencies'), 'producer': eps_rec.get('producer')}))  # L294
        # Filled spec: the registered spec with both slots set (core dc895f8a Mapper L249-259; assembler L408-414).
        fname, aname = names(r)
        fspec = read_json(os.path.join(d, fname), None, 'filled spec')[0]
        u = fspec['numerics']['uv_tail']
        need(u.get('lo_certificate') == rho_a and u.get('eps_certificate') == eslot, 'FILLED_SLOTS row %d' % r['row'])
        back = copy.deepcopy(fspec)
        for k in ('eps_certificate', 'lo_certificate'):
            back['numerics']['uv_tail'][k] = spec['numerics']['uv_tail'][k]
        need(canonical(back) == canonical(spec), 'FILLED_SPEC_DIFFERS_BEYOND_SLOTS row %d' % r['row'])
        need(digest(point_identity(fspec, C['DRIVER_SHA'])) == r['key'], 'FILLED_SPEC_KEY row %d' % r['row'])
        # Slot-proof args (lo_slot_proof_c3v003 main L376-383).
        args = read_json(os.path.join(d, aname), None, 'slot args')[0]
        need(isinstance(args, dict) and set(args) == ARGS_KEYS, 'ARGS_KEYS row %d' % r['row'])
        _, fsha = read_raw(os.path.join(d, fname), None, 'filled spec')
        need(args['spec_ref'] == {'path': os.path.join(final_dir, fname), 'sha256': fsha}, 'ARGS_SPEC_REF row %d' % r['row'])
        need(args['rho_ref'] == rho_a, 'ARGS_RHO_REF row %d' % r['row'])
        need(args['registered_rho_records'] == lst, 'ARGS_REGISTERED_LIST row %d' % r['row'])
        need(args['anchor_rho_pair'] == pair, 'ARGS_ANCHOR_PAIR row %d' % r['row'])
        need(args['root_ruling_refs'] == [dict(x) for x in S['ROOT_RULINGS']], 'ARGS_ROOT_RULINGS row %d' % r['row'])
        need(args['approved_producer_sha256'] == [p['sha256'] for p in approved] and SLOT_TOOL[1] in
             args['approved_producer_sha256'], 'ARGS_APPROVED_SHAS row %d' % r['row'])
        for rr in S['ROOT_RULINGS']:
            read_raw(rr['path'], rr['sha256'], 'root ruling')
    need(len(deps) == 1, 'EPS_SOURCE_PINS_DIFFER_ACROSS_POINTS (assembler L308)')
    # (a)4 anchor pair (slot proof L289-305).
    k16 = rows[0]['key'][:16]
    pdir = point_dir(rows[0])
    want_pair = [slot_rho[rows[0]['key']], pin_of(pdir + '/RHO_NUMERIC_%s_b.json' % k16, 'rho b')]
    need(pair == want_pair and lst[31] == want_pair[1], 'ANCHOR_PAIR_NOT_(A,B)')
    need(pair[0]['sha256'] != pair[1]['sha256'] and pair[0]['path'] != pair[1]['path'], 'ANCHOR_PAIR_NOT_TWO_RUNS')
    anchors = [read_pin(p, 'anchor rho') for p in pair]
    for i, a in enumerate(anchors):
        check_rho_record(a, S, 'anchor rho %s' % 'ab'[i])
    need(all(a.get('point_sha256') == S['ANCHOR_KEY'] for a in anchors), 'ANCHOR_RHO_RUN_NOT_AT_ANCHOR_KEY')
    need(anchors[0].get('custody') == anchors[1].get('custody') and anchors[0].get('identity') == anchors[1].get('identity'),
         'ANCHOR_RHO_RUNS_DIFFER_IN_POINT_OR_CUSTODY')
    need(rho_bitwise_canonical(anchors[0], S) == rho_bitwise_canonical(anchors[1], S), 'ANCHOR_RHO_NOT_BITWISE_EQUAL')
    need(reg.get('slot_rho_by_row') == [{'row': r['row'], 'key': r['key'], 'label': r['label'],
                                         'rho_ref': slot_rho[r['key']]} for r in rows], 'REGISTRATION_SLOT_TABLE')
    return 'drafts consistent: 31 points, 32 registered rho pins, anchor pair (a,b) 10-key equal, deps digest %s' % (
        next(iter(deps))[:16])


def last_json(stdout_path):
    with open(stdout_path, 'rb') as f:
        lines = [x for x in f.read().decode('utf-8').splitlines() if x.strip()]
    need(lines, 'EMPTY_STDOUT ' + stdout_path)
    return json.loads(lines[-1])


def cmd_slot(stdout_path, proof_path, slot_out, args_path, args_sha, key):
    S = slot_consts()
    out = last_json(stdout_path)
    need(out.get('verdict') == 'READY_FOR_MANIFEST' and out.get('blockers') == [], 'SLOT_VERDICT %r' % out)
    pin, res = out.get('proof'), out.get('result')
    need(is_pin(pin) and pin['path'] == proof_path, 'SLOT_PROOF_PIN_PATH %r' % pin)
    need(is_pin(res) and os.path.dirname(res['path']) == slot_out, 'SLOT_RESULT_PIN_PATH %r' % res)
    read_raw(res['path'], res['sha256'], 'slot result')
    proof = read_json(proof_path, pin['sha256'], 'slot proof')[0]
    args = read_json(args_path, args_sha, 'slot args')[0]
    need(proof.get('schema') == S['PROOF_SCHEMA'] and proof.get('gate') == S['GATE'], 'SLOT_PROOF_SCHEMA_OR_GATE')
    need(proof.get('status') == 'TESTED' and proof.get('verdict') == 'PASS', 'SLOT_PROOF_NOT_TESTED_PASS')
    need(not any(k in proof for k in S['FORBIDDEN_PROOF_KEYS']), 'SLOT_PROOF_CARRIES_FORBIDDEN_KEY')
    need(proof.get('point_sha256') == key, 'SLOT_PROOF_POINT')
    need(proof.get('driver_certificate') == args['rho_ref'] == proof.get('rho_record'), 'SLOT_PROOF_NOT_BOUND_TO_RHO_A')
    need(proof.get('producer') == {'path': SLOT_TOOL[0], 'sha256': SLOT_TOOL[1]}, 'SLOT_PROOF_PRODUCER_PIN')
    ar = proof.get('anchor_rho_reproducibility') or {}
    need(ar.get('records') == args['anchor_rho_pair'] and ar.get('bitwise_equal') is True
         and ar.get('anchor_point_sha256') == S['ANCHOR_KEY'], 'SLOT_PROOF_ANCHOR_PAIR')
    need(proof.get('lo_certified') is False and proof.get('slot_rule') == S['SLOT_RULE']
         and proof.get('lo_route') == S['LO_ROUTE'], 'SLOT_PROOF_RULE_FIELDS')
    need(proof.get('root_rulings') == args['root_ruling_refs'], 'SLOT_PROOF_ROOT_RULINGS')
    return pin['sha256']


def cmd_bundle(stdout_path, bundle_path, key, eps_proof, gq_proof, lo_proof, lo_sha, args_path, args_sha):
    _, C = table()
    out = last_json(stdout_path)
    pin = out.get('bundle')
    need(is_pin(pin) and pin['path'] == bundle_path, 'BUNDLE_PIN_PATH %r' % out)
    b = read_json(bundle_path, pin['sha256'], 'bundle')[0]
    args = read_json(args_path, args_sha, 'slot args')[0]
    eps_pin = pin_of(eps_proof, 'EPS proof')
    eps = read_pin(eps_pin, 'EPS proof')
    need(b.get('schema') == C['BUNDLE_SCHEMA'] and b.get('point_sha256') == key, 'BUNDLE_SCHEMA_OR_POINT')
    need(b.get('prelaunch') == {'EPS': eps_pin, 'GQ': pin_of(gq_proof, 'GQ proof'),
                                'LO_RHO_SLOT': {'path': lo_proof, 'sha256': lo_sha}}, 'BUNDLE_PRELAUNCH_PINS')
    need(b.get('driver_certificate_bindings') == {'eps_certificate': eps.get('driver_certificate'),
                                                  'lo_certificate': args['rho_ref']}, 'BUNDLE_SLOT_BINDINGS')
    need(b.get('generator') == {'path': ASSEMBLER[0], 'sha256': ASSEMBLER[1]}, 'BUNDLE_GENERATOR_PIN')
    return pin['sha256']


def cmd_registry(stdout_path, reg_out, registration_path, registration_sha, approved_path, approved_sha, *bundles):
    rows, _ = table()
    out = last_json(stdout_path)
    rpin, mpin = out.get('registry'), out.get('manifest')
    need(is_pin(rpin) and os.path.dirname(rpin['path']) == reg_out, 'REGISTRY_PIN_PATH %r' % out)
    need(is_pin(mpin) and os.path.dirname(mpin['path']) == reg_out, 'MANIFEST_PIN_PATH %r' % out)
    reg = read_json(rpin['path'], rpin['sha256'], 'registry')[0]
    man = read_json(mpin['path'], mpin['sha256'], 'registry manifest')[0]
    regn = read_json(registration_path, registration_sha, 'registration')[0]
    appr = read_json(approved_path, approved_sha, 'approved producers')[0]
    bpins = []
    for item in bundles:
        p, _, s = item.rpartition('=')
        bpins.append({'path': p, 'sha256': s})
    need(len(bpins) == 31, 'BUNDLE_ARGS_NOT_31')
    need(reg.get('schema') == REGISTRY_SCHEMA and reg.get('count') == 31 and reg.get('complete_31_point_table') is True
         and reg.get('missing_points') == [], 'REGISTRY_NOT_COMPLETE_31')
    pts = reg.get('points') or {}
    need(sorted(pts) == sorted(r['key'] for r in rows), 'REGISTRY_KEYS')
    slot = {x['key']: x['rho_ref'] for x in regn['slot_rho_by_row']}
    for r, bp in zip(rows, bpins):
        rec = pts[r['key']]
        need(rec.get('bundle') == bp, 'REGISTRY_BUNDLE_PIN row %d' % r['row'])
        need(rec.get('lo_certificate') == slot[r['key']], 'REGISTRY_LO_SLOT_NOT_RHO_A row %d' % r['row'])
        b = read_pin(bp, 'bundle')
        need(rec.get('eps_certificate') == b['driver_certificate_bindings']['eps_certificate'], 'REGISTRY_EPS_SLOT')
    need(man.get('registry') == rpin and man.get('approved_certificate_producers') == appr['approved_certificate_producers']
         and (man.get('c1_tail_readiness_fields') or {}).get('certificate_registry') == rpin, 'MANIFEST_FIELDS')
    return '%s=%s %s=%s' % (rpin['path'], rpin['sha256'], mpin['path'], mpin['sha256'])


def main(argv):
    try:
        if not argv:
            raise Fail('NO_SUBCOMMAND')
        cmd, rest = argv[0], argv[1:]
        fn = {'drafts': (cmd_drafts, 2), 'slot': (cmd_slot, 6), 'bundle': (cmd_bundle, 9)}.get(cmd)
        if fn is not None:
            need(len(rest) == fn[1], 'ARGC %s' % cmd)
            val = fn[0](*rest)
        elif cmd == 'registry':
            need(len(rest) == 6 + 31, 'ARGC registry')
            val = cmd_registry(*rest)
        else:
            raise Fail('UNKNOWN_SUBCOMMAND ' + cmd)
    except (Fail, OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
        print('FAIL\t%s: %s' % (type(exc).__name__, exc), flush=True)
        return 1
    print('OK\t%s' % val, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
