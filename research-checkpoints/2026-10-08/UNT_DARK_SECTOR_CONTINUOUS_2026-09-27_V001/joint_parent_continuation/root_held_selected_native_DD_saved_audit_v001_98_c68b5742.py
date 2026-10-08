"""Guarded saved JSON/word audit only; no EFT, FE, operator or solve replay."""
from pathlib import Path
from decimal import Decimal,localcontext
from datetime import datetime,timezone
import argparse,hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001'
AUDIT='READONLY_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_AUDIT_RESULT.json'
AUTHOR_DRAFT=True
TERMINAL=dict(pid=43274,source_sha256='1a1658c897765a265a7788906588b4d41bd02ef5af1a3dc24ebe89f125b720a1',protocol_sha256='8689dc0cbd7c4ce711359d731bb7050f9959d4e960090c50269fdf2db43599c0',result_sha256='0c67ed1ead3fa33832a83eabd7f5527116b33bf645335e305ff5013be5e22c30',receipt_sha256='e0e3add13fa0e153a766b87e446924e83b7e18ce6a137334a6bf458489b95d6d',error_sha256=None)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read(n):return json.loads(path(n).read_text())
def finite_json(v,counts):
 if isinstance(v,float):assert math.isfinite(v);counts['finite_json_numbers']+=1
 elif isinstance(v,dict):
  if 'hi' in v or 'lo' in v:
   assert 'hi' in v and 'lo' in v
   h=float.fromhex(v['hi']);l=float.fromhex(v['lo']);assert math.isfinite(h) and math.isfinite(l)
   counts['finite_word_pairs']+=1
   if 'decimal' in v:
    with localcontext() as c:
     c.prec=100;assert Decimal.from_float(h)+Decimal.from_float(l)==Decimal(v['decimal'])
    counts['exact_word_string_identities']+=1
  for x in v.values():finite_json(x,counts)
 elif isinstance(v,list):
  for x in v:finite_json(x,counts)
def audit():
 assert not AUTHOR_DRAFT and all(TERMINAL[k] is not None for k in ('pid','source_sha256','protocol_sha256','receipt_sha256')),'Unbound or guarded saved auditor'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 required={STEM+'_RECEIPT.json':TERMINAL['receipt_sha256'],'cross_u_selected_native_fe_double_double_v001.py':TERMINAL['source_sha256'],STEM+'.md':TERMINAL['protocol_sha256']}
 required[STEM+('_RESULT.json' if TERMINAL['result_sha256'] else '_ERROR.json')]=TERMINAL['result_sha256'] or TERMINAL['error_sha256']
 for n,h in required.items():assert sha(n)==h,n
 rc=read(STEM+'_RECEIPT.json');owner=rc['owner']
 assert owner['owner']=='root' and owner['pid']==TERMINAL['pid'] and owner['source_sha256']==TERMINAL['source_sha256']
 assert rc['closed']>owner['started'] and rc['result_sha256']==TERMINAL['result_sha256'] and rc['error_sha256']==TERMINAL['error_sha256']
 assert rc['status']==('CLOSED' if TERMINAL['result_sha256'] else 'CLOSED_ERROR') and all(v is False for v in rc['qualification'].values())
 bound={str(path(n).resolve()):h for n,h in required.items()}
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in bound or bound[key]==h;assert sha(n)==h,n;bound[key]=h
 own={path(n).name:h for n,h in rc['output_sha256'].items()};own[STEM+'_RECEIPT.json']=TERMINAL['receipt_sha256']
 actual={q.name:sha(q) for q in BASE.glob(STEM+'_*') if q.is_file()}
 assert all(actual[n]==h for n,h in own.items())
 partial={n:h for n,h in actual.items() if n not in own}
 if rc['status']=='CLOSED':assert not partial and len(actual)==10
 documents={n:read(n) for n in own};counts=dict(finite_json_numbers=0,finite_word_pairs=0,exact_word_string_identities=0,accuracy_controls=0,exact_fixture_controls=0)
 for d in documents.values():finite_json(d,counts)
 terminal=documents[STEM+('_RESULT.json' if TERMINAL['result_sha256'] else '_ERROR.json')]
 assert terminal['owner']==owner and terminal['qualification']==rc['qualification']
 controls=terminal['controls'];assert len(controls)<=15
 with localcontext() as c:
  c.prec=100
  for q in controls:
   a=Decimal(q['actual']);e=Decimal(q['expected']);assert a.is_finite() and e.is_finite()
   if q['tolerance']=='exact synthetic identity':assert q['passed']==(a==e);counts['exact_fixture_controls']+=1
   else:
    assert e!=0 and Decimal(q['tolerance'])==Decimal('1e-10')
    ratio=abs(a-e)/abs(e);assert ratio==Decimal(q['relative_error']) and q['passed']==(ratio<=Decimal('1e-10'))
    counts['accuracy_controls']+=1
 rows=[]
 if rc['status']=='CLOSED':
  assert terminal['status']=='BOUNDED_DOUBLE_DOUBLE_COMPONENT_COMPLETE' and len(controls)==15 and all(q['passed'] for q in controls)
  assert counts['accuracy_controls']==8 and counts['exact_fixture_controls']==7 and terminal['full_row_admission'] is False
  assert terminal['new_operator_solve'] is terminal['source_or_coefficient_change'] is terminal['original_rhs_changed'] is terminal['original_precision_witness_adoption'] is False
  inp=documents[STEM+'_INPUT.json'];assert len(inp['rows'])==len(terminal['rows'])==2 and sum(len(q['contacts']) for q in inp['rows'])==32
  assert inp['ancestry']['original_nonadmission']['parent_nonadmission_preserved'] is True
  fixture=documents[STEM+'_FIXTURE.json'];assert fixture['controls']==controls[:7]
  for row,raw in zip(terminal['rows'],inp['rows']):
   g=raw['group'];assert g in (10,14) and row['selection']=={k:v for k,v in raw.items() if k!='contacts'}
   component=documents[STEM+'_ROW_%d_COMPONENT.json'%g];certificate=documents[STEM+'_ROW_%d_CERTIFICATE.json'%g]
   assert component['owner']==certificate['owner']==owner and row['component']['sha256']==own[row['component']['file']]
   assert component['result']==row['result'] and certificate['row']==row and certificate['controls']==controls[:len(certificate['controls'])]
   assert row['reference100']==inp['references'][str(g)] and [p['point'] for p in component['points']]==[p['point'] for p in raw['contacts']]
   reference=row['reference100'];result=row['result'];errors={}
   with localcontext() as c:
    c.prec=100
    for label,field,ref in (('action','action','action'),('original_residual','original_rhs_residual','original_rhs_residual'),('centered_action','centered_action','action'),('centered_original_residual','centered_original_residual','original_rhs_residual')):
     a=Decimal(result[field]['decimal']);e=Decimal(reference[ref]);assert e!=0
     error=abs(a-e)/abs(e);assert error<=Decimal('1e-10');errors[label]=str(error)
     expected_name='row%d_%s_accuracy'%(g,label)
     q=next(q for q in controls if q['name']==expected_name);assert Decimal(q['actual'])==a and Decimal(q['expected'])==e and Decimal(q['relative_error'])==error
   rows.append(dict(group=g,selected_original_residual=result['original_rhs_residual']['decimal'],reference100_original_residual=reference['original_rhs_residual'],relative_errors=errors))
 for n,h in bound.items():assert sha(n)==h,n
 assert sha(__file__)==SOURCE_SHA
 return dict(status='SAVED_DD_COMPONENT_AUDIT_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=SOURCE_SHA,parent_terminal=TERMINAL,parent_status=rc['status'],actual_JSON_files=len(actual),sealed_JSON_files=len(own),partial_files=partial,controls=len(controls),counts=counts,rows=rows,qualification=rc['qualification'],selected_rows_only=True,full_vector_admission=False,EFT_FE_operator_or_solve_replayed=False)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args();assert args.root_run
 SOURCE_SHA=sha(__file__);report=audit();raw=(json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with path(AUDIT).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path(AUDIT).chmod(0o444);assert path(AUDIT).read_bytes()==raw
 print(json.dumps(dict(status=report['status'],pid=report['pid'],sha256=sha(AUDIT),controls=report['controls'],rows=report['rows'])))
