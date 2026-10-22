"""Independent tensor contraction check, full-domain shell-filter identity, and compare contract tests."""
import copy,hashlib,importlib.util,json,math,sys
from pathlib import Path
import numpy as np
R=Path(__file__).parent;sys.path.insert(0,str(R))
import sr_k_static_cx1v001 as SR
import shell_filter_cx1v001 as SF
T=SR.T

def pin(p):return {'path':str(p),'sha256':T.sha(p)}
def main():
    checks=[]
    def check(n,ok,**kw):
        checks.append(dict(name=n,passed=bool(ok),**kw));assert ok,n
    ax=np.array([-2.,.4,1.7])*1e-20;r=np.array([1.,2.])*1e19;z=np.array([[0.,2.],[-1.,3.]])*1e19;ph=np.array([0.,.7,2.2])
    cub=(np.arange(27).reshape(3,3,3)+1j*np.arange(27)[::-1].reshape(3,3,3))*1e-6
    got=SR.dforce(cub,ax,r,z,ph);ref=np.zeros_like(got)
    for i,rad in enumerate(r):
        for l,zz in enumerate(z[i]):
            val=0j
            for p in ph:
                for ia,kx in enumerate(ax):
                    for ib,ky in enumerate(ax):
                        for ic,kz in enumerate(ax):
                            kr=kx*math.cos(p)+ky*math.sin(p)
                            val+=cub[ia,ib,ic]*np.exp(1j*(kr*rad+kz*zz))*1j*kr/len(ph)
            ref[i,l]=T.CL**2*val.real
    rel=float(np.max(abs(got-ref))/np.max(abs(ref)));check('force_tensor_vs_direct_node_sum',rel<1e-12,relative=rel)
    cfg=T.config(outer='cylinder',K_big=4.,w_perp=.1,w_z=.1,R_eval=2.,z_eval=2.,z_src=8.)
    radii=np.array([.7,1.3])*T.KPC;phi=np.array([0.,np.pi/4,.63]);zs=np.array([0.,.4])*T.KPC
    st=T.UVT.build(config=cfg,kept={'shape':'cube','K_inverse_kpc':2.},roster=T.GaussianRoster(1.,1.),gamma_eff=1.,c_m_s=1.,eval_radii_m=radii,jn_provider=T.PV.create_provider(),i1t={'verdict':'NOT_APPLICABLE_SYNTHETIC'})
    full=SF.filter_state(T.UVT,st,2.,6.,radii);parts=[SF.filter_state(T.UVT,st,a,b,radii) for a,b in ((2.,3.),(3.,4.),(4.,5.),(5.,6.))]
    for ir,rad in enumerate(radii):
        a=st.cyl_jets(rad,phi,zs,1);b=full.cyl_jets(rad,phi,zs,1)
        for key in ('f','fR','fp','fz'):
            scale=max(float(np.max(abs(a[key]))),1e-300)
            er=float(np.max(abs(a[key]-b[key]))/scale);check(f'full_filter_identity_{ir}_{key}',er<1e-11,relative=er)
            sums=sum(p.cyl_jets(rad,phi,zs,1)[key] for p in parts);er=float(np.max(abs(sums-b[key]))/scale)
            check(f'shell_sum_identity_{ir}_{key}',er<1e-11,relative=er)
    cp=R.parent/'v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py';sp=importlib.util.spec_from_file_location('static_compare',cp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    shell=json.loads((R/'SHELL_C4R3_FIXTURE_V001.json').read_bytes());p=R/'SHELL_CONTRACT_C4T_SYNTHETIC_V001.json'
    shell['case']='C4T';shell['label']='SYNTHETIC contract mapping from partial-domain C4R3 fixture; not RB_FP production evidence'
    with p.open('x') as f:json.dump(shell,f,indent=1)
    gate=m.evaluate_gate('RB_FP',str(p),{}, {'C4T':shell['c4t_result_sha256']});check('RB_FP_contract_only',gate['status']=='PASS',codes=gate['codes'])
    state=json.loads((R/'SR_K_C4R3_FIXTURE_V001.json').read_bytes());p=R/'SR_K_CONTRACT_SYNTHETIC_V001.json'
    rec={'schema':m.GATE_SCHEMA,'gate':'SR_K','verdict':'REPLAYED','producer':pin(Path(__file__)), 'states':{k:v[1] for k,v in m.PIN_R3.items()},'Delta_km_s':{k:state['Delta_km_s'] for k in ('2','3','4')},'label':'SYNTHETIC contract fixture; repeated C4R3 vector is not C2R3/C3R3 evidence'}
    with p.open('x') as f:json.dump(rec,f,indent=1)
    gate=m.evaluate_gate('SR_K',str(p),{});check('SR_K_contract_only',gate['status']=='PASS',codes=gate['codes'])
    report={'label':'TESTED synthetic mathematics and record contracts; actual C4R3 tests recorded separately','checks':checks,'passed':len(checks),'failed':0,'compare':pin(cp),'producer':pin(Path(__file__))}
    with (R/'STATIC_PRODUCER_TESTS_V001.json').open('x') as f:json.dump(report,f,indent=1)
    print(len(checks),'static producer checks PASS')
if __name__=='__main__':main()
