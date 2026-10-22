"""Independent cylinder-minus-cube tail integral. No import of the tail module.
Direct angular GL (no harmonic expansion), quadratic corner mapping, blocked kz quadrature.
Caller supplies the same declared physical source through its factor interface; independence is of tail integration,
not of the supplied source profile. SI units. Returns actual tail values at arbitrary (R,phi,z) points.
"""
import math
import numpy as np
KPC=3.085677581491367e19

def panel(a,b,width,order):
    n=max(1,math.ceil((b-a)/width));x,w=np.polynomial.legendre.leggauss(order)
    e=np.linspace(a,b,n+1)
    return ((e[:-1,None]+e[1:,None])/2+(e[1:,None]-e[:-1,None])*x/2).ravel(),np.broadcast_to((e[1:,None]-e[:-1,None])*w/2,(n,order)).ravel()

def integral(roster,j0,gamma,c,points,K=2.,big=16.,width_p=.005,width_z=.007,order=8):
    # Disjoint domains: high z all radial, low z full outside sqrt(2)K, low z cube corner arcs.
    result=np.zeros(len(points));root=math.sqrt(2)*K
    for part in ('high','outer','corner'):
        if part=='high':kp,wp=panel(0,big,width_p,order);zlo=K
        elif part=='outer':kp,wp=panel(root,big,width_p,order);zlo=0.
        else:
            u,wu=panel(0,1,width_p/(2*(root-K)),order)
            kp=K+(root-K)*u*u;wp=wu*2*(root-K)*u;zlo=0.
        kz,wz=panel(zlo,big if part=='high' else K,width_z,order)
        P=roster.radial_factors(kp/KPC,j0);F=roster.vertical_factors(kz/KPC,c)
        gx,gw=np.polynomial.legendre.leggauss(32)
        for lo in range(0,len(kp),32):
            k=kp[lo:lo+32];S=P[lo:lo+32]@F.T
            fac=(wp[lo:lo+32]*k)[:,None]*wz[None,:]/(k[:,None]**2+kz[None,:]**2)/KPC
            for i,(R,phi,z) in enumerate(points):
                Rk=R/KPC
                if part=='corner':
                    alpha=np.arccos(K/k)
                    psi=alpha[:,None]*gx[None,:]
                    angular=np.zeros(len(k))
                    for axis in (0.,math.pi/2,math.pi,3*math.pi/2):
                        angular+=alpha*np.sum(gw[None,:]*np.cos(k[:,None]*Rk*np.cos(psi+axis-phi)),axis=1)
                else:
                    # Own direct angular quadrature, phase-limited; no Bessel angular provider.
                    psi,wpsi=panel(0,2*math.pi,min(math.pi/8,1.5/max(1.,big*Rk)),16)
                    angular=np.cos(k[:,None]*Rk*np.cos(psi[None,:]-phi))@wpsi
                E=np.exp(1j*kz*z/KPC)
                result[i]+=2*np.sum(angular[:,None]*fac*(S*E[None,:]).real)
    return result/(4*gamma*(2*math.pi)**3)
