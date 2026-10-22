"""INERT NGC43 actual-source trial entry point; root alone executes under a guard.
No target velocities, likelihood, fitting, hidden coefficient defaults or acceptance.
Requires supplied Eref [J], ell_F [m], gamma and explicit numerical resolutions.
Frozen single-point native response remains provisional; not calibrated43 predictions. Adopted H2 extrapolation is not measured outer gas.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

BASE = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
HERE = BASE/'helpers/recovered_packet_audit'
HC = BASE/'helpers/coefficient_method'
HP = BASE/'helpers/response_packet_audit'
C = BASE/'CODEX1'
KERNEL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py')
COEFFICIENT = BASE/'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz'
COEFFICIENT_SHA = '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module(path, pins):
    path = Path(path)
    pins[str(path)] = sha(path)
    spec = importlib.util.spec_from_file_location('ddo_'+path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def prepare_inputs(*, h2_tail_mass_rtol, Eref_J, ell_F_m, gamma, solar_mass_kg, kpc_m,
        kmax_inverse_kpc, fourier_points_per_axis, source_gauss_order,
        source_azimuth_count, observation_azimuth_count,
        pressure_step_kpc, azimuth_step_rad, hi_search_step_kpc,
        hi_search_limit_kpc, hi_root_tolerance_kpc, hi_log_lapse_tolerance,
        hi_max_metric_calls, hi_panels_per_side, max_iterations, relaxation,
        source_atol_J, source_rtol, pressure_atol_Pa_per_m, pressure_rtol,
        reality_atol, reality_rtol, relative_singular_floor,
        hermitian_tolerance, solve_rtol, solve_atol, progress_directory=None, analytic_initial_azimuth=False, composite_grid_spec=None, composite_grid_spec_anisotropic=None, ngc_outer_gas_cut=None):
    import numpy as np
    call_controls=dict(locals());call_controls.pop('np')
    if sha('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py')!='5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353':raise ValueError('NGC_GRID_CUT_HELPER_PIN')
    cut_helper=module(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py'),{})
    if composite_grid_spec_anisotropic is not None:
        if composite_grid_spec is not None:raise ValueError('ONE_GRID_DESCRIPTION_REQUIRED')
        cut_helper.validate_anisotropic(composite_grid_spec_anisotropic,kmax_inverse_kpc)
        if fourier_points_per_axis!=120:raise ValueError('T120L_LEGACY_AXIS_COUNT')
    scalars = [Eref_J, ell_F_m, solar_mass_kg, kpc_m, kmax_inverse_kpc,
               pressure_step_kpc, azimuth_step_rad, hi_search_step_kpc,
               hi_search_limit_kpc, hi_root_tolerance_kpc]
    if any(not math.isfinite(x) or x <= 0 for x in scalars) or not math.isfinite(gamma):
        raise ValueError('Finite physical parameters and positive explicit scales required')
    for n in (fourier_points_per_axis, source_gauss_order, source_azimuth_count,
              observation_azimuth_count):
        if type(n) is not int or n < 2:
            raise ValueError('Explicit integer quadrature orders >=2 required')
    if fourier_points_per_axis % 2:
        raise ValueError('Even Gauss-Legendre Fourier order required: no exact zero-mode inverse')
    if source_azimuth_count < 4 or observation_azimuth_count < 4:
        raise ValueError('At least four full-circle angular nodes required')
    pins = {}
    def load_json(p):
        pins[str(p)] = sha(p)
        return json.loads(p.read_text())
    profile = load_json(C/'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json')['galaxies']['NGC3198']
    binding = load_json(C/'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json')
    manifest=load_json(C/'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json')
    queries=[{'id':r['query_id'],'radius_kpc':float(r['Rad_text'])} for r in manifest['rows']]
    if len(queries)!=43 or any(r['Rad_unit']!='kpc' for r in manifest['rows']):
        raise ValueError('Exact target-free43 roster required')
    tail_path=C/'NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt'
    if sha(tail_path)!='157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2':
        raise ValueError('Adopted actual tail reduction changed')
    tail=load_json(tail_path)
    h2path=Path(tail['source']['path'])
    if sha(h2path)!=tail['source']['sha256']: raise ValueError('Actual H2 source pin changed')
    h2rows=load_json(h2path)['S1_alternative_and_stellar_median_rows']['rows'][:10]
    from fractions import Fraction
    hr=[float(Fraction(r['radius_kpc_literal']['value'])) for r in h2rows]
    hs=[float(Fraction(r['components']['H2']['value_literal']['value'])) for r in h2rows]
    if any(r['conventions']['gas_helium']['value']!='ALREADY_INCLUDED' for r in h2rows):
        raise ValueError('H2 helium convention changed')
    if not math.isfinite(h2_tail_mass_rtol) or h2_tail_mass_rtol<=0:
        raise ValueError('Explicit positive finite tail-mass arithmetic tolerance required')
    if sha(COEFFICIENT) != COEFFICIENT_SHA: raise ValueError('Frozen response pin mismatch')
    pins[str(COEFFICIENT)] = COEFFICIENT_SHA
    with np.load(COEFFICIENT, allow_pickle=False) as data:
        grid = data['source_hessian_grid'].copy()
        mubar = data['background_mu'].copy()
        Cbar = data['background_C'].copy()
    mods = {}
    paths = {
        'trial': HERE/'galaxy_coupled_fourier_hi_prediction_v004.py',
        'vertical_line': HERE/'owned_fixed_xy_fourier_line_v001.py',
        'coupled': HERE/'coupled_hi_fourier_source_iteration_v005.py',
        'fourier': HC/'owned_physical_fourier_metric_quadrature_v004.py',
        'source': HERE/'baryonic_metric_source_columns_v003.py',
        'streaming': HERE/'galaxy_baryonic_source_forward_v002.py',
        'observation': HERE/'galaxy_hi_observation_forward_v001.py',
        'hi': HC/'hi_two_sided_free_boundary_v002.py',
        'quadrature': HERE/'general_column_mass_quadrature_v002.py',
        'metric': HC/'owned_fourier_physical_metric_evaluator_v002.py',
        'cardinal': HC/'owned_positive_cardinal_source_hessian_v001.py',
        'complex': HC/'owned_complex_symbol_metric_binding_v002.py',
        'static': HP/'owned_static_action_metric_binding_v002.py',
        'bernstein': KERNEL}
    for name, path in paths.items(): mods[name] = module(path, pins)
    c = 299792458.0
    pc_m = kpc_m/1000
    sigma_unit = solar_mass_kg/(pc_m*pc_m)
    gas = profile['HI_plus_He']; stars = profile['stellar_reference']
    edges = [float(x) for x in gas['s_edges_kpc2']]
    means = [float(x) for x in gas['annular_means_Msun_pc2']]
    controls = [float(x) for x in gas['boundary_controls_Msun_pc2']]
    hi_options = dict(sigma0_m_s=11000., gamma=5/3,
        search_step_m=hi_search_step_kpc*kpc_m,
        search_limit_m=hi_search_limit_kpc*kpc_m,
        root_tolerance_m=hi_root_tolerance_kpc*kpc_m,
        log_lapse_tolerance=hi_log_lapse_tolerance,
        max_metric_calls=hi_max_metric_calls, panels_per_side=hi_panels_per_side)
    def hi_profile(R):
        p = mods['bernstein'].annular_bernstein_sigma(s_edges=edges,
            annular_means=means, boundary_controls=controls,
            s_query=[float((R/kpc_m)**2)])
        if not p['ok']: raise ValueError('HI query outside actual smooth source support: '+str(p['failures']))
        return {'Sigma_kg_m2': float(p['sigma'][0])*sigma_unit,
                'hi_options': dict(hi_options)}
    # Complete signed tensor Gauss-Legendre cube (nonperiodic quadrature):
    # fourier_points_per_axis is the even Gauss order. A finite k cutoff is NOT a physical
    # exterior bound or a declaration that omitted wavelengths carry no error.
    nk = fourier_points_per_axis
    kmax = kmax_inverse_kpc/kpc_m
    if composite_grid_spec_anisotropic is not None:
        waves,dkweights=cut_helper.tensor_grid(composite_grid_spec_anisotropic,kpc_m,kmax_inverse_kpc)
        grid_description='Anisotropic signed tensor T120L; '+json.dumps(composite_grid_spec_anisotropic,sort_keys=True)
    else:
        if composite_grid_spec is None:
            k_nodes, k_weights = np.polynomial.legendre.leggauss(nk)
            axis = kmax*k_nodes
            axis_weights = kmax*k_weights
            grid_description='Uniform tensor Gauss-Legendre cube'
        else:
            spec=composite_grid_spec
            breaks=np.asarray(spec['breaks_inverse_kpc'],dtype=float)
            orders=spec['panel_orders']
            if breaks.ndim!=1 or len(breaks)!=len(orders)+1 or not np.isfinite(breaks).all() or breaks[0]!=-kmax_inverse_kpc or breaks[-1]!=kmax_inverse_kpc or np.any(np.diff(breaks)<=0):
                raise ValueError('Composite panels must partition exactly [-kmax,kmax]')
            if any(type(n)is not int or n<2 for n in orders) or sum(orders)!=nk or nk>80 or spec['total_axis_nodes']!=nk:
                raise ValueError('Composite node budget/order mismatch')
            if not np.array_equal(breaks,-breaks[::-1]) or orders!=orders[::-1]:
                raise ValueError('Composite panels/orders must retain signed reflection symmetry')
            axis_parts=[];weight_parts=[]
            for lo,hi,n in zip(breaks[:-1],breaks[1:],orders):
                gxk,gwk=np.polynomial.legendre.leggauss(n)
                axis_parts.append(((lo+hi)/2+(hi-lo)*gxk/2)/kpc_m)
                weight_parts.append((hi-lo)*gwk/(2*kpc_m))
            axis=np.concatenate(axis_parts)
            axis_weights=np.concatenate(weight_parts)
            if np.any(axis==0): raise ValueError('This quadrature excludes the unsupported zero mode')
            grid_description='Composite tensor Gauss cube; same physical cutoff; '+json.dumps(spec,sort_keys=True)
        waves = np.array([(x,y,z) for x in axis for y in axis for z in axis])
        dkweights = np.array([wx*wy*wz for wx in axis_weights
                             for wy in axis_weights for wz in axis_weights])
    # Both signs retained once; weights include physical d^3k Jacobian only.
    # Fourier evaluator applies (2pi)^-3. Nonuniformity proves no accuracy bound.
    if not np.all(np.isfinite(waves)) or not np.all(np.isfinite(dkweights)) or np.any(dkweights<=0):
        raise ValueError('Nonfinite or underflowed physical Fourier quadrature')
    gx, gw = np.polynomial.legendre.leggauss(source_gauss_order)
    gauss = [(float(x),float(w)) for x,w in zip(gx,gw)]
    phis = [2*math.pi*i/source_azimuth_count for i in range(source_azimuth_count)]
    dphi = 2*math.pi/source_azimuth_count
    # HI quadrature in s=R²: R dR=ds/2. No double helium or distance conversion.
    gas_columns = []
    for lo,hi in zip(edges,edges[1:]):
        for x,w in gauss:
            s = (lo+hi)/2+(hi-lo)*x/2
            R = math.sqrt(s)*kpc_m
            dR = (hi-lo)*w*kpc_m*kpc_m/(4*R)
            p = hi_profile(R)
            # Exactly zero measured/reconstructed bins contain no reference mass;
            # no positive-density hydrostatic column is claimed for such a bin.
            if p['Sigma_kg_m2'] == 0: continue
            for phi in phis:
                gas_columns.append(dict(R_m=R,phi=phi,radial_weight_m=dR,
                    azimuth_weight_rad=dphi,**p))
    gas_columns,cut_record=cut_helper.apply_cut(gas_columns,ngc_outer_gas_cut,kpc_m,call_controls)
    if ngc_outer_gas_cut is not None:pins[ngc_outer_gas_cut['path']]=ngc_outer_gas_cut['sha256']
    pins[str(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py'))]='5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353'
    # Stellar distribution is held in the physical frozen-background chart at
    # this leading weak-field order. It is not updated as a full metric fluid.
    # Open Gauss nodes integrate the FULL declared exponential radial tail and
    # sech² vertical tail via variable transforms, without a finite height clip.
    radii = [float(x) for x in stars['radius_kpc']]
    sigmas = [float(x) for x in stars['surface_density_Msun_pc2']]
    rd = float(stars['outer_scale_kpc']); height = float(stars['height_kpc'])
    radial_nodes = []
    cuts = sorted(set([0.]+radii))
    for lo,hi in zip(cuts,cuts[1:]):
        for x,w in gauss:
            radial_nodes.append(((lo+hi)/2+(hi-lo)*x/2,(hi-lo)*w/2))
    for x,w in gauss:
        u=(x+1)/2
        radial_nodes.append((radii[-1]-rd*math.log(u),rd*w/(2*u)))
    positions=[]; columns=[]; stellar_mass=0.
    star_R=[];star_z=[];star_mass=[]
    for r,dr in radial_nodes:
        Sigma=mods['streaming'].radial_surface(r,radii,sigmas,outer_scale=rd)*sigma_unit
        for u,w in gauss:
            star_R.append(r*kpc_m)
            star_z.append(2*height*kpc_m*math.atanh(u))
            star_mass.append(Sigma*(r*kpc_m)*(dr*kpc_m)*(2*math.pi)*w/2)
        for phi in phis:
            mass_column=Sigma*(r*kpc_m)*(dr*kpc_m)*dphi
            for u,w in gauss:
                # sech²(z/2h)/(4h) dz = du/2, u=tanh(z/2h).
                z=2*height*kpc_m*math.atanh(u)
                mass=mass_column*w/2
                positions.append([r*kpc_m*math.cos(phi),r*kpc_m*math.sin(phi),z])
                columns.append([[-mass*c*c]]+[[0.] for _ in range(9)])
                stellar_mass += mass
    # H2: measured-center linear interpolation, constant unresolved core;
    # root-selected infinite exponential tail. The same stellar-height tracer
    # is a counted approximation, not measured molecular hydrostatics.
    h2_radial=[]
    cuts_h2=[0.]+hr
    for lo,hi in zip(cuts_h2,cuts_h2[1:]):
        for x,w in gauss:
            r=(lo+hi)/2+(hi-lo)*x/2;dr=(hi-lo)*w/2
            sigma=mods['streaming'].radial_surface(r,hr,hs,outer_scale=float(tail['outer_scale_kpc']))
            h2_radial.append((r,2*math.pi*sigma*sigma_unit*(r*kpc_m)*(dr*kpc_m)))
    # u=exp(-(R-Rlast)/Rd) maps the WHOLE tail to(0,1).
    # Positive mapped GL weights are normalized to its exact known total mass.
    # This mass-preserving quadrature does not certify Fourier shape accuracy.
    hrd=float(tail['outer_scale_kpc']);last=hr[-1]
    tail_exact=2*math.pi*hs[-1]*sigma_unit*kpc_m*kpc_m*hrd*(last+hrd)
    tail_nodes=[]
    for x,w in gauss:
        u=(x+1)/2;r=last-hrd*math.log(u)
        mass=2*math.pi*hs[-1]*sigma_unit*kpc_m*kpc_m*hrd*r*w/2
        tail_nodes.append((r,mass))
    raw_tail=math.fsum(m for r,m in tail_nodes)
    factor=tail_exact/raw_tail
    if not all(math.isfinite(v) and v>0 for v in (hrd,tail_exact,raw_tail,factor)):
        raise ValueError('Invalid tail mass/quadrature')
    normalized_tail=[(r,m*factor) for r,m in tail_nodes]
    tail_actual=math.fsum(m for r,m in normalized_tail)
    tail_error=abs(tail_actual-tail_exact)/tail_exact
    if not math.isfinite(tail_error) or tail_error>h2_tail_mass_rtol:
        raise ValueError('H2 tail total mass outside explicit arithmetic tolerance')
    h2_radial.extend(normalized_tail)
    molecular_mass=math.fsum(m for r,m in h2_radial)
    for r,ring_mass in h2_radial:
        for u,w in gauss:
            z=2*height*kpc_m*math.atanh(u);mass=ring_mass*w/2
            star_R.append(r*kpc_m);star_z.append(z);star_mass.append(mass)
            for phi in phis:
                positions.append([r*kpc_m*math.cos(phi),r*kpc_m*math.sin(phi),z])
                columns.append([[-mass/source_azimuth_count*c*c]]+[[0.] for _ in range(9)])
    h2_custody=dict(reduction=tail,tail_mass_exact_kg=tail_exact,tail_mass_quadrature_kg=tail_actual,
        tail_mass_relative_error=tail_error,tail_mass_rtol=h2_tail_mass_rtol,
        mapped_GL_raw_mass_kg=raw_tail,mapped_GL_mass_normalization=factor,
        molecular_total_quadrature_mass_kg=molecular_mass,
        scope='He once; linear centers/constant core/matched infinite exponential tail; positive mass-normalized mapped GL, Fourier radial/z error unbounded; stellar-height proxy. Outer missing observations remain missing.')
    fixed_positions=np.asarray(positions); fixed_J=np.asarray(columns)
    # A razor-thin HI initial iterate only, never the returned HI preparation.
    gaspos=[]; gasJ=[]
    gas_R=[];gas_z=[];gas_mass=[]
    for col in gas_columns:
        R=col['R_m']; phi=col['phi']
        mass=col['Sigma_kg_m2']*R*col['radial_weight_m']*col['azimuth_weight_rad']
        if phi==phis[0]:
            gas_R.append(R);gas_z.append(0.)
            gas_mass.append(col['Sigma_kg_m2']*R*col['radial_weight_m']*(2*math.pi))
        gaspos.append([R*math.cos(phi),R*math.sin(phi),0.])
        gasJ.append([[-mass*c*c]]+[[0.] for _ in range(9)])
    initial = None if analytic_initial_azimuth else mods['source'].physical_source_fourier(physical_positions_m=gaspos,
        integrated_columns_J=gasJ,k_physical_inverse_m=waves)
    def boundary(pos):
        n=len(pos)
        return dict(boundary_fields=np.zeros((n,10,1)),
            boundary_gradient=np.zeros((n,10,1,3)),
            boundary_hessian=np.zeros((n,10,1,3,3)))
    fa=dict(source_hessian_grid=grid,k_physical=waves,dk_weights=dkweights,
        registered_bravais=np.array([[0.,.5,.5],[.5,0.,.5],[.5,.5,0.]]),
        jbar=np.zeros(9),mubar=mubar,Cbar=Cbar,Eref=Eref_J,ell_F=ell_F_m,gamma=gamma,
        cardinal_module=mods['cardinal'],complex_binding_module=mods['complex'],
        static_binding_module=mods['static'],relative_singular_floor=relative_singular_floor,
        hermitian_tolerance=hermitian_tolerance,full_residual_relative_tolerance=solve_rtol,
        full_residual_absolute_tolerance=solve_atol,node_convention='full_signed',
        real_source_pairing_declared=True,
        finite_domain_description=grid_description+'; no cutoff or quadrature error bound; stellar and adopted H2 tails mapped to full support; actual HI annuli only.',
        boundary_description='Isolated frozen background N=1,Cbar; zero boundary perturbations/external tide; unmeasured extra source zero only in restricted reference.')
    fixed_source_fourier=None
    bessel_custody=None
    if type(analytic_initial_azimuth) is not bool:
        raise ValueError('Explicit boolean initial azimuth branch required')
    if analytic_initial_azimuth:
        provider=module(HERE/'posix_libm_bessel_j0_provider_v001.py',pins)
        j0,bessel_custody=provider.create_provider()
        analytic=module(HERE/'axisymmetric_initial_rest_energy_fourier_v001.py',pins)
        fixed_source_fourier=analytic.source_fourier(radius_m=star_R,z_m=star_z,
            ring_mass_kg=star_mass,k_physical_inverse_m=waves,c_m_s=c,bessel_j0=j0)
        initial=analytic.source_fourier(radius_m=gas_R,z_m=gas_z,
            ring_mass_kg=gas_mass,k_physical_inverse_m=waves,c_m_s=c,bessel_j0=j0)
        bessel_custody['source_scope']='Analytic azimuth of declared axisymmetric initial source only; numerical Bessel evaluation and radial/z quadrature retained'
    return dict(queries=queries,hi_profile_at_radius=hi_profile,c_m_s=c,ngc_outer_gas_cut=cut_record,composite_grid_spec=composite_grid_spec_anisotropic or composite_grid_spec,grid_description=grid_description,quadrature_weight_sum=float(np.sum(dkweights)),quadrature_weight_sum_expected=float((2*kmax)**3),fixed_source_fourier_J=fixed_source_fourier,bessel_custody=bessel_custody,
        analytic_initial_azimuth=analytic_initial_azimuth,
        fourier_arguments=fa,modules=mods,boundary=boundary,
        fixed_positions_m=fixed_positions,fixed_integrated_columns_J=fixed_J,
        initial_gas_fourier_J=initial,gas_columns=gas_columns,source_pins=pins,
        stellar_quadrature_mass_kg=stellar_mass,molecular_quadrature_mass_kg=molecular_mass,H2_custody=h2_custody)
