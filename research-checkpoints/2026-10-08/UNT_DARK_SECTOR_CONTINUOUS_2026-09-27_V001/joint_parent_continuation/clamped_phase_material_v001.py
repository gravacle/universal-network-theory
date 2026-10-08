"""Inert batched common-phase material; caller owns authentication and execution.

No files, producer imports, eigensolves, formation or scientific runs at import.
All gradients use the dimensionless source G=g_physical/gstar; Phi=ln(N/Nb).
"""
import math
import numpy as np
from numpy.polynomial.legendre import leggauss

CONFIG = dict(bisections=80, bracket_doublings=64, branch_eta_squared=1/12,
              default_order=128, default_chunk_size=256)


class MaterialDomainError(RuntimeError):
    """Uncertified, nonfinite or otherwise invalid constitutive request."""


def _rule(order):
    if not isinstance(order, int) or order < 2:
        raise ValueError('Quadrature order must be an integer >=2')
    nodes, weights = leggauss(order)
    theta = (nodes+1)*math.pi/4
    return weights/2, np.cos(theta), np.sin(theta)**2


def _center(r, eta):
    k = 1+r*r
    return 2*np.sqrt(k/3)*np.sinh(np.arcsinh(3*math.sqrt(3)*eta/(2*k**1.5))/3)


def _geometry(r, eta, quadrature):
    w, x, sin2 = quadrature
    c = _center(r, eta)
    rc, cc = r[:, None], c[:, None]
    op = (2*cc+rc*x)**2+2*cc*cc+rc*rc
    om = (2*cc-rc*x)**2+2*cc*cc+rc*rc
    a, b = np.sqrt(2+op), np.sqrt(2+om)
    delta = -np.sum(w*(op/(a*(math.sqrt(2)+a))
                       +om/(b*(math.sqrt(2)+b)))/2, axis=1)
    return c, a, b, -delta/(1+delta)


def _frequency_excess(r, eta, quadrature):
    return _geometry(r, eta, quadrature)[-1]


def _orbit(r, eta, quadrature):
    """Exact paired centered-orbit quadratures and analytic derivatives."""
    w, x, sin2 = quadrature
    c, a, b, omega_excess = _geometry(r, eta, quadrature)
    rc, cc = r[:, None], c[:, None]
    omega = 1+omega_excess
    odd = 4*cc*rc*x
    ie = (1/a+1/b)/2
    io = -odd/(a*b*(a+b))
    je = (a**-3+b**-3)/2
    jo = -odd*(a*a+a*b+b*b)/(a**3*b**3*(a+b))
    L = np.sum(w*ie, axis=1)

    def mean_pair(pair, power=1):
        even, odd_part = pair
        ew, ow = (ie, io) if power == 1 else (je, jo)
        return np.sum(w*(even*ew+odd_part*ow), axis=1)

    def multiply(left, right):
        le, lo = left
        re, ro = right
        return le*re+lo*ro, le*ro+lo*re

    z = (cc, rc*x)
    z2 = (cc*cc+rc*rc*x*x, 2*cc*rc*x)
    z3 = (cc**3+3*cc*rc*rc*x*x, 3*cc*cc*rc*x+rc**3*x**3)
    z4 = (cc**4+6*cc*cc*rc*rc*x*x+rc**4*x**4,
          4*cc**3*rc*x+4*cc*rc**3*x**3)
    mean2 = mean_pair(z2)/L
    mean4 = mean_pair(z4)/L
    direct_mean = mean_pair(z)/L
    # M3/eta, with its exact continuous eta=0 value. No 0/0 or
    # subtraction of opposite O(r^3) terms at a tiny source.
    m3_over_eta = np.sum(w*((cc*cc+3*rc*rc*x*x)*ie
        -4*rc*rc*x*x*(3*cc*cc+rc*rc*x*x)/(a*b*(a+b))), axis=1)
    m3_over_eta /= L*(1+r*r+c*c)
    mean3 = eta*m3_over_eta
    source_mean = eta*(1-m3_over_eta)
    d = 1+r*r+3*c*c
    cr, ce = -2*c*r/d, 1/d
    qr = (12*cc*cr[:, None]+2*rc*(1+x*x),
          4*(cc+rc*cr[:, None])*x)
    qe = (12*cc*ce[:, None], 4*rc*ce[:, None]*x)
    omega_r = omega*mean_pair(qr, 3)/(2*L)
    omega_eta = omega*mean_pair(qe, 3)/(2*L)
    i = r*r/math.sqrt(2)*np.sum(w*sin2*(a+b)/2, axis=1)
    i_r = r*(d-4*c*c*r*r/d)/omega
    i_r_direct = (math.sqrt(2)*r*np.sum(w*sin2*(a+b)/2, axis=1)
        +r*r/(2*math.sqrt(2))*mean_pair((sin2*qr[0], sin2*qr[1])))
    i_eta = r*r/(2*math.sqrt(2))*mean_pair((sin2*qe[0], sin2*qe[1]))

    def m3_derivative(za, qa):
        first = 3*mean_pair(multiply(z2, za))/L
        covariance = (mean_pair(multiply(z3, qa), 3)
                      -mean3*mean_pair(qa, 3))/L
        return first-covariance/2

    mr = m3_derivative((cr[:, None], x), qr)
    me = m3_derivative((ce[:, None], 0), qe)
    c0 = _center(np.zeros_like(r), eta)
    k0 = 1+3*c0*c0
    shift = -c*r*r/(1+c*c+c*c0+c0*c0)
    xp, xm = r+shift, -r+shift

    def excitation(v):
        return v*v*(k0/2+c0*v+v*v/4)

    epsilon_min = -.5*c0*c0-.75*c0**4
    epsilon_exc = excitation(xp)
    epsilon = epsilon_min+epsilon_exc
    pressure = mean4/4+eta*source_mean/2
    kinetic = r*r/4*np.sum(w*sin2*(a+b)/2, axis=1)/L
    moving = r > 0
    eii = 3*(1-7*c0*c0)/(4*k0*k0)
    bi = -3*c0/k0**1.5
    deficit = 3*c0*c0/k0
    maxwell = bi.copy()
    phase_deficit_other = -3*c0*c0*(3+7*c0*c0)/(k0*(1-7*c0*c0))
    eii[moving] = omega_r[moving]/i_r[moving]
    bi[moving] = -mr[moving]/i_r[moving]
    deficit[moving] = me[moving]-mr[moving]*i_eta[moving]/i_r[moving]
    maxwell[moving] = -(omega_eta[moving]
                       -omega_r[moving]*i_eta[moving]/i_r[moving])
    phase_deficit_other[moving] = (me[moving]
        -mr[moving]*omega_eta[moving]/omega_r[moving])
    # Exact h=0 positive-deficit continuation, including the empty point.
    zero = eta == 0
    origin_q = 3*(epsilon+pressure)/(1+4*epsilon)
    origin_raw_error = np.where(zero, deficit-origin_q, 0.)
    origin_moment_error = np.where(zero, m3_over_eta-origin_q, 0.)
    for value in (source_mean, direct_mean, mean3, bi, maxwell,
                  i_eta, mr, omega_eta):
        value[zero] = 0.
    deficit[zero] = origin_q[zero]
    m3_over_eta[zero] = origin_q[zero]
    phase_deficit_other[zero] = origin_q[zero]
    return dict(r=r, eta=eta, c=c, i=i, omega=omega,
        omega_excess=omega_excess, epsilon=epsilon,
        epsilon_min=epsilon_min, epsilon_exc=epsilon_exc,
        pressure=pressure, mean2=mean2, mean3=mean3, mean4=mean4,
        b=source_mean, direct_mean=direct_mean, m3_over_eta=m3_over_eta,
        eii=eii, b_i=bi, susceptibility_deficit_fixed_i=deficit,
        square_correction=bi*bi/eii,
        phase_deficit_other=phase_deficit_other, maxwell_b_i=maxwell,
        i_r=i_r, i_r_direct=i_r_direct, i_eta=i_eta,
        omega_r=omega_r, omega_eta=omega_eta,
        mean3_r=mr, mean3_eta=me, kinetic=kinetic,
        other_turning_exc=excitation(xm),
        origin_deficit_identity_error=origin_raw_error,
        origin_moment_identity_error=origin_moment_error)


class Material:
    """One authenticated-by-caller spectrum/calibration, unchanged in space."""
    def __init__(self, source_row, spectrum, beta=.005, chunk_size=256):
        self.source_row = dict(source_row)
        self.delta = np.asarray(spectrum['delta'], dtype=float).copy()
        self.weights = np.asarray(spectrum['weights'], dtype=float).copy()
        self.beta = float(beta)
        self.chunk_size = int(chunk_size)
        self.R = float(source_row['R'])
        self.S = float(source_row['S'])
        self.gstar = float(source_row['gstar'])
        self.Ib = float(source_row['I'])
        self.DeltaU = float(source_row['DeltaU'])
        self.Ws = math.fsum(self.weights)
        self.Kb = self.Ws+self.beta
        self._rules = {}
        self._baselines = {}
        scalars = [self.R,self.S,self.gstar,self.Ib,self.beta,self.Kb]
        if (self.delta.ndim != 1 or self.weights.shape != self.delta.shape
                or not np.all(np.isfinite(self.delta))
                or not np.all(np.isfinite(self.weights))
                or not np.all(self.delta > 0) or not np.all(self.weights > 0)
                or not all(math.isfinite(v) and v > 0 for v in scalars)
                or not math.isfinite(self.DeltaU) or self.chunk_size < 1):
            raise MaterialDomainError('Invalid positive finite material input')
        self.all_field_certificate_margin = 1-12*(self.S/self.R**2)**2
        if self.all_field_certificate_margin <= 0:
            raise MaterialDomainError('All-field hardening certificate not satisfied')

    def quadrature(self, order=128):
        if order not in self._rules:
            self._rules[order] = _rule(order)
        return self._rules[order]

    def baseline(self, order=128):
        if order not in self._baselines:
            energy = float(self.source_row['E'])/self.beta
            if not math.isfinite(energy) or energy <= 0:
                raise MaterialDomainError('Positive cosmic excitation required')
            b2 = 4*energy/(self.R**2+math.sqrt(self.R**4+4*energy))
            rb = math.sqrt(b2)/self.R
            o = _orbit(np.array([rb]), np.array([0.]), self.quadrature(order))
            unit = {key:float(value[0]) for key,value in o.items()}
            eh = self.beta*self.R**4*unit['epsilon']
            ph = self.beta*self.R**4*unit['pressure']
            th_unit = unit['mean2']+1.5*unit['mean4']
            self._baselines[order] = dict(Eb=eh,Pib=ph,
                Tb=self.beta*self.R**4*th_unit,hard_Eb=eh,hard_Pib=ph,
                Ib=self.Ib,unit=unit,Tb_unit=th_unit,
                K0=self.beta*unit['susceptibility_deficit_fixed_i'],
                Jb=self.beta*self.R**4*(unit['omega']**2/unit['eii']
                                      +3*unit['i']*unit['omega']),
                DeltaU=self.DeltaU)
        return self._baselines[order]

    def _phase_orbits(self, Phi, eta, order):
        quadrature = self.quadrature(order)
        base = self.baseline(order)['unit']
        target = base['omega_excess']*np.exp(-Phi)+np.expm1(-Phi)
        c0 = _center(np.zeros_like(eta), eta)
        min_excess = 3*c0*c0/(np.sqrt(1+3*c0*c0)+1)
        occupied = target > min_excess
        r = np.zeros_like(eta)
        if np.any(occupied):
            t, h = target[occupied], eta[occupied]
            lo = np.zeros_like(t)
            hi = np.maximum(math.sqrt(2*self.Ib/self.R**3),
                            np.sqrt(8*t/3))
            for _ in range(CONFIG['bracket_doublings']):
                need = _frequency_excess(hi,h,quadrature) < t
                if not np.any(need):
                    break
                hi[need] *= 2
            else:
                raise MaterialDomainError('No certified occupied frequency bracket')
            for _ in range(CONFIG['bisections']):
                mid = (lo+hi)/2
                below = _frequency_excess(mid,h,quadrature) < t
                lo = np.where(below,mid,lo)
                hi = np.where(below,hi,mid)
            r[occupied] = (lo+hi)/2
        orbit = _orbit(r,eta,quadrature)
        denominator = np.maximum(np.maximum(np.abs(target),
                                 np.abs(orbit['omega_excess'])),1e-300)
        err = np.where(occupied, np.abs(orbit['omega_excess']-target),
                       np.maximum(target-orbit['omega_excess'],0.))/denominator
        return orbit, occupied, target, err

    def _soft(self, h):
        ds, ws = self.delta[None,:], self.weights[None,:]
        ys = 2*ds/math.sqrt(3)*np.sinh(
            np.arcsinh(3*math.sqrt(3)*h[:,None]/(2*ds*ds))/3)
        v = (ys/ds)**2
        return dict(E=-np.sum(ws*(ds*ds*ys*ys/2+3*ys**4/4),axis=1),
            B_over_h=np.sum(ws/(1+v),axis=1),
            deficit_over_h=np.sum(ws*v/(1+v),axis=1),
            susceptibility_deficit=np.sum(ws*3*v/(1+3*v),axis=1))

    def _evaluate_chunk(self, Phi, G, order):
        base = self.baseline(order)
        z = (G/self.S)**2
        h_over_G = 1/np.sqrt(1+z)
        h = G*h_over_G
        hp = (1+z)**-1.5
        hpp = -3*G/self.S**2*(1+z)**-2.5
        o, occupied, target, error = self._phase_orbits(Phi,h/self.R**2,order)
        soft = self._soft(h)
        deficit_h = soft['deficit_over_h']+self.beta*o['m3_over_eta']
        B_over_h = soft['B_over_h']+self.beta*(1-o['m3_over_eta'])
        B = h*B_over_h
        F = hp*B
        ct = z*(2+z)/(1+z)**2
        KT = self.Kb*ct+hp*h_over_G*deficit_h
        KL_same_I = (self.Kb*z*(3+3*z+z*z)/(1+z)**3-hpp*B
            +hp*hp*(soft['susceptibility_deficit']
                     +self.beta*o['susceptibility_deficit_fixed_i']))
        square = np.where(occupied,hp*hp*self.beta*o['square_correction'],0.)
        KL = KL_same_I-square
        F_Phi = np.where(occupied,
            -hp*self.beta*self.R**2*o['omega']*o['b_i']/o['eii'],0.)
        J = np.where(occupied,self.beta*self.R**4*(o['omega']**2/o['eii']
                                                +3*o['i']*o['omega']),0.)
        # Ratio F_Phi/G is finite at G=0; use the exact derivative of the
        # zero-source susceptibility deficit there, rather than 0/0.
        qi = 3*((o['omega']+o['i']*o['eii'])*(1+4*o['epsilon'])
                 -4*o['i']*o['omega']**2)/(1+4*o['epsilon'])**2
        bi_over_eta = np.divide(o['b_i'],o['eta'],out=-qi.copy(),where=o['eta']!=0)
        F_Phi_over_G = np.where(occupied,
            -hp*h_over_G*self.beta*o['omega']*bi_over_eta/o['eii'],0.)
        F_over_G = hp*h_over_G*B_over_h
        zero = G == 0
        KT[zero] = self.beta*o['susceptibility_deficit_fixed_i'][zero]
        KL[zero] = KT[zero]
        KL_same_I[zero] = KT[zero]
        F[zero] = F_Phi[zero] = 0.
        hard_E = self.beta*self.R**4*o['epsilon']
        hard_Pi = self.beta*self.R**4*o['pressure']
        hard_min = self.beta*self.R**4*o['epsilon_min']
        hard_exc = self.beta*self.R**4*o['epsilon_exc']
        soft_E = soft['E']
        deltaE = soft_E+self.beta*self.R**4*(o['epsilon']-base['unit']['epsilon'])
        deltaPi = -soft_E+self.beta*self.R**4*(o['pressure']-base['unit']['pressure'])
        deltaT_soft = -2*soft_E
        deltaT_hard = self.beta*self.R**4*(o['mean2']+1.5*o['mean4']-base['Tb_unit'])
        origin = (Phi == 0)&zero
        deltaE[origin] = deltaPi[origin] = deltaT_hard[origin] = 0.
        I = self.R**3*o['i']
        I[origin] = self.Ib
        return dict(E=soft_E+hard_E,Pi=-soft_E+hard_Pi,
            deltaE=deltaE,deltaPi=deltaPi,
            deltaT=deltaT_soft+deltaT_hard,
            deltaT_soft=deltaT_soft,deltaT_hard=deltaT_hard,
            KT=KT,KL=KL,F=F,F_Phi=F_Phi,J=J,I=I,I_over_Ib=I/self.Ib,
            branch=occupied.astype(np.int8),eII=o['eii']/self.R**2,
            hard_E=hard_E,hard_Pi=hard_Pi,hard_min=hard_min,
            hard_excitation=hard_exc,soft_E=soft_E,h=h,h_prime=hp,h_second=hpp,
            B=B,F_over_G=F_over_G,F_Phi_over_G=F_Phi_over_G,
            Tg_over_G=2*F_over_G-F_Phi_over_G,
            normalized_D=G*KT/self.Kb,normalized_mu=KT/self.Kb,
            common_frequency_error=error,omega_excess=o['omega_excess'],
            target_omega_excess=target,omega=self.R*o['omega'],
            KL_same_local_I=KL_same_I,longitudinal_phase_square=square,
            unit_i=o['i'],unit_eii=o['eii'],unit_r=o['r'],eta=o['eta'],
            maxwell_error=o['b_i']-o['maxwell_b_i'],
            chain_rule_error=(o['susceptibility_deficit_fixed_i']
                              -o['square_correction']-o['phase_deficit_other']),
            action_derivative_error=o['i_r']-o['i_r_direct'],
            mean_equation_error=o['b']-o['direct_mean'],
            origin_deficit_identity_error=o['origin_deficit_identity_error'],
            origin_moment_identity_error=o['origin_moment_identity_error'],
            unit_energy_identity_error=(o['epsilon']-o['kinetic']
                -o['mean2']/2-o['mean4']/4+o['eta']*o['b']),
            unit_pressure_identity_error=o['i']*o['omega']-o['epsilon']-o['pressure'])

    def evaluate(self, Phi, G, order=128):
        """Return same-shaped arrays. G is a nonnegative source magnitude.

        Branch codes: 0 EMPTY, 1 OCCUPIED. No stiffness is clipped. Caller
        must distinguish a numerical/domain error from a physical branch.
        """
        Phi, G = np.broadcast_arrays(np.asarray(Phi,dtype=float),np.asarray(G,dtype=float))
        shape = Phi.shape
        pv, gv = Phi.ravel(),G.ravel()
        if not np.all(np.isfinite(pv)) or not np.all(np.isfinite(gv)) or np.any(gv<0):
            raise MaterialDomainError('Finite Phi and nonnegative finite G required')
        if not pv.size:
            raise MaterialDomainError('Empty material request')
        pieces = []
        try:
            with np.errstate(over='raise',invalid='raise',divide='raise'):
                for start in range(0,pv.size,self.chunk_size):
                    piece = self._evaluate_chunk(pv[start:start+self.chunk_size],
                                                 gv[start:start+self.chunk_size],order)
                    if (np.any(piece['eII']<=0)
                            or any(not np.all(np.isfinite(v)) for v in piece.values())):
                        raise MaterialDomainError('Nonfinite or nonconvex material output')
                    pieces.append(piece)
        except (FloatingPointError,OverflowError) as exc:
            raise MaterialDomainError('Floating-domain failure: '+str(exc)) from exc
        return {key:np.concatenate([p[key] for p in pieces]).reshape(shape)
                for key in pieces[0]}
