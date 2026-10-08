"""Saved-array algebra/custody only. No EOS, quadrature, RHS or integrator calls.

Stdout only; root/agent publishes the resulting audit receipt separately.
Spatial comparisons are descriptive, never an invented continuum pass gate.
"""
import base64
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
FILES={}
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def read(p):
    p=Path(p);p.relative_to(ROOT)
    for q in (p,*p.parents):
        if q==ROOT.parent:break
        if q.is_symlink():raise RuntimeError('Linked input')
    raw=p.read_bytes();FILES[str(p.relative_to(ROOT))]=sha(raw);return raw
def load(p):return json.loads(read(p))
def wrapper(p,freeze=None):
    w=load(p)
    assert sha(enc(w['payload']))==w['payload_sha256'],str(p)
    if freeze is not None:assert w['freeze_sha256']==freeze,str(p)
    return w['payload']
class Checks:
    def __init__(self):self.count=0;self.maxima={};self.failures=[]
    def eq(self,name,a,b=0.,tol=2e-11,scale=None):
        a=np.asarray(a);b=np.asarray(b)
        if scale is None:scale=np.maximum(1.,np.maximum(abs(a),abs(b)))
        e=abs(a-b)/np.maximum(abs(scale),1e-300);self.count+=e.size
        v=float(np.max(e)) if np.all(np.isfinite(e)) else None
        if v is not None:self.maxima[name]=max(self.maxima.get(name,0.),v)
        if v is None or v>tol:self.failures.append(dict(check=name,error=v,tolerance=tol))
def massfaces(m):return np.r_[(m[:-1]+m[1:])/2,m[-1]/2]
def volumes(x):return 4*math.pi*np.diff(x**3)/3
def seed(x):
    z=np.minimum(x,1.);return np.where(x<1,3465/128*(z**3/3-4*z**5/5+6*z**7/7-4*z**9/9+z**11/11),1.)


def gravity_algebra(species,qbar,A):
    """Exact elementary integrals of the SAVED piecewise-constant densities.

    Independent algebraic reconstruction, not a field solve or trajectory.
    Self potential -M(<r)/r-4pi integral_r^R rho*s ds; background counted once.
    """
    kind=np.longdouble
    xs=[np.asarray(s['faces'],dtype=kind) for s in species]
    ms=[np.asarray(s['cell_masses_over_M'],dtype=kind) for s in species]
    grid=np.unique(np.concatenate(xs));a=grid[:-1];b=grid[1:];mid=(a+b)/2
    densities=[m/(4*math.pi*np.diff(x**3)/3) for x,m in zip(xs,ms)]
    rho=np.zeros(len(a),dtype=kind)
    for x,q in zip(xs,densities):
        k=np.minimum(np.searchsorted(x,mid)-1,len(q)-1)
        rho+=np.where(mid<x[-1],q[k],0.)
    shell=4*math.pi*rho*(b**3-a**3)/3
    ml=np.r_[kind(0),np.cumsum(shell)[:-1]]
    outer=np.r_[np.cumsum((2*math.pi*rho*(b*b-a*a))[::-1])[::-1][1:],kind(0)]
    # On each interval, phi_self = constant - B/r + D*r^2.
    B=ml-4*math.pi*rho*a**3/3
    constant=-outer-2*math.pi*rho*b*b
    D=2*math.pi*(rho-kind(qbar))/3
    right=constant-B/b+D*b*b
    potential=np.r_[constant[0],right]
    integral=constant*(b**3-a**3)/3-B*(b*b-a*a)/2+D*(b**5-a**5)/5
    prim=np.r_[kind(0),np.cumsum(integral)]
    W=kind(0);forces=[]
    for x,m,q in zip(xs,ms,densities):
        indices=np.searchsorted(grid,x);vol=4*math.pi*np.diff(x**3)/3
        avg=4*math.pi*np.diff(prim[indices])/vol
        bgavg=-(2*math.pi*kind(qbar)/3)*(3/5)*(x[1:]**5-x[:-1]**5)/(x[1:]**3-x[:-1]**3)
        W+=np.dot(m,avg+bgavg)/2
        pf=potential[indices][1:]
        derivative=4*math.pi*x[1:]**2*(q*(pf-avg)+np.r_[q[1:]*(avg[1:]-pf[:-1]),kind(0)])
        forces.append(np.asarray(-derivative/(A*A*massfaces(m)),dtype=float))
    return float(W/A),forces,float(np.max(potential)-np.min(potential))/A


def compare_method(p,ck):
    n=p['case']['cells'];m=[np.array(p['samples'][0]['species'][s]['cell_masses_over_M']) for s in ['baryon','hard']]
    fm=list(map(massfaces,m));units=np.ones(1+4*n+10)
    units[1+n:1+2*n]=1/fm[0];units[1+3*n:1+4*n]=1/fm[1];units[1+4*n+7:]=1/sum(m[1])
    maxes={};v0=volumes(np.linspace(0,p['case']['L'],n+1))
    def metric(name,a,b,tol):
        aa=np.asarray(a);bb=np.asarray(b);e=float(np.max(abs(aa-bb)/np.maximum(1.,np.maximum(abs(aa),abs(bb)))))
        maxes[name]=max(maxes.get(name,0.),e);ck.eq('reproduced_'+name,a,b,tol)
    for i,f in enumerate(p['method_vectors']['RK4_fine']):
        f=np.array(f)
        for name in ['RK4_coarse','DOPRI54']:
            g=np.array(p['method_vectors'][name][i]);metric('time_state',g*units,f*units,2e-8)
            for sp in range(2):
                k=1+2*sp*n;xf=np.r_[0.,f[k:k+n]];xg=np.r_[0.,g[k:k+n]]
                metric('time_velocity',g[k+n:k+2*n]/(g[0]*fm[sp]),f[k+n:k+2*n]/(f[0]*fm[sp]),2e-7)
                metric('time_volume_ratio',volumes(xg)/v0,volumes(xf)/v0,2e-7)
                if sp==1:metric('time_action_ratio',v0/volumes(xg),v0/volumes(xf),2e-7)
    for name,val in maxes.items():ck.eq('producer_maximum_'+name,val,p['worst_errors'][name])
    return maxes


def profile(p,s,sp,width):
    """Restrict cell integrals to common original labels, never extrapolate."""
    d=s['species'][sp];factor=round(width/p['case']['dx']);n=round(4/p['case']['dx']);nf=n//factor
    x=np.array(d['faces'][:n+1]);v=np.r_[0.,d['peculiar_v_over_vdyn'][:n]]
    m=np.array(d['cell_masses_over_M'][:n]);V=volumes(x)
    group=lambda y:np.asarray(y).reshape(nf,factor).sum(axis=1)
    xx=x[::factor];vv=v[::factor];labels=np.arange(nf+1)*width
    q=group(m)/group(V);q0=p['units']['q_'+sp+'_background']
    z=dict(displacement=xx-labels,velocity=vv,density=q,density_contrast=q/q0-1.,enclosed_mass=np.r_[0.,np.cumsum(group(m))])
    if sp=='hard':
        for key,raw in [('pressure',s['hard_pressure_dimensionless']),('action_ratio',s['action_ratio'])]:
            z[key]=group(np.array(raw[:n])*V)/group(V)
    return z


def norms(diff,reference,weights):
    diff=np.asarray(diff);reference=np.asarray(reference);weights=np.asarray(weights)
    rms=float(np.sqrt(np.dot(weights,diff*diff)/sum(weights)))
    signal=float(np.sqrt(np.dot(weights,reference*reference)/sum(weights)))
    return dict(signed_min=float(np.min(diff)),signed_max=float(np.max(diff)),max_absolute=float(np.max(abs(diff))),
                weighted_rms=rms,reference_rms=signal,relative_rms=None if signal==0 else rms/signal)


def comparison(a,b,width,label):
    result=[];grid=np.arange(round(4/width)+1)*width;wc=volumes(grid);wf=np.r_[wc[0]/2,(wc[:-1]+wc[1:])/2,wc[-1]/2]
    for sa,sb in zip(a['samples'],b['samples']):
        row=dict(tau=sa['tau'],fields={})
        for sp in ['baryon','hard']:
            aa=profile(a,sa,sp,width);bb=profile(b,sb,sp,width)
            for key in aa:
                weight=wf if len(aa[key])==len(wf) else wc
                row['fields'][sp+'_'+key]=norms(aa[key]-bb[key],bb[key],weight)
        result.append(row)
    return dict(kind=label,case_a=a['case']['case_index'],case_b=b['case']['case_index'],
                common_original_label_width=width,watch_label_max=4.,comparison_pass_gate=None,epochs=result)


def enclosed(s,sp,r):
    d=s['species'][sp];x=np.asarray(d['faces']);m=np.asarray(d['cell_masses_over_M'])
    fraction=np.maximum(0.,np.minimum(1.,(r**3-x[:-1]**3)/(x[1:]**3-x[:-1]**3)))
    return float(np.dot(m,fraction))


def audit_case(p,ck):
    case=p['case'];n=case['cells'];u=p['units'];eps=u['epsilon'];R=case['gap'];x0=np.linspace(0,case['L'],n+1);v0=volumes(x0)
    m=[np.asarray(p['samples'][0]['species'][sp]['cell_masses_over_M']) for sp in ['baryon','hard']]
    ck.eq('baryon_initial_mass',m[0],np.diff(seed(x0))+u['q_baryon_background']*v0)
    ck.eq('hard_initial_mass',m[1],u['q_hard_background']*v0,scale=np.maximum(abs(m[1]),1e-300))
    ck.eq('unit_seed_mass',sum(m[0]-u['q_baryon_background']*v0),1.)
    fm=list(map(massfaces,m));initial=p['samples'][0];physical=[]
    for it,s in enumerate(p['samples']):
        A=s['A'];K=[];y=np.asarray(p['method_vectors']['RK4_fine'][it]);ck.eq('snapshot_A',A,y[0]);ck.eq('snapshot_ledger',s['ledger'],y[1+4*n:])
        for spidx,sp in enumerate(['baryon','hard']):
            d=s['species'][sp];x=np.array(d['faces']);v=np.array(d['peculiar_v_over_vdyn']);V=volumes(x);q=m[spidx]/V
            ck.eq('mass_fixed',d['cell_masses_over_M'],m[spidx],scale=np.maximum(abs(m[spidx]),1e-300))
            ck.eq('density_geometry',q,d['comoving_density'],scale=np.maximum(abs(q),1e-300))
            ck.eq('volume_ratio',V/v0,d['volume_ratio']);ck.eq('enclosed_mass',np.r_[0.,np.cumsum(m[spidx])],d['enclosed_mass_over_M'])
            ck.eq('velocity_gradient',np.diff(np.r_[0.,v])/np.diff(x),d['face_velocity_radial_gradient'])
            ck.eq('density_gradient',np.diff(np.log(q))/np.diff((x[:-1]+x[1:])/2),d['log_density_radial_gradient'])
            off=1+2*spidx*n;ck.eq('snapshot_faces',x[1:],y[off:off+n]);ck.eq('snapshot_velocity',v,y[off+n:off+2*n]/(A*fm[spidx]))
            K.append(.5*float(np.dot(fm[spidx],v*v)))
        ck.eq('kinetic_species',K,s['K_species']);ck.eq('kinetic_total',sum(K),s['K'])
        mat={k:np.array(v) for k,v in s['hard_material'].items()};I=mat['I'];e=mat['e'];pressure=mat['p'];omega=mat['omega']
        q=np.array(s['species']['hard']['comoving_density']);ck.eq('action_ratio',q/u['q_hard_background'],s['action_ratio'])
        ck.eq('physical_action',p['source_state']['I']*q/(u['q_hard_background']*A**3),I,2e-10,abs(I))
        ck.eq('recovered_action',mat['action_recovered'],I,2e-10,abs(I))
        ck.eq('enthalpy',I*omega,e+pressure,2e-10,abs(e+pressure))
        ck.eq('stable_internal_identity',mat['dE'],mat['dW']-pressure/(R*I),2e-10,np.maximum(abs(mat['dE']),1e-300))
        ck.eq('sound_identity',mat['cN_c2'],omega/R*mat['cI2'],2e-10,np.maximum(abs(mat['cN_c2']),1e-300))
        ck.eq('sound_bound_excess',np.maximum(0.,mat['cN_c2']*R**3/I-1.),0.)
        P=q*pressure/(R*I*eps);ck.eq('pressure_normalization',P,s['hard_pressure_dimensionless'],2e-10,np.maximum(abs(P),1e-300))
        x=np.array(s['species']['hard']['faces']);kick=4*math.pi*x[1:]**2*(P-np.r_[P[1:],s['background_pressure']])
        ck.eq('pressure_acceleration',kick/(A*fm[1]),s['hard_pressure_acceleration_over_gstar'])
        U=float(np.dot(m[1],mat['dE']))/eps;ck.eq('internal_energy',U,s['U']);ck.eq('excess_internal',s['U']-s['Ubar'],s['U_excess'])
        ck.eq('internal_omission',mat['dE'],s['hard_gravity_omission_internal_over_rest'])
        ck.eq('active_omission',mat['dE']+3*pressure/(R*I),s['hard_gravity_omission_active_over_rest'])
        W,acc,span=gravity_algebra([s['species'][sp] for sp in ['baryon','hard']],u['q_baryon_background']+u['q_hard_background'],A)
        ck.eq('gravity_energy_saved_geometry',W,s['W']);ck.eq('potential_span',span*eps,s['potential_span_over_c2'])
        for i,sp in enumerate(['baryon','hard']):ck.eq('gravity_force_saved_geometry',acc[i],s['species'][sp]['gravity_acceleration_over_gstar'])
        ledger=s['ledger'];E=s['K']+s['U']+s['W'];E0=initial['K']+initial['U']+initial['W']
        ck.eq('total_energy_work',E-E0,ledger[4],2e-7)
        ck.eq('mechanical_work',s['K']+s['U']-initial['K']-initial['U'],sum(ledger[:3]),2e-7)
        hardE=s['K_species'][1]+s['U']-initial['K_species'][1]-initial['U']
        ck.eq('hard_specific_work',hardE/sum(m[1]),ledger[9]/sum(m[1]),2e-7)
        ck.eq('baryon_work',s['K_species'][0]-initial['K_species'][0],ledger[0]-ledger[7]+ledger[2]-ledger[8],2e-7)
        massread=[]
        for r in [.25,.5,1.,2.,4.]:
            mh=enclosed(s,'hard',r)-u['q_hard_background']*4*math.pi*r**3/3
            mb=enclosed(s,'baryon',r)-u['q_baryon_background']*4*math.pi*r**3/3
            massread.append(dict(comoving_radius_over_ell=r,hard_excess_mass_over_seed=mh,baryon_excess_mass_over_seed=mb,
                                 ratio=None if mb==0 else mh/mb))
        physical.append(dict(tau=s['tau'],seconds=s['seconds'],A=A,hard_action_ratio_range=[float(min(s['action_ratio'])),float(max(s['action_ratio']))],
            hard_velocity_range=[float(min(s['species']['hard']['peculiar_v_over_vdyn'])),float(max(s['species']['hard']['peculiar_v_over_vdyn']))],
            baryon_velocity_range=[float(min(s['species']['baryon']['peculiar_v_over_vdyn'])),float(max(s['species']['baryon']['peculiar_v_over_vdyn']))],
            hard_pressure_acceleration_max=float(max(abs(np.asarray(s['hard_pressure_acceleration_over_gstar'])))),
            hard_gravity_acceleration_max=float(max(abs(np.asarray(s['species']['hard']['gravity_acceleration_over_gstar'])))),
            minimum_volume_ratio=min(min(s['species'][sp]['volume_ratio']) for sp in ['hard','baryon']),
            K=s['K'],U=s['U'],U_excess=s['U_excess'],W=s['W'],hard_specific_mechanical_change=hardE/sum(m[1]),
            max_internal_over_rest=float(max(mat['dE'])),max_active_over_rest=float(max(s['hard_gravity_omission_active_over_rest'])),
            mass_at_fixed_comoving_radii=massread))
    time_errors=compare_method(p,ck)
    return dict(case=case,status=p['status'],producer_checks=sum(p['checks'].values()),producer_seconds=p['seconds'],
                producer_self_rss_bytes=p['peak_self_rss_bytes'],time_error_reproduction=time_errors,
                saved_gradient_control_maxima={k:v for k,v in p['worst_errors'].items() if 'gradient' in k},
                gradient_fd_reexecution=False,primary_readouts=physical)


def main():
    if Path.cwd().resolve()!=ROOT:raise RuntimeError('Wrong root')
    ck=Checks();sfraw=read(J/'SPHERICAL_TWO_CURRENT_V001_FROZEN.json');sf=json.loads(sfraw);sfsha=sha(sfraw)
    cfraw=read(J/'SPHERICAL_TWO_CURRENT_SUPERVISOR_V001_FROZEN.json');cf=json.loads(cfraw);cfsha=sha(cfraw)
    assert cf['producer_freeze_sha256']==sfsha
    for group in [sf['files'],cf['controller_inputs']['files']]:
        for path,h in group.items():assert sha(read(ROOT/path))==h,path
    frraw=read(J/'SPHERICAL_TWO_CURRENT_V001_FREEZE_RUN.json');assert sha(frraw)==cf['freeze_invocation_receipt_sha256']
    fr=wrapper(J/'SPHERICAL_TWO_CURRENT_V001_FREEZE_RUN.json');assert base64.b64decode(fr['invocation']['stdout_base64'],validate=True)==sfraw
    wrapper(J/'SPHERICAL_TWO_CURRENT_V001_FREEZE_INTENT.json')
    cases={};summaries=[];missing=[];incomplete=[]
    for i in range(12):
        base='SPHERICAL_TWO_CURRENT_V001_CASE_'+format(i,'03d');path=J/(base+'.json')
        if not path.exists():missing.append(i);continue
        raw=read(path);p=wrapper(path,sfsha);assert p['case']==sf['cases'][i]
        run=wrapper(J/(base+'_RUN.json'),cfsha);intent=wrapper(J/(base+'_INTENT.json'),cfsha)
        assert intent['case_index']==i and intent['case']==p['case'] and run['case_index']==i and run['case']==p['case']
        inv=run['invocation'];assert base64.b64decode(inv['stdout_base64'],validate=True)==raw and inv['stdout_sha256']==sha(raw) and inv['stdout_bytes']==len(raw)
        err=base64.b64decode(inv['stderr_base64'],validate=True);assert sha(err)==inv['stderr_sha256'] and len(err)==inv['stderr_bytes']
        assert inv['argv']==intent['argv'] and run['producer_freeze_sha256']==sfsha
        complete=p['status']=='COMPLETE_FINITE_R_NUMERICAL_CASE' and not p['failures'] and run['status']=='CASE_COMPLETE'
        if not complete:incomplete.append(dict(case_index=i,scientific_status=p['status'],custody_status=run['status'],failures=p['failures']));continue
        assert inv['returncode']==0 and inv['stop_reason'] is None and inv['exception'] is None and not inv['resource_monitor_errors']
        assert inv['sampled_process_group_peak_rss_bytes']<=cf['controller_inputs']['configuration']['sampled_process_group_rss_bytes']
        assert all(p[x] is False for x in ['spatial_continuum_qualified','rigorous_characteristic_or_shock_interval_proved','full_relativistic_metric_qualified','observational_fit'])
        summary=audit_case(p,ck);summary['sampled_group_rss_bytes']=inv['sampled_process_group_peak_rss_bytes'];summaries.append(summary);cases[i]=p
    pairs=[];orders=[]
    for Roffset in (0,6):
        for Loffset in (0,3):
            ids=[Roffset+Loffset+k for k in range(3)]
            if all(i in cases for i in ids):
                ab=comparison(cases[ids[0]],cases[ids[1]],1/16,'grid_coarse_medium')
                bc=comparison(cases[ids[1]],cases[ids[2]],1/16,'grid_medium_fine')
                pairs.extend([ab,bc,comparison(cases[ids[0]],cases[ids[2]],1/16,'grid_coarse_fine')])
                for aa,bb in zip(ab['epochs'],bc['epochs']):
                    row={}
                    for key in aa['fields']:
                        e1=aa['fields'][key]['weighted_rms'];e2=bb['fields'][key]['weighted_rms']
                        row[key]=None if e1<=0 or e2<=0 else math.log2(e1/e2)
                    orders.append(dict(cases=ids,tau=aa['tau'],observed_orders=row,continuum_qualification=False))
        for k in range(3):
            if Roffset+k in cases and Roffset+3+k in cases:pairs.append(comparison(cases[Roffset+k],cases[Roffset+3+k],cases[Roffset+k]['case']['dx'],'domain_L8_minus_L16'))
    p=dict(status='SAVED_ARRAY_AUDIT_PASS_FULL_CENSUS' if len(cases)==12 and not ck.failures else 'SAVED_ARRAY_AUDIT_INCOMPLETE_OR_FAILED',
        all_case_indices=list(range(12)),completed_case_indices=sorted(cases),missing_case_indices=missing,incomplete_cases=incomplete,
        saved_arithmetic_checks=int(ck.count),maxima=ck.maxima,failures=ck.failures,cases=summaries,pairs=pairs,observed_orders=orders,
        spatial_continuum_qualified=False,new_physical_producer_run=False,new_EOS_or_quadrature_run=False,
        scope='Saved piecewise-density algebra, material identities and time-vector checks; no trajectory or material reevaluation. FD synthetic perturbations and GL64/128 arrays are not saved, so their reported controls are authenticated, not independently reexecuted.',
        source_sha256=sha(Path(__file__).read_bytes()),files=FILES)
    print(enc(dict(payload_sha256=sha(enc(p)),payload=p)).decode())
if __name__=='__main__':main()
