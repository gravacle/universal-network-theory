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
import copy
import hashlib
import importlib.util
import json
import re
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

M=load(HERE/'calibration_core_cx2v006r10_c4.py','_cx2v006r1',expected='dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')
O=M.O
S=load(HERE.parent/'v006r8/sensitivity_policy_cx2v006r8_v002.py','_cx2r7_sensitivity',expected='8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f')
G=load(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py'),'_cx2certguard',expected='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677')
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
# c2v003 (Claude2 h3_campaign_path_c2; V006 A192 items 2-3; CAMPAIGN_CERT_DESIGN_MAP_C2V001 sections 3.3 and 5): the q5b1
# wrapper 7a6af535 plus the two blocks marked c2v003 below, and nothing else.  The core is untouched: the mapper is re-patched
# here, the way the core patches the parent's.  No physics value, threshold or reading changes.
#  L1 R-C8 certificate ledger (Claude4 ROOT_ITEMS_FINAL_C4V004 L263-269).  tail_readiness.certificate_ledger = {schema
#     LEDGER_SCHEMA, path <work_dir>/CERTIFICATE_LEDGER.jsonl} carries no head sha, so the cache id (Context.__init__ below),
#     the policy gate, the adoption binding and the gate digest do not move as the ledger grows; the policy review binds it.
#     One lookup, certificate_record = genesis registry U ledger, used by the mapper, certificate_check and write_acceptance
#     (and by the c2v003 acceptance step).  The ledger is append-only and hash-chained from a genesis digest of {registry
#     pin, ledger policy}; a key already in the genesis or earlier in the ledger is refused; every entry's bundle passes the
#     b1 guard's prelaunch check whenever the ledger is read, and the full prelaunch_check (the check a genesis record gets at
#     plan) at append (Orchestrator.ledger_append, under the work-dir lock) and at every use.  A defective ledger closes the
#     certificate policy gate.  Without tail_readiness.certificate_ledger the lookup is the genesis registry alone (q5b1).
#  F6 certified MODEL_INVALID (V006 A192 item 3).  Orchestrator.reingest_invalid caches a call MODEL_INVALID only from the
#     adopted handoff's record (acceptance_q2 v004, A158) of THIS call reading NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT
#     (rows_are_model_output false), with its FINISHED receipt and its registered point; no forward call.  Cache source
#     TAIL_ACCEPTANCE_CERTIFIED, re-verified from bytes at every put, open and reuse.  resolve --decision invalid stays
#     disabled; every other reading stays a halt for root.
LEDGER_SCHEMA='DDO154_CERTIFICATE_LEDGER_C2V003'
LEDGER_ENTRY_SCHEMA='DDO154_CERTIFICATE_LEDGER_ENTRY_C2V003'
LEDGER_NAME='CERTIFICATE_LEDGER.jsonl'
LEDGER_RECORD_KEYS=('identity','bundle','eps_certificate','lo_certificate')
ACCEPTANCE_HANDOFF={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
                    'sha256':'5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}
ACCEPTANCE_RECORD_SCHEMA='DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'
TAIL_INVALID_SOURCE='TAIL_ACCEPTANCE_CERTIFIED'
TAIL_INVALID_READINGS=('NON_LAPSE_TAIL_MATERIAL','BOUND_INSUFFICIENT')
TAIL_INVALID_RULE='V006_A192_F6_CERTIFIED_MODEL_INVALID'
# c2v004 (Claude2; V006 A192 item 3: INCOMPLETE reruns once and failure readings are frozen; verifier B1, ADV rows C03 and
# C04): the c2v003 source 5ea1780a plus the lines marked c2v004 B1, and nothing else.  One more q5b1 line is replaced (the
# reingest signature).  No physics value, threshold or reading changes.
#  B1  An acceptance pass is one ACCEPTANCE_TAILSTATES_C2V002_A<nnn> directory the adopted handoff makes in the call dir
#      (v004 L90, L219-233; a pass that refuses before its state export makes none).  A record is of the call's LATEST pass
#      when its tailstate_dir is the highest-numbered one.  The passes must be A001..A<n> with no gap (the handoff takes the
#      first free number, so then the highest is the newest); a gap or any other ACCEPTANCE_TAILSTATES_* entry refuses.
#      reingest_invalid (and every put, open and reuse of its entry) refuses a record that is not of the latest pass, and
#      refuses while the call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json (written only by the VALID reingest of an ACCEPTED
#      pass).  The VALID reingest takes the record and refuses, under the work-dir lock and before anything is written, a
#      record that is not of the latest pass.  The c2v004 acceptance step allows a second pass only after a first pass read
#      INCOMPLETE, and never a third.
TAILSTATES_PREFIX='ACCEPTANCE_TAILSTATES_'
TAILSTATES_RE=re.compile(r'ACCEPTANCE_TAILSTATES_C2V002_A([0-9]{3})')       # c2v004 B1: handoff v004 L90-91 (A%03d, <= 999)

def is_exact_pin(x):
    return isinstance(x,dict) and set(x)=={'path','sha256'} and isinstance(x['path'],str) and isinstance(x['sha256'],str)

def tail_invalid_forward(reading,record_ref):
    """c2v003 F6: the engine-facing forward record of a certified tail-acceptance MODEL_INVALID (a pure function)."""
    return {'valid':False,'speeds_km_s':{},
            'reasons':['MODEL_INVALID TAIL_ACCEPTANCE_%s (V006 A192 F6; acceptance_q2 v004 record %s; no forward call; '
                       'the rows are not model output)'%(reading,record_ref['sha256'][:16])]}

def acceptance_passes(call_dir):
    """c2v004 B1: the handoff's acceptance passes in a call dir, oldest first (names).  Error on any other
    ACCEPTANCE_TAILSTATES_* entry (not a plain directory of the handoff's name) and on a gap in A001..A<n>."""
    out=[]
    for p in Path(call_dir).iterdir():
        if p.name.startswith(TAILSTATES_PREFIX):
            m=TAILSTATES_RE.fullmatch(p.name)
            if m is None or p.is_symlink() or not p.is_dir():raise Error('ACCEPTANCE_PASS_ENTRY_UNRECOGNISED: '+p.name)
            out.append((int(m.group(1)),p.name))
    out.sort()
    if [n for n,_ in out]!=list(range(1,len(out)+1)):
        raise Error('ACCEPTANCE_PASSES_NOT_CONTIGUOUS: %s (the handoff numbers passes A001, A002, ...)'%[x for _,x in out])
    return [x for _,x in out]

def latest_pass_problems(call_dir,acc,tag):
    """c2v004 B1: [] iff the acceptance record acc is of the call's latest acceptance pass (its tailstate_dir)."""
    here=Path(call_dir).resolve()
    try:passes=acceptance_passes(here)
    except (Error,OSError) as exc:return ['%s_ACCEPTANCE_PASSES_UNREADABLE: %s'%(tag,exc)]
    got=acc.get('tailstate_dir') if isinstance(acc,dict) else None
    if not passes or got!=str(here/passes[-1]):
        return ['%s_RECORD_NOT_THE_LATEST_PASS: record pass %s; the call dir holds %d passes, latest %s'
                %(tag,got,len(passes),passes[-1] if passes else None)]
    return []

def reingest_record_problems(call_dir,acceptance_ref):
    """c2v004 B1: the VALID reingest's acceptance record must be an absolute exact pin of the call's latest pass."""
    if not is_exact_pin(acceptance_ref) or not os.path.isabs(acceptance_ref['path']):
        return ['REINGEST_ACCEPTANCE_RECORD_REQUIRED: an absolute {path, sha256} of the latest acceptance pass']
    acc=json.loads(O.read_pinned(acceptance_ref,'acceptance record'))
    return latest_pass_problems(call_dir,acc,'REINGEST')

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
        bad=self.ledger_policy_problems()                                    # c2v003 L1
        if bad:return M.gate_pending(bad[0])
        try:
            for k in required:O.read_pinned(r[k],k)
            for p in producers:O.read_pinned(p,'approved certificate producer')
            g=M.checked_gate(r['certificate_policy_review'],POLICY_SCHEMA,
                {'driver_sha256':DRIVER_SHA,'custody_deriver':r['custody_deriver'],
                 'state_enumerator':r['state_enumerator'],'approved_certificate_producers':producers,
                 'guard_sha256':O.sha256_file(G.__file__),
                 'driver_slot_rule':'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',
                 'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001',
                 'certificate_ledger':r.get('certificate_ledger')},'certificate policy review')      # c2v003 L1
            if g['ok']:self.ledger_entries()                                # c2v003 L1: a defective ledger closes the gate
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
        try:rec=self.certificate_record(ident)                               # c2v003 L1: genesis U ledger
        except (Error,OSError,ValueError,KeyError,TypeError) as exc:return {'ok':False,'blockers':['CERTIFICATE_LOOKUP: '+str(exc)]}
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
            for slot,gate_name in (('eps_certificate','EPS'),('lo_certificate','LO_RHO_SLOT')):
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
                if gate_name=='LO_RHO_SLOT':
                    # A134 Q5: the lo slot is the point's registered rho record. Its proof never carries
                    # covers_all_consumed_states: LO is decided per consumed state at post-run acceptance.
                    if 'covers_all_consumed_states' in proof:
                        raise Error('LO_RHO_SLOT proof carries covers_all_consumed_states; the prelaunch LO envelope is retired (A134 Q1/Q5)')
                    if slots[slot]!=rec.get('lo_certificate'):
                        raise Error('lo slot is not the registered rho record of this point')
                    rho=M.pin_doc(slots[slot],'registered rho record')
                    if (rho.get('schema')!='UNT_POINT_RHO_NUMERICAL_CX2V001' or rho.get('gate')!='RHO_G'
                            or rho.get('point_sha256')!=M.digest(ident) or rho.get('custody')!=custody
                            or rho.get('settings')!='registered' or rho.get('full_registered_search_executed') is not True
                            or rho.get('coverage_complete') is not True):
                        raise Error('lo slot is not the full registered rho record of this point')
                    if phase=='acceptance':
                        # A134 Q5: the rho recomputed for every consumed state must equal the slot rho bitwise:
                        # identical canonical JSON over the rho content and scope (floats round-trip exactly).
                        # Run metadata (utc, seconds, peak_rss_bytes) and provenance pins are not compared.
                        keys=('schema','gate','identity','point_sha256','custody','settings','coverage_complete',
                              'required_coverage_inverse_kpc','full_registered_search_executed','shells')
                        want=M.canonical({k:rho.get(k) for k in keys})
                        rows=bundle.get('states')
                        if not isinstance(rows,list) or not rows:
                            raise Error('acceptance requires per-state LO proofs')
                        for row in rows:
                            lo=M.pin_doc(row['LO'],'per-state LO proof')
                            evidence=M.pin_doc(lo['core_record'],'per-state LO numeric record')
                            if (evidence.get('schema')!='UNT_POINT_LO_NUMERICAL_CX2V001' or evidence.get('kind')!='CURRENT_SAVED_STATE'
                                    or evidence.get('state')!=lo.get('state') or lo.get('state')!=row.get('state')):
                                raise Error('per-state LO record is not the acceptance record of this state')
                            got=evidence.get('rho')
                            if not isinstance(got,dict) or M.canonical({k:got.get(k) for k in keys})!=want:
                                raise Error('recomputed rho differs from the lo slot rho (bitwise)')
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
        rec=self.certificate_record(point_identity(spec))                    # c2v003 L1: genesis U ledger
        if not isinstance(rec,dict):raise Error('CERTIFICATE_POINT_MISSING_OR_MISMATCHED')
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
        if entry.get('source')==TAIL_INVALID_SOURCE:return self.check_tail_invalid(entry)   # c2v003 F6
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

    # ---------------------------------------------------------------- c2v003 L1: the R-C8 certificate ledger
    def ledger_policy_problems(self):
        r=self.cfg['tail_readiness'];led=r.get('certificate_ledger')
        if led is None:return []
        want={'schema':LEDGER_SCHEMA,'path':str(self.work_dir/LEDGER_NAME)}
        if led!=want:return ['CERTIFICATE_LEDGER_POLICY: tail_readiness.certificate_ledger must be %r'%(want,)]
        if not isinstance(r.get('certificate_registry'),dict):return ['CERTIFICATE_LEDGER_WITHOUT_GENESIS_REGISTRY']
        return []

    def ledger_genesis_sha256(self):
        r=self.cfg['tail_readiness']
        return M.digest({'schema':LEDGER_SCHEMA+'_GENESIS','certificate_registry':r['certificate_registry'],
                         'certificate_ledger':r['certificate_ledger']})

    def genesis_points(self):
        pts=M.pin_doc(self.cfg['tail_readiness']['certificate_registry'],'certificate registry').get('points',{})
        if not isinstance(pts,dict):raise Error('certificate registry points must be an object')
        return pts

    def ledger_record_problems(self,rec):
        """A ledger record's structure and the b1 guard's prelaunch check of its bundle (custody as the bundle states it;
        certificate_check re-derives custody from the spec at append and at every use).  [] when it passes."""
        try:
            if not isinstance(rec,dict) or set(rec)!=set(LEDGER_RECORD_KEYS):
                return ['record keys must be exactly %s'%(LEDGER_RECORD_KEYS,)]
            if not all(is_exact_pin(rec[k]) for k in ('bundle','eps_certificate','lo_certificate')):
                return ['record bundle and slots must be exact {path, sha256} pins']
            ident=rec['identity']
            if not isinstance(ident,dict) or ident.get('driver_sha256')!=DRIVER_SHA:
                return ['record identity is not of the pinned driver']
            bundle=M.pin_doc(rec['bundle'],'ledger point bundle')
            if bundle.get('identity')!=ident:return ['bundle identity differs from the record identity']
            if bundle.get('driver_certificate_bindings')!={k:rec[k] for k in ('eps_certificate','lo_certificate')}:
                return ['bundle does not bind the record slots']
            producers=self.cfg['tail_readiness'].get('approved_certificate_producers')
            if not isinstance(producers,list) or not producers:return ['approved_certificate_producers pending']
            g=G.verify_bundle(rec['bundle'],ident,expected_custody=bundle.get('custody'),
                              approved_producer_sha256=[p['sha256'] for p in producers],phase='prelaunch',required_states=[])
            return [] if g.get('ok') is True else ['b1 guard: '+'; '.join(str(x) for x in g.get('blockers') or ['refused'])]
        except (Error,OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
            return [type(exc).__name__+': '+str(exc)]

    def ledger_entries(self):
        """The verified ledger: [] without a configured ledger or before its first append.  Error on any defect."""
        r=self.cfg['tail_readiness']
        if r.get('certificate_ledger') is None:return []
        bad=self.ledger_policy_problems()
        if bad:raise Error(bad[0])
        p=Path(r['certificate_ledger']['path'])
        if not p.exists():return []
        raw=p.read_bytes();h=O.sha256_bytes(raw)
        hit=getattr(self,'_ledger_verified',None)
        if hit is not None and hit[0]==h:return hit[1]
        if raw and not raw.endswith(b'\n'):raise Error('CERTIFICATE_LEDGER_TORN: the last line has no newline')
        genesis=self.genesis_points();prev=self.ledger_genesis_sha256();seen=set();out=[]
        for i,line in enumerate(raw.split(b'\n')[:-1] if raw else []):
            where='line %d'%(i+1)
            try:e=json.loads(line)
            except ValueError:raise Error('CERTIFICATE_LEDGER_UNREADABLE: '+where)
            if not isinstance(e,dict) or M.canonical(e)!=line:raise Error('CERTIFICATE_LEDGER_NOT_CANONICAL: '+where)
            if e.get('schema')!=LEDGER_ENTRY_SCHEMA or e.get('seq')!=i+1:raise Error('CERTIFICATE_LEDGER_SCHEMA_OR_SEQ: '+where)
            if e.get('prev_sha256')!=prev:raise Error('CERTIFICATE_LEDGER_CHAIN_BREAK: '+where)
            if M.digest({k:v for k,v in e.items() if k!='entry_sha256'})!=e.get('entry_sha256'):
                raise Error('CERTIFICATE_LEDGER_ENTRY_HASH: '+where)
            rec=e.get('record')
            if not isinstance(rec,dict) or not isinstance(rec.get('identity'),dict) or M.digest(rec['identity'])!=e.get('key'):
                raise Error('CERTIFICATE_LEDGER_KEY_IS_NOT_THE_IDENTITY_DIGEST: '+where)
            if e['key'] in genesis or e['key'] in seen:raise Error('CERTIFICATE_LEDGER_KEY_ALREADY_REGISTERED: '+where)
            bad=self.ledger_record_problems(rec)
            if bad:raise Error('CERTIFICATE_LEDGER_ENTRY_INVALID: %s: %s'%(where,bad))
            seen.add(e['key']);out.append(e);prev=e['entry_sha256']
        self._ledger_verified=(h,out)
        return out

    def ledger_head(self):
        e=self.ledger_entries()
        configured=self.cfg['tail_readiness'].get('certificate_ledger') is not None
        return {'configured':configured,'n_entries':len(e),'head_sha256':e[-1]['entry_sha256'] if e else None,
                'genesis_sha256':self.ledger_genesis_sha256() if configured else None}

    def certificate_record(self,ident):
        """The one lookup (V006 A192 F5): the genesis registry, then the append-time candidates, then the ledger."""
        key=M.digest(ident)
        rec=self.genesis_points().get(key)
        if rec is not None:return rec
        cand=getattr(self,'_ledger_candidates',None) or {}
        if key in cand:return cand[key]
        for e in self.ledger_entries():
            if e['key']==key:return e['record']
        return None

    # ---------------------------------------------------------------- c2v003 F6: certified MODEL_INVALID
    def tail_invalid_problems(self,spec,spec_sha256,call_dir,acceptance_ref,rec):
        """-> (problems, record).  [] iff acceptance_ref is the adopted handoff's record of THIS call (its directory, its
        FINISHED receipt and result, its registered point) reading NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT."""
        if not is_exact_pin(acceptance_ref) or not os.path.isabs(acceptance_ref['path']):
            return ['TAIL_INVALID_RECORD_PIN_REQUIRED: an absolute {path, sha256}'],None
        acc=json.loads(O.read_pinned(acceptance_ref,'tail acceptance record'))
        if not isinstance(acc,dict):return ['TAIL_INVALID_RECORD_SCHEMA: not an object'],None
        bad=[]
        if acc.get('schema')!=ACCEPTANCE_RECORD_SCHEMA:bad.append('TAIL_INVALID_RECORD_SCHEMA: %r'%(acc.get('schema'),))
        if acc.get('handoff')!=ACCEPTANCE_HANDOFF:bad.append('TAIL_INVALID_HANDOFF_NOT_A158: %r'%(acc.get('handoff'),))
        if (acc.get('reading') not in TAIL_INVALID_READINGS or acc.get('rows_are_model_output') is not False
                or acc.get('outputs_are_evidence') is not False or acc.get('step4_stop_for_root_ruling') is not False):
            bad.append('TAIL_INVALID_READING_NOT_CERTIFIABLE: reading %r, rows_are_model_output %r, outputs_are_evidence %r, '
                       'step4 stop %r'%(acc.get('reading'),acc.get('rows_are_model_output'),acc.get('outputs_are_evidence'),
                                        acc.get('step4_stop_for_root_ruling')))
        here=Path(call_dir).resolve()
        if acc.get('call_dir')!=str(here):bad.append('TAIL_INVALID_RECORD_OTHER_CALL: record %s; this call %s'%(acc.get('call_dir'),here))
        if os.path.lexists(here/'TAIL_CERTIFICATE_ACCEPTANCE.json'):                                   # c2v004 B1
            bad.append('TAIL_INVALID_CALL_HOLDS_TAIL_CERTIFICATE_ACCEPTANCE: an ACCEPTED pass of this call was reingested')
        bad+=latest_pass_problems(here,acc,'TAIL_INVALID')                                               # c2v004 B1
        sp=here/'spec.json'
        if not sp.is_file() or O.sha256_file(sp)!=spec_sha256 or O.load_json_file(sp,'campaign spec')!=spec:
            bad.append('TAIL_INVALID_SPEC_NOT_THE_PLANNED_SPEC')
        rp,res=here/'RECEIPT.json',(here/'out'/'result.json').resolve()
        if not rp.is_file():
            bad.append('TAIL_INVALID_RECEIPT_NOT_FINISHED: no RECEIPT.json')
        else:
            v=self.M.verify_receipt(rp,spec_sha256=spec_sha256,driver_sha256=DRIVER_SHA)
            rc=v.get('receipt') or {}
            rsha=(rc.get('result') or {}).get('sha256')
            if not v.get('ok') or rc.get('status')!='FINISHED' or rc.get('driver_status')!='COMPLETED':
                bad.append('TAIL_INVALID_RECEIPT_NOT_FINISHED: %s/%s, verifies %s'%(rc.get('status'),rc.get('driver_status'),v.get('ok')))
            if acc.get('result')!={'path':str(res),'sha256':rsha} or not res.is_file() or O.sha256_file(res)!=rsha:
                bad.append('TAIL_INVALID_RECORD_OTHER_RECEIPT')
            else:
                result=O.load_json_file(res,'result')
                if result.get('call_spec_sha256')!=spec_sha256 or result.get('driver_sha256')!=DRIVER_SHA:
                    bad.append('TAIL_INVALID_RESULT_NOT_BOUND_TO_SPEC_OR_DRIVER')
                _,why=O.finish_binding(res,rsha)
                if why:bad.append('TAIL_INVALID_'+why)
        ident=point_identity(spec)
        if acc.get('point_sha256')!=M.digest(ident):bad.append('TAIL_INVALID_RECORD_OTHER_POINT')
        if not isinstance(rec,dict) or rec.get('identity')!=ident:bad.append('TAIL_INVALID_POINT_NOT_REGISTERED')
        r=self.cfg['tail_readiness'];pins=acc.get('pins') if isinstance(acc.get('pins'),dict) else {}
        if pins.get('enumerator')!=r.get('state_enumerator'):bad.append('TAIL_INVALID_ENUMERATOR_NOT_THE_CONFIG_ENUMERATOR')
        if (pins.get('guard') or {}).get('sha256')!=O.sha256_file(G.__file__):bad.append('TAIL_INVALID_GUARD_NOT_THE_WRAPPER_GUARD')
        return bad,acc

    def check_tail_invalid(self,entry):
        """Every put, open and reuse of a TAIL_ACCEPTANCE_CERTIFIED entry: reingest_invalid's checks again, from bytes."""
        p=entry.get('provenance') if isinstance(entry.get('provenance'),dict) else {}
        ta=p.get('tail_acceptance') if isinstance(p.get('tail_acceptance'),dict) else {}
        reading=ta.get('reading')
        if (entry.get('classification')!='MODEL_INVALID' or reading not in TAIL_INVALID_READINGS
                or entry.get('failure_class')!='TAIL_ACCEPTANCE_'+str(reading) or ta.get('rule')!=TAIL_INVALID_RULE
                or not is_exact_pin(ta.get('record'))):
            raise Error('CERTIFICATE_TAIL_INVALID_ENTRY_MALFORMED')
        if O.canonical(entry.get('forward'))!=O.canonical(tail_invalid_forward(reading,ta['record'])):
            raise Error('CERTIFICATE_TAIL_INVALID_FORWARD_NOT_DERIVED')
        b=self.mapper.build(entry['theta'])
        self.prelaunch_check(b['spec'])
        if b['sha256']!=p.get('spec_sha256'):raise Error('CERTIFICATE_TAIL_INVALID_SPEC_MISMATCH')
        rec=self.certificate_record(point_identity(b['spec']))
        bad,acc=self.tail_invalid_problems(b['spec'],b['sha256'],p.get('call_dir'),ta['record'],rec)
        if acc is not None and acc.get('reading')!=reading:bad.append('TAIL_INVALID_READING_DIFFERS_FROM_THE_RECORD')
        if acc is not None and acc.get('result')!={'path':p.get('result_path'),'sha256':p.get('result_sha256')}:
            bad.append('TAIL_INVALID_RESULT_PIN_DIFFERS_FROM_THE_RECORD')
        if not isinstance(rec,dict) or rec.get('bundle')!=ta.get('registered_bundle'):
            bad.append('TAIL_INVALID_REGISTERED_BUNDLE_CHANGED')
        if bad:raise Error('CERTIFICATE_TAIL_INVALID_REFUSED: '+repr(bad))

    def verify_tail_invalid_entry(self,e,stem):
        """Cache._verify_impl for source TAIL_ACCEPTANCE_CERTIFIED: the parent's generic entry checks, then check_tail_invalid."""
        body={k:v for k,v in e.items() if k!='entry_sha256'}
        if O.sha256_bytes(O.canonical(body))!=e.get('entry_sha256'):raise Error('cache entry %s self-hash mismatch'%stem)
        if e.get('schema')!=O.SCHEMA_CACHE_ENTRY or e.get('cache_id')!=self.cache_id or e.get('key')!=stem:
            raise Error('cache entry %s does not belong to this cache'%stem)
        if O.theta_key(e['theta'])!=e['key']:raise Error('cache entry %s key does not hash its theta'%stem)
        self.check_tail_invalid(e)

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
        if isinstance(e,dict) and e.get('source')==TAIL_INVALID_SOURCE:     # c2v003 F6: not a WAVE entry
            self.ctx.verify_tail_invalid_entry(e,stem)
            return
        super()._verify_impl(e,stem)
        self.ctx.check_cached_certificate(e)

    def put(self,*,key,theta,classification,failure_class,source,provenance,forward):
        self.ctx.check_cached_certificate(dict(theta=theta,classification=classification,provenance=provenance,
                                               source=source,failure_class=failure_class,forward=forward))  # c2v003: + source
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

OldMapper=O.Mapper
class Mapper(OldMapper):
    """c2v003 L1: the core mapper plus the ledger.  A point the genesis registry lacks gets its slots from its verified
    ledger record (the fill of core L256-259); raw, sha256 and changed_paths are then recomputed as core L261-263."""
    def build(self,theta,recovery=None):
        built=super().build(theta,recovery=recovery)
        ctx=self.ctx;r=ctx.cfg['tail_readiness']
        if r.get('certificate_registry') is None or r.get('certificate_ledger') is None or not hasattr(ctx,'certificate_record'):
            return built
        if built['certificate_point_key'] in ctx.genesis_points():return built
        rec=ctx.certificate_record(built['certificate_identity'])
        if rec is None:return built
        if rec.get('identity')!=built['certificate_identity']:raise Error('certificate identity collision/mismatch')
        spec=built['spec']
        for field in ('eps_certificate','lo_certificate'):
            ref=rec[field]
            O.read_pinned(ref,field)
            spec['numerics']['uv_tail'][field]=copy.deepcopy(ref)
        raw=O.json_bytes(spec)
        built.update(raw=raw,sha256=O.sha256_bytes(raw),changed_paths=O.diff_paths(ctx.base,spec))
        return built

O.DECLARED_CHANGED_PATHS=O.DECLARED_CHANGED_PATHS+tuple('numerics.uv_tail.'+slot+'.'+leaf for slot in ('eps_certificate','lo_certificate') for leaf in ('path','sha256'))
O.Mapper=Mapper                                                             # c2v003 L1
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

    def reingest(self,wave,call_index,bundle_ref,acceptance_ref=None):       # c2v004 B1: + the acceptance record
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
            bad=reingest_record_problems(directory,acceptance_ref)            # c2v004 B1: under the lock, before any write
            if bad:raise Error('REINGEST_RECORD_REFUSED: '+repr(bad))
            self.ctx.write_acceptance(directory,bundle_ref)
            cls,code,fwd,prov=self.executor.classify(c,{'call_dir':str(directory),'status':'OK'})
            if cls not in O.CACHED_CLASSES:raise Error('REINGEST_REFUSED: '+str(code))
            prov.update(wave=int(wave),call_index=int(call_index),recovery=c.get('recovery'),authorized_by=c.get('authorized_by'))
            _,new=self.cache.put(key=c['key'],theta=c['theta'],classification=cls,failure_class=code,source='WAVE',provenance=prov,forward=fwd)
            return {'status':'OK','classification':cls,'new_cache_entry':new,'launches_performed':0,
                    'wave':int(wave),'call_index':int(call_index),'tail_certificates':prov['tail_certificates']}
        finally:lock.release()

    # ---------------------------------------------------------------- c2v003 F6 and L1
    def reingest_invalid(self,wave,call_index,acceptance_ref):
        """V006 A192 item 3: certified MODEL_INVALID from the call's own acceptance_q2 v004 record reading
        NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT.  No solver call.  Root's act, call by call."""
        lock=O.Lock(self.ctx.work_dir)
        if not lock.acquire():return {'status':'LOCKED'}
        try:
            self.prepare(create=False)
            bad=self.check_identity_now()
            if bad:raise Error('REINGEST_INVALID_IDENTITY: '+repr(bad))
            wd=self.waves_dir/('wave_%04d'%int(wave))
            plan=O.load_json_file(wd/'WAVE_PLAN.json','wave plan')
            if plan.get('cache_id')!=self.ctx.cache_id:raise Error('REINGEST_INVALID_CACHE_ID_MISMATCH')
            calls=[c for c in plan['calls'] if c['call_index']==int(call_index)]
            if len(calls)!=1:raise Error('REINGEST_INVALID_CALL_INDEX_REQUIRED')
            c=calls[0];b=self.ctx.mapper.build(c['theta'])
            if b['sha256']!=c['spec_sha256'] or b['spec']!=c['spec']:raise Error('REINGEST_INVALID_SPEC_MISMATCH')
            if c['key'] in self.cache.entries:
                raise Error('REINGEST_INVALID_ALREADY_CACHED: key %s is cached %s'%(c['key'][:16],self.cache.entries[c['key']].get('classification')))
            directory=wd/'campaign'/('call_%04d'%int(call_index))
            rec=self.ctx.certificate_record(point_identity(c['spec']))
            bad,acc=self.ctx.tail_invalid_problems(c['spec'],c['spec_sha256'],directory,acceptance_ref,rec)
            if bad:raise Error('REINGEST_INVALID_REFUSED: '+repr(bad))
            reading=acc['reading'];rp=directory/'RECEIPT.json'
            ref={'path':acceptance_ref['path'],'sha256':acceptance_ref['sha256']}
            prov={'call_dir':str(directory),'spec_sha256':c['spec_sha256'],'wave':int(wave),'call_index':int(call_index),
                  'receipt_path':str(rp),'receipt_file_sha256':O.sha256_file(rp),
                  'result_path':acc['result']['path'],'result_sha256':acc['result']['sha256'],
                  'tail_acceptance':{'record':ref,'reading':reading,'all_readings':acc.get('all_readings'),
                                     'registered_bundle':rec['bundle'],'rule':TAIL_INVALID_RULE,'handoff':ACCEPTANCE_HANDOFF},
                  'taxonomy':{'rule':TAIL_INVALID_RULE,'code':'TAIL_ACCEPTANCE_'+reading,'class':'MODEL_INVALID',
                              'judgment_call':True,'taxonomy_sha256':None,
                              'detail':'root act per call (A192 item 3); recorded as a judgment call, so a run that uses '
                                       'it never meets the D5 TESTED-NEGATIVE condition'},
                  'recovery':c.get('recovery'),'authorized_by':c.get('authorized_by')}
            _,new=self.cache.put(key=c['key'],theta=c['theta'],classification='MODEL_INVALID',
                                 failure_class='TAIL_ACCEPTANCE_'+reading,source=TAIL_INVALID_SOURCE,provenance=prov,
                                 forward=tail_invalid_forward(reading,ref))
            return {'status':'OK','classification':'MODEL_INVALID','failure_class':'TAIL_ACCEPTANCE_'+reading,
                    'new_cache_entry':new,'launches_performed':0,'wave':int(wave),'call_index':int(call_index),
                    'acceptance_record':ref,'registered_bundle':rec['bundle']}
        finally:lock.release()

    def ledger_append(self,items,source):
        """V006 A192 item 2: append certified points to the R-C8 ledger under the work-dir lock (no run may hold it).
        items: [{key, theta, record, wave, pending_spec_sha256}].  Every check runs before one append of all lines."""
        ctx=self.ctx;r=ctx.cfg['tail_readiness']
        if r.get('certificate_ledger') is None:raise Error('LEDGER_NOT_CONFIGURED: tail_readiness.certificate_ledger is null')
        if not ctx.gates_ok():
            raise Error('LEDGER_APPEND_GATES_NOT_PASSED: %s'%sorted(k for k,g in ctx.gates.items() if not g.get('ok')))
        if not isinstance(items,list) or not items:raise Error('LEDGER_APPEND_NOTHING_TO_APPEND')
        if not ctx.work_dir.is_dir():raise Error('LEDGER_APPEND_WORK_DIR_NOT_CREATED (the campaign has not started)')
        lock=O.Lock(ctx.work_dir)
        if not lock.acquire():return {'status':'LOCKED'}
        try:
            if self.check_work_dir_json(False)!='MATCHES':raise Error('LEDGER_APPEND_WORK_DIR_JSON_REQUIRED')
            bad=self.check_identity_now()
            if bad:raise Error('LEDGER_APPEND_IDENTITY: '+repr(bad))
            self.check_plan_cache_ids()
            path=Path(r['certificate_ledger']['path'])
            size0=path.stat().st_size if path.exists() else 0
            ctx._ledger_verified=None
            entries=ctx.ledger_entries()
            known=set(ctx.genesis_points())|{e['key'] for e in entries}
            cand={}
            for it in items:
                if not isinstance(it,dict) or set(it)!={'key','theta','record','wave','pending_spec_sha256'}:
                    raise Error('LEDGER_ITEM_KEYS: {key, theta, record, wave, pending_spec_sha256} required')
                key,rec=it['key'],it['record']
                if key in known or key in cand:raise Error('LEDGER_KEY_ALREADY_REGISTERED: %s'%str(key)[:16])
                if (not isinstance(rec,dict) or set(rec)!=set(LEDGER_RECORD_KEYS) or not isinstance(rec.get('identity'),dict)
                        or M.digest(rec['identity'])!=key):
                    raise Error('LEDGER_RECORD_NOT_THIS_POINT: %s'%str(key)[:16])
                b0=ctx.mapper.build(it['theta'])
                if b0['certificate_point_key']!=key or b0['sha256']!=it['pending_spec_sha256']:
                    raise Error('LEDGER_THETA_OR_PENDING_SPEC_IS_NOT_THIS_POINT: %s'%key[:16])
                bad=ctx.ledger_record_problems(rec)
                if bad:raise Error('LEDGER_RECORD_GUARD_REFUSED: %s: %s'%(key[:16],bad))
                cand[key]=rec
            planned={}
            ctx._ledger_candidates=cand
            try:
                for it in items:
                    b=ctx.mapper.build(it['theta'])
                    ctx.prelaunch_check(b['spec'])         # the certificate_check a genesis record gets at plan
                    planned[it['key']]=b['sha256']
            finally:ctx._ledger_candidates=None
            prev=entries[-1]['entry_sha256'] if entries else ctx.ledger_genesis_sha256()
            seq=len(entries);blob=b''
            for it in items:
                seq+=1
                e={'schema':LEDGER_ENTRY_SCHEMA,'seq':seq,'prev_sha256':prev,'key':it['key'],'record':it['record'],
                   'wave':it['wave'],'planned_spec_sha256':planned[it['key']],'source':source,'appended_utc':O.utc()}
                e['entry_sha256']=M.digest(e)
                blob+=M.canonical(e)+b'\n';prev=e['entry_sha256']
            fd=os.open(str(path),os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o644)
            try:
                if os.fstat(fd).st_size!=size0:raise Error('LEDGER_CHANGED_DURING_APPEND')
                if os.write(fd,blob)!=len(blob):raise Error('LEDGER_SHORT_WRITE (root inspects the last line)')
                os.fsync(fd)
            finally:os.close(fd)
            ctx._ledger_verified=None
            after=ctx.ledger_entries()
            if len(after)!=len(entries)+len(items) or after[-1]['entry_sha256']!=prev:raise Error('LEDGER_REVERIFY_FAILED')
            return {'status':'OK','appended':[{'seq':e['seq'],'key':e['key'],'planned_spec_sha256':e['planned_spec_sha256']}
                                              for e in after[len(entries):]],
                    'n_entries':len(after),'head_sha256':prev,'genesis_sha256':ctx.ledger_genesis_sha256(),
                    'ledger':{'path':str(path),'sha256':O.sha256_file(path)},'launches_performed':0}
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
