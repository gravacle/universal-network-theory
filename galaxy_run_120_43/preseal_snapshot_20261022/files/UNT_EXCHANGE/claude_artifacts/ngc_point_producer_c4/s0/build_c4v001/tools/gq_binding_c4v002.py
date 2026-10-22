"""Claude4 S0 build_c4v001: the per-point NGC GQ binding record for ONE point of a pinned S0 record.  No GQ compute is run (A132
D2(a): "Per-point NGC GQ is a re-binding of be148bab, with no new compute"; A135 item 2 "GQ: re-bound to be148bab"; 0695 item 3).
Successor of gq_binding_c4v001.py (9aaf00bc): the same re-binding, now bound to one point (the theta record pin, the point key and
role, theta_key recomputed by s0theta_c4v001; no other point's key is written), with Claude3 0184 item 11's open item carried.
Reads, each sha-checked from its bytes before any parse: the S0 record (pin on the command line; SMOKE mode: the anchor record
ce26ced9), GQ_NGC_91_MS96_V001.json (be148bab) and its producer gq_ngc91_cxv001.py (ab07c00c).  Read with the sha recorded at read
(open documents): the V006 root addendum (the A132 D2(a) and A135 item 2 lines), dispatch 0685 (D2(a)), dispatch 0695 (item 3).
Writes out/S0_GQ_BINDING_<key16>_C4V002_<run>.json (SMOKE: out/SMOKE_ANCHOR_GQ_BINDING_C4V002_<run>.json), exclusive create.
No GQ, LO, rho or per-state number is computed.
usage: run_fenced_c4st4.py tools/gq_binding_c4v002.py <sha256 of this file> --run-id R
       (--s0-record P --s0-sha256 H --point-key K | --smoke-anchor 1)"""
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
PINLOAD = (os.path.join(TOOLS, 'pinload_c4v002.py'), 'b8ae4b06802b563848f6de6b2d349d5e806574b9661026614937cda4fb685067')
S0THETA = (os.path.join(TOOLS, 's0theta_c4v001.py'), '950d774a794d50315857cb1fcc901d829f9136cc60e78d45ecbc9117dfa7fd3a')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
GQ = (ART + '/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json', 'be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76')
GQ_PRODUCER = (ART + '/ngc_ntest_eval_cx/gq_ngc91_cxv001.py', 'ab07c00c3877f9a46bd6fd3c55f6ff067765f28c09809fbe355c35f98545dd54')
D0685 = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0685_2026-10-19_A132_RI45-06_D1_D2_rulings_parallel_routeA_question.md'
D0695 = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0695_2026-10-19_A135_step5_path_review_and_NGC_slot_proof.md'
ANCHOR_SAMPLES = (ART + '/tail_scheme_impl_c2/certificates_ngc_k32/out/EPS_NGC91_SAMPLES_V001.json',
                  'ce26ced9d3e864fa158e8f38bd20d83eea1d5e7de1533c3633354fa99571c1a5')
SCHEMA = 'UNT_CLAUDE4_S0_POINT_GQ_BINDING_C4V002'
OPEN_ITEM = ('Carried open item (Claude3 0184 item 11; CRITIC P3; the c4v001 binding): whether the GEOMETRY_UNIFORM bound premise '
             'nonnegative_masses_required holds on iterated route-A rosters (masses cm*(-J/c^2)) is in-run and UNTESTED; be148bab '
             'covers only the saved pre-launch roster.')
NO_LO = 'No GQ compute, and no LO, rho or per-state acceptance number is computed, read or written (A132 D2(a); 0679; A134).'


def hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def bootstrap(path_sha, name):
    with open(path_sha[0], 'rb') as f:
        b = f.read()
    if hashlib.sha256(b).hexdigest() != path_sha[1]:
        raise SystemExit('%s pin mismatch' % name)
    m = importlib.util.module_from_spec(importlib.machinery.ModuleSpec(name, None, origin=path_sha[0]))
    m.__file__ = path_sha[0]
    sys.modules[name] = m
    exec(compile(b, path_sha[0], 'exec', dont_inherit=True), m.__dict__)
    return m


def args():
    a = sys.argv[1:]
    allowed = ('--run-id', '--s0-record', '--s0-sha256', '--point-key', '--smoke-anchor')
    if len(a) % 2:
        raise SystemExit('arguments come in pairs')
    out = {}
    for i in range(0, len(a), 2):
        if a[i] not in allowed or a[i] in out:
            raise SystemExit('unknown or repeated argument ' + a[i])
        out[a[i]] = a[i + 1]
    rid = out.get('--run-id')
    if not rid or not rid.isascii() or not rid.isalnum():
        raise SystemExit('--run-id <alnum> required')
    point = any(k in out for k in ('--s0-record', '--s0-sha256', '--point-key'))
    if point == ('--smoke-anchor' in out):
        raise SystemExit('exactly one mode: --s0-record P --s0-sha256 H --point-key K, or --smoke-anchor 1')
    if point:
        if not all(k in out for k in ('--s0-record', '--s0-sha256', '--point-key')):
            raise SystemExit('point mode needs --s0-record, --s0-sha256 and --point-key')
        if not (hex64(out['--s0-sha256']) and hex64(out['--point-key']) and out['--s0-record'].startswith('/')):
            raise SystemExit('--s0-sha256 / --point-key must be 64 lowercase hex and --s0-record absolute')
        return dict(mode='point', run_id=rid, s0_record=out['--s0-record'], s0_sha=out['--s0-sha256'], point_key=out['--point-key'])
    if out['--smoke-anchor'] != '1':
        raise SystemExit('--smoke-anchor 1')
    return dict(mode='smoke', run_id=rid)


def read_at(path):
    with open(path, 'rb') as f:
        b = f.read()
    return b, hashlib.sha256(b).hexdigest()


def section_lines(text, header, test):
    lines = text.splitlines()
    hs = [i for i, s in enumerate(lines) if s.startswith(header)]
    if len(hs) != 1:
        raise SystemExit('section %r not found exactly once' % header)
    i0 = hs[0]
    i1 = next((j for j in range(i0 + 1, len(lines)) if lines[j].startswith('## ')), len(lines))
    hit = [(j + 1, lines[j]) for j in range(i0, i1) if test(lines[j])]
    if len(hit) != 1:
        raise SystemExit('line not found exactly once in %r' % header)
    return dict(section_lines=[i0 + 1, i1], line=hit[0][0], text=hit[0][1])


def main():
    A = args()
    F = sys.modules.get('fence_c4v004')
    if F is None or getattr(F, 'FENCE_VERSION', None) != 'fence_c4v004':
        raise SystemExit('run only under tools/run_fenced_c4st4.py (fence_c4v004 is not installed)')
    P = bootstrap(PINLOAD, 'pinload_c4v002')
    P.install_guard()
    S = P.load_verified_module(S0THETA[0], S0THETA[1], 's0theta_c4v001', 's0theta_c4v001')
    if A['mode'] == 'point':
        TH = S.s0_point(P.read_verified(A['s0_record'], A['s0_sha'], 'S0 record (theta source)'), A['s0_record'], A['s0_sha'],
                        A['point_key'])
        name = 'out/S0_GQ_BINDING_%s_C4V002_%s.json' % (A['point_key'][:16], A['run_id'])
        label = ('S0 POINT GQ BINDING (no GQ compute): this point binds GQ_NGC_91_MS96_V001 (be148bab) under A132 D2(a); not a '
                 'registered slot record (A132 D3 deferred until registration)')
    else:
        TH = S.anchor_smoke_theta(P.read_verified(ANCHOR_SAMPLES[0], ANCHOR_SAMPLES[1], 'anchor samples (SMOKE theta source)'),
                                  ANCHOR_SAMPLES[0], ANCHOR_SAMPLES[1])
        name = 'out/SMOKE_ANCHOR_GQ_BINDING_C4V002_%s.json' % A['run_id']
        label = 'SMOKE TEST of the S0 GQ binding writer at the anchor theta: NOT a binding of record, never to be pinned'
    rec = json.loads(P.read_verified(GQ[0], GQ[1], 'GQ_NGC_91_MS96_V001'))
    P.read_verified(GQ_PRODUCER[0], GQ_PRODUCER[1], 'gq_ngc91_cxv001')
    v6_b, v6_sha = read_at(P.PERMITTED_ADDENDA[0])
    d5_b, d5_sha = read_at(D0685)
    d9_b, d9_sha = read_at(D0695)
    v6 = v6_b.decode()
    a132 = section_lines(v6, '## A132', lambda s: s.startswith('- **D2 (a).**'))
    a135 = section_lines(v6, '## A135', lambda s: '**GQ:**' in s)
    d685 = [(j + 1, s) for j, s in enumerate(d5_b.decode().splitlines()) if s.startswith('**D2 (a).**')]
    d695 = [(j + 1, s) for j, s in enumerate(d9_b.decode().splitlines()) if s.startswith('3. **Claude4.**')]
    if len(d685) != 1 or len(d695) != 1:
        raise SystemExit('the 0685 D2 (a) line or the 0695 item 3 line is not found exactly once')
    r0 = rec['rosters'][0]
    if rec['verdict'] != 'PASS' or r0['seconds'] != 545.0:
        raise SystemExit('the record of record is not the one cited by A132 D2(a)')
    out = dict(
        schema=SCHEMA + ('_SMOKE_ANCHOR' if A['mode'] == 'smoke' else ''), label=label, binding_of_record=bool(A['mode'] == 'point'),
        utc=P.utc(), run_id=A['run_id'],
        theta_record_pin=dict(TH['record'], point_key=TH['point'].get('key'), point_role=TH['point'].get('role')),
        point=dict(key=TH['point'].get('key'), role=TH['point'].get('role'), theta_hex=TH['point'].get('theta_hex')),
        key_check=TH.get('key_check'),
        ruling=dict(id='A132 D2(a); A135 item 2',
                    addendum=dict(path=P.PERMITTED_ADDENDA[0], sha256_at_read=v6_sha, a132_d2=a132, a135_gq=a135),
                    dispatch_0685=dict(path=D0685, sha256_at_read=d5_sha, line=d685[0][0], text=d685[0][1]),
                    dispatch_0695=dict(path=D0695, sha256_at_read=d9_sha, line=d695[0][0], text=d695[0][1])),
        bound_record=dict(path=GQ[0], sha256=GQ[1], bytes=[v['bytes'] for v in P.VERIFIED if v['path'] == GQ[0]][0],
                          producer=dict(path=GQ_PRODUCER[0], sha256=GQ_PRODUCER[1], equals_record_producer_field=bool(
                              rec['producer']['path'] == GQ_PRODUCER[0] and rec['producer']['sha256'] == GQ_PRODUCER[1])),
                          schema=rec['schema'], gate=rec['gate'], label=rec['label'], verdict=rec['verdict'],
                          coverage_inverse_kpc=rec['coverage_inverse_kpc'], threshold_over_P0=rec['threshold_over_P0'],
                          function_sources=rec['function_sources'], note=rec['note'], roster0=r0),
        timing_of_record=dict(seconds=r0['seconds'], source='GQ_NGC_91_MS96_V001.json rosters[0].seconds (be148bab)',
                              context='no log file and no memory figure in the record; contention at the time not recorded'),
        point_binding=dict(
            rule='every step-5 NGC point binds this one record for GQ (A132 D2(a); A135 item 2); no per-point GQ compute',
            basis=('the GQ input is the saved initial-gas roster (rosters[0].provenance.scope "NGC saved initial-gas roster only"; '
                   'M_s 96, Kbig 91) with no point parameter in the producer call (Claude3 review of record: gq_ngc91_cxv001 L24 calls '
                   'gq_roster2 on the saved gas roster; MAP_u2_producers section 3 item 7; CRITIC P3) [FORMAL]'),
            carried_open_item=OPEN_ITEM),
        no_compute=True, no_lo_rho_per_state=NO_LO, verified=P.VERIFIED, guard=P.guard_report())
    w = P.write_new_json(name, out)
    print(json.dumps(dict(GQ_BINDING=w['sha256'], path=w['path'], point_key=TH['point'].get('key'), seconds_of_record=r0['seconds'],
                          verdict=rec['verdict'])), flush=True)


if __name__ == '__main__':
    main()
