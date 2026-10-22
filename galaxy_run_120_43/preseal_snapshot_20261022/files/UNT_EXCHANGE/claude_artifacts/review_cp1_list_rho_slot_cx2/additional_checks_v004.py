"""Independent 0824 checks on invented records; no proof/solver execution."""
import collections
import shlex

def review_case(name, fn, expected=None):
 try:
  fn()
  assert expected is None, 'unexpected acceptance: '+name
  rows.append({'case':name,'PASS':True,'scope':'independent review'})
 except m.Refusal as exc:
  assert expected and expected in str(exc),(name,str(exc),expected)
  rows.append({'case':name,'PASS':True,'reason':str(exc),'scope':'independent review'})

def variant(tag,change=None,extra_rho=False):
 p=points[0];k=p['key'][:16]
 old=R/('P300_'+k+'_INERT_0_a1')
 new=F/('cp1_run_'+tag);new.mkdir()
 folder='cp1_run_'+tag+'/P300_'+k+'_INERT_0_a1'
 rr=json.loads((old/('RHO_NUMERIC_'+k+'_a.json')).read_bytes())
 er=json.loads((old/('EPS_NUMERIC_'+k+'.json')).read_bytes())
 ed=json.loads((old/('EPS_PROOF_'+k+'.json')).read_bytes())
 gd=json.loads((old/('GQ_PROOF_'+k+'.json')).read_bytes())
 if change:change(rr,er,ed,gd)
 rp=put(folder+'/RHO_NUMERIC_'+k+'_a.json',rr)
 en=put(folder+'/EPS_NUMERIC_'+k+'.json',er)
 ed['driver_certificate']=en
 put(folder+'/EPS_PROOF_'+k+'.json',ed);put(folder+'/GQ_PROOF_'+k+'.json',gd)
 if extra_rho:put(folder+'/RHO_NUMERIC_'+k+'_b.json',rr)
 listpin=put('list_'+tag+'.json',dict(lst,points=[p]))
 return m.collect(m.Snapshot(),listpin,str(new),[p['key']],anchor,approved)

for tag,change,expected in [
 ('rho_schema',lambda r,e,p,g:r.update(schema='wrong'),'RHO_SCHEMA_OR_GATE'),
 ('rho_status',lambda r,e,p,g:r.update(status='NOT_READY'),'RHO_STATUS_OR_VERDICT'),
 ('rho_smoke',lambda r,e,p,g:r.update(settings='smoke'),'RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH'),
 ('rho_partial',lambda r,e,p,g:r.update(full_registered_search_executed=False),'RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH'),
 ('rho_coverage',lambda r,e,p,g:r.update(coverage_complete=False),'RHO_COVERAGE'),
 ('rho_partition',lambda r,e,p,g:r['shells'].pop(),'RHO_PARTITION'),
 ('rho_producer',lambda r,e,p,g:r['producer'].update(sha256='0'*64),'RHO_PRODUCER_NOT_A1DCDEA8'),
 ('rho_digest',lambda r,e,p,g:r.update(point_sha256='a'*64),'RHO_IDENTITY_POINT_SHA_INCONSISTENT'),
 ('eps_identity',lambda r,e,p,g:e.update(identity={}), 'EPS_IDENTITY'),
 ('eps_partial',lambda r,e,p,g:e.update(full_registered_search_executed=False),'PARTIAL_EPS'),
 ('rho_eps_custody',lambda r,e,p,g:r['custody'].update(grid_sha256='b'*64),'CUSTODY_MISMATCH'),
 ('proof_key',lambda r,e,p,g:p.update(point_sha256='b'*64),'PROOF_IDENTITY_CUSTODY_PRODUCER'),
 ('proof_custody',lambda r,e,p,g:g.update(custody_sha256='c'*64),'PROOF_IDENTITY_CUSTODY_PRODUCER'),
 ('proof_producer',lambda r,e,p,g:p['producer'].update(sha256='f'*64),'PROOF_IDENTITY_CUSTODY_PRODUCER'),
 ('proof_not_pass',lambda r,e,p,g:g.update(verdict='FAIL'),'PROOF_NOT_PASS'),
 ('gq_coverage',lambda r,e,p,g:g.update(all_production_kperp_nodes=False),'PARTIAL_GQ'),
 ('gq_count',lambda r,e,p,g:g.update(nodes_tested=1),'PARTIAL_GQ'),
]:
 review_case(tag,lambda tag=tag,change=change:variant(tag,change),expected)
review_case('extra_rho_attempt_refused',lambda:variant('extra_rho',extra_rho=True),
            'RHO_RECORD_SET_UNEXPECTED')

def bad_anchor(tag,doc):
 apin=put(tag+'.json',doc)
 return m.collect(m.Snapshot(),lp,str(R),keys,apin,approved)
review_case('anchor_same_record',lambda:bad_anchor('same_anchor',
            {'anchor_rho_pair':[pair[0],pair[0]],'registered_rho_records':pair}),
            'ANCHOR_NOT_TWO_RUNS')
review_case('anchor_unregistered',lambda:bad_anchor('unregistered_anchor',
            {'anchor_rho_pair':pair,'registered_rho_records':[pair[0]]}),
            'ANCHOR_UNREGISTERED')

def anchor_disagreement():
 anchor_b=json.loads(Path(pair[1]['path']).read_bytes())
 anchor_b['shells'][0]['synthetic_comparison_delta']=True
 changed=put('anchor_disagreement_record.json',anchor_b)
 return bad_anchor('disagreeing_anchor',{'anchor_rho_pair':[pair[0],changed],
                                       'registered_rho_records':[pair[0],changed]})
review_case('anchor_bitwise_disagreement',anchor_disagreement,'ANCHOR_NOT_BITWISE_EQUAL')

def cache_rechecks_sha():
 snapshot=m.Snapshot()
 raw,sha=snapshot.raw(lp['path'],lp['sha256'])
 try:snapshot.raw(lp['path'],'0'*64)
 except m.Refusal as exc:assert 'SHA_MISMATCH' in str(exc)
 else:raise AssertionError('repeated pin bypassed')
 assert snapshot.counts[lp['path']]==1
review_case('cached_buffer_rechecks_each_pin',cache_rechecks_sha)

def output_contract():
 paths=st['outputs']
 original_spec={p['row']:json.loads(Path(p['spec']['path']).read_bytes()) for p in points}
 registered=json.loads(Path(reg['path']).read_bytes())
 commands=Path(paths['COMMANDS.txt']['path']).read_text().splitlines()
 generated=[shlex.split(line) for line in commands if line and not line.startswith('#')]
 assert len(generated)==54
 for index,p in enumerate(points):
  tag='P%02d_%s'%(p['row'],p['key'][:16])
  fp=paths['FILLED_SPEC_'+tag+'.json']
  args_pin=paths['SLOT_ARGS_'+tag+'.json']
  filled=json.loads(Path(fp['path']).read_bytes());args_doc=json.loads(Path(args_pin['path']).read_bytes())
  back=copy.deepcopy(filled)
  for slotname in ('eps_certificate','lo_certificate'):
   back['numerics']['uv_tail'][slotname]=original_spec[p['row']]['numerics']['uv_tail'][slotname]
  assert m.canonical(back)==m.canonical(original_spec[p['row']])
  assert set(args_doc)==H.ARGS_KEYS
  assert args_doc['spec_ref']==fp and args_doc['rho_ref']==filled['numerics']['uv_tail']['lo_certificate']
  assert args_doc['registered_rho_records']==registered['registered_rho_records']
  assert args_doc['anchor_rho_pair']==registered['anchor_rho_pair']
  assert args_doc['root_ruling_refs']==[dict(x) for x in S['ROOT_RULINGS']]
  assert args_doc['approved_producer_sha256']==[q['sha256'] for q in ap]
  slot,bundle=generated[2*index:2*index+2]
  assert slot[:5]==['/usr/sbin/taskpolicy','-b',m.PYTHON,'-I','-B']
  assert slot[slot.index('--args')+1]==args_pin['path']
  assert slot[slot.index('--args-sha256')+1]==args_pin['sha256']
  assert set(x for x in slot if x.startswith('--'))=={'--args','--args-sha256','--out-root'}
  assert bundle[1:3]==['-I','-B']
  assert set(x for x in bundle if x.startswith('--'))=={
   '--points-list','--points-list-sha256','--out-root','--point','--eps-proof',
   '--gq-proof','--lo-proof','--approved-producers'}
  assert bundle[bundle.index('--point')+1]==p['key']
  assert bundle[bundle.index('--points-list-sha256')+1]==lp['sha256']
  assert bundle[bundle.index('--lo-proof')+1].endswith('/LO_RHO_SLOT_PROOF_'+p['key'][:16]+'.json')
review_case('27_point_FILLED_ARGS_and_command_contract',output_contract)

def output_exclusive():
 result=m.write_set(F/'registered',{'SHOULD_NOT_EXIST':b'no'})
 raise AssertionError(result)
review_case('existing_output_directory_refused',output_exclusive,'NEW_OUTPUT_DIRECTORY_REQUIRED')

stage_reads=collections.Counter()
stage_watch=False
def stage_audit(event,args):
 if stage_watch and event=='open' and isinstance(args[0],str):
  flags=args[2]
  if isinstance(flags,int) and not flags & (os.O_WRONLY|os.O_RDWR):
   stage_reads[os.path.realpath(args[0])]+=1
sys.addaudithook(stage_audit)
stage_watch=True
cli('independent_stage_single_read','stage',stageargs)
stage_watch=False
assert stage_reads and max(stage_reads.values())==1,dict(stage_reads)
rows.append({'case':'actual_stage_single_read_audit','PASS':True,
             'files':len(stage_reads),'max_opens':max(stage_reads.values())})
