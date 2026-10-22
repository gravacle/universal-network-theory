"""D022 real envelope/runtime/register callbacks on preserved inert records."""
import ast,copy,fcntl,hashlib,json,os,sys,tempfile,types
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from stateless_phase_cx1v002 import make_phase_use
from final_envelope_evidence_cx1v001 import comparator
from snapshot_cx1v001 import Refusal
root=Path(__file__).parent;case=Path(tempfile.mkdtemp(prefix='stateless_phase_',dir=root/'inert_fixtures'))
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def put(p,obj):
 with p.open('x') as f:json.dump(obj,f,sort_keys=True);f.write('\n')
 return pin(p)
base=json.loads((root/'inert_fixtures/observation_entry_zn2194gv/inert_root_binding.json').read_bytes())
reg=json.loads(Path(base['register']['path']).read_bytes());selected=reg['entries'][0]
original_start=json.loads(Path(base['envelope']['start']['path']).read_bytes())
tool=Path(base['envelope']['tool']['path']);m=comparator(tool.read_bytes(),str(tool))
# Compile the tool's exact native writer and fsync helper, never a handwritten serialization.
writer_tree=ast.parse(tool.read_bytes())
writer_nodes=[n for n in writer_tree.body if isinstance(n,ast.FunctionDef) and n.name in ('write_signed','_fsync_dir')]
assert len(writer_nodes)==2
m.os=os
exec(compile(ast.Module(body=writer_nodes,type_ignores=[]),str(tool),'exec'),m.__dict__)
def signed(p,obj):
 m.write_signed(str(p),obj)
 return pin(p),json.loads(p.read_bytes())
work=case/'WORK';work.mkdir();lp=work/'ORCHESTRATOR.lock';fd=os.open(lp,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
lock=types.SimpleNamespace(held=True,_fd=fd,path=lp);ctx=types.SimpleNamespace(work_dir=work,**base['context'])
entry=dict(key=selected['key'],provenance=dict(execution_origin='DIRECT_EXTERNAL',call_dir=selected['call_root'],external_admission=dict(config_sha256=ctx.config_sha256,cache_id=ctx.cache_id,candidate=dict(key=selected['key'],spec=selected['spec'],row=selected['row'],call_dir=selected['call_root']))))
checks=[]
try:
 for mode in ['open','final_pass','invalid','end_without_report','malformed_report','foreign_report','report_without_end','two_ends','wrong_row','wrong_start_pin','unheld_lock','orphan_sidecar','bad_sidecar','unknown_file']:
  d=case/mode;d.mkdir()
  ps=json.loads(Path(base['envelope']['pinset']['path']).read_bytes())
  pp,po=signed(d/'PINSET.json',ps)
  start=copy.deepcopy(original_start);start['pin_set']=dict(path=pp['path'],file_sha256=pp['sha256'],body_sha256=po['body_sha256'])
  sp,so=signed(d/'START.json',start)
  rb=copy.deepcopy(base);rb['schema']='CX1_IMPORTER_ROOT_BINDING_V002';rb['envelope']['start']=sp;rb['envelope']['pinset']=pp
  rb['direct_plan']=put(case/(mode+'_synthetic_direct_plan.json'),{'synthetic':True})
  if mode=='wrong_start_pin':rb['envelope']['start']['sha256']='0'*64
  rootpin=put(case/(mode+'_root_binding.json'),rb)
  if mode in ('final_pass','invalid','end_without_report','malformed_report','foreign_report','two_ends'):
   end=copy.deepcopy(so);end['label']='end';end['created_epoch_ns']+=1
   if mode=='invalid':end['files'][0]['mtime_ns']+=1
   ep,eo=signed(d/'END.json',end)
   if mode=='two_ends':signed(d/'OTHER_END.json',end)
   if mode not in ('end_without_report','two_ends'):
    result=m.compare_saved(so,eo)
    report=dict(schema=m.SCHEMA_COMPARE,phase='L2_DIRECT',pin_set=so['pin_set'],unresolved_pins_not_checked=0,**result)
    for label,p,obj in [('start',sp,so),('end',ep,eo)]:report[label]=dict(path=p['path'],file_sha256=p['sha256'],body_sha256=obj['body_sha256'],created_utc=obj.get('created_utc'))
    if mode=='foreign_report':report['start']['file_sha256']='0'*64
    if mode=='malformed_report':
     with (d/'COMPARE.json').open('x') as f:f.write('{')
    else:signed(d/'COMPARE.json',report)
  if mode=='orphan_sidecar':
   with (d/'MISSING.json.sha256').open('x') as f:f.write('0'*64+'  MISSING.json\n')
  if mode=='bad_sidecar':
   with (d/'EXTRA.json').open('x') as f:f.write('{}')
   with (d/'EXTRA.json.sha256').open('x') as f:f.write('0'*64+'  EXTRA.json\n')
  if mode=='unknown_file':
   with (d/'UNEXPECTED.txt').open('x') as f:f.write('not JSON')
  if mode=='report_without_end':put(d/'COMPARE.json',{'schema':m.SCHEMA_COMPARE})
  use=make_phase_use(root_binding_pin=rootpin,expected_policy=rb['policy'],expected_entry=rb['entry'],held_lock=lambda ctx:lock)
  sample=copy.deepcopy(entry)
  if mode=='wrong_row':sample['provenance']['external_admission']['candidate']['row']=-1
  if mode=='unheld_lock':lock.held=False
  try:
   outcome=use(ctx,sample);ok=True
  except (Refusal,ValueError,OSError) as exc:outcome=str(exc);ok=False
  finally:lock.held=True
  assert ok==(mode in ('open','final_pass')),(mode,outcome)
  if ok:assert outcome==('PROVISIONAL_ENVELOPE' if mode=='open' else 'ENVELOPE_FINAL_PASS')
  checks.append(dict(case=mode,passed=True,result=outcome))
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
report={'status':'PASS','tested':checks,'scope':__doc__,'test':pin(Path(__file__)),'callback':pin(root/'stateless_phase_cx1v002.py'),'untested':['installed campaign cache with callback','root final END publication','root remedy for prior consumption']}
print(put(case/'STATELESS_REPORT.json',report))
