"""INERT DDO12 actual-source trial entry point; root alone executes under a guard.
No target velocities, likelihood, fitting, hidden coefficient defaults or acceptance.
Requires supplied Eref [J], ell_F [m], gamma and explicit numerical resolutions.
Frozen single-point native response remains provisional; not a 12-coordinate fit.
RESUME c2v002 (Claude2 0422): identical physics/inputs; coupled solver is the
v005_resume_c2v001 copy. Optional --checkpoint-directory [--resume-checkpoint]
saves/restores exact completed-HI-column state; omitted, behaviour is v009.
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
COEFFICIENT = C/'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz'
COEFFICIENT_SHA = 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'
R0422 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module(path, pins):
    path = Path(path)
    pins[str(path)] = sha(path)
    spec = importlib.util.spec_from_file_location('ddo_'+path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def run(*, Eref_J, ell_F_m, gamma, solar_mass_kg, kpc_m,
        kmax_inverse_kpc, fourier_points_per_axis, source_gauss_order,
        source_azimuth_count, observation_azimuth_count,
        pressure_step_kpc, azimuth_step_rad, hi_search_step_kpc,
        hi_search_limit_kpc, hi_root_tolerance_kpc, hi_log_lapse_tolerance,
        hi_max_metric_calls, hi_panels_per_side, max_iterations, relaxation,
        source_atol_J, source_rtol, pressure_atol_Pa_per_m, pressure_rtol,
        reality_atol, reality_rtol, relative_singular_floor,
        hermitian_tolerance, solve_rtol, solve_atol, progress_directory=None,
        checkpoint_directory=None, resume_checkpoint=False):
    # Every run argument except output/checkpoint locations enters restart identity.
    # (Not named 'controls': that local later holds the HI boundary controls.)
    run_arguments = dict(locals())
    for key in ('progress_directory', 'checkpoint_directory', 'resume_checkpoint'): del run_arguments[key]
    import numpy as np
    if type(resume_checkpoint) is not bool or (resume_checkpoint and checkpoint_directory is None):
        raise ValueError('Explicit checkpoint directory required to resume')
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
    profile = load_json(C/'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json')['galaxies']['DDO154']
    binding = load_json(C/'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json')
    # Deliberately select IDs/radii only; no calibration response/error enters run.
    calibration = load_json(HERE/'DDO154_CURRENT_MODEL_CALIBRATION_INPUT_POPULATED_V001.json')
    queries = [{'id': r['id'], 'radius_kpc': float(r['radius_reference_kpc'])}
               for r in calibration['response_rows']]
    del calibration
    if len(queries) != 12: raise ValueError('Exact designated twelve-query roster required')
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
        'coupled': R0422/'coupled_hi_fourier_source_iteration_v005_resume_c2v001.py',
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
    if checkpoint_directory is not None:
        mods['checkpoint'] = module(R0422/'coupled_gas_checkpoint_c2v001.py', pins)
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
    k_nodes, k_weights = np.polynomial.legendre.leggauss(nk)
    axis = kmax*k_nodes
    axis_weights = kmax*k_weights
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
    for r,dr in radial_nodes:
        Sigma=mods['streaming'].radial_surface(r,radii,sigmas,outer_scale=rd)*sigma_unit
        for phi in phis:
            mass_column=Sigma*(r*kpc_m)*(dr*kpc_m)*dphi
            for u,w in gauss:
                # sech²(z/2h)/(4h) dz = du/2, u=tanh(z/2h).
                z=2*height*kpc_m*math.atanh(u)
                mass=mass_column*w/2
                positions.append([r*kpc_m*math.cos(phi),r*kpc_m*math.sin(phi),z])
                columns.append([[-mass*c*c]]+[[0.] for _ in range(9)])
                stellar_mass += mass
    fixed_positions=np.asarray(positions); fixed_J=np.asarray(columns)
    # A razor-thin HI initial iterate only, never the returned HI preparation.
    gaspos=[]; gasJ=[]
    for col in gas_columns:
        R=col['R_m']; phi=col['phi']
        mass=col['Sigma_kg_m2']*R*col['radial_weight_m']*col['azimuth_weight_rad']
        gaspos.append([R*math.cos(phi),R*math.sin(phi),0.])
        gasJ.append([[-mass*c*c]]+[[0.] for _ in range(9)])
    initial = mods['source'].physical_source_fourier(physical_positions_m=gaspos,
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
        finite_domain_description='Explicit finite signed tensor Gauss-Legendre k cube; no cutoff or quadrature error bound; stellar tails mapped to full support; actual HI annuli only.',
        boundary_description='Isolated frozen background N=1,Cbar; zero boundary perturbations/external tide; unmeasured extra source zero only in restricted reference.')
    progress=None
    if progress_directory is not None:
        import time
        progress_path=Path(progress_directory)
        progress_path.mkdir(exist_ok=False)
        started=time.monotonic()
        def progress(event):
            event=dict(event)
            stage=event['stage']; iteration=event['iteration']
            if stage=='iteration_prepared':
                prepared=event.pop('prepared_metric_response')
                current=event.pop('metric_source_fourier_J')
                with (progress_path/('iteration_%04d_prepared.npz'%iteration)).open('xb') as f:
                    np.savez(f,wavevectors=prepared['wavevectors'],
                        weighted_responses=prepared['weighted_responses'],
                        metric_source_fourier_J=current)
            if stage=='iteration_completed':
                updated=event.pop('reconstructed_gas_fourier_J')
                with (progress_path/('iteration_%04d_gas.npz'%iteration)).open('xb') as f:
                    np.savez(f,reconstructed_gas_fourier_J=updated)
            event['elapsed_seconds']=time.monotonic()-started
            with (progress_path/'progress.jsonl').open('a') as f:
                f.write(json.dumps(serial(event),allow_nan=False)+'\n');f.flush()
    checkpoint=None
    if checkpoint_directory is not None:
        # Identity evidence only; no physical input, boundary or control changes.
        checkpoint=dict(module=mods['checkpoint'],directory=str(checkpoint_directory),
            mode='resume' if resume_checkpoint else 'new',
            caller_identity=dict(code_pins=dict(pins),
                driver_code={'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},
                physical_parameters=dict(Eref_J=Eref_J,ell_F_m=ell_F_m,gamma=gamma,
                    solar_mass_kg=solar_mass_kg,kpc_m=kpc_m,c_m_s=c,hi_options=dict(hi_options)),
                numerical_controls=run_arguments,
                boundary_prescription='boundary(pos): zero perturbation fields (n,10,1), gradient (n,10,1,3), hessian (n,10,1,3,3); isolated frozen background N=1,Cbar restored by metric evaluator; fa boundary_description unchanged'))
    ca=dict(fixed_positions_m=fixed_positions,fixed_integrated_columns_J=fixed_J,
        initial_gas_fourier_J=initial,gas_columns=gas_columns,fourier_arguments=fa,
        boundary_jet_at_positions=boundary,source_module=mods['source'],fourier_module=mods['fourier'],
        metric_module=mods['metric'],hi_module=mods['hi'],quadrature_module=mods['quadrature'],
        c_m_s=c,max_iterations=max_iterations,relaxation=relaxation,source_atol_J=source_atol_J,
        source_rtol=source_rtol,reality_atol=reality_atol,reality_rtol=reality_rtol,vertical_fourier_module=mods['vertical_line'],progress_callback=progress,
        checkpoint=checkpoint)
    angular=[{'phi_rad':2*math.pi*i/observation_azimuth_count,
              'fit_weight':1/observation_azimuth_count} for i in range(observation_azimuth_count)]
    result=mods['trial'].evaluate(coupled_module=mods['coupled'],coupled_arguments=ca,
        hi_profile_at_radius=hi_profile,queries=queries,kpc_m=kpc_m,
        pressure_step_m=[pressure_step_kpc*kpc_m]*12,
        pressure_atol_Pa_per_m=pressure_atol_Pa_per_m,pressure_rtol=pressure_rtol,
        streaming_module=mods['streaming'],observation_module=mods['observation'],
        physical_inclination=math.radians(66),released_inclination=math.radians(64),orientation=1,
        circular_reference_assumption='Counted azimuth-resolved circular trial, not a stationary anisotropic flow; equal-angle equal-fit-weight thin harmonic approximation.',
        azimuth_nodes=[list(angular) for _ in queries],azimuth_step_rad=[azimuth_step_rad]*12,
        adiabatic_K_transport=True)
    return dict(result=result,source_pins=pins,physical_inputs=dict(Eref_J=Eref_J,
        ell_F_m=ell_F_m,gamma=gamma,solar_mass_kg=solar_mass_kg,kpc_m=kpc_m),
        source_realization=dict(stellar_quadrature_mass_kg=stellar_mass,
            stellar_elements=len(positions),gas_columns=len(gas_columns),fourier_modes=len(waves),
            stellar_shape='Frozen-background sech² with full transformed tails; leading weak-field fixed-source approximation.',
            HI_shape='Actual metric-dependent two-sided N-only polytrope, full determinant observed-mass normalization.',
            H2_exterior_masked='Zero EXTRA unmeasured source restricted reference only; no empirical upper bound or complete source assertion.',
            helium='Already included in actual HI annular packet, applied no further time.',
            observation='Equal-angle/equal-fit-weight thin harmonic; not recovered publication weights.'),
        status=('FAILED_SOURCE_PREPARATION' if result.get('predictions_available') is False
            and result.get('source_fixed_point',{}).get('failure') else
            'PROVISIONAL_FROZEN_RESPONSE_CIRCULAR_TRIAL'),accepted_for_calibration=False,
        uncertainty='No mixing-derived errors; finite quadrature/source/stencil errors not certified; wider source/state family retained.')


def serial(value):
    import numpy as np
    if isinstance(value,np.ndarray): return serial(value.tolist())
    if isinstance(value,np.generic): return serial(value.item())
    if isinstance(value,complex): return {'real':value.real,'imag':value.imag}
    if isinstance(value,dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serial(v) for v in value]
    return value


def main():
    p=argparse.ArgumentParser(description=__doc__)
    ints=['fourier_points_per_axis','source_gauss_order','source_azimuth_count',
          'observation_azimuth_count','hi_max_metric_calls','hi_panels_per_side','max_iterations']
    floats=['Eref_J','ell_F_m','gamma','solar_mass_kg','kpc_m','kmax_inverse_kpc',
        'pressure_step_kpc','azimuth_step_rad','hi_search_step_kpc','hi_search_limit_kpc',
        'hi_root_tolerance_kpc','hi_log_lapse_tolerance','relaxation','source_atol_J',
        'source_rtol','pressure_atol_Pa_per_m','pressure_rtol','reality_atol','reality_rtol',
        'relative_singular_floor','hermitian_tolerance','solve_rtol','solve_atol']
    for name in ints: p.add_argument('--'+name.replace('_','-'),type=int,required=True)
    for name in floats: p.add_argument('--'+name.replace('_','-'),type=float,required=True)
    p.add_argument('--progress-directory',default=None)
    p.add_argument('--checkpoint-directory',default=None)
    p.add_argument('--resume-checkpoint',action='store_true')
    args=vars(p.parse_args())
    result=run(**args)
    result['numerical_inputs']=args
    print(json.dumps(serial(result),allow_nan=False,separators=(',',':')))


if __name__=='__main__':
    main()
