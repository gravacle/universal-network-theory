"""Inert frozen-field, saved-root homotopy base at one actual saved radius.
No root search, field inversion, source equilibration or chosen mesh. Caller gives
strict interior eta nodes and positive quadrature weights; normalization uses this mesh. Full n_phi-angle fields retained; m=0 is reference only.
Action binding must compute projected r0 with its SAME derivative operators:
r0_R=D_R(P)/rho+Phi0_R-R*Omega**2; r0_z=D_z(P)/rho+Phi0_z.
These residuals must not be silently set to zero. Surface/boundary rows separate.
"""
# GAL_C2V001 (Claude2 ngc_route_construction_c2/stages2): successor of reviewed
# owned_saved_root_body_base_v003.py (sha c525ec711b7ebd1fc776299669fe9c2ed3e369a55f562f350a9e05ef6c5a0675).
# Only the 16-angle literal changed: the angular count is the required keyword n_phi (no default),
# passed by the caller from galaxy-config mesh.n_phi; the saved-record angle check uses it.
# With n_phi=16 every expression is the old one. sigma0 11000 m/s and gamma 5/3 kept (V001 sec. 5).
import hashlib
import math
from pathlib import Path
import numpy as np


def evaluate_saved_radius(*, reference_record, prepared, prepared_custody,
        eta_nodes, eta_weights, new_surface_kg_m2, c_m_s, Cbar, mubar,
        line_module, metric_module, boundary_jet_at_positions,
        accepted_module_pins, reality_atol, reality_rtol, n_phi):
    if not prepared_custody or reference_record['prepared_custody']!=prepared_custody:
        raise ValueError('Actual saved field custody mismatch')
    if type(n_phi) is not int or n_phi<1:raise ValueError('Explicit positive integer angular count n_phi required')
    for module in (line_module,metric_module):
        path=str(Path(module.__file__).resolve())
        if accepted_module_pins.get(path)!=hashlib.sha256(Path(path).read_bytes()).hexdigest():raise ValueError('Module pin mismatch')
    eta=np.asarray(eta_nodes,dtype=float)
    if eta.ndim!=1 or not len(eta) or not np.isfinite(eta).all() or np.any(np.abs(eta)>=1) or len(set(eta.tolist()))!=len(eta):raise ValueError('Distinct strict interior eta nodes required; surface rows separate')
    weights=np.asarray(eta_weights,dtype=float)
    if weights.shape!=eta.shape or not np.isfinite(weights).all() or np.any(weights<=0):raise ValueError('Positive finite eta quadrature weights matching nodes required')
    R=float(reference_record['R_m']);cols={float(k):v for k,v in reference_record['reference_columns'].items()};ref=cols[R];col=ref['column']
    c=float(c_m_s);sigma=11000.;gamma=5/3;h0=gamma/(gamma-1)*sigma*sigma
    sn=float(new_surface_kg_m2);so=float(ref['Sigma_kg_m2']);A=float(col['rho0_kg_m3'])*sn/so
    controls=[R,c,sn,so,A,reality_atol,reality_rtol]
    if not all(math.isfinite(v) for v in controls) or min(R,c,sn,so,A)<=0 or min(reality_atol,reality_rtol)<0:raise ValueError('Invalid finite physical inputs')
    roots=list(map(float,col['roots_m']))
    if not roots[0]<0<roots[1]:raise ValueError('Saved two-sided roots required')
    phis=reference_record['angular_nodes_rad']
    if phis!=[2*math.pi*i/n_phi for i in range(n_phi)]:raise ValueError('Saved%dangle convention required'%n_phi)
    if np.asarray(prepared['weighted_responses']).shape[2]!=1:raise ValueError('One actual source family required')
    lines=[line_module.prepare_line(prepared=prepared,x_m=R*math.cos(p),y_m=R*math.sin(p)) for p in phis]
    def angular(z):
        logs=[];grad=[];fields=[];metrics=[]
        for phi,line in zip(phis,lines):
            pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
            packet=line_module.evaluate_line(line=line,z_m=z,**boundary_jet_at_positions(pos))
            f=np.asarray(packet['fields'])[0,:,0];g=np.asarray(packet['gradient'])[0,:,0,:]
            for v in (f,g):
                bound=reality_atol+reality_rtol*float(np.linalg.norm(v.real))
                if not np.isfinite(v).all() or not math.isfinite(bound) or float(np.linalg.norm(v.imag))>bound:raise ValueError('Full-complex field reality failure')
            if 1+float(f[0].real)<=0:raise ValueError('Nonpositive lapse')
            met=metric_module.evaluate_point(delta_fields=f.real,delta_gradient_physical=g.real,Cbar=Cbar,mubar=mubar,R=R,phi=phi,z=z)
            logs.append(math.log1p(float(f[0].real)));grad.append([met['dlnN_dR'],met['dlnN_dphi'],met['dlnN_dz']]);fields.append(f);metrics.append(met)
        return np.asarray(logs),np.asarray(grad),np.asarray(fields),metrics
    logs0,grad0,_,_=angular(0.);mean0=math.fsum(logs0)/n_phi;PhiR0=c*c*math.fsum(grad0[:,0])/n_phi
    if not PhiR0>0:raise ValueError('Nonpositive pressure-free midplane circulation reference; no clipping')
    Omega=math.sqrt(PhiR0/R);K=sigma*sigma*A**(1-gamma);rows=[]
    for e in eta:
        z=(roots[0]+roots[1])/2+(roots[1]-roots[0])*float(e)/2
        logs,grad,fields,metrics=angular(z);mean=math.fsum(logs)/n_phi
        # Same saved logN0 reference as the original column; expose reproduction
        # difference rather than silently renormalize an existing saved shape.
        u=1-c*c*(mean-float(col['logN0']))/h0
        if not u>0:raise ValueError('Actual interior enthalpy crossing; no clipping')
        rho=A*u**(1/(gamma-1));P=sigma*sigma*A*u**(gamma/(gamma-1))
        rows.append({'eta':float(e),'z_m':z,'shape':u**(1/(gamma-1)),'rho0_kg_m3':rho,'P0_Pa':P,'K0_SI':K,'Omega_per_s':Omega,
          'Phi0_m2_s2':c*c*mean,'Phi0_R_m_s2':c*c*math.fsum(grad[:,0])/n_phi,'Phi0_z_m_s2':c*c*math.fsum(grad[:,2])/n_phi,
          'angular_forcing_dPhi_m2_s2':(c*c*(logs-mean)).tolist(),'actual_metrics':metrics,
          'full_fields_real':fields.real.tolist(),'full_fields_imag':fields.imag.tolist()})
    # Normalize on the adopted body quadrature, preserving the observed column
    # mass exactly up to reported arithmetic. No change to field/root/shape.
    half_height=(roots[1]-roots[0])/2
    shape_integral=half_height*math.fsum(float(w)*row['shape'] for w,row in zip(weights,rows))
    if not math.isfinite(shape_integral) or shape_integral<=0:raise ValueError('Invalid body quadrature shape integral')
    old_A=A;A=sn/shape_integral;factor=A/old_A;K=sigma*sigma*A**(1-gamma)
    if not all(math.isfinite(v) and v>0 for v in (A,factor,K)):raise ValueError('Invalid quadrature-normalized amplitude')
    for row in rows:
        row['rho0_kg_m3']=A*row['shape']
        row['P0_Pa']=sigma*sigma*A*row['shape']**gamma
        row['K0_SI']=K
    recovered_column=half_height*math.fsum(float(w)*row['rho0_kg_m3'] for w,row in zip(weights,rows))
    result={'R_m':R,'phi_rad':phis,'roots_m':roots,'root_brackets_m':col['root_brackets_m'],
      'body_map':'z=(zminus+zplus)/2+(zplus-zminus)*eta/2; smooth affine map; z0 evaluated separately', 'eta_nodes':eta.tolist(),'eta_weights':weights.tolist(),'rows':rows,'new_Sigma_kg_m2':sn,'old_Sigma_kg_m2':so,'rho_amplitude_kg_m3':A,
      'quadrature_normalization':{'half_height_m':half_height,'eta_weight_sum':math.fsum(weights),'shape_integral_m':shape_integral,'old_scaled_saved_amplitude_kg_m3':old_A,'new_to_old_amplitude_ratio':factor,'old_amplitude_new_quadrature_column_kg_m2':old_A*shape_integral,'recovered_column_kg_m2':recovered_column,'column_mass_residual_kg_m2':recovered_column-sn},
      'saved_logN0':col['logN0'],'recomputed_logN0_difference':mean0-col['logN0'],'Phi0_R_midplane_m_s2':PhiR0,
      'Omega_reference_per_s':Omega,'sigma_m_s':sigma,'Gamma':gamma,'prepared_custody':prepared_custody,
      'dynamics_status':'UNEQUILIBRATED_POSITIVE_CIRCULATION_REFERENCE','accepted_for_calibration':False,
      'projected_r0_rule':'Use SAME action derivative matrices on returned P0, with returned Phi0_R/Phi0_z; retain radial and vertical residuals.',
      'scope':'Fixed old field and saved roots; new-source amplitude normalized on supplied eta quadrature, with old amplitude ratio reported. Angular forcing retained. No new source gravity, no stationary correction, no completed boundary realization. Strict interior only; root locations/resolution inherited.'}
    def finite(v):
        if isinstance(v,(float,np.floating)) and not math.isfinite(v):raise ValueError('Nonfinite derived base')
        if isinstance(v,dict):
            for x in v.values():finite(x)
        elif isinstance(v,(list,tuple,np.ndarray)):
            for x in v:finite(x)
    finite(result)
    return result
