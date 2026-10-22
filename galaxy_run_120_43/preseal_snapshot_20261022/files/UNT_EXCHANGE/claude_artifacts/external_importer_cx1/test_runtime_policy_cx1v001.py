import copy,json,hashlib,tempfile
from pathlib import Path
from runtime_policy_cx1v001 import effective_environment,compare_records,RuntimeRefusal,THREADS
root=Path(__file__).resolve().parent;case=Path(tempfile.mkdtemp(prefix='runtime_policy_',dir=root/'inert_fixtures'))
env=effective_environment({'SECRET_TOKEN':'DO_NOT_RECORD','PYTHONPATH':'/inert','OMP_NUM_THREADS':'99','PATH':'/inert/bin','LANG':'C','LC_ALL':'C','TMPDIR':'/inert/tmp'})
assert 'SECRET_TOKEN' not in env and 'PYTHONPATH' not in env and all(env[k]=='1' for k in THREADS)
r=dict(schema='CX1_RUNTIME_CAPTURE_V001',coverage_complete=True,interpreter={'realpath':'/inert/python','sha256':'a'*64},sys_version='inert',sys_flags={'isolated':1},macos_build='INERT_BUILD',hardware_model='INERT_MODEL',effective_environment=env,modules=[dict(name=n,version='inert',sha256=h*64) for n,h in [('numpy','b'),('scipy','c')]])
passed=['whitelist excludes unrelated secrets and PYTHON variables; normalizes six thread variables']
assert compare_records(r,copy.deepcopy(r))['prerequisites_only'];passed.append('equal records compare')
b=copy.deepcopy(r);b['effective_environment'].update(PATH='/different',LANG='different',TMPDIR='/different');b['hardware_model']='other';b['sys_version']='other';b['sys_flags']={};b['interpreter']['realpath']='/other'
compare_records(r,b);passed.append('root-designated recorded-only fields do not change comparison')
for label,mutate in [('interpreter hash',lambda d:d['interpreter'].update(sha256='d'*64)),('module hash',lambda d:d['modules'][0].update(sha256='d'*64)),('module version',lambda d:d['modules'][0].update(version='other')),('macos build',lambda d:d.update(macos_build='other')),('DYLD present',lambda d:d['effective_environment'].update(DYLD_LIBRARY_PATH='/inert')),('PYTHON present',lambda d:d['effective_environment'].update(PYTHONPATH='/inert')),('unnormalized threads',lambda d:d['effective_environment'].update(OMP_NUM_THREADS='2')),('missing scipy',lambda d:d['modules'].pop()),('incomplete coverage',lambda d:d.update(coverage_complete=False)),('duplicate module',lambda d:d['modules'].append(copy.deepcopy(d['modules'][0])))]:
 b=copy.deepcopy(r);mutate(b)
 try:compare_records(r,b)
 except RuntimeRefusal:passed.append(label+' refuses')
 else:raise AssertionError(label)
assert 'DYLD_INSERT_LIBRARIES' in effective_environment({'DYLD_INSERT_LIBRARIES':'/inert'});passed.append('normalization retains DYLD evidence for refusal')
report=dict(status='PASS',blocking_count=0,scope='0843 comparison/whitelist primitives only; entirely inert input',tested=passed,untested=['Actual runtime capture producer','Import coverage and launch-time authentication','Real environment inspection'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'runtime_policy_cx1v001.py']])
p=case/'TEST_REPORT.json'
with p.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(p)
