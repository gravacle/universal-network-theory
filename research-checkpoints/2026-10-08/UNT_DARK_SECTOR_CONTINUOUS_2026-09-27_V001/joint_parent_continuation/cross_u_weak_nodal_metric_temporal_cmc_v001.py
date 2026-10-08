"""Guarded new six-metric weak temporal/CMC kinetic sample; root-only execution."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='60de28cc558734f648fc3845ebf18ab47b10f0cf9d06a89142e59268951baf7a'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1
TOL=2e-11;LINEAR_TOL=1e-10;NATIVE_CAP=160;EXPECTED_CONTROLS=49
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(full_metric_map_qualified=False,CMC_qualified=False,force_qualified=False,history_qualified=False,exterior_qualified=False,physical_inertia_qualified=False,source_qualified=False,physical_metric_qualified=False,galaxy_velocity_qualified=False)
PINS={'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_AND_CMC_EXTENSION_V001.md': '78491aa4158dec6152a19136d5b3265cc63cdc965ebf4002d8df371074b46806', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_MAP_AND_BASIS_V001.md': 'faf6d1d5cccb9266cde70c1a6264745da2cea9e1f3ceaab871a760ee1d0bada9', 'CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md': '60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424', 'cross_u_saved_full_native_adm_legendre_v002.py': '9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0', 'author_fragment_weak_metric_cmc_admission_v001.txt': 'f014280bd217b41cce1d70f5f0607e2bdf2e67c1ca795ddae8e4f61445ee269c', 'author_fragment_weak_metric_cmc_admission_v002.txt': 'f29e56c6c317ec6a734ab662637f6c9f70885d4e3d22fa0e1c7126f5246114a4', 'authoring_cross_u_weak_nodal_metric_temporal_cmc_v001_788_9a7b2556.py': '9a7b255638329af90e1de9d8f5f46c811669ad1f9f87f69196264eb729cef77b', 'authoring_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_11_76eded35.md': '76eded35031a5f1035b6841992bde642e2f51a83d316405fb7e06b6d3fc0d2e6', 'author_fragment_weak_nodal_metric_fixtures_v001.txt': '064dc395993f25181624b16a7a8b0c0ac81e7fc95a53f5eeec3414354e08f957', 'authoring_cross_u_weak_nodal_metric_temporal_cmc_v001_899_ade4c6d3.py': 'ade4c6d37a1343690bdb964a69449d4b20f30044abdaccd591d6e84a685c704f', 'authoring_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_12_750494e7.md': '750494e7f22931e086ad7c2cecd9695adc2944ccda97a5d9a25317429cb5d3f0'}

def now():return datetime.now(timezone.utc).isoformat()


def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p


def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()


def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Unsupported/nonfinite metadata '+type(v).__name__)


def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def publish(n,raw):
 p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;OUTPUTS[n]=sha(p);return OUTPUTS[n]


def json_file(n,v):return publish(n,encode(v))


def check(label,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);k=len(CHECKS)
 CONTEXT.update(control=label,ordinal=k)
 for n,v in (('actual',a),('expected',b),('envelope',e)):RAW[f'control_{k:03d}_{label}_{n}']=v.copy()
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=TOL,passed=error<=TOL);CHECKS.append(row)
 assert row['passed'],(label,error)


def checkpoint(tag,arrays,meta,failed=False):
 schema={}
 for k,a in arrays.items():
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiub'
  finite=bool(np.all(np.isfinite(a)));assert failed or finite,k
  schema[k]=dict(shape=list(a.shape),dtype=str(a.dtype),finite=finite)
 md=json.loads(encode(dict(meta,owner=OWNER,qualification=FLAGS,schema=schema,failed=failed)).decode())
 text=encode(md).decode();name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p);rec=dict(file=name,sha256=OUTPUTS[name],metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert str(f['metadata_json'])==text and set(f.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert f[k].shape==a.shape and f[k].dtype==a.dtype and np.array_equal(f[k],a,equal_nan=True),k
 return rec


def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for n,s in r['metadata']['schema'].items():assert list(f[n].shape)==s['shape'] and str(f[n].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[n])))==s['finite']
 if strict:
  assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}


def seal_actual():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)


def read_pair(rec,names):
 assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={};metadata_key='metadata' if rec['file'].startswith(BAND+'_') else 'metadata_json'
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{metadata_key}
  assert json.loads(str(f[metadata_key]))==rec['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a
   s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n
   out[n]=a
 return out


def resolve_record(ref):
 assert sha(path(ref['file']))==ref['sha256'] and sha(path(ref['commit_file']))==ref['commit_sha256']
 out=json.loads(path(ref['commit_file']).read_text())
 assert out['file']==ref['file'] and out['sha256']==ref['sha256']
 return dict(out,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])


def capture(name,a):
 AVAILABLE[name]=a.copy();return a


def finite_real(name,a):
 capture(name,a);assert a.dtype.kind=='f' and np.all(np.isfinite(a)),name
 return a


def native_mask():
 m=np.ones((3,87,45),dtype=bool);m[:,0]=False;m[1,:,0]=False;return m


def lift_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,0,0,:]=0;y[...,1,0,:]=y[...,1,1,:];y[...,1,:,0]=0;y[...,2,0,:]=y[...,2,1,:];return y


def restrict_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,1,1,:]+=y[...,1,0,:];y[...,2,1,:]+=y[...,2,0,:];y[..., :,0,:]=0;y[...,1,:,0]=0;return y


def evaluate_velocity(x,geo,jet=0):
 # Covector phi value R²N; radial derivative is 2RN+R²NR.
 y=lift_velocity(x);out=np.zeros(x.shape[:-3]+(4,86,44,3))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=np.broadcast_to(h[...,None],(86,44,3)).copy();factor[...,2]=R**2*h
   if jet==1:factor[...,2]+=2*R*geo['hats'][iq,a,0]
   out[...,iq,:,:,:]+=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)*factor
 return out.reshape(x.shape[:-3]+(15136,3))


def scatter_velocity(field,geo):
 assert field.shape[-2:]==(15136,3)
 f=field.reshape(field.shape[:-2]+(4,86,44,3));out=np.zeros(field.shape[:-2]+(3,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=geo['dv'][iq].reshape(86,44)/R
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   factor=np.broadcast_to(geo['hats'][iq,a,0][...,None],(86,44,3)).copy();factor[...,2]*=R**2
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(f[...,iq,:,:,:]*wq[...,None]*factor,-1,-3)
 return restrict_velocity(out)


def scatter_velocity_independent(field,geo):
 out=np.zeros(field.shape[:-2]+(3,87,45));prefix=field.shape[:-2];groups=int(math.prod(prefix)) if prefix else 1;fo=field.reshape(groups,15136,3);oo=out.reshape(groups,3,87,45)
 for iq in range(4):
  R=geo['R'][iq];wq=geo['dv'][iq]/R;f=fo[:,iq*3784:(iq+1)*3784]
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for c in range(3):
    scale=R**2 if c==2 else np.ones_like(R)
    val=f[...,c]*wq*geo['hats'][iq,a,0].reshape(3784)*scale
    for k in range(groups):np.add.at(oo[k,c],(geo['cell_i']+i,geo['cell_j']+j),val[k])
 return restrict_velocity(out)


def point_action(v,b):
 mixed=v[1:]+np.einsum('jpik,pk->jpi',b['L'],v[0],optimize=True);modes=np.einsum('jpik,jpk->jpi',b['D'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['M0'],v[0],optimize=True)+np.einsum('jpki,jpk->pi',b['L'],modes,optimize=True)
 return np.concatenate((U[None],modes))


def point_action_envelope(v,b):
 mixed=abs(v[1:])+np.einsum('jpik,pk->jpi',b['eL'],abs(v[0]),optimize=True);modes=np.einsum('jpik,jpk->jpi',b['eD'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['eM0'],abs(v[0]),optimize=True)+np.einsum('jpki,jpk->pi',b['eL'],modes,optimize=True)
 return np.concatenate((U[None],modes))


def original_action(x,b,g):return scatter_velocity(point_action(evaluate_velocity(x,g),b),g)


def original_envelope(x,b,g):return scatter_velocity(point_action_envelope(evaluate_velocity(abs(x),g),b),g)


def apply_preconditioner(rhs,pre):
 r=rhs.transpose(0,2,3,1).reshape(33,3915,3)/pre['scale'][None]
 dz=np.linalg.solve(pre['D'],r[1:,...,None])[...,0];red=r[0]-np.einsum('jnik,jnk->ni',pre['B'],dz,optimize=True);u=np.linalg.solve(pre['M0'],red[...,None])[...,0]
 z=np.linalg.solve(pre['D'],(r[1:]-np.einsum('jnki,nk->jni',pre['B'],u,optimize=True))[...,None])[...,0];y=np.concatenate((u[None],z))/pre['scale'][None]
 return y.reshape(33,87,45,3).transpose(0,3,1,2)*pre['mask'][None]


def dot(a,b):return float(np.sum(a*b))


def solve_native(rhs,b,g,pre):
 x=np.zeros_like(rhs);capture('native_iterate',x);r=rhs.copy();capture('native_original_residual',r);z=apply_preconditioner(r,pre);capture('native_preconditioned_residual',z);p=z.copy();capture('native_search',p);rz=dot(r,z);capture('native_rz',np.array(rz));scale=pre['normscale'];den=float(np.linalg.norm(rhs/scale));capture('native_scaled_rhs_norm',np.array(den));denraw=float(np.linalg.norm(rhs));capture('native_rhs_norm',np.array(denraw));history=[]
 AVAILABLE.update(native_iterate=x.copy(),native_original_residual=r.copy(),native_search=p.copy(),native_preconditioned_residual=z.copy(),native_initial_rz=np.array(rz))
 capture('native_norm_denominators',np.array([den,denraw]));assert math.isfinite(den) and math.isfinite(denraw)
 assert (den>0 and denraw>0) or np.all(rhs==0),'Underflowed nonzero native norm'
 for k in range(NATIVE_CAP+1):
  ax=original_action(x,b,g);capture('native_original_action',ax);r=rhs-ax;capture('native_original_residual',r);ratio=max(float(np.linalg.norm(r/scale))/den,float(np.linalg.norm(r))/denraw) if den else 0.
  history.append((k,ratio));AVAILABLE.update(native_iterate=x.copy(),native_original_action=ax.copy(),native_original_residual=r.copy(),native_history=np.asarray(history,dtype=float),native_search=p.copy(),native_preconditioned_residual=z.copy());assert math.isfinite(ratio) and np.all(np.isfinite(ax)) and np.all(np.isfinite(r))
  if k and k%20==0:checkpoint('NATIVE_ITERATION',{n:AVAILABLE[n] for n in ('native_iterate','native_original_action','native_original_residual','native_history','native_search','native_preconditioned_residual')},dict(kind='resumable_unqualified_native_iterate',iteration=k))
  if ratio<=LINEAR_TOL:return x,ax,r,np.asarray(history,dtype=float)
  assert k<NATIVE_CAP,'Native weak map iteration cap retained'
  if k:
   z=apply_preconditioner(r,pre);capture('native_preconditioned_residual',z);newrz=dot(r,z);capture('native_updated_rz',np.array(newrz));assert newrz>0 and math.isfinite(newrz);capture('native_beta',np.array(newrz/rz));p=z+(newrz/rz)*p;capture('native_search',p);rz=newrz;capture('native_rz',np.array(rz))
  ap=original_action(p,b,g);capture('current_native_search_action',ap);pa=dot(p,ap);capture('native_search_energy',np.array(pa));assert pa>0 and rz>0 and math.isfinite(pa) and math.isfinite(rz)
  alpha=rz/pa;capture('native_alpha',np.array(alpha));assert math.isfinite(alpha);x=x+alpha*p;capture('native_iterate',x)


def linear_gate(label,residual,rhs,scale,modal=False):
 axes=(1,2,3) if modal else None
 if modal:
  a=np.linalg.norm(residual.reshape(32,-1),axis=1);d=np.linalg.norm(rhs.reshape(32,-1),axis=1);aa=np.linalg.norm((residual/scale).reshape(32,-1),axis=1);dd=np.linalg.norm((rhs/scale).reshape(32,-1),axis=1)
 else:a=np.array([np.linalg.norm(residual)]);d=np.array([np.linalg.norm(rhs)]);aa=np.array([np.linalg.norm(residual/scale)]);dd=np.array([np.linalg.norm(rhs/scale)])
 ratios=np.zeros((len(a),2));active=d>0;ratios[active,0]=a[active]/d[active];ratios[active,1]=aa[active]/dd[active]
 for n,v in (('residual_norm',a),('rhs_norm',d),('scaled_residual_norm',aa),('scaled_rhs_norm',dd),('actual',ratios)):RAW[label+'_'+n]=v.copy()
 assert np.all(np.isfinite(a)) and np.all(np.isfinite(d)) and np.all(np.isfinite(aa)) and np.all(np.isfinite(dd)) and np.all(np.isfinite(ratios))
 assert np.all((d>0)==(dd>0)) and np.all(a[~active]==0) and np.all(aa[~active]==0)
 k=len(CHECKS);error=float(np.max(ratios,initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=LINEAR_TOL,passed=error<=LINEAR_TOL);CHECKS.append(row);assert row['passed'],row


def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)


def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)


def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)


def metric_basis():
 e=np.zeros((6,3,3))
 for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[k,i,j]=e[k,j,i]=1
 return e


def symmetric_tensor_from_coordinates(p):
 t=np.zeros((len(p),3,3));t[:,0,0]=p[:,0];t[:,1,1]=p[:,1];t[:,2,2]=p[:,2]
 for k,(i,j) in enumerate(((0,1),(0,2),(1,2)),start=3):t[:,i,j]=t[:,j,i]=p[:,k]/2
 return t


def connection_momentum(s,Pi=None,Fup=None):
 Pi=s['Pi'] if Pi is None else Pi;Fup=s['Fup'] if Fup is None else Fup
 Z=s['Z'];U=s['U'];z=s['z'];hi=s['hi']
 sym=(Pi+np.swapaxes(Pi,2,3))/2
 Klo=np.einsum('pl,pa,pb->plab',Z,U,U)-np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo)
 D=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)-Kup)/2
 mx=-ALPHA*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 return D+mx,D,mx


def reduced_momenta(s,c,PiU=None,Pi=None,Ctime=None):
 PiU=s['PiU'] if PiU is None else PiU;Pi=s['Pi'] if Pi is None else Pi
 if Ctime is None:Ctime=connection_momentum(s)[0][:,0]
 pu=np.einsum('pa,pai->pi',PiU[:,0],c['JU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],c['JzU'])
 pz=Pi[:,:,0,1:]+Pi[:,:,0,0,None]*c['Jzz'][None,:,:]
 py=c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)
 pmetric=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',Ctime,c['embed'])+np.einsum('pa,pka->pk',PiU[:,0],c['Uh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],c['zh']))
 return py,pmetric


def connection_from_jet(hi,dg):
 p=len(hi);out=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out


def native_velocity_jet(s,c,y,k):
 # y has 99 reduced field velocities; k has six symmetric hdot coefficients.
 p=len(s['U']);y=np.broadcast_to(y,(p,99));k=np.broadcast_to(k,(p,6))
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',c['JU'],y[:,:3])+np.einsum('pka,pk->pa',c['Uh'],k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',c['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',c['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',c['zh'],k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,c['embed'])
 return du,dz,dg,connection_from_jet(s['hi'],dg)


def kinetic_tangent(s,du,dz,dGa,ell=ELL):
 dn=du+np.einsum('pbal,pl->pab',dGa,s['U']);dnz=dz-np.einsum('plab,jpl->jpab',dGa,s['z'])
 dV=np.einsum('pab,jpb->jpa',s['P'],np.einsum('pa,jpab->jpb',s['U'],dnz))
 dD=np.einsum('pac,jpcd,pbd->jpab',s['P'],dnz,s['P'])
 dF=lower_last(s['g'],dn)-np.swapaxes(lower_last(s['g'],dn),1,2)
 dFu=np.einsum('pac,pcd,pdb->pab',s['hi'],dF,s['hi'])
 dPiU=-ALPHA*np.einsum('pac,pcb->pab',s['hi'],dF)
 dPi=s['w'][:,None,None,None]*(np.einsum('pa,jpb->jpab',s['U'],raise_cov(s['hi'],dV))/s['omega'][:,None,None,None]**2-ell**2*np.einsum('pac,jpcd,pdb->jpab',s['hi'],dD,s['hi']))
 # Acceleration.Z is linear in all velocities; subtract the constant connection vertex.
 zero=dict(s,Z=np.zeros_like(s['Z']));dC=connection_momentum(zero,dPi,dFu)[0]
 return dict(du=du,dz=dz,dg_connection=dGa,delta_nu=dn,delta_nz=dnz,delta_V=dV,delta_D=dD,delta_F=dF,delta_PiU=dPiU,delta_Pi=dPi,delta_Ctime=dC[:,0])


def kinetic_gram(s,tangents,ell=ELL):
 dF=np.stack([x['delta_F'] for x in tangents]);dV=np.stack([x['delta_V'] for x in tangents]);dD=np.stack([x['delta_D'] for x in tangents])
 hi=s['hi'];w=s['w'];om=s['omega'];dens=np.sqrt(-np.linalg.det(s['g']))
 mx=-ALPHA*np.einsum('Apab,pac,pbd,Bpcd->pAB',dF,hi,hi,dF)/2
 tv=np.einsum('Ajpa,pab,Bjpb->jpAB',dV,hi,dV)/om[:,None,None,None]**2
 td=-ell**2*np.einsum('Ajpab,pac,pbd,Bjpcd->jpAB',dD,hi,hi,dD)
 out=dens[:,None,None]*(mx+np.einsum('j,jpAB->pAB',w,tv+td))
 env=kinetic_operation_gram_envelope(s,dict(dens=dens),tangents,ell)
 return out,env


def connection_from_jet_envelope(hi,dg):
 # hi is the saved inverse. dg may be the actual signed metric first jet OR
 # a previously propagated nonnegative envelope for that jet's construction.
 # Bound the three Christoffel summands BEFORE their +/- cancellation.
 p=len(hi);out=np.zeros((p,4,4,4));eh=abs(hi);ed=abs(dg)
 for a in range(4):
  for b in range(4):
   terms=ed[:,a,b,:]+ed[:,b,a,:]+ed[:,:,a,b]
   out[:,:,a,b]=np.einsum('plm,pm->pl',eh,terms)/2
 RAW['operation_connection_jet_envelope']=out.copy()
 return out


def velocity_operation_envelopes(s,c,y,k,chartenv):
 p=len(s['U']);y=abs(np.broadcast_to(y,(p,99)));k=abs(np.broadcast_to(k,(p,6)))
 e=abs(metric_basis());up=chartenv['up'];N,ga=c['N'],c['gamma']
 edga=np.einsum('pi,kij,pj->pk',up,e,up)/(2*ga[:,None])
 eUh=np.empty_like(c['Uh']);eUh[:,:,0]=edga/N[:,None]
 eUh[:,:,1:]=np.einsum('pij,kjl,pl->pki',abs(c['ih']),e,up)+abs(c['beta'])[:,None,:]*eUh[:,:,0,None]
 RAW['assembling_envelope_U_metric_chain']=eUh.copy()
 ezh=np.einsum('jpa,pka->jpk',abs(s['z']),eUh)/abs(s['U'][None,:,0,None])
 RAW['assembling_envelope_zt_metric_chain']=ezh.copy()
 embed=np.zeros_like(c['embed']);embed[:,:,1:,1:]=e[None]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,abs(c['beta']));embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',abs(c['beta']),e,abs(c['beta']))
 RAW['assembling_envelope_metric_embedding']=embed.copy()
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',chartenv['JU'],y[:,:3])+np.einsum('pka,pk->pa',eUh,k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',chartenv['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',chartenv['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',ezh,k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,embed)
 RAW.update(assembling_envelope_du=du.copy(),assembling_envelope_dz=dz.copy(),assembling_envelope_dg=dg.copy())
 Ga=connection_from_jet_envelope(s['hi'],dg)
 RAW['assembling_envelope_delta_connection']=Ga.copy()
 nu=du+np.einsum('pbal,pl->pab',Ga,abs(s['U']))
 nz=dz+np.einsum('plab,jpl->jpab',Ga,abs(s['z']))
 RAW.update(assembling_envelope_nu=nu.copy(),assembling_envelope_nz=nz.copy())
 # P=I+U_cov outer U contains cancellation even when its physical00 entry is0.
 uc=np.einsum('pab,pb->pa',abs(s['g']),abs(s['U']))
 Pe=np.eye(4)[None]+np.einsum('pa,pb->pab',uc,abs(s['U']))
 RAW['assembling_envelope_projector']=Pe.copy()
 qq=np.einsum('pa,jpab->jpb',abs(s['U']),nz)
 V=np.einsum('pab,jpb->jpa',Pe,qq)
 D=np.einsum('pac,jpcd,pbd->jpab',Pe,nz,Pe)
 nuc=np.einsum('pab,pcb->pca',abs(s['g']),nu)
 F=nuc+np.swapaxes(nuc,1,2)
 RAW.update(assembling_envelope_F=F.copy(),assembling_envelope_V=V.copy(),assembling_envelope_D=D.copy())
 return dict(du=du,dz=dz,dg=dg,Gamma=Ga,nu=nu,nz=nz,projector=Pe,F=F,V=V,D=D)


def kinetic_operation_gram_envelope(s,c,tangents,ell=ELL):
 # No new signed field/action or operator. Old callers lacking attachments retain
 # their original envelope; the admitted old tilted/aligned witnesses are copied.
 F=np.stack([t.get('envelope_F',abs(t['delta_F'])) for t in tangents])
 V=np.stack([t.get('envelope_V',abs(t['delta_V'])) for t in tangents])
 D=np.stack([t.get('envelope_D',abs(t['delta_D'])) for t in tangents])
 hi=abs(s['hi']);om=s['omega'];w=s['w'];dens=c['dens']
 mx=ALPHA*np.einsum('Apab,pac,pbd,Bpcd->pAB',F,hi,hi,F)/2
 vv=np.einsum('Ajpa,pab,Bjpb->jpAB',V,hi,V)/om[:,None,None,None]**2
 dd=ell**2*np.einsum('Ajpab,pac,pbd,Bjpcd->jpAB',D,hi,hi,D)
 out=dens[:,None,None]*(mx+np.einsum('j,jpAB->pAB',w,vv+dd))
 RAW['assembling_envelope_kinetic_Gram']=out.copy()
 return out


# Guarded incremental author draft. New metric/basis/CMC core follows.

def metric_mask():
 m=np.ones((6,87,45),dtype=bool);m[:,0]=False;m[3:5,:,0]=False;return m

def lift_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,0,:]=y[..., :,1,:];y[...,3:5,:,0]=0;return y

def restrict_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,1,:]+=y[..., :,0,:];y[..., :,0,:]=0;y[...,3:5,:,0]=0;return y

def metric_value_matrix(R):
 # Physical local order RR,ZZ,phiphi,RZ,Rphi,Zphi. Coefficient order a,b,c,d,e,f.
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F

def metric_R_matrix(R):
 F=np.zeros(R.shape+(6,6));F[...,0,1]=2*R;F[...,2,0]=2*R;F[...,3,3]=1;F[...,4,2]=3*R**2;F[...,5,4]=2*R
 return F

def evaluate_metric(x,geo,jet=0):
 y=lift_metric(x);out=np.zeros(x.shape[:-3]+(4,86,44,6))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=h[...,None,None]*F
   if jet==1:factor+=geo['hats'][iq,a,0][...,None,None]*metric_R_matrix(R)
   vals=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)
   out[...,iq,:,:,:]+=np.einsum('...ijb,ijab->...ija',vals,factor,optimize=True)
 return out.reshape(x.shape[:-3]+(15136,6))

def scatter_metric(field,geo):
 assert field.shape[-2:]==(15136,6)
 f=field.reshape(field.shape[:-2]+(4,86,44,6));out=np.zeros(field.shape[:-2]+(6,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=np.einsum('...ija,ijab->...ijb',f[...,iq,:,:,:],F,optimize=True)*wq[...,None]*geo['hats'][iq,a,0][...,None]
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(val,-1,-3)
 return restrict_metric(out)

def scatter_metric_independent(field,geo):
 out=np.zeros(field.shape[:-2]+(6,87,45));prefix=field.shape[:-2];ng=int(math.prod(prefix)) if prefix else 1;fo=field.reshape(ng,15136,6);oo=out.reshape(ng,6,87,45)
 for iq in range(4):
  R=geo['R'][iq];F=metric_value_matrix(R);wq=geo['dv'][iq]/R;f=fo[:,iq*3784:(iq+1)*3784]
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for c in range(6):
    val=np.sum(f*F[:, :,c][None],axis=-1)*wq*geo['hats'][iq,a,0].reshape(3784)
    for k in range(ng):np.add.at(oo[k,c],(geo['cell_i']+i,geo['cell_j']+j),val[k])
 return restrict_metric(out)

def scalar_lift(x):
 assert x.shape[-2:]==(87,45)
 y=x.copy();y[...,0,:]=y[...,1,:];return y

def scalar_scatter(field,geo):
 assert field.shape[-1]==15136
 f=field.reshape(field.shape[:-1]+(4,86,44));out=np.zeros(field.shape[:-1]+(87,45))
 for iq in range(4):
  wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[...,i:86+i,j:44+j]+=wq*geo['hats'][iq,a,0]*f[...,iq,:,:]
 out[...,1,:]+=out[...,0,:];out[...,0,:]=0;return out

def point_metric_tensor(k):
 # k represents a symmetric metric VELOCITY; offdiagonal k values are actual hdot_ij.
 out=np.zeros(k.shape[:-1]+(3,3));out[...,0,0]=k[...,0];out[...,1,1]=k[...,1];out[...,2,2]=k[...,2]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):out[...,i,j]=out[...,j,i]=k[...,a]
 return out

def tensor_velocity_coordinates(hdot):
 return np.stack((hdot[...,0,0],hdot[...,1,1],hdot[...,2,2],hdot[...,0,1],hdot[...,0,2],hdot[...,1,2]),axis=-1)

def tensor_momentum_coordinates(pi):
 return np.stack((pi[...,0,0],pi[...,1,1],pi[...,2,2],2*pi[...,0,1],2*pi[...,0,2],2*pi[...,1,2]),axis=-1)

def new_metric_momentum_envelopes(s,c,t,ce):
 ve=t['operation'];hi=abs(s['hi']);U=abs(s['U']);z=abs(s['z']);w=s['w'];om=s['omega']
 ePiU=ALPHA*np.einsum('pac,pcb->pab',hi,ve['F'],optimize=True)
 eFu=np.einsum('pac,pcd,pdb->pab',hi,ve['F'],hi,optimize=True)
 ePi=w[:,None,None,None]*(np.einsum('pa,jpb->jpab',U,np.einsum('pab,jpb->jpa',hi,ve['V'],optimize=True),optimize=True)/om[:,None,None,None]**2+ELL**2*np.einsum('pac,jpcd,pdb->jpab',hi,ve['D'],hi,optimize=True))
 sym=(ePi+ePi.swapaxes(2,3))/2;Klo=np.einsum('jpab,jpl->plab',sym,z,optimize=True);Kup=np.einsum('plm,pmab->plab',hi,Klo,optimize=True)
 ed=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)+Kup)/2
 emx=ALPHA*(eFu[:,:,:,None]*U[:,None,None,:]+eFu[:,:,None,:]*U[:,None,:,None])/2;ect=(ed+emx)[:,0]
 pu=np.einsum('pa,pai->pi',ePiU[:,0],ce['JU'],optimize=True)+np.einsum('jp,jpi->pi',ePi[:,:,0,0],ce['JzU'],optimize=True)
 pz=ePi[:,:,0,1:]+ePi[:,:,0,0,None]*ce['Jzz'][None]
 ep=c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)
 eUh=RAW['assembling_envelope_U_metric_chain'];ezh=RAW['assembling_envelope_zt_metric_chain'];eEmbed=RAW['assembling_envelope_metric_embedding']
 eh=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',ect,eEmbed,optimize=True)+np.einsum('pa,pka->pk',ePiU[:,0],eUh,optimize=True)+np.einsum('jp,jpk->pk',ePi[:,:,0,0],ezh,optimize=True))
 raw=dict(PiU=ePiU,Pi=ePi,connection=ect,native_momentum=ep,metric_momentum=eh)
 for n,a in raw.items():RAW['new_metric_'+n+'_envelope']=a.copy();assert np.all(np.isfinite(a)) and np.all(a>=0),n
 return ep,eh,raw

def six_metric_gram(s,c,tt):
 # Independent kinetic bilinear, all32 modes, six new metric columns only.
 hi=s['hi'];F=np.stack([t['delta_F'] for t in tt]);V=np.stack([t['delta_V'] for t in tt]);D=np.stack([t['delta_D'] for t in tt])
 Fu=np.einsum('pac,Apcd,pdb->Apab',hi,F,hi,optimize=True);Vu=np.einsum('pab,Ajpb->Ajpa',hi,V,optimize=True);Du=np.einsum('pac,Ajpcd,pdb->Ajpab',hi,D,hi,optimize=True)
 mx=-ALPHA*np.einsum('Apab,Bpab->pAB',Fu,F,optimize=True)/2
 vv=np.einsum('Ajpa,Bjpa->jpAB',Vu,V,optimize=True)/s['omega'][:,None,None,None]**2
 dd=-ELL**2*np.einsum('Ajpab,Bjpab->jpAB',Du,D,optimize=True)
 G=c['dens'][:,None,None]*(mx+np.einsum('j,jpAB->pAB',s['w'],vv+dd,optimize=True))
 eF=np.stack([t['operation']['F'] for t in tt]);eV=np.stack([t['operation']['V'] for t in tt]);eD=np.stack([t['operation']['D'] for t in tt]);eh=abs(hi)
 eFu=np.einsum('pac,Apcd,pdb->Apab',eh,eF,eh,optimize=True);eVu=np.einsum('pab,Ajpb->Ajpa',eh,eV,optimize=True);eDu=np.einsum('pac,Ajpcd,pdb->Ajpab',eh,eD,eh,optimize=True)
 env=c['dens'][:,None,None]*(ALPHA*np.einsum('Apab,Bpab->pAB',eFu,eF,optimize=True)/2+np.einsum('j,jpAB->pAB',s['w'],np.einsum('Ajpa,Bjpa->jpAB',eVu,eV,optimize=True)/s['omega'][:,None,None,None]**2+ELL**2*np.einsum('Ajpab,Bjpab->jpAB',eDu,eD,optimize=True),optimize=True))
 return G,env

def EH_metric_block(c):
 e=metric_basis();ih=c['ih'];tr=np.einsum('pij,kij->pk',ih,e,optimize=True)
 q=np.einsum('aij,pjk,bkl,pli->pab',e,ih,e,ih,optimize=True);fac=c['sqrt_h']/(4*c['N']*C)
 H=fac[:,None,None]*(q-tr[:,:,None]*tr[:,None,:]);etr=np.einsum('pij,kij->pk',abs(ih),abs(e),optimize=True)
 env=fac[:,None,None]*(np.einsum('aij,pjk,bkl,pli->pab',abs(e),abs(ih),abs(e),abs(ih),optimize=True)+etr[:,:,None]*etr[:,None,:])
 return H,env

def new_six_columns(s,c,ce,iq):
 start=len(CHECKS);tt=[];B=[];T=[];eB=[];eT=[];raw={}
 for a in range(6):
  CONTEXT.update(column=iq,metric_column=a);k=np.eye(6)[a];du,dz,dg,dGa=native_velocity_jet(s,c,np.zeros(99),k)
  for n,v in dict(du=du,dz=dz,metric_jet=dg,Gamma=dGa).items():capture(f'metric_{a}_'+n,v)
  t=kinetic_tangent(s,du,dz,dGa)
  for n,v in t.items():capture(f'metric_{a}_'+n,v)
  ve=velocity_operation_envelopes(s,c,np.zeros(99),k,ce);t['operation']=ve
  for n,v in ve.items():capture(f'metric_{a}_operation_'+n,v)
  py,ph=reduced_momenta(s,c,t['delta_PiU'],t['delta_Pi'],t['delta_Ctime']);capture(f'metric_{a}_B',py);capture(f'metric_{a}_T_native',ph)
  ep,eh,op=new_metric_momentum_envelopes(s,c,t,ce);capture(f'metric_{a}_B_envelope',ep);capture(f'metric_{a}_T_envelope',eh)
  B.append(py);T.append(ph);eB.append(ep);eT.append(eh);tt.append(t)
  # Completed six-column primitives and positive bounds are retained for saved-only Gram audit.
  for n in ('delta_F','delta_V','delta_D','delta_PiU','delta_Pi','delta_Ctime'):raw[f'metric_{a}_'+n]=t[n]
  for n in ('F','V','D'):raw[f'metric_{a}_operation_'+n]=ve[n]
 b=np.stack(B,axis=-1);t=np.stack(T,axis=-1);eb=np.stack(eB,axis=-1);et=np.stack(eT,axis=-1)
 for n,v in dict(B=b,T_native=t,B_envelope=eb,T_native_envelope=et).items():capture(n,v)
 gram,ge=six_metric_gram(s,c,tt);capture('independent_six_metric_Gram',gram);capture('independent_six_metric_Gram_envelope',ge)
 check(f'q{iq}_metric_momentum_independent_Gram',t,gram,et+ge)
 check(f'q{iq}_native_metric_bilinear_symmetry',t,t.swapaxes(1,2),et+et.swapaxes(1,2))
 # One independently prescribed reduced velocity direction, not an old105 reconstruction.
 y=np.broadcast_to(np.arange(1,100,dtype=float)/101,(len(s['U']),99));ny=native_velocity_jet(s,c,y,np.zeros(6));nt=kinetic_tangent(s,ny[0],ny[1],ny[3]);nv=velocity_operation_envelopes(s,c,y,np.zeros(6),ce);nt['operation']=nv
 _,nyh=reduced_momenta(s,c,nt['delta_PiU'],nt['delta_Pi'],nt['delta_Ctime']);_,nye,_=new_metric_momentum_envelopes(s,c,nt,ce)
 by=np.einsum('pia,pi->pa',b,y,optimize=True);bye=np.einsum('pia,pi->pa',eb,abs(y),optimize=True)
 capture('independent_mixed_native_direction',y);capture('independent_mixed_native_metric_momentum',nyh)
 check(f'q{iq}_native_metric_mixed_reciprocity',by,nyh,bye+nye)
 eh,ee=EH_metric_block(c);capture('EH_six_block',eh);capture('EH_six_block_envelope',ee)
 total=t+eh;env=et+ee;capture('total_six_block',total);capture('total_six_block_envelope',env)
 raw.update(B=b,T_native=t,T_EH=eh,T_total=total,B_envelope=eb,T_native_envelope=et,T_EH_envelope=ee,T_total_envelope=env,independent_six_metric_Gram=gram,independent_six_metric_Gram_envelope=ge,independent_mixed_native_direction=y,independent_mixed_native_metric_momentum=nyh)
 return raw,start

def spatial_Lie_beta_from_saved(Ga,g,hi,beta):
 # Exact saved metric compatibility, only spatial first jets; no geometry/operator reconstruction.
 dg=np.einsum('plam,pln->pamn',Ga,g,optimize=True);dg+=dg.swapaxes(2,3)
 eg=np.einsum('plam,pln->pamn',abs(Ga),abs(g),optimize=True);eg+=eg.swapaxes(2,3)
 dhi=-np.einsum('pac,pkcd,pdb->pkab',hi,dg,hi,optimize=True);ehi=np.einsum('pac,pkcd,pdb->pkab',abs(hi),eg,abs(hi),optimize=True)
 N=1/np.sqrt(-hi[:,0,0]);Na=N[:,None]**3*dhi[:,:,0,0]/2;eNa=N[:,None]**3*ehi[:,:,0,0]/2
 db=2*N[:,None,None]*Na[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 edb=2*N[:,None,None]*eNa[:,:,None]*abs(hi[:,None,0,1:])+N[:,None,None]**2*ehi[:,:,0,1:]
 h=g[:,1:,1:];sp=np.einsum('pk,pkij->pij',beta,dg[:,1:,1:,1:],optimize=True)
 sp+=np.einsum('pkj,pik->pij',h,db[:,1:],optimize=True)+np.einsum('pik,pjk->pij',h,db[:,1:],optimize=True)
 ep=np.einsum('pk,pkij->pij',abs(beta),eg[:,1:,1:,1:],optimize=True)+np.einsum('pkj,pik->pij',abs(h),edb[:,1:],optimize=True)+np.einsum('pik,pjk->pij',abs(h),edb[:,1:],optimize=True)
 return sp,ep,dict(saved_metric_partial=dg,saved_metric_partial_envelope=eg,saved_shift_partial=db,saved_shift_partial_envelope=edb)

def metric_basis_controls(geo):
 start=len(CHECKS);r,z=geo['r'],geo['z'];xx=np.arange(6*87*45,dtype=float).reshape(6,87,45)/(6*87*45);xx*=metric_mask();field=np.sin(np.arange(15136*6,dtype=float).reshape(15136,6)/113)
 ev=evaluate_metric(xx,geo);sc=scatter_metric(field,geo);ind=scatter_metric_independent(field,geo);wq=(geo['dv']/geo['R']).reshape(15136)
 check('new_metric_true_lift_adjoint',np.array(dot(xx,sc)),np.array(np.einsum('p,pi,pi->',wq,ev,field)),np.array(dot(abs(xx),scatter_metric(abs(field),geo))+np.einsum('p,pi,pi->',wq,abs(ev),abs(field))))
 check('new_metric_independent_incidence_scatter',sc,ind,scatter_metric(abs(field),geo)+abs(ind))
 counts=np.array([np.count_nonzero(metric_mask()),86*45]);check('metric_and_CMC_scalar_dimension',counts,np.array([23048,3870]),abs(counts))
 unit=np.zeros((6,6,87,45));unit[np.arange(6),np.arange(6)]=1;vv=evaluate_metric(unit,geo);vr=evaluate_metric(unit,geo,1);vz=evaluate_metric(unit,geo,2);R=geo['R'].reshape(15136)
 expected=metric_value_matrix(R).transpose(2,0,1);er=metric_R_matrix(R).transpose(2,0,1);expected[[3,4]]=0;er[[3,4]]=0
 # Even coefficient columns a,b,c,f are constants; odd d/e use an explicit Z polynomial below.
 actual=vv[[0,1,2,5]];expect=expected[[0,1,2,5]]
 check('Cartesian_regular_even_metric_value_R_Z',np.stack((actual,vr[[0,1,2,5]],vz[[0,1,2,5]])),np.stack((expect,er[[0,1,2,5]],np.zeros_like(expect))),np.stack((abs(actual)+abs(expect),abs(vr[[0,1,2,5]])+abs(er[[0,1,2,5]]),abs(vz[[0,1,2,5]])+abs(expect))))
 zz=np.broadcast_to(z[None,:,None],(87,45,1))[...,0];odd=np.zeros((2,6,87,45));odd[0,3]=zz;odd[1,4]=zz;ov=evaluate_metric(odd,geo);oR=evaluate_metric(odd,geo,1);oZ=evaluate_metric(odd,geo,2)
 # Z at genuine quadrature from its hats, independent of column source data.
 Zq=np.zeros((4,86,44))
 for iq in range(4):
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):Zq[iq]+=geo['hats'][iq,a,0]*np.broadcast_to(z[j:44+j],(86,44))
 Zq=Zq.reshape(15136);op=np.zeros_like(ov);orp=np.zeros_like(ov);ozp=np.zeros_like(ov);op[0,:,3]=R*Zq;op[1,:,5]=R**2*Zq;orp[0,:,3]=Zq;orp[1,:,5]=2*R*Zq;ozp[0,:,3]=R;ozp[1,:,5]=R**2
 check('Cartesian_regular_odd_metric_value_R_Z',np.stack((ov,oR,oZ)),np.stack((op,orp,ozp)),np.stack((abs(ov)+abs(op),abs(oR)+abs(orp),abs(oZ)+abs(ozp))))
 RAW.update(manufactured_metric_nodal=xx,manufactured_metric_qfield=field,manufactured_metric_evaluated=ev,manufactured_metric_scatter=sc,manufactured_metric_incidence=ind,metric_independent_mask=metric_mask(),scalar_independent_mask=np.broadcast_to(np.arange(87)[:,None]>0,(87,45)).copy())
 return start
# Private definitions-only weak sixmetric/CMC admission. Runtime caller supplies json/path/sha/read_pair/resolve_record.
# No NumPy or scientific helper is evaluated by the author. Sources/outputs remain immutable.
WEAK_METRIC_PARENT="CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001"
WEAK_METRIC_WHOLE="CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002"
WEAK_METRIC_Q1="CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001"
WEAK_METRIC_PINS={'author_fragment_weak_metric_cmc_admission_v001.txt': 'f014280bd217b41cce1d70f5f0607e2bdf2e67c1ca795ddae8e4f61445ee269c', 'cross_u_whole_slice_cauchy_data_v002.py': '6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002.md': '0b9529c22d9a007e96e6088387dee5b578d9620914e6933f45d9fd28e80fdb91', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RESULT.json': 'af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json': '88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9', 'cross_u_whole_slice_q1_adm_residual_v001.py': 'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001.md': 'e5c7762d97fc6f2cd759cab4f303aa3a7463ab33e45001161d25bdf80c1ec440', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RESULT.json': '6c323ea0b01169c37c6c6c9960d7469ed57386148ff6022cc3d2bbc6da0b493b', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RECEIPT.json': '2919b4ab5715a7cff10a73836b6db65018520b234f65d1fb00f40c4581854f13', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'cross_u_weak_nodal_native_legendre_v001.py': 'e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001.md': '2c9da869068cf3d2ae9269395b111ec1d0e71f26e0ffef6ff0afb50e40995a0e', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json': 'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RECEIPT.json': '00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae', 'READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json': 'af16bda38df395882c54ca2b57bd7d9ed36cc3aae39b437687bc35930423d56d'}

def weak_metric_admission():
 pins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in pins or pins[n]==h);pins[n]=h
 for n,h in WEAK_METRIC_PINS.items():add(n,h)
 parents={}
 specs=((WEAK_METRIC_PARENT,28469,'CONDITIONAL_WEAK_NATIVE_LEGENDRE_ARITHMETIC_PASS',21,10),(WEAK_METRIC_WHOLE,24903,'CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS',92,22),(WEAK_METRIC_Q1,26129,'CONDITIONAL_WHOLE_Q1_ADM_RESIDUAL_ARITHMETIC_PASS',77,23))
 for stem,pid,status,count,npair in specs:
  result=json.loads(path(stem+'_RESULT.json').read_text());receipt=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert receipt['status']=='CLOSED' and receipt['closed'] and receipt['owner']==result['owner'] and receipt['owner']['owner']=='root' and receipt['owner']['pid']==pid
  assert result['status']==status and receipt['result_sha256']==WEAK_METRIC_PINS[stem+'_RESULT.json']
  assert len(result['controls'])==count and all(c['passed'] for c in result['controls']) and len(result['checkpoints'])==npair and all(v is False for v in result['qualification'].values())
  for key in ('input_sha256','output_sha256'):
   for n,h in receipt[key].items():add(n,h)
  assert {p.name for p in path(stem+'_RESULT.json').parent.glob(stem+'_*.npz')}=={r['file'] for r in result['checkpoints']}
  assert {p.name for p in path(stem+'_RESULT.json').parent.glob(stem+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in result['checkpoints']}
  for rec in result['checkpoints']:
   assert receipt['output_sha256'][rec['file']]==rec['sha256'] and receipt['output_sha256'][rec['commit_file']]==rec['commit_sha256']
   assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
   assert rec['metadata']['owner']==receipt['owner'] and all(v is False for v in rec['metadata']['qualification'].values())
  parents[stem]=(result,receipt)
 for n,h in pins.items():assert sha(path(n))==h,n
 weak_result,weak_rc=parents[WEAK_METRIC_PARENT];whole,whole_rc=parents[WEAK_METRIC_WHOLE];q1,q1_rc=parents[WEAK_METRIC_Q1]
 assert weak_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_weak_nodal_native_legendre_v001.py']
 assert whole_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_whole_slice_cauchy_data_v002.py'] and q1_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_whole_slice_q1_adm_residual_v001.py']
 assert [c['sigma'] for c in whole['cases']]==[.1,1.,10.,100.] and [c['sigma'] for c in q1['cases']]==[.1,1.,10.,100.]
 assert len(weak_result['cases'])==1 and weak_result['cases'][0]['sigma']==1. and weak_result['cases'][0]['status']=='CONDITIONAL_WEAK_NATIVE_LEGENDRE_PASS'
 audit=json.loads(path('READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json').read_text())
 assert audit['status']=='SAVED_PACKET_AUDIT_PASS' and audit['pair_count']==10 and audit['control_count']==21 and audit['terminal']['owner_pid']==28469
 for key,name in (('source_sha256','cross_u_weak_nodal_native_legendre_v001.py'),('result_sha256',WEAK_METRIC_PARENT+'_RESULT.json'),('receipt_sha256',WEAK_METRIC_PARENT+'_RECEIPT.json')):assert audit['terminal'][key]==WEAK_METRIC_PINS[name]
 def one(kind):
  rows=[r for r in weak_result['checkpoints'] if r['metadata']['kind']==kind];assert len(rows)==1;return rows[0]
 weak=dict(result=weak_result,receipt=weak_rc,case=weak_result['cases'][0],input=one('unchanged_grid_spectrum_and_closed_parent_references'),geometry=one('genuine_affine_native_temporal_basis'),coefficient=one('complete_fixed_metric_native99_mass_coefficients'),preparation=one('preconditioner_only_positive_node_block'),saved_audit_sha256=WEAK_METRIC_PINS['READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json'])
 wc=next(c for c in whole['cases'] if c['sigma']==1.);qc=next(c for c in q1['cases'] if c['sigma']==1.)
 whole_sigma1=dict(wc,columns=[resolve_record(r) for r in wc['columns']],input=whole['checkpoints'][0],geometry=whole['checkpoints'][1])
 q1_sigma1=dict(qc,columns=[resolve_record(r) for r in qc['columns']],input=q1['checkpoints'][0])
 fixed=whole_sigma1['input']['metadata']['fixed'];cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert fixed['eps']==cp['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 assert whole_sigma1['input']['metadata']['owned_EPS5_background']==q1_sigma1['input']['metadata']['owned_EPS5_background']==weak['input']['metadata']['owned_background']==cp['background']
 assert q1_sigma1['input']['metadata']['fixed']==weak['input']['metadata']['fixed']==fixed
 def schema(rec,n,shape,dtype='float64'):assert rec['metadata']['schema'][n]==dict(shape=shape,dtype=dtype,finite=True),n
 for n,shape in dict(r_kpc=[87],z_kpc=[45],xi=[32],weights=[32]).items():schema(weak['input'],n,shape)
 for n,shape in dict(geometry_R=[4,3784],geometry_dv=[4,3784],geometry_hats=[4,4,3,86,44]).items():schema(weak['geometry'],n,shape)
 for n in ('geometry_cell_i','geometry_cell_j'):schema(weak['geometry'],n,[3784],'int64')
 schema(weak['geometry'],'native_independent_mask',[3,87,45],'bool')
 for n,shape in dict(input_g=[15136,4,4],input_hi=[15136,4,4],input_U=[15136,4],input_z=[32,15136,4],mixing_L=[32,15136,3,3],modal_D=[32,15136,3,3],Maxwell_M0=[15136,3,3],operation_eL=[32,15136,3,3],operation_eD=[32,15136,3,3],operation_eM0=[15136,3,3],authoritative_point_velocity=[33,15136,3],authoritative_point_native_density=[33,15136,3],actual_owned_point_native_density=[33,15136,3],implicit_fixed_time_baseline=[33,15136,3],saved_affine_momentum_gap=[33,15136,3]).items():schema(weak['coefficient'],n,shape)
 for n,shape in dict(preconditioner_D=[32,3915,3,3],preconditioner_B=[32,3915,3,3],preconditioner_Maxwell=[3915,3,3],preconditioner_basis_scale=[3915,3],kinetic_congruence_scale=[33,3,87,45]).items():schema(weak['preparation'],n,shape)
 assert len(whole_sigma1['columns'])==len(q1_sigma1['columns'])==4
 for iq,(wr,qr) in enumerate(zip(whole_sigma1['columns'],q1_sigma1['columns'])):
  wm,qm=wr['metadata'],qr['metadata'];assert wm['column']==qm['column']==iq and wm['sigma']==qm['sigma']==1. and wm['points']==qm['points']==3784
  assert qm['whole_parent_file']==wr['file'] and qm['whole_parent_sha256']==wr['sha256']
  assert weak['input']['metadata']['whole_columns'][iq]==dict(file=wr['file'],sha256=wr['sha256']) and weak['input']['metadata']['owned_columns'][iq]==dict(file=qr['file'],sha256=qr['sha256'])
  for n,shape in dict(Ga=[3784,4,4,4],g=[3784,4,4],hi=[3784,4,4],U=[3784,4],z=[32,3784,4],metric_total_canonical_density=[3784,6],native_canonical_density=[3784,99],R=[3784],Z=[3784],reference_volume=[3784]).items():schema(wr,n,shape)
  for n in ('cell_i','cell_j'):schema(wr,n,[3784],'int64')
  selected=(1972,1972,1938,1938)[iq]
  schema(wr,'compact_reused_whole_indices',[selected],'int64');schema(wr,'new_whole_indices',[3784-selected],'int64')
  for n,shape in dict(up=[3784,3],sqrt_h=[3784],K=[3784,3,3],Ktrace=[3784],Uh=[3784,6,4],zh=[32,3784,6],embed=[3784,6,4,4],h=[3784,3,3],N=[3784],ih=[3784,3,3],beta=[3784,3],u=[3784,3],gamma=[3784],JU=[3784,4,3],JzU=[32,3784,3],Jzz=[3784,3],dens=[3784],old_velocity=[3784,99]).items():schema(qr,'owned_chart_'+n,shape)
  for n,shape in dict(owned_metric_native_p=[3784,6],owned_EH_p=[3784,3,3],owned_metric_total_p=[3784,3,3],owned_native_canonical_density=[3784,99],new_native_p=[3784-selected,99],new_owned_hdot_tensor=[3784-selected,3,3]).items():schema(qr,n,shape)
  schema(qr,f'copied_q{iq}_native_p',[selected,99]);schema(qr,f'copied_q{iq}_owned_hdot_tensor',[selected,3,3])
 return pins,weak,whole_sigma1,q1_sigma1,fixed,cp

def read_weak_metric_basis(weak):
 return read_pair(weak['geometry'],('geometry_R','geometry_dv','geometry_hats','geometry_cell_i','geometry_cell_j','native_independent_mask','r_kpc','z_kpc'))

def read_weak_metric_coefficients(weak):
 return read_pair(weak['coefficient'],('input_g','input_hi','input_U','input_z','mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0','authoritative_point_velocity','authoritative_point_native_density','actual_owned_point_native_density','implicit_fixed_time_baseline','saved_affine_momentum_gap'))

def read_weak_metric_preparation(weak):
 return read_pair(weak['preparation'],('preconditioner_D','preconditioner_B','preconditioner_Maxwell','preconditioner_basis_scale','kinetic_congruence_scale'))

def read_weak_metric_native_column(rec):
 return read_pair(rec,('Ga','metric_total_canonical_density','R','Z','reference_volume','cell_i','cell_j','compact_reused_whole_indices','new_whole_indices'))

def read_weak_metric_owned_column(rec):
 iq=rec['metadata']['column'];assert iq in (0,1,2,3)
 names=tuple('owned_chart_'+k for k in ('up','sqrt_h','K','Ktrace','Uh','zh','embed','h','N','ih','beta','u','gamma','JU','JzU','Jzz','dens','old_velocity'))+('owned_metric_native_p','owned_EH_p','owned_metric_total_p','owned_native_canonical_density',f'copied_q{iq}_native_p','new_native_p',f'copied_q{iq}_owned_hdot_tensor','new_owned_hdot_tensor')
 return read_pair(rec,names)

def load_weak_map(weak):
 bb=read_weak_metric_basis(weak);g=dict(R=bb['geometry_R'],dv=bb['geometry_dv'],hats=bb['geometry_hats'],cell_i=bb['geometry_cell_i'],cell_j=bb['geometry_cell_j'],r=bb['r_kpc'],z=bb['z_kpc'])
 assert np.array_equal(bb['native_independent_mask'],native_mask()) and np.all(g['R']>0) and np.all(g['dv']>0)
 bc=read_weak_metric_coefficients(weak)
 extra=read_pair(weak['coefficient'],('operation_eup','operation_eJU','operation_eJzU','operation_eJzz','original_weak_rhs','original_weak_rhs_envelope','original_weak_momentum_target'))
 bc.update(extra);pc=read_weak_metric_preparation(weak)
 b=dict(L=bc['mixing_L'],D=bc['modal_D'],M0=bc['Maxwell_M0'],eL=bc['operation_eL'],eD=bc['operation_eD'],eM0=bc['operation_eM0'])
 pre=dict(D=pc['preconditioner_D'],B=pc['preconditioner_B'],M0=pc['preconditioner_Maxwell'],scale=pc['preconditioner_basis_scale'],normscale=pc['kinetic_congruence_scale'],mask=native_mask())
 for label,a in dict(native_L=b['L'],native_D=b['D'],native_Maxwell=b['M0'],native_normscale=pre['normscale']).items():finite_real('reused_'+label,a)
 assert np.all(pre['scale']>0) and np.all(pre['normscale']>0)
 return g,b,pre,bc

def assemble_column(iq,wr,qr,bc,w,omega,Hbar):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(column=iq,stage='new_six_metric_columns');start=len(CHECKS)
 old=read_weak_metric_native_column(wr);own=read_weak_metric_owned_column(qr);sl=slice(iq*3784,(iq+1)*3784)
 for n in ('R','reference_volume'):assert np.array_equal(old[n],GEO['R' if n=='R' else 'dv'][iq])
 assert np.array_equal(old['cell_i'],GEO['cell_i']) and np.array_equal(old['cell_j'],GEO['cell_j'])
 ix,ox=old['compact_reused_whole_indices'],old['new_whole_indices'];assert np.array_equal(np.sort(np.r_[ix,ox]),np.arange(3784))
 c={k.removeprefix('owned_chart_'):v for k,v in own.items() if k.startswith('owned_chart_')}
 s=dict(g=bc['input_g'][sl],hi=bc['input_hi'][sl],U=bc['input_U'][sl],z=bc['input_z'][:,sl],w=w,omega=omega)
 s['uc']=lower(s['g'],s['U']);s['P']=np.eye(4)[None]+np.einsum('pa,pb->pab',s['uc'],s['U']);s['Z']=np.einsum('j,jpa->pa',w,s['z'])
 ce=dict(up=bc['operation_eup'][sl],JU=bc['operation_eJU'][sl],JzU=bc['operation_eJzU'][:,sl],Jzz=bc['operation_eJzz'][sl])
 pstar=np.empty((3784,99));pstar[ix]=own[f'copied_q{iq}_native_p'];pstar[ox]=own['new_native_p'];kstar=np.empty((3784,3,3));kstar[ix]=own[f'copied_q{iq}_owned_hdot_tensor'];kstar[ox]=own['new_owned_hdot_tensor'];ks=tensor_velocity_coordinates(kstar)
 ps=bc['actual_owned_point_native_density'][:,sl].transpose(1,0,2).reshape(3784,99);target=bc['authoritative_point_native_density'][:,sl].transpose(1,0,2).reshape(3784,99)
 check(f'q{iq}_actual_pstar_and_target_preserved',np.stack((pstar,own['owned_native_canonical_density'])),np.stack((ps,target)),np.stack((abs(pstar)+abs(ps),abs(own['owned_native_canonical_density'])+abs(target))))
 ehpi=tensor_momentum_coordinates(own['owned_EH_p']);pistar=own['owned_metric_native_p']+ehpi;tot=tensor_momentum_coordinates(own['owned_metric_total_p'])
 check(f'q{iq}_full_metric_momentum_offdiagonal_pairing',pistar,tot,abs(own['owned_metric_native_p'])+abs(ehpi)+abs(tot))
 vs=bc['authoritative_point_velocity'][:,sl].transpose(1,0,2).reshape(3784,99);assert np.array_equal(vs,c['old_velocity'])
 data,_=new_six_columns(s,c,ce,iq);data.update(current_native_pstar=pstar,old_native_target=target,current_metric_pistar=pistar,old_metric_momentum_target=old['metric_total_canonical_density'],current_metric_time_jet=ks,current_metric_time_tensor=kstar,current_native_velocity_star=vs,current_ih=c['ih'],current_N=c['N'],current_sqrt_h=c['sqrt_h'])
 lie,elie,derived=spatial_Lie_beta_from_saved(old['Ga'],s['g'],s['hi'],c['beta']);kp=(kstar-lie)/(2*c['N'][:,None,None]);kpenv=(abs(kstar)+elie)/(2*c['N'][:,None,None]);kt=np.einsum('pij,pij->p',c['ih'],kp,optimize=True);kte=np.einsum('pij,pij->p',abs(c['ih']),kpenv,optimize=True)
 check(f'q{iq}_independent_saved_CMC_metric_time_compatibility',kp,c['K'],kpenv+abs(c['K']))
 data.update(saved_Lie_beta_h=lie,saved_Lie_beta_h_envelope=elie,independent_K_tensor=kp,independent_K_envelope=kpenv,current_Kstar=c['Ktrace'],independent_Ktrace=kt,independent_Ktrace_envelope=kte,CMC_star_trace_gap=c['Ktrace']-3*Hbar)
 # Full affine offsets at the authentic point-star; no new physical metric target chosen.
 bk=np.einsum('pia,pa->pi',data['B'],ks,optimize=True);be=np.einsum('pia,pa->pi',data['B_envelope'],abs(ks),optimize=True)
 cm=pistar-np.einsum('pia,pi->pa',data['B'],vs,optimize=True)-np.einsum('pab,pb->pa',data['T_total'],ks,optimize=True)
 cme=abs(pistar)+np.einsum('pia,pi->pa',data['B_envelope'],abs(vs),optimize=True)+np.einsum('pab,pb->pa',data['T_total_envelope'],abs(ks),optimize=True)
 data.update(native_B_kstar=bk,native_B_kstar_envelope=be,metric_affine_offset=cm,metric_affine_offset_envelope=cme,saved_affine_gap=pstar-target)
 data.update({k:a for k,a in derived.items()});data.update({k:a for k,a in RAW.items() if k.startswith('control_')})
 rec=checkpoint('COLUMN',data,dict(kind='six_new_metric_time_columns_and_affine_CMC_operands',column=iq,sigma=SIGMA,points=3784,controls=CHECKS[start:],whole_parent_file=wr['file'],whole_parent_sha256=wr['sha256'],owned_parent_file=qr['file'],owned_parent_sha256=qr['sha256'],local_signed_metric_block='native+EH; no local elimination substituted for global weak map'))
 # Keep only the small algebraic blocks after their full raw primitives are sealed.
 keep={k:data[k] for k in ('B','B_envelope','T_total','T_total_envelope','native_B_kstar','native_B_kstar_envelope','metric_affine_offset','metric_affine_offset_envelope','current_metric_pistar','old_metric_momentum_target','current_metric_time_jet','current_ih','current_N','current_sqrt_h','current_Kstar','independent_Ktrace','independent_Ktrace_envelope','saved_Lie_beta_h','saved_Lie_beta_h_envelope')}
 return keep,rec

def trace_CMC_actions(k,ih,N,mu,g):
 tensor=point_metric_tensor(k);tr=np.einsum('pij,...pij->...p',ih,tensor,optimize=True)/(2*N)
 return scalar_scatter(mu*tr,g)

def sampled_metric_response(data,g,b,pre):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};start=len(CHECKS);R=g['R'].reshape(15136);wq=(g['dv']/g['R']).reshape(15136)
 hats=np.zeros((6,6,87,45));hats[np.arange(6),np.arange(6),43,22]=1;kv=evaluate_metric(hats,g);capture('six_metric_unit_hats',hats);capture('six_metric_unit_hat_qvalues',kv)
 B=np.concatenate([d['B'] for d in data]);eB=np.concatenate([d['B_envelope'] for d in data]);T=np.concatenate([d['T_total'] for d in data]);eT=np.concatenate([d['T_total_envelope'] for d in data])
 point=np.einsum('pia,Apa->Api',B,kv,optimize=True).reshape(6,15136,33,3).transpose(0,2,1,3);penv=np.einsum('pia,Apa->Api',eB,abs(kv),optimize=True).reshape(6,15136,33,3).transpose(0,2,1,3)
 rhs=scatter_velocity(point,g);capture('six_new_native_RHS',rhs);rhsenv=scatter_velocity(penv,g);capture('six_new_native_RHS_envelope',rhsenv);ind=scatter_velocity_independent(point,g);capture('six_new_native_RHS_independent',ind)
 check('six_new_metric_RHS_independent_weak_incidence',rhs,ind,rhsenv+abs(ind))
 solutions=[];actions=[];residuals=[];recs=[]
 checkpoint('RIGHT_HAND_SIDES',dict(six_metric_unit_hats=hats,six_metric_unit_hat_qvalues=kv,six_new_native_RHS=rhs,six_new_native_RHS_envelope=rhsenv,**{k:a for k,a in RAW.items() if k.startswith('control_')}),dict(kind='six_genuinely_new_metric_native_mixed_weak_RHS',controls=CHECKS[start:]))
 for a in range(6):
  RAW={};AVAILABLE={};CONTEXT.update(stage='six_new_metric_native_CG',probe=a);cs=len(CHECKS);capture('new_metric_native_rhs',rhs[a]);capture('new_metric_native_rhs_envelope',rhsenv[a]);sol,act,res,hist=solve_native(rhs[a],b,g,pre)
  linear_gate(f'new_metric_{a}_original_and_congruence_CG',res,rhs[a],pre['normscale']);ev=evaluate_velocity(sol,g);capture('new_metric_native_qvelocity',ev);capture('new_metric_native_nodal_solution',sol)
  capture('new_metric_native_original_action',act);capture('new_metric_native_original_residual',res);capture('new_metric_native_original_history',hist)
  back=scatter_metric(np.einsum('pia,pi->pa',B,ev.transpose(1,0,2).reshape(15136,99),optimize=True),g);capture('global_BT_native_solution',back)
  rec=checkpoint('SOLVE',dict(AVAILABLE,**{k:v for k,v in RAW.items() if k.startswith('control_') or k.startswith(f'new_metric_{a}_original')}),dict(kind='new_metric_column_original_weak_native_solve',probe=a,node=[43,22],sigma=SIGMA,iterations=int(hist[-1,0]),controls=CHECKS[cs:],tolerance=LINEAR_TOL,physical_velocity_applied=False));recs.append(rec);solutions.append(sol);actions.append(act);residuals.append(res)
 RAW={};AVAILABLE={};cs=len(CHECKS)
 yy=np.stack(solutions);aa=np.stack(actions);rr=np.stack(residuals);capture('six_new_nodal_native_solutions',yy);capture('six_new_native_original_actions',aa);capture('six_new_native_original_residuals',rr)
 direct=np.einsum('p,Apa,pab,Bpb->AB',wq,kv,T,kv,optimize=True);capture('sampled_full_T',direct);de=np.einsum('p,Apa,pab,Bpb->AB',wq,abs(kv),eT,abs(kv),optimize=True);capture('sampled_full_T_envelope',de)
 elimination=np.einsum('Agcrz,Bgcrz->AB',rhs,yy,optimize=True);capture('sampled_global_elimination',elimination);ee=np.einsum('Agcrz,Bgcrz->AB',rhsenv,abs(yy),optimize=True);capture('sampled_global_elimination_envelope',ee);S=direct-elimination;capture('sampled_signed_global_Schur',S)
 check('sampled_full_metric_T_bilinear_symmetry',direct,direct.T,de+de.T)
 expect=direct-direct.T-(np.einsum('Agcrz,Bgcrz->AB',rr,yy,optimize=True)-np.einsum('Bgcrz,Agcrz->AB',rr,yy,optimize=True))
 check('sampled_signed_global_Schur_residual_antisymmetry',S-S.T,expect,de+de.T+ee+ee.T+np.einsum('Agcrz,Bgcrz->AB',abs(rr),abs(yy),optimize=True)+np.einsum('Bgcrz,Agcrz->AB',abs(rr),abs(yy),optimize=True))
 ih=np.concatenate([d['current_ih'] for d in data]);mu=np.concatenate([d['current_sqrt_h'] for d in data]);kt=point_metric_tensor(kv)
 Q=np.einsum('p,p,Apij,pjk,Bpkl,pli->AB',wq,mu,kt,ih,kt,ih,optimize=True);capture('sampled_positive_metric_Gram',Q);eQ=np.einsum('p,p,Apij,pjk,Bpkl,pli->AB',wq,mu,abs(kt),abs(ih),abs(kt),abs(ih),optimize=True)
 capture('sampled_positive_metric_Gram',Q);capture('sampled_metric_Gram_envelope',eQ);chol=np.linalg.cholesky(Q);capture('sampled_positive_metric_Gram_Cholesky',chol);W=np.linalg.solve(chol.T,np.eye(6));capture('sampled_metric_congruence',W);cert=W.T@Q@W
 check('sampled_proper_metric_unit_certificate',cert,np.eye(6),abs(W).T@eQ@abs(W)+np.eye(6))
 normalized=W.T@S@W;capture('sampled_signed_global_Schur',S);capture('sampled_metric_normalized_global_Schur',normalized);eigen=np.linalg.eigvalsh((normalized+normalized.T)/2);capture('sampled_signed_global_Schur_eigenvalues',eigen);assert np.all(np.isfinite(eigen))
 raw=dict(six_metric_unit_hats=hats,six_metric_unit_hat_qvalues=kv,six_new_native_RHS=rhs,six_new_native_RHS_envelope=rhsenv,six_new_nodal_native_solutions=yy,six_new_native_original_actions=aa,six_new_native_original_residuals=rr,sampled_full_T=direct,sampled_full_T_envelope=de,sampled_global_elimination=elimination,sampled_global_elimination_envelope=ee,sampled_signed_global_Schur=S,sampled_positive_metric_Gram=Q,sampled_metric_Gram_envelope=eQ,sampled_metric_congruence=W,sampled_metric_normalized_global_Schur=normalized,sampled_signed_global_Schur_eigenvalues=eigen)
 raw.update({k:a for k,a in RAW.items() if k.startswith('control_')});rec=checkpoint('SAMPLED',raw,dict(kind='six_hat_signed_global_metric_Schur_sample',controls=CHECKS[cs:],global_metric_rank_claim=False,global_metric_stability_claim=False,metric_rate_selected=False,pointwise_Schur_substitution=False,congruence='positive proper metric Gram; eigenvalues diagnostic only'))
 return hats,kv,rec,recs

def affine_CMC_vectors(data,bc,g,Hbar,hats,kv):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};start=len(CHECKS);bk=np.concatenate([d['native_B_kstar'] for d in data]);ebk=np.concatenate([d['native_B_kstar_envelope'] for d in data]);field=bk.reshape(15136,33,3).transpose(1,0,2)
 load=scatter_velocity(field,g);capture('full_affine_B_kstar_weak_load',load);loadind=scatter_velocity_independent(field,g);capture('full_affine_B_kstar_independent_load',loadind);le=scatter_velocity(ebk.reshape(15136,33,3).transpose(1,0,2),g);capture('full_affine_B_kstar_weak_envelope',le)
 check('full_affine_metric_to_native_weak_RHS_incidence',load,loadind,le+abs(loadind))
 rn=bc['original_weak_rhs']+load;capture('new_affine_native_weak_RHS',rn);cn=bc['implicit_fixed_time_baseline']-field;capture('native_affine_offset_point',cn)
 cm=np.concatenate([d['metric_affine_offset'] for d in data]);capture('metric_affine_offset_point',cm);cme=np.concatenate([d['metric_affine_offset_envelope'] for d in data]);capture('metric_affine_offset_envelope',cme);cmload=scatter_metric(cm,g);capture('full_metric_affine_weak_load',cmload);cmloadenv=scatter_metric(cme,g);capture('full_metric_affine_weak_load_envelope',cmloadenv)
 oldtarget=scatter_metric(np.concatenate([d['old_metric_momentum_target'] for d in data]),g);capture('old_metric_weak_momentum_target',oldtarget);current=scatter_metric(np.concatenate([d['current_metric_pistar'] for d in data]),g);capture('current_metric_weak_momentum_star',current)
 ih=np.concatenate([d['current_ih'] for d in data]);N=np.concatenate([d['current_N'] for d in data]);mu=np.concatenate([d['current_sqrt_h'] for d in data]);ks=np.concatenate([d['current_metric_time_jet'] for d in data]);K=np.concatenate([d['current_Kstar'] for d in data]);Kind=np.concatenate([d['independent_Ktrace'] for d in data]);eKind=np.concatenate([d['independent_Ktrace_envelope'] for d in data]);lie=np.concatenate([d['saved_Lie_beta_h'] for d in data]);elie=np.concatenate([d['saved_Lie_beta_h_envelope'] for d in data])
 ck=trace_CMC_actions(ks,ih,N,mu,g);capture('CMC_star_metric_trace_action',ck);dstar=scalar_scatter(mu*(3*Hbar-K),g)+ck;capture('CMC_scalar_star_RHS',dstar)
 dliteral=scalar_scatter(mu*(3*Hbar+np.einsum('pij,pij->p',ih,lie,optimize=True)/(2*N)),g);capture('CMC_independent_scalar_star_RHS',dliteral)
 etr=np.einsum('pij,pij->p',abs(ih),abs(point_metric_tensor(ks)),optimize=True)/(2*N)
 env=scalar_scatter(mu*(6*abs(Hbar)+abs(K)+eKind+etr+np.einsum('pij,pij->p',abs(ih),elie,optimize=True)/(2*N)),g)
 check('CMC_star_load_independent_saved_shift_geometry',dstar,dliteral,env)
 Csample=trace_CMC_actions(kv,ih,N,mu,g);capture('CMC_six_hat_trace_columns',Csample);e=metric_basis();local_trace=mu[:,None]*np.einsum('pij,aij->pa',ih,e,optimize=True)/(2*N[:,None]);capture('CMC_local_trace_coefficients',local_trace);pairing=np.stack([dot(h,cmload) for h in hats]);capture('six_hat_metric_affine_pairing',pairing);cgap=scalar_scatter(mu*(K-3*Hbar),g);capture('CMC_star_weak_gap',cgap)
 for n,a in dict(new_affine_native_weak_RHS=rn,new_affine_native_weak_RHS_envelope=bc['original_weak_rhs_envelope']+le,old_fixed_kstar_native_weak_RHS=bc['original_weak_rhs'],native_affine_offset_point=cn,metric_affine_offset_point=cm,metric_affine_offset_envelope=cme,full_metric_affine_weak_load=cmload,full_metric_affine_weak_load_envelope=cmloadenv,old_metric_weak_momentum_target=oldtarget,current_metric_weak_momentum_star=current,six_hat_metric_affine_pairing=pairing,current_metric_time_jet=ks,current_Kstar=K,independent_Ktrace=Kind,CMC_star_point_gap=K-3*Hbar,CMC_star_weak_gap=cgap,CMC_scalar_star_RHS=dstar,CMC_independent_scalar_star_RHS=dliteral,CMC_six_hat_trace_columns=Csample,CMC_local_trace_coefficients=local_trace,current_ih=ih,current_N=N,current_sqrt_h=mu).items():finite_real(n,a)
 AVAILABLE.update({k:a for k,a in RAW.items() if k.startswith('control_')})
 return checkpoint('AFFINE_CMC',AVAILABLE,dict(kind='full_weak_affine_offsets_and_CMC_trace_operator_data',controls=CHECKS[start:],native_affine_baseline_inverse=None,metric_momentum_target_selected=None,metric_rate_selected=None,full_CMC_lapse_force=None,CMC_preservation_force=None,phase_current_evolution=None,ordinary_worldline_evolution=None,temporal_gauge_rates=None,exterior_ports=None,physical_worldtube=None,activity_outside_measured_support=None,scalar_basis_independent=3870,metric_basis_independent=23048))

# Definitions only; never imported or evaluated by the author. Root-only future controls.
# Eight new artificial gates, no old105/native99 fixture, state, clock or parameter replay.
# Requires np, RAW, CHECKS, C, ALPHA, check, metric_value_matrix, metric_R_matrix,
# point_metric_tensor, tensor_momentum_coordinates, symmetric_tensor_from_coordinates,
# EH_metric_block, metric_basis, native_velocity_jet, kinetic_tangent, reduced_momenta.

def metric_fixture_keep(name,value):
 RAW['metric_fixture_'+name]=value.copy();return value

def weak_metric_fixtures():
 start=len(CHECKS)
 # Independent Cartesian polynomial pullback at a nonaxial angle, for two R values.
 R=metric_fixture_keep('R',np.array([2.,3.]));coef=metric_fixture_keep('coefficients',np.array([1/3,-1/5,1/7,-1/11,1/13,2/17]))
 X=np.column_stack((3*R/5,4*R/5,np.zeros(2)));Y=np.column_stack((-4*R/5,3*R/5,np.zeros(2)));ez=np.array([0.,0.,1.])
 cart=coef[0]*np.diag([1.,1.,0.])[None]+coef[1]*np.einsum('pi,pj->pij',X,X)
 cart+=coef[2]*(np.einsum('pi,pj->pij',X,Y)+np.einsum('pi,pj->pij',Y,X))
 cart+=coef[3]*(np.einsum('pi,j->pij',X,ez)+np.einsum('i,pj->pij',ez,X))
 cart+=coef[4]*(np.einsum('pi,j->pij',Y,ez)+np.einsum('i,pj->pij',ez,Y))+coef[5]*np.outer(ez,ez)[None]
 metric_fixture_keep('Cartesian_tensor',cart)
 jac=np.zeros((2,3,3));jac[:,:,0]=np.array([3/5,4/5,0.]);jac[:,:,1]=ez;jac[:,:,2]=Y
 metric_fixture_keep('Cartesian_coordinate_jacobian',jac)
 expected=np.einsum('pki,pkl,plj->pij',jac,cart,jac);metric_fixture_keep('Cartesian_pulled_tensor',expected)
 k=np.einsum('pab,b->pa',metric_value_matrix(R),coef);metric_fixture_keep('physical_six_values',k)
 actual=point_metric_tensor(k);metric_fixture_keep('physical_six_tensor',actual)
 env=np.einsum('pki,pkl,plj->pij',abs(jac),abs(cart),abs(jac))+abs(actual)
 check('new_metric_Cartesian_regular_polynomial',actual,expected,env)
 # Radial derivative of the actual coordinate powers, at fixed coefficients.
 dk=np.einsum('pab,b->pa',metric_R_matrix(R),coef);metric_fixture_keep('physical_six_Rjet',dk)
 dk_expected=np.column_stack((2*R*coef[1],np.zeros(2),2*R*coef[0],np.full(2,coef[3]),3*R**2*coef[2],2*R*coef[4]))
 metric_fixture_keep('physical_six_Rjet_expected',dk_expected)
 check('new_metric_R_power_jets',dk,dk_expected,abs(dk)+abs(dk_expected))
 # Momentum coordinates contain offdiag2; velocity coordinates do not.
 pi=np.array([[[1/2,1/7,-1/11],[1/7,2/3,1/13],[-1/11,1/13,3/4]]]);metric_fixture_keep('canonical_tensor',pi)
 pc=tensor_momentum_coordinates(pi);metric_fixture_keep('canonical_six_coordinates',pc)
 reconstructed=symmetric_tensor_from_coordinates(pc);metric_fixture_keep('canonical_tensor_reconstructed',reconstructed)
 pair=np.einsum('a,pa->p',pc[0],k);pair_expected=np.einsum('ij,pij->p',pi[0],actual)
 metric_fixture_keep('canonical_pair',pair);metric_fixture_keep('canonical_pair_tensor',pair_expected)
 av=np.r_[pc.ravel(),reconstructed.ravel(),pair];ev=np.r_[np.array([1/2,2/3,3/4,2/7,-2/11,2/13]),pi.ravel(),pair_expected]
 pe=np.einsum('ij,pij->p',abs(pi[0]),abs(actual))+abs(pair)
 check('new_metric_offdiagonal_canonical_factor_two',av,ev,np.r_[abs(pc).ravel()+abs(ev[:6]),abs(pi).ravel()+abs(reconstructed).ravel(),pe])
 # Independent diagonal-frame DeWitt formula; no native/EH solve or eigensystem.
 ih=np.diag([1/4,1/9,1/16]);cEH=dict(ih=ih[None],sqrt_h=np.array([24.]),N=np.array([7/5]))
 EH,EHenv=EH_metric_block(cEH);metric_fixture_keep('EH_six_matrix',EH);metric_fixture_keep('EH_operation_envelope',EHenv)
 fac=30/(7*C);d=np.array([1/4,1/9,1/16]);EH_expected=np.zeros((6,6))
 for i in range(3):
  for j in range(3):
   if i!=j:EH_expected[i,j]=-fac*d[i]*d[j]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):EH_expected[a,a]=2*fac*d[i]*d[j]
 metric_fixture_keep('EH_independent_diagonal_frame',EH_expected)
 check('new_metric_EH_diagonal_frame_block',EH[0],EH_expected,EHenv[0]+abs(EH_expected))
 trace=np.array([8.,18.,32.,0.,0.,0.]);shear=np.array([0.,0.,0.,6.,0.,0.]);metric_fixture_keep('EH_trace_shear_rates',np.stack((trace,shear)))
 action=np.array([trace@EH[0]@trace,shear@EH[0]@shear,trace@EH[0]@shear]);target=np.array([-720/(7*C),60/(7*C),0.])
 bound=np.array([abs(trace)@EHenv[0]@abs(trace),abs(shear)@EHenv[0]@abs(shear),abs(trace)@EHenv[0]@abs(shear)])+abs(target)
 metric_fixture_keep('EH_trace_shear_action',action);metric_fixture_keep('EH_trace_shear_expected',target)
 check('new_metric_EH_trace_shear',action,target,bound)
 # Fresh isolated tilted witness: v=4/5,gamma=5/3,z=3/8,gw=3/10,
 # omega=1/4,ell=1/6, and hdot=2k I. At fixed spatial covector U_i,
 # L_modal=m(zdot-kz)^2/2-n(kz)^2/2, m=1798/135,n=2/135.
 # Full six-metric jets are used; no old105 assembly/inverse/helper replay.
 g=np.diag([-1.,1.,1.,1.])[None];U=np.array([[5/3,4/3,0.,0.]]);uc=np.array([[-5/3,4/3,0.,0.]])
 z=np.zeros((32,1,4));z[0,0,2]=3/8;w=np.r_[3/10,np.full(31,7/310)];omega=np.full(32,1/4)
 P=np.eye(4)[None]+np.einsum('pa,pb->pab',uc,U)
 s=dict(g=g,hi=g.copy(),U=U,z=z,Z=np.zeros((1,4)),P=P,w=w,omega=omega)
 for name,value in s.items():metric_fixture_keep('tilted_'+name,value)
 e=metric_basis();embed=np.zeros((1,6,4,4));embed[:,:,1:,1:]=e[None]
 JU=np.zeros((1,4,3));JU[0,0,0]=4/5;JU[0,1:]=np.eye(3)
 Uh=np.zeros((1,6,4));Uh[0,0]=np.array([-8/15,-4/3,0.,0.]);Uh[0,3,2]=-4/3;Uh[0,4,3]=-4/3
 JzU=np.zeros((32,1,3));JzU[0,0,1]=-9/40;Jzz=np.array([[-4/5,0.,0.]])
 zh=np.zeros((32,1,6));zh[0,0,3]=3/10
 c=dict(JU=JU,Uh=Uh,JzU=JzU,Jzz=Jzz,zh=zh,embed=embed,dens=np.ones(1))
 for name,value in c.items():metric_fixture_keep('tilted_chart_'+name,value)
 y=np.zeros(99);y[4]=1.;kiso=np.array([2.,2.,2.,0.,0.,0.]);tangents=[];mom=[];jets=[]
 for name,yn,km in (('modal',y,np.zeros(6)),('metric',np.zeros(99),kiso)):
  metric_fixture_keep('tilted_'+name+'_native_rate',yn);metric_fixture_keep('tilted_'+name+'_metric_rate',km)
  du,dz,dg,dGa=native_velocity_jet(s,c,yn,km)
  for label,a in (('du',du),('dz',dz),('dg',dg),('Gamma',dGa)):metric_fixture_keep('tilted_'+name+'_'+label,a)
  t=kinetic_tangent(s,du,dz,dGa,ell=1/6)
  for label,a in t.items():metric_fixture_keep('tilted_'+name+'_'+label,a)
  py,ph=reduced_momenta(s,c,t['delta_PiU'],t['delta_Pi'],t['delta_Ctime']);metric_fixture_keep('tilted_'+name+'_p99',py);metric_fixture_keep('tilted_'+name+'_pmetric',ph)
  tangents.append(t);mom.append((py,ph));jets.append((du,dz,dg))
 H=np.array([[mom[0][0][0,4],mom[1][0][0,4]],[2*mom[0][1][0,:3].sum(),2*mom[1][1][0,:3].sum()]])
 target=np.array([[1798/135,-899/180],[-899/180,449/240]]);metric_fixture_keep('tilted_two_column_momentum_H',H);metric_fixture_keep('tilted_two_column_expected_H',target)
 G=np.zeros((2,2));Ge=np.zeros((2,2))
 for a,ta in enumerate(tangents):
  for b,tb in enumerate(tangents):
   mx=-ALPHA*np.einsum('pab,pac,pbd,pcd->p',ta['delta_F'],s['hi'],s['hi'],tb['delta_F'])/2
   vv=np.einsum('jpa,pab,jpb->jp',ta['delta_V'],s['hi'],tb['delta_V'])/omega[:,None]**2
   dd=-(1/36)*np.einsum('jpab,pac,pbd,jpcd->jp',ta['delta_D'],s['hi'],s['hi'],tb['delta_D'])
   G[a,b]=(mx+np.einsum('j,jp->p',w,vv+dd))[0]
   emx=ALPHA*np.einsum('pab,pac,pbd,pcd->p',abs(ta['delta_F']),abs(s['hi']),abs(s['hi']),abs(tb['delta_F']))/2
   evv=np.einsum('jpa,pab,jpb->jp',abs(ta['delta_V']),abs(s['hi']),abs(tb['delta_V']))/omega[:,None]**2
   edd=(1/36)*np.einsum('jpab,pac,pbd,jpcd->jp',abs(ta['delta_D']),abs(s['hi']),abs(s['hi']),abs(tb['delta_D']))
   Ge[a,b]=(emx+np.einsum('j,jp->p',w,evv+edd))[0]
 metric_fixture_keep('tilted_two_column_independent_Gram',G);metric_fixture_keep('tilted_two_column_Gram_envelope',Ge)
 check('new_metric_tilted_fulljet_gradient_block',np.stack((H,G)),np.stack((target,target)),np.stack((Ge+abs(target),Ge+abs(target))))
 schur=H[1,1]-H[1,0]*H[0,1]/H[0,0];se=abs(H[1,1])+abs(H[1,0]*H[0,1]/H[0,0])+1/480
 metric_fixture_keep('tilted_retained_Schur',np.array(schur));metric_fixture_keep('tilted_Schur_envelope',np.array(se))
 check('new_metric_tilted_native_Schur_is_not_EH',np.array(schur),np.array(-1/480),np.array(se))
 units=[];trans=[];ue=[];te=[]
 for du,dz,dg in jets:
  units.append(np.einsum('pab,pa,pb->p',dg[:,0],U,U)+2*np.einsum('pa,pab,pb->p',U,g,du[:,0]))
  trans.append(np.einsum('pa,jpa->jp',du[:,0],z)+np.einsum('pa,jpa->jp',U,dz[:,:,0]))
  ue.append(np.einsum('pab,pa,pb->p',abs(dg[:,0]),abs(U),abs(U))+2*np.einsum('pa,pab,pb->p',abs(U),abs(g),abs(du[:,0])))
  te.append(np.einsum('pa,jpa->jp',abs(du[:,0]),abs(z))+np.einsum('pa,jpa->jp',abs(U),abs(dz[:,:,0])))
 actual=np.r_[np.asarray(units).ravel(),np.asarray(trans).ravel()];env=np.r_[np.asarray(ue).ravel(),np.asarray(te).ravel()]
 metric_fixture_keep('tilted_unit_transverse_jets',actual);metric_fixture_keep('tilted_unit_transverse_envelope',env)
 check('new_metric_tilted_constraint_preserving_jets',actual,np.zeros_like(actual),env)
 assert len(CHECKS)-start==8
 return dict(new_controls=8,scope='Artificial six-metric algebra only; no physical field, clock, inertia or source selected')


def new_packet(weak,whole,q1,fixed,cp):
 global RAW,AVAILABLE,GEO
 ev=read_pair(weak['input'],('r_kpc','z_kpc','xi','weights'));w=ev['weights'];xi=ev['xi'];assert w.shape==xi.shape==(32,) and np.all(w>0) and np.all(xi>0) and np.all(np.diff(xi)>0)
 omega=SIGMA*xi*fixed['Hunit']/299792458.;Hbar=fixed['Hunit']/299792458.*cp['background']['h'];assert math.isfinite(Hbar) and Hbar>0 and np.all(omega>0) and np.all(np.isfinite(omega))
 checkpoint('INPUT',ev,dict(kind='same_sigma1_grid_modes_and_authenticated_CLOSED_weak99',sigma=SIGMA,fixed=fixed,owned_background=cp['background'],Hbar=Hbar,weak99_result_sha256=WEAK_METRIC_PINS[WEAK_METRIC_PARENT+'_RESULT.json'],weak99_receipt_sha256=WEAK_METRIC_PINS[WEAK_METRIC_PARENT+'_RECEIPT.json'],saved_audit_sha256=weak['saved_audit_sha256'],new_RHS=6,new_source_terms=False))
 RAW={};AVAILABLE={};cs=len(CHECKS);weak_metric_fixtures();checkpoint('FIXTURE',RAW,dict(kind='independent_new_metric_and_EH_tilt_arithmetic',controls=CHECKS[cs:],physical_state=False))
 RAW={};AVAILABLE={};g,b,pre,bc=load_weak_map(weak);GEO=g;RAW={};cs=metric_basis_controls(g);RAW.update({f'geometry_{k}':a for k,a in g.items()});checkpoint('BASIS',RAW,dict(kind='regular_six_metric_temporal_Q1_basis',controls=CHECKS[cs:],metric_order=['a','b','c','d','e','f'],local_order=['RR','ZZ','phiphi','RZ','Rphi','Zphi'],metric_independent=23048,scalar_independent=3870,outer_rates_retained=True,physical_boundary_history=None))
 data=[];columns=[]
 for iq,(wr,qr) in enumerate(zip(whole['columns'],q1['columns'])):
  d,rec=assemble_column(iq,wr,qr,bc,w,omega,Hbar);data.append(d);columns.append(rec)
 hats,kv,sample,solves=sampled_metric_response(data,g,b,pre);affine=affine_CMC_vectors(data,bc,g,Hbar,hats,kv)
 return dict(sigma=SIGMA,status='CONDITIONAL_WEAK_METRIC_TEMPORAL_CMC_SAMPLE_PASS',columns=columns,solves=solves,sampled=sample,affine_CMC=affine,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded six-metric weak temporal sample: FULL root/distinct reviews required.')
 assert PROTOCOL_SHA and len(PROTOCOL_SHA)==64 and sha(path(STEM+'.md'))==PROTOCOL_SHA
 assert not list(BASE.glob(STEM+'_*')),'Unused namespace required; old outputs preserved'
 INPUTS,weak,whole,q1,fixed,cp=weak_metric_admission()
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():assert sha(path(n))==h;INPUTS[str(path(n).resolve())]=h
 INPUTS[str(Path(__file__).resolve())]=sha(__file__);OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,sigma=SIGMA,configuration=dict(new_metric_columns=6,new_native_RHS=6,modes=32,quadrature_columns=4,points=15136,grid=[87,45],native_basis=380292,metric_basis=23048,CMC_scalar_basis=3870,hat_node=[43,22],native_cap=NATIVE_CAP,arithmetic_tolerance=TOL,linear_tolerance=LINEAR_TOL),qualification=FLAGS))
  import numpy as _np
  np=_np;case=new_packet(weak,whole,q1,fixed,cp)
  assert len(CHECKS)==EXPECTED_CONTROLS and all(c['passed'] for c in CHECKS)
  normal=[r for r in RECORDS if r['metadata']['kind']!='resumable_unqualified_native_iterate'];assert len(normal)==16 and len(RECORDS)<=64
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_WEAK_METRIC_TEMPORAL_CMC_ARITHMETIC_PASS',cases=[case],controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\nSix new regular metric hats at node (43,22), their genuinely new weak native responses, and signed global Schur sample are retained. All32 modes and all four sigma1 quadrature columns are included.\n\nFull affine metric/native vectors and weak CMC trace data are saved. No affine baseline inverse, full metric solve, CMC lapse force, physical rate, source addition, history or galaxy velocity is selected. Activity outside 0.3–15.1 kpc remains undefined; no galaxy edge is inferred from that coverage.\n').encode());recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);recheck();print('CONDITIONAL_WEAK_METRIC_TEMPORAL_CMC_ARITHMETIC_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unqualified_available_weak_metric_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'*.npz') if p.name not in {r['file'] for r in RECORDS}],qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  seal_actual();recheck(False);raise

if __name__=='__main__':raise SystemExit(main())
