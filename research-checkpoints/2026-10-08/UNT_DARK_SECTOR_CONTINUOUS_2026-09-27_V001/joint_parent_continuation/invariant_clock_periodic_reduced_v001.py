"""Constraint-reduced chart of the exact periodic K(X)/J/compression action.

SOURCE ONLY: no initializer, driver, integration, file access, or qualification.
Uses invariant_clock_periodic_exact_v002 and the reviewed constraint algebra
of initial_v002, but does NOT impose zero mean shear after the initial slice.

Chart (8,N), all rows in additive, unscaled canonical units:
 [fa, fb, u, phase, mean_delta_pi_a, delta_pi_T, pi_u, delta_pi_phi].
Row4 is spatially constant and dynamical. Row5 is a fixed dust restweight
profile. Nonzero metric-momentum modes and pi_b are reconstructed from the
Hamiltonian and momentum constraints at EVERY RHS evaluation. No accepted
state is projected afterward. Only the declared reflection sector is covered:
rows2,6 odd, all other rows even, on an odd periodic grid.

Local H_pi_b=bdot>0 defines the expansion-connected branch. On that branch
P_pi_a=-adot/bdot and reduced momentum Newton action is
 [a_x-(adot/bdot)b_x]*delta_pi_a-Dx(delta_pi_a).
Its one free constant is fixed by mean(delta_pi_a), not by resetting shear.
Evolving this mean with the mean original Hamilton RHS makes the chart
equivalent to the full constrained continuum equations while regular:
 k*ra+l*rb=0, ra_x=[a_x-(k/l)b_x]*ra, mean(ra)=0 => ra=rb=0.

Default inner relative arithmetic allowance is 1e-10 against ACTUAL
perturbative constraint terms, never 6*Vbar*H^2. A numerical floor of 1e-30
only defines a denominator for identically vanishing terms; it is not an
absolute acceptance allowance. Final external evolution/refinement gates
are not supplied or altered here. All local inverse gates are inherited.

reconstruct returns a dict including z, fields, constraints and diagnostics.
rhs returns d(chart)/d log(abar), and by default (rhs,reconstruction).
matrices returns UNscaled complex modal chart tangents, shape (N//2+1,8,8).
The fixed row5 input is retained in that matrix; it is NOT an external
time-dependent ordinary source. A caller using scaled Fourier coefficients
must apply its own consistent similarity transformation.
"""

import math
import numpy as np
from invariant_clock_periodic_exact_v002 import PeriodicExact, LocalInverseError


class ConstraintReconstructionError(ValueError):
    def __init__(self, message, diagnostics):
        super().__init__(message)
        self.diagnostics = diagnostics


class Reduced:
    state_order = ("fa", "fb", "u", "phase", "mean_delta_pi_a",
                   "delta_pi_T", "pi_u", "delta_pi_phi")
    matrix_convention = "unscaled chart Fourier coefficients; d/dlog(abar)"

    def __init__(self, model, N, k, *, constraint_tolerance=1e-10,
                 local_tolerance=1e-10, iterations=16, local_iterations=20,
                 backtracks=16, parity_tolerance=1e-10, warm_start=False):
        self.core = PeriodicExact(model, N, k)
        self.m, self.n, self.k = model, self.core.n, self.core.k
        self.cT, self.F = self.core.cT, self.core.F
        self.KB, self.C = self.core.KB, self.core.C
        self.pi_phi_bar = self.core.pi_phi_bar
        for value in (constraint_tolerance, local_tolerance, parity_tolerance):
            if not math.isfinite(value) or not 0 < value < 1:
                raise ValueError("positive finite relative allowance below one required")
        for value in (iterations, local_iterations, backtracks):
            if int(value) != value or value < 1:
                raise ValueError("positive integer iteration limits required")
        self.tolerance = float(constraint_tolerance)
        self.local_tolerance = float(local_tolerance)
        self.parity_tolerance = float(parity_tolerance)
        self.iterations, self.local_iterations = int(iterations), int(local_iterations)
        self.backtracks = int(backtracks)
        self.warm_start, self._warm = bool(warm_start), None
        phase = 2*np.pi*np.arange(self.n)/self.n
        self.nm = np.arange(self.n//2+1)
        self.cosine = np.cos(self.nm[:, None]*phase)
        self.sine = np.sin(self.nm[1:, None]*phase)
        self.wave = self.k*self.nm[1:]
        self.dxcos = -self.k*self.nm[:, None]*np.sin(self.nm[:, None]*phase)
        self.mirror = (-np.arange(self.n)) % self.n

    def _chart(self, chart):
        y = np.asarray(chart)
        if y.shape != (8, self.n) or np.iscomplexobj(y) or not np.all(np.isfinite(y)):
            raise ValueError("finite real chart of shape (8,N) required")
        y = np.array(y, dtype=float, copy=True)
        row_scale = np.maximum(np.max(abs(y), axis=1), 1e-30)
        signs = np.array([1, 1, -1, 1, 1, 1, -1, 1])[:, None]
        parity = np.max(abs(y-signs*y[:, self.mirror]), axis=1)/row_scale
        if np.max(parity) > self.parity_tolerance:
            raise ConstraintReconstructionError("outside the declared reflection sector",
                                                dict(parity_relative=parity.tolist()))
        constant_error = float(np.max(abs(y[4]-np.mean(y[4])))/row_scale[4])
        if constant_error > self.parity_tolerance:
            raise ConstraintReconstructionError("row4 must be spatially constant",
                                                dict(constant_row_relative=constant_error))
        return y, float(np.max(parity)), constant_error

    def from_full(self, x, z, piT):
        """Encode an already qualified full initial state; no state projection.

        Caller must first qualify its H,D constraints. For an arbitrary
        off-constraint input, later reconstruction would define different
        metric momenta; this helper does not certify that preparation.
        """
        z = np.asarray(z)
        if z.shape != (8, self.n) or np.iscomplexobj(z) or not np.all(np.isfinite(z)):
            raise ValueError("finite full additive state of shape (8,N) required")
        piT = self.core._dust(piT)
        chart = np.array(z, dtype=float, copy=True)
        chart[4] = np.mean(z[4])
        chart[5] = piT-self.core.background(x)['pi_T_bar']
        return self._chart(chart)[0]

    def _linear_guess(self, x, y):
        g = self.core.background(x)
        z = y.copy()
        fv = y[0]+2*y[1]
        z[4] = g['pi_a_bar']*fv+self.pi_phi_bar*y[3]
        z[4] += np.mean(y[4])-np.mean(z[4])
        z[5] = (-z[4]-g['Qbar']*y[7]/g['H']
                +g['Vbar']*g['core_bar']*fv/g['H']
                +2*g['abar']*g['chi_bar']*self.core.dx(y[2])/g['H']
                -4*g['abar']*self.core.dx(self.core.dx(y[1]))/g['H']
                -self.core.dx(y[6])/g['H']-y[5]/g['H'])
        return z

    def _scales(self, g, cc, piT, target):
        z = g['state']
        background_H = (g['Vbar']*(-6*self.F*g['H']**2
                        +2*(g['Qbar']*g['mbar']-g['Kbar']))+g['pi_T_bar']
                        +(self.pi_phi_bar-2*g['Vbar']*g['mbar'])*g['Qbar'])
        terms = np.array([
            g['H']*(z[4]+z[5]), g['pi_a']*g['delta_adot'],
            g['pi_b']*g['delta_bdot'], g['pi_u']*g['udot'],
            g['Qbar']*z[7], g['pi_phi']*g['qdiff'],
            -g['core_density_delta'], -2*g['fg']*g['bx']**2,
            self.core.dx(cc['boundary']), piT-g['pi_T_bar'],
            np.full(self.n, background_H)])
        hscale = max(float(np.max(np.sum(abs(terms), axis=0))), 1e-30)
        dscale = max(float(np.max(np.sum(abs(cc['momentum_terms']), axis=0))), 1e-30)
        pscale = max(float(np.max(abs(z[4]))), abs(target), dscale/self.k, 1e-30)
        return hscale, dscale, pscale

    def _local_h(self, x, state, piT, target, ds_guess=None):
        z = state.copy()
        last = None
        for iteration in range(self.local_iterations):
            g = self.core.fields(x, z, ds_guess=ds_guess)
            if np.any(g['bdot'] <= 0):
                raise ConstraintReconstructionError("expanding transverse branch lost",
                    dict(min_bdot=float(np.min(g['bdot'])), iteration=iteration))
            cc = self.core.constraints(x, z, piT, fields=g)
            hs, _, _ = self._scales(g, cc, piT, target)
            norm = float(np.max(abs(cc['Hamiltonian'])))
            last = dict(iteration=iteration, H_absolute=norm, H_scale=hs,
                        H_relative=norm/hs)
            if norm/hs <= self.local_tolerance:
                return z, g, cc, last
            step = cc['Hamiltonian']/g['bdot']
            accepted = False
            for half in range(self.backtracks):
                trial = z.copy()
                trial[5] -= step*2.**(-half)
                try:
                    gt = self.core.fields(x, trial, ds_guess=g['ds'])
                    if np.any(gt['bdot'] <= 0):
                        continue
                    ct = self.core.constraints(x, trial, piT, fields=gt)
                except (LocalInverseError, FloatingPointError, ValueError):
                    continue
                if np.max(abs(ct['Hamiltonian'])) < norm:
                    z, ds_guess, accepted = trial, gt['ds'], True
                    break
            if not accepted:
                raise ConstraintReconstructionError("local Hamiltonian backtracking failed", last)
        raise ConstraintReconstructionError("local Hamiltonian iteration cap", last)

    def _residual(self, g, cc, piT, target):
        hs, ds, ps = self._scales(g, cc, piT, target)
        r = np.r_[np.mean(g['state'][4])-target,
                  2*np.mean(self.sine*cc['momentum'], axis=1)/self.wave]
        # Full pointwise D is checked too: no untested even residual is dropped.
        errors = dict(H_relative=float(np.max(abs(cc['Hamiltonian']))/hs),
            momentum_relative=float(np.max(abs(cc['momentum']))/ds),
            momentum_modal_relative=float(np.max(abs(r[1:]))/ps),
            mean_relative=float(abs(r[0])/ps), H_scale=hs,
            momentum_scale=ds, momentum_potential_scale=ps)
        merit = max(errors['momentum_relative'], errors['momentum_modal_relative'],
                    errors['mean_relative'])
        return r, merit, errors

    def reconstruct(self, x, chart):
        y, parity, constant_error = self._chart(chart)
        bg = self.core.background(x)
        piT = self.core._dust(bg['pi_T_bar']+y[5])
        target = float(np.mean(y[4]))
        z = self._linear_guess(x, y)
        ds_guess = None
        used_warm = False
        if self.warm_start and self._warm is not None:
            warm = z.copy()
            warm[4:6] = self._warm['momenta']
            warm[4] += target-np.mean(warm[4])
            try:
                z, g, cc, local = self._local_h(x, warm, piT, target,
                                              ds_guess=self._warm['ds'])
                ds_guess, used_warm = g['ds'], True
            except (LocalInverseError, ConstraintReconstructionError, ValueError):
                z = self._linear_guess(x, y)
        history = []
        for iteration in range(self.iterations):
            z, g, cc, local = self._local_h(x, z, piT, target, ds_guess=ds_guess)
            ds_guess = g['ds']
            r, merit, errors = self._residual(g, cc, piT, target)
            history.append(dict(iteration=iteration, local=local, **errors))
            if merit <= self.tolerance:
                if self.warm_start:
                    self._warm = dict(momenta=z[4:6].copy(), ds=g['ds'].copy())
                return dict(x=float(x), chart=y, z=z, piT=piT, fields=g,
                    constraints=cc, history=history, diagnostics=dict(
                        **errors, parity_relative=parity,
                        constant_row_relative=constant_error,
                        target_mean_delta_pa=target, warm_start_used=used_warm,
                        min_bdot=float(np.min(g['bdot'])),
                        inverse_error=g['inverse_error']))
            ratio = g['adot']/g['bdot']
            action = (g['ax']-ratio*g['bx'])*self.cosine-self.dxcos
            jac = np.empty((len(self.nm), len(self.nm)))
            jac[0] = 0.
            jac[0, 0] = 1.
            jac[1:] = 2*(self.sine@action.T)/(self.n*self.wave[:, None])
            correction = np.linalg.solve(jac, -r)@self.cosine
            accepted = False
            for half in range(self.backtracks):
                trial = z.copy()
                trial[4] += correction*2.**(-half)
                try:
                    trial, gt, ct, _ = self._local_h(x, trial, piT, target,
                                                   ds_guess=g['ds'])
                    _, mt, _ = self._residual(gt, ct, piT, target)
                except (LocalInverseError, ConstraintReconstructionError, ValueError):
                    continue
                if mt < merit or mt <= self.tolerance:
                    z, ds_guess, accepted = trial, gt['ds'], True
                    break
            if not accepted:
                raise ConstraintReconstructionError("reduced momentum/mean backtracking failed",
                                                    dict(history=history))
        raise ConstraintReconstructionError("reduced constraint iteration cap",
                                            dict(history=history))

    def rhs(self, x, chart, return_fields=True):
        rec = self.reconstruct(x, chart)
        g = rec['fields']
        # _proper_rhs already returns the additive delta_pi_a derivative,
        # including subtraction of pi_a_bar_dot. Do not subtract it twice.
        full = self.core._proper_rhs(g)
        out = np.zeros_like(rec['chart'])
        out[:4] = full[:4]
        out[4] = np.mean(full[4])
        out[6:8] = full[6:8]
        out /= g['H']
        rec['full_rhs_proper'] = full
        return (out, rec) if return_fields else out

    def matrices(self, x):
        """Exact homogeneous modal tangent in the UNscaled reduced chart.

        For n!=0 D fixes delta_pa. For n=0 chart row4 is its free value.
        H fixes delta_pb at every mode, including the fixed dust-row forcing.
        This is a numerical splitting/preconditioner, not a frozen-background
        replacement of the nonlinear RHS or a physical eigenmode selection.
        """
        g = self.core.background(x)
        a, V, H = g['abar'], g['Vbar'], g['H']
        Q, m, d = g['Qbar'], g['mbar'], g['dbar']
        waves = self.k*self.nm
        ik = 1j*waves[:, None]
        basis = np.eye(8, dtype=complex)
        fa, fb, u, phase, meanpa, dust, pu, pc = [basis[i][None, :] for i in range(8)]
        fv = fa+2*fb
        pa = np.broadcast_to(g['pi_a_bar']*fv+self.pi_phi_bar*phase,
                             (len(waves), 8)).copy()
        pa[0] = meanpa[0]
        pb = (-pa-Q*pc/H+V*g['core_bar']*fv/H
              +2*a*g['chi_bar']*ik*u/H+4*a*waves[:, None]**2*fb/H
              -ik*pu/H-dust/H)
        paV, pbV = pa/V+4*self.F*H*fv, pb/V+8*self.F*H*fv
        dc = self.cT/self.F*((paV+pbV)/4-ik*u/a**2)
        bd, ad = -paV/4+dc/2, (paV-pbV)/4+dc/2
        dm = pc/(2*V)-m*fv
        qd = np.broadcast_to(dm/d, (len(waves), 8))
        p = (Q*u+ik*phase)/a
        e = (pu/(2*a*a)-g['chi_bar']*u/a-self.C*p)/self.KB
        ud, D = a*e, self.C*(e-p)
        core = -4*H*ad-8*H*bd+2*m*qd+6*H*dc+g['core_bar']*fv
        pad = V*core-2*a*g['chi_bar']*ik*u
        meanpad = np.zeros_like(pad)
        meanpad[0] = pad[0]
        pud = 2*a*a*Q*D+2*a*g['chi_bar']*(H*u+ud)-2*a*ik*dc
        pcd = -2*a*a*ik*(D-(m/Q)*ik*phase/a)
        zero = np.zeros_like(pad)
        return np.stack((ad, bd, ud, qd, meanpad, zero, pud, pcd), axis=1)/H
