"""S1-only kept-K-3 successor of wrapper v002 q5b1 (Claude2 root workflow s1_successors_c2, c2v001; A150 R-S1-3 (2)).

Predecessors, loaded unchanged by path and sha: wrapper v002 q5b1 (7a6af535), which itself loads core dc895f8a, the
v005 orchestrator c75a889f, sensitivity policy 8fb06600 and certificate guard b1 9e3fc109. Their generated buffer is
compiled under q5b1's own path, so guard011/guard012's compile contract (7a6af535 -> 79e8936d) still covers it.

One change, for one spec family only. A spec is S1_UA_C3T when its label is exactly the S1 template's C3T label form
(registration C2V002 section 4, CHOICE C5: 'S1 transfer test C3T at u_A theta <16 hex>; base <8 hex>'). For such a spec:
  * validate_block: composite_grid_spec must equal CB C3T's (case block 76309ae3, /numerics) bitwise, so its last break
    is 3; every other clause is core dc895f8a's own validate_block, run on the same block with only the grid replaced
    by CB C4T's (the K clause is the only clause that reads the grid);
  * prelaunch: the normalized spec may also differ from the normalized base at numerics.composite_grid_spec.*, and
    only when the normalized grid equals CB C3T bitwise; the orchestrator v005 prelaunch rule is otherwise unchanged
    (A7 lint, absolute paths, the driver's normalize_spec, declared paths); no bracket recovery;
  * certificate_check (S1 only, fail closed): the registry bundle of the point must declare the kept K (3) as its
    domain K. Certificate guard b1 L94 accepts domain K 4.0 only, so S1_UA_C3T cannot pass certificate_check until
    a reviewed K=3 certificate chain exists (S1_C3T_CERT_EXTENSION_PROCEDURE.md).
Every other spec (K = 2, 5, 6, any other grid, any other label, S1_UA_C4T included) takes the predecessor's code paths
unchanged: validate_block is core's function object itself; certificate_check and prelaunch_check call q5b1's methods.
validate_block exported here is core's (the guard's adoption check and the direct adapter's config block use it).

This module is a step-4 direct-preflight context module only (guard `context_module`): no CLI, no campaign entry point.
Importing it reads pinned source bytes only; no process, no write.
"""
import contextvars
import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
PREDECESSOR = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',
               '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d')
CB_PIN = {'path': ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
          'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}
S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')
S1_C3T_KEPT_K = 3
GRID = 'numerics.composite_grid_spec'


def _load(path, name, expected):
    """q5b1's own load(): bytes, sha, exec under the file's own path."""
    p = Path(path)
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('source byte pin mismatch: ' + str(p))
    sp = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, str(p), 'exec'), m.__dict__)
    return m


W = _load(PREDECESSOR[0], '_q5b1_for_s1k3_c2v001', PREDECESSOR[1])
M = W.M
O = W.O
Error = W.Error
DRIVER_SHA = W.DRIVER_SHA
HULL = W.HULL
WAIVER = W.WAIVER
point_identity = W.point_identity
validate_block = M.validate_block              # core dc895f8a's function, unchanged
PREDECESSOR_VALIDATE_BLOCK = W.validate_block  # the same object (q5b1 L35: validate_block = M.validate_block)

_CB = {}


def cb_grid(case):
    """CB `cases.<case>.normalized_spec_equal./numerics.composite_grid_spec`, from the pinned bytes (read once)."""
    if not _CB:
        raw = Path(CB_PIN['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
            raise Error('CB case block: sha256 mismatch')
        doc = json.loads(raw)
        for c in ('C3T', 'C4T'):
            _CB[c] = doc['cases'][c]['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB[case])


def s1_c3t_identified(spec):
    lab = spec.get('label') if isinstance(spec, dict) else None
    return isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None


def validate_s1_c3t_block(block):
    """S1_UA_C3T only: grid = CB C3T bitwise, then core's validate_block on the block with only the grid set to CB C4T's."""
    if not isinstance(block, dict) or M.canonical(block.get('composite_grid_spec')) != M.canonical(cb_grid('C3T')):
        raise Error('S1_UA_C3T: composite_grid_spec must equal CB C3T bitwise (kept K 3)')
    shadow = dict(block)
    shadow['composite_grid_spec'] = cb_grid('C4T')
    M.validate_block(shadow)


def validate_spec_block(spec):
    """The spec-level check: S1_UA_C3T -> validate_s1_c3t_block; every other spec -> core's validate_block."""
    if s1_c3t_identified(spec):
        return validate_s1_c3t_block(spec['numerics'])
    return M.validate_block(spec['numerics'])


# q5b1's certificate_check calls its module-global validate_block on the spec's numerics. Inside this module's S1_UA_C3T
# certificate_check only, that one block object is checked by validate_s1_c3t_block; every other call is core's function.
_S1_BLOCK = contextvars.ContextVar('s1k3_c3t_numerics', default=None)


def _validate_block_in_predecessor(block):
    s1 = _S1_BLOCK.get()
    if s1 is not None and block is s1:
        return validate_s1_c3t_block(block)
    return PREDECESSOR_VALIDATE_BLOCK(block)


W.validate_block = _validate_block_in_predecessor


def _bundle_domain_k(ref):
    b = M.pin_doc(ref, 'S1_UA_C3T point certificate bundle')
    return (b.get('domain') or {}).get('K_inverse_kpc')


class Context(W.Context):
    """q5b1's Context; S1_UA_C3T specs only take the two overrides below."""

    def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
        if not s1_c3t_identified(spec):
            return super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        validate_s1_c3t_block(spec['numerics'])
        token = _S1_BLOCK.set(spec['numerics'])
        try:
            g = super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        finally:
            _S1_BLOCK.reset(token)
        if not g.get('ok'):
            return g
        try:
            registry = M.pin_doc(self.cfg['tail_readiness']['certificate_registry'], 'certificate registry')
            rec = registry['points'][M.digest(point_identity(spec))]
            refs = [rec['bundle']] + ([g['certificate_bundle']] if g.get('certificate_bundle') else [])
            for ref in refs:
                k = _bundle_domain_k(ref)
                if k != float(S1_C3T_KEPT_K):
                    raise Error('S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K: bundle domain K %r, kept K %d'
                                % (k, S1_C3T_KEPT_K))
        except (Error, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            return {'ok': False, 'blockers': [type(exc).__name__ + ': ' + str(exc)]}
        return g

    def prelaunch_check(self, spec, recovery=False):
        if not s1_c3t_identified(spec):
            return super().prelaunch_check(spec, recovery=recovery)
        if recovery:
            raise Error('S1_UA_C3T: no bracket recovery (R6 L1084; core Mapper L242)')
        validate_s1_c3t_block(spec['numerics'])
        sg = self.sensitivity_gate(spec)
        if not sg['ok']:
            raise Error('SENSITIVITY_DECIDING_III_REQUIRED: ' + repr(sg['reasons']))
        normalized = self._s1_c3t_normalized(spec)
        if self.cfg['tail_readiness'].get('certificate_registry') is not None:
            g = self.certificate_check(spec, 'prelaunch')
            if not g['ok']:
                raise Error('CERTIFICATE_PREFLIGHT: ' + repr(g['blockers']))
        return normalized

    def _s1_c3t_normalized(self, spec):
        """Orchestrator v005 prelaunch_check (L2020-2039) with one added allowance: numerics.composite_grid_spec.*,
        only when the normalized grid equals CB C3T bitwise."""
        a7 = O.lint_override_keys(spec) + O.relative_paths(spec)
        if a7:
            raise Error('A7_GUARD: %s' % a7[:5])
        try:
            n = self.D.normalize_spec(copy.deepcopy(spec))
        except Exception as exc:
            raise Error('DRIVER_REFUSES_SPEC: %s: %s' % (type(exc).__name__, str(exc)[:300]))
        grid_ok = M.canonical(((n or {}).get('numerics') or {}).get('composite_grid_spec')) == M.canonical(cb_grid('C3T'))
        bad = []
        for p in O.diff_paths(self.norm_base, n):
            if p in O.DECLARED_CHANGED_PATHS:
                continue
            if grid_ok and (p == GRID or p.startswith(GRID + '.')):
                continue
            bad.append(p)
        if bad:
            raise Error('normalized spec differs from the normalized base at undeclared paths %s' % bad)
        return n
