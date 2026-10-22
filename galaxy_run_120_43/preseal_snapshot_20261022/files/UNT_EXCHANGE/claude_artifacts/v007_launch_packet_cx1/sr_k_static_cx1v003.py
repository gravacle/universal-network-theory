"""SR-K saved R3-state replay. CID(C2/C3/C4) FILLED_SPEC OUTPUT.
Same common tail added to both packet and smooth-source static rows. True saved per-node unit response.
No nonlinear solve. Per-state outputs must be aggregated only after all three states exist.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
R=Path(__file__).parent;A=R.parent;TESTS=A/'tail_scheme_impl_c2/module/tests'
sys.path.insert(0,str(TESTS))
import common_tests_v001 as T
import saved_states_v001 as SS
import test_d_b2_replay_v001 as B2
sys.path.insert(0,str(A/'uv_tail_study_c2/tools'))
import common_uvtail_v001 as CU

def pin(p):return {'path':str(p),'sha256':T.sha(p)}
def dforce(cube,axis,R,z,phis):
    out=np.empty(z.shape)
    for i,rad in enumerate(R):
        line=np.zeros(len(axis),complex)
        for ph in phis:
            cx=math.cos(ph);sy=math.sin(ph);ex=np.exp(1j*axis*rad*cx);ey=np.exp(1j*axis*rad*sy)
            line+=(np.einsum('i,j,ijk->k',1j*axis*cx*ex,ey,cube)+np.einsum('i,j,ijk->k',ex,1j*axis*sy*ey,cube))/len(phis)
        out[i]=T.CL**2*(np.exp(1j*np.outer(z[i],axis))@line).real
    return out

def main():
    cid,sp,out=sys.argv[1:];case=SS.SavedCase(cid);cu=CU.Case(cid)
    spec=json.loads(Path(sp).read_bytes());cfg=T.UVT.normalize_config(spec['numerics']['uv_tail'])
    if cfg['source_rule']!='continuum_v001':raise ValueError('SR_EXPECTS_CONTINUUM')
    ni=case.seed_ni;prof=T.profile();jn=T.PV.create_provider();arr=case.source_rotation_arrays()
    stars=T.RS.stars_registered(prof,'DDO154',units={'kpc_m':ni['kpc_m'],'solar_mass_kg':ni['solar_mass_kg']})
    ros=T.RS.roster_rotation(arr,stars,s_edges_kpc2=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],kpc_m=ni['kpc_m'],M_s=cfg['gas']['M_s'])
    waves,dk,unit=cu.unit();w2,total=cu.total();assert np.array_equal(waves,w2)
    fixed=cu.stars_fourier();gas=cu.gas_fourier();identity=float(np.max(abs(unit*(fixed+gas)-total))/np.max(abs(total)))
    if identity>1e-12:raise ValueError('SAVED_UNIT_SOURCE_IDENTITY')
    axis=np.unique(waves[:,0]);n=len(axis);assert len(waves)==n**3
    assert np.array_equal(waves[:,0].reshape(n,n,n)[:,0,0],axis)
    kp,inv=np.unique(np.hypot(*np.meshgrid(axis,axis,indexing='ij')),return_inverse=True)
    smooth=T.RS.source_continuum(ros,kp,axis,T.CL,jn.j0)[inv].reshape(n,n,n)
    bias=(unit*(fixed+gas-smooth.ravel())).reshape(n,n,n)
    # I1T is independently checked on represented packet sources before a tail state is built.
    idx=np.sort(np.random.default_rng(20261018).choice(len(waves),4096,replace=False))
    zc,mc=SS.ddo_gas_elements(arr);Rg=np.repeat(arr['radial_nodes_m'],zc[0].size)
    sr=T.RS.stars_gl4_rings(prof,'DDO154',kpc_m=ni['kpc_m'],solar_mass_kg=ni['solar_mass_kg'],gauss_order=ni['source_gauss_order'])
    replica=T.RS.packet_transform(sr,waves[idx],'prep_analytic_j0',c_m_s=T.CL,j0=jn.j0)+T.RS.packet_transform({'R':Rg,'z':np.concatenate(zc),'m':np.concatenate(mc)},waves[idx],'feedback_ring_j0_v004',c_m_s=T.CL,j0=jn.j0)
    i1t=T.RS.check_represented(replica,(fixed+gas)[idx],'SR_K saved source',rtol=1e-12)
    rot=case.final_rotation_arrays();cols=case.columns();rr,binding=SS.ddo_row_radii();rad=rot['radial_nodes_m'];z=rot['z'][:,0,:];phis=2*np.pi*np.arange(16)/16
    kept=T.UVT.kept_region('fs_rotation',{'shape':'cube','kmax_inverse_kpc':None},case.K/T.KPC)
    st=T.UVT.build(config=cfg,kept=kept,roster=ros,gamma_eff=case.gamma,c_m_s=T.CL,eval_radii_m=rad,jn_provider=jn,i1t=i1t,stage_kind='fs_rotation')
    tail=np.array([T.CL**2*np.mean(st.cyl_jets(rad[i],phis,z[i],1)['fR'],axis=0) for i in range(len(rad))])
    force=dforce(bias,axis,rad,z,phis)
    obs=T.load_module(B2.OBS,'sr_obs');adapter=T.load_module(B2.ADAPTER,'sr_adapter')
    baseline=B2.rows_with(rot,cols,None,binding,obs,adapter);assert np.array_equal(baseline,case.rows)
    packet=B2.rows_with(rot,cols,tail,binding,obs,adapter);smooth_rows=B2.rows_with(rot,cols,tail-force,binding,obs,adapter)
    rec={'schema':'UNT_SR_K_STATE_CX1V001','case':cid+'R3','K':case.K,'label':'TESTED finite static proxy; not a fixed-point solve',
    'producer':pin(Path(__file__)),'state_result':pin(case.run/'result.json'),'spec':pin(Path(sp)),'unit_packet_identity_max_rel':identity,'i1t':i1t,
    'zero_correction_bitwise':True,'Delta_km_s':(packet-smooth_rows).tolist(),'packet_plus_tail_km_s':packet.tolist(),'smooth_plus_tail_km_s':smooth_rows.tolist(),
    'sign':'packet_plus_common_tail minus smooth_plus_common_tail','tail_record':st.record,
    'inputs':{k:pin(p) for k,p in {'unit':cu.offset_dir/'unit_response.npz','prepared':case.field/'refreshed_prepared.npz','source':case.src_rot/'rotation_base_arrays.npz','rotation':case.rot/'rotation_base_arrays.npz','columns':case.manifest,'binding':SS.BINDING,'saved_reader':TESTS/'saved_states_v001.py','row_adapter':B2.ADAPTER,'observation':B2.OBS}.items()}}
    with open(out,'x') as f:json.dump(rec,f,indent=1)
    print(cid,'SR_K complete',flush=True)
if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).parent))
    import producer_guard_cx1v002 as guard
    guard.authorize(sys.argv,'cid')
    main()
