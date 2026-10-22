"""Inert concrete source-fixed-point -> HI streaming -> observed row connection.
No coefficient/state/parameter defaults, file reads, target data, or solver fallback.
Conditional stationary no-shift, thin circular-streaming trial only; azimuth resolved.
Full anisotropic response remains in the source solve and returned diagnostics;
this function does not derive axisymmetry or full rotating vertical equilibrium.
"""
import math
import numpy as np


def evaluate(*, coupled_module, coupled_arguments, hi_profile_at_radius,
             queries, kpc_m, pressure_step_m, pressure_atol_Pa_per_m,
             pressure_rtol, streaming_module, observation_module,
             physical_inclination, released_inclination, orientation,
             circular_reference_assumption, azimuth_nodes, azimuth_step_rad,
             adiabatic_K_transport=False, vertical_fourier_module=None):
    """queries: ordered {id,radius_kpc}, 12 or 43, NEVER observed velocities.
    coupled_arguments are the actual solve inputs to coupled HI V002, including
    independently evaluated kernel, same state/calibration, fixed source elements,
    gas integration columns, boundary perturbations and numeric tolerances.
    hi_profile_at_radius(R_m) returns positive Sigma_kg_m2 and hi_options at that
    physical radius using the SAME smooth radial source reconstruction/preparation
    as integration columns (e.g.0403 Bernstein, NOT constant annular lookup).
    hi_options contains sigma0_m_s,gamma and explicit free-boundary budgets.
    pressure_step_m: one positive physical radial stencil step per query. Both
    steps d and d/2 solve actual two-sided columns at R +/- step; R>d required.
    Their derivative difference is reported and tested, NOT a rigorous error bound.
    No extrapolation past source coverage; the profile callable must reject it.
    circular_reference_assumption: nonempty counted model-selection description;
    it is not numerical evidence that the full metric is axisymmetric.
    adiabatic_K_transport optionally reports u^phi partial_phi K and its
    logarithmic rate, conditional on adiabatic isotropic polytropic transport.
    False leaves this diagnostic unassessed; no heating law is supplied.
    Continuity is the stationary zero-radial/vertical-flow trial divergence,
    evaluated at the midplane only, not a whole-column continuity certificate.
    Optional vertical_fourier_module groups exact equal kz at the current fixed
    (x,y); one last line retained, all complex Cartesian jets/boundaries preserved.
    Floating summation grouping changes; no angular average or interpolation.
    SI internally; only final speeds are divided by1000 for km/s observation API.
    """
    if type(adiabatic_K_transport) is not bool:
        raise ValueError('Explicit boolean adiabatic diagnostic selection required')
    if not isinstance(circular_reference_assumption,str) or not circular_reference_assumption.strip():
        raise ValueError('Explicit conditional circular observation branch required')
    if len(queries) not in (12,43) or len(pressure_step_m)!=len(queries):
        raise ValueError('Complete 12/43 ordered queries and stencil steps required')
    if any(set(q)!={'id','radius_kpc'} for q in queries) or len({q['id'] for q in queries})!=len(queries):
        raise ValueError('Only unique query IDs/radii accepted')
    if orientation not in (-1,1): raise ValueError('Signed streaming orientation required')
    for v in (kpc_m,pressure_atol_Pa_per_m,pressure_rtol):
        if not math.isfinite(v): raise ValueError('Finite units/tolerances required')
    if kpc_m<=0 or pressure_atol_Pa_per_m<0 or pressure_rtol<0:
        raise ValueError('Positive length unit and nonnegative derivative tolerances required')
    args=dict(coupled_arguments)
    result=coupled_module.solve(**args)
    if result.get('converged_finite_fixed_point') is not True:
        return {'predictions_available':False,'source_fixed_point':result,
                'reason':'Finite source closure did not converge; no velocity rows manufactured'}
    prepared=result['prepared_metric_response']
    fm=args['fourier_module']; mm=args['metric_module']; hm=args['hi_module']
    qm=args['quadrature_module']; fa=args['fourier_arguments']; c=args['c_m_s']
    boundary=args['boundary_jet_at_positions']
    # Last-line cache is scoped to this fixed prepared source only.
    line_key=None; line=None
    def metric(R,phi,z):
        nonlocal line_key,line
        pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
        if vertical_fourier_module is None:
            packet=fm.evaluate_prepared(prepared=prepared,physical_positions=pos,**boundary(pos))
        else:
            key=(float(pos[0,0]),float(pos[0,1]))
            if key!=line_key:
                line=vertical_fourier_module.prepare_line(prepared=prepared,x_m=key[0],y_m=key[1])
                line_key=key
            packet=vertical_fourier_module.evaluate_line(line=line,z_m=z,**boundary(pos))
        d=packet['fields'][0,:,0]; grad=packet['gradient'][0,:,0,:]
        for a in (d,grad):
            scale=float(np.linalg.norm(a.real)); im=float(np.linalg.norm(a.imag))
            tol=args['reality_atol']+args['reality_rtol']*scale
            if not all(math.isfinite(v) for v in (scale,im,tol)) or im>tol:
                raise ValueError('Nonreal or nonfinite physical query metric')
        return mm.evaluate_point(delta_fields=d.real,delta_gradient_physical=grad.real,
                                 Cbar=fa['Cbar'],mubar=fa['mubar'],R=R,phi=phi,z=z)
    columns={}
    def midplane(R,phi):
        key=(R,phi)
        if key in columns: return columns[key]
        profile=hi_profile_at_radius(R)
        def at_z(z):
            m=metric(R,phi,z)
            return {'N':m['N'],'metric_cyl':m['g_cylindrical'].tolist(),
                    'mode_weights':[[1.]+[0.]*9]}
        col=hm.solve_hi_column(metric_at_z=at_z,quadrature_module=qm,
            radius_m=R,radial_weight_m=1.,azimuth_weight_rad=1.,
            surface_ref_kg_m2=profile['Sigma_kg_m2'],c_m_s=c,**profile['hi_options'])
        # Unit widths only cancel in column normalization; these query columns
        # are never added to the source integral a second time.
        mids=[n for n in col['nodes'] if n['z_m']==0.]
        if len(mids)!=1: raise ValueError('Actual HI solution must contain one midplane node')
        columns[key]=(mids[0],col)
        return columns[key]
    # Each query has actual azimuths and normalized nonnegative estimator weights.
    # No uniform angular coverage, beam, or emissivity weights are invented.
    if len(azimuth_nodes)!=len(queries) or len(azimuth_step_rad)!=len(queries):
        raise ValueError('Azimuth nodes and positive derivative steps per query required')
    rows=[]; details=[]
    for q,step,angular,astep in zip(queries,pressure_step_m,azimuth_nodes,azimuth_step_rad):
        R=float(q['radius_kpc'])*kpc_m; step=float(step); astep=float(astep)
        if not all(math.isfinite(v) for v in (R,step,astep)) or not 0<step<R or not 0<astep<math.pi:
            raise ValueError('Finite positive radial/azimuth derivative steps required')
        if not angular: raise ValueError('Nonempty observed angular support required')
        phis=[float(a['phi_rad']) for a in angular]
        weights=[float(a['fit_weight']) for a in angular]
        if not all(math.isfinite(v) for v in phis+weights) or any(w<0 for w in weights):
            raise ValueError('Finite angles and nonnegative estimator weights required')
        if abs(math.fsum(weights)-1.)>1e-12:
            raise ValueError('Explicitly normalized estimator weights required; no silent renormalization')
        def local(phi):
            node,col=midplane(R,phi); derivatives=[]
            for dR in (step,step/2):
                left,_=midplane(R-dR,phi); right,_=midplane(R+dR,phi)
                derivatives.append((right['pressure_Pa']-left['pressure_Pa'])/(2*dR))
            dp=derivatives[1]; diff=abs(dp-derivatives[0])
            tol=pressure_atol_Pa_per_m+pressure_rtol*abs(dp)
            if not all(math.isfinite(v) for v in (*derivatives,diff,tol)) or diff>tol:
                raise ValueError('Pressure radial derivative unresolved at supplied scales')
            m=metric(R,phi,0.)
            v=streaming_module.pressure_streaming_speed(d_log_N=m['dlnN_dR'],
                d_log_R=m['dln_sqrt_gphiphi_dR'],d_pressure=dp,
                energy_density=node['epsilon_rest_J_m3'],pressure=node['pressure_Pa'],
                c=c,orientation=orientation)
            lor=1/math.sqrt(1-(v/c)**2)
            uphi=lor*v/m['azimuthal_tangent_norm']
            return dict(node=node,column=col,metric=m,v=v,uphi=uphi,
                        ui=uphi*m['g_cylindrical'][:,1],dp=dp,
                        radial_derivatives=derivatives,radial_difference=diff)
        pixels=[]; node_records=[]
        for phi in phis:
            center=local(phi); m=center['metric']; node=center['node']
            angular_gradients=[]; convective_gradients=[]
            flux_derivatives=[]; K_derivatives=[]; logK_derivatives=[]
            angular_stencil_columns=[]
            def volume_density(record):
                sign,logdet=np.linalg.slogdet(record['metric']['g_cylindrical'])
                if sign<=0 or not math.isfinite(float(logdet)):
                    raise ValueError('Invalid metric determinant in continuity diagnostic')
                jac=record['metric']['N']*math.exp(float(logdet)/2)
                if not math.isfinite(jac) or jac<=0:
                    raise ValueError('Nonfinite continuity spacetime volume density')
                return jac
            def flux(record):
                value=volume_density(record)*record['node']['rho_kg_m3']*record['uphi']
                if not math.isfinite(value): raise ValueError('Nonfinite mass flux')
                return value
            for da in (astep,astep/2):
                minus=local(phi-da); plus=local(phi+da)
                angular_gradients.append((plus['node']['pressure_Pa']-minus['node']['pressure_Pa'])/(2*da))
                convective_gradients.append((plus['ui']-minus['ui'])/(2*da))
                flux_derivatives.append((flux(plus)-flux(minus))/(2*da))
                angular_stencil_columns.append({'step_rad':da,'minus':minus,'plus':plus})
                if adiabatic_K_transport:
                    km=minus['column']['K_SI']; kp=plus['column']['K_SI']
                    if not all(math.isfinite(x) and x>0 for x in (km,kp)):
                        raise ValueError('Positive finite polytropic K required for adiabatic diagnostic')
                    K_derivatives.append((kp-km)/(2*da))
                    logK_derivatives.append((math.log(kp)-math.log(km))/(2*da))
            # At midplane of the actual N-only polytropic column, analytic
            # vertical preparation gives P_z/(epsilon+P)=-d_z ln N.
            ent=node['epsilon_rest_J_m3']+node['pressure_Pa']
            pg=np.array([center['dp']/ent,angular_gradients[-1]/ent,-m['dlnN_dz']])
            v=center['v']; qv=(v/c)**2
            dn=m['N_cylindrical_derivatives']/m['N']
            drr=.5*m['g_cylindrical_derivatives'][:,1,1]/m['g_cylindrical'][1,1]
            # Stationary circular trial u^phi=gamma*v/sqrt(gphiphi), u^R=u^z=0.
            # Keep convective phi derivatives and all g_i,phi cross components.
            accel=(dn-qv*drr)/(1-qv)+center['uphi']/c**2*convective_gradients[-1]
            euler=accel+pg+center['ui']*center['uphi']/c**2*pg[1]
            if not np.all(np.isfinite(euler)) or not all(math.isfinite(x) for x in angular_gradients):
                raise ValueError('Nonfinite anisotropic Euler diagnostic')
            jac=volume_density(center)
            continuity=[d/jac for d in flux_derivatives]
            rho=node['rho_kg_m3']
            rates=[d/rho for d in continuity]
            if not all(math.isfinite(x) for x in flux_derivatives+continuity+rates):
                raise ValueError('Nonfinite mass continuity residual')
            adiabatic=None
            if adiabatic_K_transport:
                transports=[center['uphi']*d for d in K_derivatives]
                log_transports=[center['uphi']*d for d in logK_derivatives]
                if not all(math.isfinite(x) for x in transports+log_transports):
                    raise ValueError('Nonfinite adiabatic transport residual')
                adiabatic={'u_dot_grad_K_SI_per_s':transports,
                    'u_dot_grad_logK_per_s':log_transports,
                    'log_rate_stencil_difference_per_s':log_transports[1]-log_transports[0],
                    'scope':'Conditional adiabatic polytrope; no imposed heating/entropy law'}
            los=observation_module.project_streaming(v_phi=v/1000.,v_radial=0.,v_vertical=0.,
                azimuth=phi,inclination=physical_inclination)
            pixels.append({'velocity':los})
            node_records.append({**center,'phi_rad':phi,'los_km_s':los,
                'pressure_phi_derivatives_Pa_per_rad':angular_gradients,
                'pressure_phi_stencil_difference':abs(angular_gradients[1]-angular_gradients[0]),
                'ui_phi_stencil_difference':convective_gradients[1]-convective_gradients[0],
                'Euler_covector_residual_R_phi_z':euler,
                'angular_stencil_columns':angular_stencil_columns,
                'mass_continuity':{
                    'coordinate_flux_N_sqrtg_rho_uphi':flux(center),
                    'coordinate_flux_phi_derivatives':flux_derivatives,
                    'divergence_kg_m3_per_s':continuity,
                    'fractional_density_rate_per_s':rates,
                    'divergence_stencil_difference_kg_m3_per_s':continuity[1]-continuity[0],
                    'scope':'Stationary circular trial, midplane: partial_phi(N sqrtg rho u_phi)/(N sqrtg); u_phi here denotes contravariant u^phi'},
                'adiabatic_K_transport':adiabatic,
                'Euler_units':'R,z inverse metres; phi per radian; normalized by enthalpy/c^2 as appropriate'})
        speed=observation_module.ring_harmonic(pixels=pixels,indices=list(range(len(pixels))),
            azimuths=phis,fit_weights=weights,released_inclination=released_inclination,
            systemic_velocity=0.)
        if not math.isfinite(speed): raise ValueError('Nonfinite observed harmonic')
        rows.append({'id':q['id'],'speed_km_s':speed})
        details.append({'id':q['id'],'radius_m':R,'nodes':node_records,
                        'normalized_estimator_weights':weights})
    return {'rows':rows,'units':'km/s','semantics':'TOTAL_OBSERVABLE',
        'predictions_available':True,  # calculable trial rows only, not admitted predictions
        'predictions_available_semantics':'CALCULABLE_TRIAL_ONLY',
        'dynamics_status':'UNASSESSED_CIRCULAR_TRIAL',
        'accepted_for_calibration':False,'source_fixed_point':result,
        'query_physics':details,'radial_azimuth_query_columns':columns,
        'circular_reference_assumption':circular_reference_assumption,
        'observation_approximation':'Supplied angular fixed-plane harmonic weights; thin no-beam projection; no azimuthal averaging of metric or speeds',
        'inclination_applied_once':True,
        'scope':'Circular-streaming trial, not stationary anisotropic Euler solution. All nonradial residuals retained without acceptance threshold; N-only vertical preparation and finite stencil/source residuals do not certify continuum or metric error.'}
