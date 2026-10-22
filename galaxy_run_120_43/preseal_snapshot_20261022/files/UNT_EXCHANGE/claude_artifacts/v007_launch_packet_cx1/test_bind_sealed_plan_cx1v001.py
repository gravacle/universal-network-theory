import importlib.util,json
from pathlib import Path
R=Path(__file__).parent;src=R/'bind_sealed_launch_plan_cx1v001.py'
s=importlib.util.spec_from_file_location('binder',src);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
D=R/'SEAL_BIND_0576_SYNTH_V001';D.mkdir()
add=D/'SYNTHETIC_FROZEN.md'
with add.open('x') as f:f.write('SYNTHETIC TEST ONLY, not a scientific addendum.\n')
template=R/'P128/LAUNCH_PLAN_V010.json';p=json.loads(template.read_bytes());driver=p['driver'];checks=[]
def check(name,fn,refuse=False):
 try:v=fn();ok=not refuse
 except ValueError:ok=refuse
 checks.append({'name':name,'passed':ok})
args=[template,driver['path'],driver['sha256'],add,M.pin(add)['sha256']]
check('valid_byte_binding',lambda:M.bind(*args,D/'bound.json',D/'command.txt'))
b=json.loads((D/'bound.json').read_bytes())
check('specs_caps_order_ramp_unchanged',lambda:None if all(b[k]==p[k] for k in ('calls','order','route_a_admission','driver','launcher','guard','runtime_worker_pins')) else (_ for _ in ()).throw(ValueError()))
check('exclusive_outputs_refuse',lambda:M.bind(*args,D/'bound.json',D/'command2.txt'),True)
bad=list(args);bad[4]='0'*64;check('wrong_frozen_sha_refuse',lambda:M.bind(*bad,D/'bad1.json',D/'bad1.txt'),True)
bad=list(args);bad[2]='0'*64;check('wrong_driver_sha_refuse',lambda:M.bind(*bad,D/'bad2.json',D/'bad2.txt'),True)
bad=list(args);bad[1]=add;bad[2]=M.pin(add)['sha256'];check('different_chosen_driver_refuse',lambda:M.bind(*bad,D/'bad3.json',D/'bad3.txt'),True)
check('same_output_refuse',lambda:M.bind(*args,D/'same.json',D/'same.json'),True)
with (R/'SEAL_BIND_0576_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED build-only synthetic frozen addendum; no launch or actual root freeze','source':M.pin(src),'tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
