"""HELD exact NEW139 config/Cg/Rv current preparation custody, root only."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,re,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
KIND=OUTCOME=None
SOURCE=('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py', 'e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222')
RESULT=('CROSS_U_NEW139_MECHANICAL_GAUGE_CURRENT_PREPARATION_V005_RESULT.json', 'a9bf500be217f474512ee257b850987ff953e0649793d0f8e06e7d265e8317e4', 'NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED')
ERROR=(None,None)
RECEIPT=('CROSS_U_NEW139_MECHANICAL_GAUGE_CURRENT_PREPARATION_V005_RECEIPT.json', '4fdf278c6141338671a014f43dd4c8cc8bd90fc8c27221f674ae541b8ee31294', 'CLOSED')
NATURAL_CLOSURE=PROOF_FILE=None
PROTOCOL='READONLY_CLOSED_NEW139_COMPONENT_PREPARATION_SEALS_V006.md'
PROTOCOL_SHA='d1bc500391ea710c73f5997029cc18b4b9d1696e2084378a31999bbd095edc28'
MAX_RECORD_TEXT=16*1024*1024
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
SPECS={
 'configuration':dict(source=('cross_u_NEW139_configuration_three_unit_preparation_v006.py','6789a603ca989f27ac97f0e91f69902b29d6e4899012931d9ccbe89de451dfbe'),stem='CROSS_U_NEW139_CONFIGURATION_THREE_UNIT_PREPARATION_V006',pid=89539,session=8018,roles=494,controls=1440,status='NEW139_THREE_CHI_COEFFICIENTS_AND_SOURCE_ENVELOPES_PREPARED_UNQUALIFIED'),
 'gauge':dict(source=('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222'),stem='CROSS_U_NEW139_MECHANICAL_GAUGE_CURRENT_PREPARATION_V005',pid=89675,session=42171,roles=74,controls=44,status='NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED'),
 'rate':dict(source=('cross_u_NEW139_literal_rate_normal_refresh_preparation_v004.py','8b3597e2ac268ab9ef63439f329ecbf270f42f89e3685bd25a7cb4420df4bb5c'),stem='CROSS_U_NEW139_LITERAL_RATE_NORMAL_REFRESH_PREPARATION_V004',pid=91239,session=43469,roles=2050,controls=0,status='NEW139_LITERAL_RATE_NORMAL_COEFFICIENTS_REFRESHED_UNQUALIFIED')}
SPECS['rate_failure_v004']=dict(SPECS['rate'],family='rate',outcome_required='FAILURE')
SPECS['rate']=dict(SPECS['rate'],source=('cross_u_NEW139_literal_rate_normal_refresh_preparation_v005.py','3deb4cfc0700adb932abc5713daf0b6a833a538cf29fdfe05082017af48b129e'),stem='CROSS_U_NEW139_LITERAL_RATE_NORMAL_REFRESH_PREPARATION_V005',pid=None,session=47707)
np=None
VERIFIED={};STATS={};TOTAL_BYTES=0

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

def unique_object(pairs):
    value={}
    for key,item in pairs:assert key not in value,key;value[key]=item
    return value

def small_json(path,limit=MAX_RECORD_TEXT):
    assert path.stat().st_size<=limit,path.name
    return json.loads(path.read_bytes(),object_pairs_hook=unique_object)

def source_constants(path):
    constants={}
    for n in ast.parse(path.read_text()).body:
        if not isinstance(n,ast.Assign) or len(n.targets)!=1 or not isinstance(n.targets[0],ast.Name):continue
        name=n.targets[0].id
        if name=='FLAGS':
            assert isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='dict' and not n.value.args
            assert all(k.arg is not None for k in n.value.keywords)
            constants[name]=unique_object([(k.arg,ast.literal_eval(k.value)) for k in n.value.keywords])
        else:
            try:constants[name]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return constants


def inventory(kind):
 family=SPECS[kind].get('family',kind)
 roles=[dict(role='INPUT')];names=[]
 for iq in range(4):
  if family=='configuration':
   roles += [dict(role=n,column=iq) for n in ('NEW139_MECHANICAL_GAUGE_INPUT','NEW139_CONFIGURATION_CACHE')]
   for k,lo in enumerate(range(0,3784,128)):
    hi=min(lo+128,3784)
    for unit in range(3):
     roles.append(dict(role='UNIT',column=iq,lo=lo,hi=hi,unit=unit));names += ['column%d_chunk%d_unit%d_%s_source_unsigned_enclosure'%(iq,lo,unit,n) for n in ('mechanical','phase','normal','CMC')]
    roles.append(dict(role='COEFFICIENT_CHUNK',column=iq,lo=lo,hi=hi,chunk_ordinal=30*iq+k))
   roles.append(dict(role='COLUMN_INDEX',column=iq))
  elif family=='gauge':
   roles.append(dict(role='MECHANICAL_GAUGE_INPUT',column=iq))
   roles += [dict(role='MECHANICAL_GAUGE_TEST',column=iq,row=r,jet=j) for r in range(4) for j in range(4)]
   roles.append(dict(role='MECHANICAL_GAUGE_COLUMN',column=iq))
   names += ['NEW139_mechanical_gauge_column%d_row0_jet0_Fraction_'%iq+n for n in ('g','hi','U','z','dg','du','dz','Ga','dens','K','metric_EH_density')]
  else:
   roles.append(dict(role='TRANSACTION_COPY',column=iq))
   for k,lo in enumerate(range(0,3784,128)):
    hi=min(lo+128,3784);common=dict(column=iq,selection=[lo,hi],chunk_ordinal=30*iq+k)
    roles += [dict(role='REFRESH_PORT',row=r,jet=j,**common) for r in range(4) for j in range(4)]
    roles.append(dict(role='REFRESH_CHUNK',**common))
   roles.append(dict(role='COLUMN_INDEX',column=iq))
 roles.append(dict(role='PREPARATION'));assert len(roles)==SPECS[kind]['roles'] and len(names)==SPECS[kind]['controls'];return roles,names

def document(path,count,state):
 # Decode bounded top-level values and one checkpoint at a time; no giant parse.
 decoder=json.JSONDecoder(object_pairs_hook=unique_object)
 with path.open('r',encoding='utf-8') as f:
  buffer=''
  def fill():
   nonlocal buffer
   part=f.read(65536);assert part,'unexpected_JSON_EOF';buffer+=part;assert len(buffer)<=MAX_RECORD_TEXT,'JSON_value_bound'
  def char(want=None):
   nonlocal buffer
   buffer=buffer.lstrip()
   while not buffer:fill();buffer=buffer.lstrip()
   value=buffer[0];buffer=buffer[1:];assert want is None or value==want,(want,value);return value
  def value():
   nonlocal buffer
   buffer=buffer.lstrip()
   while True:
    try:q,end=decoder.raw_decode(buffer)
    except json.JSONDecodeError:fill();buffer=buffer.lstrip();continue
    if end==len(buffer) or buffer[end] not in ' \t\r\n,]}:':fill();continue
    buffer=buffer[end:];return q
  char('{');seen=set();ordinal=0
  while True:
   key=value();assert isinstance(key,str) and key not in seen;seen.add(key);char(':')
   if key=='checkpoints':
    char('[')
    for ordinal in range(count):
     q=value();assert isinstance(q,dict);yield ordinal,q
     if ordinal+1<count:char(',')
    char(']');state['checkpoint_count']=count
   else:state[key]=value()
   delimiter=char();assert delimiter in ',}'
   if delimiter=='}':break
  tail=buffer+f.read(MAX_RECORD_TEXT+1);assert 'checkpoints' in seen and len(tail)<=MAX_RECORD_TEXT and not tail.strip() and f.read(1)=='','extra_JSON_tail'

def required_schema(role,md):
 out={}
 def pair(name,shape):
  for w in ('hi','lo'):out[name+'_'+w]=dict(shape=shape,dtype='float64',finite=True)
 if role=='COEFFICIENT_CHUNK':
  p=md['hi']-md['lo']
  for n,shape in dict(mechanical=[p,105,3],phase=[p,3],normal=[p,4,4,3],CMC=[p,3]).items():
   pair('completed_COEFFICIENT_CHUNK_coefficients_'+n,shape);out['completed_COEFFICIENT_CHUNK_envelopes_'+n]=dict(shape=shape,dtype='float64',finite=True)
 if role=='MECHANICAL_GAUGE_COLUMN':
  for n,width in (('native',99),('metric',6)):pair('completed_MECHANICAL_GAUGE_COLUMN_coefficients_'+n,[3784,width,4,4])
 if role=='REFRESH_CHUNK':
  lo,hi=md['selection'];p=hi-lo
  shapes=dict(normal_native=[p,4,4,99],normal_metric=[p,4,4,6],CMC_metric=[p,6],time_primary_rate_native=[p,4,99],time_primary_rate_metric=[p,4,6],current_normal_value=[p,4,4],current_time_primary_action=[p,4],current_initial_CMC_density=[p])
  for n,shape in shapes.items():pair('completed_refresh_'+n,shape)
  for n,shape in dict(e_native=[p,4,4,99],e_metric=[p,4,4,6],e_CMC_metric=[p,6],e_time_primary_rate_native=[p,4,99],e_time_primary_rate_metric=[p,4,6]).items():out['completed_refresh_'+n]=dict(shape=shape,dtype='float64',finite=True)
 assert all(md['schema'].get(n)==s for n,s in out.items()),'coupled_selector_schema_mismatch'
 return sorted(out)

def verify_record(q,i,item,owner,rc,stem,failed):
 role=item['role'];assert q['file']==stem+'_%05d_%s.npz'%(i,role) and q['commit_file']==q['file']+'.COMMIT.json'
 for f,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][f]==h
 ap=verified(q['file'],q['sha256']);cp=verified(q['commit_file'],q['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
 assert small_json(cp)=={k:q[k] for k in ('file','sha256','metadata')}
 md=q['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is failed
 if not failed:
  if 'physical_adoption' in md:assert md['physical_adoption'] is False
  for n,v in item.items():
   if n!='role':assert md[n]==v,(i,n)
  selected=required_schema(role,md)
 else:selected=[];assert role=='ERROR_RAW'
 versions={}
 with zipfile.ZipFile(ap) as z:
  names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
  for n,s in md['schema'].items():
   assert set(s)=={'shape','dtype','finite'} and isinstance(s['finite'],bool) and (failed or s['finite'])
   info=z.getinfo(n+'.npy')
   with z.open(info) as f:(shape,order,dtype),v,pos=header(f)
   assert list(shape)==s['shape'] and str(dtype)==s['dtype'] and dtype.kind in 'fiub' and not dtype.hasobject and pos+math.prod(shape)*dtype.itemsize==info.file_size,n
   versions[str(v)]=versions.get(str(v),0)+1
  with z.open('metadata_json.npy') as f:
   (shape,order,dtype),v,pos=header(f);assert shape==() and dtype.kind=='U' and dtype.itemsize<=4*MAX_RECORD_TEXT
   data=f.read();assert len(data)==dtype.itemsize and pos+len(data)==z.getinfo('metadata_json.npy').file_size
   big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
   assert json.loads(data.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'),object_pairs_hook=unique_object)==md
 canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
 return dict(ordinal=i,role=role,**thin(q),failed=failed,owner_equal=True,embedded_metadata_equal=True,member_headers=len(md['schema']),schema_sha256=hashlib.sha256(canonical(md['schema'])).hexdigest(),metadata_sha256=hashlib.sha256(canonical(md)).hexdigest(),public_header_versions=versions,coupled_selector_names=selected,byte_header_custody_verified=True)

def check_links(q,item,state):
 role=item['role'];md=q['metadata'];tr=thin(q)
 if role=='INPUT':state['input']=tr
 if role in ('NEW139_MECHANICAL_GAUGE_INPUT','MECHANICAL_GAUGE_INPUT'):state.setdefault('prepared_inputs',[]).append(tr)
 if role in ('UNIT','MECHANICAL_GAUGE_TEST','REFRESH_PORT'):state.setdefault(role,[]).append(tr)
 if role=='UNIT':assert md['controls'] and [c['name'] for c in md['controls']]==['column%d_chunk%d_unit%d_%s_source_unsigned_enclosure'%(item['column'],item['lo'],item['unit'],n) for n in ('mechanical','phase','normal','CMC')]
 if role=='COEFFICIENT_CHUNK':assert md['units']==state['UNIT'][-3:];state.setdefault('chunks',[]).append(tr)
 if role=='MECHANICAL_GAUGE_COLUMN':assert md['tests']==state['MECHANICAL_GAUGE_TEST'][-16:];state.setdefault('columns',[]).append(tr)
 if role=='REFRESH_CHUNK':assert md['port_refs']==state['REFRESH_PORT'][-16:] and md['original87_association_earned'] is False;state.setdefault('chunks',[]).append(tr)
 if role=='COLUMN_INDEX':assert md['chunks']==state['chunks'][-30:];state.setdefault('columns',[]).append(tr)
 if role=='PREPARATION':state['preparation']=tr;assert md['input']==state['input'] and md['columns']==state['columns']

def main():
 global np
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and KIND in SPECS and OUTCOME in ('SUCCESS','FAILURE'),'Root FULL-reviewed closed-only release required'
 spec=SPECS[KIND];family=spec.get('family',KIND);stem=spec['stem'];assert spec.get('outcome_required',OUTCOME)==OUTCOME
 assert SOURCE==spec['source'] and all(v is not None for v in SOURCE+RECEIPT)
 target=RESULT if OUTCOME=='SUCCESS' else ERROR;assert all(v is not None for v in target)
 assert target[0]==stem+('_RESULT.json' if OUTCOME=='SUCCESS' else '_ERROR.json') and RECEIPT[0] in (stem+'_RECEIPT.json',stem+'_ERROR_RECEIPT.json')
 assert RECEIPT[2]==('CLOSED' if OUTCOME=='SUCCESS' else 'CLOSED_ERROR')
 assert isinstance(NATURAL_CLOSURE,dict)
 persistence=NATURAL_CLOSURE.get('persistence_complete') is True
 if persistence:
  assert KIND=='gauge' and OUTCOME=='SUCCESS' and SOURCE==('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222') and spec['pid']==89675 and spec['session']==42171
  assert NATURAL_CLOSURE['pid']==89675 and NATURAL_CLOSURE['session_id']==42171 and NATURAL_CLOSURE['exit_code'] is None and NATURAL_CLOSURE['naturally_closed'] is False
  assert NATURAL_CLOSURE['producer_exit_observed'] is NATURAL_CLOSURE['post_receipt_recheck_observed'] is False and NATURAL_CLOSURE['process_absent'] is NATURAL_CLOSURE['session_retired'] is True
  assert isinstance(NATURAL_CLOSURE['observed_utc'],str) and NATURAL_CLOSURE['observed_utc'] and all(isinstance(NATURAL_CLOSURE[n],str) and NATURAL_CLOSURE[n] for n in ('process_absent_evidence','session_retired_evidence'))
 else:
  assert isinstance(NATURAL_CLOSURE,dict) and (spec['pid'] is None or NATURAL_CLOSURE['pid']==spec['pid']) and NATURAL_CLOSURE['session_id']==spec['session'] and NATURAL_CLOSURE['exit_code']==(0 if OUTCOME=='SUCCESS' else 1)
  assert NATURAL_CLOSURE['naturally_closed'] is NATURAL_CLOSURE['process_absent'] is True and isinstance(NATURAL_CLOSURE['observed_utc'],str)
 assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
 verified(PROTOCOL,PROTOCOL_SHA);src=verified(*SOURCE);tp=verified(*target[:2]);rc=small_json(verified(*RECEIPT[:2]));const=source_constants(src)
 assert const['AUTHOR_DRAFT'] is const['AUTHORING_IN_PROGRESS'] is False and const['STEM']==stem and const['FLAGS']==FLAGS
 verified(const['DRIVER_PROTOCOL'],const['PROTOCOL_SHA']);owner=rc['owner'];assert owner['pid']==NATURAL_CLOSURE['pid'] and owner['owner']=='root' and owner['source_sha256']==SOURCE[1] and rc['qualification']==FLAGS and rc['status']==RECEIPT[2]
 assert rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None if OUTCOME=='SUCCESS' else rc['error_sha256']==ERROR[1]
 for registry in ('input_sha256','output_sha256'):
  for f,h in rc[registry].items():verified(f,h)
 for f,h in ((SOURCE[0],SOURCE[1]),(const['IO_PARENT'],const['IO_PARENT_SHA']),(const['DRIVER_PROTOCOL'],const['PROTOCOL_SHA'])):assert rc['input_sha256'][str((BASE/f).resolve())]==h
 assert small_json(BASE/(stem+'_OWNER_START.json'))==owner
 roles,names=inventory(KIND);assert len(roles)==spec['roles'] and len(names)==spec['controls'];pattern=re.compile(re.escape(stem)+r'_(\d{5})_([A-Z0-9_]+)\.npz')
 rows=sorted((int(m[1]),m[2]) for f in rc['output_sha256'] if (m:=pattern.fullmatch(f)));assert [i for i,r in rows]==list(range(len(rows)))
 raw=bool(rows and rows[-1][1]=='ERROR_RAW');science=len(rows)-int(raw);assert science<=len(roles) and [r for i,r in rows[:science]]==[q['role'] for q in roles[:science]] and (OUTCOME=='FAILURE' or not raw and science==len(roles))
 import numpy as numpy
 np=numpy
 top={};state={};records=[]
 for i,q in document(tp,len(rows),top):
  failed=i==science;item=dict(role='ERROR_RAW') if failed else roles[i];records.append(verify_record(q,i,item,owner,rc,stem,failed))
  if not failed:check_links(q,item,state)
 assert top['owner']==owner and top['qualification']==FLAGS and top['status']==(spec['status'] if OUTCOME=='SUCCESS' else 'FAILED')
 controls=top['controls'];assert len(controls)<=len(names) and [c['name'] for c in controls]==names[:len(controls)]
 assert all(c['ordinal']==i and c['tolerance']==2e-11 and isinstance(c['passed'],bool) and math.isfinite(c['error']) and c['error']>=0 for i,c in enumerate(controls))
 assert all(c['passed']==(c['error']<=c['tolerance']) for c in controls),'saved_control_descriptor_inconsistent'
 assert all(c['passed'] is True for c in controls[:-1])
 if OUTCOME=='SUCCESS':
  assert RESULT[2]==spec['status'] and len(controls)==spec['controls'] and all(c['passed'] is True for c in controls) and not (BASE/(stem+'_ERROR.json')).exists() and not (BASE/(stem+'_ERROR_RECEIPT.json')).exists()
  case=top['case'];assert case['status']==spec['status'] and case['roles']==science and case['physical_adoption'] is False and case['input']==state['input'] and case['columns']==state['columns'] and case['preparation']==state['preparation']
  if family=='configuration':assert case['chunks']==state['chunks'] and case['controls']==1440 and case['uniform290_DD_or_global_inverse_qualified'] is case['original_targets_or_rates_refitted'] is case['old_q3_or_whole_direction_replayed'] is False
  if family=='gauge':assert case['prepared_inputs']==state['prepared_inputs'] and case['ports']==state['MECHANICAL_GAUGE_TEST'] and case['new_ports']==64 and case['new_controls']==44 and case['fullweak_gauge_contacts_earned'] is case['Cstar_equals_minus_Rv_assumed'] is case['normal_feedback_or_geometry_correction_admitted'] is False
  if family=='rate':assert case['chunks']==state['chunks'] and case['reverse_ports']==1920 and case['new_controls']==0 and case['represented_coefficient_only'] is True and case['original87_association_earned'] is case['normal_feedback_or_configuration_step_admitted'] is False
 else:
  assert isinstance(top['traceback'],str) and top['traceback'] and top['input_sha256']==rc['input_sha256'];assert top['raw_preservation_traceback'] is None or isinstance(top['raw_preservation_traceback'],str);assert top['closing_traceback'] is None or isinstance(top['closing_traceback'],str)
  if KIND=='rate_failure_v004':assert science==2 and raw and controls==[] and len(rc['input_sha256'])==162 and len(rc['output_sha256'])==9 and 'author_fragment_NEW139_literal_rate_normal_refresh_v001.py' in top['traceback'] and 'tuple(closed[group][n])==pin' in top['traceback'] and top['raw_preservation_traceback'] is top['closing_traceback'] is None
 expected={q[k] for q in records for k in ('file','commit_file')}|{stem+'_OWNER_START.json',target[0]}
 for suffix in ('_MANIFEST.json','_RESULT.json','_RECEIPT.json'):
  if stem+suffix in rc['output_sha256']:expected.add(stem+suffix)
 assert set(rc['output_sha256'])==expected
 if persistence:assert len(rc['input_sha256'])==109 and len(rc['output_sha256'])==151 and science==74 and not raw and len(controls)==44 and not list(BASE.glob(stem+'_*ERROR*'))
 for f,before in STATS.items():
  z=Path(f).stat();assert before==dict(inode=z.st_ino,size=z.st_size,mtime_ns=z.st_mtime_ns,mode=oct(z.st_mode&0o777)),f
 proof=dict(status='READONLY_NATURAL_CLOSED_NEW139_COMPONENT_'+OUTCOME+'_SEALS_VERIFIED',kind=KIND,outcome=OUTCOME,owner=owner,source_file=SOURCE[0],source_sha256=SOURCE[1],receipt_file=RECEIPT[0],receipt_sha256=RECEIPT[1],result_sha256=RESULT[1] if OUTCOME=='SUCCESS' else rc.get('result_sha256'),error_sha256=ERROR[1] if OUTCOME=='FAILURE' else None,naturally_closed=True,exit_code=NATURAL_CLOSURE['exit_code'],observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,all_partial_output_seals_verified=raw,input_count=len(rc['input_sha256']),output_count=len(rc['output_sha256']),planned_roles=spec['roles'],success_roles=science,failed_roles=int(raw),planned_controls=spec['controls'],controls=controls,actual_control_count=len(controls),planned_role_and_control_census_complete=OUTCOME=='SUCCESS',records=records,case=top.get('case'),traceback=top.get('traceback'),raw_preservation_traceback=top.get('raw_preservation_traceback'),closing_traceback=top.get('closing_traceback'),Rv_list_tuple_admission_refusal_before_first_reverse_port=KIND=='rate_failure_v004' and OUTCOME=='FAILURE',qualification=FLAGS,numeric_arrays_decoded=False,numerical_helpers_or_controls_evaluated=False,producer_finite_and_numerical_control_assertions_inherited=True,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,verified_at=datetime.now(timezone.utc).isoformat(),physical_adoption=False,scope='Exact registered byte/header/metadata custody only. Failure preserves earned prefix and refusal; it is never completed preparation admission. Source unsigned and wholeweak association, feedback, finite geometry and physical qualifications remain external.')
 if persistence:proof.update(status='READONLY_PERSISTENCE_COMPLETE_NEW139_COMPONENT_SUCCESS_SEALS_VERIFIED',naturally_closed=False,exit_code=None,producer_exit_observed=False,post_receipt_recheck_observed=False,persistence_complete=True,process_absent=True,session_retired=True)
 data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();dest=BASE/PROOF_FILE
 with dest.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 dest.chmod(0o444);print(json.dumps(dict(file=dest.name,sha256=hashlib.sha256(data).hexdigest(),outcome=OUTCOME,success_roles=science,controls=len(controls))))

if __name__=='__main__':main()
