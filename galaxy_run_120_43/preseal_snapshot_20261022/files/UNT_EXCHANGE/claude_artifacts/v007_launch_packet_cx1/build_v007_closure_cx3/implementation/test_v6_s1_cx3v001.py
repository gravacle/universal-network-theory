"""Bounded V6-S1 tests: actual producer mains, synthetic admission/data only.
No scientific reconstruction/library or comparator is executed. Those boundaries
are explicitly stubbed; parser, source record checks and publication are actual.
"""
from pathlib import Path
import ast, builtins, copy, hashlib, importlib.util, io, json, math, os, resource
import subprocess, sys, types
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
OUT=HERE/'run_v001'
OUT.mkdir()
checks=[]; audit_denials=[]; open_writes=[]
START=subprocess.check_output(['date','-u'],text=True).strip()

def forbidden(path):
    s=str(path).casefold()
    return ('kmax_a2f10_c5h_run_v001' in s or '/runs_ext/uvt_' in s or
            '/.codex/' in s or '/.codex-alt/' in s or
            ('ngc3198' in s and any(x in s for x in ('observed','target','rotmod','rotation_curve'))))

def audit(event,args):
    if event in ('subprocess.Popen','os.system','socket.__new__','socket.connect'):
        audit_denials.append([event,str(args)[:160]]);raise PermissionError('AUDIT_ACTION')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0]));s=str(p.absolute())
        flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        write=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if forbidden(s) or forbidden(p.resolve()):
            audit_denials.append([event,s]);raise PermissionError('AUDIT_PROTECTED')
        if write:
            if not p.resolve().is_relative_to(OUT) or not flags&os.O_EXCL:
                audit_denials.append([event,s]);raise PermissionError('AUDIT_EXCLUSIVE_OWN_OUTPUT_REQUIRED')
            open_writes.append(s)
sys.addaudithook(audit)

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':digest(p)}
def put(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:f.write(json.dumps(obj,allow_nan=False))
    return pin(p)
def rawput(p,raw):
    with p.open('xb') as f:f.write(raw)
    return pin(p)
def ck(name,fn):
    try:
        detail=fn();passed=detail is not False
        checks.append({'name':name,'passed':passed,'detail':detail})
    except BaseException as e:
        checks.append({'name':name,'passed':False,'error':type(e).__name__+': '+str(e)})
def expect(kind,fn,text=None):
    try:fn()
    except kind as e:
        if text is not None:assert text in str(e),(text,str(e))
        return {'exception':type(e).__name__,'message':str(e)}
    raise AssertionError('Expected '+kind.__name__)
def mod(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);sys.modules[name]=obj;spec.loader.exec_module(obj)
    return obj

sources={'postseal':BASE/'postseal_records_cx1v006_cx3v001.py',
         'srb':BASE/'srb_rot_record_cx1v008_cx3v001.py',
         'guard':BASE/'producer_guard_cx1v008.py'}
expected={'postseal':'4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366',
          'srb':'2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc',
          'guard':'294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731'}
for name,p in sources.items():assert digest(p)==expected[name]
G=mod(sources['guard'],'producer_guard_cx1v008')
assert not G.CONFIG.exists(),'Real root admission unexpectedly exists; stop, do not read it'
for label in ('postseal','srb'):
    ck(label+'_actual_preseal_import_refuses',lambda label=label:expect(PermissionError,lambda:mod(sources[label],'preseal_'+label),'ROOT_SEAL_ADMISSION_PENDING'))

# Synthetic admission lives only in memory. No admission/seal file is created.
G.REGISTERED=()
G.admission=lambda *a,**k:{'_verified_seal':{'driver':{'sha256':'d'*64}}}
G.stamp=lambda o,*a:dict(o,root_admission={'synthetic':True})
C=mod(sources['postseal'],'postseal_records_cx1v006_cx3v001')
S=mod(sources['srb'],'srb_rot_record_cx1v008_cx3v001')

for token in ('1e999','-1e999','1e309','-1e309','1.7976931348623159e308'):
    for scope,template in [('scalar','%s'),('list','[0,%s]'),('nested','{"note":{"deep":[{"x":%s}]}}')]:
        ck('parse_overflow_'+token+'_'+scope,lambda token=token,template=template:expect(ValueError,lambda:C.loads(template%token),'NONFINITE_JSON'))
for token in ('NaN','Infinity','-Infinity'):
    ck('parse_constant_'+token,lambda token=token:expect(ValueError,lambda:C.loads('{"deep":['+token+']}'),'NONFINITE_JSON'))
for raw in ('{"a":1,"a":2}','{"x":[{"a":1,"a":1}]}','{"a":1,"\\u0061":2}'):
    ck('duplicate_'+raw,lambda raw=raw:expect(ValueError,lambda:C.loads(raw),'DUPLICATE_JSON_KEY'))
for raw in ('0','-0.0','1e308','-1e308','5e-324','1e-999','1234567890123456789012345678901234567890','{"note":"1e999","nested":[1,2.5,true,null]}'):
    def clean(raw=raw):
        got=C.loads(raw);want=json.loads(raw)
        assert got==want and type(got) is type(want)
        assert json.dumps(got)==json.dumps(want)
        return True
    ck('clean_parser_'+raw,clean)

# Exact unchanged AST outside the three scoped edits.
for label,oldname,allowed in [('postseal','postseal_records_cx1v006.py',{'loads','main'}),('srb','srb_rot_record_cx1v008.py',{'main'})]:
    old=ast.parse((BASE/oldname).read_text());new=ast.parse(sources[label].read_text())
    olddefs={n.name:ast.dump(n,include_attributes=False) for n in old.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    newdefs={n.name:ast.dump(n,include_attributes=False) for n in new.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    ck(label+'_definition_set_unchanged',lambda olddefs=olddefs,newdefs=newdefs:set(olddefs)==set(newdefs))
    for name in olddefs:
        if name not in allowed:ck(label+'_unchanged_AST_'+name,lambda name=name,olddefs=olddefs,newdefs=newdefs:olddefs[name]==newdefs[name])
    before=(BASE/oldname).read_text();after=sources[label].read_text()
    if label=='postseal':
        after=after.replace(" def finite_float(token):\n  value=float(token)\n  if not math.isfinite(value):raise ValueError('NONFINITE_JSON')\n  return value\n return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad,parse_float=finite_float)"," return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)")
    else:after=after.replace('import postseal_records_cx1v006_cx3v001 as C','import postseal_records_cx1v006 as C')
    after=after.replace(" serialized=json.dumps(G.stamp(rec,__file__),indent=1,allow_nan=False)\n G.check_run_path(out,allow_registered=False)\n with open(out,'x') as f:f.write(serialized)"," G.check_run_path(out,allow_registered=False)\n with open(out,'x') as f:json.dump(G.stamp(rec,__file__),f,indent=1,allow_nan=False)")
    ck(label+'_exact_reverse_patch_bytes',lambda before=before,after=after:before==after)

M=types.SimpleNamespace(rpair_key_ok=lambda k:False)
for gate in ('MT','I1T','FLAG_RULINGS','SRB_ROT'):setattr(M,'g_'+gate,lambda *a:[])
C.comparator=lambda:M
refs={};leaf={'verdict':'PASS','max_rel':1e-14,'n':4096,'rtol':1e-12}
for lab in C.CASES:
    root=OUT/'synthetic'/lab;ra=root/'route_a';sc=ra/'uv_tail_sidecar'
    summary={'iteration':0,'state_digest':'1'*64,'next_state_digest':'2'*64,'converged':True}
    it=put(sc/'iteration_0000.json',{'payload':{'iteration':0,'state_digest':'1'*64,'next_state_digest':'2'*64,'summary':summary,'i1t':leaf,'next_i1t':leaf}})
    u={'schema':'SYNTHETIC_COMPUTED_RA','M_T_accepted':.1,'M_T_threshold':.25,'flags':[],'monitor_status':'M_T_WITHIN_THRESHOLD','outcome':'CONVERGED_FINITE_FIXED_POINT','accepted_iteration':0,'production_admissible':True,'admissibility':'production','iterations':[summary],'config_sha256':'c'*64,'request_sha256':'3'*64,'boundary_state_digest_at_return':'1'*64}
    sf=put(sc/'finish_000.json',{'record':copy.deepcopy(u),'files':{'iteration_0000.json':it['sha256']}})
    u['sidecar']={'directory':str(sc),'finish':sf,'files':{'iteration_0000.json':it['sha256']}}
    arp=put(ra/'result.json',{'result':{'uv_tail':u}})
    st=root/'reference';put(st/'finish.json',{'uv_tail':{'production_admissible':True,'config_sha256':'c'*64,'i1t':leaf,'state_digest':'1'*64}})
    refs[lab]=put(root/'result.json',{'status':'COMPLETED','driver_sha256':'d'*64,'normalized_spec':{'galaxy':'DDO154'},'route_a_outcome':{'result_path':arp['path'],'result_sha256':arp['sha256']},'uv_tail':{'route_a_record':u},'stage_records':[{'name':'reference','kind':'reference','executed':True,'argv':['--outdir',str(st)]}]})
    put(root/'finish.json',{'result_sha256':refs[lab]['sha256']})
manifest={'runs':refs};mp=put(OUT/'manifest.json',manifest)
rule={'flag':'SOURCE_QUADRATURE_MATERIAL','run':'C4T','run_result_sha256':refs['C4T']['sha256'],'evidence':'synthetic','disposition':'CLEARED','reason':'synthetic','root_decision':'synthetic'}
rp=put(OUT/'synthetic_rulings.json',{'schema':'UNT_ROOT_FLAG_RULINGS_REQUEST_CX1V001','authority':G.AUTHORITY,'rulings':[rule]})
flagman=dict(manifest,root_rulings=rp);fp=put(OUT/'flag_manifest.json',flagman)

# SRB fixture: actual main and archive/row/envelope code, explicit synthetic
# reconstruction/library/comparator. No production numerical module imported.
ids=['SYNTH-Q%02d'%i for i in range(1,13)];tau=[1.0]*12
bp=put(OUT/'synthetic_binding.json',{'query_rows':[{'id':k,'radius_m':float(i+1)} for i,k in enumerate(ids)],'physical_inclination_rad':0.5,'released_inclination_rad':0.5})
pr=put(OUT/'synthetic_prereg.json',{'synthetic':True})
M.PIN_ROW_RADII_BINDING=(bp['path'],bp['sha256']);M.PIN_PREREG_V005=(pr['path'],pr['sha256']);M.registered_row_maps=lambda pre:(ids,dict(zip(ids,tau)),{})
eps=put(OUT/'synthetic_eps.json',{'gate':'EPS','verdict':'CERTIFIED','envelope_bound':{'rule':'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS','dominates_actual_every_shell':True,'coverage_max_inverse_kpc':182.0},'shells':[{'lo_inverse_kpc':4.0,'hi_inverse_kpc':182.0,'eps_envelope':0.001}]})
cfg={'sha256':'c'*64,'lambda_scale':1,'source_rule':'continuum_v001','outer':{'K_big_inverse_kpc':128},'eps_certificate':eps}
rot=OUT/'srb_synthetic'/'rotation';rot.mkdir(parents=True)
arrays={'radial_nodes_m':np.array([0.5,24.0]),'rotation_Omega_squared':np.ones((2,2)),'full_fields_complex':np.zeros((2,1,2,10),complex)}
buf=io.BytesIO();np.savez(buf,**arrays);ar=rawput(rot/'rotation_base_arrays.npz',buf.getvalue())
fin=put(rot/'finish.json',{'arrays_path':ar['path'],'arrays_sha256':ar['sha256'],'uv_tail':{'state_digest':'1'*64,'production_admissible':True}})
sp=put(rot.parent/'result.json',{'status':'COMPLETED','driver_sha256':'d'*64,'normalized_spec':{'galaxy':'DDO154','numerics':{'uv_tail':cfg,'truncation':{'shape':'cube'},'composite_grid_spec':{'breaks_inverse_kpc':[-4,4]}}},'passes':[{'rotation':str(rot)}]})
put(rot.parent/'finish.json',{'result_sha256':sp['sha256']})
desc=put(OUT/'synthetic_descriptor.json',{'operation':'rebuild','state_assertion':fin,'state_field_path':['uv_tail','state_digest']})
rr=types.SimpleNamespace(config=cfg,replay_scope='PRODUCTION_P128_MS128',lib=types.SimpleNamespace(normalize_config=lambda x:cfg,srb_rot=lambda *a:{'bound_km_s':[0.001]*12}))
pp=types.SimpleNamespace(state=types.SimpleNamespace(digest='1'*64),input_pins=[desc])
S.reconstruct=lambda ref:(rr,pp)
sm=put(OUT/'srb_manifest.json',{'result':sp,'reconstruction':desc,'EPS':eps})

def invoke(mode,out,manifest_override=None):
    C.SNAPSHOTS.clear()
    if mode=='SRB_ROT':sys.argv=['synthetic_srb',manifest_override or sm['path'],str(out)];S.main()
    else:sys.argv=['synthetic_exporter',mode,manifest_override or (fp['path'] if mode=='FLAG_RULINGS' else mp['path']),str(out)];C.main()

class TracedFile:
    def __init__(self,actual,events):self.actual=actual;self.events=events
    def __enter__(self):self.actual.__enter__();return self
    def __exit__(self,*a):return self.actual.__exit__(*a)
    def write(self,value):self.events.append(['write',len(value)]);return self.actual.write(value)

for mode in ('MT','I1T','FLAG_RULINGS','SRB_ROT'):
    module=S if mode=='SRB_ROT' else C
    def success(mode=mode,module=module):
        out=OUT/(mode+'_clean.json');events=[];stamped=[]
        oldstamp=G.stamp;oldcheck=G.check_run_path
        def stamp(o,p):
            events.append(['stamp']);answer=oldstamp(o,p);stamped.append(answer);return answer
        def check(p,**k):
            if str(p)==str(out):events.append(['path_check'])
            return oldcheck(p,**k)
        def opening(p,mode):events.append(['open',mode]);return TracedFile(builtins.open(p,mode),events)
        G.stamp=stamp;G.check_run_path=check;module.open=opening
        try:invoke(mode,out)
        finally:G.stamp=oldstamp;G.check_run_path=oldcheck;del module.open
        raw=out.read_bytes();expected=json.dumps(stamped[0],indent=1,allow_nan=False).encode()
        assert raw==expected and not raw.endswith(b'\n')
        tail=events[events.index(['stamp']):]
        assert [x[0] for x in tail]==['stamp','path_check','open','write'],tail
        assert tail[2]==['open','x']
        obj=json.loads(raw)
        if mode=='I1T':assert len(obj['builds'])==30
        return {'output':pin(out),'events':tail,'legacy_serialization_bytes_equal':True}
    ck(mode+'_actual_main_clean_bytes_single_write',success)
    for failure in ('stamp_raises','serialize_infinity','serialize_nan','serialize_object','serialize_cycle'):
        def failed(mode=mode,failure=failure):
            out=OUT/(mode+'_'+failure+'.json');old=G.stamp
            def bad(o,p):
                if failure=='stamp_raises':raise PermissionError('SYNTHETIC_STAMP_REFUSAL')
                answer=old(o,p)
                if failure=='serialize_cycle':answer['bad']=answer
                else:answer['bad']={'serialize_infinity':math.inf,'serialize_nan':math.nan,'serialize_object':object()}[failure]
                return answer
            G.stamp=bad
            try:detail=expect((PermissionError,ValueError,TypeError),lambda:invoke(mode,out))
            finally:G.stamp=old
            assert not out.exists(),str(out)
            assert str(out) not in open_writes
            return dict(detail,output_absent=True,output_never_opened=True)
        ck(mode+'_'+failure+'_no_output',failed)
    def exclusive(mode=mode):
        out=OUT/(mode+'_clean.json');before=out.read_bytes()
        detail=expect(FileExistsError,lambda:invoke(mode,out));assert out.read_bytes()==before
        return dict(detail,existing_bytes_unchanged=True)
    ck(mode+'_exclusive_refusal_preserves_bytes',exclusive)
    for sign in ('1e999','-1e999'):
        def overflow(mode=mode,sign=sign):
            original=Path(sm['path'] if mode=='SRB_ROT' else (fp['path'] if mode=='FLAG_RULINGS' else mp['path'])).read_text()
            raw=(original[:-1]+',"unexpected_metadata":{"deep":[{"value":'+sign+'}]}}').encode()
            src=OUT/(mode+'_overflow_'+('negative' if sign.startswith('-') else 'positive')+'.json');rawput(src,raw)
            out=OUT/(src.stem+'_output.json')
            detail=expect(ValueError,lambda:invoke(mode,out,str(src)),'NONFINITE_JSON')
            assert not out.exists() and str(out) not in open_writes
            return dict(detail,output_absent=True)
        ck(mode+'_actual_main_nested_overflow_'+sign,overflow)

old=G.admission
G.admission=lambda *a,**k:(_ for _ in ()).throw(PermissionError('SYNTHETIC_ADMISSION_WITHDRAWN'))
ck('admission_withdrawal_preserved',lambda:expect(PermissionError,lambda:C.loads('{}'),'SYNTHETIC_ADMISSION_WITHDRAWN'))
G.admission=old
for name,p in sources.items():ck(name+'_source_pin_unchanged',lambda name=name,p=p:digest(p)==expected[name])
ck('audit_no_denials',lambda:not audit_denials)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
assert rss<8*1024**3
result={'date_u':START,'schema':'V6_S1_CX3_FOCUSED_TESTS_V001','status':'TESTED_PASS' if all(x['passed'] for x in checks) else 'TESTED_FAIL','tests_passed':sum(x['passed'] for x in checks),'tests_total':len(checks),'checks':checks,'source_pins':{k:pin(v) for k,v in sources.items()},'harness':pin(Path(__file__)),'rss_bytes_macos':rss,'audit_denials':audit_denials,'scope':'Actual selected source parser, guard preseal import, full producer mains and publication; synthetic in-memory admission and synthetic records. Comparator, SRB reconstruction and library calculation explicitly stubbed. No production numerical replay or launch.'}
with (OUT/'RESULTS_CX3V001.json').open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:result[k] for k in ('status','tests_passed','tests_total','rss_bytes_macos','audit_denials')}))
print('failures',json.dumps([x for x in checks if not x['passed']]))
assert result['status']=='TESTED_PASS'
