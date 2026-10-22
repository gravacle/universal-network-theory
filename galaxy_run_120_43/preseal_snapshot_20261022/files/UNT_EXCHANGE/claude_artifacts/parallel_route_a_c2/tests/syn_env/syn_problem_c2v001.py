"""SYNTHETIC test problem builder. Uses the REVIEWED helper modules read-only
(stable lapse facade, fixed-xy line v002, HI v003, quadrature v002, metric v002,
source columns v003) with a small synthetic Fourier response. Test-only."""
import importlib.util
import math
from pathlib import Path
import numpy as np

H=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers')
LANE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2')
HERE=Path(__file__).resolve().parent
PATHS=dict(
    reviewed_solver=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py'),
    parallel_solver=LANE/'coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py',
    checkpoint=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py'),
    stable_adapter=H/'recovered_packet_audit/owned_stable_lapse_hi_facade_v001.py',
    stable_line=H/'recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py',
    stable_hi=H/'recovered_packet_audit/hi_two_sided_free_boundary_v003.py',
    quadrature=H/'recovered_packet_audit/general_column_mass_quadrature_v002.py',
    metric=H/'coefficient_method/owned_fourier_physical_metric_evaluator_v002.py',
    source=H/'recovered_packet_audit/baryonic_metric_source_columns_v003.py',
    fourier=HERE/'syn_fourier_c2v001.py',boundary=HERE/'syn_boundary_c2v001.py',
    wrapper=HERE/'syn_hi_wrapper_c2v001.py')
KPC=3.085677581491367e19
C=299792458.0


def load(name,path):
    spec=importlib.util.spec_from_file_location('syn_'+name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def modules():
    return {k:load(k,p) for k,p in PATHS.items()}


def build(mods,*,vertical=True,n_radii=4,n_phi=8,bad=(),hi_wrapper=None,boundary_kind='zero'):
    axis_xy=np.array([-1.,-.5,0.,.5,1.])/KPC
    axis_z=np.array([-1.6,-.8,-.4,-.2,.2,.4,.8,1.6])/KPC
    waves=np.array([(x,y,z) for x in axis_xy for y in axis_xy for z in axis_z])
    nk=len(waves); A=5e-7
    base=np.zeros((nk,10,1))
    for q,(x,y,z) in enumerate(waves*KPC):
        if x==0 and y==0 and abs(z)==.2: base[q,0,0]=-A
        elif abs(z)==.4: base[q,0,0]=-0.002*A*math.exp(-(x*x+y*y))*(1+0.5*math.cos(3*x+2*y)*0+0.3*abs(x))
        if abs(z) in (.2,.8): base[q,1:7,0]=1e-9*np.array([1,.5,-.3,.2,.1,-.15])*math.exp(-(x*x+2*y*y))
        if abs(z)==.4: base[q,7:10,0]=1e-10*np.array([.3,-.2,.1])*(1+abs(y))
    Cbar=np.array([[1.0,0.01,0.0],[0.01,1.1,0.02],[0.0,0.02,0.9]])
    mubar=np.array([0.0,0.0,0.0])
    hi_options=dict(sigma0_m_s=11000.,gamma=5/3,search_step_m=0.05*KPC,search_limit_m=5*KPC,
        root_tolerance_m=1e-6*KPC,log_lapse_tolerance=1e-12,max_metric_calls=300,panels_per_side=4)
    gas_columns=[]
    for i,R in enumerate([1.5,2.0,2.5,3.0,3.5,4.0][:n_radii]):
        for j in range(n_phi):
            gas_columns.append(dict(R_m=R*KPC,phi=2*math.pi*j/n_phi,radial_weight_m=0.5*KPC,
                azimuth_weight_rad=2*math.pi/n_phi,Sigma_kg_m2=1e-3*(1+0.1*i),hi_options=dict(hi_options)))
    for index,kind in bad:
        if kind=='budget': gas_columns[index]['hi_options']['max_metric_calls']=3
        elif kind=='typeerror': gas_columns[index]['hi_options']['unexpected_option']=1
    rng=np.random.default_rng(20261017)
    star_pos=np.column_stack([rng.uniform(.5,4,30)*KPC*np.cos(rng.uniform(0,2*math.pi,30)),
        rng.uniform(.5,4,30)*KPC*np.sin(rng.uniform(0,2*math.pi,30)),rng.normal(0,.1,30)*KPC])
    star_J=np.zeros((30,10,1)); star_J[:,0,0]=-1e38*C*C
    fixed=np.asarray(mods['source'].physical_source_fourier(physical_positions_m=star_pos,
        integrated_columns_J=star_J,k_physical_inverse_m=waves),dtype=complex)
    gpos=[[c['R_m']*math.cos(c['phi']),c['R_m']*math.sin(c['phi']),0.] for c in gas_columns]
    gJ=[[[-c['Sigma_kg_m2']*c['R_m']*c['radial_weight_m']*c['azimuth_weight_rad']*C*C]]+[[0.]]*9 for c in gas_columns]
    initial=np.asarray(mods['source'].physical_source_fourier(physical_positions_m=gpos,
        integrated_columns_J=gJ,k_physical_inverse_m=waves),dtype=complex)
    fa=dict(k_physical=waves,base_responses=base,feedback=0.05,Cbar=Cbar,mubar=mubar)
    hi=mods['stable_hi'] if hi_wrapper is None else hi_wrapper
    if vertical:
        line,hi=mods['stable_adapter'].make_modules(line_module=mods['stable_line'],hi_module=hi,
            reality_atol=1e-14,reality_rtol=1e-8)
    else:
        line=None
    return dict(fixed_positions_m=star_pos,fixed_integrated_columns_J=star_J,initial_gas_fourier_J=initial,
        gas_columns=gas_columns,fourier_arguments=fa,boundary_jet_at_positions=mods['boundary'].make_boundary(boundary_kind),
        source_module=mods['source'],fourier_module=mods['fourier'],metric_module=mods['metric'],
        hi_module=hi,quadrature_module=mods['quadrature'],vertical_fourier_module=line,
        c_m_s=C,relaxation=0.5,source_atol_J=0.0,reality_atol=1e-14,reality_rtol=1e-8,
        fixed_source_fourier_J=fixed)


def caller_identity(tag):
    return dict(code_pins={str(p.resolve()):__import__('hashlib').sha256(p.read_bytes()).hexdigest() for p in PATHS.values()},
        boundary_prescription='synthetic test boundary '+tag,physical_parameters={'synthetic':True},
        numerical_controls={'tag':tag})
