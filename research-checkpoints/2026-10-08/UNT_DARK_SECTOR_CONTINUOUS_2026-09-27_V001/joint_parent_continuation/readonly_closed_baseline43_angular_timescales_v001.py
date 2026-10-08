"""Authorized independent saved-JSON interval postprocessing; no producer imports."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from datetime import datetime, timezone
import hashlib, json, math, os, resource
BASE=Path(__file__).resolve().parent
STEM='READONLY_CLOSED_BASELINE43_ANGULAR_TIMESCALES_V001'
COMPACT=('OBSERVER_CLOSED_BASELINE_DIRECT43_INSTANTANEOUS_RADIAL_COMPARISON_V001.json','c3896b31dfc266c04b0c52d14f19f90d497c0dc68b8da4b8d76dab4373abf8f9')
RESULT=('BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002_RESULT.json','790ef96dca9285bcb4394b5fe74b8b232e4c577c69303f1690197ea686214dda')
YEAR=Fraction(31557600)
MYR=YEAR*1000000
PI_DISPLAY=Decimal(str(math.pi))

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def read_events(path):
 # Parse only case.events, one <=2MiB object at a time; skip checkpoints entirely.
 decoder=json.JSONDecoder()
 with path.open() as f:
  data=f.read(4096);prefix='{"case":{"baseline_only":true,"controls":0,"events":['
  assert data.startswith(prefix),'Pinned original event layout changed'
  data=data[len(prefix):]
  for index in range(43):
   if index:
    data=data.lstrip();assert data.startswith(',');data=data[1:]
   while True:
    try:event,end=decoder.raw_decode(data);break
    except json.JSONDecodeError:
     b=f.read(65536);assert b;data+=b;assert len(data)<=2097152
   assert event['index']==index
   yield event
   data=data[end:]
  assert data.lstrip().startswith(']'),'Exact43 event census required'

def interval(value):
 assert isinstance(value,list) and len(value)==2
 out=tuple(Fraction(int(q['numerator']),int(q['denominator'])) for q in value)
 assert out[0]<=out[1];return out

def magnitude(pair):
 a,b=pair
 if a>0:return pair
 if b<0:return (-b,-a)
 return (Fraction(0),max(abs(a),abs(b)))

def encoded(pair):return [dict(numerator=str(q.numerator),denominator=str(q.denominator)) for q in pair]

def display(pair,factor=Decimal(1)):
 # Six significant digits rounded outward for the approximate pi display model.
 with localcontext() as c:
  c.prec=80;out=[]
  for q,rounding in zip(pair,(ROUND_FLOOR,ROUND_CEILING)):
   value=Decimal(q.numerator)/Decimal(q.denominator)*factor
   unit=Decimal(1).scaleb(value.adjusted()-5) if value else Decimal(1)
   out.append(str(value.quantize(unit,rounding=rounding)))
  return out

def publish(path,value):
 b=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with path.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 path.chmod(0o444);assert path.read_bytes()==b
 return hashlib.sha256(b).hexdigest(),len(b)

def main():
 assert not list(BASE.glob(STEM+'_*')),'Exclusive postprocessing output namespace'
 inputs={};stats={}
 for name,expected in (COMPACT,RESULT):
  p=BASE/name;st=p.stat();assert st.st_mode&0o222==0 and not st.st_flags&0x40000000
  assert digest(p)==expected,name
  inputs[name]=expected;stats[name]=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_mode)
 compact=json.loads((BASE/COMPACT[0]).read_text())
 assert compact['baseline_only'] is True and compact['physical_adoption'] is False
 assert compact['producer_result']==list(RESULT) and len(compact['rows'])==43
 assert compact['natural_closure_observation']['exit_code']==0
 assert all(v is False for v in compact['qualification'].values())
 rows=[];tau_all=[];period_all=[];change_all=[]
 for event,prior in zip(read_events(BASE/RESULT[0]),compact['rows']):
  index=event['index'];assert prior['index']==index and prior['R_kpc']==event['R']
  answer=event['readout'];chosen=answer['selected_index'];assert chosen==prior['selected_index']==1
  branch=next(q for q in answer['candidates'] if q['index']==chosen)
  assert branch['orientation_kind']=='DECLARED_ORIENTATION' and branch['timelike_enclosed'] is True
  assert answer['persistent_orbit_or_stability_claimed'] is answer['physical_or_velocity_adoption'] is False
  assert answer['input_phi_or_time_words_changed'] is False and answer['raw_phi_both_words_exact_zero'] is False
  assert event['general_stages'][-1]==answer['completed_stage_refs'][-1]==prior['completed_readout']
  omega=interval(branch['Omega_SI']);omega_dot=interval(branch['Omega_dot_SI'])
  a,d=magnitude(omega),magnitude(omega_dot);assert a[0]>0 and d[0]>0 and omega[0]>0 and omega_dot[1]<0
  tau=(a[0]/d[1],a[1]/d[0])
  period_over_pi=(2/a[1],2/a[0])
  change_over_pi=(2*d[0]/a[1]**2,2*d[1]/a[0]**2)
  tau_all.append(tau);period_all.append(period_over_pi);change_all.append(change_over_pi)
  rows.append(dict(index=index,R_kpc=event['R'],selected_branch=chosen,source_json_path=['case','events',index,'readout','candidates',chosen],completed_readout=prior['completed_readout'],Omega_SI=encoded(omega),Omega_dot_SI=encoded(omega_dot),instantaneous_angular_evolution_seconds=encoded(tau),instantaneous_period_seconds=dict(symbolic_factor='pi',exact_rational_coefficient_interval=encoded(period_over_pi)),instantaneous_fractional_rate_change_per_orbit=dict(symbolic_factor='pi',exact_rational_coefficient_interval=encoded(change_over_pi)),display=dict(angular_evolution_Myr=display(tuple(q/MYR for q in tau)),orbital_period_Myr_approx=display(tuple(q/MYR for q in period_over_pi),PI_DISPLAY),fractional_rate_change_per_orbit_approx=display(change_over_pi,PI_DISPLAY),percent_rate_change_per_orbit_approx=display(change_over_pi,100*PI_DISPLAY)),raw_phi_words_projected=False,physical_adoption=False))
 assert len(rows)==43
 def across(pairs):return (min(x[0] for x in pairs),max(x[1] for x in pairs))
 tau_range=across(tau_all);period_range=across(period_all);change_range=across(change_all)
 for n,t in stats.items():
  s=(BASE/n).stat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_mode)==t,n
 finding=dict(status='CLOSED_BASELINE43_SAVED_INTERVAL_ANGULAR_TIMESCALES_POSTPROCESSED',created_utc=datetime.now(timezone.utc).isoformat(),source=dict(file=Path(__file__).name,sha256=digest(Path(__file__))),authenticated_input_sha256=inputs,input_scope='Compact c389 selection and43 bounded original closed RESULT event cases only; no checkpoints, archive payloads, producers, operators, controls or trajectories replayed.',baseline_owner=compact['owner'],baseline_terminal=dict(source=compact['producer_source'],result=compact['producer_result'],receipt=compact['producer_receipt'],natural_closure_observation=compact['natural_closure_observation']),selection=dict(events=43,chosen_branch=1,orientation_selected_using_observations=False,all_selected_Omega_positive=True,all_selected_Omega_dot_negative=True,independent_interval_endpoint_bounds_ignore_unknown_correlations=True),formulae=dict(angular_evolution_seconds='abs(Omega)/abs(Omega_dot)',instantaneous_period_seconds='2*pi/abs(Omega)',fractional_rate_change_per_instantaneous_orbit='2*pi*abs(Omega_dot)/Omega**2',year_seconds=str(YEAR),year_convention='Julian365.25days; exactly31557600seconds',pi_display=str(PI_DISPLAY),display_policy='Exact rational tau endpoints and pi-free period/change coefficients are retained. Pi-bearing displayed values use numerical approximate pi and six-significant-digit outward rounding under that display model; they are not certified transcendental bounds or a future evolution theorem.'),ranges=dict(angular_evolution_seconds_exact=encoded(tau_range),orbital_period_seconds_over_pi_exact=encoded(period_range),fractional_rate_change_per_orbit_over_pi_exact=encoded(change_range),angular_evolution_Myr_display=display(tuple(q/MYR for q in tau_range)),orbital_period_Myr_approx_display=display(tuple(q/MYR for q in period_range),PI_DISPLAY),fractional_rate_change_per_orbit_approx_display=display(change_range,PI_DISPLAY),percent_rate_change_per_orbit_approx_display=display(change_range,100*PI_DISPLAY),angular_evolution_min_radius_kpc=rows[min(range(43),key=lambda i:tau_all[i][0])]['R_kpc'],angular_evolution_max_radius_kpc=rows[max(range(43),key=lambda i:tau_all[i][1])]['R_kpc'],fractional_change_min_radius_kpc=rows[min(range(43),key=lambda i:change_all[i][0])]['R_kpc'],fractional_change_max_radius_kpc=rows[max(range(43),key=lambda i:change_all[i][1])]['R_kpc']),rows=rows,interpretation='These are local angular-rate scales from the selected saved upper-side raw-jet radial-balance branch. Nonzero Omega_dot excludes constant Omega for that event; its instantaneous scale need not imply rapid breakdown. Multiplying the instantaneous derivative by one nominal period is a local dimensionless diagnostic, not an integrated orbit/history. Sheet averaging affects only its admitted normal rule; no exact axisymmetry, reflection or projected phi was assumed here.',qualification=compact['qualification'],physical_adoption=False,persistent_orbit_or_stability_claimed=False,new_coupled_or_corrected_finite_metric_evaluated=False,source_or_installed_rounding_accuracy_admitted=False,producer_or_scientific_operator_replayed=False,array_archive_decoded=False,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 h,size=publish(BASE/(STEM+'_RESULT.json'),finding)
 print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,bytes=size,ranges={k:v for k,v in finding['ranges'].items() if 'display' in k},peak_RSS_bytes=finding['peak_RSS_bytes']),sort_keys=True))
if __name__=='__main__':main()
