"""Refine only V001's failed smooth-kernel comparison, unchanged1e-6 gate.

All exact-even-polynomial and origin-parity controls passed. Smooth Plummer
512-node derivative error1.78180e-5 did not pass1e-6. Here1024/2048 nodes
test convergence, not a changed law or relaxed tolerance. This component
qualification does not qualify any lower-resolution physical trajectory.
"""
from pathlib import Path
import json
import math
import time
import numpy as np
import invariant_clock_compression_even_kernel_test_v001 as old

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_EVEN_KERNEL_TEST_V002_RESULT.json'
OLD=ROOT/'INVARIANT_CLOCK_COMPRESSION_EVEN_KERNEL_TEST_V001_RESULT.json'
OLDSHA='1468c3bed740984b05960327454a1de4b3f7ba93beb5ac25b3281f4d1d048695'

def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic()
    if old.sha(OLD)!=OLDSHA:raise ValueError('changed failure receipt')
    previous=json.loads(OLD.read_text());checks=[r for r in previous['controls'] if r['passed']];rows=[]
    for n in (1024,2048):
        r=np.sinh((np.arange(n)+.5)*math.asinh(1000)/n);T=3+.05/(1+r*r)**2.5
        chi,chir=map(np.array,old.kernel.kernel(r,T,float(-old.CT*T[-1]),old.CT))
        lo=old.plummer_oracle(r,64);hi=old.plummer_oracle(r,128)
        oracle_error=max(old.maximum(lo[0]-hi[0]),old.maximum(lo[1]-hi[1]))/(old.CT*.05)
        error=max(old.maximum(chi-hi[0]),old.maximum(r*chir-hi[1]))/(old.CT*.05)
        checks.append(dict(name=f'{n}_quadrature',error=oracle_error,gate=1e-11,passed=oracle_error<=1e-11))
        rows.append(dict(nodes=n,error=error))
    checks.append(dict(name='Plummer_fine_refined',error=rows[-1]['error'],gate=1e-6,passed=rows[-1]['error']<=1e-6))
    result=dict(protocol=__doc__,parent_sha256=OLDSHA,rows=rows,controls=checks,
        all_controls_passed=all(r['passed'] for r in checks),elapsed_seconds=time.monotonic()-started,
        hashes={str(p):old.sha(p) for p in (Path(__file__),Path(old.__file__),Path(old.kernel.__file__))})
    with OUT.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(rows=rows,checks=len(checks),all_controls_passed=result['all_controls_passed'],
        elapsed_seconds=result['elapsed_seconds'],result_sha256=old.sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
