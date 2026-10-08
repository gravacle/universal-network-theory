"""HELD root-only NEW analytic unit/readout controls; no galaxy input or old fixture."""
from pathlib import Path
from fractions import Fraction
from types import SimpleNamespace
import ast,hashlib,json,math,os,sys,traceback
AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
OUT='MODEL_METRIC_SI_CIRCLE_CONTROLS_V002_RESULT.json'
PINS={
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'MODEL_METRIC_TO_SI_LOCAL_CIRCLE_CONTROL_SPEC_V002.md':'8f11c24786f075e3dced10d169157791201837ba02837dc06cdb6d47fdd9319d',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b',
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa',
 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md':'087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523',
 'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19'}

def plain(x):
 if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [plain(v) for v in x]
 if hasattr(x,'tolist'):return x.tolist()
 return x

def load_new_apis(np):
 gtree=ast.parse((BASE/'cross_u_full_metric_geodesic_and_rotating_material_v001.py').read_text())
 defs={x.name:x for x in gtree.body if isinstance(x,ast.FunctionDef)}
 names=('floating_refusal','finite_result','real','metric_geometry','normal_observer','geodesic_rhs','dynamic_circle_residual')
 ns=dict(np=np,math=math,EPS=sys.float_info.epsilon)
 exec(compile(ast.Module(body=[defs[n] for n in names],type_ignores=[]),'supplied_geodesic_definitions','exec'),ns);G=SimpleNamespace(**ns)
 ns=dict(np=np,math=math,Fraction=Fraction,G=G)
 exec(compile((BASE/'author_fragment_full_dynamic_metric_circle_v002.py').read_text(),'dynamic_circle_definitions','exec'),ns);C=SimpleNamespace(**ns)
 ns=dict(np=np,math=math,G=G,CIRCLE=C)
 exec(compile((BASE/'author_fragment_model_metric_si_circle_readout_v002.py').read_text(),'model_SI_definitions','exec'),ns)
 assert all(PINS[n]==h for n,h in ns['MODEL_SI_UNIT_SOURCE_PINS'].items())
 return SimpleNamespace(**ns)

def main():
 assert AUTHOR_DRAFT is False and not (BASE/OUT).exists() and not (BASE/(OUT+'.ERROR.json')).exists(),'Reviewed root release/exclusive namespace required'
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 import numpy as np
 H=load_new_apis(np);controls=[];cases=[]
 def check(name,actual,expected,exact=False):
  a=np.asarray(actual,dtype=np.float64);b=np.asarray(expected,dtype=np.float64)
  assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
  if exact:error=0. if np.array_equal(a,b) else 1.;tol=0.
  else:error=float(np.max(abs(a-b),initial=0))/max(1.,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0)));tol=2e-11
  controls.append(dict(name=name,actual=a.copy(),expected=b.copy(),error=error,tolerance=tol,bit_exact_required=exact,passed=error<=tol));assert error<=tol,(name,error)
 report=dict(owner_pid=os.getpid(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),input_sha256=dict(PINS),controls=controls,cases=cases,old_fixture_source_function_or_live_payload_replayed=False,physical_galaxy_metric_supplied=False,revised43_velocities_exist=False,physical_or_observational_adoption=False)
 try:
  g=np.diag(np.array((-15/16,1.,1.,4.)));g[0,3]=g[3,0]=1/2;dg=np.zeros((4,4,4));dg[0,0,0]=1/32;dg[0,0,3]=dg[0,3,0]=1/8;dg[1,0,0]=1/16;dg[1,0,3]=dg[1,3,0]=1/2;dg[1,3,3]=4
  J=np.diag(np.array((1/2,1/8,1/8,1.)));current=dict(kind='fresh_dyadic_units',supplied_g=g.copy(),supplied_dg=dg.copy(),jacobian=J.copy(),metric_length_unit_m=8.);cases.append(current)
  p=H.affine_metric_unit_pullback(g,dg,J,8.);current['pullback']=p
  eg=np.diag(np.array((-15.,1.,1.,256.)));eg[0,3]=eg[3,0]=16;edg=np.zeros((4,4,4));edg[0,0,0]=1/4;edg[0,0,3]=edg[0,3,0]=2;edg[1,0,0]=1/8;edg[1,0,3]=edg[1,3,0]=2;edg[1,3,3]=32
  current.update(expected_g=eg,expected_dg=edg);check('dyadic_full_metric_and_derivative_units',np.r_[p['g'].ravel(),p['dg'].ravel()],np.r_[eg.ravel(),edg.ravel()],True)
  g=np.diag(np.array((-1.,1.,1.,1.)));dg=np.zeros((4,4,4));dg[0,0,0]=1;J=np.diag(np.array((2.,1.,1.,1.)));J[0,1]=1/4;current=dict(kind='fresh_affine_derivative_index',supplied_g=g.copy(),supplied_dg=dg.copy(),jacobian=J.copy(),metric_length_unit_m=1.);cases.append(current)
  p=H.affine_metric_unit_pullback(g,dg,J,1.);current['pullback']=p
  eg=np.diag(np.array((-4.,15/16,1.,1.)));eg[0,1]=eg[1,0]=-1/2;u=np.array((2.,1/4,0.,0.));edg=u[:,None,None]*u[None,:,None]*u[None,None,:]
  current.update(expected_g=eg,expected_dg=edg);check('affine_all_three_jet_indices',np.r_[p['g'].ravel(),p['dg'].ravel()],np.r_[eg.ravel(),edg.ravel()],True)
  mesh=np.array((0.,1.,2.,4.));mapping=dict(kind='coordinate_R_equals_catalogue_kpc');q1case=dict(kind='fresh_Q1_interior_contacts',mesh=mesh.copy(),mapping=dict(mapping),requests=[dict(model_R=2.,catalogue_R_kpc=2.,side='left'),dict(model_R=2.,catalogue_R_kpc=2.,side='right'),dict(model_R=1.5,catalogue_R_kpc=1.5,side='right')]);cases.append(q1case)
  left=H.q1_radial_readout_contact(mesh,2.,catalogue_R_kpc=2.,mapping=mapping,side='left');q1case['left']=left
  right=H.q1_radial_readout_contact(mesh,2.,catalogue_R_kpc=2.,mapping=mapping,side='right');q1case['right']=right
  opened=H.q1_radial_readout_contact(mesh,1.5,catalogue_R_kpc=1.5,mapping=mapping,side='right');q1case['opened']=opened
  g=np.diag(np.array((-223/256,1.,1.,4.)));g[0,3]=g[3,0]=1/8;dg=np.zeros((4,4,4));dg[0,0,0]=1/128;dg[0,0,3]=dg[0,3,0]=1/8;dg[1,0,0]=-15/256;dg[1,0,3]=dg[1,3,0]=1/8;dg[1,3,3]=4
  metric_admission=dict(finite_physical_metric_admitted=False);precision_admission={};current=dict(kind='fresh_native_scale_dynamic_circle',supplied_g=g.copy(),supplied_dg=dg.copy(),radius_contact=left,orientation=1,negative_orientation_request=-1,input_scope='new_analytic_control',metric_admission=metric_admission,readout_precision_admission=precision_admission);cases.append(current)
  event=H.supplied_model_local_circle_event(g,dg,radius_contact=left,orientation=1,input_scope='new_analytic_control',metric_admission=metric_admission,readout_precision_admission=precision_admission);current['event']=event
  negative=H.orient_dynamic_circle_candidates(event['readout']['dynamic_readout'],-1);current['negative_orientation']=negative;values=event['readout']['candidates'];assert len(values)==2 and not event['readout']['dynamic_readout']['rejected']
  L0=3.085677581491367e19;cp=299792458.;tu=L0/cp;actual=[]
  for value in values:actual.extend((value['Omega']*tu,value['Omega_dot']*tu**2,value['normal_axial_velocity']/cp,value['circle']['f']*tu));actual.extend(value['geodesic']['dw_dt']*np.array((L0/cp**2,L0/cp**2,tu**2)))
  actual.extend((event['readout']['selected_index'],negative['selected_index']));expected=[-5/32,-1/32,-1/(4*math.sqrt(7/8)),0.,0.,0.,-1/32,3/32,-1/32,1/(4*math.sqrt(7/8)),0.,0.,0.,-1/32,1.,0.]
  current.update(dimensionless_actual=np.array(actual),dimensionless_expected=np.array(expected));check('native_dynamic_frequency_time_velocity_and_orientation',actual,expected)
  assert event['galaxy_diagnostic_allowed'] is False and event['physical_metric_admitted'] is False
  actual=np.r_[left['selected_cell'],right['selected_cell'],opened['selected_cell'],left['value_weights'],left['radial_derivative_weights'],right['value_weights'],right['radial_derivative_weights'],opened['value_weights'],opened['radial_derivative_weights']];check('Q1_interior_node_and_open_cell',actual,[1.,2.,1.,0.,1.,-1.,1.,1.,0.,-.5,.5,.5,.5,-1.,1.],True)
  current=dict(kind='fresh_Q1_outer_endpoint',mesh=mesh.copy(),mapping=dict(mapping),left_request=dict(model_R=4.,catalogue_R_kpc=4.,side='left'),right_request=dict(model_R=4.,catalogue_R_kpc=4.,side='right'));cases.append(current)
  endpoint=H.q1_radial_readout_contact(mesh,4.,catalogue_R_kpc=4.,mapping=mapping,side='left');current['left']=endpoint;refused=False
  try:current['right_unexpected_result']=H.q1_radial_readout_contact(mesh,4.,catalogue_R_kpc=4.,mapping=mapping,side='right')
  except AssertionError:refused=True
  current['right_request_refused']=refused
  assert endpoint['right_cell'] is None and endpoint['right_interior_jet_defined'] is False
  check('Q1_outer_left_and_undefined_right',np.r_[endpoint['selected_cell'],endpoint['value_weights'],endpoint['radial_derivative_weights'],float(refused)],[2.,0.,1.,-.5,.5,1.],True)
  assert len(controls)==5 and all(row['passed'] for row in controls);report['status']='NEW_MODEL_METRIC_SI_CIRCLE_CONTROLS_PASS'
  for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
  with (BASE/OUT).open('x') as f:json.dump(plain(report),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
  (BASE/OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=5,maximum_error=max(row['error'] for row in controls),sha256=hashlib.sha256((BASE/OUT).read_bytes()).hexdigest())))
 except Exception:
  report.update(status='NEW_ANALYTIC_CONTROL_FAILURE',traceback=traceback.format_exc())
  with (BASE/(OUT+'.ERROR.json')).open('x') as f:json.dump(plain(report),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
  (BASE/(OUT+'.ERROR.json')).chmod(0o444);raise
if __name__=='__main__':main()
