"""NE3: all 156 saved roster rings; first 100 are acceptance rings. Seven sealed heights plus reported +-95."""
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v005 as L
from table_policy_check_cxv001 import check as table_check

def evaluate(ctx,cols,start=0,end=None):
    end=len(cols)//32 if end is None else end
    if not 0<=start<end<=len(cols)//32:raise ValueError('RING_RANGE')
    rows=[]
    for o in range(start,end):
        r={'ordinal':o,'R_kpc':cols[32*o]['R_m']/L.KPC,'lnN':[]}
        for j in range(32):
            c=cols[32*o+j]
            r['lnN'].append([ctx.lnN(c['R_m'],c['phi'],0. if z==0 else z*L.KPC) for z in L.ZK])
        rows.append(r)
        print('ring',o,flush=True)
    return rows

def replay(kbig=2.,shape='cube',doubled=False,start=0,end=None):
    t=time.monotonic();ctx,cols=L.ctx_with_tail(kbig,shape,doubled)
    cache_check=table_check(ctx,cols);print("table policy",cache_check["max_delta_lnN"],flush=True)
    rows=evaluate(ctx,cols,start,end)
    return dict(schema='NGC_RING_UVT_C2V001',label='TESTED',operator_sha256=L.OP_SHA,
        kbig=kbig,shape=shape,doubled=doubled,z_kpc=list(L.ZK),azimuths=32,rows=rows,
        tail_record=ctx.tail.record,tail_digest=ctx.tail.digest,memory_cap_override=ctx.memory_cap_override,radius_table_policy=ctx.radius_table_policy,table_policy_check=cache_check,seconds=time.monotonic()-t)
