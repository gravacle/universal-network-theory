"""HELD mechanical-only gauge ports at authenticated NEW139 point TOTAL words.
Globals np/P, fy_keep and reviewed286 candidate_gauge_raw_action_contact.
Decoded selected CLOSED records and fixed original support are caller inputs.
No139/225/116/phase/current producer, nodal TOTAL reconstruction or old C replay.
Every mechanical port is genuinely NEW; phase gauge coefficients stay external.
"""
NEW139_GAUGE_AUTHOR_DRAFT=True
NEW139_GAUGE_AUTHORING_IN_PROGRESS=False
NEW139_GAUGE_FINITE_CLOSURE=(None,None,None,None)
NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE=(None,None,None,None)
NEW139_GAUGE_LITERAL_CLOSURE=(None,None,None,None)
NEW139_GAUGE_SOURCE_PINS={
 'author_fragment_candidate_gauge_registered_current_contact_v001.py':'ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd'}
NEW139_GAUGE_ROLES=('BASELINE_COLUMN_INPUT','RATE_STATE_INPUT','RATE_STATE_FIRST_JETS','RATE_STATE_FEATURES','RATE_STATE_MOMENTA','RATE_STATE_COLUMN')

def nmg_pair(label,x,shape,keep):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 assert all(isinstance(a,np.ndarray) and a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a)) for a in x),label
 return fy_keep(label,tuple(a.copy() for a in x),keep)

def nmg_equal(label,x,y,keep):
 for tag,values in (('fresh',x),('fixed',y)):
  for w,a in enumerate(values):keep(label+'_'+tag+'_word%d'%w,np.asarray(a).copy())
 assert len(x)==len(y) and all(a.shape==b.shape and a.dtype==b.dtype==np.float64 and np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(x,y)),label

def nmg_family(data,prefix,keep,label):
 names=sorted(n[len(prefix):-3] for n in data if n.startswith(prefix) and n.endswith('_hi'))
 assert names and all(prefix+n+'_lo' in data for n in names)
 assert {n[len(prefix):-3] for n in data if n.startswith(prefix) and n.endswith('_lo')}==set(names)
 return {n:nmg_pair(label+'_'+n,(data[prefix+n+'_hi'],data[prefix+n+'_lo']),data[prefix+n+'_hi'].shape,keep) for n in names}

def nmg_stage(kind,payload,complete,records):
 assert callable(complete),'Seal the completed stage before the next operation'
 q=complete(kind,payload);assert isinstance(q,dict) and all(isinstance(q[n],str) and q[n] for n in ('file','sha256','commit_file','commit_sha256'))
 records.append(q);return q

def prepare_NEW139_mechanical_gauge_column(fixed,selected,temporal_cache,admission,keep,label,stage_complete):
 assert not NEW139_GAUGE_AUTHOR_DRAFT and not NEW139_GAUGE_AUTHORING_IN_PROGRESS
 for closure in (NEW139_GAUGE_FINITE_CLOSURE,NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE):
  assert len(closure)==4 and all(isinstance(q,(tuple,list)) and len(q) in (2,3) and all(v is not None for v in q) for q in closure),'Future CLOSED bindings required'
 assert tuple(tuple(q) for q in admission['finite_closure'])==tuple(tuple(q) for q in NEW139_GAUGE_FINITE_CLOSURE) and tuple(tuple(q) for q in admission['mechanical_cache_closure'])==tuple(tuple(q) for q in NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE)
 assert admission['source_pins']==NEW139_GAUGE_SOURCE_PINS and admission['physical_adoption'] is False
 for n in ('all_selected_NEW139_seals_authenticated','all_original_support_seals_authenticated','same_original_basis_verified','same_fixed_geometry_and_gauge_verified','same_fixed_mechanical_raw_E0_verified','original_targets_unchanged'):assert admission[n] is True,n
 iq=admission['column'];assert type(iq) is int and 0<=iq<4 and set(selected)==set(NEW139_GAUGE_ROLES)
 assert admission['finite_owner']['source_sha256']==NEW139_GAUGE_FINITE_CLOSURE[0][1] and admission['selected_records']
 refs={};records=[]
 for role,packet in selected.items():
  ref=packet['ref'];assert ref==admission['selected_records'][role] and set(ref)=={'file','sha256','commit_file','commit_sha256'} and ref['file'].endswith('_'+role+'.npz')
  md=packet['metadata'];assert md['owner']==admission['finite_owner'] and md['column']==iq and md['failed'] is False and md['qualification'] and all(v is False for v in md['qualification'].values())
  assert packet['data'] and all(n in md['schema'] and list(a.shape)==md['schema'][n]['shape'] and str(a.dtype)==md['schema'][n]['dtype'] for n,a in packet['data'].items());refs[role]=dict(ref)
 baseline=selected['BASELINE_COLUMN_INPUT']['data'];old=fixed['candidate'];s={};c={}
 for family,out in (('s',s),('c',c)):
  for n,a in old[family].items():
   key='completed_BASELINE_COLUMN_INPUT_candidate_'+family+'_'+n;assert key in baseline
   b=baseline[key];nmg_equal(label+'_same_raw_'+family+'_'+n,(b,),(a,),keep);out[n]=b.copy()
 p=len(c['N']);assert p==3784 and temporal_cache['p']==p and temporal_cache['configuration_held'] is True
 for family in ('s','c'):
  for n,a in temporal_cache[family].items():nmg_equal(label+'_same147_'+family+'_'+n,(a,),((s if family=='s' else c)[n],),keep)
 for n in ('ALPHA','ELL','C'):assert temporal_cache['constants'][n]==getattr(P,n)
 for n in ('B','GC','ALPHA','ELL','C'):assert admission['material_constants'][n]==getattr(P,n)
 inputs=selected['RATE_STATE_INPUT']['data'];columns=selected['RATE_STATE_COLUMN']['data'];get=lambda prefix,n,shape:nmg_pair(label+'_copied_'+n,(inputs[prefix+n+'_hi'],inputs[prefix+n+'_lo']),shape,keep)
 inp='completed_RATE_STATE_INPUT_';hfirst=get(inp,'h_first',(p,4,3,3));ua=get(inp,'u_jets',(p,4,3));za=get(inp,'z_jets',(32,p,4,3));Na=get(inp,'N_jets',(p,4));ba=get(inp,'beta_jets',(p,4,3));E0=get(inp,'E0',(p,4,4,4));phase=get(inp,'updated_phase',(p,4))
 total={n:nmg_pair(label+'_copied_column_TOTAL_'+n,(columns['completed_RATE_STATE_COLUMN_new_TOTAL_time_words_'+n+'_hi'],columns['completed_RATE_STATE_COLUMN_new_TOTAL_time_words_'+n+'_lo']),shape,keep) for n,shape in (('u_jets',(p,4,3)),('z_jets',(32,p,4,3)),('h_dot',(p,3,3)))}
 for n,x in (('u_jets',ua),('z_jets',za)):nmg_equal(label+'_TOTAL_duplicate_'+n,x,total[n],keep)
 nmg_equal(label+'_TOTAL_hfirst_slot0',tuple(a[:,0] for a in hfirst),total['h_dot'],keep)
 assert all(np.all(a[:,3]==0) for a in hfirst),'Reviewed286 fixes h_phi to exact zero; genuine slot3 cannot be silently omitted'
 nmg_equal(label+'_unchanged_spatial_hfirst',tuple(a[:,1:3] for a in hfirst),fixed['geometry']['h_spatial_jets'],keep)
 for n,x in (('N_jets',Na),('beta_jets',ba)):nmg_equal(label+'_unchanged_genuine_'+n,x,fixed['gauge'][n],keep)
 nmg_equal(label+'_same_owned_E0',E0,fixed['reference']['E0'],keep);nmg_equal(label+'_same147_E0',E0,temporal_cache['fixed_E0'],keep)
 nmg_equal(label+'_unchanged_spatial_u',tuple(a[:,1:] for a in ua),tuple(a[:,1:] for a in fixed['covectors']['u_jets']),keep)
 nmg_equal(label+'_unchanged_spatial_z',tuple(a[:,:,1:] for a in za),tuple(a[:,:,1:] for a in fixed['covectors']['z_jets']),keep)
 nmg_equal(label+'_same_updated_phase',phase,fixed['updated_phase_pair'],keep)
 jets=nmg_family(selected['RATE_STATE_FIRST_JETS']['data'],'completed_RATE_STATE_FIRST_JETS_jets_',keep,label+'_fresh_jets');assert set(jets)=={'du','dz','dg','Ga'}
 features=nmg_family(selected['RATE_STATE_FEATURES']['data'],'completed_RATE_STATE_FEATURES_features_paired_',keep,label+'_fresh_features')
 assert set(features)=={'du','dz','Ga','nu','nz','q','V','D','lower_nu','F','Fup','a','V_raised','D_raised','Pi','PiU'}
 for n in ('du','dz','Ga'):nmg_equal(label+'_feature_jet_duplicate_'+n,features[n],jets[n],keep)
 momenta=nmg_family(selected['RATE_STATE_MOMENTA']['data'],'completed_RATE_STATE_MOMENTA_momenta_',keep,label+'_fresh_momenta')
 assert set(momenta)=={'connection_Klo','connection_raised_Klo','connection_D','connection_Maxwell','connection_momentum','native_density','metric_native_density','K','Ktrace','metric_EH_tensor','metric_EH_density','metric_total_density'}
 copied=nmg_family(columns,'completed_RATE_STATE_COLUMN_new_point_current_',keep,label+'_column_current_duplicate');assert set(copied)==set(momenta)
 for n,x in momenta.items():nmg_equal(label+'_momentum_column_duplicate_'+n,x,copied[n],keep)
 envelopes={n[len('completed_RATE_STATE_FIRST_JETS_envelopes_'):]:a.copy() for n,a in selected['RATE_STATE_FIRST_JETS']['data'].items() if n.startswith('completed_RATE_STATE_FIRST_JETS_envelopes_')}
 for n,a in envelopes.items():keep(label+'_fresh_firstjet_envelope_'+n,a);assert a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(a>=0)
 assert envelopes
 candidate=dict(s=s,c=c,jets=jets,features=dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=features,configuration_changed=False),momenta=momenta,jet_envelopes=envelopes,physical_adoption=False)
 column=dict(candidate=candidate,geometry=fixed['geometry'],gauge=dict(fixed['gauge'],N_jets=Na,beta_jets=ba),covectors=dict(u_jets=ua,z_jets=za),mechanical=dict(h_dot=total['h_dot']),reference=dict(fixed['reference'],E0=E0),updated_phase_pair=phase,same_candidate_provenance=dict(admission),gauge_target_derivative_zero=True,physical_adoption=False)
 ref=nmg_stage('NEW139_MECHANICAL_GAUGE_INPUT',dict(column=iq,candidate=candidate,h_first=hfirst,gauge=column['gauge'],covectors=column['covectors'],mechanical=column['mechanical'],reference=column['reference'],source_records=refs,admission=admission,phase_current_or_EOS_recomputed=False,old_KADM_not_relabelled=True),stage_complete,records)
 column['input_record']=ref;column['source_records']=refs;return column

def prepare_NEW139_mechanical_gauge_coefficients(column,keep,label,test_complete,column_complete):
 assert not NEW139_GAUGE_AUTHOR_DRAFT and not NEW139_GAUGE_AUTHORING_IN_PROGRESS
 assert callable(test_complete) and callable(column_complete) and column['gauge_target_derivative_zero'] is True and column['physical_adoption'] is False
 admission=column['same_candidate_provenance'];assert tuple(tuple(q) for q in admission['finite_closure'])==tuple(tuple(q) for q in NEW139_GAUGE_FINITE_CLOSURE) and tuple(tuple(q) for q in admission['mechanical_cache_closure'])==tuple(tuple(q) for q in NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE)
 p=len(column['candidate']['c']['N']);assert p==3784;zero=lambda shape:P.a_dd(np.zeros(shape));out={'native':zero((p,99,4,4)),'metric':zero((p,6,4,4))};refs=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   direction=dict(N=zero((p,)),beta=zero((p,3)),N_jets=zero((p,4)),beta_jets=zero((p,4,3)))
   target=direction['N' if row==0 else 'beta'] if coordinate is None else direction['N_jets' if row==0 else 'beta_jets']
   index=(slice(None),) if row==0 and coordinate is None else (slice(None),row-1) if coordinate is None else (slice(None),coordinate) if row==0 else (slice(None),coordinate,row-1)
   target[0][index]=1.;tag=label+'_row%d_jet%d'%(row,jet)
   full=dict(h=zero((p,3,3)),h_spatial_jets=zero((p,2,3,3)),h_dot=zero((p,3,3)),u_jets=zero((p,4,3)),z_jets=zero((32,p,4,3)),**direction)
   for n,x in full.items():nmg_pair(tag+'_supplied_'+n,x,x[0].shape,keep)
   contact=candidate_gauge_raw_action_contact(column['candidate'],column['geometry'],column['gauge'],column['covectors'],column['mechanical'],full,column['reference'],keep,tag+'_NEW_mechanical')
   canonical={n:nmg_pair(tag+'_NEW_canonical_'+n,contact['delta_momenta'][key],(p,width),keep) for n,key,width in (('native','native_density',99),('metric','metric_total_density',6))}
   part=dict(row=row,jet=jet,coordinate=coordinate,direction=full,canonical_point_contact=canonical,mechanical=contact,input_record=column['input_record'],same_candidate_provenance=admission,gauge_target_derivative_zero=True,phase_branch_not_evaluated=True,physical_adoption=False)
   ref=nmg_stage('NEW139_MECHANICAL_GAUGE_TEST',part,lambda kind,payload:test_complete(row,jet,kind,payload),refs)
   for n,x in canonical.items():
    for w in (0,1):out[n][w][:,:,row,jet]=x[w]
    nmg_pair(tag+'_completed_coefficient_'+n,out[n],out[n][0].shape,keep)
 result=dict(coefficients=out,completed_test_refs=refs,input_record=column['input_record'],source_records=column['source_records'],same_candidate_provenance=admission,gauge_row_order=('N','beta_R','beta_Z','beta_phi'),gauge_coordinate_order=('value','R','Z','t'),all16_mechanical_gauge_ports_retained=True,gauge_target_derivative_zero=True,phase_coefficients_require_separate_exact_operand_inheritance=True,source_uncancelled_enclosure_and_fullweak_transpose_external=True,normal_time_primary_coefficients_external=True,C_equals_minus_Rv_transpose_assumed=False,uniform_DD_or_global_inverse_or_canonical_or_physical_admission=False,physical_adoption=False)
 result['column_record']=nmg_stage('NEW139_MECHANICAL_GAUGE_COLUMN',result,column_complete,[]);return result
