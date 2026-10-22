from pathlib import Path
import ast, hashlib, json, types, datetime
B=Path('/Users/bgm/Research/UNT_EXCHANGE'); A=B/'claude_artifacts'; K=A/'ks_k3_chain_c2'
D=A/'s1_c1_producer_list_cx1'
cache={}
def raw(p):
 p=Path(p)
 if p not in cache: cache[p]=p.read_bytes()
 return cache[p]
def pin(p): return {'path':str(p),'sha256':hashlib.sha256(raw(p)).hexdigest()}
def evidence(p,lo,hi):
 lines=raw(p).decode().splitlines(); return dict(pin(p),line_start=lo,line_end=hi,excerpt='\n'.join(lines[lo-1:hi]))
files=['point_response_admission_adapter_cx2v003_g4_c2v001.py','gq_producer_cx2v005_g3_c2v001.py','lo_slot_proof_c3v003_g1_c2v001.py','lo_state_proof_adapter_c3v003_ks6_c2v002.py','srb_rot_adapter_c3v003_g2_c2v001.py','current_source_evidence_b1_c2v001_g6_c2v001.py']
expected=['e00ab71d','c3699c78','6af9ed6c','c8dc59a1','7eb456cd','65834e9b']
approved=[pin(K/f) for f in files]
assert all(p['sha256'].startswith(e) for p,e in zip(approved,expected))
row=A/'s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py'
trusted=[pin(row),approved[5]]; assert trusted[0]['sha256'].startswith('67fddd24')
common=K/'s4rc1_common_c3v004_ks3_c2v002.py'; assembler=K/'registry_assembler_c3v004_ks4_c2v002.py'
# Only constant assignments are evaluated; imports and all module functions are excluded.
def constants(p):
 ns={}
 for n in ast.parse(raw(p)).body:
  if isinstance(n,ast.Assign):
   try: v=eval(compile(ast.Expression(n.value),str(p),'eval'),{'__builtins__':{}},ns)
   except Exception: continue
   for t in n.targets:
    if isinstance(t,ast.Name): ns[t.id]=v
 return ns
cn=constants(common); an=constants(assembler)
assert cn['CANONICAL_APPROVED_PRODUCERS_S1']==('eps_adapter_g4','gq_producer_g3','lo_slot_proof_g1')
canonical=lambda n:dict(zip(('path','sha256'),cn['PINS'][n]))
assert [canonical(n) for n in cn['CANONICAL_APPROVED_PRODUCERS_S1']]==approved[:3]
# Extract the exact policy gate AST; all JSON/byte I/O uses inert in-memory fixtures.
fn=next(n for n in ast.parse(raw(assembler)).body if isinstance(n,ast.FunctionDef) and n.name=='c1_policy_gate')
registry={'path':'/inert/registry.json','sha256':'1'*64}; reviewpin={'path':'/inert/review.json','sha256':'2'*64}; c1pin={'path':'/inert/c1.json','sha256':'3'*64}
docs={}; reads=[]
C=types.SimpleNamespace(**{k:cn[k] for k in ('ART','PINS','DRIVER_SHA','CANONICAL_APPROVED_PRODUCERS','CANONICAL_APPROVED_PRODUCERS_S1')})
C.canonical_pin=canonical; C.read_json_pinned=lambda p,*a:docs[p['path']]; C.read_bytes_pinned=lambda p,*a:reads.append(p)
class Refusal(Exception): pass
ns={'C':C,'Refusal':Refusal,**{k:an[k] for k in ('C1_REQUIRED_PINS','POLICY_SCHEMA','SLOT_RULE')}}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(assembler),'exec'),ns)
def case(name,prods,want):
 r={k:dict(reviewpin) for k in an['C1_REQUIRED_PINS']}
 r.update(custody_deriver=canonical('custody_ks1'),state_enumerator=canonical('state_enumerator_g6'),certificate_registry=registry,certificate_policy_review=reviewpin,approved_certificate_producers=prods)
 docs[c1pin['path']]={'tail_readiness':r}
 docs[reviewpin['path']]={'schema':an['POLICY_SCHEMA'],'status':'TESTED','ok':True,'driver_sha256':cn['DRIVER_SHA'],'custody_deriver':r['custody_deriver'],'state_enumerator':r['state_enumerator'],'approved_certificate_producers':prods,'guard_sha256':cn['PINS']['guard_ks5'][1],'driver_slot_rule':an['SLOT_RULE'],'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
 _,bad=ns['c1_policy_gate'](c1pin,registry,s1=True)
 assert len(bad)==want,(name,bad)
 return {'id':name,'PASS':True,'blockers':bad}
tests=[case('existing_three_compatibility',approved[:3],0),case('existing_six_refused',approved,3)]
# In-memory proposal only, no published module edits and no canonical_producers API override.
for name,p in zip(('lo_state_adapter_s1','srb_rot_adapter_s1','evidence_s1'),approved[3:]): C.PINS=dict(C.PINS,**{name:(p['path'],p['sha256'])})
C.canonical_pin=lambda n:dict(zip(('path','sha256'),C.PINS[n]))
C.CANONICAL_APPROVED_PRODUCERS_S1 += ('lo_state_adapter_s1','srb_rot_adapter_s1','evidence_s1')
tests += [case('proposed_six_membership_pass',approved,0),case('row_producer_seventh_refused',approved+[trusted[0]],1),case('reordered_six_still_pass_membership_only',list(reversed(approved)),0),case('duplicate_six_still_pass_membership_only',approved+[approved[0]],0)]
ev=[]
for f,lo,hi in [(files[0],196,212),(files[1],61,80),(files[2],342,350),(files[2],384,387),(files[3],692,695),(files[3],761,774),(files[4],458,467),(files[4],532,543),(files[4],381,392),(files[5],291,298),(files[5],334,353),(files[5],360,380),('certificate_guard_b1_ks5_c2v001.py',143,155),('certificate_guard_b1_ks5_c2v001.py',209,217),('certificate_guard_b1_ks5_c2v001.py',246,248),('lo_core_r5_cx2v001_ks6_c2v001.py',72,78),('lo_core_r5_cx2v001_ks6_c2v001.py',240,270),('acceptance_handoff_c2v004_ks6_c2v002.py',499,535),('acceptance_handoff_c2v004_ks6_c2v002.py',563,595),('s4rc1_common_c3v004_ks3_c2v002.py',110,125),('registry_assembler_c3v004_ks4_c2v002.py',409,451)]: ev.append(evidence(K/f,lo,hi))
ev += [evidence(row,125,134),evidence(row,215,222),evidence(A/'s1_successors_c2/s1_path_lib_c2v002c.py',110,131),evidence(A/'s1_successors_c2/s1_path_lib_c2v002c.py',933,937)]
# Record H1 precedent from permitted document without opening any referenced runs.
h1=A/'c1_h1_c2/C1_H1_C2V001.json'; hdoc=json.loads(raw(h1)); assert hdoc['acceptance_policy_inputs_from_c1']['deps']['row_producer']==trusted[0]
prec=A/'s4rc1_c3/build_c3v005_c2/DIFF_s4rc1_common_c3v004__c3v005.diff'; raw(prec)
roles=['EPS certificate','GQ certificate','LO_RHO_SLOT certificate','per-state LO certificate; own approval required','SRB_ROT certificate; own approval required','GQ_SIGNED / GQ_CURRENT_PREMISES and source reconstruction; both approval and source trust required']
out={'schema':'S1_C1_PRODUCER_LIST_DRAFT_CX1V001','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dispatch':'0792','status':'DRAFT_NOT_ADOPTED','verdict':'PASS','blocking_count':0,'verdict_scope':'Requested draft derivation only; existing S1 readiness defects remain open. No production readiness certification.','approved_certificate_producers':approved,'trusted_source_producers':[p['sha256'] for p in trusted],'trusted_source_producer_pins':trusted,'ordered_roles':[{'position':i+1,'role':r,'pin':p} for i,(r,p) in enumerate(zip(roles,approved))],'order_basis':'A182 first three preserved; append LO, SRB_ROT, evidence in A209 H1 precedent order. Code imposes membership, not a unique ordering; this exact proposed ordering requires root ruling and freeze binding. Trusted order follows H1: row producer then evidence.','policy_companions':{'approved_evidence_producer_sha256':[approved[5]['sha256']],'approved_uniform_producer_sha256':[approved[1]['sha256']],'evidence_producer':approved[5]},'excluded_from_certificate_approval':['row_reference_producer: source/readout records only','KS2 numeric response and G3 geometry: numerical provenance, not final certificate producers','G3 b1 helper: G6b emits final signed proof using its own pin','LO core: adapter emits final LO certificate using its own pin','G6c: separately bound state_enumerator'], 'scope':'S1_UA_C3T only; S1_UA_C4T retains campaign C1 and predecessor producers (A185).','registry_verifier':{'common':pin(common),'assembler':pin(assembler),'three_pin_limit':True,'six_list_observed_blockers':3,'minimal_successor':'New KS3 common: add three whole path/hash PINS for KS6-prime, G2 and G6b; extend CANONICAL_APPROVED_PRODUCERS_S1 to the ordered six. Preserve non-S1 tuple, row32/K3 logic and all existing pins. New KS4 assembler: only COMMON_PATH, COMMON_SHA and explanatory docstring. No registry/bundle/proof or producer rewrites. Keep exact-pin and policy review bindings.','limitations':'Membership does not enforce list completeness, uniqueness, order or per-gate producer restriction. Root must bind exact ordered lists in S1 C1 freeze/policy review; inspect S1 prelaunch proofs independently at its future verify. Do not use canonical_producers override as adoption.'},'integration_obligations':['Root rules ordered lists; Codex3 S1 certificate policy review; root freeze and real verify after u_A/row32 prerequisites.','S1 source closure: lib v002c S1_FENCE_SOURCES lacks KS6-prime, G2 and G6b. Expanded C1 reads all producers during prelaunch. Add exact three pins to admission sources via reviewed successor or explicit root-owned assembly; perform inert fence test and root dry launch. Actual admission base was not read, so no claim that the final assembled source list is missing them.','Keep separate evidence/uniform approvals and packet/row reviews; these lists alone do not establish acceptance.'], 'TESTED':['Byte-derived pins and exact first-three common association','Static source trace of emission, self approval, source trust and guard membership','Six isolated exact-AST c1_policy_gate cases with in-memory I/O stubs; proposed table extension only in memory'], 'UNTESTED':['Full module import and complete published suites','Full S1 acceptance, real C1, registry, row32 proofs, target data, production seal/launch','Actual admission source closure/fence and successor implementation'], 'tests':tests,'evidence':ev,'precedent':[pin(h1),pin(prec)]}
D.mkdir(exist_ok=False)
def write(p,obj):
 with p.open('x') as f: f.write(json.dumps(obj,indent=2)+'\n')
write(D/'S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json',out)
with (D/'README.md').open('x') as f: f.write('''# S1 C1 producer-list draft — 0792\n\nPASS, 0 blockers to the draft deliverable; NOT adopted and not a readiness verdict.\n\nProposed certificate order: G4 EPS, G3 GQ, G1 slot proof, KS6′ LO adapter, G2 SRB-ROT adapter, G6b evidence. Trusted source order: row_reference_producer_c2v003, G6b evidence (hash strings in the policy). Code establishes membership requirements; order follows A182 plus A209 and remains for root to rule.\n\nThe current KS4′ verifier rejects the six with exactly three canonical-producer blockers. Six isolated AST policy-gate cases pass their expected outcomes; no real registry or acceptance execution occurred. The JSON carries exact byte hashes, line excerpts, the proposed minimal KS3/KS4 successor and untested scope.\n\nThe three additions must also enter the admission source closure: lib v002c does not include them in its additions. The actual base admission was not inspected. Exact list order/completeness/uniqueness need freeze/review binding; verifier membership alone is insufficient.\n\nRoot rules after reset; Codex3 signs the S1 policy review. No production modules changed, scientific calculation, seal, launch or protected run/data access.\n''')
with (D/'derive_and_check_cx1v001.py').open('xb') as f: f.write(Path(__file__).read_bytes())
write(D/'SOURCE_HASHES.json',[pin(p) for p in sorted(cache)])
print(json.dumps({'draft':pin(D/'S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json'),'tests':len(tests),'all_pass':all(x['PASS'] for x in tests)}))
