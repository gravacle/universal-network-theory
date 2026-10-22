"""External cache prerequisite revalidation only; parent/cache certificate checks still required.
Does not reuse admission: an already ingested wave and cached key are expected here.
Caller supplies a fresh snapshot shared with the subsequent parent verification.
"""
from request_guard_cx1v002 import require, check_request
from custody_guard_cx1v003 import check_valid_custody

def check_external_cache(snapshot, *, ctx, entry, theta_key):
 p=entry.get('provenance') or {}
 require(entry.get('source')=='WAVE' and entry.get('classification')=='VALID','EXTERNAL_CACHE_SOURCE')
 require(p.get('execution_origin')=='DIRECT_EXTERNAL','EXTERNAL_CACHE_ORIGIN')
 a=p.get('external_admission') or {}
 require(a.get('schema')=='CX1_EXTERNAL_VALID_ADMISSION_V001','EXTERNAL_CACHE_SCHEMA')
 require(a.get('config_sha256')==ctx.config_sha256 and a.get('cache_id')==ctx.cache_id,'EXTERNAL_CACHE_IDENTITY')
 c=a.get('candidate') or {}
 require(c.get('key')==entry.get('key') and c.get('theta')==entry.get('theta'),'EXTERNAL_CACHE_THETA')
 require(c.get('call_dir')==p.get('call_dir'),'EXTERNAL_CACHE_DIRECTORY')
 pp=a.get('natural_plan') or {};plan=snapshot.document(pp)
 mapped=ctx.mapper.build(entry['theta'])
 r=check_request(snapshot,work_dir=ctx.work_dir,wave=plan.get('wave'),call_index=c.get('call_index'),
  plan_pin=pp,config_sha256=ctx.config_sha256,cache_id=ctx.cache_id,gate_digest=ctx.gate_digest,
  candidate=c,mapped=mapped,theta_key=theta_key,cached_keys=(),driver_pin=ctx.driver)
 custody=check_valid_custody(snapshot,call=r['call'],candidate=c,driver_pin=ctx.driver,monitor_pin=ctx.cfg['monitor'])
 require((p.get('tail_certificates') or {}).get('certificate_bundle')==c.get('bundle'),'EXTERNAL_CACHE_BUNDLE')
 return {'candidate':c,'call':r['call'],'custody':custody,'prerequisites_only':True}
