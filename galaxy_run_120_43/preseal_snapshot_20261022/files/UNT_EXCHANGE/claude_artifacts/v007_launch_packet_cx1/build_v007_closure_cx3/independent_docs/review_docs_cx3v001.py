"""Independent A99 S2/S3 metadata checks. No imports/execution of producers,
binder, launcher or scientific code. Embedded run/output paths stay strings.
"""
from pathlib import Path,PurePosixPath
import ast, hashlib,json,os,resource,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
EX=Path('/Users/bgm/Research/UNT_EXCHANGE')
DOC=EX/'claude_artifacts/build_v007_closure_cx3/docs_plans'
ROOT='/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007/'
date_u=subprocess.check_output(['date','-u'],text=True).strip()
checks=[];readpins={};denials=[]
def forbidden(p):
    s=str(p).casefold()
    return ('kmax_a2f10_c5h_run_v001' in s or '/runs_ext/uvt_' in s or '/.codex/' in s or '/.codex-alt/' in s or '/unt_internal_runs/' in s)
def audit(event,args):
    if event in ('subprocess.Popen','os.system','socket.__new__','socket.connect'):
        denials.append(event);raise PermissionError('NO_EXECUTION')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0]));s=str(p.absolute())
        if forbidden(s):denials.append(s);raise PermissionError('NO_EMBEDDED_RUN_IO')
        flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
            if not s.startswith(str(HERE)+'/') or not flags&os.O_EXCL:raise PermissionError('EXCLUSIVE_REVIEW_OUTPUT_ONLY')
sys.addaudithook(audit)
def read(p):
    # Embedded scientific/output paths never pass here. Callers provide only
    # explicit metadata/source inputs, with lexical restrictions before I/O.
    assert not forbidden(p),str(p)
    raw=p.read_bytes();readpins[str(p)]={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()};return raw
def load(p):return json.loads(read(p))
def ck(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
def leaves(x,p=()):
    if isinstance(x,dict):
        for k,v in x.items():yield from leaves(v,p+(k,))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from leaves(v,p+(i,))
    else:yield p,x
def compare(a,b):
    aa=dict(leaves(a));bb=dict(leaves(b));assert aa.keys()==bb.keys()
    return [(p,aa[p],bb[p]) for p in aa if type(aa[p]) is not type(bb[p]) or aa[p]!=bb[p]]

old=load(BASE/'P128/LAUNCH_PLAN_V010.json');new=load(BASE/'P128/LAUNCH_PLAN_V011_CX3V001.json')
delta=compare(old,new)
expected={('launcher_log',)}
for i in range(10):
    expected|={('calls',i,k) for k in ('outdir','receipt','monitor_log')}
    for option in ('--outdir','--receipt'):
        at=old['calls'][i]['monitor_argv'].index(option)+1
        expected.add(('calls',i,'monitor_argv',at))
ck('exact_51_field_locations',{p for p,_,_ in delta}==expected and len(delta)==51)
ck('exact_31_distinct_output_locations',len({a for _,a,_ in delta})==len({b for _,_,b in delta})==31)
ck('all_output_changes_are_strings',all(type(a) is type(b) is str for _,a,b in delta))
ck('all_new_outputs_internal_lexical',all(b.startswith(ROOT) and '..' not in PurePosixPath(b).parts for _,_,b in delta))
ck('no_external1_new_plan_field',not any(isinstance(v,str) and '/Volumes/External1' in v for _,v in leaves(new)))
ck('fresh_versioned_output_names',all('V011_CX3V001' in b and b!=a for _,a,b in delta))
ck('every_other_plan_leaf_exact',all(p in expected for p,_,_ in delta))
for k in old:
    if k not in ('calls','launcher_log'):ck('top_level_unchanged_'+k,old[k]==new[k])
ck('ten_calls_exact_order',len(new['calls'])==10 and [c['case'] for c in new['calls']]==new['order']==old['order'])
ck('r5_exact_driver_pin',new['driver']==old['driver'] and new['driver']['sha256']=='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
ck('ramp_caps_exact',new['route_a_admission']=={'max_active':6,'minimum_free_percent':25,'poll_seconds':60,'source':'/usr/bin/memory_pressure','ramp':'previous_first_completed_route_a_iteration','first_case_exception':'C4T-KHI'})
for i,(a,b) in enumerate(zip(old['calls'],new['calls'])):
    label=b['case']
    ck(label+'_non_output_fields_exact',all(a[k]==b[k] for k in a if k not in ('outdir','receipt','monitor_log','monitor_argv')))
    av=list(a['monitor_argv']);bv=list(b['monitor_argv'])
    for opt in ('--outdir','--receipt'):
        at=av.index(opt)+1;av[at]=bv[at]
    ck(label+'_argv_only_two_output_changes',av==bv)
    ck(label+'_argv_output_consistency',b['monitor_argv'][b['monitor_argv'].index('--outdir')+1]==b['outdir'] and b['monitor_argv'][b['monitor_argv'].index('--receipt')+1]==b['receipt'])
    ck(label+'_normal_qos_command',not any(x in ('taskpolicy','-b','nice','-n') for x in b['monitor_argv']))
    p=Path(b['spec']['path']);assert p.parent==BASE/'P128/specs' and p.name.endswith('.FILLED.json')
    raw=read(p);ck(label+'_unchanged_spec_byte_pin',hashlib.sha256(raw).hexdigest()==a['spec']['sha256']==b['spec']['sha256'])

om=load(BASE/'P128/CASES_MANIFEST_TEMPLATE_V010.json');nm=load(BASE/'P128/CASES_MANIFEST_TEMPLATE_V011_CX3V001.json')
mdelta=compare(om,nm)
ck('case_manifest_exact_ten_changes',len(mdelta)==10 and {p for p,_,_ in mdelta}=={('cases',c) for c in new['order']})
ck('ten_case_refs_match_plan',all(nm['cases'][c['case']]==c['outdir'] for c in new['calls']))
# No Path(), stat(), resolve(), open() or guard call on the legacy reference.
ck('legacy_C5H_opaque_string_exact',type(nm['cases']['C5H']) is str and nm['cases']['C5H']==om['cases']['C5H'])
ck('only_legacy_case_reference_external',[(p,v) for p,v in leaves(nm) if isinstance(v,str) and '/Volumes/External1' in v]==[(('cases','C5H'),om['cases']['C5H'])])
oc=read(BASE/'P128/LAUNCH_COMMAND_V010.txt').decode();nc=read(BASE/'P128/LAUNCH_COMMAND_V011_CX3V001.txt').decode()
ck('command_only_plan_basename_changed',oc.replace('LAUNCH_PLAN_V010.json','LAUNCH_PLAN_V011_CX3V001.json')==nc)
ck('command_pending_not_authorization','PENDING TEMPLATE' in nc and '--execute-root-only' in nc and 'Claude2 only after seal' in nc)

oldallow=read(BASE/'ALLOWLIST_DRAFT_V005.txt').decode().splitlines()
allow=read(BASE/'ALLOWLIST_DRAFT_V006_CX3V001.txt').decode().splitlines()
oi=load(BASE/'PRODUCER_INDEX_V008.json');ni=load(BASE/'PRODUCER_INDEX_V009_CX3V001.json')
rows=[{'path':s.split('  ',1)[1],'sha256':s.split('  ',1)[0]} for s in allow]
ck('exact_15_unique_allowlist',len(rows)==len({x['path'] for x in rows})==15)
ck('first13_allowlist_bytes_unchanged',allow[:13]==oldallow[:13])
ck('first13_index_entries_unchanged',ni['supported_entries'][:13]==oi['supported_entries'][:13])
ck('index_exact_allowlist_order_and_pins',ni['supported_entries']==rows)
expectednames=['postseal_records_cx1v006_cx3v001.py','srb_rot_record_cx1v008_cx3v001.py']
ck('two_successor_entries_only',[PurePosixPath(x['path']).name for x in rows[13:]]==expectednames)
for row in rows:
    p=Path(row['path']);assert p.parent==BASE and p.suffix=='.py'
    raw=read(p);ck('allowlist_bytes_'+p.name,hashlib.sha256(raw).hexdigest()==row['sha256'])
for gate in ('MT','I1T','FLAG_RULINGS'):ck('gate_mapping_'+gate,ni['gate_producers'][gate]==rows[13])
ck('gate_mapping_SRB',ni['gate_producers']['SRB_ROT']==rows[14])
ck('gate_mapping_SRK_unchanged',ni['gate_producers']['SR_K']==oi['gate_producers']['SR_K'])
ck('index_remaining_fields_unchanged',all(ni[k]==oi[k] for k in oi if k not in ('date_u','build','supported_entries','gate_producers')))
ck('index_BUILD_V007',ni['build']=='BUILD_V007.md')
guard=read(BASE/'producer_guard_cx1v008.py').decode()
ck('shared_guard_config_same_directory',"HERE=Path(__file__).resolve().parent" in guard and "CONFIG=HERE/'ROOT_SEAL_ADMISSION_V001.json'" in guard)
for name in expectednames:
    text=read(BASE/name).decode();ck(name+'_shared_guard_import','import producer_guard_cx1v008 as G' in text and 'G.admission(__file__)' in text)
ck('srb_reconstruction_relative_path_unchanged',"RECON=Path(__file__).parent.parent/'calib_tail_readiness_cx2/certificates_per_point/reconstruction_cx2v003.py'" in read(BASE/expectednames[1]).decode())

runbook=read(BASE/'RUNBOOK_V008_CX3V001.md').decode();fmt=read(BASE/'ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md').decode()
read(BASE/'RUNBOOK_V007.md');read(BASE/'ROOT_SEAL_ADMISSION_FORMAT_V004.md')
snapshot=read(DOC/'ROOT_DECISIONS_V005_READ_SNAPSHOT_CX3V001.md').decode()
custody=load(DOC/'ROOT_DECISIONS_SNAPSHOT_CUSTODY_CX3V001.json')
fs=load(DOC/'FILESYSTEM_EVIDENCE_CX3V001.json')
read(EX/'FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md')
read(EX/'FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md')
for name,needles in {
 'A85_normal_qos':('normal QoS','Do not place that tree under taskpolicy -b'),
 'A85_noncritical_from_step2':("From the step-2 launch onward",'non-critical probes, fixtures, reviews','taskpolicy -b'),
 'A95_lane_waiver':('A95 permits sandbox lane work','default priority','no escalation wait','does not withdraw A85.2'),
 'A85_internal_root':(ROOT.rstrip('/'),'internal startup data volume','no unexpected symlink redirection','before RI25 plan binding'),
 'A85_sleep_assertion':('caffeinate -i -w <pid>',"actual long-lived launcher's PID",'entire step-2 execution',"in addition to the app's assertion"),
 'A96_r5_no_cache_adoption':('A96 selects r5','unfinished r6 bytes are unused','No cache or rotation parallelism saving is adopted'),
 'S3_exact15':('exactly 15 sources','first 13 entries remain unchanged','two S1 producer successors replace'),
 'physical_verification_not_overclaimed':('DiskManagement hardware inspection was unavailable','does not replace the root launch-time filesystem check','No scientific output directory was created'),
 'pending_and_root_only':('Claude2 is the only scientific launcher','pending templates, not a bound launch authorization','No binder, launcher, scientific stage, config, seal or receipt was executed'),
 'historical_timing_not_new_forecast':('historical timing fields in the template are UNTESTED','not updated forecasts'),
 }.items():ck('runbook_'+name,all(s in runbook for s in needles))
for name,needles in {
 'exact15_admission':('exactly the 15 supported runtime source','no extra or missing entry','first 13 entries are unchanged'),
 'publication_trust':('independently before invoking','Do not derive the trusted expected value from the local config alone'),
 'acyclic_records':('Receipt stays separate: no cyclic seal/config hashes','No actual root config, seal or receipt'),
 'operations':('normal-QoS sealed T-runs','A95 sandbox refusal waiver','caffeinate -i -w','internal SSD output root before RI25 plan binding'),
 'successor_sources':tuple(expectednames),
 }.items():ck('format_'+name,all(s in fmt for s in needles))
ck('snapshot_contains_exact_authority',all(s in snapshot for s in ('## A85:','## A95:','## A96:','## A99:','Step-2 outputs go on the internal SSD','V007 seals on driver v010 r5','preferred, not required')))
ck('snapshot_pin_in_runbook',readpins[str(DOC/'ROOT_DECISIONS_V005_READ_SNAPSHOT_CX3V001.md')]['sha256'] in runbook)
ck('historical_tests_retained_not_reexecuted',all(s in runbook for s in ('admission21/21','launch-control28/28','output/aggregate56/56','binding generator7/7','preseal imports11/11')))
ck('no_audit_denials',not denials)
result={'date_u':date_u,'status':'TESTED_PASS' if all(x['passed'] for x in checks) else 'TESTED_FAIL','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'plan_diff':[{'path':list(p),'before':a,'after':b} for p,a,b in delta],'case_diff':[{'path':list(p),'before':a,'after':b} for p,a,b in mdelta],'read_pins':list(readpins.values()),'harness':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'audit_denials':denials,'rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Static metadata/string and byte-pin checks only. No embedded run/output path metadata or contents accessed. No binder/launcher/science imports or execution. Historical runbook test totals are carried evidence, not rerun.'}
with (HERE/'RESULTS_CX3V001.json').open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:result[k] for k in ('status','passed','total','rss_bytes_macos','audit_denials')}))
print(json.dumps([x for x in checks if not x['passed']]))
assert result['status']=='TESTED_PASS'
