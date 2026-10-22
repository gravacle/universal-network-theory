"""Independent c2v006 A71/header/token and Store probes. Fresh synthetic trees only."""
import os,sys
from pathlib import Path
def audit(event,args):
    if event.startswith(('subprocess.','socket.','os.system','os.exec','os.spawn')) or event=='os.fork':raise RuntimeError('NO_LAUNCH_NETWORK')
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.path.realpath(os.fsdecode(args[0]))
        if '/runs_ext/' in p or '/runs/' in p or '/.codex/sessions/' in p or 'KMAX_A2F10_C5H_RUN' in p or '/gates_v006/out/IDENTITY' in p or '/gates_v006/records/R4' in p:raise RuntimeError('PROHIBITED_READ:'+p)
        if 'NGC3198' in p and any(x in p.lower() for x in ('target','observed','rotmod')):raise RuntimeError('PROHIBITED_TARGET')
sys.addaudithook(audit)
import argparse,ast,contextlib,hashlib,io,json,resource,struct,time,types,zipfile
import numpy as np
BASE=Path(__file__).parent
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
TARGET=ART/'tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py'
PIN='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
FACTORY=ART/'review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py'
FPIN='711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p,h,name):
    raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==h
    m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(raw,str(p),'exec'),m.__dict__);return m
def write(p,x):
    with Path(p).open('x') as f:json.dump(x,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def npy(prefix='',vals=(1.,2.)):
    hdr=("{"+prefix+"'descr': '<f8', 'fortran_order': False, 'shape': (2,), }").encode()
    pad=64-((10+len(hdr)+1)%64);hdr+=b' '*pad+b'\n'
    return b'\x93NUMPY\x01\x00'+struct.pack('<H',len(hdr))+hdr+np.array(vals,dtype='<f8').tobytes()
def zipbytes(raw):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:z.writestr('state.npy',raw)
    return b.getvalue()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(exist_ok=False);t=time.monotonic()
    M=load(TARGET,PIN,'cx2_v6_a71');F=load(FACTORY,FPIN,'cx2_own_prior_fixture')
    M.DRIVER[:]=M.DRIVERS['r5'];drv=M.load_driver();cm=M.load_cm();rows=[];units=[]
    def u(name,passed,detail=None):units.append({'name':name,'pass':bool(passed),'detail':detail})
    normal=npy(); duplicate=npy("'descr': '<i8', ")
    u('npy_duplicate_header_accepted_as_same',M.npy_identity_bytes(normal)==M.npy_identity_bytes(duplicate),{'expected_strict_behavior':'REJECT','finding':True})
    p=out/'standalone_duplicate.npy'
    with p.open('xb') as f:f.write(duplicate)
    st=M.Store(out,'synthetic');v=st.array(p)
    u('Store_duplicate_header_has_no_problem',v[0]=='npy' and not st.problems,{'expected_strict_behavior':'STRICT_PARSE_FAIL','problems':st.problems,'finding':True})
    for name,raw in [('normal_npy',normal),('normal_npz',zipbytes(normal))]:
        q=out/(name+('.npz' if 'npz' in name else '.npy'))
        with q.open('xb') as f:f.write(raw)
        store=M.Store(out,'synthetic');first=store.array(q);second=store.array(q)
        u(name+'_cached_array_object',first is second)
        u(name+'_hash_matches_parsed_bytes',store.sha_of(q)==hashlib.sha256(raw).hexdigest())
        u(name+'_stable_verify',not store.verify())
    for name,raw in [('json_equal_duplicate',b'{"x":1,"x":1}'),('json_unequal_duplicate',b'{"x":0,"x":1}')]:
        q=out/(name+'.json')
        with q.open('xb') as f:f.write(raw)
        store=M.Store(out,'synthetic');v=store.json(q);u(name,isinstance(v,M.Unparseable) and bool(store.problems))
    for field,val in [('descr',"'<f8'"),('shape','(2,)'),('fortran_order','False')]:
        try:M.npy_identity_bytes(npy("'%s': %s, "%(field,val)));accepted=True
        except Exception:accepted=False
        u('header_duplicate_equal_'+field,accepted,{'finding':True,'expected':'REJECT'})
    p1,bad,joined=M.build_tokens([['left0','right0','<X>|<Y>'],['left1','right1','<X>'],['left1','right1','<Y>']])
    u('joined_label_alias_not_rejected',not bad and len({p[2] for p in p1})<len(p1),{'pairs':p1,'bad':bad,'finding':True})
    p2,bad2,j2=M.build_tokens([['a','b','<T>'],['a','b','<T>']])
    u('exact_token_duplicate_not_rejected',not bad2 and len(p2)==1,{'pairs':p2,'bad':bad2,'finding':True})
    # Unit mutation injection uses in-memory replacement bytes only, never edits a file.
    q=out/'cache_probe.json'
    with q.open('xb') as f:f.write(b'{"value":1}')
    store=M.Store(out,'synthetic');old=store.json(q)
    orig=M.sha_file;M.sha_file=lambda path:'0'*64 if str(path)==str(q) else orig(path)
    try:u('Store_verify_detects_end_hash_change',bool(store.verify()))
    finally:M.sha_file=orig
    u('Store_json_cached_value',store.json(q) is old)
    store._record(q,'0'*64);u('Store_records_intermediate_hash_change',bool(store.unstable))
    def case(name,expected='FAIL',owner=None,mut=None,tokens=None):
        d=out/name;d.mkdir();r=F.Tree(d/'REF','REF','B0P_RERUN',M,drv,cm);n=F.Tree(d/'NEW','NEW','B0P_RERUN',M,drv,cm)
        if mut:mut(r,n)
        for tree in (r,n):tree.obj('finish.json')['result_sha256']=F.sha(F.raw_json(tree.obj('result.json')))
        r.publish();n.publish();tp=d/'TOKENS.json';F.jfile(tp,{'declared':tokens or []});rp=d/'REPORT.json'
        argv=['--reference',str(r.root),'--new',str(n.root),'--tokens',str(tp),'--out',str(rp),'--driver','r5','--gate','B0P_RERUN']
        err=None
        try:
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):M.main(argv)
        except BaseException as ex:err=type(ex).__name__+':'+str(ex)
        rep=json.loads(rp.read_bytes()) if rp.exists() else {}
        actual=rep.get('verdict','NO_REPORT');met=actual==('PASS_BITWISE_EQUAL' if expected=='PASS' else 'FAIL') and (owner is None or owner in rep.get('failing',[]))
        row={'name':name,'expected':expected,'owner':owner,'actual':actual,'expectation_met':met,'failing':rep.get('failing',[]),'exception':err,'report':{'path':str(rp),'sha256':sha(rp)} if rp.exists() else None};rows.append(row)
        print(json.dumps(row))
    def array_mut(r,n,newraw,kind='npy'):
        rel='stages/11_reference/reference/extra.'+kind
        r.files[rel]=('raw',normal if kind=='npy' else zipbytes(normal));n.files[rel]=('raw',newraw)
    case('P00_plain_synthetic_baseline','PASS')
    case('F01_npy_duplicate_descr',owner='STRICT_PARSE',mut=lambda r,n:array_mut(r,n,duplicate))
    case('F02_npz_member_duplicate_shape',owner='STRICT_PARSE',mut=lambda r,n:array_mut(r,n,zipbytes(npy("'shape': (900,), ")),'npz'))
    case('F03_npy_duplicate_equal_fortran',owner='STRICT_PARSE',mut=lambda r,n:array_mut(r,n,npy("'fortran_order': False, ")))
    case('C04_ordinary_array_change',owner='STAGES',mut=lambda r,n:array_mut(r,n,npy(vals=(3.,2.))))
    case('F05_duplicate_exact_declared_token',owner='NO_LAST_WINS',tokens=[['cx2_left','cx2_right','<CX2>']]*2)
    toks=[['cx2_left0','cx2_right0','<X>|<Y>'],['cx2_left1','cx2_right1','<X>'],['cx2_left1','cx2_right1','<Y>']]
    def textchange(r,n):r.obj('result.json')['scientific_probe']='cx2_left0';n.obj('result.json')['scientific_probe']='cx2_right1'
    case('F06_joined_label_alias_changes_result',owner='NORM_INJECTIVE',mut=textchange,tokens=toks)
    case('C07_same_result_change_without_tokens',owner='RESULT',mut=textchange)
    case('P08_one_honest_declared_pair','PASS',mut=lambda r,n:[r.obj('result.json').update(scientific_probe='cx2_left0'),n.obj('result.json').update(scientific_probe='cx2_right0')],tokens=[toks[0]])
    assert sha(TARGET)==PIN
    result={'schema':'CX2_C2V006_A71_STORE_PROBES_V001','date_u':a.date_u,'status':'TESTED_SYNTHETIC_ONLY','source_before_after_sha256':PIN,'rows':rows,'unit_observations':units,'unit_observations_matched':sum(x['pass'] for x in units),'unit_count':len(units),'unexpected_whole_gate_passes':[x['name'] for x in rows if x['expected']=='FAIL' and x['actual']=='PASS_BITWISE_EQUAL'],'all_whole_gate_baselines_pass':all(x['actual']=='PASS_BITWISE_EQUAL' for x in rows if x['expected']=='PASS'),'source_pin':{'path':str(TARGET),'sha256':PIN},'fixture_factory_pin':{'path':str(FACTORY),'sha256':FPIN},'harness_pin':{'path':str(Path(__file__)),'sha256':sha(__file__)},'runtime_seconds':time.monotonic()-t,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scientific_launches':0,'actual_run_reads':0,'limits':['Unit observations marked finding are reproductions of undesired behavior, not passing correctness tests.','End-hash change is synthetic in-memory function fault injection restored immediately; no existing file modified.','No supplied checker imported or executed. Own prior fixture writer builds fresh local files.','Production data incidence is UNTESTED.']}
    write(out/'RESULTS_CX2V001.json',result)
    print(json.dumps({'result_sha256':sha(out/'RESULTS_CX2V001.json'),'unexpected':result['unexpected_whole_gate_passes'],'units':[result['unit_observations_matched'],result['unit_count']]}))
if __name__=='__main__':main()
