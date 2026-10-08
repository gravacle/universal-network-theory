"""Guarded new initial weak-CMC derivative of the earned combined direction."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMBINED_INITIAL_WEAK_CMC_DERIVATIVE_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='ae14d9bdd57d4958e947118b233c4770e5967a2bab0a18d1dd13ffc939151e85'
PROVIDER=('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py','5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18')
FRAGMENTS={'author_fragment_combined_initial_weak_CMC_contact_v001.py':'2f06b048844769c0c511e99dc87873a994a6b869f1c6a9593d8521fd2970ab69','author_fragment_combined_initial_CMC_admission_v002.txt':'ec1602c7a817957615f52fa0c5d1d1ea4784d01e9bc80196aa973b38ce52b3f0'}
P=np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())

def put(n,x):keep(n+'_hi',x[0]);keep(n+'_lo',x[1]);return x

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def initialize():
 global P,np,ORIGINAL_CAPTURE,normal_keep_pair
 n,h=PROVIDER;assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h
 spec=importlib.util.spec_from_file_location('initial_CMC_provider',BASE/n);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;ORIGINAL_CAPTURE=P.capture;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(finite_configuration_prepared=False,initial_CMC_constraint_qualified=False,full_CMC_preservation_computed=False,primitive_bridge_resolved=False,physical_adoption=False,evolution_qualified=False)
 globals().update(path=P.path,INPUTS=P.INPUTS,normal_keep_pair=lambda n,x,k:(k(n+'_hi',x[0]),k(n+'_lo',x[1]),x)[-1])
 for n in ('a_dd','a_sub','a_mul64','a_mul','a_add'):globals()[n]=getattr(P,n)
 for n,h in {PROVIDER[0]:PROVIDER[1],**FRAGMENTS,STEM+'.md':PROTOCOL_SHA,__file__:P.sha(__file__)}.items():bind(n,h)
 for n in FRAGMENTS:exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def reset(stage,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)

def pair_fields(raw,n):return raw[n+'_hi'],raw[n+'_lo']

def pair_sum(x,label):
 put(label+'_operands',x);out=a_dd(np.array(0.));hi=x[0].reshape(-1);lo=x[1].reshape(-1)
 for h,l in zip(hi,lo):out=a_add(out,(h,l));put(label+'_current_partial',out)
 return put(label+'_sum',out)

def initial_CMC_packet(refs):
 reset('copy_new_combined_geometry');geo=P.read_pair(refs['input'],('R','dv','hats'));Hbar=refs['bg']['h']*refs['fixed']['Hunit']/299792458.;assert math.isfinite(Hbar) and Hbar>0
 inp=P.checkpoint('INPUT',geo,dict(kind='same_combined_direction_initial_CMC_derivative_inputs',combined_input=thin(refs['input']),columns=[thin(q) for q in refs['columns']],pilots=[thin(q) for q in refs['pilots']],compact=[thin(q) for q in refs['compact']],fixed=refs['fixed'],owned_background=refs['bg'],signed_bridge_refs=refs['prior_bridge_refs'],Hbar=Hbar,phase_direct_metric_CMC_contact_zero=True))
 columns=[];records=[]
 for iq in range(4):
  reset('new_initial_CMC_density_contact',column=iq)
  current=P.read_pair(refs['pilots'][iq],('chart_sqrt_h','chart_dens','chart_N','momentum_Ktrace_hi','momentum_Ktrace_lo'))
  names=('indices','delta_momentum_Ktrace_hi','delta_momentum_Ktrace_lo','delta_chart_sqrt_h_hi','delta_chart_sqrt_h_lo','delta_chart_log_dens_hi','delta_chart_log_dens_lo')+tuple('trace_'+kind+'_'+field+'_'+word for kind in ('Gamma','ADM') for field in ('delta_density','pointwise_CMC_gap') for word in ('hi','lo'))
  config=P.read_pair(refs['compact'][iq],names)
  rate=P.read_pair(refs['columns'][iq],('new_rate_momentum_Ktrace_hi','new_rate_momentum_Ktrace_lo'))
  for family,raw in (('owned_current',current),('owned_compact',config),('owned_new_rate',rate)):
   for n,x in raw.items():keep(family+'_'+n,x)
  out=combined_initial_CMC_density(current['chart_sqrt_h'],pair_fields(current,'momentum_Ktrace'),pair_fields(config,'delta_momentum_Ktrace'),pair_fields(config,'delta_chart_sqrt_h'),pair_fields(config,'delta_chart_log_dens'),pair_fields(rate,'new_rate_momentum_Ktrace'),config['indices'],Hbar,keep,'initial_CMC')
  put('copied_compact_Gamma_minus_ADM_density_contact',a_sub(pair_fields(config,'trace_Gamma_delta_density'),pair_fields(config,'trace_ADM_delta_density')))
  put('copied_compact_Gamma_minus_ADM_pointwise_CMC_gap',a_sub(pair_fields(config,'trace_Gamma_pointwise_CMC_gap'),pair_fields(config,'trace_ADM_pointwise_CMC_gap')))
  take=config['indices'];computed=(out['compact'][0][take],out['compact'][1][take]);put('new_compact_density_minus_saved_Gamma_density_contact',a_sub(computed,pair_fields(config,'trace_Gamma_delta_density')))
  reference=P.a_div64(a_dd(current['chart_dens']),current['chart_N'],keep,'current_native_density_reference');put('current_sqrt_h_minus_native_density_reference',a_sub(a_dd(current['chart_sqrt_h']),reference))
  data={n:np.asarray(x).copy() for n,x in P.AVAILABLE.items()};data['compact_point_indices']=config['indices'].copy()
  rec=P.checkpoint('COLUMN',data,dict(kind='new_same_direction_initial_weak_CMC_density_contact',column=iq,combined_rate_ref=thin(refs['columns'][iq]),current_moment_ref=thin(refs['pilots'][iq]),compact_ref=thin(refs['compact'][iq]),phase_direct_metric_contact_zero=True,Gamma_and_ADM_serialized_trace_gaps_retained=True,physical_ports=None))
  columns.append(out);records.append(rec)
 reset('new_initial_CMC_weak_scalar_contact');fields={};point={};rows={}
 for n in ('compact','rate','total'):
  x=tuple(np.concatenate([c[n][word] for c in columns]) for word in (0,1));point[n]=put(n+'_density_contact',x);rows[n]=P.dd_scalar_scatter(x,geo,keep,n+'_initial_CMC');put(n+'_weak_initial_CMC_contact',rows[n])
  for word,suffix in enumerate(('hi','lo')):fields[n+'_density_contact_'+suffix]=x[word].copy();fields[n+'_weak_initial_CMC_contact_'+suffix]=rows[n][word].copy()
 test=(np.arange(87*45)%19-9).reshape(87,45)/37.;test[0]=0;tv=P.scalar_evaluate(test,geo);weight=(geo['dv']/geo['R']).reshape(15136)
 gaps=[];bounds=[]
 for n in ('compact','rate','total'):
  nodal=pair_sum(a_mul64(test,rows[n]),n+'_nodal_functional');direct=pair_sum(a_mul64(weight*tv,point[n]),n+'_direct_functional');gap=put(n+'_functional_gap',a_sub(nodal,direct))
  for label,x in (('nodal',nodal),('direct',direct),('gap',gap)):
   for word,suffix in enumerate(('hi','lo')):fields[n+'_functional_'+label+'_'+suffix]=np.asarray(x[word]).copy()
  epoint=abs(point[n][0])+abs(point[n][1]);bound=np.sum(abs(test)*P.scalar_scatter(epoint,geo))+np.sum(weight*abs(tv)*epoint);gaps.append(float(gap[0]+gap[1]));bounds.append(float(bound))
 P.check('new_initial_CMC_scalar_nodal_direct_functionals',np.array(gaps),np.zeros(3),np.array(bounds));fields.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 loads=P.checkpoint('LOADS',fields,dict(kind='same_combined_direction_initial_weak_CMC_contact',columns=[thin(q) for q in records],scalar_free_coordinates=3870,Hbar_fixed=True,initial_CMC_only=True,full_CMC_preservation_computed=False,physical_ports=None,controls=P.CHECKS.copy()))
 assert len(P.CHECKS)==1 and len(P.RECORDS)==6
 return dict(status='COMBINED_DIRECTION_INITIAL_WEAK_CMC_DERIVATIVE_MEASURED',input=inp,columns=records,loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,finite_configuration_prepared=False,initial_CMC_qualified=False,primitive_bridge_resolved=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root and distinct FULL review required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_same_direction_initial_CMC_derivative');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=initial_CMC_derivative_admission();case=initial_CMC_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=1,pairs=6)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})};arrays={n:np.asarray(x).copy() for n,x in arrays.items()}
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='current_initial_CMC_contact_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
