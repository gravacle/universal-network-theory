"""Dispatch 0511 build: v010 r4 calibration adapter over the pinned v005 engine.

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
DRIVER_SHA = 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
WAIVER = 'nice unavailable (sandbox); 0514 waiver'
MODULE_NAME = 'calibration_orchestrator_cx2v006'
HULL = [151250000.0, 317625000.0]
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'

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

def check_deciding(dt, driver_sha256, mon, synthetic=False):
    if synthetic:
        raise Error('v006 real driver cannot use synthetic gate bypass')
    g = checked_gate(dt, 'DDO154_V010R4_DECIDING_CX2V006',
                     {'driver_sha256': driver_sha256, 'route_a_column_workers': 8}, 'deciding')
    if g['ok']:
        for row in g['document'].get('runs', []):
            try:
                O._receipt_ok(mon, row['receipt'], row['spec_sha256'], driver_sha256,
                              row['result'], 'v006 deciding')
            except (Error, KeyError, OSError) as exc:
                g['reasons'].append(str(exc))
        if len(g['document'].get('runs', [])) < 2:
            g['reasons'].append('tail-ON reanchor and workers-8 evidence required')
        g['ok'] = not g['reasons']
    g['route_a_column_workers_verified'] = 8 if g['ok'] else None
    return g

def check_numerics(ncfg, template_numerics, deciding_route_a_n, synthetic=False):
    if synthetic:
        raise Error('v006 synthetic bypass is forbidden')
    block = copy.deepcopy(ncfg['block'])
    validate_block(block)
    # V007 verdict's actual schema is still under revision. A root-produced
    # adapter must bind original verdict bytes, adopted block and uncertainty.
    g = checked_gate(ncfg.get('verdict_artifact'), 'DDO154_V007_ADOPTION_CX2V006',
                     {'numerics_sha256': digest(block), 'driver_sha256': DRIVER_SHA}, 'V007 adoption')
    if g['ok']:
        d = g['document']
        original = pin_doc(d['original_verdict'], 'original V007 verdict')
        if original.get('decision', {}).get('outcome') != 'ADOPT' or original.get('test_mode') is not False:
            g['reasons'].append('original verdict is not real ADOPT')
        source = pin_doc(ncfg.get('block_source'), 'adopted call spec')
        if source.get('numerics') != block:
            g['reasons'].append('block differs from adopted call spec')
        g['u_i_km_s'] = d.get('u_i_km_s')
        g['ok'] = not g['reasons']
    return block, g

def validate_block(block):
    u = block.get('uv_tail', {})
    if u.get('enabled') is not True or u.get('source_rule') != 'continuum_v001':
        raise Error('production continuum tail-ON required')
    if block.get('truncation') != {'shape': 'cube'}:
        raise Error('kept cube required')
    if block['composite_grid_spec']['breaks_inverse_kpc'][-1] != 4:
        raise Error('kept K must be 4')
    if u['outer'] not in ({'shape':'cylinder','K_big_inverse_kpc':64.0},
                          {'shape':'cylinder','K_big_inverse_kpc':128.0}):
        raise Error('this candidate build supports K_big 64 or 128 only')
    if u.get('lambda_scale') != 1.0 or u.get('lapse_only') is not True:
        raise Error('tail must be unrescaled lapse-only')
    if block['route_a'].get('column_workers') != 8 or block['route_a'].get('ro1_workers') is not True:
        raise Error('route A workers 8 and explicit RO1 required')
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
                    O._receipt_ok(self.M,row['receipt'],p['spec_sha256'],DRIVER_SHA,row['result'],'A32 corner')
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
        raise Error('v006 requires pinned v010 r4')
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
