"""Common-state nonlinear spatial evaluation audit; NO new trajectory.

Use saved129- and257-node constrained states at a=.1,.316...,1. Restore
only six independent fields plus mean pi_a; Fourier-prolong to2N+1 and
4N+1, reconstruct BOTH momenta on each padded grid, evaluate the same
original constrained RHS, and project back. This isolates instantaneous
spatial evaluation from differing evolved histories. Use stable analytic
dust contrast in all cases, and separately report its native-grid RHS
difference from the old subtraction. No filter or changed physical model.
Report absolute/normalized commutators and the isolated nonanalytic J
contribution to charge flux. No post-hoc pass criterion or a=1 acceptance.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_source_precision_v001 as precise
import plane_constrained_evolution_v001 as old
import plane_canonical_evolution_v002 as spec
import plane_canonical_evolution_v001 as base

BASE=Path(__file__).resolve().parent
FILES=['PLANE_CONSTRAINED_EVOLUTION_V001_RESULT.json','PLANE_CONSTRAINED_EVOLUTION_V002_RESULT.json']
OUT=BASE/'PLANE_COMMON_STATE_AUDIT_V001_RESULT.json'


def project(z,N):
    f=np.fft.rfft(z,axis=-1)/z.shape[-1]
    return np.fft.irfft(f[...,:N//2+1]*N,n=N,axis=-1)


def evaluate(saved,z,a):
    m=precise.Model(saved,z.shape[-1]);x=math.log(a)
    full=m.reconstruct(x,z);rhs=m.rhs(x,z);g=m.unpack(x,full)
    Jflux=2*m.C*m.dx(g['B']**2*g['c']*g['j']*g['p'])/(m.pcbar*g['h'])
    return full,rhs,Jflux


def main():
    started=time.monotonic();saved=json.loads(base.SOURCE.read_text())
    rr=[json.loads((BASE/f).read_text()) for f in FILES]
    source_rows=[rr[0]['rows'][-1],rr[1]['rows'][1]]
    output=[]
    for row in source_rows:
        N=row['nodes']
        for i in (32,48,64):
            snap=row['snapshots'][i];a=snap['a'];z=np.array(snap['state'])
            z[4]=np.mean(z[4]);z[5]=0.
            native,fnative,jnative=evaluate(saved,z,a)
            fraw=old.Model(saved,N).rhs(math.log(a),z)
            sr=np.maximum(np.max(abs(fnative),axis=1),1e-8)
            sc=np.maximum(np.max(abs(native),axis=1),1e-8)
            cases=[];evaluations=[]
            for M in (2*N+1,4*N+1):
                zz=spec.prolong(z,M);full,rhs,jflux=evaluate(saved,zz,a)
                fc=project(full,N);ff=project(rhs,N);jf=project(jflux[None,:],N)[0]
                evaluations.append((fc,ff,jf))
                cases.append(dict(padding_nodes=M,
                    reconstruction_absolute=np.max(abs(fc-native),axis=1).tolist(),
                    reconstruction_normalized=(np.max(abs(fc-native),axis=1)/sc).tolist(),
                    rhs_absolute=np.max(abs(ff-fnative),axis=1).tolist(),
                    rhs_normalized=(np.max(abs(ff-fnative),axis=1)/sr).tolist(),
                    J_charge_flux_absolute_commutator=float(np.max(abs(jf-jnative))),
                    J_charge_flux_native_amplitude=float(np.max(abs(jnative)))))
            pad_delta=np.max(abs(evaluations[1][1]-evaluations[0][1]),axis=1)/sr
            output.append(dict(nodes=N,a=a,dust_precision_rhs_change=np.max(abs(fraw-fnative),axis=1).tolist(),
                cases=cases,padding_2N_4N_rhs_disagreement=pad_delta.tolist()))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ([base.SOURCE]+[BASE/f for f in FILES])},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ('plane_source_precision_v001.py','plane_constrained_evolution_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py')},
        cases=output,elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
