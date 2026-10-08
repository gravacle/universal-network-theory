"""NEW uncompressed constrained-U/physical-clock/one-gradient FLRW response.

Standalone prospective finite-mode DAE. No legacy producer/calibration is called.
Root alone launches --execute after complete reviews and ownership checks.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import time
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
PROTOCOL_SHA='5d4a7abceca7f005ac9efd95bc2638ae94dd8eb8b0992ea80793193a079c55b2'
PINS={
 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0',
 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json':'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f',
 'BOUNDED_CLOCK_ACTION_AND_RESULT_V001.md':'cf308c536629640fc5594b49b47447dc0c370e5e61e8fa622efa954ba975902b',
 'INVARIANT_CLOCK_SUPPORTED_SOURCE_V001.md':'cd0700b3ace4282cb7413860053d1db1324ea0fdb893193054474dc042313426',
 'SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md':'a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57',
 'same_t_clock_gradient_flrw_response_v001.py':'61e6191713e5eb628b2ec551de43c200a029a6f236f7da255e867fca1d8d0990',
 'NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md':'b2158042a2ce0867f5984e72cdea06b536975e1817fa48a9198272c0d394fffc',
}
AI,SEED=.01,1e-8
X0=math.log(AI)
CP_KMS=299792.458
KB,C,MBAR,CBAR=.02,1.98,.5,.99
CASES=[(k,om) for k in (.01,.1) for om in (.1,1.,10.,100.)]
TRIALS=[('COARSE',65536,48),('FINE',131072,48),('MODES',131072,96)]
FLUID_NAMES=['Phi','delta_b','Hstar_v_b','delta_rad','Hstar_v_rad',
 'Hstar_pi_U','delta_n_clock_over_n','Hstar_V_phi','Ptot','Z','Z_dot','n_U','sigma']
PHYSICAL_NAMES=['comoving_delta_b','comoving_baryon_density','comoving_rad_density',
 'comoving_clock_density','polarization_density','Weyl','normal_acceleration']
CREATED_SEALS={}
READ_SEALS={}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

def write_json(name, obj):
    path = BASE / name
    with path.open('x') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), allow_nan=False)
        f.write('\n')
    path.chmod(0o444)
    seal=sha(path)
    CREATED_SEALS[str(path)]=seal
    return seal

def journal(event, **kwargs):
    with (BASE / (STEM + '_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(time=now(), event=event, **kwargs), sort_keys=True)+'\n')

def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))



def fields(x,y,fixed,snodes,weights):
    bg=background(x,fixed)
    h,b,r,w,s,Q=(bg[n] for n in ('h','b','r','w','cs','Q'))
    q=np.array([k*CP_KMS/fixed['Hunit']/bg['a'] for k,_ in CASES])[:,None]
    om2=np.array([om*om for _,om in CASES])[:,None]
    ns=len(snodes)
    z,zd=y[:,:,9:9+ns],y[:,:,9+ns:]
    Z,Zd=z@weights,zd@weights
    R1=(z*snodes[None,None,:]**2)@weights*om2
    alpha=om2*float(snodes**2@weights)
    phi,db,ub,dr,ur,pi,d,V,P=(y[:,:,i] for i in range(9))
    mom=b*ub+4*r*ur/3+w*V
    phid=mom-h*phi
    n=(P-CBAR*Z)/(MBAR*KB*q)
    Vd=phi+s*(d+3*h*V)
    v=V-pi
    vd=n+s*(d+3*h*V)
    L=Q*q
    Ld=-h*(1+3*s)*L
    Ldd=(-bg['h_dt']*(1+3*s)-3*h*bg['cs_dt']+h*h*(1+3*s)**2)*L
    Bq=1+(fixed['L']*q)**2
    Fv=(-h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cs_dt']*(d+3*h*V)
         +s*(3*phid-q*q*V+3*bg['h_dt']*V+3*h*Vd))
    D=w/s
    Delta=alpha+C*Q*Q/KB+CBAR*Q*Q*q*q/D
    sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta
    return dict(bg=bg,q=q,z=z,zd=zd,Z=Z,Zd=Zd,phi=phi,db=db,ub=ub,dr=dr,ur=ur,
                pi=pi,d=d,V=V,P=P,mom=mom,phid=phid,n=n,Vd=Vd,v=v,vd=vd,
                L=L,Ld=Ld,Bq=Bq,Delta=Delta,sigma=sigma)


def rates(x,y,fixed,snodes,weights):
    f=fields(x,y,fixed,snodes,weights)
    bg=f['bg']; h,w,s,Q=(bg[n] for n in ('h','w','cs','Q'))
    q,n,sigma=f['q'],f['n'],f['sigma']
    ns=len(snodes)
    om2=np.array([om*om for _,om in CASES])[:,None,None]
    out=np.empty_like(y)
    out[:,:,0]=f['phid']
    out[:,:,1]=3*f['phid']-q*q*f['ub']
    out[:,:,2]=f['phi']
    out[:,:,3]=4*f['phid']-4*q*q*f['ur']/3
    out[:,:,4]=f['phi']+f['dr']/4+h*f['ur']
    out[:,:,5]=f['phi']-n
    out[:,:,6]=3*f['phid']-q*q*f['V']-CBAR*Q*q*sigma/w
    out[:,:,7]=f['Vd']
    out[:,:,8]=-2*h*f['P']-CBAR*Q*sigma
    out[:,:,9:9+ns]=f['zd']
    out[:,:,9+ns:]=(-3*h*f['zd']-om2*snodes[None,None,:]**2*
                   (f['Bq'][:,:,None]*f['z']-q[:,:,None]*n[:,:,None]-sigma[:,:,None]))
    return out/h


def initial_state(fixed,ns):
    bg=background(X0,fixed)
    y=np.zeros((len(CASES),2,9+2*ns))
    B=bg['b']+4*bg['r']/3+bg['w']
    for c,(k,_) in enumerate(CASES):
        q=k*CP_KMS/fixed['Hunit']/AI
        for seed in range(2):
            phi,V=(SEED,0.) if seed==0 else (0.,SEED/bg['h'])
            d=-q*q*phi/(B+MBAR*KB*q*q*bg['cs'])-3*bg['h']*V
            n=-bg['cs']*(d+3*bg['h']*V)
            y[c,seed,:9]=[phi,d,V,4*d/3,V,V,d,V,MBAR*KB*q*n]
    return y


def readouts(x,y,fixed,snodes,weights):
    f=fields(x,y,fixed,snodes,weights)
    bg=f['bg']; h,b,r,w,s,Q=(bg[n] for n in ('h','b','r','w','cs','Q'))
    q=f['q']
    terms=np.stack((q*q*f['phi'],3*h*f['mom'],b*f['db'],r*f['dr'],w*f['d'],-q*f['P']),axis=-1)
    norm_floor=q*q*SEED*1e-10
    norm_den=np.maximum(np.sum(abs(terms),axis=-1),norm_floor)
    cterms=np.stack((f['Z'],-f['L']*f['v']),axis=-1)
    jterms=np.stack((f['Zd'],-f['Ld']*f['v'],-f['L']*f['vd']),axis=-1)
    cfloor=f['L']*SEED*1e-10
    jfloor=cfloor*max(h,Q,max(om for _,om in CASES))
    cden=np.maximum(np.sum(abs(cterms),axis=-1),cfloor)
    jden=np.maximum(np.sum(abs(jterms),axis=-1),jfloor)
    fluids=np.concatenate((y[:,:,:9],f['Z'][:,:,None],f['Zd'][:,:,None],
                            f['n'][:,:,None],f['sigma'][:,:,None]),axis=-1)
    comov_b=f['db']+3*h*f['ub']
    physical=np.stack((comov_b,b*comov_b,r*(f['dr']+4*h*f['ur']),
                       w*(f['d']+3*h*f['V']),-q*f['P'],2*f['phi'],q*f['n']),axis=-1)
    amp=np.stack((abs(f['phi']),abs(f['db']),abs(f['dr']),abs(f['d']),
                  abs(q*f['ub']),abs(q*f['ur']),abs(q*f['V']),abs(q*f['pi']),
                  abs(q*f['v']),abs(f['n'])),axis=-1)
    eps,u,qp=fixed['eps'],bg['s'],bg['qbar']
    lower=eps*u/((1+u)*qp*(qp+1))
    upper=eps/((1+u)*qp*(math.sqrt(1+eps)+qp))
    rate=s*f['d']; relative=q*f['v']
    domain=np.stack((rate,np.full_like(rate,lower),np.full_like(rate,upper),
                     abs(rate)/min(lower,upper),q*f['V'],q*f['pi'],relative,
                     relative*relative/(2*min(lower,upper))),axis=-1)
    return dict(background=bg,fluids=fluids,physical=physical,normal_terms=terms,
                normal_error=abs(np.sum(terms,axis=-1))/norm_den,normal_floor=norm_floor,
                constraint_terms=cterms,constraint_error=abs(np.sum(cterms,axis=-1))/cden,
                constraint_floor=cfloor,first_jet_terms=jterms,
                first_jet_error=abs(np.sum(jterms,axis=-1))/jden,first_jet_floor=jfloor,
                reaction_denominator=f['Delta'],amplitudes=amp,physical_domain=domain)


def trial(label, steps, ns, fixed, lineage):
    xn, wn = np.polynomial.legendre.leggauss(ns)
    snodes, weights = (xn+1)/2, wn*(xn+1)/2
    dx = -X0/steps
    y, n0, snapshots = initial_state(fixed, ns), 0, []
    commits = sorted(BASE.glob(STEM+'_'+label+'_CP_*_COMMIT.json'))
    payloads = set(p.name for p in BASE.glob(STEM+'_'+label+'_CP_*.json')
                   if not p.name.endswith('_COMMIT.json'))
    committed = set(p.name.replace('_COMMIT.json', '.json') for p in commits)
    if payloads != committed:
        raise RuntimeError('Orphan checkpoint preserved for root inspection; no overwrite/rerun')
    if commits:
        last=int(commits[-1].stem.rsplit('_',2)[-2])
        expected=[STEM+'_'+label+'_CP_'+str(n).zfill(6)+'_COMMIT.json' for n in range(8192,last+1,8192)]
        if [p.name for p in commits]!=expected:
            raise RuntimeError('Incomplete checkpoint prefix preserved')
        events = [json.loads(line) for line in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
        for cp in commits:
            row = json.loads(cp.read_text())
            READ_SEALS[str(cp)]=sha(cp)
            if set(row)!=set(('lineage','steps','ns','payload','sha256')) or row['payload']!=cp.name.replace('_COMMIT.json','.json'):
                raise RuntimeError('Checkpoint exact commit schema/name mismatch')
            if row.get('lineage')!=lineage or row.get('steps')!=steps or row.get('ns')!=ns:
                raise RuntimeError('Earlier checkpoint lineage/census mismatch')
            READ_SEALS[str(BASE/row['payload'])]=row['sha256']
            entries = [e for e in events if e.get('event') == 'CHECKPOINT'
                       and e.get('trial') == label and e.get('payload') == row['payload']]
            if len(entries) != 1 or entries[0]['commit_sha256'] != sha(cp):
                raise RuntimeError('Checkpoint commit journal authentication failed')
            if entries[0]['sha256'] != row['sha256'] or sha(BASE/row['payload']) != row['sha256']:
                raise RuntimeError('Checkpoint payload journal authentication failed')
        commit = json.loads(commits[-1].read_text())
        if commit['lineage'] != lineage or commit['steps'] != steps or commit['ns'] != ns:
            raise RuntimeError('Checkpoint lineage/census mismatch; preserved without overwrite')
        payload = BASE / commit['payload']
        if sha(payload) != commit['sha256']:
            raise RuntimeError('Checkpoint payload seal mismatch')
        saved = json.loads(payload.read_text())
        if set(saved)!=set(('lineage','steps','ns','n','state','snapshots')):
            raise RuntimeError('Saved payload exact schema mismatch')
        if any(saved[k] != commit[k] for k in ('lineage', 'steps', 'ns')):
            raise RuntimeError('Saved checkpoint metadata mismatch')
        y, n0, snapshots = np.array(saved['state']), saved['n'], saved['snapshots']
        if type(n0) is not int or not 0 < n0 <= steps or n0 % 8192:
            raise RuntimeError('Invalid saved step')
        if y.shape != (len(CASES), 2, 9+2*ns) or not np.all(np.isfinite(y)):
            raise RuntimeError('Saved full state schema failure')
        if [s['n'] for s in snapshots] != list(range(0, n0+1, steps//64)):
            raise RuntimeError('Saved ordered snapshot prefix mismatch')
        expected_snapshot=set(('n','x','state','background','fluids','physical','normal_terms','normal_error','normal_floor','constraint_terms','constraint_error','constraint_floor','first_jet_terms','first_jet_error','first_jet_floor','reaction_denominator','amplitudes','physical_domain'))
        for s in snapshots:
            if set(s)!=expected_snapshot:
                raise RuntimeError('Saved snapshot exact schema mismatch')
            if s['x'] != X0+s['n']*dx or np.array(s['state']).shape != y.shape:
                raise RuntimeError('Saved snapshot coordinate/shape mismatch')
            if not np.all(np.isfinite(np.array(s['state']))):
                raise RuntimeError('Saved snapshot nonfinite state')
        if n0 != int(payload.stem.rsplit('_', 1)[-1]) or snapshots[-1]['state'] != saved['state']:
            raise RuntimeError('Saved checkpoint end-state mismatch')
        journal('RESUME', trial=label, n=n0, commit=commits[-1].name)
    if n0 == 0:
        rr = readouts(X0, y, fixed, snodes, weights)
        snapshots.append(dict(n=0, x=X0, state=y.tolist(),
                              **{k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in rr.items()}))
    for n in range(n0+1, steps+1):
        x = X0+(n-1)*dx
        k1 = rates(x, y, fixed, snodes, weights)
        k2 = rates(x+dx/2, y+dx*k1/2, fixed, snodes, weights)
        k3 = rates(x+dx/2, y+dx*k2/2, fixed, snodes, weights)
        k4 = rates(x+dx, y+dx*k3, fixed, snodes, weights)
        y += dx*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(y)):
            raise FloatingPointError('Nonfinite state at '+label+' step '+str(n))
        if n % (steps//64) == 0:
            xx = X0+n*dx
            rr = readouts(xx, y, fixed, snodes, weights)
            snapshots.append(dict(n=n, x=xx, state=y.tolist(),
                                  **{k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in rr.items()}))
        if n % 8192 == 0 or n == steps:
            stem = STEM+'_'+label+'_CP_'+str(n).zfill(6)
            payload = stem+'.json'
            seal = write_json(payload, dict(lineage=lineage, steps=steps, ns=ns, n=n,
                                            state=y.tolist(), snapshots=snapshots))
            commit_sha = write_json(stem+'_COMMIT.json', dict(lineage=lineage, steps=steps, ns=ns,
                                                             payload=payload, sha256=seal))
            journal('CHECKPOINT', trial=label, n=n, payload=payload, sha256=seal, commit_sha256=commit_sha)
            print(json.dumps(dict(trial=label, completed_steps=n, total_steps=steps)), flush=True)
    return dict(label=label, steps=steps, ns=ns, snodes=snodes.tolist(),
                weights=weights.tolist(), snapshots=snapshots)



def main():
    start=time.monotonic()
    direct=dict(PINS,**{STEM+'.md':PROTOCOL_SHA})
    for name,expected in direct.items():
        if sha(BASE/name)!=expected: raise RuntimeError('Direct input mismatch '+name)
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    inputs={str((BASE/name).resolve()):h for name,h in direct.items()}
    for path,h in cal['hashes'].items():
        if path in inputs and inputs[path]!=h: raise RuntimeError('Conflicting calibration seal')
        if sha(path)!=h: raise RuntimeError('Historical calibration seal mismatch '+path)
        inputs[path]=h
    source_sha=sha(__file__)
    lineage=dict(inputs=inputs,source_sha256=source_sha)
    sel,owned=cal['selected'],cal['fixed']
    ctx=cal['trials'][-1]['atomic_invocation']['context']
    if (ctx['fixed']['H0_km_s_Mpc']!=sel['Hunit'] or ctx['fixed']['omega_b_cos']!=sel['OB']
        or owned['KB']!=KB or owned['Q0_over_H0']!=100. or owned['rG']!=.98):
        raise RuntimeError('Frozen physical inventory identity mismatch')
    fixed=dict(Hunit=sel['Hunit'],OA=owned['omega_A'],OB=sel['OB'],OR=ctx['OR'],
               d0=owned['d0'],eps=owned['eps'],rG=.98/.99,old_rG=.98,new_Gcos_over_GN=.99,
               Q0_over_Hstar=owned['Q0_over_H0'],ell_pc=100.,L=100e-6*sel['Hunit']/CP_KMS,
               seed=SEED,initial_a=AI,KB=KB,C=C,Mbar=MBAR,Cbar=CBAR,
               density_unit='rho_star=2 M_bare^2 Hstar^2',time_unit='Hstar proper_time')
    manifest=dict(lineage=lineage,fixed=fixed,cases=CASES,trials=TRIALS,
                  seeds=['constraint_consistent_fixed_Phi_zero_velocity',
                         'constraint_consistent_zero_Phi_fixed_velocity'],numpy_version=np.__version__,
                  prospective_action='uncompressed cTheta0 constrained polarization replacement',
                  extra_native_remainder='absent',radiation='conserved perfect fluid, no anisotropic stress',
                  physical_domain_scope='sampled linear phase and relative-velocity heads, not nonlinear certificate')
    mp=BASE/(STEM+'_MANIFEST.json')
    if mp.exists():
        if json.loads(mp.read_text())!=json.loads(json.dumps(manifest)):
            raise RuntimeError('Existing manifest mismatch')
        READ_SEALS[str(mp)]=sha(mp)
    else: write_json(mp.name,manifest)
    if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')):
        raise RuntimeError('Final artifact exists; no overwrite/duplicate run')
    journal('OWNER_START',pid=os.getpid(),owner='root',source_sha256=source_sha)
    rows=[trial(*arm,fixed,lineage) for arm in TRIALS]
    gates=[]
    def check(name,error,tolerance,**ident):
        gates.append(dict(name=name,error=float(error),tolerance=tolerance,
                          passed=bool(math.isfinite(error) and error<=tolerance),**ident))
    for tr in rows:
        check('spectral_normalization',abs(sum(tr['weights'])-1),1e-13,trial=tr['label'])
        check('charge_root',max(s['background']['charge_error'] for s in tr['snapshots']),1e-13,trial=tr['label'])
        for c,_ in enumerate(CASES):
            for seed in range(2):
                for name,tol in [('normal_error',1e-6),('constraint_error',1e-7),('first_jet_error',1e-7)]:
                    check(name,max(s[name][c][seed] for s in tr['snapshots']),tol,
                          trial=tr['label'],case=c,seed=seed)
    fine=np.array([s['fluids'] for s in rows[1]['snapshots']])
    for arm,name in [(0,'time'),(2,'spectral')]:
        comp=np.array([s['fluids'] for s in rows[arm]['snapshots']])
        error=np.max(abs(comp-fine),axis=0)/np.maximum(np.max(abs(fine),axis=0),1e-16)
        for c,_ in enumerate(CASES):
            for seed in range(2):
                for i,label in enumerate(FLUID_NAMES):
                    check(name+'_refinement',error[c,seed,i],1e-4,case=c,seed=seed,variable=label)
    bg1=background(0.,fixed)
    pex=(math.log1p(bg1['s'])-bg1['s']/(1+bg1['s']))/(1/fixed['eps']-math.log1p(1/fixed['eps']))
    check('fixed_inventory_H_identity',abs(bg1['h']**2*fixed['rG']-
          (fixed['OA']*(1+bg1['qbar']*bg1['charge']-pex)+fixed['OB']+fixed['OR'])),1e-13)
    if len(gates)!=567: raise RuntimeError('Exact numerical gate census mismatch')
    endpoints,flags,effects=[],[],[]
    for c,(k,om) in enumerate(CASES):
        ref=(c//4)*4
        for seed in range(2):
            physical=np.array(rows[1]['snapshots'][-1]['physical'])
            endpoints.append(dict(case=c,k_Mpc_inverse=k,omega_over_Hstar=om,seed=seed,
                physical=physical[c,seed].tolist(),difference_from_fixed_omega_point1=(physical[c,seed]-physical[ref,seed]).tolist()))
            paired=[np.array(tr['snapshots'][-1]['physical'])[c,seed]-
                    np.array(tr['snapshots'][-1]['physical'])[ref,seed] for tr in rows]
            dt,ds=paired[0]-paired[1],paired[2]-paired[1]
            margin=3*np.maximum(abs(dt),abs(ds))
            effects.append(dict(case=c,seed=seed,reference='omega=.1 same k and seed, not mode-off/GR',
                coarse_effect=paired[0].tolist(),fine_effect=paired[1].tolist(),spectral_effect=paired[2].tolist(),
                time_change=dt.tolist(),spectral_change=ds.tolist(),three_change_margin=margin.tolist(),
                resolution=['reference_zero' if c==ref else ('resolved' if abs(a)>m else 'unresolved')
                            for a,m in zip(paired[1],margin)]))
            snaps=rows[1]['snapshots']
            amp=max(max(t['amplitudes'][c][seed]) for t in snaps)
            phase=max(t['physical_domain'][c][seed][3] for t in snaps)
            rel=max(abs(t['physical_domain'][c][seed][6]) for t in snaps)
            relsq=max(t['physical_domain'][c][seed][7] for t in snaps)
            flags.append(dict(case=c,seed=seed,maximum_linear_amplitude=amp,small_perturbation=amp<.01,
                maximum_linear_phase_domain_fraction=phase,inside_linear_phase_domain=phase<1,
                maximum_relative_velocity=rel,small_relative_velocity=rel<.01,
                maximum_relative_square_over_phase_gap=relsq,
                sampled_basis_amplitude_ceiling=min(.01*SEED/amp if amp else 1.,SEED/phase if phase else 1.),
                scope='65 samples, linear heads; relative-square diagnostic is not a full nonlinear certificate'))
    status='ARITHMETIC_PASS' if all(g['passed'] for g in gates) else 'ARITHMETIC_FAILED'
    result=dict(manifest=manifest,trials=rows,numerical_gates=gates,status=status,
                all_numerical_gates_passed=status=='ARITHMETIC_PASS',physical_names=PHYSICAL_NAMES,
                fluid_names=FLUID_NAMES,endpoints=endpoints,endpoint_effect_refinements=effects,
                physical_fixture_flags=flags,elapsed_seconds=time.monotonic()-start,
                scope='NEW constrained effective response basis; no primordial/data/galaxy/structure qualification')
    for path,h in dict(inputs,**READ_SEALS,**CREATED_SEALS).items():
        if sha(path)!=h: raise RuntimeError('Input/checkpoint seal changed; prefix preserved '+path)
    if sha(__file__)!=source_sha: raise RuntimeError('Source changed; publication refused')
    rsha=write_json(STEM+'_RESULT.json',result)
    lines=['# Constrained U/clock/gradient FLRW response V001','',
           'NEW uncompressed effective hypothesis; fixed physical inventory, Gcos/GN=.99, ONE matched GN.',
           'Exact-constraint basis seeds; no inherited stationary-galaxy, primordial or observational claim.','',
           f'Status {status}: {sum(g["passed"] for g in gates)}/{len(gates)} numerical gates PASS.',
           f'Present H / old Hstar: {bg1["h"]:.12g}.','',
           '| k/Mpc | omega/Hstar | basis | comoving db contrast | Weyl | polarization density |',
           '|---|---|---|---|---|---|']
    for row in endpoints:
        v=row['physical']
        lines.append(f'| {row["k_Mpc_inverse"]} | {row["omega_over_Hstar"]} | {row["seed"]} | {v[0]:.12g} | {v[5]:.12g} | {v[4]:.12g} |')
    lines+=['','All arms and signed failures are retained; physical phase/relative heads are separate sampled diagnostics.',
            'omega=.1 paired effects are an inertia comparison, not a GR or mode-off reference.']
    report=BASE/(STEM+'_REPORT.md')
    with report.open('x') as f:f.write('\n'.join(lines)+'\n')
    report.chmod(0o444)
    report_sha=sha(report)
    for path,h in dict(inputs,**READ_SEALS,**CREATED_SEALS).items():
        if sha(path)!=h: raise RuntimeError('Post-output sealed bytes changed '+path)
    if sha(__file__)!=source_sha: raise RuntimeError('Post-output source changed')
    journal('OWNER_COMPLETE',status=status,result_sha256=rsha,gates=len(gates),passed=sum(g['passed'] for g in gates))
    write_json(STEM+'_RECEIPT.json',dict(lineage=lineage,status=status,manifest_sha256=sha(mp),
        result_sha256=rsha,report_sha256=report_sha,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),
        checkpoint_seals={p:h for p,h in dict(READ_SEALS,**CREATED_SEALS).items() if '_CP_' in p}))
    print(json.dumps(dict(status=status,passed=sum(g['passed'] for g in gates),total=len(gates),
         result_sha256=rsha,elapsed_seconds=result['elapsed_seconds'])),flush=True)
    return 0 if status=='ARITHMETIC_PASS' else 3


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute: raise SystemExit('Refusing numerical work without explicit --execute')
    try:
        raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write_json(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',
            error=repr(exc),pid=os.getpid(),time=now()))
        raise

