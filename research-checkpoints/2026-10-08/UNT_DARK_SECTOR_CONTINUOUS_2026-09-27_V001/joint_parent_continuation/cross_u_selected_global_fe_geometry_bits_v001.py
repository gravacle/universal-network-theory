"""Guarded actual-array versus saved-scalar geometry bits; no action or solve."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SELECTED_GLOBAL_FE_GEOMETRY_BITS_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='c579b2ff765a4ab12ba83a3b7b242c978339949e27cce72eab421f97dbee91c7'
np=None;OWNER=None;INPUTS={};OUTPUTS={};ACTIVE={}
FLAGS=dict(original_canonical_admission=False,physical_rate_adoption=False,normal_constraint_seed=False,operator_evaluated=False,geometry_alignment_changed=False)
PINS={'CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_RESULT.json':'0c67ed1ead3fa33832a83eabd7f5527116b33bf645335e305ff5013be5e22c30','CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_RECEIPT.json':'e0e3add13fa0e153a766b87e446924e83b7e18ce6a137334a6bf458489b95d6d','READONLY_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_AUDIT_RESULT.json':'be8850340dcde4edd6fbcd1fad4f937aaff9887f5d18af6b3e7172778fe64633','CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_RESULT.json':'efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82','CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_RECEIPT.json':'8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'}
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(n)==h,n;INPUTS[key]=h
def publish(tag,obj):
 n=STEM+'_'+tag+'.json';raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with path(n).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path(n).chmod(0o444);assert path(n).read_bytes()==raw;OUTPUTS[n]=sha(n);return dict(file=n,sha256=OUTPUTS[n])
def recheck():
 for n,h in INPUTS.items():assert sha(n)==h,n
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(n)==h,n
def admission():
 for n,h in PINS.items():bind(n,h)
 st='CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001'
 proof=json.loads(path(st+'_RESULT.json').read_text());rc=json.loads(path(st+'_RECEIPT.json').read_text());reader=json.loads(path('READONLY_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_AUDIT_RESULT.json').read_text())
 assert rc['status']=='CLOSED' and rc['owner']==proof['owner'] and proof['owner']['pid']==43274 and rc['result_sha256']==PINS[st+'_RESULT.json'] and rc['error_sha256'] is None
 assert proof['status']=='BOUNDED_DOUBLE_DOUBLE_COMPONENT_COMPLETE' and len(proof['controls'])==15 and all(x['passed'] for x in proof['controls']) and all(x is False for x in proof['qualification'].values())
 assert reader['status']=='SAVED_DD_COMPONENT_AUDIT_PASS' and reader['pid']==43547 and reader['controls']==15 and reader['parent_status']=='CLOSED'
 assert reader['parent_terminal']['result_sha256']==PINS[st+'_RESULT.json'] and reader['parent_terminal']['receipt_sha256']==PINS[st+'_RECEIPT.json']
 n=st+'_INPUT.json';bind(n,rc['output_sha256'][n]);raw=json.loads(path(n).read_text())
 assert raw['owner']==proof['owner'] and len(raw['rows'])==2 and [r['group'] for r in raw['rows']]==[10,14]
 for row,result in zip(raw['rows'],proof['rows']):assert result['selection']=={k:v for k,v in row.items() if k!='contacts'} and len(row['contacts'])==16
 oldst='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001';old=json.loads(path(oldst+'_RESULT.json').read_text());oldrc=json.loads(path(oldst+'_RECEIPT.json').read_text())
 assert oldrc['status']=='CLOSED' and oldrc['owner']==old['owner'] and old['owner']['pid']==39611 and oldrc['result_sha256']==PINS[oldst+'_RESULT.json'] and oldrc['error_sha256'] is None
 assert old['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED' and len(old['controls'])==17 and all(x['passed'] for x in old['controls'])
 records=[q for q in old['checkpoints'] if q['metadata']['kind']=='unchanged_E_F_S_bases_and_positive_solver_congruences'];assert len(records)==1;rec=records[0]
 for key in ('file','commit_file'):
  n=rec[key];h=rec['sha256' if key=='file' else 'commit_sha256'];assert oldrc['output_sha256'][n]==h;bind(n,h)
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 for n,s in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44)),('cell_i',(3784,)),('cell_j',(3784,))):
  md=rec['metadata']['schema'][n];assert md['shape']==list(s) and md['dtype']==('int64' if n.startswith('cell_') else 'float64') and md['finite'] is True
 return raw['rows'],rec
def read_geometry(rec):
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==rec['metadata'] and set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'}
  out={}
  for n in ('R','dv','hats','cell_i','cell_j'):
   a=f[n];ACTIVE['loaded_'+n]=dict(shape=list(a.shape),dtype=str(a.dtype));md=rec['metadata']['schema'][n]
   assert list(a.shape)==md['shape'] and str(a.dtype)==md['dtype'] and np.all(np.isfinite(a));out[n]=a.copy()
 return out
def metric_F(R):
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F
def comparisons(rows,g):
 complete=[];same=0;different=0
 for row in rows:
  for p in row['contacts']:
   iq=p['iq'];ci,cj=p['cell'];local=p['local'];assert int(g['cell_i'][local])==ci and int(g['cell_j'][local])==cj and local==44*ci+cj and p['point']==iq*3784+local
   R=g['R'][iq].reshape(86,44);F=metric_F(R);hats=[g['hats'][iq,a,0] for a in range(4)];nf=[];mf=[]
   for h in hats:
    factor=np.broadcast_to(h[...,None],(86,44,3)).copy();factor[...,2]=R**2*h;nf.append(factor[ci,cj].copy());mf.append((F*h[...,None,None])[ci,cj].copy())
   actual=dict(R2_64=np.asarray((R**2)[ci,cj]),R3_64=np.asarray((R**3)[ci,cj]),weight64=np.asarray((g['dv'][iq]/g['R'][iq])[local]),native_factors=np.asarray(nf),metric_factors=np.asarray(mf),hats=np.asarray([h[ci,cj] for h in hats]),scatter_factor64=np.asarray(hats[p['row_corner']][ci,cj]))
   point=dict(group=row['group'],point=p['point'],fields={});ACTIVE.clear();ACTIVE.update(completed_points=complete.copy(),current_point=point)
   for name,a in actual.items():
    b=np.asarray(p[name],dtype=np.float64);assert a.shape==b.shape and a.dtype==b.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    av=a.view(np.uint64).ravel();bv=b.view(np.uint64).ravel();eq=av==bv
    field=dict(shape=list(a.shape),actual_bits=[format(int(x),'016x') for x in av],reference_bits=[format(int(x),'016x') for x in bv],equal=eq.tolist(),actual_values=a.tolist(),reference_values=b.tolist())
    point['fields'][name]=field;same+=int(np.count_nonzero(eq));different+=int(np.count_nonzero(~eq))
   complete.append(point)
 assert len(complete)==32 and same+different==5248
 return dict(points=complete,compared_binary64_entries=same+different,same_bits=same,different_bits=different,exact_match=different==0)
def main():
 global np,OWNER
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA,'Guarded geometry component; ROOT only'
 assert not list(BASE.glob(STEM+'_*'))
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(__file__),scope='32 saved contacts geometry bits only');publish('OWNER_START',OWNER)
 try:
  bind(STEM+'.md',PROTOCOL_SHA);rows,record=admission()
  import numpy as np_local
  np=np_local;g=read_geometry(record);result=comparisons(rows,g);publish('COMPARISONS',dict(owner=OWNER,result=result,basis=record,qualification=FLAGS))
  control=dict(name='actual_array_geometry_matches_scalar_frozen_contacts',compared_entries=5248,passed=result['exact_match'],tolerance='exact binary64 bits')
  status='GEOMETRY_BITS_MATCH' if control['passed'] else 'GEOMETRY_BITS_DIFFER'
  recheck();r=publish('RESULT',dict(status=status,owner=OWNER,controls=[control],result=result,basis=record,qualification=FLAGS,source_or_factor_change=False))
  recheck();publish('RECEIPT',dict(status='CLOSED',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),result_sha256=r['sha256'],error_sha256=None,input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),qualification=FLAGS));recheck();print(json.dumps(dict(status=status,pid=OWNER['pid'],result_sha256=r['sha256'],different_bits=result['different_bits'])))
  return 0 if control['passed'] else 3
 except BaseException:
  e=publish('ERROR',dict(status='FAILED',owner=OWNER,traceback=traceback.format_exc(),active=ACTIVE,qualification=FLAGS))
  prior=path(STEM+'_RECEIPT.json')
  publish('ERROR_RECEIPT' if prior.exists() else 'RECEIPT',dict(status='CLOSED_ERROR',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),error_sha256=e['sha256'],result_sha256=None,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),qualification=FLAGS));raise
if __name__=='__main__':raise SystemExit(main())
