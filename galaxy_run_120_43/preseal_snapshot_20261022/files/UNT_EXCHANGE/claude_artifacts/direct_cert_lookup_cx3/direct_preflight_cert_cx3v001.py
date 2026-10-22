"""0828 direct preflight successor: frozen genesis plus pinned non-genesis records.
Only certificate lookup changes. Native C1 policy, custody, proof, sensitivity and
normalization remain. This adapter exposes prelaunch only, no acceptance/launch.
Existing HEADLINE11 admission keeps its original adapter and sources.
"""
import copy
import json
from pathlib import Path
DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'
LOOKUP={'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py', 'sha256': '1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5'}
BASE_ADAPTER={'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py', 'sha256': 'eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1'}

def build(C,config,*,guard,admission):
    SG=guard
    bridge=admission.get('direct_certificate_lookup')
    SG.require(isinstance(bridge,dict) and set(bridge)=={'request','manifest'},'DIRECT_CERT_LOOKUP_BINDING_REQUIRED')
    L=SG.load(LOOKUP,admission,'_direct_cert_lookup')
    SG.require(L.DIRECT_LOOKUP_API=='DIRECT_CERT_LOOKUP_CX2V001','DIRECT_CERT_LOOKUP_API')
    s=L.Snapshot()
    lookup=L.validate(s,bridge['request'])
    manifest=s.doc(bridge['manifest'])
    SG.require(manifest.get('schema')==L.MANIFEST_SCHEMA and manifest.get('request')==bridge['request']
        and manifest.get('generator')==LOOKUP and manifest.get('verification_replayed') is True
        and manifest.get('points_list')==lookup['points_list'] and manifest.get('wave')==lookup['wave'],
        'DIRECT_CERT_MANIFEST_BINDING')
    pts=manifest.get('points')
    SG.require(isinstance(pts,list) and len(pts)==len(lookup['points']),'DIRECT_CERT_MANIFEST_POINTS')
    for actual,expected in zip(pts,lookup['points']):
        want={k:copy.deepcopy(v) for k,v in expected.items() if k not in ('raw','sha256')}
        SG.require(isinstance(actual,dict) and set(actual)==set(want)|{'spec'},'DIRECT_CERT_MANIFEST_POINT_FIELDS')
        SG.require({k:v for k,v in actual.items() if k!='spec'}==want,'DIRECT_CERT_MANIFEST_POINT_MISMATCH')
        SG.require(s.read(actual['spec'])==expected['raw'] and actual['spec']['sha256']==expected['sha256'],
            'DIRECT_CERT_FINAL_SPEC_BYTES')
    frozen=s.doc(L.C1)['tail_readiness']
    for field in ('certificate_registry','certificate_policy_review','approved_certificate_producers',
                  'custody_deriver','state_enumerator'):
        SG.require(config.get('tail_readiness',{}).get(field)==frozen[field],'DIRECT_CERT_C1_POLICY_MISMATCH')
    original=SG.load(BASE_ADAPTER,admission,'_direct_preflight_original')
    with s.reads():
        base=original.build(C,config,guard=SG,admission=admission)
    O=C.O;M=C.M;G=C.G;Error=C.Error;DRIVER_SHA=C.DRIVER_SHA
    validate_block=C.validate_block;point_identity=C.point_identity
    genesis=s.doc(L.GENESIS)['points']
    extra={p['key']:p for p in lookup['points']}
    class DirectNonGenesisContext(type(base)):
        def _direct_certificate_record(self,ident,spec):
            key=L.digest(ident)
            if key in genesis:
                return copy.deepcopy(genesis[key])
            p=extra.get(key)
            if p is None:
                return None
            SG.require(L.json_bytes(spec)==p['raw'],'DIRECT_CERT_SPEC_NOT_EXACT_FINAL')
            return copy.deepcopy(p['record'])
        def certificate_policy_gate(self):
            with s.reads():
                return super().certificate_policy_gate()
        def sensitivity_gate(self,spec):
            with s.reads():
                return super().sensitivity_gate(spec)
        def prelaunch_check(self,spec,recovery=False):
            with s.reads():
                return super().prelaunch_check(spec,recovery=recovery)
        def certificate_check(self,spec,phase,*,result=None,call_dir=None,_handoff=None):
            if phase!='prelaunch':
                return {'ok':False,'blockers':['DIRECT_CERT_PREFLIGHT_ONLY']}
            with s.reads():
                return self._certificate_check_snapshot(spec,phase,result=result,call_dir=call_dir,_handoff=_handoff)
        def _certificate_check_snapshot(self,spec,phase,*,result=None,call_dir=None,_handoff=None):
            validate_block(spec['numerics'])
            gate=self.certificate_policy_gate()
            if not gate['ok']:return {'ok':False,'blockers':gate['reasons']}
            if phase not in ('prelaunch','acceptance'):return {'ok':False,'blockers':['UNKNOWN_CERTIFICATE_PHASE']}
            if spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc'] != self.numerics['uv_tail']['outer']['K_big_inverse_kpc']:
                return {'ok':False,'blockers':['CERTIFICATE_BLOCK_K_MISMATCH']}
            r=self.cfg['tail_readiness'];ident=point_identity(spec)
            rec=self._direct_certificate_record(ident,spec)
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

    ctx=object.__new__(DirectNonGenesisContext)
    ctx.__dict__.update(base.__dict__)
    return ctx
