"""Chi-primary equivalent local chart, source only and not qualified yet.

Same positive K(X)/J/compression branch as exact_v002. delta_chi is supplied
independently and never recovered from pi_b inside fields_chi or the RHS.
At fixed chi the scalar charge derivative is Aq, not its eliminated Schur.
The original fields() is inherited only as an independent reference and an
optional starting guess; a reconstructed fields dict must be passed directly
to constraints and _proper_rhs. This file changes no action or acceptance gate.
"""
import numpy as np
from invariant_clock_periodic_exact_v002 import PeriodicExact as Parent, LocalInverseError

class PeriodicChi(Parent):
    def fields_chi(self, x, z, delta_chi, *, s_guess=None, ds_guess=None):
        z = np.asarray(z)
        if z.shape != (8, self.n) or np.iscomplexobj(z) or not np.all(np.isfinite(z)):
            raise ValueError("finite real additive canonical state of shape (8,n) required")
        delta_chi = np.asarray(delta_chi, dtype=float)
        if delta_chi.shape != (self.n,) or not np.all(np.isfinite(delta_chi)):
            raise ValueError('finite independent delta_chi required')
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
            step = local['inverse_residual']/(local['qq_entry']*ds_dq_inverse)
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
        # Reconstruct momentum from independent chi using stable background deltas.
        dpbV = (-(1+2*sigma*sigma)*dpaV
            +4*self.F*g['H']*sigma*sigma*(2-3/(c+1))
            +4*c*(chi_block*dc+delta_chiblock*g['chi_bar']+Gx)
            +4*sigma*(P-self.C*g['p'])/self.KB)
        delta_pb = V*dpbV+g['pi_b_bar']*np.expm1(fvol)
        z = z.copy()
        z[5] = delta_pb
        pi_b = g['pi_b_bar']+delta_pb
        pbV = -8*self.F*g['H']+dpbV
        g['Kchi'] = chi_block-cross*cross/g['qq_entry']
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


