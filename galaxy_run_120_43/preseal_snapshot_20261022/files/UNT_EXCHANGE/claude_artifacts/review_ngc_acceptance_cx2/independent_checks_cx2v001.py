"""0767 P-106: reviewer synthetic checks and mutation probes; exclusive creation only."""
import ast, copy, hashlib, itertools, json, math, os, subprocess, sys, types
from pathlib import Path
import numpy as np
B = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2')
ROOT = Path(__file__).parent
RUN = ROOT/'independent_run_cx2v001'
RUN.mkdir()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, raw):
    p=Path(p);p.parent.mkdir(exist_ok=True,parents=True)
    if not isinstance(raw,bytes):raw=raw.encode()
    with p.open('xb') as f:f.write(raw)
    return {'path':str(p),'sha256':sha(p)}
def load(p,name,expected=None):
    p=Path(p);raw=p.read_bytes()
    if expected:assert hashlib.sha256(raw).hexdigest()==expected
    m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m
    exec(compile(raw,str(p),'exec'),m.__dict__)
    return m
T5=load(B/'test_ngc_acceptance_c2v005.py','review_suite5','ae045203a3c6bb2b9663ebfb807f0c1208d8177067cca4f83857a7c088802605')
sys.addaudithook(T5._audit)
def extra_guard(event,args):
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.path.realpath(os.fsdecode(args[0]))
        if any(x in p for x in ('/.codex/','/CLAUDE2/runs/','/runs_ext/','V007_STEP2_LAUNCH_ROOT','V007_POSTSEAL_RECORDS','/s4rc1_c3/cp1_run_')) or '_RUN_' in p:
            raise PermissionError('REVIEW_SCOPE_BLOCKED')
sys.addaudithook(extra_guard)
T=T5.load(str(B/T5.PREV_SUITE[0]),'review_suite3',T5.PREV_SUITE[1]);T.NAMES=dict(T.NAMES,H=T5.HANDOFF_NAME)
S=T5.make_suite_class(T)(str(RUN),str(B))
# Never call Suite.all or P16/P18/P29/F38: their real-data operations are root-owned.
A=S.A;H=S.H
checks=[];mutants=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'ok':bool(ok),'detail':detail});assert ok,name

def oracle_readings(mod):
    cs=[mod.ACCEPTED,mod.INHERITED,mod.ROUTE_B,mod.ITERATE]
    bad=[]
    for vs in itertools.product(['PASS','FAIL','UNAVAILABLE'],repeat=4):
        want='NON_LAPSE_TAIL_MATERIAL' if 'FAIL' in vs[:3] else 'LO_UNCERTIFIED_TRANSIENT' if vs[3]=='FAIL' and vs[:3]==('PASS',)*3 else 'PASS' if vs==('PASS',)*4 else 'INCOMPLETE'
        ss=[{'state_class':c,'verdict':v} for c,v in zip(cs,vs)]
        if mod.call_reading(ss)['reading']!=want:bad.append(vs)
    return not bad,bad

def arithmetic(mod):
    ed=np.arange(2.,48.);b=np.zeros(len(ed)-1);b[0]=.005
    shells=[{'range_inverse_kpc':r,'rho_used':1.0} for r in mod.RHO_PARTITION]
    row=[{'id':'q','status':mod.ROW_INCLUDED,'v':.002,'R':1.0}]
    a=mod.aggregate(shells,ed,b,row,c=2.,theta=.5)
    ok=(a['shells'][0]['max_g']==.005 and a['G']==.005 and mod.decide(a,row)[0]=='PASS')
    b[0]=np.nextafter(.005,math.inf);hi=mod.aggregate(shells,ed,b,row,c=2.,theta=.5)
    ok=ok and mod.decide(hi,row)[0]=='FAIL'
    missing=[dict(row[0],status=mod.ROW_MISSING)]
    ok=ok and mod.decide(hi,missing)==('FAIL',[],True)
    zero=[dict(row[0],v=0.)];z=mod.aggregate(shells,ed,b,zero,c=2.,theta=.5)
    ok=ok and z['G']==0. and z['zero_speed_rows']==['q'] and mod.decide(z,zero)[0]=='PASS'
    empty=mod.aggregate(shells,ed,b,[],c=2.,theta=.5)
    ok=ok and mod.decide(empty,[])[0]=='UNAVAILABLE' and empty['G'] is None
    return ok

def readout_max(mod):
    r1=[{'id':'q','valid':True,'speed_km_s':-3.}];r2=[{'id':'q','valid':True,'speed_km_s':2.}]
    o=mod.own_call_readouts({'passes':[{'rows':r1,'invalid_rows':[]},{'rows':r2,'invalid_rows':[]}],'rows':r2,'invalid_rows':[]},['q'])
    return o['rows'][0]['v']==3. and o['rows'][0]['status']==mod.ROW_INCLUDED
check('81 Q5 mixed-verdict combinations vs independent clause oracle',*oracle_readings(A))
for vs in itertools.product(['PASS','FAIL','UNAVAILABLE'],repeat=4):
    cs=[A.ACCEPTED,A.INHERITED,A.ROUTE_B,A.ITERATE]
    want=A.call_reading([{'state_class':c,'verdict':v} for c,v in zip(cs,vs)])['reading'];want='ACCEPTED' if want=='PASS' else want
    got=H.readings({'states':[{'class':c,'verdict':v,'state':{'id':i}} for i,(c,v) in enumerate(zip(cs,vs))],'blockers':[]})[0]
    check('handoff Q5 '+','.join(vs),got==want)
check('scalar ratio, exact threshold, nextafter, monotone missing row, zero, empty',arithmetic(A))
check('readout maximum absolute speed across all passes',readout_max(A))
raw=(B/'ngc_lo_state_adapter_c2v003a.py').read_text()
mutations=[('linear_speed','(v * KM_S_TO_M_S) ** 2','(v * KM_S_TO_M_S) ** 1',arithmetic),('inclusive_failure',"s['max_g'] > PER_SHELL_MAX","s['max_g'] >= PER_SHELL_MAX",arithmetic),('looser_threshold','PER_SHELL_MAX = 0.005','PER_SHELL_MAX = 0.05',arithmetic),('route_b_not_decisive','DECISIVE_CLASSES = (ACCEPTED, INHERITED, ROUTE_B)','DECISIVE_CLASSES = (ACCEPTED, INHERITED)',lambda m:oracle_readings(m)[0]),('readout_minimum','a > vmax[i]','a < vmax[i]',readout_max)]
for name,old,new,probe in mutations:
    assert raw.count(old)==1,(name,raw.count(old))
    pin=write(RUN/'mutants'/(name+'.py'),raw.replace(old,new));m=load(pin['path'],'mutant_'+name)
    killed=not bool(probe(m));check('kill '+name,killed);mutants.append({'name':name,'source':pin,'killed':killed})
# One synthetic recipe fixture; all generated records stay under this new review folder.
c=S.rfx.make_call('independent_recipe')
targets,_=S.rfx.route_b_targets(c)
bykind={t['state']['stage_kind']:t for t in targets}
ns,_=S.rfx.route_a_targets(c)
nt=[t for t in ns if t['origin']['iteration']==c['a'] and t['origin']['role']==T5.NEXT][0]
for name,t in [('columns',bykind['fs_columns']),('rotation',bykind['fs_rotation']),('N',nt)]:
    adm,pin=S.rfx.admit(c,t,'baseline_'+name)
    check('baseline recipe '+name,adm['admitted'],adm.get('codes'))
rr=(B/'ngc_roster_recipes_c2v002.py').read_text()
probes=[('sort_column_ids','return [float(nodes[i]) for i in ids],','return [float(nodes[i]) for i in sorted(ids)],',bykind['fs_columns'],True),('reverse_rotation',"return z['radial_nodes_m'],", "return z['radial_nodes_m'][::-1],",bykind['fs_rotation'],True),('drop_rotation_radius',"return z['radial_nodes_m'],", "return z['radial_nodes_m'][:-1],",bykind['fs_rotation'],False),('omit_N_update','gas = (1 - r) * gas + r * updated','gas = gas',nt,False),('N_gamma_one_ulp',"'gamma_eff': ctl.gamma_eff,", "'gamma_eff': float(np.nextafter(ctl.gamma_eff, math.inf)),",nt,False)]
for name,old,new,t,expected in probes:
    assert rr.count(old)==1,(name,rr.count(old))
    mp=write(RUN/'mutants'/(name+'.py'),rr.replace(old,new))
    wrapper=write(RUN/'mutants'/(name+'_wrapper.py'),T5.WRAPPER_TEMPLATE % {'recipes':(mp['path'],mp['sha256']),'toolkit':(S.rfx.toolkit_pin['path'],S.rfx.toolkit_pin['sha256'])})
    adm,pin=S.rfx.admit(c,t,name,recipe=wrapper)
    check('recipe mutation '+name,adm['admitted'] is expected,{'codes':adm['codes'],'admitted':adm['admitted']})
    mutants.append({'name':name,'source':mp,'wrapper':wrapper,'admission':pin,'admitted':adm['admitted'],'expected_order_equivalence':expected,'codes':adm['codes']})
check('no forbidden open attempted in independent checks',T5.GUARD['blocked']==[],T5.GUARD['blocked'])
res={'schema':'CX2_P106_INDEPENDENT_CHECKS_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'status':'TESTED','verdict':'PASS','checks':checks,'n_checks':len(checks),'mutants':mutants,'script':{'path':__file__,'sha256':sha(__file__)},'baseline_pins':S.shas,'skipped_before_entry':['P16','P18','P29','F38'],'guard_refused_opens':T5.GUARD['blocked'],'synthetic_only':True,'flags':{'isolated':sys.flags.isolated,'dont_write_bytecode':sys.flags.dont_write_bytecode}}
pin=write(ROOT/'INDEPENDENT_CHECKS_RESULT_CX2V001.json',json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps({'verdict':'PASS','checks':len(checks),'mutants':len(mutants),'result':pin}))
