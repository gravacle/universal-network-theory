# R2-A closure lens: print slots V003 alternatives metadata and any string field naming the observation rule (no numeric arrays).
import json, hashlib
P = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
b = open(P, 'rb').read()
assert hashlib.sha256(b).hexdigest() == 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
d = json.loads(b.decode('utf-8'))
alts = d['alternatives']
print('alternatives keys:', list(alts.keys()))
for k, v in alts.items():
    if isinstance(v, list):
        for a in v:
            print(' ', k, {kk: a.get(kk) for kk in ('name', 'kind', 'status', 'headline', 'scope', 'scoring_scope', 'outer_rows') if kk in a})
    else:
        print(' ', k, str(v)[:300])
print('alternatives_note:', d.get('alternatives_note'))
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:60]): yield from walk(v, path + '[%d]' % i)
    elif isinstance(o, str):
        yield path, o
for path, s in walk(d):
    low = s.lower()
    if ('interpolat' in low or 'observation' in low or 'azimuth' in low) and 'query_block/rows' not in path:
        print(path, '::', s[:400])
print('stage0_registration keys:', list(d['stage0_registration'].keys()) if isinstance(d['stage0_registration'], dict) else type(d['stage0_registration']))
