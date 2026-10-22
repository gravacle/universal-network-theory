"""Terminal receipt association prerequisites, not authenticated liveness or admission.
Caller must supply root-bound layout/runtime/caps and exact pins. No missing-file fallback.
"""
import hashlib,json
from pathlib import Path
from datetime import datetime
from request_guard_cx1v002 import require
SCHEMA='UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001'

def terminal_association(snapshot, *, receipt_pin, launch_pin, spec, driver, monitor, python, outdir, caps):
 require(launch_pin['path']==receipt_pin['path']+'.launch.json','TERMINAL_SIDECAR_PATH')
 out=Path(outdir)
 require(out.is_absolute() and str(out.resolve())==str(out),'TERMINAL_OUTDIR')
 require(receipt_pin['path']==str(out.parent/'RECEIPT.json'),'TERMINAL_RECEIPT_PATH')
 r=snapshot.document(receipt_pin);l=snapshot.document(launch_pin)
 require(type(r) is dict and type(l) is dict,'TERMINAL_SCHEMA')
 require(r.get('schema')==SCHEMA and l.get('schema')==SCHEMA+'_LAUNCH','TERMINAL_SCHEMA')
 body={k:v for k,v in r.items() if k!='receipt_sha256'}
 sha=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 require(r.get('receipt_sha256')==sha,'TERMINAL_SELF_HASH')
 pins=dict(spec=spec,driver=driver,monitor=monitor,python=python)
 command=[python,'-I','-B',driver['path'],'run','--spec',spec['path'],'--outdir',outdir]
 require(r.get('pins')==l.get('pins')==pins,'TERMINAL_EXACT_PINS')
 require(r.get('command')==l.get('command')==command,'TERMINAL_COMMAND')
 require(r.get('caps')==l.get('caps')==caps,'TERMINAL_CAPS')
 require(type(r.get('child_pid')) is int and r['child_pid']>0 and r['child_pid']==l.get('child_pid'),'TERMINAL_PID')
 require(r.get('utc_start')==l.get('utc'),'TERMINAL_START')
 try:
  start=datetime.fromisoformat(r['utc_start'].replace('Z','+00:00'));end=datetime.fromisoformat(r['utc_end'].replace('Z','+00:00'))
  ordered=start.tzinfo is not None and end.tzinfo is not None and end>=start
 except (KeyError,TypeError,ValueError,AttributeError):ordered=False
 require(ordered,'TERMINAL_TIME')
 require(type(r.get('retries')) is int and r['retries']==0 and type(l.get('retries_allowed')) is int and l['retries_allowed']==0,'TERMINAL_RETRIES')
 code=r.get('exit_code');stop=r.get('stop_reason');status=r.get('status')
 require(type(code) is int,'TERMINAL_EXIT_CODE')
 if status=='FINISHED':
  require(code==0 and stop is None,'TERMINAL_STATUS');decision='NEEDS_TAXONOMY'
 elif status=='CHILD_FAILED':
  require(code!=0 and stop is None,'TERMINAL_STATUS');decision='INFRA_UNCOUNTED'
 else:
  require(stop in ('WALL_CAP','RSS_CAP','OUTPUT_CAP') and status=='STOPPED_'+stop,'TERMINAL_STATUS')
  decision='CAP_UNCOUNTED'
 result=r.get('result')
 if result is not None:
  require(type(result) is dict and result.get('path')==str(out/'result.json'),'TERMINAL_RESULT_PATH')
  snapshot.pin(result)
 return {'prerequisites_only':True,'receipt':r,'launch':l,'outcome_hint':decision}
