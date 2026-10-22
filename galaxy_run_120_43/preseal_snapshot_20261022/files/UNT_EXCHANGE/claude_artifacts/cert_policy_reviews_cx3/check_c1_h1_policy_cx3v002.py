"""Codex3 read-only C1 policy checker, 0860 / D018. No producer, guard or verifier execution."""
SOURCES = {'draft': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json', 'sha256': '387b1b35988e83435fc74826a744868d5ff54fbf9f52e5d5d031ef6c792ad1c1'}, 'registry': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json', 'sha256': '2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319'}, 'custody': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py', 'sha256': '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'}, 'enumerator': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', 'sha256': '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'}, 'eps': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py', 'sha256': '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'}, 'gq': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py', 'sha256': '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'}, 'slot': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py', 'sha256': 'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3'}, 'lo_adapter': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py', 'sha256': '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c'}, 'srb_adapter': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py', 'sha256': '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a'}, 'evidence': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py', 'sha256': '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'}, 'wrapper': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/calibration_orchestrator_q5b1_ledger_a296_cx2v001.py', 'sha256': 'cb1f5e73753b69d1e8b6067c746b8fcda89d94d6bc4f34fb0a78f927e07cca04'}, 'core': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'sha256': 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'}, 'guard': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py', 'sha256': '3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25'}, 'guard011': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_c2v011.py', 'sha256': 'eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033'}, 'final_specs': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py', 'sha256': 'fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba'}, 'lo_core': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/lo_core_r5_cx2v001.py', 'sha256': '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'}, 'response': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py', 'sha256': 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'}, 'facade': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/lo_producer_cx2v004.py', 'sha256': '5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'}, 'rows': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py', 'sha256': '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e'}, 'handoff': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py', 'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}, 'common5': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py', 'sha256': '2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5'}, 'assembler5': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py', 'sha256': '7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310'}, 'common4': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py', 'sha256': '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'}, 'approval_DLO': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0153_2026-10-19_Q4_DLO_row_policy_APPROVED.json', 'sha256': '07eee40b7fe672716c189ff79ec87c2dd94422eb3dadc0fb88d9c88c19db2ef2'}, 'contract_DLO': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/q4_row_contracts_c2/ROW_CONTRACT_DLO_C2V001.json', 'sha256': 'fefbfe66b5de66f9927c15f6ba36335046e90006e9c7ef7dbeaa3f727ac2578e'}, 'approval_D404': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0154_2026-10-19_Q4_D404_row_policy_APPROVED.json', 'sha256': '6c9475e1e65161f5c67bbee4f94c813291167f1e19a59a52528f610ebbc87ca7'}, 'contract_D404': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/q4_row_contracts_c2/ROW_CONTRACT_D404_C2V001.json', 'sha256': 'f9bb13a92b43ca49cf5012b10d4d90b75f52dabbe80484920e60a173aed9ebea'}, 'approval_DHI': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0155_2026-10-19_Q4_DHI_row_policy_APPROVED.json', 'sha256': 'f5b6c66e6fadf5fc20e9a7df767819da6e10eb24e4c75c02911c5486b13ccb23'}, 'contract_DHI': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/q4_row_contracts_c2/ROW_CONTRACT_DHI_C2V001.json', 'sha256': 'a14024eaa9876b43ac52af5d3d1f4f8cb6ee988251fecf0e6e4238465cf45b14'}, 'base_c1': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json', 'sha256': '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}, 'leaf_diff': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/c1_successor/draft_c3v001/LEAF_DIFF_C1_H1_DRAFT_C2V003.json', 'sha256': '5966bb66a79459f58e1a38f40c644f2c5961a3c926cd623b378ea2f9d12eb822'}, 'bridge': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py', 'sha256': '1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'}, 'binding': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py', 'sha256': '141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43'}, 'bound_verifier': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py', 'sha256': '60ed81b58ea205a3dc61f43b58bfee47dee688fd2ab448ea1762f94e8b48a5e0'}, 'request': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/CERT_POLICY_REVIEW_REQUEST_C2V002.md', 'sha256': '2e21dd1b8339e23a239ecc665e5ab06460de15afe99858bc20ce183e29abc840'}, 'draft_builder': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/c1_successor/build_c1_successor_draft_c3v001.py', 'sha256': '2fec6c976e27914fffc7081881b19e23263a369e329b729de2be4246552f0a82'}, 'fill_tool': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/c1_successor/fill_c1_pin_c2v003_c3v001.py', 'sha256': '8a645ca33fbe630b270057da0b36a492a8886f0530148a88863d3f8d013a67b7'}, 'previous_check': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/check_c1_h1_policy_cx3v001.py', 'sha256': '4124986639bc5d234f5d15326e50cd2271854fc37c9baeed14ea2fcd43fc6309'}, 'dispatch': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0860_2026-10-22_codex3_credit_reserve_verdict_gates_and_policy_resign.md', 'sha256': '73c1bda13a67bea2efbd0788695a652bd6f2d1d47a21b749d80d5a9c1055c43f'}, 'deputy': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0327_2026-10-21_deputy-D018-Codex3-re-sign-C1-policy-review-for-C1-successor-against-draft-C2V003-now-campaign-re-sign-prepared-waits-for-root-C1-sha.md', 'sha256': '63f1515deba3546e95dd01e71e7a8045dc9a657ec272246aa5f7d68e475e5eed'}, 'deputy_followup': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0330_2026-10-22_ack-0858-0861-deputy-no-C1-pin-successor-needed-on-A296-bound-path-two-re-signs-C1-tail-first-importer-rule-logged.md', 'sha256': '077663a0194a8ab67cfa68f50fce8ab0be4837f58a19fc7f9da425133475d0a9'}, 'R3_handoff': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0709_2026-10-21_0857_D016_A296_R3_rows302_501_504_APPROVED.md', 'sha256': '9441a2001a4801f51605e3b242f76ba9991f492c60791b9c20bc3f2d19d88aa5'}}

import ast
import hashlib
import json
from pathlib import Path
import stat
from types import SimpleNamespace
SCRIPT='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/check_c1_h1_policy_cx3v002.py'
FINAL='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002.json'
DRIVER='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
DIGEST='3c03bae3473954fdeb842de508c64702602c981675f839d604c7156b8c5db030'
SCHEMA='DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001'
SLOT='POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'
HANDOFF='TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'
ORDER=('eps','gq','slot','lo_adapter','srb_adapter','evidence','bridge')
OPENED={}; RAW={}; ALLOWED={p['path']:p['sha256'] for p in SOURCES.values()}
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate key '+k)
   d[k]=v
  return d
 def bad(x):raise ValueError('nonfinite '+x)
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def require(v):
 if not v:raise AssertionError('condition false')
def read(path,sha=None,grant=False):
 p=Path(path)
 require(p.is_absolute() and str(p)==path and str(p.resolve())==path)
 for q in (p,*p.parents):require(not q.is_symlink())
 st=p.stat();require(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=8388608)
 if grant:
  require(sha and (path not in ALLOWED or ALLOWED[path]==sha));ALLOWED[path]=sha
 require(path in ALLOWED)
 b=p.read_bytes();h=hashlib.sha256(b).hexdigest();require(h==ALLOWED[path] and (sha is None or h==sha))
 OPENED[path]=h;return b
def pin(p,grant=False):
 require(type(p) is dict and set(p)=={'path','sha256'});return read(p['path'],p['sha256'],grant)
def txt(n):return RAW[n].decode()
def has(n,*ss):
 for s in ss:require(s in txt(n))
def constants(n,extra=None):
 env=dict(extra or {})
 def ev(x):
  if isinstance(x,ast.Constant):return x.value
  if isinstance(x,ast.Name):return env[x.id]
  if isinstance(x,(ast.Tuple,ast.List)):return tuple(ev(y) for y in x.elts) if isinstance(x,ast.Tuple) else [ev(y) for y in x.elts]
  if isinstance(x,ast.Dict):return {ev(k):ev(v) for k,v in zip(x.keys,x.values)}
  if isinstance(x,ast.BinOp) and isinstance(x.op,ast.Add):return ev(x.left)+ev(x.right)
  if isinstance(x,ast.BinOp) and isinstance(x.op,ast.Div):return Path(ev(x.left))/ev(x.right)
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('str','Path') and len(x.args)==1 and not x.keywords:
   return str(ev(x.args[0])) if x.func.id=='str' else Path(ev(x.args[0]))
  raise ValueError('nonliteral')
 for x in ast.parse(txt(n)).body:
  if isinstance(x,ast.Assign) and len(x.targets)==1 and isinstance(x.targets[0],ast.Name):
   try:env[x.targets[0].id]=ev(x.value)
   except (KeyError,TypeError,ValueError):pass
 return env
def fn(n,name,cls=None):
 b=ast.parse(txt(n)).body
 if cls:b=next(x for x in b if isinstance(x,ast.ClassDef) and x.name==cls).body
 return next(x for x in b if isinstance(x,ast.FunctionDef) and x.name==name)
def bindings(r):
 call=next(x for x in ast.walk(fn('wrapper','certificate_policy_gate','Context')) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='checked_gate')
 e={'DRIVER_SHA':constants('core')['DRIVER_SHA'],'r':r,'producers':r['approved_certificate_producers'],'O':SimpleNamespace(sha256_file=lambda p:hashlib.sha256(read(str(p))).hexdigest()),'G':SimpleNamespace(__file__=SOURCES['guard']['path'])}
 out=eval(compile(ast.Expression(call.args[2]),'<pinned binding expression>','eval'),{'__builtins__':{}},e)
 require(out.pop('certificate_ledger') is None)
 return out
def checks(script_sha=None):
 OPENED.clear();RAW.clear()
 for n,p in SOURCES.items():RAW[n]=pin(p)
 if script_sha is None:
  script_sha=hashlib.sha256(Path(SCRIPT).read_bytes()).hexdigest();ALLOWED[SCRIPT]=script_sha;read(SCRIPT)
 r=strict(RAW['draft'])['tail_readiness'];expected=[SOURCES[n] for n in ORDER]
 d={'schema':SCHEMA,'status':'TESTED','ok':True,'driver_sha256':DRIVER,'custody_deriver':SOURCES['custody'],'state_enumerator':SOURCES['enumerator'],'approved_certificate_producers':expected,'guard_sha256':SOURCES['guard']['sha256'],'driver_slot_rule':SLOT,'post_state_handoff':HANDOFF,'reviewed_c1_draft':SOURCES['draft'],'c1_tail_readiness_digest_excluding_review':DIGEST,'certificate_registry':SOURCES['registry'],'trusted_source_producers':[SOURCES[n]['sha256'] for n in ('rows','evidence')],'trusted_row_policy_review_sha256':[SOURCES['approval_'+n]['sha256'] for n in ('DLO','D404','DHI')],'reviewer_lane':'Codex3','distinct_from_producer_lane':True,'blocking_findings':[],'check_script':{'path':SCRIPT,'sha256':script_sha},'checks':[],
 'q3_rule':'A134 Q2/Q3, with A158: every tail-ON direct call (HEADLINE11, SENS_LO9, SENS_HI9) is read only after post-run per-state acceptance through acceptance_handoff_c2v004.py (sha256 '+SOURCES['handoff']['sha256']+'). Outputs are evidence only when every consumed state has LO, GQ and the Q10 bound at TESTED/PASS. Otherwise the call reads INCOMPLETE and is preserved. The frozen v004 acceptance classifications remain in force; no waiver is added.',
 'q8_rule':'A134 Q8: one EPS policy review, instantiated per point by script; no cap reviews and no per-point LO reviews. A203: CP-1 EPS is 31/31: rows 1-9 Claude4, rows 10-31 Codex3. A296 R3 EPS reviews for rows 302, 501 and 504 are signed by Codex3 (0709). The three Codex1 row-policy approvals remain separate. Registered numerical conventions and their limitations are retained.',
 'disclosure':'Codex3 signed 22 CP-1 EPS instances, rows 10-31; their proofs were emitted by the EPS adapter. Codex3 authored none of the seven bound producers or c3 tools; A296 R3 reviews for rows 302, 501 and 504 are signed by Codex3, delivered in 0709. A205 also assigns this lane verdict-byte finalization, campaign compatibility review, and prospective wave review: role concentration is disclosed. This review attests policy bindings, not producer scientific validity or a real launch gate.',
 'limitations':['FORMAL: source-level producer minimality and acceptance-list data flow.','UNTESTED: production acceptance, actual PRELAUNCH, final C1 freeze, and the explicit-bound A296 verifier; root and other-lane steps remain.','TESTED static binding-expression evaluation only; no wrapper Context, producer, guard or verifier is executed.']}
 def run(cid,f,e):
  try:
   x=f();d['checks'].append({'id':cid,'result':'PASS','evidence':e+(' '+str(x) if x is not None else '')})
  except Exception as ex:
   msg=type(ex).__name__+': '+str(ex);d['checks'].append({'id':cid,'result':'FAIL','evidence':msg});d['blocking_findings'].append({'check':cid,'file_line':SOURCES['draft']['path']+':1','sha256':SOURCES['draft']['sha256'],'detail':msg})
 def c01():
  refs=[]
  def visit(x):
   if isinstance(x,dict):
    if 'path' in x and 'sha256' in x:pin(x);refs.append(x)
    else:
     for v in x.values():visit(v)
   elif isinstance(x,list):
    for v in x:visit(v)
  visit(r);require(len(refs)==13 and canonical(r['approved_certificate_producers'])==canonical(expected))
  return '13 pins. Pending review text is not a pin.'
 run('C01',c01,'TESTED bytes and absolute, realpath-equal, nonsymlink regular files.')
 run('C02',lambda:require(digest({k:v for k,v in r.items() if k!='certificate_policy_review'})==DIGEST),'TESTED independent canonical digest excluding only certificate_policy_review.')
 def c03():
  require(constants('core')['DRIVER_SHA']==constants('guard011')['R5_SHA']==constants('binding')['DRIVER_SHA']==DRIVER)
  assigns={n.targets[0].id:n.value for n in ast.parse(txt('wrapper')).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
  require(ast.unparse(assigns['DRIVER_SHA'])=='M.DRIVER_SHA')
  require(ast.literal_eval(next(k.value for k in assigns['M'].keywords if k.arg=='expected'))==SOURCES['core']['sha256'])
 run('C03',c03,'TESTED static AST: core, guard011, binding DRIVER_SHA and wrapper M.DRIVER_SHA/core expected pin agree.')
 def c04():
  x=next(x for x in ast.parse(txt('wrapper')).body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='G' for t in x.targets))
  p=ast.literal_eval(x.value.args[0].args[0]);h=ast.literal_eval(next(k.value for k in x.value.keywords if k.arg=='expected'))
  require({'path':p,'sha256':h}==SOURCES['guard']==constants('binding')['GUARD']);read(p,h)
 run('C04',c04,'TESTED A296 wrapper L32 guard path/expected and binding GUARD equal the actual full byte hash.')
 def c05():
  b=bindings(r);require(b['driver_slot_rule']==SLOT and b['post_state_handoff']==HANDOFF);has('wrapper',"handoff.get('schema')!='"+HANDOFF+"'")
 run('C05',c05,'TESTED wrapper L74-75 slot/handoff bindings and L130 schema check.')
 def c06():
  reg=strict(RAW['registry']);require(reg['schema']=='S4RC1_C1_CERTIFICATE_REGISTRY_C3V003' and reg['complete_31_point_table'] is True and reg['count']==len(reg['points'])==31)
  producers={g:set() for g in ('EPS','GQ','LO_RHO_SLOT')}
  for k,rec in reg['points'].items():
   require(set(rec)=={'identity','bundle','eps_certificate','lo_certificate'} and digest(rec['identity'])==k)
   b=strict(pin(rec['bundle'],True));require(set(b['prelaunch'])==set(producers) and b['point_sha256']==k and canonical(b['identity'])==canonical(rec['identity']))
   for g,i in (('EPS',0),('GQ',1),('LO_RHO_SLOT',2)):
    p=strict(pin(b['prelaunch'][g],True));require(p['schema']=='UNT_CALIBRATION_POINT_PROOF_CX2V001' and p['gate']==g and p['point_sha256']==k and p['status']=='TESTED' and p['verdict']=='PASS' and canonical(p['producer'])==canonical(expected[i]));producers[g].add(canonical(p['producer']).decode())
  require(all(len(v)==1 for v in producers.values()));d['registry_producer_sets']={k:[strict(x) for x in sorted(v)] for k,v in producers.items()}
 run('C06',c06,'TESTED 31 identity keys, exact record shape, 31 bundle pins and 93 proof pins, whole producer dictionaries. No numeric, rho, or driver certificate references opened.')
 def c07():
  for n,label in [('lo_adapter','LO_STATE_ADAPTER_NOT_APPROVED'),('srb_adapter','SRB_ROT_ADAPTER_NOT_APPROVED')]:has(n,"me = env.self_pin()","if me['sha256'] not in approved:",label)
  has('evidence',"proof=dict(schema='UNT_CALIBRATION_POINT_PROOF_CX2V001'","producer=C.pin(__file__)","proof.update(gate='GQ_SIGNED'")
  has('guard',"if producer.get('sha256') not in approved:","signed = proof(row['GQ_SIGNED'], 'GQ_SIGNED')","lo = proof(row['LO'], 'LO')")
  require(txt('handoff').count("approved_producer_sha256=[p['sha256'] for p in policy['approved_certificate_producers']]")>=3)
  for n in ('rows','lo_core','response','facade'):require('UNT_CALIBRATION_POINT_PROOF_CX2V001' not in txt(n))
  for n,key,w in [('rows','SCHEMA','UNT_POINT_LO_ROWS_CX2V001'),('rows','SRB_ROWS_SCHEMA','S4RC1_SRB_ROT_ROWS_INPUT_C3V001'),('lo_core','OUTPUT_SCHEMA','UNT_POINT_LO_NUMERICAL_CX2V001'),('response','EPS_SCHEMA','UNT_POINT_EPS_NUMERICAL_CX2V001'),('response','RHO_SCHEMA','UNT_POINT_RHO_NUMERICAL_CX2V001')]:require(constants(n)[key]==w)
  has('facade',"out['production_admissible']=False","out['certificate_status']='UNAVAILABLE'","out['verdict']='UNAVAILABLE'")
  has('wrapper',"producer not in r['approved_certificate_producers']")
  has('bridge',"ns={'__file__':str(Path(__file__).absolute())","exec(compile(pinned(CORE_PATH,CORE_SHA)")
  require(constants('binding')['EPS_ADAPTER']==SOURCES['bridge'])
  has('binding',"approved=old['approved_certificate_producers']+[EPS_ADAPTER]","len(old['approved_certificate_producers'])==6 and tr['approved_certificate_producers']==approved")
 run('C07',c07,'FORMAL source review; TESTED source-expression checks: LO adapter L676-678, SRB adapter L384-387, b1 L311-319, guard L112-114/174/207, handoff same list L466/502/527. Excluded rows/core/response emit inputs or numeric schemas; facade forces UNAVAILABLE. A296 guard uses the same approved set; the bridge binds its own producer identity; binding requires the exact old six plus the bridge.')
 def c08():
  require(r['trusted_source_producers']==d['trusted_source_producers'])
  has('lo_core','trusted_producer(row, trusted_source_producers)','trusted_producer(src, trusted_source_producers)')
  has('handoff',"tsp = policy.get('trusted_source_producers')","B1_EVIDENCE['sha256'] in tsp","trusted_source_producers=policy['trusted_source_producers']")
  has('srb_adapter',"prod['sha256'] not in set(trusted_source_producers)")
 run('C08',c08,'TESTED ordered trusted list; FORMAL flow: lo_core L223/248, handoff L456-458/467/503, SRB L314-315.')
 def c09():
  require(r['trusted_row_policy_review_sha256']==d['trusted_row_policy_review_sha256']);want={}
  for n in ('DLO','D404','DHI'):
   p=SOURCES['approval_'+n];a=strict(RAW['approval_'+n]);h=SOURCES['contract_'+n]['sha256'];require(a['verdict']=='APPROVED' and a['row_contract_sha256']==h);want[h]=p
  require(canonical(want)==canonical(r['row_policy_reviews']))
 run('C09',c09,'TESTED 0153/0154/0155 APPROVED; contract byte hashes equal approval fields and map keys; trusted order exact.')
 def c10():
  for name,key in [('custody_deriver','custody'),('state_enumerator','state_enumerator')]:
   p5=constants('common5')['PINS'][key];p4=constants('common4')['PINS'][key];require(p5==p4 and {'path':p5[0],'sha256':p5[1]}==r[name])
   l5=next(x for x in txt('common5').splitlines() if x.strip().startswith(repr(key)+':'));l4=next(x for x in txt('common4').splitlines() if x.strip().startswith(repr(key)+':'));require(l5==l4)
 run('C10',c10,'TESTED custody/enumerator pins and exact source lines equal c3v004, c3v005, and draft.')
 def c11():
  b=bindings(r);require(len(b)==7)
  for k,v in b.items():require(canonical(d[k])==canonical(v))
  d['seven_bindings_digest']=digest(b)
 run('C11',c11,'TESTED seven canonical C1 bindings derived from the pinned A296 wrapper expression; its eighth campaign-ledger binding is None for C1 and excluded here. No gate executed.')
 def c12():
  a=constants('common5');b=constants('common4')
  resolve=lambda c:[{'path':c['PINS'][k][0],'sha256':c['PINS'][k][1]} for k in c['CANONICAL_APPROVED_PRODUCERS']]
  require(canonical(resolve(a))==canonical(expected[:6]) and resolve(b)==expected[:3])
  x=constants('assembler5',{'HERE':str(Path(SOURCES['assembler5']['path']).parent)})
  require({'path':x['COMMON_PATH'],'sha256':x['COMMON_SHA']}==SOURCES['common5'])
  require(constants('binding')['GUARD']==SOURCES['guard'] and constants('binding')['EPS_ADAPTER']==SOURCES['bridge'])
  has('binding',"set(tr)==set(old)","all(tr[k]==v for k,v in old.items() if k not in ('approved_certificate_producers','certificate_policy_review'))",
      "review.get('status')=='TESTED' and review.get('ok') is True","all(review.get(k)==v for k,v in want.items())")
  has('bound_verifier','bound=A.H.validate_binding(s,binding_ref)',"c1_ref=bound['c1']","canonical_producers=bound['tail_readiness']['approved_certificate_producers']","len(rows)==31","report['n']==31")
  d['verifier_of_record']={'binding':SOURCES['binding'],'explicit_bound_verifier':SOURCES['bound_verifier'],
      'scope':'FORMAL source review only. c3v005 ordered six is the legacy verifier for frozen C1; A296 requires the explicit-bound verifier and the seven producers.'}
 run('C12',c12,'TESTED static source assertions; FORMAL consumer trace. Neither binding gate nor verifier executed.')
 def c13():
  base=strict(RAW['base_c1']);draft=strict(RAW['draft']);leaf=strict(RAW['leaf_diff'])
  def flatten(v,p=''):
   if isinstance(v,dict) and v:
    out={}
    for k,x in v.items():out.update(flatten(x,p+'.'+k if p else k))
    return out
   if isinstance(v,list) and v:
    out={}
    for i,x in enumerate(v):out.update(flatten(x,p+'.['+str(i)+']'))
    return out
   return {p:canonical(v)}
  aa,bb=flatten(base),flatten(draft)
  changed=sorted(k for k in set(aa)|set(bb) if aa.get(k)!=bb.get(k))
  require(changed==leaf['changed_leaves'] and len(changed)==leaf['n_changed']==38)
  require(leaf['base']==SOURCES['base_c1'] and leaf['draft_sha256']==SOURCES['draft']['sha256'])
  tail_changed=[k for k in changed if k.startswith('tail_readiness.')]
  require(tail_changed==leaf['tail_changed_leaves'])
  require(all(k.startswith('tail_readiness.approved_certificate_producers.[6].') or k.startswith('tail_readiness.certificate_policy_review') for k in tail_changed))
  require({k.split('.')[0] for k in changed}<={'tail_readiness','schema','status','supersedes','drafted_by','drafted_utc','frozen','placeholder'})
  oldtail=base['tail_readiness'];newtail=draft['tail_readiness']
  require(set(oldtail)==set(newtail))
  require(canonical(newtail['approved_certificate_producers'])==canonical(oldtail['approved_certificate_producers']+[SOURCES['bridge']]))
  require(all(canonical(newtail[k])==canonical(v) for k,v in oldtail.items() if k not in ('approved_certificate_producers','certificate_policy_review')))
  require('frozen' not in draft and 'frozen' in base and 'placeholder' in draft)
  require(draft['schema']=='UNT_DDO154_C1_TAIL_READINESS_H1_DRAFT_C2V003')
  require(digest({k:v for k,v in newtail.items() if k!='certificate_policy_review'})==leaf['c1_tail_readiness_digest_excluding_review']==DIGEST)
  d['independent_leaf_diff']={'changed_leaves':changed,'n_changed':len(changed),'tail_changed_leaves':tail_changed}
 run('C13',c13,'TESTED independent flatten/diff from both pinned C1 documents: exactly 38 documented changed leaves, only permitted top-level metadata and tail entry seven/review placeholder.')
 d['ok']=not d['blocking_findings'];d['source_pins']=SOURCES;d['files_opened']=sorted(OPENED);d['opened_file_pins']=[{'path':p,'sha256':s} for p,s in sorted(OPENED.items())]
 require([x['id'] for x in d['checks']]==['C%02d'%i for i in range(1,14)])
 def validate(x):
  if isinstance(x,dict):
   require(not({'synthetic','synthetic_fixture'} & set(x)))
   for v in x.values():validate(v)
  elif isinstance(x,list):
   for v in x:validate(v)
 validate(d);strict(canonical(d));return d
if __name__=='__main__':print(json.dumps(checks(),sort_keys=True,indent=2,allow_nan=False))
