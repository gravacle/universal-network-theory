"""S4-R-C1 C1 certificate registry assembler and OFFLINE verifier c3v004 (Claude3; A122, A134, A138; Codex1 under A115).

bundle    one point: three reviewed proofs (EPS from adapter v003, GQ from gq_producer v005, and LO_RHO_SLOT from the
          A134 Q5 slot-proof producer lo_slot_proof_c3v003) -> bundle manifest UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001.
          The lo slot is the point's registered rho record. An LO_ENVELOPE proof, or a proof carrying
          covers_all_consumed_states or cover_all_consumed_states, is refused.
registry  bundles -> C1 tail_readiness.certificate_registry document: points[key] =
          {identity, bundle, eps_certificate, lo_certificate}, exact {path, sha256} pins, a schema
          and a generator pin; plus a manifest of every pin (for C1 and review). lo_certificate is the rho pin,
          which wrapper v002 L165 compares with the slot.
verify    OFFLINE and read-only, against root's wrapper v002 7a6af535 (core dc895f8a): replicates
          certificate_policy_gate L59-77 on the C1 document's tail_readiness (L61-62 required pins, L63-66
          producers, L67-75 certificate_policy_review checked_gate = core L66-82, with root's L74 slot rule and
          guard_sha256 = the guard that wrapper L30 loads), then L80-93 (with core Mapper L249-259 slot filling). It
          then EXECUTES wrapper v002's own L145-191 bytes, taken from the 7a6af535 file by AST, with core dc895f8a's
          canonical/digest/pin_doc and parent v005's read_pinned (both AST-extracted from their pinned bytes), and
          calls verify_bundle(phase='prelaunch') of the guard that wrapper L30 loads (b1 9e3fc109). The custody deriver
          and the approved producers are READ FROM THE C1 and must equal the canonical pins (F3).
          Not replicated: Context construction (L43-57), the sensitivity and other prelaunch gates, and the
          guard007/guard009 fence (R1). A PASS here is not launch authorization.
c3v003 (FROM_CODEX/0696, 0697): LO_ENVELOPE -> LO_RHO_SLOT everywhere; root's slot-rule string; wrapper v002 in place of
          r10_c4 ef3d3d69; its L145-191 block executed from its bytes; the guard binding follows wrapper L30.
c3v004 (A138, FROM_CODEX/0703): common c3v004 only: wrapper v002 read at its published path (V09, same sha 7a6af535),
          the b1 enumerator in the manifest's draft C1 fields (V02), and the canonical slot producer c3v003.
Everything is written by exclusive create into the caller's own output root. Hashes from bytes.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import sys
import textwrap
import types

HERE = os.path.dirname(os.path.realpath(__file__))
COMMON_PATH = HERE + '/s4rc1_common_c3v004.py'
COMMON_SHA = '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'


def _load_common():
    with open(COMMON_PATH, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != COMMON_SHA:
        raise SystemExit('REFUSED: s4rc1_common pin mismatch')
    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004', COMMON_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    exec(compile(raw, COMMON_PATH, 'exec'), mod.__dict__)
    return mod


C = _load_common()
Refusal = C.Refusal
ASSEMBLER_PATH = os.path.realpath(__file__)
REGISTRY_SCHEMA = 'S4RC1_C1_CERTIFICATE_REGISTRY_C3V003'                       # c3v003: LO_RHO_SLOT bundles
POLICY_SCHEMA = 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001'                     # F3: wrapper L40 (v002 unchanged)
C1_REQUIRED_PINS = ('certificate_registry', 'custody_deriver', 'state_enumerator', 'certificate_policy_review')  # L61
HULL = [151250000.0, 317625000.0]
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'                                  # the lo slot record (A134 Q5)
EPS_NUMERIC_SCHEMA = 'UNT_POINT_EPS_NUMERICAL_CX2V001'
SLOT_GATE = 'LO_RHO_SLOT'                                                       # wrapper v002 L148
SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'         # wrapper v002 L74 (root's string, 0697)
FORBIDDEN_PROOF_KEYS = ('covers_all_consumed_states', 'cover_all_consumed_states')   # A134 Q5
WRAPPER_BLOCK_LINES = (145, 191)                                                # wrapper v002 L145-191 (L185 core_record)
PARENT_V005 = (C.ART + '/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
               'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d')   # core dc895f8a PARENT/PARENT_SHA


def _wrapper_v002():
    """Root's wrapper v002 bytes (7a6af535), read by its canonical pin. Returns (path, source text)."""
    path, sha = C.PINS['wrapper_q5b1']
    raw = C.read_bytes_pinned({'path': path, 'sha256': sha}, (C.ART,), 'wrapper v002', max_bytes=None)
    return path, raw.decode('utf-8')


def wrapper_l30_guard_pin():
    """The guard binding follows what wrapper v002 L30 loads: G=load(Path(<path>),'_cx2certguard',expected=<sha>)."""
    path, src = _wrapper_v002()
    nodes = [n for n in ast.parse(src).body if isinstance(n, ast.Assign) and n.lineno == 30]
    try:
        node = nodes[0]
        call = node.value
        if len(nodes) != 1 or [t.id for t in node.targets] != ['G'] or call.func.id != 'load':
            raise ValueError('shape')
        gpath = call.args[0].args[0].value
        gsha = [k.value.value for k in call.keywords if k.arg == 'expected'][0]
    except (IndexError, AttributeError, ValueError, TypeError) as exc:
        raise Refusal('WRAPPER_V002_L30_GUARD_LOAD_NOT_READABLE: %s' % exc)
    if not isinstance(gpath, str) or not C.is_sha(gsha):
        raise Refusal('WRAPPER_V002_L30_GUARD_LOAD_NOT_READABLE')
    return {'path': gpath, 'sha256': gsha}


def wrapper_slot_block():
    """Wrapper v002 L145-191 (slot checks; L185 reads lo['core_record']), taken from the 7a6af535 bytes by AST and
    compiled unchanged into a function of the names it reads. Returns (function, provenance)."""
    path, src = _wrapper_v002()
    tree = ast.parse(src)
    ctx = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Context']
    cc = [n for n in ctx[0].body if isinstance(n, ast.FunctionDef) and n.name == 'certificate_check'] if len(ctx) == 1 else []
    tries = [n for n in cc[0].body if isinstance(n, ast.Try)] if len(cc) == 1 else []
    if len(tries) != 1:
        raise Refusal('WRAPPER_V002_CERTIFICATE_CHECK_SHAPE')
    lo_l, hi_l = WRAPPER_BLOCK_LINES
    sel = [n for n in tries[0].body if lo_l <= n.lineno <= hi_l]
    if not sel or sel[0].lineno != lo_l or sel[-1].end_lineno != hi_l:
        raise Refusal('WRAPPER_V002_BLOCK_NOT_AT_L145_L191')
    blk = '\n'.join(src.split('\n')[lo_l - 1:hi_l]) + '\n'
    fsrc = ('def _wrapper_v002_slot_block(spec, bundle, custody, ident, r, rec, phase, M, O, G, Error):\n'
            + textwrap.indent(textwrap.dedent(blk), '    ') + '    return True\n')
    ns = {}
    exec(compile(fsrc, path + ' L%d-%d' % (lo_l, hi_l), 'exec'), ns)
    return ns['_wrapper_v002_slot_block'], {'wrapper': {'path': path, 'sha256': C.PINS['wrapper_q5b1'][1]},
                                            'lines': [lo_l, hi_l], 'block_sha256': C.sha256_bytes(blk.encode('utf-8')),
                                            'statements': len(sel)}


def wrapper_primitives(roots):
    """The block's M (core dc895f8a canonical/digest/pin_doc) and O (parent v005 read_pinned), AST-extracted from their
    pinned bytes. O.read_pinned is fenced stricter-only by the lexical path policy before it opens anything."""
    core_path, core_sha = C.PINS['core_r10_c4']
    core_src = C.read_bytes_pinned({'path': core_path, 'sha256': core_sha}, (C.ART,), 'wrapper core', max_bytes=None).decode('utf-8')
    par_src = C.read_bytes_pinned({'path': PARENT_V005[0], 'sha256': PARENT_V005[1]}, (C.ART,), 'parent v005',
                                  max_bytes=None).decode('utf-8')
    ctree, ptree = ast.parse(core_src), ast.parse(par_src)
    psha = [n.value.value for n in ctree.body if isinstance(n, ast.Assign) and [getattr(t, 'id', None) for t in n.targets] == ['PARENT_SHA']]
    if psha != [PARENT_V005[1]]:
        raise Refusal('CORE_PARENT_SHA_NOT_V005_C75A889F')

    class Error(Exception):
        """The wrapper's Error (O.OrchestratorError)."""

    def take(tree, names, ns):
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        if sorted(n.name for n in nodes) != sorted(names):
            raise Refusal('PRIMITIVES_NOT_FOUND: %r' % (names,))
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'wrapper primitives', 'exec'), ns)
        return ns
    from pathlib import Path
    ns_o = take(ptree, ['sha256_bytes', 'read_pinned'], {'hashlib': hashlib, 'Path': Path, 'OrchestratorError': Error})

    def read_pinned(pin, label):
        if isinstance(pin, dict) and isinstance(pin.get('path'), str):
            bad = C.policy_violations(pin['path'], roots)
            if bad:
                raise Error('%s: %s: %s' % (label, pin['path'], ','.join(bad)))
        return ns_o['read_pinned'](pin, label)
    O = types.SimpleNamespace(read_pinned=read_pinned)
    ns_m = take(ctree, ['canonical', 'digest', 'pin_doc'], {'json': json, 'hashlib': hashlib, 'O': O})
    M = types.SimpleNamespace(canonical=ns_m['canonical'], digest=ns_m['digest'], pin_doc=ns_m['pin_doc'])
    return M, O, Error


def generator_pin():
    return {'path': ASSEMBLER_PATH, 'sha256': C.sha256_file(ASSEMBLER_PATH)}


def validate_block(block):
    """Transcribed from core a595c5c0 L212-231, unchanged in dc895f8a (wrapper r10_c4 L80, L173)."""
    u = block.get('uv_tail', {})
    if u.get('enabled') is not True or u.get('source_rule') != 'continuum_v001':
        raise Refusal('production continuum tail-ON required')
    if block.get('truncation') != {'shape': 'cube'}:
        raise Refusal('kept cube required')
    if block['composite_grid_spec']['breaks_inverse_kpc'][-1] != 4:
        raise Refusal('kept K must be 4')
    if u.get('outer') != {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}:
        raise Refusal('A55 production K_big 128 required')
    if u.get('gas') != {'M_s': 128, 'interp': 'lagrange3_s_gl4'}:
        raise Refusal('A57 production gas M_s 128 required')
    if u.get('lambda_scale') != 1.0 or u.get('lapse_only') is not True:
        raise Refusal('tail must be unrescaled lapse-only')
    if block['route_a'].get('column_workers') != 8 or 'ro1_workers' in block['route_a']:
        raise Refusal('route A workers 8 required')
    fs = block['brackets']['rule']['fs_absolute_overrides']
    if set(fs) != {str(i) for i in range(72)} or any(v != HULL for v in fs.values()):
        raise Refusal('full A32 hull required on every one of 72 columns')


def load_point_spec(row):
    path = C.require_policy(row['spec_path'], (C.ART,), 'spec')
    with open(path, 'rb') as f:
        raw = f.read()
    if C.sha256_bytes(raw) != row['spec_sha256']:
        raise Refusal('SPEC_PIN_MISMATCH: ' + path)
    spec = json.loads(raw)
    if C.point_key(spec) != row['key']:
        raise Refusal('POINT_KEY_MISMATCH: ' + row['label'])
    return spec


def load_approved(path, roots):
    """C1 approved_certificate_producers: a non-empty list of exact pins (wrapper r10_c4 L63-66)."""
    ref = C.pin_of(path, roots, 'approved producers file')
    doc = json.loads(C.read_bytes_pinned(ref, roots, 'approved producers file'))
    lst = doc.get('approved_certificate_producers') if isinstance(doc, dict) else doc
    if not isinstance(lst, list) or not lst or not all(C.is_pin(p) for p in lst):
        raise Refusal('APPROVED_CERTIFICATE_PRODUCERS_MUST_BE_NONEMPTY_PIN_LIST')
    for p in lst:
        C.read_bytes_pinned(p, roots, 'approved producer')
    return lst, ref


def _proof(path_or_pin, gate, roots):
    pin = path_or_pin if isinstance(path_or_pin, dict) else C.pin_of(path_or_pin, roots, gate + ' proof')
    doc = C.read_json_pinned(pin, roots, gate + ' proof')
    if doc.get('schema') != C.PROOF_SCHEMA or doc.get('gate') != gate:
        raise Refusal(gate + '_PROOF_SCHEMA_OR_GATE')
    if doc.get('status') != 'TESTED' or doc.get('verdict') != 'PASS':
        raise Refusal(gate + '_PROOF_NOT_TESTED_PASS')
    return pin, doc


def assemble_bundle(row, *, eps_proof, gq_proof, lo_proof, approved, out_root, roots=(C.ART,)):
    spec = load_point_spec(row)
    ident = C.point_identity(spec)
    key = C.digest(ident)
    eps_pin, eps = _proof(eps_proof, 'EPS', roots)
    gq_pin, gq = _proof(gq_proof, 'GQ', roots)
    lo_pin, lo = _proof(lo_proof, SLOT_GATE, roots)          # an LO_ENVELOPE (or any other gate) proof is refused
    bad = [k for k in FORBIDDEN_PROOF_KEYS if k in lo]
    if bad:
        raise Refusal('LO_RHO_SLOT_PROOF_CARRIES_' + ','.join(bad).upper() + ' (A134 Q5)')
    eps_slot, lo_slot = eps.get('driver_certificate'), lo.get('driver_certificate')
    if not (C.is_pin(eps_slot) and C.is_pin(lo_slot)):
        raise Refusal('SLOT_PINS_REQUIRED')
    if lo.get('rho_record') != lo_slot:
        raise Refusal('LO_RHO_SLOT_PROOF_RHO_RECORD_DIFFERS_FROM_ITS_DRIVER_CERTIFICATE')
    eps_rec = C.read_json_pinned(eps_slot, roots, 'EPS numeric record (eps slot)', max_bytes=None)
    lo_rec = C.read_json_pinned(lo_slot, roots, 'rho record (lo slot)', max_bytes=None)
    if eps_rec.get('schema') != EPS_NUMERIC_SCHEMA or eps_rec.get('identity') != ident:
        raise Refusal('EPS_RECORD_SCHEMA_OR_POINT_MISMATCH')
    if eps_rec.get('settings') != 'registered' or eps_rec.get('full_registered_search_executed') is not True:
        raise Refusal('SMOKE_OR_PARTIAL_EPS_RECORD_REFUSED')
    if lo_rec.get('schema') != RHO_SCHEMA or lo_rec.get('gate') != 'RHO_G' or lo_rec.get('identity') != ident:
        raise Refusal('LO_SLOT_RECORD_IS_NOT_THIS_POINTS_RHO_RECORD')
    if lo_rec.get('settings') != 'registered' or lo_rec.get('full_registered_search_executed') is not True \
            or lo_rec.get('coverage_complete') is not True:
        raise Refusal('SMOKE_OR_PARTIAL_RHO_RECORD_REFUSED')
    custody = eps_rec.get('custody')
    if not isinstance(custody, dict) or set(custody) != {'grid_sha256', 'background_sha256', 'geometry_sha256',
                                                          'modules_sha256', 'row_contract_sha256'}:
        raise Refusal('CUSTODY_FIVE_KEYS_REQUIRED')
    if lo_rec.get('custody') != custody:
        raise Refusal('CUSTODY_MISMATCH_BETWEEN_SLOT_RECORDS')
    csha = C.digest(custody)
    for gate, doc in (('EPS', eps), ('GQ', gq), (SLOT_GATE, lo)):
        if doc.get('point_sha256') != key:
            raise Refusal(gate + '_POINT_MISMATCH')
        if doc.get('custody_sha256') != csha:
            raise Refusal(gate + '_CUSTODY_MISMATCH')
        if doc.get('producer') not in approved:
            raise Refusal(gate + '_PRODUCER_NOT_APPROVED (whole-dict pin, wrapper r10_c4 L158)')
    if gq.get('all_production_kperp_nodes') is not True or gq.get('nodes_tested') != gq.get('production_nodes'):
        raise Refusal('PARTIAL_GQ_PROOF_REFUSED')
    bundle = {'schema': C.BUNDLE_SCHEMA, 'identity': ident, 'custody': custody, 'domain': dict(C.DOMAIN),
              'prelaunch': {'EPS': eps_pin, 'GQ': gq_pin, SLOT_GATE: lo_pin},
              'driver_certificate_bindings': {'eps_certificate': eps_slot, 'lo_certificate': lo_slot},
              'acceptance_rule': C.ACCEPTANCE_RULE, 'point_sha256': key, 'custody_sha256': csha,
              'point_label': row['label'], 'generator': generator_pin(), 'utc': C.utc(),
              'custody_source': 'EPS numeric record custody; the verifier re-derives custody independently'}
    pin = C.write_new(os.path.join(out_root, 'BUNDLE_P%02d_%s.json' % (row['row'], key[:16])), bundle, out_root)
    if os.path.getsize(pin['path']) > C.EIGHT_MIB:
        raise Refusal('BUNDLE_EXCEEDS_8_MIB')
    return pin


def assemble_registry(bundle_paths, *, approved, out_root, roots=(C.ART,)):
    table = {r['key']: r for r in C.point_rows()}
    points, manifest_pins, deps = {}, [], {}
    for bp in bundle_paths:
        pin = C.pin_of(bp, roots, 'bundle')
        b = C.read_json_pinned(pin, roots, 'bundle')
        if b.get('schema') != C.BUNDLE_SCHEMA:
            raise Refusal('BUNDLE_SCHEMA')
        ident = b.get('identity')
        key = C.digest(ident)
        if key not in table:
            raise Refusal('BUNDLE_POINT_NOT_IN_31_POINT_TABLE: ' + key[:16])
        if ident != C.point_identity(load_point_spec(table[key])):
            raise Refusal('BUNDLE_IDENTITY_DIFFERS_FROM_PINNED_SPEC')
        if key in points:
            raise Refusal('DUPLICATE_POINT_IN_REGISTRY: ' + key[:16])
        slots = b.get('driver_certificate_bindings') or {}
        if set(slots) != {'eps_certificate', 'lo_certificate'} or not all(C.is_pin(v) for v in slots.values()):
            raise Refusal('BUNDLE_SLOT_BINDINGS')
        eps_rec = C.read_json_pinned(slots['eps_certificate'], roots, 'EPS numeric record', max_bytes=None)
        deps[key] = C.digest({'dependencies': eps_rec.get('dependencies'), 'producer': eps_rec.get('producer')})
        for gate in ('EPS', 'GQ', SLOT_GATE):
            proof = C.read_json_pinned(b['prelaunch'][gate], roots, gate + ' proof')
            if proof.get('producer') not in approved:
                raise Refusal(gate + '_PRODUCER_NOT_APPROVED')
            manifest_pins.append({'role': gate + '_proof', 'point': key, 'pin': b['prelaunch'][gate]})
            manifest_pins.append({'role': gate + '_producer', 'point': key, 'pin': proof['producer']})
        points[key] = {'identity': ident, 'bundle': pin, 'eps_certificate': slots['eps_certificate'],
                       'lo_certificate': slots['lo_certificate']}
        manifest_pins += [{'role': 'bundle', 'point': key, 'pin': pin},
                          {'role': 'eps_slot', 'point': key, 'pin': slots['eps_certificate']},
                          {'role': 'lo_slot', 'point': key, 'pin': slots['lo_certificate']}]
    if not points:
        raise Refusal('EMPTY_REGISTRY')
    if len(set(deps.values())) != 1:
        raise Refusal('EPS_SOURCE_PINS_DIFFER_ACROSS_POINTS (upstream code or data drifted during CP-1)')
    reg = {'schema': REGISTRY_SCHEMA, 'generator': generator_pin(),
           'common': {'path': COMMON_PATH, 'sha256': COMMON_SHA}, 'utc': C.utc(), 'points': points,
           'count': len(points), 'complete_31_point_table': len(points) == len(C.POINTS),
           'missing_points': [r['key'] for r in C.point_rows() if r['key'] not in points],
           'eps_source_pins_digest': next(iter(deps.values())),
           'record_rule': ('points[key] = {identity, bundle, eps_certificate, lo_certificate} (core L249-259, wrapper L86-90); '
                           'lo_certificate is the registered rho record (wrapper v002 L165)')}
    stamp = C.utc_compact()
    rpin = C.write_new(os.path.join(out_root, 'REGISTRY_%02dpts_%s.json' % (len(points), stamp)), reg, out_root)
    man = {'schema': 'S4RC1_C1_REGISTRY_MANIFEST_C3V002', 'utc': C.utc(), 'registry': rpin,
           'generator': generator_pin(), 'approved_certificate_producers': approved,
           'c1_tail_readiness_fields': {'certificate_registry': rpin, 'approved_certificate_producers': approved,
                                        'custody_deriver': C.canonical_pin('custody'),
                                        'state_enumerator': C.canonical_pin('state_enumerator')},
           'guard': wrapper_l30_guard_pin(), 'wrapper': C.canonical_pin('wrapper_q5b1'), 'slot_rule': SLOT_RULE,
           'pins': manifest_pins,
           'note': 'DRAFT for root: C1 content and certificate_policy_review are root items (brief 1.5, 6 Q9).'}
    mpin = C.write_new(os.path.join(out_root, 'REGISTRY_MANIFEST_%02dpts_%s.json' % (len(points), stamp)), man, out_root)
    return rpin, mpin


def real_custody_fn(deriver_pin=None):
    ref = deriver_pin or C.canonical_pin('custody')
    mod = C.load_exact(ref['path'], ref['sha256'], 's4rc1_verify_custody_cx2v002')
    return lambda spec: mod.derive_custody(spec=spec, driver_sha256=C.DRIVER_SHA)


def real_guard():
    """The guard that wrapper v002 L30 loads (path and sha read from the 7a6af535 bytes): b1 9e3fc109."""
    g = wrapper_l30_guard_pin()
    return C.load_exact(g['path'], g['sha256'], 's4rc1_verify_guard_l30_c3v003')


def c1_policy_gate(c1_ref, registry_ref, *, roots=(C.ART,), canonical_producers=None):
    """F3: wrapper r10_c4 certificate_policy_gate (L59-77) on the C1 document's tail_readiness, with the
    certificate_policy_review checked_gate of core dc895f8a L66-82, plus fail-closed canonical pins: the custody
    deriver and every approved producer must equal the canonical pins, and the C1 must name the registry being
    verified. Returns (tail_readiness or None, blockers); no blockers means the gate passed. canonical_producers
    defaults to the canonical GQ/EPS pins (common CANONICAL_APPROVED_PRODUCERS); the CLI never overrides it.
    """
    try:
        doc = C.read_json_pinned(c1_ref, roots, 'C1 document')
        r = doc.get('tail_readiness') if isinstance(doc, dict) else None
        if not isinstance(r, dict):
            return None, ['TAIL_READINESS_CONFIG_REQUIRED']                                      # L45-46
        missing = [k for k in C1_REQUIRED_PINS if not isinstance(r.get(k), dict)]                  # L61-62
        producers = r.get('approved_certificate_producers')
        if not isinstance(producers, list) or not producers:                                      # L63-65
            missing.append('approved_certificate_producers')
        if missing:
            return r, ['CERTIFICATE_POLICY_PENDING: ' + ','.join(missing)]                        # L66
        canon = ([C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS] if canonical_producers is None
                 else list(canonical_producers))
        bad = ([] if r['custody_deriver'] == C.canonical_pin('custody') else
               ['C1_CUSTODY_DERIVER_NOT_CANONICAL: %r' % (r['custody_deriver'],)])
        bad += ['C1_APPROVED_PRODUCER_NOT_CANONICAL: %r' % (p,) for p in producers if p not in canon]
        if r['certificate_registry'] != registry_ref:
            bad.append('C1_CERTIFICATE_REGISTRY_IS_NOT_THE_VERIFIED_REGISTRY (wrapper L87 reads the C1 pin)')
        if bad:
            return r, bad
        for k in C1_REQUIRED_PINS:                                                                # L68
            C.read_bytes_pinned(r[k], roots, 'C1 ' + k)
        for p in producers:                                                                       # L69
            C.read_bytes_pinned(p, roots, 'C1 approved certificate producer')
        rv = C.read_json_pinned(r['certificate_policy_review'], roots, 'certificate policy review')  # L70-75
        want = {'driver_sha256': C.DRIVER_SHA, 'custody_deriver': r['custody_deriver'],
                'state_enumerator': r['state_enumerator'], 'approved_certificate_producers': producers,
                'guard_sha256': wrapper_l30_guard_pin()['sha256'], 'driver_slot_rule': SLOT_RULE,
                'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
        bad = [] if rv.get('schema') == POLICY_SCHEMA else ['wrong evidence schema']              # core L72-78
        if rv.get('status') != 'TESTED' or rv.get('ok') is not True:
            bad.append('evidence is not TESTED ok')
        return r, bad + ['binding mismatch: ' + k for k, v in want.items() if rv.get(k) != v]
    except (Refusal, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return None, [type(exc).__name__ + ': ' + str(exc)]


def verify_point(row, registry, *, approved, custody_fn, guard, roots=(C.ART,), guard_roots=None, policy_blockers=(),
                 block=None, primitives=None):
    """Wrapper v002 certificate_check(phase='prelaunch') replica: L80-93 transcribed, L145-191 executed from the 7a6af535
    bytes, then the L30 guard's verify_bundle (L192-194)."""
    res = {'row': row['row'], 'label': row['label'], 'key': row['key'], 'wrapper_replica': {'ok': False, 'blockers': []},
           'guard_b1': None}
    fail = res['wrapper_replica']['blockers'].append
    try:
        if policy_blockers:                                                               # F3: the C1 gate, L81-82
            raise Refusal('CERTIFICATE_POLICY_GATE: ' + '; '.join(policy_blockers))
        if not isinstance(approved, list) or not approved or not all(C.is_pin(p) for p in approved):
            raise Refusal('CERTIFICATE_POLICY_PENDING: approved_certificate_producers')   # L63-66
        spec = load_point_spec(row)
        validate_block(spec['numerics'])                                                  # L80
        if spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc'] != 128.0:
            raise Refusal('CERTIFICATE_BLOCK_K_MISMATCH')                                  # L84-85
        ident = C.point_identity(spec)
        key = C.digest(ident)
        rec = (registry.get('points') or {}).get(key)
        if not isinstance(rec, dict) or rec.get('identity') != ident:
            raise Refusal('CERTIFICATE_POINT_MISSING_OR_MISMATCHED')                       # L86-90
        filled = copy.deepcopy(spec)                                                       # core Mapper L249-259
        for field in ('eps_certificate', 'lo_certificate'):
            ref = rec[field]
            C.read_bytes_pinned(ref, roots, field, max_bytes=None)
            filled['numerics']['uv_tail'][field] = copy.deepcopy(ref)
        if C.point_identity(filled) != ident:
            raise Refusal('SLOT_FILL_CHANGED_IDENTITY')
        custody = custody_fn(filled)                                                       # L92-93
        bundle_ref = rec['bundle']
        bundle = C.read_json_pinned(bundle_ref, roots, 'point certificate bundle')        # L140
        fn, info = block or wrapper_slot_block()
        M, O, Error = primitives or wrapper_primitives(roots)
        res['wrapper_replica']['block'] = info
        try:                                                                              # L145-191, the 7a6af535 bytes
            fn(filled, bundle, custody, ident, {'approved_certificate_producers': approved}, rec, 'prelaunch', M, O, guard, Error)
        except Exception as exc:
            raise Refusal('WRAPPER_V002_L145_L191: %s: %s' % (type(exc).__name__, exc))
        res['wrapper_replica']['ok'] = True
        kw = {} if guard_roots is None else {'allowed_roots': guard_roots}
        res['guard_b1'] = guard.verify_bundle(bundle_ref, ident, expected_custody=custody,       # L192-194
                                              approved_producer_sha256=[p['sha256'] for p in approved],
                                              phase='prelaunch', required_states=[], **kw)
    except (Refusal, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        fail(type(exc).__name__ + ': ' + str(exc))
    g = res['guard_b1'] or {}
    res['ok'] = res['wrapper_replica']['ok'] and g.get('ok') is True
    return res


def verify_registry(registry_ref, rows, *, c1_ref, custody_loader, guard, roots=(C.ART,), guard_roots=None,
                    canonical_producers=None):
    """F3: the approved producers and the custody deriver come from the C1 document (c1_ref), never from a
    separate list or a hard-coded pin; custody_loader(deriver_pin) returns the custody function."""
    registry = C.read_json_pinned(registry_ref, roots, 'certificate registry')
    if registry.get('schema') != REGISTRY_SCHEMA:
        raise Refusal('REGISTRY_SCHEMA')
    tr, policy = c1_policy_gate(c1_ref, registry_ref, roots=roots, canonical_producers=canonical_producers)
    approved, custody_fn = None, None
    if not policy:
        approved = tr['approved_certificate_producers']
        custody_fn = custody_loader(tr['custody_deriver'])          # the C1's deriver (equal to the canonical pin)
    out = [verify_point(r, registry, approved=approved, custody_fn=custody_fn, guard=guard, roots=roots,
                        guard_roots=guard_roots, policy_blockers=policy) for r in rows]
    return {'schema': 'S4RC1_C1_REGISTRY_OFFLINE_VERIFY_C3V003', 'utc': C.utc(), 'registry': registry_ref,
            'c1': c1_ref, 'c1_policy_gate': {'ok': not policy, 'blockers': policy, 'approved_certificate_producers': approved,
                                             'custody_deriver': (tr or {}).get('custody_deriver')},
            'generator': generator_pin(), 'guard': wrapper_l30_guard_pin(), 'wrapper': C.canonical_pin('wrapper_q5b1'),
            'points': out, 'ok': not policy and all(x['ok'] for x in out), 'n_ok': sum(x['ok'] for x in out), 'n': len(out),
            'scope': 'offline replica against root\'s wrapper v002 7a6af535 (core dc895f8a): certificate_policy_gate '
                     'L59-77 on the C1 tail_readiness (L61-62 required pins, L63-66 producers, L67-75 '
                     'certificate_policy_review checked_gate = core L66-82, root\'s L74 slot rule, guard_sha256 = the L30 '
                     'guard), with the custody deriver and the approved producers read from the C1 and required to equal '
                     'the canonical pins; prelaunch certificate_check L80-93 and L140 transcribed; L145-191 EXECUTED from the '
                     '7a6af535 bytes (AST-extracted); the L30 guard (b1 9e3fc109) verify_bundle (L192-194). NOT replicated: '
                     'Context construction (L43-57: driver pin, parent config validation), the sensitivity and other '
                     'prelaunch gates, and the guard007/guard009 fence (R1). Not launch authorization.'}


def _out_root(p, lane_root=C.LANE_ROOT):
    """F5: an existing, canonical <lane_root>/registry_<name> folder; never build_* or any other folder."""
    p = C.require_policy(p, (lane_root,), 'out-root')
    name = os.path.basename(p)
    if os.path.dirname(p) != lane_root or not name.startswith('registry_') or name == 'registry_':
        raise Refusal('ASSEMBLER_OUT_ROOT_MUST_BE %s/registry_<name> (never build_*): %s' % (lane_root, p))
    if os.path.realpath(p) != p or not os.path.isdir(p):
        raise Refusal('OUT_ROOT_MUST_EXIST_AND_BE_CANONICAL: ' + p)
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('bundle')
    for a in ('--out-root', '--point', '--eps-proof', '--gq-proof', '--lo-proof', '--approved-producers'):
        b.add_argument(a, required=True)
    r = sub.add_parser('registry')
    r.add_argument('--out-root', required=True)
    r.add_argument('--bundle', action='append', required=True)
    r.add_argument('--approved-producers', required=True)
    v = sub.add_parser('verify')
    v.add_argument('--registry', required=True)
    v.add_argument('--registry-sha256', required=True)
    v.add_argument('--c1', required=True)             # F3: the C1 document; producers and custody deriver come from it
    v.add_argument('--c1-sha256', required=True)
    v.add_argument('--points')
    v.add_argument('--out-root')
    ns = ap.parse_args(argv)
    try:
        if ns.cmd in ('bundle', 'registry'):
            approved, _ = load_approved(ns.approved_producers, (C.ART,))
        if ns.cmd == 'bundle':
            sel = C.select_points(ns.point)
            if len(sel) != 1:
                raise Refusal('ONE_POINT_REQUIRED')
            pin = assemble_bundle(sel[0], eps_proof=ns.eps_proof, gq_proof=ns.gq_proof, lo_proof=ns.lo_proof,
                                  approved=approved, out_root=_out_root(ns.out_root))
            print(json.dumps({'bundle': pin}))
            return 0
        if ns.cmd == 'registry':
            rpin, mpin = assemble_registry(ns.bundle, approved=approved, out_root=_out_root(ns.out_root))
            print(json.dumps({'registry': rpin, 'manifest': mpin}))
            return 0
        if not C.background_qos():
            raise Refusal('BACKGROUND_QOS_REQUIRED for custody derivation: run under taskpolicy -b')
        ref = {'path': C.require_canonical(ns.registry), 'sha256': ns.registry_sha256}
        c1_ref = {'path': C.require_canonical(ns.c1), 'sha256': ns.c1_sha256}
        rep = verify_registry(ref, C.select_points(ns.points), c1_ref=c1_ref, custody_loader=real_custody_fn,
                              guard=real_guard())
        if ns.out_root:
            pin = C.write_new(os.path.join(_out_root(ns.out_root), 'VERIFY_%s_%s.json' % (ns.registry_sha256[:12],
                              C.utc_compact())), rep, _out_root(ns.out_root))
            rep['written'] = pin
        print(json.dumps({'ok': rep['ok'], 'n_ok': rep['n_ok'], 'n': rep['n'], 'written': rep.get('written'),
                          'c1_policy_gate_blockers': rep['c1_policy_gate']['blockers']}))
        return 0 if rep['ok'] else 3
    except Refusal as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
