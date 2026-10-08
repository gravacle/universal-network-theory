"""HELD import-free ancestor record custody for150/220 and selected consumers.
The containing producer owns its future natural-success binding and release.
No numeric archive, scientific operation or original owner is rewritten.
"""
FIXED_RATE_INHERITED_ADMISSION_AUTHOR_DRAFT=True

def fixed_rate_inherited_success_admission(result,receipt,bind):
 if 'ancestor_failure' not in result:return None
 expected=dict(source=('cross_u_fixed_geometry_total_rate_state_evaluation_v004.py','59f23b9476d38aadc8297c104d4cf8e5ab217ac1ce3a0bc077e34f2fec99b39f'),error=('CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004_ERROR.json','183070c4620623ee5f82f93f8c65de2a73815c0c60bcaeead64ea6fcecb09fea'),receipt=('CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004_RECEIPT.json','fa2972d289c42d29be375c1d42e3533ec0d40ddd67724adebf0a1e3d4928487d','CLOSED_ERROR'),root_proof=('READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_V001.json','7b70a0936d9ca72ee38fab4a25cd543918c656829750443e50ace9251f875b17','READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_VERIFIED'))
 expected=json.loads(json.dumps(expected));ancestor=result['ancestor_failure']
 assert ancestor==result['case']['ancestor_failure']==receipt['ancestor_failure']
 for name,q in expected.items():assert ancestor[name]==q;bind(q[0],q[1])
 assert all(P.path(expected[name][0]).stat().st_size<=128*1024*1024 for name in ('error','receipt','root_proof'))
 error=json.loads(P.path(expected['error'][0]).read_text());old_rc=json.loads(P.path(expected['receipt'][0]).read_text());proof=json.loads(P.path(expected['root_proof'][0]).read_text())
 owner=error['owner'];assert owner==old_rc['owner']==proof['owner']==ancestor['owner'] and owner['owner']=='root' and owner['pid']==65759 and owner['source_sha256']==expected['source'][1]
 assert owner!=result['owner'] and result['owner']==receipt['owner']
 assert error['status']=='FAILED' and old_rc['status']==ancestor['status']=='CLOSED_ERROR' and old_rc['error_sha256']==expected['error'][1] and old_rc['prior_receipt_sha256'] is None
 assert proof['status']==expected['root_proof'][2] and proof['source_sha256']==expected['source'][1] and proof['error_sha256']==expected['error'][1] and proof['receipt_sha256']==expected['receipt'][1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1
 for name in ('all_input_seals_verified','all_output_seals_verified','all_success_role_seals_verified','all_failed_raw_seals_verified'):assert proof[name] is True
 assert proof['success_roles']==90 and proof['failed_raw_roles']==1 and proof['original_controls_passed']==0 and proof['controls']==error['controls']==[]
 assert error['raw_preservation_traceback'] is error['closing_traceback'] is None
 assert error['qualification']==old_rc['qualification']==proof['qualification'] and all(v is False for v in error['qualification'].values())
 assert ancestor['original_RESULT_absent'] is ancestor['original_failure_preserved'] is True and ancestor['original_controls']==0 and not P.path('CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004_RESULT.json').exists()
 original=error['checkpoints'];assert len(original)==len(proof['records'])==91 and ancestor['failed_raw']==thin(original[90])==proof['error_raw'] and original[90]['metadata']['failed'] is True
 old=original[:90];refs=[thin(q) for q in old];assert result['checkpoints'][:90]==old and result['inherited_success_records']==result['case']['inherited_success_records']==refs
 assert len(result['checkpoints'])==91 and len(result['new_owned_records'])==1 and result['new_owned_records']==result['case']['new_owned_records']==[result['case']['readout']]==[thin(result['checkpoints'][-1])]
 new=result['checkpoints'][-1];assert new['metadata']['owner']==result['owner'] and new['metadata']['kind']=='READOUT' and new['metadata']['failed'] is False
 inherited={q[k]:q[h] for q in old for k,h in (('file','sha256'),('commit_file','commit_sha256'))};assert receipt['inherited_output_sha256']==inherited
 assert not set(inherited)&set(receipt['output_sha256'])
 for i,(q,pr) in enumerate(zip(old,proof['records'][:90])):
  assert thin(q)==thin(pr) and pr['ordinal']==i and pr['failed'] is False and q['metadata']['owner']==owner and q['metadata']['failed'] is False
  assert q['metadata']['qualification']==error['qualification']
  for name,digest in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert old_rc['output_sha256'][name]==inherited[name]==digest
 return dict(owner=owner,records={q['file']:thin(q) for q in old},output_sha256=inherited,ancestor_failure=ancestor)

def fixed_rate_record_seals(result,receipt,record):
 md=record['metadata'];assert md['failed'] is False
 if md['owner']==result['owner']:return receipt['output_sha256']
 context=receipt.get('_fixed_rate_inherited_success');assert context is not None and md['owner']==context['owner']
 assert context['records'].get(record['file'])==thin(record) and receipt['inherited_output_sha256']==context['output_sha256']
 return receipt['inherited_output_sha256']
