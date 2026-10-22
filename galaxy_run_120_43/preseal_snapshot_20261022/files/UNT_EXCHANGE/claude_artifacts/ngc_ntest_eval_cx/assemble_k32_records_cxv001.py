"""0546 K32 records; additional EPS/LO/GQ91 coverage is a separate compare admission condition."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import validate_kept_k32_cxv001 as V
import assemble_k32_cxv001 as A
import ngc_ring_tail_ctx_c2v001 as L
if __name__=='__main__':
 m=json.loads(Path(sys.argv[1]).read_bytes());V.validate(m);producers={}
 for name,ref in m.items():
  d=A.raw(ref);p=d['producer'];s=Path(p['path']);assert s.resolve().is_relative_to(L.HERE) and L.sha(s)==p['sha256'] and s.stem==p['version'];producers[name]=p
 producer={'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem};oldbase=A.base
 A.base=lambda n:dict(oldbase(n),producer=producer,replay_producers=producers)
 oldwrite=L.write
 def write(name,obj):
  if name.endswith('_MANIFEST.json'):
   for k,p in [('GQ_NGC',L.HERE/'out/GQ_NGC_91_MS96_V001.json'),('EPS_NGC',L.CERT/'EPS_CERT_V006.json')]:obj[k]={'path':str(p),'sha256':L.sha(p)}
  return oldwrite(name,obj)
 L.write=write;A.main()
