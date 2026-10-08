"""Independent midpoint integration of the zero-energy orbit coefficient; no data fit."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'QUENCH_MEAN_COEFFICIENT_V001.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    saved=json.loads(SOURCE.read_text());payload=dict(saved);digest=payload.pop('payload_sha256')
    assert hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==digest
    assert sha(ROOT/'quench_mean_coefficient_v001.py')==saved['script_sha256']
    assert all(saved['checks'].values())
    results=[]
    for n in (64,128,256,512):
        # Uniform midpoint orbit angle over a complete cycle; no Gauss nodes.
        theta=(np.arange(n)+.5)*(2*math.pi/n)
        x=(1-np.cos(theta))/2
        phi=(np.arange(n)+.5)*(math.pi/(2*n))
        z=np.sin(phi)**2
        w=1/np.sqrt(1+(1-z[:,None])*(x+x*x)[None,:])
        moment=np.sum(w*x[None,:]**3,axis=1)/np.sum(w,axis=1)
        integrand=2*math.sqrt(2)*z*(3-2*z)*moment
        value=math.fsum(float(v) for v in integrand)*math.pi/(2*n)
        assert abs(value-saved['C_quench'])<2e-11
        results.append(dict(midpoints_per_angle=n,C_quench=value,
            relative_difference_from_saved=value/saved['C_quench']-1,
            R3_min=float(np.min(moment)),R3_max=float(np.max(moment))))
    cref=3*math.pi/16;cq=results[-1]['C_quench']
    out=dict(scope='Independent original dimensionless integral, no galaxy input, fit or trajectory.',
        source_sha256=sha(Path(__file__)),input_sha256=sha(SOURCE),rows=results,
        exact_ratio_lower_bound=math.sqrt(2),exact_ratio_upper_bound=5*math.sqrt(2)/4,
        C_quench=cq,C_relaxed=cref,C_quench_over_relaxed=cq/cref,
        a0_mean_over_a0_relaxed=cref/cq)
    print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))


if __name__=='__main__':main()
