"""0539: store exact kept delta_n once for literal reuse by all N3 tail cases. No exp(logN)."""
import json,math,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v001 as L
import ngc_ring_tail_ctx_c2v003 as P
ctx,cols=L.ctx_with_tail(2.,'cube',False)
old=json.loads((L.HERE/'out/N0_REPLAY_V001.json').read_bytes())['rows'];rows=[]
for o in range(100):
 vals=[]
 for j in range(32):
  c=cols[32*o+j];v=[P.TailCtx.kept_delta_n(ctx,c['R_m'],c['phi'],z*L.KPC) for z in L.ZK]
  assert np.array([math.log(1.+x) for x in v]).tobytes()==np.array(old[o]['lnN'][j]).tobytes(),'N0_STORED_KEPT_MISMATCH'
  vals.append(v)
 rows.append({'ordinal':o,'R_kpc':cols[32*o]['R_m']/L.KPC,'kept_delta_n':vals});print('kept ring',o,flush=True)
r={'schema':'NGC_STORED_KEPT_CXV001','label':'TESTED','operator_sha256':L.OP_SHA,'azimuths':32,'z_kpc':list(L.ZK),'rows':rows,'N0_all_nine_heights_bitwise':True,'producer_sha256':L.sha(__file__)}
print(L.write('out/STORED_KEPT_100_V001.json',r))
