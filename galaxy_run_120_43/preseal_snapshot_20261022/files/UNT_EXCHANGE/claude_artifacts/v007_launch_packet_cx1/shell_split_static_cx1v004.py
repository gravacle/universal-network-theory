"""Saved state shell reporter: RUN LABEL FILLED_SPEC EPS_CERT OUTPUT [--fixture-hi VALUE].
Full production shells use exactly EPS edges intersecting the tail. Fixture-hi truncates only the test decomposition,
which is reported explicitly and cannot be used as a full C4T RB_FP gate.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
R=Path(__file__).parent;A=R.parent
sys.path.insert(0,str(R));sys.path.insert(0,str(A/'tail_scheme_impl_c2/module/tests'))
import shell_filter_cx1v001 as SF
import common_tests_v001 as T
import saved_states_v001 as SS
import test_d_b2_replay_v001 as B2

def pin(p):return {'path':str(p),'sha256':T.sha(p)}
class Saved(SS.SavedCase):
    def __init__(self,run):
        self.run=Path(run);r=json.loads((self.run/'result.json').read_bytes());last=r['passes'][-1]
        self.rows=np.array([x['speed_km_s'] for x in last['rows']]);self.rot=Path(last['rotation']);self.field=Path(last['field'])
        fm=SS.argmap(self.field.parent/'request.json');self.src_rot=Path(fm['--rotation-directory']);rm=SS.argmap(self.rot.parent/'request.json');self.manifest=Path(rm['--column-manifest'])
        assert Path(rm['--feedback-directory'])==self.field
        self.gamma=float(r['identity']['route_a']['custody']['physical']['gamma']);self.seed_ni=json.loads((self.run/'inputs/seed_c2v001.json').read_bytes())['numerical_inputs']
        self.K=4.;self.result=r

def main():
    run,label,sp,ep,out=sys.argv[1:6];fixture_hi=float(sys.argv[7]) if len(sys.argv)>6 and sys.argv[6]=='--fixture-hi' else None
    if fixture_hi is not None and label not in ('C4R3','C5R3','C6R3'):raise ValueError('PARTIAL_DOMAIN_RESTRICTED_TO_FIXTURE_LABELS')
    c=Saved(run);cfg=T.UVT.normalize_config(json.loads(Path(sp).read_bytes())['numerics']['uv_tail']);ni=c.seed_ni
    prof=T.profile();jn=T.PV.create_provider();arr=c.source_rotation_arrays();units={'kpc_m':ni['kpc_m'],'solar_mass_kg':ni['solar_mass_kg']}
    stars=T.RS.stars_registered(prof,'DDO154',units=units);ros=T.RS.roster_rotation(arr,stars,s_edges_kpc2=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],kpc_m=ni['kpc_m'],M_s=cfg['gas']['M_s'])
    waves=c.unit_waves();idx=np.sort(np.random.default_rng(20261018).choice(len(waves),4096,replace=False));zc,mc=SS.ddo_gas_elements(arr)
    sr=T.RS.stars_gl4_rings(prof,'DDO154',kpc_m=ni['kpc_m'],solar_mass_kg=ni['solar_mass_kg'],gauss_order=ni['source_gauss_order'])
    ck=Path(c.result['identity']['route_a']['checkpoint']);start=json.loads((ck/'iteration_0004/START.json').read_bytes());ref=start['fixed_source_fourier_J'];assert T.sha(ck/ref['blob'])==ref['file_sha256']
    fixed=np.load(ck/ref['blob'],mmap_mode='r',allow_pickle=False)[:,0,0][idx]
    rep=T.RS.packet_transform(sr,waves[idx],'prep_analytic_j0',c_m_s=T.CL,j0=jn.j0)+T.RS.packet_transform({'R':np.repeat(arr['radial_nodes_m'],zc[0].size),'z':np.concatenate(zc),'m':np.concatenate(mc)},waves[idx],'feedback_ring_j0_v004',c_m_s=T.CL,j0=jn.j0)
    i1t=T.RS.check_represented(rep,fixed+c.gas_packet()[idx],'shell replay',rtol=1e-12)
    rot=c.final_rotation_arrays();cols=c.columns();rr,binding=SS.ddo_row_radii();rad=rot['radial_nodes_m'];zs=rot['z'][:,0,:];phis=2*np.pi*np.arange(16)/16
    kept=T.UVT.kept_region('fs_rotation',{'shape':'cube','kmax_inverse_kpc':None},c.K/T.KPC)
    st=T.UVT.build(config=cfg,kept=kept,roster=ros,gamma_eff=c.gamma,c_m_s=T.CL,eval_radii_m=rad,jn_provider=jn,i1t=i1t,stage_kind='fs_rotation')
    eps=json.loads(Path(ep).read_bytes());obs=T.load_module(B2.OBS,'shell_obs');adapter=T.load_module(B2.ADAPTER,'shell_adapter')
    baseline=B2.rows_with(rot,cols,None,binding,obs,adapter);assert np.array_equal(baseline,c.rows)
    shells=[];rows={};sumforce=np.zeros_like(zs);top=min(fixture_hi or float('inf'),math.sqrt(2)*cfg['outer']['K_big_inverse_kpc'])
    for e in eps['shells']:
        lo=e['lo_inverse_kpc'];hi=e['hi_inverse_kpc']
        if hi<=c.K or lo>=top:continue
        hi=min(hi,top);part=SF.filter_state(T.UVT,st,lo,hi,rad)
        force=np.array([T.CL**2*np.mean(part.cyl_jets(rad[i],phis,zs[i],1)['fR'],axis=0) for i in range(len(rad))]);sumforce+=force
        lab=f'{lo:g}_to_{hi:g}';shells.append(lab);rows[lab]=(B2.rows_with(rot,cols,force,binding,obs,adapter)-baseline).tolist()
        print('shell',lab,flush=True)
    direct=SF.filter_state(T.UVT,st,c.K,top,rad)
    totalforce=np.array([T.CL**2*np.mean(direct.cyl_jets(rad[i],phis,zs[i],1)['fR'],axis=0) for i in range(len(rad))])
    err=float(np.max(abs(sumforce-totalforce)));scale=float(np.max(abs(totalforce)))
    if err>max(1e-30,1e-10*scale):raise ValueError('SHELL_FORCE_SUM_MISMATCH')
    rec={'schema':'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002','gate':'RB_FP','verdict':'SHELL_SPLIT_COMPUTED','producer':pin(Path(__file__)),
    'case':label,'c4t_result_sha256':T.sha(c.run/'result.json'),'eps_max':eps['eps_max'],'shells':shells,'dV_static_shells_km_s':rows,
    'label':'TESTED finite shell replay; fixture partial domain' if fixture_hi else 'TESTED finite shell replay',
    'fixture_hi':fixture_hi,'full_tail_domain':fixture_hi is None,'force_partition_max_abs':err,'force_partition_scale':scale,
    'definition':'each shell separately through the static row adapter; no nonlinear fixed-point solve','i1t':i1t,'spec':pin(Path(sp)),'EPS':pin(Path(ep)),
    'state':pin(c.run/'result.json'),'shell_filter':pin(R/'shell_filter_cx1v001.py'),'tail_record':st.record}
    with open(out,'x') as f:json.dump(rec,f,indent=1)
if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).parent))
    import producer_guard_cx1v002 as guard
    guard.authorize(sys.argv,'run')
    main()
