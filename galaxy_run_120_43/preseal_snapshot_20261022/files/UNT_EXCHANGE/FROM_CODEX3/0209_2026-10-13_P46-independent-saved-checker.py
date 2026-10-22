"""Codex3 SOURCE ONLY independent reader; root runs after distinct source review.
Exact manufactured integer expectations; score tolerance 0 (all terms exactly1).
No producer/harness/fixture import. Complete70-file/20-call census.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
RUNNER = ROOT/'P46_METHOD_PRODUCER_V001.py'
RUN_PIN = 'd6d01f93ee25dff9fa4fa4370e82fbf44bf1c9a87f46b95409ad9595b7ea6066'
CONFIG = ROOT/'P46_METHOD_CONFIG_V001.json'
CONFIG_PIN = 'bfa6c074a8ef53b75f041b4b556bd96134a16006daf9d133813e259b544cbde9'
PINS = {'harness':'5a18ba208d18abf60063fb411770b3b3356c289215f1fced116128311abf5615',
        'fixtures':'d8a7dca2e294d3db18ed662a81160a33555ed390eb9c3770dadb3cad4225bda4'}


def need(x, why):
    if not x:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def read(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size<=2**20,'bounded regular file')
    def pairs(items):
        result={}
        for k,v in items:
            need(k not in result,'duplicate key')
            result[k]=v
        return result
    return json.loads(path.read_text(),object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def context():
    return {'scope':'METHOD_ONLY','query_ids':['METHOD:%02d'%i for i in range(43)],
        'query_definition':{'kind':'43 manufactured labels, no spatial geometry'},
        'source_bundle':{'kind':'SYNTHETIC','values':list(range(1,44))},
        'choice_ledger':{'source':'manufactured sequence; no empirical density'},
        'calibration':{'scope':'METHOD_ONLY',
            'coordinate':{'name':'A','value':2,'units':'km/s','observation_id':'SYNTHETIC_ONLY',
                          'fit_role':'MANUFACTURED_CALIBRATION_FIXTURE'},
            'empirical_inputs':[],'premises':['manufactured A=2, not physical calibration'],
            'P8_acceptance':None,'P9_freeze':None}}


def payload(stage,state,ids):
    return {'scope':'METHOD_ONLY','stage':stage,'query_ids':ids,'full_state':state,
        'error_budget':{'kind':'EXACT_INTEGER_MANUFACTURED_ARITHMETIC'},
        'meaning':'Nonlocal nonlinear composition fixture, not native physics'}


def check(directory):
    for path,pin in [(RUNNER,RUN_PIN),(CONFIG,CONFIG_PIN)]:
        need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'source/config pin')
    config=read(CONFIG)
    need(set(config)=={'sources','scope'} and config['scope']=='METHOD_ONLY_FIXED_CASES','config schema')
    need(set(config['sources'])==set(PINS),'roles')
    for role,pin in PINS.items():
        item=config['sources'][role]
        need(item['sha256']==pin and hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==pin,'role pin')
    files=set()
    hashes={}
    def actual(name):
        files.add(name)
        p=directory/name
        value=read(p)
        hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        return value
    def same(name,expected):
        need(actual(name)==expected,'mismatch '+name)
    same('START.json',{'scope':'MANUFACTURED_P46_METHOD_ONLY','config':config,
        'config_sha256':CONFIG_PIN,'runner_sha256':RUN_PIN,'physical_prediction_released':False})
    snapshots=actual('SOURCE_SNAPSHOTS.json')
    need(set(snapshots)==set(PINS),'snapshot roles')
    for role,pin in PINS.items():
        need(hashlib.sha256(snapshots[role].encode()).hexdigest()==pin,'snapshot pin')

    calls=[]
    def call(tag,function,before,value=None,after=None,error=None):
        index=len(calls)
        pre={'tag':tag,'function':function,'arguments_before':deepcopy(before)}
        ret={'tag':tag,'arguments_after':deepcopy(before if after is None else after)}
        if error is None:ret['value']=deepcopy(value)
        else:ret.update(exception='ValueError',message=error)
        same('CALL_%04d_PRE.json'%index,pre)
        same('CALL_%04d_RETURN.json'%index,ret)
        calls.append(index)

    names=['positive','total_null','perturbed','bad_query_count','missing_source',
           'target_in_context','bad_calibration_scope','fake_P8','native_context',
           'mutating_provider','injected_target','missing_velocity']
    errors={'bad_query_count':'43 unique ordered queries','missing_source':'whole source bundle',
        'target_in_context':'target/template field in provider input',
        'bad_calibration_scope':'no physical calibration execution',
        'fake_P8':'method declaration cannot mock physical acceptance',
        'native_context':'native execution unavailable','mutating_provider':'provider mutated input',
        'injected_target':'target/template field in provider input',
        'missing_velocity':'complete ordered velocities'}
    outer=[]; sealed=None
    for name in names:
        ctx=context(); ids=deepcopy(ctx['query_ids'])
        providers={s:s for s in ('matter','response','motion')}
        if name=='total_null':providers['response']='zero_response'
        if name=='perturbed':ctx['source_bundle']['values'][0]=2
        if name=='bad_query_count':ctx['query_ids'].pop()
        if name=='missing_source':ctx['source_bundle']={}
        if name=='target_in_context':ctx['vobs']=[1]*43
        if name=='bad_calibration_scope':ctx['calibration']['scope']='NATIVE'
        if name=='fake_P8':ctx['calibration']['P8_acceptance']='fake'
        if name=='native_context':ctx['scope']='NATIVE'
        if name=='mutating_provider':providers['matter']='mutating_matter'
        if name=='injected_target':providers['response']='target_injection'
        if name=='missing_velocity':providers['motion']='wrong_query_motion'
        refusal=name in errors
        same(name+'_INPUT.json',{'context':ctx,'providers':providers,'expects_refusal':refusal})
        first=len(calls); stages={}
        if name not in names[3:9]:
            for stage in ('matter','response','motion'):
                request={'context':deepcopy(ctx),'upstream':deepcopy(stages)}
                changed=deepcopy(request)
                if stage=='matter':
                    if name=='mutating_provider':changed['context']['source_bundle']['values'][0]=999
                    state=deepcopy(changed['context']['source_bundle'])
                elif stage=='response':
                    xs=stages['matter']['full_state']['values']
                    # Independent closed form for frozen fixtures; do not call producer response.
                    values=[0]*43 if name=='total_null' else [k*k+946 for k in range(1,44)]
                    if name=='perturbed':values=[951]+[k*k+947 for k in range(2,44)]
                    need(len(xs)==43,'whole matter state')
                    state={'values':values,'original_matter':deepcopy(stages['matter'])}
                else:state=deepcopy(stages)
                value=payload(stage,state,ids)
                if name=='injected_target' and stage=='response':value['vobs']=[1]*43
                if stage=='motion':
                    velocities=[2*(k*k+946) for k in range(1,44)]
                    if name=='total_null':velocities=[0]*43
                    if name=='perturbed':velocities=[1902]+[2*(k*k+947) for k in range(2,44)]
                    value.update(units='km/s',semantics='TOTAL_OBSERVABLE',
                                 rows=[{'id':i,'velocity':v} for i,v in zip(ids,velocities)])
                    if name=='missing_velocity':value['rows'].pop()
                call('P46_LINE_A_'+stage,providers[stage],[request],value,[changed])
                if (name=='mutating_provider' and stage=='matter') or (name=='injected_target' and stage=='response'):
                    break
                stages[stage]=deepcopy(value)
        row={'name':name,'refused':refusal,'expects_refusal':refusal,'first_call':first,'after_call':len(calls)}
        if refusal:row.update(exception='ValueError',message=errors[name])
        else:
            pred={'scope':'LINE_A_HARNESS_METHOD_ONLY','context':ctx,'stages':stages,
                'query_ids':ids,'rows':deepcopy(stages['motion']['rows']),
                'calibration':deepcopy(ctx['calibration']),'fitted_coordinates':1,
                'empirical_identifying_rank':None,'physical_prediction_released':False}
            result={'prediction':pred,'prediction_sha256':digest(pred)}
            row['value']=result
            if name=='positive':sealed=deepcopy(result)
        same(name+'_RETURN.json',row);outer.append(row)

    same('PREDICTION_SEAL.json',sealed)
    obs=[{'id':'METHOD:%02d'%i,'velocity':2*((i+1)**2+946)+1,'sigma':1} for i in range(43)]
    same('OBSERVATIONS.json',obs)
    need((directory/'PREDICTION_SEAL.json').stat().st_mtime_ns <= (directory/'OBSERVATIONS.json').stat().st_mtime_ns,
         'seal timestamp after observations')
    scores=[]
    for name in ('score','zero_error','observation_order','changed_prediction'):
        pred=deepcopy(sealed); observations=deepcopy(obs)
        if name=='zero_error':observations[0]['sigma']=0
        if name=='observation_order':observations[0],observations[1]=observations[1],observations[0]
        if name=='changed_prediction':pred['prediction']['rows'][0]['velocity']+=1
        error={'zero_error':'positive quoted error','observation_order':'exact observation order',
               'changed_prediction':'changed prediction'}.get(name)
        value={'chi2':43,'rows':[{'id':o['id'],'residual':-1,'chi2_contribution':1} for o in obs],
            'prediction_sha256':sealed['prediction_sha256'],'calibration':deepcopy(context()['calibration']),
            'fitted_coordinates':1,'empirical_identifying_rank':None,
            'error_model':'CONDITIONAL_QUOTED_DIAGONAL_ONLY_NOT_FULL_COVARIANCE',
            'blind_test_claim':False,'physical_prediction_released':False}
        call('P46_'+name,'score_diagonal_method',[pred,observations],value,error=error)
        row={'name':name,'refused':error is not None,'expects_refusal':error is not None}
        if error:row.update(exception='ValueError',message=error)
        else:row['value']=value
        scores.append(row)
    message='Missing accepted line-A matter/response/motion, source closure and P8/P9/root release'
    call('P46_native_refusal','predict_native',[],error=message)
    native={'refused':True,'exception':'ValueError','message':message}
    need(len(calls)==20,'exact call census')
    same('RESULTS.json',{'composition_cases':outer,'score_cases':scores,'native_refusal':native,
                        'call_count':20,'physical_prediction_released':False})
    same('FINISH.json',{'status':'AWAITING_DISTINCT_SAVED_CHECKER','physical_prediction_released':False,'call_count':20})
    need(len(files)==70 and {p.name for p in directory.iterdir()}==files,'whole flat file census')
    return {'status':'PASS_FIXED_P46_METHOD_CUSTODY_AND_VALUES','files':70,'actual_calls':20,
        'comparison':'EXACT_MANUFACTURED_INTEGER_VALUES_NO_TOLERANCE','saved_sha256':hashes,
        'physical_prediction_released':False,'resource_acceptance':'ROOT_SEPARATE_SUPERVISOR_GATE'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.directory),indent=2,allow_nan=False))
