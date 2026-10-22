"""0544 provenance successors. RAW_MANIFEST OUTPUT_PREFIX; never modifies existing replay bytes."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v001 as L
mapping={'N0':'run_ntests_c2v001.py','NQ_FINE':'run_ntests_c2v005.py','SPHERE16':'run_ntests_c2v005.py','CUBE8':'replay_stored_kept_cxv001.py','CUBE16':'replay_stored_kept_cxv001.py','CUBE32':'replay_stored_kept_cxv001.py','C1PRIME':'c1prime_evidence_cxv001.py'}
if __name__=='__main__':
 manifest=json.loads(Path(sys.argv[1]).read_bytes());prefix=sys.argv[2];out={}
 for name,ref in manifest.items():
  p=Path(ref['path'])
  if not p.resolve().is_relative_to(L.HERE) or L.sha(p)!=ref['sha256']:raise ValueError('RAW_PIN_OR_PATH')
  d=json.loads(p.read_bytes());source=mapping[name]
  if name=='CUBE16' and p.name=='NQ_BASE_V001.json':source='run_ntests_c2v001.py'
  producer=L.HERE/source
  d['producer']={'path':str(producer),'sha256':L.sha(producer),'version':producer.stem}
  d['original_replay']=ref
  if name=="CUBE16":
   bp=L.HERE/"out/NQ_BASE_V001.json";bs=L.HERE/"run_ntests_c2v001.py"
   d["nq_original_base"]={"path":str(bp),"sha256":L.sha(bp)}
   d["nq_original_base_producer"]={"path":str(bs),"sha256":L.sha(bs),"version":bs.stem}
  if "tail_record" in d:d["quadrature_node_counts_rule"]="derived by module, not fixed declared-input counts (0544 F3)"
  if name=='NQ_FINE':d['resolution_note']='below one N step (3.3e-8 theta) for base/fine difference; raw floats retained'
  out[name]=L.write(prefix+'_'+name+'.json',d)
 print(L.write(prefix+'_MANIFEST.json',out))
