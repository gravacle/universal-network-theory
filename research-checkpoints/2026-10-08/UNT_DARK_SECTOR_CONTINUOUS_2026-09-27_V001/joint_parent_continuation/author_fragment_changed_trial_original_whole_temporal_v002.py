"""HELD saved finite196 caches to original67/147 signed and124 unsigned action.
Import-free definitions in the exact private CTP/67/147/124 arithmetic scope.
No temporal preparation, primal/current/EOS/test body or old action is invoked.
This is fixed-configuration mechanical temporal authority only.
"""
CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHOR_DRAFT=True
CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHORING_IN_PROGRESS=False
CHANGED_TRIAL_WHOLE_TEMPORAL_PRIVATE_SCOPE=False
CHANGED_TRIAL_WHOLE_TEMPORAL_SOURCE_PINS={
 'author_fragment_changed_trial_paired_point_provider_v003.py':'0efb82b873713b6899cd2641087d528df5ac7e1918355f441868edd4df78aa2c',
 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py':'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_weak_mechanical_positive_v002.py':'7a97350378c1687029cf2ffc02ab2302286727aed3b79cbc05cdbdda40068057'}
CTW_BASIS_SHAPES={'R':(4,3784),'dv':(4,3784),'hats':(4,4,3,86,44),'r':(87,),'z':(45,)}


def ctw_commit(callback,args):
 assert callable(callback),'Every completed input/column/output requires immediate containing custody'
 ref=callback(*args)
 assert isinstance(ref,dict) and all(isinstance(ref[n],str) and ref[n] for n in ('file','sha256','commit_file','commit_sha256'))
 return ref


def admit_changed_trial_original_whole_temporal(result,receipt,proof,selected,bind,read_commit):
 assert not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHOR_DRAFT and not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHORING_IN_PROGRESS
 assert CHANGED_TRIAL_WHOLE_TEMPORAL_PRIVATE_SCOPE is True
 for name,h in CHANGED_TRIAL_WHOLE_TEMPORAL_SOURCE_PINS.items():bind(name,h)
 scope=globals()
 for fn in (admit_changed_trial_point_provider,specialized_weak_mechanical_action,candidate_specialized_temporal_action,candidate_weak_mechanical_positive):
  assert fn.__globals__ is scope,'One selected namespace with original repaired arithmetic required'
 # The existing exact admission retains future finite SOURCE/RESULT/RC/proof,
 # five original collector controls, ordered stage refs and original basis ties.
 return admit_changed_trial_point_provider(result,receipt,proof,selected,bind,read_commit)


def prepare_changed_trial_original_whole_temporal(admitted,read_closed,keep,label,input_complete):
 assert not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHOR_DRAFT and not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHORING_IN_PROGRESS and CHANGED_TRIAL_WHOLE_TEMPORAL_PRIVATE_SCOPE is True
 assert admitted['physical_adoption'] is False and len(admitted['caches'])==4
 assert callable(read_closed) and callable(input_complete)
 inp=admitted['input'];names=tuple('completed_INPUT_data_basis_'+n for n in CTW_BASIS_SHAPES)
 for n,shape in CTW_BASIS_SHAPES.items():
  spec=inp['metadata']['schema']['completed_INPUT_data_basis_'+n]
  assert spec['dtype']=='float64' and spec['finite'] is True and tuple(spec['shape'])==shape
 owned=read_closed(inp,names);basis={}
 for n,shape in CTW_BASIS_SHAPES.items():
  a=owned['completed_INPUT_data_basis_'+n]
  assert isinstance(a,np.ndarray) and a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
  basis[n]=a.copy();basis[n].flags.writeable=False
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 input_refs=[ctw_commit(input_complete,('basis',dict(source=ctp_thin(inp),members=names,original_basis_provenance=admitted['original_basis'])))]
 caches=[]
 for iq,ref in enumerate(admitted['caches']):
  md=ref['metadata'];assert md['column']==iq
  cache_ref=md['physical_cache'];raw_ref=md['physical_raw_candidate']
  data=read_closed(cache_ref,tuple(changed_trial_point_schema('cache')))
  raw=read_closed(raw_ref,tuple(changed_trial_point_schema('raw')))
  for kind,values in (('cache',data),('raw',raw)):
   for n,shape in changed_trial_point_schema(kind).items():
    a=values[n];assert isinstance(a,np.ndarray) and a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
  links=[]
  for family,shapes in (('s',CTP_S),('c',CTP_C),('envelopes',CTP_ENVELOPES)):
   for n in shapes:
    left=CTP_CACHE_PREFIX+family+'_'+n;right=CTP_RAW_PREFIX+('coefficient_envelopes' if family=='envelopes' else family)+'_'+n
    same=bool(np.array_equal(data[left].view(np.uint64),raw[right].view(np.uint64)))
    links.append(dict(cache_member=left,raw_member=right,same_uint64_words=same));assert same,(iq,left,right)
  assert len(links)==51
  cache={'s':{n:data[CTP_CACHE_PREFIX+'s_'+n] for n in CTP_S},'c':{n:data[CTP_CACHE_PREFIX+'c_'+n] for n in CTP_C},'p':3784,
         'envelopes':{n:data[CTP_CACHE_PREFIX+'envelopes_'+n] for n in CTP_ENVELOPES},'constants':dict(md['constants']),
         'candidate_provenance':md['candidate_provenance'],'configuration_held':True}
  for n in CTP_PAIRS:cache[n]=(data[CTP_CACHE_PREFIX+n+'_hi'],data[CTP_CACHE_PREFIX+n+'_lo'])
  assert all(np.all(a>=0) for a in cache['envelopes'].values())
  assert np.all(cache['c']['N']>0) and np.all(cache['c']['gamma']>0) and np.all(cache['c']['dens']>0) and np.all(cache['s']['omega']>0) and np.all(cache['s']['w']>=0)
  assert set(cache['constants'])=={'ALPHA','ELL','C'} and all(cache['constants'][n]==getattr(P,n) for n in cache['constants'])
  for n in ('s','c','envelopes'):
   for a in cache[n].values():a.flags.writeable=False
  for n in CTP_PAIRS:
   for a in cache[n]:a.flags.writeable=False
  input_refs.append(ctw_commit(input_complete,(iq,dict(cache=ctp_thin(cache_ref),raw_candidate=ctp_thin(raw_ref),links=links,provenance=cache['candidate_provenance']))))
  caches.append(cache);del raw,data
 return dict(columns=caches,basis=basis,closed_provenance=admitted['closed_provenance'],completed_input_refs=input_refs,
             source='changed_trial_saved_fixed_configuration_temporal147',all_four_actual_columns_required=True,
             temporal_prepare_or_primal_current_replayed=False,global_inverse_earned=False,physical_adoption=False)


def changed_trial_original_whole_temporal(blocks,packed,keep,label,signed_column_complete,unsigned_column_complete,output_complete):
 assert not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHOR_DRAFT and not CHANGED_TRIAL_WHOLE_TEMPORAL_AUTHORING_IN_PROGRESS and CHANGED_TRIAL_WHOLE_TEMPORAL_PRIVATE_SCOPE is True
 assert isinstance(packed,tuple) and len(packed)==2
 assert all(a.dtype==np.float64 and a.shape==(403340,) and np.all(np.isfinite(a)) for a in packed)
 supplied=sw_keep(label+'_supplied_original_packed_words',packed,keep)
 parts=[P.unpack_fields(a,False) for a in supplied];native=tuple(q[0] for q in parts);metric=tuple(q[1] for q in parts)
 signed_refs=[];unsigned_refs=[]
 def signed_column(iq,payload):
  ref=ctw_commit(signed_column_complete,(iq,payload));signed_refs.append(ref);return ref
 def unsigned_column(iq,payload):
  ref=ctw_commit(unsigned_column_complete,(iq,payload));unsigned_refs.append(ref);return ref
 signed=specialized_weak_mechanical_action(blocks,blocks['basis'],native,metric,keep,label+'_NEW_original67',signed_column)
 action=sw_keep(label+'_completed_original_packed_action',tuple(P.pack_fields(signed['weak']['native'][w],signed['weak']['metric'][w]) for w in (0,1)),keep)
 signed_ref=ctw_commit(output_complete,('SIGNED',dict(input=supplied,action=action,columns=signed_refs,closed_provenance=blocks['closed_provenance'])))
 positive=candidate_weak_mechanical_positive(blocks,blocks['basis'],supplied,keep,label+'_NEW_original124',unsigned_column)
 assert positive.dtype==np.float64 and positive.shape==(403340,) and np.all(np.isfinite(positive)) and np.all(positive>=0)
 unsigned_ref=ctw_commit(output_complete,('UNSIGNED',dict(input=supplied,operation_envelope=positive,columns=unsigned_refs,signed_ref=signed_ref,closed_provenance=blocks['closed_provenance'])))
 assert len(signed_refs)==len(unsigned_refs)==4
 return dict(action=action,positive=positive,signed_record=signed_ref,unsigned_record=unsigned_ref,
             fixed_configuration_mechanical_temporal_authority=True,configuration_normal_phase_whole_correction_authority=False,
             finite_primal_forward_error_or_precision_certificate=False,all_direction_DD_proxy_equality=False,
             stationarity_or_finite_constraint_or_physical_adoption=False)

