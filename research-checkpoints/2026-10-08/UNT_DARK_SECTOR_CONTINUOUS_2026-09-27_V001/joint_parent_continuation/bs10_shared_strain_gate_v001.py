#!/usr/bin/env python3
"""New sealed-array strain/source gate; no producer run or diagonalization."""
from __future__ import annotations
from datetime import datetime, timezone
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=J/'BS10_SHARED_STRAIN_GATE_V001.md'
SOURCE=J/'bs10_shared_strain_gate_v001.py'
RESULT=J/'BS10_SHARED_STRAIN_GATE_V001_RESULT.json'
REPORT=J/'BS10_SHARED_STRAIN_GATE_V001_RESULT.md'
CP=J/'bs10_shared_strain_gate_v001_checkpoints'
OLD_SOURCE=J/'bs10_two_record_formation_v001.py'
OLD_RESULT=J/'BS10_TWO_RECORD_FORMATION_V001_RESULT.json'
OLD_CP=J/'bs10_two_record_formation_v001_checkpoints'
OLD_SOURCE_SHA='41843d768cde60d3a5404cc1db3e6bd799eb8aa0778856c2d7e020a7bce74428'
OLD_RESULT_SHA='d90a5ff3fd1d6b9a8a536cce762c5104b8ec9cbccf9d3ef0e6289c082ed95cbc'
GS=(0.,.1); STRETCHES=(.75,1.,2.); DELAYS=(.1,.5,1.)
STARTS=(21,42); AGES=(0.,1.,2.,5.,10.,20.,50.)
MAX_RSS=512*1024*1024; OP_TOL=1e-11; SAVE_TOL=2e-10
IDENTITY_TOL=3e-9; KICK_TOL=3e-6; KICK=1e-6; STRAIN_STEP=1e-5
ENV_KEYS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
def exclusive(p,o):
    with p.open('x',encoding='utf-8') as f:
        json.dump(o,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def rss(): return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def journal(event,**kw):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=event,pid=os.getpid(),utc=utc(),**kw),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def check(dst,name,ok,evidence=None):
    dst.append(dict(name=name,passed=bool(ok),**({} if evidence is None else {'evidence':evidence})))
def close(np,dst,name,a,b,tol=IDENTITY_TOL):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    lim=tol*(1+max(float(np.max(np.abs(a))),float(np.max(np.abs(b)))))
    check(dst,name,err<=lim,dict(error=err,tolerance=lim))
def canonical(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def save_checkpoint(name,obj,t0):
    obj['elapsed_seconds']=time.monotonic()-t0;obj['peak_RSS_bytes']=rss()
    p=CP/(name+'.json');exclusive(p,obj)
    journal('row_complete',path=str(p),sha256=sha(p),elapsed_seconds=obj['elapsed_seconds'],peak_RSS_bytes=obj['peak_RSS_bytes'])
    print(json.dumps(dict(checkpoint=name,elapsed_seconds=obj['elapsed_seconds'],peak_RSS_bytes=obj['peak_RSS_bytes'])),flush=True)
    if obj['peak_RSS_bytes']>=MAX_RSS: raise MemoryError('Frozen RSS gate reached; subsequent rows stopped')

def authenticate():
    if sha(OLD_SOURCE)!=OLD_SOURCE_SHA or sha(OLD_RESULT)!=OLD_RESULT_SHA: raise RuntimeError('Original producer/result seal changed')
    old=json.loads(OLD_RESULT.read_text())
    if old['status']!='QUALIFIED_ARITHMETIC': raise RuntimeError('Original receipt not qualified')
    paths={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE),str(OLD_RESULT):sha(OLD_RESULT)}
    for p,h in old['input_sha256'].items():
        if sha(Path(p))!=h: raise RuntimeError('Original anchor changed: '+p)
        paths[p]=h
    events=[json.loads(line) for line in (OLD_CP/'events.jsonl').read_text().splitlines() if line]
    paths[str(OLD_CP/'manifest.json')]=sha(OLD_CP/'manifest.json');paths[str(OLD_CP/'events.jsonl')]=sha(OLD_CP/'events.jsonl')
    groups=[]
    for gi,g in enumerate(GS):
        p=OLD_CP/f'g{gi}.json';d=json.loads(p.read_text());ep=Path(d['eigensystem_path'])
        if d['g']!=g or sha(ep)!=d['eigensystem_sha256']: raise RuntimeError('Saved eigensystem changed')
        if d['failed_count']!=0 or not any(e.get('event')=='Hamiltonian_complete' and e.get('key')==f'g{gi}' and e.get('sha256')==sha(p) and e.get('failed')==0 for e in events): raise RuntimeError('No original qualified g-summary journal seal')
        if not any(e.get('event')=='eigensystem_saved' and e.get('sha256')==d['eigensystem_sha256'] for e in events): raise RuntimeError('No original eigensystem journal seal')
        paths[str(p)]=sha(p);paths[str(ep)]=sha(ep);states=[]
        for n in STARTS:
            for ti,t in enumerate(AGES):
                sp=OLD_CP/f'g{gi}_n{n}_main{ti}.json';sd=json.loads(sp.read_text());ap=Path(sd['state_path'])
                if sd['g']!=g or sd['start']!=n or sd['tau']!=t or sha(ap)!=sd['state_sha256'] or sd['eigensystem_sha256']!=d['eigensystem_sha256']: raise RuntimeError('Saved prepared state changed')
                if sd['failed_count']!=0: raise RuntimeError('Original state arithmetic not qualified')
                if not any(e.get('event')=='state_complete' and e.get('sha256')==sha(sp) for e in events): raise RuntimeError('No original state journal seal')
                paths[str(sp)]=sha(sp);paths[str(ap)]=sha(ap);states.append((sd,ap))
        groups.append((d,ep,states))
    return paths,groups

def kernel(np,matrices,c,E,t):
    phase=np.exp(-1j*E*t);wc=[a@c for a in matrices];ac=[a@(phase*c) for a in matrices]
    return np.array([[2*np.imag(np.vdot(ac[i],phase*wc[j])) for j in range(len(matrices))] for i in range(len(matrices))])
def components(np,k): return k[:2,:2],k[:2,2:]+k[2:,:2],k[2:,2:]
def static(np,D,E):
    gap=E[1:]-E[0];v=np.stack([a[1:,0] for a in D],axis=1)
    full=2*(v.T/gap)@v
    return full,components(np,full)
def impulse_derivative(np,D,c,E,t,axis):
    phase=np.exp(-1j*E*t);v=D[axis]@c;vv=D[axis]@v
    plus=phase*(c-1j*KICK*v-KICK*KICK*vv/2);minus=phase*(c+1j*KICK*v-KICK*KICK*vv/2)
    plus/=np.linalg.norm(plus);minus/=np.linalg.norm(minus)
    return np.array([(np.real(np.vdot(plus,a@plus))-np.real(np.vdot(minus,a@minus)))/(2*KICK) for a in D])

def execute(np,groups,checks,t0):
    spec=importlib.util.spec_from_file_location('sealed_bs10_pure_helpers',OLD_SOURCE)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    b=old.basis(np);allrows=[];coldrows=[]
    for gi,(meta,ep,states) in enumerate(groups):
        g=GS[gi];journal('group_started',g=g)
        H,G,parts,degree=old.build(np,g,b)
        for name,a in [('H',H),('Gx',G[0]),('Gy',G[1])]:
            check(checks,f'g{gi}_sealed_matrix_{name}',old.matrix_sha(np,a)==meta['matrix_sha256'][name])
        with np.load(ep,allow_pickle=False) as z:
            E=z['complete_eigenvalues'];V=z['eigenvectors_columns']
            check(checks,f'g{gi}_embedded_matrix_hashes',json.loads(str(z['matrix_sha256_json']))==meta['matrix_sha256'])
            check(checks,f'g{gi}_embedded_input_hashes',json.loads(str(z['input_sha256_json']))==meta['input_sha256'])
        res=orth=0.;scale=max(1.,float(np.max(np.sum(np.abs(H),axis=1))))
        for a in range(0,len(E),128):
            stop=min(a+128,len(E));v=V[:,a:stop]
            res=max(res,float(np.max(np.abs(H@v-v*E[a:stop]))));vprod=V.T@v
            vprod[np.arange(a,stop),np.arange(stop-a)]-=1
            orth=max(orth,float(np.max(np.abs(vprod))))
        check(checks,f'g{gi}_full_saved_eigen_residual',res<=SAVE_TOL*scale,dict(error=res,tolerance=SAVE_TOL*scale))
        check(checks,f'g{gi}_saved_orthogonality',orth<=SAVE_TOL,dict(error=orth))
        check(checks,f'g{gi}_unique_ground',float(E[1]-E[0])>1e-10,dict(gap=float(E[1]-E[0])))
        check(checks,f'g{gi}_supported_Hint_bound',float(E[0]-1)>=5.45-g-SAVE_TOL)
        car=[b['pos'][b['carrier'],i].copy() for i in range(2)]
        rest=[G[i].copy() for i in range(2)]
        for i in range(2):rest[i][b['rows'],b['rows']]-=car[i]
        D=[V.T@(car[i][:,None]*V) for i in range(2)]+[V.T@rest[i]@V for i in range(2)]
        for i in range(4):check(checks,f'g{gi}_source_{i}_Hermitian',float(np.max(np.abs(D[i]-D[i].T)))<=OP_TOL)
        # Independent complete lapse construction, retaining every term.
        for s in STRETCHES:
            Hs=H/s;Hs[b['rows'],b['rows']]+=1-1/s
            lapse=np.full(12,.93);Ccar=.93*np.ones(len(E));weighted=old.weighted(np,g,b,lapse)/s
            weighted[b['rows'],b['rows']]+=(1-1/s)*Ccar
            close(np,checks,f'g{gi}_s{s}_uniform_lapse',weighted,.93*Hs,OP_TOL)
            eta=np.array([1e-6,-2e-6]);lapse=1+s*b['allpos']@eta
            check(checks,f'g{gi}_s{s}_positive_lapse',float(np.min(lapse))>0)
            weighted=old.weighted(np,g,b,lapse)/s
            Ccar=lapse[b['carrier']]
            weighted[b['rows'],b['rows']]+=(1-1/s)*Ccar
            expected=Hs+eta[0]*(G[0]+(s-1)*np.diag(car[0]))+eta[1]*(G[1]+(s-1)*np.diag(car[1]))
            close(np,checks,f'g{gi}_s{s}_whole_affine_source',weighted,expected,OP_TOL)
            for i in range(2):
                plus=(s+STRAIN_STEP)*D[i]+D[i+2];minus=(s-STRAIN_STEP)*D[i]+D[i+2]
                close(np,checks,f'g{gi}_s{s}_mixed_contact_{i}',(plus-minus)/(2*STRAIN_STEP),D[i])
            del Hs,weighted,expected
        del H,G,rest,parts,degree;gc.collect()
        full,(cc,cross,rr)=static(np,D,E)
        cold=dict(g=g,complete_ground_energy=float(E[0]),first_gap=float(E[1]-E[0]),u=float(E[0]-1),S_car=cc.tolist(),S_cross=cross.tolist(),S_rest=rr.tolist(),stretches=[],checks=[])
        for s in STRETCHES:
            Ds=[s*D[i]+D[i+2] for i in range(2)];gap=(E[1:]-E[0])/s
            v=np.stack([a[1:,0] for a in Ds],axis=1);direct=2*(v.T/gap)@v/s**3
            pred=cc+cross/s+rr/s**2
            close(np,cold['checks'],f'cold_s{s}_full_static_scaling',direct,pred)
            ev=np.linalg.eigvalsh(direct)
            check(cold['checks'],f'cold_s{s}_static_PSD',float(ev[0])>=-IDENTITY_TOL*(1+float(np.max(np.abs(direct)))))
            u=cold['u'];p=u/(3*s**4);energy=1+u/s
            check(cold['checks'],f'cold_s{s}_positive_pressure',p>0)
            cold['stretches'].append(dict(s=s,E=energy,rho=energy/s**3,p=p,rho_plus_3p=(1+2*u/s)/s**3,S=direct.tolist(),S_eigenvalues=ev.tolist()))
        save_checkpoint(f'g{gi}_cold',cold,t0);coldrows.append(cold)
        for state,ap in states:
            n=int(state['start']);age=float(state['tau']);rowchecks=[]
            with np.load(ap,allow_pickle=False) as z:
                psi=z['complete_state'];check(rowchecks,'embedded_state_ownership',int(z['start'])==n and float(z['tau'])==age and float(z['g'])==g and str(z['eigensystem_sha256'])==meta['eigensystem_sha256'])
                check(rowchecks,'embedded_original_inputs',json.loads(str(z['input_sha256_json']))==state['input_sha256'])
            c=V.T@psi;seed=n*24;expected=V@(np.exp(-1j*E*age)*V[seed,:])
            close(np,rowchecks,'saved_exact_prepared_state',psi,expected,SAVE_TOL)
            check(rowchecks,'saved_state_norm',abs(float(np.vdot(c,c).real)-1)<=SAVE_TOL)
            energy=float(np.sum(np.abs(c)**2*E));u=energy-1
            close(np,rowchecks,'saved_complete_energy',energy,float(state['complete_energy']),SAVE_TOL)
            close(np,rowchecks,'retained_history_energy',energy,float(state['initial_complete_energy']),SAVE_TOL)
            check(rowchecks,'positive_retained_interaction_energy',u>=5.45-g-SAVE_TOL)
            row=dict(g=g,start=n,age=age,state_sha256=state['state_sha256'],u=u,record_mean=state['record_mean'],work=[],response=[],checks=rowchecks)
            for s in STRETCHES:
                Es=1+(E-1)/s;Ds=[s*D[i]+D[i+2] for i in range(2)]
                energy_s=float(np.sum(np.abs(c)**2*Es));p=u/(3*s**4)
                close(np,rowchecks,f's{s}_exact_work_energy',energy_s,1+u/s)
                h=STRAIN_STEP;fd=(1+u/(s+h)-(1+u/(s-h)))/(2*h)
                close(np,rowchecks,f's{s}_strain_work_derivative',fd,-u/s**2)
                check(rowchecks,f's{s}_positive_pressure',p>0)
                row['work'].append(dict(s=s,E=energy_s,rho=energy_s/s**3,p=p,rho_plus_3p=(1+2*u/s)/s**3,deltaE_from_s1=u*(1/s-1)))
                for delay in DELAYS:
                    k=kernel(np,D,c,E,delay/s);kc,kcross,kr=components(np,k)
                    pred=kc/s+kcross/s**2+kr/s**3
                    direct=kernel(np,Ds,c,Es,delay)/s**3
                    close(np,rowchecks,f's{s}_t{delay}_causal_scaling',direct,pred)
                    if delay==DELAYS[0]:
                        k0=kernel(np,Ds,c,Es,0)
                        close(np,rowchecks,f's{s}_zero_delay_antisymmetry',k0+k0.T,np.zeros((2,2)))
                        close(np,rowchecks,f's{s}_zero_delay_diagonal',np.diag(k0),np.zeros(2))
                    if n==21 and age in (0.,50.) and delay==.1:
                        for axis in range(2):close(np,rowchecks,f's{s}_plus_impulse_sign_axis{axis}',impulse_derivative(np,Ds,c,Es,delay,axis)/s**3,direct[:,axis],KICK_TOL)
                    row['response'].append(dict(s=s,delay=delay,plus_source_kernel_density=direct.tolist(),car_component=(kc/s).tolist(),cross_component=(kcross/s**2).tolist(),rest_component=(kr/s**3).tolist()))
                # Energy conservation holds for arbitrary source-off time at this stretch.
                after=np.exp(-1j*Es*DELAYS[-1])*c
                close(np,rowchecks,f's{s}_source_off_u_conserved',float(np.sum(np.abs(after)**2*(E-1))),u)
            save_checkpoint(f'g{gi}_n{n}_age{int(age)}',row,t0);allrows.append(row)
        # Actual original-state C2 reflection controls; never impose isotropy.
        parity=np.diag([1.,-1.])
        for age in AGES:
            a=next(r for r in allrows if r['g']==g and r['start']==21 and r['age']==age)
            z=next(r for r in allrows if r['g']==g and r['start']==42 and r['age']==age)
            close(np,checks,f'g{gi}_age{age}_reflected_work',a['u'],z['u'])
            for ri,(ar,zr) in enumerate(zip(a['response'],z['response'])):
                close(np,checks,f'g{gi}_age{age}_response{ri}_C2',np.array(zr['plus_source_kernel_density']),parity@np.array(ar['plus_source_kernel_density'])@parity)
        del V,E,D;gc.collect();journal('group_complete',g=g,peak_RSS_bytes=rss())
    return coldrows,allrows

def main():
    t0=time.monotonic()
    if any(p.exists() for p in (RESULT,REPORT,CP)): raise RuntimeError('Exclusive output exists; no replay/resume authorized')
    if any(os.environ.get(k)!='1' for k in ENV_KEYS): raise RuntimeError('Frozen one-thread environment absent before NumPy import')
    paths,groups=authenticate();CP.mkdir()
    manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),utc=utc(),input_sha256=paths,environment={k:os.environ[k] for k in ENV_KEYS},inputs=dict(g=GS,s=STRETCHES,delays=DELAYS,starts=STARTS,ages=AGES,V0=1.,hbar_conditional=1.,peak_RSS_limit_bytes=MAX_RSS,no_diagonalization=True,no_producer_execution=True))
    exclusive(CP/'manifest.json',manifest);journal('started',manifest_sha256=sha(CP/'manifest.json'))
    print(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),manifest=str(CP/'manifest.json'),status='started')),flush=True)
    try:
        import numpy as np
        checks=[];cold,rows=execute(np,groups,checks,t0)
        allchecks=checks+[c for r in cold+rows for c in r['checks']]
        failed=[c for c in allchecks if not c['passed']]
        payload=dict(status='QUALIFIED_ARITHMETIC' if not failed else 'FAILED_ARITHMETIC',scientific_status='COUNTED_COMPLETION_HAS_POSITIVE_PRESSURE_NOT_ACCELERATION_OR_NATIVE_DICTIONARY',manifest=manifest,checks=checks,cold=cold,prepared_states=rows,passed_count=len(allchecks)-len(failed),failed_count=len(failed),failed_checks=failed,elapsed_seconds=time.monotonic()-t0,peak_RSS_bytes=rss(),pid=os.getpid())
        payload['canonical_payload_sha256']=canonical(payload);exclusive(RESULT,payload)
        journal('result_saved',sha256=sha(RESULT),canonical_payload_sha256=payload['canonical_payload_sha256'],status=payload['status'],peak_RSS_bytes=rss())
        with REPORT.open('x',encoding='utf-8') as f:
            f.write('# BS10 shared strain gate V001 — sealed result\n\n')
            f.write(f"Status: {payload['status']}; {payload['passed_count']}/{len(allchecks)} controls passed. Runtime {payload['elapsed_seconds']:.6f} s; peak RSS {payload['peak_RSS_bytes']/1048576:.3f} MiB. Worker PID {os.getpid()}.\n\n")
            f.write('This new gate reuses the two sealed 1536D eigensystems and all 28 already prepared main states. No diagonalization or old producer was executed. Whole nodal source, signed cross response, absolute carrier rest energy and record/support energies remain present.\n\n')
            f.write('The counted deformation is H_s=1+(H-1)/s, G_s=s Gcar+Grest, V=s^3 V0. It is an effective physical postulate, not an earned spatial metric, galaxy calibration, or observer-clock law. In each retained state E=1+u/s and p=u/(3V0 s^4)>0. Under the scoped supported bound u>=5.45-g, rho+3p>0. This completion supplies no accelerated expansion. It does not exclude every other native scaling.\n\n')
            for c in cold:
                f.write(f"g={c['g']}: cold u={c['u']:.12g}; first complete gap={c['first_gap']:.12g}. S_car={json.dumps(c['S_car'])}; S_cross={json.dumps(c['S_cross'])}; S_rest={json.dumps(c['S_rest'])}.\n\n")
            f.write('The positive cold static tensor obeys S(s)=S_car+S_cross/s+S_rest/s^2; S is the negative regulated time integral of the plus-source retarded kernel divided by volume. Signed prepared-state causal kernels instead obey their actual retarded commutator at the saved state, with delay t/s and density scaling 1/s,1/s^2,1/s^3. They are not replaced by cold/static susceptibilities. Only the actual C2 reflection relates ice starts; no three-dimensional isotropy is claimed. The source conversion and physical clock remain uncalibrated.\n\n')
            f.write('All completed cold/prepared-state rows have exclusive JSON checkpoints and journal seals. No job is left running by this script, no scheduler/resumption is installed, and no rerun is authorized by this receipt. The parent integrates conclusions into its current continuation log/ledger.\n\n')
            f.write(f"Raw result SHA256: {sha(RESULT)}\n\nCanonical payload SHA256: {payload['canonical_payload_sha256']}\n\nProtocol SHA256: {paths[str(PROTOCOL)]}\n\nSource SHA256: {paths[str(SOURCE)]}\n")
            if failed:f.write('\nFrozen failures preserved: '+json.dumps(failed)+'\n')
            f.flush();os.fsync(f.fileno())
        journal('report_saved',path=str(REPORT),sha256=sha(REPORT));print(json.dumps(dict(status=payload['status'],passed=payload['passed_count'],failed=payload['failed_count'],result_sha256=sha(RESULT),report_sha256=sha(REPORT),elapsed_seconds=payload['elapsed_seconds'],peak_RSS_bytes=payload['peak_RSS_bytes'])),flush=True)
        return 0 if not failed else 2
    except BaseException as e:
        err=dict(status='INTERRUPTED_OR_FAILED',error=repr(e),traceback=traceback.format_exc(),pid=os.getpid(),elapsed_seconds=time.monotonic()-t0,peak_RSS_bytes=rss())
        exclusive(CP/'error.json',err);journal('error',error_sha256=sha(CP/'error.json'));print(json.dumps(err),flush=True);return 3

if __name__=='__main__':sys.exit(main())
