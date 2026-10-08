"""Source-only polar Cauchy equations for the proposed compression completion.

This is not a driver or a qualified evolution. It adds only the already
declared -cTheta*(div U)**2 term, cTheta=.01, to polar_source_v005's full
mixed-p K(X)/J fields and conserved collisionless ordinary populations.
The inherited 5 kpc, kappa=1e-7 and 300L-compensated preparation scales are
unchanged; this module does NOT create a preparation or select support.

The caller MUST provide outer_callback(t)->(chi_outer, N_outer) at r[-1],
from its declared evolving outer solution. There is no held boundary,
invented boundary time derivative, fitted lapse or chi clipping here.
The caller separately checks compatibility of the returned chi_t with
that history, outer-domain validity and ordinary/field boundary work.

The coupled metric/compression constraints use regular-volume mass
quadrature and the inward chi kernel at fixed T0. Undamped Picard has
prospective absolute A tolerance 1e-12, relative chi tolerance 1e-10 and
maximum 50 iterations. Warm starts are numerical guesses only. Final
joint, chi-derivative and multiplier residuals are returned, not erased.
These tolerances are solver criteria, not physics/trajectory acceptance.

initial() and diagnose() deliberately do not inherit the old preparation
or compression-free Einstein checks. Root supplies initial data, exact
background/boundary history, independent diagnostics and any execution.
There is no main, file access, numerical run or coefficient scan here.
"""

import math
import numpy as np
import invariant_clock_polar_source_v005 as old
import invariant_clock_compression_radial_v001 as radial
import invariant_clock_compression_multiplier_v001 as multiplier


class GeometryConvergenceError(ValueError):
    """Failed prospective coupled iteration, retaining its last diagnostics."""

    def __init__(self, diagnostics):
        super().__init__("coupled compression geometry did not converge in 50 iterations")
        self.diagnostics = diagnostics


class Polar(old.Polar):
    A_TOL = 1e-12
    CHI_REL_TOL = 1e-10
    MAX_GEOMETRY_ITERATIONS = 50
    canonical_mode = False

    def __init__(self, saved, n=160, extent=.012, *, outer_callback):
        if not callable(outer_callback):
            raise ValueError("an explicit evolving outer_callback is required")
        # The inherited constructor calls bg(), so set these first.
        self.cTheta = .01
        self.Fcompression = 1 + 1.5*self.cTheta
        self.outer_callback = outer_callback
        super().__init__(saved, n, extent)
        self.canonical_mode = False
        self.chiguess = None
        self.chirguess = None
        self.max_chi_iteration = 0.

    def bg(self, x):
        values = list(super().bg(x))
        values[5] /= math.sqrt(self.Fcompression)
        # d ln H/d ln a is unchanged by this constant rescaling. All action
        # densities/charges are unchanged; this is not a recalibration.
        return tuple(values)

    def initial(self):
        raise NotImplementedError("supply independently constrained compression initial data")

    def diagnose(self, t, z):
        raise NotImplementedError("supply compression-aware independent evolution diagnostics")

    def _boundary(self, t):
        chi_outer, lapse_outer = self.outer_callback(float(t))
        chi_outer, lapse_outer = float(chi_outer), float(lapse_outer)
        if not math.isfinite(chi_outer) or not math.isfinite(lapse_outer) or lapse_outer <= 0:
            raise ValueError("outer chi must be finite and outer lapse finite and positive")
        return chi_outer, lapse_outer

    @staticmethod
    def _relative_chi_error(delta, chi, chi_outer):
        scale = max(float(np.max(np.abs(chi))), abs(chi_outer))
        error = float(np.max(np.abs(delta)))
        # No numerical floor or artificial nonzero chi is inserted.
        return (error/scale if scale else (0. if error == 0 else math.inf)), scale

    def _constraint_map(self, z, A, chi, chi_R, chi_outer, ur):
        r = self.r
        g = self.fields(z, A)
        sig, c = g['sig'], g['c']
        P_b = z[4]*z[5] + z[7]*z[8]
        j0 = (z[0]*g['divZ'] - z[3]*g['phir'] + P_b)/(A*A)
        rho0 = g['rhoC'] + g['rhoB']
        rhochi = sig*chi_R/A - chi*chi/(2*self.cTheta)
        rho_total = rho0 + rhochi
        mass = self.massint @ (rho_total/2)
        compactness = 2*mass/r
        if not np.all(np.isfinite(compactness)) or np.any(compactness >= 1):
            raise ValueError("nonfinite or trapped compression polar metric")
        mapped_A = 1/np.sqrt(1-compactness)
        # Local radial Einstein equation using the integrated mass, avoiding
        # loss of centre curvature in a rounded A nearly equal to one.
        # ar denotes A_R/A, not A_R. The joint mass defect is reported below.
        ar = A*A*(r*rho_total/2-mass/(r*r))
        sr = (ur-z[0]*ar)/A
        T0 = (-r*A*j0/(2*c) + sig*g['e']/c
              + (sr/(c*c)+2*sig/r)/A)
        mapped_chi, mapped_chi_R = radial.kernel(r, T0, chi_outer, self.cTheta)
        mapped_chi, mapped_chi_R = np.asarray(mapped_chi), np.asarray(mapped_chi_R)
        if not all(np.all(np.isfinite(v)) for v in
                   (mapped_A, mapped_chi, mapped_chi_R, ar, sr, rho_total)):
            raise ValueError("nonfinite compression constraint map")
        g.update(A=A, ar=ar, Ar=A*ar, sr=sr, P_b=P_b, j0=j0,
                 rho0=rho0, rhochi=rhochi, rho_total=rho_total,
                 mass=mass, compactness=compactness, T0=T0,
                 chi=chi, chi_R=chi_R)
        return g, mapped_A, mapped_chi, mapped_chi_R

    def geometry(self, t, z):
        z = np.asarray(z)
        if z.shape != (9, self.n) or np.iscomplexobj(z) or not np.all(np.isfinite(z)):
            raise ValueError("finite real mixed-p state of shape (9,n) required")
        if self.canonical_mode:
            raise ValueError("compression source uses mixed p, not the inherited canonical mode")
        if np.any(z[[4, 7]] < 0):
            raise ValueError("negative ordinary restweight")
        chi_outer, lapse_outer = self._boundary(t)
        A = np.array(self.Aguess, copy=True)
        chi = (np.full(self.n, chi_outer) if self.chiguess is None
               else np.array(self.chiguess, copy=True))
        chi_R = (np.zeros(self.n) if self.chirguess is None
                 else np.array(self.chirguess, copy=True))
        if any(v.shape != (self.n,) or not np.all(np.isfinite(v)) for v in (A, chi, chi_R)):
            raise ValueError("invalid numerical geometry warm start")
        if np.any(A <= 0):
            raise ValueError("positive metric warm start required")
        ur = self.derivative(z[0], -1)
        for iteration in range(1, self.MAX_GEOMETRY_ITERATIONS+1):
            g, next_A, next_chi, next_chi_R = self._constraint_map(
                z, A, chi, chi_R, chi_outer, ur)
            A_error = float(np.max(np.abs(next_A-A)))
            chi_error, chi_scale = self._relative_chi_error(next_chi-chi, next_chi, chi_outer)
            chi_R_error, _ = self._relative_chi_error(
                self.r*(next_chi_R-chi_R), next_chi, chi_outer)
            iteration_report = dict(iterations=iteration, A_absolute=A_error,
                                    chi_relative=chi_error, chi_scale=chi_scale,
                                    R_chi_R_relative=chi_R_error)
            if A_error <= self.A_TOL and chi_error <= self.CHI_REL_TOL:
                # g and the fixed-point defects refer to this SAME state;
                # do not return untested updated primitives from next_*.
                break
            A, chi, chi_R = next_A, next_chi, next_chi_R
        else:
            raise GeometryConvergenceError(iteration_report)

        Xminus = self.Q0*self.eps*g['s']/((1+g['s'])*(g['qr']+1))
        qminus = Xminus + g['w']**2/(g['q']+g['X'])
        q_R = self.derivative(qminus)
        Pr0 = g['PC'] + g['PrB']

        def radial_derivative(value, parity):
            if parity not in ('even', 'odd'):
                raise ValueError("unexpected derivative parity")
            return self.derivative(value, 1 if parity == 'even' else -1)

        solved = multiplier.multipliers(
            R=self.r, A=A, Ar=g['Ar'], sigma=g['sig'], sigma_R=g['sr'],
            w=g['w'], M=g['target'], Z=z[2], divZ=g['divZ'],
            X=g['X'], m=g['m'], d=g['d'], q=g['q'], Q=g['Q'], p=g['p'],
            e=g['e'], D=g['DD'], Jcur=g['cur'], jt=g['jt'],
            rhoB=g['rhoB'], PrB=g['PrB'], PtB=g['PtB'], P_b=g['P_b'],
            Pr0=Pr0, chi=chi, chi_R=chi_R,
            KB=self.KB, C=self.C, cTheta=self.cTheta,
            derivative=radial_derivative, q_R=q_R)
        lapsegrad = solved['lapse_gradient']
        lnN = self.lapseint @ lapsegrad
        lnN += math.log(lapse_outer)-lnN[-1]
        N = np.exp(lnN)
        if not np.all(np.isfinite(N)) or np.any(N <= 0):
            raise ValueError("nonpositive or nonfinite solved lapse")
        tauN = solved['chi_dot_over_N']
        sig, c = g['sig'], g['c']
        Prchi = sig*chi_R/A+chi*chi/(2*self.cTheta)-tauN/c
        Ptchi = -sig*chi_R/A+chi*chi/(2*self.cTheta)-c*tauN
        Pt0 = z[2]*g['e']-g['Ecal']/2+g['PtB']
        g.update(N=N, lnN=lnN, g=lapsegrad, q_R=q_R, qminus=qminus,
                 tauN=tauN, chi_dot_over_N=tauN, chi_t=N*tauN, Pr0=Pr0, Pt0=Pt0,
                 Prchi=Prchi, Ptchi=Ptchi, Pr_total=Pr0+Prchi,
                 Pt_total=Pt0+Ptchi, j_total=g['j0']+c*chi_R/A,
                 multiplier=solved, geometry_iteration=iteration_report,
                 mass_constraint_defect=(A-1)*(A+1)/(A*A)-2*g['mass']/self.r,
                 chi_constraint_defect=chi-self.cTheta*self.r*chi_R/2+self.cTheta*g['T0'],
                 chi_kernel_derivative_defect=next_chi_R-chi_R,
                 outer_chi=chi_outer, outer_lapse=lapse_outer,
                 outer_chi_state_defect=float(chi[-1]-chi_outer))
        self.Aguess, self.chiguess, self.chirguess = A.copy(), chi.copy(), chi_R.copy()
        self.max_metric_iteration = max(self.max_metric_iteration, A_error)
        self.max_chi_iteration = max(self.max_chi_iteration, chi_error)
        return g

    def rhs(self, t, z, return_g=False):
        if np.iscomplexobj(z):
            raise ValueError("real mixed-p state required")
        z = np.asarray(z, dtype=float)
        g = self.geometry(t, z)
        r, A, N, ar, gg = self.r, g['A'], g['N'], g['ar'], g['g']
        u, p, Z, cp, ns, ps, ell, nb, pb = z
        sig, c, X, Q, q, w = (g[k] for k in ('sig', 'c', 'X', 'Q', 'q', 'w'))
        sr, chi_R, tauN = g['sr'], g['chi_R'], g['tauN']
        adot = -N*r*(A*g['j0']+c*chi_R)/2
        out = np.zeros_like(z)
        out[0] = N*(A*g['e']-gg*c-sig*sr/c)
        sigt = out[0]/A-sig*adot
        out[2] = N*(Q*g['DD']/c-sig*g['divZ']/(A*c)-chi_R/A-sig*tauN/c)
        out[3] = -N*(self.divergence(g['cur'])+gg*g['cur'])
        Xminus = self.Q0*self.eps*g['s']/((1+g['s'])*(g['qr']+1))
        xr, pr = self.derivative(Xminus), self.derivative(p, -1)
        FF = (N*c*X*xr/(A*q)+N*w*pr/(A*q)-N*Q*p*sr/(A*q*c*c)
              +N*Q*g['e']/c-Q*p*adot/(q*c))
        Mp = g['m']*w/(X*Q)-sig*self.C*(2/self.KB+g['jt'])
        Ms = g['DD']-g['m']*w/(c*X)
        Xt = (out[3]/A-g['target']*adot-Mp*FF-Ms*sigt
              -sig*(self.C/self.KB)*out[2])/g['inverse']
        out[1] = FF+sig*X*Xt/q
        for ni, pi, energy, ell2 in ((4, 5, g['es'], ell*ell),
                                      (7, 8, g['eb'], np.zeros(self.n))):
            density, momentum = z[ni], z[pi]
            velocity = N*momentum/(A*A*energy)
            out[ni] = self.rest_flux(density, velocity)[0]
            out[pi] = (-velocity*self.derivative(momentum, -1)-N*gg*energy
                       +N/energy*(momentum*momentum*ar/(A*A)+ell2/r**3))
            if ni == 4:
                out[6] = -velocity*self.derivative(ell)
        if not np.all(np.isfinite(out)) or not np.all(np.isfinite(Xt)):
            raise ValueError("nonfinite compression mixed-p RHS")
        g.update(adot=adot, sigt=sigt, Xt=Xt, FF=FF)
        return (out, g) if return_g else out
