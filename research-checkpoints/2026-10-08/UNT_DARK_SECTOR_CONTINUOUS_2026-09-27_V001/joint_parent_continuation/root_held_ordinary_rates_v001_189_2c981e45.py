"""Guarded instantaneous ordinary Hamiltonian rates on authenticated saved points."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_ORDINARY_CANONICAL_RATES_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='91ea7c74515748563af64573c6413fac2df380e19e9c54e9300dcf798497fed8'
TOL=2e-11;np=None;OWNER=None;RAW={};CREATED={};RECORDS=[];CHECKS=[]
FLAGS=dict(ordinary_evolution_qualified=False,metric_evolution_qualified=False,CMC_qualified=False,physical_history_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
PINS={
 'author_fragment_d0_ordinary_canonical_spatial_rates_v001.txt':'d3526ce6e0a2a08e87bdd6ff5a7f5937bba35078291b76758aed34015ca5eb61',
 'READONLY_FORCE_V003_ORDINARY_SOURCE_MAPPING_V001.json':'585bcda308a3f7a4522f76b456feba1a50836994d4da35eb1cf89a713269d95d',
 'READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json':'80b7fac6e83d178bc2eb706853d301bbf258e0fe9f22caa0423e28010eac66e2',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RESULT.json':'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RECEIPT.json':'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_00003_ARM.npz':'4d2d7a2e8df8367735884eb2e5dd6440ac4c49850fa82e5c5affe31e3b575bb1',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_00003_ARM.npz.COMMIT.json':'02682c4edd894466acba1c159ec845eee0a8089240e09c4d8f5c209608b6bd76',
 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json':'981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770',
 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RECEIPT.json':'822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2',
 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_00007_LOADS.npz':'4b6b6db0ccdc7b678c43150fa55d9eab5c54d09eabe6a71254e5986b4f0fa9cc',
 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_00007_LOADS.npz.COMMIT.json':'f81ae230cfb2712438b52da727d7f636f05d0422ab30ee098ddc864447ebd349'}
INPUTS={}

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for a in iter(lambda:f.read(1048576),b''):h.update(a)
 return h.hexdigest()

def now():return datetime.now(timezone.utc).isoformat()

def encoded(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==b;CREATED[n]=sha(p);return CREATED[n]

def json_file(n,v):return publish(n,encoded(v))

def capture(n,a):RAW[n]=a.copy();return a

def check(n,a,b,e):
 a=np.asarray(a);b=np.asarray(b);e=np.asarray(e);k=len(CHECKS)
 for key,v in dict(actual=a,expected=b,envelope=e).items():capture(f'control_{k:03d}_{key}',v)
 assert a.shape==b.shape==e.shape and all(np.all(np.isfinite(v)) for v in (a,b,e)) and np.all(e>=0)
 err=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(ordinal=k,name=n,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row);assert row['passed'],row

def pair(tag,arrays,meta):
 schema={}
 for n,a in arrays.items():
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiub';schema[n]=dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
 md=dict(meta,owner=OWNER,schema=schema,qualification=FLAGS);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name);text=encoded(md).decode()
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);CREATED[name]=sha(p);rec=dict(file=name,sha256=CREATED[name],metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec);rec.update(commit_file=cf,commit_sha256=ch);RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as z:
  assert str(z['metadata_json'])==text and set(z.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert z[k].dtype==a.dtype and z[k].shape==a.shape and np.array_equal(z[k],a,equal_nan=True)
 return rec

def recheck():
 for n,h in INPUTS.items():assert sha(n)==h,n
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in CREATED.items():assert sha(n)==h,n

def read_parent(rec,names):
 assert sha(rec['file'])==rec['sha256'] and sha(rec['commit_file'])==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={}
 with np.load(path(rec['file']),allow_pickle=False) as z:
  assert json.loads(str(z['metadata_json']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata_json'}
  for n in names:
   a=z[n].copy();capture('loaded_'+n,a);sd=rec['metadata']['schema'][n]
   assert list(a.shape)==sd['shape'] and str(a.dtype)==sd['dtype'] and sd['finite'] is True and np.all(np.isfinite(a));out[n]=a
 return out

# Guarded definitions only; no function/array evaluation in authoring.
# Caller authenticates fullmetric sigma1 ARM00003 plus force V003 LOADS point order.
# np and capture(name,array) supplied by the root-owned caller. Coordinates/time
# are the inherited geometrical kpc and kpc/c chart; p is specific covariant p_i.
# Mapping witness: READONLY_FORCE_V003_ORDINARY_SOURCE_MAPPING_V001.json
# SHA 585bcda308a3f7a4522f76b456feba1a50836994d4da35eb1cf89a713269d95d.
# No metric inverse, interpolation, source continuation or time history is built.

def ordinary_canonical_spatial_rates(g,hi,Ga,p,label):
 a=np.einsum('plam,pln->pamn',Ga,g);dg=a+np.swapaxes(a,2,3)
 ea=np.einsum('plam,pln->pamn',abs(Ga),abs(g));edg=ea+np.swapaxes(ea,2,3)
 dhi=-np.einsum('pmi,pain,pnj->pamj',hi,dg,hi)
 edhi=np.einsum('pmi,pain,pnj->pamj',abs(hi),edg,abs(hi))
 N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 ih=hi[:,1:,1:]+beta[:,:,None]*beta[:,None,:]/N[:,None,None]**2
 dh=dg[:,:,1:,1:];dih=-np.einsum('pmi,pain,pnj->pamj',ih,dh,ih)
 eih=abs(hi[:,1:,1:])+abs(beta[:,:,None]*beta[:,None,:])/N[:,None,None]**2
 edih=np.einsum('pmi,pain,pnj->pamj',eih,edg[:,:,1:,1:],eih)
 dN=.5*N[:,None]**3*dhi[:,:,0,0];edN=.5*N[:,None]**3*edhi[:,:,0,0]
 dbeta=2*N[:,None,None]*dN[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 edbeta=2*N[:,None,None]*edN[:,:,None]*abs(hi[:,None,0,1:])+N[:,None,None]**2*edhi[:,:,0,1:]
 up=np.einsum('pij,pj->pi',ih,p);gamma=np.sqrt(1+np.sum(p*up,axis=1))
 xdot=N[:,None]*up/gamma[:,None]-beta
 Hamiltonian=N*gamma-np.sum(beta*p,axis=1)
 pdot=-dN[:,1:]*gamma[:,None]-N[:,None]*np.einsum('pi,paij,pj->pa',p,dih[:,1:],p)/(2*gamma[:,None])+np.einsum('pai,pi->pa',dbeta[:,1:],p)
 pdot_envelope=edN[:,1:]*gamma[:,None]+N[:,None]*np.einsum('pi,paij,pj->pa',abs(p),edih[:,1:],abs(p))/(2*gamma[:,None])+np.einsum('pai,pi->pa',edbeta[:,1:],abs(p))
 out=dict(dg=dg,dhi=dhi,N=N,beta=beta,ih=ih,dh=dh,dih=dih,dN=dN,dbeta=dbeta,up=up,gamma=gamma,Hamiltonian=Hamiltonian,xdot=xdot,pdot_one_sided=pdot,pdot_envelope=pdot_envelope,operation_dg=edg,operation_dhi=edhi,operation_dN=edN,operation_dbeta=edbeta,operation_dih=edih)
 for k,v in out.items():capture(label+'_'+k,v)
 assert np.all(np.isfinite(N)) and np.all(N>0) and np.all(np.isfinite(gamma)) and np.all(gamma>=1)
 assert all(np.all(np.isfinite(v)) for v in out.values())
 # On the razor-thin source Ga is the authenticated upper one-sided jet.
 # A reflected mean requires the separately disclosed symmetric sheet branch;
 # neither zero vertical traction nor a smooth continuation is inferred here.
 return out

def ordinary_canonical_spatial_rate_fixture(label):
 # Fresh nonuniform-lapse Cartesian control, not a replay of a parent fixture.
 # N=5/4, d_R N=3/8, p_R=3/4: gamma=5/4, xdot_R=3/4,
 # pdot_R=-15/32. Transverse canonical momenta are conserved.
 g=np.diag([-25/16,1.,1.,1.])[None,:,:];hi=np.diag([-16/25,1.,1.,1.])[None,:,:]
 Ga=np.zeros((1,4,4,4));Ga[:,0,0,1]=3/10;Ga[:,0,1,0]=3/10;Ga[:,1,0,0]=15/32
 p=np.array([[3/4,0.,0.]]);out=ordinary_canonical_spatial_rates(g,hi,Ga,p,label)
 expected=np.array([[5/4,3/8,5/4,25/16,3/4,0.,0.,-15/32,0.,0.]])
 actual=np.column_stack((out['N'],out['dN'][:,1],out['gamma'],out['Hamiltonian'],out['xdot'],out['pdot_one_sided']))
 envelope=np.column_stack((abs(out['N']),out['operation_dN'][:,1],abs(out['gamma']),abs(out['Hamiltonian']),abs(out['xdot']),out['pdot_envelope']))
 return dict(g=g,hi=hi,Ga=Ga,p=p,actual=actual,expected=expected,envelope=envelope)

def geodesic_canonical_contraction(g,Ga,u,label):
 # Independent covariant Euler row dp_i/dt=Gamma^lambda_{i mu}u_lambda u^mu/u^0.
 uc=np.einsum('pln,pn->pl',g,u);euc=np.einsum('pln,pn->pl',abs(g),abs(u))
 val=np.einsum('plam,pl,pm->pa',Ga[:,:,1:,:],uc,u)/u[:,0,None]
 env=np.einsum('plam,pl,pm->pa',abs(Ga[:,:,1:,:]),euc,abs(u))/abs(u[:,0,None])
 for n,a in dict(u=u,uc=uc,uc_envelope=euc,actual=val,envelope=env).items():capture(label+'_'+n,a)
 return val,env

def calculation(metric,force):
 global RAW
 m=read_parent(metric,('source_g','source_hi','source_Ga','source_R','source_Z','source_k','source_D','source_Gamma','source_vertical_sheet_contact_plus','source_vertical_sheet_contact_minus'))
 f=read_parent(force,('ordinary_input_source_g','ordinary_input_source_R','ordinary_input_source_Z','ordinary_input_source_specific_covariant_p','ordinary_input_source_mass_weight','ordinary_input_source_indices','ordinary_input_source_right_weight','ordinary_gamma'))
 for n in ('g','R','Z'):
  a=m['source_'+n];b=f['ordinary_input_source_'+n];assert a.dtype==b.dtype and a.shape==b.shape and a.tobytes()==b.tobytes(),n
 input_data=dict(m,**f);pair('INPUT',input_data,dict(kind='exact_same_point_source_metric_connection_and_canonical_momenta',sigma=1.,points=4832,source=metric,force_loads=force,new_source_terms=False))
 RAW={};v=ordinary_canonical_spatial_rate_fixture('fresh_lapse');check('fresh_nonuniform_lapse_Hamiltonian_rates',v['actual'],v['expected'],v['envelope'])
 u=np.array([[1.,3/4,0.,0.]]) # gamma/N=1, contravariant u_R=3/4.
 gv,ge=geodesic_canonical_contraction(v['g'],v['Ga'],u,'fresh_geodesic')
 check('fresh_Hamiltonian_covariant_geodesic',RAW['fresh_lapse_pdot_one_sided'],gv,RAW['fresh_lapse_pdot_envelope']+ge)
 pair('FIXTURE',dict(RAW),dict(kind='two_fresh_nonuniform_lapse_fixture_controls',controls=list(CHECKS),synthetic_only=True))
 RAW={};g=m['source_g'];hi=m['source_hi'];Ga=m['source_Ga'];p=f['ordinary_input_source_specific_covariant_p'];o=ordinary_canonical_spatial_rates(g,hi,Ga,p,'ordinary')
 D=m['source_D'];assert np.all(D>0);u=m['source_k']/np.sqrt(D)[:,None]
 uc=np.einsum('pab,pb->pa',g,u);euc=np.einsum('pab,pb->pa',abs(g),abs(u))
 a=np.column_stack((o['gamma'],o['Hamiltonian'],o['xdot']));b=np.column_stack((f['ordinary_gamma'],-uc[:,0],u[:,1:]/u[:,0,None]))
 e=np.column_stack((abs(o['gamma'])+abs(f['ordinary_gamma']),abs(o['N']*o['gamma'])+abs(o['beta']*p).sum(axis=1)+euc[:,0],abs(o['N'][:,None]*o['up']/o['gamma'][:,None])+abs(o['beta'])+abs(u[:,1:]/u[:,0,None])))
 check('actual_registered_worldline_Hamiltonian_chart',a,b,e)
 gv,ge=geodesic_canonical_contraction(g,Ga,u,'ordinary_geodesic');check('actual_Hamiltonian_covariant_geodesic',o['pdot_one_sided'],gv,o['pdot_envelope']+ge)
 data=dict(RAW);data.update(source_R=m['source_R'],source_Z=m['source_Z'],source_mass_weight=f['ordinary_input_source_mass_weight'],source_indices=f['ordinary_input_source_indices'],source_right_weight=f['ordinary_input_source_right_weight'],source_upper_vertical_contact=m['source_vertical_sheet_contact_plus'],source_lower_vertical_contact=m['source_vertical_sheet_contact_minus'])
 pair('ORDINARY',data,dict(kind='instantaneous_canonical_position_momentum_rates_from_held_metric_first_jet',sigma=1.,points=4832,controls=CHECKS[2:],vertical_scope='source_Ga is upper one-sided; no reflected mean or traction-free continuation adopted',source_history=None,ordinary_support_evolution=None,outer_ports=None,new_source_terms=False))

def main():
 global np,OWNER,INPUTS,RAW
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args();assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS
 assert PROTOCOL_SHA and sha(STEM+'.md')==PROTOCOL_SHA and not list(BASE.glob(STEM+'_*'))
 INPUTS={str(path(n).resolve()):h for n,h in PINS.items()};INPUTS[str(path(STEM+'.md').resolve())]=PROTOCOL_SHA;INPUTS[str(Path(__file__).resolve())]=sha(__file__)
 for n,h in INPUTS.items():assert sha(n)==h,n
 owner=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__));OWNER=owner;json_file(STEM+'_OWNER_START.json',owner)
 try:
  map_audit=json.loads(path('READONLY_FORCE_V003_ORDINARY_SOURCE_MAPPING_V001.json').read_text());assert map_audit['status']=='SAVED_ORDINARY_MAPPING_PASS' and map_audit['source_Ga_usable_with_exact_saved_geometry'] is True and map_audit['source_hi_owned'] is True and map_audit['sigma']==1. and map_audit['points']==4832
  mr=json.loads(path('CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RESULT.json').read_text());fr=json.loads(path('CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json').read_text());mc=next(x for x in mr['cases'] if x['sigma']==1.);metric=mc['checkpoint'];force=fr['cases'][0]['loads']
  for stem,result,pid in (('CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001',mr,13990),('CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003',fr,36387)):
   rc=json.loads(path(stem+'_RECEIPT.json').read_text());assert rc['status']=='CLOSED' and rc['owner']==result['owner'] and result['owner']['pid']==pid and rc['result_sha256']==PINS[stem+'_RESULT.json'] and rc.get('error_sha256') is None
  assert metric['metadata']['sigma']==1. and fr['cases'][0]['sigma']==1. and all(v is False for v in fr['qualification'].values())
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(sigma=1.,points=4832,controls=4,pairs=3,tolerance=TOL,floor=1e-30,new_source_terms=False,physical_history=None),qualification=FLAGS))
  import numpy as npx
  np=npx;calculation(metric,force);assert len(RECORDS)==3 and len(CHECKS)==4 and all(c['passed'] for c in CHECKS)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_ORDINARY_CANONICAL_RATE_ARITHMETIC_PASS',checkpoints=RECORDS,controls=CHECKS,qualification=FLAGS,unknowns=dict(ordinary_support_evolution=None,source_history=None,metric_evolution=None,physical_exterior=None,vertical_traction_law=None)))
  recheck();json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck();print('PASS',len(CHECKS),len(RECORDS),flush=True);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None
  try:
   if np is not None and RAW:pair('ERROR_RAW',dict(RAW),dict(kind='unaccepted_available_operands',controls=list(CHECKS)))
  except BaseException:raw_error=traceback.format_exc()
  for p in BASE.glob(STEM+'_*'):
   if p.is_file():p.chmod(0o444);CREATED[p.name]=sha(p)
  prior=sha(STEM+'_RECEIPT.json') if path(STEM+'_RECEIPT.json').exists() else None
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,controls=CHECKS,checkpoints=RECORDS,preserved_outputs=dict(CREATED),prior_receipt_sha256=prior,qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=None,error_sha256=eh,qualification=FLAGS))
  return 1

if __name__=='__main__':raise SystemExit(main())
