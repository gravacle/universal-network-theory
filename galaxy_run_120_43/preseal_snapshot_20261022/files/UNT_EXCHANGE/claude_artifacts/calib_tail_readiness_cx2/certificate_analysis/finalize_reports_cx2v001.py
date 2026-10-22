"""Exclusive-create short reports and SHA256 manifests; no numerical solver import.

Run once with the prescribed Python -I -B and single-thread environment. Source
inspection is TESTED; no box certificate or production runtime is asserted.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
sources = {
 'S01_dispatch': EX/'FROM_CODEX/0511_2026-10-18_codex2_calibration_readiness_and_v010_review.md',
 'S02_waiver': EX/'FROM_CODEX/0514_2026-10-18_codex_any_nice_waiver.md',
 'S03_frozen_decisions': UPC/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
 'S04_open_decisions': UPC/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md',
 'S05_binder': ART/'long_wavelength_response_c2/tools/lwr_common_v001.py',
 'S06_anchor_factory': ART/'tail_scheme_impl_c2/certificates_v001/tools/certs_common_c2v001.py',
 'S07_envelope': ART/'tail_scheme_impl_c2/certificates_v002/tools/certs2_common_c2v002.py',
 'S08_LO_producer': ART/'tail_scheme_impl_c2/certificates_v002/tools/lo_cert_c2v002.py',
 'S09_GQ_producer': ART/'tail_scheme_impl_c2/certificates_v002/tools/gq_cert_c2v002.py',
 'S10_cert_index': ART/'tail_scheme_impl_c2/certificates_v002/CERTIFICATES_V002.json',
 'S11_roster': ART/'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py',
 'S12_driver': ART/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
 'S13_A_controller': ART/'tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001.py',
 'S14_B_binding': ART/'tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001.py',
 'S15_timing_A64': ART/'tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0064_n6_V002.json',
 'S16_timing_A128': ART/'tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0128_n6_V002.json',
 'S17_timing_A128_initial': ART/'tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0128_n0_V002.json',
 'S18_timing_B64': ART/'tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_b_KB0064_V002.json',
 'S19_timing_B128': ART/'tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_b_KB0128_V002.json',
 'S20_EPS_record': ART/'tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json',
 'S21_guard': HERE/'certificate_guard_cx2v001.py',
 'S22_tests': HERE/'check_guard_cx2v001.py',
 'S23_test_result': HERE/'synthetic_checks_v001/RESULT.json',
 'S24_requirements': HERE/'PER_POINT_REQUIREMENTS_CX2V001.json'
}
def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()
def write(name, text):
    with (HERE/name).open('xb') as f:
        f.write(text.encode())
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
records = {k: {'path':str(p),'sha256':sha(p)} for k,p in sources.items()}
refs = '\n'.join('- %s: `%s`, SHA256 `%s`.' % (k, v['path'], v['sha256']) for k,v in records.items())
write('SOURCES_CX2V001.json', json.dumps({'utc':stamp,'files':records},indent=2)+'\n')
report = '''# Calibration certificate dependency and enforceable point rule

UTC: {stamp}. Scope: dispatch 0511 Lane A. Source/static review only; no launches.
Execution waiver for the bounded synthetic checks: "nice unavailable (sandbox); 0514 waiver".

**Conclusion — TESTED source inspection; numerical box coverage UNTESTED.** Existing V002 certificates bind the anchor symbol and saved R3 source states. They do not certify the calibration box. Use the fail-closed per-point rule in S24 and the metadata verifier S21. No new scientific EPS/LO/GQ certificate is issued here. Synthetic guard refutations in S22/S23 passed 22/22 at approximately 22.4 MB RSS; these establish guard behavior only.

Let r=gamma/Eref_base, E_eff=s Eref_base, gamma_eff=s r Eref_base, V=v0 ell_F^3, and N=J^T Gamma(F)J. From S05, K_density=E_eff*N/V+gamma_eff*H(k), and x=-K_density^-1 e0. Therefore q=4 gamma_eff |k|^2 x0 and normalized non-lapse rho=4 gamma_eff |k|^2 ||Cbar^-1/2 mat(x[1:7]) Cbar^-1/2|| cancel a common factor s Eref_base. The actual finite-k F depends on ell_F k. In the free cardinal-torus envelope, that phase is independent, but N/(r V) remains. The cancellation is exact algebra (TESTED by source inspection); floating-point equality across rescalings and box-wide finite-k maxima are UNTESTED here.

| Coordinate | EPS | LO | GQ |
|---|---|---|---|
| common s | Analytically invariant at fixed r, ell_F, grid/background | rho invariant, but B1 scales as 1/gamma_eff for a fixed source; state/speeds may change | No direct symbol dependence; saved-source normalized error may change with nonuniform source weights |
| gamma/Eref_base r | Finite-k symbol and envelope depend on r | rho, B1 and solved state depend on r | No direct dependence; indirect evolving source dependence |
| Eref_base | Invariant only when gamma is changed with it to keep r fixed | B1 scales inversely if both effective coefficients scale; state may change | No direct dependence; indirect source dependence |
| ell_F | Actual torus phase and native/EH ratio change; envelope depends on r ell_F^3 | rho and solved source change | No direct dependence; indirect source dependence |
| D | No direct symbol dependence | Source radii/masses, evaluation radii, v and row contract change | Radial geometry changes; fixed-geometry GQ proof cannot be reused |
| inclination | No direct symbol dependence | A rederived source/readout would change | A rederived source/geometry could change |

**TESTED executable limitation:** S12 rejects inclination other than 66 degrees with BLOCKED_GAS_REDEPROJECTION. The requested inclination dependence is therefore a mathematical/conditional concern, not an available calibration coordinate. S12 derives D-dependent HI edges and row radii, so D must enter geometry custody. Holding gamma fixed while changing Eref changes r and does not invoke the EPS cancellation.

**A21 does not make EPS scale with Qinf.** S03 states Qinf=c^4/(16 pi G gamma_eff), roughly 0.403–161 across the box. This is the tail amplitude, whereas EPS is relative error q-1 and cancels common scale. An anchor EPS or LO pass is not a box pass. S06 hard-codes the anchor Binder; S08 binds saved C4R3 rows/source; S09 uses saved C2R3/C3R3/C4R3 rosters. S10's reported passing values are prior producer measurements, not independent replays by this lane.

**EPS point rule.** Exact grid/background, r, ell_F, units and module custody; conservative envelope over direction x cardinal torus on all required |k| shells, including cylinder corners through ceil(sqrt(2)*K_big): 91 for K_big64 and 182 for K_big128. Preserve the registered refinement condition (two failures uncertified). The envelope remains a numerical maximization estimate, not a rigorous analytic supremum. S20 currently covers through 363 at the anchor; coverage in k does not imply coverage in calibration coordinates. The new guard deliberately requires eps >= eps_envelope throughout, which is conservative relative to S20's actual-set values in its lowest shells.

**A source-independent GQ rule can be enforced before a call.** S11 gives S=sum_i P_i(k_perp) sigma_i(k_z), P_i(0)=2 pi rdr_i>0 (GL4 exactly integrates cubic Lagrange), sigma_i(k_z)=sum_a m_ia exp(-i k_z z_ia)/(2 pi rdr_i). For nonnegative element masses, |sigma_i(k_z)|<=sigma_i(0). Thus |S_M-S_2M|/sum(m)<=max_i |P_i^M-P_i^2M|/P_i(0), uniformly in all vertical positions and arbitrary nonnegative mass redistribution. Compute this maximum at every production k_perp node and every possible column at each D, accounting conservatively for zero-mode floating-point discrepancy; require <=1e-12. This covers the registered seeded-node criterion more strongly. **UNTESTED numerically:** the max-column criterion itself has not been computed for this box. Existing mass-weighted saved-roster bounds do not establish it.

**LO current-state rule.** S08 uses |delta v_i,shell| <= (v_i R_i/4)*rho_shell*B1_shell, with B1 an absolute source-tail integral. It depends on the actual roster and row contract. A coordinator-reviewed point/source envelope may cover all iterates; otherwise replay each consumed state and gate acceptance only after all required LO records pass (each shell <=0.005 tau; sum <=0.05 tau), exact current state/source hashes, and I1T source fidelity. A changed state invalidates the old LO. This metadata guard does not prove nonlinear fixed-point error bounds beyond the registered LO definition.

**Integration and remaining work.** S21 verifies byte integrity, point/custody identity, reviewed producer hashes, numerical thresholds, full shell coverage and an exact caller-supplied state inventory. Its caller must run the adapter's production validate_block (kept K4), derive custody and complete state inventory independently, and call acceptance before cache/result admission. It cannot infer missing states from a certificate manifest or approve its own producer. Prelaunch EPS/GQ acceptance is not launch authorization; the production module still needs an appropriate LO slot, and no provisional-anchor shortcut is authorized. Present proofs are missing, so the correct status is pending certificates. Full live integration into driver iteration/accepted-result handling, real point proofs, and a complete tail-on calibration are UNTESTED.

All cited files are bound below from bytes. S04 is the observed open addendum, not a frozen program pin; no new root decision is inferred here.

{refs}
'''.format(stamp=stamp,refs=refs)
write('CERTIFICATE_ANALYSIS_CX2V001.md', report)
timings = {}
for kb in (64,128):
    a=json.loads(sources['S15_timing_A64' if kb==64 else 'S16_timing_A128'].read_bytes())
    b=json.loads(sources['S18_timing_B64' if kb==64 else 'S19_timing_B128'].read_bytes())
    cold=a['cold_build_wall_seconds']; warm=a['warm_build']['build_wall_seconds']; rb=b['cold_build_wall_seconds']
    timings[str(kb)]={'route_A_cold_s':cold,'route_A_warm_s':warm,'route_B_rotation_cold_s':rb,
      'route_A_later_lapse_pair_s':a['evaluation']['lapse_pair_later_s']['mean'],
      'route_A_first_line_s':a['evaluation']['lapse_pair_first_per_line_s']['mean'],
      'route_A_peak_rss_bytes_measured':a['peak_rss_bytes_end'],
      'route_B_peak_rss_bytes_measured':b['peak_rss_bytes_end'],
      'projection_A_build_only':[{'iterations':i,'calls':q,'seconds':q*(cold+i*warm)} for i in (6,32) for q in (1,7,12)]}
cost={'utc':stamp,'status':'TESTED_EXTRACTION_AND_ARITHMETIC_UNTESTED_PRODUCTION_PROJECTION',
      'waiver':'nice unavailable (sandbox); 0514 waiver','timings':timings,
      'formula':'T_call = T_kept_cube_and_other + A_cold + I*A_warm + sum_j B_build_j + T_tail_evaluations + T_serialization_IO + T_certificates',
      'measured_B_proxy':'n_B * measured le_rotation cold build; applicability to other stages UNTESTED',
      'wave_formula':'sum over cache misses of per-call costs; q in {7,12} is a scenario, not an executed plan; cache hits retain validation costs',
      'limitations':['No complete tail-on call timed','No 8-worker tail serialization/IPC or aggregate RSS timing',
        'Warm sample repeats same saved state; later changing sources and >6 iterations are unmeasured',
        'n_B depends on actual consuming stages and process lifetime; not assumed one per Picard pass',
        'Current account 2-process limit is for replays, not a production scheduling authorization',
        'No production K_big selected; no comparison with forbidden C5H/UVT runs'],
      'sources':{k:v for k,v in records.items() if k.startswith(('S13_','S14_','S15_','S16_','S17_','S18_','S19_'))}}
write('COST_MODEL_CX2V001.json',json.dumps(cost,indent=2)+'\n')
rows='\n'.join('| %s | %.2f | %.2f | %.2f | %.3f |' % (k,v['route_A_cold_s'],v['route_A_warm_s'],v['route_B_rotation_cold_s'],1000*v['route_A_later_lapse_pair_s']) for k,v in timings.items())
prows='\n'.join('| %s | %s | %s | %.2f |' % (k,r['iterations'],r['calls'],r['seconds']/60) for k,v in timings.items() for r in v['projection_A_build_only'])
costtext='''# Cost projection — tail components, not complete calls

UTC: {stamp}. TESTED extraction/arithmetic from saved timing records; complete production cost UNTESTED.

| K_big | A cold build s | A warm build s | B rotation cold s | A later lapse pair ms |
|---|---:|---:|---:|---:|
{rows}

S13 builds the initial source, then one next-source state per completed route-A iteration. begin_iteration reuses that pending state. Thus a cold uninterrupted call has I+1 builds, modeled as cold + I*warm. S17's K128 initial-source sample is 260.28s cold / 76.87s warm, compared with 284.82/103.43 at saved iteration6; the latter is used below, without claiming an upper bound.

| K_big | Completed A iterations | Cache-miss calls | A build subtotal minutes |
|---|---:|---:|---:|
{prows}

Per call add n_B*60.62s (K64) or n_B*232.75s (K128) as a **rotation-stage build proxy only**, plus tail evaluations, kept-cube computation, certificates, serialization, stage setup and I/O. Exact n_B is not yet available from an executed candidate plan. The 7-call and 12-call rows are wave scenarios; substitute actual uncached calls from the Jacobian/exploration plan. Neither row is a measured whole wave. For unequal calls, sum each call's I and stage costs. Do not divide serial controller/build terms by eight: workers8 parallelizes column solving; the measured build is in the controller.

Saved route-A iterations have roughly 60,000 metric calls each. Warm pair costs imply roughly 17.5s/34.6s of additional pair CPU per 60,000 calls, before approximately 18ms first-line setup, jets, monitors, IPC and parallel efficiency. This is only a workload illustration; exact invocation/cache counts are unmeasured. Eight-worker aggregate memory is unmeasured; measured single-build RSS cannot be multiplied into a validated whole-run bound. S15/S16 report about 1.61/2.90 GB process peak; S18/S19 about 0.83/1.27 GB. The module's smaller memory estimates omit important temporaries/process duplication.

No forward, route-A or route-B launch occurred. No forbidden run was opened. The coordinator must set the production K_big and operational caps after actual call-plan accounting and admitted production evidence. These projections do not authorize launches.

Timing/source pins:

{refs}
'''.format(stamp=stamp,rows=rows,prows=prows,refs='\n'.join('- %s: `%s`, SHA256 `%s`.'%(k,v['path'],v['sha256']) for k,v in cost['sources'].items()))
write('COST_PROJECTION_CX2V001.md',costtext)
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name != 'HASHES.txt')
write('HASHES.txt',''.join('%s  %s\n'%(sha(p),p) for p in files))
print(json.dumps({'utc':stamp,'reports_written':True,'files_hashed':len(files),'scientific_box_certificates':'UNTESTED'}))
