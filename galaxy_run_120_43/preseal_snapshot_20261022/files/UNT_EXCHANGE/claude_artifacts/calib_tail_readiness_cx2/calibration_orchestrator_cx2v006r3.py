"""v006 r2: certificate checks at preflight, ingest, cache put and cache reuse.

The source adapter is usable only with independently reviewed, pinned certificate
producers, a custody derivation function and a complete consumed-state enumerator.
Those scientific artifacts remain pending. Missing adapters fail closed. No launch
CLI is exposed in this build/review lane. Inherited v005 campaign code is unchanged.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
def load(path,name,expected=None):
    path=Path(path);raw=path.read_bytes()
    if expected is not None and hashlib.sha256(raw).hexdigest()!=expected:
        raise ValueError('source byte pin mismatch: '+str(path))
    sp=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m

M=load(HERE/'calibration_orchestrator_cx2v006r1.py','_cx2v006r1',expected='003d64ba52342b6741a1fa162a93731e0c8ee480f4107dfbf59ab7873976949a')
O=M.O
G=load(HERE/'certificate_analysis/certificate_guard_cx2v001.py','_cx2certguard',expected='f69678f92c6e18d07c765952c104b1d2fe0fbb90d72746cf9f5d41f2ae2d58b3')
Error=M.Error
WAIVER=M.WAIVER
DRIVER_SHA=M.DRIVER_SHA
HULL=M.HULL
validate_block=M.validate_block
point_identity=M.point_identity
OldContext=M.Context
OldCache=O.Cache
OldExecutor=O.CampaignExecutor
POLICY_SCHEMA='DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001'

class Context(OldContext):
    def __init__(self,config):
        super().__init__(config)
        self.gates['certificate_policy']=self.certificate_policy_gate()
        # Certificate scope/producer/enumerator/registry changes make a new cache.
        self.cache_id=M.digest({'schema':'DDO154_CACHE_CX2V006R2',
            'parent_cache_id':self.cache_id,'certificate_policy':self.cfg['tail_readiness'],
            'adapter_sha256':O.sha256_file(__file__),
            'guard_sha256':O.sha256_file(G.__file__)})
        self.gate_digest=self.gate_digest_of(self.gates)
        self.pins=self.all_pins()

    def certificate_policy_gate(self):
        r=self.cfg['tail_readiness']
        required=('certificate_registry','custody_deriver','state_enumerator','certificate_policy_review')
        missing=[k for k in required if not isinstance(r.get(k),dict)]
        producers=r.get('approved_certificate_producers')
        if not isinstance(producers,list) or not producers:
            missing.append('approved_certificate_producers')
        if missing:return M.gate_pending('CERTIFICATE_POLICY_PENDING: '+','.join(missing))
        try:
            for k in required:O.read_pinned(r[k],k)
            for p in producers:O.read_pinned(p,'approved certificate producer')
            g=M.checked_gate(r['certificate_policy_review'],POLICY_SCHEMA,
                {'driver_sha256':DRIVER_SHA,'custody_deriver':r['custody_deriver'],
                 'state_enumerator':r['state_enumerator'],'approved_certificate_producers':producers,
                 'guard_sha256':O.sha256_file(G.__file__)},'certificate policy review')
            return g
        except (Error,ValueError,OSError) as exc:return M.gate_pending(str(exc))

    def certificate_check(self,spec,phase,*,result=None,call_dir=None):
        validate_block(spec['numerics'])
        gate=self.certificate_policy_gate()
        if not gate['ok']:return {'ok':False,'blockers':gate['reasons']}
        r=self.cfg['tail_readiness'];ident=point_identity(spec)
        registry=M.pin_doc(r['certificate_registry'],'certificate registry')
        rec=registry.get('points',{}).get(M.digest(ident))
        if not isinstance(rec,dict) or rec.get('identity')!=ident:
            return {'ok':False,'blockers':['CERTIFICATE_POINT_MISSING_OR_MISMATCHED']}
        try:
            deriver=O.load_pinned_module(r['custody_deriver'],'cx2_cert_custody','custody deriver')
            custody=deriver.derive_custody(spec=spec,driver_sha256=DRIVER_SHA)
            states=[]
            if phase=='acceptance':
                enum=O.load_pinned_module(r['state_enumerator'],'cx2_cert_states','state enumerator')
                inv=enum.consumed_states(spec=spec,result=result,call_dir=str(call_dir))
                if not isinstance(inv,dict) or inv.get('complete') is not True:
                    return {'ok':False,'blockers':['COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED']}
                states=inv['states']
            return G.verify_bundle(rec['bundle'],ident,expected_custody=custody,
                approved_producer_sha256=[p['sha256'] for p in r['approved_certificate_producers']],
                phase=phase,required_states=states)
        except (Error,OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
            return {'ok':False,'blockers':[type(exc).__name__+': '+str(exc)]}

    def prelaunch_check(self,spec,recovery=False):
        normalized=super().prelaunch_check(spec,recovery=recovery)
        # An unfilled plan is inspectable, but cannot pass certificate_policy_gate.
        if self.cfg['tail_readiness'].get('certificate_registry') is not None:
            g=self.certificate_check(spec,'prelaunch')
            if not g['ok']:raise Error('CERTIFICATE_PREFLIGHT: '+repr(g['blockers']))
        return normalized

    def check_adoption(self):
        r=self.cfg['tail_readiness']
        return M.checked_gate(self.cfg.get('adoption_derivation'),'DDO154_TAIL_READINESS_CX2V006',
            {'base_spec_sha256':self.base_sha256,'driver_sha256':DRIVER_SHA,
             'certificate_registry':r.get('certificate_registry')},'tail production readiness')

    def fresh_gates(self):
        out=super().fresh_gates()
        out['certificate_policy']=self.certificate_policy_gate()
        return out

    def check_cached_certificate(self,entry):
        if entry.get('classification')!='VALID':return
        b=self.mapper.build(entry['theta'])
        self.prelaunch_check(b['spec'])
        p=entry['provenance'];rp=Path(p['result_path'])
        if O.sha256_file(rp)!=p['result_sha256']:raise Error('CERTIFICATE_RESULT_BYTES_CHANGED')
        g=self.certificate_check(b['spec'],'acceptance',result=O.load_json_file(rp,'result'),
                                 call_dir=p['call_dir'])
        if not g['ok']:raise Error('CERTIFICATE_CACHE_REFUSED: '+repr(g['blockers']))

class Cache(OldCache):
    def forward(self,key):
        entry=self.entries.get(key)
        if entry is not None:self.ctx.check_cached_certificate(entry)
        return super().forward(key)

    def _verify_impl(self,e,stem):
        super()._verify_impl(e,stem)
        self.ctx.check_cached_certificate(e)

    def put(self,*,key,theta,classification,failure_class,source,provenance,forward):
        self.ctx.check_cached_certificate(dict(theta=theta,classification=classification,provenance=provenance))
        return super().put(key=key,theta=theta,classification=classification,failure_class=failure_class,
                           source=source,provenance=provenance,forward=forward)

class CampaignExecutor(OldExecutor):
    def classify(self,plan_call,rec):
        cls,code,fwd,prov=super().classify(plan_call,rec)
        if cls!='VALID':return cls,code,fwd,prov
        try:
            res=O.load_json_file(prov['result_path'],'result')
            g=self.ctx.certificate_check(plan_call['spec'],'acceptance',result=res,call_dir=prov['call_dir'])
            prov['tail_certificates']=g
            if not g['ok']:return 'INFRA','CERTIFICATE_ACCEPTANCE_REFUSED: '+repr(g['blockers']),None,prov
            return cls,code,fwd,prov
        except (Error,OSError,ValueError,KeyError,TypeError) as exc:
            return 'INFRA','CERTIFICATE_ACCEPTANCE_REFUSED: '+str(exc),None,prov

O.Cache=Cache
O.CampaignExecutor=CampaignExecutor
O.Context=Context
O.NEVER_INVALID_PREFIXES=O.NEVER_INVALID_PREFIXES+('CERTIFICATE_',)
Orchestrator=O.Orchestrator
def planning_context(config):return Context(config)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('plan','wave'))
    p.add_argument('--config',required=True);p.add_argument('--output',required=True)
    a=p.parse_args()
    try:
        ctx=Context(a.config);orch=Orchestrator(ctx)
        if a.command=='plan':out=orch.plan_only()
        else:
            orch.prepare(create=False)
            out={'status':'OK','probe':orch.probe.run(orch.cache,'probe'),'gates':ctx.gate_report()}
        out.update(execution_note=WAIVER,launches_performed=0,source_status='CANDIDATE_REQUIRES_DISTINCT_REVIEW')
    except (Error,OSError,ValueError,KeyError,TypeError) as exc:
        out={'status':'REFUSED','reasons':[str(exc)],'execution_note':WAIVER,'launches_performed':0}
    O.write_json_x(a.output,out)
    print(json.dumps({'status':out.get('status'),'output':a.output}))
if __name__=='__main__':main()
