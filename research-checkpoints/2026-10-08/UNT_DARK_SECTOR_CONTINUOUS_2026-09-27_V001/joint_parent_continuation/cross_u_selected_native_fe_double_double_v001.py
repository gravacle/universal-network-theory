"""Guarded same32-contact double-double arithmetic; no global operator or solve."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='8689dc0cbd7c4ce711359d731bb7050f9959d4e960090c50269fdf2db43599c0'
ROW_PRECISION=Decimal('1e-10')
EXPECTED_CONTROLS=15
PRIVATE_DEFINITIONS=(('author_fragment_selected_native_fe_double_double_admission_v002.txt','a99fa93b541f2b31ce9af706d8f334b4e43d590146907dbe05640faea1fcf3b6'),('author_fragment_selected_fe_dd_fixtures_v001.txt','1781720ab4be40473a94407928429f642dbb74981cd5a97323d467ef71ae33aa'))
OWNER=None;INPUTS={};OUTPUTS={};CHECKS=[];ACTIVE={};EFT_LAST={}
FLAGS=dict(original_canonical_admission=False,physical_rate_adoption=False,normal_constraint_seed=False,metric_adoption=False,galaxy_prediction=False,global_operator_adoption=False)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(n)==h,n;INPUTS[key]=h
def publish(tag,obj):
 n=STEM+'_'+tag+'.json';raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with path(n).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path(n).chmod(0o444);assert path(n).read_bytes()==raw;OUTPUTS[n]=sha(n);return dict(file=n,sha256=OUTPUTS[n])
def recheck():
 for n,h in INPUTS.items():assert sha(n)==h,n
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(n)==h,n
def eft_capture(name,**values):
 EFT_LAST.clear();EFT_LAST.update(operation=name,values={k:float(v).hex() for k,v in values.items()})
 for v in values.values():assert math.isfinite(v),(name,EFT_LAST)
def two_sum(a,b):
 # Knuth error-free addition, IEEE binary64 round-to-nearest, no overflow.
 a=float(a);b=float(b);eft_capture('two_sum_input',a=a,b=b)
 s=a+b;eft_capture('two_sum_sum',a=a,b=b,s=s)
 bb=s-a;eft_capture('two_sum_split',a=a,b=b,s=s,bb=bb)
 e=(a-(s-bb))+(b-bb);eft_capture('two_sum_result',a=a,b=b,s=s,e=e)
 return s,e
def split(a):
 # Bounded inputs make split products and every low-low product normal.
 a=float(a);eft_capture('split_input',a=a)
 assert a==0. or 2.**-450<=abs(a)<=2.**450,('Dekker_safe_operand_domain',a.hex())
 c=(2.**27+1.)*a;eft_capture('split_product',a=a,c=c)
 hi=c-(c-a);lo=a-hi;eft_capture('split_result',a=a,hi=hi,lo=lo)
 return hi,lo
def two_prod(a,b):
 a=float(a);b=float(b);eft_capture('two_prod_input',a=a,b=b)
 ah,al=split(a);bh,bl=split(b)
 p=a*b;eft_capture('two_prod_product',a=a,b=b,p=p)
 t0=ah*bh-p;eft_capture('two_prod_t0',a=a,b=b,p=p,t0=t0)
 t1=t0+ah*bl;eft_capture('two_prod_t1',a=a,b=b,p=p,t0=t0,t1=t1)
 t2=t1+al*bh;eft_capture('two_prod_t2',a=a,b=b,p=p,t1=t1,t2=t2)
 e=t2+al*bl;eft_capture('two_prod_result',a=a,b=b,p=p,e=e)
 return p,e
def dd(x):return float(x),0.
def dd_neg(a):return -a[0],-a[1]
def dd_add(a,b):
 # Retain both low words even if high words cancel; no quick-two-sum assumption.
 s,e=two_sum(a[0],b[0]);t,f=two_sum(a[1],b[1]);u,v=two_sum(e,t)
 h,w=two_sum(s,u);l0,l1=two_sum(w,v);l2,l3=two_sum(l0,f)
 tail0,tail1=two_sum(l1,l3);low0,low1=two_sum(l2,tail0)
 return two_sum(h,low0+(low1+tail1))
def dd_sub(a,b):return dd_add(a,dd_neg(b))
def dd_mul(a,b):
 # All four products preserve their low parts before cancellation.
 out=two_prod(a[0],b[0]);out=dd_add(out,two_prod(a[0],b[1]))
 out=dd_add(out,two_prod(a[1],b[0]));return dd_add(out,two_prod(a[1],b[1]))
def dd_dot(a,b):
 out=dd(0.)
 for x,y in zip(a,b):out=dd_add(out,dd_mul(x,y))
 return out
def dd_sum(a):
 out=dd(0.)
 for x in a:out=dd_add(out,x)
 return out
def decimal_value(a):return Decimal.from_float(a[0])+Decimal.from_float(a[1])
def words(a):return dict(hi=a[0].hex(),lo=a[1].hex())
def record(name,values):
 ACTIVE[name]=[words(x) for x in values];return values
def collect(name,iterator):
 out=[];ACTIVE[name]=[]
 for value in iterator:
  out.append(value);ACTIVE[name].append(words(value))
 return out
def compare_nonzero(name,a,reference):
 # True row precision; no operation envelope or numerical floor replaces |reference|.
 with localcontext() as ctx:
  ctx.prec=100;actual=decimal_value(a);expected=Decimal(reference)
  assert expected!=0,(name,'nonzero reference required')
  error=abs(actual-expected)/abs(expected)
  row=dict(name=name,actual=str(actual),expected=str(expected),relative_error=str(error),tolerance=str(ROW_PRECISION),passed=error<=ROW_PRECISION)
  CHECKS.append(row);assert row['passed'],row
def exact_fixture(name,a,reference):
 with localcontext() as ctx:
  ctx.prec=100;actual=decimal_value(a);expected=Decimal(reference)
  row=dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected,tolerance='exact synthetic identity')
  CHECKS.append(row);assert row['passed'],row

def selected_polynomial(row):
 # Every geometry factor is the immutable binary64 intermediate already selected.
 direct=centered=cs=ps=ds=dd(0.);points=[]
 for p in row['contacts']:
  ACTIVE.clear();ACTIVE.update(group=row['group'],point=p['point'],completed_points=points.copy(),row_accumulators={n:words(x) for n,x in zip(('action','centered','cn','pstar','delta'),(direct,centered,cs,ps,ds))})
  L=[[dd(x) for x in r] for r in p['L']];D=[[dd(x) for x in r] for r in p['modal_D']];B=[[dd(x) for x in r] for r in p['Bz']]
  v=collect('interpolated_native',(dd_dot([dd(x) for x in p['native_corner_values'][c]],[dd(p['native_factors'][j][c%3]) for j in range(4)]) for c in range(6)))
  k=collect('interpolated_metric',(dd_sum(dd_mul(dd(p['metric_corner_values'][a][j]),dd(p['metric_factors'][j][t][a])) for j in range(4) for a in range(6)) for t in range(6)))
  def modal(u,z,h,label):
   mixed=collect(label+'_mixed',(dd_add(z[t],dd_dot(L[t],u)) for t in range(3)))
   Dz=collect(label+'_D_mixed',(dd_dot(D[t],mixed) for t in range(3)))
   Bh=collect(label+'_B_metric',(dd_dot(B[t],h) for t in range(3)))
   return collect(label+'_momentum',(dd_add(Dz[t],Bh[t]) for t in range(3)))
  val=modal(v[:3],v[3:],k,'current');ru=[dd(x) for x in p['vstar_U']];rz=[dd(x) for x in p['vstar_Z']];rh=[dd(x) for x in p['kstar']]
  ref=modal(ru,rz,rh,'reference')
  delta=modal([dd_sub(v[t],ru[t]) for t in range(3)],[dd_sub(v[t+3],rz[t]) for t in range(3)],[dd_sub(k[t],rh[t]) for t in range(6)],'delta')
  cn=[dd(x) for x in p['cn']];star=[dd(x) for x in p['pstar']]
  defect=collect('point_reference_defect',(dd_sub(dd_add(cn[t],ref[t]),star[t]) for t in range(3)))
  momentum=collect('point_centered_momentum',(dd_add(dd_add(star[t],defect[t]),delta[t]) for t in range(3)))
  q=dd_mul(dd(p['weight64']),dd(p['scatter_factor64']));record('scatter_weight',[q])
  direct=dd_add(direct,dd_mul(q,val[0]));record('accumulated_action',[direct])
  centered=dd_add(centered,dd_mul(q,dd_sub(momentum[0],cn[0])));record('accumulated_centered_action',[centered])
  cs=dd_add(cs,dd_mul(q,cn[0]));record('accumulated_cn',[cs])
  ps=dd_add(ps,dd_mul(q,star[0]));record('accumulated_pstar',[ps])
  ds=dd_add(ds,dd_mul(q,dd_add(defect[0],delta[0])));record('accumulated_centered_delta',[ds])
  points.append(dict(point=p['point'],native_rate=[words(x) for x in v],metric_rate=[words(x) for x in k],D_mixed=ACTIVE['current_D_mixed'],B_metric=ACTIVE['current_B_metric'],current_momentum=[words(x) for x in val],reference_momentum=[words(x) for x in ref],reference_defect=[words(x) for x in defect],centered_delta=[words(x) for x in delta],centered_momentum=[words(x) for x in momentum],accumulated_action=words(direct)))
 rhs=dd(row['original_rhs']);target=dd(row['actual_Pn_target']);res=dd_sub(rhs,direct);record('original_rhs_residual',[res])
 epsilon=dd_sub(dd(row['original_float_residual']),res);record('saved_residual_minus_double_double',[epsilon])
 rhsdef=dd_sub(rhs,dd_sub(target,cs));record('frozen_rhs_defect',[rhsdef])
 targetdef=dd_sub(target,ps);record('target_scatter_defect',[targetdef])
 centered_res=dd_sub(dd_add(rhsdef,targetdef),ds);record('centered_original_residual',[centered_res])
 pnres=dd_sub(dd_sub(target,cs),direct);record('actual_Pn_point_cn_residual',[pnres])
 output=dict(action=direct,centered_action=centered,original_rhs_residual=res,saved_residual_minus_double_double=epsilon,actual_Pn_point_cn_residual=pnres,frozen_rhs_defect=rhsdef,target_scatter_defect=targetdef,centered_original_residual=centered_res)
 ACTIVE['completed_row']={n:words(v) for n,v in output.items()}
 return output,points

def encoded_result(out):
 with localcontext() as ctx:
  ctx.prec=100
  return {name:dict(words(value),decimal=str(decimal_value(value))) for name,value in out.items()}
# Private definitions only. Caller supplies EFT/DD helpers, record, exact_fixture,
# ACTIVE and CHECKS. No import, invocation or numerical evaluation by the author.
# Seven fresh gates; all constants below are artificial exact binary64 values.
# Definitions only. Caller supplies json, path, sha and bind; no old NPZ loads.
DD_PRECISION_STEM='CROSS_U_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001'
DD_PRECISION_RESULT_SHA='848c0411bab21dcdc8e4e2518cae444fd96566e264fa554ad25c9079955b4f5e'
DD_PRECISION_RECEIPT_SHA='fc9e621b17357fb23a79482e3b41ab126d5c199c6eff3492c3ec00defd281cec'
DD_PRECISION_SOURCE_SHA='30d0cc625dddc09be6e845bde409e1d244253073e4803f253b5fdab29e1e637e'
DD_PRECISION_PROTOCOL_SHA='8f8343fde9c0ca6df436bb4e9fb5cd69db80227729fee669ba060a46e21d7c6f'
DD_PRECISION_AUDIT_FILE='READONLY_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001_AUDIT_RESULT.json'
DD_PRECISION_AUDIT_SHA='0507d69496c67537b441993d794ba808c05c5de53a6af1d433f2b146906e8eff'

def dd_selected_admission():
 st=DD_PRECISION_STEM
 for n,h in ((st+'_RESULT.json',DD_PRECISION_RESULT_SHA),(st+'_RECEIPT.json',DD_PRECISION_RECEIPT_SHA),('cross_u_selected_native_fe_precision_witness_v001.py',DD_PRECISION_SOURCE_SHA),(st+'.md',DD_PRECISION_PROTOCOL_SHA),(DD_PRECISION_AUDIT_FILE,DD_PRECISION_AUDIT_SHA)):bind(n,h)
 r=json.loads(path(st+'_RESULT.json').read_text());rc=json.loads(path(st+'_RECEIPT.json').read_text());owner=r['owner']
 assert rc['status']=='CLOSED' and rc['owner']==owner and owner['owner']=='root' and owner['pid']==42546 and owner['source_sha256']==DD_PRECISION_SOURCE_SHA
 assert rc['closed']>owner['started'] and rc['result_sha256']==DD_PRECISION_RESULT_SHA and rc['error_sha256'] is None
 assert r['status']=='BOUNDED_PRECISION_WITNESS_COMPLETE' and len(r['controls'])==16 and all(q['passed'] for q in r['controls'])
 assert r['full_row_admission'] is False and r['new_operator_solve'] is False and r['qualification']==rc['qualification'] and all(q is False for q in r['qualification'].values())
 mappings={}
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in mappings or mappings[key]==h;mappings[key]=h
 assert mappings[str(path(st+'.md').resolve())]==DD_PRECISION_PROTOCOL_SHA
 for n,h in rc['output_sha256'].items():bind(n,h)
 rawref=r['point_operands'];assert set(rawref)=={'file','sha256'} and rawref['file']==st+'_POINT_OPERANDS.json'
 assert rc['output_sha256'][rawref['file']]==rawref['sha256'];raw=json.loads(path(rawref['file']).read_text())
 assert raw['owner']==owner and raw['qualification']==r['qualification'] and len(raw['selected_records'])==7 and len(raw['rows'])==len(r['rows'])==2
 expected=((10,9,0,[82,39]),(14,13,0,[84,37]));references={}
 contact_keys={'Bz','L','R','R2_64','R3_64','cell','cn','dv','hats','iq','kstar','local','metric_corner_values','metric_factors','modal_D','native_corner_values','native_factors','point','pstar','row_corner','scatter_factor64','vstar_U','vstar_Z','weight64'}
 row_keys={'actual_Pn_target','component','contacts','group','mode_index','node','original_float_action','original_float_residual','original_rhs','packed_native_index','rate','scale'}
 result_keys={'action','actual_Pn_residual','centered_action','frozen_rhs_defect','operation_envelope','original_rhs_residual','points','precision','saved_residual_minus_high_precision','scaled_original_residual','target_scatter_defect'}
 def shape(a,dims):
  if not dims:return isinstance(a,(int,float)) and not isinstance(a,bool)
  return isinstance(a,list) and len(a)==dims[0] and all(shape(x,dims[1:]) for x in a)
 for row,saved,(group,mode,component,node) in zip(raw['rows'],r['rows'],expected):
  assert set(row)==row_keys and (row['group'],row['mode_index'],row['component'],row['node'])==(group,mode,component,node)
  assert row['packed_native_index']==group*11524+(node[0]-1)*45+node[1] and len(row['contacts'])==16
  assert saved['selection']=={k:v for k,v in row.items() if k!='contacts'}
  incidence=set()
  for p in row['contacts']:
   assert set(p)==contact_keys and shape(p['cell'],(2,)) and p['iq'] in range(4) and p['row_corner'] in range(4)
   ci,cj=p['cell'];assert ci in (node[0]-1,node[0]) and cj in (node[1]-1,node[1])
   assert p['local']==44*ci+cj and p['point']==p['iq']*3784+p['local'];incidence.add((p['iq'],ci,cj))
   for n,dims in (('L',(3,3)),('modal_D',(3,3)),('Bz',(3,6)),('native_corner_values',(6,4)),('metric_corner_values',(6,4)),('native_factors',(4,3)),('metric_factors',(4,6,6)),('hats',(4,)),('cn',(3,)),('pstar',(3,)),('vstar_U',(3,)),('vstar_Z',(3,)),('kstar',(6,))):assert shape(p[n],dims),(group,n)
  assert len(incidence)==16
  n=st+'_ROW_%d_PRECISION100.json'%group;ref=json.loads(path(n).read_text())
  assert ref['owner']==owner and ref['selection']==[group,component,node] and ref['qualification']==r['qualification']
  assert ref['controls']==r['controls'][:len(ref['controls'])] and ref['result']==saved['decimal100']
  assert set(ref['result'])==result_keys and ref['result']['precision']==100 and len(ref['result']['points'])==16
  assert [p['point'] for p in ref['result']['points']]==[p['point'] for p in row['contacts']]
  references[str(group)]=ref['result']
 audit=json.loads(path(DD_PRECISION_AUDIT_FILE).read_text())
 assert audit['status']=='SAVED_PRECISION_WITNESS_AUDIT_PASS' and audit['pid']==42766 and audit['controls']==16 and audit['comparisons']==38
 assert audit['parent_terminal_status']=='CLOSED' and audit['parent_result_sha256']==DD_PRECISION_RESULT_SHA and audit['parent_receipt_sha256']==DD_PRECISION_RECEIPT_SHA and audit['parent_error_sha256'] is None
 assert audit['old_arrays_or_A_replayed'] is False and audit['polynomial_replay'] is False and audit['selected_rows_only'] is True and audit['qualification']==r['qualification']
 assert r['ancestry']['parent_nonadmission_preserved'] is True
 ancestry=dict(precision_owner=owner,precision_closed=rc['closed'],precision_input_sha256=rc['input_sha256'],precision_output_sha256=rc['output_sha256'],selected_records=raw['selected_records'],original_nonadmission=r['ancestry'],coefficient_rounding=r['coefficient_rounding'],saved_reader=dict(file=DD_PRECISION_AUDIT_FILE,sha256=DD_PRECISION_AUDIT_SHA,pid=audit['pid'],status=audit['status']),authority='The closed precision capsule and its passed saved reader authenticate the selected original binary64 operands; no original NPZ reload or full ancestral map rehash.',selected_rows_only=True,full_row_admission=False)
 return raw['rows'],references,ancestry

def fresh_dd_fixtures():
 start=len(CHECKS)
 ACTIVE['fresh_fixture_scope']='scalar EFT/DD and frozen synthetic FE only'
 # A true two-word sum must retain the unit below the binary64 high-word ulp.
 a=two_sum(2.**60,1.);record('fresh_two_sum_words',[a])
 exact_fixture('fresh_two_sum_retains_low_word',a,'1152921504606846977')
 b=dd_add(a,dd(-2.**60));record('fresh_cancelled_high_word_result',[b])
 exact_fixture('fresh_DD_high_word_cancellation',b,'1')
 # (2^53+2)(1-2^-52)-2^53=-2^-51. The multiplication low part matters.
 p=two_prod(2.**53+2.,1.-2.**-52);record('fresh_Dekker_product_words',[p])
 low=dd_sub(p,dd(2.**53));record('fresh_Dekker_exposed_low_part',[low])
 exact_fixture('fresh_Dekker_product_low_part',low,'-0.000000000000000444089209850062616169452667236328125')
 # Both low words contribute: (2^60+1)(1-2^-60)-2^60=-2^-60.
 left=two_sum(2.**60,1.);right=two_sum(1.,-2.**-60)
 record('fresh_four_product_inputs',[left,right])
 product=dd_mul(left,right);record('fresh_four_product_result',[product])
 remainder=dd_sub(product,dd(2.**60));record('fresh_four_product_low_remainder',[remainder])
 exact_fixture('fresh_DD_all_four_products_survive_cancellation',remainder,'-0.000000000000000000867361737988403547205962240695953369140625')
 # Fresh FE geometry: R=4, four N=1/4, so frozen R^2*N=4.
 # Four phi coefficients (2^60,1,-2^60,1) produce exactly8, including low words.
 ACTIVE['fresh_covector_phi_geometry']=dict(R64=4.,R2_64=16.,hat64=.25,factor64=4.)
 phi=dd_dot([dd(2.**60),dd(1.),dd(-2.**60),dd(1.)],[dd(4.)]*4)
 record('fresh_phi_FE_cancellation_words',[phi])
 exact_fixture('fresh_frozen_covector_phi_FE_cancellation',phi,'8')
 # Fresh radial scatter: dv=8,R=4,hat=1/4 -> q=1/2, once.
 # The exposed product low part above scatters to -2^-52, rather than zero.
 ACTIVE['fresh_radial_scatter_geometry']=dict(dv64=8.,R64=4.,weight64=2.,hat64=.25)
 q=dd_mul(dd(2.),dd(.25));record('fresh_radial_scatter_weight',[q])
 row=dd_mul(q,low);record('fresh_radial_scattered_low_part',[row])
 exact_fixture('fresh_frozen_FE_weight_retains_product_low_part',row,'-0.0000000000000002220446049250313080847263336181640625')
 # Refusal is part of this deliberately restricted EFT interface, not truncation.
 refused=0;cases=[]
 for x in (2.**-451,2.**451):
  try:split(x)
  except AssertionError:
   refused+=1;cases.append(dict(operand_hex=x.hex(),refused=True))
  else:cases.append(dict(operand_hex=x.hex(),refused=False))
 ACTIVE['fresh_split_domain_refusal_cases']=cases
 exact_fixture('fresh_declared_split_domain_refusals',dd(float(refused)),'2')
 assert len(CHECKS)-start==7
 return dict(kind='seven_new_scalar_EFT_DD_and_frozen_synthetic_FE_controls',controls=CHECKS[start:],source_or_state_evaluation=False)

def main():
 global OWNER
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA,'Guarded selected DD component; ROOT only'
 assert sys.float_info.radix==2 and sys.float_info.mant_dig==53 and sys.float_info.rounds==1,'binary64 nearest-rounding required'
 assert not list(BASE.glob(STEM+'_*')),'unused runtime namespace required'
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(__file__),scope='same32 saved FE contacts; double-double precision component only')
 publish('OWNER_START',OWNER)
 try:
  bind(STEM+'.md',PROTOCOL_SHA)
  for n,h in PRIVATE_DEFINITIONS:bind(n,h)
  rows,references,ancestry=dd_selected_admission()
  publish('INPUT',dict(owner=OWNER,rows=rows,references=references,ancestry=ancestry,qualification=FLAGS,contract='Exact saved binary64 geometry/coefficient/RHS operands; no pointwise or global state adoption'))
  fixture=fresh_dd_fixtures();publish('FIXTURE',dict(owner=OWNER,fixture=fixture,controls=CHECKS.copy(),qualification=FLAGS))
  results=[]
  for row in rows:
   out,points=selected_polynomial(row);data=encoded_result(out)
   completed=publish('ROW_%d_COMPONENT'%row['group'],dict(owner=OWNER,selection=[row['group'],row['component'],row['node']],result=data,points=points,checks_before_row=CHECKS.copy(),qualification=FLAGS))
   ref=references[str(row['group'])]
   compare_nonzero('row%d_action_accuracy'%row['group'],out['action'],ref['action'])
   compare_nonzero('row%d_original_residual_accuracy'%row['group'],out['original_rhs_residual'],ref['original_rhs_residual'])
   compare_nonzero('row%d_centered_action_accuracy'%row['group'],out['centered_action'],ref['action'])
   compare_nonzero('row%d_centered_original_residual_accuracy'%row['group'],out['centered_original_residual'],ref['original_rhs_residual'])
   summary=dict(selection={k:v for k,v in row.items() if k!='contacts'},component=completed,result=data,reference100=ref,qualification=FLAGS)
   results.append(summary);publish('ROW_%d_CERTIFICATE'%row['group'],dict(owner=OWNER,row=summary,controls=CHECKS.copy(),qualification=FLAGS))
  assert len(CHECKS)==EXPECTED_CONTROLS and len(rows)==2 and sum(len(r['contacts']) for r in rows)==32
  recheck();publish('MANIFEST',dict(owner=OWNER,input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),qualification=FLAGS))
  result=publish('RESULT',dict(status='BOUNDED_DOUBLE_DOUBLE_COMPONENT_COMPLETE',owner=OWNER,rows=results,controls=CHECKS,qualification=FLAGS,new_operator_solve=False,source_or_coefficient_change=False,original_rhs_changed=False,original_precision_witness_adoption=False,arithmetic='binary64 EFT high/low words; frozen elementary geometry; no longdouble',full_row_admission=False))
  recheck();publish('RECEIPT',dict(status='CLOSED',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),result_sha256=result['sha256'],error_sha256=None,input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),qualification=FLAGS));recheck()
  print(json.dumps(dict(status='BOUNDED_DOUBLE_DOUBLE_COMPONENT_COMPLETE',pid=OWNER['pid'],controls=len(CHECKS),result_sha256=result['sha256'])))
 except BaseException:
  error=publish('ERROR',dict(status='FAILED',owner=OWNER,traceback=traceback.format_exc(),controls=CHECKS,active=ACTIVE,eft_last=EFT_LAST,qualification=FLAGS))
  prior=path(STEM+'_RECEIPT.json')
  publish('ERROR_RECEIPT' if prior.exists() else 'RECEIPT',dict(status='CLOSED_ERROR',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),error_sha256=error['sha256'],result_sha256=None,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),qualification=FLAGS));raise
if __name__=='__main__':main()
