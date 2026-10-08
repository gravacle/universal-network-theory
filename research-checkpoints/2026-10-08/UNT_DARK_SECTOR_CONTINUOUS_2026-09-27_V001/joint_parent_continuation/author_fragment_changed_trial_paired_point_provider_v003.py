"""HELD dictionary-only handoff of closed finite196 caches to unchanged133/96.
Definitions only. Globals np,P,json and the reviewed133/96/147 definitions live
in an explicitly private selected namespace. No old owner is substituted.
"""
CHANGED_TRIAL_POINT_AUTHOR_DRAFT=True
CHANGED_TRIAL_POINT_AUTHORING_IN_PROGRESS=False
CHANGED_TRIAL_POINT_PRIVATE_SCOPE=False
CHANGED_TRIAL_POINT_SOURCE=(None,None)
CHANGED_TRIAL_POINT_RESULT=(None,None,'COUPLED_POINT_TOTAL_FRESH_NONLINEAR_FINITE_RESIDUAL_MEASURED_UNQUALIFIED')
CHANGED_TRIAL_POINT_RECEIPT=(None,None,'CLOSED')
CHANGED_TRIAL_POINT_PROOF=(None,None,None)
CHANGED_TRIAL_POINT_SELECTED=(None,None,'ROOT_CHANGED_TRIAL_POINT_PROVIDER_SELECTED_STAGE_MAP_VERIFIED')
CHANGED_TRIAL_POINT_RECORDS={'input':None,'total_fields':None,'readout':None,'columns':(None,None,None,None)}
CHANGED_TRIAL_POINT_SOURCE_PINS={
 'cross_u_coupled_point_TOTAL_finite_continuation_v005.py':'9095fbd4efbcaddc84c837623b5a88eb68d503de6006f4beae91105a67666db8',
 'author_fragment_fresh_trial_residual_packet_v001.py':'5814945f10ed230da7a26d234c83b49966a2376e692f81a55c0b38d077d48af4',
 'author_fragment_total_trial_fields_to_column_v001.py':'c0c3f97320301834666f35db66195aa5715c182dd2bb29ec4e957433808aaf94',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_chunk_point_block_provider_v001.py':'4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625',
 'author_fragment_candidate_modal_head_point_reconstruction_v001.py':'a49fce7da61d67c514b3cbd3a4b247a0fa17c3a417a0577b26571e3e6daf9827'}
CTP_CACHE_PREFIX='completed_TRIAL_NEW_TEMPORAL_CACHE_cache_'
CTP_RAW_PREFIX='completed_TRIAL_RAW_CANDIDATE_candidate_'
CTP_S={'g':(3784,4,4),'hi':(3784,4,4),'U':(3784,4),'z':(32,3784,4),'P':(3784,4,4),'w':(32,),'omega':(32,)}
CTP_C={'h':(3784,3,3),'ih':(3784,3,3),'N':(3784,),'beta':(3784,3),'u':(3784,3),'up':(3784,3),'gamma':(3784,),'dens':(3784,),'sqrt_h':(3784,),'JU':(3784,4,3),'JzU':(32,3784,3),'Jzz':(3784,3),'Uh':(3784,6,4),'zh':(32,3784,6),'embed':(3784,6,4,4)}
CTP_PAIRS={'A':(32,3784),'NA':(32,3784),'gamma_squared':(3784,),'fixed_E0':(3784,4,4,4),'formal_Iu':(3784,3)}
CTP_ENVELOPES={'h':(3784,3,3),'ih':(3784,3,3),'N':(3784,),'beta':(3784,3),'u':(3784,3),'up':(3784,3),'gamma':(3784,),'dens':(3784,),'sqrt_h':(3784,),'g':(3784,4,4),'hi':(3784,4,4),'U':(3784,4),'z':(32,3784,4),'uc':(3784,4),'P':(3784,4,4),'Z':(3784,4),'r':(3784,4),'z2':(32,3784),'f':(32,3784),'phi':(3784,4),'omega':(32,),'xi':(32,),'w':(32,),'JU':(3784,4,3),'Jzz':(3784,3),'JzU':(32,3784,3),'Uh':(3784,6,4),'zh':(32,3784,6),'embed':(3784,6,4,4)}


def ctp_thin(ref):
    return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}


def changed_trial_point_schema(kind):
    assert kind in ('cache','raw')
    out={}
    for family,shapes in (('s',CTP_S),('c',CTP_C)):
        for name,shape in shapes.items():out[(CTP_CACHE_PREFIX if kind=='cache' else CTP_RAW_PREFIX)+family+'_'+name]=shape
    for name,shape in CTP_ENVELOPES.items():out[(CTP_CACHE_PREFIX+'envelopes_' if kind=='cache' else CTP_RAW_PREFIX+'coefficient_envelopes_')+name]=shape
    if kind=='cache':
        for name,shape in CTP_PAIRS.items():
            for word in ('hi','lo'):out[CTP_CACHE_PREFIX+name+'_'+word]=shape
    assert len(out)==(61 if kind=='cache' else 51)
    return out


def admit_changed_trial_point_provider(result,receipt,proof,selected,bind,read_commit):
    assert not CHANGED_TRIAL_POINT_AUTHOR_DRAFT and not CHANGED_TRIAL_POINT_AUTHORING_IN_PROGRESS
    refs=(CHANGED_TRIAL_POINT_SOURCE,CHANGED_TRIAL_POINT_RESULT,CHANGED_TRIAL_POINT_RECEIPT,CHANGED_TRIAL_POINT_PROOF,CHANGED_TRIAL_POINT_SELECTED)
    assert all(x is not None for ref in refs for x in ref),'Future changed-trial closure and selected map required'
    for ref in refs:bind(ref[0],ref[1])
    for name,h in CHANGED_TRIAL_POINT_SOURCE_PINS.items():bind(name,h)
    assert result['status']==CHANGED_TRIAL_POINT_RESULT[2] and receipt['status']==CHANGED_TRIAL_POINT_RECEIPT[2] and receipt['error_sha256'] is None
    assert proof['status']==CHANGED_TRIAL_POINT_PROOF[2] and proof['source_sha256']==CHANGED_TRIAL_POINT_SOURCE[1] and proof['result_sha256']==receipt['result_sha256']==CHANGED_TRIAL_POINT_RESULT[1] and proof['receipt_sha256']==CHANGED_TRIAL_POINT_RECEIPT[1]
    assert result['owner']==receipt['owner']==proof['owner'] and result['owner']['source_sha256']==CHANGED_TRIAL_POINT_SOURCE[1]
    assert proof['naturally_closed'] is True and type(proof['exit_code']) is int and proof['exit_code']==0
    assert proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is True
    assert result['qualification']==receipt['qualification'] and all(x is False for x in result['qualification'].values())
    case=result['case'];assert case['status']==result['status'] and case['fresh_feedback_required'] is True and case['frozen_proxy_feedback_substituted'] is case['physical_adoption'] is False
    expected={'NEW_finite_residual_sheet_polynomial_transpose'}|{'NEW_finite_residual_NEW_global_'+family+'_'+name+'_polynomial_transpose' for family in ('value','delta') for name in ('normal','CMC')}
    assert len(result['controls'])==len(expected)==5 and {c['name'] for c in result['controls']}==expected and all(c['passed'] is True and c['tolerance']==2e-11 for c in result['controls'])
    assert selected['status']==CHANGED_TRIAL_POINT_SELECTED[2] and selected['source_pins']==CHANGED_TRIAL_POINT_SOURCE_PINS
    closure={'owner':result['owner'],'source':CHANGED_TRIAL_POINT_SOURCE,'result':CHANGED_TRIAL_POINT_RESULT,'receipt':CHANGED_TRIAL_POINT_RECEIPT,'proof':CHANGED_TRIAL_POINT_PROOF}
    canonical=lambda x:json.loads(json.dumps(x))
    assert selected['finite_terminal']==canonical(closure) and selected['reviewed_producer_source']==['cross_u_coupled_point_TOTAL_finite_continuation_v005.py',CHANGED_TRIAL_POINT_SOURCE_PINS['cross_u_coupled_point_TOTAL_finite_continuation_v005.py']]
    assert selected['released_producer_functions_equal_reviewed_source'] is selected['original_basis_and_fixed_E0_source_links_verified'] is True
    assert selected['physical_adoption'] is False and selected['records']==canonical(CHANGED_TRIAL_POINT_RECORDS)
    assert all(CHANGED_TRIAL_POINT_RECORDS[n] is not None for n in ('input','total_fields','readout')) and len(CHANGED_TRIAL_POINT_RECORDS['columns'])==4 and all(c is not None for c in CHANGED_TRIAL_POINT_RECORDS['columns'])
    records=result['checkpoints'];lookup={r['file']:r for r in records};assert len(lookup)==len(records)
    def record(ref,role):
        assert ref['file'] in lookup and ctp_thin(lookup[ref['file']])==ctp_thin(ref)
        actual=lookup[ref['file']];md=actual['metadata'];assert md['owner']==result['owner'] and md['failed'] is False and md['qualification']==result['qualification'] and md['completed_stage_name']==role
        for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][actual[n]]==actual[h];bind(actual[n],actual[h])
        assert read_commit(actual)=={n:actual[n] for n in ('file','sha256','metadata')}
        return actual
    old=selected['records'];inp=record(old['input'],'INPUT');total=record(old['total_fields'],'POINT_TOTAL_TRIAL_FIELDS');readout=record(old['readout'],'TRIAL_CURRENT_LITERAL_AND_UNFEEDBACKED_RESIDUAL')
    assert ctp_thin(total)==ctp_thin(case['trial_fields']) and ctp_thin(readout)==ctp_thin(case['readout'])
    actual_caches=[r for r in records if r['metadata']['completed_stage_name']=='TRIAL_NEW_TEMPORAL_CACHE'];assert len(actual_caches)==4
    columns=[]
    for iq,item in enumerate(old['columns']):
        cache=record(item['cache'],'TRIAL_NEW_TEMPORAL_CACHE');raw=record(item['raw_candidate'],'TRIAL_RAW_CANDIDATE');index=record(item['column_index'],'COLUMN_INDEX')
        assert ctp_thin(cache)==ctp_thin(actual_caches[iq]) and ctp_thin(index)==ctp_thin(case['columns'][iq])
        assert index['metadata']['payload_tags']['column']==iq and raw['metadata']['context']['active_column']==iq
        assert ctp_thin(raw) in index['metadata']['explicit_source_and_child_stage_refs']
        assert ctp_thin(total) in cache['metadata']['explicit_source_and_child_stage_refs']
        for kind,ref in (('cache',cache),('raw',raw)):
            for name,shape in changed_trial_point_schema(kind).items():
                spec=ref['metadata']['schema'][name];assert spec['dtype']=='float64' and spec['finite'] is True and tuple(spec['shape'])==shape
        constants=item['constants'];assert set(constants)=={'ALPHA','ELL','C'} and all(constants[n]==getattr(P,n) for n in constants)
        provenance={'closed_changed_trial':canonical(closure),'column':iq,'cache':ctp_thin(cache),'raw_candidate':ctp_thin(raw),'column_index':ctp_thin(index),'total_fields':ctp_thin(total),'selected_map':CHANGED_TRIAL_POINT_SELECTED[:2],'descriptor_is_source_linked_not_relabelled_original_object':True}
        md={'column':iq,'constants':constants,'schema':{n:cache['metadata']['schema'][n] for n in changed_trial_point_schema('cache')},'candidate_provenance':provenance,'physical_metadata':cache['metadata'],'physical_cache':cache,'physical_raw_candidate':raw}
        columns.append(dict(ctp_thin(cache),metadata=md))
    return {'caches':columns,'input':inp,'preparation':readout,'original_basis':selected['basis_provenance'],'closed_provenance':closure,'physical_adoption':False}


def changed_trial_point_cache_names(metadata):
    expected=changed_trial_point_schema('cache')
    assert set(metadata['schema'])==set(expected)
    return tuple(expected)


def changed_trial_point_hydrate(data,metadata,selection,keep,label):
    assert isinstance(selection,slice) and selection.step in (None,1) and type(selection.start) is type(selection.stop) is int
    lo,hi=selection.start,selection.stop;p=hi-lo;assert 0<=lo<hi<=3784 and 1<=p<=128 and POINT_CHUNK_CAP==128
    local={n:candidate_point_slice(data,n,selection,keep,label+'_copied') for n in changed_trial_point_cache_names(metadata)}
    s={n:local[CTP_CACHE_PREFIX+'s_'+n] for n in CTP_S};c={n:local[CTP_CACHE_PREFIX+'c_'+n] for n in CTP_C}
    pair=lambda n:(local[CTP_CACHE_PREFIX+n+'_hi'],local[CTP_CACHE_PREFIX+n+'_lo'])
    envelopes={n:local[CTP_CACHE_PREFIX+'envelopes_'+n] for n in CTP_ENVELOPES}
    cache={'s':s,'c':c,'p':p,'A':pair('A'),'NA':pair('NA'),'gamma_squared':pair('gamma_squared'),'fixed_E0':pair('fixed_E0'),'formal_Iu':pair('formal_Iu'),'envelopes':envelopes,'constants':dict(metadata['constants']),'candidate_provenance':metadata['candidate_provenance'],'configuration_held':True,'old_coefficients_or_primal_features_replayed':False}
    assert c['N'].shape==(p,) and s['z'].shape==(32,p,4) and s['w'].shape==s['omega'].shape==(32,) and c['JzU'].shape==(32,p,3) and c['zh'].shape==(32,p,6)
    assert np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(c['dens']>0) and np.all(s['omega']>0) and np.all(s['w']>=0)
    assert all(cache['constants'][n]==getattr(P,n) for n in cache['constants'])
    keep(label+'_exact_full_column_point_indices',np.arange(lo,hi,dtype=np.int64));return cache


def prepare_changed_trial_paired_point_provider(admitted,read_closed,seal_completed,clear_completed,describe,check,input_complete):
    assert not CHANGED_TRIAL_POINT_AUTHOR_DRAFT and not CHANGED_TRIAL_POINT_AUTHORING_IN_PROGRESS and CHANGED_TRIAL_POINT_PRIVATE_SCOPE is True
    scope=globals();assert prepare_candidate_point_block_provider.__globals__ is scope and candidate_point_slice.__globals__ is scope and candidate_specialized_temporal_action.__globals__ is scope
    assert POINT_CHUNK_CAP==128 and tuple(CTP_S)==POINT_S and tuple(CTP_C)==POINT_C and admitted['physical_adoption'] is False
    assert callable(read_closed) and callable(input_complete)
    def reader(ref,names):
        md=ref['metadata'];assert tuple(names)==changed_trial_point_cache_names(md)
        cache=md['physical_cache'];raw=md['physical_raw_candidate'];data=read_closed(cache,names);original=read_closed(raw,tuple(changed_trial_point_schema('raw')))
        links=[]
        for name,shape in changed_trial_point_schema('cache').items():
            a=data[name];assert a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
        for family,shapes in (('s',CTP_S),('c',CTP_C),('envelopes',CTP_ENVELOPES)):
            for name,shape in shapes.items():
                left=CTP_CACHE_PREFIX+family+'_'+name;right=CTP_RAW_PREFIX+('coefficient_envelopes' if family=='envelopes' else family)+'_'+name
                a,b=data[left],original[right];assert b.dtype==np.float64 and b.shape==shape and np.all(np.isfinite(b))
                same=bool(np.array_equal(a.view(np.uint64),b.view(np.uint64)));links.append({'cache_member':left,'raw_member':right,'same_uint64_words':same});assert same,(cache['file'],left,raw['file'],right)
        assert len(links)==51 and all(np.all(data[CTP_CACHE_PREFIX+'envelopes_'+n]>=0) for n in CTP_ENVELOPES)
        completed=input_complete(md['column'],cache,raw,links);assert completed['committed'] is True
        return data
    scope.update(candidate_point_cache_names=changed_trial_point_cache_names,candidate_point_hydrate=changed_trial_point_hydrate,POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False,MECHANICAL_SOURCE=CHANGED_TRIAL_POINT_SOURCE,MECHANICAL_RESULT=CHANGED_TRIAL_POINT_RESULT,MECHANICAL_RECEIPT=CHANGED_TRIAL_POINT_RECEIPT,MECHANICAL_CLOSURE_PROOF=CHANGED_TRIAL_POINT_PROOF)
    return prepare_candidate_point_block_provider(admitted,reader,seal_completed,clear_completed,describe,check)
