"""Claude independent toy check of P-47 0118 chain kernel: carrier on a ring (hopping t), all Records written,
Bind g toggles the Record at the carrier site; an erased Record costs Delta. Truncate to <=1 erased Record (leading g^2).
Ground state -> P(r) = prob. that the erased Record sits at distance r from the carrier, given one erased.
Prediction: P(r) ~ exp(-r/xi), xi = 1/[2 arccosh(1 + Delta/(2|t|))]."""
import numpy as np
def run(N,t,g,D):
    # basis: (x) no erased: N states; (x,j) erased at j: N*N states
    n0=N; dim=N+N*N
    H=np.zeros((dim,dim))
    idx=lambda x,j: N+x*N+j
    for x in range(N):
        for dx in (1,-1):
            y=(x+dx)%N
            H[y,x]+=-t
            for j in range(N): H[idx(y,j),idx(x,j)]+=-t
        H[idx(x,x),x]+=g; H[x,idx(x,x)]+=g      # Bind erases/writes at carrier site
        for j in range(N): H[idx(x,j),idx(x,j)]+=D
    w,v=np.linalg.eigh(H); gs=v[:,0]
    P=np.zeros(N//2+1)
    for x in range(N):
        for j in range(N):
            r=min((x-j)%N,(j-x)%N); P[r]+=gs[idx(x,j)]**2
    return P/P.sum()
for (t,D) in ((1.0,1.0),(1.0,0.5),(0.5,2.0)):
    P=run(40,t,0.05,D); xi=1/(2*np.arccosh(1+D/(2*abs(t))))
    rs=np.arange(2,12); slope=np.polyfit(rs,np.log(P[2:12]),1)[0]
    print(f"t={t} Delta={D}: fitted xi={-1/slope:.4f}  predicted xi={xi:.4f}")
