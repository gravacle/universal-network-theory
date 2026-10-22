import tempfile,json,hashlib,copy
from pathlib import Path
from runtime_distribution_record_cx1v002 import assemble,compare,validate
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='distribution_record_',dir=b/'inert_fixtures'))
pins={}
for name in ['interpreter','driver','monitor']:
 p=c/name
 with p.open('xb') as f:f.write(('INERT '+name).encode())
 pins[name]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
discovery={'distributions':[dict(name=n,version='1',sha256='a'*64,identity_basis='sorted_relative_names_and_file_bytes_v001',files=[{'path':n+'/x','sha256':'b'*64,'size':1,'outside_RECORD':False,'excluded_from_equality':False}]) for n in ['numpy','scipy']],'import_bindings':[{'import':n,'distribution':n,'origin':'/INERT/'+n} for n in ['numpy','scipy']]}
args=dict(discovery=discovery,interpreter_path=pins['interpreter']['path'],driver_pin=pins['driver'],monitor_pin=pins['monitor'],inherited_environment={'SECRET':'not recorded'},sys_version='INERT',sys_flags={'isolated':1,'dont_write_bytecode':1},macos_build='INERT',hardware_model='INERT',captured_utc='2026-10-21T00:00:00+00:00',producer_pin={'path':'/INERT/producer.py','sha256':'e'*64})
r=assemble(**args);assert 'SECRET' not in r['effective_environment'];compare(r,r);passed=['inert assembly and equal comparison']
for mode in ['package','driver','build','association','missing_scipy']:
 bad=copy.deepcopy(r)
 if mode=='package':bad['distributions'][0]['sha256']='c'*64
 elif mode=='driver':bad['driver']['sha256']='c'*64
 elif mode=='build':bad['macos_build']='OTHER'
 elif mode=='association':bad['import_bindings'][0]['distribution']='scipy'
 else:bad['import_bindings']=bad['import_bindings'][:1]
 try:compare(r,bad)
 except ValueError:passed.append(mode+' refuses')
 else:raise AssertionError(mode)
bad=copy.deepcopy(r);bad['hardware_model']='OTHER';compare(r,bad);passed.append('hardware recorded not compared')
for mode in ['excluded_native','unsafe_path','missing_producer','duplicate_file','unbound_distribution']:
 bad=copy.deepcopy(r)
 if mode=='excluded_native':bad['distributions'][0]['files'][0]['excluded_from_equality']=True
 elif mode=='unsafe_path':bad['distributions'][0]['files'][0]['path']='../escape'
 elif mode=='missing_producer':bad['producer']={}
 elif mode=='duplicate_file':bad['distributions'][0]['files']*=2
 else:
  extra=copy.deepcopy(bad['distributions'][0]);extra['name']='unbound';bad['distributions'].append(extra)
 try:validate(bad)
 except ValueError:passed.append(mode+' refuses')
 else:raise AssertionError(mode)
report=dict(status='PASS',blocking_count=0,tested=passed,scope='Inert runtime assembly and comparison only',untested=['Launch-time capture CLI','Additional malformed and adversarial record shapes','Root authentication and importer integration'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'runtime_distribution_record_cx1v002.py',Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
