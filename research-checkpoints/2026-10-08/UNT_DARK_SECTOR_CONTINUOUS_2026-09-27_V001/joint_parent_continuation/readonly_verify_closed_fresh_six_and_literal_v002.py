"""HELD specific read-only closure verifier: fresh six150 or literal220.
Root alone supplies actual successor/terminal/natural-exit bindings and runs.
Only source AST, byte hashes, public NPY headers and Unicode metadata are read.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, math, re, sys, zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
VERIFY_KIND=None
SOURCE=(None,None)
RESULT=(None,None)
RECEIPT=(None,None)
OBSERVED_PID=None
OBSERVED_SESSION=None
ROOT_NATURALLY_CLOSED=None
ROOT_OBSERVED_EXIT_CODE=None
PROOF_FILE=None
TEMPLATES={
 'six':('closed_fixed_geometry_total_rate_original_six_v002.py','a238f1b16468b6be585fef7a93f9a694bd08dfe989d0fa1fef7ef15dc0c361a1'),
 'literal':('cross_u_refreshed_total_rate_literal_gradient_contacts_v002.py','5d1b4b30c01616c0514446b9546f9a6c434423c0723891fa8fec487d4dff0080')}
VERIFIED={};STATS={};TOTAL_BYTES=0;HEADER_COUNT=0;METADATA_BYTES=0

def path(name):
 p=Path(name);return p if p.is_absolute() else BASE/p

def verified(name,digest):
 global TOTAL_BYTES
 p=path(name);key=str(p.resolve());before=p.stat()
 if key in VERIFIED:
  assert VERIFIED[key]==digest and STATS[key]==(before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode);return p
 assert isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest) and before.st_size>0
 h=hashlib.sha256()
 with p.open('rb') as f:
  while block:=f.read(1024*1024):h.update(block)
 after=p.stat();assert h.hexdigest()==digest and (before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode),name
 VERIFIED[key]=digest;STATS[key]=(after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode);TOTAL_BYTES+=after.st_size;return p

def constants(file):
 tree=ast.parse(file.read_text());out={};wanted={'STEM','FLAGS','AUTHOR_DRAFT','AUTHORING_IN_PROGRESS','DRIVER_PROTOCOL','PROTOCOL_SHA','FINITE_SOURCE','FINITE_RESULT','FINITE_RECEIPT','FINITE_CLOSURE_PROOF','ANCHOR_SOURCE','ANCHOR_RESULT','ANCHOR_RECEIPT','ANCHOR_PROOF'}
 for n in tree.body:
  if not isinstance(n,ast.Assign) or len(n.targets)!=1 or not isinstance(n.targets[0],ast.Name) or n.targets[0].id not in wanted:continue
  value=n.value
  if isinstance(value,ast.Call):
   assert n.targets[0].id=='FLAGS' and isinstance(value.func,ast.Name) and value.func.id=='dict' and not value.args and all(k.arg for k in value.keywords)
   out['FLAGS']={k.arg:ast.literal_eval(k.value) for k in value.keywords}
  else:out[n.targets[0].id]=ast.literal_eval(value)
 return out,tree

def thin(q):return {k:q[k] for k in ('file','sha256','commit_file','commit_sha256')}

def archive_record(q,ordinal,role,stem,owner,flags,receipt,np):
 global HEADER_COUNT,METADATA_BYTES
 assert q['file']==f"{stem}_{ordinal:05d}_{role}.npz" and q['commit_file']==q['file']+'.COMMIT.json'
 for a,b in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][q[a]]==q[b]
 archive=verified(q['file'],q['sha256']);commit=verified(q['commit_file'],q['commit_sha256'])
 assert not archive.stat().st_mode&0o222 and not commit.stat().st_mode&0o222
 cm=json.loads(commit.read_bytes());assert set(cm)=={'file','sha256','metadata'} and cm['file']==q['file'] and cm['sha256']==q['sha256']
 md=cm['metadata'];assert md==q['metadata'] and md['owner']==owner and md['failed'] is False and md['qualification']==flags
 def header(f):
  version=np.lib.format.read_magic(f)
  if version==(1,0):return np.lib.format.read_array_header_1_0(f)
  if version==(2,0):return np.lib.format.read_array_header_2_0(f)
  raise AssertionError(('Unsupported public NPY header',version))
 with zipfile.ZipFile(archive) as z:
  assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
  for name,schema in md['schema'].items():
   info=z.getinfo(name+'.npy')
   with z.open(info) as f:shape,order,dtype=header(f);length=f.tell()
   assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and schema['finite'] is True and not dtype.hasobject
   assert info.file_size==length+math.prod(shape)*dtype.itemsize;HEADER_COUNT+=1
  with z.open('metadata_json.npy') as f:
   shape,order,dtype=header(f);assert shape==() and dtype.kind=='U' and not dtype.hasobject
   raw=f.read();assert len(raw)==dtype.itemsize;METADATA_BYTES+=len(raw)
   big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
   assert json.loads(raw.decode('utf-32-be' if big else 'utf-32-le').rstrip('\0'))==md
 return md

def schema(md,key,shape):assert md['schema'][key]==dict(shape=shape,dtype='float64',finite=True),key

def verify_six(r,metadata):
 case=r['case'];controls=r['controls'];assert len(metadata)==2 and len(controls)==6
 names=[a+'_'+b for a in ('native_original_affine','native_original_canonical','metric_NEW_target') for b in ('raw','scaled')]
 assert [c['name'] for c in controls]==names and [c['ordinal'] for c in controls]==list(range(6)) and [len(row) for row in case['scores']]==[2,2,2]
 flat=[v for row in case['scores'] for v in row];zero=case['zero_reference_flags'];assert len(zero)==3 and all(type(v) is bool for v in zero)
 assert len(case['norms_references_thresholds'])==3 and all(len(row)==6 and all(math.isfinite(v) and v>=0 for v in row) for row in case['norms_references_thresholds'])
 for i,(c,v) in enumerate(zip(controls,flat)):
  assert type(v) in (int,float) and math.isfinite(v) and v>=0 and c['score']==v and c['tolerance']==1e-10 and c['passed'] is (v<=1e-10)
  assert c['relative_ratio_defined'] is (not zero[i//2]) and c['exact_zero_reference_rule'] is zero[i//2]
 admitted=all(c['passed'] for c in controls);assert case['original_six_admitted'] is admitted
 assert r['status']==case['status']==('FRESH_TOTAL_RATE_ORIGINAL_SIX_ADMITTED' if admitted else 'FRESH_TOTAL_RATE_ORIGINAL_SIX_MEASURED_NOT_ADMITTED')
 inp,cert=metadata;assert case['input']==thin(r['checkpoints'][0]) and case['certificate']==thin(r['checkpoints'][1]) and cert['input']==case['input']
 assert cert['six_gate_names']==names and cert['scores']==case['scores'] and cert['norms_references_thresholds']==case['norms_references_thresholds'] and cert['zero_reference_flags']==case['zero_reference_flags']
 assert cert['original_six_admitted'] is admitted and cert['metric_denominator_is_original_anchor_epsilon'] is inp['original_metric_epsilon_reference_is_fixed'] is True
 assert cert['no_action_EOS_solver_or_scatter_replay'] is True and cert['normal_CMC_or_physical_acceptance'] is case['normal_CMC_stationarity_evolution_and_new43_acceptance'] is case['physical_adoption'] is False
 assert inp['finite_terminal']==case['finite_terminal'] and inp['anchor_terminal']==case['anchor_terminal']
 for n,shape in (('original_rhs',[403340]),('current_Pn',[33,3,87,45]),('native_scale',[33,3,87,45]),('metric_scale',[6,87,45])):schema(inp,'anchor_INPUT_original_reference_'+n,shape)
 for group,shape in (('native',[33,3,87,45]),('metric',[6,87,45])):
  for word in ('hi','lo'):
   schema(inp,'anchor_CANONICAL_NEW_reference_anchor_unchanged_or_prepared_target_'+group+'_'+word,shape);schema(inp,'finite_READOUT_completed_READOUT_current_'+group+'_'+word,shape)
 for word in ('hi','lo'):schema(inp,'anchor_CANONICAL_NEW_reference_anchor_target_minus_current_epsilon_metric_'+word,[6,87,45])
 schema(cert,'unchanged_original_metric_epsilon_reference_both_words',[2,6,87,45]);schema(cert,'FRESH_TOTAL_RATE_ORIGINAL_SIX_exact_zero_reference_authoritative_scores',[3,2])
 return dict(original_six_admitted=admitted,measured_not_admitted_is_valid_closure=True,original_metric_epsilon_denominator_preserved=True,controls_may_be_false=True)

def verify_literal(r,metadata):
 case=r['case'];roles=['INPUT','CANONICAL_COPY','DIRECTION']+['TRANSACTION_COPY','GRADIENT_COLUMN','JET_COLUMN','COMPONENT_CONTACT']*4+['EVALUATION_TRANSPOSE','WEAK_BRIDGE','WEAK_CONTACT','PREPARATION']
 assert len(metadata)==len(roles)==23 and case['roles']==23 and case['new_controls']==26
 assert r['status']==case['status']=='REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS'
 expected=[f'NEW_refreshed_literal_q{i}_independent_'+n for i in range(4) for n in ('Maxwell','modal_V','modal_D','acceleration','formal_native','formal_EH')]+['NEW_refreshed_weighted_Estar_polynomial_'+n for n in ('native','metric')]
 assert [c['name'] for c in r['controls']]==expected and [c['ordinal'] for c in r['controls']]==list(range(26)) and all(c['passed'] is True and c['tolerance']==2e-11 and 0<=c['error']<=2e-11 for c in r['controls'])
 assert case['source_polynomial_only'] is True and case['normal_feedback_or_geometry_correction_admitted'] is case['physical_adoption'] is False
 for key,ordinal in (('input',0),('canonical_copy',1),('literal_weak',19),('stationarity_bridge',20),('preparation',22)):assert case[key]==thin(r['checkpoints'][ordinal])
 assert case['transactions']==[thin(r['checkpoints'][3+4*i]) for i in range(4)] and case['columns']==[thin(r['checkpoints'][4+4*i]) for i in range(4)]
 for i in range(4):
  tx,g,j,c=metadata[3+4*i:7+4*i];assert all(m['column']==i for m in (tx,g,j,c))
  assert tx['same_raw_configuration_and_E0_words_verified'] is True and tx['old_rate_dependent_current_contacts_reused'] is False and g['transaction']==j['transaction']==case['transactions'][i]
  assert c['gradient']==case['columns'][i] and c['jets']==thin(r['checkpoints'][5+4*i]) and c['controls']==r['controls'][6*i:6*(i+1)]
 inp,canonical=metadata[:2];weak,bridge,contact,prep=metadata[19:23]
 assert canonical['anchor']==inp['anchor_canonical'] and canonical['fresh_current']==inp['finite_readout'] and canonical['metric_denominator_is_original_anchor_epsilon'] is canonical['original_targets_and_scales_unchanged'] is canonical['registered_current_copied_not_rescattered'] is True
 assert bridge['canonical']==case['canonical_copy'] and bridge['literal']==case['literal_weak'] and bridge['finite_readout']==inp['finite_readout']
 assert bridge['epsilon_sign']=='target minus registered current' and bridge['eL_sign']=='epsilon minus (literal minus registered)'
 assert bridge['same_new_state_adjoint_required'] is True and bridge['old_lambda_or_gauge_current_reused'] is bridge['stationarity_or_feedback_zero_assumed'] is False
 assert weak['columns']==case['columns'] and weak['registered_S_association_distinct'] is weak['literal_weak_from_fresh_current'] is True
 assert contact['literal']==case['literal_weak'] and contact['controls']==r['controls'][-2:] and contact['independent_Fraction_original_rounded_maps'] is True
 assert prep['input']==case['input'] and prep['canonical_copy']==case['canonical_copy'] and prep['stationarity_bridge']==case['stationarity_bridge'] and prep['columns']==case['columns'] and prep['new_rate_dependent_feedback_required'] is True
 for n in ('NEW_literal_stationarity_eL_packed','NEW_literal_registered_epsilon_packed'):
  for word in ('hi','lo'):schema(bridge,n+'_'+word,[403340])
 for n in ('NEW_literal_original_scale_packed','NEW_literal_source_operation_bound_packed'):schema(bridge,n,[403340])
 return dict(stationarity_bridge=case['stationarity_bridge'],eL_sign=bridge['eL_sign'],old_lambda_adoption=False,new_same_state_adjoint_required=True,max_control_error=max(c['error'] for c in r['controls']))

def main():
 assert not AUTHOR_DRAFT and VERIFY_KIND in TEMPLATES and all(v is not None for q in (SOURCE,RESULT,RECEIPT) for v in q),'Root binding/release after actual natural closure only'
 assert type(OBSERVED_PID) is int and type(OBSERVED_SESSION) is int and ROOT_NATURALLY_CLOSED is True and type(ROOT_OBSERVED_EXIT_CODE) is int and ROOT_OBSERVED_EXIT_CODE==0
 assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not path(PROOF_FILE).exists()
 template=verified(*TEMPLATES[VERIFY_KIND]);source=verified(*SOURCE);c,t=constants(source);original_constants,original=constants(template)
 old={n.name:ast.dump(n,include_attributes=False) for n in original.body if isinstance(n,ast.FunctionDef)};new={n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)};assert old==new,'Scientific successor changes need a separate review'
 assert c['AUTHOR_DRAFT'] is c['AUTHORING_IN_PROGRESS'] is False and c['FLAGS']==original_constants['FLAGS'] and all(v is False for v in c['FLAGS'].values())
 stem=c['STEM'];assert RESULT[0]==stem+'_RESULT.json' and RECEIPT[0]==stem+'_RECEIPT.json'
 r=json.loads(verified(*RESULT).read_bytes());rc=json.loads(verified(*RECEIPT).read_bytes())
 assert r['owner']==rc['owner'] and r['owner']['pid']==OBSERVED_PID and r['owner']['source_sha256']==SOURCE[1]
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==RESULT[1] and r['qualification']==rc['qualification']==c['FLAGS']
 assert rc['input_sha256'][str(source.resolve())]==SOURCE[1] and rc['input_sha256'][str(path(c['DRIVER_PROTOCOL']).resolve())]==c['PROTOCOL_SHA']
 assert not path(stem+'_ERROR.json').exists() and not path(stem+'_ERROR_RECEIPT.json').exists()
 for side in ('input_sha256','output_sha256'):
  for name,digest in rc[side].items():verified(name,digest)
 import numpy as np
 roles=['INPUT','CERTIFICATE'] if VERIFY_KIND=='six' else ['INPUT','CANONICAL_COPY','DIRECTION']+['TRANSACTION_COPY','GRADIENT_COLUMN','JET_COLUMN','COMPONENT_CONTACT']*4+['EVALUATION_TRANSPOSE','WEAK_BRIDGE','WEAK_CONTACT','PREPARATION']
 assert len(r['checkpoints'])==len(roles)
 md=[archive_record(q,i,roles[i],stem,r['owner'],c['FLAGS'],rc,np) for i,q in enumerate(r['checkpoints'])]
 assert len(md)==(2 if VERIFY_KIND=='six' else 23)
 expected={q[k] for q in r['checkpoints'] for k in ('file','commit_file')}|{stem+'_OWNER_START.json',stem+'_MANIFEST.json',stem+'_RESULT.json'}
 assert set(rc['output_sha256'])==expected,'Extra or missing closing output/census'
 owner=json.loads(verified(stem+'_OWNER_START.json',rc['output_sha256'][stem+'_OWNER_START.json']).read_bytes());manifest=json.loads(verified(stem+'_MANIFEST.json',rc['output_sha256'][stem+'_MANIFEST.json']).read_bytes());assert owner==manifest['owner']==r['owner']
 if VERIFY_KIND=='six':assert manifest['closed_sources']==md[0]['sources'] and manifest['new_scientific_producer_calls']==0 and manifest['physical_adoption'] is False
 else:assert manifest['future_finite_terminal']==r['case']['finite_terminal'] and manifest['new_literal142_sections']==4 and manifest['new_controls']==26 and manifest['physical_adoption'] is False
 assert r['case']['finite_terminal']==json.loads(json.dumps([c[n] for n in ('FINITE_SOURCE','FINITE_RESULT','FINITE_RECEIPT','FINITE_CLOSURE_PROOF')]))
 assert r['case']['anchor_terminal']==json.loads(json.dumps([c[n] for n in ('ANCHOR_SOURCE','ANCHOR_RESULT','ANCHOR_RECEIPT','ANCHOR_PROOF')]))
 details=verify_six(r,md) if VERIFY_KIND=='six' else verify_literal(r,md)
 for name,before in STATS.items():
  s=Path(name).stat();assert before==(s.st_ino,s.st_size,s.st_mtime_ns,s.st_mode),name
 proof=dict(status='READONLY_NATURAL_CLOSED_FRESH_SIX_MEASURED_SEALS_VERIFIED' if VERIFY_KIND=='six' else 'READONLY_NATURAL_CLOSED_REFRESHED_LITERAL_EL_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=r['owner'],source_sha256=SOURCE[1],result_sha256=RESULT[1],receipt_sha256=RECEIPT[1],naturally_closed=True,exit_code=0,natural_exit_authority='Root-observed release fields; verifier does not infer process exit from JSON',observed_session=OBSERVED_SESSION,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_seals_verified=len(rc['input_sha256']),output_seals_verified=len(rc['output_sha256']),roles=len(md),role_inventory=roles,controls=len(r['controls']),details=details,public_headers_verified=HEADER_COUNT,embedded_unicode_metadata_bytes=METADATA_BYTES,numeric_arrays_decoded=False,numeric_finiteness_scope='Authenticated producer schema finite=true only; no numeric scan',total_bytes_verified=TOTAL_BYTES,qualification=c['FLAGS'],physical_adoption=False,old_actions_or_controls_replayed=False)
 out=path(PROOF_FILE)
 with out.open('x') as f:json.dump(proof,f,sort_keys=True,indent=2);f.write('\n')
 out.chmod(0o444);print(out.name,hashlib.sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':main()
