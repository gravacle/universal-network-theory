"""Guarded future saved-JSON/string audit; no A, field, array or polynomial replay."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
PARENT='CROSS_U_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001'
STEM='READONLY_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001_AUDIT'
AUTHOR_DRAFT=True
TERMINAL={'pid': 42546, 'source_sha256': '30d0cc625dddc09be6e845bde409e1d244253073e4803f253b5fdab29e1e637e', 'protocol_sha256': '8f8343fde9c0ca6df436bb4e9fb5cd69db80227729fee669ba060a46e21d7c6f', 'result_sha256': '848c0411bab21dcdc8e4e2518cae444fd96566e264fa554ad25c9079955b4f5e', 'error_sha256': None, 'receipt_sha256': 'fc9e621b17357fb23a79482e3b41ab126d5c199c6eff3492c3ec00defd281cec'}
TOL=Decimal('2e-11');FLOOR=Decimal('1e-30');COMPARISONS=0;MAX_RATIO=Decimal(0)
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load(n):return json.loads(path(n).read_text())
def D(v):
 x=Decimal.from_float(v) if type(v) is float else Decimal(v);assert x.is_finite();return x
def same(a,b,e,label):
 global COMPARISONS,MAX_RATIO
 a,b,e=D(a),D(b),D(e);assert e>=0;ratio=abs(a-b)/max(e,FLOOR);COMPARISONS+=1;MAX_RATIO=max(MAX_RATIO,ratio);assert ratio<=TOL,(label,str(ratio))
def finite(v):
 if isinstance(v,dict):
  for a in v.values():finite(a)
 elif isinstance(v,list):
  for a in v:finite(a)
 elif type(v) is float:assert math.isfinite(v)
def control(c):
 a,b,e=D(c['actual']),D(c['expected']),D(c['envelope']);assert e>=0;ratio=abs(a-b)/max(e,FLOOR)
 assert abs(ratio-D(c['error']))<=Decimal('1e-60')*max(Decimal(1),abs(ratio)),'70/100-digit descriptor rounding only'
 assert D(c['tolerance'])==TOL and c['passed']==(ratio<=TOL)
def audit_row(raw,result):
 out=[]
 assert len(raw['contacts'])==16 and len({p['point'] for p in raw['contacts']})==16
 for label in ('decimal70','decimal100'):
  a=result[label];assert a['precision']==(70 if label=='decimal70' else 100)
  assert [p['point'] for p in a['points']]==[p['point'] for p in raw['contacts']]
  action=centered=cs=ps=Decimal(0)
  for p,s in zip(raw['contacts'],a['points']):
   # Contract ONLY stored signed mode terms and saved centered momentum, not D/L/B or nodal rates.
   q=D(p['weight64'])*D(p['scatter_factor64']);terms=s['mode_terms'];action+=q*sum((D(terms[n]) for n in ('D_vz','D_Lvu','Bz_k')),Decimal(0))
   centered+=q*(D(s['point_centered_momentum'][0])-D(p['cn'][0]));cs+=q*D(p['cn'][0]);ps+=q*D(p['pstar'][0])
  e=D(a['operation_envelope']);rhs=D(raw['original_rhs']);target=D(raw['actual_Pn_target']);saved=D(raw['original_float_residual'])
  same(action,a['action'],e,label+' stored-term scatter');same(centered,a['centered_action'],e,label+' stored centered scatter')
  same(a['centered_action'],a['action'],e,label+' direct-centered identity')
  r=D(a['original_rhs_residual']);same(r,rhs-D(a['action']),e+abs(rhs),label+' frozen RHS residual')
  same(a['scaled_original_residual'],r/D(raw['scale']),e/abs(D(raw['scale'])),label+' fixed scale')
  epsilon=D(a['saved_residual_minus_high_precision']);same(epsilon,saved-r,e+abs(saved),label+' epsilon sign')
  same(a['actual_Pn_residual'],target-cs-D(a['action']),e+abs(target),label+' point-cn diagnostic')
  same(a['frozen_rhs_defect'],rhs-(target-cs),e+abs(rhs)+abs(target),label+' retained RHS translation')
  same(a['target_scatter_defect'],target-ps,e+abs(target),label+' retained target scatter')
  out.append(dict(precision=a['precision'],saved_residual=str(saved),high_precision_residual=str(r),epsilon=str(epsilon),abs_epsilon_over_saved=None if not saved else str(abs(epsilon/saved)),abs_remaining_over_saved=None if not saved else str(abs(r/saved)),abs_epsilon_over_remaining=None if not r else str(abs(epsilon/r)),actual_Pn_residual=str(a['actual_Pn_residual']),point_cn_only=True))
 same(result['decimal70']['action'],result['decimal100']['action'],result['decimal100']['operation_envelope'],'70/100 agreement')
 return dict(group=raw['group'],mode_index=raw['mode_index'],node=raw['node'],contacts=16,precision=out,full_row_or_vector_admission=False)
def publish(tag,obj):
 n=STEM+'_'+tag+'.json';b=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with path(n).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 path(n).chmod(0o444);assert path(n).read_bytes()==b;return sha(n)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root-audit',action='store_true');args=ap.parse_args()
 t=TERMINAL;assert args.root_audit and not AUTHOR_DRAFT,'Future ROOT-released saved-only auditor'
 assert all(t[n] is not None for n in ('pid','source_sha256','protocol_sha256','receipt_sha256')) and (t['result_sha256'] is None)!=(t['error_sha256'] is None),'Natural CLOSED terminal bindings mandatory before I/O'
 assert not list(BASE.glob(STEM+'_*'));selfhash=sha(__file__);rcn=PARENT+'_RECEIPT.json';assert sha(rcn)==t['receipt_sha256'];rc=load(rcn)
 assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['owner']['owner']=='root' and rc['owner']['pid']==t['pid'] and rc['closed']>rc['owner']['started']
 assert rc['owner']['source_sha256']==t['source_sha256'] and sha('cross_u_selected_native_fe_precision_witness_v001.py')==t['source_sha256'] and sha(PARENT+'.md')==t['protocol_sha256']
 assert all(v is False for v in rc['qualification'].values())
 n=PARENT+('_RESULT.json' if rc['status']=='CLOSED' else '_ERROR.json');h=t['result_sha256'] if rc['status']=='CLOSED' else t['error_sha256'];assert sha(n)==h and rc['result_sha256' if rc['status']=='CLOSED' else 'error_sha256']==h;doc=load(n)
 assert doc['owner']==rc['owner'];files=[]
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for name,digest in mapping.items():assert sha(name)==digest
 for name in rc['output_sha256']:
  p=path(name)
  if p.suffix=='.json' and p.name.startswith(PARENT+'_'):
   a=load(name);finite(a);files.append(p.name)
   if 'controls' in a:
    with localcontext() as ctx:
     ctx.prec=110
     for c in a['controls']:control(c)
 try:
  reports=[]
  with localcontext() as ctx:
   ctx.prec=110
   if rc['status']=='CLOSED':
    assert doc['status']=='BOUNDED_PRECISION_WITNESS_COMPLETE' and len(doc['controls'])==16 and len(doc['rows'])==2 and doc['full_row_admission'] is False and doc['new_operator_solve'] is False
    raw=load(doc['point_operands']['file']);assert sha(doc['point_operands']['file'])==doc['point_operands']['sha256']
    assert [(a['group'],a['component'],*a['node']) for a in raw['rows']]==[(10,0,82,39),(14,0,84,37)]
    for r,w in zip(raw['rows'],doc['rows']):
     assert w['selection']=={k:r[k] for k in r if k!='contacts'};reports.append(audit_row(r,w))
     for precision in (70,100):
      snap=PARENT+'_ROW_%d_PRECISION%d.json'%(r['group'],precision);a=load(snap);assert a['result']==w['decimal%d'%precision] and a['selection']==[r['group'],r['component'],r['node']]
    assert doc['ancestry']['parent_nonadmission_preserved'] is True and all(v is False for v in doc['qualification'].values())
   else:assert doc['status']=='FAILED'
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for name,digest in mapping.items():assert sha(name)==digest
  assert sha(__file__)==selfhash and sha(rcn)==t['receipt_sha256'] and sha(n)==h
  result=dict(status='SAVED_PRECISION_WITNESS_AUDIT_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),parent_terminal_status=rc['status'],parent_result_sha256=t['result_sha256'],parent_error_sha256=t['error_sha256'],parent_receipt_sha256=t['receipt_sha256'],source_sha256=selfhash,comparisons=COMPARISONS,max_scaled_identity_gap=str(MAX_RATIO),controls=len(doc.get('controls',[])),preserved_json_files=files,rows=reports,qualification=rc['qualification'],old_arrays_or_A_replayed=False,polynomial_replay=False,selected_rows_only=True)
  print(json.dumps(dict(pid=os.getpid(),status=result['status'],sha256=publish('RESULT',result))))
 except BaseException:
  publish('ERROR',dict(status='AUDITOR_FAILURE',pid=os.getpid(),source_sha256=selfhash,parent_receipt_sha256=t['receipt_sha256'],traceback=traceback.format_exc()));raise
if __name__=='__main__':main()
