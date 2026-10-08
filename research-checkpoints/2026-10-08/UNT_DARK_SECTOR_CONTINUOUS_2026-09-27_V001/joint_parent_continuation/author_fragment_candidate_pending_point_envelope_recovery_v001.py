"""HELD selective saved point-chunk recovery and outward numerical envelopes.
Globals np,P,json,thin; original133 provider passed by caller. No old action.
First earned chunk is copied from authenticated CLOSED14122 output. Other
chunks are NEW. Real coefficients, pairs, gaps and source remain unchanged.
Enclosures are numerical right-factor operands, never new physics or gates.
"""
POINT_RECOVERY_AUTHOR_DRAFT=True
POINT_RECOVERY_AUTHORING_IN_PROGRESS=False
POINT_PENDING_SOURCE=(None,None)
POINT_PENDING_ERROR=(None,None,'FAILED')
POINT_PENDING_RECEIPT=(None,None,'CLOSED_ERROR')
POINT_PENDING_CLOSURE_PROOF=(None,None,'ROOT_NATURAL_CLOSED_NODAL_POINT_ENVELOPE_PARTIAL_SEALS_VERIFIED')

def candidate_point_outward_envelopes(point,keep,label):
 # gamma_2048 conservatively encloses the short positive contractions. The
 # independent pair magnitude is enclosed by an upward nextafter sum.
 eps=np.finfo(np.float64).eps;gamma=2048*eps/(1-2048*eps)
 keep(label+'_numerical_positive_flow_gamma2048',np.asarray(gamma))
 for n in ('H','B','E','D'):
  raw=keep(label+'_raw_uncancelled_e'+n,point['e'+n].copy());pair=point['paired_raw'][n]
  assert raw.shape==pair[0].shape==pair[1].shape==point[n].shape
  assert np.all(raw>=0) and np.all(np.isfinite(raw))
  zero=raw==0;assert all(np.all(w[zero]==0) for w in pair),'Missing positive-flow term; zero envelope cannot be repaired'
  pair_bound=np.nextafter(abs(pair[0])+abs(pair[1]),np.inf)
  padded=np.nextafter(raw*(1+gamma),np.inf)
  pair_bound[zero]=0.;padded[zero]=0.
  # A discrepancy larger than positive-flow rounding is a genuine blocker.
  assert np.all(pair_bound<=padded),'Positive-flow bound mismatch exceeds declared rounding enclosure'
  bound=np.nextafter(np.maximum(padded,pair_bound),np.inf);bound[zero]=0.
  keep(label+'_represented_pair_magnitude_upper_'+n,pair_bound.copy())
  keep(label+'_outward_positive_flow_e'+n,bound.copy())
  keep(label+'_enclosure_increment_e'+n,(bound-raw).copy())
  assert np.all(np.isfinite(bound)) and np.all(bound>=abs(point[n]))
  point['e'+n]=bound
 return point

def prepare_candidate_pending_point_recovery(admitted,provider,bind,read_closed,seal_completed,clear_completed,keep):
 assert not POINT_RECOVERY_AUTHOR_DRAFT and not POINT_RECOVERY_AUTHORING_IN_PROGRESS
 refs=(POINT_PENDING_SOURCE,POINT_PENDING_ERROR,POINT_PENDING_RECEIPT,POINT_PENDING_CLOSURE_PROOF)
 assert all(x is not None for ref in refs for x in ref)
 for ref in refs:bind(ref[0],ref[1])
 error=json.loads(P.path(POINT_PENDING_ERROR[0]).read_text());rc=json.loads(P.path(POINT_PENDING_RECEIPT[0]).read_text());proof=json.loads(P.path(POINT_PENDING_CLOSURE_PROOF[0]).read_text())
 assert error['status']==POINT_PENDING_ERROR[2] and rc['status']==POINT_PENDING_RECEIPT[2] and proof['status']==POINT_PENDING_CLOSURE_PROOF[2]
 assert error['owner']==rc['owner']==proof['owner'] and proof['source_sha256']==POINT_PENDING_SOURCE[1]
 assert proof['error_sha256']==POINT_PENDING_ERROR[1]==rc['error_sha256'] and proof['receipt_sha256']==POINT_PENDING_RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1 and proof['all_input_seals_verified'] is True and proof['all_committed_role_seals_verified'] is True and proof['failed_raw_preserved'] is True
 assert proof['earned_new_point_directions']==12 and proof['no_moment_or_factor_computed'] is True and proof['pending_unit_has_earned_point_actions'] is True
 assert error['raw_preservation_traceback'] is None and error['closing_traceback'] is None
 controls=error['controls'];assert len(controls)==3 and all(x['passed'] and x['tolerance']==2e-11 for x in controls)
 ref=error['checkpoints'][-2];assert thin(ref)==proof['completed_point_chunk']
 for key,hkey in (('file','sha256'),('commit_file','commit_sha256')):bind(ref[key],ref[hkey]);assert rc['output_sha256'][ref[key]]==ref[hkey]
 assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
 md=ref['metadata'];assert md['owner']==error['owner'] and md['failed'] is False and md['source']['column']==0 and md['source']['selection']==[0,128]
 expected=json.loads(P.encode(admitted['closed_provenance']).decode());assert md['source']['closed_mechanical']==expected
 assert md['closed_candidate_provenance']==admitted['caches'][0]['metadata']['candidate_provenance']
 stem='NEW_directed_nodal_q0_chunk000_NEW_point';labels=dict(H=stem+'_NEW_HE_H9',B=stem+'_NEW_B_head_from_arm',E=stem+'_NEW_HE_arm_from_head',D=stem+'_NEW_D')
 names=tuple(v+tail for v in labels.values() for tail in ('_real_binary64_readout','_represented_pair_hi','_represented_pair_lo','_represented_pair_minus_real_hi','_represented_pair_minus_real_lo'))+tuple(stem+'_e'+n for n in labels)
 consumed=False
 def wrapped(column,selection,keep,label):
  nonlocal consumed
  if column==0 and selection.start==0 and selection.stop==128:
   assert not consumed;consumed=True;data=read_closed(ref,names);point={};pairs={};gaps={}
   for n,v in labels.items():
    point[n]=keep(label+'_inherited_'+n,data[v+'_real_binary64_readout'].copy());point['e'+n]=keep(label+'_inherited_raw_e'+n,data[stem+'_e'+n].copy())
    pairs[n]=tuple(keep(label+'_inherited_pair_'+n+'_'+w,data[v+'_represented_pair_'+w].copy()) for w in ('hi','lo'))
    gaps[n]=tuple(keep(label+'_inherited_readout_gap_'+n+'_'+w,data[v+'_represented_pair_minus_real_'+w].copy()) for w in ('hi','lo'))
    assert np.array_equal(point[n],pairs[n][0]+pairs[n][1])
   point.update(paired_raw=pairs,readout_gaps=gaps,closed_candidate_provenance=md['closed_candidate_provenance'],construction_contacts=md['construction_contacts'],source=md['source'],global_or_uniform_DD_inverse_qualified=False,physical_adoption=False)
   candidate_point_outward_envelopes(point,keep,label+'_NEW_enclosure')
   record=seal_completed('POINT_BLOCK_RESTORE',dict(kind='copied_earned_closed_point_chunk_with_NEW_outward_envelopes',original_point_chunk=thin(ref),closure_proof=POINT_PENDING_CLOSURE_PROOF,inherited_controls=controls,source=md['source'],closed_candidate_provenance=md['closed_candidate_provenance'],no_old_point_action_replayed=True,real_pairs_gaps_unchanged=True,physical_adoption=False));clear_completed();point['committed_chunk']=thin(record)
   return point
  result=provider(column,selection,keep,label)
  return candidate_point_outward_envelopes(result,keep,label+'_NEW_enclosure')
 return wrapped,dict(inherited_point_actions=12,inherited_controls=controls,closed_pending_chunk=thin(ref),proof=POINT_PENDING_CLOSURE_PROOF,new_raw_point_chunks=119,real_coefficient_or_gate_change=False)
