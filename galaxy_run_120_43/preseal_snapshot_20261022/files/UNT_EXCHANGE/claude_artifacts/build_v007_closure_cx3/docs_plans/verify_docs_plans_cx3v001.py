from pathlib import Path
import hashlib,json,os,resource,subprocess
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1')
E=Path(__file__).parent
N='/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007/'
checks=[]
def check(name,condition):
    checks.append({'name':name,'pass':bool(condition)})
    if not condition: raise AssertionError(name)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads(Path(p).read_bytes())
def differences(a,b,path=()):
    if type(a)!=type(b):return [path]
    if isinstance(a,dict):
        if a.keys()!=b.keys():return [path]
        return [x for k in a for x in differences(a[k],b[k],path+(k,))]
    if isinstance(a,list):
        if len(a)!=len(b):return [path]
        return [x for i,(u,v) in enumerate(zip(a,b)) for x in differences(u,v,path+(i,))]
    return [] if a==b else [path]
def get(o,path):
    for k in path:o=o[k]
    return o
build=j(E/'BUILD_DOCS_PLANS_CX3V001.json')
for pin in build['input_pins']+build['output_pins']:
    check('Byte pin '+pin['path'],h(pin['path'])==pin['sha256'])
a=j(P/'P128/LAUNCH_PLAN_V010.json');b=j(P/'P128/LAUNCH_PLAN_V011_CX3V001.json')
expected={('launcher_log',)}
for i in range(10):
    expected.update({('calls',i,k) for k in ('outdir','receipt','monitor_log')})
    expected.update({('calls',i,'monitor_argv',11),('calls',i,'monitor_argv',13)})
diff=differences(a,b)
check('Exactly 51 authorized plan JSON paths differ',len(diff)==51 and set(diff)==expected)
locations=[]
for path in diff:
    old,new=get(a,path),get(b,path)
    check('Output path mapping '+str(path),new.startswith(N) and new[len(N):]==old.rsplit('/',1)[1].replace('_V010','_V011_CX3V001'))
    locations.append(new)
check('31 unique launch output locations',len(set(locations))==31)
check('R5 driver selected',b['driver']==a['driver'] and b['driver']['sha256']=='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
check('Exact ten-case order',b['order']==['C4T-KHI','C6T','C4T-D5','C4T','S4T','C4T-A','C3T','C2T','C4T-KLO','C4T-C5c'])
for i,c in enumerate(b['calls']):
    check('Monitor outdir equals call '+str(i),c['monitor_argv'][10:12]==['--outdir',c['outdir']])
    check('Monitor receipt equals call '+str(i),c['monitor_argv'][12:14]==['--receipt',c['receipt']])
    check('Scientific spec bytes '+str(i),h(c['spec']['path'])==c['spec']['sha256'])
    old=a['calls'][i]
    check('Unchanged scientific call fields '+str(i),all(v==old[k] for k,v in c.items() if k not in ('outdir','receipt','monitor_log','monitor_argv')))
check('Ramp admission controls unchanged',b['route_a_admission']==a['route_a_admission'])
check('All other plan metadata unchanged',all(b[k]==v for k,v in a.items() if k not in ('calls','launcher_log')))
ma=j(P/'P128/CASES_MANIFEST_TEMPLATE_V010.json');mb=j(P/'P128/CASES_MANIFEST_TEMPLATE_V011_CX3V001.json')
check('Exactly ten case refs change',set(differences(ma,mb))=={('cases',c['case']) for c in b['calls']})
check('C5H opaque string unchanged',ma['cases']['C5H']==mb['cases']['C5H'])
check('Case refs bind new output dirs',all(mb['cases'][c['case']]==c['outdir'] for c in b['calls']))
ca=(P/'P128/LAUNCH_COMMAND_V010.txt').read_bytes();cb=(P/'P128/LAUNCH_COMMAND_V011_CX3V001.txt').read_bytes()
check('Command differs only in template filename',cb==ca.replace(b'P128/LAUNCH_PLAN_V010.json',b'P128/LAUNCH_PLAN_V011_CX3V001.json'))
check('Command retains pending state',cb.startswith(b'# PENDING TEMPLATE:'))
rb=(P/'RUNBOOK_V008_CX3V001.md').read_text();fmt=(P/'ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md').read_text()
for term in ('normal QoS','taskpolicy -b','step-2 launch onward','not a process cap','A95','sandbox','default priority','caffeinate -i -w <pid>','actual long-lived launcher','entire step-2','internal startup data volume','BUILD_V007.md','exactly 15 sources','ALLOWLIST_DRAFT_V006_CX3V001.txt','PRODUCER_INDEX_V009_CX3V001','A96','r5','UNTESTED'):
    check('Runbook operational text '+term,term in rb)
for term in ('exactly the 15','BUILD_V007.md','RUNBOOK_V008_CX3V001.md','caffeinate -i -w','A95','A96','ALLOWLIST_DRAFT_V006_CX3V001.txt','PRODUCER_INDEX_V009_CX3V001.json'):
    check('Format operational text '+term,term in fmt)
check('No stale 13-source statement','remains13 sources' not in rb and 'mapping the 13 supported' not in fmt)
check('No stale BUILD references','BUILD_V005' not in fmt and 'BUILD_V006' not in rb+fmt)
snap=j(E/'ROOT_DECISIONS_SNAPSHOT_CUSTODY_CX3V001.json')
check('Immutable authority snapshot byte pin',h(snap['path'])==snap['sha256'] and snap['sha256']==snap['source_sha256_at_read'])
check('Snapshot explicitly not root frozen addendum',snap['not_a_root_frozen_addendum'] is True)
check('Runbook pins snapshot',snap['path'] in rb and snap['sha256'] in rb)
st=Path(snap['path']).read_text()
for term in ('## A85:','## A95:','## A96:','## A99:'):
    check('Authority snapshot includes '+term,term in st)
idx=j(P/'PRODUCER_INDEX_V009_CX3V001.json');oldidx=j(P/'PRODUCER_INDEX_V008.json')
check('Index published pin',h(P/'PRODUCER_INDEX_V009_CX3V001.json')=='7a61747efeee8ff27e8e5b3c2213a0aa2f3e8ed888e871ac1df193a6a64b6a97')
check('Allowlist published pin',h(P/'ALLOWLIST_DRAFT_V006_CX3V001.txt')=='18300b52fdef500defacae06e4b98564534cd37661874ae7e2aa92d5c9f5fc47')
allow=[{'path':s.split('  ',1)[1],'sha256':s.split('  ',1)[0]} for s in (P/'ALLOWLIST_DRAFT_V006_CX3V001.txt').read_text().splitlines() if s.strip()]
check('Allowlist exactly same 15 supported entries',len(allow)==15 and allow==idx['supported_entries'])
check('First 13 supported entries unchanged',idx['supported_entries'][:13]==oldidx['supported_entries'][:13])
check('Two historical producers replaced',all(idx['supported_entries'][i]['path']!=oldidx['supported_entries'][i]['path'] for i in (13,14)))
for pin in allow:check('Supported source byte verification '+pin['path'],h(pin['path'])==pin['sha256'])
check('No scientific output root or ancestor created',not os.path.lexists('/Users/bgm/Research/UNT_INTERNAL_RUNS'))
fs=j(E/'FILESYSTEM_EVIDENCE_CX3V001.json')
check('Startup data-volume parent verified',fs['parent_st_dev']==fs['startup_data_st_dev'] and '/System/Volumes/Data' in fs['df'])
check('Hardware inspection limit disclosed','UNTESTED' in fs['hardware_inspection'])
for pin in build['input_pins']:check('Original inputs still unchanged '+pin['path'],h(pin['path'])==pin['sha256'])
out={'date_u':subprocess.check_output(['date','-u'],text=True).strip(),'status':'TESTED_PASS','checks':checks,'passed':len(checks),'failed':0,
     'scope':'JSON/tree and byte identity plus static operational wording; no binder, launcher, monitor, scientific stage, root config/seal/receipt or protected-path access.',
     'plan_differences':[list(p) for p in diff],'unique_output_locations':31,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'rss_limit_evidence':'Observed process RSS only, not a hard address-space cap.',
     'runbook_and_format_links_to_final_BUILD':'By filename only; final BUILD author owns reverse byte pins and adoption.'}
with (E/'VERIFICATION_CX3V001.json').open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'passed':len(checks),'failed':0,'sha256':h(E/'VERIFICATION_CX3V001.json'),'peak_rss_bytes':out['peak_rss_bytes']}))
