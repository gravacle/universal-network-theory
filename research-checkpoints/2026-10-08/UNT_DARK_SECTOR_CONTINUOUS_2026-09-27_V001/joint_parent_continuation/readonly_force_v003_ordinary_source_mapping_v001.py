"""Root-authorized CLOSED saved-source mapping only; no producer/helper calls."""
import hashlib,json,os,pathlib,traceback
BASE=pathlib.Path(__file__).resolve().parent
OUTPUT=BASE/'READONLY_FORCE_V003_ORDINARY_SOURCE_MAPPING_V001.json'
TERMINALS={
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001':('ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798','eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde',13990),
 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003':('981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770','822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2',36387)}
AUDIT='READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json'
AUDIT_SHA='80b7fac6e83d178bc2eb706853d301bbf258e0fe9f22caa0423e28010eac66e2'
PINS={};CHECKS=[];np=None

def path(name):
 p=pathlib.Path(name);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for a in iter(lambda:f.read(1048576),b''):h.update(a)
 return h.hexdigest()

def bind(name,expected):
 key=str(path(name).resolve());assert PINS.get(key,expected)==expected
 assert sha(name)==expected,(name,'seal');PINS[key]=expected

def resolve(ref,mapping):
 bind(ref['commit_file'],ref['commit_sha256']);d=json.loads(path(ref['commit_file']).read_text())
 assert d['file']==ref['file'] and d['sha256']==ref['sha256']
 if 'metadata' in ref:assert d['metadata']==ref['metadata']
 bind(d['file'],d['sha256'])
 assert mapping[str(path(d['file']).resolve())]==d['sha256']
 assert mapping[str(path(ref['commit_file']).resolve())]==ref['commit_sha256']
 return d

def load(rec,names):
 schema=rec['metadata']['schema'];out={}
 with np.load(path(rec['file']),allow_pickle=False) as z:
  for n in names:
   a=z[n];sd=schema[n]
   assert list(a.shape)==sd['shape'] and str(a.dtype)==sd['dtype'] and sd['finite'] is True
   assert np.all(np.isfinite(a)),n;out[n]=a
 return out

def bit(name,a,b):
 assert a.shape==b.shape and a.dtype==b.dtype and a.tobytes()==b.tobytes(),name
 CHECKS.append(dict(name=name,kind='bit_exact',entries=int(a.size)))

def close(name,a,b,envelope):
 e=np.broadcast_to(envelope,np.shape(a));ratio=np.abs(a-b)/np.maximum(e,1e-30)
 value=float(np.max(ratio));assert value<=2e-11,(name,value)
 CHECKS.append(dict(name=name,kind='saved_contraction',error=value,tolerance=2e-11))

def main():
 global np
 print('SAVED_MAPPING_PID',os.getpid(),flush=True)
 bind(AUDIT,AUDIT_SHA);aud=json.loads(path(AUDIT).read_text());assert aud['status']=='SAVED_PACKET_AUDIT_PASS'
 terminals={};merged={}
 for stem,(rh,ch,pid) in TERMINALS.items():
  bind(stem+'_RESULT.json',rh);bind(stem+'_RECEIPT.json',ch)
  r=json.loads(path(stem+'_RESULT.json').read_text());rc=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['pid']==pid and rc['result_sha256']==rh
  assert rc.get('error_sha256') is None and all(v is False for v in r['qualification'].values())
  mp={str(path(k).resolve()):v for group in ('input_sha256','output_sha256') for k,v in rc[group].items()}
  for k,h in mp.items():assert merged.get(k,h)==h;merged[k]=h
  terminals[stem]=(r,rc,mp)
 metric,_,mm=terminals['CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001']
 force,_,fm=terminals['CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003']
 mr=resolve(next(c['checkpoint'] for c in metric['cases'] if c['sigma']==1.),merged)
 assert mr['file']=='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_00003_ARM.npz' and mr['metadata']['sigma']==1.
 fr=resolve(force['cases'][0]['loads'],merged);assert force['cases'][0]['sigma']==1.
 ir=resolve(metric['checkpoints'][0],merged)
 # The exact force-owned ancestor references are authenticated by its CLOSED map.
 qrname='CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00012_ARM.npz'
 orname='CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001_00003_ARM.npz'
 refs=[]
 for n in (qrname,orname):
  cn=n+'.COMMIT.json';bind(cn,fm[str(path(cn).resolve())]);d=json.loads(path(cn).read_text())
  refs.append(resolve(dict(file=n,sha256=d['sha256'],commit_file=cn,commit_sha256=fm[str(path(cn).resolve())]),fm))
 qr,orr=refs;assert qr['metadata']['sigma']==orr['metadata']['sigma']==1.
 import numpy as numpy
 np=numpy
 m=load(mr,('source_g','source_hi','source_Ga','source_R','source_Z','source_k','source_D','source_n','source_Gamma'))
 f=load(fr,tuple('ordinary_input_'+n for n in ('source_g','source_R','source_Z','source_specific_covariant_p','source_mass_weight','source_indices','source_right_weight'))+('ordinary_gamma','ordinary_up'))
 q=load(qr,tuple(n for n in qr['metadata']['schema'] if n.startswith('source_')))
 o=load(orr,('source_g','source_k','source_D','p_phi','mass_weight'))
 sam=load(ir,('source_samples32','r_kpc'))
 for n in ('source_g','source_R','source_Z'):
  bit('metric_to_force_'+n,m[n],f['ordinary_input_'+n]);bit('Q1_to_force_'+n,q[n],f['ordinary_input_'+n])
 for n in ('source_specific_covariant_p','source_mass_weight','source_indices','source_right_weight'):
  bit('Q1_to_force_'+n,q[n],f['ordinary_input_'+n])
 bit('Frechet_metric',m['source_g'],o['source_g']);bit('Frechet_worldline',m['source_k'],o['source_k']);bit('Frechet_D',m['source_D'],o['source_D'])
 bit('Frechet_mass_weight',o['mass_weight'],f['ordinary_input_source_mass_weight']);bit('Frechet_p_phi',o['p_phi'],f['ordinary_input_source_specific_covariant_p'][:,2])
 bit('sample_radius_order',m['source_R'],sam['source_samples32'][:,0])
 g=m['source_g'];hi=m['source_hi'];k=m['source_k'];D=m['source_D'];p=f['ordinary_input_source_specific_covariant_p']
 assert np.all(D>0) and np.all(m['source_Z']==0) and np.all(f['ordinary_input_source_mass_weight']>=0)
 idx=f['ordinary_input_source_indices'];t=f['ordinary_input_source_right_weight'];r=sam['r_kpc']
 assert idx.dtype==np.dtype('int64') and np.all((idx>=0)&(idx<86)) and np.all((t>0)&(t<1))
 close('support_hat_location',(1-t)*r[idx]+t*r[idx+1],m['source_R'],abs((1-t)*r[idx])+abs(t*r[idx+1])+abs(m['source_R']))
 dd=-np.einsum('pa,pab,pb->p',k,g,k);de=np.einsum('pa,pab,pb->p',abs(k),abs(g),abs(k));close('worldline_norm',D,dd,de)
 pp=np.einsum('pij,pj->pi',g[:,1:,:],k)/np.sqrt(D)[:,None]
 pe=np.einsum('pij,pj->pi',abs(g[:,1:,:]),abs(k))/np.sqrt(D)[:,None];close('specific_covariant_momentum',p,pp,pe)
 N=1/np.sqrt(-hi[:,0,0]);close('saved_lapse',N,m['source_n'],abs(N)+abs(m['source_n']))
 close('material_gamma',f['ordinary_gamma'],N/np.sqrt(D),abs(f['ordinary_gamma'])+N/np.sqrt(D))
 close('saved_material_gamma',f['ordinary_gamma'],m['source_Gamma'],abs(f['ordinary_gamma'])+abs(m['source_Gamma']))
 close('gamma_momentum_norm',f['ordinary_gamma']**2,1+np.sum(p*f['ordinary_up'],axis=1),f['ordinary_gamma']**2+1+np.sum(abs(p*f['ordinary_up']),axis=1))
 close('inverse_metric',np.einsum('pij,pjk->pik',g,hi),np.broadcast_to(np.eye(4),g.shape),np.einsum('pij,pjk->pik',abs(g),abs(hi))+np.eye(4))
 for n,h in PINS.items():assert sha(n)==h
 out=dict(status='SAVED_ORDINARY_MAPPING_PASS',pid=os.getpid(),source_sha256=sha(__file__),input_sha256=PINS,points=4832,sigma=1.,checks=CHECKS,source_Ga_usable_with_exact_saved_geometry=True,source_hi_owned=True,qualification=False,scope='saved point-order/mass/momentum/metric association only; no Hamiltonian-rate/helper/metric reconstruction or physical evolution')
 with OUTPUT.open('x') as fjson:json.dump(out,fjson,sort_keys=True,indent=2);fjson.write('\n')
 OUTPUT.chmod(0o444);print('SAVED_ORDINARY_MAPPING_PASS',len(CHECKS),sha(OUTPUT),flush=True)

if __name__=='__main__':
 try:main()
 except BaseException:
  failure=BASE/'READONLY_FORCE_V003_ORDINARY_SOURCE_MAPPING_V001_REFUSAL.json'
  with failure.open('x') as f:json.dump(dict(pid=os.getpid(),source_sha256=sha(__file__),inputs=PINS,checks=CHECKS,traceback=traceback.format_exc()),f,indent=2)
  failure.chmod(0o444);raise
