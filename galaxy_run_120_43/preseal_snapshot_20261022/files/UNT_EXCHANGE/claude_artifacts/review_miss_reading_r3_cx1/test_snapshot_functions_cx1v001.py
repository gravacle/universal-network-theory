"""Snapshot-only independent M12 preparation. Never import complete source modules or read score files."""
import ast,contextlib,copy,hashlib,json,os,statistics,sys,types
from pathlib import Path
assert os.getpriority(os.PRIO_PROCESS,0)>=10 and sys.flags.isolated and sys.dont_write_bytecode
R=Path(__file__).parent;S=R/'SNAPSHOT_CX1V001';O=R/'FUNCTION_SLICE_CX1V001';O.mkdir();manifest=json.loads((S/'SNAPSHOT_MANIFEST_CX1V001.json').read_bytes());raw={}
for name,p in manifest.items():
 raw[name]=Path(p['snapshot_path']).read_bytes();assert hashlib.sha256(raw[name]).hexdigest()==p['sha256']
checks=[];outputs={};active=False;denials=[]
def ck(n,ok,detail=None):checks.append({'name':n,'pass':bool(ok),'detail':detail})
def audit(event,args):
 if active and (event in ('open','import') or event.startswith(('os.','shutil.','ctypes.','socket.','subprocess.'))):denials.append(event);raise PermissionError('INERT_NO_IO_FENCE')
sys.addaudithook(audit)
@contextlib.contextmanager
def fence():
 global active
 keys=('stat','lstat','readlink','listdir','scandir','chdir');old={k:getattr(os,k) for k in keys}
 def deny(*a,**kw):denials.append('metadata');raise PermissionError('INERT_NO_IO_FENCE')
 for k in keys:setattr(os,k,deny)
 active=True
 try:yield
 finally:
  active=False
  for k,v in old.items():setattr(os,k,v)
def extract(name,functions,constants,env=None):
 tree=ast.parse(raw[name]);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in functions or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets)]
 assert {n.name for n in nodes if isinstance(n,ast.FunctionDef)}==set(functions)
 ns={} if env is None else dict(env)
 with fence():exec(compile(ast.Module(nodes,[]),manifest[name]['snapshot_path'],'exec'),ns)
 return ns
A=extract('author_rules.py',{'median','zone_summary','outer_trend','classify'},{'ZONES'})
Q=extract('independent_oracle.py',{'z','patterns','verdict'},set())
ids=['SYNTH_ROW_%02d'%i for i in range(43)];queries=[{'query_id':q,'Rad_text':'1' if i<24 else '20' if i<35 else '40'} for i,q in enumerate(ids)];pin_calls=[]
def mockpin(p):pin_calls.append(str(p));return {'path':str(p),'sha256':'0'*64,'scope':'NO_FILESYSTEM_MOCK'}
B=extract('old_B_rehearsal.py',{'classify'},{'ZONES','GRID_NOTE','READINGS','DT'},{'statistics':statistics,'copy':copy,'IDS':ids,'Q':queries,'pin':mockpin,'PR':Path('/INERT_NO_DATA/text.md'),'FD':Path('/INERT_NO_DATA'),'F':types.SimpleNamespace(__file__='/INERT_NO_DATA/module.py'),'Path':Path,'trace':{'root_pins':{} }})
H=('HIT',0.0,False);N=('NULLR',None,False);G=('GATE',None,False);I=('BUILTIN',None,False);D=('MISS',-2.0,False);E=('MISS',2.0,False)
def case(outer,inner=None,trans=None):return {'INNER':list(inner if inner is not None else [H]),'TRANSITION':list(trans if trans is not None else [H]),'OUTER':list(outer)}
cases={'outer_unsigned':case([N,N]),'inner_unsigned':case([H],inner=[N,N]),'transition_unsigned':case([H],trans=[N,N]),'all_hit':case([H]),'all_builtin_outer':case([I,I]),'all_gate_outer':case([G,G]),'late_signed_to_unsigned':case([D,G,G]),'outer_centered_miss':case([D,E]),'outer_crossing':case([E,D],trans=[('HIT',0.5,False)]),'outer_growing':case([D,('MISS',-3.0,False)]),'half_count_tie':case([H,E]),'signed_minority':case([H,E,N]),'null_TSR':case([H],trans=[('NULLR',None,True)]),'gate_TSR_excluded':case([H],trans=[('GATE',None,True)])}
def oracle(data,late):
 zs={};meds={}
 for name,rows in data.items():
  valid=[x for x in rows if x[0]!='BUILTIN' and (x[0]!='GATE' or late)]
  vals=[x[1] for x in valid if x[0] in ('HIT','MISS')];med=statistics.median(vals) if vals else None;meds[name]=med
  mc='UNDEFINED' if med is None else 'DEFICIT' if med<-1 else 'EXCESS' if med>1 else 'CENTERED'
  zs[name]=Q['z'](sum(x[0]=='HIT' for x in valid),sum(x[0]=='MISS' for x in valid),sum(x[0] in ('NULLR','GATE') for x in valid),len(rows)-len(valid),mc)
 values=[x[1] for x in data['OUTER'] if x[0] in ('HIT','MISS')];mid=len(values)//2;far=statistics.median(values[mid:]) if len(values)>1 else None;delta=far-statistics.median(values[:mid]) if len(values)>1 else None
 o=zs['OUTER'];trend=delta is not None and delta<0 and meds['TRANSITION'] is not None and meds['OUTER'] is not None and meds['TRANSITION']>meds['OUTER']
 p=Q['patterns'](zs['INNER'],zs['TRANSITION'],o,any(x[2] and x[0] in ('MISS','NULLR') for rows in data.values() for x in rows),trend,trend and far is not None and far<-1)
 return zs,meds,p,Q['verdict'](o).replace('TESTED_NEGATIVE','TESTED-NEGATIVE'),delta
with fence():
 for name,data in cases.items():
  for late in (False,True):
   got=A['classify'](copy.deepcopy(data),late);zs,meds,p,e3,delta=oracle(data,late);tag=name+('_late' if late else '_ontime')
   ck(tag+'_patterns',got['pats']==p,{'actual':sorted(got['pats']),'oracle':sorted(p)})
   ck(tag+'_e3_and_failure',got['e3']==e3 and got['of']==zs['OUTER']['miss_dominated'])
   ck(tag+'_trend',got['dout']==delta)
   for zone in A['ZONES']:
    mapping={'Nv':'nv','H':'h','M':'m','U':'u','I':'i','S':'s','miss_dominated':'miss_dom','hit_dominated':'hit_dom'}
    ck(tag+'_'+zone+'_summary',all(zs[zone][x]==got['S'][zone][y] for x,y in mapping.items()) and meds[zone]==got['S'][zone]['med'])
   outputs[tag]={'patterns':sorted(got['pats']),'outer_failure':got['of'],'e3':got['e3'],'deficit_reading':got['deficit_reading'],'zone_counts':{z:{k:v for k,v in got['S'][z].items() if k!='defined'} for z in A['ZONES']}}
 ck('original_unsigned_OUTER_P14','P14' in A['classify'](cases['outer_unsigned'],True)['pats'])
 ck('original_unsigned_INNER_P15','P15' in A['classify'](cases['inner_unsigned'],True)['pats'])
 ck('signed_to_unsigned_replacement','P1' in A['classify'](cases['late_signed_to_unsigned'],False)['pats'] and 'P14' in A['classify'](cases['late_signed_to_unsigned'],True)['pats'])
 ck('C2_all_HIT_CENTERED_not_C9_summary',A['classify'](cases['all_hit'],False)['S']['OUTER']['s']=='CENTERED')
 ck('half_count_tie_is_not_hit_dominated',A['classify'](cases['half_count_tie'],False)['S']['OUTER']['hit_dom'] is False)
# Exercise only the old B function definition; all globals/score records are invented.
def score():
 rows=[{'id':q,'status':'VALID','score_status':'HIT','within_error':True,'sigma_ratio':0.0,'registered_reason':None} for q in ids]
 return {'headline':{'reference_member_id':'SYNTHETIC_REFERENCE'},'members':[{'member_id':'SYNTHETIC_REFERENCE','log_index':0,'member_valid':True,'rows':rows}],'pointwise_envelope':{'rows':[{'id':q,'band_overlaps_error_bar':False} for q in ids]},'alternatives':[],'manifest_file_sha256_actual':'0'*64,'manifest_file_sha256_expected':'0'*64,'registration_file_sha256':'0'*64,'freeze_status':'OWNED_SYNTHETIC_ONLY'}
old_gaps={}
with fence():
 s=score();g=B['classify'](s);ck('old_B_positive_all_HIT_control',g['patterns']['P8'] and g['zones']['OUTER']['sign_class']=='CENTERED')
 s=score()
 for row in s['members'][0]['rows'][35:]:row.update(within_error=False,score_status='MISS',sigma_ratio=None)
 try:B['classify'](s);gap=False
 except ValueError as exc:gap=str(exc)=='CLASSIFICATION_INPUT_DEFECT'
 ck('old_B_null_ratio_gap_reproduced',gap);old_gaps['null_ratio']='CLASSIFICATION_INPUT_DEFECT instead of unsigned MISS/P14'
 s=score();s['gate_status_list']={'OWN_GATE':'LATE'}
 for row in s['members'][0]['rows'][35:]:row.update(status='INVALID',score_status='INVALID_AS_MISS',within_error=False,sigma_ratio=None,registered_reason='OWN_GATE')
 g=B['classify'](s);ck('old_B_LATE_gap_reproduced',g['patterns']['P9'] and 'P14' not in g['patterns']);old_gaps['LATE']='P9 instead of r3 P14; no gate timing support'
 s=score()
 for row,e in zip(s['members'][0]['rows'][35:],s['pointwise_envelope']['rows'][35:]):row.update(within_error=False,score_status='MISS',sigma_ratio=2.0);e['band_overlaps_error_bar']=True
 g=B['classify'](s);ck('old_B_NEAR_gap_reproduced',g['patterns']['P8'] and g['zones']['OUTER']['counts']['NEAR']==8 and g['zones']['OUTER']['counts']['MISS']==0);old_gaps['NEAR']='NEAR is a separate tier, removes eight MISS counts and permits P8'
 s=score()
 for row in s['members'][0]['rows'][39:]:row.update(within_error=False,score_status='MISS',sigma_ratio=2.0)
 g=B['classify'](s);ck('old_B_half_tie_gap_reproduced',g['zones']['OUTER']['hit_dominated'] and g['zones']['OUTER']['miss_dominated']);old_gaps['tie']='H=4/M=4 makes both hit- and miss-dominated under old >= rule'
 ck('old_B_P14_P15_absent','P14' not in g['patterns'] and 'P15' not in g['patterns'])
ck('function_calls_no_IO_or_process_attempts',denials==[])
# Inert boundary tests do not call any OS mutation or protected path.
with fence():
 for event in ('open','os.chmod','subprocess.Popen','socket.connect'):
  try:sys.audit(event,'INERT_NO_OPERATION');ok=False
  except PermissionError:ok=True
  ck('fence_'+event,ok)
 try:os.stat('/INERT_NEVER_READ');ok=False
 except PermissionError:ok=True
 ck('fence_metadata_before_OS',ok)
ck('fence_restored',active is False and os.getpriority(os.PRIO_PROCESS,0)>=10)
ck('author_reports_M12_not_built',b'the M-12 classifier is not built' in raw['author_partial.md'])
result={'schema':'UNT_R3_SNAPSHOT_FUNCTION_REVIEW_CX1V001','date_u':sys.argv[1],'status':'TESTED_SNAPSHOT_FUNCTION_SLICES_ONLY','final_verdict':'PENDING_PUBLISHED_TUPLE_AND_M12_IMPLEMENTATIONS','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'invented_cases':cases,'case_outputs':outputs,'old_B_required_updates':old_gaps,'old_B_scope':'Known r2 rehearsal, not a submitted r3 implementation. Its expected gaps do not invalidate author r3 text-helper results.','actual_M12_agreement':'NOT_RUN_IMPLEMENTATIONS_AND_PINNED_AGREEMENT_ABSENT_IN_REVIEWED_SCOPE','concrete_dependency':'Author text_c4/PARTIAL.md says M-12 classifier not built. Named B is old r2 rehearsal source. Need exact r3 A/B source and agreement tuple before production claim.','snapshot_sources':manifest,'harness_pin':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'function_slices':{'author_rules.py':['median','zone_summary','outer_trend','classify'],'independent_oracle.py':['z','patterns','verdict'],'old_B_rehearsal.py':['classify']},'IO_scope':'All function compile/calls in no-open/no-import/no-process/no-network/no-metadata fence; old B pin() replaced by explicit mock returning inert metadata only. No complete source import or main call.','limitations':['Current author helper is a text-rule self-test, not full M12 A; reviewer oracle is an independent predicate oracle, not adopted M12 B.','Only invented row statuses, dimensionless ratios, identifiers, radius-zone scaffolding and metadata were used. No actual score, prediction, observed/target velocity or protected run was read.','Focused new actual-function tests complement prior bounded logical enumeration; not a proof or a production classifier agreement suite.','Reading tuples, real freeze custody, TSR carriers, STAGE0 carriers, targets and scientific outcomes remain UNTESTED.','Prior two provisional SHOULD_FIX wording/version-contract items remain pending actual publication.']}
p=O/'RESULTS_CX1V001.json'
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'passed':result['passed'],'total':result['total'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'result_path':str(p),'unexpected_failures':[x for x in checks if not x['pass']],'actual_M12_agreement':result['actual_M12_agreement']}))
raise SystemExit(0 if result['passed']==result['total'] else 1)
