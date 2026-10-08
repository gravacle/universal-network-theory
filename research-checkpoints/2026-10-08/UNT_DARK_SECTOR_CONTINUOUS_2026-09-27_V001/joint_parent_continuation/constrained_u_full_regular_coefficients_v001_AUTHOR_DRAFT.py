"""UNLAUNCHABLE AUTHOR DRAFT: full formal regular coefficient assembly.

Root alone may eventually execute a reviewed frozen successor.  This draft
contains no producer imports, background root sampling or coefficient results.
Exact sparse arithmetic refers to explicit rationalized-log representations;
it is not a directed exact-transcendental rank theorem.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, time

class DecimalArithmetic:
    """Standard-library80/120-digit logarithm/root arithmetic; no dependency."""
    __version__ = 'stdlib-decimal'

    @property
    def mp(self):
        return self

    @property
    def dps(self):
        return getcontext().prec

    @dps.setter
    def dps(self,value):
        context = getcontext()
        context.prec = value
        context.rounding = ROUND_HALF_EVEN
        context.Emin,context.Emax = -999999999,999999999

    @staticmethod
    def mpf(value):
        return Decimal(value)

    @staticmethod
    def sqrt(value):
        return Decimal(value).sqrt()

    @staticmethod
    def log(value):
        return Decimal(value).ln()

    @staticmethod
    def log1p(value):
        return (1+Decimal(value)).ln()

    @staticmethod
    def nstr(value,digits):
        return format(Decimal(value),'.'+str(digits)+'g')

BASE = Path(__file__).resolve().parent
STEM = 'CONSTRAINED_U_FULL_REGULAR_COEFFICIENTS_V001'
PROTOCOL_SHA = 'PENDING'
UNLAUNCHABLE_AUTHOR_DRAFT = True
PRECISIONS = (80, 120)
OMEGAS = ('0.1', '1', '10', '100')
NREL, HALO, LOGDEG = 4, 6, 2
NS, LG, LN = 32, 96, 128
BACKGROUND_REL = 18
PINS = {
 'CONSTRAINED_U_FULL_REGULAR_INITIAL_COEFFICIENT_PACKET_DESIGN_V002.md': '69415077f30cd5b6ecaa14397605d36157860bed4edc10b833ac3843aca58ae6',
 'constrained_u_clock_gradient_early_transfer_v005.py': 'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20',
 'constrained_u_common_boundary_comoving_chart_v001.py': 'dc2181f3ce40166dfded934107705bcffb4b524b29ee36f4ff039baaf33933b3',
 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001_RESULT.json': '822f1e6e831ec5cd88e3f18777ef6ce2ebdc195f1e0bffa45dbcd293c1b059d5',
 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001_RECEIPT.json': 'a7434fd302b0c88e8ed6bb10112dbb0a86d0761e3f5a25f26fb3492265f98454',
 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RESULT.json': '8edf04b504f89b0e378823c2b5eda6547138361bb5ad13f6858bd0e34ce5be20',
 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': '867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd'}

def require(condition, message):
    if not condition:
        raise AssertionError(message)

class CoefficientRefusal(Exception):
    def __init__(self,message,details):
        super().__init__(message)
        self.details = details

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def exact_input(value):
    """Calibrated binary64 inputs are lifted exactly, with no hidden decimals."""
    require(type(value) in (int, float), 'Literal calibrated scalar')
    return Fraction(value)

class Field:
    """Q(hr,qinf), basis 1,hr,qinf,hr*qinf; explicit rational radicands."""
    rad = None

    def __init__(self, coefficients=0):
        if isinstance(coefficients, Field):
            self.v = coefficients.v
        elif isinstance(coefficients, (tuple, list)):
            require(len(coefficients) == 4, 'Biquadratic coefficient axis')
            self.v = tuple(Fraction(x) for x in coefficients)
        else:
            self.v = (Fraction(coefficients), Fraction(0), Fraction(0), Fraction(0))

    @classmethod
    def configure(cls, hr2, qi2):
        def square(q):
            return math.isqrt(q.numerator)**2 == q.numerator and math.isqrt(q.denominator)**2 == q.denominator
        hr2, qi2 = Fraction(hr2), Fraction(qi2)
        require(hr2 > 0 and qi2 > 0 and not any(square(x) for x in (hr2, qi2, hr2*qi2)),
                'Independent positive biquadratic basis; no rank guess')
        cls.rad = (hr2, qi2)

    def __bool__(self):
        return any(self.v)

    def __neg__(self):
        return Field(tuple(-x for x in self.v))

    def __add__(self, other):
        if isinstance(other, Series):
            return NotImplemented
        if isinstance(other, Linear):
            return other + self
        other = Field(other)
        return Field(tuple(x+y for x,y in zip(self.v, other.v)))

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Series):
            return NotImplemented
        return self + (-other if isinstance(other, (Field, Linear)) else -Field(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Series):
            return NotImplemented
        if isinstance(other, Linear):
            return other * self
        other = Field(other)
        require(Field.rad is not None, 'Configured exact field')
        out = [Fraction(0)]*4
        for i,x in enumerate(self.v):
            for j,y in enumerate(other.v):
                c = x*y
                if i & j & 1:
                    c *= Field.rad[0]
                if i & j & 2:
                    c *= Field.rad[1]
                out[i ^ j] += c
        return Field(out)

    __rmul__ = __mul__

    def conjugate(self, mask):
        return Field(tuple(-x if bin(i & mask).count('1') % 2 else x for i,x in enumerate(self.v)))

    def inverse(self):
        require(bool(self), 'Exact nonzero pivot')
        numerator = self.conjugate(1)*self.conjugate(2)*self.conjugate(3)
        norm = self*numerator
        require(not any(norm.v[1:]) and norm.v[0] != 0, 'Exact field norm')
        return Field(tuple(x/norm.v[0] for x in numerator.v))

    def __truediv__(self, other):
        if isinstance(other, Series):
            return NotImplemented
        return self * Field(other).inverse()

    def __pow__(self, exponent):
        require(type(exponent) is int, 'Integer field power')
        if exponent < 0:
            return self.inverse()**(-exponent)
        answer = Field(1)
        while exponent:
            if exponent & 1:
                answer *= self
            self = self*self
            exponent //= 2
        return answer

    def encode(self):
        return [[str(x.numerator), str(x.denominator)] for x in self.v]

    @classmethod
    def decode(cls,value):
        require(isinstance(value,list) and len(value) == 4, 'Full saved field coefficient')
        require(all(isinstance(x,list) and len(x) == 2 and all(type(s) is str for s in x) for x in value), 'Canonical rational components')
        decoded = cls(tuple(Fraction(int(n),int(d)) for n,d in value))
        require(decoded.encode() == value, 'Canonical reduced rational representation')
        return decoded

    def evaluate(self, mp):
        hr = mp.sqrt(mp.mpf(Field.rad[0].numerator)/Field.rad[0].denominator)
        qi = mp.sqrt(mp.mpf(Field.rad[1].numerator)/Field.rad[1].denominator)
        return sum(mp.mpf(x.numerator)/x.denominator*y for x,y in zip(self.v, (1, hr, qi, hr*qi)))

class Linear:
    """Sparse affine coefficient; column -1 is a declared constant."""
    def __init__(self, values=None):
        self.v = {int(k): Field(x) for k,x in (values or {}).items() if bool(Field(x))}

    def __bool__(self):
        return bool(self.v)

    def __neg__(self):
        return Linear({k:-x for k,x in self.v.items()})

    def __add__(self, other):
        other = other if isinstance(other, Linear) else Linear({-1:Field(other)})
        out = self.v.copy()
        for k,x in other.v.items():
            out[k] = out.get(k, Field(0)) + x
            if not out[k]:
                del out[k]
        return Linear(out)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other if isinstance(other, (Linear, Field)) else -Field(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        require(not isinstance(other, Linear), 'Linear system; no state-state product')
        return Linear({k:x*Field(other) for k,x in self.v.items()})

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self*Field(other).inverse()

    def encode(self):
        return [[k,x.encode()] for k,x in sorted(self.v.items())]

class Series:
    """Finite formal Laurent/polynomial-log series; no physical sampling."""
    MIN, MAX, ALGEBRA_LOG_MAX = -24, 320, 16

    def __init__(self, entries=None):
        self.v = {(int(p),int(l)):x if isinstance(x, (Field,Linear)) else Field(x)
                  for (p,l),x in (entries or {}).items() if bool(x)}
        require(all(self.MIN <= p <= self.MAX and 0 <= l <= self.ALGEBRA_LOG_MAX for p,l in self.v), 'Formal source range')

    @staticmethod
    def scalar(value):
        return Series({(0,0):value})

    @staticmethod
    def monomial(power, value=1, log=0):
        return Series({(power,log):value})

    def __neg__(self):
        return Series({k:-x for k,x in self.v.items()})

    def __add__(self, other):
        other = other if isinstance(other,Series) else Series.scalar(other)
        out = self.v.copy()
        for k,x in other.v.items():
            out[k] = out.get(k, Field(0)) + x
            if not out[k]:
                del out[k]
        return Series(out)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other if isinstance(other,Series) else -Series.scalar(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other,Series) else Series.scalar(other)
        out = {}
        for (p,l),x in self.v.items():
            for (q,m),y in other.v.items():
                k = (p+q,l+m)
                if self.MIN <= k[0] <= self.MAX:
                    require(k[1] <= self.ALGEBRA_LOG_MAX, 'Unsupported algebraic polynomial-log degree')
                    out[k] = out.get(k, Field(0)) + x*y
        return Series(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self*(other.inverse() if isinstance(other,Series) else Field(other).inverse())

    def __rtruediv__(self, other):
        return self.inverse()*other

    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'Nonnegative series power')
        out = Series.scalar(1)
        for _ in range(n):
            out = out*self
        return out

    def trim(self, low, high):
        return Series({k:x for k,x in self.v.items() if low <= k[0] <= high})

    def derivative(self):
        """a*d/da, including every explicit logarithm contact."""
        out = {}
        for (p,l),x in self.v.items():
            out[p,l] = out.get((p,l),Field(0)) + p*x
            if l:
                out[p,l-1] = out.get((p,l-1),Field(0)) + l*x
        return Series(out)

    def binomial(self, exponent, leading, power=0, order=BACKGROUND_REL):
        """Known leading root, so no numerical branch/root is selected."""
        require(type(exponent) is Fraction and isinstance(leading, Field), 'Declared rational power/leading root')
        ratio = self/Series.monomial(power, leading**exponent.denominator)
        r = ratio-1
        require(all(p >= 1 for p,l in r.v), 'Strict positive-order binomial remainder')
        out, term, coefficient = Series.scalar(1), Series.scalar(1), Fraction(1)
        for j in range(1,order+1):
            term = (term*r).trim(0,order)
            coefficient *= (exponent-(j-1))/j
            out += term*coefficient
        # This general interface is intentionally limited to square roots.
        require(exponent == Fraction(1,2) and power % 2 == 0, 'Owned square-root chart')
        return (Series.monomial(power//2,leading)*out).trim(power//2,power//2+order)

    def inverse(self, order=BACKGROUND_REL):
        require(self.v and not any(isinstance(x,Linear) for x in self.v.values()), 'Scalar nonzero source inverse')
        power = min(p for p,l in self.v)
        require((power,0) in self.v and all(p > power or l == 0 for p,l in self.v), 'Nonlogarithmic leading inverse')
        leading = self.v[power,0]
        unit = Series({(p-power,l):x/leading for (p,l),x in self.v.items()})-1
        require(all(p >= 1 for p,l in unit.v), 'Strict positive-order inverse remainder')
        out, term = Series.scalar(1), Series.scalar(1)
        for j in range(1,order+1):
            term = (-term*unit).trim(0,order)
            out += term
        return (Series.monomial(-power,leading.inverse())*out).trim(-power,-power+order)

    def log_unit(self, order=BACKGROUND_REL):
        require(self.v.get((0,0)) and not any(isinstance(x,Linear) for x in self.v.values()), 'Scalar unit logarithm')
        require(not (self.v[0,0]-1), 'Exact unit leading logarithm')
        r = self-1
        require(all(p >= 1 for p,l in r.v), 'Positive source logarithm remainder')
        out, term = Series(), Series.scalar(1)
        for j in range(1,order+1):
            term = (term*r).trim(0,order)
            out += term*Fraction((-1)**(j+1),j)
        return out

    def encode(self):
        return [[p,l,x.encode()] for (p,l),x in sorted(self.v.items())]

class Layout:
    def __init__(self):
        self.fg = {l:9+l-2 for l in range(2,LG+1)}
        i = 9+LG-1
        self.pol = {l:i+l for l in range(LG+1)}
        i += LG+1
        self.fn = {l:i+l-2 for l in range(2,LN+1)}
        i += LN-1
        self.z, self.zd = list(range(i,i+NS)), list(range(i+NS,i+2*NS))
        self.n, self.sigma = i+2*NS, i+2*NS+1
        require(self.n == 392 and self.sigma == 393, 'Entire392+2 inventory')
        self.names = ['R','Gamma_b','U_relative','Gamma_gamma','W_gamma_b','Gamma_nu','w_nu','Gamma_phi','V']
        self.names += ['F_gamma_'+str(l) for l in self.fg]+['G_gamma_'+str(l) for l in self.pol]
        self.names += ['F_nu_'+str(l) for l in self.fn]
        self.names += ['z_'+str(i) for i in range(NS)]+['zd_'+str(i) for i in range(NS)]+['n_U','sigma']
        self.powers = [0,2,4,2,6,2,4,2,2]
        self.powers += [2*l-1 for l in self.fg]+[3 if l in (0,2) else 5 if l == 1 else 2*l-1 for l in self.pol]
        self.powers += list(self.fn)+[6]*NS+[4]*NS+[5,2]
        require(len(self.names) == len(self.powers) == 394, 'All declared powers and names')

def formal_background(fixed, thermal, digits, mp):
    """Literal charge law plus one owned absolute stress/reference inventory."""
    q = {k:exact_input(fixed[k]) for k in ('eps','d0','OA','OB','OR','rG','Q0_over_Hstar','fgamma','Hunit','ell_native')}
    mp.mp.dps = digits+20
    eps_mp = mp.mpf(q['eps'].numerator)/q['eps'].denominator
    norm_text = mp.nstr(1/eps_mp-mp.log1p(1/eps_mp),digits)
    norm = Fraction(norm_text)
    alpha = q['eps']*norm*q['d0']/2
    qi_mp = mp.sqrt(1+eps_mp)
    log_text = mp.nstr(mp.log((mp.mpf(alpha.numerator)/alpha.denominator)/qi_mp),digits)
    q['norm'], q['alpha'], q['log_alpha_over_qinf'] = norm,alpha,Fraction(log_text)
    Field.configure(q['OR']/q['rG'],1+q['eps'])
    hr,qi = Field((0,1,0,0)),Field((0,0,1,0))
    a3 = Series.monomial(3)
    qb = Series.scalar(qi)
    # The cubic charge equation fixes each next coefficient without root sampling.
    for n in range(1,7):
        residual = qb*qb+(a3/alpha)*(qb**3-qb)-(1+q['eps'])
        require(all(l == 0 for p,l in residual.v), 'No charge logarithm')
        coef = residual.v.get((3*n,0),Field(0))
        qb -= Series.monomial(3*n,coef/(2*qi))
    t = (a3*qb/alpha).trim(0,BACKGROUND_REL)
    pex = ((1+t).log_unit()+Series.scalar(q['log_alpha_over_qinf'])
           -Series.monomial(0,3,1)-(qb/qi).log_unit()-(1+t).inverse())/norm
    b = Series.monomial(-3,Fraction(3,2)*q['OB']/q['rG'])
    r = Series.monomial(-4,Fraction(3,2)*q['OR']/q['rG'])
    w = qb*Series.monomial(-3,Fraction(3,2)*q['OA']*q['d0']/q['rG'])
    rho = (1+qb*Series.monomial(-3,q['d0'])-pex)*(Fraction(3,2)*q['OA']/q['rG'])
    h2 = (b+r+rho)*Fraction(2,3)
    h = h2.binomial(Fraction(1,2),hr,-4)
    c = q['eps']*t/(2*t*t+(4+3*q['eps'])*t+2*(1+q['eps']))
    Q = qb*q['Q0_over_Hstar']
    g0 = Fraction(299792458)*Fraction('6.6524587321e-29')*exact_input(thermal['nH0_cm3'])*10**6
    g0 *= 1+2*exact_input(thermal['fHe'])
    g0 /= q['Hunit']*1000/Fraction('3.0856775814913673e22')
    q0 = Fraction('0.01')*299792458/(1000*q['Hunit'])
    ans = dict(qbar=qb,t=t,pex=pex,b=b,r=r,rg=r*q['fgamma'],rn=r*(1-q['fgamma']),
               w=w,rho=rho,h2=h2,h=h,c=c,Q=Q,g=Series.monomial(-3,g0),
               q=Series.monomial(-1,q0),Hd=-b-Fraction(4,3)*r-w,cd=h*c.derivative(),
               hr=hr,qi=qi,parameters=q,g0=g0,q0=q0,
               transcendental_strings=dict(norm=norm_text,log_alpha_over_qinf=log_text))
    ans['Qd'] = h*Q.derivative()
    ans['rb'] = 3*b/(4*ans['rg'])
    return ans

def unknown_series(layout):
    fields = []
    inventory = []
    for i,power in enumerate(layout.powers):
        entries = {}
        for n in range(HALO+1):
            for log in range(LOGDEG+1):
                col = ((n*(LOGDEG+1)+log)*394+i)
                entries[power+n,log] = Linear({col:Field(1)})
                inventory.append(dict(column=col,var=i,name=layout.names[i],relative_order=n,log_degree=log))
        fields.append(Series(entries))
    require(len(inventory) == 8274 and len({x['column'] for x in inventory}) == 8274, 'Entire U0..U6/log0..2 census')
    return fields,sorted(inventory,key=lambda x:x['column'])

def stable_formal_operator(y,bg,layout,nodes,weights,omega):
    """Independent literal stable rows, with exact current/slip range separation."""
    KB,C,CBAR = Fraction(1,50),Fraction(99,50),Fraction(99,100)
    h,b,rg,rn,w,c,Q,q,g,rb = (bg[k] for k in ('h','b','rg','rn','w','c','Q','q','g','rb'))
    R,Gb,U,Gg,W,Gn,wn,Gamma,V = y[:9]
    B,G = b,Fraction(4,3)*rg
    wb = U-G/(B+G)*W
    wg = U+B/(B+G)*W
    S = (B+G)*U+Fraction(4,3)*rn*wn
    Rd = S+h*c*Gamma
    psi = R-h*V
    shear = rg*y[layout.fg[2]]+rn*y[layout.fn[2]]
    phi = psi-2*shear/(q*q)
    Z = sum((weights[i]*y[j] for i,j in enumerate(layout.z)),Series())
    Zd = sum((weights[i]*y[j] for i,j in enumerate(layout.zd)),Series())
    freqs = [omega*node for node in nodes]
    aw = sum(weights[i]*freqs[i]**2 for i in range(NS))
    R1 = sum((weights[i]*freqs[i]**2*y[j] for i,j in enumerate(layout.z)),Series())
    L = Q*q
    Ld = -h*(1+3*c)*L
    Ldd = (h*h*(1+3*c)**2-bg['Hd']*(1+3*c)-3*h*bg['cd'])*L
    v = Z/L
    vd = (Zd-Ld*v)/L
    n,sigma = y[layout.n],y[layout.sigma]
    Bq = 1+(q*bg['parameters']['ell_native'])**2
    Delta = aw+C*Q*Q/KB+CBAR*Q*Q*q*q*c/w
    Fv = -h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cd']*Gamma+c*(3*Rd-q*q*V)
    sigma_numerator = L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-aw*q*n
    out = [Series() for _ in range(394)]
    out[0] = Rd
    out[1] = 3*Rd-q*q*(V+wb)
    out[2] = G/(B+G)*(h*U+Gg/4-y[layout.fg[2]]/2)-c*Gamma
    out[3] = 4*Rd-Fraction(4,3)*q*q*(V+wg)
    out[4] = h*wg+Gg/4-y[layout.fg[2]]/2-g*(1+1/rb)*W
    out[5] = 4*Rd-Fraction(4,3)*q*q*(V+wn)
    out[6] = h*wn+Gn/4-y[layout.fn[2]]/2-c*Gamma
    out[7] = 3*Rd-q*q*V-CBAR*Q*q*sigma/w
    out[8] = phi+c*Gamma
    Pi = y[layout.fg[2]]+y[layout.pol[0]]+y[layout.pol[2]]
    for indices,velocity,collision in ((layout.fg,V+wg,g),(layout.fn,V+wn,Series())):
        for l,i in indices.items():
            previous = Fraction(4,3)*q*velocity if l == 2 else y[indices[l-1]]
            following = y[indices[l+1]] if l < max(indices) else Series()
            out[i] = q*(l*previous-(l+1)*following)/Fraction(2*l+1)-collision*y[i]
            if l == 2 and collision.v:
                out[i] += collision*Pi/10
    for l,i in layout.pol.items():
        previous = y[layout.pol[l-1]] if l else Series()
        following = y[layout.pol[l+1]] if l < LG else Series()
        out[i] = q*(l*previous-(l+1)*following)/Fraction(2*l+1)-g*y[i]
        if l in (0,2):
            out[i] += g*Pi*(Fraction(1,2) if l == 0 else Fraction(1,10))
    for i,(z,zd) in enumerate(zip(layout.z,layout.zd)):
        out[z] = y[zd]
        out[zd] = -3*h*y[zd]-freqs[i]**2*(Bq*y[z]-q*n-sigma)
    # Proper algebraic rows retain exact residual scaling, not a new ODE.
    out[layout.n] = n-vd+c*Gamma
    out[layout.sigma] = sigma-sigma_numerator/Delta
    return out,dict(wb=wb,wg=wg,S=S,Rd=Rd,psi=psi,phi=phi,shear=shear,Z=Z,Zd=Zd,
        L=L,Ld=Ld,Ldd=Ldd,v=v,vd=vd,n=n,sigma=sigma,Delta=Delta,
        aw=aw,R1=R1,P=KB*q*n/2+CBAR*Z,freqs=freqs)

def coefficient_rows(y,out,bg,layout):
    rows,meta = [],[]
    for i in range(394):
        residual = y[i].derivative()-out[i]/bg['h'] if i < 392 else out[i]
        p0 = layout.powers[i]
        for n in range(-2,NREL+1):
            for log in range(LOGDEG+2):
                value = residual.v.get((p0+n,log),Linear())
                value = value if isinstance(value,Linear) else Linear({-1:value})
                rows.append(value.v.copy())
                meta.append(dict(var=i,name=layout.names[i],relative_order=n,log_degree=log,
                                 role='descriptor' if i < 392 else 'reaction'))
        require(not any(p < p0-2 and bool(x) for (p,l),x in residual.v.items()), 'Full negative-band census')
        require(not any(p0-2 <= p <= p0+NREL and l > LOGDEG+1 and bool(x)
                        for (p,l),x in residual.v.items()), 'Unsupported retained logarithm; no discarded coefficient')
    # No logarithmic leading amplitude; all other no-incoming/entropy rules
    # are explicit leading powers, not a post-solve residual branch choice.
    for log in range(LOGDEG+1):
        col = log*394
        rows.append({col:Field(1),-1:Field(-Fraction('1e-5'))} if log == 0 else {col:Field(1)})
        meta.append(dict(var=0,name='R',relative_order=0,log_degree=log,role='predeclared_curvature'))
    return rows,meta

def sparse_eliminate(rows,inventory):
    """Exact sparse field elimination; tail/mode columns precede small core."""
    def priority(col):
        d = inventory[col]
        name = d['name']
        group = 0 if name.startswith(('F_gamma_','G_gamma_','F_nu_')) else 1 if name.startswith(('z_','zd_')) else 2
        return (group,-d['var'] if group == 0 else d['var'],d['relative_order'],d['log_degree'])
    active = [dict(r) for r in rows]
    adjacency = {}
    for rid,row in enumerate(active):
        for col in row:
            if col >= 0:
                adjacency.setdefault(col,set()).add(rid)
    pivots,proof = [],[]
    for col in sorted(range(len(inventory)),key=priority):
        if col not in adjacency:
            continue
        candidates = adjacency[col]
        rid = min(candidates,key=lambda j:(len(active[j]),j))
        row = active[rid]
        pivot = row[col]
        require(bool(pivot), 'Exact sparse nonzero pivot')
        inv = pivot.inverse()
        row = {c:x*inv for c,x in row.items() if c != col}
        touched = sorted(candidates-{rid})
        for j in touched:
            target = active[j]
            factor = target.pop(col)
            for c,x in row.items():
                old = target.get(c,Field(0))
                new = old-factor*x
                if new:
                    target[c] = new
                    if c >= 0 and not old:
                        adjacency.setdefault(c,set()).add(j)
                elif c in target:
                    del target[c]
                    if c >= 0:
                        adjacency[c].discard(j)
        for c in active[rid]:
            if c >= 0:
                adjacency[c].discard(rid)
        del adjacency[col]
        for c in list(adjacency):
            if not adjacency[c]:
                del adjacency[c]
        active[rid] = {}
        pivots.append((col,row))
        proof.append(dict(column=col,row=rid,pivot=pivot.encode(),support=len(row),eliminated_rows=len(touched)))
    require(not adjacency, 'Complete sparse column elimination')
    inconsistent = [dict(row=j,constant=r[-1].encode()) for j,r in enumerate(active) if r.get(-1)]
    pivot_columns = {c for c,row in pivots}
    free = sorted(set(range(len(inventory)))-pivot_columns)
    affine = {col:Linear({col:Field(1)}) for col in free}
    for col,row in reversed(pivots):
        val = Linear({-1:-row.get(-1,Field(0))})
        for other,x in row.items():
            if other >= 0:
                require(other in affine, 'Exact reverse sparse dependency')
                val -= affine[other]*x
        affine[col] = val
    retained_free = []
    for col,d in enumerate(inventory):
        if d['relative_order'] <= NREL:
            retained_free.extend((col,k) for k in affine[col].v if k >= 0)
    # Remaining halo coordinates are not selected physical incoming states.
    # Zero is only a canonical representative after exact retained independence.
    return dict(affine=affine,free=free,retained_free=retained_free,
                pivots=proof,rank=len(pivots),equations=len(rows),left_null_incompatibility=inconsistent)

def substitute(series,answer):
    entries = {}
    for key,value in series.v.items():
        if isinstance(value,Linear):
            out = Field(value.v.get(-1,Field(0)))
            for col,coef in value.v.items():
                if col >= 0:
                    out += coef*answer[col]
        else:
            out = value
        entries[key] = out
    return Series(entries)

def preparation_controls(values,bg,layout,f,weights,nodes,omega):
    """Uncanceled independent normal/Euler/trace and source identities."""
    h,b,rg,rn,w,c,Q,q = (bg[k] for k in ('h','b','rg','rn','w','c','Q','q'))
    R,Gb,U,Gg,W,Gn,wn,Gamma,V = values[:9]
    wb,wg = f['wb'],f['wg']
    dot = lambda v:h*v.derivative()
    psi,phi,P = f['psi'],f['phi'],f['P']
    psid = dot(psi)
    phid = dot(phi)
    normal_terms = [q*q*psi,3*h*f['S'],b*Gb,rg*Gg,rn*Gn,w*Gamma,-q*P]
    trace_terms = [dot(psid),h*phid,3*h*psid,(2*bg['Hd']+3*h*h)*phi,
                   q*q*(psi-phi)/3,-c*w*(Gamma-3*h*V),
                   -(rg*(Gg-4*h*V)+rn*(Gn-4*h*V))/3]
    euler_terms = [dot(P),2*h*P,Fraction(99,100)*Q*values[layout.sigma]]
    rawmom = f['S']+(b+Fraction(4,3)*(rg+rn)+w)*V
    momentum_terms = [psid,h*phi,-rawmom]
    Eb = b*(Gb+3*h*wb)
    Er = rg*(Gg+4*h*wg)+rn*(Gn+4*h*wn)
    Ec = w*Gamma
    Ep = -q*P
    force_terms = [-q*q*phi,-Eb,-Er,-Ec,-Ep,-2*f['shear']]
    lens_terms = [-q*q*(phi+psi)/2,-Eb,-Er,-Ec,-Ep,-f['shear']]
    phase_terms = [dot(Ec),3*h*Ec,-3*w*dot(R),3*h*c*w*Gamma,w*q*q*V,
                   Fraction(99,100)*Q*q*values[layout.sigma]]
    baryon_terms = [dot(wb),c*Gamma,-bg['g']/bg['rb']*(wg-wb)]
    return dict(normal=normal_terms,proper_trace=trace_terms,omitted_normal_Euler=euler_terms,
                momentum=momentum_terms,force_plus_normal=force_terms+normal_terms,
                lens_plus_normal=lens_terms+normal_terms,phase_work=phase_terms,baryon_Euler=baryon_terms)

def raw_formal_operator(y,bg,layout,nodes,weights,omega):
    """Independent original-coordinate generator, including actual chart contacts."""
    KB,C,CBAR = Fraction(1,50),Fraction(99,50),Fraction(99,100)
    h,b,rg,rn,w,c,Q,q,g,rb = (bg[k] for k in ('h','b','rg','rn','w','c','Q','q','g','rb'))
    psi,db,ub,dg,ug,dn,un,d,V = y[:9]
    phi = psi-2*(rg*y[layout.fg[2]]+rn*y[layout.fn[2]])/(q*q)
    mom = b*ub+Fraction(4,3)*rg*ug+Fraction(4,3)*rn*un+w*V
    psid = mom-h*phi
    Gamma = d+3*h*V
    Vd = phi+c*Gamma
    Z = sum((weights[i]*y[j] for i,j in enumerate(layout.z)),Series())
    Zd = sum((weights[i]*y[j] for i,j in enumerate(layout.zd)),Series())
    freqs = [omega*node for node in nodes]
    aw = sum(weights[i]*freqs[i]**2 for i in range(NS))
    R1 = sum((weights[i]*freqs[i]**2*y[j] for i,j in enumerate(layout.z)),Series())
    L = Q*q
    Ld = -h*(1+3*c)*L
    Ldd = (h*h*(1+3*c)**2-bg['Hd']*(1+3*c)-3*h*bg['cd'])*L
    v = Z/L
    vd = (Zd-Ld*v)/L
    n,sigma = y[392],y[393]
    Bq = 1+(q*bg['parameters']['ell_native'])**2
    Delta = aw+C*Q*Q/KB+CBAR*Q*Q*q*q*c/w
    Fv = -h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cd']*Gamma+c*(3*psid-q*q*V+3*bg['Hd']*V+3*h*Vd)
    numerator = L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-aw*q*n
    out = [Series() for _ in range(394)]
    out[:9] = [psid,3*psid-q*q*ub,phi+g/rb*(ug-ub),
               4*psid-Fraction(4,3)*q*q*ug,h*ug+phi+dg/4-y[layout.fg[2]]/2+g*(ub-ug),
               4*psid-Fraction(4,3)*q*q*un,h*un+phi+dn/4-y[layout.fn[2]]/2,
               3*psid-q*q*V-CBAR*Q*q*sigma/w,Vd]
    Pi = y[layout.fg[2]]+y[layout.pol[0]]+y[layout.pol[2]]
    for indices,velocity,collision in ((layout.fg,ug,g),(layout.fn,un,Series())):
        for l,i in indices.items():
            before = Fraction(4,3)*q*velocity if l == 2 else y[indices[l-1]]
            after = y[indices[l+1]] if l < max(indices) else Series()
            out[i] = q*(l*before-(l+1)*after)/Fraction(2*l+1)-collision*y[i]
            if l == 2 and collision.v:
                out[i] += collision*Pi/10
    for l,i in layout.pol.items():
        before = y[layout.pol[l-1]] if l else Series()
        after = y[layout.pol[l+1]] if l < LG else Series()
        out[i] = q*(l*before-(l+1)*after)/Fraction(2*l+1)-g*y[i]
        if l in (0,2):
            out[i] += g*Pi*(Fraction(1,2) if l == 0 else Fraction(1,10))
    for i,(z,zd) in enumerate(zip(layout.z,layout.zd)):
        out[z] = y[zd]
        out[zd] = -3*h*y[zd]-freqs[i]**2*(Bq*y[z]-q*n-sigma)
    out[392],out[393] = n-vd+c*Gamma,sigma-numerator/Delta
    return out

SEALS,CREATED = {},{}
SOURCE_SHA,MANIFEST_SHA = None,None

def canonical(value):
    def finite(x):
        if x is None or type(x) in (str,int,bool):
            return
        if type(x) is float:
            require(math.isfinite(x), 'Finite native serialized scalar')
            return
        if isinstance(x,list):
            for item in x:
                finite(item)
            return
        if isinstance(x,dict):
            require(all(type(k) is str for k in x), 'Native JSON string keys')
            for item in x.values():
                finite(item)
            return
        raise AssertionError('Unsupported canonical serialization type')
    finite(value)
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def seal(path,digest):
    path = Path(path).resolve()
    compiler = Path('/usr/bin/clang').resolve()
    require(path.is_relative_to(BASE.parent.parent) or
            (path == compiler and digest == '179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'),
            'Owned input or exact inherited read-only compiler bytes; no build')
    require(sha(path) == digest, 'Actual input bytes '+str(path))
    require(str(path) not in SEALS or SEALS[str(path)] == digest, 'Consistent input seal')
    SEALS[str(path)] = digest

def recheck():
    require(SOURCE_SHA is not None and sha(__file__) == SOURCE_SHA, 'Frozen own source')
    for path,digest in dict(SEALS,**CREATED).items():
        require(sha(path) == digest, 'Preserved sealed input/output '+path)

def write(name,value):
    data = canonical(value)
    path = BASE/name
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o444)
    CREATED[str(path)] = sha(path)
    return CREATED[str(path)]

def parent_authentication():
    for name,digest in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():
        seal(BASE/name,digest)
    stem = 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001'
    result,receipt,manifest = (read(BASE/(stem+suffix)) for suffix in ('_RESULT.json','_RECEIPT.json','_MANIFEST.json'))
    require(result['lineage'] == manifest and receipt['input_sha256'] == manifest['inputs']
            and receipt['source_sha256'] == PINS['constrained_u_common_boundary_comoving_chart_v001.py']
            and receipt['result_sha256'] == PINS[stem+'_RESULT.json']
            and receipt['status'] == result['status'], 'Full completed physical parent binding')
    require(len(result['numerical_gates']) == 306 and all(x['passed'] for x in result['numerical_gates'])
            and len(result['chart_gates']) == 84 and sum(x['passed'] for x in result['chart_gates']) == 56,
            'Preserve actual306 PASS and28 chart-contact failures')
    for key in ('input_sha256','output_sha256'):
        for path,digest in receipt[key].items():
            seal(path,digest)
    seal(BASE/(stem+'_MANIFEST.json'),receipt['manifest_sha256'])
    seal(BASE/(stem+'_JOURNAL.jsonl'),receipt['journal_sha256'])
    events = [json.loads(line) for line in (BASE/(stem+'_JOURNAL.jsonl')).read_text().splitlines()]
    require([x['event'] for x in events] == ['OWNER_START']+['CHECKPOINT']*28+['OWNER_COMPLETE'],
            'Full28-pair natural parent closure')
    require(events[-1]['result_sha256'] == receipt['result_sha256'], 'Parent exact terminal result')
    names = set()
    for event in events:
        require(event['owner'] == 'root' and event['source_sha256'] == receipt['source_sha256']
                and event['manifest_sha256'] == receipt['manifest_sha256'], 'Parent root/source epoch')
        if event['event'] != 'CHECKPOINT':
            continue
        payload = BASE/event['payload']
        commit = BASE/(event['payload'][:-5]+'_COMMIT.json')
        require(str(payload) in SEALS and str(commit) in SEALS, 'Committed parent already in full receipt')
        seal(payload,event['sha256'])
        seal(commit,event['commit_sha256'])
        p,c = read(payload),read(commit)
        require(payload.read_bytes() == canonical(p) and commit.read_bytes() == canonical(c), 'Entire canonical parent pair')
        require(c['payload'] == payload.name and c['sha256'] == event['sha256']
                and c['owner'] == p['owner'] == 'root' and c['pid'] == p['pid'] == event['pid']
                and c['source_sha256'] == p['source_sha256'] == receipt['source_sha256']
                and c['lineage'] == p['lineage'] == manifest, 'Complete parent pair identity')
        names.update((payload.name,commit.name))
    require({p.name for p in BASE.glob(stem+'_*CP*.json')} == names, 'Exact full parent checkpoint prefix')
    require(manifest['ns'] == NS and manifest['lg'] == LG and manifest['ln'] == LN
            and manifest['k'] == .01 and manifest['curvature'] == 1e-5, 'Unchanged392-mode physical census')
    runs = result['runs']
    require(len(runs) == 4 and all(len(r['snodes']) == len(r['weights']) == NS for r in runs), 'Actual saved mode nodes/weights')
    nodes,weights = runs[0]['snodes'],runs[0]['weights']
    require(all(r['snodes'] == nodes and r['weights'] == weights for r in runs), 'One literal spectral chart')
    require(all(0 < x < 1 for x in nodes) and all(x > 0 for x in weights), 'Positive admitted spectrum')
    atomic = 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002'
    ar,ac = read(BASE/(atomic+'_RESULT.json')),read(BASE/(atomic+'_RECEIPT.json'))
    require(ar['status'] == ac['status'] == 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS'
            and ac['result_sha256'] == PINS[atomic+'_RESULT.json']
            and len(ar['numerical_gates']) == 12 and all(g['passed'] for g in ar['numerical_gates']),
            'Actual BBN-helium atomic fixture retained')
    for path,digest in ac['lineage']['input_sha256'].items():
        seal(path,digest)
    for path,digest in ac['output_sha256'].items():
        seal(path,digest)
    thermal_name = atomic+'_HALF_OUTPUT.json'
    require(str(BASE/thermal_name) in SEALS, 'Consumed physical thermal metadata is sealed')
    thermal = read(BASE/thermal_name)
    require(thermal['YHe_atomic'] == .24445561896834236 and thermal['H_grid_last_z'] == 7999.96221370981,
            'Unchanged actual BBN/terminal table metadata; the admitted ionized branch starts at z8000')
    return dict(fixed=manifest['fixed'],thermal=thermal,nodes=nodes,weights=weights,
                original_numerical_gates=result['numerical_gates'],original_chart_gates=result['chart_gates'])

def coefficient_array(series,power):
    return [[series.v.get((power+n,l),Field(0)).encode() for l in range(LOGDEG+1)] for n in range(HALO+1)]

def add_zero_controls(controls,name,terms,base,mp,low=-2,high=NREL):
    """Every signed coefficient and sum of uncanceled constituent magnitudes."""
    total = sum(terms,Series())
    require(not any(base+low <= p <= base+high and l > LOGDEG+1 and bool(x)
                    for (p,l),x in total.v.items()), 'Unsupported retained physical/control logarithm')
    for n in range(low,high+1):
        for log in range(LOGDEG+2):
            key = base+n,log
            value = total.v.get(key,Field(0))
            require(isinstance(value,Field), 'Solved coefficient field')
            scale = sum(abs(x.v.get(key,Field(0)).evaluate(mp)) for x in terms)
            residual = abs(value.evaluate(mp))
            floor = mp.mpf('1e-4000')
            error = residual/max(scale,floor)
            controls.append(dict(name=name,relative_order=n,log_degree=log,
                role='decomposition_identity' if name in ('force_plus_normal','lens_plus_normal') else 'independent_coefficient_control',
                signed_residual=mp.nstr(value.evaluate(mp),40),operation_scale=mp.nstr(scale,40),
                error=mp.nstr(error,40),tolerance='2e-11',passed=bool(error <= mp.mpf('2e-11')),
                exact_rationalized_zero=not bool(value)))

def solve_case(parent,digits,omega_text,mp):
    layout = Layout()
    bg = formal_background(parent['fixed'],parent['thermal'],digits,mp)
    nodes = [Field(exact_input(x)) for x in parent['nodes']]
    weights = [Field(exact_input(x)) for x in parent['weights']]
    # The literal saved quadrature weights are not silently renormalized.
    # Their exact binary sum is saved and used in every owned mode row.
    omega = Field(Fraction(omega_text))
    y,inventory = unknown_series(layout)
    out,f = stable_formal_operator(y,bg,layout,nodes,weights,omega)
    rows,row_metadata = coefficient_rows(y,out,bg,layout)
    solved = sparse_eliminate(rows,inventory)
    if solved['retained_free'] or solved['left_null_incompatibility']:
        raise CoefficientRefusal('Complete negative-band prepared block is incompatible or retains physical/halo freedom',
            dict(digits=digits,omega=omega_text,inventory=inventory,row_metadata=row_metadata,
                 parameters={k:[str(v.numerator),str(v.denominator)] for k,v in bg['parameters'].items()},
                 background={k:v.encode() for k,v in bg.items() if isinstance(v,Series)},
                 field_radicands=[[str(v.numerator),str(v.denominator)] for v in Field.rad],
                 sparse_equation_rows=[[[col,x.encode()] for col,x in sorted(row.items())] for row in rows],
                 pivots=solved['pivots'],rank=solved['rank'],null_columns=solved['free'],
                 retained_free=solved['retained_free'],left_null_incompatibility=solved['left_null_incompatibility'],
                 full_affine_witnesses=[[col,val.encode()] for col,val in sorted(solved['affine'].items())],
                 coefficient_seed_qualified=False))
    answer = {col:value.v.get(-1,Field(0)) for col,value in solved['affine'].items()}
    values = [substitute(v,answer) for v in y]
    derived = {key:substitute(v,answer) if isinstance(v,Series) else v for key,v in f.items()}
    solved_out,_ = stable_formal_operator(values,bg,layout,nodes,weights,omega)
    controls = []
    for i in range(394):
        terms = [values[i].derivative(),-solved_out[i]/bg['h']] if i < 392 else [solved_out[i]]
        add_zero_controls(controls,'descriptor_'+layout.names[i],terms,layout.powers[i],mp)
    # Independent physical source/contact rows are checked without dividing
    # by a tiny species source or discarding anisotropic radiation.
    physics = preparation_controls(values,bg,layout,derived,weights,nodes,omega)
    physical_base = dict(normal=-2,proper_trace=-4,omitted_normal_Euler=2,momentum=-2,
                         force_plus_normal=-2,lens_plus_normal=-2,phase_work=-3,baryon_Euler=2)
    for name,terms in physics.items():
        add_zero_controls(controls,name,terms,physical_base[name],mp)
    charge = bg['qbar']*bg['qbar']+(Series.monomial(3)/bg['parameters']['alpha'])*(bg['qbar']**3-bg['qbar'])-(1+bg['parameters']['eps'])
    add_zero_controls(controls,'charge_cubic',[charge],0,mp,0,6)
    add_zero_controls(controls,'background_Hdot',[bg['h']*bg['h'].derivative(),-bg['Hd']],-4,mp,0,6)
    add_zero_controls(controls,'background_Qdot',[bg['Qd'],3*bg['h']*bg['c']*bg['Q']],1,mp,0,6)
    # Exact leading controls are stated before coefficient outcomes.
    p = bg['parameters']
    hr,qi,q0 = bg['hr'],bg['qi'],Field(bg['q0'])
    Rstar = Field(Fraction('1e-5'))
    Rnu = Field(1-p['fgamma'])
    A = Rstar/(Fraction(3,2)+Fraction(2,5)*Rnu)
    c3 = Field(1)/(Field(p['norm']*p['d0'])*qi)
    Qc = qi*p['Q0_over_Hstar']
    L0 = Qc*q0
    aw = derived['aw']
    Delta0 = aw+Fraction(99,1)*Qc*Qc
    gp2 = -q0*q0*Rstar/(4*hr*hr)
    sigma2 = 6*hr*L0*c3*gp2/Delta0
    V2 = A/(2*hr)
    photon3 = 32*q0*q0*V2/(45*Field(bg['g0']))
    m = Field(p['OB'])/p['OR']+Field(p['OA']*p['d0']/p['OR'])*qi
    photon_shear1 = Fraction(16,15)*(1-Rnu)*hr*A/Field(bg['g0'])
    phi1 = (-m*A/4+Fraction(2,3)*Rnu*m*A-3*photon_shear1)/(4+Fraction(8,15)*Rnu)
    psi1 = -m*A/12-phi1/3
    r0 = Fraction(3,4)*Field(p['OB'])/(Field(p['OR'])*Field(p['fgamma']))
    witnesses = {
        'R0':(values[0],0,Rstar),
        'R2':(values[0],2,-q0*q0*A*(5+4*Rnu)/(120*hr*hr)),
        'Gamma_b2':(values[1],2,gp2),
        'Gamma_gamma2':(values[3],2,Fraction(4,3)*gp2),
        'Gamma_nu2':(values[5],2,Fraction(4,3)*gp2),
        'Gamma_phi2':(values[7],2,gp2),
        'U4':(values[2],4,-q0*q0*Rstar/(36*hr**3)),
        'wn4':(values[6],4,-q0*q0*Rstar/(36*hr**3)-q0*q0*A/(45*hr**3)),
        'sigma2':(values[393],2,sigma2),
        'n5':(values[392],5,-99*Qc*Qc*c3*gp2/Delta0),
        'W6':(values[4],6,-r0*q0*q0*Rstar/(9*Field(bg['g0'])*hr*hr)),
        'Phi0':(derived['phi'],0,A),'Psi0':(derived['psi'],0,A*(1+Fraction(2,5)*Rnu)),
        'Phi1_finite_opacity':(derived['phi'],1,phi1),'Psi1_finite_opacity':(derived['psi'],1,psi1),
        'Fgamma23':(values[layout.fg[2]],3,photon3),
        'Ggamma03':(values[layout.pol[0]],3,Fraction(5,4)*photon3),
        'Ggamma23':(values[layout.pol[2]],3,photon3/4),
        'Ggamma15':(values[layout.pol[1]],5,q0*photon3/(4*Field(bg['g0'])))}
    for i in range(NS):
        z6 = omega*omega*nodes[i]*nodes[i]*sigma2/(42*hr*hr)
        witnesses['z6_'+str(i)] = values[layout.z[i]],6,z6
        witnesses['zd4_'+str(i)] = values[layout.zd[i]],4,6*hr*z6
    for name,(series,power,expected) in witnesses.items():
        actual = Series({(0,log):value for (p,log),value in series.v.items() if p == power})
        add_zero_controls(controls,'leading_'+name,[actual,Series.scalar(-expected)],0,mp,0,0)
    outputs = values.copy()
    outputs[2],outputs[4] = derived['wb'],derived['wg']
    output_powers = layout.powers.copy()
    output_powers[4] = 4
    output_names = layout.names.copy()
    output_names[2],output_names[4] = 'w_b','w_gamma'
    raw_values = values.copy()
    h,V = bg['h'],values[8]
    raw_values[:9] = [derived['psi'],values[1]-3*h*V,V+derived['wb'],values[3]-4*h*V,V+derived['wg'],
                     values[5]-4*h*V,V+values[6],values[7]-3*h*V,V]
    raw_rhs = raw_formal_operator(raw_values,bg,layout,nodes,weights,omega)
    raw_powers = [0,0,2,0,2,0,2,0,2]+layout.powers[9:]
    for i in range(394):
        terms = [raw_values[i].derivative(),-raw_rhs[i]/bg['h']] if i < 392 else [raw_rhs[i]]
        add_zero_controls(controls,'raw_chart_contact_'+layout.names[i],terms,raw_powers[i],mp)
    require(len(controls) == 22704, 'Prospective exact control census')
    return dict(digits=digits,omega=omega_text,parameters={k:[str(v.numerator),str(v.denominator)] for k,v in p.items()},
        field_radicands=[[str(v.numerator),str(v.denominator)] for v in Field.rad],
        transcendental_strings=bg['transcendental_strings'],
        exact_weight_sum=sum(weights,Field(0)).encode(),
        background={k:v.encode() for k,v in bg.items() if isinstance(v,Series)},
        internal_names=layout.names,internal_powers=layout.powers,
        output_names=output_names,output_powers=output_powers,
        internal_coefficients=[coefficient_array(v,power) for v,power in zip(values,layout.powers)],
        output_coefficients=[coefficient_array(v,power) for v,power in zip(outputs,output_powers)],
        raw_powers=raw_powers,raw_coefficients=[coefficient_array(v,power) for v,power in zip(raw_values,raw_powers)],
        inventory=inventory,row_metadata=row_metadata,
        sparse_equation_rows=[[[col,value.encode()] for col,value in sorted(row.items())] for row in rows],
        pivot_witnesses=solved['pivots'],rank=solved['rank'],null_columns=solved['free'],
        exact_affine_null_witnesses=[[col,val.encode()] for col,val in sorted(solved['affine'].items()) if any(k >= 0 for k in val.v)],
        retained_halo_free=[],canonical_halo_representative='ZERO_ONLY_AFTER_EXACT_RETAINED_INDEPENDENCE',
        controls=controls,exact_transcendental_rank_qualified=False,
        rank_scope='Exact rank of this explicit rationalized-log biquadratic representation; symbolic or directed nonzero proof still required for uncertain transcendental physical-selection pivots')

def refinement_controls(cases,mp):
    controls = []
    for omega in OMEGAS:
        coarse,fine = (cases[(precision,omega)] for precision in PRECISIONS)
        require(coarse['rank'] == fine['rank'] and coarse['null_columns'] == fine['null_columns']
                and [p['column'] for p in coarse['pivot_witnesses']] == [p['column'] for p in fine['pivot_witnesses']],
                'Representation-dependent rank/halo: explicit refusal, no branch selection')
        require(coarse['output_names'] == fine['output_names'] and coarse['output_powers'] == fine['output_powers'], 'Identical complete output inventory')
        require(coarse['field_radicands'] == fine['field_radicands'], 'One calibrated algebraic chart')
        Field.configure(*(Fraction(int(n),int(d)) for n,d in fine['field_radicands']))
        mp.mp.dps = 150
        for i in range(394):
            for n in range(HALO+1):
                for log in range(LOGDEG+1):
                    a,b = (Field.decode(case['output_coefficients'][i][n][log]).evaluate(mp) for case in (coarse,fine))
                    scale = max(abs(a)+abs(b),mp.mpf('1e-4000'))
                    error = abs(a-b)/scale
                    controls.append(dict(name='coefficient80_vs120',omega=omega,var=i,name_field=fine['output_names'][i],
                        relative_order=n,log_degree=log,signed_difference=mp.nstr(a-b,50),scale=mp.nstr(scale,50),
                        error=mp.nstr(error,50),tolerance='2e-11',passed=bool(error <= mp.mpf('2e-11'))))
    require(len(controls) == 33096, 'Complete80/120 coefficient comparison census')
    return controls

def literal_binary_background(a,fixed):
    """Owned five-Newton binary evaluator, used only as a saved comparison."""
    eps,d0,OA,OB,OR,rG = (fixed[k] for k in ('eps','d0','OA','OB','OR','rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b,r = 1.5*OB/rG/a**3,1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    return dict(h=h,Q=fixed['Q0_over_Hstar']*qbar,c=cs,rho=rho,w=w,pex=pex,
                charge_error=abs(2*qbar*s/(eps*norm)/d-1))

def finite_diagnostics(case,fixed,mp):
    """All coordinates retained; J2/J4/casting diagnostics do not choose a seed."""
    Field.configure(*(Fraction(int(n),int(d)) for n,d in case['field_radicands']))
    mp.mp.dps = case['digits']+40
    out = []
    for start in ('1e-7','5e-8'):
        a,l = mp.mpf(start),mp.log(mp.mpf(start))
        rows = []
        for i,power in enumerate(case['output_powers']):
            values = {}
            for order in (2,4):
                value = sum(Field.decode(case['output_coefficients'][i][n][log]).evaluate(mp)
                            *a**(power+n)*l**log for n in range(order+1) for log in range(LOGDEG+1))
                values[order] = value
            cast = float(values[4])
            require(math.isfinite(cast), 'Finite casting overflow refusal')
            lifted = mp.mpf(Fraction(cast).numerator)/Fraction(cast).denominator
            rows.append(dict(var=i,name=case['output_names'][i],power=power,
                J2=mp.nstr(values[2],60),J4=mp.nstr(values[4],60),signed_J4_minus_J2=mp.nstr(values[4]-values[2],60),
                binary64=cast,signed_cast_error=mp.nstr(lifted-values[4],60),
                underflow=bool(values[4] != 0 and cast == 0),role='FINITE_CASTING_AND_TRUNCATION_DIAGNOSTIC_NOT_A_PREPARATION_GATE'))
        require(len(rows) == 394, 'Every physical/algebraic finite coordinate retained')
        literal = literal_binary_background(float(start),fixed)
        comparisons = []
        for name in ('h','Q','c','rho','w','pex'):
            formal = sum(Field.decode(coefficient).evaluate(mp)*a**power*l**log
                         for power,log,coefficient in case['background'][name])
            binary = mp.mpf(Fraction(literal[name]).numerator)/Fraction(literal[name]).denominator
            scale = max(abs(formal)+abs(binary),mp.mpf('1e-4000'))
            comparisons.append(dict(field=name,formal=mp.nstr(formal,60),literal_binary64=literal[name],
                signed_literal_minus_formal=mp.nstr(binary-formal,60),relative_operation_difference=mp.nstr(abs(binary-formal)/scale,60),
                role='LITERAL_BINARY_VS_FORMAL_SOURCE_DIAGNOSTIC_NOT_A_NEW_COEFFICIENT_OR_SEED_GATE'))
        out.append(dict(start=start,rows=rows,background_comparisons=comparisons,literal_charge_error=literal['charge_error'],
                        background_comparison_qualified=False,asymptotic_Rstar='1e-5',finite_normal_corrected=False,
                        cosmic_seed_qualified=False,source_history_qualified=False))
    return out

def event(kind,epoch,**extra):
    value = dict(event=kind,time=datetime.now(timezone.utc).isoformat(),owner='root',pid=os.getpid(),epoch=epoch,
                 source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**extra)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as stream:
        stream.write(canonical(value).decode())

def stage_names():
    return ['AUTH']+[f'P{digits}_W{omega}' for digits in PRECISIONS for omega in OMEGAS]+['SUMMARY']

def validate_case(case,digits,omega):
    expected_keys = {'digits','omega','parameters','field_radicands','transcendental_strings','exact_weight_sum','background',
        'internal_names','internal_powers','output_names','output_powers','internal_coefficients','output_coefficients',
        'raw_powers','raw_coefficients','inventory','row_metadata','sparse_equation_rows','pivot_witnesses','rank',
        'null_columns','exact_affine_null_witnesses','retained_halo_free','canonical_halo_representative','controls',
        'exact_transcendental_rank_qualified','rank_scope','finite_diagnostics'}
    require(set(case) == expected_keys, 'Entire coefficient payload schema; no partial case')
    require(case['digits'] == digits and case['omega'] == omega and len(case['inventory']) == 8274,
            'Exact prepared coefficient case identity')
    layout = Layout()
    expected_inventory = [dict(column=((n*3+log)*394+i),var=i,name=layout.names[i],relative_order=n,log_degree=log)
        for n in range(7) for log in range(3) for i in range(394)]
    expected_rows = [dict(var=i,name=layout.names[i],relative_order=n,log_degree=log,
        role='descriptor' if i < 392 else 'reaction') for i in range(394) for n in range(-2,5) for log in range(4)]
    expected_rows += [dict(var=0,name='R',relative_order=0,log_degree=log,role='predeclared_curvature') for log in range(3)]
    require(case['inventory'] == expected_inventory and case['row_metadata'] == expected_rows,
            'Entire exact coefficient/negative-band/log inventory and order')
    output_names,output_powers = layout.names.copy(),layout.powers.copy()
    output_names[2],output_names[4],output_powers[4] = 'w_b','w_gamma',4
    require(case['internal_names'] == layout.names and case['internal_powers'] == layout.powers
            and case['output_names'] == output_names and case['output_powers'] == output_powers
            and case['raw_powers'] == [0,0,2,0,2,0,2,0,2]+layout.powers[9:], 'Exact retained physical coordinate charts')
    require(len(case['internal_names']) == len(case['output_names']) == 394
            and len(case['internal_coefficients']) == len(case['output_coefficients']) == 394,
            'Full394 internal and output arrays')
    require(len(case['raw_coefficients']) == len(case['raw_powers']) == 394, 'Whole original-coordinate coefficients')
    for name in ('internal_coefficients','output_coefficients','raw_coefficients'):
        require(all(len(v) == 7 and all(len(row) == 3 for row in v) for v in case[name]), 'Complete U0..6/log0..2 axes')
        for v in case[name]:
            for row in v:
                for component in row:
                    Field.decode(component)
    require(len(case['row_metadata']) == len(case['sparse_equation_rows']) == 11035
            and len(case['controls']) == 22704 and case['retained_halo_free'] == [], 'Full equations/control/halo census')
    for row in case['sparse_equation_rows']:
        require(all(isinstance(v,list) and len(v) == 2 and type(v[0]) is int and -1 <= v[0] < 8274 for v in row),
                'Whole exact sparse equation schema')
        require([v[0] for v in row] == sorted(set(v[0] for v in row)), 'Canonical unique sparse columns')
        for column,value in row:
            require(bool(Field.decode(value)), 'No saved zero sparse coefficient')
    pivots = case['pivot_witnesses']
    require(case['rank'] == len(pivots) and 0 <= case['rank'] <= 8274
            and len({v['column'] for v in pivots}) == len(pivots), 'Complete unique exact pivot census')
    require(case['null_columns'] == sorted(set(range(8274))-{v['column'] for v in pivots}), 'Full complementary null columns')
    for pivot in pivots:
        require(set(pivot) == {'column','row','pivot','support','eliminated_rows'}
                and 0 <= pivot['column'] < 8274 and 0 <= pivot['row'] < 11035
                and bool(Field.decode(pivot['pivot'])), 'Exact nonzero pivot witness schema')
    for gate in case['controls']:
        require(set(gate) == {'name','relative_order','log_degree','role','signed_residual','operation_scale','error',
                            'tolerance','passed','exact_rationalized_zero'} and gate['tolerance'] == '2e-11'
                and type(gate['passed']) is bool and type(gate['exact_rationalized_zero']) is bool,
                'Full fixed arithmetic disposition schema')
    require(case['exact_transcendental_rank_qualified'] is False, 'No rationalized-log rank promotion')
    require([s['start'] for s in case['finite_diagnostics']] == ['1e-7','5e-8']
            and all([r['var'] for r in s['rows']] == list(range(394)) and len(s['background_comparisons']) == 6
                    and s['cosmic_seed_qualified'] is False and s['background_comparison_qualified'] is False
                    for s in case['finite_diagnostics']), 'Complete finite casting inventory and refusal scopes')

def validate_runtime(manifest,complete=False):
    journal = BASE/(STEM+'_JOURNAL.jsonl')
    require(journal.exists() and journal.stat().st_size > 0, 'Refuse missing/empty owner journal')
    events = [json.loads(line) for line in journal.read_text().splitlines()]
    stages = stage_names()
    prefix,files,cases = [],set(),{}
    current,epoch = None,-1
    for pos,e in enumerate(events):
        require(e['owner'] == 'root' and e['source_sha256'] == SOURCE_SHA and e['manifest_sha256'] == MANIFEST_SHA,
                'Entire source/root journal identity')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            require(e['epoch'] == epoch+1 and e['completed_prefix'] == len(prefix)
                    and (pos == 0) == (e['event'] == 'OWNER_START'), 'Exact root epoch/prefix transition')
            current,epoch = e['pid'],e['epoch']
            require(type(current) is int and current > 0, 'Current actual root PID')
            continue
        require(e['pid'] == current and e['epoch'] == epoch, 'Current owner epoch at every event')
        if e['event'] == 'FAILED':
            raise AssertionError('Scientifically failed prefix is immutable; a new reviewed attempt is required')
        if e['event'] == 'OWNER_COMPLETE':
            require(complete and pos == len(events)-1 and len(prefix) == len(stages), 'Exact final natural closure')
            result = read(BASE/(STEM+'_RESULT.json'))
            require(e['result_sha256'] == sha(BASE/(STEM+'_RESULT.json')) and e['status'] == result['status']
                    and e['checkpoint_count'] == 10 and e['control_count'] == len(result['controls']) == 214728
                    and result['manifest'] == manifest and result['exact_transcendental_rank_qualified'] is False,
                    'Exact natural result/status/count lineage')
            continue
        require(e['event'] == 'CHECKPOINT' and e['stage'] == stages[len(prefix)], 'Exact global ten-stage prefix')
        pn,cn = STEM+'_'+e['stage']+'_CP.json',STEM+'_'+e['stage']+'_CP_COMMIT.json'
        require(e['payload'] == pn and e['commit'] == cn, 'Declared immutable checkpoint namespace')
        p,c = read(BASE/pn),read(BASE/cn)
        require((BASE/pn).read_bytes() == canonical(p) and (BASE/cn).read_bytes() == canonical(c), 'Whole finite canonical checkpoint pair')
        require(sha(BASE/pn) == e['payload_sha256'] and sha(BASE/cn) == e['commit_sha256'], 'Whole checkpoint hashes')
        require(set(p) == {'stage','owner','pid','epoch','source_sha256','manifest_sha256','data'}
                and p['stage'] == e['stage'] and p['owner'] == 'root' and p['pid'] == current and p['epoch'] == epoch
                and p['source_sha256'] == SOURCE_SHA and p['manifest_sha256'] == MANIFEST_SHA, 'Full payload source/owner schema')
        require(c == dict(stage=e['stage'],owner='root',pid=current,epoch=epoch,source_sha256=SOURCE_SHA,
                         manifest_sha256=MANIFEST_SHA,payload=pn,payload_sha256=e['payload_sha256']), 'Exact entire commit')
        if e['stage'].startswith('P'):
            digits,omega = e['stage'][1:].split('_W')
            validate_case(p['data'],int(digits),omega)
            cases[int(digits),omega] = p['data']
        elif e['stage'] == 'AUTH':
            require(set(p['data']) == {'input_sha256','manifest'} and p['data']['input_sha256'] == SEALS
                    and p['data']['manifest'] == manifest, 'Whole authenticated stage inputs')
        else:
            require(p['data']['case_count'] == 8 and p['data']['coefficient_control_count'] == 181632
                    and p['data']['refinement_control_count'] == 33096, 'Exact full summary counts')
        for name in (pn,cn):
            CREATED[str(BASE/name)] = sha(BASE/name)
            files.add(name)
        prefix.append(e['stage'])
    actual = {p.name for p in BASE.glob(STEM+'_*CP*.json')}
    require(actual == files, 'Refuse orphan or unknown immutable checkpoint pairs')
    allowed = files|{STEM+'_MANIFEST.json',STEM+'_JOURNAL.jsonl'}
    if complete:
        allowed |= {STEM+'_RESULT.json',STEM+'_REPORT.md'}
    for path in BASE.glob(STEM+'_*'):
        if path.name in allowed:
            continue
        require(path.name.startswith(STEM+'_FAILED_') and path.suffix == '.json', 'Refuse unknown runtime namespace')
        err = read(path)
        require(err['source_sha256'] == SOURCE_SHA and err['input_sha256'] == SEALS, 'Preserved failed-source lineage')
        CREATED[str(path)] = sha(path)
    if complete:
        require(prefix == stages, 'All ten complete checkpoints')
    return prefix,cases,epoch

def checkpoint(stage,data,epoch):
    recheck()
    pn,cn = STEM+'_'+stage+'_CP.json',STEM+'_'+stage+'_CP_COMMIT.json'
    digest = write(pn,dict(stage=stage,owner='root',pid=os.getpid(),epoch=epoch,
                          source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,data=data))
    cd = write(cn,dict(stage=stage,owner='root',pid=os.getpid(),epoch=epoch,
                      source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,payload=pn,payload_sha256=digest))
    event('CHECKPOINT',epoch,stage=stage,payload=pn,payload_sha256=digest,commit=cn,commit_sha256=cd)

def main():
    global SOURCE_SHA,MANIFEST_SHA
    require(not UNLAUNCHABLE_AUTHOR_DRAFT and PROTOCOL_SHA != 'PENDING',
            'Incomplete author draft refuses all coefficient execution')
    require(not any((BASE/(STEM+suffix)).exists() for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json')),
            'Completed output namespace: refuse before any mutation')
    require(not list(BASE.glob(STEM+'_FAILED_*.json')), 'Failed prefix: refuse unchanged deterministic replay before mutation')
    SOURCE_SHA = sha(__file__)
    started = time.monotonic()
    parent = parent_authentication()
    mp = DecimalArithmetic()
    manifest = dict(source_sha256=SOURCE_SHA,input_sha256=SEALS.copy(),precisions=list(PRECISIONS),
        omegas=list(OMEGAS),relative_order=NREL,halo_order=HALO,log_degree=LOGDEG,
        physical_variables=392,reactions=2,unknown_coefficients=8274,equations_per_case=11035,
        case_count=8,coefficient_controls_per_case=22704,coefficient_controls=181632,
        refinement_controls=33096,total_controls=214728,checkpoint_stages=stage_names(),
        fixed=parent['fixed'],literal_nodes=parent['nodes'],literal_weights=parent['weights'],
        parameter_semantics='Calibrated binary64 values lifted exactly; structural KB=1/50,C=99/50,CBAR=99/100; exact saved weights without silent normalization; norm/log at80/120 explicit decimal-rational representations',
        preparation='Rstar1e-5; declared adiabatic/no-incoming power-log candidate, not an origin or finite-start qualification',
        rank_scope='Exact rationalized-log field witnesses only; exact-transcendental physical rank remains unqualified',
        arithmetic_engine=mp.__version__,physical_seed_qualified=False,background_through_annihilation_qualified=False)
    path = BASE/(STEM+'_MANIFEST.json')
    if path.exists():
        require(read(path) == manifest and path.read_bytes() == canonical(manifest), 'Identical full recovery manifest')
        MANIFEST_SHA = sha(path)
        CREATED[str(path)] = MANIFEST_SHA
        prefix,cases,old_epoch = validate_runtime(manifest)
        epoch = old_epoch+1
        event('OWNER_RESUME',epoch,completed_prefix=len(prefix))
    else:
        require(not list(BASE.glob(STEM+'_*')), 'Refuse every pre-manifest orphan')
        MANIFEST_SHA = write(STEM+'_MANIFEST.json',manifest)
        prefix,cases,epoch = [],{},0
        event('OWNER_START',epoch,completed_prefix=0)
    if not prefix:
        checkpoint('AUTH',dict(input_sha256=SEALS.copy(),manifest=manifest),epoch)
    for digits in PRECISIONS:
        for omega in OMEGAS:
            if (digits,omega) in cases:
                continue
            case = solve_case(parent,digits,omega,mp)
            case['finite_diagnostics'] = finite_diagnostics(case,parent['fixed'],mp)
            validate_case(case,digits,omega)
            checkpoint(f'P{digits}_W{omega}',case,epoch)
            cases[digits,omega] = case
            print(json.dumps(dict(precision=digits,omega=omega,rank=case['rank'],controls=len(case['controls']),
                                  exact_transcendental_rank_qualified=False,elapsed=time.monotonic()-started)),flush=True)
    refined = refinement_controls(cases,mp)
    controls = [dict(precision=digits,omega=omega,**g) for digits in PRECISIONS for omega in OMEGAS
                for g in cases[digits,omega]['controls']]+refined
    require(len(controls) == 214728, 'Exact complete prospective control census')
    failed = [g for g in controls if not g['passed']]
    status = 'FORMAL_COEFFICIENT_ARITHMETIC_PASS_ANALYTIC_RANK_UNQUALIFIED' if not failed else 'FORMAL_COEFFICIENT_ARITHMETIC_FAILED'
    summary = dict(status=status,case_count=8,coefficient_control_count=181632,refinement_control_count=33096,
                   total_controls=214728,failed_control_count=len(failed),physical_seed_qualified=False,
                   exact_transcendental_rank_qualified=False)
    if 'SUMMARY' not in prefix:
        checkpoint('SUMMARY',summary,epoch)
    else:
        require(read(BASE/(STEM+'_SUMMARY_CP.json'))['data'] == summary, 'Exact recomputed recovered summary and dispositions')
    recheck()
    result = dict(status=status,manifest=manifest,cases=[cases[d,o] for d in PRECISIONS for o in OMEGAS],
                  controls=controls,original_numerical_gates=parent['original_numerical_gates'],
                  original_chart_gates=parent['original_chart_gates'],physical_seed_qualified=False,
                  exact_transcendental_rank_qualified=False,elapsed_seconds=time.monotonic()-started)
    rh = write(STEM+'_RESULT.json',result)
    report = '# Full formal regular coefficient packet\n\n'+status+'; '+str(len(controls)-len(failed))+'/214728 arithmetic controls. '
    report += 'All392 physical variables, two reactions, eight full coefficient cases, negative-band/null witnesses and finite casting diagnostics are retained. '
    report += 'Rank refers to the explicit80/120 rationalized-log representations. Exact-transcendental rank, physical seed adequacy, cosmic preparation and observations remain unqualified.\n'
    rp = BASE/(STEM+'_REPORT.md')
    with rp.open('xb') as stream:
        stream.write(report.encode())
    rp.chmod(0o444)
    CREATED[str(rp)] = sha(rp)
    event('OWNER_COMPLETE',epoch,status=status,result_sha256=rh,checkpoint_count=10,control_count=214728)
    validate_runtime(manifest,complete=True)
    jp = BASE/(STEM+'_JOURNAL.jsonl')
    jp.chmod(0o444)
    CREATED[str(jp)] = sha(jp)
    recheck()
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,input_sha256=SEALS,
        output_sha256=CREATED.copy(),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),
        result_sha256=rh,checkpoint_count=10,control_count=214728))
    recheck()
    return 0 if not failed else 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    args = parser.parse_args()
    require(args.execute, 'Root only after full frozen independent review')
    try:
        raise SystemExit(main())
    except Exception as error:
        if MANIFEST_SHA is not None and not (BASE/(STEM+'_RESULT.json')).exists():
            import traceback
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
            name = STEM+'_FAILED_'+stamp+'.json'
            write(name,dict(owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,
                manifest_sha256=MANIFEST_SHA,input_sha256=SEALS,created=CREATED.copy(),traceback=traceback.format_exc(),
                refusal_details=getattr(error,'details',None)))
            # The current epoch is recovered from the actual final owner line.
            es = [json.loads(x) for x in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
            event('FAILED',es[-1]['epoch'],failure=name,failure_sha256=sha(BASE/name))
        raise
