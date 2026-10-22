"""selfcheck_contract_c2v004.py -- the contract self-check (K-rows) of FREEZE_EXPECTED_INPUTS_C2V004 (s0_launch_kit_c2).

It checks the rows Claude4 0223 found BLOCKING (B1 notes, B2 spec) and the two items A163 folds in (N2 interior_count,
V-N1 Phase-2 allow_incomplete) against the pinned bytes, in memory.  It writes nothing.
  K1  spec row: value.spec_of_record is canonically equal to the recipe rebuilt here from the pinned bytes,
      make_freeze_coordinate_spec(apply_coordinate_mode(CX2V006 coordinates + slots V003 ngc3198_slots,
      COORDINATE_ADDENDUM_CX2V006 coordinate_mode).coordinates).spec; its sha256 equals the recorded one, and the spec
      file (value.file) holds exactly its canonical bytes at that sha256; the mode is
      DDO154_DISTANCE_FIXED_AT_REGISTERED; its two NGC3198 slots are slots V003's; a member theta_ngc carries the
      registered geometry 13.8 Mpc / 72 deg.
  K2  engine part: the spec's engine_coordinates (canonical JSON) equal (a) those of the phase1 freeze_spec build from
      CX2V006's placeholder slots, (b) orchestrator c2v005 Context._apply_coordinate_mode applied to CX2V006
      engine_coordinates (the campaign derivation, orchestrator L1656-1665), and (c) the recorded sha256; and the
      orchestrator's V001 equality (L1663) holds for both slot sources.
  K3  notes row: every key of slots V003 notes_block_for_manifest is present and equal; structural_assumptions carries
      exactly one more entry, with section A18, whose text_verbatim is the V004 A18 section read from bytes (lines and
      section sha256 as recorded); the only other extra keys are A13 and A16.1; v003g _safe_scan finds no target name.
  K4  the notes pass v003g _check_slot_geometry and _headline_conditions with the spec of record (a sensitivity with no
      evaluation entries), and fail both with the placeholder spec (control inside the row).
  K5  interior_count: value 5 (int), status ROOT_DECLARED_IN_V006, the cited V006 line names 5, and every IC-* check
      row requires 5.
  K6  allow_incomplete: phase1 true; phase2 carries the V-N1 rule (A163) with its deciding record and the two
      dispositions UNEVALUATED_CAP and UNEVALUATED_STEP7_DISCREPANCY.
Reads only: v003g (48a1e48a), CX2V006 (50e7288e), its addendum (9962b2aa), slots V003 (d3859b42; only the keys
ngc3198_slots and notes_block_for_manifest are used), the V004 addendum (487d4449; its A18 section), orchestrator c2v005
(c75a889f; imported, "Importing this module does nothing"; only Context._apply_coordinate_mode is called) and V006
(current bytes; the lines the list cites).  It prints pass/fail and reasons only.
Usage: PY -I -B selfcheck_contract_c2v004.py LIST.json  -> JSON on stdout; exit 0 PASS, 3 REFUSED, 2 usage
"""
import copy
import hashlib
import importlib.util
import json
import sys

SCHEMA = 'UNT_FREEZE_CONTRACT_SELFCHECK_C2V004'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
UNTPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
V003G = (A + 'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
         '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405')
SLOTS = (A + 'freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json',
         'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969')
CX2V006 = (A + 'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
           '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f')
ADDENDUM = (A + 'calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json',
            '9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9')
V004 = (UNTPC + 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
        '487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b')
ORCH = (A + 'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
        'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d')
V006_PATH = UNTPC + 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
A18_KEY = 'A18-ROOT-V004'
EXTRA_NOTE_KEYS = ('A13', 'A16.1')
REGISTERED_GEOMETRY = {'ngc3198_distance_Mpc': 13.8, 'ngc3198_inclination_deg': 72.0}
IC_REQUIRED_ROWS = ('IC-P1-HANDOFF', 'IC-P1-FDPLAN', 'IC-P1-MEMBERS', 'IC-P1-FREEZE', 'IC-P2-SELECTION', 'IC-P2-PLAN',
                    'IC-P2-AT1', 'IC-P2-FREEZE')
VN1_DISPOSITIONS = ['UNEVALUATED_CAP', 'UNEVALUATED_STEP7_DISCREPANCY']


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def pinned(pin):
    with open(pin[0], 'rb') as fh:
        b = fh.read()
    if sha_bytes(b) != pin[1]:
        raise SystemExit('PIN MISMATCH: %s does not hash to %s' % (pin[0], pin[1]))
    return b


def load_module(pin, name):
    pinned(pin)
    sp = importlib.util.spec_from_file_location(name, pin[0])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    pinned(pin)
    return m


def slots_allowed():
    """slots V003: only ngc3198_slots and notes_block_for_manifest leave this function (task rule; A141)."""
    d = json.loads(pinned(SLOTS))
    return {'ngc3198_slots': d['ngc3198_slots'], 'notes_block_for_manifest': d['notes_block_for_manifest']}


def a18_section(raw):
    """The V004 A18 section, verbatim: its heading line through the last non-blank line before the next '## '."""
    lines = raw.decode('utf-8').split('\n')
    starts = [i for i, s in enumerate(lines) if s.startswith('## A18:')]
    if len(starts) != 1:
        raise ValueError('V004 has %d A18 headings' % len(starts))
    s = starts[0]
    e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith('## '))
    body = lines[s:e]
    while body and not body[-1].strip():
        body.pop()
    text = '\n'.join(body)
    return text, s + 1, s + len(body), sha_bytes(text.encode('utf-8'))


def build_spec(G, cx, ngc, cm):
    am = G.apply_coordinate_mode(coordinates=copy.deepcopy(list(cx['coordinates'])) + copy.deepcopy(list(ngc)),
                                 coordinate_mode=copy.deepcopy(cm))
    if not am.get('ok'):
        raise ValueError('apply_coordinate_mode: %s' % am.get('reasons'))
    fs = G.make_freeze_coordinate_spec(coordinates=am['coordinates'])
    if not fs.get('ok'):
        raise ValueError('make_freeze_coordinate_spec: %s' % fs.get('reasons'))
    return fs


class Ctx:
    def __init__(self):
        self.G = load_module(V003G, 'c2v004_contract_v003g')
        self.O = load_module(ORCH, 'c2v004_contract_orch')
        self.slots = slots_allowed()
        self.cx = json.loads(pinned(CX2V006))
        self.add = json.loads(pinned(ADDENDUM))
        self.v004 = pinned(V004)
        with open(V006_PATH, 'rb') as fh:
            self.v006 = fh.read()


def kw_rows(doc):
    return {e.get('kwarg'): e for e in doc.get('write_freeze_manifest_inputs') or []}


def check(doc, ctx=None):
    ctx = ctx or Ctx()
    G, O = ctx.G, ctx.O
    canon = G._canonical_bytes
    rows = []

    def row(rid, fn):
        reasons = []
        try:
            fn(reasons)
        except Exception as exc:   # a malformed list is a refusal, never a pass
            reasons.append('EXCEPTION %s: %s' % (type(exc).__name__, str(exc)[:300]))
        rows.append({'id': rid, 'ok': not reasons, 'reasons': reasons[:8]})

    wfm = kw_rows(doc)
    cm = ctx.add['coordinate_mode']
    ngc_real = ctx.slots['ngc3198_slots']
    ngc_ph = ctx.cx['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']
    fs_rec = build_spec(G, ctx.cx, ngc_real, cm)
    fs_ph = build_spec(G, ctx.cx, ngc_ph, cm)

    def k1(r):
        v = wfm['spec']['value']
        spec = v['spec_of_record']
        if canon(spec) != canon(fs_rec['spec']):
            r.append('K1: spec_of_record is not the recipe rebuilt from the pinned bytes')
        if v.get('spec_canonical_sha256') != sha_bytes(canon(spec)):
            r.append('K1: spec_canonical_sha256 differs from the bytes of spec_of_record')
        f = v.get('file') or {}
        try:
            with open(f.get('path'), 'rb') as fh:
                fb = fh.read()
        except (OSError, TypeError) as exc:
            fb = None
            r.append('K1: the spec file cannot be read: %s' % type(exc).__name__)
        if fb is not None and (fb != canon(spec) or sha_bytes(fb) != f.get('sha256')):
            r.append('K1: the spec file bytes are not the canonical bytes of spec_of_record at the recorded sha256')
        reasons = []
        S = G._spec_from(spec, reasons)
        if S is None:
            r.append('K1: v003g refuses the spec: %s' % reasons[:3])
            return
        if S['coordinate_mode'] != G.MODE_D_FIXED:
            r.append('K1: coordinate mode %r is not %s' % (S['coordinate_mode'], G.MODE_D_FIXED))
        want = {c['name']: c for c in ngc_real}
        if sorted(S['ngc_nuisance_names']) != sorted(want):
            r.append('K1: NGC3198 slot names differ from slots V003')
        for nm in S['ngc_nuisance_names']:
            c, w = S['by_name'].get(nm), want.get(nm)
            if c is None or w is None:
                continue
            for f in ('lower', 'upper', 'trial_value', 'reference_value'):
                if (c[f] is None) != (w[f] is None) or (c[f] is not None and float(c[f]) != float(w[f])):
                    r.append('K1: slot %s.%s differs from slots V003' % (nm, f))
            for f in ('units', 'transform', 'kind', 'scope', 'role'):
                if c[f] != w[f]:
                    r.append('K1: slot %s.%s differs from slots V003' % (nm, f))
        th = G._theta_ngc_from_engine(S, G._theta_engine_from_u(S, [0.5] * len(S['varying_engine'])))
        geo = {nm: th[nm] for nm in S['ngc_nuisance_names']}
        if geo != REGISTERED_GEOMETRY:
            r.append('K1: a member theta_ngc carries %r, not the registered geometry %r' % (geo, REGISTERED_GEOMETRY))
        if v.get('member_theta_ngc_geometry') != REGISTERED_GEOMETRY:
            r.append('K1: recorded member_theta_ngc_geometry is not the registered geometry')

    def k2(r):
        v = wfm['spec']['value']
        e_rec = O.canonical(fs_rec['engine_coordinates'])
        e_ph = O.canonical(fs_ph['engine_coordinates'])
        camp = O.Context._apply_coordinate_mode(copy.deepcopy(ctx.cx['engine_coordinates']), copy.deepcopy(cm))
        if e_rec != e_ph:
            r.append('K2a: engine coordinates differ from the placeholder-slot (phase1 freeze_spec) build')
        if e_rec != O.canonical(camp):
            r.append('K2b: engine coordinates differ from the orchestrator campaign derivation')
        if v.get('engine_coordinates_canonical_sha256') != sha_bytes(e_rec):
            r.append('K2c: recorded engine_coordinates_canonical_sha256 differs')
        for label, ngc in (('slots V003', ngc_real), ('CX2V006 placeholder', ngc_ph)):
            fs1 = G.make_freeze_coordinate_spec(coordinates=copy.deepcopy(list(ctx.cx['coordinates'])) +
                                                copy.deepcopy(list(ngc)))
            if not fs1.get('ok') or O.canonical(fs1['engine_coordinates']) != O.canonical(ctx.cx['engine_coordinates']):
                r.append('K2d: the orchestrator V001 equality (L1663) fails with %s' % label)

    def k3(r):
        n = wfm['notes']['value']
        nbm = ctx.slots['notes_block_for_manifest']
        extra = sorted(set(n) - set(nbm))
        if extra != sorted(EXTRA_NOTE_KEYS):
            r.append('K3: notes keys beyond the slots block must be exactly %s, got %s' % (list(EXTRA_NOTE_KEYS), extra))
        for k in nbm:
            if k not in n:
                r.append('K3: notes lacks the slots block key %s' % k)
            elif k != 'structural_assumptions' and canon(n[k]) != canon(nbm[k]):
                r.append('K3: notes.%s differs from slots V003' % k)
        sa, sa0 = n.get('structural_assumptions') or {}, nbm['structural_assumptions']
        if sorted(set(sa) - set(sa0)) != [A18_KEY]:
            r.append('K3: structural_assumptions must add exactly %s' % A18_KEY)
        for k in sa0:
            if k not in sa or canon(sa[k]) != canon(sa0[k]):
                r.append('K3: structural_assumptions.%s differs from slots V003' % k)
        e = sa.get(A18_KEY) or {}
        text, l0, l1, ssha = a18_section(ctx.v004)
        if e.get('section') != 'A18' or e.get('text_verbatim') != text:
            r.append('K3: %s is not {section A18, text_verbatim = V004 A18 from bytes}' % A18_KEY)
        src = e.get('source') or {}
        if src.get('path') != V004[0] or src.get('sha256') != V004[1] or src.get('lines') != [l0, l1] or \
                src.get('section_sha256') != ssha:
            r.append('K3: %s.source does not pin the V004 bytes, lines and section sha256' % A18_KEY)
        hits, rs = [], []
        G._safe_scan(n, 'notes', hits, rs)
        if hits or rs:
            r.append('K3: forbidden target field names in notes: %s %s' % (hits[:4], rs[:2]))
        a161 = n.get('A16.1')
        if not isinstance(a161, str) or a161.encode('utf-8') not in ctx.v006:
            r.append('K3: notes.A16.1 is not a verbatim V006 text')

    def k4(r):
        n = wfm['notes']['value']
        alts = {'declared': doc['exact_alternative_declarations']['declared']}
        for label, spec, expect in (('spec of record', fs_rec['spec'], True), ('placeholder spec', fs_ph['spec'], False)):
            reasons = []
            S = G._spec_from(spec, reasons)
            a16 = G._check_slot_geometry(S, {'evaluations': [], 'per_query': []}, n, reasons)
            hc = G._headline_conditions(S, alts, a16, n, reasons)
            ok = a16 is not None and hc is not None and not reasons
            if ok != expect:
                r.append('K4: with the %s the notes %s (expected %s): %s' % (
                    label, 'pass' if ok else 'refuse', 'pass' if expect else 'refuse', [x[:120] for x in reasons[:3]]))
            if expect and ok and A18_KEY not in hc['structural_assumptions_present']:
                r.append('K4: headline_conditions does not list %s' % A18_KEY)

    def k5(r):
        ic = doc.get('interior_count') or {}
        if type(ic.get('value')) is not int or ic['value'] != 5:
            r.append('K5: interior_count.value is not the int 5')
        if ic.get('status') != 'ROOT_DECLARED_IN_V006':
            r.append('K5: interior_count.status is not ROOT_DECLARED_IN_V006')
        src = ic.get('registered_value_source') or {}
        lines = ctx.v006.decode('utf-8').split('\n')
        ln = src.get('line')
        if not isinstance(ln, int) or not 1 <= ln <= len(lines) or 'interior_count = **5**' not in lines[ln - 1] or \
                src.get('line_text') != lines[ln - 1]:
            r.append('K5: the cited V006 line does not declare interior_count = 5')
        checks = {c.get('id'): c for c in ic.get('checks') or []}
        for rid in IC_REQUIRED_ROWS:
            if rid not in checks:
                r.append('K5: check row %s missing' % rid)
            elif checks[rid].get('required_value') != 5:
                r.append('K5: check row %s does not require 5' % rid)
        if 'interior_count = 5' not in wfm['selection'].get('value_rule', ''):
            r.append('K5: the selection row does not name interior_count = 5')

    def k6(r):
        v = wfm['allow_incomplete'].get('value') or {}
        if v.get('phase1') is not True:
            r.append('K6: Phase 1 value is not true')
        p2 = v.get('phase2')
        if not isinstance(p2, dict) or p2.get('rule') != 'V-N1 (A163)' or p2.get('dispositions') != VN1_DISPOSITIONS \
                or p2.get('value_when_any') is not True or p2.get('value_otherwise') is not False or \
                not isinstance(p2.get('deciding_record'), str) or not p2['deciding_record']:
            r.append('K6: Phase 2 does not carry the V-N1 rule with its dispositions and deciding record')

    for rid, fn in (('K1', k1), ('K2', k2), ('K3', k3), ('K4', k4), ('K5', k5), ('K6', k6)):
        row(rid, fn)
    return {'schema': SCHEMA, 'ok': all(x['ok'] for x in rows), 'rows': rows}


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[1], 'rb') as fh:
        doc = json.loads(fh.read())
    r = check(doc)
    print(json.dumps(r, indent=1))
    return 0 if r['ok'] else 3


if __name__ == '__main__':
    sys.exit(main(sys.argv))
