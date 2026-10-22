"""Dispatch 0511 build: v010 r5 calibration adapter over the pinned v005 engine.

No launch command is exposed by this build/review lane. Claude2 may import Context
and Orchestrator after the pending production evidence has been supplied/reviewed.
CLI plan and wave are read-only; output is exclusive-create. The v005 cache,
receipt verification, budget probe, replay, locking and work-volume checks remain.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import contextvars
import copy
import hashlib
import json
import math
import sys
import types
from pathlib import Path

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PARENT = BASE / 'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
PARENT_SHA = 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
WAIVER = 'nice unavailable (sandbox); 0514 waiver'
MODULE_NAME = 'calibration_orchestrator_cx2v006'
HULL = [151250000.0, 317625000.0]
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'
REGISTERED_ANCHOR = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/REGISTERED_ANCHOR_CX2V006R8.json', 'sha256': '7693959ceca48581a06c1ca439c02bd80fd2ecfb158073270e3d2dc614ea79c3'}
ANCHOR_CONTEXT = contextvars.ContextVar('cx2r8_anchor', default=None)
DECIDING_NUMERICS_CONTEXT = contextvars.ContextVar('cx2r9_deciding_numerics', default=None)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def load_parent():
    raw = PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PARENT_SHA:
        raise ValueError('parent bytes changed')
    m = types.ModuleType('_calibration_cx2_parent_v005')
    m.__file__ = str(PARENT)
    sys.modules[m.__name__] = m
    exec(compile(raw, str(PARENT), 'exec'), m.__dict__)
    return m

O = load_parent()
O.MODULE_NAME = MODULE_NAME
O.MAPPING_ID = 'CX2V006_PHYS4_FULL_HULL_POINT_CERTIFICATES'
O.SCHEMA_CACHE_ID = 'DDO154_CALIBRATION_CACHE_ID_CX2V006'
O.KNOWN_REAL_DRIVER_SHA256.add(DRIVER_SHA)
O.CONFIG_KEYS = O.CONFIG_KEYS | {'tail_readiness'}
O.DECLARED_CHANGED_PATHS = O.DECLARED_CHANGED_PATHS + (
    'numerics.uv_tail.eps_certificate', 'numerics.uv_tail.lo_certificate')
Error = O.OrchestratorError

def pin_doc(pin, label):
    return json.loads(O.read_pinned(pin, label))

def gate_pending(reason):
    return {'ok': False, 'reasons': [reason], 'status': 'UNTESTED'}

def checked_gate(pin, schema, bindings, label):
    if pin is None:
        return gate_pending(label + ': evidence pending')
    try:
        doc = pin_doc(pin, label)
        reasons = []
        if doc.get('schema') != schema:
            reasons.append('wrong evidence schema')
        if doc.get('status') != 'TESTED' or doc.get('ok') is not True:
            reasons.append('evidence is not TESTED ok')
        for k, v in bindings.items():
            if doc.get(k) != v:
                reasons.append('binding mismatch: ' + k)
        # These are custody attestations; actual receipt checks are added by caller.
        return {'ok': not reasons, 'reasons': reasons, 'evidence': pin, 'document': doc}
    except (Error, ValueError, OSError) as exc:
        return gate_pending(label + ': ' + str(exc))

def registered_anchor(anchor):
    """0554 exact target-free anchor registration, independent of a proposed row."""
    reg = pin_doc(REGISTERED_ANCHOR, 'registered A2F10 anchor')
    template = pin_doc(reg['source_template'], 'registered anchor source template')
    if (reg.get('schema') != 'DDO154_REGISTERED_ANCHOR_CX2V006R8' or
            reg.get('galaxy') != 'DDO154' or reg.get('physical') != template.get('physical') or
            reg.get('coefficients') != template.get('coefficients') or
            reg['physical'].get('distance_Mpc') != 4.04 or
            reg['coefficients'].get('sha256') != '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'):
        raise Error('REGISTERED_ANCHOR_SOURCE_MISMATCH')
    coordinate = pin_doc(reg['coordinate_registration'], 'anchor coordinate registration')
    if coordinate['trial_point']['anchor_spec'] != reg['source_template']:
        raise Error('REGISTERED_ANCHOR_COORDINATE_MISMATCH')
    if (not isinstance(anchor, dict) or anchor.get('registered_point') != REGISTERED_ANCHOR or
            anchor.get('physical') != reg['physical'] or anchor.get('coefficients') != reg['coefficients'] or
            anchor.get('driver_sha256') != DRIVER_SHA):
        raise Error('CONFIG_ANCHOR_REGISTRATION_MISMATCH')
    if anchor.get('use') is not False:
        raise Error('R8_ANCHOR_ALIAS_DISABLED')
    return reg

def deciding_numerics_identity(block):
    """0557: remove exactly the two per-point certificate slots, as point_identity."""
    if not isinstance(block, dict) or not isinstance(block.get('uv_tail'), dict):
        raise Error('DECIDING_CONFIG_NUMERICS_BLOCK_REQUIRED')
    numerical_identity = copy.deepcopy(block)
    for slot in ('eps_certificate', 'lo_certificate'):
        numerical_identity['uv_tail'].pop(slot, None)
    return numerical_identity

def check_deciding(dt, driver_sha256, mon, synthetic=False, *, anchor=None, numerics_block=None):
    """0540 F2: named, fresh headline runs bound to actual driver normalization."""
    if synthetic:
        raise Error('v006 real driver cannot use synthetic gate bypass')
    g = checked_gate(dt, 'DDO154_V010R5_DECIDING_CX2V006',
                     {'driver_sha256': driver_sha256, 'route_a_column_workers': 8}, 'deciding')
    if g['ok']:
        try:
            anchor = ANCHOR_CONTEXT.get() if anchor is None else anchor
            registered = registered_anchor(anchor)
            numerics_block = DECIDING_NUMERICS_CONTEXT.get() if numerics_block is None else numerics_block
            expected_numerics = canonical(deciding_numerics_identity(numerics_block))
            if driver_sha256 != DRIVER_SHA:
                raise Error('DECIDING_DRIVER_NOT_PINNED_R5')
            rows = g['document'].get('runs')
            if (not isinstance(rows, list) or len(rows) != 2 or
                    any(not isinstance(row, dict) for row in rows) or
                    {row.get('name') for row in rows} != {'reanchor', 'workers_8'}):
                raise Error('DECIDING_EXACT_NAMED_REANCHOR_AND_WORKERS_8_REQUIRED')
            normalizer = O.exec_pinned_bytes(
                {'path': str(BASE/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'),
                 'sha256': DRIVER_SHA}, '_cx2r7_deciding_normalizer', 'deciding r5 normalizer')
            result_hashes = set()
            for row in rows:
                label = 'deciding ' + row['name']
                sp = pin_doc(row['spec'], label + ' spec')
                if row['spec_sha256'] != row['spec']['sha256']:
                    raise Error('DECIDING_SPEC_PIN_MISMATCH')
                if sp.get('galaxy') != 'DDO154' or sp['physical'].get('distance_Mpc') != 4.04:
                    raise Error('DECIDING_DDO154_HEADLINE_REQUIRED')
                if sp.get('admit', {}) != {}:
                    raise Error('DECIDING_FRESH_CALL_REQUIRED')
                validate_block(sp['numerics'])
                if canonical(deciding_numerics_identity(sp['numerics'])) != expected_numerics:
                    raise Error('DECIDING_NUMERICS_NOT_CONFIG_BLOCK: ' + row['name'])
                if row['name'] == 'reanchor':
                    if sp['physical'] != registered['physical'] or sp.get('coefficients') != registered['coefficients']:
                        raise Error('REANCHOR_NOT_EXACT_REGISTERED_A2F10_POINT')
                    if (anchor.get('result') is None or anchor.get('receipt') is None or
                            anchor.get('spec_sha256') is None):
                        raise Error('CONFIG_ANCHOR_TAIL_REANCHOR_PENDING')
                    if (row['result'] != anchor['result'] or row['receipt'] != anchor['receipt'] or
                            row['spec']['sha256'] != anchor['spec_sha256']):
                        raise Error('REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH')
                res = pin_doc(row['result'], label + ' result')
                if (res.get('call_spec_sha256') != row['spec']['sha256'] or
                        res.get('driver_sha256') != DRIVER_SHA or
                        res.get('status') != 'COMPLETED' or res.get('valid') is not True):
                    raise Error('DECIDING_RESULT_BINDING_OR_VALIDITY')
                normalized = res.get('normalized_spec')
                expected = normalizer.normalize_spec(copy.deepcopy(sp))
                if normalized != expected:
                    raise Error('DECIDING_NORMALIZED_SPEC_NOT_EXACT_DRIVER_REPLAY')
                if normalized.get('galaxy') != 'DDO154' or normalized['physical'].get('distance_Mpc') != 4.04:
                    raise Error('DECIDING_NORMALIZED_HEADLINE_REQUIRED')
                # r5 adds this deterministic None default; the full normalized
                # object was already compared exactly to the driver's output.
                normalized_block = copy.deepcopy(normalized['numerics'])
                if normalized_block.get('truncation') != {'shape': 'cube', 'kmax_inverse_kpc': None}:
                    raise Error('DECIDING_NORMALIZED_KEPT_CUBE_REQUIRED')
                normalized_block['truncation'] = {'shape': 'cube'}
                validate_block(normalized_block)
                workers = normalized['numerics']['route_a'].get('column_workers')
                if type(workers) is not int or workers != 8:
                    raise Error('DECIDING_NORMALIZED_WORKERS_8_REQUIRED')
                bad = O._receipt_ok(mon, row['receipt'], row['spec_sha256'], DRIVER_SHA,
                                    row['result'], label)
                if bad:
                    raise Error(bad)
                finish_ref, why = O.finish_binding(row['result']['path'], row['result']['sha256'])
                if why:
                    raise Error(why)
                finish = pin_doc(finish_ref, label + ' adjacent finish')
                if finish.get('status') != 'COMPLETED' or finish.get('valid') is not True:
                    raise Error('DECIDING_FINISH_NOT_COMPLETED_VALID')
                result_hashes.add(row['result']['sha256'])
            if len(result_hashes) != 2:
                raise Error('DECIDING_DISTINCT_RUN_RESULTS_REQUIRED')
        except (Exception,) as exc:
            # Driver normalizer may raise its own Refusal class; none is a pass.
            g['reasons'].append(type(exc).__name__ + ': ' + str(exc))
        g['ok'] = not g['reasons']
    g['route_a_column_workers_verified'] = 8 if g['ok'] else None
    return g

def check_numerics(ncfg, template_numerics, deciding_route_a_n, synthetic=False):
    p = Path(__file__).resolve().parent.parent/'v006r7/adoption_policy_cx2v006r7.py'
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d':
        raise Error('adoption policy source pin mismatch')
    mod = types.ModuleType('_cx2r7_adoption')
    mod.__file__ = str(p)
    sys.modules[mod.__name__] = mod
    exec(compile(raw, str(p), 'exec'), mod.__dict__)
    return mod.check_numerics(ncfg, template_numerics, deciding_route_a_n,
        O=O, validate_block=validate_block, driver_sha=DRIVER_SHA, synthetic=synthetic)


def validate_block(block):
    u = block.get('uv_tail', {})
    if u.get('enabled') is not True or u.get('source_rule') != 'continuum_v001':
        raise Error('production continuum tail-ON required')
    if block.get('truncation') != {'shape': 'cube'}:
        raise Error('kept cube required')
    if block['composite_grid_spec']['breaks_inverse_kpc'][-1] != 4:
        raise Error('kept K must be 4')
    if u.get('outer') != {'shape':'cylinder','K_big_inverse_kpc':128.0}:
        raise Error('A55 production K_big 128 required')
    if u.get('gas') != {'M_s':128,'interp':'lagrange3_s_gl4'}:
        raise Error('A57 production gas M_s 128 required')
    if u.get('lambda_scale') != 1.0 or u.get('lapse_only') is not True:
        raise Error('tail must be unrescaled lapse-only')
    if block['route_a'].get('column_workers') != 8 or 'ro1_workers' in block['route_a']:
        raise Error('route A workers 8 required; tail-ON automatically selects RO1 (tail-OFF flag forbidden)')
    rules = block['brackets']['rule']
    fs = rules['fs_absolute_overrides']
    if set(fs) != {str(i) for i in range(72)} or any(v != HULL for v in fs.values()):
        raise Error('full A32 hull required on every one of 72 columns')

def point_identity(spec):
    n = copy.deepcopy(spec['numerics'])
    for key in ('eps_certificate','lo_certificate'):
        n['uv_tail'].pop(key, None)
    return {'driver_sha256': DRIVER_SHA, 'physical': spec['physical'],
            'coefficients': spec['coefficients'], 'numerics': n}

class Mapper(O.Mapper):
    def build(self, theta, recovery=None):
        if recovery is not None:
            raise Error('v006 no automatic bracket recovery; successor registration required')
        built = super().build(theta)
        spec = built['spec']
        # A32 is an absolute enthalpy search interval: no D-rescaling is declared.
        # Every column retains the full hull at every D; run-mode evidence still gates D!=4.04.
        ident = point_identity(spec)
        registry = self.ctx.cfg['tail_readiness'].get('certificate_registry')
        if registry is not None:
            doc = pin_doc(registry, 'point certificate registry')
            rec = doc.get('points', {}).get(digest(ident))
            if rec is not None:
                if rec.get('identity') != ident:
                    raise Error('certificate identity collision/mismatch')
                for field in ('eps_certificate','lo_certificate'):
                    ref = rec[field]
                    O.read_pinned(ref, field)
                    spec['numerics']['uv_tail'][field] = copy.deepcopy(ref)
        spec['label'] = 'DDO154 cx2v006 theta %s; point %s' % (built['key'][:16], digest(ident)[:16])
        raw = O.json_bytes(spec)
        built.update(raw=raw, sha256=O.sha256_bytes(raw), changed_paths=O.diff_paths(self.ctx.base,spec),
                     certificate_identity=ident, certificate_point_key=digest(ident))
        return built

O.Mapper = Mapper
O.check_deciding = check_deciding
O.check_numerics = check_numerics

class Context(O.Context):
    def __init__(self,config):
        cfg = O.load_json_file(config, 'config') if isinstance(config,(str,Path)) else config
        registered_anchor(cfg.get('anchor'))
        bound_anchor = copy.deepcopy(cfg['anchor'])
        bound_numerics = copy.deepcopy(cfg['numerics']['block'])
        canonical(deciding_numerics_identity(bound_numerics))
        anchor_token = ANCHOR_CONTEXT.set(bound_anchor)
        numerics_token = DECIDING_NUMERICS_CONTEXT.set(bound_numerics)
        try:
            super().__init__(cfg)
        finally:
            DECIDING_NUMERICS_CONTEXT.reset(numerics_token)
            ANCHOR_CONTEXT.reset(anchor_token)

    def fresh_gates(self):
        # The inherited pre-wave recheck calls the same global gate outside init.
        # Bind this instance's anchor and numerics for the complete call, then restore.
        registered_anchor(self.cfg.get('anchor'))
        bound_anchor = copy.deepcopy(self.cfg['anchor'])
        bound_numerics = copy.deepcopy(self.cfg['numerics']['block'])
        canonical(deciding_numerics_identity(bound_numerics))
        anchor_token = ANCHOR_CONTEXT.set(bound_anchor)
        numerics_token = DECIDING_NUMERICS_CONTEXT.set(bound_numerics)
        try:
            return super().fresh_gates()
        finally:
            DECIDING_NUMERICS_CONTEXT.reset(numerics_token)
            ANCHOR_CONTEXT.reset(anchor_token)

    def check_adoption(self):
        r = self.cfg['tail_readiness']
        g = checked_gate(self.cfg.get('adoption_derivation'), 'DDO154_TAIL_READINESS_CX2V006',
                         {'base_spec_sha256':self.base_sha256, 'driver_sha256':DRIVER_SHA,
                          'certificate_registry':r.get('certificate_registry')}, 'tail production readiness')
        if g['ok']:
            # The verifier needs scientifically valid EPS/GQ/LO proofs and complete
            # per-iterate source custody. That interface is a remaining build gate,
            # and cannot be replaced by an asserted ok flag.
            g['reasons'].append('POST_STATE_LO_GQ_ACCEPTANCE_VERIFIER_NOT_INTEGRATED')
            g['ok'] = False
        return g

    def capability_probe(self):
        results = []
        for label, th in self.probe_points():
            try:
                b = self.mapper.build(th)
                self.prelaunch_check(b['spec'])
                results.append({'point':label,'spec_sha256':b['sha256'],'normalize_ok':True})
            except (Error, ValueError) as exc:
                results.append({'point':label,'normalize_ok':False,'reason':str(exc)})
        g = checked_gate(self.cfg.get('capability_evidence'), 'DDO154_TAIL_BOX_RUN_CAPABILITY_CX2V006',
                         {'driver_sha256':DRIVER_SHA,'base_spec_sha256':self.base_sha256}, 'A32 run-mode box evidence')
        if g['ok']:
            rows = {x['spec_sha256']: x for x in g['document'].get('rows',[])}
            for p in results:
                row = rows.get(p.get('spec_sha256'))
                if not row or row.get('run_mode_admitted') is not True:
                    g['reasons'].append('missing run-mode evidence for '+p['point'])
                    continue
                try:
                    bad = O._receipt_ok(self.M,row['receipt'],p['spec_sha256'],DRIVER_SHA,row['result'],'A32 corner')
                    if bad: g['reasons'].append(bad)
                except (Error,KeyError,OSError) as exc:
                    g['reasons'].append(str(exc))
            g['ok'] = not g['reasons']
        g['normalization'] = results
        g['layer1_normalize_ok'] = all(p['normalize_ok'] for p in results)
        g['ok'] = g['ok'] and g['layer1_normalize_ok']
        return g

O.Context = Context
Orchestrator = O.Orchestrator

def planning_context(config):
    """Pinned v005/v003b budget probe, no forward or work-directory writes."""
    ctx = Context(config)
    if ctx.driver['sha256'] != DRIVER_SHA:
        raise Error('v006 requires pinned v010 r5')
    return ctx

def plan(config):
    ctx = planning_context(config)
    rep = Orchestrator(ctx).plan_only()
    rep['execution_note'] = WAIVER
    rep['build_status'] = 'CANDIDATE_NOT_PRODUCTION_READY'
    rep['launches_performed'] = 0
    return rep

def wave(config, replay_cache=None):
    """Return next actual engine wave from a supplied immutable replay snapshot.

    No fixture values are manufactured. Snapshot entries must be v006 cache
    records; v005 Cache verification binds their original specs and receipts.
    """
    ctx = planning_context(config)
    orch = Orchestrator(ctx)
    orch.prepare(create=False)
    if replay_cache is not None:
        raise Error('use the configured v006 verified cache; unverified snapshots refused')
    pr = orch.probe.run(orch.cache, 'probe')
    return {'execution_note':WAIVER,'cache_id':ctx.cache_id,'probe':pr,
            'gates':ctx.gate_report(),'gates_ok':ctx.gates_ok(),'launches_performed':0}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=('plan','wave'))
    ap.add_argument('--config',required=True)
    ap.add_argument('--output',required=True)
    a = ap.parse_args()
    try:
        out = plan(a.config) if a.command == 'plan' else wave(a.config)
    except (Error,ValueError,OSError,KeyError) as exc:
        out = {'status':'REFUSED','reasons':[type(exc).__name__+': '+str(exc)],
               'execution_note':WAIVER,'launches_performed':0}
    O.write_json_x(a.output,out)
    print(json.dumps({'output':a.output,'status':out.get('status'),'gates_ok':out.get('gates_ok')}))
    return 0 if out.get('status') == 'OK' else 3

if __name__ == '__main__':
    sys.exit(main())
