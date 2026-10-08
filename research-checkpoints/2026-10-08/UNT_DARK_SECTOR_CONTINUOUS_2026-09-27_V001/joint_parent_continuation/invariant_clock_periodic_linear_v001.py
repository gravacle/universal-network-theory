"""Homogeneous tangent of the EXACT canonical action, not truncated evolution.

Used only as a modal implicit-stage preconditioner. The stage residual uses
the entire nonlinear parent RHS. No fast mode, harmonic, charge or field is
removed. Phase and vector factors include their complex spatial derivative.
"""
import numpy as np

def scales(run):
    k=run.k
    return np.array([1.,1/k**2,1/k,run.m.Q0/k**2,1/k**2,1.,1/k,run.pi_phi_bar])

def matrices(run,x):
    g=run.background(x);a=g['abar'];V=a**3;H=g['H'];m=g['mbar'];Q=g['Qbar'];d=g['dbar']
    k=run.k*np.arange(run.n//2+1);ik=1j*k[:,None]
    scale=scales(run);basis=np.diag(scale).astype(complex)
    fa,fb,u,phase,pa,pb,pu,pc=[basis[i][None,:] for i in range(8)]
    fv=fa+2*fb;paV=pa/V+4*run.F*H*fv;pbV=pb/V+8*run.F*H*fv
    dc=run.cT/run.F*((paV+pbV)/4-ik*u/a**2)
    bd=-paV/4+dc/2;ad=(paV-pbV)/4+dc/2
    dm=pc/(2*V)-m*fv;qd=np.broadcast_to(dm/d,(len(k),8))
    p=(Q*u+ik*phase)/a;e=(pu/(2*a*a)-g['chi_bar']*u/a-run.C*p)/run.KB
    ud=a*e;D=run.C*(e-p)
    core=-4*H*ad-8*H*bd+2*m*qd+6*H*dc+g['core_bar']*fv
    pad=V*core-2*a*g['chi_bar']*ik*u
    pbd=2*V*core-4*a*g['chi_bar']*ik*u+4*a*k[:,None]**2*fb
    pud=2*a*a*Q*D+2*a*g['chi_bar']*(H*u+ud)-2*a*ik*dc
    pcd=-2*a*a*ik*(D-(m/Q)*ik*phase/a)
    return np.stack([ad,bd,ud,qd,pad,pbd,pud,pcd],axis=1)/scale[None,:,None]/H
