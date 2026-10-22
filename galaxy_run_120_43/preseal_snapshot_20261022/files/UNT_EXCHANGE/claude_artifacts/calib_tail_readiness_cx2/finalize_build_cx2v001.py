"""Seal the 0511/0515 build report and byte manifest; create-only outputs."""
import hashlib
import json
import os
from pathlib import Path
H=Path(__file__).resolve().parent
E=H.parent.parent
UTC=os.environ['UNT_CX2_PACKET_UTC']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def write(n,s):
    with (H/n).open('x') as f:f.write(s)

src=H/'calibration_orchestrator_cx2v006r5.py'
assert sha(src)=='d85af8eb20051b1a4faceac8ba142660556d744f585358a538cd3133a06f8358'
closure={'date_u':UTC,'status':'TESTED_SCOPED_STATIC_REVIEW','reviewer':'Codex2 lane_b_review helper',
 'source':pin(src),'basis':'Reviewer tool message at final r5 recheck; no separate scientific execution.',
 'findings_closed':['EPS and LO_ENVELOPE require exact proof schema, gate and independently derived custody digest.',
 'Acceptance pins the bytes parsed from the handoff and bundle; classifier persists these and cache put/reuse compares them with fresh verification.'],
 'remaining_concrete_gaps_in_scoped_paths':[],
 'limits':'Scientific producers, complete state enumerator, real point proofs and production readiness remain pending. Guard v001 deliberately unchanged.'}
write('REVIEW_CLOSURE_CX2V006R5.json',json.dumps(closure,indent=1)+'\n')

entries=[
('dispatch',E/'FROM_CODEX/0511_2026-10-18_codex2_calibration_readiness_and_v010_review.md'),
('waiver',E/'FROM_CODEX/0514_2026-10-18_codex_any_nice_waiver.md'),
('clarification',E/'FROM_CODEX/0515_2026-10-18_codex2_lane_A_scope_clarification.md'),
('orchestrator',src),
('parent_adapter',H/'calibration_orchestrator_cx2v006r1.py'),
('config64',H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json'),
('config128',H/'RUN_CONFIG_DDO154_CX2V006_KB128_R2.json'),
('coordinate_spec',H/'DDO154_COORDINATES_CX2V006.json'),
('coordinate_addendum',H/'COORDINATE_ADDENDUM_CX2V006.json'),
('taxonomy',H/'FAILURE_TAXONOMY_CX2V006_CANDIDATE.json'),
('config_generator',H/'generate_configs_cx2v006r2.py'),
('guard_active',H/'certificate_analysis/certificate_guard_cx2v001.py'),
('guard_signed_proposal',H/'certificate_analysis/certificate_guard_cx2v002.py'),
('point_requirements',H/'certificate_analysis/PER_POINT_REQUIREMENTS_CX2V001.json'),
('dependency_analysis',H/'certificate_analysis/CERTIFICATE_ANALYSIS_CX2V001.md'),
('box_replay_report',H/'certificate_analysis/BOX_REPLAY_REPORT_CX2V002.md'),
('static_test',H/'test_readiness_static_cx2v006.py'),
('static_result',H/'STATIC_CHECK_V006.json'),
('hook_test',H/'test_certificate_hooks_cx2v003.py'),
('hook_result',H/'CERTIFICATE_HOOK_CHECK_V003.json'),
('guard_result',H/'certificate_analysis/synthetic_checks_v001/RESULT.json'),
('signed_guard_result',H/'certificate_analysis/synthetic_signed_checks_v002/RESULT.json'),
('review_closure',H/'REVIEW_CLOSURE_CX2V006R5.json'),
('wave_fixture',H/'WAVE_FIXTURE_V001.json'),
('dry_summary',H/'DRIVER_DRYRUN_SUMMARY_V002.json'),
('corner_list',H/'corner_preparation_v001/CORNER_LAUNCH_LIST_V002.json'),
('corner_producer',H/'prepare_corner_specs_cx2v001.py'),
('cost_base',H/'certificate_analysis/COST_MODEL_CX2V001.json'),
('cost_waves',H/'COST_WAVES_CX2V002.json'),
('typed_blockers',H/'TYPED_BLOCKERS_CX2V006.json'),
('certificate_manifest',H/'certificate_analysis/HASHES_V002.txt'),
('metadata_producer',H/'finalize_metadata_cx2v001.py'),
('report_producer',Path(__file__))]
cfg=json.loads((H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json').read_bytes())
for k in ['driver','python','monitor','campaign']:
    assert pin(cfg[k]['path'])==cfg[k]
    entries.append((k,Path(cfg[k]['path'])))
entries.append(('v005_parent',H.parent/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'))
for n in ['STATIC_CHECK_V006.json','CERTIFICATE_HOOK_CHECK_V003.json','DRIVER_DRYRUN_SUMMARY_V002.json']:
    d=json.loads((H/n).read_bytes());assert d['passed']==d['total']

body='''# Codex2 Lane A — tail-corrected calibration readiness candidate

date -u: **{utc}**

**TESTED build/replay deliverable complete; production readiness PENDING. No scientific launches.** This packet executes dispatch0511 and clarification0515. Claude2 remains the sole coordinator and scientific launcher. The exact final implementation is `orchestrator`, with `config64` and `config128`; evidence labels below resolve to full paths and byte SHA256 values. The declared execution note is **"nice unavailable (sandbox); 0514 waiver"**. Replays used isolated prescribed Python, numpy/stdlib only, single-thread BLAS, and stayed below8GB per process.

**Implementation.** The successor retains the byte-pinned v005 engine/cache/receipt/lock/budget behavior through `parent_adapter`. Final source adds per-point certificate enforcement before calls, at result ingestion, cache insertion, cache verification, and cache reuse. Missing/mismatched certificate evidence is INFRA and is never promoted to scientific MODEL_INVALID. Both VALID and MODEL_INVALID cacheable results need verified evidence. Registry, producer policy, final adapter bytes and guard bytes enter the new cache identity; neither K candidate reuses the old3a1374df namespace or aliases the old tail-OFF anchor. Candidate source/taxonomy and scientific admission policy require coordinator/distinct review before production.

Tail ON uses the kept cube K=4 plus the continuum Qinf tail to the outer cylinder K_big64 or128, lambda1 and lapse-only. Route-A column_workers=8; free-surface column_workers=2. v010r4 arms RO1 c2v002 automatically on the tail-ON path. Its explicit ro1_workers flag is tail-OFF-only and is correctly omitted. All72 free-surface columns receive the full absolute hull [151250000,317625000] in enthalpy units. That absolute interval is retained under exact driver D geometry changes; no automatic widening or scaling is introduced. Headline D=4.04 and i=66 remain fixed. The driver refuses another inclination. Alternate-D specifications are separate capability/sensitivity cases, not a restored nuisance coordinate.

Both final configs declare new External1 workdirs and retain the original VolumeUUID guard. Sandbox volume lookup cannot validate the actual production context. Declared local, read-only planning fixtures substitute only workdir identity for dry checks; this does not establish production-volume readiness. No production workdir was created. The final CLI exposes plan/wave only; no launch command was used or added here.

**Certificate dependencies and computed evidence.** `dependency_analysis` gives source algebra; `box_replay_report` supersedes its formerly untested numerical portions. Let r=gamma/Eref_base and gamma_eff=s*r*Eref_base. EPS relative error and normalized non-lapse rho cancel common s*Eref_base at fixed r,ell_F; EPS still depends on r and ell_F (actual phase ell_F*k). Changing Eref at fixed gamma changes r and does not use this invariance. Qinf varies approximately0.403–161 but is an amplitude, not EPS relative error. LO additionally depends on source amplitude, rows/speeds and solved state; for a fixed source its B1 scales inversely with gamma_eff. D changes source/radial geometry; inclination would require rederivation and is unavailable in this driver.

TESTED: all8 free-box corners plus27 declared strict interior points in logarithmic coordinates;13 distinct r/ell pairs after exact common-scale cancellation. Actual-symbol sampled maximum |1-q|=0.012482344958803071 at the low-r/low-ell corner and |k|=4. A free-cardinal-torus spot-grid maximum is0.01504752661822473 at the same parameter pair. Both are finite sampled lower estimates of a supremum, not conservative box-wide EPS certificates. Common-scale and Eref-times2 cancellation probes agreed exactly on the declared sample set.

TESTED fixed-saved-source LO diagnostic: largest coarse-shell/tau estimates0.0029097531 for K64 and0.0065372280 for K128; corresponding sums0.0067912652 and0.0131771325. These use saved anchor speeds/source, sampled rho and enclosing shells extending to128/256, not exact candidate domains/current solved states. The K128 enclosing-shell indicator above0.005 is neither a K128 scientific failure nor permission to choose K64. Neither calculation supplies a box LO certificate. Current-point/current-state LO, including all consumed states and any required prelaunch envelope, remains UNTESTED.

TESTED stronger GQ evidence: exact driver-derived radial geometry at D=3.9810717055349722,4.04,4.111497211045223, both K candidates, every actual k_perp node and every GL4 column. The largest conservative M_s64/128 doubling bound is4.63528552591e-14 against1e-12. The positive-mass mixture theorem makes this reusable over all vertical positions and arbitrary nonnegative mixtures at each exact tested geometry. Thus it covers all35 s/r/ell points at headline D, subject to geometry/module/positivity custody; it does not certify arbitrary intermediate D. Float64/libm error is not analytically bounded; this is the registered numerical doubling convention.

Signed offset is body_gas minus routeA_gas_IT. Positive-component bounds imply absolute error<=b*(M_body+M_RA), not the same relative error divided by|M_body-M_RA|. The separate `guard_signed_proposal` permits only an explicit, nonzero signed-P0 branch with b*TV/P0<=1e-12 and verified component positivity. It does not silently use TV as the denominator. Zero P0 needs a coordinator normalization ruling; insufficient nonzero bounds need exact signed-source evidence. This proposal passed6/6 synthetic checks but is deliberately NOT imported by the final orchestrator: active guard v001 conservatively refuses signed states until policy is reviewed.

**Enforced point rule.** Byte-pinned registry entries must match each point. Independently reviewed custody derivation, complete consumed-state enumeration and approved producers are mandatory. The attached driver EPS and LO slots must equal the reviewed bundle bindings and their point/custody-bound proofs. LO_ENVELOPE must explicitly cover all consumed states; an anchor substitution cannot pass. The active guard checks EPS/GQ preflight and all required per-state LO/GQ at acceptance. An immutable per-call TAIL_CERTIFICATE_ACCEPTANCE.json binds the result SHA, call-spec SHA and post-state bundle. Ingestion stores its byte pin; cache put/reuse verifies it and the bundle again. The independent scientific adapters/proofs are absent, so real acceptance remains fail-closed. No scientific certificate has been fabricated to fill these slots.

**Verification.** TESTED33/33 final static/context checks;9/9 synthetic preflight/ingest/cache hook checks;22/22 core guard checks;6/6 proposed signed guard checks. The final scoped second review closed the proof schema/custody and handoff/cache substitution findings. These are control-path checks, not scientific validation of missing producers. `dry_summary` verifies70 actual v010r4 in-process reports:18 wave plans,4 distance plans and48 corner plans. Every report has0 executed stages, no simulated scientific pass, no pin/binding/unexplained blocker, and only pending EPS/LO beyond fields explicitly produced by a future call.

The first Jacobian fanout is3 calls per K (<=12); successful two-sided probes plus seed would be7 calls. Adaptive halving can add later waves. The first exploration fixture generates6 calls per K. Responses used to obtain that direction are explicitly synthetic midpoints, not physical model outputs; the production Jacobian and exploration direction remain UNTESTED. Corner and D plans exercise real driver geometry/hull assembly but supply no run-mode root-coverage evidence.

**Exact corner handoff.** `corner_list` pins48 immutable templates and48 dry reports:8 headline corners plus16 alternate-D corners per K. A55 selects one K. Every row carries exact theta, driver/template hash, intended output directory and proposed caps. EPS/LO remain sentinels. Fill only those slots into NEW filenames, hash the filled bytes and repeat the dry plan after prerequisite reviews; a template hash is not a launchable spec hash. Runtime, monitor and campaign are byte-pinned in the corrected list. Claude2 must ratify the proposed per-call8-hour wall,64-GiB RSS,12-GiB output,2-second poll ceilings; one concurrent call,8 route-A workers,2 fs workers and17 future process budget are production proposals, not an override of this account's2-process replay limit.

**Cost projection.** `cost_base` contains saved timing provenance; `cost_waves` gives28 arithmetic scenarios for3/6/7/8/12/16/24 cache misses and6/32 route-A iterations. Route-A tail construction is cold+I*warm (initial build plus one per completed iteration), not2I and not divided by8. Measured cold/warm seconds: K64=79.32/31.96; K128=284.82/103.43. The resulting per-call construction subtotals are4.52/15.09minutes atI6 and18.37/59.91minutes atI32. First3-call wave subtotals atI6 are13.55/45.27minutes;6-call exploration27.11/90.54minutes. Add every route-B consuming build, kept-cube work, tail evaluation, serialization/IO, certificate work and other stages. A measured le_rotation cold proxy is60.62/232.75seconds per B build, but its reuse for other stages is UNTESTED. Whole-call n_B, later changing sources,8-worker IPC/aggregate memory and total elapsed time are UNTESTED; these subtotals are not resource bounds. Saved single-process peaks~1.61/2.90GB do not justify an8-worker whole-call memory claim.

**Remaining decisions.** `typed_blockers` is the required six-category handoff: CERTIFICATE_SCOPE (Codex2 build/review plus Claude2 scientific decisions/launches), A55_K_BIG, V007_ADOPTION, TAIL_REANCHOR, CORNER_EVIDENCE and UNCERTAINTY_CARRIER_DECLARATION (Claude2). Each has deciding steps and byte-pinned evidence. No claim of zero production blockers is made. Actual tail-ON solved states, run-mode corner evidence, full scientific Jacobian/exploration, production runtime and blinded gates are UNTESTED by this lane.

**Immutable succession.** Earlier drafts and failed harness results remain for audit. The final source/config/result selections are the labels above. V001 wave/distance summaries used absent top-level keys and recorded null status/blockers; the corrected summary reads the real raw-report keys. Corner-list V001 had null runtime metadata; V002 pins the configured runtime without altering specs/reports. Initial explicit tail-ON ro1 flag drafts are superseded by R2 configs. The generator named below produces R2 successors into a new output directory. The final aggregate HASHES.txt covers every existing file below this lane directory except itself, including this report and preserved predecessors; its own SHA is carried in the numbered finished packet.

All cited evidence is pinned from current bytes below. Input manifests in the certificate report carry detailed source/state pins. No NGC3198 observed/target velocities or prohibited blinded run contents were opened; no network, git writes, deletion, renaming or overwriting was used.

'''.format(utc=UTC)
for label,p in entries:
    body+=f'- **{label}**: `{p}`; SHA256 `{sha(p)}`.\n'
write('BUILD.md',body)
files=sorted(p for p in H.rglob('*') if p.is_file() and p!=H/'HASHES.txt')
write('HASHES.txt','# date -u: '+UTC+'\n# SHA256 from file bytes; manifest excludes itself.\n'+''.join(f'{sha(p)}  {p}\n' for p in files))
print(json.dumps({'BUILD':pin(H/'BUILD.md'),'HASHES':pin(H/'HASHES.txt'),'files':len(files),'total_bytes':sum(p.stat().st_size for p in files)}))
