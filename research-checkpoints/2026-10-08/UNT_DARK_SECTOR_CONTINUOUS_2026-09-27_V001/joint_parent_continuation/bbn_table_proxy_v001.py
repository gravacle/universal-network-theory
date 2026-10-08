"""Pinned BBN table proxy plus thermal-interface qualification; stdout only.
No PRIMAT import, nuclear/oscillator ODE, fitting, network or file writes.
"""
import bisect
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = HERE / "bbn_inputs_v001"
THERM = DATA / "primat_source_reference"
FREEZE = HERE / "BBN_TABLE_PROXY_V001_FROZEN.json"
CONFIG = dict(
    expected_rows=360, expected_table_rows=1300,
    local_rectangle=[.020, .024, 0., 3.],
    interpolation_allowance=dict(helium=2e-5, deuterium=5e-8),
    arithmetic_tolerance=2e-12, spline_tolerance=2e-10,
    polynomial_padding=2e-12, thermal_subdivisions=[4, 8],
    thermal_temperature_MeV=[.001, 40.],
    finite_gap_reference_temperature_MeV=.01,
    inherited_T0_K=2.72548, table_T0_K=2.7255,
    m_e_MeV=.51099895,
    k_B_J_K=1.380649e-23, eV_J=1.602176634e-19,
    method="local tensor cubic; bilinear theory marginal sigmas",
    conserved_scalar_abundance_status="NOT_YET_QUALIFIED",
)


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        path.relative_to(ROOT)
        h = sha(path)
        if expected is not None and h != expected:
            raise RuntimeError("Changed input: " + str(path))
        files[str(path.relative_to(ROOT))] = h
        return path

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, expected in json.loads(path.read_text())["files"].items():
            q = Path(name)
            candidates = set()
            for candidate in ([q] if q.is_absolute() else [ROOT / q, path.parent / q]):
                try:
                    candidate = candidate.resolve(strict=True)
                    candidate.relative_to(ROOT)
                except (ValueError, FileNotFoundError):
                    continue
                if candidate.is_file():
                    candidates.add(candidate)
            if len(candidates) != 1:
                raise RuntimeError("Ambiguous/missing manifest input " + name)
            q = add(candidates.pop(), expected)
            if q.name.endswith("_FROZEN.json"):
                manifest(q)

    def wrapped(name, expected):
        path = add(HERE / (name + "_RESULTS.json"), expected)
        old = json.loads(path.read_text())
        f = HERE / (name + "_FROZEN.json")
        manifest(f)
        if old["freeze_sha256"] != sha(f):
            raise RuntimeError("Old freeze differs")
        if old["payload_sha256"] != hashlib.sha256(encode(old["payload"])).hexdigest():
            raise RuntimeError("Old payload differs")
        return old["payload"]

    old = wrapped("FINITE_GAP_PHOTON_BUDGET_V001",
                  "23feee802337320fde647fe87ff3ff24b1006c935cc3f31d9cf6a4a9574dba10")
    cal = wrapped("GLOBAL_GAP_LIMIT_CALIBRATION_V001",
                  "11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628")
    if old["status"] != "COMPLETE" or old["failures"] or len(old["rows"]) != 360:
        raise RuntimeError("Incomplete inherited budget")
    add(DATA / "PRIMAT_Yp_DH_ErrorMC_1000_2026.dat",
        "48f864ecda028e7c7b4306c777bf694b9d3a214c920736894103d3163f7adec3")
    receipt = json.loads(add(THERM / "SOURCE_RECEIPT_V001.json").read_text())
    for member in receipt["files"]:
        q = add(THERM / member["name"], member["sha256"])
        if q.stat().st_size != member["bytes"]:
            raise RuntimeError("Snapshot byte count differs")
    for name in [Path(__file__).name, "BBN_TABLE_PROXY_PROTOCOL_V001.md",
                 "PRIMAT_2026_INTERFACE_AUDIT_V001.md",
                 "FINITE_GAP_BBN_DISCRIMINATOR_DESIGN_V001.md"]:
        add(HERE / name)
    obs = json.loads(add(DATA / "BBN_OBSERVATIONS_V001.json").read_text())
    return old, cal, obs, dict(configuration=CONFIG, files=files)


class Checks:
    def __init__(self):
        self.counts, self.maxima, self.failures = {}, {}, []

    def check(self, name, value, target=0., scale=1., tol=None, context=None):
        tol = CONFIG["arithmetic_tolerance"] if tol is None else tol
        err = abs(value - target) / max(abs(scale), 1e-300)
        self.counts[name] = self.counts.get(name, 0) + 1
        self.maxima[name] = max(self.maxima.get(name, 0.), err)
        if not math.isfinite(err) or err > tol:
            self.failures.append(dict(check=name, error=err, tolerance=tol, context=context))

    def yes(self, name, condition, context=None):
        self.check(name, int(bool(condition)), 1., context=context)


def rows(path, delimiter=None):
    return [[float(v) for v in s.split(delimiter)] for line in path.read_text().splitlines()
            if (s := line.strip()) and not s.startswith("#")]


def nodes(grid, x, degree=3, exclude=None):
    choices = [v for v in grid if v != exclude]
    if not choices[0] <= x <= choices[-1]:
        raise ValueError("No extrapolation")
    start = min(max(bisect.bisect_right(choices, x) - 1 - degree // 2, 0),
                len(choices) - degree - 1)
    return choices[start:start + degree + 1]


def lagrange(xs, x):
    scale = xs[-1] - xs[0]
    z = (x - xs[0]) / scale
    t = [(v - xs[0]) / scale for v in xs]
    return [math.prod((z - tj) / (ti - tj) for j, tj in enumerate(t) if j != i)
            for i, ti in enumerate(t)]


class AbundanceTable:
    def __init__(self):
        rr = rows(DATA / "PRIMAT_Yp_DH_ErrorMC_1000_2026.dat")
        self.raw = rr
        self.x = sorted({r[0] for r in rr})
        self.y = sorted({r[2] for r in rr})
        self.data = {(r[0], r[2]): r for r in rr}

    def sample(self, x, y, degree=3, omit_x=None, omit_y=None):
        xn, yn = nodes(self.x, x, degree, omit_x), nodes(self.y, y, degree, omit_y)
        wx, wy = lagrange(xn, x), lagrange(yn, y)
        return [math.fsum(wx[i] * wy[j] * self.data[(a, b)][c]
                         for i, a in enumerate(xn) for j, b in enumerate(yn))
                for c in range(8)]

    def qualify(self, ck):
        ck.yes("table_census", len(self.raw) == 1300 and len(self.x) == 52
               and len(self.y) == 25 and len(self.data) == 1300)
        withheld = []
        for r in self.raw:
            v = self.sample(r[0], r[2])
            for col in range(8):
                ck.check("table_node_recovery", v[col], r[col], max(abs(r[col]), 1e-30))
            if .020 <= r[0] <= .024 and 0. <= r[2] <= 3.:
                for label, ox, oy in [("baryon", r[0], None), ("radiation", None, r[2]),
                                      ("both", r[0], r[2])]:
                    p = self.sample(r[0], r[2], omit_x=ox, omit_y=oy)
                    err = dict(helium=p[4]-r[4], deuterium=p[6]-r[6])
                    for key in err:
                        ck.check("withheld_" + key, err[key],
                                 tol=CONFIG["interpolation_allowance"][key],
                                 context=[r[0], r[2], label])
                    withheld.append(dict(omega_b=r[0], Delta=r[2], omitted=label,
                                         signed_errors=err))
        for i in range(4):
            for j in range(4):
                xs, ys, x, y = [-2., -.1, .7, 3.], [-1., .2, 1.1, 4.], .23, .63
                got = math.fsum(a*b*xx**i*yy**j for a,xx in zip(lagrange(xs,x),xs)
                               for b,yy in zip(lagrange(ys,y),ys))
                ck.check("interpolation_polynomial", got, x**i*y**j)
        return withheld


# Small polynomial routines in a local t in [0,1]. No external spline library.
def padd(*terms):
    out = [0.] * max(len(p) for p in terms)
    for p in terms:
        for i,v in enumerate(p):
            out[i] += v
    return out


def pscale(p, c):
    return [c*v for v in p]


def pmul(p, q):
    out = [0.] * (len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            out[i+j] += a*b
    return out


def pder(p):
    return [i*p[i] for i in range(1, len(p))] or [0.]


def peval(p, x):
    return math.fsum(v*x**i for i,v in enumerate(p))


def pshift(p, a, b):
    out = [0.] * len(p)
    for j,v in enumerate(p):
        for i in range(j+1):
            out[i] += v*math.comb(j,i)*a**(j-i)*b**i
    return out


class Spline:
    """Independent standard not-a-knot cubic via second-derivative tridiagonal."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        h = [b-a for a,b in zip(x,x[1:])]
        n = len(x)
        lo, di, up, rhs = [], [], [], []
        for i in range(1,n-1):
            lo.append(h[i-1]);di.append(2*(h[i-1]+h[i]));up.append(h[i])
            rhs.append(6*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1]))
        di[0] += h[0]*(h[0]+h[1])/h[1]
        up[0] -= h[0]**2/h[1];lo[0] = 0.
        di[-1] += h[-1]*(h[-2]+h[-1])/h[-2]
        lo[-1] -= h[-1]**2/h[-2];up[-1] = 0.
        for i in range(1,n-2):
            f = lo[i]/di[i-1]
            di[i] -= f*up[i-1];rhs[i] -= f*rhs[i-1]
        mid = [0.]*(n-2)
        mid[-1] = rhs[-1]/di[-1]
        for i in range(n-4,-1,-1):
            mid[i] = (rhs[i]-up[i]*mid[i+1])/di[i]
        mm = [((h[0]+h[1])*mid[0]-h[0]*mid[1])/h[1]] + mid
        mm.append(((h[-2]+h[-1])*mid[-1]-h[-1]*mid[-2])/h[-2])
        self.c = [[y[i], y[i+1]-y[i]-h[i]**2*(2*mm[i]+mm[i+1])/6,
                   h[i]**2*mm[i]/2, h[i]**2*(mm[i+1]-mm[i])/6]
                  for i in range(n-1)]

    def coeff(self, a, b):
        i = min(max(bisect.bisect_right(self.x,(a+b)/2)-1,0),len(self.c)-1)
        h = self.x[i+1]-self.x[i]
        if a < self.x[i]-1e-13*max(1,abs(a)) or b > self.x[i+1]+1e-13*max(1,abs(b)):
            raise ValueError("Thermal interval crossed a spline knot or extrapolated")
        return pshift(self.c[i], (a-self.x[i])/h, (b-a)/h)

    def at(self, x):
        i = min(max(bisect.bisect_right(self.x,x)-1,0),len(self.c)-1)
        if not self.x[0] <= x <= self.x[-1]:
            raise ValueError("Thermal spline extrapolation")
        return peval(self.c[i],(x-self.x[i])/(self.x[i+1]-self.x[i]))

    def qualify(self, ck, name):
        for x,y in zip(self.x,self.y):
            ck.check("spline_node", self.at(x), y, max(abs(y),1e-100),
                     tol=CONFIG["spline_tolerance"], context=name)
        for i in range(len(self.c)-1):
            for order in [0,1,2]:
                p,q = self.c[i][:],self.c[i+1][:]
                for _ in range(order):
                    p=pder(p);q=pder(q)
                a=peval(p,1)/(self.x[i+1]-self.x[i])**order
                b=peval(q,0)/(self.x[i+2]-self.x[i+1])**order
                scale=max(abs(a),abs(b),max(abs(v) for v in p+q)
                          /min(self.x[i+1]-self.x[i],self.x[i+2]-self.x[i+1])**order,1e-100)
                ck.check("spline_continuity",a,b,scale,tol=CONFIG["spline_tolerance"],context=name)
        for i,j in [(0,1),(-2,-1)]:
            a=self.c[i][3]/(self.x[i+1]-self.x[i])**3 if i>=0 else self.c[i][3]/(self.x[i]-self.x[i-1])**3
            b=self.c[j][3]/(self.x[j+1]-self.x[j])**3 if j>=0 else self.c[j][3]/(self.x[j]-self.x[j-1])**3
            ck.check("spline_not_a_knot",a,b,max(abs(a),abs(b),1e-100),
                     tol=CONFIG["spline_tolerance"],context=name)


def prange(p, a, b, power=4, cancellation_scale=0.):
    """Padded Bernstein numerator hull divided by positive T**power."""
    n = len(p)-1
    bb = [math.fsum(p[j]*math.comb(i,j)/math.comb(n,j) for j in range(i+1))
          for i in range(n+1)]
    pad = CONFIG["polynomial_padding"]*max([abs(v) for v in p+bb]+[cancellation_scale,1e-300])
    low, high = min(bb)-pad, max(bb)+pad
    vals = [v/d for v in [low,high] for d in [a**power,b**power]]
    return min(vals),max(vals)


def interval_add(a,b):
    return a[0]+b[0],a[1]+b[1]


def log_history_integrand(sigma, ct, cs, heating):
    return (4/3)*(heating*ct/(sigma*(3*sigma+heating))
                   +3*(ct-cs)/(3*sigma+heating))


def thermal_qualification(ck):
    er=rows(THERM/"electron_thermo_0c03542043bd1b1a.txt")
    qa=rows(THERM/"QED_pressure_correction_e2.txt")
    qb=rows(THERM/"QED_pressure_correction_e3.txt")
    nr=rows(THERM/"NEVOPRIMAT_col_1_7.csv",",")
    ck.yes("thermal_table_census",len(er)==2000 and len(qa)==len(qb)==500 and len(nr)==600)
    ck.yes("qed_common_grid",[r[0] for r in qa]==[r[0] for r in qb])
    sx=[r[0] for r in er];qx=[r[0] for r in qa]
    spl = dict(
        E=Spline(sx,[r[1]+r[2] for r in er]),
        DE=Spline(sx,[r[3]+r[4] for r in er]),
        rho=Spline(sx,[r[1] for r in er]),
        Q=Spline(qx,[a[1]+b[1] for a,b in zip(qa,qb)]),
        Q1=Spline(qx,[a[2]+b[2] for a,b in zip(qa,qb)]),
        Q2=Spline(qx,[a[3]+b[3] for a,b in zip(qa,qb)]))
    for key,s in spl.items():
        s.qualify(ck,key)
    for degree in range(4):
        s=Spline([.2,.3,.8,1.7,2.5],[v**degree for v in [.2,.3,.8,1.7,2.5]])
        for x in [.2,.27,.51,1.1,2.4,2.5]:
            ck.check("spline_synthetic_polynomial",s.at(x),x**degree,max(1,x**degree))
    nevo=sorted((CONFIG["m_e_MeV"]*r[1]/r[0],max(0.,r[5])) for r in nr)
    nt=[r[0] for r in nevo]
    def heat(T):
        if not nt[0] <= T <= nt[-1]:return 0.
        i=min(bisect.bisect_right(nt,T)-1,len(nt)-2)
        f=(T-nt[i])/(nt[i+1]-nt[i])
        return nevo[i][1]*(1-f)+nevo[i+1][1]*f

    Tlo,Thi=CONFIG["thermal_temperature_MeV"]
    cutoff=CONFIG["m_e_MeV"]/30
    ck.check("electron_cutoff",sx[0],cutoff,cutoff,tol=2e-14)
    raw_knots=sorted({Tlo,Thi,cutoff,*[x for x in sx+qx+nt if Tlo<x<Thi]})
    # m_e/30 and the printed first electron knot differ only by roundoff.
    # Represent that owned cutoff by the larger endpoint; never make a
    # near-zero-width differentiation interval from decimal conversion.
    knots=[]
    for v in raw_knots:
        if knots and abs(v-knots[-1])<=2e-14*max(abs(v),abs(knots[-1])):
            knots[-1]=max(v,knots[-1])
        else:
            knots.append(v)
    sg=4*math.pi**2/45
    per_resolution=[]
    for subdivisions in CONFIG["thermal_subdivisions"]:
        total=[0.,0.]; heating=[0.,0.]; drift=[0.,0.]
        midpoint=0.;prefix_lo=prefix_hi=0.
        sigma_global=[math.inf,-math.inf];rho_global=[math.inf,-math.inf]
        witness=[];nsegments=0
        for left,right in zip(knots,knots[1:]):
            for sub in range(subdivisions):
                a=left+(right-left)*sub/subdivisions
                b=left+(right-left)*(sub+1)/subdivisions
                t=[a,b-a];t2=pmul(t,t);t4=pmul(t2,t2)
                p={k:s.coeff(a,b) if (k not in ["E","DE","rho"] or a>=cutoff) else [0.]
                   for k,s in spl.items()}
                Ep=pscale(pder(p["E"]),1/(b-a))
                Qp=pscale(pder(p["Q1"]),1/(b-a))
                sigma=padd(pscale(t4,sg),p["E"],pmul(t,p["Q1"]))
                ct=padd(pscale(t4,3*sg),pmul(t,Ep),pscale(p["E"],-1),pmul(t2,Qp))
                drift_terms=[pmul(t,Ep),pmul(t,p["DE"]),pmul(t2,Qp),pmul(t2,p["Q2"])]
                drift_num=padd(drift_terms[0],pscale(drift_terms[1],-1),
                               drift_terms[2],pscale(drift_terms[3],-1))
                rho=padd(pscale(t4,math.pi**2/15),p["rho"],pmul(t,p["Q1"]),pscale(p["Q"],-1))
                ss,cc,rr=(prange(q,a,b) for q in [sigma,ct,rho])
                dd=prange(drift_num,a,b,cancellation_scale=max(abs(v) for q in drift_terms for v in q))
                # N is linear on each original NEVO interval; at the outer edge,
                # include its interior limiting value as well as the zero exterior.
                nn=[heat(a),heat(b),heat((a+b)/2)]
                nl,nh=min(nn),max(nn)
                ck.yes("thermal_positive_denominators",ss[0]>0 and cc[0]>0 and cc[0]-dd[1]>0 and rr[0]>0,
                       [a,b,subdivisions])
                if min(ss[0],rr[0])<=0:
                    raise RuntimeError("Unbounded thermal denominator")
                denlo=3*ss[0]+nl;denhi=3*ss[1]+nh
                hh=((4/3)*nl*max(0,cc[0])/(ss[1]*denhi),
                    (4/3)*nh*cc[1]/(ss[0]*denlo))
                dv=[4*v/d for v in dd for d in [denlo,denhi]]
                dr=(min(dv),max(dv))
                lg=math.log(b/a)
                val=interval_add(hh,dr)
                for i in [0,1]:
                    heating[i]+=hh[i]*lg;drift[i]+=dr[i]*lg;total[i]+=val[i]*lg
                prefix_lo=min(prefix_lo,total[0]);prefix_hi=max(prefix_hi,total[1])
                T=(a+b)/2;sig=peval(sigma,.5)/T**4
                cv=peval(ct,.5)/T**4;dc=peval(drift_num,.5)/T**4;hn=heat(T)
                mid=(4/3)*(hn*cv/(sig*(3*sig+hn))+3*dc/(3*sig+hn))
                ck.yes("thermal_midpoint_inside_bounds",val[0]-1e-13<=mid<=val[1]+1e-13)
                midpoint+=mid*lg
                sigma_global=[min(sigma_global[0],ss[0]),max(sigma_global[1],ss[1])]
                rho_global=[min(rho_global[0],rr[0]),max(rho_global[1],rr[1])]
                nsegments+=1
            if left<=.01<=right or left<=.1<=right or left<=1<=right or right==Thi:
                witness.append(dict(T_upper_MeV=right,log_ratio_bounds=total[:]))
        ck.yes("thermal_integral_inside_bounds",total[0]<=midpoint<=total[1])
        per_resolution.append(dict(subdivisions=subdivisions,segments=nsegments,
            log_ratio_end_bounds=total,heating_only_bounds=heating,derivative_drift_bounds=drift,
            log_ratio_all_T_bounds=[prefix_lo,prefix_hi],midpoint_readout=midpoint,
            sigma_bounds=sigma_global,plasma_rho_over_T4_bounds=rho_global,witness=witness))
    for sig in [.5,1.,3.]:
        for ratio in [2.,3.,5.]:
            ct=ratio*sig
            ck.check("zero_heating_consistent_limit",log_history_integrand(sig,ct,ct,0.))
            for hn,offset in [(0.,.01),(.003,0.),(.1,-.02)]:
                cs=ct+offset
                raw=(4/3)*ct/sig-4*cs/(3*sig+hn)
                ck.check("synthetic_factored_history_identity",
                         log_history_integrand(sig,ct,cs,hn),raw,max(1.,abs(raw)))
    # The official endpoint is a_end*T_end/T0=(sigma_end/s_gamma)^(-1/3).
    # Include BOTH normalization factors; the product cancels analytically.
    endpoint_sigma=sg+spl["Q1"].at(Tlo)/Tlo**3
    ck.yes("endpoint_entropy_positive",math.isfinite(endpoint_sigma) and endpoint_sigma>0)
    endpoint_extra=(endpoint_sigma/sg)**(4/3)
    endpoint_a4=(endpoint_sigma/sg)**(-4/3)
    endpoint_ratio=endpoint_extra*endpoint_a4
    ck.check("endpoint_normalization_cancellation",endpoint_ratio,1.)
    intersection=[max(r["log_ratio_all_T_bounds"][0] for r in per_resolution)+math.log(endpoint_ratio),
                  min(r["log_ratio_all_T_bounds"][1] for r in per_resolution)+math.log(endpoint_ratio)]
    ck.yes("history_interval_intersection_nonempty",intersection[0]<=intersection[1])
    return dict(
        status="QUALIFIED_PINNED_INTERPOLANTS_ONLY",
        per_resolution=per_resolution,
        log_ratio_all_T_intersection=intersection,
        nevo_raw_negative_rows=sum(r[5]<0 for r in nr),
        nevo_raw_negative_min=min(r[5] for r in nr),
        endpoint_sigma_over_photon=endpoint_sigma/sg,
        endpoint_extra_density_normalization=endpoint_extra,
        endpoint_scale_factor_fourth_power_normalization=endpoint_a4,
        endpoint_combined_late_normalization=endpoint_ratio,
        fixed_neutrino_history=True,altered_neutrino_decoupling_qualified=False)


def run(old,cal,obs):
    start=time.perf_counter();ck=Checks()
    table=AbundanceTable()
    withheld=table.qualify(ck)
    thermal=thermal_qualification(ck)
    conversion=(7/8)*(4/11)**(4/3)
    ck.check("late_radiation_normalization",
             (7*math.pi**2/120)/(math.pi**2/15)*(4/11)**(4/3),conversion)
    expected={(s,r,R) for s in range(4) for r in range(18) for R in [32,128,512,2048,8192]}
    ck.yes("inherited_label_census",
           {(r["spectrum_index"],r["reference"],r["R"]) for r in old["rows"]}==expected)
    output=[];baselines={}
    def prediction(omega,delta,label):
        if not table.x[0]<=omega<=table.x[-1] or not table.y[0]<=delta<=table.y[-1]:
            return dict(status="OUTSIDE_TABLE_DOMAIN",omega_b=omega,Delta=delta)
        cub=table.sample(omega,delta)
        quad=table.sample(omega,delta,degree=2)
        linear=table.sample(omega,delta,degree=1)
        local=.020<=omega<=.024 and 0<=delta<=3
        data={}
        for name,col,scol in [("helium",4,5),("deuterium",6,7)]:
            delta_num=cub[col]-quad[col]
            if local:
                ck.check("target_order_comparison_"+name,delta_num,
                         tol=CONFIG["interpolation_allowance"][name],context=label)
            sigma=linear[scol]
            ck.yes("positive_table_sigma",sigma>0,label)
            residual=cub[col]-obs[name]["value"]
            data[name]=dict(prediction=cub[col],signed_residual=residual,
                observational_sigma=obs[name]["sigma"],table_theory_sigma=sigma,
                numerical_allowance=CONFIG["interpolation_allowance"][name],
                cubic_minus_quadratic=delta_num,
                cubic_minus_bilinear_theory_sigma=cub[scol]-sigma,
                descriptive_marginal_standardized_residual=residual/math.hypot(sigma,obs[name]["sigma"]))
        Y,D=cub[4],cub[6]
        return dict(status="TABLE_PROXY",omega_b=omega,Delta=delta,
            local_numerical_rectangle=local,observables=data,
            atomic_Yp_not_scored=cub[3],eta10=cub[1],
            helium_D_only_denominator_correction=Y*(1+2*D)/(1+2*Y*D)-Y,
            helium_linear_coefficient_unprovided_He3_over_H=3*Y*(1-Y)/(1+2*Y*D)**2)
    fine=thermal["per_resolution"][-1]
    llo,lhi=thermal["log_ratio_all_T_intersection"]
    sigmax=fine["sigma_bounds"][1];rho_min=fine["plasma_rho_over_T4_bounds"][0]
    for ref in cal["references"]:
        i=ref["reference"];omega=ref["bbn"]["omega_b"]
        baselines[i]=prediction(omega,0.,["baseline",i])
    Aref=CONFIG["finite_gap_reference_temperature_MeV"]*1e6*CONFIG["eV_J"]/(
        CONFIG["k_B_J_K"]*CONFIG["inherited_T0_K"])
    # Exact inspected-history relation: A=(T/T0)(sigma/s_gamma)^(1/3)e^(-L/4).
    # Use global thermal bounds rather than assuming residual heating is zero.
    Aref_lower=Aref*(fine["sigma_bounds"][0]/(4*math.pi**2/45))**(1/3)*math.exp(-lhi/4)
    ck.yes("finite_gap_scale_factor_bound_positive",math.isfinite(Aref_lower) and Aref_lower>0)
    for saved in old["rows"]:
        ref=cal["references"][saved["reference"]];omega=ref["bbn"]["omega_b"]
        delta=saved["asymptote_over_photons"]/conversion
        pred=prediction(omega,delta,saved["source_row_index"])
        shifted=prediction(omega*(CONFIG["table_T0_K"]/CONFIG["inherited_T0_K"])**3,
                           delta,["T0_sensitivity",saved["source_row_index"]])
        x_over_ordinary=delta*(7*math.pi**2/120)*(sigmax/(11*math.pi**2/45))**(4/3)/rho_min
        def Hratio(L):
            return math.sqrt((1+x_over_ordinary)/(1+x_over_ordinary*math.exp(-L)))-1
        envelope=[min(0.,Hratio(llo)),max(0.,Hratio(lhi))]
        if pred["status"]=="TABLE_PROXY":
            pred["minus_matched_Delta0"]={
                key:pred["observables"][key]["prediction"]-baselines[saved["reference"]]["observables"][key]["prediction"]
                for key in ["helium","deuterium"]}
            pred["T0_eta_coordinate_sensitivity"]={
                key:shifted["observables"][key]["prediction"]-pred["observables"][key]["prediction"]
                for key in ["helium","deuterium"]}
        output.append(dict(source_row_index=saved["source_row_index"],
            spectrum_index=saved["spectrum_index"],reference=saved["reference"],R=saved["R"],
            late_photon_ratio=saved["asymptote_over_photons"],late_Delta_coordinate=delta,
            conditional_baryon_benchmark=ref["bbn"],proxy=pred,
            thermal_proxy_minus_conserved_fractional_H_bounds=envelope,
            scalar_fractional_energy_gap_bound_at_10keV=saved["D"]/(saved["Q"]*Aref_lower**2),
            conserved_scalar_abundance_status="NOT_YET_QUALIFIED"))
    ck.yes("output_census",len(output)==360 and len(baselines)==18)
    summaries=[]
    for R in [32,128,512,2048,8192]:
        subset=[r for r in output if r["R"]==R]
        supported=[r for r in subset if r["proxy"]["status"]=="TABLE_PROXY"]
        item=dict(R=R,rows=len(subset),table_supported=len(supported),
                  Delta_range=[min(r["late_Delta_coordinate"] for r in subset),
                               max(r["late_Delta_coordinate"] for r in subset)])
        if supported:
            item["proxy_marginal_ranges"]={
                key:{field:[min(r["proxy"]["observables"][key][field] for r in supported),
                            max(r["proxy"]["observables"][key][field] for r in supported)]
                     for field in ["prediction","signed_residual","descriptive_marginal_standardized_residual"]}
                for key in ["helium","deuterium"]}
        summaries.append(item)
    return dict(status="FAILED_NUMERICAL_QUALIFICATION" if ck.failures else "COMPLETE_PROXY_AND_INTERFACE_QUALIFICATION",
        conserved_scalar_abundance_status="NOT_YET_QUALIFIED",configuration=CONFIG,
        scope="Fixed-heating table proxy only; no exact scalar BBN completion, confidence exclusion, new abundance or baryon fit.",
        observations=obs,table_metadata=dict(rows=1300,omega_grid=table.x,Delta_grid=table.y,
            ordinary_Neff=3.044,tau_n_seconds=878.4,tau_n_sigma_seconds=.5,
            T0_K=2.7255,MC_samples=1000,helium_column="YpBBN"),
        counts=ck.counts,maxima=ck.maxima,failures=ck.failures,
        withheld_interpolation=withheld,thermal_interface=thermal,matched_Delta0=baselines,
        photon_scale_reference_A_at_10keV=Aref,
        thermal_history_lower_bound_A_at_10keV=Aref_lower,rows=output,summaries=summaries,
        seconds=time.perf_counter()-start,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    old,cal,obs,snapshot=inputs()
    if sys.argv[1:]==["freeze"]:
        print(encode(snapshot).decode());return 0
    if sys.argv[1:]!=["run"]:
        raise RuntimeError("Use freeze or run")
    if json.loads(FREEZE.read_text())!=snapshot:
        raise RuntimeError("Prospective freeze differs")
    payload=run(old,cal,obs)
    print(encode(dict(freeze_sha256=sha(FREEZE),
                     payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                     payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__":
    sys.exit(main())
