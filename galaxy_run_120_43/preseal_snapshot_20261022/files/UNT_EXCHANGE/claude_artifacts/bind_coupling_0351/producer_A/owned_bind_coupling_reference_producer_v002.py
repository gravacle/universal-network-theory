"""INERT producer V002: restricted sixth-degree Feshbach Bind/bridge coefficient C_yx (task 0351-A; V001 607ebc4d... + distinct
review notes: BELOW_E1_PREMISE_VIOLATED status with min|w-E1|, positivity of the realization coordinates, gated count of
negative inverse entries beyond tolerance, the global remainder bound stated verbatim). ROOT ALONE runs it, after
the Feshbach distinct review and a code review; the author has executed only GENERIC synthetic tests (no native matrix,
inverse, eigensolve or contraction for the frozen cases).

Implements exactly the contraction of Q_RELAXED_BRIDGE_BAND_SIXTH_FESHBACH_BIND_COUPLING_PROPOSED_V001.md (3d72a017...) under
the frozen spec BIND_COUPLING_REFERENCE_FROZEN_SPEC_V001.json (pinned), for cases L4 and L6, t = 1:
  M(u,v;q) = -[R_L + u B_old + v B_new] + {A(u+v) + r sum(q) - (r+sigma)[u(qo0+qo1) + v(qn0+qn1)]} I,
  x = old (1,0;1,1,0,0), y = new (0,1;0,0,1,1); E1 = lowest eigenvalue of M(x) (= a_eff - lambda_L, cross-checked);
  phi_x, phi_y positive normalized (phase: positive sum); six operations flip u, v, qo0, qo1, qn0, qn1 exactly once; the
  contact is the identity for a bridge flip and the carrier site projector of that q bit for a Bind flip;
  C_yx = sum over all 720 orderings of <phi_y| O6 R5 O5 R4 O4 R3 O3 R2 O2 R1 O1 |phi_x>, R_j = [M(S_j,q_j) - E1 I]^-1, the FULL
  carrier inverse of each intermediate block (every nonempty proper subset; never a q-minimized energy).
Two independently organized contractions: (1) literal enumeration of all 720 orderings with every contribution retained;
(2) subset dynamic programming over the 62 nonempty proper subsets. Inverses by full linear solve (primary) and full
spectral sum (cross-check, used in a second DP total). C_xy is computed independently from y to x (Hermiticity check).
Reported per case: every proper-subset matrix (dense, with exact diagonal), spectrum, gap to E1, uncertainty, inverse
residual, solve-vs-spectral agreement, minimum inverse entries; all 720 contributions (no clipping), totals, agreements and
absolute discrepancies; -C_yx; the conservative ceiling 720/Delta_family^5 with Delta_family from bound (G) of the all-even
proof; the symbolic small-coupling tail inequality with the computed numbers inserted; window (W) and frozen relations.
Margin policy: if any intermediate block's lowest eigenvalue lies within the frozen margin (plus numerical uncertainty) of
E1, the case is RESONANT_OR_UNRESOLVED and NO inverse is formed (no pseudoinverse, no dropped mode, no broadening).
Failed consistency checks are preserved in check_failures, never repaired. Floating warnings are recorded (0347 V003 style).
Scope: restricted fixed-energy coefficient only; full_parent_ready false; not motion, gravity sign, distance/clock or DM/DE.
Outputs: --output OUT (exclusive) and --journal JOURNAL (exclusive JSON lines START, CASE L4, CASE L6, END; flushed+fsynced).
Stdout: JSON events ending with TERMINAL. Exit 0 iff COMPLETED (computation finished, NOT a scientific pass), 1 FAILED (case
or post-analysis error; outputs written), 2 coded input/usage failure (nothing written), 3 unexpected. Strict JSON.
Environment: five BLAS thread variables forced to 1 before importing NumPy; NumPy from the normal path (do not use -I/-s).
Usage: python3 -B owned_bind_coupling_reference_producer_v002.py --output OUT.json --journal JOURNAL.jsonl
"""
import os
THREAD_VARS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
for _v in THREAD_VARS:os.environ[_v]='1'
import datetime,hashlib,itertools,json,math,platform,resource,sys,time,warnings
from fractions import Fraction
from pathlib import Path
import numpy as np

B='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
SPEC=(B+'CODEX1/BIND_COUPLING_REFERENCE_FROZEN_SPEC_V001.json','789b4a2ffa533d62e0588e14be97f17474d15bfabf8af94a87af27f4f6b549f9')
BOUND={'feshbach_source':(B+'helpers/coefficient_method/Q_RELAXED_BRIDGE_BAND_SIXTH_FESHBACH_BIND_COUPLING_PROPOSED_V001.md','3d72a0170961634f4627723b0ac8edb503960a36705d412cdb3c429fee7b70e8'),
 'source_family_companion':(B+'helpers/coefficient_method/Q_RELAXED_BRIDGE_BAND_MOTION_SOURCE_FAMILY_SCOPE_COMPANION_V001.md','ebd22c4ab843b2e89196cf0b5e7192c59ebc1b15dd23d5cb0c6728eac84b51de'),
 'all_even_family_proof':(B+'CODEX1/OWNED_Q_RELAXED_ALL_EVEN_BRIDGES_REFERENCE_BAND_PROPOSED_V001.md','aa6b636d3c4d6251d7baf3b0e5381858f5d7171d5c0568ddb4c304e0fb6042b7'),
 'all_even_family_review':(B+'helpers/response_packet_audit/OWNED_Q_RELAXED_ALL_EVEN_BRIDGES_REFERENCE_BAND_DISTINCT_REVIEW_V001.md','50f67cb4b4bcbaa820365276c66cc5f3e13ba15870ddbfc2bc94390825f499fa'),
 'feshbach_distinct_review':(B+'helpers/response_packet_audit/Q_RELAXED_BRIDGE_BAND_SIXTH_FESHBACH_BIND_DISTINCT_REVIEW_V001.md','5b19337cfb6d23bd589bda63cf2bf3934f72b675a2c0cabae0437ce03cec1be8')}
FREEZING=(B+'CODEX1/CLAUDE_BIND_COUPLING_INERT_IMPLEMENTATION_TASK_0351_V001.md','22c99a06e63f0167b762f1b4fd46575921cafff81a8152bc860adcd810b4f943')
CASE_IDS=['L4','L6']
OPS=['flip_old_bridge','flip_new_bridge','bind_qo0','bind_qo1','bind_qn0','bind_qn1']
X_BITS=(1,0,1,1,0,0);Y_BITS=(0,1,0,0,1,1)
CHECK_KEYS=['endpoint_eigen_residual_relative_tolerance','endpoint_orthogonality_absolute_tolerance','inverse_residual_relative_tolerance','inverse_method_relative_tolerance','contraction_agreement_relative_tolerance','minimum_numerical_denominator_margin']
EPS=float(np.finfo(np.float64).eps)
class Fail(Exception):pass
def sha(b):return hashlib.sha256(b).hexdigest()
def fin(x):
 x=float(x)
 if not math.isfinite(x):raise Fail('E_NONFINITE')
 return x
def flist(a):return [fin(x) for x in np.asarray(a).ravel().tolist()]
def fmat(a):return [[fin(x) for x in row] for row in np.asarray(a).tolist()]
def _pairs(ps):
 d={}
 for k,v in ps:
  if k in d:raise Fail('E_JSON_DUPLICATE_KEY')
  d[k]=v
 return d
def _const(c):raise Fail('E_JSON_NONFINITE_TOKEN')
def pinned(path,want,code):
 try:b=Path(path).read_bytes()
 except OSError:raise Fail(code+'_MISSING')
 if sha(b)!=want:raise Fail(code)
 return b
def rat(o,code):
 if not isinstance(o,dict) or set(o)!={'num','den'} or type(o['num']) is not int or type(o['den']) is not int or o['den']<=0:raise Fail(code)
 return Fraction(o['num'],o['den'])
def rstr(q):return '%d/%d'%(q.numerator,q.denominator)
# ---------------- spec ----------------
def load_spec():
 b=pinned(*SPEC,'E_PIN_SPEC')
 try:d=json.loads(b,object_pairs_hook=_pairs,parse_constant=_const)
 except ValueError:raise Fail('E_SPEC_JSON')
 bd=d.get('bound_documents')
 if not isinstance(bd,dict) or set(bd)!=set(BOUND):raise Fail('E_SPEC_BOUND_SET')
 for k,(p,h) in BOUND.items():
  if bd[k]!={'path':p,'sha256':h}:raise Fail('E_SPEC_BOUND_'+k)
 if d.get('freezing_document')!={'path':FREEZING[0],'sha256':FREEZING[1]}:raise Fail('E_SPEC_FREEZING')
 if [c.get('case_id') for c in d.get('cases',[])]!=CASE_IDS or [c.get('L') for c in d['cases']]!=[4,6]:raise Fail('E_SPEC_CASES')
 co=d.get('coordinates',{});im=d.get('implied',{});pr=d.get('positive_realization',{})
 t=rat(co.get('t'),'E_SPEC_T');a=rat(co.get('a_eff'),'E_SPEC_A_EFF');r=rat(co.get('r'),'E_SPEC_R');s=rat(co.get('sigma'),'E_SPEC_SIGMA')
 lR=rat(im.get('lambda_R'),'E_SPEC_LAMBDA_R');er=rat(im.get('epsilon_r'),'E_SPEC_EPSILON_R');A=rat(im.get('A'),'E_SPEC_A')
 if type(pr.get('dstar')) is not int:raise Fail('E_SPEC_DSTAR')
 ds=pr['dstar'];Ud=rat(pr.get('Ud'),'E_SPEC_UD');De=rat(pr.get('Delta_edge'),'E_SPEC_DELTA_EDGE')
 if t!=1:raise Fail('E_SPEC_T_NOT_ONE')
 rel={'Ud > 0':Ud>0,'Delta_edge > 0':De>0,'dstar >= 1':ds>=1,'r == epsilon_r - 2 lambda_R':r==er-2*lR,'sigma == 3 lambda_R - epsilon_r':s==3*lR-er,'A == Delta_edge + 2 Ud (5 - 2 dstar)':A==De+2*Ud*(5-2*ds),'a_eff == A - 2 sigma':a==A-2*s,'r > 0':r>0,'sigma > 0':s>0,'lambda_R > 0':lR>0}
 for k,v in rel.items():
  if not v:raise Fail('E_SPEC_RELATION:'+k)
 ch=d.get('checks')
 if not isinstance(ch,dict) or not all(k in ch and type(ch[k]) in (int,float) and math.isfinite(ch[k]) and ch[k]>0 for k in CHECK_KEYS):raise Fail('E_SPEC_CHECKS')
 return b,d,{'a':a,'r':r,'sigma':s,'A':A,'lambda_R':lR,'epsilon_r':er,'dstar':ds,'Ud':Ud,'Delta_edge':De},{k:float(ch[k]) for k in CHECK_KEYS},rel
# ---------------- native assembly ----------------
def index(ell,n,L):return ell*2*L+(n%(2*L))
def q_sites(L):return [index(0,0,L),index(1,0,L),index(0,2,L),index(1,2,L)]
def scalar(bits,p):
 u,v,qo0,qo1,qn0,qn1=bits
 return p['A']*(u+v)+p['r']*(qo0+qo1+qn0+qn1)-(p['r']+p['sigma'])*(u*(qo0+qo1)+v*(qn0+qn1))
def assemble(L,bits,p):
 if L<2:raise Fail('E_L_TOO_SMALL')
 N=4*L;adj=np.zeros((N,N))
 for ell in (0,1):
  for n in range(2*L):
   i,j=index(ell,n,L),index(ell,n+1,L);adj[i,j]=adj[j,i]=1.0
 if bits[0]:i,j=index(0,0,L),index(1,0,L);adj[i,j]=adj[j,i]=1.0
 if bits[1]:i,j=index(0,2,L),index(1,2,L);adj[i,j]=adj[j,i]=1.0
 c=scalar(bits,p);M=-adj+float(c)*np.eye(N)
 return M,c  # the exact rational scalar is reported with its float64 rounding error (frozen values are not all dyadic)
def contact(k,L):
 """Return None for identity (bridge flip) or the carrier site index for a Bind flip."""
 return None if k<2 else q_sites(L)[k-2]
def apply_contact(k,L,vec):
 s=contact(k,L)
 if s is None:return vec.copy()
 out=np.zeros_like(vec);out[s]=vec[s];return out
def flip(bits,k):b=list(bits);b[k]^=1;return tuple(b)
def analytic_lambda(L):
 f=lambda k:2*math.sinh(k)*math.tanh(L*k)-1
 lo,hi=0.0,1.0
 while f(hi)<=0:hi*=2
 for _ in range(200):
  mid=0.5*(lo+hi)
  if f(mid)>0:hi=mid
  else:lo=mid
 k=0.5*(lo+hi);return {'k_L':k,'lambda_L':2*math.cosh(k),'method':'bisection on 2 sinh(k) tanh(L k) = 1'}
# ---------------- generic engine ----------------
def eig(M):
 w,V=np.linalg.eigh(M);N=M.shape[0];norm=max(float(np.max(np.abs(w))),1.0)
 res=np.linalg.norm(M@V-V*w,axis=0);orth=float(np.max(np.abs(V.T@V-np.eye(N))))
 return w,V,res,norm,orth,res+4*N*EPS*norm
def endpoint(M,checks):
 w,V,res,norm,orth,err=eig(M);phi=V[:,0].copy()
 if phi.sum()<0:phi=-phi
 simple=len(w)<2 or (w[1]-w[0])>checks['minimum_numerical_denominator_margin']+err[0]+err[1]
 return {'E':float(w[0]),'phi':phi,'err':float(err[0]),'eigenvalues':w,'residual_rel_max':float(np.max(res)/norm),'orthogonality_max_abs':orth,
  'checks':{'eigen_residual':bool(np.max(res)/norm<=checks['endpoint_eigen_residual_relative_tolerance']),'orthogonality':orth<=checks['endpoint_orthogonality_absolute_tolerance'],'positive_phase':bool(phi.min()>0),'simple':bool(simple)}}
def contract_literal(start,start_bits,end,R,L):
 contribs=[]
 for perm in itertools.permutations(range(6)):
  v=start;bits=start_bits
  for j,k in enumerate(perm):
   v=apply_contact(k,L,v);bits=flip(bits,k)
   if j<5:v=R[bits]@v
  contribs.append((perm,float(end@v)))
 return contribs
def contract_dp(start,start_bits,end,R,L):
 w={0:start}
 for size in range(1,6):
  for m in range(64):
   if bin(m).count('1')!=size:continue
   bits=start_bits
   for k in range(6):
    if m>>k&1:bits=flip(bits,k)
   acc=np.zeros_like(start)
   for k in range(6):
    if m>>k&1:acc=acc+apply_contact(k,L,w[m^(1<<k)])
   w[m]=R[bits]@acc
 return float(sum(end@apply_contact(k,L,w[63^(1<<k)]) for k in range(6)))
def agree(a,b,scale,tol):return abs(a-b)<=tol*max(abs(a),abs(b),scale)
def analyze(L,p,checks):
 Mx,cx=assemble(L,X_BITS,p);My,cy=assemble(L,Y_BITS,p)
 ex=endpoint(Mx,checks);ey=endpoint(My,checks);E1=ex['E'];N=Mx.shape[0]
 out={'L':L,'dimension':N,'dimension_is_4L':N==4*L,'E1':fin(E1),'endpoints':{}}
 for k,e,c in (('x_old',ex,cx),('y_new',ey,cy)):
  out['endpoints'][k]={'E':fin(e['E']),'E_uncertainty':fin(e['err']),'phi':flist(e['phi']),'eigenvalues':flist(e['eigenvalues']),'scalar_exact':rstr(c),'scalar_float64_rounding_error':fin(abs(float(Fraction(float(c))-c))),'residual_rel_max':fin(e['residual_rel_max']),'orthogonality_max_abs':fin(e['orthogonality_max_abs']),'checks':e['checks']}
 out['endpoint_translation_identity']={'E_y_minus_E_x':fin(ey['E']-E1),'holds_numerically':abs(ey['E']-E1)<=ex['err']+ey['err']+checks['contraction_agreement_relative_tolerance']*max(1.0,abs(E1))}
 subsets=[];R_solve={};R_spec={};resonant=False
 for m in range(1,63):
  bits=X_BITS
  for k in range(6):
   if m>>k&1:bits=flip(bits,k)
  M,c=assemble(L,bits,p);w,V,res,norm,orth,err=eig(M)
  gap=float(w[0]-E1);unc=float(err[0]+ex['err'])
  ent={'mask_from_x':m,'operations_applied_from_x':[OPS[k] for k in range(6) if m>>k&1],'bits':{'u':bits[0],'v':bits[1],'qo0':bits[2],'qo1':bits[3],'qn0':bits[4],'qn1':bits[5]},
   'scalar_exact':rstr(c),'scalar_float64':fin(float(c)),'scalar_float64_rounding_error':fin(abs(float(Fraction(float(c))-c))),'matrix':fmat(M),'eigenvalues':flist(w),'eigen_residual_rel_max':fin(float(np.max(res)/norm)),'orthogonality_max_abs':fin(orth),
   'gap_to_E1':fin(gap),'gap_uncertainty':fin(unc),'min_abs_eigenvalue_minus_E1':fin(float(np.min(np.abs(w-E1))))}
  if gap+unc<0 and float(np.min(np.abs(w-E1)))-unc>checks['minimum_numerical_denominator_margin']:ent['status']='BELOW_E1_PREMISE_VIOLATED';resonant=True
  elif gap-unc<=checks['minimum_numerical_denominator_margin']:ent['status']='RESONANT_OR_UNRESOLVED';resonant=True
  else:ent['status']='SEPARATED_NUMERICAL_EVIDENCE_ONLY'
  ent['_w']=w;ent['_V']=V;ent['_M']=M;ent['_bits']=bits
  subsets.append(ent)
 if resonant:
  for ent in subsets:
   for k in ('_w','_V','_M','_bits'):ent.pop(k)
  st='BELOW_E1_PREMISE_VIOLATED' if any(e['status']=='BELOW_E1_PREMISE_VIOLATED' for e in subsets) and not any(e['status']=='RESONANT_OR_UNRESOLVED' for e in subsets) else 'RESONANT_OR_UNRESOLVED'
  out['proper_subsets']=subsets;out['contraction']={'status':st,'C_yx':None,'C_xy':None,'note':'no inverse formed for any block (margin policy / proof premise that every intermediate block lies above E1); no pseudoinverse, dropped mode or broadening'}
  return out
 inv_ok=True
 for ent in subsets:
  w,V,M,bits=ent.pop('_w'),ent.pop('_V'),ent.pop('_M'),ent.pop('_bits')
  A_=M-E1*np.eye(N);Rs=np.linalg.solve(A_,np.eye(N));Rp=(V/(w-E1))@V.T
  rel=float(np.linalg.norm(A_@Rs-np.eye(N),2)/(np.linalg.norm(A_,2)*np.linalg.norm(Rs,2)))
  agr=float(np.max(np.abs(Rs-Rp))/np.max(np.abs(Rs)))
  negtol=checks['inverse_method_relative_tolerance']*float(np.max(np.abs(Rs)))
  ent.update({'negative_inverse_entries_beyond_tolerance':int(np.sum(Rs<-negtol)),'negative_inverse_tolerance_used':fin(negtol),'inverse_residual_rel':fin(rel),'inverse_residual_ok':rel<=checks['inverse_residual_relative_tolerance'],'inverse_solve_vs_spectral_rel':fin(agr),'inverse_methods_agree':agr<=checks['inverse_method_relative_tolerance'],
   'min_inverse_entry_solve':fin(float(Rs.min())),'min_inverse_entry_spectral':fin(float(Rp.min()))})
  inv_ok&=ent['inverse_residual_ok'] and ent['inverse_methods_agree'] and ent['negative_inverse_entries_beyond_tolerance']==0
  R_solve[bits]=Rs;R_spec[bits]=Rp
 out['proper_subsets']=subsets
 px,py=ex['phi'],ey['phi']
 lit_yx=contract_literal(px,X_BITS,py,R_solve,L);lit_xy=contract_literal(py,Y_BITS,px,R_solve,L)
 tot={'C_yx_literal_solve':math.fsum(c for _,c in lit_yx),'C_yx_dp_solve':contract_dp(px,X_BITS,py,R_solve,L),'C_yx_dp_spectral':contract_dp(px,X_BITS,py,R_spec,L),
  'C_xy_literal_solve':math.fsum(c for _,c in lit_xy),'C_xy_dp_solve':contract_dp(py,Y_BITS,px,R_solve,L),'C_xy_dp_spectral':contract_dp(py,Y_BITS,px,R_spec,L)}
 scale_yx=math.fsum(abs(c) for _,c in lit_yx);scale_xy=math.fsum(abs(c) for _,c in lit_xy);tol=checks['contraction_agreement_relative_tolerance']
 cmp={}
 for name,a_,b_,sc in (('literal_vs_dp_yx',tot['C_yx_literal_solve'],tot['C_yx_dp_solve'],scale_yx),('solve_vs_spectral_dp_yx',tot['C_yx_dp_solve'],tot['C_yx_dp_spectral'],scale_yx),
   ('literal_vs_dp_xy',tot['C_xy_literal_solve'],tot['C_xy_dp_solve'],scale_xy),('solve_vs_spectral_dp_xy',tot['C_xy_dp_solve'],tot['C_xy_dp_spectral'],scale_xy),
   ('hermiticity_C_yx_vs_C_xy',tot['C_yx_literal_solve'],tot['C_xy_literal_solve'],max(scale_yx,scale_xy))):
  cmp[name]={'a':fin(a_),'b':fin(b_),'absolute_discrepancy':fin(abs(a_-b_)),'agree_within_tolerance':bool(agree(a_,b_,sc,tol))}
 canon=(1,4,5,2,3,0)  # add new bridge, Bind qn0, Bind qn1, Bind qo0, Bind qo1, remove old bridge
 cval=[c for perm,c in lit_yx if perm==canon][0]
 neg=[c for _,c in lit_yx+lit_xy if c<0];negtol=checks['contraction_agreement_relative_tolerance']*max(scale_yx,scale_xy)
 C=tot['C_yx_literal_solve']
 out['contraction']={'status':'EVALUATED_NUMERICAL_EVIDENCE_ONLY','definition':'C_yx = sum_pi <phi_y|O6 R5 O5 R4 O4 R3 O3 R2 O2 R1 O1|phi_x>; [h^2 g^4]<y|F(E1)|x> = -C_yx',
  'totals':{k:fin(v) for k,v in tot.items()},'comparisons':cmp,'C_yx':fin(C),'C_xy':fin(tot['C_xy_literal_solve']),'coefficient_of_h2g4_in_offdiagonal_F':fin(-C),
  'all_inverse_checks_ok':bool(inv_ok),'contributions_yx':[{'ordering':[OPS[k] for k in perm],'value':fin(c)} for perm,c in lit_yx],
  'contributions_xy':[{'ordering':[OPS[k] for k in perm],'value':fin(c)} for perm,c in lit_xy],
  'negative_contributions':{'count':len(neg),'min':fin(min(neg)) if neg else None,'count_beyond_tolerance':sum(1 for c in neg if c<-negtol),'tolerance_used':fin(negtol),'note':'not clipped; theory gives nonnegative summands; negatives within tolerance of the summed magnitudes are reported only (numerical zero of disconnected blocks)'},
  'strictness_ordering':{'ordering':[OPS[k] for k in canon],'value':fin(cval),'positive':cval>0},
  'C_yx_positive':C>0}
 return out
# ---------------- per case (native) ----------------
def run_case(L,p,checks,dfam):
 res=analyze(L,p,checks)
 try:post(res,L,p,checks,dfam)
 except Exception as e:res['post_analysis_error']={'type':type(e).__name__,'message':str(e)[:300]}
 return res
def post(res,L,p,checks,dfam):
 lam=analytic_lambda(L);E1a=float(p['a'])-lam['lambda_L']
 res['E1_analytic']={'a_eff_minus_lambda_L':fin(E1a),'analytic':{k:(fin(v) if isinstance(v,float) else v) for k,v in lam.items()},'agrees':abs(res['E1']-E1a)<=checks['contraction_agreement_relative_tolerance']*max(1.0,abs(E1a))+res['endpoints']['x_old']['E_uncertainty']}
 gaps=[e['gap_to_E1'] for e in res['proper_subsets']]
 res['family_gap']={'Delta_family_bound_G':fin(dfam),'min_intermediate_gap':fin(min(gaps)),'all_intermediate_gaps_at_least_bound':all(g>=dfam-e['gap_uncertainty'] for g,e in zip(gaps,res['proper_subsets']))}
 c=res['contraction']
 if c['status']=='EVALUATED_NUMERICAL_EVIDENCE_ONLY':
  ceil=720.0/dfam**5
  c['ceiling']={'value_720_over_Delta_family_pow5':fin(ceil),'C_yx_within_ceiling':c['C_yx']<=ceil,'note':'sufficient norm ceiling, not an evaluated value'}
  c['tail_inequality_symbolic']={'statement':'choose h = s h0, g = s g0 (h0, g0 nonzero), v0 = L|h0| + 4L|g0|; s > 0 with s v0 < Delta/4 and s^2 v0^8 / [Delta^7 (1 - s^2 v0^2 / Delta^2)] < h0^2 g0^4 C_yx',
   'global_remainder_bound':'|<y|F(E1)|x> + h^2 g^4 C_yx| <= v^8 / [Delta^7 (1 - (v/Delta)^2)],  v = L|h| + 4L|g| (or L|h| + |g|), v < Delta/4',
   'inserted':{'L':L,'Delta_family':fin(dfam),'C_yx':c['C_yx']},'note':'global sufficient bounds from the proof; no threshold evaluated; h, g are not chosen'}
# ---------------- I/O ----------------
def journal_line(f,obj):f.write(json.dumps(obj,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
def say(obj):print(json.dumps(obj,allow_nan=False),flush=True)
def main(argv):
 if len(argv)!=5 or argv[1]!='--output' or argv[3]!='--journal':raise Fail('E_USAGE')
 outp,jp=Path(os.path.abspath(argv[2])),Path(os.path.abspath(argv[4]))
 if outp==jp or str(outp).lower()==str(jp).lower():raise Fail('E_USAGE_SAME_PATH')
 if os.path.lexists(outp) or os.path.lexists(jp):raise Fail('E_OUTPUT_EXISTS')
 t0=time.monotonic();me=Path(os.path.abspath(__file__)).read_bytes()
 sb,spec,p,checks,rel=load_spec()
 pins={'producer':{'path':os.path.abspath(__file__),'sha256':sha(me)},'spec':{'path':SPEC[0],'sha256':SPEC[1]},'freezing_document':{'path':FREEZING[0],'sha256':FREEZING[1]}}
 pinned(*FREEZING,'E_PIN_freezing_document')
 for k,(pth,h) in BOUND.items():pinned(pth,h,'E_PIN_'+k);pins[k]={'path':pth,'sha256':h}
 a=float(p['a']);dfam=min(math.sqrt(5)-2-a,a-(math.sqrt(6)-math.sqrt(5)),float(p['r']),float(p['sigma']))
 window={'lower':math.sqrt(6)-math.sqrt(5),'a_eff':a,'upper':math.sqrt(5)-2}
 window['holds']=window['lower']<a<window['upper']
 env={'python':sys.version,'executable':sys.executable,'numpy':np.__version__,'numpy_file':np.__file__,'platform':platform.platform(),'thread_env':{v:os.environ.get(v) for v in THREAD_VARS}}
 errors=[];records=[];wrec={}
 with open(jp,'x') as jf:
  journal_line(jf,{'event':'START','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pins':pins,'environment':env,'case_ids':CASE_IDS})
  say({'event':'START','case_ids':CASE_IDS})
  for cid,L in zip(CASE_IDS,[4,6]):
   W=[]
   try:
    with warnings.catch_warnings(record=True) as W:
     warnings.simplefilter('always')
     with np.errstate(all='warn'):r=run_case(L,p,checks,dfam)
    r['status']='COMPUTED'
    if 'post_analysis_error' in r:r['status']='COMPUTED_WITH_POST_ANALYSIS_ERROR';errors.append({'case_id':cid,'stage':'post_analysis',**r['post_analysis_error']})
   except Exception as e:
    r={'status':'CASE_ERROR','error':{'type':type(e).__name__,'message':str(e)[:300]}};errors.append({'case_id':cid,**r['error']})
   wrec[cid]={'count':len(W),'entries':[{'category':w.category.__name__,'message':str(w.message)[:200],'line':w.lineno} for w in W][:50]}
   r={'case_id':cid,**r};records.append(r)
   summ={'status':r['status']}
   if 'contraction' in r:summ.update(contraction_status=r['contraction']['status'],C_yx=r['contraction'].get('C_yx'))
   journal_line(jf,{'event':'CASE','case_id':cid,'summary':summ})
   say({'event':'CASE','case_id':cid,'status':r['status']})
  cf=[]
  for r in records:
   if r['status']=='CASE_ERROR':continue
   for k,e in r['endpoints'].items():
    for ck,ok in e['checks'].items():
     if not ok:cf.append({'case_id':r['case_id'],'endpoint':k,'check':ck})
   if not r['endpoint_translation_identity']['holds_numerically']:cf.append({'case_id':r['case_id'],'check':'endpoint_translation_identity'})
   if not r['dimension_is_4L']:cf.append({'case_id':r['case_id'],'check':'dimension_is_4L'})
   c=r['contraction']
   if c['status']=='EVALUATED_NUMERICAL_EVIDENCE_ONLY':
    if not c['all_inverse_checks_ok']:cf.append({'case_id':r['case_id'],'check':'inverse_residual_or_methods'})
    for n,v in c['comparisons'].items():
     if not v['agree_within_tolerance']:cf.append({'case_id':r['case_id'],'check':n})
    if not c['strictness_ordering']['positive']:cf.append({'case_id':r['case_id'],'check':'strictness_ordering_positive'})
    if not c['C_yx_positive']:cf.append({'case_id':r['case_id'],'check':'C_yx_positive'})
    if c['negative_contributions']['count_beyond_tolerance']:cf.append({'case_id':r['case_id'],'check':'negative_contributions_beyond_tolerance'})
   if 'post_analysis_error' in r:cf.append({'case_id':r['case_id'],'check':'post_analysis_error'});continue
   if not r['E1_analytic']['agrees']:cf.append({'case_id':r['case_id'],'check':'E1_analytic'})
   if not r['family_gap']['all_intermediate_gaps_at_least_bound']:cf.append({'case_id':r['case_id'],'check':'intermediate_gap_vs_Delta_family'})
   if c['status']=='EVALUATED_NUMERICAL_EVIDENCE_ONLY' and not c['ceiling']['C_yx_within_ceiling']:cf.append({'case_id':r['case_id'],'check':'ceiling'})
  if not window['holds']:cf.append({'check':'window_W'})
  status='COMPLETED' if not errors else 'FAILED'
  out={'schema':'BIND_COUPLING_REFERENCE_OUTPUT_V002','status':status,'status_meaning':'COMPLETED = computation finished; NOT a scientific pass','case_ids':CASE_IDS,'cases':records,'errors':errors,'check_failures':cf,
   'full_parent_ready':False,'frozen':{'coordinates':{k:rstr(v) if isinstance(v,Fraction) else v for k,v in p.items()},'relations_checked':rel,'window_W':window,'Delta_family_bound_G':dfam,'checks':checks},
   'labels':{'evidence':'NUMERICAL_EVIDENCE_ONLY','scope':'restricted fixed-energy Feshbach coefficient of a reviewed native coupling; h, g factored out; not motion, gravity sign, distance/clock normalization or DM/DE','energy_map':'F(E1) is not an exact time generator; actual cluster energies need F(E)u = Eu'},
   'pins':pins,'environment':env,'floating_point_warnings_captured':wrec,
   'resources':{'elapsed_seconds':time.monotonic()-t0,'peak_rss_self_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}}
  b=(json.dumps(out,allow_nan=False,indent=1)+'\n').encode()
  with open(outp,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
  for _d in sorted({str(outp.parent),str(jp.parent)}):
   try:
    dfd=os.open(_d,os.O_RDONLY)
    try:os.fsync(dfd)
    finally:os.close(dfd)
   except OSError:pass
  journal_line(jf,{'event':'END','status':status,'output_sha256':sha(b),'output_bytes':len(b)})
 say({'event':'TERMINAL','status':status,'case_ids':CASE_IDS,'full_parent_ready':False,'output_sha256':sha(b)})
 return 0 if status=='COMPLETED' else 1
if __name__=='__main__':
 try:sys.exit(main(sys.argv))
 except Fail as e:say({'event':'TERMINAL','status':'FAILED','code':str(e),'case_ids':CASE_IDS,'full_parent_ready':False});sys.exit(2)
 except Exception as e:say({'event':'TERMINAL','status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__,'case_ids':CASE_IDS,'full_parent_ready':False});sys.exit(3)
