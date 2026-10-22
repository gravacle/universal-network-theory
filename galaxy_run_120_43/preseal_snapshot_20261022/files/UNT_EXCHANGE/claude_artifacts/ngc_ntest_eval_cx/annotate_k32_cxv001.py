"""0546 raw K32 replay provenance successors; exclusive writes."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v005 as L
mapping={'N0':'run_ntests_c2v001.py','CUBE16':'replay_stored_kept_cxv001.py','CUBE32':'replay_stored_kept_cxv001.py','CUBE64':'replay_stored_kept_cxv002.py','NQ_FINE':'replay_stored_kept_cxv002.py','SPHERE32':'run_ntests_c2v006.py','C1PRIME':'c1prime_evidence_cxv002.py'}
if __name__=='__main__':
 m=json.loads(Path(sys.argv[1]).read_bytes());prefix=sys.argv[2];out={}
 for name,ref in m.items():
  p=Path(ref['path']);assert p.resolve().is_relative_to(L.HERE) and L.sha(p)==ref['sha256']
  d=json.loads(p.read_bytes());s=L.HERE/mapping[name]
  d.update(producer={'path':str(s),'sha256':L.sha(s),'version':s.stem},original_replay=ref)
  if 'tail_record' in d:d['quadrature_node_counts_rule']='derived by module, not fixed declared-input counts (0544 F3)'
  out[name]=L.write(prefix+'_'+name+'.json',d)
 print(L.write(prefix+'_MANIFEST.json',out))
