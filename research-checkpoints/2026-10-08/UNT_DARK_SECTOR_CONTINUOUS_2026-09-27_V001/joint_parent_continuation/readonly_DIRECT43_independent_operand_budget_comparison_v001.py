"""HELD exact-rational finite-input budgets; root alone binds/runs.
Only saved primitives/public headers and authenticated dyadic scalar defects.
No original floating kernel, producer, current, physical or circle admission.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import ast,hashlib,itertools,json,math,os,struct,sys,traceback,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
READER=('readonly_DIRECT43_exact_dyadic_axisymmetry_certificate_v003.py','41e995d38f1d6966b061f23aa3894a9c53a4a788ceaaa52dbbe1ab04d3288ab7')
READER_NAMES=('verified','metadata','thin','member','at','read_event','serial','publish')
DIAGNOSTIC=('ROOT_DIRECT43_EXACT_DYADIC_COMPATIBILITY_GAUGE_DEFECTS_V001.json','9cc04123499c2d9009559fb12f34e99413bbb4ac5fda1ddc900f8e971cf0c17d','CLOSED_DIRECT43_EXACT_DYADIC_COMPATIBILITY_AND_GAUGE_DEFECTS_MEASURED')
SOURCE_AUDIT=('OBSERVER_DIRECT43_INDEPENDENT_FORWARD_ARITHMETIC_AND_INVERSE_BOUND_SOURCE_AUDIT_V001.json','7447c49aec662c655481f7acb9af9c1cf1702da810d5c5d5251a498b615b37e0')
BASELINE_TERMINAL=None
ROOT_RELEASE=None
PROTOCOL='DIRECT43_INDEPENDENT_OPERAND_BUDGET_COMPARISON_V001.md'
PROTOCOL_SHA=None
OUTPUT_FILE=None
VERIFIED={};STATS={};np=None
U=F(1,2**53);ETA=F(1,2**1075)
MAX_FINITE=F(2**1024-2**971)
STAGE_FIELDS=('seed_connection_defect','owned_connection_defect','connection_sum_defect','recovery_defect_phi','inverse_jet_defect_phi')
TOTAL_FIELDS=('actual_chart_dg_phi','actual_lapse_phi','actual_shift_phi')

def initialize_reader():
 p=BASE/READER[0];before=p.stat();raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==READER[1] and not before.st_mode&0o222
 tree=ast.parse(raw);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 assert all(n in defs for n in READER_NAMES) and 'exact_certificate' not in READER_NAMES and 'main' not in READER_NAMES
 constants={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('RAW_FIELDS','PAIR_FIELDS','PINS')}
 assert set(constants)=={'RAW_FIELDS','PAIR_FIELDS','PINS'};globals().update(constants)
 exec(compile(ast.Module(body=[defs[n] for n in READER_NAMES],type_ignores=[]),str(p),'exec'),globals())
 after=p.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode);verified(*READER)

def rational_tree(value):
 if isinstance(value,dict) and set(value)=={'numerator','denominator'}:
  assert isinstance(value['numerator'],str) and isinstance(value['denominator'],str);d=int(value['denominator']);assert d>0;return F(int(value['numerator']),d)
 if isinstance(value,list):return [rational_tree(v) for v in value]
 if isinstance(value,dict):return {n:rational_tree(v) for n,v in value.items()}
 return value

def budget_data(a,residual):
 # This function accepts no observed stage defect. Every allowance is operand-only.
 g,I,Cs,Co,Gs,Go,G,D,J=(a[n] for n in ('source_g','source_hi','seed_dg_operand','owned_increment_dg','seed_Gamma_operand','owned_Gamma_increment','owned_Gamma','chart_dg','chart_dhi'))
 for A in (g,I):assert all(at(A,i,j)==at(A,j,i) for i in range(4) for j in range(4))
 assert all(at(C,3,i,j)==0 for C in (Cs,Co) for i in range(4) for j in range(4))
 assert len(residual)==4 and all(len(row)==4 and all(isinstance(v,F) for v in row) for row in residual)
 peaks=[]
 def add(x,ex,y,ey):
  z=x+y;b=ex+ey;e=b+U*(abs(z)+b)+ETA;peaks.append(abs(z)+e);return z,e
 def multiply(x,ex,y,ey):
  z=x*y;b=abs(x)*ey+abs(y)*ex+ex*ey;e=b+U*(abs(z)+b)+ETA;peaks.append(abs(z)+e);return z,e
 def product(values):
  cases=[]
  for order in itertools.permutations(values):
   x,e=order[0],F(0)
   for y in order[1:]:x,e=multiply(x,e,y,F(0))
   cases.append((x,e))
  assert all(x==cases[0][0] for x,e in cases);return cases[0][0],max(e for x,e in cases)
 def sum_terms(terms):
  # Every binary summation tree has depth <=n-1; additive eta covers subnormals.
  n=len(terms);center=sum((x for x,e in terms),F(0));amp=sum((abs(x) for x,e in terms),F(0));errors=sum((e for x,e in terms),F(0));factor=(1+U)**max(0,n-1)
  radius=factor*errors+(factor-1)*amp+max(0,n-1)*factor*ETA;peaks.append(amp+radius);return center,radius
 def half(x,e):
  z=x/2;b=e/2;r=b+U*(abs(z)+b)+ETA;peaks.append(abs(z)+r);return z,r
 def amplitude(C,l,m):return abs(at(C,3,m,l))+abs(at(C,m,3,l))+abs(at(C,l,3,m))
 def gamma_branch(C):
  centers=[];radii=[];amps=[]
  for k in range(4):
   cr=[];er=[];ar=[]
   for m in range(4):
    terms=[]
    for l in range(4):
     x,e=add(at(C,3,m,l),F(0),at(C,m,3,l),F(0));x,e=add(x,e,-at(C,l,3,m),F(0));terms.append(multiply(at(I,k,l),F(0),x,e))
    x,e=sum_terms(terms);x,e=half(x,e);cr.append(x);er.append(e);ar.append(sum((abs(at(I,k,l))*amplitude(C,l,m)/2 for l in range(4)),F(0)))
   centers.append(cr);radii.append(er);amps.append(ar)
  return centers,radii,amps
 sc,es,sa=gamma_branch(Cs);oc,eo,oa=gamma_branch(Co)
 ez=[[U*(abs(at(Gs,k,3,m))+abs(at(Go,k,3,m)))+ETA for m in range(4)] for k in range(4)]
 eg=[[es[k][m]+eo[k][m]+U*(sa[k][m]+oa[k][m]+es[k][m]+eo[k][m])+ETA for m in range(4)] for k in range(4)]
 for k in range(4):
  for m in range(4):peaks.append(sa[k][m]+oa[k][m]+eg[k][m])
 ac=[[sum_terms([product((at(G,l,3,m),at(g,l,n))) for l in range(4)]) for n in range(4)] for m in range(4)]
 er=[[add(ac[m][n][0],ac[m][n][1],ac[n][m][0],ac[n][m][1])[1] for n in range(4)] for m in range(4)]
 compatibility=[[sum((abs(residual[n][l])*(amplitude(Cs,l,m)+amplitude(Co,l,m))+abs(residual[m][l])*(amplitude(Cs,l,n)+amplitude(Co,l,n)) for l in range(4)),F(0))/2 for n in range(4)] for m in range(4)]
 bd=[[compatibility[m][n]+sum((eg[l][m]*abs(at(g,l,n))+eg[l][n]*abs(at(g,l,m)) for l in range(4)),F(0))+er[m][n] for n in range(4)] for m in range(4)]
 ei=[[sum_terms([product((at(I,i,k),at(D,3,k,l),at(I,l,j))) for k in range(4) for l in range(4)])[1] for j in range(4)] for i in range(4)]
 bj=[[sum((abs(at(I,i,k))*bd[k][l]*abs(at(I,l,j)) for k in range(4) for l in range(4)),F(0))+ei[i][j] for j in range(4)] for i in range(4)]
 N=at(a['source_N']);assert N>0;na=at(a['genuine_N_jets'],3)
 cube,ecube=product((N,N,N));lapse,elapse=multiply(cube,ecube,at(J,3,0,0),F(0));lapse,en=half(lapse,elapse)
 eb=[]
 for i in range(3):
  x,e=multiply(F(2),F(0),N,F(0));x,e=multiply(x,e,na,F(0));x,e=multiply(x,e,at(I,0,i+1),F(0))
  y,ey=product((N,N));y,ey=multiply(y,ey,at(J,3,0,i+1),F(0));eb.append(add(x,e,y,ey)[1])
 bn=N**3*bj[0][0]/2+en;bb=[2*N*bn*abs(at(I,0,i+1))+N**2*bj[0][i+1]+eb[i] for i in range(3)]
 r=max(sum((abs(v) for v in row),F(0)) for row in residual);ni=max(sum((abs(at(I,i,j)) for j in range(4)),F(0)) for i in range(4));ng=max(sum((abs(at(g,i,j)) for j in range(4)),F(0)) for i in range(4))
 return dict(stage={STAGE_FIELDS[0]:es,STAGE_FIELDS[1]:eo,STAGE_FIELDS[2]:ez,STAGE_FIELDS[3]:er,STAGE_FIELDS[4]:ei,'lapse_jet_defect_phi':en,'shift_jet_defect_phi':eb},total={'actual_chart_dg_phi':bd,'inverse_jet_actual_phi':bj,'actual_lapse_phi':bn,'actual_shift_phi':bb},compatibility=compatibility,range_bound=max(peaks),basic_operation_range_bound_valid=max(peaks)<=MAX_FINITE,conditioning=dict(residual_infinity_norm=r,strict_neumann_margin=1-r,represented_inverse_bound_valid=r<1,inverse_norm_upper=ni/(1-r) if r<1 else None,inverse_error_norm_upper=ni*r/(1-r) if r<1 else None,condition_infinity_upper=ng*ni/(1-r) if r<1 else None),cube_reference_is_two_multiplication_graph_not_original_pow_theorem=True)

def compare_event(a,measured,budget):
 checks=[]
 def compare(name,actual,bound):
  if isinstance(bound,list):
   assert isinstance(actual,list) and len(actual)==len(bound)
   for i,(v,b) in enumerate(zip(actual,bound)):compare(name+'_'+str(i),v,b)
  else:
   assert isinstance(actual,F) and isinstance(bound,F) and bound>=0;checks.append(dict(name=name,actual=actual,independent_budget=bound,within_budget=abs(actual)<=bound))
 for n,b in budget['stage'].items():compare('stage_'+n,measured[n],b)
 for n,b in budget['total'].items():
  actual=([[at(a['chart_dhi'],3,i,j) for j in range(4)] for i in range(4)] if n=='inverse_jet_actual_phi' else measured[n]);compare('total_'+n,actual,b)
 expected=84+36;assert len(checks)==expected and len({q['name'] for q in checks})==expected
 return dict(checks=checks,comparison_count=len(checks),all_stage_defects_within_declared_model_budgets=all(q['within_budget'] for q in checks if q['name'].startswith('stage_')),all_total_words_within_independent_enclosures=all(q['within_budget'] for q in checks if q['name'].startswith('total_')),raw_exact_zero_flag=measured['raw_exact_zero_flag'],raw_gauge_phi_words_hex=measured['raw_gauge_phi_words_hex'],raw_chart_phi_words_hex=measured['raw_chart_phi_words_hex'],genuine_time_words_hex=measured['genuine_time_words_hex'])

def main():
 global np
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and isinstance(ROOT_RELEASE,dict) and isinstance(BASELINE_TERMINAL,tuple) and len(BASELINE_TERMINAL)==4 and all(v is not None for t in BASELINE_TERMINAL for v in t)
 assert PROTOCOL_SHA is not None and isinstance(OUTPUT_FILE,str) and OUTPUT_FILE.endswith('.json') and '/' not in OUTPUT_FILE and not (BASE/OUTPUT_FILE).exists() and not list(BASE.glob(OUTPUT_FILE[:-5]+'_*.json'))
 assert ROOT_RELEASE['closed_baseline_and_diagnostic_seals_verified'] is True and ROOT_RELEASE['root_only_execution'] is True
 initialize_reader();verified(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());verified(PROTOCOL,PROTOCOL_SHA);audit=metadata(*SOURCE_AUDIT);diagnostic=metadata(*DIAGNOSTIC[:2])
 assert diagnostic['status']==DIAGNOSTIC[2] and diagnostic['baseline_terminal']==json.loads(json.dumps(BASELINE_TERMINAL)) and diagnostic['event_count']==len(diagnostic['rows'])==43
 for n in ('all_selected_byte_seals_verified','all_exact_dyadic_defect_identities_verified','raw_flags_and_words_preserved','source_phi_input_exact_zero'):assert diagnostic[n] is True
 for n in ('apriori_roundoff_model_or_inverse_conditioning_qualified','axisymmetry_precision_admitted','exact132_axisymmetry_guard_promoted','physical_or_velocity_adoption','original_bodies_or_controls_replayed'):assert diagnostic[n] is False
 for n,h in PINS.items():verified(n,h);assert diagnostic['source_pins'][n]==audit['source_pins'][n]==h
 source,result,receipt,custody=BASELINE_TERMINAL
 for t in BASELINE_TERMINAL:verified(*t[:2])
 r=metadata(*result[:2]);rc=metadata(*receipt[:2]);proof=metadata(*custody[:2]);owner=rc['owner']
 assert source==('direct43_original_baseline_preparation_v003.py','68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336') and owner==r['owner']==proof['owner']==diagnostic['baseline_owner'] and owner['pid']==1071 and owner['source_sha256']==source[1]
 assert r['status']==result[2]=='DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED' and rc['status']==receipt[2]=='CLOSED' and rc['result_sha256']==result[1] and rc['error_sha256'] is None
 assert proof['status']==custody[2] and proof['source_sha256']==source[1] and proof['result_sha256']==result[1] and proof['receipt_sha256']==receipt[1] and proof['naturally_closed'] is True and proof['exit_code']==0
 assert all(proof[n] is True for n in ('all_input_seals_verified','all_output_seals_verified','all_success_role_seals_verified','full87_preparation_completed')) and proof['science_role_count']==proof['total_records']==87
 assert proof['input_count']==len(rc['input_sha256'])==41 and proof['output_count']==len(rc['output_sha256'])==177
 assert proof['events']==r['case']['events'] and len(r['checkpoints'])==len(proof['records'])==87 and r['controls']==proof['controls']==[] and r['qualification']==rc['qualification']==proof['qualification'] and all(v is False for v in rc['qualification'].values())
 import numpy as numpy
 np=numpy;rows=[];completed=[];context={};analysis_owner=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 try:
  for i,event in enumerate(r['case']['events']):
   ref=event['reference_event'];context=dict(index=i,R=event['R'],reference_event=ref);row=diagnostic['rows'][i]
   assert event['index']==row['index']==i and event['R']==row['R'] and ref==row['reference_event']==thin(r['checkpoints'][2*i+1])==thin(proof['records'][2*i+1])
   a,md=read_event(ref,i,owner,rc);assert md['R']==row['R'] and md['axisymmetric_gauge_phi_exact_zero']==row['raw_exact_zero_flag']
   assert {n:v['member_sha256'] for n,v in a.items()}==row['source_member_payload_sha256']
   residual=rational_tree(row['raw_inverse_compatibility']);budget=budget_data(a,residual);measured=rational_tree(row);comparison=compare_event(a,measured,budget)
   certificate=dict(index=i,R=row['R'],reference_event=ref,conditioning=budget['conditioning'],basic_operation_range_bound_valid=budget['basic_operation_range_bound_valid'],range_bound=budget['range_bound'],comparison=comparison,model='Exact operand-only RN-binary64 graph budget with gradual-underflow eta; any binary summation tree. Cube comparison uses two-multiplication reference, not a verified original pow theorem.',installed_kernel_rounding_contract_verified=False,universal_apriori_roundoff_qualified=False,physical_or_circle_admission=False)
   completed.append(publish(OUTPUT_FILE[:-5]+'_%02d_EVENT.json'%i,dict(analysis_owner=analysis_owner,baseline_owner=owner,certificate=certificate)));rows.append(certificate)
 except BaseException:
  publish(OUTPUT_FILE[:-5]+'_ERROR.json',dict(status='FAILED_INDEPENDENT_BUDGET_COMPARISON_PREFIX_PRESERVED',analysis_owner=analysis_owner,context=context,completed_event_certificates=completed,input_sha256=VERIFIED,traceback=traceback.format_exc(),raw_words_projected_to_zero=False,physical_or_circle_admission=False));raise
 for name,identity in STATS.items():
  s=Path(name).stat();assert identity==(s.st_ino,s.st_size,s.st_mtime_ns,s.st_mode)
 out=dict(status='CLOSED_DIRECT43_INDEPENDENT_OPERAND_BUDGET_COMPARISONS_MEASURED',analysis_owner=analysis_owner,baseline_owner=owner,baseline_terminal=BASELINE_TERMINAL,diagnostic=DIAGNOSTIC,source_audit=SOURCE_AUDIT,event_count=len(rows),comparison_count=sum(v['comparison']['comparison_count'] for v in rows),completed_event_certificates=completed,rows=rows,all_stage_defects_within_declared_model_budgets=all(v['comparison']['all_stage_defects_within_declared_model_budgets'] for v in rows),all_total_words_within_independent_enclosures=all(v['comparison']['all_total_words_within_independent_enclosures'] for v in rows),all_basic_operation_range_bounds_valid=all(v['basic_operation_range_bound_valid'] for v in rows),all_represented_inverse_Neumann_bounds_valid=all(v['conditioning']['represented_inverse_bound_valid'] for v in rows),raw_flags_and_words_preserved=True,roundoff_origin_uniquely_proved=False,installed_kernel_rounding_contract_verified=False,universal_apriori_roundoff_qualified=False,unrounded_metric_source_uncertainty_qualified=False,exact132_axisymmetry_guard_promoted=False,geodesic_accuracy_budget_supplied=False,physical_or_velocity_adoption=False,original_floating_kernels_or_producers_replayed=False,input_sha256=VERIFIED,stable_stats=STATS,qualification=rc['qualification'])
 out['finite_input_declared_model_comparisons_all_passed']=out['all_stage_defects_within_declared_model_budgets'] and out['all_total_words_within_independent_enclosures'] and out['all_basic_operation_range_bounds_valid']
 answer=publish(OUTPUT_FILE,out);print(json.dumps(dict(answer,events=43,finite_input_model_comparisons_only=True)))

if __name__=='__main__':main()
