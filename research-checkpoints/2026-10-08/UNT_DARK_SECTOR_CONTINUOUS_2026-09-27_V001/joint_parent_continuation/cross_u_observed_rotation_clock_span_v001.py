"""Guarded finite observed-rotation/charged-clock arithmetic; no field solve."""
from pathlib import Path
import argparse,datetime,hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_OBSERVED_ROTATION_CLOCK_SPAN_V001'
AUTHOR_DRAFT=False
PROTOCOL_SHA='2093db674b13ac43ede9f17decef3ebc7968654407028720a80d6ce6fd8cda85'
PINS={'../ngc3198_sparc_excerpt_v001.txt':'58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900','CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_EXP24_CASE.json':'2a25fb0da765a9db6490b912aab45cad415506a70b1cfc1a5cfb8d4fd93063a7','INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0','CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md':'b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5'}
SPEED_C_KMS=299792.458
RANGES=((.32,44.08),(2.89,44.08),(5.78,44.08))
ERROR_SHIFTS=(-2.,-1.,0.,1.,2.)
EPS=(1e-6,1e-5)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def publish(name,v):
 p=BASE/name;raw=(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;return sha(p)
def mean_power(a,b,k):return sum(a**i*b**(k-i) for i in range(k+1))/(k+1)
def integrate(points):
 leading=conformal=rem=0.;panels=[]
 for (r0,v0),(r1,v1) in zip(points,points[1:]):
  h=math.log(r1/r0);a=(v0/SPEED_C_KMS)**2;b=(v1/SPEED_C_KMS)**2
  basic=h*(a+b)/2;proper=h*sum((-1)**(k+1)*mean_power(a,b,k) for k in range(1,9));bound=h*max(a,b)**9/(1-max(a,b))
  assert h>0 and 0<=a<1 and 0<=b<1 and 0<=proper<=basic
  leading+=basic;conformal+=proper;rem+=bound;panels.append(dict(R0=r0,R1=r1,velocity0_kms=v0,velocity1_kms=v1,u0=a,u1=b,log_width=h,leading_integral=basic,conformal_integral=proper,conformal_series_remainder_bound=bound))
 return leading,conformal,rem,panels
def main():
 assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
 assert not list(BASE.glob(STEM+'_*')),'Existing outputs preserved'
 inputs=dict(PINS,**{STEM+'.md':PROTOCOL_SHA})
 for n,h in inputs.items():assert sha(BASE/n)==h,n
 owner=dict(owner='root',pid=os.getpid(),source_sha256=sha(__file__),started=datetime.datetime.now(datetime.timezone.utc).isoformat());outputs={}
 case=json.loads((BASE/'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_EXP24_CASE.json').read_text());data=[]
 for line in (BASE/'../ngc3198_sparc_excerpt_v001.txt').read_text().splitlines():
  if line.startswith('NGC3198 '):
   a=line.split();data.append(tuple(float(v) for v in a[2:5]))
 assert len(data)==len(case['rows'])==43
 for a,b in zip(data,case['rows']):assert a==(b['R_kpc'],b['observed_velocity_kms'],b['observed_error_kms'])
 h=math.log(3.);u=(100/SPEED_C_KMS)**2;t=integrate(((1.,100.),(3.,100.)))
 assert abs(t[0]-h*u)<=1e-20 and abs(t[1]-h*u/(1+u))<=1e-20 and t[2]<1e-50
 assert abs(math.expm1(2*(.5*math.log1p(EPS[0])))-EPS[0])<1e-20
 rows=[]
 for lo,hi in RANGES:
  selected=[x for x in data if lo<=x[0]<=hi];assert selected[0][0]==lo and selected[-1][0]==hi
  for shift in ERROR_SHIFTS:
   # The speed lower envelope is disclosed, not an inferred confidence band.
   points=[(r,max(0.,v+shift*e)) for r,v,e in selected]
   I,J,rem,panels=integrate(points);assert I>0
   comparisons=[]
   for ep in EPS:
    band=.5*math.log1p(ep)
    admitted=True if J+rem<band else False if J>=band else None
    comparisons.append(dict(eps=ep,full_clock_log_lapse_span=band,leading_excess=I-band,conformal_excess_lower=J-band,conformal_excess_upper=J+rem-band,required_u_weighted_mean_R_Psi_prime=1-band/I,leading_within_full_band=I<band,conformal_within_full_band=admitted,conformal_comparison_reason='Remainder interval straddles strict band' if admitted is None else 'Alternating-series truncation interval; ordinary floating arithmetic'))
   rows.append(dict(R_interval_kpc=[lo,hi],number_of_points=len(points),quoted_error_shift=shift,leading_log_lapse_drop=I,leading_drop_kms2=I*SPEED_C_KMS**2,conformal_leading_drop_lower=J,conformal_leading_drop_upper=J+rem,conformal_series_remainder_bound=rem,necessary_eps_under_leading_mapping=math.expm1(2*I),panels=panels,comparisons=comparisons))
 result=dict(status='CONDITIONAL_ARITHMETIC_PASS',owner=owner,input_sha256=inputs,source_rows=data,controls_pass=3,rows=rows,assumptions=['Fixed published distance/inclination/quoted errors','Linear interpolation of squared speed versus log radius between every selected observation','Quoted error shifts are sensitivity envelopes, not correlated confidence limits','Phase phi=omega*t with invariant X=sqrt(-g_inverse(dphi,dphi))=omega/N; U does not define X','Observed speed identified with local circular/ZAMO speed in declared static scalar chart','Leading static mapping or leading conformal Psi=Phi only; no full metric solved'],identity='Full charged P(X) range gives Delta(log N)<0.5*log(1+EPS), independent of homogeneous charge and absolute lapse normalization',full_static_identity='DeltaPhi=integral[u*(1-R*Psi_prime)]dlogR with u=v_ZAMO^2/c^2',qualification=dict(no_global_nonexistence_proof=True,no_observational_likelihood=True,no_field_or_clock_replay=True,no_new_EPS_adoption=True))
 outputs[STEM+'_RESULT.json']=publish(STEM+'_RESULT.json',result)
 for n,h in inputs.items():assert sha(BASE/n)==h
 assert sha(__file__)==owner['source_sha256']
 receipt=dict(status='CLOSED',owner=owner,closed=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_sha256=inputs,output_sha256=outputs,result_sha256=outputs[STEM+'_RESULT.json'])
 publish(STEM+'_RECEIPT.json',receipt)
 for r in rows:
  if r['quoted_error_shift'] in (-2.,0.):print(json.dumps({k:v for k,v in r.items() if k not in ('panels','comparisons')},allow_nan=False),flush=True)
 return 0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root-owned',action='store_true');assert p.parse_args().root_owned;raise SystemExit(main())
