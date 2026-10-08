"""Guarded new compact configuration partial from sixteen saved paired contacts."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,hashlib,json,os,sys,traceback,math
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_METRIC_CONFIGURATION_CONTACT_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='5a21d179be7ce9a4ec6b66c7e982a036438842014af25336594134ac3e7a8eb0'
PARENT='cross_u_paired_current_normal_constraints_v002.py'
PARENT_SHA='a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40'
PINS={'author_fragment_compact_metric_configuration_contact_v004.py':'1bc331c697650ac97e24460fbac2c74308794514080d9746c981eae3e46776fc','author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd','author_fragment_compact_metric_weak_trace_contact_v001.py':'f8055bb3de6e7ff7128a6d0208878f6f128198b7595f7b8b873949bd52683f47',PARENT:PARENT_SHA}
NORMAL_TERMINAL=dict(pid=51682,result_sha256='ca1056f8798864eb7ae86c61812379ad8be46c4586560bf832f308fb79242158',receipt_sha256='00a630bd20e5ac06ce3dcc63dd4187c6d82b8ea73989274b0d105157cfee25b2',source_sha256=PARENT_SHA,protocol_sha256='cd13109df6ed827a052a9f4daf55b2c93824706d8f820b74f8f475f84f1e3e1e')
NORMAL_READER=dict(file='READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json',sha256='1e3b72fee21d3ec31335a02ae814d74c982d2970c39c9fb0575f28589ba2442b',pid=53056)
P=None;np=None

def bind(name,h):
 p=BASE/name;assert h is not None and P.sha(p)==h,name
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h
 return p

def keep(name,a):return P.capture(name,a)

def packet_pair(store,name,pair):
 normal_keep_pair(name,pair,keep);store[name+'_hi']=pair[0].copy();store[name+'_lo']=pair[1].copy()

def pair_bound(x):return abs(x[0])+abs(x[1])

def recheck_outputs():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 assert (BASE/(STEM+'_OWNER_START.json')).read_bytes()==P.encode(P.OWNER)
 for n,h in P.OUTPUTS.items():assert P.sha(BASE/n)==h,('output changed',n)

def initialize():
 global P,np
 import numpy as numpy_module
 np=numpy_module
 assert PARENT_SHA==hashlib.sha256((BASE/PARENT).read_bytes()).hexdigest()
 spec=importlib.util.spec_from_file_location('compact_contact_saved_providers',BASE/PARENT);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 # Import installs definitions only; no inherited main, fixture or science call.
 P.np=np;P.PINS=dict(PINS);P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(configuration_preparation_admitted=False,global_induced_rate_computed=False,normal_constraints_qualified=False,phase_charge_preserved=False,evolution_qualified=False,physical_metric_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
 P.B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
 providers=['a_dd','a_add','a_sub','a_mul','a_mul64','a_prod','a_matvec','a_stack','a_slice','a_transpose','a_reshape','a_div64','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','normal_keep_pair','normal_pair_connection_from_jet','paired_normal_chart_jets']
 for n in providers:globals()[n]=getattr(P,n)
 globals().update(C=P.C,ALPHA=P.ALPHA,ELL=P.ELL,B=P.B,GC=P.GC)
 for n,h in PINS.items():bind(n,h)
 for n in PINS:
  if n!=PARENT:exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def contact_admission():
 assert all(v is not None for v in NORMAL_TERMINAL.values()) and all(v is not None for v in NORMAL_READER.values()),'Actual normal closure and saved-only PASS required'
 for n,h in ((STEM+'.md',PROTOCOL_SHA),('CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002.md',NORMAL_TERMINAL['protocol_sha256']),('CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json',NORMAL_TERMINAL['result_sha256']),('CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RECEIPT.json',NORMAL_TERMINAL['receipt_sha256']),(NORMAL_READER['file'],NORMAL_READER['sha256'])):bind(n,h)
 result=json.loads((BASE/'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json').read_text());rc=json.loads((BASE/'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RECEIPT.json').read_text());reader=json.loads((BASE/NORMAL_READER['file']).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==NORMAL_TERMINAL['result_sha256'] and rc['owner']==result['owner'] and rc['owner']['pid']==51682 and rc['owner']['source_sha256']==PARENT_SHA
 assert len(result['controls'])==12 and len(result['checkpoints'])==8 and all(c['passed'] is True for c in result['controls']) and all(v is False for v in result['qualification'].values())
 assert reader['parent_terminal']==NORMAL_TERMINAL and reader['status']=='SAVED_PAIRED_NORMAL_CLOSURE_PASS' and reader['pid']==NORMAL_READER['pid'] and reader['committed_pairs']==8 and reader['qualification']==result['qualification']
 pins,pilot,fixed,cp=P.paired_pilot_admission()
 for n,h in pins.items():assert n not in P.INPUTS or P.INPUTS[n]==h;P.INPUTS[n]=h
 assert pilot['primitive_bridge_admitted'] is False
 return pilot,fixed,cp,result

def slice_point_fields(s,c,jets,feature,moments,raw,take):
 mode_config={'z','z2','f'};mode_chart={'JzU','zh'};mode_feature={'nz','q','V','D','V_raised','D_raised','Pi'}
 constants={'omega','xi','w'}
 ss={n:(v if n in constants else np.take(v,take,axis=1 if n in mode_config else 0)) for n,v in s.items()}
 cc={n:np.take(v,take,axis=1 if n in mode_chart else 0) for n,v in c.items()}
 def pairs(values,modes):return {n:(np.take(x[0],take,axis=1 if n in modes else 0),np.take(x[1],take,axis=1 if n in modes else 0)) for n,x in values.items()}
 jj=pairs(jets,{'dz'});ff=dict(constants=ss,paired=pairs(feature['paired'],mode_feature));mm=pairs(moments,set())
 rates={n:raw[n][take].copy() for n in ('native_rate_hi','native_rate_lo','metric_rate_hi','metric_rate_lo','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot')}
 return ss,cc,jj,ff,mm,rates

def owned_mechanical_jets(s,c,jets,rates,old_cov,keep,label):
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_readout');p=len(s['U'])
 y=(rates['native_rate_hi'],rates['native_rate_lo']);k=(rates['metric_rate_hi'],rates['metric_rate_lo'])
 u=a_dd(old_cov.copy());u[0][:,0]=y[0][:,:3];u[1][:,0]=y[1][:,:3]
 z=a_slice(jets['dz'],(slice(None),slice(None),slice(None),slice(1,None)));z=(z[0].copy(),z[1].copy())
 for w in range(2):z[w][:,:,0]=y[w][:,3:].reshape(p,32,3).transpose(1,0,2)
 h=(cj['dh'][0].copy(),cj['dh'][1].copy());kt=compact_trace_symmetric_rate(k)
 for w in range(2):h[w][:,0]=kt[w]
 N=(cj['dN'][0].copy(),cj['dN'][1].copy());beta=(cj['dbeta'][0].copy(),cj['dbeta'][1].copy())
 N[0][:,0]=rates['seed_owned_coordinate_Ndot'];N[1][:,0]=0;beta[0][:,0]=rates['seed_owned_coordinate_betadot'];beta[1][:,0]=0
 return dict(u=u,z=z,h=h,N=N,beta=beta),y,k

def contact_operation_bounds(s,c,jets,mechanical,Q,Qa):
 # Positive raw products preceding inverse, chart, metric-jet and Gamma cancellation.
 ih,h,U,g,beta=c['ih'],c['h'],s['U'],s['g'],c['beta'];ew=np.einsum('pij,pjk,pk->pi',abs(ih),abs(Q),abs(c['up']))
 eg=np.einsum('pi,pij,pj->p',abs(c['up']),abs(Q),abs(c['up']))/(2*c['gamma']);e0=eg/c['N'];eeta=np.column_stack((e0,ew+abs(beta)*e0[:,None]))
 ei=np.einsum('pij,pjk,pkl->pil',abs(ih),abs(Q),abs(ih));eq=np.zeros_like(g);eq[:,1:,1:]=abs(Q)
 eq[:,0,1:]=np.einsum('pij,pj->pi',abs(Q),abs(beta));eq[:,1:,0]=eq[:,0,1:];eq[:,0,0]=np.einsum('pi,pij,pj->p',abs(beta),abs(Q),abs(beta))
 eDG=np.zeros_like(jets['dg'][0]);eDG[:,:,1:,1:]=abs(Qa);eb=pair_bound(mechanical['beta'])
 eDG[:,:,0,1:]=np.einsum('paij,pj->pai',abs(Qa),abs(beta))+np.einsum('pij,paj->pai',abs(Q),eb);eDG[:,:,1:,0]=eDG[:,:,0,1:]
 eDG[:,:,0,0]=2*np.einsum('pai,pij,pj->pa',eb,abs(Q),abs(beta))+np.einsum('pi,paij,pj->pa',abs(beta),abs(Qa),abs(beta))
 G=pair_bound(jets['Ga']);enq=eDG+np.einsum('plam,pln->pamn',G,eq)+np.einsum('plam,pln->panm',G,eq)
 eGa=P.connection_from_jet_envelope(abs(s['hi']),enq)
 return dict(ih=ei,up=ew,U=eeta,g=eq,dg=eDG,Ga=eGa)

def compact_independent_controls(s,c,jets,d,dc,Q,bounds,keep,label):
 # Independently differentiated inverse and fixed-covector value identities.
 columns=[]
 for j in range(3):columns.append(a_add(a_matvec(Q,a_dd(c['ih'][:,:,j])),compact_lift_matvec(a_dd(c['h']),a_slice(dc['ih'],(slice(None),slice(None),j)))))
 inverse=a_stack(columns,2)
 cov=a_add(compact_lift_matvec(a_slice(d['g'],(slice(None),slice(1,None),slice(None))),a_dd(s['U'])),a_matvec(s['g'][:,1:],d['U']))
 actual=a_stack([a_slice(inverse,(slice(None),i,j)) for i in range(3) for j in range(3)]+[a_slice(cov,(slice(None),i)) for i in range(3)],1)
 einv=np.einsum('pij,pjk->pik',abs(Q),abs(c['ih']))+np.einsum('pij,pjk->pik',abs(c['h']),bounds['ih'])
 ecov=np.einsum('pij,pj->pi',bounds['g'][:,1:],abs(s['U']))+np.einsum('pij,pj->pi',abs(s['g'][:,1:]),bounds['U'])
 P.check(label+'_inverse_and_fixed_covector_value_contact',actual[0]+actual[1],np.zeros((len(Q),12)),np.column_stack((einv.reshape(len(Q),9),ecov)))
 torsion=a_sub(d['Ga'],a_transpose(d['Ga'],(0,1,3,2)));normal_keep_pair(label+'_delta_torsion',torsion,keep)
 P.check(label+'_torsion_free_connection_contact',torsion[0]+torsion[1],np.zeros_like(torsion[0]),bounds['Ga']+bounds['Ga'].swapaxes(2,3))
 rows=[]
 for a in range(4):
  G=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)));dG=a_slice(d['Ga'],(slice(None),slice(None),a,slice(None)))
  reaction=a_add(normal_pair_right(a_transpose(dG,(0,2,1)),s['g']),normal_pair_left(s['g'],dG))
  reaction=a_add(reaction,a_add(compact_contact_matrix_product(a_transpose(G,(0,2,1)),d['g']),compact_contact_matrix_product(d['g'],G)))
  rows.append(a_sub(a_slice(d['dg'],(slice(None),a,slice(None),slice(None))),reaction))
 dE=a_stack(rows,1);normal_keep_pair(label+'_delta_compatibility_readout',dE,keep)
 eg=bounds['dg']+np.einsum('plam,pln->pamn',bounds['Ga'],abs(s['g']))+np.einsum('plam,pln->panm',bounds['Ga'],abs(s['g']))
 eg+=np.einsum('plam,pln->pamn',pair_bound(jets['Ga']),bounds['g'])+np.einsum('plam,pln->panm',pair_bound(jets['Ga']),bounds['g'])
 P.check(label+'_retained_metric_compatibility_derivative',dE[0]+dE[1],np.zeros_like(dE[0]),eg)

def phase_contact(s,c,d,dc,df,current_J,keep,label):
 # Absolute EOS plus the existing relative projector term, with phi fixed.
 phi=a_dd(s['phi']);dX=a_div64(a_mul64(-.5,compact_contact_dot(phi,compact_lift_matvec(d['hi'],phi))),s['phase_X'],keep,label+'_delta_X')
 hi_phi=a_matvec(s['hi'],phi);dhi_phi=compact_lift_matvec(d['hi'],phi);Ppair=a_dd(s['P']);r=a_dd(s['r'])
 J=a_mul64(-s['phase_PX'][:,None],a_div64(dhi_phi,s['phase_X'][:,None],keep,label+'_pressure_inverse_clock'))
 clock=a_mul((dX[0][:,None],dX[1][:,None]),hi_phi)
 J=a_add(J,a_mul64(-s['phase_PXX'][:,None],a_div64(clock,s['phase_X'][:,None],keep,label+'_pressure_clock_first')))
 J=a_add(J,a_mul64(s['phase_PX'][:,None],a_div64(clock,s['phase_X'][:,None]**2,keep,label+'_pressure_clock_second')))
 raised=a_matvec(s['hi'],r);draised=a_add(compact_lift_matvec(d['hi'],r),a_matvec(s['hi'],df['configuration']['r']))
 J=a_sub(J,compact_lift_matvec(compact_contact_swap(df['configuration']['P']),raised));J=a_sub(J,compact_lift_matvec(compact_contact_swap(Ppair),draised))
 density=a_add(a_mul64(c['dens'],a_slice(J,(slice(None),0))),a_mul(dc['dens'],a_dd(current_J[:,0])))
 return dict(X=dX,P=a_mul64(s['phase_PX'],dX),current=J,canonical_density=density)

def scatter_compact_contact(columns,geo,keep):
 pn=a_dd(np.zeros((33,3,3,3)));pm=a_dd(np.zeros((6,3,3)));theta=a_dd(np.zeros((3,3)));theta_adm=a_dd(np.zeros((3,3)))
 for iq,row in enumerate(columns):
  take=row['indices'];Rfull=geo['R'][iq];R=Rfull[take];weight=(geo['dv'][iq]/Rfull)[take]
  native=a_transpose(a_reshape(row['momenta']['native_density'],(4,33,3)),(1,0,2));weighted=a_mul64(weight[None,:,None],native)
  F=np.zeros((3784,6,6));F[:,0,0]=1;F[:,0,1]=Rfull**2;F[:,1,5]=1;F[:,2,0]=Rfull**2;F[:,3,3]=Rfull;F[:,4,2]=Rfull**3;F[:,5,4]=Rfull**2
  met=a_mul64(weight[:,None],a_matvec(F[take].swapaxes(1,2),row['momenta']['metric_total_density']))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   fullhat=geo['hats'][iq,corner,0].reshape(3784);hat=fullhat[take];factor=np.broadcast_to(hat[:,None],(4,3)).copy();factor[:,2]=(fullhat*Rfull**2)[take]
   nv=a_mul64(factor[None],weighted);mv=a_mul64(hat[:,None],met)
   tv=a_mul64(hat,a_mul64(weight,row['trace']['Gamma']['delta_density']));av=a_mul64(hat,a_mul64(weight,row['trace']['ADM']['delta_density']))
   for a,cell in enumerate(take):
    i,j=int(geo['cell_i'][cell]+di-42),int(geo['cell_j'][cell]+dj-21);assert 0<=i<3 and 0<=j<3
    for target,value,key in ((pn,a_slice(nv,(slice(None),a,slice(None))),(slice(None),slice(None),i,j)),(pm,a_slice(mv,(a,slice(None))),(slice(None),i,j)),(theta,a_slice(tv,a),(i,j)),(theta_adm,a_slice(av,a),(i,j))):
     update=a_add(a_slice(target,key),value);target[0][key]=update[0];target[1][key]=update[1]
   for n,x in dict(native=pn,metric=pm,trace_Gamma=theta,trace_ADM=theta_adm).items():normal_keep_pair('completed_patch_'+n,x,keep)
 return dict(native=pn,metric=pm,trace_Gamma=theta,trace_ADM=theta_adm)

def packet(pilot,fixed,cp,normal_result):
 geo=P.read_pair(pilot['basis'],('R','dv','hats','cell_i','cell_j','r','z'));P.RAW.clear();P.AVAILABLE.clear()
 assert geo['z'][21]>0 and geo['z'][23]>geo['z'][21]
 P.checkpoint('INPUT',dict(node=np.array([43,22],dtype=np.int64),local_nodes_R=np.array([42,43,44],dtype=np.int64),local_nodes_Z=np.array([21,22,23],dtype=np.int64)),dict(kind='same_action_compact_metric_configuration_partial',pilot_input=pilot['input'],pilot_columns=pilot['columns'],normal_terminal=NORMAL_TERMINAL,normal_saved_reader=NORMAL_READER,fixed=fixed,owned_background=cp['background'],primitive_bridge_admitted=False,original_affine_and_actual_target_ratios=pilot['case']['original_affine_and_actual_target_ratios'],mechanical_rate_change=False,global_induced_rate=None,physical_ports=None))
 Hbar=cp['background']['h']*fixed['Hunit']/299792458.;columns=[];refs=[]
 for iq,ref in enumerate(pilot['columns']):
  P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='compact_metric_configuration_contact',column=iq)
  take,Q,Qa=compact_metric_hat(geo,iq,keep,'hat');full=P.load_pilot_column(ref)
  s,c,jets,feature,moments,rates=slice_point_fields(*full[:5],full[6],take)
  oldref=P.resolve_record(ref)['metadata']['old_force_ref'];rc=json.loads((BASE/'CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002_RECEIPT.json').read_text())
  for n,h in ((oldref['file'],oldref['sha256']),(oldref['commit_file'],oldref['commit_sha256'])):assert rc['input_sha256'][str((BASE/n).resolve())]==h;bind(n,h)
  owned=P.read_pair(oldref,('seed_chart_derivative_du_cov',))['seed_chart_derivative_du_cov'][take]
  current_J=full[6]['unchanged_new_phase_current'][take];P.RAW.clear();P.AVAILABLE.clear()
  assert np.all(s['Z_coordinate']>0)
  mechanical,y,k=owned_mechanical_jets(s,c,jets,rates,owned,keep,'owned')
  d,dc,aux=compact_metric_configuration_contact(s,c,jets,mechanical,Q,Qa,keep,'lift')
  df,dm=compact_contact_momenta(s,c,jets,feature,moments,d,dc,keep,'delta_momenta')
  trace=compact_metric_weak_trace_contact(s,c,jets,k,d,dc,aux,Hbar,keep,'weak_trace')
  phase=phase_contact(s,c,d,dc,df,current_J,keep,'phase');bounds=contact_operation_bounds(s,c,jets,mechanical,Q,Qa)
  data=dict(indices=take,Q=Q,Q_jet=Qa,ordinary_sheet_contact=np.zeros(4))
  for family,values in (('delta_primitive',d),('delta_chart',dc),('delta_feature',df['paired']),('delta_configuration',df['configuration']),('delta_momentum',dm),('delta_phase',phase),('owned_mechanical',mechanical)):
   for n,x in values.items():packet_pair(data,family+'_'+n,x)
  for n in ('Gamma','ADM'):
   for key,x in trace[n].items():packet_pair(data,'trace_'+n+'_'+key,x)
  for n,x in P.AVAILABLE.items():
   if n.startswith(('lift_gaps_','lift_raw_minus_owned_','lift_delta_raw_minus_owned_')):data[n]=x.copy()
  compact_independent_controls(s,c,jets,d,dc,Q,bounds,keep,'column_'+str(iq))
  data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
  record=P.checkpoint('CONTACT',data,dict(kind='new_fixed_rate_configuration_derivative_at_four_owned_contacts',column=iq,parent=ref,owned_spatial_covector_parent=oldref,contact_node=[43,22],local_metric_direction='shared_a_equals_f',controls=P.CHECKS[-3:],global_induced_rate_computed=False,old_compatibility_defect_retained=True,normal_stationarity_bridge_retained=True,phase_charge_fixed=False,ordinary_sheet_contact_zero=True,physical_ports=None))
  refs.append(record);columns.append(dict(indices=take,momenta=dm,trace=trace))
 P.RAW.clear();P.AVAILABLE.clear();patch=scatter_compact_contact(columns,geo,keep);data={}
 for n,x in patch.items():packet_pair(data,'weak_'+n,x)
 oref=pilot['ordinary_loads'];sheet=P.read_pair(oref,('ordinary_input_source_Z',))['ordinary_input_source_Z'];assert np.all(sheet==0)
 data['ordinary_source_contact']=np.zeros(len(sheet));P.RAW.clear()
 loads=P.checkpoint('LOADS',data,dict(kind='compact_canonical_and_weak_trace_configuration_contact',contact_refs=refs,patch_nodes_R=[42,43,44],patch_nodes_Z=[21,22,23],quadrature_contacts=16,coordinate_density_measure='reference_volume/R_once',native_covphi_R_power=2,metric_offdiagonal_factor_already_in_density=True,original_ordinary_source=oref,ordinary_contact_reason='compact_hat_support_off_sheet',global_induced_rate=None,normal_configuration_response=None,physical_exterior=None,phase_charge_preservation=False))
 assert len(P.CHECKS)==12 and len(P.RECORDS)==6
 return dict(status='COMPACT_FIXED_RATE_CONFIGURATION_CONTACT_MEASURED',contact_refs=refs,loads=loads,quadrature_contacts=16,controls=P.CHECKS,original_affine_bridge_admitted=False,original_affine_and_actual_target_ratios=pilot['case']['original_affine_and_actual_target_ratios'],global_induced_rate_computed=False,normal_rank_qualified=False,configuration_updated=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root review/release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);pilot,fixed,cp,normal=contact_admission()
 P.OWNER=dict(pid=os.getpid(),source_sha256=P.sha(__file__),source_file=Path(__file__).name,started_utc=P.now(),execution='root_owned_compact_configuration_contact')
 P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=packet(pilot,fixed,cp,normal);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS,checkpoints=P.RECORDS));recheck_outputs()
  receipt=dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS)
  P.json_file(STEM+'_RECEIPT.json',receipt);recheck_outputs();print(json.dumps(dict(status=case['status'],controls=12,pairs=6)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE}
  arrays.update({str(n):a for n,a in P.DD_ARRAY_CURRENT.get('arrays',{}).items()})
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='current_compact_contact_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,qualification=P.FLAGS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,traceback=traceback.format_exc()))
  prior=BASE/(STEM+'_RECEIPT.json');name=STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json')
  P.json_file(name,dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
