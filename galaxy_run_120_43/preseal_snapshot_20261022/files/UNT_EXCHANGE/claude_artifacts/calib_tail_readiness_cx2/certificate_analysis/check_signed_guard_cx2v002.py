"""Synthetic signed-source guard tests; not a scientific source certificate."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('guard_v002',HERE/'certificate_guard_cx2v002.py')
G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
OUT=HERE/'synthetic_signed_checks_v002';OUT.mkdir(exist_ok=False)
n=0
def pin(obj):
    global n
    n+=1;p=OUT/('fixture_%03d.json'%n);raw=G.canonical(obj)+b'\n'
    with p.open('xb') as f:f.write(raw)
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}
producer={'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
original=json.loads((HERE/'synthetic_checks_v001/synthetic_004.json').read_bytes())
# The first v001 manifest is fixture4; source pin changes only the synthetic
# proof producers, which this test intentionally approves.
assert original['schema']==G.SCHEMA
doc=copy.deepcopy(original)
for name,ref in doc['prelaunch'].items():
    obj=json.loads(Path(ref['path']).read_bytes());obj['producer']=producer;doc['prelaunch'][name]=pin(obj)
state=doc['states'][0]['state'];state['nonnegative_masses']=False
lo=json.loads(Path(doc['states'][0]['LO']['path']).read_bytes())
lo['producer']=producer;lo['state']=state;lo['GQ_uniform_proof_sha256']=doc['prelaunch']['GQ']['sha256']
doc['states'][0]['LO']=pin(lo)
gq=json.loads(Path(doc['prelaunch']['GQ']['path']).read_bytes())
bound=gq['max_column_difference_over_analytic_Pi0']/(1-gq['max_zero_mode_relative_error'])
signed={k:lo[k] for k in ('schema','status','verdict','producer','point_sha256','custody_sha256')}
signed.update(gate='GQ_SIGNED',state=state,method='TV_BOUND_WITH_SIGNED_P0',normalization='ABS_SIGNED_ZERO_MODE',
    positive_components_verified=True,GQ_uniform_proof_sha256=doc['prelaunch']['GQ']['sha256'],
    P0_abs_signed_mass_kg=1.,component_mass_sum_kg=2.,max_difference_over_signed_P0_bound=bound*2)
checks=[]
def run(name,obj,expected):
    d=copy.deepcopy(doc)
    if obj is not None:d['states'][0]['GQ_SIGNED']=pin(obj)
    result=G.verify_bundle(pin(d),d['identity'],expected_custody=d['custody'],
        approved_producer_sha256=[producer['sha256']],phase='acceptance',required_states=[state])
    checks.append({'name':name,'expected':expected,'actual':result['ok'],'blockers':result['blockers']})
    assert result['ok']==expected,name
run('positive_component_TV_bound_pass',signed,True)
run('missing_signed_proof',None,False)
s=copy.deepcopy(signed);s['P0_abs_signed_mass_kg']=0.;run('zero_signed_P0',s,False)
s=copy.deepcopy(signed);s['P0_abs_signed_mass_kg']=1e-6;s['max_difference_over_signed_P0_bound']=bound*2e6;run('near_cancellation_amplifies_error',s,False)
s=copy.deepcopy(signed);s['normalization']='TOTAL_VARIATION_MASS';run('silent_renormalization_refused',s,False)
s=copy.deepcopy(signed);s['max_difference_over_signed_P0_bound']=0.;run('contradictory_bound_refused',s,False)
out={'status':'TESTED_SYNTHETIC_ONLY','checks':checks,'all_passed':True,
     'waiver':'nice unavailable (sandbox); 0514 waiver','peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
with (OUT/'RESULT.json').open('xb') as f:f.write(G.canonical(out)+b'\n')
print(json.dumps({'checks':len(checks),'all_passed':True,'rss':out['peak_rss_bytes']}))
