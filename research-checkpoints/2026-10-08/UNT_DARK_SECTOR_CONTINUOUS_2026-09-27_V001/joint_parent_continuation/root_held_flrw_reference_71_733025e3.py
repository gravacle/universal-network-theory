"""Guarded new homogeneous-budget comparison; no local source/adoption."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,io,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001'
AUTHOR_DRAFT=True
PROTOCOL_SHA='5100422cb94248b136988950c8fbaf5fa1aa014b2bcd9302ef199d5a532f3889'
NORMAL='CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002'
PINS={NORMAL+'_RESULT.json':'ca1056f8798864eb7ae86c61812379ad8be46c4586560bf832f308fb79242158',NORMAL+'_RECEIPT.json':'00a630bd20e5ac06ce3dcc63dd4187c6d82b8ea73989274b0d105157cfee25b2','READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json':'1e3b72fee21d3ec31335a02ae814d74c982d2970c39c9fb0575f28589ba2442b','authoring_cross_u_owned_flrw_ordinary_reference_benchmark_v001_71_47d224ee.py':'47d224ee805d758a65cfd6c4dc7b7cd728b0bbd77f63549ae392bf032adbe6d9','authoring_owned_flrw_ordinary_reference_benchmark_v001_8_71ced14c.md':'71ced14c6eaa286adce7dec74b03ac46ad4a11cb6395e1529c99b428f5b4af57'}
INPUTS={};OUTPUTS={};AVAILABLE={};np=None;OWNER=None
FLAGS=dict(local_ordinary_source_admitted=False,background_subtraction_adopted=False,normal_constraint_zero_qualified=False,physical_metric_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def bind(n,h):
 p=BASE/n;assert h is not None and sha(p)==h,n;INPUTS[str(p.resolve())]=h;return p
def write(n,x):
 p=BASE/n;b=(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);return OUTPUTS[str(p.resolve())]
def recheck():
 for p,h in dict(INPUTS,**OUTPUTS).items():assert sha(p)==h,p
def read(ref,names):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256'])
 with np.load(BASE/ref['file'],allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json'].item()))==ref['metadata'];out={n:f[n].copy() for n in names}
 for n,a in out.items():
  AVAILABLE['loaded_'+n]=a;assert a.dtype==np.float64 and list(a.shape)==ref['metadata']['schema'][n]['shape'] and np.all(np.isfinite(a))
 return out
def checkpoint(tag,data,failed=False):
 schema={n:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for n,a in data.items()};md=dict(kind='homogeneous_reference_only',owner=OWNER,schema=schema,failed=failed,qualification=FLAGS)
 b=io.BytesIO();np.savez_compressed(b,**data,metadata_json=np.array(json.dumps(md,sort_keys=True,separators=(',',':'))));p=BASE/(STEM+'_'+tag+'.npz')
 with p.open('xb') as f:f.write(b.getvalue());f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);rec=dict(file=p.name,sha256=sha(p),metadata=md);cf=p.name+'.COMMIT.json';ch=write(cf,rec);return dict(rec,commit_file=cf,commit_sha256=ch)
def packet(result):
 inp=result['checkpoints'][0];fixed=inp['metadata']['fixed'];bg=inp['metadata']['owned_background'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100 and fixed['rG']==.98989898989899
 coords=read(inp,('r_kpc','z_kpc'));geo=read(result['checkpoints'][2],('r','z'));stored=read(result['case']['loads'],('normal_Hamiltonian_rows_hi','normal_Hamiltonian_rows_lo'))
 r,z=geo['r'],geo['z'];assert r.shape==(87,) and z.shape==(45,) and np.array_equal(r,coords['r_kpc']) and np.array_equal(z,coords['z_kpc']) and np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and r[0]>=0 and z[0]==0
 hi,lo=stored['normal_Hamiltonian_rows_hi'][0],stored['normal_Hamiltonian_rows_lo'][0];assert hi.shape==lo.shape==(87,45)
 eta=fixed['Hunit']/299792458.;C=1.98;ordinary=3*eta**2*(fixed['OB']+fixed['OR'])/(C*fixed['rG']);phase=2*eta**2*bg['rho']/C;EH=-3*eta**2*bg['h']**2/C
 scalars=np.array((eta,C,ordinary,phase,EH));AVAILABLE['reference_scalars_eta_C_ordinary_phase_EH']=scalars
 dr=np.diff(r);dz=np.diff(z);rw=np.zeros(87);zw=np.zeros(45)
 left=r[:-1]*dr/2+dr**2/6;right=r[:-1]*dr/2+dr**2/3;rw[:-1]+=left;rw[1:]+=right;zw[:-1]+=dz/2;zw[1:]+=dz/2
 volume=rw[:,None]*zw[None];restricted=volume.copy();restricted[1]+=restricted[0];restricted[0]=0;restricted[-1]=0;restricted[:,-1]=0
 for n,a in dict(radial_left_integrals=left,radial_right_integrals=right,radial_hat_integrals=rw,vertical_hat_integrals=zw,analytic_volume=volume,restricted_analytic_volume=restricted).items():AVAILABLE[n]=a
 analytic_total=(r[-1]**2-r[0]**2)*(z[-1]-z[0])/2;controls=[]
 for name,actual,expected,envelope in (('owned_homogeneous_EH_phase_ordinary_budget',phase+EH,-ordinary,abs(phase)+abs(EH)+ordinary),('analytic_Q1_volume_partition',float(np.sum(volume)),float(analytic_total),float(np.sum(abs(volume)))+abs(float(analytic_total)))):
  a=np.array([actual]);e=np.array([expected]);v=np.array([envelope]);error=float(np.max(abs(a-e)/np.maximum(v,1e-30)));AVAILABLE['control_'+name+'_actual']=a;AVAILABLE['control_'+name+'_expected']=e;AVAILABLE['control_'+name+'_envelope']=v;controls.append(dict(name=name,error=error,tolerance=2e-11,passed=error<=2e-11))
 negative=-ordinary*restricted;saved=hi+lo;difference=saved-negative
 AVAILABLE.update(saved_lapse_hi=hi,saved_lapse_lo=lo,saved_lapse_rounded=saved,negative_homogeneous_shortfall=negative,descriptive_difference_from_negative_reference=difference)
 assert ordinary>0 and np.all(np.isfinite(scalars)) and all(c['passed'] for c in controls)
 index=np.unravel_index(int(np.argmax(abs(saved))),saved.shape);i,j=map(int,index)
 norm=lambda a:float(np.linalg.norm(a));refnorm=norm(negative);refmax=float(np.max(abs(negative)));assert refnorm>0 and refmax>0
 data={n:a.copy() for n,a in AVAILABLE.items()};ref=checkpoint('BENCHMARK',data)
 return dict(status='HOMOGENEOUS_ORDINARY_REFERENCE_BENCHMARK_MEASURED',controls=controls,checkpoint=ref,reference_density=ordinary,reference_phase_EH_shortfall=phase+EH,unrestricted_volume=float(np.sum(volume)),restricted_volume=float(np.sum(restricted)),saved_lapse_L2=norm(saved),negative_reference_L2=refnorm,difference_L2=norm(difference),difference_L2_over_reference=norm(difference)/refnorm,difference_Linf_over_reference=float(np.max(abs(difference)))/refmax,largest_saved_node=dict(indices=[i,j],R_kpc=float(r[i]),Z_kpc=float(z[j]),saved=float(saved[index]),negative_reference=float(negative[index]),difference=float(difference[index])),reference_sign='negative',original_state_changed=False,local_source_added=False,physical_zero_gate=False,velocity_bound=False)
def main():
 global np,OWNER
 assert AUTHOR_DRAFT is False and PROTOCOL_SHA is not None,'Root review and release required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Existing runtime files preserved'
 for n,h in PINS.items():bind(n,h)
 bind(STEM+'.md',PROTOCOL_SHA);INPUTS[str(Path(__file__).resolve())]=sha(__file__)
 result=json.loads((BASE/(NORMAL+'_RESULT.json')).read_text());rc=json.loads((BASE/(NORMAL+'_RECEIPT.json')).read_text());proof=json.loads((BASE/'READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json').read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['owner']['pid']==51682 and rc['result_sha256']==PINS[NORMAL+'_RESULT.json'] and result['owner']==rc['owner']
 assert proof['status']=='SAVED_PAIRED_NORMAL_CLOSURE_PASS' and proof['parent_terminal']['result_sha256']==PINS[NORMAL+'_RESULT.json'] and proof['parent_terminal']['receipt_sha256']==PINS[NORMAL+'_RECEIPT.json'] and all(v is False for v in result['qualification'].values()) and proof['qualification']==result['qualification']
 import numpy as numpy_module
 np=numpy_module;OWNER=dict(pid=os.getpid(),started=now(),source_sha256=sha(__file__),parent_pid=51682);write(STEM+'_OWNER_START.json',OWNER)
 try:
  case=packet(result);recheck();rh=write(STEM+'_RESULT.json',dict(case,owner=OWNER,qualification=FLAGS));recheck();write(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=OWNER,closed=now(),result_sha256=rh,error_sha256=None,input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS));recheck();print(case['status'],flush=True);return 0
 except BaseException:
  failure=traceback.format_exc();partial=checkpoint('ERROR_RAW',AVAILABLE,True) if AVAILABLE else None;eh=write(STEM+'_ERROR.json',dict(status='FAILED',owner=OWNER,traceback=failure,partial=partial,qualification=FLAGS));prior=BASE/(STEM+'_RECEIPT.json');write(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=OWNER,closed=now(),error_sha256=eh,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS));raise
if __name__=='__main__':sys.exit(main())
