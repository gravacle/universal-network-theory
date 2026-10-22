"""P50 independent saved checker. SOURCE ONLY; root executes after distinct review.
Fixed22file9call schema, stdlib matrix arithmetic, no scientificsource imports.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
SOURCE_PIN='d2c31296f2b58ae55be68393871f182671ca53f31ffae2fa003d596771d18e18'
RUNNER_PIN='a8ac0cc6f21597dcc0abf989df438b44572237765053dabdda7308c84228da0f'
SOURCE_PATH='/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0246_2026-10-13_P50-candidate-signature-source-v002.py'
NAMES=['incidence_bias','carrier_instant_null','phase_current','nonhermitian','bad_density',
       'nonunitary_candidate','nonunitary_probe','nonhermitian_read','empty_candidates']
def need(ok,label):
    if not ok:raise ValueError(label)

def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON');out[k]=v
        return out
    def bad(x):raise ValueError('nonfinite JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def encode(v):
    if isinstance(v,complex):return {'real':v.real,'imag':v.imag}
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [encode(x) for x in v]
    return v

def compare(a,b,label):
    if isinstance(b,dict):
        need(isinstance(a,dict) and set(a)==set(b),label+' fields')
        for k in b:compare(a[k],b[k],label+'/'+k)
    elif isinstance(b,list):
        need(isinstance(a,list) and len(a)==len(b),label+' length')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,label+'/'+str(i))
    elif type(b) in (float,int):
        need(type(a) in (float,int) and math.isfinite(a) and abs(a-b)<=2e-12,label+' number')
    else:need(type(a)==type(b) and a==b,label+' literal')

def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a):return [[c*z for z in row] for row in a]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def dag(a):return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def sub(a,b):return add(a,scale(-1,b))
def diag(values):return [[complex(values[i] if i==j else 0) for j in range(len(values))] for i in range(len(values))]

def inputs():
    x=[[0j,1+0j],[1+0j,0j]];y=[[0j,-1j],[1j,0j]];z=diag([1,-1]);ident=diag([1,1])
    flipfirst=[[complex(j==i^2) for j in range(4)] for i in range(4)]
    flipq=[[complex(j==i^1) for j in range(4)] for i in range(4)]
    rho=diag([1,0,0,0]);read=diag([0,0,1,1])
    def pack(h,r,v,w,a):return {'H':h,'rho':r,'preparations':{'candidate':v},'probes':{'q':w},
                               'reads':{'inventory':a},'tolerance':1e-9}
    a=pack(diag([0,3,5,6]),rho,flipfirst,flipq,read)
    h=diag([0,3,5,8]);h[2][3]=h[3][2]=1+0j
    b=pack(h,rho,flipfirst,flipq,read)
    c=pack(scale(-1,x),scale(.5,add(ident,y)),z,x,diag([1,0]))
    return [a,b,c,dict(c,H=[[0j,0j],[-1+0j,0j]]),dict(c,rho=diag([2,-1])),
            dict(c,preparations={'candidate':scale(2,z)}),dict(c,probes={'q':scale(2,x)}),
            dict(c,reads={'inventory':[[0j,1+0j],[0j,0j]]}),dict(c,preparations={})]

def expected(v):
    h=v['H'];rho=v['rho'];ps=v['preparations'];ws=v['probes'];reads=v['reads']
    costs={k:sub(mul(mul(dag(w),h),w),h) for k,w in ws.items()}
    currents={k:scale(1j,sub(mul(h,a),mul(a,h))) for k,a in reads.items()}
    def snapshot(state):
        return {'rho':state,'energy':complex(tr(mul(h,state))),
                'writer_costs':{k:complex(tr(mul(c,state))) for k,c in costs.items()},
                'currents':{k:complex(tr(mul(j,state))) for k,j in currents.items()},
                'state_trace':complex(tr(state))}
    baseline=snapshot(rho);rows={}
    for name,p in ps.items():
        state=mul(mul(p,rho),dag(p));row=snapshot(state)
        row['preparation_work_not_rest_energy']=row['energy']-baseline['energy']
        row['writer_cost_changes']={k:row['writer_costs'][k]-baseline['writer_costs'][k] for k in costs}
        row['current_changes']={k:row['currents'][k]-baseline['currents'][k] for k in currents}
        rows[name]=row
    # All three fixed inputstates are explicit rank-one projectors, all V/W signed permutations.
    return {'scope':'SUPPLIED_UNITARY_CANDIDATE_SIGNATURE_METHOD_ONLY','baseline':baseline,'candidates':rows,
        'cost_operators':costs,'current_operators':currents,
        'diagnostics':{'input_min_eigenvalue':0.0,'input_trace_error':0.0,
                       'preparation_unitarity_fro':{k:0.0 for k in ps},'probe_unitarity_fro':{k:0.0 for k in ws}},
        'error_scope':'FLOAT_DIAGNOSTICS_NOT_CERTIFIED_FULL_ERROR',
        'species_qualification':'LOCALIZATION_PERSISTENCE_REST_ENERGY_RECORD_AND_UNIVERSALITY_NOT_TESTED',
        'writer_qualification':'COMPARATOR_ONLY_UNLESS_SEPARATELY_CERTIFIED',
        'native_matter_release':False,'H1':'UNDETERMINED','H2':'UNDETERMINED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);args=p.parse_args();root=args.input
    need(root.is_dir() and not root.is_symlink(),'plain root')
    names={'START.json','SOURCE_SNAPSHOT.py','RESULTS.json','FINISH.json'}
    names|={'CALL_%02d_%s.json'%(i,k) for i in range(9) for k in ('PRE','RETURN')}
    entries=list(root.iterdir())
    need({f.name for f in entries}==names and all(f.is_file() and not f.is_symlink() for f in entries),'complete22filecensus')
    need(sum(f.stat().st_size for f in entries)<=10*2**20,'bounded complete input')
    raws={f.name:f.read_bytes() for f in entries}
    need(hashlib.sha256(raws['SOURCE_SNAPSHOT.py']).hexdigest()==SOURCE_PIN,'complete pinned snapshot')
    docs={n:decode(raw) for n,raw in raws.items() if n.endswith('.json')}
    compare(docs['START.json'],{'source':SOURCE_PATH,'source_sha256':SOURCE_PIN,'runner_sha256':RUNNER_PIN,
         'scope':'P50_FIXED_CANDIDATE_SIGNATURE_METHOD_ONLY','tolerance':1e-9,'dimensions':[2,4],
         'native_matter_release':False},'START')
    cases={};refusals={}
    messages=['exact stored Hermiticity required','trace-one positive state required',
              'unitary preparation/probe required','unitary preparation/probe required',
              'Hermitian transport read required','one to8 named operators required']
    for i,(name,v) in enumerate(zip(NAMES,inputs())):
        compare(docs['CALL_%02d_PRE.json'%i],encode({'name':name,'inputs':v}),name+'/PRE')
        if i<3:record={'inputs':v,'result':expected(v)};cases[name]=record
        else:record={'inputs':v,'refused':True,'exception':'ValueError','message':messages[i-3]};refusals[name]=record
        compare(docs['CALL_%02d_RETURN.json'%i],encode({'name':name,'actual':record}),name+'/RETURN')
    checks={k:True for k in NAMES[:3]};checks.update({'refuses_'+k:True for k in NAMES[3:]})
    compare(docs['RESULTS.json'],encode({'cases':cases,'refusals':refusals,'checks':checks,'all_method_checks':True,
         'status':'FIXED_COMPARATOR_CONTROLS_NOT_PHYSICAL_SPECIES','native_matter_release':False}),'RESULTS')
    compare(docs['FINISH.json'],{'status':'AWAITING_DISTINCT_SAVED_CHECKER','call_names':NAMES,'call_count':9,
         'native_matter_release':False,'producer_check_flag':True,
         'resource_acceptance':'EXTERNAL_ROOT_SUPERVISOR_REQUIRED'},'FINISH')
    for name,raw in raws.items():need((root/name).read_bytes()==raw,'closing original bytes')
    report={'status':'INDEPENDENT_FIXED_P50_SAVED_METHOD_COMPARISON_PASS','source_author':'Codex2',
        'complete_files':22,'positive_calls':3,'actual_refusals':6,
        'comparison_absolute_tolerance':2e-12,'input_method_tolerance':1e-9,
        'original_files':{n:{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for n,raw in raws.items()},
        'requires_distinct_root_adjudication':True,
        'resource_acceptance':'ROOT_ORIGINAL_PROCESS_AND_WHOLE_RUNTIME_CUSTODY_REQUIRED_SEPARATELY',
        'native_matter_release':False,'physical_prediction_released':False}
    with args.output.open('x') as f:
        json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

if __name__=='__main__':main()
