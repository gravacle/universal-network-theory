"""V002 additive-delta-s inverse of the exact periodic K(X)/J action.

Arithmetic repair ONLY: V001 is preserved unchanged. Newton evolves ds=s-sbar
as an independent floating-point number. Xdiff, mdiff and deltaK use that ds,
never a subtraction of two rounded total s values. Total s=sbar+ds is used
only for smooth constitutive coefficients and the inherited positive-sheet
check. Default local inverse tolerance is tightened from 4e-14 to 1e-16.
No physical equation, external acceptance gate, state or branch is changed.

No driver, integrator, initializer, file access, calibration or numerical
qualification is supplied. Pass the authenticated inherited Model instance:
its constitutive(s) and UNCOMPRESSED, dust-only bg(log_a) primitives are used.
The sole declared completion is cTheta=.01. H=H_old/sqrt(1+1.5*cTheta);
no cosmological density or scalar charge is refitted here.

Coordinates: ds^2=-dt^2+A^2 dx^2+B^2(dy^2+dz^2), x periodic 2*pi/k.
All velocities and canonical momenta refer to proper coordinate time t.
The public rhs() returns d/d log(abar); rhs_proper() returns d/dt.
State shape (8,n), ADDITIVE conventions (not the old normalized variables):
  [fa, fb, u, phase, delta_pi_a, delta_pi_b, pi_u, delta_pi_phi].
A=abar*exp(fa), B=abar*exp(fb), u=U_x, phi=phi_bar(t)+phase.
pi_a_bar=-4*abar^3*F*H, pi_b_bar=2*pi_a_bar, pi_phi_bar=model.pcbar
is constant. Spectral derivatives subtract the mean first; odd grids are
required so there is no discarded Nyquist mode. No mode filter is applied.

L=V[-4*adot*bdot-2*bdot^2+KB*e^2+2*C*e*p-C*(p^2+J)
    +2*K(X)-cTheta*Theta^2]+2*(B^2/A)*b_x^2.
X=sqrt(q^2-w^2), q=phi_dot, w=phi_x/A, sigma=u/A, c=sqrt(1+sigma^2),
p=sigma*q+c*w, e=(u_dot+c_x)/A, chi=-cTheta*Theta.
The local solve follows s>0 and the positive regular Legendre sheet. Newton
backtracking changes an ITERATE only; no evolved state/charge is clipped.
Failure raises LocalInverseError with diagnostics. Warm guesses are optional
and never physical branch/charge data. Dust pi_T is fixed and enters ONLY
constraints/stress: rho_b=pi_T/(2V). Geodesic-comoving dust requires a
single-valued congruence; shell crossing is outside this representation.

Vary lapse and shift BEFORE gauge fixing. Their exact continuum constraints:
 Hcan+Dx[4*(B^2/A)*b_x+c*pi_u]+pi_T=0,
 pi_a*a_x+pi_b*b_x-Dx(pi_a)-u*Dx(pi_u)+pi_phi*phi_x=0.
The primary Hamiltonian diagnostic uses this canonical divergence, not a
discrete product-rule replacement. A separate geometric form is returned
to expose spectral product-rule/aliasing error. Initial constraints must be
solved by the caller; a linear gauge lift is not exact initial data.

Required independent controls before evolution: homogeneous FLRW, analytic
Legendre/Jacobian tests, finite-difference Euler--Lagrange/Hamiltonian tests,
charge conservation, constraint-flow tangents, time/grid/alias refinement,
branch and dust-volume checks. No such controls have been executed here.
"""

import math
import numpy as np


class LocalInverseError(ValueError):
    """An unqualified local inverse, with the last finite diagnostic values."""

    def __init__(self, message, diagnostics):
        super().__init__(message)
        self.diagnostics = diagnostics


class PeriodicExact:
    state_order = ("fa", "fb", "u", "phase", "delta_pi_a", "delta_pi_b",
                   "pi_u", "delta_pi_phi")

    def __init__(self, model, n, k_comoving, *, cTheta=.01,
                 inverse_tolerance=1e-16, inverse_iterations=24):
        if int(n) != n or n < 5 or n % 2 != 1:
            raise ValueError("an odd periodic grid with n>=5 is required")
        if not math.isfinite(k_comoving) or k_comoving <= 0:
            raise ValueError("positive finite comoving fundamental k required")
        if not math.isfinite(cTheta) or cTheta <= 0:
            raise ValueError("positive cTheta required; this module is not a cTheta=0 solver")
        if not (0 < model.KB < 2 and model.Q0 > 0 and model.eps > 0
                and model.bs > 0 and model.pcbar > 0):
            raise ValueError("unsupported inherited constitutive parameters")
        if not (math.isfinite(inverse_tolerance) and 0 < inverse_tolerance < 1):
            raise ValueError("positive inverse tolerance below one required")
        if int(inverse_iterations) != inverse_iterations or inverse_iterations < 1:
            raise ValueError("positive integer inverse iteration limit required")
        self.m = model
        self.n, self.k = int(n), float(k_comoving)
        self.cT, self.F = float(cTheta), 1+1.5*float(cTheta)
        self.KB, self.C = float(model.KB), float(model.C)
        self.eta = self.C/self.KB
        self.pi_phi_bar = float(model.pcbar)
        self.tolerance, self.iterations = float(inverse_tolerance), int(inverse_iterations)
        self.modes = np.fft.fftfreq(self.n, 1/self.n)
        self.coordinate = 2*np.pi*np.arange(self.n)/(self.n*self.k)

    def dx(self, f):
        f = np.asarray(f)
        if f.shape != (self.n,) or np.iscomplexobj(f) or not np.all(np.isfinite(f)):
            raise ValueError("spectral derivative requires a finite real grid vector")
        return np.fft.ifft(1j*self.k*self.modes*np.fft.fft(f-np.mean(f))).real

    def background(self, x):
        abar, sbar, Qbar, mbar, Kbar, H_old, hx, qrootbar = self.m.bg(float(x))
        H = H_old/math.sqrt(self.F)
        Hdot = hx*H*H
        Vbar = abar**3
        pi_a_bar = -4*Vbar*self.F*H
        pi_b_bar = 2*pi_a_bar
        pi_a_bar_dot = -4*self.F*Vbar*(3*H*H+Hdot)
        chi_bar = -3*self.cT*H
        dbar = float(self.m.constitutive(sbar)[2])
        core_bar = -6*self.F*H*H+2*Kbar
        return dict(abar=abar, sbar=sbar, Qbar=Qbar, mbar=mbar, Kbar=Kbar,
                    qrootbar=qrootbar, dbar=dbar, H=H, Hdot=Hdot, hx=hx,
                    Vbar=Vbar, pi_a_bar=pi_a_bar, pi_b_bar=pi_b_bar,
                    pi_a_bar_dot=pi_a_bar_dot, pi_b_bar_dot=2*pi_a_bar_dot,
                    chi_bar=chi_bar, core_bar=core_bar, pi_T_bar=6*self.m.OB)

    @staticmethod
    def _log_remainder(t):
        """log(1+t)-t/(1+t), avoiding its small-t cancellation."""
        out = np.log1p(t)-t/(1+t)
        small = abs(t) < 1e-3
        ts = t[small]
        series = np.zeros_like(ts)
        for power in range(10, 1, -1):
            series = series*ts+((-1.)**power)*(power-1)/power
        out[small] = ts*ts*series
        return out

    def _j(self, p):
        z = abs(p)/self.m.bs
        root = np.hypot(p, self.m.bs)
        j = self.m.lam*abs(p)/root
        jt = self.m.lam*abs(p)*(p*p+2*self.m.bs**2)/root**3
        J = self.m.lam*self.m.bs**2*(z*np.sqrt(1+z*z)-np.arcsinh(z))
        small = z < .01
        t = z[small]
        J[small] = self.m.lam*self.m.bs**2*(2*t**3/3-t**5/5+3*t**7/28-5*t**9/72)
        return j, jt, J

    def fields(self, x, z, *, s_guess=None, ds_guess=None):
        z = np.asarray(z)
        if z.shape != (8, self.n) or np.iscomplexobj(z) or not np.all(np.isfinite(z)):
            raise ValueError("finite real additive canonical state of shape (8,n) required")
        g = self.background(x)
        fa, fb, u, phase, delta_pa, delta_pb, pi_u, delta_pc = z
        fvol = fa+2*fb
        A, B = g['abar']*np.exp(fa), g['abar']*np.exp(fb)
        V = g['Vbar']*np.exp(fvol)
        if not np.all(np.isfinite(V)) or np.any(V <= 0):
            raise ValueError("nonpositive/nonfinite volume")
        pi_a, pi_b = g['pi_a_bar']+delta_pa, g['pi_b_bar']+delta_pb
        pi_phi = self.pi_phi_bar+delta_pc
        ax, bx, ux, phix = (self.dx(f) for f in (fa, fb, u, phase))
        sigma = u/A
        c = np.hypot(1., sigma)
        sigmax = (ux-u*ax)/A
        cx = sigma*sigmax/c
        w = phix/A
        P = pi_u/(2*B*B)
        # Ratios are split analytically about the same FLRW background.
        dpaV = -4*self.F*g['H']*np.expm1(-fvol)+delta_pa/V
        dpbV = -8*self.F*g['H']*np.expm1(-fvol)+delta_pb/V
        paV, pbV = -4*self.F*g['H']+dpaV, -8*self.F*g['H']+dpbV
        base_charge_offset = self.pi_phi_bar/(2*g['Vbar'])-g['mbar']
        delta_M = g['mbar']*np.expm1(-fvol)+delta_pc/(2*V)+base_charge_offset*np.exp(-fvol)
        M = g['mbar']+delta_M
        Gx = sigmax/(A*c*c)+2*sigma*bx/A
        delta_gmetric = (self.F*g['H']*sigma*sigma*(2-3/(c+1))/c
                        -((1+2*sigma*sigma)*dpaV+dpbV)/(4*c))
        delta_chiblock = sigma*sigma/(c*c)*(.5-1/self.KB)
        chi_block = self.F/self.cT+delta_chiblock
        if np.any(chi_block <= 0) or not np.all(np.isfinite(chi_block)):
            raise LocalInverseError("left the positive chi block", dict(min_chi_block=float(np.min(chi_block))))
        cross = -self.eta*sigma*sigma/c

        def evaluate(ds):
            # Total s is NOT used to recover ds. Keep the small inverse
            # unknown through all residual, norm and pressure differences.
            s = g['sbar']+ds
            if np.any(s <= 0) or not np.all(np.isfinite(s)):
                return None
            X, m, d, K, dm_ds, qroot = self.m.constitutive(s)
            Xdiff = self.m.Q0*self.m.eps*ds/((1+s)*(1+g['sbar'])*(qroot+g['qrootbar']))
            mdiff = self.m.mpref*(qroot*ds+g['sbar']*Xdiff/self.m.Q0)
            q = np.hypot(X, w)
            qdiff = Xdiff+w*w/(q+X)
            p = (sigma*g['Qbar']+c*w)+sigma*qdiff
            delta_beta = delta_gmetric+Gx+sigma*(P-self.C*p)/(c*self.KB)
            delta_chi = -(delta_beta+delta_chiblock*g['chi_bar'])/chi_block
            chi = g['chi_bar']+delta_chi
            Z = (P-sigma*g['chi_bar']/c)-sigma*delta_chi/c
            e = (Z-self.C*p)/self.KB
            j, jt, J = self._j(p)
            D = self.C*(e-(1+j)*p)
            qq_entry = d*q*q/(X*X)-m*w*w/(X**3)-sigma*sigma*self.C*(2/self.KB+jt)
            schur = qq_entry-cross*cross/chi_block
            residual = mdiff+m*w*w/(X*(q+X))+sigma*D-delta_M
            scale = np.maximum.reduce((abs(M), abs(m), abs(sigma*D), np.full(self.n, abs(g['mbar']))))
            error = float(np.max(abs(residual)/scale))
            if not all(np.all(np.isfinite(v)) for v in (X, m, d, chi, q, D, schur, residual)):
                return None
            return dict(s=s, ds=ds, X=X, m=m, d=d, K=K, dm_ds=dm_ds, qroot=qroot,
                        Xdiff=Xdiff, mdiff=mdiff, q=q, qdiff=qdiff, p=p,
                        delta_chi=delta_chi, chi=chi, Z=Z, e=e, j=j, jt=jt,
                        J=J, D=D, qq_entry=qq_entry, schur=schur,
                        determinant=chi_block*schur, inverse_residual=residual,
                        inverse_scale=scale, inverse_error=error)

        if s_guess is not None and ds_guess is not None:
            raise ValueError("pass only one optional inverse guess")
        if ds_guess is not None:
            ds = np.array(ds_guess, dtype=float, copy=True)
        elif s_guess is not None:
            # Legacy absolute-s input is only an initial numerical guess.
            # Every subsequent Newton iterate retains its additive ds.
            ds = np.array(s_guess, dtype=float, copy=True)-g['sbar']
        else:
            ds = np.zeros(self.n)
        if ds.shape != (self.n,):
            raise ValueError("inverse guess must have shape (n,)")
        local = evaluate(ds)
        count = 0
        for count in range(1, self.iterations+1):
            if local is None or np.any(local['schur'] <= 0):
                raise LocalInverseError("invalid positive-sheet local iterate", dict(iteration=count, ds=ds.tolist(), s=(g['sbar']+ds).tolist()))
            if local['inverse_error'] <= self.tolerance:
                break
            ds_dq_inverse = (local['X']/local['q'])*(local['dm_ds']/local['d'])
            step = local['inverse_residual']/(local['schur']*ds_dq_inverse)
            accepted = False
            for halving in range(24):
                trial_ds = ds-step*(.5**halving)
                trial = evaluate(trial_ds)
                if (trial is not None and np.all(trial['schur'] > 0)
                        and trial['inverse_error'] < local['inverse_error']):
                    ds, local, accepted = trial_ds, trial, True
                    break
            if not accepted:
                raise LocalInverseError("local Newton backtracking failed", dict(
                    iteration=count, residual=local['inverse_error'], min_s=float(np.min(g['sbar']+ds))))
        if local is None or local['inverse_error'] > self.tolerance:
            raise LocalInverseError("local inverse iteration limit", dict(
                iterations=count, residual=None if local is None else local['inverse_error']))

        g.update(local)
        chi, dc = g['chi'], g['delta_chi']
        inv_c_minus_one = -sigma*sigma/(c*(c+1))
        shift_c = sigma*sigma*(1+.5/c)/(c+1)
        delta_bdot = -dpaV/4+dc/(2*c)+g['chi_bar']*inv_c_minus_one/2
        delta_adot = (dpaV-dpbV)/4+(.5+shift_c)*dc+g['chi_bar']*shift_c
        adot, bdot = g['H']+delta_adot, g['H']+delta_bdot
        udot = A*g['e']-cx
        Theta = -chi/self.cT
        t = g['ds']/(1+g['sbar'])
        delta_K = 3*self.m.OA/self.m.D*(self._log_remainder(t)
                    +g['sbar']/(1+g['sbar'])*t/(1+t))
        Lvec = self.KB*g['e']**2+2*self.C*g['e']*g['p']-self.C*(g['p']**2+g['J'])
        delta_kin = -4*g['H']*delta_adot-8*g['H']*delta_bdot-4*delta_adot*delta_bdot-2*delta_bdot**2
        delta_core = delta_kin+Lvec+2*delta_K+6*g['H']*dc-dc*dc/self.cT
        core_density_delta = V*delta_core+g['Vbar']*np.expm1(fvol)*g['core_bar']
        fg = B*B/A
        g.update(state=z, fa=fa, fb=fb, u=u, phase=phase, fvol=fvol, A=A, B=B,
                 V=V, pi_a=pi_a, pi_b=pi_b, pi_u=pi_u, pi_phi=pi_phi,
                 ax=ax, bx=bx, ux=ux, phix=phix, sigma=sigma, c=c,
                 sigmax=sigmax, cx=cx, w=w, P=P, M=M, delta_M=delta_M,
                 paV=paV, pbV=pbV, chi_block=chi_block, cross=cross, Gx=Gx,
                 delta_adot=delta_adot, delta_bdot=delta_bdot, adot=adot,
                 bdot=bdot, udot=udot, Theta=Theta, delta_K=delta_K,
                 Lvec=Lvec, delta_kin=delta_kin, delta_core=delta_core,
                 core_density_delta=core_density_delta, fg=fg,
                 inverse_iterations=count)
        return g

    def _coordinate_variation(self, g, *, da=0., du=0.):
        """Non-volume part of dL/V at fixed velocities and spatial jets."""
        A, sig, c, sx = g['A'], g['sigma'], g['c'], g['sigmax']
        dsig = du/A-sig*da
        dsx = -du*g['ax']/A-sx*da
        dc = sig*dsig/c
        dcx = sx*dsig/c**3+sig*dsx/c
        dw = -g['w']*da
        de = dcx/A-g['e']*da
        dp = g['q']*dsig+g['w']*dc+c*dw
        dX = -g['w']*dw/g['X']
        dTheta = (-g['adot']*dc/c**2+2*g['bdot']*dc
                  +g['udot']/A*(dsig/c-sig*dc/c**2-sig*da/c)
                  +(dsx+2*g['bx']*dsig-(sx+2*sig*g['bx'])*da)/A)
        return 2*g['Z']*de+2*g['D']*dp+2*g['m']*dX+2*g['chi']*dTheta

    def _proper_rhs(self, g):
        V, A, B, sig, c = g['V'], g['A'], g['B'], g['sigma'], g['c']
        chi, Z, bx = g['chi'], g['Z'], g['bx']
        flux_a = -2*B*B*(chi*sig+Z*sig*sig/c)
        flux_b = 4*B*B*chi*sig+4*g['fg']*bx
        # Subtract the spatially constant u_x conjugate flux analytically.
        fv = 2*g['fb']-g['fa']
        flux_u_delta = 2*g['abar']*(np.exp(fv)*(g['delta_chi']+sig*Z/c)
                                             +g['chi_bar']*np.expm1(fv))
        current = c*g['D']-(g['m']/g['X'])*g['w']
        flux_phi = 2*B*B*current
        rest_a = self._coordinate_variation(g, da=1.)
        rest_u = self._coordinate_variation(g, du=1.)
        background_defect = g['Vbar']*g['core_bar']-g['pi_a_bar_dot']
        dpa = (g['core_density_delta']+V*rest_a-2*g['fg']*bx*bx
               -self.dx(flux_a)+background_defect)
        dpb = (2*g['core_density_delta']+4*g['fg']*bx*bx
               -self.dx(flux_b)+2*background_defect)
        dpu = V*rest_u-self.dx(flux_u_delta)
        dpc = -self.dx(flux_phi)
        out = np.array([g['delta_adot'], g['delta_bdot'], g['udot'],
                        g['qdiff'], dpa, dpb, dpu, dpc])
        if not np.all(np.isfinite(out)):
            raise ValueError("nonfinite exact canonical RHS")
        g.update(current=current, flux_a=flux_a, flux_b=flux_b,
                 flux_u_delta=flux_u_delta, flux_phi=flux_phi,
                 rest_a=rest_a, rest_u=rest_u)
        return out

    def rhs_proper(self, x, z, *, return_fields=False, s_guess=None, ds_guess=None):
        g = self.fields(x, z, s_guess=s_guess, ds_guess=ds_guess)
        out = self._proper_rhs(g)
        return (out, g) if return_fields else out

    def rhs(self, x, z, *, return_fields=False, s_guess=None, ds_guess=None):
        out, g = self.rhs_proper(x, z, return_fields=True, s_guess=s_guess, ds_guess=ds_guess)
        out = out/g['H']
        return (out, g) if return_fields else out

    def _dust(self, pi_T):
        pi_T = np.asarray(pi_T, dtype=float)
        if pi_T.shape != (self.n,) or not np.all(np.isfinite(pi_T)) or np.any(pi_T < 0):
            raise ValueError("finite nonnegative fixed dust restweight of shape (n,) required")
        return pi_T

    def constraints(self, x, z, pi_T, *, fields=None):
        g = self.fields(x, z) if fields is None else fields
        pi_T = self._dust(pi_T)
        delta_pa, delta_pb, delta_pc = g['state'][4], g['state'][5], g['state'][7]
        delta_Hcan = (g['H']*(delta_pa+delta_pb)+g['pi_a']*g['delta_adot']
            +g['pi_b']*g['delta_bdot']+g['pi_u']*g['udot']+g['Qbar']*delta_pc
            +g['pi_phi']*g['qdiff']-g['core_density_delta']-2*g['fg']*g['bx']**2)
        background_H = (g['Vbar']*(-6*self.F*g['H']**2+2*(g['Qbar']*g['mbar']-g['Kbar']))
            +g['pi_T_bar']+(self.pi_phi_bar-2*g['Vbar']*g['mbar'])*g['Qbar'])
        boundary = 4*g['fg']*g['bx']+g['c']*g['pi_u']
        Hamiltonian = delta_Hcan+self.dx(boundary)+(pi_T-g['pi_T_bar'])+background_H
        momentum_terms = np.array([g['pi_a']*g['ax'], g['pi_b']*g['bx'],
             -self.dx(delta_pa), -g['u']*self.dx(g['pi_u']), g['pi_phi']*g['phix']])
        stress = self.stress_coefficients(x, z, pi_T, fields=g)
        R3 = (-4*self.dx(g['bx'])-6*g['bx']**2+4*g['ax']*g['bx'])/g['A']**2
        rho_bar = g['Qbar']*g['mbar']-g['Kbar']-g['chi_bar']**2/(2*self.cT)
        geo_background = g['Vbar']*(-6*g['H']**2+2*rho_bar)+g['pi_T_bar']
        geometric = (g['V']*(g['delta_kin']-R3+2*stress['delta_rho_clock'])
             +g['Vbar']*np.expm1(g['fvol'])*(-6*g['H']**2+2*rho_bar)
             +pi_T-g['pi_T_bar']+geo_background)
        return dict(Hamiltonian=Hamiltonian, momentum=np.sum(momentum_terms, axis=0),
                    momentum_terms=momentum_terms, Hamiltonian_geometric=geometric,
                    canonical_minus_geometric=Hamiltonian-geometric,
                    R3=R3, boundary=boundary, rho_dust=pi_T/(2*g['V']),
                    inverse_error=g['inverse_error'], min_s=float(np.min(g['s'])),
                    min_schur_fraction=float(np.min(g['schur']/(g['d']*g['q']**2/g['X']**2))),
                    min_chi_block=float(np.min(g['chi_block'])),
                    min_determinant=float(np.min(g['determinant'])),
                    mean_delta_pi_phi=float(np.mean(g['state'][7])))

    def stress_coefficients(self, x, z, pi_T=None, *, fields=None, chi_dot=None):
        """Exact continuum normal stress; pressures are affine in chi_dot.

        chi_dot must be the consistent proper-time derivative of the local
        inverse, not an imposed multiplier. If absent, return its coefficients
        instead of silently supplying zero. No time-tangent solver is hidden.
        Spatial geometric stress uses continuum product rules; compare against
        the canonical constraints to measure semidiscrete aliasing defects.
        """
        g = self.fields(x, z) if fields is None else fields
        A, B, V, sig, c = g['A'], g['B'], g['V'], g['sigma'], g['c']
        divZ = self.dx(g['Z'])+2*g['bx']*g['Z']
        chix = self.dx(g['delta_chi'])
        delta_rho = (self.KB*g['e']**2/2+self.C*(g['p']**2+g['J'])/2
            -g['delta_K']+g['delta_M']*g['Qbar']+g['M']*g['qdiff']
            +(c*divZ+sig*chix)/A
            -(2*g['chi_bar']*g['delta_chi']+g['delta_chi']**2)/(2*self.cT))
        rho_bar = g['Qbar']*g['mbar']-g['Kbar']-g['chi_bar']**2/(2*self.cT)
        energy_flux = sig*divZ/A-g['M']*g['w']+c*chix/A
        Tvol = g['adot']+2*g['bdot']
        sigmadot = g['udot']/A-sig*g['adot']
        cdot = sig*sigmadot/c
        Lmat = g['Lvec']+2*(g['Kbar']+g['delta_K'])-g['chi']**2/self.cT
        flux_a = -2*B*B*(g['chi']*sig+g['Z']*sig*sig/c)
        flux_b_mat = 4*B*B*g['chi']*sig
        Ppar0 = ((Lmat+self._coordinate_variation(g, da=1.))/2
                 -self.dx(flux_a)/(2*V)-g['chi']*Tvol/c+g['chi']*cdot/c**2)
        Ptrans0 = Lmat/2-self.dx(flux_b_mat)/(4*V)-g['chi']*c*Tvol-g['chi']*cdot
        answer = dict(rho_clock=rho_bar+delta_rho, delta_rho_clock=delta_rho,
                      energy_flux_clock=energy_flux, P_parallel_constant=Ppar0,
                      P_transverse_constant=Ptrans0, P_parallel_chidot=-1/c,
                      P_transverse_chidot=-c)
        if chi_dot is not None:
            chi_dot = np.asarray(chi_dot, dtype=float)
            if chi_dot.shape != (self.n,) or not np.all(np.isfinite(chi_dot)):
                raise ValueError("consistent finite proper-time chi_dot of shape (n,) required")
            answer.update(P_parallel=Ppar0-chi_dot/c, P_transverse=Ptrans0-c*chi_dot)
        if pi_T is not None:
            rho_dust = self._dust(pi_T)/(2*V)
            answer.update(rho_dust=rho_dust, rho_total=rho_bar+delta_rho+rho_dust)
        return answer
