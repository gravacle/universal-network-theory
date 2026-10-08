"""HELD saved-only failure/gate proof. New positive operation bounds only.
No producer import, signed feature/canonical/operator replay, solve or evolution.
All V001 signed arrays, original seven True/one False controls remain unchanged.
"""
from pathlib import Path
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001'
AUDIT='READONLY_'+STEM+'_FAILURE_GATE_PROOF'
AUTHOR_DRAFT=True
TERMINAL=dict(owner_pid=34079,source_sha256='8aba0c892ec0a029e09d5380b18d489f9f9838aac84d6a95628dd1e41508e1c2',protocol_sha256='bf321450bae902a94099e28e27de5c1e197b0c4d11551ecefce1826050ed14de',error_sha256='8abfa418e010ebd5728845461e3391a73064925015537bdaa88643202e8d0c83',receipt_sha256='fd79952cefba089c86568c8641e88df1a9df50a8ef3c1935a5e6a3490b300b85')
ALPHA=.02/1.98;ELL=.1;RAW={}
BOUND_FRAGMENT_SHA256='c333059f668027a34b4f17d566aca5d6202e7b9ab290956513288efbd34268d3'
np=None;COUNTS=dict(pairs=0,arrays=0,entries=0,negative_entries=0,nonfinite_entries=0)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def read_json(n):return json.loads(path(n).read_text())

def record(r,owner,names=None):
 assert sha(r['file'])==r['sha256'] and sha(r['commit_file'])==r['commit_sha256']
 assert read_json(r['commit_file'])=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 md=r['metadata'];assert md['owner']==owner and all(v is False for v in md['qualification'].values());out={}
 with np.load(path(r['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for n,s in md['schema'].items():
   a=f[n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and a.dtype.kind in 'fiub';fin=np.isfinite(a);assert bool(np.all(fin))==s['finite'] and s['finite'],n
   COUNTS['arrays']+=1;COUNTS['entries']+=a.size;COUNTS['negative_entries']+=int(np.count_nonzero(a<0));COUNTS['nonfinite_entries']+=int(a.size-np.count_nonzero(fin))
   if names is None or n in names or n.startswith('control_'):out[n]=a.copy()
 COUNTS['pairs']+=1;return out

def parent(ref,names):
 assert sha(ref['file'])==ref['sha256'] and sha(ref['commit_file'])==ref['commit_sha256'];md=read_json(ref['commit_file']);assert md=={k:v for k,v in ref.items() if k not in ('commit_file','commit_sha256')}
 with np.load(path(ref['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md['metadata'];out={}
  for n in names:
   a=f[n];s=md['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a));out[n]=a.copy()
 return out

# Definitions only. Exact pre-cancellation readout bounds; no signed physics call.
def native_momentum_operation_envelopes(s,c,label,du=None,dz=None):
 g,hi,U,z=s['g'],s['hi'],s['U'],s['z'];w,om=s['w'],s['omega'];N,ga,be,ih=c['N'],c['gamma'],c['beta'],c['ih']
 du=s['du'] if du is None else du;dz=s['dz'] if dz is None else dz
 out={}
 def put(name,a):
  out[name]=a;RAW['momentum_operation_'+label+'_'+name]=a.copy()
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0)
  return a
 # All additions precede covariant derivative and projector cancellations.
 euc=put('U_cov',np.einsum('pab,pb->pa',abs(g),abs(U)))
 enu=put('nu',abs(du)+np.einsum('pbal,pl->pab',abs(s['Ga']),abs(U)))
 enz=put('nz',abs(dz)+np.einsum('plab,jpl->jpab',abs(s['Ga']),abs(z)))
 ep=put('P',np.eye(4)[None]+euc[:,:,None]*abs(U)[:,None,:])
 eq=put('q',np.einsum('pa,jpab->jpb',abs(U),enz))
 ev=put('V',np.einsum('pab,jpb->jpa',ep,eq))
 ed=put('D',np.einsum('pac,jpcd,pbd->jpab',ep,enz,ep))
 elower=put('nu_lower',np.einsum('pab,pcb->pca',abs(g),enu))
 ef=put('F',elower+elower.swapaxes(1,2))
 ez=put('Z',np.einsum('j,jpa->pa',abs(w),abs(z)))
 epiu=put('PiU',abs(ALPHA)*np.einsum('pac,pcb->pab',abs(hi),ef)+np.einsum('pa,pb->pab',abs(U),ez))
 epi=put('Pi',abs(w)[:,None,None,None]*(np.einsum('pa,jpb->jpab',abs(U),np.einsum('pab,jpb->jpa',abs(hi),ev))/abs(om)[:,None,None,None]**2+ELL**2*np.einsum('pac,jpcd,pdb->jpab',abs(hi),ed,abs(hi))))
 # u=g_sp U and h^-1 u are propagated before their possible exact-zero sums.
 eup=put('up',np.einsum('pij,pj->pi',abs(ih),euc[:,1:]))
 eju=np.empty_like(c['JU']);eju[:,0]=eup/abs(N*ga)[:,None]
 eju[:,1:]=abs(ih)+abs(be)[:,:,None]*eju[:,None,0,:];put('JU',eju)
 ejzu=put('JzU',np.einsum('jpa,pai->jpi',abs(z),eju)/abs(U[None,:,0,None]))
 ejzz=put('Jzz',(eup+abs(be)*abs(ga/N)[:,None])/abs(U[:,0,None]))
 eu=put('native_U',np.einsum('pa,pai->pi',epiu[:,0],eju)+np.einsum('jp,jpi->pi',epi[:,:,0,0],ejzu))
 em=put('native_modes',epi[:,:,0,1:]+epi[:,:,0,0,None]*ejzz[None])
 value=put('native_density',abs(c['dens'])[:,None]*np.concatenate((eu,em.transpose(1,0,2).reshape(len(U),96)),axis=1))
 return value,out

def saved_affine_point_momentum_envelope(s,c,bc,iq,new_rate,old_rate,old_du,old_dz):
 # The primal old pstar and recovered p were already saved; no p/field replay.
 old,operands=native_momentum_operation_envelopes(s,c,'old_pointstar',old_du,old_dz)
 sl=slice(iq*3784,(iq+1)*3784);p=len(new_rate)
 # Preserve the original subtraction's operation bound, not its rounded residue.
 v=abs(new_rate)+abs(old_rate);u=v[:,:3];zm=v[:,3:].reshape(p,32,3).transpose(1,0,2)
 M=bc['operation_eM0'][sl];L=bc['operation_eL'][:,sl];D=bc['operation_eD'][:,sl]
 mixed=zm+np.einsum('jpik,pk->jpi',L,u,optimize=True)
 modes=np.einsum('jpik,jpk->jpi',D,mixed,optimize=True)
 nativeU=np.einsum('pik,pk->pi',M,u,optimize=True)+np.einsum('jpki,jpk->pi',L,modes,optimize=True)
 action=np.concatenate((nativeU,modes.transpose(1,0,2).reshape(p,96)),axis=1)
 value=old+action
 for name,a in dict(delta_velocity=v,eM0=M,eL=L,eD=D,mixed=mixed,modes=modes,native_U=nativeU,action=action,old_pointstar=old,expected_density=value).items():
  RAW['momentum_operation_saved_affine_'+name]=a.copy()
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0)
 return value

def publish(n,v):
 raw=(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;print('READONLY_AUDIT_SHA256',sha(n),flush=True)

def main():
 global np
 if AUTHOR_DRAFT:raise SystemExit('HELD: root FULL static review and saved-only execution authorization required.')
 print('READONLY_SPATIAL_FAILURE_AUDIT_PID',os.getpid(),flush=True)
 assert sha('author_fragment_spatial_euler_v002_momentum_envelopes.txt')==BOUND_FRAGMENT_SHA256
 for n,k in (('cross_u_weak_canonical_spatial_euler_loads_v001.py','source_sha256'),(STEM+'.md','protocol_sha256'),(STEM+'_ERROR.json','error_sha256'),(STEM+'_RECEIPT.json','receipt_sha256')):assert sha(n)==TERMINAL[k]
 er=read_json(STEM+'_ERROR.json');rc=read_json(STEM+'_RECEIPT.json');owner=rc['owner'];assert rc['status']=='CLOSED_ERROR' and rc['closed'] and er['owner']==owner and owner['owner']=='root' and owner['pid']==34079 and owner['source_sha256']==TERMINAL['source_sha256']
 assert rc['error_sha256']==TERMINAL['error_sha256'] and er['status']=='FAILED' and er['prior_receipt_sha256'] is None and all(x is False for x in rc['qualification'].values()) and er['qualification']==rc['qualification']
 assert read_json(STEM+'_OWNER_START.json')==owner and read_json(STEM+'_MANIFEST.json')['input_sha256']==rc['input_sha256']
 hashes={}
 for group in ('input_sha256','output_sha256'):
  for n,h in rc[group].items():assert n not in hashes or hashes[n]==h;hashes[n]=h;assert sha(n)==h,n
 for n,h in er['preserved_outputs'].items():assert sha(n)==h
 recs=er['checkpoints'];controls=er['controls'];assert len(recs)==4 and len(controls)==8 and [x['ordinal'] for x in controls]==list(range(8)) and all(x['passed'] for x in controls[:7]) and controls[7]['passed'] is False
 assert er['context']['column']==0 and er['context']['ordinal']==7 and er['unqualified_npz']==[] and not path(STEM+'_RESULT.json').exists()
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in recs} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in recs}
 for n in rc['output_sha256']:assert path(n).stat().st_mode&0o777==0o444
 import numpy as _np
 np=_np;arrays={};witness=set()
 needed={'current_'+k for k in ('U','z','g','hi','Ga','w','omega','du','dz') }|{'seed_owned_du','seed_owned_dz','seed_current_du','seed_current_dz','seed_nodal_native_rate','seed_old_L2_native_rate','native_config_momentum','native_config_momentum_envelope'}
 for rec in recs:
  names=needed if rec['metadata']['failed'] else ({'geometry_R','geometry_cell_i','geometry_cell_j'} if 'BASIS' in rec['file'] else set())
  d=record(rec,owner,names);arrays[rec['metadata']['kind']]=d
  for row in controls:
   prefix=f"control_{row['ordinal']:03d}_{row['name']}_"
   if prefix+'actual' in d:
    a,b,e=[d[prefix+k] for k in ('actual','expected','envelope')];assert a.shape==b.shape==e.shape and np.all(e>=0)
    error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));assert row['tolerance']==2e-11 and abs(error-row['error'])<=2e-13*max(1.,abs(error)) and (error<=2e-11) is row['passed'];witness.add(row['ordinal'])
 assert witness==set(range(8));raw=arrays['unqualified_available_canonical_spatial_Euler_operands'];basis=arrays['unchanged_genuine_native_and_regular_six_metric_configuration_basis']
 assert len(recs[-1]['metadata']['schema'])==118 and all(r['metadata']['kind']!='new_sigma1_canonical_spatial_Euler_coefficients_on_explicit_mixed_seed' for r in recs)
 wr=read_json('CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json');coef=next(r for r in wr['checkpoints'] if r['metadata']['kind']=='complete_fixed_metric_native99_mass_coefficients');solution=wr['cases'][0]['solution'];solution=dict(read_json(solution['commit_file']),commit_file=solution['commit_file'],commit_sha256=solution['commit_sha256'])
 bc=parent(coef,('operation_eL','operation_eD','operation_eM0'))
 qr=read_json('CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RESULT.json');qcase=next(x for x in qr['cases'] if x['sigma']==1.);qref=qcase['columns'][0]
 assert sha(qref['commit_file'])==qref['commit_sha256'];qrecord=read_json(qref['commit_file']);assert qrecord['file']==qref['file'] and qrecord['sha256']==qref['sha256']
 qrecord=dict(qrecord,commit_file=qref['commit_file'],commit_sha256=qref['commit_sha256']);owned=parent(qrecord,tuple('owned_chart_'+k for k in ('N','gamma','beta','ih','JU','dens')));c={k.removeprefix('owned_chart_'):v for k,v in owned.items()}
 s={k:raw['current_'+k] for k in ('g','hi','Ga','U','z','du','dz','w','omega')}
 sv=parent(solution,('recovered_point_momentum_density','recovered_qpoint_native_velocity'));prefix='control_007_new_seed_native_canonical_momentum_';a,b,e=[raw[prefix+k] for k in ('actual','expected','envelope')]
 assert np.array_equal(a,raw['native_config_momentum']) and np.array_equal(e,raw['native_config_momentum_envelope']+abs(b))
 assert np.array_equal(b,sv['recovered_point_momentum_density'][:,:3784].transpose(1,0,2).reshape(3784,99)) and np.array_equal(raw['seed_nodal_native_rate'],sv['recovered_qpoint_native_velocity'][:,:3784].transpose(1,0,2).reshape(3784,99))
 assert np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(s['U'][:,0]>0) and np.all(s['omega']>0) and np.all(s['w']>0)
 actual_bound,_=native_momentum_operation_envelopes(s,c,'new_current')
 expected_bound=saved_affine_point_momentum_envelope(s,c,bc,0,raw['seed_nodal_native_rate'],raw['seed_old_L2_native_rate'],raw['seed_owned_du'],raw['seed_owned_dz'])
 newden=actual_bound+expected_bound;oldratio=abs(a-b)/np.maximum(e,1e-30);newratio=abs(a-b)/np.maximum(newden,1e-30);i=np.unravel_index(int(np.argmax(oldratio)),a.shape);j=np.unravel_index(int(np.argmax(newratio)),a.shape)
 groups=[dict(group='U_'+name,old_max=float(np.max(oldratio[:,k])),propagated_max=float(np.max(newratio[:,k]))) for k,name in enumerate(('R','Z','phi'))]+[dict(group='mode_'+str(k),old_max=float(np.max(oldratio[:,3+3*k:6+3*k])),propagated_max=float(np.max(newratio[:,3+3*k:6+3*k]))) for k in range(32)]
 def peak(ix):
  return dict(point=int(ix[0]),coordinate=int(ix[1]),R=float(basis['geometry_R'][0,ix[0]]),cell_i=int(basis['geometry_cell_i'][ix[0]]),cell_j=int(basis['geometry_cell_j'][ix[0]]),actual=float(a[ix]),expected=float(b[ix]),difference=float(a[ix]-b[ix]),old_envelope=float(e[ix]),actual_operation_bound=float(actual_bound[ix]),expected_operation_bound=float(expected_bound[ix]),old_ratio=float(oldratio[ix]),propagated_ratio=float(newratio[ix]))
 schema=recs[-1]['metadata']['schema'];features=all('current_'+k in schema for k in ('g','hi','Ga','U','du','z','dz','phi','nu','nz','P','q','V','D','F','Fup','Pi','PiU','Z','A','mu','a','r','f','z2','uc','omega','xi','w'));charts=all('chart_first_'+k in schema for k in ('dg','dhi','dN','dbeta','dh','dih','du_cov','dup','dgamma','dJU','dJzU','dJzz','dUh','dzh','dembed'));native=all('native_config_'+k in schema for k in ('coefficient','envelope','momentum','momentum_envelope','A_can','P_can','A_z_raw','nJU','nJzu','nJzz'))
 assert features and charts and native;assert np.all(np.isfinite(newden)) and np.all(newden>=0)
 for n,h in hashes.items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('author_fragment_spatial_euler_v002_momentum_envelopes.txt')==BOUND_FRAGMENT_SHA256
 report=dict(positive_bound_fragment_sha256=BOUND_FRAGMENT_SHA256,status='SAVED_FAILURE_GATE_PROOF_COMPLETE',terminal=TERMINAL,audit_pid=os.getpid(),census=COUNTS,input_bindings=len(rc['input_sha256']),output_bindings=len(rc['output_sha256']),original_controls=controls,original_failed_control_preserved=True,new_operation_bound_comparison=dict(tolerance=2e-11,max_ratio=float(np.max(newratio)),passed=bool(np.max(newratio)<=2e-11),different_denominator=True),old_peak=peak(i),propagated_peak=peak(j),groups=groups,norms=dict(actual=float(np.linalg.norm(a)),expected=float(np.linalg.norm(b)),difference=float(np.linalg.norm(a-b))),cached_column0=dict(raw_fields=118,complete_features=features,complete_chart_derivatives=charts,complete_native_configuration_coefficients=native,completed_column_checkpoint=False,physical_tail_uncomputed=True),scientific_operator_or_producer_replay=False,qualification=er['qualification'])
 publish(AUDIT+'.json',report);print(json.dumps({k:report[k] for k in ('status','audit_pid','census','new_operation_bound_comparison','old_peak')},sort_keys=True),flush=True)

if __name__=='__main__':
 try:main()
 except BaseException:
  if not AUTHOR_DRAFT:publish(AUDIT+'_READER_REFUSAL.json',dict(status='READER_REFUSAL',terminal=TERMINAL,audit_pid=os.getpid(),traceback=traceback.format_exc(),audit_source_sha256=sha(__file__)))
  raise
