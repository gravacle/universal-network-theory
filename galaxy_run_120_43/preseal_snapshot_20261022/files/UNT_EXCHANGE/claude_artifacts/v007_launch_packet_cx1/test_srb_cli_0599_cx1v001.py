"""SRB actual main with synthetic saved rotation and explicitly stubbed reconstruction.
The actual pinned library's srb_rot arithmetic and actual R11 gate are used.
No production run or numerical state reconstruction is executed.
"""
import sys,json,hashlib,importlib.util,types,io,zipfile,copy
from pathlib import Path
import numpy as np
R=Path(__file__).parent;sys.path.insert(0,str(R))
import producer_guard_cx1v008 as G
D=R/'SRB_CLI_SYNTH_V001';D.mkdir();G.REGISTERED=()
G.admission=lambda *a,**k:{'_verified_seal':{'driver':{'sha256':'d'*64}}};G.stamp=lambda o,*a:dict(o,root_admission={'synthetic':True})
import postseal_records_cx1v004 as C
import srb_rot_record_cx1v006 as S
checks=[]
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(p,o):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(o,f)
 return pin(p)
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
M=mod(R.parent/'v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py','srb_r11')
U=mod(R.parent/'tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py','srb_actual_lib')
C.comparator=lambda:M
binding=C.read({'path':M.PIN_ROW_RADII_BINDING[0],'sha256':M.PIN_ROW_RADII_BINDING[1]})
q=[x['radius_m'] for x in binding['query_rows']];rad=np.array([min(q)*.5,max(q)*2]);omega=(50000/rad)**2
arr={'radial_nodes_m':rad,'rotation_Omega_squared':np.repeat(omega[:,None],2,axis=1),'full_fields_complex':np.zeros((2,1,2,10),complex)}
rot=D/'run'/'rotation';rot.mkdir(parents=True)
buf=io.BytesIO();np.savez(buf,**arr);ap=rot/'rotation_base_arrays.npz'
with ap.open('xb') as f:f.write(buf.getvalue())
ar=pin(ap);fin=put(rot/'finish.json',{'arrays_path':ar['path'],'arrays_sha256':ar['sha256'],'uv_tail':{'state_digest':'1'*64,'production_admissible':True}})
spec=json.loads((R/'P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json').read_bytes());cfg=U.normalize_config(spec['numerics']['uv_tail'])
rp=put(D/'run/result.json',{'status':'COMPLETED','driver_sha256':'d'*64,'normalized_spec':spec,'passes':[{'rotation':str(rot)}]});put(D/'run/finish.json',{'result_sha256':rp['sha256']})
desc=put(D/'descriptor.json',{'operation':'rebuild','state_assertion':fin,'state_field_path':['uv_tail','state_digest']})
state=types.SimpleNamespace(empty=False,digest='1'*64,_a={'shell_edges_inverse_kpc':np.array([4.,5.]),'shell_integrals':np.array([[0.,1e-40,0.]])},record={'c_m_s':299792458.})
r=types.SimpleNamespace(config=cfg,replay_scope='PRODUCTION_P128_MS128',lib=U);p=types.SimpleNamespace(state=state,input_pins=[desc])
S.reconstruct=lambda ref:(r,p)
manifest={'result':rp,'reconstruction':desc,'EPS':cfg['eps_certificate']};mp=put(D/'manifest.json',manifest)
def ck(n,fn,refuse=False):
 try:v=fn();ok=not refuse and v is not False;err=None
 except Exception as e:ok=refuse;err=type(e).__name__+': '+str(e)
 checks.append({'name':n,'passed':ok,'error':err})
def run(m,out):sys.argv=['srb',str(m),str(out)];S.main();return json.loads(out.read_bytes())
ck('actual_SRB_main_synthetic_reconstruction',lambda:run(Path(mp['path']),D/'SRB.json')['verdict']=='PASS')
if (D/'SRB.json').exists():
 o=json.loads((D/'SRB.json').read_bytes());eps=C.read(cfg['eps_certificate']);e=next(x['eps_envelope'] for x in eps['shells'] if x['lo_inverse_kpc']==4)
 factor=np.sin(binding['physical_inclination_rad'])/np.sin(binding['released_inclination_rad'])
 expected=max(rad)*299792458.**2*e*1e-40/(2*50000)/1000*factor
 ck('independent_literal_srb_bound',lambda:np.allclose(o['srb_rot_km_s'],expected,rtol=1e-14,atol=0))
ck('exclusive_SRB_output',lambda:run(Path(mp['path']),D/'SRB.json'),True)
bad=copy.deepcopy(manifest);bad['reconstruction']=put(D/'bad_descriptor.json',{'operation':'accepted_manifest'});bp=put(D/'bad_manifest.json',bad)
ck('wrong_reconstruction_occurrence',lambda:run(Path(bp['path']),D/'bad_out.json'),True)
ck('valid_rotation_archive',lambda:S.rotation_arrays(ar)['full_fields_complex'].shape==(2,1,2,10))
b=io.BytesIO();np.save(b,np.ones(1));raw=b.getvalue()
for name,entries in [('alias',[('x.npy',raw),('x',raw)]),('duplicate',[('x.npy',raw),('x.npy',raw)]),('header_duplicate',[('x.npy',b'\x93NUMPY\x01\x00'+(len(h:=b"{'descr':'<f8','descr':'<f8','fortran_order':False,'shape':(1,)}\n")).to_bytes(2,'little')+h+b'\0'*8)])]:
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w') as z:
  for nm,data in entries:z.writestr(nm,data)
 pp=D/(name+'.npz')
 with pp.open('xb') as f:f.write(buf.getvalue())
 ck('npz_refuses_'+name,lambda pp=pp:S.rotation_arrays(pin(pp)),True)
with (R/'SRB_CLI_0599_TESTS_V001.json').open('x') as f:json.dump({'scope':'TESTED actual SRB main with stubbed reconstruction, synthetic arrays, actual library arithmetic and r11; production UNTESTED','source_pins':[pin(R/'srb_rot_record_cx1v006.py'),pin(R/'postseal_records_cx1v004.py'),pin(Path(U.__file__)),pin(Path(M.__file__))],'tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));print([x for x in checks if not x['passed']]);assert all(x['passed'] for x in checks)
