"""0539 evidence validation: literal common stored kept packet, and rederived C1prime references."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import validate_k32_cxv001 as V
import assemble_k32_cxv001 as A
import c1prime_evidence_cxv001 as C
import ngc_ring_tail_ctx_c2v001 as L

def validate(manifest):
 V.validate(manifest)
 if 'C1PRIME' in manifest:
  c=A.raw(manifest['C1PRIME']);expected=C.calculate(A.raw(manifest['CUBE32']),c['reference_inputs'])
  for k,v in expected.items():
   if c.get(k)!=v:raise ValueError('C1PRIME_REFERENCE_STATISTIC '+k)
 if all(k in manifest for k in ('CUBE16','CUBE32','CUBE64')):
  raws=[A.raw(manifest[k]) for k in ('CUBE16','CUBE32','CUBE64')];refs=[x.get('stored_kept_reference') for x in raws]
  if refs[0] is None or refs!=[refs[0]]*3:raise ValueError('N3_COMMON_STORED_KEPT_REQUIRED')
  p=Path(refs[0]['path'])
  if not p.resolve().is_relative_to(L.HERE):raise ValueError('KEPT_PATH_SCOPE')
  if L.sha(p)!=refs[0]['sha256']:raise ValueError('KEPT_HASH')
  q=json.loads(p.read_bytes())
  if q['operator_sha256']!=L.OP_SHA or q['N0_all_nine_heights_bitwise'] is not True:raise ValueError('KEPT_CUSTODY')
  for x in raws:
   if x.get('arithmetic')!='1.+(n_kept+t)' or len(x.get('parent_arithmetic_checks',[]))!=6 or not all(y['bitwise_equal'] for y in x['parent_arithmetic_checks']):raise ValueError('N3_PARENT_ARITHMETIC')
  if raws[0].get('base_replay_bitwise_equal') is not True:raise ValueError('N3_BASE_IDENTITY')
 return True
if __name__=='__main__':validate(json.loads(Path(sys.argv[1]).read_bytes()));A.main()
