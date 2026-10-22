"""Immutable metadata successors only; no scientific execution."""
import hashlib
import json
import os
from pathlib import Path

H=Path(__file__).resolve().parent
UTC=os.environ['UNT_CX2_PACKET_UTC']
WAIVER='nice unavailable (sandbox); 0514 waiver'
def pin(p):
    p=Path(p)
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return json.loads(Path(p).read_bytes())
def put(n,d):
    with (H/n).open('x') as f:json.dump(d,f,indent=1,sort_keys=True);f.write('\n')

cfg=read(H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json')
corn=read(H/'corner_preparation_v001/CORNER_LAUNCH_LIST_V001.json')
corn.update(schema='DDO154_CORNER_LAUNCH_LIST_CX2V002',date_u=UTC,
    runtime=cfg['python'],runtime_flags=['-I','-B'],monitor=cfg['monitor'],campaign=cfg['campaign'],
    predecessor=pin(H/'corner_preparation_v001/CORNER_LAUNCH_LIST_V001.json'),
    production_workdir_guard='Existing External1 VolumeUUID guard unchanged. Local dry-run context is not production-volume validation.',
    build_account_cap='Two processes; each replay below8GB. Future production caps below are proposals for Claude2, not permission for this account.',
    metadata_correction='V001 runtime null came from wrong metadata lookup. V002 pins actual configured runtime; call templates and dry reports are unchanged.')
corn['sources'] += [pin(H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json'),pin(H/'RUN_CONFIG_DDO154_CX2V006_KB128_R2.json'),pin(__file__)]
for k in ('runtime','monitor','campaign'):
    assert pin(corn[k]['path'])==corn[k]
put('corner_preparation_v001/CORNER_LAUNCH_LIST_V002.json',corn)

rows=[]
for group,root in [('wave','driver_wave_dryplans_v001'),('distance','driver_distance_dryplans_v001'),('corner','corner_preparation_v001')]:
    for p in sorted((H/root).glob('*/DRYRUN_REPORT.json')):
        d=read(p);s=d['summary']
        reasons=s['refusals_beyond_pending_inputs']
        expected=['PENDING_UV_TAIL_CERTIFICATE: uv_tail.eps_certificate','PENDING_UV_TAIL_CERTIFICATE: uv_tail.lo_certificate']
        ok=(d['executed_stages']==0 and d['passes_simulated']==[] and not s['pin_problems']
            and not d['binding_blockers'] and not s['binding_blockers'] and not s['unexplained_refusals']
            and sorted(reasons)==sorted(expected))
        rows.append({'group':group,'report':pin(p),'structurally_ok_except_certificates':ok,
            'executed_stages':d['executed_stages'],'stages_planned':s['stages_planned'],
            'remaining_refusals':s['remaining_refusals_by_class']})
assert len(rows)==70 and all(r['structurally_ok_except_certificates'] for r in rows)
put('DRIVER_DRYRUN_SUMMARY_V002.json',{'date_u':UTC,'status':'TESTED','launches_performed':0,
    'execution_note':WAIVER,'counts':{g:sum(r['group']==g for r in rows) for g in ['wave','distance','corner']},
    'passed':len(rows),'total':len(rows),'rows':rows,
    'scope':'Actual in-process v010r4 dry plans; synthetic response fixtures determine wave coordinates. No production Jacobian or scientific solution measured.',
    'correction':'V001 wave/distance summaries looked for absent top-level status/blockers and recorded null. This successor reads actual summary keys and verifies every raw report.',
    'source':pin(__file__)})

blocks=[
 {'type':'CERTIFICATE_SCOPE','owner':'Codex2 build/review; Claude2 scientific decisions and launches',
  'status':'PENDING','deciding_step':'Review and supply byte-pinned independent custody deriver, complete consumed-state enumerator, certificate producers and policy. Produce point EPS envelope and prelaunch LO envelope; require exact-state LO/GQ at acceptance. Use saved finite-grid diagnostics only within stated scope. Signed offset needs reviewed nonzero-P0 branch or exact signed proof; zero P0 needs Claude2 normalization ruling. Missing solved sources require Claude2 corner/re-anchor launches.',
  'evidence':[pin(H/'certificate_analysis/BOX_REPLAY_REPORT_CX2V002.md'),pin(H/'calibration_orchestrator_cx2v006r5.py'),pin(H/'certificate_analysis/certificate_guard_cx2v002.py')]},
 {'type':'A55_K_BIG','owner':'Claude2','status':'PENDING','deciding_step':'Choose production K_big64 or128 under A55; retain both candidates until ruling. No inference from forbidden runs.',
  'evidence':[pin(H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json'),pin(H/'RUN_CONFIG_DDO154_CX2V006_KB128_R2.json')]},
 {'type':'V007_ADOPTION','owner':'Claude2, with distinct reviewer for candidate source/taxonomy','status':'PENDING',
  'deciding_step':'Seal adopted numerics and exact v010r4 driver binding; supply adoption derivation and review tail-aware taxonomy/certificate policy. Review the separate signed guard proposal before any promotion.',
  'evidence':[pin(H/'FAILURE_TAXONOMY_CX2V006_CANDIDATE.json')]},
 {'type':'TAIL_REANCHOR','owner':'Claude2 sole scientific launcher','status':'PENDING',
  'deciding_step':'Run chosen adopted tail-ON anchor after prerequisite certificate/adoption gates; provide immutable spec/result/receipt pins. Old tail-OFF anchor is never aliased into new cache.',
  'evidence':[pin(H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json')]},
 {'type':'CORNER_EVIDENCE','owner':'Claude2 sole scientific launcher','status':'PENDING',
  'deciding_step':'Select one K candidate, ratify proposed caps, fill per-point cert pins into new filenames, repeat dry plans, then launch eight headline corners. Sixteen alternative-D corner specs per K are separate capability/sensitivity evidence. Record full-hull bracket/root coverage and contraction evidence. No run-mode evidence currently exists in this lane.',
  'evidence':[pin(H/'corner_preparation_v001/CORNER_LAUNCH_LIST_V002.json')]},
 {'type':'UNCERTAINTY_CARRIER_DECLARATION','owner':'Claude2','status':'PENDING',
  'deciding_step':'Set declared_by and basis for the uncertainty carrier (or reviewed supported alternative). Current NOT_CARRIED_DECLARED placeholder is unsigned and fails readiness.',
  'evidence':[pin(H/'RUN_CONFIG_DDO154_CX2V006_KB064_R2.json')]}
]
put('TYPED_BLOCKERS_CX2V006.json',{'date_u':UTC,'status':'TESTED_PRESENT_GATES_UNTESTED_PRODUCTION_READINESS',
    'launches_performed':0,'execution_note':WAIVER,'blockers':blocks,
    'operational_guard':'External1 volume identity must pass in Claude2 launch context; preserved unchanged. Current local fixtures validate planning only.',
    'source':pin(__file__)})

base=read(H/'certificate_analysis/COST_MODEL_CX2V001.json')
out=[]
for k,t in base['timings'].items():
    for it in [6,32]:
        for label,n in [('jacobian_first_wave',3),('first_exploration_wave',6),('seed_plus_two_sided_jacobian',7),('headline_corners',8),('12_call_scenario',12),('alternative_D_corners',16),('all_prepared_corners',24)]:
            out.append({'K_big':int(k),'route_A_iterations':it,'scenario':label,'cache_misses':n,
                'route_A_tail_build_subtotal_seconds':n*(t['route_A_cold_s']+it*t['route_A_warm_s']),
                'extra_B_proxy_seconds_per_additional_build_per_call':n*t['route_B_rotation_cold_s']})
put('COST_WAVES_CX2V002.json',{'date_u':UTC,'status':'TESTED_ARITHMETIC_UNTESTED_WHOLE_CALL_PROJECTION',
    'execution_note':WAIVER,'source':pin(H/'certificate_analysis/COST_MODEL_CX2V001.json'),
    'wave_fixture':pin(H/'WAVE_FIXTURE_V001.json'),'rows':out,
    'formula':base['formula'],'limitations':base['limitations']+[
      'Measured timings are anchor component samples, not proven bounds at corners. Do not divide controller build time by eight.',
      'First Jacobian wave has3 planned calls. Six successful side probes plus seed are a conditional7-call scenario; adaptive halving can add later calls.',
      'First exploration has6 calls only in the declared synthetic response fixture. No physical direction/Jacobian has been measured.',
      'Dry reports expose11 first-pass stages but cannot determine full-call n_B before produced states and later passes exist.',
      '8-hour,64-GiB RSS,12-GiB output ceilings are proposed root caps, not timing-derived whole-call guarantees.']})
print(json.dumps({'dry_reports_checked':len(rows),'typed_blockers':len(blocks),'cost_scenarios':len(out)}))
