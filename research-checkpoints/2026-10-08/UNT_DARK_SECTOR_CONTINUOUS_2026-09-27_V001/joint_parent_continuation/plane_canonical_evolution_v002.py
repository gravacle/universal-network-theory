"""Numerical repair/refinement of failed V001, unchanged physics and gates.

Keep V001 immutable. It completed but failed spatial/Hamiltonian control.
V002 evaluates c_x by direct D(c-1), retains exact background cancellation
in metric momentum RHS, and compares Fourier-prolonged states on the ENTIRE
fine grid, including the unmatched fine tail. No clipping, smoothing,
constraint projection, smaller seed, revised action or relaxed tolerances.
Use odd grids to remove the even-grid unrepresented Nyquist component.
Run65/4096,129/8192,129/16384,257/16384 serially. Use the last two spatial
resolutions for acceptance, and129-node temporal refinement. Retain all
coarser errors without claiming that previously failed resolutions passed.
Controls unchanged from V001. Inspect Nyquist/tail power and saved V001
full-grid error; these are diagnostics, not post-hoc scientific gates.
"""
import hashlib
import json
import math
import resource
import time
from pathlib import Path
import numpy as np
import plane_canonical_evolution_v001 as old

BASE=Path(__file__).resolve().parent
OUT=BASE/'PLANE_CANONICAL_EVOLUTION_V002_RESULT.json'
OLD_RESULT=BASE/'PLANE_CANONICAL_EVOLUTION_V001_RESULT.json'


def prolong(z,N):
    n=z.shape[-1]; f=np.fft.rfft(z,axis=-1)/n
    g=np.zeros(z.shape[:-1]+(N//2+1,),complex)
    g[...,:n//2+1]=f
    if n%2==0:
        g[...,n//2]*=.5  # Split real coarse Nyquist cosine into +/- frequencies.
    return np.fft.irfft(g*N,n=N,axis=-1)


def compare(a,b):
    if not a['completed'] or not b['completed']:return None
    za=np.array([r['state'] for r in a['snapshots']]);zb=np.array([r['state'] for r in b['snapshots']])
    if za.shape[-1]<zb.shape[-1]:za=prolong(za,zb.shape[-1])
    scale=np.maximum(np.max(abs(zb),axis=(0,2)),1e-8)
    e=np.max(abs(za-zb),axis=(0,2))/scale
    return dict(per_variable=e.tolist(),maximum=float(np.max(e)))


def spectral_report(row):
    z=np.array(row['snapshots'][-1]['state']);N=row['nodes']
    f=np.fft.rfft(z,axis=-1)/N
    return dict(nodes=N,amplitudes=(2*abs(f)).tolist(),
        last_quarter_tail_amplitude=(2*np.max(abs(f[:,3*N//8:]),axis=1)).tolist())


class Model(old.Model):
    def __init__(self,saved,N):
        super().__init__(saved,N)
        self.modes=np.fft.fftfreq(N,1/N)
        if N%2==0:self.modes[N//2]=0

    def rhs(self,x,z):
        g=self.unpack(x,z);a=g['abar'];h=g['h'];V=g['V'];A=g['A'];B=g['B']
        sig=g['sig'];c=g['c'];piux=g['piux'];S=g['S'];cur=g['cur']
        pa=z[4];pb=z[5];v=z[0]+2*z[1];ev=g['ev'];inv=np.exp(-v)
        bx=g['bx'];fg=B*B/A
        Lvec=self.KB*g['e']**2+2*self.C*g['e']*g['p']-self.C*g['p']**2-self.C*g['J']
        nA=-2*fg*bx*bx+V*(Lvec-2*g['Z']*g['e']-2*(sig*S/c+g['w']*cur))+sig*sig*piux/c
        nB=4*fg*bx*bx-4*self.dx(fg*bx)+2*V*Lvec
        dK=3*self.OA/self.D*(np.log1p((g['s']-g['sbar'])/(1+g['sbar']))-(g['s']-g['sbar'])/((1+g['s'])*(1+g['sbar'])))
        kA=(g['Kbar']*(pa-np.expm1(v))-ev*dK)/(2*h*h)
        kB=(g['Kbar']*(pb-np.expm1(v))-ev*dK)/(2*h*h)
        shared=1.5*(1+pa)*np.expm1(-v)+.5*inv*(1+pa)*(4*pb-pa)
        out=np.empty_like(z)
        out[0]=np.expm1(-v)+inv*(2*pb-pa)
        out[1]=np.expm1(-v)+inv*pa
        out[2]=(A*g['e']-self.dx(sig*sig/(c+1)))/(a*h)-z[2]
        out[3]=g['qdiff']/h
        out[4]=shared+kA+nA/(-4*a**3*h*h)
        out[5]=shared+1.5*(pa-pb)+kB+nB/(-8*a**3*h*h)
        rU=2*B*B*S/c-sig*piux/(A*c)
        out[6]=rU/(2*a*a*h)-2*z[6]
        out[7]=-2*self.dx(B*B*cur)/(self.pcbar*h)
        return out

    def diagnostics(self,x,z):
        result=super().diagnostics(x,z);g=self.unpack(x,z)
        fg=g['B']**2/g['A'];bx=g['bx'];ax=g['ax']
        defect=4*(self.dx(fg*bx)-fg*self.dx(bx)-fg*(-ax+2*bx)*bx)
        result['curvature_product_rule_defect_normalized']=float(np.max(abs(defect)/(6*g['V']*g['h']**2)))
        return result


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    started=time.monotonic();saved=json.loads(old.SOURCE.read_text())
    previous=json.loads(OLD_RESULT.read_text())
    previous_full_grid=compare(previous['rows'][1],previous['rows'][2])
    print(json.dumps(dict(previous_full_grid=previous_full_grid)),flush=True)
    # Independent algebraic oracle: cancellation-resistant formula vs owned V001.
    m=Model(saved,32);baseline=old.Model(saved,32);y=m.y
    probe=m.initial();probe[0]+=1e-6*np.cos(y);probe[1]+=2e-6*np.cos(y)
    probe[2]+=1e-6*np.sin(y);probe[3]+=1e-7*np.cos(y)
    probe[4]+=3e-6*np.cos(y);probe[5]+=1e-6*np.cos(y)
    probe[6]+=1e-6*np.sin(y);probe[7]+=1e-5*np.cos(y)
    algebra_error=float(np.max(abs(m.rhs(math.log(.01),probe)[4:6]-baseline.rhs(math.log(.01),probe)[4:6])))
    if algebra_error>2e-12:raise ValueError('stable metric algebra mismatch')
    old.Model=Model
    rows=[old.integrate(saved,N,steps) for N,steps in ((65,4096),(129,8192),(129,16384),(257,16384))]
    rt=compare(rows[1],rows[2]);rs=compare(rows[2],rows[3]);coarse=compare(rows[0],rows[1])
    # Numerical acceptance is for the fine converged sequence, not the failed coarse resolutions.
    accepted=rows[1:];samples=[s for r in accepted for s in r['snapshots']]
    checks=dict(all_completed=all(r['completed'] for r in accepted),
        algebra=algebra_error<=2e-12,
        homogeneous=max(r['homogeneous_rhs_error'] for r in accepted)<=2e-12,
        initial_shear=max(r['initial_shear_relative_error'] for r in accepted)<=1e-6,
        inverse=max(r['maximum_inverse_error'] for r in accepted)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        space_refinement=rs is not None and rs['maximum']<=1e-4,
        Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        Hamiltonian_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        conserved_charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12)
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (old.SOURCE,OLD_RESULT)},
        dependency_sha256=hashlib.sha256((BASE/'plane_canonical_evolution_v001.py').read_bytes()).hexdigest(),
        previous_full_grid_refinement=previous_full_grid,stable_metric_algebra_error=algebra_error,
        rows=rows,time_refinement=rt,space_refinement=rs,coarse_space_refinement=coarse,
        spectral_diagnostics=[spectral_report(r) for r in rows],controls=checks,
        all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-started,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','rows','spectral_diagnostics')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
