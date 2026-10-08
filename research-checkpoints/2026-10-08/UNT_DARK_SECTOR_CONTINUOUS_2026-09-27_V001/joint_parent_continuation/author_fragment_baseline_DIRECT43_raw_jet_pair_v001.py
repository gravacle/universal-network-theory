"""HELD same-geometry baseline raw-jet pair bridge; no imports, IO or runner.
Globals np,P and exact selected fce_pair/fce_block/fy_mv/fy_sum. Only the time
slab is new paired product-rule arithmetic. Raw g and R/Z/phi dg are copied.
The authentic TOTAL hdot is supplied after separate47969/60363 Fhat lifts.
This baseline diagnostic does not invoke132's axisymmetry guard or circle.
"""
BASELINE_RAW_JET_AUTHOR_DRAFT=True
BASELINE_RAW_JET_AUTHORING_IN_PROGRESS=False
BASELINE_RAW_JET_SOURCE=(None,None)
BASELINE_RAW_JET_RESULT=(None,None,None)
BASELINE_RAW_JET_RECEIPT=(None,None,None)
BASELINE_RAW_JET_PROOF=(None,None,None)
BASELINE_RAW_JET_SOURCE_PINS={
 'direct43_original_baseline_preparation_v003.py':'68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336',
 'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1',
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235'}

def baseline_DIRECT43_raw_jet_require(admission):
 assert not BASELINE_RAW_JET_AUTHOR_DRAFT and not BASELINE_RAW_JET_AUTHORING_IN_PROGRESS
 assert admission['source_pins']==BASELINE_RAW_JET_SOURCE_PINS
 for n,pin in (('source',BASELINE_RAW_JET_SOURCE),('result',BASELINE_RAW_JET_RESULT),('receipt',BASELINE_RAW_JET_RECEIPT),('proof',BASELINE_RAW_JET_PROOF)):
  assert all(v is not None for v in pin) and tuple(admission['baseline_terminal'][n])==tuple(pin)
 q=admission['baseline_terminal'];assert q['naturally_closed'] is True and q['exit_code']==0
 assert q['all_input_seals_verified'] is q['all_success_role_seals_verified'] is True
 assert q['owner']['source_sha256']==BASELINE_RAW_JET_SOURCE[1]
 for n in ('reference_record','baseline_record'):
  assert all(isinstance(admission[n].get(k),str) and admission[n][k] for k in ('file','sha256','commit_file','commit_sha256'))
 a,b=admission['reference_metadata'],admission['baseline_metadata']
 for md in (a,b):
  assert md['owner']==q['owner'] and md['failed'] is False and md['physical_adoption'] is False
  assert len(md['qualification'])==9 and all(v is False for v in md['qualification'].values()) and md['Z']==0.
 assert 0<=a['index']<43 and a['index']==b['index'] and np.isfinite(a['R']) and a['R']>0 and a['R']==b['R']
 assert a['radial_side']==b['radial_side']=='left' and a['vertical_side']==b['vertical_side']=='upper'
 assert {k:b['reference_event'][k] for k in ('file','sha256','commit_file','commit_sha256')}==admission['reference_record']
 assert a['stationary_seed_adopted_as_current'] is False
 assert b['original_point_first_order'] is True and b['node_sum_then_lift_equivalence_claimed'] is False
 assert b['Gauss_rate_interpolated'] is b['KADM_plus_Lie_inverse_used'] is False
 assert admission['selected_metadata_and_words_authenticated'] is True
 assert admission['same_geometry_baseline_not_new_coupled_trial'] is True

def baseline_DIRECT43_raw_jet_pair(reference,baseline_TOTAL_hdot,*,admission,keep,label,stage_complete):
 baseline_DIRECT43_raw_jet_require(admission);assert callable(keep) and callable(stage_complete)
 assert all(reference[n]==admission['reference_metadata'][n] for n in ('R','Z','radial_side'))
 assert reference['provenance']==admission['reference_metadata']['reference_event_provenance']
 fields=(('h',(3,3)),('h_spatial_jets',(2,3,3)),('N',()),('beta',(3,)),('N_jets',(4,)),('beta_jets',(4,3)),('g',(4,4)),('dg',(4,4,4)))
 for n,shape in fields:fce_pair(label+'_owned_'+n,reference[n],keep,shape)
 ht=fce_pair(label+'_authentic_baseline_TOTAL_hdot',baseline_TOTAL_hdot,keep,(3,3))
 h,N,beta,Na,ba,rawg,rawd=(reference[n] for n in ('h','N','beta','N_jets','beta_jets','g','dg'))
 assert all(np.array_equal(w.view(np.uint64),w.swapaxes(-1,-2).view(np.uint64)) for pair in (h,ht,rawg,rawd) for w in pair)
 assert all(np.array_equal(a.view(np.uint64),b[1:,1:].view(np.uint64)) for a,b in zip(h,rawg))
 assert all(np.array_equal(a.view(np.uint64),b[1:3,1:,1:].view(np.uint64)) for a,b in zip(reference['h_spatial_jets'],rawd))
 assert N[0]-abs(N[1])>0
 refs={};refs['input']=stage_complete(label+'_INPUT',dict(reference=reference,baseline_TOTAL_hdot=ht,admission=admission))
 assert all(isinstance(refs['input'].get(k),str) and refs['input'][k] for k in ('file','sha256','commit_file','commit_sha256'))
 nd=fce_pair(label+'_genuine_Ndot',P.a_slice(Na,0),keep,());bd=fce_pair(label+'_genuine_betadot',P.a_slice(ba,0),keep,(3,))
 hb=fce_pair(label+'_h_beta',fy_mv(h,beta),keep,(3,))
 left=fce_pair(label+'_TOTAL_hdot_beta',fy_mv(ht,beta),keep,(3,))
 right=fce_pair(label+'_h_betadot',fy_mv(h,bd),keep,(3,))
 hbt=fce_pair(label+'_product_rule_g0i_time',P.a_add(left,right),keep,(3,))
 first=fce_pair(label+'_betadot_dot_h_beta',fy_sum(P.a_mul(bd,hb),0),keep,())
 second=fce_pair(label+'_beta_dot_g0i_time',fy_sum(P.a_mul(beta,hbt),0),keep,())
 lapse=fce_pair(label+'_two_N_Ndot',P.a_mul64(2.,P.a_mul(N,nd)),keep,())
 time=fce_block(P.a_sub(P.a_add(first,second),lapse),hbt,ht,keep,label+'_completed_product_rule_time_slab')
 refs['time']=stage_complete(label+'_TIME',dict(time=time,baseline_TOTAL_hdot=ht,Ndot=nd,betadot=bd,input=refs['input']))
 assert all(isinstance(refs['time'].get(k),str) and refs['time'][k] for k in ('file','sha256','commit_file','commit_sha256'))
 g=fce_pair(label+'_raw_chart_g_unchanged',tuple(w.copy() for w in rawg),keep,(4,4))
 dg=tuple(w.copy() for w in rawd)
 for w,t in zip(dg,time):w[0]=t
 dg=fce_pair(label+'_baseline_product_rule_raw_dg',dg,keep,(4,4,4))
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(g,rawg))
 assert all(np.array_equal(a[1:].view(np.uint64),b[1:].view(np.uint64)) for a,b in zip(dg,rawd))
 refs['raw_pair']=stage_complete(label+'_RAW_PAIR',dict(g=g,dg=dg,input=refs['input'],time=refs['time']))
 assert all(isinstance(refs['raw_pair'].get(k),str) and refs['raw_pair'][k] for k in ('file','sha256','commit_file','commit_sha256'))
 N2=fce_pair(label+'_lapse_squared',P.a_mul(N,N),keep,())
 adm=fce_block(P.a_sub(fy_sum(P.a_mul(beta,hb),0),N2),hb,h,keep,label+'_comparison_ADM_g')
 gaps={}
 for n,x,y,shape in (('ADM_minus_raw_chart_g',adm,rawg,(4,4)),('product_rule_minus_raw_chart_time',time,P.a_slice(rawd,0),(4,4)),('TOTAL_hdot_minus_raw_chart_hdot',ht,P.a_slice(rawd,(0,slice(1,None),slice(1,None))),(3,3))):
  gaps[n]=fce_pair(label+'_'+n,P.a_sub(x,y),keep,shape)
 out=dict(g=g,dg=dg,reference=reference,baseline_TOTAL_hdot=ht,time_gauge=dict(Ndot=nd,betadot=bd),source_association_gaps=gaps,coordinate_system='native313_cp_model_equals_one',derivative_index_first=True,coordinate=[0.,admission['reference_metadata']['R'],0.,0.],radial_side='left',vertical_side='upper',raw_metric_words_preserved=True,raw_R_Z_phi_jet_words_preserved=True,phi_projection_used=False,source_stage_refs=refs.copy(),same_geometry_baseline_not_corrected_metric=True,finite_constraint_solution_admitted=False,full_circle_admitted=False,source_uncertainty_admitted=False,physical_adoption=False)
 refs['output']=stage_complete(label+'_OUTPUT',out)
 assert all(isinstance(refs['output'].get(k),str) and refs['output'][k] for k in ('file','sha256','commit_file','commit_sha256'))
 out['source_stage_refs']=refs;return out
