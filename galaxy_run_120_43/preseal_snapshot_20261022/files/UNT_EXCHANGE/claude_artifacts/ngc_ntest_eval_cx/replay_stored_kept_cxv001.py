"""0539 cube N3 replay with one byte-pinned kept array reused literally. K OUTPUT; no solve."""
import json,math,sys,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v004 as L
K=float(sys.argv[1]);name=sys.argv[2]
if K not in (8.,16.,32.):raise ValueError('REGISTERED_CUBE_ONLY')
if (L.HERE/name).exists():raise ValueError('OUTPUT_EXISTS')
ctx,cols=L.ctx_with_tail(K,'cube',False);p=L.HERE/'out/STORED_KEPT_100_V001.json'
while not p.exists():print('waiting for stored kept packet',flush=True);time.sleep(30)
ref={'path':str(p),'sha256':L.sha(p)};d=json.loads(p.read_bytes());assert d['operator_sha256']==L.OP_SHA and d['N0_all_nine_heights_bitwise'] is True
rows=[];spot=[];tailmax=0.
for o,old in enumerate(d['rows']):
 assert old['ordinal']==o and old['R_kpc']==cols[32*o]['R_m']/L.KPC
 row={'ordinal':o,'R_kpc':old['R_kpc'],'lnN':[]}
 for j in range(32):
  c=cols[32*o+j];R=c['R_m'];phi=c['phi'];values=[]
  for h,z in enumerate(L.ZK):
   zm=z*L.KPC;pos=np.array([[R*math.cos(phi),R*math.sin(phi),zm]])
   t=float(ctx.tail.jet(pos,1)['boundary_fields'][0,0,0]);tailmax=max(tailmax,abs(t));N=1.+(old['kept_delta_n'][j][h]+t)
   if not math.isfinite(N) or N<=0:raise ValueError('NONPOSITIVE_LAPSE')
   val=math.log(N);values.append(val)
   if o in (1,7,15) and j==0 and h in (0,1):
    parent=ctx.lnN(R,phi,zm);assert np.float64(val).tobytes()==np.float64(parent).tobytes(),'PARENT_ARITHMETIC_MISMATCH';spot.append({'ordinal':o,'height':h,'bitwise_equal':True})
  row['lnN'].append(values)
 rows.append(row);print('stored case',K,'ring',o,flush=True)
r=dict(schema='NGC_RING_UVT_C2V001',label='TESTED',operator_sha256=L.OP_SHA,kbig=K,shape='cube',doubled=False,z_kpc=list(L.ZK),azimuths=32,rows=rows,tail_record=ctx.tail.record,tail_digest=ctx.tail.digest,memory_cap_override=ctx.memory_cap_override,radius_table_policy=ctx.radius_table_policy,stored_kept_reference=ref,arithmetic='1.+(n_kept+t)',parent_arithmetic_checks=spot,max_abs_tail=tailmax,case='CUBE'+str(int(K)))
if K==16.:
 base=json.loads((L.HERE/'out/NQ_BASE_V001.json').read_bytes())['rows'];assert np.array([x['lnN'] for x in rows]).tobytes()==np.array([x['lnN'] for x in base]).tobytes(),'STORED_BASE_MISMATCH';r['base_replay_bitwise_equal']=True
print(L.write(name,r))
