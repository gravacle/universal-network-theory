"""Imposed uniform polarization control; not a formed finite-response theory."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import hashlib
import json
import pathlib
import math
import sys
import time
import numpy as np
import solar_aqual_quadrupole_v001 as base

ROOT=pathlib.Path(__file__).resolve().parent
STEM='SOLAR_FROZEN_POLARIZATION_V001'


def custody():
    frozen=json.loads((ROOT/(base.STEM+'_FROZEN.json')).read_text())
    controls=json.loads((ROOT/(base.STEM+'_TESTS.json')).read_text())
    assert frozen['inputs']==base.inputs()==controls['inputs']
    assert controls['all_pass']
    p=[pathlib.Path(__file__),ROOT/(STEM+'.md'),ROOT/(base.STEM+'_FROZEN.json'),
       ROOT/(base.STEM+'_TESTS.json')]
    return {**base.inputs(),**{x.name:base.sha(x) for x in p}}


def save(suffix,obj):
    with (ROOT/(STEM+suffix+'.json')).open('x') as f:
        json.dump(obj,f,indent=2,allow_nan=False)
        f.write('\n')


class FrozenGrid(base.Grid):
    def __init__(self,spec,e):
        super().__init__(spec)
        self.e=e
        self.rs=base.law.RATIO
        fe=(1+(e/self.rs)**2)**(-.5)
        self.bmag=e*float(base.deficit(e))/fe**3
        self.perp=1+self.bmag*e*fe**3/self.rs**2
        self.para=1+3*self.bmag*e*fe**5/self.rs**2
        self.extB=self.bmag*fe**3
        self.elliptic_bound=4/math.sqrt(3)*self.bmag/self.rs
        self.outer=((1-1/(math.sqrt(self.perp*self.para)*np.sqrt(
                    1-self.u**2+self.perp/self.para*self.u**2)))/self.r[-1])@self.proj

    def source(self,psi,e,newton=False):
        dr=np.gradient(psi,self.h,axis=0,edge_order=2)@self.P.T
        du=psi@self.D.T
        rr=self.r[:,None]
        gr=rr**(-2)-e*self.u+dr/rr
        gt=e*self.s-self.s*du/rr
        ff=(1+(gr*gr+gt*gt)/self.rs**2)**(-.5)
        br0,bt0=-self.bmag*self.u,self.bmag*self.s
        dot=gr*br0+gt*bt0
        Br=ff*br0-ff**3*gr*dot/self.rs**2+self.extB*self.u
        Bt=ff*bt0-ff**3*gt*dot/self.rs**2-self.extB*self.s
        br=Br@self.proj
        th=Bt@self.aproj
        src=self.r[:,None]*(np.gradient(br,self.h,axis=0,edge_order=2)+2*br+th)
        return src,br,th,1-self.elliptic_bound


def direct(g,b,rs):
    ff=(1+np.dot(g,g)/rs**2)**(-.5)
    return g-ff*b+ff**3*g*np.dot(b,g)/rs**2


def energy(g,b,rs):
    return np.dot(g,g)/2-np.dot(g,b)/math.sqrt(1+np.dot(g,g)/rs**2)


def control():
    check=[]
    def add(name,val,lim):
        check.append({'name':name,'error':float(val),'limit':lim,'pass':bool(val<=lim)})
    gg=FrozenGrid(base.SPECS[0],base.GEXT/base.A0)
    bv=np.array([0.,0.,-gg.bmag])
    for j,g in enumerate([np.zeros(3),np.array([.1,.2,.3]),np.array([2.,-1.,.4]),
                          np.array([10.,20.,-5.]),np.array([100.,-30.,50.])]):
        dd=direct(g,bv,gg.rs)
        h=1e-5*max(1.,float(np.linalg.norm(g)))
        numerical=np.array([(energy(g+np.eye(3)[i]*h,bv,gg.rs)-
                             energy(g-np.eye(3)[i]*h,bv,gg.rs))/(2*h) for i in range(3)])
        add('energy_gradient_'+str(j),np.max(abs(numerical-dd))/max(1.,np.max(abs(dd))),1e-6)
        add('zero_polarization_'+str(j),np.max(abs(direct(g,np.zeros(3),gg.rs)-g)),1e-13)
    ge=np.array([0.,0.,-gg.e])
    h=1e-5
    H=np.column_stack([(direct(ge+np.eye(3)[i]*h,bv,gg.rs)-
                        direct(ge-np.eye(3)[i]*h,bv,gg.rs))/(2*h) for i in range(3)])
    add('external_hessian',np.max(abs(H-np.diag([gg.perp,gg.perp,gg.para]))),1e-6)
    add('external_B',np.max(abs(ge-direct(ge,bv,gg.rs)-np.array([0.,0.,-gg.extB]))),1e-13)
    add('sufficient_global_ellipticity',gg.elliptic_bound,1.)
    for name,c in [('perp',gg.perp),('parallel',gg.para)]:
        add('positive_'+name,max(0.,-c),0.)
    save('_TESTS',{'inputs':custody(),'checks':check,'all_pass':all(c['pass'] for c in check)})
    print(json.dumps({'checks':len(check),'all_pass':all(c['pass'] for c in check)}))


def run(index):
    frozen=json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())
    tests=json.loads((ROOT/(STEM+'_TESTS.json')).read_text())
    assert frozen['inputs']==tests['inputs']==custody() and tests['all_pass']
    assert index in range(7)
    if index>=5:
        assert summarize(False)['qualified_primary']
    ext=base.GEXT if index<5 else (2.16e-10 if index==5 else 2.48e-10)
    spec=base.SPECS[min(index,4)]
    start=time.perf_counter()
    grid=FrozenGrid(spec,ext/base.A0)
    psi=np.zeros((spec[0],spec[1]+1))
    history=[]
    good=0
    status='iteration_limit'
    for k in range(240):
        src,br,theta,lower=grid.source(psi,grid.e)
        target=grid.solve(src,grid.outer)
        change=float(np.max(abs(target-psi))/max(1.,np.max(abs(psi))))
        psi=.5*(target+psi)
        good=good+1 if change*.5<1e-8 else 0
        if k%10==0 or good>=3:
            history.append({'iteration':k+1,'half_update':change*.5})
        if good>=3:
            status='converged'
            break
        if time.perf_counter()-start>50:
            status='time_limit'
            break
    src,br,theta,lower=grid.source(psi,grid.e)
    target=grid.solve(src,grid.outer)
    defect=float(np.max(abs(target-psi))/max(1.,np.max(abs(psi))))
    mask=(grid.r>=.003)&(grid.r<=.02)
    cs=psi[mask,2]/grid.r[mask]**2
    c2=float(np.median(cs))
    plateau=float(np.max(abs(cs-c2))/max(abs(c2),1e-5))
    obj={'inputs':custody(),'index':index,'spec':spec,'external_acceleration':ext,
         'a0':base.A0,'GM':base.GM,'rM':base.RM,'shape_ratio':grid.rs,'b_magnitude':grid.bmag,
         'external_C_perp':grid.perp,'external_C_parallel':grid.para,
         'global_ellipticity_lower_bound':lower,'imposed_frozen_polarization':True,
         'converged':status=='converged' and defect<3e-8,'status':status,
         'iterations':k+1,'fixed_point_defect':defect,'plateau_relative':plateau,
         'c2':c2,'Q2':-3*base.A0/base.RM*c2,'history':history,
         'radii':grid.r.tolist(),'psi_modes':psi.tolist(),'Br_modes':br.tolist(),
         'Theta_modes':theta.tolist(),'elapsed_seconds':time.perf_counter()-start}
    save('_CASE_'+str(index),obj)
    print(json.dumps({k:obj[k] for k in ('index','status','converged','Q2',
                    'fixed_point_defect','plateau_relative','elapsed_seconds')}))


def summarize(write=True):
    cases=[json.loads((ROOT/(STEM+'_CASE_'+str(i)+'.json')).read_text()) for i in range(5)]
    for i,c in enumerate(cases):
        assert c['inputs']==custody() and c['index']==i and c['spec']==list(base.SPECS[i])
        assert c['external_acceleration']==base.GEXT
    scale=max(abs(cases[-1]['c2']),1e-5)
    diffs={str(a)+'_'+str(b):abs(cases[a]['c2']-cases[b]['c2'])/scale
           for a,b in ((1,2),(2,3),(3,4))}
    ok=all(c['converged'] and c['plateau_relative']<.01 for c in cases) and all(v<.05 for v in diffs.values())
    obj={'inputs':custody(),'qualified_primary':ok,'relative_changes':diffs,
         'Q2_primary':cases[-1]['Q2'] if ok else None,
         'cassini_standardized_residual':(cases[-1]['Q2']-1.6e-27)/1.8e-27 if ok else None,
         'cases':[{k:c[k] for k in ('index','converged','Q2','c2','fixed_point_defect',
                   'plateau_relative','elapsed_seconds')} for c in cases],
         'receipt_hashes':{STEM+'_CASE_'+str(i)+'.json':base.sha(ROOT/(STEM+'_CASE_'+str(i)+'.json')) for i in range(5)},
         'interpretation':'Imposed nonresponding-polarization limit, not a finite-response or native formation result'}
    if write:
        save('_RESULT',obj)
        print(json.dumps(obj))
    return obj


if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='freeze':
        save('_FROZEN',{'inputs':custody(),'specs':base.SPECS})
        print('Frozen')
    elif mode=='test':
        control()
    elif mode=='case':
        run(int(sys.argv[2]))
    elif mode=='summary':
        summarize()
    else:
        raise ValueError(mode)
