"""Definitions only; selected earned68607/47969/50104 metadata, no payloads.
Caller supplies bind(name,sha), json and P.path. Returned frozen system includes
its old NONADMITTED solution as a reference, never as a current accepted state.
"""
def t_rate_response_admission():
 parents=(('CROSS_U_INITIAL_YORK_FIVE_FIELD_TARGET_CONTACTS_V001',68607,'155e2bc36ea5a9d8256c9c75008cb2175dce2afc2c2a3e7be4e0dbf5cb95c32f','fe4ae11461ca6bf23301c3dcc10b0e1dc207d4c93ef7d82fd6f99e4c4c107534','cross_u_initial_york_five_field_target_contacts_v001.py','063c5248f3b0ce0bd0190289e1715a5c4083b9a1075fe73d56d6fed08360eaa5','ab2742209785d3e374a0d6f22d2ccc5949eeca771a157c7e93ad86af93e2ad4b'),('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001',47969,'6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc','a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d','cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py','5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18','1f3c5afbb26dd9f43fcea053f92bfad073fdeb75221265d6212772125445e23e'),('CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002',50104,'7289a181e37a8f3277dfc7a587f09bf9078e1d20381eb0c0c371aac2511203be','293295534b3c32ea152641ee4bd54b4cf224a171e3de9e14f2833759787eadaa','cross_u_paired_current_primitive_momentum_readout_v002.py','b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19','0ccd71e96ff40c8105256fd9cce17b68ff06ad0292a726bd1ecac458d8bff30a'))
 rr=[]
 for stem,pid,rh,ch,source,sh,ph in parents:
  for n,h in ((stem+'_RESULT.json',rh),(stem+'_RECEIPT.json',ch),(source,sh),(stem+'.md',ph)):bind(n,h)
  r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==rh and r['owner']==rc['owner'] and r['owner']['pid']==pid and r['owner']['source_sha256']==sh
  assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());rr.append((r,rc))
 def thin(q):return {k:q[k] for k in ('file','sha256','commit_file','commit_sha256')}
 def selected(q,m,output=True,pid=None):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert m[n if output else str(P.path(n).resolve())]==h;bind(n,h)
  raw=json.loads(P.path(q['commit_file']).read_text());assert raw['file']==q['file'] and raw['sha256']==q['sha256'] and (q.get('metadata') is None or q['metadata']==raw['metadata'])
  out=dict(raw,commit_file=q['commit_file'],commit_sha256=q['commit_sha256']);md=out['metadata'];assert md['failed'] is False and all(s['finite'] for s in md['schema'].values())
  if pid is not None:assert md['owner']['pid']==pid
  return out
 target,tr=rr[0];node,nr=rr[1];pilot,pr=rr[2]
 assert len(target['controls'])==2 and len(target['checkpoints'])==7 and all(q['passed'] and q['tolerance']==2e-11 for q in target['controls']) and target['physical_adoption'] is False and target['canonical_primitive_bridge_resolved'] is False
 tp=('READONLY_INITIAL_YORK_FIVE_FIELD_TARGET_CLOSURE_V001_RESULT.json','e6df0f35635b2e89a4d2bbf88e28ff656655dc083f76365a43174a131fc0380c');np=('READONLY_DD_NODE_COORDINATE_WORDS_V001_RESULT.json','ce19e353075341a82b475f019cd3fb6ca6f630868001b479b5aee1760c9bb8fc')
 for n,h in (tp,np):bind(n,h)
 proof=json.loads(P.path(tp[0]).read_text());checked=json.loads(P.path(np[0]).read_text())
 assert proof['status']=='SAVED_INITIAL_YORK_FIVE_FIELD_TARGET_CLOSURE_PASS' and proof['owner_pid']==69140 and proof['controls']==2 and proof['committed_pairs']==7 and proof['physical_adoption'] is False and proof['parent']==dict(pid=68607,result_sha256=parents[0][2],receipt_sha256=parents[0][3])
 assert checked['status']=='SAVED_DD_NODE_COORDINATE_WORDS_PASS' and checked['pid']==48542 and checked['canonical_and_weak_trace_admitted'] is True and checked['parent_terminal']['pid']==47969 and checked['parent_terminal']['result_sha256']==parents[1][2] and checked['parent_terminal']['receipt_sha256']==parents[1][3] and checked['physical_state_or_history_adopted'] is False
 ti=selected(target['input'],tr['output_sha256'],pid=68607);tl=selected(target['loads'],tr['output_sha256'],pid=68607)
 ni=[q for q in node['checkpoints'] if q['metadata']['kind']=='inherited_closed_float_node_nonadmission_and_saved_reader_with_frozen_system'];assert len(ni)==1;ni=selected(ni[0],nr['output_sha256'],pid=47969)
 system=ni['metadata']['system_records'];assert set(system)=={'0','1','2','3','affine','basis','coefficient','solution'};system={k:selected(q,nr['input_sha256'],False) for k,q in system.items()}
 compatibility=selected(node['case']['compatibility'],nr['output_sha256'],pid=47969);assert compatibility['metadata']['canonical_and_trace_admitted'] is True and compatibility['metadata']['physical_adoption'] is False
 assert compatibility['metadata']['schema']['original_rhs']==dict(shape=[403340],dtype='float64',finite=True) and compatibility['metadata']['schema']['current_Pn']==dict(shape=[33,3,87,45],dtype='float64',finite=True)
 columns=[selected(q,pr['output_sha256'],pid=50104) for q in pilot['case']['columns']];assert len(columns)==4 and [q['metadata']['column'] for q in columns]==list(range(4)) and [thin(q) for q in columns]==[thin(q) for q in ti['metadata']['pilot_refs']]
 readout=selected(pilot['case']['readout'],pr['output_sha256'],pid=50104);assert thin(readout)==thin(ti['metadata']['prior_signed_primitive_readout_ref']) and pilot['case']['canonical_primitive_readout_admitted'] is False and readout['metadata']['offsets_targets_or_state_refitted'] is False
 assert thin(system['basis'])==thin(ti['metadata']['shared_basis_ref']) and thin(system['basis'])==thin(compatibility['metadata']['basis_ref'])
 for w in ('hi','lo'):
  assert tl['metadata']['schema']['t_full_coupled_target_RHS_'+w]==dict(shape=[403340],dtype='float64',finite=True) and tl['metadata']['schema']['t_weak_metric_target_'+w]==dict(shape=[6,87,45],dtype='float64',finite=True)
 return dict(target_input=ti,target_loads=tl,node_system=system,node_compatibility=compatibility,pilot_columns=columns,prior_readout=readout,fixed=ti['metadata']['fixed'],bg=ti['metadata']['owned_background'])
