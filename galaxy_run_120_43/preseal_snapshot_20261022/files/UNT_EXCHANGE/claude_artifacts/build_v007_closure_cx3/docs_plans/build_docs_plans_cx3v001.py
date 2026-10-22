from pathlib import Path
import copy, hashlib, json, os, subprocess

P = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1')
E = Path(__file__).parent
NEWROOT = '/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007'
OLDROOT = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
EXPECTED = {
 'RUNBOOK_V007.md':'648cfd748eb65bf08e9e79e9a27b5fb30c575128fdfd6556b71ae9e2c9e390cf',
 'ROOT_SEAL_ADMISSION_FORMAT_V004.md':'6908ee88e903443487280bfde6d4e91d6d4a53b621aee543eba8948cfcda1fb1',
 'P128/LAUNCH_PLAN_V010.json':'26f1ebf90d95d2674d4bcba7ac3416049cdba171c5754c32440b4c66480c8021',
 'P128/CASES_MANIFEST_TEMPLATE_V010.json':'ec884ff7d9797044422ce2752ef3d94d7062b63e3f1c02502a80d56686e5e1ce',
 'P128/LAUNCH_COMMAND_V010.txt':'7d649ac5e0fe6a17625e7c773e1ed500101367ea8b99d578c2da8f716e1809c4',
 'ALLOWLIST_DRAFT_V005.txt':'23af0a4000374627fdaab622cd82bd49fef49fc66edd097cfebe29ef2961ab39',
 'postseal_records_cx1v006_cx3v001.py':'4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366',
 'srb_rot_record_cx1v008_cx3v001.py':'2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc',
}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, b):
    with Path(p).open('xb') as f: f.write(b if isinstance(b,bytes) else b.encode())
def jbytes(x): return (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
for n,h in EXPECTED.items(): assert sha(P/n)==h, n
date = subprocess.check_output(['date','-u'],text=True).strip()
root = Path('/Users/bgm/Research')
assert root.resolve()==root
assert root.stat().st_dev == Path('/System/Volumes/Data').stat().st_dev
assert not os.path.lexists('/Users/bgm/Research/UNT_INTERNAL_RUNS')
fs = {'date_u':date, 'status':'TESTED', 'parent_path':str(root), 'resolved_parent':str(root.resolve()),
      'parent_st_dev':root.stat().st_dev,'startup_data_st_dev':Path('/System/Volumes/Data').stat().st_dev,
      'df':subprocess.check_output(['df','-P',str(root)],text=True),
      'scientific_output_ancestor_exists':False,'scientific_output_directories_created':False,
      'scope':'Existing parent is the local startup data volume; proposed UNT_INTERNAL_RUNS ancestor is absent. No scientific run path was accessed.',
      'hardware_inspection':'UNTESTED: prior diskutil info /dev/disk3s5 failed because DiskManagement framework unavailable; no escalation requested.'}
write(E/'FILESYSTEM_EVIDENCE_CX3V001.json',jbytes(fs))
live=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
livebytes=live.read_bytes()
snapshot=E/'ROOT_DECISIONS_V005_READ_SNAPSHOT_CX3V001.md'
write(snapshot,livebytes)
snapshotpin={'source':str(live),'source_sha256_at_read':hashlib.sha256(livebytes).hexdigest(),'date_u':date,'path':str(snapshot),'sha256':sha(snapshot),'not_a_root_frozen_addendum':True}
write(E/'ROOT_DECISIONS_SNAPSHOT_CUSTODY_CX3V001.json',jbytes(snapshotpin))
plan=json.loads((P/'P128/LAUNCH_PLAN_V010.json').read_bytes())
oldplan=copy.deepcopy(plan)
changes=[]
def remap(v):
    assert isinstance(v,str) and v.startswith(OLDROOT+'/')
    assert v.count('_V010')==1
    return NEWROOT+'/'+v[len(OLDROOT)+1:].replace('_V010','_V011_CX3V001')
for i,c in enumerate(plan['calls']):
    for k in ('outdir','receipt','monitor_log'):
        v=c[k];c[k]=remap(v);changes.append({'path':['calls',i,k],'before':v,'after':c[k]})
    for flag in ('--outdir','--receipt'):
        j=c['monitor_argv'].index(flag)+1
        v=c['monitor_argv'][j];c['monitor_argv'][j]=remap(v)
        changes.append({'path':['calls',i,'monitor_argv',j],'before':v,'after':c['monitor_argv'][j]})
v=plan['launcher_log'];plan['launcher_log']=remap(v)
changes.append({'path':['launcher_log'],'before':v,'after':plan['launcher_log']})
assert len(changes)==51
manifest=json.loads((P/'P128/CASES_MANIFEST_TEMPLATE_V010.json').read_bytes())
oldmanifest=copy.deepcopy(manifest)
for c in plan['calls']: manifest['cases'][c['case']]=c['outdir']
assert manifest['cases']['C5H']==oldmanifest['cases']['C5H']
command=(P/'P128/LAUNCH_COMMAND_V010.txt').read_text().replace('P128/LAUNCH_PLAN_V010.json','P128/LAUNCH_PLAN_V011_CX3V001.json')
runbook=(P/'RUNBOOK_V007.md').read_text()
runbook=runbook.replace('# V007 r5 P128/MS128 runbook — 0559/0561 successor','# V007 r5 P128/MS128 runbook — A99 BUILD_V007 successor\n\ndate -u: '+date)
for a,b in [
 ('BUILD_V006','BUILD_V007'),('ROOT_SEAL_ADMISSION_FORMAT_V004.md','ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md'),
 ('P128/LAUNCH_PLAN_V010.json','P128/LAUNCH_PLAN_V011_CX3V001.json'),('PRODUCER_INDEX_V008','PRODUCER_INDEX_V009_CX3V001'),
 ('postseal_records_cx1v006.py','postseal_records_cx1v006_cx3v001.py'),('srb_rot_record_cx1v008.py','srb_rot_record_cx1v008_cx3v001.py'),
 ('Preserve r5 while r6 BUILD/policy is pending.','A96 selects r5 for V007; unfinished r6 bytes are unused and its workflow is stopped.'),
 ('Supported guarded-entry allowlist remains13 sources; third-party runtime workers are separately pinned dependencies, not new public guarded entry points.',
  'The supported guarded-entry allowlist has exactly 15 sources. BUILD_V007.md, PRODUCER_INDEX_V009_CX3V001.json and ALLOWLIST_DRAFT_V006_CX3V001.txt must agree on every absolute path and byte SHA256. The first 13 entries remain unchanged; the two S1 producer successors replace their predecessors. Third-party runtime workers remain separately pinned dependencies.'),
 ('r6 variant waits for BUILD','r5 selected by A96'),
 ('A89 / 0601: root adopts r6 only if its BUILD, bitwise evidence, independent check, identity runs and comparisons all finish by completion of r5 seal inputs. Otherwise seal r5. Preserve both variants when r6 BUILD is published; no delay to the r5 seal. The prior KHI timing preview is superseded by the measured timing record cited in 0601.',
  'A96 resolves the earlier A89 condition: V007 seals r5. Unfinished r6 sources are unused. The prior KHI timing preview is superseded by the measured timing record cited in 0601; unchanged historical timing fields in the template are UNTESTED and are not updated forecasts. No cache or rotation parallelism saving is adopted by this build.')]:
    assert a in runbook, a
    runbook=runbook.replace(a,b)
runbook+='''
## A85.2–4 operational obligations retained by A99

Before binding or launch, Claude2 verifies the proposed output root `/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007` is still on the internal startup data volume, has sufficient free space, has no unexpected symlink redirection, and uses fresh exclusive output paths. The builder checked only the existing `/Users/bgm/Research` parent: it is on `/System/Volumes/Data`; the proposed `UNT_INTERNAL_RUNS` ancestor was absent. DiskManagement hardware inspection was unavailable. This does not replace the root launch-time filesystem check. No scientific output directory was created. All 51 launch-output fields and the ten corresponding manifest case references use the internal root. The historical C5H reference is preserved as an opaque string; this build never accesses it. Root chooses the internal output location before RI25 plan binding and seal publication. Output location is not a scientific result.

The sealed T-runs and their launcher/monitor/scientific process tree run at normal QoS. Do not place that tree under taskpolicy -b or a background nice policy. From the step-2 launch onward, every lane's non-critical probes, fixtures, reviews and concurrently running post-seal gate-writer work use taskpolicy -b. This is a QoS rule, not a process cap. A95 permits sandbox lane work to continue at default priority when taskpolicy is refused, with the refusal disclosed and no escalation wait; it does not withdraw A85.2 as Claude2's operational launch obligation. Existing A88 saved-replay instructions remain non-critical/background work.

Claude2 starts `caffeinate -i -w <pid>` against the actual long-lived launcher's PID and keeps that assertion for the entire step-2 execution, in addition to the app's assertion. Bind to the launcher, not an intermediate shell or one case monitor. Record the launcher PID, assertion process and operational checks in the root launch record.

Before any producer runs, root checks that admission producer_allowlist is exactly the final 15 path/SHA pairs in BUILD_V007.md and its allowlist/index successors: no missing, extra, or replaced predecessor entry. The finite-float producer successors reject numeric overflow such as 1e309 and finish serialization before exclusive output creation. See the new BUILD's synthetic evidence; scientific output remains UNTESTED.

This runbook names BUILD_V007.md without pinning its bytes to avoid a BUILD/runbook hash cycle; BUILD pins this runbook. P128/LAUNCH_PLAN_V011_CX3V001.json, CASES_MANIFEST_TEMPLATE_V011_CX3V001.json and LAUNCH_COMMAND_V011_CX3V001.txt are pending templates, not a bound launch authorization. No binder, launcher, scientific stage, config, seal or receipt was executed or created by this work.
'''
runbook+='\nOperational authority was read once into the immutable evidence snapshot '+str(snapshot)+' (SHA256 '+sha(snapshot)+'). This snapshot is review evidence, not the root frozen addendum. Its custody record names the live source and read time; no ongoing equality of a mutable addendum is required.\n'
fmt=(P/'ROOT_SEAL_ADMISSION_FORMAT_V004.md').read_text()
fmt=fmt.replace('# Root seal publication format — 0561','# Root seal publication format — A99 BUILD_V007\n\ndate -u: '+date)
fmt=fmt.replace('producer_allowlist mapping the 13 supported runtime source absolute paths to full byte hashes. Build pins BUILD_V005.md.',
 'producer_allowlist mapping exactly the 15 supported runtime source absolute paths to full byte hashes. Build pins BUILD_V007.md. Its path/SHA mapping must equal ALLOWLIST_DRAFT_V006_CX3V001.txt and PRODUCER_INDEX_V009_CX3V001.json exactly, with no extra or missing entry. The two S1 producer successors replace their predecessors; the first 13 entries are unchanged.')
fmt+='''

A99 / A85 operational prerequisites: follow RUNBOOK_V008_CX3V001.md, including normal-QoS sealed T-runs, taskpolicy -b for every lane's non-critical concurrent work from step 2 onward, the disclosed A95 sandbox refusal waiver for lane work, and caffeinate -i -w tied to the actual launcher PID for all step 2. Choose and verify the internal SSD output root before RI25 plan binding; do not use External1 for the new T outputs. The r5 P128/LAUNCH_PLAN_V011_CX3V001.json is the selected pending template under A96. It is not a bound plan or authorization to launch. Root must pin the selected r5 driver and the root-created frozen addendum, and publish the separate receipt/config/seal hashes before execution.

BUILD_V007.md pins the final docs and the two supported S1 successors postseal_records_cx1v006_cx3v001.py and srb_rot_record_cx1v008_cx3v001.py. Do not admit the historical predecessors in addition. This document creates no config, seal, receipt, output directory or launch. Production remains UNTESTED.
'''
outputs={
 'RUNBOOK_V008_CX3V001.md':runbook,
 'ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md':fmt,
 'P128/LAUNCH_PLAN_V011_CX3V001.json':jbytes(plan),
 'P128/CASES_MANIFEST_TEMPLATE_V011_CX3V001.json':jbytes(manifest),
 'P128/LAUNCH_COMMAND_V011_CX3V001.txt':command,
}
assert all(not os.path.lexists(P/n) for n in outputs)
for n,b in outputs.items(): write(P/n,b)
for n,h in EXPECTED.items(): assert sha(P/n)==h,n
evidence={'date_u':date,'status':'BUILT_REQUIRES_INDEPENDENT_STATIC_CHECK','input_pins':[{'path':str(P/n),'sha256':h} for n,h in EXPECTED.items()],
 'output_pins':[{'path':str(P/n),'sha256':sha(P/n)} for n in outputs],'builder':{'path':str(Path(__file__)),'sha256':sha(__file__)},
 'filesystem_evidence':{'path':str(E/'FILESYSTEM_EVIDENCE_CX3V001.json'),'sha256':sha(E/'FILESYSTEM_EVIDENCE_CX3V001.json')},
 'operational_snapshot':snapshotpin,'authorized_plan_changes':changes,'plan_change_count':len(changes),
 'manifest_case_changes':10,'historical_C5H_preserved_as_string_only':True,'scientific_executions':0,'new_output_root':NEWROOT}
write(E/'BUILD_DOCS_PLANS_CX3V001.json',jbytes(evidence))
print(json.dumps(evidence['output_pins'],indent=2))
