#!/usr/bin/env python3
"""Independent A99 structural review; protected and scientific loaders excluded."""
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()
HERE=Path(__file__).absolute().parent
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PINS=[]
CHECKS=[]
ATTEMPTS=[]

def protected(p):
    if not isinstance(p,(str,bytes,os.PathLike)):
        return
    s=os.fsdecode(p)
    if (any(v in s.split('/') for v in ('runs','runs_ext','.codex')) or 'KMAX_A2F10_C5H_RUN_V001' in s
            or 'NGC3198' in s or '/c5h_hull_c2/' in s):
        ATTEMPTS.append(s)
        raise PermissionError('protected path')
for name in ('stat','lstat','readlink','listdir','scandir'):
    old=getattr(os,name)
    def wrapped(p,*a,_old=old,**kw):
        protected(p)
        return _old(p,*a,**kw)
    setattr(os,name,wrapped)
def audit(event,args):
    if event in ('open','os.listdir','os.scandir'):
        protected(args[0])
    if event in ('subprocess.Popen','os.system','socket.connect','socket.__new__'):
        raise PermissionError('execution/network forbidden')
sys.addaudithook(audit)

def pairs(xs):
    d={}
    for k,v in xs:
        if k in d:
            raise ValueError('duplicate JSON key')
        d[k]=v
    return d
def read(rel,sha,text=False):
    p=A/rel
    b=p.read_bytes()
    if hashlib.sha256(b).hexdigest()!=sha:
        raise ValueError('byte mismatch: '+rel)
    PINS.append({'path':str(p),'sha256':sha,'kind':'observed_input'})
    if text:
        return b.decode()
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def check(name,ok,owner,detail=None):
    CHECKS.append({'name':name,'passed':bool(ok),'owner':owner,'detail':detail})

source=read('v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py',
            '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28',True)
cb=read('v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
        '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
build=read('v007_final_prereg_c4/r5/out/CASE_BLOCK_BUILD_C4V001.json',
           'bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad')
pre5=read('kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
          'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
pre6=read('kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json',
          '807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c')

tree=ast.parse(source)
nodes={x.name:x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
assigns={t.id:n for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
r5=ast.literal_eval(assigns['PIN_DRIVER_V010_R5'].value.elts[1])
c5sha=ast.literal_eval(assigns['PIN_C5H_SPEC'].value.elts[1])
grids={k:pre5['grids'][k]['composite_grid_spec'] for k in ('G2','G3','G4')}
grids.update({k:pre6['grids'][k]['composite_grid_spec'] for k in ('G5','G6')})
functions={'canon','_hex64','_num','jptr','duplicate_entry_code','unique_keys_codes','_hook_factory','loads_strict',
           'ra4_block_expected','_strip_keys','tail_content_codes','drop_mapped_keys'}
constants={'PRODUCTION_K_BIG_A55','PRODUCTION_GAS_M_S_A57','T3_KBIG_FACTOR','UV_TAIL_DIFFERING_KEYS',
           'C5C_OUTER','C4TA_LAMBDA_SCALE','CASE_BLOCK_SCHEMA','T_CASES','C5H','REGISTERED','EXPECTED_GRID',
           'EXPECTED_TRUNCATION','ROUTE_A_MAX_ITERATIONS','ROUTE_A_MODES','ROUTE_A_MODE_DEFAULT',
           'SEED_FACTOR_ABSENT_EQUIVALENT','UV_TAIL_MUST_DIFFER','CASE_ENTRY_KEYS_T','CASE_ENTRY_KEYS_C5H',
           'DRIVER_V009_EXT','KINDS'}
selected=[]
selected_functions=[]
for n in tree.body:
    if isinstance(n,ast.FunctionDef) and n.name in functions:
        selected.append(copy.deepcopy(n));selected_functions.append(n.name)
    elif isinstance(n,ast.ClassDef) and n.name=='DuplicateKey':
        selected.append(copy.deepcopy(n));selected_functions.append(n.name)
    elif isinstance(n,ast.Assign):
        targets=[t.id for t in n.targets if isinstance(t,ast.Name)]
        subscript=any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='EXPECTED_TRUNCATION' for t in n.targets)
        if any(t in constants for t in targets) or subscript:
            selected.append(copy.deepcopy(n))

original=nodes['validate_case_block']
fn=copy.deepcopy(original)
fn.name='validate_case_block_structural_slice'
cuts=[i for i,n in enumerate(fn.body) if isinstance(n,ast.If) and any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='c5h_numerics_reference' for x in ast.walk(n))]
assert len(cuts)==1 and cuts[0]==len(fn.body)-2
removed=fn.body[cuts[0]]
fn.body=fn.body[:cuts[0]]+[copy.deepcopy(fn.body[-1])]
selected.append(fn)
module=ast.fix_missing_locations(ast.Module(body=selected,type_ignores=[]))
# Prove no unauthorized imports or filesystem calls enter the extracted code.
assert not any(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(module))
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'open','Path','load_pinned_module','load_pinned_json','c5h_numerics_reference','build_context','read_all'} for n in ast.walk(module))
def forbidden_loader(*a,**kw):
    raise AssertionError('excluded loader was reached')
env={'json':json,'math':math,'PIN_C5H_SPEC':('UNOPENED_SOURCE_DECLARATION',c5sha),
     'sealed_driver_sha':lambda:r5,'registered_grids':lambda:copy.deepcopy(grids),
     'load_uvt_lib':forbidden_loader}
exec(compile(module,'<r12_structural_slice_only>','exec'),env)
validator=env['validate_case_block_structural_slice']
def run(x,mode=None):
    return validator(x,check_uv_link=False,route_a_mode=mode)

check('actual_candidate_structural_slice',run(cb)==[],'r12 retained structural slice',run(cb))
check('ten_T_plus_one_legacy_declaration',set(cb['cases'])==set(env['REGISTERED']) and len(env['T_CASES'])==10 and len(cb['cases'])==11,'independent closed set')
check('parallel8_and_empty_keymap',cb['route_a_mode']=='parallel8' and cb['key_equivalence_map']==[],'published contract')
check('builder_source_and_candidate_pins',build['compare']['sha256']==PINS[0]['sha256'] and build['case_block']['sha256']==PINS[1]['sha256'],'byte custody only; builder verdict not adopted')
summary={}
for lab in env['T_CASES']:
    e=cb['cases'][lab];n=e['normalized_spec_equal']['/numerics'];uv=n['uv_tail']
    check(lab+'/exact_registered_pointer_set',set(e['normalized_spec_equal'])=={'/numerics'},'independent candidate observation')
    check(lab+'/runtime_route_A_controls',n['route_a'].get('column_workers')==8 and n['route_a'].get('max_iterations')==32,'independent static runtime-premise check')
    check(lab+'/runtime_picard_controls',n['picard']=={'passes':6,'speed_change_bound_km_s':.01,'observe_every_pass':True},'independent registered six-pass check')
    check(lab+'/gas_integer_128',type(uv['gas']['M_s']) is int and uv['gas']['M_s']==128,'independent actual-type check')
    summary[lab]={'grid':e['grid'],'tail':e['tail'],'ro1_required':e['ro1_required'],
                  'outer':uv['outer'],'lambda_scale':uv['lambda_scale'],'gas_M_s':uv['gas']['M_s'],
                  'source_rule':uv['source_rule']['rule'] if isinstance(uv['source_rule'],dict) else uv['source_rule'],
                  'driver_sha256':e['drivers_allowed'][0],'uv_tail_config_sha256':e['uv_tail_config_sha256']}
check('C5H_declaration_only',cb['cases']['C5H']['normalized_spec_equal']=={} and cb['cases']['C5H']['call_spec_sha256']==c5sha,'pinned source literal only; actual legacy bytes UNTESTED')

def mutate(name,change,owner):
    x=copy.deepcopy(cb);change(x)
    reasons=run(x)
    check(name,bool(reasons) and any(owner in r for r in reasons),'r12 structural slice: '+owner,{'reasons':reasons})
def num(x,lab='C4T'):return x['cases'][lab]['normalized_spec_equal']['/numerics']
def uv(x,lab='C4T'):return num(x,lab)['uv_tail']
mutate('missing_case',lambda x:x['cases'].pop('C3T'),'cases must be exactly')
mutate('extra_case',lambda x:x['cases'].update({'OTHER':copy.deepcopy(x['cases']['C4T'])}),'cases must be exactly')
mutate('wrong_schema',lambda x:x.update(schema='WRONG'),'schema must be')
mutate('unknown_top_key',lambda x:x.update(permit=True),'unknown keys')
mutate('unknown_T_entry_key',lambda x:x['cases']['C4T'].update(permit=True),'unknown case-entry keys')
mutate('T_entry_cannot_carry_raw_spec_hash',lambda x:x['cases']['C4T'].update(call_spec_sha256='0'*64),'unknown case-entry keys')
mutate('unknown_C5H_entry_key',lambda x:x['cases']['C5H'].update(permit=True),'unknown case-entry keys')
mutate('missing_whole_numerics',lambda x:x['cases']['C4T']['normalized_spec_equal'].pop('/numerics'),'register /numerics whole')
mutate('grid_label_swap',lambda x:x['cases']['C2T'].update(grid='G4'),'registered G2')
mutate('actual_grid_swap',lambda x:num(x,'C2T').update(composite_grid_spec=copy.deepcopy(grids['G4'])),'not the registered grid G2')
mutate('sphere_entry_truncation',lambda x:x['cases']['S4T'].update(truncation={'shape':'cube','kmax_inverse_kpc':None}),'truncation differs')
mutate('sphere_numerics_truncation',lambda x:num(x,'S4T').update(truncation={'shape':'sphere','kmax_inverse_kpc':3.0}),'truncation differs')
mutate('tail_disabled',lambda x:x['cases']['C4T'].update(tail=False),'tail and ro1_required must be true')
mutate('RO1_disabled',lambda x:x['cases']['C4T'].update(ro1_required=False),'tail and ro1_required must be true')
mutate('legacy_tail_enabled',lambda x:x['cases']['C5H'].update(tail=True),'C5H: tail and ro1_required must be false')
mutate('wrong_T_driver',lambda x:x['cases']['C4T'].update(drivers_allowed=['0'*64]),'drivers_allowed must be [the sealed driver')
mutate('extra_T_driver',lambda x:x['cases']['C4T']['drivers_allowed'].append('0'*64),'drivers_allowed must be [the sealed driver')
mutate('wrong_legacy_driver',lambda x:x['cases']['C5H'].update(drivers_allowed=[r5]),'drivers_allowed must be [v009-EXT')
mutate('wrong_legacy_spec_declaration',lambda x:x['cases']['C5H'].update(call_spec_sha256='0'*64),'call_spec_sha256 must be the registered spec')
mutate('missing_tail_hash',lambda x:x['cases']['C4T'].pop('uv_tail_config_sha256'),'uv_tail_config_sha256 required')
mutate('invalid_tail_hash',lambda x:x['cases']['C4T'].update(uv_tail_config_sha256='G'*64),'uv_tail_config_sha256 required')
mutate('duplicate_numerics',lambda x:x['cases']['C3T']['normalized_spec_equal'].update({'/numerics':copy.deepcopy(num(x))}),'registered numerics are identical')
for aa,bb in env['UV_TAIL_MUST_DIFFER']:
    mutate('required_hash_distinct/'+aa+'/'+bb,lambda x,a=aa,b=bb:x['cases'][b].update(uv_tail_config_sha256=x['cases'][a]['uv_tail_config_sha256']),'registered uv_tail must differ')
mutate('production_P64',lambda x:uv(x)['outer'].update(K_big_inverse_kpc=64.0),'A55 production K_big')
mutate('gas_Ms64',lambda x:uv(x)['gas'].update(M_s=64),'A57 production M_s 128')
mutate('gas_Ms_float128',lambda x:uv(x)['gas'].update(M_s=128.0),'A57 production M_s 128')
mutate('gas_Ms_bool',lambda x:uv(x)['gas'].update(M_s=True),'A57 production M_s 128')
mutate('KLO_wrong_outer',lambda x:uv(x,'C4T-KLO')['outer'].update(K_big_inverse_kpc=128.0),'K_big = P/2')
mutate('KHI_wrong_outer',lambda x:uv(x,'C4T-KHI')['outer'].update(K_big_inverse_kpc=128.0),'K_big = 2P')
mutate('C5c_wrong_shape',lambda x:uv(x,'C4T-C5c').update(outer={'shape':'cylinder','K_big_inverse_kpc':128.0}),'outer must be cube K_out 5')
mutate('C4A_wrong_lambda',lambda x:uv(x,'C4T-A').update(lambda_scale=1.0),'lambda_scale must be 1.05')
mutate('D5_wrong_source_rule',lambda x:uv(x,'C4T-D5').update(source_rule='continuum_v001'),'source_rule must be nodes_v001')
mutate('D5_wrong_external_grid',lambda x:uv(x,'C4T-D5')['source_rule'].update(ext_grid=copy.deepcopy(grids['G4'])),'ext_grid = the registered G5')
mutate('tail_enabled_content_false',lambda x:uv(x).update(enabled=False),'enabled and lapse_only')
mutate('lapse_only_false',lambda x:uv(x).update(lapse_only=False),'enabled and lapse_only')
mutate('unregistered_tail_difference',lambda x:uv(x,'C3T')['stars'].update(segment_rule='OTHER'),'outside outer/lambda_scale/source_rule')
mutate('seed_factor_point1',lambda x:num(x)['route_a'].update(seed_source_rtol_factor=.1),'seed_source_rtol_factor must be absent or 1.0')
mutate('RA4_bracket_drift',lambda x:num(x)['brackets']['rule']['fs_absolute_overrides']['0'].__setitem__(0,1.0),'brackets differ from RA4')
mutate('unknown_mode',lambda x:x.update(route_a_mode='unknown'),'route_a_mode')
mutate('keymap_not_list',lambda x:x.update(key_equivalence_map={}), 'key_equivalence_map must be a list')
entry={'pointer':'/numerics/route_a/seed_source_rtol_factor','absent_equivalent_value':1.0,'b0_identity_evidence':'OWNED_SYNTHETIC'}
mutate('duplicate_map_pointer',lambda x:x.update(key_equivalence_map=[copy.deepcopy(entry),copy.deepcopy(entry)]),'one pointer mapped twice')
mutate('forbidden_map_uvtail',lambda x:x.update(key_equivalence_map=[dict(entry,pointer='/numerics/uv_tail/enabled')]),'may not be mapped')
mutate('map_unknown_key',lambda x:x.update(key_equivalence_map=[dict(entry,permit=True)]),'needs exactly')
mutate('map_missing_evidence',lambda x:x.update(key_equivalence_map=[dict(entry,b0_identity_evidence='')]),'needs exactly')

for name,raw in [
 ('duplicate_case_equal','{"cases":{"C4T":{},"C4T":{}}}'),
 ('duplicate_case_different','{"cases":{"C4T":{"tail":true},"C4T":{"tail":false}}}'),
 ('duplicate_nested_numerics','{"cases":{"C4T":{"normalized_spec_equal":{"/numerics":{},"/numerics":{}}}}}'),
 ('duplicate_top_schema','{"schema":"a","schema":"a"}')]:
    try:
        env['loads_strict'](raw)
        code=None
    except env['DuplicateKey'] as e:
        code=e.code
    check(name,code is not None and 'members[' in code,'actual r12 loads_strict/_hook_factory',code)

# Precise omitted-premise controls: these are EXPECTED admissions by the
# structural slice, not evidence that the full review accepts them.
x=copy.deepcopy(cb)
x['cases']['C2T']['uv_tail_config_sha256']='0'*64
check('boundary_wrong_but_hex_tail_hash_not_checked_here',run(x)==[],'EXCLUDED normalizer/hash link; delegated independent lane')
x=copy.deepcopy(cb);num(x,'C2T')['route_a']['column_workers']=1
check('boundary_runtime_workers_not_owned_by_structural_slice',run(x)==[],'runtime _case_validity; actual candidate statically checked above')
check('boundary_argument_mode_mismatch_owned_by_CLI',run(cb,'serial_with_exemption')==[],'CLI seal mode check; candidate mode is explicit parallel8')
drop=env['drop_mapped_keys']
a={'route_a':{'seed_source_rtol_factor':1.0}};b={'route_a':{}}
aa,bb,used=drop(a,b,[entry]);check('map_exact_absent_value_drops',aa==bb and used==[entry['pointer']] and a['route_a']['seed_source_rtol_factor']==1.0,'actual r12 drop_mapped_keys')
aa,bb,used=drop({'route_a':{'seed_source_rtol_factor':.1}},b,[entry]);check('map_wrong_value_kept',used==[] and aa!=bb,'actual r12 drop_mapped_keys')
aa,bb,used=drop(a,{'route_a':{'seed_source_rtol_factor':2.0}},[entry]);check('map_other_side_wrong_value_kept',used==[] and aa!=bb,'actual r12 drop_mapped_keys')
check('candidate_and_source_bytes_unchanged',all(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'] for p in PINS),'end byte custody')
check('zero_protected_attempts',not ATTEMPTS,'path guards')
check('no_project_modules_imported',not any(str(getattr(m,'__file__','')).startswith(str(A)) for m in sys.modules.values() if m is not sys.modules[__name__]),'import inventory')

result={'schema':'A99_CASE_BLOCK_STRUCTURAL_REVIEW_CX2V001','date_u':DATE,
        'verdict':'PASS_LIMITED_SCOPE' if all(t['passed'] for t in CHECKS) else 'FAIL',
        'tested':'Actual candidate strict parse and structural/content contract; independently owned mutations of a safe AST slice.',
        'untested':['Actual uv_tail normalization/hash linkage (other lane).','Ten raw filled-spec and dry-report provenance joins (other lane).',
                    'Legacy C5H file/run/dry-run custody and D5-versus-legacy comparison, deliberately excluded.',
                    'Full validator, CLI, seal admission, producer registry, scientific gates, runtime outputs and launchability.'],
        'AST_seams':{'functions':selected_functions,'validator_original_lines':[original.lineno,original.end_lineno],
                     'removed_legacy_block_lines':[removed.lineno,removed.end_lineno],
                     'check_uv_link':False,'registered_grids':'pinned prereg declarations read directly',
                     'sealed_driver_sha':'literal r5 sha extracted from pinned comparator, no active-build loader',
                     'legacy_spec_sha':'literal source declaration only; protected path never loaded',
                     'slice_ast_sha256':hashlib.sha256(ast.dump(module,include_attributes=False).encode()).hexdigest()},
        'cases':summary,'legacy_declaration':cb['cases']['C5H'],'findings':[],
        'passed':sum(t['passed'] for t in CHECKS),'total':len(CHECKS),'checks':CHECKS,
        'input_pins':PINS,'protected_attempts':ATTEMPTS}
p=HERE/'CONTRACT_RESULTS_CX2V001.json'
with p.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'verdict':result['verdict'],
                  'passed':result['passed'],'total':result['total'],'failed':[t for t in CHECKS if not t['passed']]}))
