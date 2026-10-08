"""Inert clamped common-phase FV diagnostic. Sole producer: root; stdout only."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import sys
sys.dont_write_bytecode=True
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import zlib
import numpy as np
import clamped_phase_material_v001 as material

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/'CLAMPED_COMMON_PHASE_PATCH_V001_FROZEN.json'
CONFIG=dict(spectrum_index=1,reference=0,R=[128,8192],L=[1.,2.],N=[16,32],
    seeds=[1.,2.],a_kpc=3.2,parsec_m=3.085677581491367e16,c_m_s=299792458.,
    primary_order=128,control_order=64,newton_iterations=40,line_halvings=18,
    residual_tolerance=1e-9,flux_tolerance=2e-8,arithmetic_tolerance=2e-11,
    directional_steps=[1e-5,5e-6],directional_tolerance=2e-5,
    quadrature_tolerance=2e-8,newtonian_potential_tolerance=.02,
    newtonian_force_tolerance=.05,sheet_bisections=64,sheet_bracket_doublings=40)

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inputs():
    files={};seen=set()
    def add(p,h=None):
        p=p.resolve(strict=True);p.relative_to(ROOT);digest=sha(p)
        if h is not None and h!=digest:raise RuntimeError('Changed input '+str(p))
        files[str(p.relative_to(ROOT))]=digest;return p
    def manifest(p):
        p=add(p)
        if p in seen:return
        seen.add(p)
        for name,h in json.loads(p.read_text())['files'].items():
            q=Path(name);opts=[q] if q.is_absolute() else [ROOT/q,p.parent/q]
            matches={v.resolve() for v in opts if v.resolve().is_relative_to(ROOT) and v.is_file()}
            if len(matches)!=1:raise RuntimeError('Ambiguous ancestor '+name)
            f=add(matches.pop(),h)
            if f.name.endswith('_FROZEN.json'):manifest(f)
    def packet(name,digest,freeze):
        t=json.loads(add(HERE/name,digest).read_text());d=zlib.decompressobj()
        raw=d.decompress(base64.b64decode(t['data'],validate=True))+d.flush()
        if not d.eof or d.unused_data or d.unconsumed_tail:raise RuntimeError('Invalid transport')
        if len(raw)!=t['raw_bytes'] or hashlib.sha256(raw).hexdigest()!=t['raw_sha256']:raise RuntimeError('Changed raw packet')
        v=json.loads(raw);p=v['payload'];manifest(HERE/freeze)
        if v['freeze_sha256']!=sha(HERE/freeze) or v['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():raise RuntimeError('Changed wrapper')
        if p['status']!='COMPLETE' or p['failures']:raise RuntimeError('Unqualified input')
        return p
    old=packet('FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json','11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4','FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json')
    local=packet('FINITE_FIELD_PHASE_RESPONSE_V001_TRANSPORT.json','18788e16f5575da64a7e6ed527179bd7142b9cd42ce3d814f98642c81e76a3a2','FINITE_FIELD_PHASE_RESPONSE_V001_FROZEN.json')
    globalp=json.loads(add(HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json','11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628').read_text())['payload']
    for name in [Path(__file__).name,'clamped_phase_material_v001.py','CLAMPED_COMMON_PHASE_PATCH_PROTOCOL_V001.md','CLAMPED_COMMON_PHASE_KUZMIN_PATCH_V001.md']:
        add(HERE/name)
    selected={r['R']:r for r in old['rows'] if r['spectrum_index']==1 and r['reference']==0 and r['R'] in CONFIG['R']}
    if set(selected)!={128,8192}:raise RuntimeError('Selected source census differs')
    return selected,globalp,local,dict(configuration=CONFIG,files=files)


def derivative_matrix(c):
    """Three-point nonuniform derivative, identical stencil to edge_order=2."""
    n=len(c);d=np.zeros((n,n))
    for i in range(n):
        ids=[0,1,2] if i==0 else ([n-3,n-2,n-1] if i==n-1 else [i-1,i,i+1])
        x=c[i]
        for j in ids:
            others=[k for k in ids if k!=j]
            d[i,j]=(2*x-c[others[0]]-c[others[1]])/((c[j]-c[others[0]])*(c[j]-c[others[1]]))
    return d


class Geometry:
    def __init__(self,n,L,newtonian_boundary=False):
        self.n=n;self.L=L;self.size=n*n
        self.edges=np.expm1(np.linspace(0,math.log1p(L),n+1))
        self.c=(self.edges[:-1]+self.edges[1:])/2;self.width=np.diff(self.edges)
        self.area=np.diff(self.edges**2)/2
        self.volume=(self.area[:,None]*self.width[None,:]).ravel()
        self.x,self.z=np.meshgrid(self.c,self.c,indexing='ij')
        d=derivative_matrix(self.c);self.GR=np.kron(d,np.eye(n));self.GZ=np.kron(np.eye(n),d)
        P=[];XR=[];XZ=[];p0=[];r0=[];z0=[];left=[];right=[];areas=[];axis=[];outer=[]
        def face(a,b,normal,facearea,pm,rm,zm,pconst=0.,rconst=0.,zconst=0.):
            left.append(a);right.append(b);axis.append(normal);areas.append(facearea);outer.append(b<0)
            P.append(pm);XR.append(rm);XZ.append(zm);p0.append(pconst);r0.append(rconst);z0.append(zconst)
        def empty():return np.zeros(self.size)
        for i in range(1,n):
            frac=self.width[i-1]/(self.width[i-1]+self.width[i])
            for j in range(n):
                a=(i-1)*n+j;b=i*n+j;pm=empty();rm=empty()
                pm[a]=1-frac;pm[b]=frac;rm[a]=-1/(self.c[i]-self.c[i-1]);rm[b]=-rm[a]
                face(a,b,0,self.edges[i]*self.width[j],pm,rm,(1-frac)*self.GZ[a]+frac*self.GZ[b])
        for j in range(n):
            a=(n-1)*n+j;rm=empty();rm[a]=-2/self.width[-1]
            s=math.sqrt(L*L+(self.c[j]+1)**2)
            val=-1/s if newtonian_boundary else 0.;tan=(self.c[j]+1)/s**3 if newtonian_boundary else 0.
            face(a,-1,0,L*self.width[j],empty(),rm,empty(),val,2*val/self.width[-1],tan)
        for i in range(n):
            for j in range(1,n):
                frac=self.width[j-1]/(self.width[j-1]+self.width[j]);a=i*n+j-1;b=i*n+j
                pm=empty();zm=empty();pm[a]=1-frac;pm[b]=frac
                zm[a]=-1/(self.c[j]-self.c[j-1]);zm[b]=-zm[a]
                face(a,b,1,self.area[i],pm,(1-frac)*self.GR[a]+frac*self.GR[b],zm)
        for i in range(n):
            a=i*n+n-1;zm=empty();zm[a]=-2/self.width[-1]
            s=math.sqrt(self.c[i]**2+(L+1)**2)
            val=-1/s if newtonian_boundary else 0.;tan=self.c[i]/s**3 if newtonian_boundary else 0.
            face(a,-1,1,self.area[i],empty(),empty(),zm,val,tan,2*val/self.width[-1])
        self.P=np.asarray(P);self.XR=np.asarray(XR);self.XZ=np.asarray(XZ)
        self.p0=np.asarray(p0);self.r0=np.asarray(r0);self.z0=np.asarray(z0)
        self.left=np.asarray(left);self.right=np.asarray(right);self.internal=self.right>=0
        self.face_area=np.asarray(areas);self.axis=np.asarray(axis);self.outer=np.asarray(outer)
        self.sheet=1/np.sqrt(1+self.edges[:-1]**2)-1/np.sqrt(1+self.edges[1:]**2)
        self.bottom=np.arange(n)*n

    def divergence(self,flux):
        weighted=self.face_area*flux
        integrated=np.bincount(self.left,weighted,minlength=self.size)
        integrated-=np.bincount(self.right[self.internal],weighted[self.internal],minlength=self.size)
        integrated[self.bottom]-=self.sheet
        return integrated/self.volume


def evaluate(u,geo,mat,eps,order=128,jacobian=False,newtonian=False):
    cr=geo.GR@u;cz=geo.GZ@u;fr=geo.XR@u+geo.r0;fz=geo.XZ@u+geo.z0
    cg=np.hypot(cr,cz);fg=np.hypot(fr,fz)
    if newtonian:
        cell=None;face=None;rhs=np.zeros_like(u);flux=np.where(geo.axis==0,fr,fz)
    else:
        cell=mat.evaluate(eps*u,cg,order=order)
        face=mat.evaluate(eps*(geo.P@u+geo.p0),fg,order=order)
        flux=face['normalized_mu']*np.where(geo.axis==0,fr,fz)
        rhs=eps/mat.Kb*cell['deltaT']
    residual=geo.divergence(flux)-rhs
    integrated=geo.volume*residual
    sheet_total=float(np.sum(geo.sheet));volume_source=float(np.dot(geo.volume,rhs))
    outer_flux=float(np.dot(geo.face_area[geo.outer],flux[geo.outer]))
    norm=float(np.sum(np.abs(integrated)))/sheet_total
    out=dict(residual=residual,norm=norm,flux=flux,outer_flux=outer_flux,sheet_flux=sheet_total,
        volume_source=volume_source,flux_balance=outer_flux-sheet_total-volume_source,
        cr=cr,cz=cz,cg=cg,fr=fr,fz=fz,fg=fg,cell=cell,face=face)
    if not jacobian:return out
    normal_map=np.where((geo.axis==0)[:,None],geo.XR,geo.XZ)
    if newtonian:df=normal_map.copy()
    else:
        er=np.divide(fr,fg,out=np.zeros_like(fr),where=fg>0);ez=np.divide(fz,fg,out=np.zeros_like(fz),where=fg>0)
        en=np.where(geo.axis==0,er,ez)
        df=(face['KT']/mat.Kb)[:,None]*normal_map
        df+=((face['KL']-face['KT'])*en/mat.Kb)[:,None]*(er[:,None]*geo.XR+ez[:,None]*geo.XZ)
        df-=(eps*face['F_Phi']*en/mat.Kb)[:,None]*geo.P
    J=np.zeros((geo.size,geo.size));term=geo.face_area[:,None]*df
    np.add.at(J,geo.left,term)
    np.add.at(J,geo.right[geo.internal],-term[geo.internal]);J/=geo.volume[:,None]
    if not newtonian:
        er=np.divide(cr,cg,out=np.zeros_like(cr),where=cg>0);ez=np.divide(cz,cg,out=np.zeros_like(cz),where=cg>0)
        J-=((eps/mat.Kb)*(2*cell['F']-cell['F_Phi']))[:,None]*(er[:,None]*geo.GR+ez[:,None]*geo.GZ)
        J[np.diag_indices(geo.size)]+=eps*eps/mat.Kb*cell['J']
    out['jacobian']=J
    return out


def solve(seed,geo,mat,eps):
    u=seed.copy();history=[];status='ITERATION_LIMIT';last=None
    for iteration in range(CONFIG['newton_iterations']):
        try:current=evaluate(u,geo,mat,eps,jacobian=True)
        except material.MaterialDomainError as error:
            return u,history,'MATERIAL_DOMAIN_FAILURE',None,str(error)
        last=current
        history.append(dict(iteration=iteration,residual=current['norm'],flux_balance=current['flux_balance'],
            occupied_cells=int(np.sum(current['cell']['branch']==1)),occupied_faces=int(np.sum(current['face']['branch']==1)),
            min_KT=float(min(np.min(current['cell']['KT']),np.min(current['face']['KT']))),
            min_KL=float(min(np.min(current['cell']['KL']),np.min(current['face']['KL'])))))
        if current['norm']<=CONFIG['residual_tolerance']:
            status='CONVERGED';break
        try:step=np.linalg.solve(current['jacobian'],-current['residual'])
        except np.linalg.LinAlgError:
            status='SINGULAR_JACOBIAN';break
        if not np.all(np.isfinite(step)):
            status='NONFINITE_NEWTON_STEP';break
        accepted=False;rejected=[]
        for half in range(CONFIG['line_halvings']+1):
            damping=2.**(-half);trial=u+damping*step
            try:test=evaluate(trial,geo,mat,eps)
            except material.MaterialDomainError as error:
                rejected.append(dict(damping=damping,reason=str(error)));continue
            if test['norm']<current['norm']*(1-1e-4*damping):
                history[-1].update(damping=damping,accepted_residual=test['norm'],rejected_domain_trials=rejected)
                u=trial;last=test;accepted=True;break
        if not accepted:
            history[-1]['rejected_domain_trials']=rejected;status='LINE_SEARCH_FAILED';break
    # Re-evaluate the actual retained state, including a final accepted update.
    try:last=evaluate(u,geo,mat,eps,jacobian=True)
    except material.MaterialDomainError as error:return u,history,'MATERIAL_DOMAIN_FAILURE',None,str(error)
    if last['norm']<=CONFIG['residual_tolerance']:status='CONVERGED'
    return u,history,status,last,None


def directional_checks(u,geo,mat,eps,state):
    out=[];x=geo.x.ravel();z=geo.z.ravel();L=geo.L
    directions=[np.sin(math.pi*x/L)*np.sin(math.pi*z/L),np.cos(math.pi*x/(2*L))*np.sin(math.pi*z/L)]
    for index,d in enumerate(directions):
        d/=np.max(np.abs(d));exact=state['jacobian']@d
        for scale in CONFIG['directional_steps']:
            h=scale*max(1.,float(np.max(np.abs(u))))
            try:a=evaluate(u+h*d,geo,mat,eps);b=evaluate(u-h*d,geo,mat,eps)
            except material.MaterialDomainError as error:
                out.append(dict(direction=index,step=h,status='MATERIAL_DOMAIN',message=str(error)));continue
            same=all(np.array_equal(a[p]['branch'],b[p]['branch']) and np.array_equal(a[p]['branch'],state[p]['branch']) for p in ['cell','face'])
            fd=(a['residual']-b['residual'])/(2*h)
            error=float(np.linalg.norm(geo.volume*(fd-exact))/max(np.linalg.norm(geo.volume*exact),1e-300))
            out.append(dict(direction=index,step=h,status='CHECKED' if same else 'ACTIVE_SET_SWITCH',error=error))
    return out


def boundary_normal_diagnostic(u,geo,mat,eps):
    """Postprocess the prescribed sheet flux; not an extra fitted boundary."""
    n=geo.n;a=geo.c[0]/(geo.c[1]-geo.c[0]);table=u.reshape(n,n)
    sheet_u=(1+a)*table[:,0]-a*table[:,1]
    tangential=derivative_matrix(geo.c)@sheet_u;target=geo.sheet/geo.area
    lower=np.zeros(n);upper=np.maximum(1.,2*target);phi=eps*sheet_u
    def flux(v):
        o=mat.evaluate(phi,np.hypot(tangential,v),order=CONFIG['primary_order'])
        return o['normalized_mu']*v,o
    try:
        for _ in range(CONFIG['sheet_bracket_doublings']):
            f,o=flux(upper);missing=f<target
            if not np.any(missing):break
            upper=np.where(missing,2*upper,upper)
        else:return dict(status='NO_NORMAL_BRACKET')
        for _ in range(CONFIG['sheet_bisections']):
            mid=(lower+upper)/2;f,o=flux(mid)
            lower=np.where(f<target,mid,lower);upper=np.where(f>=target,mid,upper)
        normal=(lower+upper)/2;f,o=flux(normal)
        return dict(status='BRACKETED_LOCAL_INVERSION',sheet_u=sheet_u.tolist(),tangential=tangential.tolist(),
            normal=normal.tolist(),target_bin_average=target.tolist(),recovered=f.tolist(),
            relative_error=float(np.max(np.abs(f-target)/target)),branch=o['branch'].tolist(),
            min_KT=float(np.min(o['KT'])),min_KL=float(np.min(o['KL'])),
            scope='Diagnostic extrapolated sheet potential and bin-averaged prescribed flux; not a uniqueness proof for all normal roots.')
    except material.MaterialDomainError as error:return dict(status='MATERIAL_DOMAIN',message=str(error))


def run_case(case,selected,globalp,local):
    start=time.perf_counter();cases=[(R,L,n) for R in CONFIG['R'] for L in CONFIG['L'] for n in CONFIG['N']]
    R,L,n=cases[case];src=selected[R];spec=globalp['spectra'][1]['spectrum'];ref=globalp['references'][0]
    mat=material.Material(src,spec,beta=.005,chunk_size=256)
    a=CONFIG['a_kpc']*1000*CONFIG['parsec_m'];eps=src['gstar']*a/CONFIG['c_m_s']**2
    geo=Geometry(n,L);checks={};failures=[]
    def check(name,error,tolerance):
        checks[name]=dict(error=float(error),tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance))
        if not checks[name]['passed']:failures.append(name)
    check('volume',abs(float(np.sum(geo.volume))-L**3/2)/(L**3/2),CONFIG['arithmetic_tolerance'])
    check('sheet_flux',abs(float(np.sum(geo.sheet))-(1-1/math.sqrt(1+L*L))),CONFIG['arithmetic_tolerance'])
    # Independent pure-Newtonian operator/geometry check with analytic outer data.
    ng=Geometry(n,L,newtonian_boundary=True);zero=np.zeros(n*n)
    initial=evaluate(zero,ng,mat,eps,jacobian=True,newtonian=True)
    nu=np.linalg.solve(initial['jacobian'],-initial['residual'])
    ns=evaluate(nu,ng,mat,eps,newtonian=True)
    truth=-1/np.sqrt(ng.x.ravel()**2+(ng.z.ravel()+1)**2)
    denom=(ng.x.ravel()**2+(ng.z.ravel()+1)**2)**1.5
    tr=ng.x.ravel()/denom;tz=(ng.z.ravel()+1)/denom
    check('newtonian_potential',float(np.max(np.abs(nu-truth))/np.max(np.abs(truth))),CONFIG['newtonian_potential_tolerance'])
    check('newtonian_force',float(np.linalg.norm(np.hstack([ns['cr']-tr,ns['cz']-tz]))/np.linalg.norm(np.hstack([tr,tz]))),CONFIG['newtonian_force_tolerance'])
    check('newtonian_residual',ns['norm'],CONFIG['residual_tolerance'])
    check('newtonian_flux',abs(ns['flux_balance'])/ns['sheet_flux'],CONFIG['flux_tolerance'])
    # Bind the vectorized material to all 9 already saved local probes for this source.
    controls=[r for r in local['rows'] if r['R']==R and r['spectrum_index']==1 and r['reference']==0]
    vals=mat.evaluate(np.array([r['Phi'] for r in controls]),np.array([r['G'] for r in controls]),order=128)
    for key,oldkey in [('E','E'),('Pi','Pi'),('KT','K_transverse'),('KL','K_longitudinal'),('F','F'),('F_Phi','F_Phi'),('J','J_static')]:
        wanted=np.array([r['response'][oldkey] for r in controls]);scale=np.maximum(np.abs(wanted),1e-300)
        check('saved_material_'+key,float(np.max(np.abs(vals[key]-wanted)/scale)),CONFIG['quadrature_tolerance'])
    if failures:
        return dict(status='FAILED_PREREQUISITES',configuration=CONFIG,case_index=case,R=R,L=L,n=n,
            source_row=src,epsilon_scale=eps,a_m=a,Kb=mat.Kb,DeltaU=mat.DeltaU,cosmic_baseline=mat.baseline(128),
            edges=geo.edges.tolist(),centres=geo.c.tolist(),checks=checks,failures=failures,outcomes=[],
            unstarted_seeds=CONFIG['seeds'],two_seed_max_u_difference=None,
            seconds=time.perf_counter()-start,
            peak_self_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)),
            scope='Prerequisite operator/material qualification failed; both physical Newton seeds deliberately unstarted and retained as such. No physical branch conclusion.')
    seed=-(1-geo.x**2/L**2)*(1-geo.z**2/L**2)/np.sqrt(geo.x**2+(geo.z+1)**2)
    outcomes=[]
    for amplitude in CONFIG['seeds']:
        u,history,status,state,message=solve(amplitude*seed.ravel(),geo,mat,eps)
        outcome=dict(seed_multiplier=amplitude,status=status,history=history,u=u.reshape(n,n).tolist(),message=message)
        if state is not None:
            cell=state['cell'];face=state['face'];directional=directional_checks(u,geo,mat,eps,state)
            for location,values in [('cell',cell),('face',face)]:
                check(f'seed{amplitude}_{location}_frequency',float(np.max(values['common_frequency_error'])),CONFIG['arithmetic_tolerance'])
                energy_scale=np.maximum((np.abs(values['hard_min'])+values['hard_excitation'])/(.005*R**4),1e-300)
                for identity in ['unit_energy_identity_error','unit_pressure_identity_error']:
                    check(f'seed{amplitude}_{location}_{identity}',float(np.max(np.abs(values[identity])/energy_scale)),CONFIG['arithmetic_tolerance'])
                reaction_scale=np.maximum(np.maximum(np.abs(values['deltaT']),abs(mat.baseline(128)['Tb'])),1e-300)
                reaction_error=np.abs(values['deltaT']-values['deltaE']-3*values['deltaPi'])/reaction_scale
                check(f'seed{amplitude}_{location}_reaction_identity',float(np.max(reaction_error)),CONFIG['arithmetic_tolerance'])
            for j,d in enumerate(directional):
                if d['status']=='CHECKED':check(f'seed{amplitude}_direction{j}',d['error'],CONFIG['directional_tolerance'])
            checked_directions=[d for d in directional if d['status']=='CHECKED']
            jacobian_qualified=(len(checked_directions)==4 and all(d['error']<=CONFIG['directional_tolerance'] for d in checked_directions))
            alternate=evaluate(u,geo,mat,eps,order=64)
            field_scale=max(state['sheet_flux'],abs(state['volume_source']),1e-300)
            quadrature=float(np.sum(np.abs(geo.volume*(alternate['residual']-state['residual'])))/field_scale)
            check(f'seed{amplitude}_quadrature',quadrature,CONFIG['quadrature_tolerance'])
            ledger_error=abs(float(np.dot(geo.volume,state['residual']))-state['flux_balance'])/field_scale
            check(f'seed{amplitude}_ledger_identity',ledger_error,CONFIG['arithmetic_tolerance'])
            if status=='CONVERGED':check(f'seed{amplitude}_flux_balance',abs(state['flux_balance'])/field_scale,CONFIG['flux_tolerance'])
            sheet=boundary_normal_diagnostic(u,geo,mat,eps)
            if sheet['status']=='BRACKETED_LOCAL_INVERSION':check(f'seed{amplitude}_sheet_inverse',sheet['relative_error'],CONFIG['quadrature_tolerance'])
            J=cell['J'];lengths={}
            maxwidth=np.maximum(geo.width[:,None],geo.width[None,:]).ravel()
            for axis,key in [('transverse','KT'),('longitudinal','KL')]:
                ell=np.sqrt(np.divide(cell[key],J,out=np.full_like(J,np.nan),where=(J>0)&(cell[key]>0)))/eps
                lengths[axis+'_length_over_a']=np.where(np.isfinite(ell),ell,None).reshape(n,n).tolist()
                ratio=np.divide(maxwidth,ell,out=np.full_like(ell,np.nan),where=np.isfinite(ell)&(ell>0))
                lengths[axis+'_width_over_length']=np.where(np.isfinite(ratio),ratio,None).reshape(n,n).tolist()
                lengths[axis+'_valid']=np.isfinite(ell).reshape(n,n).tolist()
            cosmo=ref['H0_s_inverse']*a*L/CONFIG['c_m_s']
            er=np.divide(state['cr'],state['cg'],out=np.zeros_like(u),where=state['cg']>0)
            ez=np.divide(state['cz'],state['cg'],out=np.zeros_like(u),where=state['cg']>0)
            gF=state['cg']*cell['F']
            storekeys=['E','Pi','deltaE','deltaPi','deltaT','deltaT_soft','deltaT_hard','KT','KL','F','F_Phi','J','I','I_over_Ib','hard_E','hard_Pi','hard_min','hard_excitation','soft_E','branch','eII','common_frequency_error']
            outcome.update(residual=state['norm'],outer_flux=state['outer_flux'],sheet_flux=state['sheet_flux'],
                volume_source=state['volume_source'],volume_source_soft=float(eps/mat.Kb*np.dot(geo.volume,cell['deltaT_soft'])),
                volume_source_hard=float(eps/mat.Kb*np.dot(geo.volume,cell['deltaT_hard'])),flux_balance=state['flux_balance'],
                gradients=dict(radial=state['cr'].reshape(n,n).tolist(),vertical=state['cz'].reshape(n,n).tolist()),
                material={key:np.asarray(cell[key]).reshape(n,n).tolist() for key in storekeys},
                face_branch=face['branch'].tolist(),face_min_KT=float(np.min(face['KT'])),face_min_KL=float(np.min(face['KL'])),
                directional_checks=directional,jacobian_checked_comparisons=len(checked_directions),jacobian_qualified=jacobian_qualified,
                jacobian_qualification='QUALIFIED' if jacobian_qualified else ('UNQUALIFIED_ACTIVE_SET_OR_DOMAIN' if len(checked_directions)<4 else 'FAILED_DIRECTIONAL_CONTROL'),
                quadrature_residual_difference=quadrature,sheet_normal=sheet,local_lengths=lengths,
                dimensionless_per_copy_action_inventory=float(np.dot(geo.volume,cell['I'])),
                action_inventory_normalization='Per-copy sum of dimensionless volumes times I; leading physical hard phase charge multiplies by C beta 2pi a^3. The clamped fixed-mu patch is not closed.',
                omitted_estimates=dict(max_abs_Phi=float(np.max(np.abs(eps*u))),H_a_L_over_c=cosmo,
                    gF=gF.reshape(n,n).tolist(),Kb_g_squared=(mat.Kb*state['cg']**2).reshape(n,n).tolist(),
                    pressure_trace=(3*cell['deltaPi']).reshape(n,n).tolist(),
                    anisotropic_RR=(-gF*er*er).reshape(n,n).tolist(),anisotropic_Rz=(-gF*er*ez).reshape(n,n).tolist(),
                    anisotropic_zz=(-gF*ez*ez).reshape(n,n).tolist()))
        outcomes.append(outcome)
    difference=float(np.max(np.abs(np.asarray(outcomes[0]['u'])-np.asarray(outcomes[1]['u']))))
    return dict(status='FAILED_NUMERICAL_CONTROLS' if failures else 'COMPLETE_RETAINED_OUTCOMES',configuration=CONFIG,
        case_index=case,R=R,L=L,n=n,source_row=src,epsilon_scale=eps,a_m=a,Kb=mat.Kb,DeltaU=mat.DeltaU,
        cosmic_baseline=mat.baseline(128),edges=geo.edges.tolist(),centres=geo.c.tolist(),
        checks=checks,failures=failures,outcomes=outcomes,two_seed_max_u_difference=difference,
        seconds=time.perf_counter()-start,peak_self_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)),
        scope='Open-reservoir clamped weak-lapse diagnostic, not isolated galaxy/halo fit, full tensor metric solution, native formation or stability proof. All seed outcomes retained; coarse convergence is not grid resolution.')


def main():
    selected,globalp,local,snapshot=inputs()
    if sys.argv[1:]==['freeze']:print(encode(snapshot).decode());return
    if len(sys.argv)!=3 or sys.argv[1]!='run-case':raise RuntimeError('Use freeze or run-case 0..7')
    case=int(sys.argv[2])
    if case not in range(8):raise RuntimeError('Unknown case')
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Prospective freeze differs')
    payload=run_case(case,selected,globalp,local)
    raw=encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload))
    print(encode(dict(encoding='zlib_base64_canonical_json',raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),
        data=base64.b64encode(zlib.compress(raw,9)).decode(),summary=dict(case=case,status=payload['status'],
        outcomes=[o['status'] for o in payload['outcomes']],failures=payload['failures'],seconds=payload['seconds']))).decode())
    return 0 if not payload['failures'] else 2

if __name__=='__main__':sys.exit(main())
