"""SOURCE ONLY. Independent full native diagonal reads and word statistics.
One-pass exact integer mass AND attained full-component norm census.
Declared global upper bounds need not be attained; all ten norms are derived.
No producer function imported. Root authenticates all states/center/error.
Internal rational values are wired by the final independently reviewed adapter.
"""
from fractions import Fraction as Q
S=1<<80
WORDS=('00','01','10','11')
DIAGONALS=('old_presence','born_presence','carriers','Ready','Nq_old','Nq_all')
CAPS={'old_presence':1,'born_presence':1,'carriers':1,'Ready':1,'Nq_old':2,'Nq_all':4}


def need(ok,why):
    if not ok:raise ValueError(why)


def product(a,b):
    corners=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return [min(corners),max(corners)]


def distance(a,b):
    # Range of absolute distance between arbitrary members of two intervals.
    return [max(Q(0),a[0]-b[1],b[0]-a[1]),max(abs(a[0]-b[1]),abs(a[1]-b[0]))]


def statistics(words):
    need(set(words)==set(WORDS),'all four ordered words')
    for lo,hi in words.values():need(0<=lo<=hi<=1,'closed probability interval')
    need(sum(v[0] for v in words.values())<=1<=sum(v[1] for v in words.values()),'normalization not excluded')
    marginals=[]
    for coordinate in range(2):
        yes=[words[w] for w in WORDS if w[coordinate]=='1']
        marginals.append([max(Q(0),sum(v[0] for v in yes)),min(Q(1),sum(v[1] for v in yes))])
    independent={}
    for word in WORDS:
        factors=[marginals[j] if word[j]=='1' else [1-marginals[j][1],1-marginals[j][0]] for j in range(2)]
        independent[word]=product(*factors)
    both=product(*marginals)
    cov=[words['11'][0]-both[1],words['11'][1]-both[0]]
    def tv(other):
        diffs=[distance(words[w],other[w]) for w in WORDS]
        return [max(Q(0),sum(v[0] for v in diffs)/2),min(Q(1),sum(v[1] for v in diffs)/2)]
    return {'marginals':marginals,'connected_covariance':cov,'product_of_marginals':independent,
        'TV_fair_coin':tv({w:[Q(1,4),Q(1,4)] for w in WORDS}),
        'TV_same_marginal_independent':tv(independent)}


def readout(states,center,error,guard):
    need(len(states)==len(center)==10432,'entire authenticated active-state vector')
    e=Q(error);need(0<=e<Q(1,1<<51),'exact native cumulative radius')
    mass={name:0 for name in WORDS+DIAGONALS};norm=0;observed_caps={name:0 for name in WORDS+DIAGONALS}
    for index,(state,z) in enumerate(zip(states,center)):
        need(len(state)==6 and all(type(x)is int for x in state),'literal six-register state')
        need(len(z)==2 and all(type(x)is int for x in z),'complete unnormalized I80 center')
        sector,inc,p,q,r,s=state;re,im=z;weight=re*re+im*im;norm+=weight
        word=str(q%2)+str((q//2)%2);mass[word]+=weight;observed_caps[word]=1
        counts={'old_presence':int(sector==0),'born_presence':int(sector==1),
            'carriers':bin(p).count('1'),'Ready':bin(r).count('1'),
            'Nq_old':int(bool(q&1))+int(bool(q&2)),'Nq_all':bin(q).count('1')}
        for name,coefficient in counts.items():
            need(0<=coefficient<=CAPS[name],'native full observable range')
            mass[name]+=coefficient*weight;observed_caps[name]=max(observed_caps[name],coefficient)
        if index%256==0:guard()
    # All states, including zero-amplitude states, contribute to each maximum.
    # CAPS is only a declared global upper bound, not an attained maximum.
    def interval(name,cap):
        point=Q(mass[name],S*S);delta=cap*e*(2+e)
        lo,hi=max(Q(0),point-delta),min(Q(cap),point+delta)
        need(lo<=hi,'normalized true state compatible with full center/error')
        return {'center_expectation':point,'interval':[lo,hi],
            'vector_error_allowance':delta,'operator_norm_upper':cap}
    words={w:interval(w,observed_caps[w]) for w in WORDS};diag={name:interval(name,observed_caps[name]) for name in DIAGONALS}
    return {'words':words,'statistics':statistics({w:words[w]['interval'] for w in WORDS}),
        'diagonal':diag,'norm_center_squared':Q(norm,S*S),'L2_error':e,
        'state_phase':'exp(-i(H-(2121/80)I)t), hbar=1','DE':False}


def interval_vector(read):
    return [read['words'][w]['interval'] for w in WORDS]+[read['diagonal'][name]['interval'] for name in DIAGONALS]


def add_trapezoid(integrals,left,right):
    # Integrals are unnormalised cumulative endpoint enclosures, not averaged
    # statistics. Every step h=1/512 contributes h/2*(left+right).
    need(len(integrals)==10,'all ten accumulator intervals')
    a,b=interval_vector(left),interval_vector(right)
    return [[Q(integrals[j][k])+Q(a[j][k]+b[j][k],1024) for k in range(2)] for j in range(10)]


def operator_norms(read):
    # Caller supplies a read reconstructed above from the whole native basis.
    need(set(read['words'])==set(WORDS) and set(read['diagonal'])==set(DIAGONALS),'whole read norm domain')
    caps={name:read['words' if name in WORDS else 'diagonal'][name]['operator_norm_upper'] for name in WORDS+DIAGONALS}
    need(all(type(value)is int and 0<=value<=(1 if name in WORDS else CAPS[name]) for name,value in caps.items()),'attained norms within declared global bounds')
    return caps


def average_intervals(integrals,steps,component_caps):
    need(type(steps)is int and 1<=steps<=512 and len(integrals)==10,'whole positive uniform window')
    need(set(component_caps)==set(WORDS+DIAGONALS),'all ten independently reconstructed component norms')
    need(all(type(value)is int and 0<=value<=(1 if name in WORDS else CAPS[name]) for name,value in component_caps.items()),'exact component norm domains')
    T=Q(steps,512);answer=[]
    for j,pair in enumerate(integrals):
        cap=component_caps[(WORDS+DIAGONALS)[j]]
        # Integral nearest-half-cell proof gives average error L*h/4.
        allowance=Q(1,2048) if j<4 else Q(10207*cap,560*1024)
        raw=[Q(v)/T for v in pair]
        value=[max(Q(0),raw[0]-allowance),min(Q(cap),raw[1]+allowance)]
        need(value[0]<=value[1],'complete averaged interval')
        if j<4:need(value[1]-value[0]<=Q(1,512),'frozen averaged-word halfwidth budget')
        answer.append({'trapezoid_interval':raw,'quadrature_allowance':allowance,'interval':value})
    return answer
