"""Finish only when every production-K32 replay and root91 certificate exists. No launches.
Exclusive writes; run once. Missing dependencies refuse before any output creation.
"""
import hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).parent
if __name__=='__main__':
 names={'N0':'N0_REPLAY_V001.json','CUBE16':'CUBE16_STORED_V001.json','CUBE32':'CUBE32_STORED_V001.json','CUBE64':'CUBE64_STORED_V001.json','NQ_FINE':'NQ32_FINE_STORED_V001.json','SPHERE32':'SPHERE32_V001.json','C1PRIME':'C1PRIME_K32_EVIDENCE_V001.json'}
 cert=R.parent/'tail_scheme_impl_c2/certificates_ngc_k32/gates'
 paths=[R/'out'/v for v in names.values()]+[R/'out/GQ_NGC_91_MS96_V001.json',cert/'EPS_CERT_NGC91_V001.json',cert/'LO_NGC_K32_CERT_V001.json']
 absent=[str(p) for p in paths if not p.is_file()]
 if absent:raise SystemExit('DEPENDENCIES_PENDING: '+json.dumps(absent))
 manifest={k:{'path':str(R/'out'/v),'sha256':hashlib.sha256((R/'out'/v).read_bytes()).hexdigest()} for k,v in names.items()}
 p=R/'out/K32_RAW_COMPLETE_V001.json'
 with p.open('x') as f:json.dump(manifest,f,indent=1)
 sys.argv=['annotate',str(p),'out/K32_ANNOTATED_COMPLETE_V001'];runpy.run_path(str(R/'annotate_k32_cxv001.py'),run_name='__main__')
 sys.argv=['assemble',str(R/'out/K32_ANNOTATED_COMPLETE_V001_MANIFEST.json'),'out/K32_RECORDS_COMPLETE_V001'];runpy.run_path(str(R/'assemble_k32_records_cxv003.py'),run_name='__main__')
 sys.argv=['compare',str(R/'out/K32_RECORDS_COMPLETE_V001_MANIFEST.json'),str(R/'out/K32_COMPARE_COMPLETE_V001.json')];runpy.run_path(str(R/'ntests_compare_k32_cxv003.py'),run_name='__main__')
