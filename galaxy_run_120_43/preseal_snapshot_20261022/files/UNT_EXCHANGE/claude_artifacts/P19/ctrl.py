"""Claude P-19: independent implementations (no Codex code) of the BUILD_ONCE control fixtures.
Gapless: OBC hard-core chain by explicit many-body ED (N<=16) + Jordan-Wigner check via 1-particle matrix eigvals (N<=128).
Walks: exact Bessel-function amplitudes on the infinite chain (scipy.special.jv), independent of spectral/Taylor."""
import itertools, math, json
import numpy as np
def bessel_all(nmax,z):
    """Integer-order J_0..J_nmax(z) by Miller backward recurrence, normalized by J0+2*sum J_2k=1."""
    M=nmax+int(z)+60
    if M%2: M+=1
    j=[0.0]*(M+2); j[M+1]=0.0; j[M]=1e-300
    for n in range(M,0,-1): j[n-1]=(2*n/z)*j[n]-j[n+1]
    norm=j[0]+2*sum(j[k] for k in range(2,M+1,2))
    return np.array([j[n]/norm for n in range(nmax+1)])
out={}
# --- gapless: many-body ED for N=8,12,16 (independent of JW), sector energies at n=N/2, N/2+-1
def mb_ground(N,n,t=1.0):
    confs=[c for c in itertools.combinations(range(N),n)]; idx={c:i for i,c in enumerate(confs)}
    H=np.zeros((len(confs),len(confs)))
    for c in confs:
        s=set(c)
        for i in range(N-1):
            if (i in s)!=(i+1 in s):
                d=tuple(sorted((s-{i,i+1})|({i+1} if i in s else {i})))
                H[idx[d],idx[c]]-=t
    return np.linalg.eigvalsh(H)[0]
rows=[]
for N in (8,12,16):
    n=N//2; E=[mb_ground(N,k) for k in (n-1,n,n+1)]
    dp,dm=E[2]-E[1],E[0]-E[1]
    rows.append(dict(N=N,method="many-body ED",delta_plus=dp,delta_minus=dm,curv=dp+dm,exact=4*math.sin(math.pi/(2*(N+1)))))
# one-particle (JW) route for N=16..128 using numeric eigvals of the hopping matrix (not the closed form)
for N in (16,32,64,128):
    A=np.diag(-np.ones(N-1),1); A=A+A.T; ev=np.sort(np.linalg.eigvalsh(A)); n=N//2
    E=lambda k: ev[:k].sum()
    dp,dm=E(n+1)-E(n),E(n-1)-E(n)
    rows.append(dict(N=N,method="1-particle eigvals",delta_plus=dp,delta_minus=dm,curv=dp+dm,exact=4*math.sin(math.pi/(2*(N+1))),E_n=E(n)))
out["gapless"]=rows
# --- Mott atomic: onsite m in {0,1,2}, H=(U/2)m(m-1)-(U/2)m, U=1; ground per sector by counting
def mott(N,U=1.0):
    e={0:0.0,1:-U/2,2:0.0}
    def Emin(M):  # min total over occupations summing to M, each 0..2
        # greedy is exact here: fill singles first (cost -U/2), then doubles (0) or empties (0)
        ones=min(M,N); rest=M-ones  # extra particles create doubles: converting a 1 to 2 costs +U/2
        return ones*e[1] + rest*(e[2]-e[1]) if M<=2*N else None
    En=[Emin(N-1),Emin(N),Emin(N+1)]
    return dict(N=N,delta_plus=En[2]-En[1],delta_minus=En[0]-En[1],curv=En[2]+En[0]-2*En[1])
out["mott"]=[mott(N) for N in (16,32,64,128)]
# --- walks: |psi_x(T)|^2 = J_x(2 t T)^2 on infinite chain (N=512 periodic is indistinguishable at T<=16)
def walk(t,T,q=0.95):
    xs=np.arange(-300,301); J=bessel_all(300,2*t*T); p=J[np.abs(xs)]**2
    tot=p.sum(); m2=(xs**2*p).sum()
    R=next(r for r in range(0,300) if p[np.abs(xs)<=r].sum()>=q*tot)
    return dict(t=t,T=T,norm=tot,second_moment=m2,expected=2*t*t*T*T,radius95=R,front_speed=R/T)
out["walks"]={"common":[walk(1.0,T) for T in (4,8,12,16)],"split_B":[walk(1.5,T) for T in (4,8,12,16)]}
# --- lapse vs medium: universal N_lapse=1+.2rho multiplies all terms; medium t_A=(1+.2rho), t_B=(1+.8rho)
lm=[]
for rho in (0,0.5,1):
    N=1+0.2*rho
    lm.append(dict(rho=rho,lapse_ratio_speedA_over_B=(2*N*1)/(2*N*1),lapse_speed_per_coclock=(2*N)/N,
                   medium_fractional_A=0.2*rho,medium_fractional_B=0.8*rho))
out["lapse_medium"]=lm
json.dump(out,open("P19_RESULT.json","w"),indent=1,default=float)
for r in out["gapless"]: print("gapless",r["method"],r["N"],f'{r["delta_plus"]:.15f}',f'{r["curv"]:.15f}',f'exact {r["exact"]:.15f}', f'E_n={r.get("E_n",float("nan")):.12f}')
for r in out["mott"]: print("mott",r)
for k,v in out["walks"].items():
    for r in v: print("walk",k,r["T"],"R95",r["radius95"],"v",r["front_speed"],"m2",round(r["second_moment"],9),"exp",r["expected"],"norm",round(r["norm"],12))
