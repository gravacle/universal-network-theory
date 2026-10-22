"""Expanded actual-chain inert variants; no launch or scientific execution."""
from pathlib import Path
import tempfile,hashlib,json,io,contextlib
b=Path(__file__).parent;out=Path(tempfile.mkdtemp(prefix='terminal_chain_variants_',dir=b/'inert_fixtures'))
base=b/'test_natural_registered_observation_cx1v005.py';source=base.read_text();results=[]
variants=[('child_failure','CHILD_FAILED',1,None),('wall','STOPPED_WALL_CAP',-15,'WALL_CAP'),('rss','STOPPED_RSS_CAP',-15,'RSS_CAP'),('output','STOPPED_OUTPUT_CAP',-15,'OUTPUT_CAP'),('foreign_caps','FINISHED',0,None)]
for name,status,code,stop in variants:
 s=source.replace("status='FINISHED',exit_code=0,stop_reason=None",'status='+repr(status)+',exit_code='+repr(code)+',stop_reason='+repr(stop))
 old="got=observe(**a);assert decide(**got)=='HOLD_UNCLASSIFIED_OUTCOME';passed.append('whole helper chain: FINISHED remains unclassified')"
 if name=='foreign_caps':
  begin=s.index(' # Inject fresh-boundary');end=s.index(" for name,changes in [('unrequested'",begin);s=s[:begin]+s[end:]
  s=s.replace("receipt['receipt_sha256']=", "receipt['caps']=dict(caps,wall_cap_s=99);side['caps']=dict(caps,wall_cap_s=99)\n receipt['receipt_sha256']=")
  new="try:observe(**a)\n except Refusal:passed.append('self-consistent foreign receipt caps refuse')\n else:raise AssertionError('foreign caps')"
 else:new="got=observe(**a);assert decide(**got)=='NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK';passed.append('associated "+name+" yields uncounted fallback hint')"
 s=s.replace(old,new)
 variant=out/(name+'.py')
 with variant.open('x') as f:f.write(s)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(compile(s,str(variant),'exec'),{'__file__':str(base),'__name__':'__main__'})
 report=Path(buf.getvalue().strip().splitlines()[-1]);data=json.loads(report.read_bytes())
 results.append(dict(name=name,status='PASS',variant=dict(path=str(variant),sha256=hashlib.sha256(variant.read_bytes()).hexdigest()),report=dict(path=str(report),sha256=hashlib.sha256(report.read_bytes()).hexdigest()),tested=data['tested']))
with (out/'TEST_REPORT.json').open('x') as f:json.dump(results,f,indent=2)
print(out/'TEST_REPORT.json')
