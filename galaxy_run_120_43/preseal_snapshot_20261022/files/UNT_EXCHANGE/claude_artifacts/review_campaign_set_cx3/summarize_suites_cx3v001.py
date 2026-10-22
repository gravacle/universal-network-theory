import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).parent
roots=[H/'h3_repeat1_v4/RUN_20261020T145057Z_11218',H/'h3_repeat2/RUN_20261020T145158Z_11934',H/'campaign_repeat1_v3/RUN_20261020T144828Z_10146',H/'campaign_repeat2/RUN_20261020T145103Z_11379']
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
reports=[];auditpins=[];foreign={};data=[]
for r,want in zip(roots,[94,94,90,90]):
 p=r/'TEST_RESULTS.json';d=json.loads(p.read_bytes());assert d['all_pass'] and d['n']==want and d['n_pass']==want and not d['audit']['denied']
 reports.append({'result':pin(p),'n':want,'n_pass':want,'wall_s':d['wall_s'],'audit':d['audit']});data.append(d)
for l,r in [(0,1),(2,3)]:assert [(x['name'] if 'name' in x else x.get('id'),x['expect'],x['pass']) for x in data[l]['results']]==[(x['name'] if 'name' in x else x.get('id'),x['expect'],x['pass']) for x in data[r]['results']]
for p in sorted((H/'suite_audits_cx3v001').glob('AUDIT_*.json')):
 d=json.loads(p.read_bytes());texts=[d['script']['path'],*d['argv']]
 if not any(any(str(r) in str(x) for x in texts) for r in roots):continue
 assert not d['denied'],(p,d['denied'])
 assert d['peak_rss_bytes']<8<<30,(p,d['peak_rss_bytes'])
 auditpins.append(pin(p));data.append(d)
 for q in [d['script'],*d['foreign_read_pins']]:
  path=Path(q['path'])
  if path.is_relative_to(H):continue
  assert q==pin(path),('source changed',q)
  if q['path'] in foreign:assert foreign[q['path']]==q['sha256']
  foreign[q['path']]=q['sha256']
pres=sum(len(d.get('preserved_redundant_tmp_names',[])) for d in data)
rec={'schema':'CX3_A205_SUITE_SUMMARY_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'status':'TESTED','suite_results':reports,'same_row_expectation_outcomes_each_repeat':True,'instrumented_processes':len(auditpins),'peak_rss_bytes_max':max(d.get('peak_rss_bytes',0) for d in data),'audit_denials':0,'loaded_program_dependencies':[{'path':p,'sha256':s} for p,s in sorted(foreign.items())],'audit_records':auditpins,'harness':pin(H/'run_audited_suite_cx3v003.py'),'summary_script':pin(Path(__file__)),'substitutions':['Unmodified pinned suites executed through inherited audit wrapper; only pinned suites, monitor and hash-exact synthetic mock may run as Python subprocesses','Redundant hardlinked temporary names preserved instead of deletion; count '+str(pres),'macOS sandbox rejected resource.setrlimit; per-process watchdog checked actual peak RSS against8GiB. Values reported are Darwin bytes','H3 final repeats used approved process-table access for genuine F4 ps check; earlier sandbox-only retry refused closed'],'earlier_attempts':['Wrapper v001 failed before suite at setrlimit','Wrapper v002 denied local gethostname and misplaced final audit write; no production finding','H3 wrapper v003 sandboxed attempt93/94: F4 ps denied; two later complete repeats94/94'],'disclosure':'Codex3 holds generator/output-diff review, campaign-set review, policy signing and per-wave EPS signing. Signer gate/request-form findings are same-path. Synthetic suite substitutions are declared by the pinned test source; these results do not certify producer science.'}
p=H/'SUITE_SUMMARY_CX3V001.json'
with p.open('x') as f:json.dump(rec,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'summary':pin(p),'suites':[(x['n_pass'],x['n']) for x in reports],'instrumented_processes':len(auditpins),'dependencies':len(foreign),'max_rss':rec['peak_rss_bytes_max'],'temp_names_preserved':pres}))
