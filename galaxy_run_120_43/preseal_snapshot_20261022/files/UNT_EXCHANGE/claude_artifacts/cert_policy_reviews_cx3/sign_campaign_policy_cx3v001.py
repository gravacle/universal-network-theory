"""0838(b)/0840: immutable campaign policy signature; isolated gate AST only."""
SOURCES=[{'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json', 'sha256': 'f848888f7778124414302b8f216813f44dcdf89c594a4a3c066c17da887b6bdc'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json', 'sha256': '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py', 'sha256': '381fa2957edabf18032afba9a8ff026744f6cc1d933efb5f3d30f289ea9decb9'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_core_cx2v006r12_c4.py', 'sha256': '192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', 'sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/README_CAMPAIGN_CERT_C2V001.md', 'sha256': 'bc0ea884aef73c699d78886b097ce3c8afd90cfe3af8ae4ac8463657207b569d'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/README_CAMPAIGN_CERT_C2V004.md', 'sha256': '638d6543d09cf8305235197ea42ed9c3530f13bc531743b012466c8ba68dc9c1'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0838_2026-10-21_codex3_S0_J0_J2_sheet_addendum_then_policy_then_S1_pair.md', 'sha256': '0e6ad28a0dd6c44086413f1973a56d11502b221ce989be3fa8952355ac391f28'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/CAMPAIGN_POLICY_PREPARATION_CX3V001.json', 'sha256': '7ada4ae7b73cd754bd5c824c5e1a1030070ea0666c80d4088aa7bd75cfb6c8db'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0840_2026-10-21_codex3_campaign_work_dir_path_ruled_sign_now.md', 'sha256': '013d435339df4953e1efe4700bc248a2bb0fab9a19cfda9e6c3f2da50b0dbf7a'}]

import ast,copy,hashlib,json,subprocess,sys,datetime
from pathlib import Path,PurePosixPath
from types import SimpleNamespace
D=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3')
FINAL=D/'DDO154_CERTIFICATE_POLICY_REVIEW_CAMPAIGN_CX3V001.json'
EVIDENCE=D/'CAMPAIGN_POLICY_VALIDATION_CX3V001.json'
WORK='/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001'
LEDGER={'schema':'DDO154_CERTIFICATE_LEDGER_C2V003','path':WORK+'/CERTIFICATE_LEDGER.jsonl'}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 stamp=subprocess.check_output(['/bin/date','-u'],text=True).strip()
 violations=[]
 def audit(event,args):
  if event in ('subprocess.Popen','os.system','os.fork','os.posix_spawn','socket.connect','socket.bind'):
   violations.append(event);raise PermissionError('process/network blocked')
  if event=='open' and isinstance(args[0],(str,bytes)) and str(args[0]).startswith('/Volumes/'):
   violations.append('volume open');raise PermissionError('volume open blocked')
 sys.addaudithook(audit)
 raw={}
 for p in SOURCES:
  b=Path(p['path']).read_bytes();assert sha(b)==p['sha256'];raw[Path(p['path']).name]=b
 base=json.loads(raw['DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json'])
 c1=json.loads(raw['C1_H1_C2V001.json']);r=copy.deepcopy(c1['tail_readiness']);r['certificate_ledger']=LEDGER
 assert r['certificate_registry']==base['certificate_registry']
 for k in ('custody_deriver','state_enumerator','approved_certificate_producers'):assert r[k]==base[k]
 allowed={p['path']:raw[Path(p['path']).name] for p in SOURCES}
 pins=[r['certificate_registry'],r['custody_deriver'],r['state_enumerator'],*r['approved_certificate_producers']]
 for p in pins:
  b=Path(p['path']).read_bytes();assert sha(b)==p['sha256'];allowed[p['path']]=b
 opened=[{'path':p,'sha256':sha(b)} for p,b in allowed.items()]
 wt=ast.parse(raw['calibration_orchestrator_cx2v006r12_c4_q5b1.py']);ct=ast.parse(raw['calibration_core_cx2v006r12_c4.py'])
 cls=next(n for n in wt.body if isinstance(n,ast.ClassDef) and n.name=='Context')
 fn=lambda name:next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name==name)
 nodes=[n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name in ('pin_doc','gate_pending','checked_gate')]+[fn(n) for n in ('certificate_policy_gate','ledger_policy_problems','ledger_entries')]
 expr=next(n.args[2] for n in ast.walk(fn('certificate_policy_gate')) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='checked_gate')
 guard=base['source_pins']['guard'];assert sha(allowed[guard['path']])==guard['sha256']
 bindenv={'DRIVER_SHA':base['driver_sha256'],'r':r,'producers':r['approved_certificate_producers'],'O':SimpleNamespace(sha256_file=lambda p:sha(allowed[p])),'G':SimpleNamespace(__file__=guard['path'])}
 bindings=eval(compile(ast.Expression(expr),'<actual eight bindings>','eval'),{'__builtins__':{}},bindenv)
 assert set(bindings)==set(('driver_sha256','custody_deriver','state_enumerator','approved_certificate_producers','guard_sha256','driver_slot_rule','post_state_handoff','certificate_ledger'))
 for k,v in bindings.items():
  if k!='certificate_ledger':assert v==base[k]
 review={'schema':base['schema'],'status':'TESTED','ok':True,**bindings,
  'reviewer_lane':'Codex3','distinct_from_producer_lane':True,'signed_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'date_u':stamp,
  'certificate_registry':r['certificate_registry'],'planned_work_dir':WORK,'blocking_findings':[],
  'scope':'Campaign certificate policy bindings under 0838(b)/0840; inherited frozen C1 scientific policy and its six producers. Separate ledger path signature before mount.',
  'inherited_policy_review':next(p for p in SOURCES if p['path'].endswith('/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json')),
  'frozen_c1':next(p for p in SOURCES if p['path'].endswith('/C1_H1_C2V001.json')),
  'root_path_ruling':SOURCES[-1],
  'check_script':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes())},
  'eight_bindings_digest':sha(canon(bindings)),
  'trusted_source_producers':base['trusted_source_producers'],'trusted_row_policy_review_sha256':base['trusted_row_policy_review_sha256'],
  'driver_slot_rule':base['driver_slot_rule'],'q8_rule':base['q8_rule'],
  'post_state_policy':'Campaign calls use the adopted h3_accept_call_c2v004 path and per-state acceptance; this signature changes no certificate, acceptance classification, rerun rule or scientific threshold.',
  'disclosure':base['disclosure'],
  'validation_scope':'TESTED exact selected wrapper/core AST and all eight policy bindings, pinned genesis/custody/enumerator/six producer bytes. The extracted ledger_entries takes only its missing-ledger branch using an absent-path stand-in. No production Context or volume was accessed.',
  'limitations':['UNTESTED: actual mounted volume UUID, work-dir inode, storage, cache identity and runtime ledger; root checks at W1.','UNTESTED: production campaign Context, final W1 configuration and actual post-state acceptance.','Actual r12 verdict regeneration must retain the reviewed wrapper method bodies; its gating finalization remains separate.','A changed mounted path requires a new immutable signature.'],
  'sources':opened}
 checks=[];mem={}
 class AbsentLedger:
  def __init__(self,p):assert p==LEDGER['path'];self.p=p
  def exists(self):return False
  def read_bytes(self):raise AssertionError('absent ledger must never be read')
 def rp(ref,label):
  assert set(ref)=={'path','sha256'}
  b=mem[ref['path']] if ref['path'] in mem else allowed[ref['path']]
  assert sha(b)==ref['sha256'];return b
 env={'json':json,'Error':ValueError,'POLICY_SCHEMA':base['schema'],'DRIVER_SHA':base['driver_sha256'],
      'LEDGER_SCHEMA':LEDGER['schema'],'LEDGER_NAME':'CERTIFICATE_LEDGER.jsonl','Path':AbsentLedger,
      'O':SimpleNamespace(read_pinned=rp,sha256_file=lambda p:sha(allowed[p])),'G':SimpleNamespace(__file__=guard['path'])}
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<exact selected campaign policy AST>','exec'),env)
 env['M']=SimpleNamespace(checked_gate=env['checked_gate'],gate_pending=env['gate_pending'])
 def run_gate(doc,local=None):
  rr=copy.deepcopy(r if local is None else local);bb=canon(doc);mem[str(FINAL)]=bb
  rr['certificate_policy_review']={'path':str(FINAL),'sha256':sha(bb)}
  ctx=SimpleNamespace(cfg={'tail_readiness':rr},work_dir=PurePosixPath(WORK))
  ctx.ledger_policy_problems=lambda:env['ledger_policy_problems'](ctx)
  ctx.ledger_entries=lambda:env['ledger_entries'](ctx)
  return env['certificate_policy_gate'](ctx)
 assert run_gate(review)['ok'] is True;checks.append({'id':'exact_planned_path_gate','status':'PASS'})
 for k in bindings:
  m=copy.deepcopy(review);m[k]=None
  assert run_gate(m)['ok'] is False;checks.append({'id':'changed_binding_'+k,'status':'PASS'})
 for field,value in [('path',WORK+'_OTHER/CERTIFICATE_LEDGER.jsonl'),('schema','WRONG')]:
  rr=copy.deepcopy(r);rr['certificate_ledger'][field]=value
  assert run_gate(review,rr)['ok'] is False;checks.append({'id':'changed_config_ledger_'+field,'status':'PASS'})
 for k,v in [('ok',False),('status','UNTESTED'),('schema','WRONG')]:
  m=copy.deepcopy(review);m[k]=v;assert run_gate(m)['ok'] is False;checks.append({'id':'changed_review_'+k,'status':'PASS'})
 assert not violations
 review['checks']=checks
 bb=(json.dumps(review,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
 assert run_gate(review)['ok'] is True
 with FINAL.open('xb') as f:f.write(bb)
 # Check the actual saved signed bytes against the same gate; no synthetic success report replaces them.
 saved=json.loads(FINAL.read_bytes());assert run_gate(saved)['ok'] is True
 result={'date_u':stamp,'status':'TESTED','checks':checks,'n_pass':len(checks),'n_total':len(checks),'review':{'path':str(FINAL),'sha256':sha(FINAL.read_bytes())},'process_or_volume_violations':violations,'production':'UNTESTED','absent_ledger_branch_substitution':True,'sources':opened}
 with EVIDENCE.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({'review':result['review'],'validation':{'path':str(EVIDENCE),'sha256':sha(EVIDENCE.read_bytes())},'checks':len(checks)}))
if __name__=='__main__':main()
