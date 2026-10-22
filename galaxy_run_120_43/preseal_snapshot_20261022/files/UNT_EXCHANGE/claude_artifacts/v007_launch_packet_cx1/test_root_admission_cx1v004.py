"""Synthetic admission and copied-marker tests. Actual root CONFIG never written. No protected run read."""
import copy,hashlib,importlib.util,json,os
from pathlib import Path
R=Path(__file__).parent;src=R/'producer_guard_cx1v008.py'
s=importlib.util.spec_from_file_location('gtest',src);G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
D=R/'ROOT_ADMISSION_SYNTH_V004';D.mkdir();checks=[]
def write(name,data):
 p=D/name
 with p.open('x') as f:f.write(data if isinstance(data,str) else json.dumps(data))
 return p
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def check(name,fn,typ=None):
 try:v=fn();ok=typ is None and v is not False
 except Exception as e:ok=typ is not None and isinstance(e,typ)
 checks.append({'name':name,'passed':ok})
G.CONFIG=D/'not_written.json'
check('no_root_record_refuses',lambda:G.admission(__file__),PermissionError)
check('argv_seal_authority_refused',lambda:G.authorize([__file__,'--seal','fake'],'records'),PermissionError)
p=write('prereg.json',{'label':'SYNTHETIC'});c=write('compare.py','# SYNTHETIC\n');allow={str(src.resolve()):pin(src)['sha256'],str(Path(__file__).resolve()):pin(Path(__file__))['sha256']}
b=write('BUILD.md','SYNTHETIC allowlist\n'+'\n'.join(f'{v}  {k}' for k,v in allow.items()))
seal=write('SEAL.json',{'sealed_by':G.AUTHORITY,'prereg':pin(p),'compare':pin(c),'driver':pin(c),'frozen_addendum':pin(p)})
cfg={'schema':'UNT_ROOT_SEAL_ADMISSION_CX1V001','authority':G.AUTHORITY,'seal':pin(seal),'prereg':pin(p),'compare':pin(c),'build':pin(b),'producer_allowlist':allow}
G.CONFIG=write('CONFIG_valid.json',cfg)
check('missing_published_sha',lambda:G.admission(__file__),PermissionError)
os.environ['UNT_ROOT_ADMISSION_SHA256']='0'*64
check('wrong_published_sha',lambda:G.admission(__file__),PermissionError)
os.environ['UNT_ROOT_ADMISSION_SHA256']=pin(G.CONFIG)['sha256']
check('synthetic_pinned_admission',lambda:G.admission(__file__))
check('embedded_provenance',lambda:G.stamp({'schema':'SYNTH'},__file__)['root_admission']=={'config':pin(G.CONFIG),'seal':pin(seal),'compare':pin(c),'driver':pin(c),'frozen_addendum':pin(p)})
valid_config=G.CONFIG
check('unlisted_source_refused',lambda:G.admission(c),PermissionError)
for label,change in [('seal_hash',lambda x:x['seal'].update(sha256='0'*64)),('prereg_binding',lambda x:x.update(prereg=pin(c))),('allowlist_hash',lambda x:x['producer_allowlist'].update({str(Path(__file__).resolve()):'0'*64}))]:
 q=copy.deepcopy(cfg);change(q);G.CONFIG=write('CONFIG_'+label+'.json',q);os.environ['UNT_ROOT_ADMISSION_SHA256']=pin(G.CONFIG)['sha256'];check(label,lambda:G.admission(__file__),(ValueError,PermissionError))
free=write('SEAL_string_actor.json',{'sealed_by':'Claude2 (root)','prereg':pin(p),'compare':pin(c),'driver':pin(c),'frozen_addendum':pin(p)})
q=copy.deepcopy(cfg);q['seal']=pin(free);G.CONFIG=write('CONFIG_string_actor.json',q);os.environ['UNT_ROOT_ADMISSION_SHA256']=pin(G.CONFIG)['sha256'];check('free_string_actor_refused',lambda:G.admission(__file__),PermissionError)
# Never stat actual registered run; use a wholly synthetic registered path for marker tests.
G.REGISTERED=(D/'synthetic_registered',);G.REGISTERED[0].mkdir()
copydir=D/'copied_run';copydir.mkdir();marker=write('source_marker.json',{'call_spec_sha256':G.C5H_SPEC});os.link(marker,copydir/'start.json')
check('hardlinked_marker_copy_refused',lambda:G.check_run_path(copydir),PermissionError)
check('nested_output_in_copy_refused',lambda:G.check_run_path(copydir/'nested'/'new_output'),PermissionError)
ordinary=D/'ordinary';ordinary.mkdir();check('unmarked_synthetic_path_allowed',lambda:G.check_run_path(ordinary))
for missing_key in ('driver','frozen_addendum'):
 seal_data={'sealed_by':G.AUTHORITY,'prereg':pin(p),'compare':pin(c),'driver':pin(c),'frozen_addendum':pin(p)};seal_data.pop(missing_key)
 badseal=write('missing_'+missing_key+'_seal.json',seal_data);q=copy.deepcopy(cfg);q['seal']=pin(badseal);G.CONFIG=write('missing_'+missing_key+'_config.json',q);os.environ['UNT_ROOT_ADMISSION_SHA256']=pin(G.CONFIG)['sha256']
 check('missing_seal_'+missing_key,lambda:G.admission(__file__),PermissionError)
G.CONFIG=valid_config;os.environ['UNT_ROOT_ADMISSION_SHA256']=pin(G.CONFIG)['sha256']
@G.guarded
def imported_entry(run):raise AssertionError('marked path entered body')
check('import_route_marked_refused',lambda:imported_entry(copydir/'child'),PermissionError)
oldcwd=os.getcwd();os.chdir(D)
check('relative_ancestor_refused',lambda:imported_entry('copied_run/child'),PermissionError)
os.chdir(oldcwd)
alias=D/'alias';alias.symlink_to(copydir,target_is_directory=True)
check('symlink_ancestor_refused',lambda:imported_entry(alias/'child'),PermissionError)
check('nested_object_path_refused',lambda:imported_entry({'run':str(alias/'child')}),PermissionError)
G.CONFIG=D/'missing_again.json'
@G.guarded
def public_entry():raise AssertionError('body should not execute')
check('public_entry_reauthorizes',public_entry,PermissionError)
with (R/'ROOT_ADMISSION_TESTS_V004.json').open('x') as f:json.dump({'label':'TESTED synthetic only; root config path patched in test process; no production seal admitted','guard':pin(src),'tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
