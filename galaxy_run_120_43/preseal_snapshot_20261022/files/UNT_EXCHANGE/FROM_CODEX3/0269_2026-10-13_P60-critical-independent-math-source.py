"""Codex3 SOURCE ONLY; root executes only inside reviewed saved checker.
Independent binomial products cover every actual count, not selected probes.
Shared mathematical dependency: axis-split identity and stated C90 tail proofs.
No producer imports, historical outputs, floats, files or launch operations.
"""
from fractions import Fraction as F
from math import comb, isqrt

TARGETS = ((2,0,0),(4,0,0),(6,0,0),(8,0,0),(12,0,0),(16,0,0),
           (2,2,0),(4,4,0),(8,8,0),(2,2,2),(4,4,4),(8,8,8))
ALL_TARGETS = ((0,0,0),)+TARGETS


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choose_row(n):
    row = [1]
    for k in range(1, n+1):
        quotient, remainder = divmod(row[-1]*(n-k+1), k)
        require(remainder == 0, 'integer binomial row division')
        row.append(quotient)
    return row


def shifted_central_table(maximum, shifts):
    return {s: [comb(2*j, j+s) if j >= s else 0 for j in range(maximum+1)]
            for s in sorted(set(shifts))}


def complete_even_counts(maximum, record):
    """Direct sum of FOUR independent binomial factors per summand.
    Unlike producer, never obtains the next full summand from its ratio.
    """
    split = [(abs(a)//2, abs(b+c)//2, abs(b-c)//2) for a,b,c in ALL_TARGETS]
    cache = shifted_central_table(maximum, [x for t in split for x in t])
    for m in range(maximum+1):
        choose = choose_row(2*m)
        counts = []
        for s, t, u in split:
            value = 0
            for j in range(s, m-max(t,u)+1):
                value += choose[2*j]*cache[s][j]*cache[t][m-j]*cache[u][m-j]
            counts.append(value)
        require(all(v <= counts[0] for v in counts), 'whole-domain central maximum')
        record('critical_counts', m, counts)
        yield m, counts


def finite_lemma_checks():
    # These checks accompany the inherited ALL-m mathematical proof; they do
    # not promote a finite scan to an asymptotic theorem.
    for m in range(1,1001):
        require((2*m+1)**2 > 4*m*(m+1), 'Wallis increasing sign')
        require((2*m+1)*(2*m+3) < (2*m+2)**2, 'Wallis decreasing sign')
    for m in range(8,401):
        for j in range(m):
            r=m-j; numerator=r**4; denominator=(j+1)**2*2*r*(2*r-1)
            if 4*(j+1)<=m:
                require(2*numerator>=3*denominator, 'region A')
            if 10*(j+1)<=3*m:
                require(8*numerator>=9*denominator, 'region A2')
            if m>=10 and j>=2*m//5+1 and j<m-2 and 5*j>=2*m and r>=2:
                require(4*numerator<=3*denominator, 'region C')
            if 4*j>=3*m and r>=2:
                require(2*numerator<=denominator, 'region B')
    rho=F(199,200)
    require(rho**12>=F(2,3) and rho**20>=F(8,9) and rho**20>=F(3,4)**7, 'rho powers')
    for m in range(1,4001):
        require(4*m**5>(m-1)**3*(2*m+3)**2, 'five-half telescoping')
        require(4*m**3>(m-1)*(2*m+1)**2, 'three-half telescoping')


def critical_expected(record=lambda *args: None):
    M=1400; denominator=36**M
    # Powers are shared integer denominators; no Fraction/gcd per summand.
    powers=[36**k for k in range(M+1)]
    numerators=[0]*len(TARGETS); origin=[]; formula=[]; sector=[]
    rho=F(199,200); edge=F(40)
    finite_lemma_checks()
    for m, counts in complete_even_counts(M, record):
        origin.append(counts[0])
        for i, target in enumerate(TARGETS):
            difference=counts[0]-counts[i+1]
            numerators[i]+=difference*powers[M-m]
            if 30<=m<=240:
                a,b,c=target; s=abs(a)//2; t=abs(b+c)//2; u=abs(b-c)//2
                bound=F(4*(s*s+t*t+u*u),m)+edge*rho**m
                require(difference<=counts[0]*bound, 'all actual assembled-bound domain')
        if m<=16:
            formula.extend({'m':m,'target':list(target),'recurrence':count,'axis_split':count}
                           for target,count in zip(ALL_TARGETS,counts))
        if 1<=m<=40:
            den=(2*m+1)*(m+1)*(m+2)
            require(2*36**m<=counts[0]*den and counts[0]<=36**m,'sector sandwich')
            sector.append({'m':m,'return_count':counts[0],'lower_numerator':2*36**m,
                           'lower_denominator':den,'upper':36**m})
    kernels={t:F(n,denominator) for t,n in zip(TARGETS,numerators)}
    partial=lambda n:F(sum(origin[m]*powers[n-m] for m in range(n+1)),powers[n])
    total=partial(M); half=partial(700); quarter=partial(350)
    last=F(origin[M],powers[M])
    wallis=F(comb(480,240),4**240)**2
    low=240*wallis; high=F(481,2)*wallis
    scale=10**12
    root=isqrt(high.numerator*scale**2//high.denominator)
    sqrt_high=F(root+2,scale)
    require(F(root,scale)**2<=high<=sqrt_high**2,'tail root bracket')
    # Balanced trinomial max follows exchange of any two counts differing by2.
    q=F(comb(300,100)*comb(200,100),3**300)
    q3=300*q/(1-F(2,900)); B=q3*sqrt_high
    radius=M-2; sqrt_floor=isqrt(radius)
    sum52=F(2,3*radius*sqrt_floor); sum32=F(2,sqrt_floor)
    tails={}
    for target in TARGETS:
        a,b,c=target; s=abs(a)//2; t=abs(b+c)//2; u=abs(b-c)//2
        tails[target]=4*(s*s+t*t+u*u)*B*sum52 + edge*B*F(1,radius*sqrt_floor)*rho**(M+1)/(1-rho)
    absolute=2*B*sum32+last
    inc1=half-quarter; inc2=total-half
    finite=inc2<inc1 and inc2<F(1,50) and absolute<F(1,15)
    def increment(a,b):
        return (kernels[b]-kernels[a]-tails[a],kernels[b]+tails[b]-kernels[a])
    axis={d:increment((d,0,0),(2*d,0,0)) for d in [2,4,6,8]}
    face={d:increment((d,d,0),(2*d,2*d,0)) for d in [2,4]}
    body={d:increment((d,d,d),(2*d,2*d,2*d)) for d in [2,4]}
    inv=(F(2,5),F(3,5)); log=(F(4,5),F(5,4)); lin=(F(9,5),F(11,5))
    ratios=[]
    for ray,values,pairs in [('axis',axis,[(2,4),(4,8)]),('fdiag',face,[(2,4)]),('bdiag',body,[(2,4)])]:
        for d,e in pairs:
            require(values[d][0]>0 and values[e][0]>0,'positive ratio domain')
            lo=values[e][0]/values[d][1]; hi=values[e][1]/values[d][0]
            ratios.append({'ray':ray,'d':d,'next_d':e,'interval':[lo,hi],
                           'in_INV':inv[0]<=lo<=hi<=inv[1],
                           'excludes_LOG':hi<log[0],'excludes_LIN':hi<lin[0]})
    contains=ratios[1]['interval'][0]<=F(1,2)<=ratios[1]['interval'][1]
    prediction=(axis[4][0]*F(11,18),axis[4][1]*F(13,18))
    overlap=prediction[1]>=axis[6][0] and axis[6][1]>=prediction[0]
    matched=finite and contains and overlap and all(r['in_INV'] and r['excludes_LOG'] and r['excludes_LIN'] for r in ratios)
    return {'scope':'C90_FIXED_EXACT_CRITICAL_INSTRUMENT_SECOND_TORIC_CARRIER_CONDITIONAL',
            'M':M,'mu':'1/6','targets':[list(t) for t in TARGETS],
            'tail_anchors':{'wallis_low':low,'wallis_high':high,'sqrt_high':sqrt_high,'Q3':q3,'B5':B,
                           'rho':rho,'edgeC':edge,'assembled_gate_range':(30,240)},
            'kernel_and_tail':[{'target':list(t),'partial_kernel':kernels[t],'tail_upper':tails[t]} for t in TARGETS],
            'return_sum':total,'return_term':last,'absolute_tail':absolute,
            'return_quarter':quarter,'return_half':half,'return_doubling_increments':[inc1,inc2],
            'critical_finiteness_gate':finite,'increments':{'axis':axis,'fdiag':face,'bdiag':body},
            'ratios':ratios,'windows':{'INV':inv,'LOG':log,'LIN':lin},
            'deepest_axis_contains_half':contains,'out_of_sample_prediction':prediction,
            'out_of_sample_measured':axis[6],'out_of_sample_overlap':overlap,
            'finite_window_class':'INV_EXPONENT1_BRACKET' if matched else 'UNRESOLVED_OR_DIFFERENT',
            'proof_gates':{'formula_rows':formula,'sector_sandwich_rows':sector,
                           'wallis_direct_range':[1,1000],'edge_regions_checked_m':[8,400],
                           'telescoping_checked_m':[1,4000],
                           'all_m_extension':'C90 original driver header polynomial/Wallis/trinomial proofs, separately reviewed'},
            'exact_asymptotic_exponent_proved_by_fit':False,
            'requires_prior_distinct_carrier_qualification':True,'TWO_CARRIER_adopted':False,
            'conservation_or_critical_selection_earned':False,'physical_prediction_released':False}


def one_dimension(k,x):
    if abs(x)>k or (k+x)%2:
        return 0
    return comb(k,(k+x)//2)


def noncritical_expected(record=lambda *args: None):
    rows=[]
    # Independent direct axis-split binomial products, including ODD k and d.
    # Counts are reused only between fixed mu rows sharing the same lattice.
    one_cache={(k,x):one_dimension(k,x) for k in range(601) for x in range(25)}
    counts={d:[] for d in range(1,25)}
    for k in range(601):
        choose=choose_row(k)
        values=[]
        for d in range(1,25):
            value=0
            for j in range(d,k+1,2):
                value+=choose[j]*one_cache[j,d]*one_cache[k-j,0]**2
            counts[d].append(value); values.append(value)
        record('noncritical_counts',k,values)
    for p,q,K,dmax in [(1,12,90,12),(1,8,160,14),(3,20,300,16),(4,25,600,24)]:
        mu=F(p,q); upper=(6*mu)**(K+1)/(1-6*mu)
        weights=[p**k*q**(K-k) for k in range(K+1)]
        series={d:(F(sum(counts[d][k]*weights[k] for k in range(K+1)),q**K),upper)
                for d in range(1,dmax+1)}
        ratios={d:(series[d+1][0]/(series[d][0]+upper),
                   (series[d+1][0]+upper)/series[d][0]) for d in range(1,dmax)}
        below=all(hi<=F(19,20) for lo,hi in ratios.values())
        cauchy=abs(ratios[dmax-1][0]-ratios[dmax-2][1])<=F(1,40)
        power=(dmax-1)*(1-ratios[dmax-1][1])
        rows.append({'mu':mu,'K':K,'dmax':dmax,'full_partial_and_tail_by_distance':series,
                     'all_ratio_intervals':ratios,'all_ratios_below_margin':below,'cauchy':cauchy,
                     'power_exclusion_value':power,
                     'class':'EXPONENTIAL_DECLARED_SCOPE' if below and cauchy and power>8 else 'UNRESOLVED'})
    special={}
    for m,row in complete_even_counts(151,record):
        if m in [75,150,151]:special[m]=row[0]
    a=special[150]; b=special[151]; half=special[75]; witness=[]
    for mu in [F(13,72),F(1,5),F(1,4)]:
        term=a*mu**300; h=half*mu**150; ratio=F(b,a)*mu**2
        witness.append({'mu':mu,'m':150,'count_at_m':a,'count_at_m_plus1':b,'count_at_half_m':half,
                        'term':term,'half_term':h,'term_ratio':ratio,
                        'growing_witness':ratio>F(21,20) and term>h,
                        'all_mu_above_critical_divergence':'requires all-m sector sandwich proof'})
    return {'scope':'FIXED_C90_NONCRITICAL_CONTROLS_SECOND_CARRIER_CONDITIONAL',
            'subcritical':rows,'supercritical':witness,'TWO_CARRIER_adopted':False,
            'physical_prediction_released':False}
