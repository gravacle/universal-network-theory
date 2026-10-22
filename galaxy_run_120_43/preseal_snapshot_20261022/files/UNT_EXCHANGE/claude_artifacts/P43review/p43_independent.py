"""Claude independent recomputation of P43 frozen fixture expectations (own code; author source not imported/run).
Reads only the frozen fixture JSON. Exact rationals. Reports density (relative) and baseline residuals separately."""
import json,sys,itertools
from fractions import Fraction as F
d=json.load(open(sys.argv[1]))
def iv(x): return (F(x[0]),F(x[1]))
def rng(f,boxes):
    vals=[f(*c) for c in itertools.product(*boxes)]; return (min(vals),max(vals))
def status(res,eq,dm,adm):
    if not all(adm.values()): return "UNDETERMINED"
    prec=all((h-l)/2<min(eq,dm)/4 for l,h in res)
    if not prec: return "UNDETERMINED"
    if all(-eq<=l and h<=eq for l,h in res): return "UNIVERSAL_COMPATIBLE"
    if any(l>=dm or h<=-dm for l,h in res): return "SPECIES_DEPENDENT"
    return "UNDETERMINED"
def inv3(m):
    a,b,c=m[0];d_,e,f=m[1];g,h,i=m[2]
    det=a*(e*i-f*h)-b*(d_*i-f*g)+c*(d_*h-e*g)
    return [[(e*i-f*h)/det,(c*h-b*i)/det,(b*f-c*e)/det],[(f*g-d_*i)/det,(a*i-c*g)/det,(c*d_-a*f)/det],[(d_*h-e*g)/det,(b*g-a*h)/det,(a*e-b*d_)/det]]
for fx in d['fixtures']:
    p=fx['payload']; eq,dm=F(p['delta_eq']),F(p['delta_min'])
    try:
        if fx['method']=='compare_isotropic':
            b=[iv(x) for x in p['box']]
            if b[0][0]<=0 or b[4][0]<=0: print(fx['name'],'->UNDEFINED_CLOCK | expected',fx['expected_status']);continue
            if any(l<=0 for l,h in b): print(fx['name'],'->UNDEFINED_POSITIVE_DISPERSION | expected',fx['expected_status']);continue
            rI1=rng(lambda c0,e0,c1,e1:(e1/c1)/(e0/c0)-1,[b[0],b[1],b[4],b[5]])
            rI2=rng(lambda e0,k0,v0,e1,k1,v1:(k1*e1/v1**2)/(k0*e0/v0**2)-1,[b[1],b[2],b[3],b[5],b[6],b[7]])
            bI2=rng(lambda e,k,v:k*e/v**2-1,[b[1],b[2],b[3]])
            cI2=rng(lambda e,k,v:k*e/v**2-1,[b[5],b[6],b[7]])
            merged=status([rI1,rI2,bI2,cI2],eq,dm,p['admission']); dens=status([rI1,rI2],eq,dm,p['admission']); base=status([bI2],eq,dm,p['admission'])
        else:
            s0,s1=p['baseline'],p['current']
            pt=lambda s:{k:(F(v[0]) if k in('clock','rest') else [[F(x[0]) for x in r] for r in v]) for k,v in s.items() if k!='frame_id'}
            wid=any(x[0]!=x[1] for s in (s0,s1) for k in('kinetic','light_squared') for r in s[k] for x in r)
            a,b_=pt(s0),pt(s1)
            if s0['frame_id']!=s1['frame_id']: print(fx['name'],'-> frame error | expected',fx['expected_status']);continue
            if wid: print(fx['name'],'-> (interval tensor; skipped point check) expected',fx['expected_status']);continue
            I1=(b_['rest']/b_['clock'])/(a['rest']/a['clock'])-1
            M=lambda s:[[s['rest']*sum(s['kinetic'][i][k]*inv3(s['light_squared'])[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
            M0,M1=M(a),M(b_)
            rel=max(abs(M1[i][j]-M0[i][j]) for i in range(3) for j in range(3))
            base0=max(abs(M0[i][j]-(1 if i==j else 0)) for i in range(3) for j in range(3))
            dens='UNIVERSAL_COMPATIBLE' if abs(I1)<=eq and rel<=eq else ('SPECIES_DEPENDENT' if abs(I1)>=dm or rel>=dm else 'UNDETERMINED')
            base='UNIVERSAL_COMPATIBLE' if base0<=eq else 'MISMATCH'
            merged=dens if base=='UNIVERSAL_COMPATIBLE' else '(merged fails)'
        print(f"{fx['name']}: merged={merged} density={dens} baseline={base} | expected {fx['expected_status']}")
    except Exception as e: print(fx['name'],'-> error',e,'| expected',fx['expected_status'])
