"""Synthetic control-flow refutations for v006 certificate hooks; no science."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import importlib.util
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('cx2_hooks',HERE/'calibration_orchestrator_cx2v006r4.py')
M=importlib.util.module_from_spec(sp);sys.modules[sp.name]=M;sp.loader.exec_module(M)
checks=[]
def check(name,ok):checks.append({'name':name,'status':'TESTED','passed':bool(ok)})
cfg=json.loads((HERE/'RUN_CONFIG_DDO154_CX2V006_KB064_R1.json').read_bytes())
cfg['work_dir']=str(HERE/'NO_LAUNCH_HOOK_FIXTURE');cfg['work_dir_volume']=None
cfg['work_dir_identity']={'resolved':cfg['work_dir'],'volume':None,'volume_uuid':None,'symlinks':[]}
ctx=M.Context(cfg)
check('missing policy fails gate',not ctx.gates['certificate_policy']['ok'])
check('missing policy fails preflight verifier',not ctx.certificate_check(ctx.base,'prelaunch')['ok'])
check('missing policy fails state acceptance',not ctx.certificate_check(ctx.base,'acceptance',result={},call_dir=HERE)['ok'])
check('certificate errors never root-resolvable as model invalid',
      ctx.taxonomy.never_invalid_code('CERTIFICATE_ACCEPTANCE_REFUSED: missing'))
class Fixture:
    def __init__(self,allowed):self.allowed=allowed;self.seen=[]
    def certificate_check(self,spec,phase,**kw):
        self.seen.append(phase);return {'ok':self.allowed,'blockers':[] if self.allowed else ['SYNTHETIC_MISSING']}
rp=HERE/'HOOK_SYNTHETIC_RESULT_V002.json'
with rp.open('x') as f:json.dump({'not_scientific':True},f)
old=M.O.CampaignExecutor.__mro__[1].classify
try:
    M.O.CampaignExecutor.__mro__[1].classify=lambda self,p,r:('VALID',None,{'fixture':True},{'result_path':str(rp),'call_dir':str(HERE)})
    for ok in (False,True):
        f=Fixture(ok);ex=M.CampaignExecutor(f)
        got=ex.classify({'spec':{}},{})
        check('ingest hook '+str(ok),got[0]==('VALID' if ok else 'INFRA') and f.seen==['acceptance'])
        if not ok:check('rejected ingest no forward',got[2] is None)
finally:M.O.CampaignExecutor.__mro__[1].classify=old
class Denied:
    work_dir=HERE;cache_id='fixture'
    def check_cached_certificate(self,entry):raise M.Error('CERTIFICATE_CACHE_REFUSED: synthetic')
cache=M.Cache(Denied());cache.entries={'a':{'forward':{'valid':True}}}
for name,fn in [('read',lambda:cache.forward('a')),('put',lambda:cache.put(key='a',theta={},classification='VALID',
    failure_class=None,source='fixture',provenance={},forward={}))]:
    refused=False
    try:fn()
    except M.Error as e:refused=str(e).startswith('CERTIFICATE_CACHE_REFUSED')
    check('cache '+name+' calls certificate hook',refused)
result={'execution_note':M.WAIVER,'launches_performed':0,'scope':'synthetic hook control flow only',
        'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)}
with (HERE/'CERTIFICATE_HOOK_CHECK_V002.json').open('x') as f:json.dump(result,f,indent=1);f.write('\n')
print(json.dumps({'passed':result['passed'],'total':result['total']}))
