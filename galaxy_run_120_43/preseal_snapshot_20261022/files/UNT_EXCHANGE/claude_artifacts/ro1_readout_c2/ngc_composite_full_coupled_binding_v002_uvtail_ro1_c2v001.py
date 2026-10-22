"""Inert full NGC43 join: reviewed composite prep ->0424 gas ->line-cached motion.
No numerical defaults, launch, solver implementation or new source model.
UVTAIL c2v001 (Claude2 tail_scheme_impl_c2/route_a; successor of cc5db369, the NGC binding v002 lineage of
route_a_f10/LAUNCH.json d70cbcfe; TAIL_SCHEME_DESIGN_V002 sec 2.1 A14, 3.5, K16): optional uv_tail=dict(controller_module,
request, sidecar_directory). uv_tail=None executes the reviewed statements. Supplied: controller from the prep result
(galaxy NGC3198: stars + H2 of the prep's own reduction source), data['boundary'] (L82 slot) IS controller.boundary,
the solver is the uvtail successor's bind_uv_tail view, the checkpoint identity carries numerical_controls.uv_tail.
No facade on this path (HI v002 reads N, which includes the tail through the boundary slot).
RO1 c2v001 (Claude2 ro1_readout_c2; successor of e666bede; ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM
A42.2): once the bound solve has RETURNED a converged finite fixed point, a ValueError raised by the circular-trial readout
(prediction v005 after its L56 convergence check) whose message is exactly one of RO1_MESSAGES is recorded as
ROUTE_A_READOUT_NO_CIRCULAR_BRANCH (query, phi, R, numerator, denominator, message) and the converged solve is returned
with predictions_available False and rows None (readout rows unavailable). Every other exception, and any exception
raised before the solve returns, propagates unchanged. The streaming and metric modules the readout calls are
pass-through recorders (same function, same keyword arguments, same return object); nothing else changes.
"""
import hashlib
import math
from pathlib import Path
import types

RO1_CODE='ROUTE_A_READOUT_NO_CIRCULAR_BRANCH'
RO1_MESSAGES=('NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH','NON_TIMELIKE_COLUMN')  # A42.2, exact str(exc) only
RO1_RULE='RO1 (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM A42.2)'


def _ro1_views(streaming_module,metric_module,state):
    """RO1: pass-through views recording the last metric read (R,phi,z) and the last streaming call (index, kwargs)."""
    def evaluate_point(**kw):
        state['metric_read']=(kw['R'],kw['phi'],kw['z'])
        return metric_module.evaluate_point(**kw)
    def pressure_streaming_speed(**kw):
        state['calls']+=1;state['call']=(state['calls'],dict(kw),state['metric_read'])
        try:
            return streaming_module.pressure_streaming_speed(**kw)
        except BaseException as exc:
            state['raised']=exc
            raise
    return (types.SimpleNamespace(__file__=streaming_module.__file__,pressure_streaming_speed=pressure_streaming_speed),
            types.SimpleNamespace(__file__=metric_module.__file__,evaluate_point=evaluate_point))


def _ro1_number(x):
    try: x=float(x)
    except (TypeError,ValueError,OverflowError): return repr(x)
    return x if math.isfinite(x) else repr(x)


def _ro1_record(exc,state,queries,kpc_m):
    """RO1: the refusal record (event field names of the V007 compare FIELDS.md route_a_outcome/ro1/events[], A48 AMB-15:
    code, refusal, query = 1-based roster position, phi_rad, R_kpc, numerator, denominator, after_convergence).
    numerator/denominator are pressure_streaming_speed's own L201-203 arithmetic on the arguments of the call that raised;
    None when the refusal was not raised by that call. message = refusal = str(exc)."""
    rec={'code':RO1_CODE,'refusal':str(exc),'message':str(exc),'rule':RO1_RULE,'after_convergence':True,
         'query':None,'query_id':None,'phi_rad':None,'R_kpc':None,'R_m':None,'numerator':None,'denominator':None,
         'streaming_call_index':None,
         'raised_by':'pressure_streaming_speed' if state['call'] is not None and state['raised'] is exc else 'circular_trial_readout'}
    read=state['metric_read']
    if rec['raised_by']=='pressure_streaming_speed':
        n,kw,read=state['call']
        rec['streaming_call_index']=n
        rec['streaming_arguments']={k:_ro1_number(v) for k,v in kw.items()}
        try:
            pgrad=float(kw['d_pressure'])/(float(kw['energy_density'])+float(kw['pressure']))
            num=float(kw['d_log_N'])+pgrad;den=float(kw['d_log_R'])+pgrad
            rec.update(pgrad=_ro1_number(pgrad),numerator=_ro1_number(num),denominator=_ro1_number(den),
                       v2_over_c2=_ro1_number(num/den) if den!=0 else None)
        except (KeyError,TypeError,ValueError,ArithmeticError) as e:
            rec['numerator_note']='not computable from the call arguments: %s: %s'%(type(e).__name__,e)
    if read is not None:
        R,phi,z=read
        rec.update(R_m=_ro1_number(R),phi_rad=_ro1_number(phi),metric_read_z_m=_ro1_number(z))
        hit=[i for i,q in enumerate(queries) if float(q['radius_kpc'])*kpc_m==R]
        if len(hit)==1:
            rec.update(query=hit[0]+1,query_id=queries[hit[0]]['id'],R_kpc=float(queries[hit[0]]['radius_kpc']))
        else:
            rec['R_kpc']=_ro1_number(R/kpc_m)
    return rec


def evaluate(*, prep_module, prep_arguments, solver_module, accepted_solver_sha256,
             composite_adapter, streaming_adapter, streaming_base,
             prediction_module, accepted_module_pins, checkpoint,
             node_log_directory, start_iteration, progress_callback=None, uv_tail=None):
    """Root supplies accepted module paths/hashes and explicit prep controls.

    Node logs use a new attempt directory, while checkpoint directory is reused
    only with unchanged identity. All actual source/provisional failures retained.
    Observation branch is exactly the existing driver reference (72/73 degrees,
    positive orientation, supplied equal-angle count), not new empirical weights.
    """
    modules=(prep_module,solver_module,composite_adapter,streaming_adapter,streaming_base,prediction_module)
    if uv_tail is not None: modules=modules+(uv_tail['controller_module'],)  # UVTAIL: controller pinned like the rest
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
    controller=None
    if uv_tail is not None:
        # UVTAIL: tail controller from this prep result; its TailBoundary replaces the zero boundary closure.
        if not hasattr(solver_module,'bind_uv_tail'): raise ValueError('UV-tail solver successor required')
        controller=uv_tail['controller_module'].RouteATailController.from_prepared(galaxy='NGC3198',
            prep_module=prep_module,prep_arguments=prep_arguments,data=data,request=uv_tail['request'],
            sidecar_directory=uv_tail['sidecar_directory'])
        data['boundary']=controller.boundary
        solver_module=solver_module.bind_uv_tail(controller)
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
        identity['numerical_controls']=stable_controls if controller is None else dict(stable_controls,uv_tail=controller.identity())
        identity['source_parameters']=dict(source_pins=dict(data['source_pins']),
            stellar_quadrature_mass_kg=data['stellar_quadrature_mass_kg'],
            fixed_source_selection='SUPPLIED analytic initial fixed source; included once',
            updated_gas='Actual phi-dependent Cartesian columns; no J0 replacement',
            preparation_scope='Adopted reference rest-energy source, N-only HI vertical preparation')
        identity['boundary_prescription']=fa['boundary_description']
        if controller is not None: identity['boundary_prescription']+=controller.boundary_prescription_suffix()
        # These are all mandatory caller fields in accepted c2v003 _identity.
        for name in ('code_pins','boundary_prescription','physical_parameters','numerical_controls'):
            if name not in identity:raise ValueError('Missing checkpoint caller field: '+name)
        if not isinstance(identity['boundary_prescription'],str) or not identity['boundary_prescription'].strip():
            raise ValueError('Explicit actual boundary prescription required')
        identity['code_pins']=dict(identity['code_pins'])
        identity['code_pins'].update(data['source_pins'])
        identity['code_pins'].update(pins)
        if controller is not None: identity['code_pins'].update(uv_tail['controller_module'].code_pins())
        identity['composite_full_driver']=dict(module_pins=pins,preparation_arguments=stable_controls,
            driver={'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            observation='existing equal-angle harmonic 72/73 degrees orientation+1')
        ck['caller_identity']=identity
    # The prediction module needs these actual metric-read inputs after source
    # convergence. Its solve callback delegates to the already-reviewed adaptor.
    ro1={'calls':0,'call':None,'raised':None,'metric_read':None,'solved':None}  # RO1
    ro1_streaming,ro1_metric=_ro1_views(mods['streaming'],mods['metric'],ro1)  # RO1: pass-through recorders
    ca=dict(fourier_module=facade,metric_module=ro1_metric,hi_module=mods['hi'],
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
        ro1['solved']=answer['result']  # RO1: set only once the solve has RETURNED
        return answer['result']
    coupled=types.SimpleNamespace(solve=solve)
    n=controls['observation_azimuth_count']
    angular=[{'phi_rad':2*math.pi*i/n,'fit_weight':1/n} for i in range(n)]
    queries=data['queries']
    if len(queries)!=43: raise ValueError('NGC43 roster required')
    try:  # RO1
        result=prediction_module.evaluate(coupled_module=coupled,coupled_arguments=ca,
            hi_profile_at_radius=data['hi_profile_at_radius'],queries=queries,kpc_m=controls['kpc_m'],
            pressure_step_m=[controls['pressure_step_kpc']*controls['kpc_m']]*len(queries),
            pressure_atol_Pa_per_m=controls['pressure_atol_Pa_per_m'],pressure_rtol=controls['pressure_rtol'],
            streaming_module=ro1_streaming,observation_module=mods['observation'],
            physical_inclination=math.radians(72),released_inclination=math.radians(73),orientation=1,
            circular_reference_assumption='Counted azimuth-resolved circular trial, not a stationary anisotropic flow; equal-angle equal-fit-weight thin harmonic approximation.',
            azimuth_nodes=[list(angular) for _ in queries],azimuth_step_rad=[controls['azimuth_step_rad']]*len(queries),
            adiabatic_K_transport=True,vertical_fourier_module=mods['vertical_line'])
    except ValueError as exc:  # RO1 (A42.2): only the named readout refusals, only after a returned converged solve
        solved=ro1['solved']
        if not (type(exc) is ValueError and str(exc) in RO1_MESSAGES and isinstance(solved,dict)
                and solved.get('converged_finite_fixed_point') is True):
            raise
        result={'predictions_available':False,'rows':None,'readout_status':RO1_CODE,
            'route_a_readout_refusal':_ro1_record(exc,ro1,queries,controls['kpc_m']),'source_fixed_point':solved,
            'reason':'RO1: converged finite fixed point; circular-trial readout refused (%s); no velocity rows manufactured; '
                     'route B proceeds on the checkpoint'%str(exc),
            'accepted_for_calibration':False}
    return dict(result=result,H2_custody=data['H2_custody'],binding_custody=custody,source_pins=data['source_pins'],
        composite_grid_spec=data['composite_grid_spec'],quadrature_weight_sum=data['quadrature_weight_sum'],
        quadrature_weight_sum_expected=data['quadrature_weight_sum_expected'],
        bessel_custody=data['bessel_custody'],accepted_for_calibration=False,
        uncertainty='Original failed mixing retained; no quadrature/tail/source/stencil convergence certificate.',
        **({} if controller is None else {'uv_tail':controller.last_record}))
