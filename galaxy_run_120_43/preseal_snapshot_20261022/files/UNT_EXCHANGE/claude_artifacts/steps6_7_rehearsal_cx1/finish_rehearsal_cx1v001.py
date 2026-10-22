import json,hashlib,types,sys,datetime,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
source=ROOT/'miss_reading_rehearsal_cx1v001.py'
s=source.read_text().replace("OUT=ROOT/'reading_v001';OUT.mkdir()","OUT=ROOT/'reading_validation_v001';OUT.mkdir()")
m=types.ModuleType('rehearsal_reading_validation');m.__file__=str(source);sys.modules[m.__name__]=m;exec(compile(s,str(source),'exec'),m.__dict__)
t=time.monotonic();outer=ROOT/'run_20261018T185531505825Z';m.trace=json.loads((outer/'TRACE.json').read_bytes());score=json.loads((outer/'LADDER_SYNTHETIC.json').read_bytes());report=m.classify(score)
assert report['patterns']['P9'] and report['A15']['E2']=='NOT_TESTABLE'
assert report['zones']['OUTER']['N_v']==0 and report['zones']['OUTER']['counts']['INVALID_AS_MISS']==8
m.write(m.OUT/'OUTER_INVALID_PUBLIC_READING.json',report)
results=json.loads((ROOT/'reading_v001/RESULTS.json').read_bytes())
results['rough_edges']=[r for r in results['rough_edges'] if r['id']!='P9']
results['checks'].append({'name':'P9_public_two_pass_freeze_and_score','passed':True})
results['wall_seconds_P9_validation']=time.monotonic()-t
results['P9_public_trace']=m.pin(outer/'TRACE.json');results['P9_report']=m.pin(m.OUT/'OUTER_INVALID_PUBLIC_READING.json')
m.write(ROOT/'REHEARSAL_COMPLETE_V001.json',results)
files=[p for p in sorted(ROOT.rglob('*')) if p.is_file()]
with open(ROOT/'HASHES_REHEARSAL_V001.txt','x') as f:
 for p in files:f.write(m.pin(p)['sha256']+'  '+str(p)+'\n')
lines=['# 0603 steps 6–7 synthetic rehearsal','',datetime.datetime.now(datetime.timezone.utc).strftime('date -u: %a %b %d %H:%M:%S UTC %Y'),'','TESTED: two independent public two-pass freezes, exact v010-shaped synthetic route A/B results, eight selected members, 43-row LADDER scores; deliberate Q20 INVALID-as-miss and an all-outer-invalid public P9 case. All 14 classification/adoption checks pass. Every P0–P10 plus P1g and all 13 reading identifiers are reachable. No scientific inference.','', 'Step timings (seconds):']
for run in (ROOT/'run_20261018T185402142937Z',outer):
 tr=json.loads((run/'TRACE.json').read_bytes());lines += [f"- {run.name}: "+', '.join(x['step']+'='+format(x['wall_seconds'],'.4f') for x in tr['steps'])]
lines += ['', 'Public STAGE0_GRID_OUTER remains NOT_EVALUATED_BEFORE_FREEZE. Synthetic alternative raw rows are saved; the exact eight-row private score arithmetic and public status-flip refusal pass. An evaluated public alternative requires a root-adopted successor.', '', 'UNTESTED: production predictions, physical certificates, physical TSR flag assignment, preregistration adoption and scientific readings. The prereg is unsealed r2 round1. Explicit NOT_AVAILABLE/NOT_RUN fields expose missing E1b, C3 and flag carriers; none is fabricated. The rehearsal classifier is not a reviewed production producer.', '', 'Rough edges and owners are in the complete result; input/output byte pins are in the manifest. No targets from NGC3198, protected runs, network or solver launches were accessed. taskpolicy -b, nice10 and single-thread BLAS used. Geometry-box refusal remains the registered behavior, not zero uncertainty.', '', 'Pinned deliverables:']
for p in (ROOT/'REHEARSAL_COMPLETE_V001.json',ROOT/'HASHES_REHEARSAL_V001.txt',source,ROOT/'rehearse_freeze_cx1v001.py',ROOT/'rehearse_outer_invalid_cx1v001.py'):
 lines.append('- '+str(p)+' — '+m.pin(p)['sha256'])
with open(ROOT/'BUILD_REHEARSAL_V001.md','x') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'checks':len(results['checks']),'all_pass':all(x['passed'] for x in results['checks']),'build':m.pin(ROOT/'BUILD_REHEARSAL_V001.md')}))
