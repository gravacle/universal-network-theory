"""Create an immutable successor of Codex3's own checker for root 0860 / D018."""
import ast
import hashlib
import json
from pathlib import Path

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT = ART / 'cert_policy_reviews_cx3'
OLD = OUT / 'check_c1_h1_policy_cx3v001.py'
NEW = OUT / 'check_c1_h1_policy_cx3v002.py'
old = OLD.read_text()
tree = ast.parse(old)
sources = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'SOURCES' for t in n.targets)))
for key in ('rulings', 'v006', 'ruling0688', 'dispatch0774', 'dispatch0776', 'dispatch0778'):
    sources.pop(key)


def source(key, relative, expected):
    path = ART / relative
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    assert h.startswith(expected), (key, h, expected)
    sources[key] = {'path': str(path), 'sha256': h}


source('draft', 'root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json', '387b1b35988e83435fc74826a744868d5ff54fbf9f52e5d5d031ef6c792ad1c1')
source('base_c1', 'c1_h1_c2/C1_H1_C2V001.json', '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1')
source('leaf_diff', 'root_thu_checklist_c3/c1_successor/draft_c3v001/LEAF_DIFF_C1_H1_DRAFT_C2V003.json', '5966bb66a79459f58e1a38f40c644f2c5961a3c926cd623b378ea2f9d12eb822')
source('wrapper', 'eps_rule_successor_cx2/integration/campaign/calibration_orchestrator_q5b1_ledger_a296_cx2v001.py', 'cb1f5e73')
source('guard', 'eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py', '3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25')
source('bridge', 'eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py', '1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4')
source('binding', 'eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py', '141c1cd2')
source('bound_verifier', 'eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py', '60ed81b5')
source('request', 'c1_h1_c2/CERT_POLICY_REVIEW_REQUEST_C2V002.md', '2e21dd1b8339e23a239ecc665e5ab06460de15afe99858bc20ce183e29abc840')
source('draft_builder', 'root_thu_checklist_c3/c1_successor/build_c1_successor_draft_c3v001.py', '2fec6c976e27914fffc7081881b19e23263a369e329b729de2be4246552f0a82')
source('fill_tool', 'root_thu_checklist_c3/c1_successor/fill_c1_pin_c2v003_c3v001.py', '8a645ca33fbe630b270057da0b36a492a8886f0530148a88863d3f8d013a67b7')
sources['previous_check'] = {'path': str(OLD), 'sha256': hashlib.sha256(OLD.read_bytes()).hexdigest()}
for key, folder, prefix in [('dispatch', 'FROM_CODEX', '0860_'),
                            ('deputy', 'FROM_CLAUDE3', '0327_'),
                            ('deputy_followup', 'FROM_CLAUDE3', '0330_'),
                            ('R3_handoff', 'FROM_CODEX3', '0709_')]:
    matches = [p for p in (ART.parent / folder).iterdir() if p.name.startswith(prefix) and p.suffix == '.md']
    assert len(matches) == 1
    p = matches[0]
    sources[key] = {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

# All helper logic is our own predecessor. No root helper/tool is executed.
text = '"""Codex3 read-only C1 policy checker, 0860 / D018. No producer, guard or verifier execution."""\n'
text += 'SOURCES = ' + repr(sources) + '\n'
text += old[old.index('\nimport ast'):]


def replace(a, b, count=1):
    global text
    assert text.count(a) == count, (a[:100], text.count(a), count)
    text = text.replace(a, b)


replace("SCRIPT='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/check_c1_h1_policy_cx3v001.py'",
        "SCRIPT=" + repr(str(NEW)))
replace("FINAL='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json'",
        "FINAL=" + repr(str(OUT / 'DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002.json')))
replace("DIGEST='6dc87838fc0e44ff5a8bd8067281644cf2bc2ddab0e367baca180eddeee335aa'",
        "DIGEST='3c03bae3473954fdeb842de508c64702602c981675f839d604c7156b8c5db030'")
replace("ORDER=('eps','gq','slot','lo_adapter','srb_adapter','evidence')",
        "ORDER=('eps','gq','slot','lo_adapter','srb_adapter','evidence','bridge')")
replace('stat.S_ISREG(st.st_mode) and st.st_size<=8388608',
        'stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=8388608')
replace("  if isinstance(x,ast.BinOp) and isinstance(x.op,ast.Add):return ev(x.left)+ev(x.right)",
"""  if isinstance(x,ast.BinOp) and isinstance(x.op,ast.Add):return ev(x.left)+ev(x.right)
  if isinstance(x,ast.BinOp) and isinstance(x.op,ast.Div):return Path(ev(x.left))/ev(x.right)
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('str','Path') and len(x.args)==1 and not x.keywords:
   return str(ev(x.args[0])) if x.func.id=='str' else Path(ev(x.args[0]))""")
replace(" return eval(compile(ast.Expression(call.args[2]),'<pinned binding expression>','eval'),{'__builtins__':{}},e)",
""" out=eval(compile(ast.Expression(call.args[2]),'<pinned binding expression>','eval'),{'__builtins__':{}},e)
 require(out.pop('certificate_ledger') is None)
 return out""")
replace("Codex3 authored none of the six bound producers or c3 tools.",
        "Codex3 authored none of the seven bound producers or c3 tools; A296 R3 reviews for rows 302, 501 and 504 are Codex3's, delivered in 0709.")
replace("The three Codex1 row-policy approvals remain separate.",
        "A296 R3 EPS reviews for rows 302, 501 and 504 are Codex3's (0709). The three Codex1 row-policy approvals remain separate.")
replace("actual PRELAUNCH, final C1 freeze, and c3v005 verify",
        "actual PRELAUNCH, final C1 freeze, and the explicit-bound A296 verifier")
replace("TESTED isolated gate extraction uses in-memory review bytes; no production Context is initialized.",
        "TESTED static binding-expression evaluation only; no wrapper Context, producer, guard or verifier is executed.")
replace('len(refs)==12', 'len(refs)==13')
replace("'12 pins. Pending review text is not a pin.'", "'13 pins. Pending review text is not a pin.'")
replace(" run('C03',lambda:require(constants('core')['DRIVER_SHA']==constants('guard011')['R5_SHA']==DRIVER),'TESTED core DRIVER_SHA and guard011 L10 R5_SHA equal.')",
""" def c03():
  require(constants('core')['DRIVER_SHA']==constants('guard011')['R5_SHA']==constants('binding')['DRIVER_SHA']==DRIVER)
  assigns={n.targets[0].id:n.value for n in ast.parse(txt('wrapper')).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
  require(ast.unparse(assigns['DRIVER_SHA'])=='M.DRIVER_SHA')
  require(ast.literal_eval(next(k.value for k in assigns['M'].keywords if k.arg=='expected'))==SOURCES['core']['sha256'])
 run('C03',c03,'TESTED static AST: core, guard011, binding DRIVER_SHA and wrapper M.DRIVER_SHA/core expected pin agree.')""")
replace("  require({'path':p,'sha256':h}==SOURCES['guard']);read(p,h)",
        "  require({'path':p,'sha256':h}==SOURCES['guard']==constants('binding')['GUARD']);read(p,h)")
replace("'TESTED wrapper L30 guard path/expected equals actual full byte hash.'",
        "'TESTED A296 wrapper L32 guard path/expected and binding GUARD equal the actual full byte hash.'")
replace("  has('wrapper',\"producer not in r['approved_certificate_producers']\")",
"""  has('wrapper',"producer not in r['approved_certificate_producers']")
  has('bridge',"ns={'__file__':str(Path(__file__).absolute())","exec(compile(pinned(CORE_PATH,CORE_SHA)")
  require(constants('binding')['EPS_ADAPTER']==SOURCES['bridge'])
  has('binding',"approved=old['approved_certificate_producers']+[EPS_ADAPTER]","len(old['approved_certificate_producers'])==6 and tr['approved_certificate_producers']==approved")""")
replace("Excluded rows/core/response emit inputs or numeric schemas; facade forces UNAVAILABLE.",
        "Excluded rows/core/response emit inputs or numeric schemas; facade forces UNAVAILABLE. A296 guard uses the same approved set; the bridge binds its own producer identity; binding requires the exact old six plus the bridge.")
start = text.index('  local=dict(r);mem=canonical(d);')
stop = text.index(" run('C11',", start)
text = text[:start] + text[stop:]
replace("'TESTED seven canonical bindings derived from draft plus pinned wrapper/core expression. Extracted actual gate returns ok true.'",
        "'TESTED seven canonical C1 bindings derived from the pinned A296 wrapper expression; its eighth campaign-ledger binding is None for C1 and excluded here. No gate executed.'")
start = text.index(' def c12():')
stop = text.index(" d['ok']=", start)
text = text[:start] + """ def c12():
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
""" + text[stop:]
replace("['C%02d'%i for i in range(1,13)]", "['C%02d'%i for i in range(1,14)]")
compile(text, str(NEW), 'exec')
with NEW.open('x') as f:
    f.write(text)
print(json.dumps({'path': str(NEW), 'sha256': hashlib.sha256(NEW.read_bytes()).hexdigest(),
                  'source_count': len(sources), 'parent_sha256': hashlib.sha256(OLD.read_bytes()).hexdigest()}))
