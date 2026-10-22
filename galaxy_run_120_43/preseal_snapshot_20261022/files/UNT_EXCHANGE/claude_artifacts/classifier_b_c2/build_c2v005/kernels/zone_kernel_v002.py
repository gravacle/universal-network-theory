"""Independent pure zone kernel from prereg sections 1-2,4. Inert prep only.
Caller must validate external schemas; this module accepts normalized Rows.
No filesystem access. None in NEAR means unavailable, not false.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Row:
    kind: str
    ratio: object = None
    near: object = False

    def __post_init__(self):
        if self.kind not in {"HIT", "MISS", "INVALID", "LATE"}:
            raise ValueError("kind")
        if self.near is not None and type(self.near) is not bool:
            raise ValueError("near")
        if self.ratio is not None:
            if type(self.ratio) not in (int,float): raise ValueError("ratio")
            try: finite=math.isfinite(self.ratio)
            except OverflowError: finite=False
            if not finite: raise ValueError("ratio")
        if self.kind in {"INVALID", "LATE"} and self.ratio is not None:
            raise ValueError("ratio on absent prediction")
        if self.kind == "HIT" and (self.ratio is None or abs(self.ratio)>1):
            raise ValueError("hit ratio")
        if self.kind == "MISS" and self.ratio is not None and abs(self.ratio)<=1:
            raise ValueError("miss ratio")
        if self.kind != "MISS" and self.near is not False:
            raise ValueError("near outside tier MISS")

def summarize(rows):
    rows=tuple(rows)
    invalid=sum(r.kind=="INVALID" for r in rows)
    hit=sum(r.kind=="HIT" for r in rows)
    miss=sum(r.kind in {"MISS","LATE"} for r in rows)
    nv=hit+miss
    unsigned=sum(r.kind in {"MISS","LATE"} and r.ratio is None for r in rows)
    ratios=[r.ratio for r in rows if r.ratio is not None]
    center=median(ratios) if ratios else None
    md=nv>0 and 2*miss>=nv
    hd=nv>0 and 2*hit>nv
    if center is None or (md and 2*(miss-unsigned)<nv): sign="UNDEFINED"
    elif center < -1: sign="DEFICIT"
    elif center > 1: sign="EXCESS"
    else: sign="CENTERED"
    near=None if any(r.kind=="MISS" and r.near is None for r in rows) else sum(r.near is True for r in rows)
    return dict(N_v=nv,H=hit,M=miss,U=unsigned,I=invalid,N=near,m=center,
                S=sign,miss_dominated=md,hit_dominated=hd)

def drift_comparison(primary,twin):
    if len(primary)!=len(twin): raise ValueError("unaligned rows")
    pairs=[(a,b) for a,b in zip(primary,twin) if a.ratio is not None and b.ratio is not None]
    if not pairs: return "NOT_DECIDED"
    hp=sum(a.kind=="HIT" for a,b in pairs)
    hs=sum(b.kind=="HIT" for a,b in pairs)
    ap=median(abs(a.ratio) for a,b in pairs)
    ass=median(abs(b.ratio) for a,b in pairs)
    if hs>hp and ass<ap:return "CONSISTENT"
    if hs<=hp and ass>=ap:return "AGAINST"
    return "NOT_DECIDED"


def median(values):
    """Conventional midpoint; avoid overflowing a finite same-sign mean."""
    ordered=sorted(values)
    n=len(ordered)
    if not n:raise ValueError("empty median")
    if n%2:return ordered[n//2]
    a,b=ordered[n//2-1:n//2+1]
    try:
        result=(a+b)/2
        if math.isfinite(result):return result
    except OverflowError:
        pass
    return a/2+b/2
