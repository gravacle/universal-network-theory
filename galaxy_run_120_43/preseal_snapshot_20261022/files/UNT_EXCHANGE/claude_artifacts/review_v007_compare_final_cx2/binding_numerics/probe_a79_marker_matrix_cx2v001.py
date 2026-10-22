"""Independent synthetic r10 probes. No supplied tests or scientific evidence imports."""
import argparse, ast, copy, hashlib, importlib.util, json, math, os, re, stat, sys, time, types, zipfile
from pathlib import Path
import numpy as np

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics')
SRC = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py')
EXPECTED = 'e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93'
ROOT = BASE / ('run_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '_' + str(os.getpid()))
ROOT.mkdir()
access, blocked, tests = [], [], []
def sh(raw): return hashlib.sha256(raw).hexdigest()
def norm(p): return os.path.abspath(os.fsdecode(p))
def guard_path(p, op):
    if isinstance(p, int) or p is None: return
    s = norm(p)
    if ('/runs/' in s or '/runs_ext/' in s or '/.codex/' in s or '/.vol/' in s):
        blocked.append([op,s]); raise PermissionError('OUTSIDE_SYNTHETIC_AUTHORITY')
    if op in ('open','list','stat','readlink'):
        if s.startswith(str(ROOT) + '/') or s == str(ROOT) or s == str(SRC): return
        # realpath walks parents. Allow their metadata only, never their contents.
        if op in ('stat','readlink') and str(ROOT).startswith(s.rstrip('/')+'/'): return
        if op in ('stat','readlink') and str(SRC).startswith(s.rstrip('/')+'/'): return
        blocked.append([op,s]); raise PermissionError('OUTSIDE_SYNTHETIC_ALLOWLIST')
def audit(event,args):
    if event == 'open':
        p, mode, flags = args
        guard_path(p,'open')
        if isinstance(p,(str,bytes)):
            access.append({'event':'open','path':os.fsdecode(p),'mode':mode})
            if flags & (os.O_WRONLY | os.O_RDWR):
                if not norm(p).startswith(str(ROOT)+'/') or not flags & os.O_EXCL:
                    blocked.append([event,os.fsdecode(p)]); raise PermissionError('EXCLUSIVE_NEW_WRITES_ONLY')
    if event in ('os.listdir','os.scandir'): guard_path(args[0],'list')
    if event.startswith(('subprocess','socket.')) or event in ('os.system','os.remove','os.rename','os.rmdir','os.link','os.symlink'):
        blocked.append([event,str(args)]); raise PermissionError('NO_LAUNCH_NETWORK_MUTATION')
sys.addaudithook(audit)
for opname in ('stat','lstat','readlink'):
    old = getattr(os,opname)
    def wrapped(p,*args,_old=old,_op=opname,**kwargs):
        guard_path(p,'readlink' if _op=='readlink' else 'stat')
        return _old(p,*args,**kwargs)
    setattr(os,opname,wrapped)
raw=SRC.read_bytes(); assert sh(raw)==EXPECTED
tree=ast.parse(raw)
imports=[]
for n in ast.walk(tree):
    if isinstance(n,ast.Import): imports.extend(x.name for x in n.names)
    elif isinstance(n,ast.ImportFrom): imports.append(n.module)
allowed={'argparse','ast','hashlib','importlib.util','json','math','os','re','stat','sys','time','zipfile','pathlib','numpy'}
assert set(imports)<=allowed
m=types.ModuleType('cx2_independent_r10'); m.__file__=str(SRC)
sys.modules[m.__name__]=m
exec(compile(raw,str(SRC),'exec'),m.__dict__)
def put(name,obj,raw=False):
    p=ROOT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    b=obj if raw else json.dumps(obj,sort_keys=True,indent=2,allow_nan=True).encode()+b'\n'
    with p.open('xb') as f: f.write(b)
    return p,sh(b)
def pin(name,b):
    p,h=put(name,b,True); return {'path':str(p),'sha256':h}
def add(name,section,expect,actual,detail=None,kind='TESTED'):
    tests.append({'id':name,'section':section,'expected':expect,'actual':actual,'pass':expect==actual,'detail':detail,'status':kind})
def context(ms=128):
    cases={k:{'normalized_spec_equal':{'/numerics':{'uv_tail':{'gas':{'M_s':ms},'outer':{'shape':'cylinder','K_big_inverse_kpc':128}}}}} for k in ('C2T','C3T','C4T')}
    return {'case_block':{'cases':cases},'ids':[f'r{i:02d}' for i in range(12)],'tau':{f'r{i:02d}':1.0 for i in range(12)}}
prod=pin('synthetic_producer.fixture',b'CX2 invented producer bytes only\n')
def registry(gate,record_sha,counts=None,marker=False):
    return {'schema':m.PRODUCER_REGISTRY_SCHEMA,'producers':{gate:[prod]},'identity_comparators':[], 'identity_tokens':{},'gate_records':{gate:m.GATE_RECORD_AFTER_SEAL if marker else [record_sha]},'gq_all_nodes_counts':counts or {}}
def gate(name,g,rec,ctx=None,counts=None,override_registry=None):
    obj={'schema':m.GATE_SCHEMA,'gate':g,'producer':copy.deepcopy(prod),'verdict':m.GATE_PASS_VERDICTS[g]}
    obj.update(copy.deepcopy(rec)); p,h=put('records/'+name+'.json',obj)
    c=copy.deepcopy(ctx or context())
    reg=registry(g,h,counts)
    c['producer_registry']=m.producer_registry_from_obj(reg) if override_registry is None else override_registry
    out=m.evaluate_gate(g,p,c,{'C4T':'c'*64})
    put('reports/'+name+'.json',out)
    return out
def gatetest(name,sec,g,rec,expect='RECORD_DEFECT',ctx=None,counts=None):
    out=gate(name,g,rec,ctx,counts)
    add(name,sec,expect,out['status'],out['codes']); return out
def lo(ms=128):
    return {'state_result_sha256':m.PIN_R3['C4R3'][1],'source_gas_M_s':ms,'gas_M_s':ms,'tail_config_gas':{'M_s':ms},'build':{'roster_gas':{'M_s':ms}},'shells':[{'range_inverse_kpc':list(r),'max_over_tau':.0001} for r in m.LO_RANGES],'summed_max_over_tau':.001}
def doubling(ms=128):
    return {'ddo_state_result_sha256':m.PIN_R3['C4R3'][1],'ddo_max_change_over_tau':.001,'ddo_K_big_inverse_kpc':[128,256],'ddo_gas_M_s':ms,'ngc_operator_sha256':m.NGC_T120L_OPERATOR_SHA256,'ngc_max_change_over_theta':.001}
def gq(ms=128):
    rs=[]
    for k,edge in ((2,128),(3,128),(4,256)):
        rs.append({'roster':f'DDO_C{k}T','geometry':f'C{k}T_KB{edge}','kept':{'shape':'cube','K_inverse_kpc':k},'outer':{'shape':'cylinder','K_big_inverse_kpc':edge},'k_range_inverse_kpc':[k,edge],'M_s':ms,'M_s_doubled':2*ms,'nodes':4096,'max_abs_diff_over_P0':1e-14,'all_nodes':{'nodes':8192,'max_abs_diff_over_P0':1e-14}})
    rs.append({'roster':'NGC_T120L','k_range_inverse_kpc':[2,32],'M_s':96,'M_s_doubled':192,'nodes':4096,'max_abs_diff_over_P0':1e-14})
    return {'source_gas_M_s':ms,'gas_M_s_DDO':ms,'rosters':rs}
def counts(rec): return {x['geometry']:8192 for x in rec['rosters'] if 'geometry' in x}

# A75.7: probe every named permitted/disallowed token route at loader + gate recheck.
expected_allowed=set()  # A79: every gate must refuse the marker
for g in m.ALL_GATES:
    r=registry(g,'a'*64,marker=True)
    try:m.producer_registry_from_obj(r);actual=True;why=[]
    except m.Refused as e:actual=False;why=[e.refusal_code]
    add('MARKER_load_'+g,'N2',g in expected_allowed,actual,why)
    normalized={'gate_records':{g:m.GATE_RECORD_AFTER_SEAL}}
    why=m.gate_record_sha_codes(g,'a'*64,normalized)
    add('MARKER_gate_'+g,'N2',g in expected_allowed,not why,why)

after=sh(SRC.read_bytes())
add('source_unchanged','HYGIENE',EXPECTED,after)
add('guard_blocked_events','HYGIENE',[],blocked)
summary={'date_utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime()),'source':str(SRC),'source_before':sh(raw),'source_after':after,'imports_reviewed':imports,'synthetic_only':True,'science_stages_executed':0,'test_seams':['Own minimal case block and exact-byte synthetic producer registry','A72 constants repinned to owned inert files; original validation functions unchanged','No production evidence imported; no supplied test executed; no build_context called'],'counts':{'total':len(tests),'passed':sum(x['pass'] for x in tests),'failed':sum(not x['pass'] for x in tests)},'sections':{},'tests':tests,'guard_blocked_events':blocked,'access_count':len(access)}
for s in sorted({x['section'] for x in tests}):
    xs=[x for x in tests if x['section']==s];summary['sections'][s]={'total':len(xs),'passed':sum(x['pass'] for x in xs),'failed':sum(not x['pass'] for x in xs)}
put('ACCESS_LOG.json',access)
p,h=put('RESULTS.json',summary)
print(json.dumps({'path':str(p),'sha256':h,'counts':summary['counts'],'sections':summary['sections'],'failures':[{'id':x['id'],'actual':x['actual'],'detail':x['detail']} for x in tests if not x['pass']]}))
