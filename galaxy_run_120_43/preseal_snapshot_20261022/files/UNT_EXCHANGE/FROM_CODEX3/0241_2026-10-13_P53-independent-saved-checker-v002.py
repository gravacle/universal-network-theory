"""Codex3 P53 complete saved checker SOURCE ONLY; root runs after distinct review.
Exact literal/metadata comparisons, no parsing/recomputing astrophysical numbers.
No producer, guard, fixture or scientific-library import. Expected37files/16calls.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
CONFIG=ROOT/'P53_TRANSPORT_CONFIG_V001.json'
CONFIG_PIN='22d14ba84a742378fde40d8c92a94e170ddf8fa045b6a0d13ee1e6c3c33290fb'
RUNNER=ROOT/'P53_TRANSPORT_PRODUCER_V001.py'
RUNNER_PIN='1ec38501d3332913e1a088f37b089f0cc9b212197c58b67d76642b861f3b7725'


def need(x,why):
    if not x:raise ValueError(why)


def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate key');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def raw_bounded(path,limit=2**20):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular file')
    with path.open('rb') as stream:raw=stream.read(limit+1)
    need(len(raw)<=limit,'bounded read')
    return raw


def read(path,limit=2**20):
    return decode(raw_bounded(path,limit))


def wire(value):
    if type(value) is bytes:return {'__bytes_hex__':value.hex()}
    if isinstance(value,dict):return {k:wire(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [wire(v) for v in value]
    return value


def check(directory):
    output_limit=10*2**20
    need(directory.is_dir() and not directory.is_symlink(),'regular output directory')
    expected={'START.json','SOURCE_SNAPSHOTS.json','INPUT_BYTES.json','RESULTS.json','FINISH.json'}
    expected.update('CALL_%02d_%s.json'%(i,phase) for i in range(16) for phase in ('PRE','RETURN'))
    entries=list(directory.iterdir())
    need(len(entries)==37 and {p.name for p in entries}==expected,'prospective complete flat37file census')
    need(all(p.is_file() and not p.is_symlink() and p.stat().st_size<=output_limit for p in entries),
         'bounded regular output files')
    need(sum(p.stat().st_size for p in entries)<=output_limit,'prospective whole output10MiB cap')
    need(hashlib.sha256(raw_bounded(CONFIG)).hexdigest()==CONFIG_PIN,'config pin')
    need(hashlib.sha256(raw_bounded(RUNNER)).hexdigest()==RUNNER_PIN,'runner pin')
    cfg=read(CONFIG)
    need(set(cfg)=={'scope','sources','inputs'} and cfg['scope']=='P53_FIXED_LITERAL_TRANSPORT_ONLY','config schema')
    need(set(cfg['sources'])=={'guard','controls'} and set(cfg['inputs'])=={'freeze','density','acceptance'},'roles')
    originals={};sources={}
    for group,destination in [('sources',sources),('inputs',originals)]:
        for role,pin in cfg[group].items():
            raw=raw_bounded(Path(pin['path']))
            need(len(raw)<=2**20 and hashlib.sha256(raw).hexdigest()==pin['sha256'],'original pin '+role)
            destination[role]=raw
    seen={};consumed=0
    def same(name,expected):
        nonlocal consumed
        p=directory/name;raw=raw_bounded(p,output_limit)
        consumed+=len(raw)
        need(consumed<=output_limit,'whole consumed output10MiB cap')
        actual=decode(raw)
        need(actual==wire(expected),'mismatch '+name)
        seen[name]=hashlib.sha256(raw).hexdigest()
    same('START.json',{'config':cfg,'config_sha256':CONFIG_PIN,'runner_sha256':RUNNER_PIN,
                      'scope':'P53_LITERAL_TRANSPORT_ONLY','physical_prediction_released':False})
    same('SOURCE_SNAPSHOTS.json',{k:v.decode() for k,v in sources.items()})
    same('INPUT_BYTES.json',originals)
    freeze=decode(originals['freeze']);data=decode(originals['density']);acceptance=decode(originals['acceptance'])
    need(freeze['data']==cfg['inputs']['density'] and acceptance['source']==cfg['inputs']['freeze'],'acceptance ancestry')
    need(acceptance['status']=='PASS_LITERAL_DOCUMENTARY_ONLY','literal scope')
    archived=data['value']['rows']
    need(len(archived)==23 and [r['original_line_number'] for r in archived]==list(range(320,343)),'all source rings')
    projected=[]
    for row in archived:
        p={'source_line':row['original_line_number'],'radius_kpc':row['radius_kpc'],
           'radius_over_r25':row['radius_over_r25']}
        for k in ('HI','H2','stars'):
            cell=row[k];v=cell['published_value'];e=cell['published_error_field']
            semantic='PUBLISHED_FIELD_NO_LIKELIHOOD_ADOPTED'
            if v is None:semantic='MISSING_NO_ZERO_OR_LIMIT'
            if k in ('HI','stars') and e=='1':semantic='UNRESOLVED_NOTE3_CONFLICT'
            p[k]={'published_value':v,'published_error_field':e,'missing':v is None,
                  'statistical_interpretation':semantic,'likelihood_permitted':False}
        projected.append(p)
    need(sum(r['H2']['missing'] for r in projected)==13,'all thirteen missing molecular rows')
    need(projected[2]['stars']['published_value']=='105' and projected[2]['stars']['published_error_field']=='1',
         'specific conflicted literal retained')
    slots=('native_matter_coupling','native_response','native_motion_law',
           'target_free_43_query_manifest','selected_complete_joint_source')
    need(all(freeze[k] is None for k in slots),'incomplete native slots')
    provider={'schema':'P53_TARGET_FREE_LITERAL_TRANSPORT_V001','scope':'TRANSPORT_ONLY_NOT_NATIVE_READY',
        'galaxy':freeze['galaxy'],'representation':'MASS_SURFACE_DENSITY','units':'Msun/pc^2',
        'rows':projected,'choices':deepcopy(freeze['choices']),
        'empirical_accounting':deepcopy(freeze['accounting']),
        'source_sha256':{k:p['sha256'] for k,p in cfg['inputs'].items()},
        'native_interfaces':{k:None for k in slots},'complete_43_source':False,'native_ready':False,
        'likelihood_permitted':False,'physical_prediction_released':False}
    bundle={'provider_payload':provider,'custody_only':{'whole_freeze':freeze,
        'complete_density_return':data,'literal_acceptance':acceptance,'input_pins':cfg['inputs'],
        'do_not_supply_to_native_callbacks':True},
        'status':'LOSSLESS_CUSTODY_WITH_MINIMIZED_TRANSPORT_ONLY','native_ready':False,
        'complete_43_source':False,'physical_prediction_released':False}
    args=[originals[k] for k in ('freeze','density','acceptance')]
    cases=[]
    def add(name,function,arguments,expected,result=None,message=None):
        case={'id':name,'function':function,'args':deepcopy(arguments),'expected':expected}
        if message is not None:case['message']=message
        cases.append((case,result,message))
    add('transport','transport_literal',args,'TRANSPORT_ONLY',bundle)
    for i,role in enumerate(('freeze','density','acceptance')):
        changed=list(args);changed[i]+=b' '
        add('corrupt_'+role,'transport_literal',changed,'ValueError',message='whole '+role+' hash')
    for mode in ('GAUSSIAN','UPPER_LIMIT','NATIVE_READY','COMPLETE_43'):
        add('operation_'+mode,'transport_literal',args+[mode],'ValueError',message='no statistical/native-source operation')
    add('checked_transport','checked_provider_payload',[bundle]+args,'MINIMIZED_PAYLOAD',provider)
    for mode in ('GAUSSIAN','UPPER_LIMIT'):
        add('likelihood_'+mode,'request_likelihood',[bundle,mode],'ValueError',
            message='UNRESOLVED source semantics/covariance: neither Gaussian nor upper-limit likelihood authorized')
    add('native_source','request_native_source',[bundle],'ValueError',
        message='INCOMPLETE support/geometry/query/native map: no native-ready43 source')
    for name in ('target_injection','annotation_unquarantine','readiness_promotion','drop_custody'):
        b=deepcopy(bundle)
        if name=='target_injection':b['provider_payload']['vobs']=[1]*43
        if name=='annotation_unquarantine':b['provider_payload']['rows'][2]['stars']['statistical_interpretation']='GAUSSIAN'
        if name=='readiness_promotion':b['provider_payload']['native_ready']=True
        if name=='drop_custody':del b['custody_only']['complete_density_return']
        add(name,'checked_provider_payload',[b]+args,'ValueError',message='whole transport bundle changed or target content injected')
    rows=[]
    need(len(cases)==16,'case census')
    for i,(case,result,error) in enumerate(cases):
        same('CALL_%02d_PRE.json'%i,case)
        row={'id':case['id'],'refused':error is not None,'arguments_after':case['args']}
        if error:row.update(exception='ValueError',message=error)
        else:row['value']=result
        same('CALL_%02d_RETURN.json'%i,row);rows.append(row)
    same('RESULTS.json',{'calls':rows,'call_count':16,'physical_prediction_released':False})
    same('FINISH.json',{'status':'AWAITING_INDEPENDENT_SAVED_CHECKER','call_count':16,'physical_prediction_released':False})
    need(len(seen)==37 and {p.name for p in directory.iterdir()}==set(seen),'complete flat37file census')
    return {'status':'PASS_LITERAL_TRANSPORT_AND_QUARANTINE_METHOD_ONLY','files':37,'calls':16,
        'whole_source_rows':23,'component_cells':69,'actual_refusals':14,'saved_sha256':seen,
        'native_ready':False,'likelihood_permitted':False,'physical_prediction_released':False,
        'resource_acceptance':'ROOT_SEPARATE_GATE','comparison':'EXACT_LITERAL_AND_METADATA_NO_NUMERIC_CONVERSION'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.directory),indent=2,allow_nan=False))
