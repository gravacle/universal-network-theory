"""HELD bounded saved-readout recovery-success verifier, root release only.
No numeric-array decoding or scientific bodies. Inherited65759 artifact seals
use authenticated7b70 bytes/headers plus unchanged immutable file stats.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
SOURCE='saved_fixed_geometry_total_rate_column_readout_recovery_v002.py'
SOURCE_SHA='06e5ea35f657ee14624740435bf9e36f1ee84e812dad9adb28304bd623c59075'
STEM='SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002'
RESULT_SHA=None
RECEIPT_SHA=None
NATURAL_CLOSURE=None
PARENT_PROOF=('READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_V001.json','7b70a0936d9ca72ee38fab4a25cd543918c656829750443e50ace9251f875b17','READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_VERIFIED')
PROOF=BASE/'READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_V001.json'
STATUS='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
FLAGS={'physical_adoption':False,'uniform_DD_or_global_inverse_qualified':False,'fresh_current_six_or_normal_CMC_admitted':False,'changed_spatial_geometry':False,'stationarity_feedback_or_new43_earned':False}
np=None;VERIFIED={};STATS={};TOTAL_BYTES=0

def verified(name, digest):
    global TOTAL_BYTES
    p = Path(name); p = (p if p.is_absolute() else BASE / p).resolve()
    key = str(p)
    if key in VERIFIED:
        assert VERIFIED[key] == digest
        s = p.stat(); assert STATS[key] == dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode & 0o777)); return p
    before = p.stat(); assert before.st_size > 0
    h = hashlib.sha256()
    with p.open('rb') as f:
        while block := f.read(1024 * 1024): h.update(block)
    assert h.hexdigest() == digest, name
    after = p.stat()
    assert (before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_ino, after.st_size, after.st_mtime_ns), name
    VERIFIED[key] = digest; TOTAL_BYTES += after.st_size
    STATS[key] = dict(inode=after.st_ino, size=after.st_size, mtime_ns=after.st_mtime_ns, mode=oct(after.st_mode & 0o777))
    return p

def header(f):
    version = np.lib.format.read_magic(f)
    assert version in ((1, 0), (2, 0)), ('unreviewed_public_NPY_header_version', version)
    value = np.lib.format.read_array_header_1_0(f) if version == (1, 0) else np.lib.format.read_array_header_2_0(f)
    return value, version, f.tell()

def thin(ref):
    return {k: ref[k] for k in ('file', 'sha256', 'commit_file', 'commit_sha256')}

def required_pair(md, name, shape):
    for word in ('hi', 'lo'):
        s = md['schema'][name + '_' + word]
        assert s['shape'] == list(shape) and s['dtype'] == 'float64' and s['finite'] is True, name

def carried_seals(parent,receipt):
 carried={}
 for name,digest in receipt['output_sha256'].items():
  p=Path(name);p=(p if p.is_absolute() else BASE/p).resolve();key=str(p);s=p.stat()
  assert parent['verified_sha256'][key]==digest and parent['stable_stats'][key]==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
  assert not s.st_mode&0o222,'Inherited output must remain immutable'
  carried[key]=dict(sha256=digest,stable_stats=parent['stable_stats'][key])
 return carried

def verify_readout(ref,owner):
 ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256'])
 assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
 commit=json.loads(cp.read_bytes());assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
 md=commit['metadata'];assert md['owner']==owner and md['failed'] is False and md['qualification']==FLAGS and md['kind']=='READOUT' and md['physical_adoption'] is False
 for name,shape in dict(current_native=(33,3,87,45),current_metric=(6,87,45),weak_normal=(4,87,45),weak_initial_CMC=(87,45),unchanged_sheet_weak_normal=(4,87,45),normal_CMC_value_time_primary_action_coefficients=(15136,4),normal_CMC_delta_time_primary_action_coefficients=(15136,4)).items():required_pair(md,'completed_READOUT_'+name,shape)
 for family in ('value','delta'):
  for name,shape in (('point_Hamiltonian_normal',(15136,4,3)),('initial_CMC_density',(15136,))):required_pair(md,'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_'+family+'_current_'+name,shape)
 before=ap.stat();versions={}
 with zipfile.ZipFile(ap) as z:
  names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
  for name,schema in md['schema'].items():
   info=z.getinfo(name+'.npy')
   with z.open(info) as f:(shape,order,dtype),version,position=header(f)
   assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and schema['finite'] is True and not dtype.hasobject
   assert position+math.prod(shape)*dtype.itemsize==info.file_size,name;versions[str(version)]=versions.get(str(version),0)+1
  with z.open('metadata_json.npy') as f:
   (shape,order,dtype),version,position=header(f);assert shape==() and dtype.kind=='U';data=f.read();assert len(data)==dtype.itemsize
   big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
   assert json.loads(data.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'))==md
 after=ap.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
 return dict(**thin(ref),member_headers=len(md['schema']),public_header_versions=versions,owner_equal=True,embedded_metadata_equal=True,member_names_headers_and_structural_lengths_equal=True,failed=False,qualification_all_false=True)

def payload_digest(ref,name):
 # Numeric MEMBER BYTES are streamed for copy identity; no numeric decode.
 p=BASE/ref['file'];before=p.stat();h=hashlib.sha256();total=0
 with zipfile.ZipFile(p) as z:
  with z.open(name+'.npy') as f:
   (shape,order,dtype),version,position=header(f);assert list(shape)==ref['metadata']['schema'][name]['shape'] and str(dtype)=='float64'
   while block:=f.read(1048576):h.update(block);total+=len(block)
   assert total==math.prod(shape)*dtype.itemsize
 after=p.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
 return dict(sha256=h.hexdigest(),bytes=total,shape=list(shape),fortran_order=order)

def main():
 global np
 assert not AUTHOR_DRAFT and RESULT_SHA is not None and RECEIPT_SHA is not None and isinstance(NATURAL_CLOSURE,dict),'Root FULL-reviewed natural-success release required'
 assert NATURAL_CLOSURE['naturally_closed'] is True and NATURAL_CLOSURE['exit_code']==0 and isinstance(NATURAL_CLOSURE['pid'],int) and isinstance(NATURAL_CLOSURE['observed_utc'],str) and not PROOF.exists()
 import numpy as numpy
 np=numpy;constants={};source=verified(SOURCE,SOURCE_SHA)
 for n in ast.parse(source.read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:constants[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
 assert constants['STEM']==STEM and constants['STATUS']==STATUS and constants['FLAGS']==FLAGS and constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False
 parent=json.loads(verified(*PARENT_PROOF[:2]).read_bytes());assert parent['status']==PARENT_PROOF[2] and parent['naturally_closed'] is True and parent['exit_code']==1
 assert parent['owner']['pid']==65759 and parent['success_roles']==90 and parent['failed_raw_roles']==1 and parent['original_controls_passed']==0
 for name in ('all_input_seals_verified','all_output_seals_verified','all_success_role_seals_verified','all_failed_raw_seals_verified'):assert parent[name] is True,name
 e=json.loads(verified(*constants['PARENT_ERROR']).read_bytes());orc=json.loads(verified(*constants['PARENT_RECEIPT'][:2]).read_bytes());assert e['owner']==orc['owner']==parent['owner'] and e['controls']==[] and e['qualification']==orc['qualification']==parent['qualification']==FLAGS
 assert parent['source_sha256']==constants['PARENT_SOURCE'][1] and parent['error_sha256']==constants['PARENT_ERROR'][1] and parent['receipt_sha256']==constants['PARENT_RECEIPT'][1]
 assert constants['PARENT_FAILURE_PROOF']==PARENT_PROOF and e['status']=='FAILED' and orc['status']=='CLOSED_ERROR' and orc['error_sha256']==parent['error_sha256']
 carried=carried_seals(parent,orc);assert len(carried)==185
 r=json.loads(verified(STEM+'_RESULT.json',RESULT_SHA).read_bytes());rc=json.loads(verified(STEM+'_RECEIPT.json',RECEIPT_SHA).read_bytes());owner=r['owner']
 assert owner==rc['owner'] and owner['owner']=='root' and owner['pid']==NATURAL_CLOSURE['pid'] and owner['source_sha256']==SOURCE_SHA
 assert r['status']==r['case']['status']==STATUS and rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==RESULT_SHA and r['qualification']==rc['qualification']==FLAGS
 expected=[STEM+'_'+n for n in ('OWNER_START.json','MANIFEST.json','00000_READOUT.npz','00000_READOUT.npz.COMMIT.json','RESULT.json')];assert len(rc['input_sha256'])==111 and set(rc['output_sha256'])==set(expected) and rc['output_sha256'][STEM+'_RESULT.json']==RESULT_SHA
 for side in ('input_sha256','output_sha256'):
  for name,digest in rc[side].items():verified(name,digest)
 assert rc['input_sha256'][str(source.resolve())]==SOURCE_SHA
 for name,digest in constants['PINS'].items():assert rc['input_sha256'][str((BASE/name).resolve())]==digest
 assert rc['input_sha256'][str((BASE/constants['DRIVER_PROTOCOL']).resolve())]==constants['PROTOCOL_SHA']
 assert not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
 assert {p.name for p in BASE.glob(STEM+'_*')}==set(expected)|{STEM+'_RECEIPT.json'}
 assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_bytes())==owner
 manifest=json.loads((BASE/(STEM+'_MANIFEST.json')).read_bytes());assert manifest['owner']==owner and manifest['new_point_ports_or_current_scatters']==0 and manifest['qualification']==FLAGS
 inherited=e['checkpoints'][:90];out=r['checkpoints'][-1];case=r['case'];oldrefs=[thin(q) for q in inherited]
 assert len(r['checkpoints'])==91 and r['checkpoints'][:90]==inherited and r['inherited_success_records']==case['inherited_success_records']==manifest['inherited_success_records']==oldrefs
 assert r['new_owned_records']==case['new_owned_records']==[thin(out)] and thin(out)==case['readout'] and out['file']==STEM+'_00000_READOUT.npz'
 assert rc['inherited_output_sha256']=={q[k]:q[h] for q in inherited for k,h in (('file','sha256'),('commit_file','commit_sha256'))}
 assert case['input']==parent['input'] and case['columns']==parent['columns'] and case['original_targets']==inherited[0]['metadata']['provenance']['unchanged_original_targets'] and case['correction']==inherited[0]['metadata']['correction']
 assert case['original_controls']==0 and case['new_collector_controls']==4 and case['new_point_ports_or_current_scatters']==0
 for flag in ('all16normal_ports_per_section','current99_and_physical6_fresh','spatial_geometry_unchanged'):assert case[flag] is True,flag
 for flag in ('new_current_six_canonical_gates_or_normal_CMC_acceptance','stationarity_feedback_or_new43_earned','physical_adoption'):assert case[flag] is False,flag
 failure=r['ancestor_failure'];assert failure==case['ancestor_failure']==rc['ancestor_failure']==manifest['ancestor_failure']==out['metadata']['ancestor_failure'] and failure['owner']==parent['owner'] and failure['status']=='CLOSED_ERROR' and failure['original_controls']==0 and failure['original_failure_preserved'] is True
 assert failure['source']==list(constants['PARENT_SOURCE']) and failure['error']==list(constants['PARENT_ERROR']) and failure['receipt']==list(constants['PARENT_RECEIPT']) and failure['root_proof']==list(PARENT_PROOF) and failure['failed_raw']==parent['error_raw']
 md=out['metadata'];assert md['provenance']==inherited[0]['metadata']['provenance'] and md['inherited_success_input']==parent['input'] and md['inherited_success_columns']==parent['columns'] and md['completed_current_evidence']==parent['error_raw'] and md['only_unstarted_collector_and_original_mask_restricted_probe'] is True
 names=['NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_'+f+'_'+k+'_polynomial_transpose' for f in ('value','delta') for k in ('normal','CMC')]
 assert len(r['controls'])==4 and [q['name'] for q in r['controls']]==names and [q['ordinal'] for q in r['controls']]==list(range(4))
 for q in r['controls']:
  assert q['passed'] is True and q['tolerance']==2e-11 and math.isfinite(q['error']) and 0<=q['error']<=2e-11
  for field in ('actual','expected','envelope'):assert md['schema']['control_%03d_'%q['ordinal']+q['name']+'_'+field]==dict(shape=[],dtype='float64',finite=True)
 checked=verify_readout(out,owner);ties=[];raw=e['checkpoints'][90]
 for family in ('native','metric'):
  for word in ('hi','lo'):
   a='NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_'+family+'_current_'+word;b='completed_READOUT_current_'+family+'_'+word
   original=payload_digest(raw,a);copied=payload_digest(out,b);assert original==copied;ties.append(dict(original=thin(raw),original_member=a,new=thin(out),new_member=b,**original))
 for name,before in STATS.items():
  s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
 assert carried_seals(parent,orc)==carried
 proof=dict(status='READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE,source_sha256=SOURCE_SHA,result_sha256=RESULT_SHA,receipt_sha256=RECEIPT_SHA,naturally_closed=True,exit_code=0,observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,new_success_roles=1,inherited_success_roles=90,logical_success_roles=91,controls_passed=4,original_controls=0,original_failure_proof=PARENT_PROOF,all_inherited_success_role_seals_verified=True,inherited_seal_method='Authenticated7b70 fullbyte/header proof plus unchanged immutable185-output stats; no full old archive restream',inherited_owner=parent['owner'],original_naturally_closed_exit_code=1,inherited_readonly_seal_stats=carried,readout=checked,current_copy_payload_byte_ties=ties,qualification=FLAGS,numeric_arrays_decoded=False,scientific_actions_or_controls_replayed=False,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,scope='New5output+registeredinput byte/public-header custody and4collector metadata controls; original90scientific successes/failed RAW evidence preserve original owner and natural1; no canonical six/stationarity/geometry/physical admission')
 data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
 with PROOF.open('xb') as f:f.write(data)
 PROOF.chmod(0o444);print(json.dumps(dict(file=PROOF.name,sha256=hashlib.sha256(data).hexdigest(),new_roles=1,inherited_roles=90,controls=4)))
if __name__=='__main__':main()
