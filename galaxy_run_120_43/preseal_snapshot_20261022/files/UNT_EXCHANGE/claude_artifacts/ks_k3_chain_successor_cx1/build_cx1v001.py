from pathlib import Path
import json,hashlib,ast
B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'); K=B/'ks_k3_chain_c2'; D=B/'ks_k3_chain_successor_cx1'
draft=B/'s1_c1_producer_list_cx1/S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json'
buf=draft.read_bytes();assert hashlib.sha256(buf).hexdigest()=='ccb8f7d1ed5c2a4ae58b4a5595826dfa6ae17aee6b47d5713dc443aa930ff83a'; data=json.loads(buf)
oldc=K/'s4rc1_common_c3v004_ks3_c2v002.py'; olda=K/'registry_assembler_c3v004_ks4_c2v002.py'
c=oldc.read_bytes();a=olda.read_bytes();assert hashlib.sha256(c).hexdigest()=='fcd63a739c8ec36e3ce3f9ad9de65532acd649da5ecc91e7131b60d020c9d4c8'
assert hashlib.sha256(a).hexdigest().startswith('85c3343d')
keys=['lo_state_adapter_s1','srb_rot_adapter_s1','evidence_s1']
for p in data['approved_certificate_producers']:
 assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
s=c.decode(); node=next(n for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PINS' for t in n.targets))
ls=s.splitlines(keepends=True)
ls[node.end_lineno-1:node.end_lineno-1]=[f"    {k!r}: ({p['path']!r}, {p['sha256']!r}),\n" for k,p in zip(keys,data['approved_certificate_producers'][3:])]
s=''.join(ls)
old="CANONICAL_APPROVED_PRODUCERS_S1 = ('eps_adapter_g4', 'gq_producer_g3', 'lo_slot_proof_g1')"
assert s.count(old)==1
s=s.replace(old,old[:-1]+", 'lo_state_adapter_s1', 'srb_rot_adapter_s1', 'evidence_s1')")
s='# A240 / 0794: six-producer S1 verifier successor. Historical docstring below describes its predecessor.\n'+s
cn='s4rc1_common_ks3_cx1v001.py';an='registry_assembler_ks4_cx1v001.py'
newc=s.encode(); sha=hashlib.sha256(newc).hexdigest()
news=a.decode().replace("COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v002.py'",f"COMMON_PATH = HERE + '/{cn}'").replace("COMMON_SHA = 'fcd63a739c8ec36e3ce3f9ad9de65532acd649da5ecc91e7131b60d020c9d4c8'",f"COMMON_SHA = '{sha}'")
news='# A240 / 0794: KS3 successor pin only; inherited policy logic unchanged.\n'+news
D.mkdir(exist_ok=False)
for name,raw in [(cn,newc),(an,news.encode())]:
 with (D/name).open('xb') as f:f.write(raw)
closure={'schema':'S1_SOURCE_CLOSURE_DELTA_CX1V001','status':'DRAFT_ROOT_INTEGRATION_REQUIRED','basis':'A240; append to lib v002c S1 admission additions; no lib edits','source_map_additions':{p['path']:p['sha256'] for p in data['approved_certificate_producers'][3:]},'sources_to_add':data['approved_certificate_producers'][3:],'trusted_source_producers':data['trusted_source_producers'],'limitations':'Actual admission base uninspected. Root dry launch is deciding test. These are the three certificate-byte reads, not a claim of complete transitive acceptance imports.'}
with (D/'S1_SOURCE_CLOSURE_DELTA_CX1V001.json').open('x') as f:json.dump(closure,f,indent=2);f.write('\n')
with (D/'BUILD_INPUTS.json').open('x') as f:json.dump([{'path':str(p),'sha256':hashlib.sha256(v).hexdigest()} for p,v in [(oldc,c),(olda,a),(draft,buf)]],f,indent=2);f.write('\n')
with (D/'build_cx1v001.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(D)
