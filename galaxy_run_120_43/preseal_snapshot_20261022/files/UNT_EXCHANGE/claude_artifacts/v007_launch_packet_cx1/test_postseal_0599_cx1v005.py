"""Synthetic unit checks only; patched admission in memory, no production data."""
import sys,json,copy,importlib.util,types,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).parent;sys.path.insert(0,str(R))
import producer_guard_cx1v008 as G
G.admission=lambda *a,**k: {};G.check_entry_paths=lambda *a,**k:None
G.stamp=lambda obj,*a:obj
import postseal_records_cx1v006 as C
import srb_rot_record_cx1v008 as S
P=R.parent/'v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py'
s=importlib.util.spec_from_file_location('r11tests',P);M=importlib.util.module_from_spec(s);sys.modules[s.name]=M;s.loader.exec_module(M)
checks=[]
def ck(name,fn,refuse=False):
 try:
  v=fn();ok=not refuse and v is not False;err=None
 except Exception as e:ok=refuse;err=type(e).__name__+': '+str(e)
 checks.append(dict(name=name,passed=ok,error=err))
ck('duplicate_json',lambda:C.loads('{"a":1,"a":2}'),True)
ck('nonfinite_json',lambda:C.loads('{"a":NaN}'),True)
b={'verdict':'PASS','max_rel':1e-14,'n':4096,'rtol':1e-12}
ck('i1t_leaf',lambda:C.i1_value(b)==(1e-14,4096))
ck('i1t_parts',lambda:C.i1_value({'verdict':'PASS','parts':[b,b],'rtol':1e-12})==(1e-14,4096))
for k,v in [('n',4095),('max_rel',float('nan')),('max_rel',-1),('max_rel',2e-12),('rtol',1e-9),('verdict','NOT_APPLICABLE_SYNTHETIC')]:
 q=dict(b);q[k]=v;ck('i1t_bad_'+k+'_'+str(v),lambda q=q:C.i1_value(q),True)
rr={x:{'uv_tail':{'route_a_record':{}}} for x in C.CASES};man={'runs':{x:{'path':'synthetic/'+x,'sha256':'a'*64} for x in C.CASES}}
old=C.route_a_record;C.route_a_record=lambda o:o
base={'M_T_accepted':0.25,'M_T_threshold':0.25,'flags':[],'monitor_status':'M_T_WITHIN_THRESHOLD','outcome':'CONVERGED_FINITE_FIXED_POINT'}
rs={x:copy.deepcopy(base) for x in C.CASES}
ck('mt_exact_threshold',lambda:C.mt_record(man,rs)['verdict']=='PASS')
rs2=copy.deepcopy(rs);rs2['C4T'].update(M_T_accepted=.2501,flags=['TAIL_SOURCE_UNDERCONVERGED'],monitor_status='FLAGGED')
ck('mt_above_threshold',lambda:C.mt_record(man,rs2)['verdict']=='FAIL')
ck('mt_gate_r11',lambda:M.g_MT(dict(C.mt_record(man,rs2)),{},lambda *a:None,[])==['MT_RUN_FAILS_FLAGGED:C4T'])
for k,v in [('flags',['TAIL_SOURCE_UNDERCONVERGED']),('M_T_threshold',.3),('M_T_accepted',-1),('monitor_status','FLAGGED')]:
 q=copy.deepcopy(rs);q['C4T'][k]=v;ck('mt_bad_'+k,lambda q=q:C.mt_record(man,q),True)
C.route_a_record=old
ids=['r'+str(i) for i in range(12)];binding={'query_rows':[{'id':x,'radius_m':1.5} for x in ids],'physical_inclination_rad':.5,'released_inclination_rad':.5}
a={'radial_nodes_m':np.array([1.,2.]),'rotation_Omega_squared':np.array([[4.,9.],[9.,16.]]),'full_fields_complex':np.zeros((2,1,2,10),complex)}
ck('srb_row_support_and_speed',lambda:S.row_contract(a,binding,ids,[.1]*12)[0]['v_c_m_s']==[2.,6.])
ck('srb_interpolation_support',lambda:S.row_contract(a,binding,ids,[.1]*12)[0]['row_columns']==[[0,1]]*12)
for kind in ('negative_N','negative_speed','nan_radius','out_of_domain'):
 q=copy.deepcopy(a);bb=copy.deepcopy(binding)
 if kind=='negative_N':q['full_fields_complex'][0,0,0,0]=-2
 if kind=='negative_speed':q['rotation_Omega_squared'][0,0]=-1
 if kind=='nan_radius':q['radial_nodes_m'][0]=float('nan')
 if kind=='out_of_domain':bb['query_rows'][0]['radius_m']=3
 ck('srb_'+kind,lambda q=q,bb=bb:S.row_contract(q,bb,ids,[.1]*12),True)
eps={'gate':'EPS','verdict':'CERTIFIED','envelope_bound':{'rule':'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS','dominates_actual_every_shell':True,'coverage_max_inverse_kpc':6},'shells':[{'lo_inverse_kpc':4,'hi_inverse_kpc':5,'eps_envelope':.2,'eps_actual_set':.1},{'lo_inverse_kpc':5,'hi_inverse_kpc':6,'eps_envelope':.3,'eps_actual_set':.2}]}
ck('srb_uses_envelope',lambda:[x['eps'] for x in S.envelope_certificate(eps,4,6)['shells']]==[.2,.3])
for kind in ('gap','duplicate','below_actual','short','wrong_rule'):
 q=copy.deepcopy(eps)
 if kind=='gap':q['shells'][1]['lo_inverse_kpc']=5.1
 if kind=='duplicate':q['shells'].append(q['shells'][1])
 if kind=='below_actual':q['shells'][0]['eps_envelope']=.01
 if kind=='short':q['envelope_bound']['coverage_max_inverse_kpc']=5
 if kind=='wrong_rule':q['envelope_bound']['rule']='unknown'
 ck('srb_envelope_'+kind,lambda q=q:S.envelope_certificate(q,4,6),True)
# Gate arithmetic verified independently by literal expectation.
rec={'case':'C4T','c4t_result_sha256':'a'*64,'srb_rot_km_s':[.01]*12}
ck('r11_srb_boundary',lambda:M.g_SRB_ROT(rec,{'ids':ids,'tau':dict.fromkeys(ids,.1)},lambda *a:None,[])==[])
q=copy.deepcopy(rec);q['srb_rot_km_s'][0]=.01001
ck('r11_srb_fail',lambda:M.g_SRB_ROT(q,{'ids':ids,'tau':dict.fromkeys(ids,.1)},lambda *a:None,[])==['SRB_ROT_ROW_01_GT_TAU_OVER_10'])
with (R/'POSTSEAL_0599_TESTS_V005.json').open('x') as f:json.dump({'scope':'TESTED synthetic pure checks; no production data, process, or science execution','source_pins':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'postseal_records_cx1v006.py',R/'srb_rot_record_cx1v008.py',P)},'tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));print([x for x in checks if not x['passed']]);assert all(x['passed'] for x in checks)
