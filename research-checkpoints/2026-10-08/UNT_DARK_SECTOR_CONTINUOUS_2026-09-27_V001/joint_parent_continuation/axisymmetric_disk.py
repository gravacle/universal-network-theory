"""Nonuniform cylindrical finite-volume disk operator, reusing frozen flux law."""
import math
import numpy as np
import disk_solver as law


def mesh(n, extent, scale=1.):
    edges = scale*np.expm1(np.linspace(0., math.log1p(extent/scale), n+1))
    centres = (edges[:-1]+edges[1:])/2
    return edges, centres, np.diff(edges)


def spherical_potential(s, mass, order=64, newtonian=False):
    """Phi(s)-Phi(1); log-radius integration is well-conditioned at large s."""
    if newtonian:
        return mass*(1-1/np.asarray(s))
    nodes, weights = np.polynomial.legendre.leggauss(order)
    upper = np.log(np.asarray(s))
    t = upper[..., None]*(nodes+1)/2
    return upper/2*np.sum(np.exp(t)*law.inverse(mass*np.exp(-2*t))*weights,axis=-1)


def operator(phi, geometry, boundary, newtonian=False):
    edges, c, width = geometry
    pr, pz, tr, tz, bottom = boundary
    n = len(c)
    gr, gz = np.gradient(phi, c, c, edge_order=2)
    radial_mu = np.ones((n+1,n))
    vertical_mu = np.ones((n,n+1))
    clipped = 0

    def mu(normal, transverse):
        nonlocal clipped
        norm = np.hypot(normal, transverse)
        if newtonian:
            return np.ones_like(norm)
        result = np.divide(law.f(norm),norm,out=np.zeros_like(norm),where=norm>0)
        clipped += int(np.sum(result < 1e-12))
        return np.maximum(result,1e-12)

    separation = np.diff(c)
    # At the face, opposite-side cell width weights linear interpolation.
    fraction = width[:-1]/(width[:-1]+width[1:])
    grface = (1-fraction)[None,:]*gr[:,:-1]+fraction[None,:]*gr[:,1:]
    gzface = (1-fraction)[:,None]*gz[:-1]+fraction[:,None]*gz[1:]
    radial_mu[1:n] = mu(np.diff(phi,axis=0)/separation[:,None],gzface)
    vertical_mu[:,1:n] = mu(np.diff(phi,axis=1)/separation[None,:],grface)
    radial_mu[n] = mu((pr-phi[-1])/(width[-1]/2),tr)
    vertical_mu[:,n] = mu((pz-phi[:,-1])/(width[-1]/2),tz)
    kr = np.zeros_like(radial_mu)
    kz = np.zeros_like(vertical_mu)
    kr[1:n] = edges[1:n,None]*width[None,:]/separation[:,None]*radial_mu[1:n]
    kr[n] = edges[-1]*width/(width[-1]/2)*radial_mu[n]
    area = (edges[1:]**2-edges[:-1]**2)/2
    kz[:,1:n] = area[:,None]/separation[None,:]*vertical_mu[:,1:n]
    kz[:,n] = area/(width[-1]/2)*vertical_mu[:,n]
    diagonal = kr[:-1]+kr[1:]+kz[:,:-1]+kz[:,1:]
    rhs = np.zeros_like(phi)
    rhs[-1] += kr[-1]*pr
    rhs[:,-1] += kz[:,-1]*pz
    rhs[:,0] -= bottom

    def apply(v):
        out = diagonal*v
        out[1:] -= kr[1:-1]*v[:-1]
        out[:-1] -= kr[1:-1]*v[1:]
        out[:,1:] -= kz[:,1:-1]*v[:,:-1]
        out[:,:-1] -= kz[:,1:-1]*v[:,1:]
        return out
    return apply, diagonal, rhs, clipped, kr, kz


def solve(geometry,boundary,initial,newtonian=False):
    phi = initial.copy()
    pr,pz,tr,tz,bottom = boundary
    mass = float(np.sum(bottom))
    history = []
    success = False
    for outer in range(300):
        apply, diagonal, rhs, _, _, _ = operator(phi,geometry,boundary,newtonian)
        candidate,inner,inner_error,ok = law.pcg(apply,diagonal,rhs,phi)
        if not ok:
            history.append({'outer':outer,'inner':inner,'inner_error':inner_error,'linear_failed':True})
            break
        phi = candidate if newtonian else .4*phi+.6*candidate
        apply,diagonal,rhs,clipped,kr,kz = operator(phi,geometry,boundary,newtonian)
        residual = float(np.linalg.norm(apply(phi)-rhs)/np.linalg.norm(rhs))
        outgoing = float(np.sum(kr[-1]*(pr-phi[-1]))+np.sum(kz[:,-1]*(pz-phi[:,-1])))
        balance = abs(outgoing-mass)/mass
        history.append({'outer':outer,'inner':inner,'inner_error':inner_error,
                        'nonlinear_error':residual,'flux_balance_error':balance,'clipped_faces':clipped})
        if residual <= 1e-9 and clipped == 0 and balance <= 2e-6:
            success = True
            break
    _,c,_ = geometry
    disk_phi = phi[:,0]-c[0]*(phi[:,1]-phi[:,0])/(c[1]-c[0])
    radial = np.gradient(disk_phi,c,edge_order=2)
    return phi,radial,history,success
