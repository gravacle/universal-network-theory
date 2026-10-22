"""Independent source/leaf/token audit and synthetic comparator canaries; no science launch."""
from pathlib import Path
import ast, contextlib, copy, hashlib, importlib.util, io, json, os, resource, subprocess, sys
import numpy as np

EX=Path('/Users/bgm/Research/UNT_EXCHANGE')
ART=EX/'claude_artifacts'
G=ART/'tail_scheme_impl_c2/gates_v003'
V=ART/'v007_identity_gates_c2'
OUT=ART/'review_certs_gates_cx3/identity_specs_v002'
DATE=subprocess.check_output(['date','-u'],text=True).strip()
OUT.mkdir(parents=True,exist_ok=False)
PINS={}

def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.remove','os.rename','os.rmdir','socket.connect','socket.getaddrinfo'):
        raise RuntimeError('review audit denied '+event)
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])); s=str(p.resolve()).casefold()
        if 'kmax_a2f10_c5h_run_v001' in s or '/runs_ext/uvt_' in s or '/.codex/' in s or '/.codex-alt/sessions/' in s:
            raise RuntimeError('forbidden read '+str(p))
        flags=args[2]
        if isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR):
            if not p.resolve().is_relative_to(OUT) or p.exists():raise RuntimeError('nonexclusive write '+str(p))
sys.addaudithook(audit)

def pin(p):
    p=Path(p); raw=p.read_bytes(); h=hashlib.sha256(raw).hexdigest()
    PINS[str(p)]={'path':str(p),'sha256':h,'bytes':len(raw)}
    return h
def read(p):
    pin(p); return json.loads(Path(p).read_text())
def write(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(o,f,indent=2,allow_nan=False)
def module(p,name):
    pin(p); m=importlib.util.module_from_spec(importlib.util.spec_from_file_location(name,p))
    sys.modules[name]=m; m.__spec__.loader.exec_module(m);return m

C=module(G/'run_identity_compare_c2v003.py','cx3_review_cmp')
assert pin(G/'run_identity_compare_c2v003.py').startswith('8f14f466')
D=module(Path(C.DRIVER[0]),'cx3_review_driver')
assert pin(Path(C.DRIVER[0]))==C.DRIVER[1]
CM=C.load_cm();pin(C.CKPT[0])
TOLD=read(G/'tokens/TOKENS_Z2_C2V003.json')
TNEW=read(V/'z2_v002/TOKENS_Z2_C2V004.json')
EMPTY=OUT/'TOKENS_EMPTY.json';write(EMPTY,{'declared':[]})

# Derive the expected extra pairs ourselves from the driver's two literal pin tables.
old=TOLD['declared']; new=TNEW['declared']; expected=[]; table=[]
for kind,(up,us) in D.SCRIPTS_UVT.items():
    bp,bs=D.SCRIPTS[kind]
    assert pin(up)==us and pin(bp)==bs
    assert ('successor of %s (sha256 %s)'%(Path(bp).name,bs)) in Path(up).read_text()
    for field,b,u in [('path',str(bp),str(up)),('sha256',bs,us)]:
        hits=[x for x in old if x[1]==b and x[2].startswith('<GEO_PIN_')]
        assert len(hits)==1
        row=[hits[0][0],u,hits[0][2]];expected.append(row)
        table.append({'kind':kind,'field':field,'base':b,'successor':u,'reference':row[0],'token':row[2]})
    rp=[x for x in expected if x[1]==str(up)][0][0]
    rs=[x for x in expected if x[1]==us][0][0]
    assert pin(rp)==rs
token_checks={'old_prefix_unchanged':new[:len(old)]==old,
              'exact_declared_driver_successors':sorted(new[len(old):])==sorted(expected),
              'added_pairs':len(expected),'stage_kinds':len(D.SCRIPTS_UVT)}
assert token_checks['old_prefix_unchanged'] and token_checks['exact_declared_driver_successors']

# Type-sensitive recursive leaf comparisons, independent of the provided leafdiff tool.
def leaves(o,p=''):
    if isinstance(o,dict) and o:
        return {k:v for key,value in o.items() for k,v in leaves(value,p+'/'+key).items()}
    if isinstance(o,list) and o:
        return {k:v for i,value in enumerate(o) for k,v in leaves(value,p+'/'+str(i)).items()}
    return {p:(type(o).__name__,o)}
def differences(a,b):
    aa,bb=leaves(a),leaves(b)
    return {k:{'base':aa.get(k),'member':bb.get(k)} for k in sorted(aa.keys()|bb.keys()) if aa.get(k)!=bb.get(k)}
BASES={'C5H':ART/'c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json',
       'D5':ART/'tail_scheme_impl_c2/driver_r4/specs/CALL_KMAX_TAIL_C4T_D5_A2F10_HULL_N8_M32_C2V010R4.TEMPLATE.json'}
bases={k:read(p) for k,p in BASES.items()}
registry=read(G/'specs/SPECS_RPAIR_T2_C5H_D5_C2V001.json');members=[]
for item in registry['specs']:
    p=Path(item['file']);o=read(p);assert pin(p)==item['sha256']
    who='C5H' if 'C5H@' in item['role'] else 'D5';br=item['derived_from']['branch']
    diff=differences(bases[who],o)
    preA53={'/label'}|({'/numerics/route_a/seed_source_rtol_factor'} if br=='ROUTE_A' else {'/numerics/picard/passes','/numerics/picard/speed_change_bound_km_s'})|({'/numerics/route_a/ro1_workers'} if who=='C5H' else set())
    ra=o['numerics']['route_a']
    a53=(ra.get('seed_source_rtol_factor')==.1 and (who!='C5H' or ra.get('ro1_workers') is True)) if br=='ROUTE_A' else (ra.get('column_workers')==1 and 'ro1_workers' not in ra and 'admit' in ra)
    members.append({'path':str(p),'sha256':pin(p),'who':who,'branch':br,'leaf_diff':diff,
                    'matches_old_A52_declared_leaves':set(diff)==preA53,'A53_branch_contract':a53,
                    'route_a':ra})
ROOT=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
pin(ROOT);rt=ROOT.read_text();excerpt=rt[rt.index('## A53:'):rt.index('**Other items:**',rt.index('## A53:'))]
with (OUT/'A53_READ_SNAPSHOT.txt').open('x') as f:f.write(excerpt)

def inv_new(v):
    hits=[x[0] for x in old if x[1]==str(v)]
    assert hits,(v,'no token inverse')
    return hits[0]
def fixture(path,gate,side,mutation=''):
    path=path.resolve(); path.mkdir(parents=True)
    isnew=side=='NEW'; armed=gate=='Z2'
    value=1.0
    res={'status':'COMPLETED','valid':True,'final_pass':1,'speeds_km_s':[value],
         'rows':[{'id':'SYN01','speed_km_s':value}],
         'passes':[{'pass':1,'rows':[{'id':'SYN01','speed_km_s':value}],'max_abs_change_km_s':0.0}]}
    w=D.RO1_ROUTE_A['worker_parallel'];bind=D.RO1_ROUTE_A['binding'];fac=D.AUX_UVT['facade']
    res['route_a_outcome']={'classification':'CONVERGED','ro1':{'rule':'RO1','armed':armed,'fired':False,'events':[],
          'worker_sha256':w[1] if armed else None,'binding_sha256':bind[1] if armed else None}}
    if isnew and mutation=='result_ulp':res['speeds_km_s'][0]=float(np.nextafter(1.,2.))
    if isnew and mutation=='valid_int':res['valid']=1
    if isnew and mutation=='result_signed_zero':res['passes'][0]['max_abs_change_km_s']=-0.0
    if isnew and mutation=='result_bool_speed':res['speeds_km_s'][0]=True
    write(path/'start.json',{'driver':'/SYNTHETIC/driver.py','driver_sha256':'a'*64})
    write(path/'result.json',res)
    stage=path/'stages/02_reference'; script='/SYNTHETIC/reference.py';sha='b'*64
    if isnew and mutation=='arbitrary_script':script='/SYNTHETIC/undeclared_successor.py';sha='c'*64
    argv=['--tolerance','0.01']
    if isnew and mutation=='request_numeric':argv=['--tolerance','0.99']
    write(stage/'request.json',{'script':script,'script_sha256':sha,'argv':argv})
    finish={'status':'COMPLETED','metric':2.,'worker_sha256':sha,'nested':{'probe':3.}}
    if isnew and mutation=='json_ulp':finish['metric']=float(np.nextafter(2.,3.))
    if isnew and mutation=='stray_tail':finish['uv_tail']={'enabled':False}
    write(stage/'reference/finish.json',finish)
    if not(isnew and mutation=='missing_npz'):
        a=np.array([0.,2.,3.])
        if isnew and mutation=='npz_ulp':a[1]=np.nextafter(a[1],3.)
        if isnew and mutation=='npz_signed_zero':a[0]=-0.
        if isnew and mutation=='npz_dtype':a=a.astype(np.float32)
        with (stage/'reference/arrays.npz').open('xb') as f:np.savez(f,physical=a)
    if mutation=='npy_numeric':
        with (stage/'reference/field.npy').open('xb') as f:np.save(f,np.array([2. if isnew else 1.]),allow_pickle=False)
    if isnew and mutation=='extra_npz':
        with (stage/'reference/new_physical.npz').open('xb') as f:np.savez(f,physical=np.array([999.]))
    if isnew and mutation=='extra_json':write(stage/'reference/new_physical.json',{'metric':999.})
    if not armed:return
    ra=path/'stages/01_route_a'; usew=(str(w[0]),w[1]) if isnew else (str(ART/'parallel_route_a_c2/ddo_composite_stable_cached_root_worker_v002_parallel_c2v001.py'),'9dbdaf11eb80fd4fa8d47e8c0827eae51d06e87f05efdd6e5c11d422ecbd197a')
    pins={str(bind[0]):bind[1],str(fac[0]):fac[1]} if isnew else {inv_new(bind[0]):inv_new(bind[1]),inv_new(fac[0]):inv_new(fac[1])}
    write(ra/'request.json',{'script':usew[0],'script_sha256':usew[1],'argv':['--column-workers','8']})
    write(ra/'attempt_000/start.json',{'worker_pin':usew[1],'input_pins':pins})
    (ra/'attempt_000/arrays').mkdir()
    with (ra/'attempt_000/arrays/000000_gas.npz').open('xb') as f:np.savez(f,gas=np.array([1.,2.]))
    (ra/'checkpoint/blobs').mkdir(parents=True)
    with (ra/'checkpoint/blobs/0000.npy').open('xb') as f:f.write(b'SYNTHETIC_BLOB_BYTES')
    write(ra/'checkpoint/iteration_0000/COMPLETED.json',{'iteration':0,'residual':1e-9})
    caller={'code_pins':pins,'physical_parameters':{'gamma':2.9e42},'numerical_controls':{'source_rtol':.01}}
    body={'format':CM.FORMAT,'kind':'identity','identity':{'caller':{'sha256':CM.digest(caller),'record':CM.encode(caller)}},'identity_sha256':'7'*64}
    body['payload_sha256']=CM._sha(CM._canonical(body))
    with (ra/'checkpoint/IDENTITY.json').open('xb') as f:f.write(CM._canonical(body)+b'\n')

mutations=['','result_ulp','json_ulp','npz_ulp','npz_signed_zero','npz_dtype','missing_npz','stray_tail',
           'extra_npz','extra_json','npy_numeric','request_numeric','arbitrary_script','valid_int','result_bool_speed','result_signed_zero']
canaries=[]
for gate in ['B0P_RERUN','Z2']:
    for i,mut in enumerate(mutations):
        p=OUT/('CANARY_%s_%02d_%s'%(gate,i,mut or 'baseline'))
        fixture(p/'REF',gate,'REF',mut);fixture(p/'NEW',gate,'NEW',mut)
        report=p/'REPORT.json';t=V/'z2_v002/TOKENS_Z2_C2V004.json' if gate=='Z2' else EMPTY
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                code=C.main(['--gate',gate,'--reference',str(p/'REF'),'--new',str(p/'NEW'),'--tokens',str(t),'--out',str(report)])
            rr=json.loads(report.read_text())
            canaries.append({'gate':gate,'mutation':mut or 'baseline','exit_code':code,'verdict':rr['verdict'],'failing':rr['failing'],'report':{'path':str(report),'sha256':pin(report)}})
        except Exception as e:canaries.append({'gate':gate,'mutation':mut or 'baseline','exception':repr(e)})
    assert canaries[-len(mutations)]['verdict']=='PASS_BITWISE_EQUAL',canaries[-len(mutations)]

record_reports=[]
for p in [V/'IDENTITY_Z2_OFF_RO1_V001.json',V/'IDENTITY_B0P_RERUN_V001.json',V/'IDENTITY_Z2_V001.json',G/'out/B0_C5H_RPAIR_V003/B0_C5H_RPAIR_C2V001.json']:
    rr=read(p);record_reports.append({'path':str(p),'sha256':pin(p),'reported_verdict':rr.get('verdict'),'scope':'Report bytes only; original UVT run bytes forbidden and unopened'})
out={'date_u':DATE,'scope':'Independent source tables, leaf diffs and own synthetic comparator canaries only; no real run opened',
     'token_checks':token_checks,'token_derivation':table,'members':members,'canaries':canaries,'reports_read':record_reports,
     'inputs':list(PINS.values()),'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
write(OUT/'REVIEW_RESULTS_V001.json',out)
print(json.dumps({'output':str(OUT/'REVIEW_RESULTS_V001.json'),'sha256':pin(OUT/'REVIEW_RESULTS_V001.json'),'token_checks':token_checks,
                  'A53_members':[(m['who'],m['branch'],m['A53_branch_contract']) for m in members],
                  'canaries':[(c['gate'],c['mutation'],c.get('verdict',c.get('exception'))) for c in canaries]}))
