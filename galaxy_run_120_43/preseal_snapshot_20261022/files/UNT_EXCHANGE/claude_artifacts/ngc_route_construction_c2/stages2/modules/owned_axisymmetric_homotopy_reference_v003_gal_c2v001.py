"""Inert n_phi-angle reference columns and actual anisotropic base residuals.
Reference only, not isotropization of the final constitutive kernel or equilibrated source.
"""
# GAL_C2V001 (Claude2 ngc_route_construction_c2/stages2): successor of reviewed
# owned_axisymmetric_homotopy_reference_v003.py (sha 81a04b1241c1004f8766f68d22f9c586824ae3b3cbe32ca36243a2d3da387128).
# Only the 16-angle literal changed: the angular count is the required keyword n_phi (no default),
# passed by the caller from galaxy-config mesh.n_phi. With n_phi=16 every expression is the old one.
# sigma0 11000 m/s and gamma 5/3 are kept (schema V001 sec. 5 KEEP_LITERAL). No other change.
import math
import hashlib
from pathlib import Path
import numpy as np


def evaluate_radius(*,prepared,R_m,radial_step_m,z_positions_m,radial_domain_m,
        profile_at_radius,hi_options,c_m_s,Cbar,mubar,boundary_jet_at_positions,
        line_module,metric_module,column_module,quadrature_module,reality_atol,reality_rtol,
        prepared_custody,source_roster_custody,accepted_module_pins,n_phi):
    """Caller supplies existing run numerical controls and exact prepared source.
    profile_at_radius(R) supplies Sigma_kg_m2 from existing independent source.
    hi_options: existing search_step_m,search_limit_m,root_tolerance_m,
    log_lapse_tolerance,max_metric_calls,panels_per_side. No new defaults.
    Numerical radial d,d/2 comparison; explicit z or center_common_interior selects actual center nodes strictly inside all five references plus0, records omissions.
    Negative Omega² is reported, never sqrt-clipped or assigned a motion state.
    """
    if not prepared_custody or not source_roster_custody:raise ValueError("Actual prepared packet and full-domain source roster custody required")
    if type(n_phi) is not int or n_phi<1:raise ValueError('Explicit positive integer angular count n_phi required')
    pins={}
    for module in (line_module,metric_module,column_module,quadrature_module):
        path=str(Path(module.__file__).resolve());pin=hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if accepted_module_pins.get(path)!=pin:raise ValueError("Module pin mismatch: "+path)
        pins[path]=pin
    if np.asarray(prepared["weighted_responses"]).shape[2]!=1:raise ValueError("One actual combined source family required")
    R=float(R_m);d=float(radial_step_m);c=float(c_m_s)
    lo,hi=map(float,radial_domain_m)
    if not all(math.isfinite(x) for x in (R,d,c,lo,hi,reality_atol,reality_rtol)) or not 0<d<R or c<=0 or not lo<=R-d<R+d<=hi or reality_atol<0 or reality_rtol<0:raise ValueError('Explicit interior radial stencil/domain and finite controls required')
    phis=[2*math.pi*i/n_phi for i in range(n_phi)];sigma=11000.;gamma=5/3;h0=gamma/(gamma-1)*sigma*sigma
    def finite(x):
        x=np.asarray(x,float)
        if not np.isfinite(x).all():raise ValueError('Nonfinite reference quantity')
        return x
    refs={}
    for r in (R,R-d,R+d,R-d/2,R+d/2):
        lines=[line_module.prepare_line(prepared=prepared,x_m=r*math.cos(phi),y_m=r*math.sin(phi)) for phi in phis]
        cache={}
        def angular(z,*,r=r,lines=lines,cache=cache):
            if z in cache:return cache[z]
            logs=[];grads=[];actual=[]
            for phi,line in zip(phis,lines):
                pos=np.array([[r*math.cos(phi),r*math.sin(phi),z]])
                pk=line_module.evaluate_line(line=line,z_m=z,**boundary_jet_at_positions(pos))
                f=np.asarray(pk['fields'])[0,:,0];g=np.asarray(pk['gradient'])[0,:,0,:]
                for v in (f,g):
                    if not np.isfinite(v).all() or float(np.linalg.norm(v.imag))>reality_atol+reality_rtol*float(np.linalg.norm(v.real)):raise ValueError('Full-complex reality check failed')
                N=1+float(f[0].real)
                if N<=0:raise ValueError('Nonpositive actual lapse')
                met=metric_module.evaluate_point(delta_fields=f.real,delta_gradient_physical=g.real,
                    Cbar=Cbar,mubar=mubar,R=r,phi=phi,z=z)
                logs.append(math.log1p(float(f[0].real)))
                grads.append([met['dlnN_dR'],met['dlnN_dphi'],met['dlnN_dz']]);actual.append(met)
            ans={'logN':math.fsum(logs)/n_phi,'grad_logN':np.sum(np.asarray(grads),axis=0)/n_phi,'actual':actual}
            cache[z]=ans;return ans
        def at_z(z,*,angular=angular,r=r):
            v=angular(z)
            return {'N':math.exp(v['logN']),'logN':v['logN'],'metric_cyl':[[1.,0.,0.],[0.,r*r,0.],[0.,0.,1.]],'mode_weights':[[1.]+[0.]*9]}
        prof=profile_at_radius(r)
        col=column_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
            radius_m=r,radial_weight_m=1.,azimuth_weight_rad=1.,surface_ref_kg_m2=prof['Sigma_kg_m2'],
            sigma0_m_s=sigma,gamma=gamma,c_m_s=c,**hi_options)
        refs[r]={'column':col,'angular':angular,'Sigma_kg_m2':prof['Sigma_kg_m2']}
    def state(r,z):
        ref=refs[r];col=ref['column']
        if not col['roots_m'][0]<z<col['roots_m'][1]:raise ValueError('Requested point outside common positive interior; no boundary extrapolation')
        av=ref['angular'](z);u=1-c*c*(av['logN']-col['logN0'])/h0
        if u<=0:raise ValueError('Interior enthalpy crossing')
        rho=col['rho0_kg_m3']*u**(1/(gamma-1));P=col['K_SI']*rho**gamma
        return rho,P,av
    height_selection={'mode':'explicit_positions','excluded_center_nodes':[]}
    if isinstance(z_positions_m,str):
        if z_positions_m!='center_common_interior':raise ValueError('Unknown height-selection mode')
        left=max(v['column']['roots_m'][0] for v in refs.values())
        right=min(v['column']['roots_m'][1] for v in refs.values())
        if not left<0.<right:raise ValueError('No common positive interval containing midplane')
        selected=[];excluded=[]
        for i,node in enumerate(refs[R]['column']['nodes']):
            z=float(node['z_m'])
            if not left<z<right:
                excluded.append({'center_node_index':i,'z_m':z,'reason':'outside strict common root interval'})
                continue
            # A hidden sampled crossing is a failure, not a silently omitted point.
            for r in refs: state(r,z)
            selected.append(z)
        for r in refs: state(r,0.)
        if 0. not in selected:selected.append(0.)
        selected=sorted(set(selected))
        height_selection={'mode':'center_common_interior','common_root_bounds_m':[left,right],
            'selected_z_m':selected,'excluded_center_nodes':excluded,
            'scope':'Only actual center quadrature nodes in strict common interior plus midplane; near-surface omissions explicit. Positive enthalpy checked in all five references; hidden sampled crossings fail.'}
        z_positions_m=selected
    output=[]
    for z in z_positions_m:
        z=float(z)
        if not math.isfinite(z):raise ValueError('Finite supplied height required')
        rho,P,av=state(R,z);prs=[]
        for step in (d,d/2):prs.append((state(R+step,z)[1]-state(R-step,z)[1])/(2*step))
        PhiR=c*c*av['grad_logN'][0];PhiZ=c*c*av['grad_logN'][2]
        omega2=(PhiR+prs[1]/rho)/R
        rec={'z_m':z,'rho_kg_m3':rho,'P_Pa':P,'K_SI':refs[R]['column']['K_SI'],
             'Phi0_m2_s2':c*c*av['logN'],'Phi0_R_m_s2':PhiR,'Phi0_z_m_s2':PhiZ,
             'P_R_stencils_Pa_per_m':prs,'P_R_halving_difference':prs[1]-prs[0],
             'P_z_Pa_per_m':-rho*PhiZ,'Omega_squared_per_s2':omega2,'actual_metric_residuals':[]}
        if omega2<0:
            rec['status']='NEGATIVE_OMEGA_SQUARED_NO_CIRCULAR_REFERENCE';output.append(rec);continue
        Omega=math.sqrt(omega2);ent=rho*c*c+P/(gamma-1)+P
        for phi,met in zip(phis,av['actual']):
            N=float(met['N']);G=finite(met['g_cylindrical']);dG=finite(met['g_cylindrical_derivatives']);dn=finite(met['N_cylindrical_derivatives'])/N
            norm=N*N-G[1,1]*Omega*Omega/(c*c)
            if norm<=0:raise ValueError('Reference coordinate rotation is not timelike in actual metric')
            ut=1/math.sqrt(norm);up=Omega*ut;ui=G[:,1]*up
            dup=up*(-N*N*dn[1]+.5*dG[1,1,1]*Omega*Omega/(c*c))/norm
            dui=dG[1,:,1]*up+G[:,1]*dup
            accel=up*dui/(c*c)+N*N*ut*ut*dn-.5*up*up*dG[:,1,1]/(c*c)
            pg=np.array([prs[1],0.,-rho*PhiZ])/ent
            residual=finite(accel+pg) # u^i partial_i P=0 for axisymmetric reference
            divergence_rate=up*(dn[1]+.5*np.trace(np.linalg.solve(G,dG[1])))+dup
            rec['actual_metric_residuals'].append({'phi_rad':phi,'Euler_covector_R_phi_z':residual.tolist(),
                'continuity_fractional_rate_per_proper_s':float(divergence_rate),'entropy_advection':0.,
                'u_phi_contravariant_per_s':up,'spatial_metric_perturbation':(finite(met['g_cartesian'])-np.eye(3)).tolist(),
                'pressure_over_rho_c2':P/(rho*c*c),'coordinate_rotation_speed_ratio_squared':G[1,1]*Omega*Omega/(N*N*c*c)})
        rec['status']='REFERENCE_WITH_ACTUAL_ANISOTROPIC_RESIDUALS';output.append(rec)
    return {'prepared_custody':prepared_custody,'source_roster_custody':source_roster_custody,'actual_module_pins':pins,'R_m':R,'radial_step_m':d,'radial_domain_m':[lo,hi],'angular_nodes_rad':phis,
        'reference_columns':{str(r):{'Sigma_kg_m2':v['Sigma_kg_m2'],'column':v['column']} for r,v in refs.items()},
        'positions':output,'height_selection':height_selection,'scope':'%d-angle homotopy reference only. Sigma normalized in background Cartesian volume; no external pressure. Source is the actual old prepared field, not the field generated by this new base gas. No completed equilibrium, forcing feedback, entropy/circulation selection or corrected forward rows claimed. Angular/radial/quadrature errors require separate refinement. Negative Omega² retained. Exact selected anisotropic equations evaluated on this reference; weak-field construction retained explicitly.'%n_phi}
