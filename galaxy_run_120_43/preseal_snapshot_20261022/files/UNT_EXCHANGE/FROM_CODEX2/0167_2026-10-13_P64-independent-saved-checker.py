"""Independent P64 saved method checker; root-only after distinct source review.
stdlib 2x2 arithmetic, no producer/scientific imports, no native claim.
"""
import argparse
import cmath
import hashlib
import json
import math
import os
from pathlib import Path

SOURCE_PIN='693448ad4a3568b7bae1b981404bc586dacae84302951e8959dd14e9c4598892'
RUNNER_PIN='c97a30c1beebf1cc5ba049c5241509136ca7a604f62815a2676e735a4d042131'
SOURCE_PATH='/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0225_2026-10-13_P64-current-history-method-source-v002.py'
NAMES=['hopping','reversed_phase','common_frame','bind_no_transport',
       'hermiticity','density','class_sum','unitarity','read','empty_classes','too_many_classes']


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


def add(a,b):return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def scale(c,a):return [[c*z for z in row] for row in a]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def dag(a):return [[a[j][i].conjugate() for j in range(2)] for i in range(2)]
def tr(a):return a[0][0]+a[1][1]
def fro(a):return math.sqrt(sum(abs(z)**2 for row in a for z in row))
def sub(a,b):return add(a,scale(-1,b))
I=[[1+0j,0j],[0j,1+0j]]
X=[[0j,1+0j],[1+0j,0j]]
Y=[[0j,-1j],[1j,0j]]
P=[[1+0j,0j],[0j,0j]]
Q=[[0j,0j],[0j,1+0j]]


def expected_inputs():
    rho=scale(.5,add(I,Y));h=scale(-1,X)
    base={'H':h,'rho':rho,'A':P,'U':I,'classes':[P,Q],'tolerance':1e-9}
    out=[dict(base),dict(base,rho=scale(.5,sub(I,Y)))]
    # Common S=diag(i,1) conjugation: H becomes Y; rho becomes (I+X)/2.
    out.append(dict(base,H=Y,rho=scale(.5,add(I,X))))
    paths=[[a,b,c] for a in (0,1) for b in (0,1) for c in (0,1)]
    classes=[]
    for a,b,c in paths:
        # Each matrix unit |c><a| carries two stay/hop factors, each1/sqrt2.
        amplitude=((1 if c==b else -1j)*(1 if b==a else -1j))/2
        v=[[0j,0j],[0j,0j]];v[c][a]=amplitude;classes.append(v)
    out.append(dict(base,H=X,rho=P,A=I,U=scale(-1j,X),classes=classes))
    out.extend([dict(base,H=[[0j,0j],[-1+0j,0j]]),
                dict(base,rho=[[2+0j,0j],[0j,-1+0j]]),
                dict(base,classes=[P]),dict(base,U=scale(2,I),classes=[scale(2,P),scale(2,Q)]),
                dict(base,A=[[0j,1+0j],[0j,0j]]),dict(base,classes=[]),
                dict(base,classes=[scale(1/17,I) for _ in range(17)])])
    return out,paths


def expected_result(v):
    h,r,a,u,cs=(v[k] for k in ('H','rho','A','U','classes'))
    j=scale(1j,sub(mul(h,a),mul(a,h)));final=mul(mul(u,r),dag(u))
    branches=[[mul(mul(c,r),dag(b)) for b in cs] for c in cs]
    d=[[tr(z) for z in row] for row in branches]
    m=[[tr(mul(j,z)) for z in row] for row in branches]
    diag=sum(m[k][k] for k in range(len(cs)));total=sum(map(sum,m))
    current=tr(mul(j,final));summed=[[sum(c[i][k] for c in cs) for k in range(2)] for i in range(2)]
    small_eigen=(tr(r).real-math.sqrt((r[0][0].real-r[1][1].real)**2+4*abs(r[0][1])**2))/2
    def herm_error(mat):
        return math.sqrt(sum(abs(mat[i][k]-mat[k][i].conjugate())**2 for i in range(len(mat)) for k in range(len(mat))))
    return {'scope':'SUPPLIED_COHERENT_CLASS_CURRENT_METHOD_ONLY',
        'J':j,'rho_final':final,'D':d,'M_current':m,
        'D_phase_radians':[[cmath.phase(z) if abs(z)>1e-9 else None for z in row] for row in d],
        'phase_null_meaning':'UNRESOLVED_BELOW_FLOAT_TOLERANCE_NOT_PROVEN_ZERO',
        'absolute_current':complex(current),'diagonal_class_current':complex(diag),
        'offdiagonal_current':complex(total-diag),
        'D_diagonal_sum':complex(sum(d[k][k] for k in range(len(cs)))),'D_total':complex(sum(map(sum,d))),
        'diagnostics':{'rho_trace_error':float(abs(tr(r)-1)),'rho_min_eigenvalue':small_eigen,
            'unitarity_fro':fro(sub(mul(dag(u),u),I)),'class_sum_fro':fro(sub(summed,u)),
            'D_hermiticity_fro':herm_error(d),'M_hermiticity_fro':herm_error(m),
            'current_sum_error':float(abs(total-current))},
        'error_scope':'FLOAT_DIAGNOSTICS_ONLY_NOT_CERTIFIED_INPUT_OR_PROPAGATION_ERROR',
        'class_provenance':'ROOT_MUST_AUTHENTICATE_NATIVE_PROJECTORS_AND_FULL_HISTORIES',
        'native_motion_release':False,'H1':'UNDETERMINED','H2':'UNDETERMINED'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    root=args.input
    need(root.is_dir() and not root.is_symlink(),'plain input root')
    names={'START.json','SOURCE_SNAPSHOT.py','RESULTS.json','FINISH.json'}
    names|={'CALL_%02d_%s.json'%(i,k) for i in range(11) for k in ('PRE','RETURN')}
    entries=list(root.iterdir())
    need({p.name for p in entries}==names and all(p.is_file() and not p.is_symlink() for p in entries),'complete26filecensus')
    need(sum(p.stat().st_size for p in entries)<=10*2**20,'bounded complete input')
    raws={p.name:p.read_bytes() for p in entries}
    need(hashlib.sha256(raws['SOURCE_SNAPSHOT.py']).hexdigest()==SOURCE_PIN,'whole source snapshot')
    documents={n:decode(v) for n,v in raws.items() if n.endswith('.json')}
    compare(documents['START.json'],{'source':SOURCE_PATH,'source_sha256':SOURCE_PIN,
        'runner_sha256':RUNNER_PIN,'scope':'P64_FIXED_MANUFACTURED_CURRENT_HISTORY_METHOD_ONLY',
        'tolerance':1e-9,'dimension':2,'native_motion_release':False},'START')
    inputs,paths=expected_inputs();cases={};refusals={}
    messages=['exact stored Hermiticity required','trace-one positive state required',
              'complete class sum must equal evolution','unitary evolution required',
              'exact stored Hermiticity required','one to16 complete class operators required',
              'one to16 complete class operators required']
    for i,(name,v) in enumerate(zip(NAMES,inputs)):
        compare(documents['CALL_%02d_PRE.json'%i],encode({'name':name,'inputs':v}),name+'/PRE')
        if i<4:
            result=expected_result(v);actual={'result':result}
            cases[name]={'inputs':v,'result':result}
        else:
            actual={'refused':True,'exception':'ValueError','message':messages[i-4]}
            refusals[name]=dict(actual,inputs=v)
        compare(documents['CALL_%02d_RETURN.json'%i],encode({'name':name,'actual':actual}),name+'/RETURN')
    checks={k:True for k in ['hopping_current','zero_D_offdiag','inserted_cross_current','reverse',
                             'common_frame','Bind_interference','Bind_zero_current']}
    checks.update({'refuses_'+n:True for n in NAMES[4:]})
    compare(documents['RESULTS.json'],encode({'cases':cases,'refusals':refusals,'checks':checks,
        'all_method_checks':True,'bind_paths':paths,
        'status':'PROSPECTIVE_MANUFACTURED_CURRENT_CONTROLS_ONLY','native_motion_release':False}),'RESULTS')
    compare(documents['FINISH.json'],{'status':'AWAITING_DISTINCT_SAVED_CHECKER','call_names':NAMES,
        'call_count':11,'native_motion_release':False,'producer_check_flag':True,
        'resource_acceptance':'EXTERNAL_ROOT_SUPERVISOR_REQUIRED'},'FINISH')
    for name,raw in raws.items():need((root/name).read_bytes()==raw,'closing saved bytes '+name)
    result={'status':'INDEPENDENT_FIXED_METHOD_SAVED_COMPARISON_PASS','source_author':'Codex2',
        'complete_files':26,'positive_calls':4,'actual_refusals':7,
        'output_files':{n:{'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for n,v in raws.items()},
        'comparison_absolute_tolerance':2e-12,'input_method_tolerance':1e-9,
        'native_motion_release':False,'physical_prediction_released':False,
        'resource_acceptance':'ROOT_ORIGINAL_SUPERVISOR_CLOSURE_REQUIRED_SEPARATELY',
        'requires_distinct_root_adjudication':True}
    with args.output.open('x') as f:
        json.dump(result,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

if __name__=='__main__':main()
