"""Create immutable 0515 replay report and byte manifests. No launches."""
import datetime
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
EX=ART.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def get(n):return json.loads((HERE/n).read_bytes())
def write(n,v):
    with (HERE/n).open('xb') as f:f.write(v.encode())
symbol=get('BOX_SYMBOL_LO_REPLAY_CX2V001.json')
env=get('BOX_ENVELOPE_SPOT_REPLAY_CX2V001.json')
gq=get('BOX_GQ_EXACT_REPLAY_CX2V002.json')
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
paths={
 'dispatch':EX/'FROM_CODEX/0515_2026-10-18_codex2_lane_A_scope_clarification.md',
 'symbol':HERE/'BOX_SYMBOL_LO_REPLAY_CX2V001.json',
 'envelope':HERE/'BOX_ENVELOPE_SPOT_REPLAY_CX2V001.json',
 'gq_exact':HERE/'BOX_GQ_EXACT_REPLAY_CX2V002.json',
 'gq_scaled_predecessor':HERE/'BOX_GQ_REPLAY_CX2V001.json',
 'symbol_producer':HERE/'box_replay_cx2v001.py',
 'envelope_producer':HERE/'box_envelope_spot_cx2v001.py',
 'gq_exact_producer':HERE/'box_gq_exact_geometry_cx2v002.py',
 'guard_v002':HERE/'certificate_guard_cx2v002.py',
 'guard_builder':HERE/'build_signed_guard_cx2v002.py',
 'guard_tests':HERE/'check_signed_guard_cx2v002.py',
 'guard_test_result':HERE/'synthetic_signed_checks_v002/RESULT.json',
 'requirements_v001':HERE/'PER_POINT_REQUIREMENTS_CX2V001.json',
 'prior_report':HERE/'CERTIFICATE_ANALYSIS_CX2V001.md',
 'coordinate_spec':ART/'calibration_orchestrator_c2/DDO154_CALIBRATION_COORDINATE_SPEC_V001.json',
 'coordinate_addendum':ART/'calibration_orchestrator_c2/v005/COORDINATE_SPEC_ADDENDUM_V005.json',
 'engine':ART/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py',
 'LO_saved_bound':ART/'tail_scheme_impl_c2/certificates_v002/gates/LO_CERT_V002.json',
 'GQ_prior_producer':ART/'tail_scheme_impl_c2/certificates_v002/tools/gq_cert_c2v002.py',
 'offset_binding':ART/'tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001.py',
 'driver':ART/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
 'report_producer':Path(__file__)}
pins={k:{'path':str(p),'sha256':sha(p)} for k,p in paths.items()}
pins.update({'symbol_input_'+k:v for k,v in symbol['anchor_info']['pins'].items()})
write('SOURCES_CX2V002.json',json.dumps({'utc':stamp,'sources':pins},indent=1)+'\n')
worst=symbol['EPS_worst'];point=next(p for p in symbol['points'] if p['point']==worst['point'])
epspair=symbol['EPS'][worst['pair_index']]
epsarg=max(epspair['shells'],key=lambda r:r['sampled_eps'])
epair=env['worst'];earg=max(epair['rows'],key=lambda r:r['sampled_envelope_eps'])
lo_rows='\n'.join('| %d | %s | %.12g | %.12g | %s |' % (k,symbol['LO_worst'][str(k)]['point'],
    symbol['LO_worst'][str(k)]['LO_fixed_state'][str(k)]['max_shell_over_tau'],
    symbol['LO_worst'][str(k)]['LO_fixed_state'][str(k)]['sum_max_over_tau'],
    symbol['LO_worst'][str(k)]['LO_fixed_state'][str(k)]['enclosing_shell_endpoint']) for k in (64,128))
gq_rows='\n'.join('| %.15g | %d | %.12g | %.12g | %d |' % (r['distance_Mpc'],k,r['worst'][str(k)]['conservative_bound'],r['worst'][str(k)]['kp'],r['worst'][str(k)]['column_1based']) for r in gq['cases'] for k in (64,128))
refs='\n'.join('- %s: `%s`; SHA256 `%s`.'%(k,v['path'],v['sha256']) for k,v in pins.items())
text='''# 0515 calibration-box replay evidence and remaining point gates

UTC: {stamp}. No launches. Every replay used the prescribed isolated Python, one process, single-thread BLAS, and "nice unavailable (sandbox); 0514 waiver". Files are immutable successors.

**Outcome: TESTED finite-grid EPS/LO evidence and geometry-uniform GQ; no whole-box scientific certificate claimed.** The actionable admission path remains a per-point EPS/LO/state rule. This is the 0515 extension of the prior source-only report, not a promotion of anchor certificates.

**Declared box/grid.** Read the coordinate spec, V005 addendum and v003b engine. Headline coordinates are s, gamma/Eref and ell_F, all logarithmic; D=4.04 Mpc and inclination66 degrees are fixed. Eref_base=1.4642919592009638e58 J is fixed; its placeholder lower/upper values are not a free box. Evaluated all8 free-box corners plus27 strictly interior points at u=(0.25,0.5,0.75)^3 in the engine log-box. Exact common-scale cancellation reduced symbol work to13 distinct (gamma/Eref,ell_F) pairs; each of the35 physical points has an explicit derived record. Separate GQ evaluations cover D lower/registered/upper. Those three D values do not certify every intermediate D.

**EPS — TESTED samples, UNTESTED supremum.** Actual symbol:52 declared directions times lower/geometric-middle/upper radius in every unit shell from4 through182 /kpc. The largest sampled |1-q| is **{eps:.16g}**, at {pointid}, shell {shell}, physical k vector {karg} /kpc. Coordinates: s={s:.17g}, gamma/Eref={r:.17g}, ell_F={ell:.17g} m. gamma_eff={ge:.17g}, Qinf={qi:.17g}. This is a lower-bound estimate of the supremum, not an upper envelope or a gate pass.

The additional free-cardinal-torus spot grid used52directions x64torus points at |k|=4,4.5,5,8,32,64,128,182 for each of13pairs. Its largest sampled envelope error is **{enveps:.16g}** at |k|={envk:g}, direction {envdir}, torus {envt}, at the same low-r/low-ell pair. This too is a sampled lower bound, not a maximized/global supremum. q_env(k,t(k)) matched the actual q path to maximum absolute difference {envdiff:.6g}. The anchor QINF reproduction was bitwise equal. Across all13pairs, s-endpoint and Eref-times2 probes at52directions gave maximum absolute q change {scdiff:.6g}; exact algebraic cancellation was therefore numerically confirmed on that declared probe set.

**LO — TESTED fixed-saved-source estimates, UNTESTED solved-state certificate.** Replayed normalized non-lapse rho at52directions and3radii per registered coarse shell; used the byte-pinned existing saved-C4R3 B1 quadrature and its saved row speeds/radii, with exact1/gamma_eff source-amplitude scaling. B1 was not independently rebuilt. The K64 estimate uses enclosing shells through128, and K128 through256 from the saved cylinder256 record. Thus neither is the exact candidate-domain calculation. Every maximum below is at saved row8.

| Candidate K_big | Worst declared point | Largest shell /tau | Sum of shell maxima /tau | Enclosing shell endpoint |
|---|---|---:|---:|---:|
{lo_rows}

The K128 enclosing-shell indicator exceeds0.005 at the low-s/low-r/low-ell corner; **this is not a K128 scientific failure**: the source and row speeds are the saved anchor's, rho is sampled, and the high shell contains frequencies outside the K128 cylinder. It demonstrates why a blanket anchor LO certificate is unjustified. K64's sampled estimates below threshold likewise do not certify the box. The deciding work is exact-domain/current-source LO at each candidate call, after Claude2's required source-state launches. The fixed-state computations make no claim about fixed-point validity, proper-volume feedback error beyond the registered LO indicator, or D-rescaled solved states.

**GQ — TESTED stronger all-column positive-mass bound.** Computed both M_s64 and128 radial transforms at every actual production k_perp node for K64(10496nodes) and K128(20736nodes), union30072, every GL4 column. Used exact v010r4 derive_geometry output for each D. The earlier simple-rescaled-edges record is preserved as a diagnostic predecessor and superseded for point geometry by gq_exact. At nonregistered D the two edge constructions are not bitwise equal; exact driver edges matter for custody.

| D Mpc | K_big | Conservative all-column bound | k_perp argmax /kpc | Column1based |
|---|---|---:|---:|---:|
{gq_rows}

Every value is below1e-12, with at least21.5x margin. The bound is max_i|P_i64-P_i128|/analytic P_i(0), divided by1-minus-the-measured-zero-mode-relative-error. Since P_i(0)=2pi rdr_i>0 and |sigma_i(kz)|<=sigma_i(0) for nonnegative element masses, this covers arbitrary vertical positions and nonuniform positive mass mixtures, all k_z, and every registered seeded node for that exact geometry/config. Therefore it applies to all35 s/r/ell points at D4.04, and to the alternative-box corners at tested D endpoints, conditional on actual mass positivity and identical radial geometry/module/quadrature custody. It does not require the missing solved source merely to establish this positive-roster radial-quadrature bound. POSIX libm/float64 error is not analytically bounded; the measured criterion is the registered M_s doubling convention.

**Signed offset — distinct remaining gate.** Source inspection confirms offset=body_gas minus routeA_gas_IT in _DifferenceRoster. Existing GQ producer records P0=abs(S_gas(0))=gas mass for positive component rosters; it neither evaluates that signed offset nor defines a replacement denominator. The positive-mass theorem gives |delta S_offset|<=b*(M_body+M_RA). It does not give the same relative bound divided by |M_body-M_RA|. Conservatively retain signed P0 and demand b*TV/P0<=1e-12, with positive component custody; if this is insufficient, an exact signed-source replay or a root normalization ruling is required. At P0=0 the signed relative criterion is undefined. **No silent TV renormalization is used.**

The v001 guard rejected signed states outright. Guard v002 adds only this explicit nonzero signed-P0/TV-bound branch, requiring exact state/proof hashes and independently approved producers. It still refuses zero/invalid P0, missing component positivity, contradictory bounds, silent normalization change or an insufficient bound. Six synthetic signed tests passed; no real signed state has been certified by this helper. The root must review the proposed branch and carry any normalization decision before registry admission.

**Enforcement / deciding launch.** Keep EPS/LO pending at unproved points. Verify full point/grid/background/geometry/module/row custody, per-state source hashes and complete caller-derived consumed-state inventory. GQ positive-source evidence may be reused only by the exact tested geometry. Signed offset needs the branch above or a reviewed explicit source replay. The production orchestrator must apply the acceptance guard before admitting or replaying a cache result. For missing point route-A states, Claude2's listed v010r4 tail-ON corner/re-anchor calls are the deciding launches; Codex2 does not launch them. Interior-point solved states remain absent and need owner-approved per-point calls when encountered. A55 K_big, V007 adoption, tail re-anchor, run-mode corner evidence and uncertainty-carrier declaration remain coordinator decisions/evidence, not inferable from these replays.

**Measured resources.** Symbol/LO: {sysec:.2f}s, peak{symem:.2f}MB; envelope spot: {ensec:.2f}s, peak{enmem:.2f}MB; exact-geometry GQ: {gqsec:.2f}s, peak{gqmem:.2f}MB. All below8GB. The predecessor GQ geometry diagnostic took68.90s/55.00MB. Outputs remain small; no state arrays were copied.

Byte pins for every cited artifact/input:

{refs}
'''.format(stamp=stamp,eps=worst['EPS_sampled_max'],pointid=worst['point'],shell=epsarg['range_inverse_kpc'],karg=epsarg['k_argmax_inverse_kpc'],
    s=point['common_scale_s'],r=point['gamma_over_Eref'],ell=point['ell_F_m'],ge=worst['gamma_eff'],qi=worst['Qinf'],
    enveps=earg['sampled_envelope_eps'],envk=earg['k_inverse_kpc'],envdir=earg['eps_argmax_direction'],envt=earg['eps_argmax_t'],
    envdiff=env['max_env_actual_difference'],scdiff=symbol['max_scaling_abs_q_change'],lo_rows=lo_rows,gq_rows=gq_rows,
    sysec=symbol['seconds'],symem=symbol['peak_rss_bytes']/1e6,ensec=env['seconds'],enmem=env['peak_rss_bytes']/1e6,
    gqsec=gq['seconds'],gqmem=gq['peak_rss_bytes']/1e6,refs=refs)
write('BOX_REPLAY_REPORT_CX2V002.md',text)
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='HASHES_V002.txt')
write('HASHES_V002.txt',''.join('%s  %s\n'%(sha(p),p) for p in files))
print(json.dumps({'utc':stamp,'report_sha256':sha(HERE/'BOX_REPLAY_REPORT_CX2V002.md'),
  'manifest_sha256':sha(HERE/'HASHES_V002.txt'),'files':len(files)}))
