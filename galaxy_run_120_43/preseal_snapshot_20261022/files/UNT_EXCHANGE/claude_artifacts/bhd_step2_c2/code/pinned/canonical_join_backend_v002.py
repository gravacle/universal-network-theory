"""Definitions only: literal canonical #7 + coherent admission, old/complete one-Born.
Exact Gaussian-rational coefficientwise columns; no I/O, imports of producers or launch.
All coefficients/phases/profiles are explicit inputs. Tiny quotients are method fixtures.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations,product
from math import comb,isfinite
from typing import NamedTuple
from types import MappingProxyType


def rational(x):
    if isinstance(x,bool):raise TypeError('boolean is not a coefficient')
    if isinstance(x,Fraction):return x
    if isinstance(x,int):return Fraction(x)
    if isinstance(x,float):
        if not isfinite(x):raise ValueError('nonfinite coefficient')
        return Fraction(x)
    if isinstance(x,str):return Fraction(x)
    raise TypeError('explicit finite rational/decimal/binary64 coefficient required')

@dataclass(frozen=True)
class Scalar:
    re: Fraction=Fraction(0)
    im: Fraction=Fraction(0)
    def __post_init__(self):
        object.__setattr__(self,'re',rational(self.re));object.__setattr__(self,'im',rational(self.im))
    @staticmethod
    def coerce(x):
        if isinstance(x,Scalar):return x
        if isinstance(x,complex):return Scalar(rational(x.real),rational(x.imag))
        if isinstance(x,(tuple,list)) and len(x)==2:return Scalar(x[0],x[1])
        return Scalar(rational(x))
    def __add__(self,x):
        x=Scalar.coerce(x);return Scalar(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return Scalar(-self.re,-self.im)
    def __sub__(self,x):return self+-Scalar.coerce(x)
    def __rsub__(self,x):return Scalar.coerce(x)+-self
    def __mul__(self,x):
        x=Scalar.coerce(x);return Scalar(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Scalar.coerce(x);a=x.norm2()
        if not a:raise ZeroDivisionError('zero Gaussian scalar')
        return self*x.conjugate()*Scalar(1/a)
    def conjugate(self):return Scalar(self.re,-self.im)
    def norm2(self):return self.re*self.re+self.im*self.im
    def __bool__(self):return bool(self.re or self.im)
    def __complex__(self):return complex(float(self.re),float(self.im))
    def serial(self):return [str(self.re),str(self.im)]
ZERO=Scalar();ONE=Scalar(1);IM=Scalar(0,1)

def bounded_int(x,lo,hi,label):
    if isinstance(x,bool) or not isinstance(x,int) or not lo<=x<=hi:raise ValueError(label)
    return x

def word_masks(n,k):
    if not 0<=k<=n:return
    for sites in combinations(range(n),k):yield sum(1<<v for v in sites)

@dataclass(frozen=True)
class Graph:
    vertices:int
    edges:tuple
    label:str
    def __post_init__(self):
        bounded_int(self.vertices,2,10**9,'vertex census')
        edges=tuple(tuple(x) for x in self.edges);object.__setattr__(self,'edges',edges)
        degrees=[0]*self.vertices
        for u,v in edges:
            bounded_int(u,0,self.vertices-1,'edge endpoint');bounded_int(v,0,self.vertices-1,'edge endpoint')
            if u==v:raise ValueError('no self-loops; labelled parallel channels allowed')
            degrees[u]+=1;degrees[v]+=1
        if any(d!=4 for d in degrees):raise ValueError('complete degree-four graph required')
        if not isinstance(self.label,str) or not self.label:raise ValueError('explicit graph/construction label required')
    @property
    def num_edges(self):return len(self.edges)
    def degrees(self,incidence):
        bounded_int(incidence,0,(1<<self.num_edges)-1,'incidence word')
        d=[0]*self.vertices
        for e,(u,v) in enumerate(self.edges):
            if (incidence>>e)&1:d[u]+=1;d[v]+=1
        return tuple(d)

def periodic_q4(side):
    """Primary V006 periodic diamond graph; distinct shift-0 anchor cuts for side>=2."""
    bounded_int(side,2,10**3,'primary distinct-anchor side>=2')
    xyz=tuple(product(range(side),repeat=3));index={r:i for i,r in enumerate(xyz)};nv=2*side**3
    shifts=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
    edges=tuple((i,side**3+index[tuple((r[k]+s[k])%side for k in range(3))]) for i,r in enumerate(xyz) for s in shifts)
    cuts=tuple(4*index[r] for r in ((0,0,0),(1,0,0),(0,1,0),(0,0,1)))
    return Graph(nv,edges,f'PRIMARY_PERIODIC_Q4_SIDE_{side}'),cuts

def tiny_four_channel_quotient():
    """Method fixture only: all four labelled A0->B1 parallel channels are cut.
    This substitutes distinct channel cuts for collapsed shift-0 anchors. Born is
    two disconnected parallel-edge pairs; no simple-graph rank/IR transfer.
    """
    return Graph(2,((0,1),)*4,'METHOD_N2_FOUR_PARALLEL_CHANNEL_QUOTIENT'),(0,1,2,3)

class State(NamedTuple):
    sector:int              # 0 old, 1 complete Born
    incidence:int
    carriers:int
    records:int             # native q, independent of cells and Qresource
    ready:int
    spent:int
    def serial(self):return list(self)

class Channel(NamedTuple):
    kind:str
    index:int
    target:State
    features:dict

class BirthMap:
    def __init__(self,old,cuts):
        if not isinstance(old,Graph):raise TypeError('declared Graph required')
        cuts=tuple(cuts)
        if len(cuts)!=4 or len(set(cuts))!=4:raise ValueError('four distinct labelled cuts required')
        for e in cuts:bounded_int(e,0,old.num_edges-1,'cut index')
        self.old=old;self.cuts=cuts;self.keep=tuple(e for e in range(old.num_edges) if e not in cuts)
        self.star_A=old.vertices;self.star_B=old.vertices+1
        edges=[old.edges[e] for e in self.keep];paths=[]
        for e in cuts:
            u,v=old.edges[e];paths.append((len(edges),len(edges)+1));edges.extend(((u,self.star_B),(self.star_A,v)))
        self.paths=tuple(paths);self.born=Graph(old.vertices+2,tuple(edges),'ONE_BORN_OF_'+old.label)
    def encode_incidence(self,n):
        bounded_int(n,0,(1<<self.old.num_edges)-1,'old incidence')
        a=sum(((n>>e)&1)<<i for i,e in enumerate(self.keep))
        for e,pair in zip(self.cuts,self.paths):
            if (n>>e)&1:
                for k in pair:a|=1<<k
        return a
    def cut_count(self,n):return sum((n>>e)&1 for e in self.cuts)
    def checked(self,state,sector):
        if not isinstance(state,State):raise TypeError('State required for Birth map')
        g=self.old if sector==0 else self.born
        if state.sector!=sector:raise ValueError('Birth map sector')
        bounded_int(state.incidence,0,(1<<g.num_edges)-1,'Birth incidence domain')
        for x in (state.carriers,state.records,state.ready,state.spent):bounded_int(x,0,(1<<g.vertices)-1,'Birth site domain')
        if state.ready&state.spent:raise ValueError('Birth orthogonal cell domain')
    def encode(self,state):
        self.checked(state,0)
        if state.sector!=0:raise ValueError('F maps old to Born only')
        return State(1,self.encode_incidence(state.incidence),state.carriers,state.records,state.ready,state.spent)
    def decode(self,state):
        self.checked(state,1)
        if state.sector!=1:raise ValueError('Fdag maps Born only')
        if any(x>>self.old.vertices for x in (state.carriers,state.records,state.ready,state.spent)):return None
        n=sum(((state.incidence>>i)&1)<<e for i,e in enumerate(self.keep))
        for e,(a,b) in zip(self.cuts,self.paths):
            x=(state.incidence>>a)&1;y=(state.incidence>>b)&1
            if x!=y:return None
            n|=x<<e
        return State(0,n,state.carriers,state.records,state.ready,state.spent)
    def T(self,state):
        self.checked(state,0)
        return self.encode(state) if self.cut_count(state.incidence)==2 else None
    def Tdag(self,state):
        old=self.decode(state)
        return old if old is not None and self.cut_count(old.incidence)==2 else None

REAL_KEYS=('h','Delta','Ud','epsilon_c','t','epsilon_r','g','lambda_R','lambda_J','E_I','E_R','E_S','identity_offset')

@dataclass(frozen=True)
class Parameters:
    real:dict
    dstar:Fraction
    kappa:tuple
    epsilon_B:Scalar
    old_hop_phases:tuple
    born_hop_phases:tuple
    def __post_init__(self):
        if set(self.real)!=set(REAL_KEYS):raise ValueError('all exact real coefficients and common offset explicitly required')
        object.__setattr__(self,'real',MappingProxyType({k:rational(v) for k,v in self.real.items()}))
        object.__setattr__(self,'dstar',rational(self.dstar));object.__setattr__(self,'kappa',tuple(Scalar.coerce(z) for z in self.kappa));object.__setattr__(self,'epsilon_B',Scalar.coerce(self.epsilon_B))
        for name in ('old_hop_phases','born_hop_phases'):
            phases=tuple(Scalar.coerce(z) for z in getattr(self,name));object.__setattr__(self,name,phases)
            # Binary64 exp(i theta) may differ from exact unit norm by roundoff.
            # Inputs are kept literally; there is no silent normalization.
            if any(abs(z.norm2()-1)>Fraction(1,10**12) for z in phases):raise ValueError('declared unit hopping phases required')
    def coefficients(self):
        x=dict(self.real)
        for v,z in enumerate(self.kappa):x[f'kappa_{v}_re']=z.re;x[f'kappa_{v}_im']=z.im
        x['epsilon_B_re']=self.epsilon_B.re;x['epsilon_B_im']=self.epsilon_B.im
        return x
    def conjugated(self):
        return Parameters(dict(self.real),self.dstar,tuple(z.conjugate() for z in self.kappa),self.epsilon_B.conjugate(),tuple(z.conjugate() for z in self.old_hop_phases),tuple(z.conjugate() for z in self.born_hop_phases))
    def uniformly_scaled(self,factor):
        factor=rational(factor)
        return Parameters({k:v*factor for k,v in self.real.items()},self.dstar,tuple(z*factor for z in self.kappa),self.epsilon_B*factor,self.old_hop_phases,self.born_hop_phases)
    def serial(self):
        return dict(real={k:str(v) for k,v in self.real.items()},dstar=str(self.dstar),kappa=[z.serial() for z in self.kappa],epsilon_B=self.epsilon_B.serial(),old_hop_phases=[z.serial() for z in self.old_hop_phases],born_hop_phases=[z.serial() for z in self.born_hop_phases])

def charges(state):return state.carriers.bit_count()+state.ready.bit_count(),(state.ready|state.spent).bit_count()

def dimension(graph,Q=None,M=None):
    """Complete tensor or invariant Q/M block, with no fixed-Nc restriction."""
    n=graph.vertices;e=graph.num_edges
    if Q is None and M is None:return (1<<e)*12**n
    if Q is None or M is None:raise ValueError('declare both Q and M or neither')
    # Q/M label the JOINED resource sector, not a graph-local admissibility bound.
    # An absent old sector must not reject a nonempty larger Born sector.
    for x,label in ((Q,'resource Q'),(M,'resource M')):
        if isinstance(x,bool) or not isinstance(x,int) or x<0:raise ValueError(label+' must be a nonnegative integer')
    if M>n or Q>n+M:return 0
    # Choose M active cells; among V carrier bits plus M Ready-vs-Spent bits choose Q.
    return (1<<(e+n))*comb(n,M)*comb(n+M,Q)

def graph_basis(graph,sector,Q=None,M=None,max_dimension=None):
    total=dimension(graph,Q,M)
    bounded_int(max_dimension,1,10**12,'explicit enumeration cap required')
    if total>max_dimension:raise MemoryError('full requested block exceeds cap before enumeration')
    if total==0:return
    n=graph.vertices
    if Q is None:
        configurations=((p,r,s) for c in product(range(3),repeat=n) for r in [sum(1<<v for v,a in enumerate(c) if a==1)] for s in [sum(1<<v for v,a in enumerate(c) if a==2)] for p in range(1<<n))
        configs=tuple(configurations)
    else:
        configs=[]
        for nr in range(max(0,Q-n),min(M,Q)+1):
            for r in word_masks(n,nr):
                other=tuple(v for v in range(n) if not (r>>v)&1)
                for sp in combinations(other,M-nr):
                    s=sum(1<<v for v in sp)
                    for p in word_masks(n,Q-nr):configs.append((p,r,s))
        configs=tuple(configs)
    for inc in range(1<<graph.num_edges):
        for p,r,s in configs:
            for q in range(1<<n):yield State(sector,inc,p,q,r,s)

class CanonicalJoin:
    def __init__(self,birth,parameters):
        if not isinstance(birth,BirthMap) or not isinstance(parameters,Parameters):raise TypeError('explicit BirthMap and Parameters')
        self.birth=birth;self.parameters=parameters;self.graphs=(birth.old,birth.born)
        if len(parameters.kappa)!=birth.born.vertices or len(parameters.old_hop_phases)!=birth.old.num_edges or len(parameters.born_hop_phases)!=birth.born.num_edges:raise ValueError('complete declared old/Born profiles required')
    def checked(self,state):
        if not isinstance(state,State):raise TypeError('exact State required')
        bounded_int(state.sector,0,1,'old/Born sector');g=self.graphs[state.sector]
        bounded_int(state.incidence,0,(1<<g.num_edges)-1,'incidence domain')
        for x in (state.carriers,state.records,state.ready,state.spent):bounded_int(x,0,(1<<g.vertices)-1,'site factor domain')
        if state.ready&state.spent:raise ValueError('I/R/S states are orthogonal, not two simultaneous cell bits')
        return state
    def channels(self,state):
        """Labelled H[target,source] channels. Aggregation occurs only in columns.
        T_e=phase*b_u^dag b_v+phase.conj*b_v^dag b_u: v->u has +theta.
        Every native channel acts on arbitrary Born off-image states.
        """
        self.checked(state);g=self.graphs[state.sector];d=g.degrees(state.incidence);p=state.carriers;q=state.records;r=state.ready;s=state.spent
        diag={'Delta':state.incidence.bit_count(),'Ud':sum((x-self.parameters.dstar)**2 for x in d),'epsilon_c':p.bit_count(),'epsilon_r':q.bit_count(),'lambda_R':-sum(d[v]*((q>>v)&1) for v in range(g.vertices)),'lambda_J':sum(d[v]*((p>>v)&1) for v in range(g.vertices)),'E_I':g.vertices-(r|s).bit_count(),'E_R':r.bit_count(),'E_S':s.bit_count(),'identity_offset':1}
        yield Channel('diagonal',-1,state,{k:Scalar.coerce(v) for k,v in diag.items() if v})
        phases=self.parameters.old_hop_phases if state.sector==0 else self.parameters.born_hop_phases
        for e,(u,v) in enumerate(g.edges):
            yield Channel('incidence_flip',e,state._replace(incidence=state.incidence^(1<<e)),{'h':-ONE})
            pu=(p>>u)&1;pv=(p>>v)&1
            if (state.incidence>>e)&1 and pu!=pv:
                amp=-phases[e].conjugate() if pu else -phases[e]
                yield Channel('hop',e,state._replace(carriers=p^(1<<u)^(1<<v)),{'t':amp})
        for v in range(g.vertices):
            if (p>>v)&1:yield Channel('bind',v,state._replace(records=q^(1<<v)),{'g':ONE})
            if (r>>v)&1 and not (p>>v)&1:
                target=state._replace(carriers=p|(1<<v),ready=r^(1<<v),spent=s|(1<<v))
                yield Channel('admission_forward',v,target,{f'kappa_{v}_re':ONE,f'kappa_{v}_im':IM})
            if (s>>v)&1 and (p>>v)&1:
                target=state._replace(carriers=p^(1<<v),ready=r|(1<<v),spent=s^(1<<v))
                yield Channel('admission_reverse',v,target,{f'kappa_{v}_re':ONE,f'kappa_{v}_im':-IM})
        target=self.birth.T(state) if state.sector==0 else self.birth.Tdag(state)
        if target is not None:yield Channel('Birth' if state.sector==0 else 'unBirth',0,target,{'epsilon_B_re':ONE,'epsilon_B_im':IM if state.sector==0 else -IM})
    def column_terms(self,state):
        out={}
        for ch in self.channels(state):
            dest=out.setdefault(ch.target,{})
            for k,z in ch.features.items():
                value=dest.get(k,ZERO)+z
                if value:dest[k]=value
                else:dest.pop(k,None)
        return {s:f for s,f in out.items() if f}
    def column(self,state):
        coefficients=self.parameters.coefficients();out={}
        for target,terms in self.column_terms(state).items():
            z=sum((amp*coefficients[k] for k,amp in terms.items()),ZERO)
            if z:out[target]=z
        return out
    def action_sparse(self,vector):
        """Exact matrix-free action on declared sparse ket, retaining every target.
        This is not a Krylov/evolution algorithm or an implicit state truncation.
        """
        out={}
        for state,weight in vector.items():
            self.checked(state);weight=Scalar.coerce(weight)
            if not weight:continue
            for target,z in self.column(state).items():
                value=out.get(target,ZERO)+z*weight
                if value:out[target]=value
                else:out.pop(target,None)
        return out
    def dimension(self,Q=None,M=None):return sum(dimension(g,Q,M) for g in self.graphs)
    def basis(self,Q=None,M=None,max_dimension=None):
        total=self.dimension(Q,M);bounded_int(max_dimension,1,10**12,'explicit joined enumeration cap')
        if total>max_dimension:raise MemoryError('complete joined support exceeds cap before enumeration')
        for sector,g in enumerate(self.graphs):yield from graph_basis(g,sector,Q,M,max_dimension)
