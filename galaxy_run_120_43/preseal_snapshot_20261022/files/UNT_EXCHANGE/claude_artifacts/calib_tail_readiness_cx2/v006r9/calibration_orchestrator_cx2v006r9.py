"""v006 r8 (0554): certificate checks at preflight, ingest, cache put and cache reuse.

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
    m=importlib.util.module_from_spec(sp);sys.modules[name]=m
    exec(compile(raw,str(path),'exec'),m.__dict__);return m

M=load(HERE/'calibration_core_cx2v006r9.py','_cx2v006r1',expected='a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605')
O=M.O
S=load(HERE.parent/'v006r8/sensitivity_policy_cx2v006r8_v002.py','_cx2r7_sensitivity',expected='8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f')
G=load(HERE.parent/'certificates_per_point/certificate_guard_cx2v003.py','_cx2certguard',expected='5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f')
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
        cfg = O.load_json_file(config, 'config') if isinstance(config,(str,Path)) else config
        if not isinstance(cfg,dict) or not isinstance(cfg.get('tail_readiness'),dict):
            raise Error('TAIL_READINESS_CONFIG_REQUIRED')
        if cfg.get('driver',{}).get('sha256') != DRIVER_SHA:
            raise Error('v006r9 requires pinned v010 r5')
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
                 'guard_sha256':O.sha256_file(G.__file__),
                 'driver_slot_rule':'POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE',
                 'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'},'certificate policy review')
            return g
        except (Error,ValueError,OSError) as exc:return M.gate_pending(str(exc))

    def certificate_check(self,spec,phase,*,result=None,call_dir=None,_handoff=None):
        validate_block(spec['numerics'])
        gate=self.certificate_policy_gate()
        if not gate['ok']:return {'ok':False,'blockers':gate['reasons']}
        if phase not in ('prelaunch','acceptance'):return {'ok':False,'blockers':['UNKNOWN_CERTIFICATE_PHASE']}
        if spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc'] != self.numerics['uv_tail']['outer']['K_big_inverse_kpc']:
            return {'ok':False,'blockers':['CERTIFICATE_BLOCK_K_MISMATCH']}
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
                directory=Path(call_dir)
                actual_spec=directory/'spec.json'
                archived_spec=directory/'out/inputs/call_spec.json'
                if O.load_json_file(actual_spec,'campaign spec') != spec or O.load_json_file(archived_spec,'archived spec') != spec:
                    raise Error('CERTIFICATE_RESULT_SPEC_CONTENT_MISMATCH')
                if not (O.sha256_file(actual_spec)==O.sha256_file(archived_spec)==result.get('call_spec_sha256')):
                    raise Error('CERTIFICATE_RESULT_SPEC_SHA_MISMATCH')
                if result.get('driver_sha256') != DRIVER_SHA:
                    raise Error('CERTIFICATE_RESULT_DRIVER_MISMATCH')
                if O.load_json_file(directory/'out/result.json','result') != result:
                    raise Error('CERTIFICATE_SUPPLIED_RESULT_DIFFERS_FROM_BYTES')
                fin,why=O.finish_binding(directory/'out/result.json',O.sha256_file(directory/'out/result.json'))
                if why:raise Error('CERTIFICATE_'+why)
                receipt=directory/'RECEIPT.json'
                verified_receipt=self.M.verify_receipt(receipt,spec_sha256=result['call_spec_sha256'],driver_sha256=DRIVER_SHA)
                rc=verified_receipt.get('receipt') or {}
                if not verified_receipt.get('ok') or rc.get('status')!='FINISHED' or rc.get('driver_status')!='COMPLETED' or (rc.get('result') or {}).get('sha256')!=O.sha256_file(directory/'out/result.json'):
                    raise Error('CERTIFICATE_FINISHED_RECEIPT_REQUIRED')
                enum=O.load_pinned_module(r['state_enumerator'],'cx2_cert_states','state enumerator')
                inv=enum.consumed_states(spec=spec,result=result,call_dir=str(call_dir))
                if not isinstance(inv,dict) or inv.get('complete') is not True:
                    return {'ok':False,'blockers':['COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED']}
                states=inv['states']
            bundle_ref=rec['bundle']
            if phase=='acceptance':
                directory=Path(call_dir)
                handoff_path=directory/'TAIL_CERTIFICATE_ACCEPTANCE.json'
                if _handoff is None:
                    handoff_raw=handoff_path.read_bytes()
                    handoff=json.loads(handoff_raw)
                    handoff_pin={'path':str(handoff_path),'sha256':O.sha256_bytes(handoff_raw)}
                else:
                    handoff=_handoff
                    handoff_pin=None
                if handoff.get('schema')!='TAIL_CERTIFICATE_ACCEPTANCE_CX2V001':
                    raise Error('post-state handoff schema mismatch')
                rp=directory/'out/result.json'
                if handoff.get('result_sha256')!=O.sha256_file(rp) or O.load_json_file(rp,'result')!=result:
                    raise Error('post-state handoff/result mismatch')
                if handoff.get('call_spec_sha256')!=result.get('call_spec_sha256'):
                    raise Error('post-state handoff/spec mismatch')
                bundle_ref=handoff['certificate_bundle']
                if handoff.get('prelaunch_bundle')!=rec['bundle']:
                    raise Error('post-state handoff/prelaunch registry lineage mismatch')
            bundle=M.pin_doc(bundle_ref,'point certificate bundle')
            if phase=='acceptance' and bundle_ref!=rec['bundle']:
                prebundle=M.pin_doc(rec['bundle'],'registered prelaunch bundle')
                if bundle.get('parent_prelaunch_bundle')!=rec['bundle'] or bundle.get('prelaunch')!=prebundle.get('prelaunch'):
                    raise Error('post-state bundle does not inherit registered prelaunch proofs')
            slots={k:spec['numerics']['uv_tail'][k] for k in ('eps_certificate','lo_certificate')}
            if bundle.get('driver_certificate_bindings')!=slots:
                raise Error('bundle does not bind the actual driver certificate slots')
            for slot,gate_name in (('eps_certificate','EPS'),('lo_certificate','LO_ENVELOPE')):
                proof=M.pin_doc(bundle['prelaunch'][gate_name],gate_name+' slot proof')
                if proof.get('schema')!=G.PROOF_SCHEMA or proof.get('gate')!=gate_name or proof.get('custody_sha256')!=M.digest(custody):
                    raise Error(gate_name+' proof schema/gate/custody mismatch')
                if proof.get('driver_certificate')!=slots[slot]:
                    raise Error(gate_name+' proof differs from attached driver certificate')
                O.read_pinned(slots[slot],slot)
                if proof.get('point_sha256')!=M.digest(ident) or proof.get('status')!='TESTED' or proof.get('verdict')!='PASS':
                    raise Error(gate_name+' slot proof is not TESTED PASS for this point')
                producer=proof['producer'];O.read_pinned(producer,gate_name+' producer')
                if producer not in r['approved_certificate_producers']:
                    raise Error(gate_name+' producer is not approved')
                if gate_name=='LO_ENVELOPE' and proof.get('covers_all_consumed_states') is not True:
                    raise Error('a reviewed prelaunch LO envelope is required; no anchor substitution')
            verified=G.verify_bundle(bundle_ref,ident,expected_custody=custody,
                approved_producer_sha256=[p['sha256'] for p in r['approved_certificate_producers']],
                phase=phase,required_states=states)
            if phase=='acceptance':
                verified['acceptance_handoff']=handoff_pin
                verified['certificate_bundle']=bundle_ref
            return verified
        except (Error,OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
            return {'ok':False,'blockers':[type(exc).__name__+': '+str(exc)]}

    def prelaunch_check(self,spec,recovery=False):
        validate_block(spec['numerics'])
        sg=self.sensitivity_gate(spec)
        if not sg['ok']:raise Error('SENSITIVITY_DECIDING_III_REQUIRED: '+repr(sg['reasons']))
        normalized=super().prelaunch_check(spec,recovery=recovery)
        # An unfilled plan is inspectable, but cannot pass certificate_policy_gate.
        if self.cfg['tail_readiness'].get('certificate_registry') is not None:
            g=self.certificate_check(spec,'prelaunch')
            if not g['ok']:raise Error('CERTIFICATE_PREFLIGHT: '+repr(g['blockers']))
        return normalized

    def check_adoption(self):
        # Exact v005 C4-6 implementation, fed verified ADOPT_TAIL input bindings.
        g=OldContext.__mro__[1].check_adoption(self)
        if g['ok']:
            d=M.pin_doc(self.cfg['adoption_derivation'],'tail adoption derivation')
            r=self.cfg['tail_readiness']
            want={'driver_sha256':DRIVER_SHA,'certificate_registry':r.get('certificate_registry'),
                  'reading':'ADOPT_TAIL','compare_sha256':self.gates['numerics_verdict']['adopted']['compare_sha256'],
                  'sealed_prereg_sha256':self.gates['numerics_verdict']['adopted']['prereg_sha256']}
            for k,v in want.items():
                if v is None or d.get(k)!=v:g['reasons'].append('TAIL_ADOPTION_BINDING: '+k)
            if not self.gates.get('driver_capability',{}).get('ok'):
                g['reasons'].append('TAIL_ADOPTION_CAPABILITY_NOT_VERIFIED')
            g['ok']=not g['reasons']
        return g

    def sensitivity_gate(self,spec):
        return S.sensitivity_gate(config=self.cfg,spec=spec,core=M)

    def write_acceptance(self,call_dir,bundle_ref):
        """Postrun producer entry point: verify first, exclusive-create handoff, then reverify."""
        directory=Path(call_dir)
        spec=O.load_json_file(directory/'spec.json','campaign spec')
        result=O.load_json_file(directory/'out/result.json','result')
        registry=M.pin_doc(self.cfg['tail_readiness']['certificate_registry'],'registry')
        rec=registry['points'][M.digest(point_identity(spec))]
        handoff={'schema':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001',
                 'result_sha256':O.sha256_file(directory/'out/result.json'),
                 'call_spec_sha256':O.sha256_file(directory/'spec.json'),
                 'certificate_bundle':bundle_ref,'prelaunch_bundle':rec['bundle'],
                 'writer':{'path':__file__,'sha256':O.sha256_file(__file__)}}
        g=self.certificate_check(spec,'acceptance',result=result,call_dir=directory,_handoff=handoff)
        if not g['ok']:raise Error('CERTIFICATE_HANDOFF_NOT_WRITTEN: '+repr(g['blockers']))
        hp=directory/'TAIL_CERTIFICATE_ACCEPTANCE.json'
        if hp.exists():
            if O.load_json_file(hp,'handoff')!=handoff:raise Error('immutable handoff already differs')
        else:O.write_json_x(hp,handoff)
        final=self.certificate_check(spec,'acceptance',result=result,call_dir=directory)
        if not final['ok']:raise Error('CERTIFICATE_HANDOFF_REVERIFY: '+repr(final['blockers']))
        return final

    def fresh_gates(self):
        out=super().fresh_gates()
        out['certificate_policy']=self.certificate_policy_gate()
        return out

    def check_cached_certificate(self,entry):
        if entry.get('classification') not in O.CACHED_CLASSES:return
        if not isinstance(entry.get('provenance'),dict) or not all(k in entry['provenance'] for k in ('result_path','result_sha256','call_dir')):
            raise Error('CERTIFICATE_UNCERTIFIED_CACHEABLE_RESULT')
        b=self.mapper.build(entry['theta'])
        self.prelaunch_check(b['spec'])
        p=entry['provenance'];rp=Path(p['result_path'])
        if O.sha256_file(rp)!=p['result_sha256']:raise Error('CERTIFICATE_RESULT_BYTES_CHANGED')
        g=self.certificate_check(b['spec'],'acceptance',result=O.load_json_file(rp,'result'),
                                 call_dir=p['call_dir'])
        if not g['ok']:raise Error('CERTIFICATE_CACHE_REFUSED: '+repr(g['blockers']))
        previous=p.get('tail_certificates') or {}
        if any(previous.get(k)!=g.get(k) for k in ('acceptance_handoff','certificate_bundle')):
            raise Error('CERTIFICATE_ACCEPTANCE_EVIDENCE_CHANGED')

class CertificateRefusal(BaseException):
    """Escapes engine Exception guards and surfaces as exit 3."""

class Cache(OldCache):
    def forward(self,key):
        entry=self.entries.get(key)
        if entry is not None:
            try:self.ctx.check_cached_certificate(entry)
            except (Error,OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
                raise CertificateRefusal('CERTIFICATE_CACHE_REFUSED: '+str(exc)) from exc
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
        if cls not in O.CACHED_CLASSES:return cls,code,fwd,prov
        try:
            res=O.load_json_file(prov['result_path'],'result')
            g=self.ctx.certificate_check(plan_call['spec'],'acceptance',result=res,call_dir=prov['call_dir'])
            prov['tail_certificates']=g
            if not g['ok']:return 'INFRA','CERTIFICATE_ACCEPTANCE_REFUSED: '+repr(g['blockers']),None,prov
            return cls,code,fwd,prov
        except (Error,OSError,ValueError,KeyError,TypeError) as exc:
            return 'INFRA','CERTIFICATE_ACCEPTANCE_REFUSED: '+str(exc),None,prov

O.DECLARED_CHANGED_PATHS=O.DECLARED_CHANGED_PATHS+tuple('numerics.uv_tail.'+slot+'.'+leaf for slot in ('eps_certificate','lo_certificate') for leaf in ('path','sha256'))
O.Cache=Cache
O.CampaignExecutor=CampaignExecutor
O.Context=Context
O.NEVER_INVALID_PREFIXES=O.NEVER_INVALID_PREFIXES+('CERTIFICATE_',)

_resolve_source='def resolve(self, wave, decision, reason, tokens=None, all_items=False, halt_sha256=None, recovery_path=None):\n    """M2/L5/C11: validated completely before anything is written; cache put succeeds before the RESOLUTIONS commit per item."""\n    ctx = self.ctx\n    if decision not in DECISIONS:\n        raise OrchestratorError(\'decision must be one of %s\' % (DECISIONS,))\n    if not isinstance(reason, str) or not reason.strip():\n        raise OrchestratorError(\'resolve needs a non-empty --reason\')\n    rr = None\n    if decision == \'retry_with_recovery\':\n        if not recovery_path:\n            raise OrchestratorError(\'retry_with_recovery needs --recovery PATH (an allowlisted rule)\')\n        rr = ctx.recovery_rule(recovery_path)\n    elif recovery_path:\n        raise OrchestratorError(\'--recovery is only valid with retry_with_recovery\')\n    if not ctx.work_dir.is_dir():\n        raise OrchestratorError(\'work dir %s does not exist\' % ctx.work_dir)\n    lock = Lock(ctx.work_dir)\n    if not lock.acquire():\n        return {\'status\': \'LOCKED\', \'reason\': \'an orchestrator run holds the lock (L5)\'}\n    try:\n        self.work_dir_json = self.check_work_dir_json(False)                  # F3\n        self.check_plan_cache_ids()                                          # v005 C4-2\n        wd = self.waves_dir / (\'wave_%04d\' % int(wave))\n        hp = wd / \'HALT.json\'\n        if not hp.is_file():\n            raise OrchestratorError(\'wave %s has no HALT.json\' % wave)\n        halt = load_json_file(hp, \'HALT.json\')\n        plan = load_json_file(wd / \'WAVE_PLAN.json\', \'WAVE_PLAN.json\')\n        if plan.get(\'cache_id\') != ctx.cache_id:                             # v005 C4-2\n            raise OrchestratorError(\'C4-2 config changed: use a new work dir (wave %s was planned under cache id %s, \'\n                                    \'this config gives %s)\' % (wave, str(plan.get(\'cache_id\'))[:16], ctx.cache_id[:16]))\n        by_key = {c[\'key\']: c for c in plan[\'calls\']}\n        if all_items:\n            if tokens:\n                raise OrchestratorError(\'use either --token or --all --halt-sha256\')\n            if halt_sha256 != sha256_file(hp):\n                raise OrchestratorError(\'--all needs --halt-sha256 equal to the sha256 of %s\' % hp)\n            items = list(halt[\'items\'])\n        else:\n            if not tokens:\n                raise OrchestratorError(\'resolve needs --token T (repeatable) or --all --halt-sha256 H\')\n            by_tok = {it[\'token\']: it for it in halt[\'items\']}\n            miss = [t for t in tokens if t not in by_tok]\n            if miss:\n                raise OrchestratorError(\'token(s) not in the HALT of wave %s: %s\' % (wave, [t[:16] for t in miss]))\n            if len(set(tokens)) != len(tokens):\n                raise OrchestratorError(\'duplicate --token\')\n            items = [by_tok[t] for t in tokens]\n        self.cache.open(create=True)\n        self.materialize_invalid_resolutions()\n        used = set(ln.get(\'token\') for ln in self.cache.resolutions())\n        last = self.last_launch_wave()\n        problems = []\n        for it in items:\n            if it[\'token\'] in used:\n                problems.append(\'%s: TOKEN_ALREADY_USED\' % it[\'key\'][:16])\n            if last.get(it[\'key\']) != int(wave):\n                problems.append(\'%s: STALE_TOKEN (the key\\\'s latest launch is wave %s)\' % (it[\'key\'][:16], last.get(it[\'key\'])))\n            if it[\'key\'] in self.cache.entries:\n                problems.append(\'%s: ALREADY_CACHED\' % it[\'key\'][:16])\n            if decision == \'invalid\' and ctx.taxonomy.never_invalid_code(it.get(\'reason\')):\n                problems.append(\'%s: INVALID_REFUSED_FOR_%s (C11)\' % (it[\'key\'][:16], str(it.get(\'reason\')).split(\':\')[0]))\n        if problems:\n            raise OrchestratorError(\'resolve refused, nothing written: %s\' % problems)\n        if decision != \'invalid\':\n            for it in items:\n                cd = (it.get(\'provenance\') or {}).get(\'call_dir\')\n                if cd:\n                    procs = live_processes(CampaignExecutor.call_markers(cd))\n                    if procs is None or procs:\n                        raise OrchestratorError(\'F4: live process(es) still reference %s: %s; wait or stop them first\'\n                                                % (cd, procs))\n        done = []\n        for it in items:\n            line = {\'schema\': SCHEMA_RESOLUTION, \'utc\': utc(), \'wave\': int(wave), \'key\': it[\'key\'],\n                    \'token\': it[\'token\'], \'decision\': decision, \'reason\': reason, \'halt_class\': it[\'class\'],\n                    \'halt_reason\': it[\'reason\'], \'cache_id\': ctx.cache_id,           # v005 C4-2\n                    \'config_sha256\': ctx.config_sha256}\n            if rr is not None:\n                line[\'recovery\'] = {\'path\': rr[\'path\'], \'sha256\': rr[\'sha256\'], \'rule_id\': rr[\'rule_id\']}\n            if decision == \'invalid\':\n                ent = resolution_entry(it, line, by_key[it[\'key\']][\'theta\'])\n                self.cache.put(key=it[\'key\'], **ent)\n            append_jsonl(self.resolution_path, line)\n            self.cache._resolutions = None\n            done.append(line)\n        return {\'status\': \'OK\', \'resolved\': done}\n    finally:\n        lock.release()\n'
exec(compile(_resolve_source,__file__,'exec'),O.__dict__)
class Orchestrator(O.Orchestrator):
    def run(self,max_waves=None,new_campaign=False):
        # CertificateRefusal inherits BaseException so the numerical engine cannot
        # turn cache rejection into an ordinary model failure. Catch at run API.
        try:
            return super().run(max_waves=max_waves,new_campaign=new_campaign)
        except CertificateRefusal as exc:
            return {'status':'REFUSED','exit_code':3,'reasons':[str(exc)],
                    'execution_note':WAIVER}

    def resolve(self,wave,decision,reason,tokens=None,all_items=False,
                halt_sha256=None,recovery_path=None):
        # 0540 F4: completed-valid source certificates cannot justify MODEL_INVALID.
        # Refuse before taking a lock or mutating cache/resolution records.
        if decision == 'invalid':
            raise Error('ROOT_INVALID_DISABLED_FOR_TAIL_ON: MODEL_INVALID requires a later certified successor')
        return O.resolve(self,wave,decision,reason,tokens=tokens,all_items=all_items,
                         halt_sha256=halt_sha256,recovery_path=recovery_path)

    def reingest(self,wave,call_index,bundle_ref):
        """No solver call: re-read completed saved result after post-state certificates arrive."""
        lock=O.Lock(self.ctx.work_dir)
        if not lock.acquire():return {'status':'LOCKED'}
        try:
            self.prepare(create=False)
            bad=self.check_identity_now()
            if bad:raise Error('REINGEST_IDENTITY: '+repr(bad))
            wd=self.waves_dir/('wave_%04d'%int(wave))
            plan=O.load_json_file(wd/'WAVE_PLAN.json','wave plan')
            if plan.get('cache_id')!=self.ctx.cache_id:raise Error('REINGEST_CACHE_ID_MISMATCH')
            calls=[c for c in plan['calls'] if c['call_index']==int(call_index)]
            if len(calls)!=1:raise Error('REINGEST_CALL_INDEX_REQUIRED')
            c=calls[0];b=self.ctx.mapper.build(c['theta'])
            if b['sha256']!=c['spec_sha256'] or b['spec']!=c['spec']:raise Error('REINGEST_SPEC_MISMATCH')
            directory=wd/'campaign'/('call_%04d'%int(call_index))
            self.ctx.write_acceptance(directory,bundle_ref)
            cls,code,fwd,prov=self.executor.classify(c,{'call_dir':str(directory),'status':'OK'})
            if cls not in O.CACHED_CLASSES:raise Error('REINGEST_REFUSED: '+str(code))
            prov.update(wave=int(wave),call_index=int(call_index),recovery=c.get('recovery'),authorized_by=c.get('authorized_by'))
            _,new=self.cache.put(key=c['key'],theta=c['theta'],classification=cls,failure_class=code,source='WAVE',provenance=prov,forward=fwd)
            return {'status':'OK','classification':cls,'new_cache_entry':new,'launches_performed':0,
                    'wave':int(wave),'call_index':int(call_index),'tail_certificates':prov['tail_certificates']}
        finally:lock.release()

O.Orchestrator=Orchestrator
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
    except (CertificateRefusal,Error,OSError,ValueError,KeyError,TypeError) as exc:
        out={'status':'REFUSED','reasons':[str(exc)],'execution_note':WAIVER,'launches_performed':0}
    O.write_json_x(a.output,out)
    print(json.dumps({'status':out.get('status'),'output':a.output}))
    return 0 if out.get('status')=='OK' else 3
if __name__=='__main__':sys.exit(main())
