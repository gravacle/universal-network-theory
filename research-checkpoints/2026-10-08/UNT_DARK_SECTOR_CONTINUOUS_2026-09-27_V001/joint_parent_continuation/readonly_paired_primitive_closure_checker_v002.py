"""Guarded saved-only pilot closure: controls, paired word identities and norms.
No feature, EFT, chart, FE scatter, operator, kinetic, solve or history replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
TERMINAL=dict(pid=50104,source_sha256='b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',protocol_sha256='0ccd71e96ff40c8105256fd9cce17b68ff06ad0292a726bd1ecac458d8bff30a',result_sha256='7289a181e37a8f3277dfc7a587f09bf9078e1d20381eb0c0c371aac2511203be',receipt_sha256='293295534b3c32ea152641ee4bd54b4cf224a171e3de9e14f2833759787eadaa')
PARENT='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002'
OUTPUT='READONLY_PAIRED_PRIMITIVE_CLOSURE_V002_RESULT.json'
TOL=2e-11;FLOOR=1e-30;LINEAR_TOL=1e-10
np=None;IDENTITIES=[]
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def metadata(n,h):
 assert sha(n)==h,n;return json.loads(path(n).read_text())
def record(ref,receipt):
 assert receipt['output_sha256'][ref['file']]==ref['sha256'] and receipt['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 assert sha(ref['file'])==ref['sha256'];c=metadata(ref['commit_file'],ref['commit_sha256']);assert c=={k:v for k,v in ref.items() if k not in ('commit_file','commit_sha256')}
 assert c['metadata']['owner']==receipt['owner'];return ref
def read(rec,names):
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata']
  out={}
  for n in names:
   a=f[n].copy();md=rec['metadata']['schema'][n];assert list(a.shape)==md['shape'] and str(a.dtype)==md['dtype'] and md['finite'] is True and np.all(np.isfinite(a)),n;out[n]=a
  return out
def identity(label,a,b,e):
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 err=float(np.max(abs(a-b)/np.maximum(e,FLOOR),initial=0));IDENTITIES.append(dict(name=label,error=err,tolerance=TOL));assert err<=TOL,(label,err)
def control(rec,row):
 prefix='control_%03d_%s_'%(row['ordinal'],row['name']);x=read(rec,[prefix+n for n in ('actual','expected','envelope')]);a,b,e=(x[prefix+n] for n in ('actual','expected','envelope'))
 err=float(np.max(abs(a-b)/np.maximum(e,FLOOR),initial=0));assert row['tolerance']==TOL and row['passed'] is True and err<=TOL and abs(err-row['error'])<=TOL*max(abs(err),abs(row['error']),FLOOR),(row['name'],err,row['error']);return err
def norm_ratios(x,reference,scale):
 assert np.all(scale>0);raw=float(np.linalg.norm(x));den=float(np.linalg.norm(reference));white=float(np.linalg.norm(x/scale));wd=float(np.linalg.norm(reference/scale));assert den>0 and wd>0
 out=np.array((raw/den,white/wd));assert np.all(np.isfinite(out));return out
def family(rec,name):
 prefixes=('primitive_momentum','earned_achieved_momentum','primitive_minus_earned_bridge','original_affine_residual','actual_target_residual','frozen_rhs_defect','identity_gap')
 names=[name+'_'+p+'_'+w for p in prefixes for w in ('hi','lo')]+[name+'_'+p for p in ('original_target','rounded_offset','positive_congruence','original_rhs')];a=read(rec,names)
 words={p:tuple(a[name+'_'+p+'_'+w] for w in ('hi','lo')) for p in prefixes};v={p:x[0]+x[1] for p,x in words.items()}
 target,offset,scale,rhs=(a[name+'_'+p] for p in ('original_target','rounded_offset','positive_congruence','original_rhs'))
 positive=abs(target)+abs(offset)+abs(rhs)
 for x in words.values():positive=positive+abs(x[0])+abs(x[1])
 identity(name+'_bridge',v['primitive_minus_earned_bridge'],v['primitive_momentum']-v['earned_achieved_momentum'],positive)
 identity(name+'_original_affine',v['original_affine_residual'],rhs-v['primitive_momentum']+offset,positive)
 identity(name+'_actual_target',v['actual_target_residual'],target-v['primitive_momentum'],positive)
 identity(name+'_rhs_defect',v['frozen_rhs_defect'],rhs-target+offset,positive)
 identity(name+'_bridge_identity_gap',v['identity_gap'],v['actual_target_residual']-(v['original_affine_residual']-v['frozen_rhs_defect']),positive)
 return [norm_ratios(v['original_affine_residual'],rhs,scale),norm_ratios(v['actual_target_residual'],target,scale)],[norm_ratios(v['primitive_minus_earned_bridge'],rhs,scale),norm_ratios(v['primitive_minus_earned_bridge'],target,scale)]
def main():
 global np
 if AUTHOR_DRAFT:raise SystemExit('Guarded saved-only checker; root review/release required.')
 assert all(v is not None for v in TERMINAL.values()),'Natural CLOSED terminal required before I/O'
 assert not path(OUTPUT).exists(),'Preserve prior reader results'
 import numpy as numpy
 np=numpy
 t=TERMINAL;result=metadata(PARENT+'_RESULT.json',t['result_sha256']);rc=metadata(PARENT+'_RECEIPT.json',t['receipt_sha256'])
 assert sha('cross_u_paired_current_primitive_momentum_readout_v002.py')==t['source_sha256'] and sha(PARENT+'.md')==t['protocol_sha256']
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==t['result_sha256'] and rc['owner']==result['owner'] and result['owner']['pid']==t['pid'] and result['owner']['source_sha256']==t['source_sha256']
 rows=result['controls'];records=result['checkpoints'];case=result['case'];assert len(rows)==18 and len(records)==7 and all(v is False for v in result['qualification'].values()) and rc['qualification']==result['qualification']
 assert [r['ordinal'] for r in rows]==list(range(18));assert len(case['columns'])==4 and case['readout']==records[-1] and case['columns']==records[2:6]
 for ref in records:record(ref,rc)
 assert records[0]['metadata']['kind']=='unchanged_configuration_and_earned_paired_rate_references' and records[1]['metadata']['kind']=='authenticated_unchanged_E_F_geometry_reused_without_operator_replay'
 errors=[]
 for iq,ref in enumerate(case['columns']):
  md=ref['metadata'];assert md['column']==iq and md['controls']==rows[4*iq:4*iq+4] and md['rate_word_collapse_adopted'] is False and md['source_configuration_changed'] is False and md['full_normal_coefficients_computed'] is False
  for r in md['controls']:errors.append(control(ref,r))
 readout=case['readout'];assert readout['metadata']['controls']==rows[16:18] and readout['metadata']['offsets_targets_or_state_refitted'] is False and readout['metadata']['primitive_and_frozen_operator_admission_distinct'] is True
 for r in rows[16:18]:errors.append(control(readout,r))
 r1,b1=family(readout,'native');r2,b2=family(readout,'metric');ratios=np.stack(r1+r2);bridge=np.stack(b1+b2);saved=read(readout,('original_affine_and_actual_target_ratios','bridge_rhs_and_target_ratios'))
 for n,actual in (('original_affine_and_actual_target_ratios',ratios),('bridge_rhs_and_target_ratios',bridge)):
  expected=saved[n];identity(n,actual,expected,np.maximum(abs(actual),abs(expected)));assert np.array_equal(expected,np.asarray(case[n]))
 admitted=bool(np.all(ratios<=LINEAR_TOL));assert admitted==case['canonical_primitive_readout_admitted']==readout['metadata']['canonical_primitive_readout_admitted']
 assert result['status']==('CURRENT_PRIMITIVE_CANONICAL_READOUT_ADMITTED' if admitted else 'CURRENT_PRIMITIVE_CANONICAL_READOUT_MISMATCH') and case['frozen_canonical_admission_preserved'] is True and case['physical_adoption'] is False
 for ref in records:assert sha(ref['file'])==ref['sha256'] and sha(ref['commit_file'])==ref['commit_sha256']
 assert sha(PARENT+'_RESULT.json')==t['result_sha256'] and sha(PARENT+'_RECEIPT.json')==t['receipt_sha256']
 assert {x.name for x in BASE.glob(PARENT+'_*.npz')}=={r['file'] for r in records}
 assert {x.name for x in BASE.glob(PARENT+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
 out=dict(status='SAVED_PAIRED_PRIMITIVE_CLOSURE_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=sha(__file__),parent_terminal=t,parent_status=result['status'],canonical_primitive_readout_admitted=admitted,original_affine_and_actual_target_ratios=ratios.tolist(),bridge_rhs_and_target_ratios=bridge.tolist(),controls=18,committed_pairs=7,identities=IDENTITIES,maximum_control_error=max(errors),qualification=result['qualification'],old_input_maps_or_feature_EFT_scatter_operator_solver_replayed=False)
 raw=(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with path(OUTPUT).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path(OUTPUT).chmod(0o444);assert path(OUTPUT).read_bytes()==raw
 for ref in records:assert sha(ref['file'])==ref['sha256'] and sha(ref['commit_file'])==ref['commit_sha256']
 assert sha(PARENT+'_RESULT.json')==t['result_sha256'] and sha(PARENT+'_RECEIPT.json')==t['receipt_sha256'];print('PASS',os.getpid(),sha(OUTPUT),18,len(IDENTITIES))
if __name__=='__main__':main()
