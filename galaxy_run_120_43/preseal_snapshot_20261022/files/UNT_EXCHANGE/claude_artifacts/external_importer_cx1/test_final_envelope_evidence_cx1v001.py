from pathlib import Path
import tempfile,json,hashlib,copy
from final_envelope_evidence_cx1v001 import check,comparator
from snapshot_cx1v001 import Snapshot,Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='final_saved_',dir=b/'inert_fixtures'));tool=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py'
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
m=comparator(tool.read_bytes(),str(tool))
root=json.loads((b/'inert_fixtures/observation_entry_zn2194gv/inert_root_binding.json').read_bytes());pspin=root['envelope']['pinset'];base=json.loads(Path(root['envelope']['start']['path']).read_bytes())
def signed(name,obj):
 obj=copy.deepcopy(obj);obj.pop('body_sha256',None);obj['body_sha256']=m.sha_b(m.canon(obj).encode('ascii'));p=c/name
 with p.open('x') as f:json.dump(obj,f)
 return pin(p),obj
passed=[]
for i,mode in enumerate(['ok','invalid','false_ok','wrong_end_binding','wrong_label','wrong_body','wrong_phase']):
 s=copy.deepcopy(base);e=copy.deepcopy(base);e['label']='end';e['created_epoch_ns']+=1
 if mode in ('invalid','false_ok'):
  # Change saved metadata only; never alter the referenced file.
  e['files'][0]['mtime_ns']+=1
 sp,so=signed(str(i)+'s.json',s);ep,eo=signed(str(i)+'e.json',e);actual=m.compare_saved(so,eo)
 r=dict(schema=m.SCHEMA_COMPARE,phase='L2_DIRECT',pin_set=so['pin_set'],unresolved_pins_not_checked=0,**actual)
 for name,p,o in [('start',sp,so),('end',ep,eo)]:r[name]=dict(path=p['path'],file_sha256=p['sha256'],body_sha256=o['body_sha256'],created_utc=o.get('created_utc'))
 if mode=='false_ok':r.update(verdict='OK',problems=[])
 if mode=='wrong_end_binding':r['end']['file_sha256']='0'*64
 if mode=='wrong_label':
  e['label']='observation';ep,eo=signed(str(i)+'wrong_label.json',e);r['end'].update(path=ep['path'],file_sha256=ep['sha256'],body_sha256=eo['body_sha256'])
 if mode=='wrong_phase':r['phase']='FOREIGN'
 rp,ro=signed(str(i)+'r.json',r)
 if mode=='wrong_body':
  ro['body_sha256']='0'*64;p=c/(str(i)+'badbody.json')
  with p.open('x') as f:json.dump(ro,f)
  rp=pin(p)
 try:
  got=check(Snapshot(),tool_pin=pin(tool),start_pin=sp,end_pin=ep,report_pin=rp,pinset_pin=pspin);ok=True
  assert got['storage_event_kind']==('FINAL_INVALIDATE' if mode=='invalid' else 'FINAL_PASS')
 except Refusal:ok=False
 assert ok==(mode in ('ok','invalid')),mode;passed.append(dict(case=mode,status='PASS'))
with (c/'TEST_REPORT.json').open('x') as f:json.dump(passed,f,indent=2)
print(c/'TEST_REPORT.json')
