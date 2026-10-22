"""0544 records: explicit producer/version and required GQ_NGC input. Exclusive successor records."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import assemble_ntests_c2v003 as V
import assemble_ntests_c2v001 as A
import ngc_ring_tail_ctx_c2v001 as L
if __name__=='__main__':
 manifest=json.loads(Path(sys.argv[1]).read_bytes());V.validate(manifest)
 replay_producers={}
 for name,ref in manifest.items():
  d=A.raw(ref);p=d['producer'];source=Path(p['path'])
  if not source.resolve().is_relative_to(L.HERE) or L.sha(source)!=p['sha256'] or p['version']!=source.stem:raise ValueError('REPLAY_PRODUCER_PIN')
  replay_producers[name]=p
  if name=="CUBE16":
   bp=d["nq_original_base_producer"];bf=d["nq_original_base"]
   if L.sha(bp["path"])!=bp["sha256"] or L.sha(bf["path"])!=bf["sha256"]:raise ValueError("ORIGINAL_NQ_BASE_PROVENANCE")
   replay_producers["NQ_ORIGINAL_BASE"]=bp
 producer={'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem}
 oldbase=A.base
 def base(n):return dict(oldbase(n),producer=producer,replay_producers=replay_producers)
 A.base=base
 oldwrite=L.write
 def write(name,obj):
  if name.endswith('_MANIFEST.json'):
   p=L.CERT/'GQ_CERT_V003_KB128.json';obj['GQ_NGC']={'path':str(p),'sha256':L.sha(p)}
  if obj.get('test')=='NQ':obj['resolution_note']='below one N step (3.3e-8 theta); raw float differences retained'
  return oldwrite(name,obj)
 L.write=write;A.main()
