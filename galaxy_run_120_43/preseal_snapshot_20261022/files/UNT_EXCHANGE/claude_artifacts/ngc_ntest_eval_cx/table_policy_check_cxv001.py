"""Replay diagnostic: precomputed versus on-demand module tables on three actual roster rings.
No file changes, no source/kernel/config changes; the second state shares immutable numerical arrays.
"""
import copy,math
import numpy as np

def check(ctx,cols):
    original=ctx.tail
    if original.empty:return dict(label='TESTED',empty=True,passed=True,max_delta_lnN=0.)
    arrays=dict(original._a)
    arrays['ring_radii_m']=np.array([],float)
    arrays['ring_tables']=np.zeros((0,3,len(arrays['kz'])),complex)
    rec=copy.deepcopy(original.record);rec['n_eval_radii']=0
    demand=original.__class__(empty=False,record=rec,arrays=arrays,jn_provider=original._provider())
    rows=[]
    try:
        for o in (1,7,15):
            col=cols[32*o];R=col['R_m'];phi=col['phi']
            for z in (0.,10.*3.085677581491367e19):
                ctx.tail=original;a=ctx.lnN(R,phi,z)
                ctx.tail=demand;b=ctx.lnN(R,phi,z)
                rows.append(dict(ordinal=o,z_m=z,precomputed=a,on_demand=b,delta=abs(a-b)))
    finally:ctx.tail=original
    worst=max(r['delta'] for r in rows)
    passed=worst<=3.3657664138980042e-09/2000
    if not passed:raise ValueError('RADIUS_TABLE_POLICY_DISAGREEMENT')
    return dict(label='TESTED',passed=passed,max_delta_lnN=worst,points=rows,
                scope='three actual rings, z=0/10, phi=0; NQ separately bounds total base/fine discrepancy on all acceptance reads')
