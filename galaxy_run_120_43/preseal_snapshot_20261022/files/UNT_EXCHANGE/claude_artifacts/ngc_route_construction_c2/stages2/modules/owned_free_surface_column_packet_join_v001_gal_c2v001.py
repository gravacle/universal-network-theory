"""Inert exact join of complete fixed-K free-surface column measures.
No source inversion, density rescaling, derivative interpolation or flow acceptance.
The returned quadrature has two panels through z=0, not a single affine GL mesh.
"""
# GAL_C2V001 (Claude2 ngc_route_construction_c2/stages2): successor of reviewed
# owned_free_surface_column_packet_join_v001.py (sha c3d4e08bf108d4fff908d8c34af9c20b7f50d38d678a6d7f999df71c78c7d62b).
# Only the 72-column and 16-angle literals changed: n_columns is a new required keyword (no default) and the
# declared n_phi is used instead of requiring 16; the caller passes radial.n_columns / mesh.n_phi from the
# galaxy config. The completeness guard stays: exactly n_columns columns and radial arrays of shape (n_columns,).
# With n_columns=72, n_phi=16 every expression is the old one. Sigma<=0 is still refused (schema S1).
import numpy as np

def join(*, columns, radial_nodes_m, radial_RdR_weights_m2, expected_Sigma,
         expected_K, gamma, c_m_s, n_phi, mass_relative_tolerance, n_columns):
    R=np.asarray(radial_nodes_m,float);wr=np.asarray(radial_RdR_weights_m2,float)
    sig=np.asarray(expected_Sigma,float);K=np.asarray(expected_K,float)
    if type(n_columns) is not int or n_columns<1:raise ValueError('Declared positive integer column count n_columns required')
    if R.shape!=(n_columns,) or wr.shape!=R.shape or sig.shape!=R.shape or K.shape!=R.shape or len(columns)!=n_columns:
        raise ValueError('Complete actual%d radial columns required, no partial splice'%n_columns)
    if any(not np.isfinite(v).all() for v in (R,wr,sig,K)) or any(np.any(v<=0) for v in (R,wr,sig,K)) or np.any(np.diff(R)<=0):raise ValueError('Positive ordered finite inputs')
    if type(n_phi) is not int or n_phi<1 or not np.isfinite(c_m_s) or c_m_s<=0 or not np.isfinite(gamma) or gamma<=1 or not np.isfinite(mass_relative_tolerance) or mass_relative_tolerance<0:raise ValueError('Declared branch and controls required')
    nz=len(columns[0]['z_m']);zs=[];ws=[];rs=[];ps=[];hs=[];roots=[];res=[]
    for i,col in enumerate(columns):
        if col['status']!='FIXED_LAGGED_POTENTIAL_COLUMN_ONLY' or col['radial_index']!=i or col['R_m']!=R[i] or col['K_SI']!=K[i] or col['Sigma_kg_m2']!=sig[i] or col['gamma']!=gamma:raise ValueError('Column identity/thermodynamics mismatch')
        z=np.asarray(col['z_m'],float);w=np.asarray(col['weights_m'],float);rho=np.asarray(col['rho_kg_m3'],float);P=np.asarray(col['pressure_Pa'],float);h=np.asarray(col['enthalpy_m2_s2'],float);ends=np.asarray(col['roots_m'],float)
        if any(v.shape!=(nz,) or not np.isfinite(v).all() for v in (z,w,rho,P,h)) or ends.shape!=(2,) or not np.isfinite(ends).all():raise ValueError('Finite equal-order actual quadratures required')
        if nz%2 or not ends[0]<0<ends[1] or np.any(np.diff(z)<=0) or not ends[0]<z[0]<0<z[-1]<ends[1] or np.any(w<=0) or np.any(rho<=0) or np.any(P<=0) or np.any(h<=0):raise ValueError('Positive connected interior source required')
        mass=float(np.sum(w*rho));r=(mass-sig[i])/sig[i]
        if not np.isfinite(r) or abs(r)>mass_relative_tolerance:raise ValueError('Unrenormalized actual column mass fails')
        zs.append(z);ws.append(w);rs.append(rho);ps.append(P);hs.append(h);roots.append(ends);res.append(r)
    z=np.asarray(zs);w=np.asarray(ws);rho=np.asarray(rs);P=np.asarray(ps);h=np.asarray(hs);ends=np.asarray(roots)
    # Same actual solved positions and weights; neither remap nor renormalize.
    shape=(n_columns,n_phi,nz);phi=2*np.pi*np.arange(n_phi)/n_phi
    rr=np.broadcast_to(R[:,None,None],shape);pp=np.broadcast_to(phi[None,:,None],shape);zz=np.broadcast_to(z[:,None,:],shape)
    volume=np.broadcast_to(wr[:,None,None]*(2*np.pi/n_phi)*w[:,None,:],shape).copy()
    density=np.broadcast_to(rho[:,None,:],shape).copy()
    J=np.zeros(shape+(10,1));J[...,0,0]=-c_m_s**2*density*volume
    result=dict(R=rr.copy(),phi=pp.copy(),z=zz.copy(),physical_positions_m=np.stack((rr*np.cos(pp),rr*np.sin(pp),zz),axis=-1),volume_weights_m3=volume,
        rho0=density,P0=np.broadcast_to(P[:,None,:],shape).copy(),K0=np.broadcast_to(K[:,None,None],shape).copy(),enthalpy=np.broadcast_to(h[:,None,:],shape).copy(),roots_m=ends,
        radial_nodes_m=R.copy(),radial_RdR_weights_m2=wr.copy(),Sigma_kg_m2=sig.copy(),column_mass_relative_residual=np.asarray(res),integrated_source_J=J)
    if any(not np.isfinite(v).all() for v in result.values()):raise ValueError('Nonfinite joined output')
    return dict(arrays=result,scope='Complete solved column source measure only; potential at these positions must be evaluated from prepared waves, no sample interpolation',
        feedback_contract='new total field=G4+unit_response*(Fourier(new gas measure)-actual G4 gas Fourier). Fixed stars identical. If using old base total field, subtract actual old base gas instead; never both offsets.',
        motion_contract='Rebuild derivative operators on actual two-panel geometry. Compute Omega_squared=(D_R Phi0+D_R P/rho)/R without clipping, then D_R Omega,D_z Omega and full r0 with the same operators. Current72x8 weak modal code cannot consume these arrays unchanged.',
        status='SOURCE_PACKET_NOT_MOTION_SOLUTION')
