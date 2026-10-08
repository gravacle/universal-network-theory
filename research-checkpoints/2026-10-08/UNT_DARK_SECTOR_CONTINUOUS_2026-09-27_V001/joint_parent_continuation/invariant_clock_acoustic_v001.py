"""Measured-temperature acoustic geometry of the fixed K(X) calibration.

Prospective protocol is in NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md.
Use existing authenticated HYREC FULL external-H binaries, one at a time.
No install, compilation, atomic source edit, dark calibration or ruler fit.
Ordinary thermal assumptions: T0=2.72548K, Neff3.046, YHe.245, zero injection,
minimal photon coupling, flat metric, cold baryons/massless neutrinos.
These are adopted, not native UNT or BBN predictions. The old radiation
benchmark OR9e-5 is replaced by blackbody energy ONLY for this new test.
The Planck compressed theta summary is exposed development evidence, not
a universal likelihood or a fresh held-out score. No n-sigma claim.
"""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import time
import numpy as np
import invariant_clock_plasma_v001 as plasma
import hyrec_standard_oracle_v001 as oracle

BASE=Path(__file__).resolve().parent
ATOMIC=BASE/'hyrec_inputs_v001'
OUT=BASE/'INVARIANT_CLOCK_ACOUSTIC_V001_RESULT.json'
PREFIX='INVARIANT_CLOCK_ACOUSTIC_V001'
T0=2.72548
KBOLTZ=1.380649e-23
HPLANCK=6.62607015e-34
S=plasma.SI
PLANCK_THETA100=1.0411
PLANCK_ERROR=.0003


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate():
    rp=ATOMIC/'HYREC_LOCAL_BUILD_V001.json'
    if sha(rp)!=oracle.RECEIPT_SHA:raise ValueError('Changed atomic build receipt')
    receipt=json.loads(rp.read_text());freeze=ATOMIC/receipt['freeze']['path']
    if sha(freeze)!=receipt['freeze']['sha256']:raise ValueError('Changed atomic freeze')
    manifest=json.loads(freeze.read_text())
    for name,digest in manifest['files'].items():
        if sha(oracle.bounded(oracle.ROOT/name))!=digest:raise ValueError('Changed atomic source '+name)
    for item in json.loads((ATOMIC/'HYREC_SOURCE_RECEIPT_V001.json').read_text())['files']:
        p=ATOMIC/'upstream'/item['name']
        if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:raise ValueError('Changed upstream '+item['name'])
    for entry in receipt['binaries'].values():
        if sha(ATOMIC/entry['path'])!=entry['sha256']:raise ValueError('Changed atomic binary')
    return receipt


class Background:
    def __init__(self,model,dust=False):
        self.model=model;self.dust=dust
        self.hunit=model.p['H0_km_s_Mpc']*1000/S['Mpc']
        self.unit=S['c']/(self.hunit*S['Mpc'])
        self.gcos=S['GN']*S['Gcos_over_GN']
        self.ug=8*math.pi**5*KBOLTZ**4*T0**4/(15*HPLANCK**3*S['c']**3)
        self.og=8*math.pi*self.gcos*self.ug/(3*S['c']**2*self.hunit**2)
        self.OR=self.og*(1+plasma.RN)
        self.Rb0=3*model.OB/(4*self.og)
        self.omega_b=model.OB*(model.p['H0_km_s_Mpc']/100)**2/S['Gcos_over_GN']
    def E(self,a):
        a=np.asarray(a,dtype=float);m=self.model
        if self.dust:
            h2=m.OA+(m.OB+m.p['omega_clock_excess'])/a**3+self.OR/a**4
        else:
            target=3*m.OA*m.p['d0']/(m.Q0*a**3)
            s=target/(m.mpref*math.sqrt(1+m.eps))
            for _ in range(3):
                Q,charge,d,Kfun,dm,q=m.constitutive(s)
                s=s-(charge-target)/dm
            Q,charge,d,Kfun,dm,q=m.constitutive(s)
            h2=(Q*charge-Kfun)/3+m.OB/a**3+self.OR/a**4
        if np.any(h2<=0):raise ValueError('Nonpositive expansion')
        return np.sqrt(h2)
    def H(self,z):return self.hunit*self.E(1/(1+np.asarray(z)))


def cubic(x,y,q):
    q=np.asarray(q)
    if np.any(q<x[0]) or np.any(q>x[-1]):raise ValueError('Interpolation outside grid')
    j=np.clip(np.searchsorted(x,q)-2,0,len(x)-4)
    nodes=x[j[:,None]+np.arange(4)]
    vals=y[j[:,None]+np.arange(4)];out=np.zeros(len(q))
    for k in range(4):
        w=np.ones(len(q))
        for l in range(4):
            if l!=k:w*=(q-nodes[:,l])/(nodes[:,k]-nodes[:,l])
        out+=w*vals[:,k]
    return out


def packet(bg,build,label,alternate=False):
    step=8.49e-5/(2 if build=='half' else 1)
    nz=int(math.log(8001)/step)+2
    z=np.arange(nz)*(8000/nz);HH=bg.H(z);err=0.
    if alternate:
        u=np.linspace(0,math.log(8001),math.ceil(nz/2)+1)
        logs=np.log(bg.H(np.expm1(u))/bg.hunit)
        alt=bg.hunit*np.exp(cubic(u,logs,np.log1p(z)))
        err=float(np.max(abs(alt/HH-1)));HH=alt
    context=dict(source_sha256=sha(Path(__file__)),background='pressureless' if bg.dust else 'KX',
        fixed=bg.model.p,T0=T0,YHe=plasma.YHE,Neff=plasma.NEFF,OR=bg.OR,og=bg.og,
        physical_omega_b=bg.omega_b,build=build,alternate_log_H_grid=alternate)
    claim=hashlib.sha256(json.dumps(context,sort_keys=True).encode()).hexdigest()
    lines=[f'UNT_HYREC_EXTERNAL_V001 {label} {claim}',
        f'{bg.omega_b:.17g} {T0:.17g} {plasma.YHE:.17g} {bg.model.p["H0_km_s_Mpc"]:.17g} {nz}']
    lines.extend(f'{zz:.17g} {hh:.17g}' for zz,hh in zip(z,HH))
    return ('\n'.join(lines)+'\n').encode(),context,err


def invoke(bg,build,label,receipt,alternate=False):
    raw,context,err=packet(bg,build,label,alternate)
    input_path=BASE/f'{PREFIX}_{label}_INPUT.txt'
    output_path=BASE/f'{PREFIX}_{label}_OUTPUT.json'
    stderr_path=BASE/f'{PREFIX}_{label}_STDERR.txt'
    for p in (input_path,output_path,stderr_path):
        if p.exists():raise FileExistsError(p)
    with input_path.open('xb') as stream:stream.write(raw)
    binary=ATOMIC/receipt['binaries'][build]['path']
    call=[str(binary),str(ATOMIC/'upstream')+'/', 'external']
    tick=time.monotonic()
    result=subprocess.run(call,input=raw,capture_output=True,check=False,timeout=60)
    with output_path.open('xb') as stream:stream.write(result.stdout)
    with stderr_path.open('xb') as stream:stream.write(result.stderr)
    if result.returncode or result.stderr:raise RuntimeError(f'Atomic failure {label}; raw outputs retained')
    data=json.loads(result.stdout)
    if data['status']!='COMPLETE_ATOMIC_HISTORY_ONLY' or data['mode']!='external':raise ValueError('Wrong atomic identity')
    for key,expected in [('omega_b',bg.omega_b),('T0_K',T0),('YHe_atomic',plasma.YHE)]:
        if abs(data[key]/expected-1)>1e-14:raise ValueError('Atomic input mismatch '+key)
    return data,dict(context=context,command=call,binary_sha256=sha(binary),
        elapsed_seconds=time.monotonic()-tick,input_path=input_path.name,input_sha256=sha(input_path),
        output_path=output_path.name,output_sha256=sha(output_path),stderr_path=stderr_path.name,
        native_alternate_H_relative_error=err,peak_self_rss_bytes=data['peak_self_rss_bytes'])


def quad(func,lo,hi,n):
    t,w=np.polynomial.legendre.leggauss(n)
    x=(lo+hi)/2+(hi-lo)*t/2
    return float((hi-lo)*np.dot(w,func(x))/2)


def distances(bg,z,n=256):
    astar=1/(1+z)
    sound=bg.unit*quad(lambda a:1/(a*a*bg.E(a)*np.sqrt(3*(1+bg.Rb0*a))),0.,astar,n)
    distance=bg.unit*quad(lambda x:np.exp(-x)/bg.E(np.exp(x)),math.log(astar),0.,n)
    return dict(rs_Mpc=sound,DM_Mpc=distance,theta100=100*sound/distance,
                ell_A=math.pi*distance/sound)


def observables(bg,data,thinning=1,nquad=256):
    arr=np.array(data['rows'],dtype=float)[::thinning]
    arr=arr[arr[:,0]>=10]
    z,xe=arr[:,0],arr[:,1];aa=1+z
    nH0=data['nH0_cm3']*1e6
    rate=S['c']*S['sigmaT']*nH0*xe*aa**3
    tauder=rate/(aa*bg.H(z))
    tau=np.concatenate(([0.],np.cumsum(np.diff(z)*(tauder[1:]+tauder[:-1])/2)))
    logvis=np.log(rate/aa)-tau
    imax=int(np.argmax(logvis))
    if not 0<imax<len(z)-1:raise ValueError('Visibility peak is not interior')
    dz=z[1]-z[0];vv=logvis[imax-1:imax+2]
    offset=dz*(vv[0]-vv[2])/(2*(vv[0]-2*vv[1]+vv[2]))
    if abs(offset)>dz:raise ValueError('Invalid visibility vertex')
    zstar=float(z[imax]+offset)
    dragder=tauder*aa/bg.Rb0
    drag=np.concatenate(([0.],np.cumsum(np.diff(z)*(dragder[1:]+dragder[:-1])/2)))
    low=quad(lambda zz:S['c']*S['sigmaT']*nH0*(1+2*data['fHe'])*(1+zz)**3/(bg.H(zz)*bg.Rb0),0,10,nquad)
    if not 0<1-low<1<drag[-1]:raise ValueError('Drag root is not bracketed')
    zd=[float(np.interp(target,drag,z)) for target in (1-low,1.)]
    ds=distances(bg,zstar,nquad)
    rsd=[distances(bg,q,nquad)['rs_Mpc'] for q in zd[::-1]]
    return dict(zstar=zstar,**ds,drag_redshift_interval=zd,drag_ruler_Mpc_interval=rsd,
        unknown_low_z_drag_depth_max=low,visibility_peak_convention='per conformal time; unknown low-z constant omitted',
        descriptor_Planck_theta100=PLANCK_THETA100,descriptor_Planck_error=PLANCK_ERROR,
        fractional_theta_offset=ds['theta100']/PLANCK_THETA100-1,
        Rb_at_visibility_peak=bg.Rb0/(1+zstar))


def main():
    start=time.monotonic();builds=authenticate()
    saved=json.loads(plasma.prior.old.base.SOURCE.read_text());saved['inherited']['Q0_over_H0']=100.
    model=plasma.prior.old.base.Model(saved,1);controls=[];rows=[]
    def check(name,value,gate):
        controls.append(dict(name=name,error=float(value),tolerance=gate,passed=bool(value<=gate)))
    # Direct vector H is checked against the old independently called scalar path.
    for dust in (False,True):
        bg=Background(model,dust);label='REFERENCE' if dust else 'CANDIDATE'
        aa=np.array([1e-8,1e-6,.0001,.001,.01,.1,1.])
        direct=bg.E(aa)
        old=np.array([plasma.prior.background(model,math.log(a),radiation=bg.OR,dust=dust)['H'] for a in aa])
        check(label+'_vector_scalar_H',np.max(abs(direct/old-1)),1e-10)
        calls={};atoms={};obs={}
        for build in ('default','half'):
            atoms[build],calls[build]=invoke(bg,build,label+'_'+build.upper(),builds)
            obs[build]=observables(bg,atoms[build])
        # Inspect exactly the common integer outputs; never compare different z.
        co=np.array(atoms['default']['rows'],dtype=float);fi=np.array(atoms['half']['rows'],dtype=float)[::2]
        if co.shape!=fi.shape or np.max(abs(co[:,0]-fi[:,0]))>1e-12:raise ValueError('Mismatched atomic outputs')
        check(label+'_xe_refinement',np.max(abs(co[:,1]-fi[:,1])/np.maximum(1e-3,abs(fi[:,1]))),2e-3)
        check(label+'_Tm_refinement',np.max(abs(co[:,2]/fi[:,2]-1)),2e-3)
        thin=observables(bg,atoms['half'],thinning=2)
        quadr=observables(bg,atoms['half'],nquad=128)
        fields=['zstar','rs_Mpc','DM_Mpc','theta100','drag_redshift_interval','drag_ruler_Mpc_interval']
        for key in fields:
            fine=np.array(obs['half'][key])
            check(label+'_'+key+'_atomic_refinement',np.max(abs(np.array(obs['default'][key])/fine-1)),2e-4)
            check(label+'_'+key+'_output_thinning',np.max(abs(np.array(thin[key])/fine-1)),1e-4)
            check(label+'_'+key+'_quadrature',np.max(abs(np.array(quadr[key])/fine-1)),2e-8)
        if not dust:
            alt,altcall=invoke(bg,'default',label+'_ALTERNATE_GRID',builds,alternate=True)
            altobs=observables(bg,alt)
            check(label+'_H_grid_pointwise',altcall['native_alternate_H_relative_error'],2e-7)
            for key in ('theta100','rs_Mpc','drag_ruler_Mpc_interval'):
                check(label+'_'+key+'_H_grid',np.max(abs(np.array(altobs[key])/np.array(obs['default'][key])-1)),1e-5)
            calls['alternate_H']=altcall;obs['alternate_H']=altobs
        row=dict(kind=label,omega_gamma_cos=bg.og,omega_radiation_cos=bg.OR,physical_omega_b=bg.omega_b,
            blackbody_energy_J_m3=bg.ug,actual_H_today=model.p['H0_km_s_Mpc']*float(bg.E(1)),
            invocations=calls,observables=obs,thinned=thin,quadrature128=quadr,
            adopted_early_tail_a0_to_1e_minus10_Mpc=bg.unit*quad(lambda a:1/(a*a*bg.E(a)*np.sqrt(3*(1+bg.Rb0*a))),0,1e-10,32))
        rows.append(row)
        print(json.dumps(dict(kind=label,observables=obs['half'])),flush=True)
    result=dict(protocol=__doc__,fixed=model.p,T0_K=T0,T0_error_K=.00057,Neff=plasma.NEFF,YHe=plasma.YHE,
        rows=rows,controls=controls,all_controls_passed=all(c['passed'] for c in controls),
        elapsed_seconds=time.monotonic()-start,
        hashes={p.name:sha(p) for p in (Path(__file__),Path(plasma.__file__),Path(plasma.prior.__file__),
            Path(plasma.prior.old.base.__file__),plasma.prior.old.base.SOURCE,
            ATOMIC/'HYREC_LOCAL_BUILD_V001.json',Path(oracle.__file__))})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],controls=controls,
                         elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
