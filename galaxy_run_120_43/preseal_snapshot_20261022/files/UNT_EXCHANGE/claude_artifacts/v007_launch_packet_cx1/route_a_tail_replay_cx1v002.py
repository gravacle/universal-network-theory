"""Reconstruct a saved route-A tail at iteration n, without solving or altering a checkpoint."""
import json,sys,types
from pathlib import Path
import numpy as np
A=Path(__file__).parent.parent
sys.path.insert(0,str(A/'tail_scheme_impl_c2/module/tests'))
import common_tests_v001 as T
sys.path.insert(0,str(A/'tail_scheme_impl_c2/kbig_proxy_v002/tools'))
import kbig_build_timing_c2v002 as B

def build(run,ck,n,cfg,radius):
    import producer_runtime_cx1v001 as RT
    RT.bind(T)
    run=Path(run);result=json.loads((run/'result.json').read_bytes());ni=json.loads((run/'inputs/seed_c2v001.json').read_bytes())['numerical_inputs']
    gamma=float(result['identity']['route_a']['custody']['physical']['gamma']);prof=T.profile();jn=T.PV.create_provider()
    src=B.route_a_inputs(T.UVT,T.RS,T.PV,types.SimpleNamespace(checkpoint=Path(ck),ni=ni),prof,n)
    stars=T.RS.stars_registered(prof,'DDO154',units={'kpc_m':ni['kpc_m'],'solar_mass_kg':ni['solar_mass_kg']})
    edges=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'];spec=result['normalized_spec']['numerics']['composite_grid_spec']
    K=max(spec['breaks_inverse_kpc']) if spec else 2.
    kept=T.UVT.kept_region('route_a',None,K/T.KPC)
    if cfg['source_rule']=='continuum_v001':
        ros=T.RS.roster_route_a(stars,src['init'],src['elements'],src['relaxation'],s_edges_kpc2=edges,kpc_m=ni['kpc_m'],M_s=cfg['gas']['M_s'],c_m_s=T.CL)
        return T.UVT.build(config=cfg,kept=kept,roster=ros,gamma_eff=gamma,c_m_s=T.CL,eval_radii_m=[radius],jn_provider=jn,i1t=src['i1t'],stage_kind='route_a')
    NL=T.load_module(A/'tail_scheme_impl_c2/nodes_v001/lib/owned_uv_tail_nodes_v001.py','ra10_nodes')
    ctx=NL.ext_context(ext_spec=cfg['source_rule']['ext_grid'],kept_spec=spec,kpc_m=ni['kpc_m']);axis=ctx['axis'];mask=ctx['mask3']
    sr=T.RS.stars_gl4_rings(prof,'DDO154',kpc_m=ni['kpc_m'],solar_mass_kg=ni['solar_mass_kg'],gauss_order=ni['source_gauss_order'])
    fixed=NL.extract_ext(NL.ring_transform_tensor(axis,sr['R'],sr['z'],sr['m'],T.CL,jn.j0),mask)
    init=src['init'];gas=NL.extract_ext(NL.ring_transform_tensor(axis,np.array(init['R']),np.array(init['z']),np.array(init['m']),T.CL,jn.j0),mask)
    relax=src['relaxation']
    for e in src['elements']:
        update=NL.extract_ext(NL.point_transform_tensor(axis,e['positions_m'],e['integrated_J']),mask);gas=(1-relax)*gas+relax*update
    return NL.build_state(config=cfg,kept=kept,ctx=ctx,parts=[('fixed',1,fixed,{'kind':'prep_analytic_j0'}),('gas',1,gas,{'kind':'saved_route_a_mixture','iteration':n})],gamma_eff=gamma,c_m_s=T.CL,i1t=src['i1t'],stage_kind='route_a',source_record={'run':str(run),'iteration':n})
