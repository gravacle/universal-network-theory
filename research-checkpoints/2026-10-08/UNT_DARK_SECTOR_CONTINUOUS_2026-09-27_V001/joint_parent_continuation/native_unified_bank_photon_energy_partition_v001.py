"""Prospective saved-only autonomous-bank assessment; root execution only."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import argparse,hashlib,json,math,os,time
BASE=Path(__file__).resolve().parent
STEM='NATIVE_UNIFIED_BANK_PHOTON_ENERGY_PARTITION_V001'
PROTOCOL_SHA='4158a8ed7e9323fc8be162e62440340b5eb68d91d179a53665d6e51368214f86'
PINS={
 'native_canonical_maxwell_pair_v003.py':'3bb87715229c29719c2246289d5650359e72f1c34ffbbbc4a8c9536e31713e56',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003.md':'f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json':'f74554aa51beb5756fb4da8608a436f29d1efeb2e0958c808d7873ff09d9a1ff',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json':'2fa61745ad09a1aeafee078539f59f4de5258231e5794b0b0ce7c212fd5b2ec2'}
IDS=('q','edge','omega','kappa','tau','preparation','age')
ROW_KEYS={'M','age','cutoff_probability','each_polarization_mean_photon_number','edge','field_lapse_contact','field_metric_second_contact','field_mixed_N_psi_contact','field_spatial_first_contact','ground_control','initial_norm','interaction_energy','kappa','kappa_first_contact','kappa_second_contact','ledger_residual','native_change','native_energy','native_energy_initial','native_lapse_contact','native_release','net_switch_work','norm','omega','pair_number','photon_change','photon_energy_initial','photon_free_energy','photon_number','preparation','q','steps','switch_off_work','switch_on_work','tau','total_lapse_contact','total_on_energy'}
PAIR_KEYS=set(IDS)|{'joint_state_error','kind','left_M','left_steps','right_M','right_steps','signed_changes'}
CHANGE_KEYS={'interaction_energy','kappa_first_contact','kappa_second_contact','native_change','net_switch_work','photon_change','photon_number'}
CONFIG={'ages':[0.,.5,2.],'cutoff_probability_tolerance':2e-8,'cutoffs':[8,12,16],'durations':[.25,1.,2.],'energy_tolerance':2e-8,'incidences':[0,3],'kappas':[0.,-.001,.001],'native_preparations':['cycle','tree'],'norm_tolerance':2e-11,'omegas':[.5,1.,2.],'operator_tolerance':2e-10,'record_occupations':[0,1],'state_tolerance':2e-8,'steps':[128,256]}
SCOPE='Saved constant-H plateau energy-source partition; no thermal, escaped-radiation, macroscopic-phase, matter, BBN, formation or inflation qualification'

def require(ok,msg):
    if not ok:raise AssertionError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def read(name):return json.loads((BASE/name).read_text())
def finite_tree(x):
    if x is None or type(x) in (bool,int,str):return
    if type(x) is float:require(math.isfinite(x),'Finite serialized float');return
    if type(x) is list:
        for v in x:finite_tree(v)
        return
    if type(x) is dict:
        require(all(type(k) is str for k in x),'String keys')
        for v in x.values():finite_tree(v)
        return
    raise AssertionError('Unexpected serialized value')
def canonical(x):
    finite_tree(x);return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,obj):
    data=canonical(obj);p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);return sha(p)
def ratio(n,d):
    if d==0:return {'value':None,'status':'ZERO_DENOMINATOR','numerator':n,'denominator':d}
    v=n/d
    return {'value':v if math.isfinite(v) else None,'status':'FINITE' if math.isfinite(v) else 'NONFINITE_RATIO_REFUSED','numerator':n,'denominator':d}
def identity(r):return tuple(r[k] for k in IDS)
def row_identity(r):return identity(r)+(r['M'],r['steps'])
def pair_identity(c):return identity(c)+(c['kind'],c['left_M'],c['left_steps'],c['right_M'],c['right_steps'])
def partition(r):
    D=-r['native_change'];G=r['photon_change'];S=r['switch_on_work']-r['interaction_energy'];R=r['ledger_residual']
    return dict(native_debit=D,photon_gain=G,initial_interaction_storage=r['switch_on_work'],interaction_storage_release=S,original_ledger_residual=R,independent_partition_leftover=math.fsum([G,-D,-S,-R]),native_fraction=ratio(D,G),storage_fraction=ratio(S,G),ledger_fraction=ratio(R,G),actuator_work_during_plateau=0.,hypothetical_switch_off_is_applied=False)
def pair_differences(c):
    d=c['signed_changes']
    return dict(native_debit_difference=-d['native_change'],photon_gain_difference=d['photon_change'],storage_release_difference=-d['interaction_energy'],original_interaction_difference=d['interaction_energy'],original_net_switch_difference=d['net_switch_work'],joint_state_error=c['joint_state_error'])
def check_inputs(seals,source_sha):
    require(sha(__file__)==source_sha,'Executing source changed')
    for n,h in seals.items():require(sha(BASE/n)==h,'Direct input changed '+n)
def authenticate(seals,source_sha):
    check_inputs(seals,source_sha);d=read('NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json');r=read('NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json')
    finite_tree(d);finite_tree(r)
    require(d['status']==r['status']=='CANONICAL_MAXWELL_FIXTURE_PASS','Closed accepted numerical parent')
    require(r['source_sha256']==PINS['native_canonical_maxwell_pair_v003.py'] and r['result_sha256']==PINS['NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json'],'Source/result receipt binding')
    require(r['input_sha256'][str(BASE/'NATIVE_CANONICAL_MAXWELL_PAIR_V003.md')]==PINS['NATIVE_CANONICAL_MAXWELL_PAIR_V003.md'],'Original protocol receipt binding')
    require(r['output_sha256'][str(BASE/'NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json')]==r['result_sha256'],'Original result output binding')
    require(d['manifest']['source_sha256']==r['source_sha256'] and d['manifest']['input_sha256']==r['input_sha256'],'Whole parent source/input map binding')
    require(d['configuration']==d['manifest']['configuration']==CONFIG and d['checkpoint_count']==r['checkpoint_count']==216,'Exact inherited configuration and closure count')
    require(d['physical_rates_or_thermalization_qualified'] is False,'Physical qualification remains false')
    rows=d['rows'];pairs=d['comparisons'];checks=d['checks']
    require(len(rows)==4536 and len(pairs)==3780 and len(checks)==34256,'Complete original census')
    require(all(set(v)==ROW_KEYS and type(v['ground_control']) is bool for v in rows),'Original complete row schema')
    require(all(set(v)==PAIR_KEYS and set(v['signed_changes'])==CHANGE_KEYS for v in pairs),'Original complete comparison schema')
    require(all(type(v['passed']) is bool for v in checks),'Original criterion dispositions')
    expected=[]
    preps=[(p,a) for p in CONFIG['native_preparations'] for a in CONFIG['ages']]+[('complete_native_ground',None)]
    for q in CONFIG['record_occupations']:
      for e in CONFIG['incidences']:
       for o in CONFIG['omegas']:
        for k in CONFIG['kappas']:
         for M in CONFIG['cutoffs']:
          for n in CONFIG['steps']:
           for t in CONFIG['durations']:
            for p,a in preps:expected.append((q,e,o,k,t,p,a,M,n))
    require([row_identity(v) for v in rows]==expected,'Original all-row order without sign selection')
    require(all(v['ground_control']==(v['preparation']=='complete_native_ground') for v in rows),'Complete bare native ground controls')
    rowmap={row_identity(v):v for v in rows};pairmap={pair_identity(v):v for v in pairs}
    require(len(rowmap)==4536 and len(pairmap)==3780,'Unique descriptors')
    for c in pairs:
        require(c['kind'] in ('time','cutoff'),'Original comparison kind')
        require(identity(c)+(c['left_M'],c['left_steps']) in rowmap and identity(c)+(c['right_M'],c['right_steps']) in rowmap,'Comparison endpoint rows present')
    return d,r,pairmap

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args();require(args.root_owned,'Root launch authorization flag required')
    started=utc();clock=time.monotonic();source_sha=sha(__file__);seals={**PINS,STEM+'.md':PROTOCOL_SHA}
    names=[STEM+s for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
    require(not any((BASE/n).exists() for n in names),'Exclusive publication; no resume or overwrite')
    d,parent_receipt,pairmap=authenticate(seals,source_sha);assessed=[];finest=[]
    for row in d['rows']:
        part=partition(row);assessed.append(dict(original_row=row,partition=part))
        if (row['M'],row['steps'])!=(16,256):continue
        key=identity(row)
        time_pair=pairmap[key+('time',16,128,16,256)];cut_pair=pairmap[key+('cutoff',12,256,16,256)]
        td=pair_differences(time_pair);cd=pair_differences(cut_pair);empirical={}
        for contribution,difference in (('native_debit','native_debit_difference'),('photon_gain','photon_gain_difference'),('interaction_storage_release','storage_release_difference')):
            scale=max(abs(td[difference]),abs(cd[difference]),abs(part['original_ledger_residual']))
            empirical[contribution]=dict(empirical_change_scale=scale,signed_contribution_over_scale=ratio(part[contribution],scale),time_signed_difference=td[difference],cutoff_signed_difference=cd[difference],ledger_residual=part['original_ledger_residual'],uncertainty_bound_qualified=False)
        finest.append(dict(descriptor={k:row[k] for k in (*IDS,'M','steps')},ground_control=row['ground_control'],partition=part,original_time_comparison=time_pair,original_cutoff_comparison=cut_pair,time_differences=td,cutoff_differences=cd,empirical_resolution=empirical))
    require(len(assessed)==4536 and len(finest)==756 and sum(v['descriptor']['kappa']!=0 for v in finest)==504 and sum(v['descriptor']['kappa']==0 for v in finest)==252,'Inherited finest complete census')
    original_checks=dict(parent_result_sha256=PINS['NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json'],json_field='checks',count=34256,passed=sum(v['passed'] for v in d['checks']),failed=sum(not v['passed'] for v in d['checks']),kind_counts=dict(Counter(v['kind'] for v in d['checks'])),unchanged=True)
    result=dict(status='SAVED_ENERGY_PARTITION_READOUT_COMPLETE',scope=SCOPE,owner='root',pid=os.getpid(),started_utc=started,source_sha256=source_sha,input_sha256=seals,original_parent_status=d['status'],original_numerical_checks=original_checks,parent_receipt_ancestry=dict(input_count=len(parent_receipt['input_sha256']),output_count=len(parent_receipt['output_sha256']),complete_receipt_sha256=PINS['NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json'],historical_replay_performed=False),rows=assessed,original_comparisons=d['comparisons'],finest_rows=finest,counts=dict(all_rows=4536,all_comparisons=3780,finest_rows=756,finest_nonzero_coupling=504,finest_zero_coupling=252),physical_qualifications={k:False for k in ('escaped_radiation','thermalization','irreversibility','macroscopic_PX_emergence','ordinary_matter_origin','BBN_history','formation','inflation','empirical_resolution_as_uncertainty')},elapsed_seconds=time.monotonic()-clock)
    check_inputs(seals,source_sha);outputs={};outputs[names[0]]=write(names[0],result)
    report='# Unified native bank and photon energy partition\n\nSAVED_ENERGY_PARTITION_READOUT_COMPLETE\n\nAll 4536 original rows and 3780 comparisons are retained; all 34256 original criteria remain bound unchanged. The inherited finest census has 756 rows (504 nonzero coupling and 252 zero controls), with both original time and cutoff comparisons.\n\nConstant plateau actuator work is zero. Photon gain equals native debit plus initial-interaction-storage release plus the original ledger residual. The original W_on denotes preparation energy here; W_off remains hypothetical. All signs and zero-denominator refusals are retained. Empirical contribution/change ratios are descriptive, not new physical pass or uncertainty bounds.\n\nThis finite homogeneous closed fixture does not derive escaped radiation, thermalization, macroscopic P(X), matter budgets, BBN, formation or inflation.\n'
    p=BASE/names[1]
    with p.open('xb') as f:f.write(report.encode())
    p.chmod(0o444);outputs[names[1]]=sha(p);check_inputs(seals,source_sha)
    receipt=dict(status=result['status'],owner='root',pid=os.getpid(),started_utc=started,completed_utc=utc(),source_sha256=source_sha,input_sha256=seals,before_after_direct_inputs_identical=True,output_sha256=outputs,counts=result['counts'])
    write(names[2],receipt);check_inputs(seals,source_sha)
    for n,h in outputs.items():require(sha(BASE/n)==h,'Published readout changed')
    print(json.dumps(dict(status=result['status'],rows=4536,finest_rows=756,elapsed_seconds=result['elapsed_seconds'])));return 0

if __name__=='__main__':raise SystemExit(main())
