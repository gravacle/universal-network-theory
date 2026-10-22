# R2-A closure lens: print slots V003 stage0_registration (metadata) and the SA-REACH-01 / SA-BH-01 note blocks.
import json, hashlib
P = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
b = open(P, 'rb').read()
assert hashlib.sha256(b).hexdigest() == 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
d = json.loads(b.decode('utf-8'))
s = d['stage0_registration']
for k in ('evaluated_status_transition', 'execution_status', 'registration_status', 'outer_rows', 'root_ruling_section'):
    print(k, '::', json.dumps(s.get(k))[:800])
nb = d['notes_block_for_manifest']
print('notes keys:', list(nb.keys()))
sa = nb.get('structural_assumptions', {})
print('structural_assumptions keys:', list(sa.keys()))
for k, v in sa.items():
    print('---', k)
    print(json.dumps(v, indent=1)[:1500])
