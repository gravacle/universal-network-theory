"""Inert full NGC43 join: reviewed composite prep ->0424 gas ->line-cached motion.
No numerical defaults, launch, solver implementation or new source model.
"""
import hashlib
import math
from pathlib import Path
import types


def evaluate(*, prep_module, prep_arguments, solver_module, accepted_solver_sha256,
             composite_adapter, streaming_adapter, streaming_base,
             prediction_module, accepted_module_pins, checkpoint,
             node_log_directory, start_iteration, progress_callback=None):
    """Root supplies accepted module paths/hashes and explicit prep controls.

    Node logs use a new attempt directory, while checkpoint directory is reused
    only with unchanged identity. All actual source/provisional failures retained.
    Observation branch is exactly the existing driver reference (72/73 degrees,
    positive orientation, supplied equal-angle count), not new empirical weights.
    """
    modules=(prep_module,solver_module,composite_adapter,streaming_adapter,streaming_base,prediction_module)
    pins={}
    for module in modules:
        path=str(Path(module.__file__).resolve())
        actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if accepted_module_pins.get(path)!=actual: raise ValueError('Unaccepted binding module: '+path)
        pins[path]=actual
    if pins[str(Path(solver_module.__file__).resolve())]!=accepted_solver_sha256:
        raise ValueError('Solver pin disagreement')
    if prep_arguments['analytic_initial_azimuth'] is not True or prep_arguments['composite_grid_spec'] is None:
        raise ValueError('Declared analytic initial source and composite grid required')
    data=prep_module.prepare_inputs(**prep_arguments)
    facade=streaming_adapter.make_fourier_module(base_module=streaming_base,
        log_directory=node_log_directory,start_iteration=start_iteration)
    data['modules']['fourier']=facade
    data['source_pins'].update(facade.source_pins)
    data['source_pins'].update(pins)
    mods=data['modules'];controls=prep_arguments
    ck=None
    if checkpoint is not None:
        ck=dict(checkpoint);identity=dict(ck['caller_identity'])
        if 'composite_full_driver' in identity: raise ValueError('Driver identity already assigned')
        # Attempt log location/start index are deliberately excluded; physical and
        # integration controls, code and source arrays remain checkpoint-bound.
        stable_controls={k:v for k,v in controls.items() if k!='progress_directory'}
        # Complete c2v003 caller contract, from ACTUAL prepared inputs. The
        # checkpoint separately hashes all source arrays, roster and modules.
        fa=data['fourier_arguments']
        physical=dict(Eref_J=fa['Eref'],ell_F_m=fa['ell_F'],gamma=fa['gamma'],
            solar_mass_kg=controls['solar_mass_kg'],kpc_m=controls['kpc_m'],c_m_s=data['c_m_s'],
            Cbar=fa['Cbar'],mubar=fa['mubar'],jbar=fa['jbar'],
            registered_bravais=fa['registered_bravais'],
            hi_options_by_column=[dict(col['hi_options']) for col in data['gas_columns']])
        supplied=identity.get('physical_parameters',{})
        for name in ('Eref_J','ell_F_m','gamma','solar_mass_kg','kpc_m'):
            if name in supplied and supplied[name]!=physical[name]:
                raise ValueError('Caller/prepared physical parameter mismatch: '+name)
        identity['physical_parameters']=physical
        identity['numerical_controls']=stable_controls
        identity['source_parameters']=dict(source_pins=dict(data['source_pins']),
            stellar_quadrature_mass_kg=data['stellar_quadrature_mass_kg'],
            fixed_source_selection='SUPPLIED analytic initial fixed source; included once',
            updated_gas='Actual phi-dependent Cartesian columns; no J0 replacement',
            preparation_scope='Adopted reference rest-energy source, N-only HI vertical preparation')
        identity['boundary_prescription']=fa['boundary_description']
        # These are all mandatory caller fields in accepted c2v003 _identity.
        for name in ('code_pins','boundary_prescription','physical_parameters','numerical_controls'):
            if name not in identity:raise ValueError('Missing checkpoint caller field: '+name)
        if not isinstance(identity['boundary_prescription'],str) or not identity['boundary_prescription'].strip():
            raise ValueError('Explicit actual boundary prescription required')
        identity['code_pins']=dict(identity['code_pins'])
        identity['code_pins'].update(data['source_pins'])
        identity['code_pins'].update(pins)
        identity['composite_full_driver']=dict(module_pins=pins,preparation_arguments=stable_controls,
            driver={'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            observation='existing equal-angle harmonic 72/73 degrees orientation+1')
        ck['caller_identity']=identity
    # The prediction module needs these actual metric-read inputs after source
    # convergence. Its solve callback delegates to the already-reviewed adaptor.
    ca=dict(fourier_module=facade,metric_module=mods['metric'],hi_module=mods['hi'],
        quadrature_module=mods['quadrature'],fourier_arguments=data['fourier_arguments'],
        c_m_s=data['c_m_s'],boundary_jet_at_positions=data['boundary'],
        reality_atol=controls['reality_atol'],reality_rtol=controls['reality_rtol'])
    custody={}
    def solve(**arguments):
        if set(arguments)!=set(ca) or any(arguments[k] is not ca[k] for k in ca):
            raise ValueError('Prediction changed bound coupled read arguments')
        answer=composite_adapter.solve_prepared(prepared=data,solver_module=solver_module,
            accepted_solver_sha256=accepted_solver_sha256,preparation_file=prep_module.__file__,
            accepted_preparation_sha256=pins[str(Path(prep_module.__file__).resolve())],
            c_m_s=data['c_m_s'],max_iterations=controls['max_iterations'],relaxation=controls['relaxation'],
            source_atol_J=controls['source_atol_J'],source_rtol=controls['source_rtol'],
            reality_atol=controls['reality_atol'],reality_rtol=controls['reality_rtol'],
            checkpoint=ck,progress_callback=progress_callback)
        custody.update(answer['binding_custody'])
        return answer['result']
    coupled=types.SimpleNamespace(solve=solve)
    n=controls['observation_azimuth_count']
    angular=[{'phi_rad':2*math.pi*i/n,'fit_weight':1/n} for i in range(n)]
    queries=data['queries']
    if len(queries)!=43: raise ValueError('NGC43 roster required')
    result=prediction_module.evaluate(coupled_module=coupled,coupled_arguments=ca,
        hi_profile_at_radius=data['hi_profile_at_radius'],queries=queries,kpc_m=controls['kpc_m'],
        pressure_step_m=[controls['pressure_step_kpc']*controls['kpc_m']]*len(queries),
        pressure_atol_Pa_per_m=controls['pressure_atol_Pa_per_m'],pressure_rtol=controls['pressure_rtol'],
        streaming_module=mods['streaming'],observation_module=mods['observation'],
        physical_inclination=math.radians(72),released_inclination=math.radians(73),orientation=1,
        circular_reference_assumption='Counted azimuth-resolved circular trial, not a stationary anisotropic flow; equal-angle equal-fit-weight thin harmonic approximation.',
        azimuth_nodes=[list(angular) for _ in queries],azimuth_step_rad=[controls['azimuth_step_rad']]*len(queries),
        adiabatic_K_transport=True,vertical_fourier_module=mods['vertical_line'])
    return dict(result=result,H2_custody=data['H2_custody'],binding_custody=custody,source_pins=data['source_pins'],
        composite_grid_spec=data['composite_grid_spec'],quadrature_weight_sum=data['quadrature_weight_sum'],
        quadrature_weight_sum_expected=data['quadrature_weight_sum_expected'],
        bessel_custody=data['bessel_custody'],accepted_for_calibration=False,
        uncertainty='Original failed mixing retained; no quadrature/tail/source/stencil convergence certificate.')
