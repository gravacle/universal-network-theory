"""Root-authorized saved-only EH compact-divergence diagnosis.

Only frozen tensors, elementary contractions, scalar polynomial identities and
grid-cell classification are evaluated. No producer is imported, and no field
operator, variation, inverse, solve, Gram, eigensystem or evolution is replayed.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib, json, math, os, traceback

BASE=Path(__file__).resolve().parent
STEM='ROOT_AUTHORIZED_SAVED_EH_COMPACT_DIVERGENCE_DIAGNOSIS_V001'
SOURCE='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002'
METRIC='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
RESULT_SHA='82dc17bc2d3d5ab730110887ea24c67d5b5b99fdff843397d98b455a8b5f29d2'
RECEIPT_SHA='bdbe52eaf088bf2139d1bc7c385dcee755cd1fffcbbfef8467d86c85edfc46a7'
METRIC_RESULT_SHA='ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798'
METRIC_RECEIPT_SHA='eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde'
BOXES=((2.,12.),(16.,48.));SIGMAS=(.1,1.,10.,100.);C=1.98
INPUTS={};OUTPUTS={};RAW={};OWNER=None
FLAGS=dict(physical_meridional_flow_inferred=False,constraint_solution_qualified=False,
           metric_or_source_changed=False,activity_extended=False,operator_replayed=False)

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def bound(name,expected):
 p=BASE/name;assert p.is_file() and p.stat().st_mode&0o222==0
 actual=sha(p);assert actual==expected,(name,actual,expected)
 INPUTS[name]=actual;return p
def read_json(name,expected):return json.loads(bound(name,expected).read_text())
def publish_json(name,obj):
 p=BASE/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p)
def publish_npz(name,arrays):
 p=BASE/name
 with p.open('xb') as f:np.savez(f,**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p)
def certify_pair(pair,receipt):
 assert receipt['output_sha256'][pair['file']]==pair['sha256']
 assert receipt['output_sha256'][pair['commit_file']]==pair['commit_sha256']
 bound(pair['file'],pair['sha256']);cm=read_json(pair['commit_file'],pair['commit_sha256'])
 assert cm['file']==pair['file'] and cm['sha256']==pair['sha256']
 return cm
def select(name,names):
 with np.load(BASE/name,allow_pickle=False) as f:out={k:f[k].copy() for k in names}
 for k,v in out.items():assert v.dtype.kind in 'fiu' and np.all(np.isfinite(v)),k
 return out
def metric_derivative_from_saved_connection(g,Ga):
 # Metric compatibility at the saved first jet; no derivative is taken.
 one=np.einsum('plk,plaj->pajk',g,Ga,optimize=True)
 return one+one.swapaxes(2,3)
def scaled_error(a,b,envelope):
 error=abs(a-b);assert np.all(np.isfinite(error)) and np.all(envelope>=0)
 assert np.all(error[envelope==0]==0)
 ratio=np.zeros_like(error);np.divide(error,envelope,out=ratio,where=envelope>0)
 return float(ratio.max(initial=0)),float(error.max(initial=0))
def partition_report(value,weight,active,cutR,cutZ):
 groups=(('uncut',~cutR&~cutZ),('radial_cut_only',cutR&~cutZ),
         ('vertical_cut_only',~cutR&cutZ),('both_cut',cutR&cutZ))
 return {name:dict(points=int(np.count_nonzero(active&mask)),
                  sum=float(np.sum(weight[mask]*value[mask]))) for name,mask in groups}
def exact_witness():
 a2=Fraction(1,3)
 radial=2*((1-a2)**3-6*a2*(1-a2)**2)
 def moment(n):return sum(Fraction(math.comb(n,k),3**(k//2)) for k in range(0,n+1,2))/2**n
 vertical=1-9*moment(2)+15*moment(4)-7*moment(6)
 assert radial==Fraction(-32,27) and vertical==Fraction(2,27)
 return dict(radial=dict(continuous=0,two_node_Gauss_integral_divided_by_halfwidth=str(radial)),
             vertical=dict(continuous=0,two_node_Gauss_integral=str(vertical)),
             proof='R=m+d*x,bR=(1-x^2)^3; y in[0,1],bZ=y*(1-y^2)^3. Boundary flux is zero. Fractions exact.',
             interpretation='With positive H/C the EH radial artifact is positive and vertical artifact negative; not trial-data evaluation.')

def main():
 global np,OWNER,RAW
 assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace is already used.'
 OWNER=dict(owner='root_authorized_saved_only_auditor',pid=os.getpid(),started=now(),
            scope='All four frozen arms: EH divergence identity and quadrature support partition only',
            authorization='Root explicit NEW_TASK authorizes actual SMALL SAVED-ONLY meridional EH diagnosis',
            source_file=Path(__file__).name,source_sha256=sha(__file__))
 publish_json(STEM+'_OWNER_START.json',OWNER)
 source=read_json(SOURCE+'_RESULT.json',RESULT_SHA)
 receipt=read_json(SOURCE+'_RECEIPT.json',RECEIPT_SHA)
 assert receipt['status']=='CLOSED' and receipt['owner']['pid']==23177
 assert receipt['result_sha256']==RESULT_SHA and source['owner']==receipt['owner']
 assert len(source['controls'])==42 and all(x['passed'] for x in source['controls'])
 assert tuple(x['sigma'] for x in source['cases'])==SIGMAS
 bound(receipt['owner']['source_file'],receipt['owner']['source_sha256'])
 metric=read_json(METRIC+'_RESULT.json',METRIC_RESULT_SHA)
 mr=read_json(METRIC+'_RECEIPT.json',METRIC_RECEIPT_SHA)
 assert mr['status']=='CLOSED' and mr['result_sha256']==METRIC_RESULT_SHA
 assert tuple(x['sigma'] for x in metric['cases'])==SIGMAS
 input_pair=metric['checkpoints'][0];certify_pair(input_pair,mr)
 for old,new in zip(source['cases'],metric['cases']):
  certify_pair(old['checkpoint'],receipt);certify_pair(new['checkpoint'],mr)
  assert old['checkpoint']['metadata']['metric_parent_file']==new['checkpoint']['file']
  assert old['checkpoint']['metadata']['metric_parent_sha256']==new['checkpoint']['sha256']
 INPUTS[Path(__file__).name]=sha(__file__)
 import numpy as np_local
 np=np_local
 grid=select(input_pair['file'],('r_kpc','z_kpc'));rg,zg=grid['r_kpc'],grid['z_kpc']
 assert rg.shape==(87,) and zg.shape==(45,) and np.all(np.diff(rg)>0) and np.all(np.diff(zg)>0)
 rows=[];arms=[]
 for case,mc in zip(source['cases'],metric['cases']):
  sigma=case['sigma'];RAW={};armrows=[];H=case['checkpoint']['metadata']['owned_Hbar']
  assert H>0 and math.isfinite(H)
  for iq,count in enumerate((1972,1972,1938,1938)):
   q=f'q{iq}_'
   native=select(case['checkpoint']['file'],[q+x for x in ('R','Z_coordinate','reference_volume','chart_N','chart_density','metric_EH_p','new_K','old_K','K_expected')]+[f'b{ib}_a{d}_q{iq}_'+x for ib in range(2) for d in (1,2) for x in ('b','db','Hamiltonian_signed_density')])
   old=select(mc['checkpoint']['file'],[q+x for x in ('g','Ga')])
   R,Z,vol=native[q+'R'],native[q+'Z_coordinate'],native[q+'reference_volume']
   g,Ga=old[q+'g'],old[q+'Ga'];h=g[:,1:,1:];hd=np.diagonal(h,axis1=1,axis2=2)
   assert R.shape==Z.shape==vol.shape==(count,) and np.all(vol>0) and np.all(hd>0)
   ihd=1/hd  # Elementary division in the known diagonal chart, no inverse operation.
   diagmask=np.eye(3)[None,:,:];hdiag=hd[:,:,None]*diagmask
   assert np.array_equal(h,hdiag)
   dg=metric_derivative_from_saved_connection(g,Ga);dh=dg[:,1:,1:,1:]
   egone=np.einsum('plk,plaj->pajk',abs(g),abs(Ga),optimize=True)
   edh=(egone+egone.swapaxes(2,3))[:,1:,1:,1:]
   sqrth=native[q+'chart_density']/native[q+'chart_N'];ratio=sqrth/R
   ih=ihd[:,:,None]*diagmask
   Kold=native[q+'old_K'];Ktold=np.sum(ihd*np.diagonal(Kold,axis1=1,axis2=2),axis=1)
   piold=sqrth[:,None,None]*(ihd[:,:,None]*Kold*ihd[:,None,:]-Ktold[:,None,None]*ih)/(2*C)
   piiso=-sqrth[:,None,None]*H*ih/C;pi=native[q+'metric_EH_p']
   penv=abs(pi)+abs(piold)+abs(piiso)
   pierr=scaled_error(pi,piold+piiso,penv)
   logderiv=.5*np.sum(ihd[:,None,:]*np.diagonal(dh,axis1=2,axis2=3),axis=2)
   elog=.5*np.sum(abs(ihd[:,None,:])*np.diagonal(edh,axis1=2,axis2=3),axis=2)
   ci=np.searchsorted(rg,R,side='right')-1;cj=np.searchsorted(zg,Z,side='right')-1
   assert np.all((ci>=0)&(ci<len(rg)-1)&(cj>=0)&(cj<len(zg)-1))
   RAW[q+'R']=R;RAW[q+'Z']=Z;RAW[q+'reference_volume']=vol
   RAW[q+'cell_R_index']=ci;RAW[q+'cell_Z_index']=cj
   RAW[q+'saved_pi_EH']=pi;RAW[q+'isotropic_pi_EH']=piiso;RAW[q+'old_rotating_pi_EH']=piold
   for ib,(lo,hi) in enumerate(BOXES):
    cutR=((rg[ci]<lo)&(rg[ci+1]>lo))|((rg[ci]<hi)&(rg[ci+1]>hi))
    cutZ=(zg[cj]<16)&(zg[cj+1]>16)
    for d in (1,2):
     tag=f'b{ib}_a{d}_q{iq}_';b=native[tag+'b'];db=native[tag+'db'];actual=native[tag+'Hamiltonian_signed_density'][:,3]
     Lie=np.einsum('pk,pkij->pij',b,dh,optimize=True)+np.einsum('pik,pjk->pij',h,db[:,1:],optimize=True)+np.einsum('pkj,pik->pij',h,db[:,1:],optimize=True)
     eLie=np.einsum('pk,pkij->pij',abs(b),edh,optimize=True)+np.einsum('pik,pjk->pij',abs(h),abs(db[:,1:]),optimize=True)+np.einsum('pkj,pik->pij',abs(h),abs(db[:,1:]),optimize=True)
     oldrow=np.einsum('pij,pij->p',piold,Lie,optimize=True)/R
     trace_db=np.trace(db[:,1:],axis1=1,axis2=2)
     iso=-(2*H/C)*ratio*(trace_db+np.sum(logderiv*b,axis=1))
     expected=iso+oldrow
     ediv=(2*H/C)*ratio*(np.trace(abs(db[:,1:]),axis1=1,axis2=2)+np.sum(elog*abs(b),axis=1))
     en=abs(actual)+ediv+np.einsum('pij,pij->p',abs(piold),eLie,optimize=True)/R
     err=scaled_error(actual,expected,en)
     rotational_env=np.einsum('pij,pij->p',abs(piold),eLie,optimize=True)/R
     rerr=scaled_error(oldrow,np.zeros_like(oldrow),rotational_env)
     flat=-(2*H/C)*(trace_db+b[:,0]/R)
     active=np.any(b!=0,axis=1)|np.any(db!=0,axis=(1,2))
     for key,val in dict(original_EH_signed_density=actual,independent_isotropic_divergence=iso,old_rotating_density=oldrow,identity_envelope=en,flat_measure_density=flat,conformal_geometry_difference=iso-flat,active=active,radial_cut=cutR,vertical_cut=cutZ).items():RAW[tag+key]=val.copy()
     row=dict(sigma=sigma,rectangle=[lo,hi],direction=('radial' if d==1 else 'vertical'),quadrature_column=iq,points=count,active_points=int(active.sum()),identity_max_scaled_error=err[0],identity_max_absolute_error=err[1],old_rotation_scaled_zero_error=rerr[0],old_rotation_absolute= float(abs(oldrow).max(initial=0)),pi_split_max_scaled_error=pierr[0],original_sum=float(np.sum(vol*actual)),independent_divergence_sum=float(np.sum(vol*iso)),old_rotation_sum=float(np.sum(vol*oldrow)),flat_measure_sum=float(np.sum(vol*flat)),conformal_geometry_difference_sum=float(np.sum(vol*(iso-flat))),partition=partition_report(actual,vol,active,cutR,cutZ),qualification='Original signed row retained; continuous compact EH divergence is zero; discrete value is quadrature alias if pointwise identity passes.')
     armrows.append(row);rows.append(row)
  publish_npz(STEM+f'_SIGMA_{str(sigma).replace(".","p")}_OPERANDS.npz',RAW)
  combined=[]
  for box in BOXES:
   for direction in ('radial','vertical'):
    selected=[r for r in armrows if tuple(r['rectangle'])==box and r['direction']==direction]
    assert len(selected)==4
    combined.append(dict(rectangle=list(box),direction=direction,**{key:sum(r[key] for r in selected) for key in ('original_sum','independent_divergence_sum','old_rotation_sum','flat_measure_sum','conformal_geometry_difference_sum')},partition={k:dict(points=sum(r['partition'][k]['points'] for r in selected),sum=sum(r['partition'][k]['sum'] for r in selected)) for k in ('uncut','radial_cut_only','vertical_cut_only','both_cut')}))
  arms.append(dict(sigma=sigma,Hbar=H,combined_rows=combined))
  print(json.dumps(dict(pid=os.getpid(),sigma=sigma,rows=len(armrows),max_identity_scaled_error=max(r['identity_max_scaled_error'] for r in armrows)),sort_keys=True),flush=True)
 assert len(rows)==64 and all(r['identity_max_scaled_error']<=2e-11 and r['pi_split_max_scaled_error']<=2e-11 and r['old_rotation_scaled_zero_error']<=2e-11 for r in rows)
 result=dict(owner=OWNER,status='SAVED_POINTWISE_DIVERGENCE_IDENTITY_CONFIRMED',inputs=INPUTS,arms=arms,per_quadrature_rows=rows,exact_fraction_witness=exact_witness(),flags=FLAGS,
  scope='Only saved EH tensors and compact meridional tests. No producer/helper/operator/inverse/solve/eigen/evolution. Old original signed rows unchanged. Four arms, four authentic quadrature columns, both boxes and both meridional directions.',
  conclusion='On this supplied diagonal axisymmetric trial, old rotational EH contribution is zero and the owned spatially constant isotropic H contribution is a compact total divergence. Its continuous integral is zero; the retained nonzero quadrature sums measure numerical integration alias, not physical meridional flow.',
  quadrature_scope='Two Gauss nodes/coordinate are exact only through polynomial degree three. Bumps/divergences reach degree six, support crosses mesh cells, and exp(-3Phi) is nonpolynomial. Partition is diagnostic, not a new quadrature or a field correction.',
  next_nodal_scope='Use genuine Q1 test loads and conservative momentum face/incidence assembly. Pointwise canonical data require an explicit mixed or nodal projection registration. No solve or physical exterior/Cauchy qualification here.')
 publish_json(STEM+'_RESULT.json',result)
 publish_json(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS))

if __name__=='__main__':
 try:main()
 except BaseException:
  detail=traceback.format_exc()
  if OWNER is not None:
   try:
    if RAW and 'np' in globals():publish_npz(STEM+'_ERROR_RAW.npz',RAW)
   except BaseException:detail+='\nRaw preservation failure:\n'+traceback.format_exc()
   for p in BASE.glob(STEM+'_*'):
    if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)
   if not (BASE/(STEM+'_ERROR.json')).exists():publish_json(STEM+'_ERROR.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),error=detail,inputs=INPUTS,outputs=OUTPUTS.copy(),qualification=FLAGS))
  raise
