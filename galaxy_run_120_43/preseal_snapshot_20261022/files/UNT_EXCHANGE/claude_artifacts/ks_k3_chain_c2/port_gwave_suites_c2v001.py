"""Ported predecessor suites for the G-wave (ks_k3_chain_c2 G-wave c2v001; root A175, A176): exact, counted text
substitutions only, as the wave-1 port generator (port_ks_suites_c2v001.py) does.

  python3 -I -B port_gwave_suites_c2v001.py TARGET_DIR [suite ...]

Each predecessor suite is read from its own path (sha256 checked from bytes) and written, with the substitutions listed
here and nothing else, into TARGET_DIR (the G-wave successors' folder) by exclusive create. A unified DIFF of every
port goes to TARGET_DIR/diffs/PORT_<name>.diff. A substitution points the suite at the successor file, or, where
marked PORT (G-wave), adapts a seam, a fixture or a static check to the successor (README section 5); every adaptation
is listed in the README. Each substitution is (old, new, count): old must occur exactly `count` times.
"""
import difflib
import hashlib
import json
import os
import sys

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
KS = ART + '/ks_k3_chain_c2'
B1T = ART + '/s4_acceptance_c2/offset_b1/tests'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
GW_FILES = {'G3A': 'gq_geometry_r5_cx2v001_g3_c2v001.py', 'G3B': 'gq_producer_cx2v005_g3_c2v001.py',
            'G3C': 'gq_producer_b1_c2v001_g3_c2v001.py', 'G4': 'point_response_admission_adapter_cx2v003_g4_c2v001.py',
            'G6A': 'execution_graph_cx2v002_g6_c2v001.py', 'G6B': 'current_source_evidence_b1_c2v001_g6_c2v001.py',
            'G6C': 'consumed_states_b1_c2v001_g6_c2v001.py'}
C3T_LABEL = 'S1 transfer test C3T at u_A theta 0123456789abcdef; base 89abcdef'
CB_PIN_CODE = ("{'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', "
               "'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}")


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


Q2_GWAVE_APPENDIX = r'''

# ============================================================================ GW: S1_UA_C3T acceptance (G-wave additions)
# PORT (G-wave): NEW cases, not part of the predecessor suite (README section 5). An S1_UA_C3T call through the KS6'
# handoff's own S1 path, end to end: the KS6' LO adapter (real; its four science seams as above), the G2 SRB-ROT adapter
# (real, library 2026f2b6 and r14 apply_flag; derive_details seam), the G6c enumerator (this suite's explicit enumerator
# seams), the G1 slot proof (real) binding a K=3 rho slot (KS2 producer, coverage [3, 182], 10 shells) with the K=4
# anchor pair, guard KS5 (domain K 3), and the evidence double stamping the G6b evidence pin. Every other piece is this
# suite's synthetic call machinery, unchanged.
GW_KS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2')
GW_PIN = {k: ref(ITEM / n) for k, n in (('G1', 'lo_slot_proof_c3v003_g1_c2v001.py'), ('G2', 'srb_rot_adapter_c3v003_g2_c2v001.py'),
                                       ('G6C', 'consumed_states_b1_c2v001_g6_c2v001.py'),
                                       ('G6B', 'current_source_evidence_b1_c2v001_g6_c2v001.py'))}
G1M = load(GW_PIN['G1']['path'], 'q2gw_g1', GW_PIN['G1']['sha256'])
G2M = load(GW_PIN['G2']['path'], 'q2gw_g2', GW_PIN['G2']['sha256'])
G6CM = load(GW_PIN['G6C']['path'], 'q2gw_g6c', GW_PIN['G6C']['sha256'])
LOAD6 = HAND.load_pinned(HAND.LO_ADAPTER_KS6, 'q2gw_lo_adapter_ks6pp')
KS5G = load(GW_KS / 'certificate_guard_b1_ks5_c2v001.py', 'q2gw_ks5', 'e394ae94c6f48ff9e0919e9b186103d2f7c5b00077967579029e8404a62215d6')
LOCORE6 = load(GW_KS / 'lo_core_r5_cx2v001_ks6_c2v001.py', 'q2gw_lo_core_ks6', '2cf7c59790638cc1595a615b226143a5a3eb74e713001d85db4d469edf0b2b2f')
KS2_PIN = {'path': str(GW_KS / 'point_response_producer_cx2v002_ks2_c2v001.py'), 'sha256': '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'}
LOCORE6_PIN = {'path': str(GW_KS / 'lo_core_r5_cx2v001_ks6_c2v001.py'), 'sha256': '2cf7c59790638cc1595a615b226143a5a3eb74e713001d85db4d469edf0b2b2f'}
G6B_PIN = dict(GW_PIN['G6B'])
KS6PP_PIN = {'path': HAND.LO_ADAPTER_KS6['path'], 'sha256': HAND.LO_ADAPTER_KS6['sha256']}
GW_C3T_LABEL = 'S1 transfer test C3T at u_A theta 0123456789abcdef; base 89abcdef'
_cbraw = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json').read_bytes()
assert hashlib.sha256(_cbraw).hexdigest() == '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'
CB_C3T = json.loads(_cbraw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
IDENTITY_C3T = copy.deepcopy(IDENTITY)
IDENTITY_C3T['numerics']['composite_grid_spec'] = copy.deepcopy(CB_C3T)
RHO_SHELLS_C3T = [[3.0, 4.0]] + RHO_SHELLS
RHO_USED_C3T = [0.005] + RHO_USED


def rho_record_c3t(identity, utc, seconds, shells=None, producer=None, cov=None):
    """The KS2 rho record format at kept K 3 (coverage [3, 182], the 10-shell partition), synthetic values."""
    sh = shells or RHO_SHELLS_C3T
    used = RHO_USED_C3T if shells is None else [0.01] * len(sh)
    return {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'gate': 'RHO_G', 'status': 'TESTED',
            'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED', 'identity': identity, 'point_sha256': digest(identity),
            'custody': CUSTODY, 'producer': producer or KS2_PIN, 'settings': 'registered', 'coverage_complete': True,
            'required_coverage_inverse_kpc': cov or [3.0, 182.0], 'full_registered_search_executed': True, 'utc': utc,
            'seconds': seconds, 'covers_all_consumed_states': False, 'synthetic_fixture': True,
            'shells': [{'range_inverse_kpc': s, 'rho_used': r, 'rho_envelope': {'estimate': r, 'seed': 20261019 + i}}
                       for i, (s, r) in enumerate(zip(sh, used))]}


def g1_env(details):
    e = G1M._real_env()
    e.derive_details = lambda spec: copy.deepcopy(details)
    return e


def make_point_c3t(tag, identity, *, slot_rho=None):
    """The S1_UA_C3T point: K=3 slots, EPS proof from [3,4], the REAL G1 LO_RHO_SLOT proof, domain K 3, LR edges from 3."""
    P = SimpleNamespace(tag=tag, identity=identity, point=digest(identity))
    base = SH / tag
    P.details = {'identity': identity, 'custody': CUSTODY, 'custody_sha256': digest(CUSTODY), 'point_sha256': P.point,
                 'row_contract': ROW_CONTRACT, 'modules': {}}
    P.rho_slot = wjson(base / 'RHO_SLOT.json', slot_rho or rho_record_c3t(identity, 'slot-time', 12.5))
    P.eps_slot = wjson(base / 'EPS_SLOT.json', {
        'schema': 'UNT_POINT_EPS_NUMERICAL_CX2V001', 'gate': 'EPS', 'identity': identity, 'custody': CUSTODY,
        'point_sha256': P.point, 'status': 'TESTED', 'settings': 'registered', 'full_registered_search_executed': True,
        'coverage_complete': True, 'required_coverage_inverse_kpc': [3.0, 182.0], 'synthetic': True,
        'shells': [{'lo_inverse_kpc': float(a), 'hi_inverse_kpc': float(a + 1), 'range_inverse_kpc': [float(a), float(a + 1)],
                    'eps': 1e-4, 'eps_envelope': 1e-4} for a in range(3, 182)]})
    P.spec_base = {'galaxy': 'DDO154', 'label': GW_C3T_LABEL, 'coefficients': identity['coefficients'], 'physical': identity['physical'],
                   'numerics': copy.deepcopy(identity['numerics'])}
    P.spec_base['numerics']['uv_tail'].update(eps_certificate=P.eps_slot, lo_certificate=P.rho_slot)
    P.eps_proof = wjson(base / 'EPS_PROOF.json', {
        'schema': PROOF, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': P.point,
        'custody_sha256': digest(CUSTODY), 'producer': eps_prod, 'driver_certificate': P.eps_slot,
        'envelope_rule': 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS',
        'shells': [{'range_inverse_kpc': [float(a), float(a + 1)], 'refinement_failures': 0, 'eps': 1e-4, 'eps_envelope': 1e-4}
                   for a in range(3, 182)]})
    P.gq_proof = wjson(base / 'GQ_PROOF.json', {
        'schema': PROOF, 'gate': 'GQ', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': P.point,
        'custody_sha256': digest(CUSTODY), 'producer': gq_prod, 'method': 'GEOMETRY_UNIFORM_COLUMN_BOUND',
        'all_columns_included': True, 'all_production_kperp_nodes': True, 'nonnegative_masses_required': True,
        'M_s': 128, 'M_s_doubled': 256, 'K_big_inverse_kpc': 128.0,
        'max_column_difference_over_analytic_Pi0': B_GQ, 'max_zero_mode_relative_error': Z_GQ})
    res = G1M._prove(P.spec_base, P.rho_slot, registered_rho_records=[P.rho_slot] + ANCHOR_PAIR, anchor_rho_pair=ANCHOR_PAIR,
                     root_ruling_refs=RULINGS, approved_producer_sha256=[GW_PIN['G1']['sha256']], env=g1_env(P.details))
    P.slot_result = res
    if res.get('verdict') == 'READY_FOR_MANIFEST':
        (base / 'slot_proof').mkdir()
        P.slot_proof = G1M.write_proof(res, str((base / 'slot_proof').resolve()))
    else:
        P.slot_proof = None
        return P
    P.prelaunch_doc = {'schema': 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001', 'identity': identity, 'custody': CUSTODY,
                       'domain': {'K_inverse_kpc': 3.0, 'K_big_inverse_kpc': 128.0},
                       'prelaunch': {'EPS': P.eps_proof, 'GQ': P.gq_proof, 'LO_RHO_SLOT': P.slot_proof},
                       'driver_certificate_bindings': {'eps_certificate': P.eps_slot, 'lo_certificate': P.rho_slot},
                       'acceptance_rule': 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED'}
    P.prelaunch = wjson(base / 'PRELAUNCH_BUNDLE.json', P.prelaunch_doc)
    record = {'schema': 'UNT_UV_TAIL_STATE_C2V001', 'stage_kind': 'le_rotation', 'roster_digest': h('source:LR'),
              'eps_certificate': P.eps_slot, 'lo_certificate': P.rho_slot, 'c_m_s': 299792458.0, 'empty': False,
              'synthetic_fixture': True}
    b = np.zeros((179, 3))
    b[:, 1] = [1e-30 / (1.0 + k) for k in range(179)]
    P.LR_TS = LIB.TailState(empty=False, record=record, arrays={'shell_edges_inverse_kpc': np.arange(3.0, 183.0), 'shell_integrals': b})
    P.SD = dict(SD_BASE, LR=P.LR_TS.digest)
    return P


PC3 = make_point_c3t('POINT_S1_UA_C3T', IDENTITY_C3T)
for _n, _d in PC3.SD.items():
    SRC[_d] = h('source:' + _n)
    NAME_OF[_d] = _n
LR_BY_DIGEST[PC3.SD['LR']] = PC3.LR_TS


def stub_produce_current_lo_c3t(spec, state_ref, *, expected_state=None, trusted_source_producers=(), trusted_review_hashes=(),
                                settings='registered', shell_ranges=None, context=None, progress=None):
    """The K=3 twin of stub_produce_current_lo: the KS6 lo_core's (2cf7c597) aggregate_shares on unit edges from 3, and
    the KS6 lo_core / KS2 producer pins the KS6' adapter requires for S1_UA_C3T."""
    d = CUR['details']
    CORE_CALLS.append({'state': expected_state, 'settings': settings, 'shell_ranges': shell_ranges, 'context': context,
                       'trusted': list(trusted_source_producers)})
    sin = CU.read_pin(state_ref)
    if sin.get('schema') != 'UNT_POINT_LO_STATE_INPUT_CX2V001' or sin.get('identity') != d['identity'] or sin.get('custody') != d['custody']:
        raise ValueError('reference schema / point mismatch')
    state, blockers = sin['state'], []
    if expected_state is None or state != expected_state:
        raise ValueError('consumed state differs from independently enumerated state')
    CU.read_pin(sin['tail_state']['record'])
    CU.read_pin(sin['tail_state']['arrays'], document=False)
    row = CU.read_pin(sin['row_reference'])
    ids, R, tau, speed = LOCORE6.row_values(row, {'details': d})
    if (row.get('producer') or {}).get('sha256') not in trusted_source_producers:
        blockers.append('ROW_RECONSTRUCTION_PRODUCER_NOT_APPROVED')
    rv = row.get('policy_review')
    if not rv or rv.get('sha256') not in trusted_review_hashes:
        blockers.append('ROW_REFERENCE_POLICY_NOT_REVIEWED')
    src = CU.read_pin(sin['source_reconstruction'])
    if src.get('state') != state or src.get('tail_state') != sin['tail_state']:
        raise ValueError('source reconstruction state/custody mismatch')
    for f in src.get('source_files') or []:
        CU.read_pin(f, document=False)
    if (src.get('producer') or {}).get('sha256') not in trusted_source_producers:
        blockers.append('SOURCE_RECONSTRUCTION_PRODUCER_NOT_APPROVED')
    rho = copy.deepcopy(CU.read_pin(spec['numerics']['uv_tail']['lo_certificate']))
    rho.update(utc='acceptance-time', seconds=99.0)
    b1 = np.full(179, B1_UNIT)
    shares = LOCORE6.aggregate_shares(rho, np.arange(3.0, 183.0), b1, R, tau, np.abs(speed))
    if not shares['all_nonzero_B1_consumed']:
        blockers.append('LO_SHELL_COVERAGE_INCOMPLETE')
    if not shares['numerical_thresholds_pass']:
        blockers.append('LO_NUMERICAL_INDICATOR_ABOVE_THRESHOLD')
    rec = dict(schema='UNT_POINT_LO_NUMERICAL_CX2V001', gate='LO', kind='CURRENT_SAVED_STATE', utc='acceptance-time',
               status='TESTED', producer=dict(LOCORE6_PIN), response_producer=dict(KS2_PIN), identity=d['identity'],
               point_sha256=d['point_sha256'], custody=d['custody'], production_admissible=False,
               cover_all_consumed_states=False, covers_all_consumed_states=False, rigorous_supremum=False,
               driver_certificate=None, limitations=['synthetic test double of the KS6 lo_core produce_current_lo (K=3)'])
    rec.update(state=state, state_input=state_ref, state_digest_verified=state['state_sha256'], rho=rho, row_ids=ids,
               v_reference_km_s=np.abs(speed).tolist(), **shares, blockers=blockers,
               verdict='BLOCKED' if blockers else 'CURRENT_LO_NUMERICAL_EVIDENCE_REVIEW_REQUIRED', synthetic_test_double=True)
    return rec


REAL_LO6_ENV = LOAD6._real_env
REAL_G2_ENV = G2M._real_env


def lo_env6():
    e = REAL_LO6_ENV()
    e.derive_details = lambda spec: copy.deepcopy(CUR['details'])
    e.point_context = lambda spec: {'synthetic_point_context': CUR['details']['point_sha256']}
    e.produce_current_lo = stub_produce_current_lo_c3t
    e.validate_config = stub_validate
    return e


def g2_env():
    e = REAL_G2_ENV()
    e.derive_details = lambda spec: copy.deepcopy(CUR['details'])
    return e


LOAD6._real_env = lo_env6
G2M._real_env = g2_env
G6CM.D.consumed_states = lambda **kw: copy.deepcopy(CUR['discovery'])
G6CM.X.validate_graph = lambda **kw: {'ok': True, 'blockers': [], 'controls': [CUR['control']]}
G6CM.C.derive_details = lambda **kw: {'point_sha256': CUR['details']['point_sha256'], 'custody_sha256': CUR['details']['custody_sha256'],
                                      'modules': {}, 'row_contract': {'prereg': prereg}}
G6CM.A.compute_i1t = stub_compute
G6CM.A.verify_product = lambda r, p: p.v
G6CM.A.verify_point = lambda spec, r, p, details: None
G6CM.A.verify_occurrence = stub_occurrence


def srb_adapter_g2(spec, *, call_dir, result, inventory, bundle_ref, state_input_ref, rows_input_ref, root_ruling_refs,
                   approved_producer_sha256, trusted_source_producers):
    out = G2M.adapt_call_srb_rot(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
                                 state_input_ref=state_input_ref, rows_input_ref=rows_input_ref, root_ruling_refs=root_ruling_refs,
                                 approved_producer_sha256=approved_producer_sha256, trusted_source_producers=trusted_source_producers)
    SRB_SEEN['out'] = out
    return out


def stub_export_c3t(spec, recon, packet, occurrence, tail, *, uniform_gq_ref, review_ref, approved_review_sha256,
                    approved_producer_sha256, approved_uniform_producer_sha256):
    """stub_export with the G6b evidence pin (export_lo_source of an S1_UA_C3T state) and the b1 GQ_SIGNED form."""
    if review_ref is None or review_ref['sha256'] not in approved_review_sha256:
        raise ValueError('PACKET_BINDING_REVIEW_UNAVAILABLE')
    if G6B_PIN['sha256'] not in approved_producer_sha256:
        raise ValueError('CURRENT_SOURCE_PRODUCER_NOT_APPROVED')
    assert uniform_gq_ref == CUR['P'].gq_proof
    _, p, i1t = stub_compute(recon, packet)
    state = p.v['state']
    readpin(tail['record'])
    if hashlib.sha256(Path(tail['arrays']['path']).read_bytes()).hexdigest() != tail['arrays']['sha256']:
        raise ValueError('TAIL_ARRAYS_PIN')
    if state['nonnegative_masses']:
        gq = {'schema': PROOF, 'gate': 'GQ_CURRENT_PREMISES', 'status': 'TESTED', 'verdict': 'PASS', 'state': state, 'producer': G6B_PIN}
    else:
        gq = dict(gq_signed(state, b1=True), producer=G6B_PIN)
    d = CUR['details']
    return {'schema': 'UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001', 'status': 'TESTED', 'verdict': 'PASS', 'producer': G6B_PIN,
            'identity': d['identity'], 'custody': d['custody'], 'state': state, 'tail_state': tail, 'i1t_verdict': 'PASS',
            'current_gq': gq, 'source_files': i1t['source_files'], 'complete_source_files': True, 'synthetic': True}


EVSTUB_C3T = SimpleNamespace(R=EVSTUB.R, export_lo_source=stub_export_c3t)


def deps_c3t(enumerator=None, guard=None, lo_adapter=None, lo_pin=None, srb=None):
    return {'enumerator': enumerator or G6CM, 'writer': WRITER, 'row_producer': ROWP, 'guard': guard or KS5G, 'evidence': EVSTUB_C3T,
            'lo_core': LOSTUB, 'lo_adapter': lo_adapter or LOAD6.adapt_call_lo, 'srb_adapter': srb or srb_adapter_g2,
            'pins': {'lo_adapter': dict(lo_pin or HAND.LO_ADAPTER_KS6), 'srb_adapter': dict(GW_PIN['G2'], entry='adapt_call_srb_rot')}}


def policy_c3t(c, **over):
    p = policy(c, approved_certificate_producers=[eps_prod, gq_prod, G6B_PIN, KS6PP_PIN, dict(GW_PIN['G2']), dict(GW_PIN['G1'])],
               trusted_source_producers=[G6B_PIN['sha256'], ROWP_SHA], approved_evidence_producer_sha256=[G6B_PIN['sha256']],
               evidence_producer=G6B_PIN)
    p.update(over)
    return p


def accept_c3t(name, variant=(), dps=None, pol_over=None, point=None):
    c = make_call(name, variant, point or PC3)
    prepare(c, None, {'b1': True}, None)
    r, g = derived(c)
    out = HAND.accept_call(call_dir=c.call, spec=c.spec, deps=dps or deps_c3t(), policy=policy_c3t(c, **(pol_over or {})),
                           records_dir=RUN / 'records' / name, initial_rings_ref=r, final_next_gas_ref=g)
    PAIRS.append(reading_pair(name, out[0]))
    return c, out


def gw_tests():
    check('GW00_S1_UA_C3T_point_fixture_real_G1_slot_proof_ready', 'MUST_PASS',
          PC3.slot_proof is not None and readpin(PC3.slot_proof)['producer'] == GW_PIN['G1'] and
          [s['range_inverse_kpc'] for s in readpin(PC3.rho_slot)['shells']] == RHO_SHELLS_C3T and
          HAND._s1_c3t_spec(PC3.spec_base) and not HAND._s1_c3t_spec(PT.spec_base),
          json.dumps(PC3.slot_result.get('blockers')))
    c, (r, _) = accept_c3t('GW01_S1_UA_C3T_HONEST')
    lo = lo_call_of(r)
    inv = G6CM.consumed_states(spec=c.spec, result=c.result, call_dir=str(c.call))
    srb_rec = readpin(r['srb_rot']['record']) if (r.get('srb_rot') or {}).get('record') else {}
    proofs = [readpin(e['LO']) if e.get('LO') else {} for e in r['states']]
    check('GW01_S1_UA_C3T_call_ACCEPTED_end_to_end_KS6pp_G2_G6c_G1_KS5', 'MUST_PASS',
          r['reading'] == 'ACCEPTED' and (r['guard'] or {}).get('ok') is True and r['outputs_are_evidence'] is True and not r['blockers']
          and len(r['states']) == 8 and all(e['reading'] == 'PASS' for e in r['states']) and r['lo_adapter']['pin'] == HAND.LO_ADAPTER_KS6
          and lo.get('call_lo_reading') == 'PASS' and lo.get('producer') == KS6PP_PIN and inv['producer'] == GW_PIN['G6C']
          and r['srb_rot']['reading'] == 'PASS' and srb_rec.get('producer') == GW_PIN['G2']
          and all(p.get('shells', [{}])[0].get('range_inverse_kpc') == [3.0, 4.0] for p in proofs)
          and r['handoff'] == ref(ITEM / 'acceptance_handoff_c2v004_ks6_c2v002.py'),
          json.dumps({k: r.get(k) for k in ('reading', 'blockers', 'guard', 'srb_rot')}, default=str)[:700])
    _, (r, _) = accept_c3t('GW02_C3T_WITH_THE_B1_ENUMERATOR_4CA7F364', dps=deps_c3t(enumerator=ENUM))
    lo = lo_call_of(r)
    check('GW02_S1_UA_C3T_with_the_4ca7f364_inventory_refused_INCOMPLETE', 'MUST_FAIL',
          r['reading'] == 'INCOMPLETE' and 'INVENTORY_PRODUCER_NOT_THE_G6_ENUMERATOR' in json.dumps(lo.get('blockers'))
          and r['outputs_are_evidence'] is False, json.dumps({'lo': lo.get('blockers'), 'srb': r.get('srb_rot')}, default=str)[:600])
    _, (r, _) = accept_c3t('GW03_C3T_TRUSTED_LIST_7044E131_NOT_G6B', pol_over={'trusted_source_producers': [B1_EV['sha256'], ROWP_SHA]})
    check('GW03_S1_UA_C3T_trusted_list_without_the_G6b_evidence_INCOMPLETE', 'MUST_FAIL',
          r['reading'] == 'INCOMPLETE' and HAND.B1_UNTRUSTED_BLOCKER_G6 in r['blockers'] and r['outputs_are_evidence'] is False,
          json.dumps(r['blockers'])[:400])
    _, (r, _) = accept_c3t('GW04_C3T_WITH_THE_08E9AC0A_SRB_ADAPTER', dps=deps_c3t(srb=srb_adapter),
                           pol_over={'approved_certificate_producers': [eps_prod, gq_prod, G6B_PIN, KS6PP_PIN, dict(GW_PIN['G2']),
                                                                        dict(GW_PIN['G1']), srb_ad_ref]})
    check('GW04_S1_UA_C3T_with_the_08e9ac0a_SRB_adapter_UNAVAILABLE_INCOMPLETE', 'MUST_FAIL',
          r['reading'] == 'INCOMPLETE' and (r.get('srb_rot') or {}).get('reading') == 'UNAVAILABLE'
          and 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in json.dumps(SRB_SEEN.get('out', {}).get('blockers')),
          json.dumps({'srb': r.get('srb_rot'), 'srb_out': SRB_SEEN.get('out', {}).get('blockers')}, default=str)[:500])
    _, (r1, _) = accept_c3t('GW05_C3T_WITH_THE_211A3220_ADAPTER', dps=deps_c3t(lo_adapter=LOAD.adapt_call_lo, lo_pin=LO_PIN))
    w1 = {'path': str(GW_KS / 'lo_state_proof_adapter_c3v003_ks6_c2v001.py'), 'sha256': '8fa371a719b41c174175942308ca64bebe40fb1e0d42b99ae27def939cbe6c33',
          'entry': 'adapt_call_lo'}
    w1m = HAND.load_pinned(w1, 'q2gw_ks6_wave1_adapter')
    _, (r2, _) = accept_c3t('GW05b_C3T_WITH_THE_WAVE1_KS6_ADAPTER', dps=deps_c3t(lo_adapter=w1m.adapt_call_lo, lo_pin=w1))
    check('GW05_S1_UA_C3T_with_the_211a3220_or_wave1_KS6_LO_adapter_refused_before_anything_is_read', 'MUST_FAIL',
          r1['reading'] == r2['reading'] == 'INCOMPLETE' and 'LO_ADAPTER_PIN_NOT_A138' in json.dumps(r1['blockers'])
          and 'LO_ADAPTER_PIN_NOT_A138' in json.dumps(r2['blockers']) and not r1['states'] and not r2['states'],
          json.dumps([r1['blockers'], r2['blockers']])[:500])
    _, (r, _) = accept_c3t('GW06_C3T_WITH_THE_B1_GUARD', dps=deps_c3t(guard=GUARD_B1))
    check('GW06_S1_UA_C3T_acceptance_with_guard_b1_9e3fc109_refused_domain_K3', 'MUST_FAIL',
          r['reading'] == 'INCOMPLETE' and (r['guard'] or {}).get('ok') is False
          and 'unsupported calibration domain' in json.dumps((r['guard'] or {}).get('blockers')),
          json.dumps(r.get('guard'))[:300])
    k4slot = make_point_c3t('POINT_S1_UA_C3T_K4_SLOT', IDENTITY_C3T, slot_rho=rho_record_c3t(IDENTITY_C3T, 'slot-time', 12.5, shells=RHO_SHELLS, cov=[4.0, 182.0]))
    a1slot = make_point_c3t('POINT_S1_UA_C3T_A1_SLOT', IDENTITY_C3T, slot_rho=rho_record_c3t(IDENTITY_C3T, 'slot-time', 12.5, producer=RESPONSE))
    check('GW07_S1_UA_C3T_K4_or_a1dcdea8_rho_slot_never_gets_a_G1_slot_proof', 'MUST_FAIL',
          k4slot.slot_proof is None and 'RHO_COVERAGE_NOT_3_TO_182' in json.dumps(k4slot.slot_result['blockers'])
          and a1slot.slot_proof is None and 'RHO_PRODUCER_NOT_RESPONSE_KS2' in json.dumps(a1slot.slot_result['blockers']),
          json.dumps([k4slot.slot_result['blockers'], a1slot.slot_result['blockers']])[:500])


safe('GW_S1_suite', gw_tests)
'''


def suites(tgt):
    S = {}
    # ------------------------------------------------------------------ the wave-1 KS suite -> KS3', KS4', KS5'', KS6'
    S['ks'] = (KS + '/test_ks_k3_chain_c2v001.py', '171f4ec2d4bb3a6cc3d9c3aa494d97a31d470d016729e1bfdf78939ce45688ac',
               'test_ks_k3_chain_c2v001_PORT_gwave_c2v001.py', [
        ('"""KS1-KS6 synthetic tests (ks_k3_chain_c2 c2v001; root A160): MUST_PASS, MUST_FAIL, DIFFERENTIAL and FINDING cases.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the wave-1 KS suite run against KS3\', KS4\', KS5\'\' and KS6\' (KS1, KS2, KS5 and the\n'
         'KS6 lo_core/lo_config are unchanged). Adaptations are marked PORT (G-wave) and listed in README_KS_K3_GWAVE_C2V001.md.\n\n'
         'KS1-KS6 synthetic tests (ks_k3_chain_c2 c2v001; root A160): MUST_PASS, MUST_FAIL, DIFFERENTIAL and FINDING cases.\n', 1),
        ("""NAMES = {
    'KS1': 'custody_cx2v002_ks1_c2v001.py', 'KS2': 'point_response_producer_cx2v002_ks2_c2v001.py',
    'KS5': 'certificate_guard_b1_ks5_c2v001.py', 'KS5P': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py',
    'KS3C': 's4rc1_common_c3v004_ks3_c2v001.py', 'KS3R': 'cp1_runner_c3v004_ks3_c2v001.py',
    'KS4': 'registry_assembler_c3v004_ks4_c2v001.py', 'KS6CORE': 'lo_core_r5_cx2v001_ks6_c2v001.py',
    'KS6CFG': 'lo_config_r5_cx2v001_ks6_c2v001.py', 'KS6AD': 'lo_state_proof_adapter_c3v003_ks6_c2v001.py',
    'KS6HO': 'acceptance_handoff_c2v004_ks6_c2v001.py'}
""", """NAMES = {   # PORT (G-wave): KS5P, KS3C, KS3R, KS4, KS6AD and KS6HO are their G-wave successors (in --gw-dir)
    'KS1': 'custody_cx2v002_ks1_c2v001.py', 'KS2': 'point_response_producer_cx2v002_ks2_c2v001.py',
    'KS5': 'certificate_guard_b1_ks5_c2v001.py', 'KS5P': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py',
    'KS3C': 's4rc1_common_c3v004_ks3_c2v002.py', 'KS3R': 'cp1_runner_c3v004_ks3_c2v002.py',
    'KS4': 'registry_assembler_c3v004_ks4_c2v002.py', 'KS6CORE': 'lo_core_r5_cx2v001_ks6_c2v001.py',
    'KS6CFG': 'lo_config_r5_cx2v001_ks6_c2v001.py', 'KS6AD': 'lo_state_proof_adapter_c3v003_ks6_c2v002.py',
    'KS6HO': 'acceptance_handoff_c2v004_ks6_c2v002.py'}
GW_KEYS = ('KS5P', 'KS3C', 'KS3R', 'KS4', 'KS6AD', 'KS6HO')   # PORT (G-wave)
""", 1),
        ("""    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    KS = os.path.realpath(a.ks_dir)
    run = os.path.abspath(a.run_dir)
    if not run.startswith(KS + '/synthetic/'):
""", """    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--gw-dir')                                    # PORT (G-wave): the G-wave successors' folder
    a = ap.parse_args()
    KS = os.path.realpath(a.ks_dir)
    GWD = os.path.realpath(a.gw_dir or a.ks_dir)
    run = os.path.abspath(a.run_dir)
    if not run.startswith((KS + '/synthetic/', KS + '/dev/')):
""", 1),
        ("    M = {k: load(os.path.join(KS, n), 'kst_' + k.lower()) for k, n in NAMES.items()}\n",
         "    M = {k: load(os.path.join(GWD if k in GW_KEYS else KS, n), 'kst_' + k.lower()) for k, n in NAMES.items()}   # PORT (G-wave)\n", 1),
        ("    KSPIN = {k: {'path': os.path.join(KS, n), 'sha256': sha_file(os.path.join(KS, n))} for k, n in NAMES.items()}\n",
         "    KSPIN = {k: {'path': os.path.join(GWD if k in GW_KEYS else KS, n), 'sha256': sha_file(os.path.join(GWD if k in GW_KEYS else KS, n))}\n"
         "             for k, n in NAMES.items()}   # PORT (G-wave)\n", 1),
        ("            'KS3C.wrapper_s1k3_ks5p': list(C.PINS['wrapper_s1k3_ks5p']) == [KSPIN['KS5P']['path'], KSPIN['KS5P']['sha256']],\n",
         "            'KS3C.wrapper_s1k3_ks5pp': list(C.PINS['wrapper_s1k3_ks5pp']) == [KSPIN['KS5P']['path'], KSPIN['KS5P']['sha256']],   # PORT (G-wave): KS5''\n", 1),
        ("                'custody_sha256': digest(CUST), 'producer': producer or C.canonical_pin('gq_producer'),\n",
         "                'custody_sha256': digest(CUST), 'producer': producer or C.canonical_pin('gq_producer_g3' if C.s1_c3t_spec(spec) else 'gq_producer'),   # PORT (G-wave): row 32's GQ producer is G3\n", 1),
        ("""        ok = (g1['ok'] is False and 'is not the kept K 3.0' in str(g1['blockers'])
              and g2['ok'] is False and 'binding mismatch: guard_sha256' in str(g2['blockers'])
              and g3['ok'] is True)
        return ok, {'k4_bundle': g1['blockers'], 'b1_bound_c1': g2['blockers'],
                    'note_k4_rho_slot': 'the wrapper reads no partition (q5b1 L168-172); KS6 check_rho_record and KS4 do'}
""", """        ok = (g1['ok'] is False and 'is not the kept K 3.0' in str(g1['blockers'])
              and g2['ok'] is False and 'binding mismatch: guard_sha256' in str(g2['blockers'])
              and g3['ok'] is False and 'S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT' in str(g3['blockers']))   # PORT (G-wave, A175)
        return ok, {'k4_bundle': g1['blockers'], 'b1_bound_c1': g2['blockers'], 'k4_rho_slot': g3.get('blockers'),
                    'note_k4_rho_slot': 'PORT (G-wave, A175): KS5\\'\\' now checks the slot rho at prelaunch (wave 1 read ok)'}
""", 1),
        ("""    def c1_doc(registry, deriver, guard_sha, tag):
        rv = FX.json(FX.uniq(tag) + '/REVIEW.json', {
            'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': C.DRIVER_SHA,
            'custody_deriver': deriver, 'state_enumerator': C.canonical_pin('state_enumerator'),
""", """    def c1_doc(registry, deriver, guard_sha, tag):
        enum_ = C.canonical_pin('state_enumerator_g6' if guard_sha == KSPIN['KS5']['sha256'] else 'state_enumerator')   # PORT (G-wave): an S1 C1 names G6c
        rv = FX.json(FX.uniq(tag) + '/REVIEW.json', {
            'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': C.DRIVER_SHA,
            'custody_deriver': deriver, 'state_enumerator': enum_,
""", 1),
        ("""            'certificate_registry': registry, 'custody_deriver': deriver, 'state_enumerator': C.canonical_pin('state_enumerator'),
            'certificate_policy_review': rv, 'approved_certificate_producers': APPROVED}})
""", """            'certificate_registry': registry, 'custody_deriver': deriver, 'state_enumerator': enum_,
            'certificate_policy_review': rv, 'approved_certificate_producers': APPROVED}})
""", 1),
        ("""               'producer': {'path': ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', 'sha256': AD6.ENUMERATOR_SHA},
""", """               'producer': ({'path': AD6.ENUMERATOR_G6[0], 'sha256': AD6.ENUMERATOR_G6[1]} if C.s1_c3t_spec(spec0) else   # PORT (G-wave): S1 -> G6c
                            {'path': ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', 'sha256': AD6.ENUMERATOR_SHA}),
""", 1),
        ("    with open(os.path.join(run, 'TEST_RESULTS_KS_C2V001.json'), 'xb') as f:\n",
         "    with open(os.path.join(run, 'TEST_RESULTS_KS_PORT_GWAVE_C2V001.json'), 'xb') as f:   # PORT (G-wave)\n", 1),
    ])
    # ------------------------------------------------------------------ CP-1 suite (wave-1 port) -> KS3', KS4'
    S['cp1'] = (KS + '/test_s4rc1_c3v004_PORT_ks3_ks4_c2v001.py', '5b116472eaa0eced696d91c33565b6d4f4c31afbedc346515999ae7e5dfe1462',
                'test_s4rc1_c3v004_PORT_gwave_c2v001.py', [
        ('"""S4-R-C1 c3v004 synthetic test suite (Claude3 builder; A122, A134, A138; distinct-lane review under A115).\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the c3v004 suite (wave-1 port) against KS3\' and KS4\' (runner/assembler c2v002).\n\n'
         'S4-R-C1 c3v004 synthetic test suite (Claude3 builder; A122, A134, A138; distinct-lane review under A115).\n', 1),
        ("cp1_runner_c3v004_ks3_c2v001.py", "cp1_runner_c3v004_ks3_c2v002.py", 8),
        ("registry_assembler_c3v004_ks4_c2v001.py", "registry_assembler_c3v004_ks4_c2v002.py", 1)])
    # ------------------------------------------------------------------ proof-side suite (wave-1 port) -> G1, G2, KS6'
    S['proofside'] = (KS + '/test_proof_side_c3v003_PORT_ks6_c2v001.py', '272082829ed9f3a325dc6476161e3ff189b4eab52b813d9bb9573a694ad3d28a',
                      'test_proof_side_c3v003_PORT_gwave_c2v001.py', [
        ('"""S4-R-C1 proof side c3v003: synthetic MUST_PASS / MUST_FAIL suite (Claude3 builder; A134, FROM_CODEX/0688, 0696; A138 0703;\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the proof-side c3v003 suite against G1 (slot proof), G2 (SRB-ROT) and KS6\'.\n\n'
         'S4-R-C1 proof side c3v003: synthetic MUST_PASS / MUST_FAIL suite (Claude3 builder; A134, FROM_CODEX/0688, 0696; A138 0703;\n', 1),
        ("""        self.paths = {'slot': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py', 'state': b + '/lo_state_proof_adapter_c3v003_ks6_c2v001.py',
                      'srb': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py'}   # PORT (ks_k3_chain_c2): the state adapter is KS6
""", """        self.paths = {'slot': b + '/lo_slot_proof_c3v003_g1_c2v001.py', 'state': b + '/lo_state_proof_adapter_c3v003_ks6_c2v002.py',
                      'srb': b + '/srb_rot_adapter_c3v003_g2_c2v001.py'}   # PORT (G-wave): G1, KS6', G2
""", 1)])
    # ------------------------------------------------------------------ acceptance q2 (wave-1 port) -> KS6' handoff
    S['q2'] = (KS + '/tests/test_acceptance_q2_c2v004_PORT_ks6_c2v001.py', '5d7ba399fa45de9dc93185e2b5010ca0eaaf61419c4e131397294ad5a8151186',
               'tests_gwave/test_acceptance_q2_c2v004_PORT_gwave_c2v001.py', [
        ('"""Synthetic MUST_PASS / MUST_FAIL tests for acceptance_q2 v004 (A145). Run: python3 -I -B <this file>.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the acceptance q2 v004 suite against the KS6\' handoff (c2v002).\n\n'
         'Synthetic MUST_PASS / MUST_FAIL tests for acceptance_q2 v004 (A145). Run: python3 -I -B <this file>.\n', 1),
        ("acceptance_handoff_c2v004_ks6_c2v001.py", "acceptance_handoff_c2v004_ks6_c2v002.py", 3),
        ("RUN = ITEM / 'tests' / (", "RUN = ITEM / 'tests_gwave' / (", 1),
        ("safe('L_suite', l_tests)\n", "safe('L_suite', l_tests)\n" + Q2_GWAVE_APPENDIX, 1)])
    # ------------------------------------------------------------------ s1k3 wrapper suite (wave-1 port) -> KS5''
    lo_k3 = ("{'schema': 'SYNTHETIC_LO', 'coverage_complete': True, 'required_coverage_inverse_kpc': [3.0, 182.0], "
             "'shells': [{'range_inverse_kpc': p} for p in [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], "
             "[16.0, 32.0], [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]], 'producer': {'path': '%s/point_response_producer_cx2v002_ks2_c2v001.py', "
             "'sha256': '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'}}" % KS)
    S['wrapper'] = (KS + '/test_wrapper_s1k3_c2v001_PORT_ks5p_c2v002.py', '9fc131d1c3f418f8b794ddad757347b95afb2225431cbf4c640c8b54122a754f',
                    'test_wrapper_s1k3_c2v001_PORT_gwave_c2v003.py', [
        ('"""Synthetic MUST_PASS / MUST_FAIL tests for the S1-only kept-K-3 wrapper successor\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the s1k3 wrapper suite (wave-1 port) against KS5\'\' (wrapper c2v003).\n\n'
         'Synthetic MUST_PASS / MUST_FAIL tests for the S1-only kept-K-3 wrapper successor\n', 1),
        ("SUCC_PATH = str(HERE / 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py')   # PORT: KS5'\n",
         "SUCC_PATH = str(HERE / 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py')   # PORT (G-wave): KS5''\n", 1),
        ("    srcs[str(HERE / 'certificate_guard_b1_ks5_c2v001.py')] = sha(rb(str(HERE / 'certificate_guard_b1_ks5_c2v001.py')))   # PORT: KS5' loads KS5\n",
         "    srcs['%s/certificate_guard_b1_ks5_c2v001.py'] = sha(rb('%s/certificate_guard_b1_ks5_c2v001.py'))   # PORT: KS5'' loads KS5 (wave-1 folder)\n" % (KS, KS), 1),
        ("m.MODULE_NAME.endswith('s1k3_c2v002')", "m.MODULE_NAME.endswith('s1k3_c2v003')", 1),
        ("        FX['lo'] = wj(RUN / 'cert_lo_syn.json', {'schema': 'SYNTHETIC_LO'})\n",
         "        FX['lo'] = wj(RUN / 'cert_lo_syn.json', %s)   # PORT (G-wave, A175): KS5'' reads the S1 slot rho's K=3 contract\n" % lo_k3, 1)])
    # ------------------------------------------------------------------ offset_b1 suites -> G3c, G6b, G6c
    succ = {k: (os.path.join(tgt, GW_FILES[k]), sha_file(os.path.join(tgt, GW_FILES[k]))) for k in ('G3C', 'G6B', 'G6C')}
    S['b1common'] = (B1T + '/b1_common_c2v001.py', '8b407c95c615c987acb78aee8dec1b300ff5bfabe4f566eb4d0707c07bc1c9bd',
                     'tests_b1_gwave/b1_common_c2v001_PORT_gwave_c2v001.py', [
        ('"""Shared helpers for the A134 (b1) synthetic tests. No producer is run on real inputs."""\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): offset_b1 test helpers with the G-wave successors under test (G3c, G6b, G6c).\n\n'
         'Shared helpers for the A134 (b1) synthetic tests. No producer is run on real inputs."""\n', 1),
        ("""    'gq': (B1 / 'gq_producer_b1_c2v001.py', '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5'),
    'evidence': (B1 / 'current_source_evidence_b1_c2v001.py', '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
    'enumerator': (B1 / 'consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),
""", """    'gq': (Path(%r), %r),   # PORT (G-wave): G3c
    'evidence': (Path(%r), %r),   # PORT (G-wave): G6b
    'enumerator': (Path(%r), %r),   # PORT (G-wave): G6c
""" % (succ['G3C'] + succ['G6B'] + succ['G6C']), 1),
        ("    if not d.parent.is_relative_to(B1 / 'tests')", "    if not d.parent.is_relative_to(Path(__file__).resolve().parent)", 1),
        ("""def runtime():
""", """# PORT (G-wave): the b1 module each successor delegates every other spec to, the S1_UA_C3T fixture, and the static check
# that replaces each suite's b1-vs-v0xx diff-scope check: the successor is its predecessor plus exactly the listed edits.
B1MOD = {
    'gq': (B1 / 'gq_producer_b1_c2v001.py', '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5'),
    'evidence': (B1 / 'current_source_evidence_b1_c2v001.py', '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
    'enumerator': (B1 / 'consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),
}
GW_DIR = Path(__file__).resolve().parent.parent
GW_KEY = {'gq': 'G3C', 'evidence': 'G6B', 'enumerator': 'G6C'}
S1_LABEL = %r
CB_PIN = %s


def cb_c3t_grid():
    raw = Path(CB_PIN['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
        raise SystemExit('CB pin mismatch')
    return json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']


def rerender_equal(which):
    \"\"\"The successor's bytes are exactly the G-wave build's render of its predecessor (every edit exact-once, listed).\"\"\"
    bp = GW_DIR / 'build_gwave_c2v001.py'
    B = load_pinned(bp, hashlib.sha256(bp.read_bytes()).hexdigest(), 'b1t_gwave_build')
    shas = {k: v for k, (n, v) in B.WAVE1.items()}
    for k in B.ORDER:
        p = GW_DIR / B.NAME[k]
        if p.exists():
            shas[k] = hashlib.sha256(p.read_bytes()).hexdigest()
    _old, new = B.render(GW_KEY[which], shas, str(GW_DIR))
    return new == Path(SUCC[which][0]).read_text(), sorted(B.EDITS[GW_KEY[which]][i][0].splitlines()[0][:60] for i in range(len(B.EDITS[GW_KEY[which]])))


def runtime():
""" % (C3T_LABEL, CB_PIN_CODE), 1)])
    S['b1gq'] = (B1T + '/test_gq_b1_c2v001.py', '37bc9c1bdad7c596a01b172b8ca748513b648505cd6a359cb9db99e39db183bc',
                 'tests_b1_gwave/test_gq_b1_c2v001_PORT_gwave_c2v001.py', [
        ('"""A134 (b1) signed_bound successor: synthetic MUST_PASS / MUST_FAIL tests.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the b1 GQ suite against G3c (gq_producer_b1 successor); static checks adapted.\n\n'
         'A134 (b1) signed_bound successor: synthetic MUST_PASS / MUST_FAIL tests.\n', 1),
        ("sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/tests')\n",
         "sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.realpath(__file__)))   # PORT (G-wave)\n", 1),
        ("import b1_common_c2v001 as T\n", "import b1_common_c2v001_PORT_gwave_c2v001 as T   # PORT (G-wave)\n", 1),
        ("""ck('MP09_produce_function_AST_identical', fn_ast(T.PRED['gq'][0], 'produce') == fn_ast(T.SUCC['gq'][0], 'produce'), 'MUST_PASS')
ck('MP10_same_pinned_geometry_kernel', T.sha_file(new.P) == new.S == old.S and T.sha_file(old.P) == old.S, 'MUST_PASS', new.S)
""", """def fn_ast_without_s1_gate(path, name):   # PORT (G-wave): G3c's produce is 3e668a2b's (= v005's) plus the S1_UA_C3T gate
    tree = ast.parse(open(path).read())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    gate = fn.body[0]
    assert isinstance(gate, ast.If) and ast.unparse(gate.test) == 'not C.s1_c3t_spec(spec)', 'S1 gate missing'
    fn.body = fn.body[1:]
    return ast.dump(fn, include_attributes=False)


ck('MP09_produce_function_AST_identical', fn_ast(T.PRED['gq'][0], 'produce') == fn_ast_without_s1_gate(T.SUCC['gq'][0], 'produce'), 'MUST_PASS')
ck('MP10_same_pinned_geometry_kernel', T.sha_file(new.P) == new.S and new.P.name == 'gq_geometry_r5_cx2v001_g3_c2v001.py'
   and new.PRED.S == old.S and T.sha_file(new.PRED.P) == old.S and T.sha_file(old.P) == old.S, 'MUST_PASS', new.S)   # PORT (G-wave): G3 kernel
""", 1),
        ("""tree = ast.parse(old_text)
allowed = set(range(1, 7))
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in ('policy', 'signed_bound'):
        allowed.update(range(n.lineno, n.end_lineno + 1))
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('P', 'RULING') for t in n.targets):
        allowed.update(range(n.lineno, n.end_lineno + 1))
touched = T.changed_lines(old_text, new_text)
ck('MF07_diff_confined_to_docstring_paths_ruling_policy_signed_bound', touched <= allowed and touched, 'MUST_FAIL', sorted(touched - allowed))
""", """same, edits = T.rerender_equal('gq')   # PORT (G-wave): the successor is 3e668a2b plus exactly the listed G3 edits
b1_text = open(T.B1MOD['gq'][0]).read()
ck('MF07_diff_confined_to_docstring_paths_ruling_policy_signed_bound', same and T.changed_lines(b1_text, new_text), 'MUST_FAIL', edits)
""", 1)])
    S['b1evidence'] = (B1T + '/test_evidence_b1_c2v001.py', '95d788a076ca742ff1287793a1327152df5a43c8fe6c23c9d8fafc4064d440ee',
                       'tests_b1_gwave/test_evidence_b1_c2v001_PORT_gwave_c2v001.py', [
        ('"""A134 (b1) current-source evidence successor: synthetic MUST_PASS / MUST_FAIL tests.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the b1 evidence suite against G6b, in two modes (env GW_PORT_MODE):\n'
         '  DELEGATED  the suite\'s own non-S1 synthetic spec: G6b hands it to 7044e131 (seams on that object), so every check\n'
         '             must hold with the b1 module\'s own records (the successor pin of the swap is 7044e131\'s);\n'
         '  S1         the same spec with the S1_UA_C3T label and the CB C3T grid: G6b\'s own code (seams on G6b), so every\n'
         '             check must hold with G6b\'s self-pins. The mutation checks run on G6b\'s text in S1 mode.\n\n'
         'A134 (b1) current-source evidence successor: synthetic MUST_PASS / MUST_FAIL tests.\n', 1),
        ("sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/tests')\n",
         "sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.realpath(__file__)))   # PORT (G-wave)\n", 1),
        ("import b1_common_c2v001 as T\n", "import b1_common_c2v001_PORT_gwave_c2v001 as T   # PORT (G-wave)\nMODE = __import__('os').environ['GW_PORT_MODE']\nassert MODE in ('DELEGATED', 'S1')\n", 1),
        ("PRED_PIN, SUCC_PIN = T.pin_file(T.PRED['evidence'][0]), T.pin_file(T.SUCC['evidence'][0])\n"
         "ck('MP_succ_G_is_b1_gq_and_R_L_unchanged', T.pin_file(ES.G.__file__) == T.pin_file(T.SUCC['gq'][0]) and ES.PINS['R'][1] == EP.PINS['R'][1]\n"
         "   and ES.PINS['L'][1] == EP.PINS['L'][1] and T.sha_file(ES.R.__file__) == EP.PINS['R'][1] and T.sha_file(ES.L.__file__) == EP.PINS['L'][1], 'MUST_PASS')\n",
         "PRED_PIN, SUCC_PIN = T.pin_file(T.PRED['evidence'][0]), T.pin_file(T.SUCC['evidence'][0] if MODE == 'S1' else T.B1MOD['evidence'][0])   # PORT (G-wave)\n"
         "ck('MP_succ_G_is_b1_gq_and_R_L_unchanged', T.pin_file(ES.G.__file__) == T.pin_file(T.SUCC['gq'][0]) and ES.PINS['R'][1] == EP.PINS['R'][1]\n"
         "   and ES.PINS['L'][1] == '510ff07b9557c3829063fe25fe127dc0477a0bfdace5627d84f61aba8b256a2b' and T.sha_file(ES.R.__file__) == EP.PINS['R'][1]\n"
         "   and T.sha_file(ES.L.__file__) == ES.PINS['L'][1] and T.sha_file(ES.PRED.__file__) == T.B1MOD['evidence'][1], 'MUST_PASS')   # PORT (G-wave): L = KS6 lo_config (MAP H1 (a))\n", 1),
        ("SPEC = {'synthetic_spec': True, 'numerics': {'uv_tail': {'quadrature': 'SYNTHETIC_QUADRATURE', 'outer': {'K_big_inverse_kpc': 128.0}}}}\n",
         "SPEC = {'synthetic_spec': True, 'numerics': {'uv_tail': {'quadrature': 'SYNTHETIC_QUADRATURE', 'outer': {'K_big_inverse_kpc': 128.0}}}}\n"
         "if MODE == 'S1':   # PORT (G-wave): the S1_UA_C3T label and the CB C3T grid route assemble_current to G6b's own code\n"
         "    SPEC = dict(SPEC, label=T.S1_LABEL, numerics=dict(SPEC['numerics'], composite_grid_spec=T.cb_c3t_grid()))\n", 1),
        ("for _m in (EP, ES):\n    seam(_m)\n",
         "for _m in (EP, ES) + ((ES.PRED,) if MODE == 'DELEGATED' else ()):   # PORT (G-wave): the delegated object takes the same seams\n    seam(_m)\n", 1),
        ("""@contextlib.contextmanager
def mass_seam(M, mutate):
    orig = M.verify_product
""", """@contextlib.contextmanager
def mass_seam(M, mutate):
    M = M.PRED if (MODE == 'DELEGATED' and M is ES) else M     # PORT (G-wave): in DELEGATED mode the b1 object computes
    orig = M.verify_product
""", 1),
        ("""old_text, new_text = open(T.PRED['evidence'][0]).read(), open(T.SUCC['evidence'][0]).read()
ol = old_text.splitlines()
p0 = next(i for i, x in enumerate(ol, 1) if x.startswith('PINS={'))
p1 = next(i for i, x in enumerate(ol, 1) if x.startswith(" 'G':("))
s0 = next(i for i, x in enumerate(ol, 1) if x.strip() == "if 'body' in v['gas']:")
s1 = next(i for i, x in enumerate(ol, 1) if x.strip().startswith('positive_components_verified=True,signed_offset_policy=G.policy())'))
allowed = set(range(p0, p1 + 1)) | set(range(s0, s1 + 1))
touched = T.changed_lines(old_text, new_text)
ck('MF_diff_confined_to_pins_and_offset_branch', touched and touched <= allowed, 'MUST_FAIL', {'outside': sorted(touched - allowed), 'pins': [p0, p1], 'offset_branch': [s0, s1]})
lits = ('1e-12', 'I1T_SAMPLES=4096', 'I1T_SEED=20261018', 'b/(1-z)')
ck('MF_threshold_literals_unchanged', all(old_text.count(x) == new_text.count(x) for x in lits), 'MUST_FAIL', {x: [old_text.count(x), new_text.count(x)] for x in lits})
""", """old_text, new_text = open(T.B1MOD['evidence'][0]).read(), open(T.SUCC['evidence'][0]).read()   # PORT (G-wave): 7044e131 -> G6b
same, edits = T.rerender_equal('evidence')
ck('MF_diff_confined_to_pins_and_offset_branch', same, 'MUST_FAIL', edits)
lits = ('1e-12', 'I1T_SAMPLES=4096', 'I1T_SEED=20261018', 'b/(1-z)')
ck('MF_threshold_literals_unchanged', all(old_text.count(x) == new_text.count(x) for x in lits), 'MUST_FAIL', {x: [old_text.count(x), new_text.count(x)] for x in lits})
""", 1),
        ("""M1 = mutant('max_difference_over_P0_bound=b/(1-z))', 'max_difference_over_P0_bound=2*b/(1-z))', 'nonneg')
hits = [case for case in NONNEG if not identical(call(EP, case, UQ), call(M1, case, UQ))]
ck('MF_mutation_max_component_applied_to_nonnegative_detected', hits == list(NONNEG), 'MUST_FAIL', hits)
M2 = mutant("            if v['state']['stage_kind']!='offset':raise ValueError('MAX_COMPONENT_NORMALIZATION_OFFSET_STAGES_ONLY')\\n", '', 'scope')
ck('MF_mutation_offset_scope_removed_detected', run_seam(M2, stage_route_a)['verdict'] == 'SOURCE_EVIDENCE_READY', 'MUST_FAIL')
""", """if MODE == 'S1':   # PORT (G-wave): mutants of G6b's text act on its own (S1) code path only
    M1 = mutant('max_difference_over_P0_bound=b/(1-z))', 'max_difference_over_P0_bound=2*b/(1-z))', 'nonneg')
    hits = [case for case in NONNEG if not identical(call(EP, case, UQ), call(M1, case, UQ))]
    ck('MF_mutation_max_component_applied_to_nonnegative_detected', hits == list(NONNEG), 'MUST_FAIL', hits)
    M2 = mutant("            if v['state']['stage_kind']!='offset':raise ValueError('MAX_COMPONENT_NORMALIZATION_OFFSET_STAGES_ONLY')\\n", '', 'scope')
    ck('MF_mutation_offset_scope_removed_detected', run_seam(M2, stage_route_a)['verdict'] == 'SOURCE_EVIDENCE_READY', 'MUST_FAIL')
else:   # PORT (G-wave): in DELEGATED mode every entry is the b1 object's (identity of the delegation, by sentinel)
    _saved = ES.PRED.assemble_current
    ES.PRED.assemble_current = lambda *a, **k: 'B1_OBJECT_7044E131'
    try:
        _got = call(ES, 'accepted', UQ)
    finally:
        ES.PRED.assemble_current = _saved
    ck('MF_delegated_mode_assemble_current_is_the_b1_object', _got == 'B1_OBJECT_7044E131', 'MUST_FAIL', str(_got)[:80])
""", 1),
        ("result = {'schema': 'OFFSET_B1_EVIDENCE_TESTS_C2V001',", "result = {'schema': 'OFFSET_B1_EVIDENCE_TESTS_C2V001', 'gwave_port_mode': MODE,", 1),
        ("print(T.write_json_x(OUT / 'RESULT_EVIDENCE_B1_C2V001.json', result))",
         "print(T.write_json_x(OUT / ('RESULT_EVIDENCE_B1_PORT_GWAVE_%s_C2V001.json' % MODE), result))", 1)])
    S['b1enum'] = (B1T + '/test_enumerator_b1_c2v001.py', 'a67135918633d1a977357098e77f5ed5a9b2b9fbc2d2192f31ad399746767ff9',
                   'tests_b1_gwave/test_enumerator_b1_c2v001_PORT_gwave_c2v001.py', [
        ('"""A134 (b1) enumerator successor: the v010 join-protocol harness run on both.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the b1 enumerator harness against G6c, in two modes (env GW_PORT_MODE):\n'
         '  DELEGATED  the harness spec (non-S1): G6c hands it to 4ca7f364, whose module takes the harness seams;\n'
         '  S1         the harness spec with the S1_UA_C3T label and the CB C3T grid: G6c\'s own code takes the seams.\n'
         'The joined inventory must equal v010\'s once the module pins are swapped (to 4ca7f364/7044e131 in DELEGATED mode,\n'
         'to G6c/G6b in S1 mode). The b1-vs-v010 diff-scope check becomes the G6c render check.\n\n'
         'A134 (b1) enumerator successor: the v010 join-protocol harness run on both.\n', 1),
        ("sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/tests')\n",
         "sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.realpath(__file__)))   # PORT (G-wave)\n", 1),
        ("import b1_common_c2v001 as T\n", "import b1_common_c2v001_PORT_gwave_c2v001 as T   # PORT (G-wave)\nMODE = __import__('os').environ['GW_PORT_MODE']\nassert MODE in ('DELEGATED', 'S1')\n", 1),
        ("PRED_PIN, SUCC_PIN = T.pin_file(T.PRED['enumerator'][0]), T.pin_file(T.SUCC['enumerator'][0])\n"
         "EV_PRED, EV_SUCC = T.pin_file(T.PRED['evidence'][0]), T.pin_file(T.SUCC['evidence'][0])\n",
         "PRED_PIN, SUCC_PIN = T.pin_file(T.PRED['enumerator'][0]), T.pin_file(T.SUCC['enumerator'][0] if MODE == 'S1' else T.B1MOD['enumerator'][0])   # PORT (G-wave)\n"
         "EV_PRED, EV_SUCC = T.pin_file(T.PRED['evidence'][0]), T.pin_file(T.SUCC['evidence'][0] if MODE == 'S1' else T.B1MOD['evidence'][0])\n", 1),
        ("ck('MP_succ_A_is_b1_evidence', T.pin_file(MS_.A.__file__) == EV_SUCC and MS_.A.G.policy()['branch'] == 'MAX_COMPONENT_NORMALIZATION'\n",
         "ck('MP_succ_A_is_b1_evidence', T.pin_file(MS_.A.__file__) == T.pin_file(T.SUCC['evidence'][0]) and MS_.A.G.policy()['branch'] == 'MAX_COMPONENT_NORMALIZATION'   # PORT (G-wave): A is G6b\n", 1),
        ("ck('MP_succ_D_X_bytes_identical_to_v010', all(T.sha_file(getattr(MS_, k).__file__) == T.sha_file(getattr(MP_, k).__file__) == MP_.PINS[k][1] for k in ('D', 'X'))\n",
         "ck('MP_succ_D_X_bytes_identical_to_v010', all(T.sha_file(getattr(MS_, k).__file__) == T.sha_file(getattr(MP_, k).__file__) == MP_.PINS[k][1] for k in ('D',))\n"
         "   and T.sha_file(MS_.X.__file__) == MS_.PINS['X'][1] and MS_.X.PRED.__file__ == MP_.X.__file__   # PORT (G-wave): X is the G6a successor of v010's X\n", 1),
        ("spec = {'galaxy': 'DDO154', 'synthetic_protocol_fixture': True, 'coefficients': coef}\n",
         "spec = {'galaxy': 'DDO154', 'synthetic_protocol_fixture': True, 'coefficients': coef}\n"
         "if MODE == 'S1':   # PORT (G-wave): the S1_UA_C3T label and the CB C3T grid route consumed_states to G6c's own code\n"
         "    spec = dict(spec, label=T.S1_LABEL, numerics={'composite_grid_spec': T.cb_c3t_grid()})\n", 1),
        ("""    st = {'mode': 'normal', 'calls': []}
""", """    st = {'mode': 'normal', 'calls': []}
    M_obj = M                                            # PORT (G-wave): the module whose seams the harness sets
    if MODE == 'DELEGATED' and hasattr(M, 'PRED'):
        M = M.PRED                                       # the b1 object 4ca7f364, which computes every non-S1 spec
""", 1),
        ("""    joined = M.consumed_states(spec=spec, result=result, call_dir=call)
""", """    M = M_obj                                            # PORT (G-wave): calls go through the module under test
    joined = M.consumed_states(spec=spec, result=result, call_dir=call)
""", 1),
        ("""old_text, new_text = open(T.PRED['enumerator'][0]).read(), open(T.SUCC['enumerator'][0]).read()
ol = old_text.splitlines()
p0 = next(i for i, x in enumerate(ol, 1) if x.startswith(" 'D':("))
p1 = next(i for i, x in enumerate(ol, 1) if x.startswith(" 'X':("))
touched = T.changed_lines(old_text, new_text)
ck('MF_diff_confined_to_three_pin_lines', touched == set(range(p0, p1 + 1)), 'MUST_FAIL', sorted(touched))
""", """same, edits = T.rerender_equal('enumerator')   # PORT (G-wave): the successor is 4ca7f364 plus exactly the listed G6c edits
ck('MF_diff_confined_to_three_pin_lines', same, 'MUST_FAIL', edits)
""", 1),
        ("pairs = [(PRED_PIN, SUCC_PIN), (EV_PRED, EV_SUCC)]\n",
         "pairs = [(PRED_PIN, SUCC_PIN), (EV_PRED, EV_SUCC)] + ([(T.pin_file(MP_.X.__file__), T.pin_file(MS_.X.__file__))] if MODE == 'S1' else [])   # PORT (G-wave): X is G6a in S1 mode\n", 1),
        ("result = {'schema': 'OFFSET_B1_ENUMERATOR_TESTS_C2V001',", "result = {'schema': 'OFFSET_B1_ENUMERATOR_TESTS_C2V001', 'gwave_port_mode': MODE,", 1),
        ("print(T.write_json_x(OUT / 'RESULT_ENUMERATOR_B1_C2V001.json', result))",
         "print(T.write_json_x(OUT / ('RESULT_ENUMERATOR_B1_PORT_GWAVE_%s_C2V001.json' % MODE), result))", 1)])
    # ------------------------------------------------------------------ r5 closure -> G3 producer, G4 adapter, G6a graph
    S['r5'] = (CERT + '/test_r5_closure_cx2v002.py', '144569fb9df47052ab71fa7e738c93d75cc455519bd932027b21946b4ea59bf4',
               'tests_r5_gwave/test_r5_closure_cx2v002_PORT_gwave_c2v001.py', [
        ('"""Bounded r5 dependency/scope checks. No solver, run read or full grid replay.\n',
         '"""PORT (ks_k3_chain_c2 G-wave c2v001): the r5 closure checks with G (gq_producer), P (EPS adapter) and X (execution\n'
         'graph) replaced by their G-wave successors. Adapted (PORT (G-wave)): the successors\' custody is KS1 and P\'s response\n'
         'producer KS2; the GQ library check reads certs common c75aaa5a directly (no driver import); the three checks that\n'
         'derive custody from the real template inputs are not run (synthetic-only rule; 6810b7c3 is unchanged); writes go\n'
         'to this port\'s own folder. Usage: python3 -I -B <this file> OUT_DIR (new).\n\n'
         'Bounded r5 dependency/scope checks. No solver, run read or full grid replay.\n', 1),
        ("""H=Path(__file__).resolve().parent
A=H.parent.parent
""", """H=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # PORT (G-wave)
A=H.parent.parent
GWD=Path(__file__).resolve().parent.parent                                       # PORT (G-wave): the successors' folder
OUTD=Path(sys.argv[1]).resolve();OUTD.mkdir()                                   # PORT (G-wave): this run's own folder
""", 1),
        ("""def module(name):
    p=H/name
""", """def module(name):
    p=(GWD if name.endswith('_c2v001.py') and ('_g3_' in name or '_g4_' in name or '_g6_' in name) else H)/name   # PORT (G-wave)
""", 1),
        ("G=module('gq_producer_cx2v005.py')\n", "G=module('gq_producer_cx2v005_g3_c2v001.py')   # PORT (G-wave): G3\n", 1),
        ("P=module('point_response_admission_adapter_cx2v003.py')\n", "P=module('point_response_admission_adapter_cx2v003_g4_c2v001.py')   # PORT (G-wave): G4\n", 1),
        ("X=module('execution_graph_cx2v002.py')\n", "X=module('execution_graph_cx2v002_g6_c2v001.py')   # PORT (G-wave): G6a\n", 1),
        ("check('all_public_custodies_v002',all(Path(m.__file__).name=='custody_cx2v002.py' for m in (L.CU,G.C,E.C,P.CU,X.C)))\n",
         "check('all_public_custodies_v002',all(Path(m.__file__).name=='custody_cx2v002.py' for m in (L.CU,E.C))\n"
         "      and all(Path(m.__file__).name=='custody_cx2v002_ks1_c2v001.py' and Path(m.P.__file__).name=='custody_cx2v002.py' for m in (G.C,P.CU,X.C)))   # PORT (G-wave): KS1 over 6810b7c3\n", 1),
        ("check('response_r5',Path(L.PR.__file__).name=='point_response_producer_cx2v002.py' and Path(P.PR.__file__).name=='point_response_producer_cx2v002.py')\n",
         "check('response_r5',Path(L.PR.__file__).name=='point_response_producer_cx2v002.py' and Path(P.PR.__file__).name=='point_response_producer_cx2v002_ks2_c2v001.py'\n"
         "      and Path(P.PR.P.__file__).name=='point_response_producer_cx2v002.py')   # PORT (G-wave): KS2 over a1dcdea8\n", 1),
        ("for name,cc in [('LO',L.PR.CC),('EPS',P.PR.CC),('GQ',C.libraries()[1])]:\n",
         "for name,cc in [('LO',L.PR.CC),('EPS',P.PR.CC),('GQ',module('certs_common_r5_cx2v001.py'))]:   # PORT (G-wave): no driver import\n", 1),
        ("""details=C.derive_details(spec=spec)
check('actual_geometry_custody_r5',details['identity']==good and details['point_sha256']==C.digest(good))
check('actual_module_custody_r5',details['modules'][str(C.DRIVER)]==C.DRIVER_SHA)
check('actual_geometry_ordered_rows',len(details['row_contract']['rows'])>0)
""", """# PORT (G-wave): actual_geometry_custody_r5, actual_module_custody_r5, actual_geometry_ordered_rows are not run (real inputs).
""", 1),
        ("D=H/'r5_closure_synthetic_cx2v002';D.mkdir()\n", "D=OUTD/'r5_closure_synthetic_cx2v002';D.mkdir()   # PORT (G-wave)\n", 1),
        ("            fixture_spec=write('production_scope_only_spec.json',spec),point_sha256=details['point_sha256'],custody_sha256=details['custody_sha256'],\n",
         "            fixture_spec=write('production_scope_only_spec.json',spec),gwave_port=True,   # PORT (G-wave)\n", 1),
        ("with (H/'R5_CLOSURE_TESTS_CX2V002.json').open('x') as f:json.dump(report,f,indent=2);f.write('\\n')\n"
         "print(json.dumps({k:report[k] for k in ('passed','total','seconds','point_sha256','custody_sha256')}))\n",
         "with (OUTD/'R5_CLOSURE_TESTS_PORT_GWAVE_C2V001.json').open('x') as f:json.dump(report,f,indent=2);f.write('\\n')   # PORT (G-wave)\n"
         "print(json.dumps({k:report[k] for k in ('passed','total','seconds')}))\n", 1)])
    return S


def main():
    tgt = os.path.realpath(sys.argv[1])
    if not (tgt == KS or tgt.startswith(KS + '/dev/')):
        raise SystemExit('target must be %s or a folder under its dev/' % KS)
    S = suites(tgt)
    want = sys.argv[2:] or list(S)
    os.makedirs(os.path.join(tgt, 'diffs'), exist_ok=True)
    out = []
    for k in want:
        src, sha, name, subs = S[k]
        with open(src, 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise SystemExit('SUITE_PIN_MISMATCH %s %s' % (k, src))
        text = raw.decode('utf-8')
        counts = []
        for i, (old, new, n) in enumerate(subs):
            c = text.count(old)
            if c != n:
                raise SystemExit('SUBSTITUTION_COUNT %s #%d: %d != %d: %r' % (k, i, c, n, old[:100]))
            text = text.replace(old, new)
            counts.append(c)
        p = os.path.join(tgt, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        data = text.encode('utf-8')
        with open(p, 'xb') as f:
            f.write(data)
        diff = ''.join(difflib.unified_diff(raw.decode('utf-8').splitlines(True), text.splitlines(True), fromfile=src, tofile=p, n=2))
        dp = os.path.join(tgt, 'diffs', 'PORT_%s.diff' % os.path.basename(name)[:-3])
        with open(dp, 'xb') as f:
            f.write(diff.encode('utf-8'))
        out.append({'suite': k, 'source': {'path': src, 'sha256': sha}, 'port': {'path': p, 'sha256': hashlib.sha256(data).hexdigest()},
                    'substitutions': counts, 'diff': {'path': dp, 'sha256': hashlib.sha256(diff.encode('utf-8')).hexdigest()}})
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
