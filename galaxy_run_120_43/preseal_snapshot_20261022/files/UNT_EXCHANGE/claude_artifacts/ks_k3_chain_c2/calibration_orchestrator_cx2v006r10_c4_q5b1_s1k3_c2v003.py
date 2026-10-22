"""KS5'' (ks_k3_chain_c2 G-wave c2v003; root A175 ruling on ADV-D1/D2): KS5' (66560a6a) plus an S1-only rho slot check.

c2v003 changes one thing. In an S1_UA_C3T certificate_check (prelaunch, so prelaunch_check too, and acceptance), after
q5b1's checks with KS5 and c2v001's domain-K check pass, the point's registered lo slot (the rho record) must be the K=3
contract: required_coverage_inverse_kpc [3, 182] with coverage_complete, the 10-shell partition [3,4], [4,5], [5,6],
[6,8], [8,12], [12,16], [16,32], [32,64], [64,128], [128,182], and the KS2 response producer (the whole pin, and its
bytes read through q5b1's O.read_pinned). q5b1 L168-172 checks only the slot rho's schema, custody and flags, so a K=4
slot cost a 10-18 h S1 call before the acceptance adapter refused it (wave-1 P-F2 note; A175). Every other spec, and
every non-rho clause, is c2v002's. Edits: this docstring head, MODULE_NAME, the S1 rho contract after GUARD_KS5, the
check function after _bundle_domain_k, and three lines after the domain-K check. The text of c2v002 follows.

KS5' (ks_k3_chain_c2 c2v002; root A160): s1k3 c2v001 (e7f52461) whose S1_UA_C3T certificate checks use KS5.

c2v002 changes one thing. q5b1's module-global guard G (L30) becomes a dispatch that is certificate guard b1 (9e3fc109,
unchanged) except inside a KS5 scope, where it is KS5 (certificate_guard_b1_ks5_c2v001, by path and sha below):
  * certificate_check / prelaunch_check of an S1_UA_C3T spec (label, then CB C3T grid as c2v001) run in a KS5 scope:
    q5b1 L73 (policy review guard_sha256), L150 (PROOF_SCHEMA) and L192 (verify_bundle) read KS5;
  * every other spec runs in an explicit b1 scope: q5b1's code with b1, exactly as c2v001 and q5b1;
  * outside a spec (Context construction, a direct certificate_policy_gate() call: guard012 L256) the scope is the
    Context's own: KS5 iff its C1's certificate policy review binds KS5's sha, else b1. So an S1_UA_C3T C1 binds KS5
    (procedure step 6.6); under it every other spec still meets b1's sha and its policy gate reads pending.
c2v001's S1-only domain check (bundle domain K == kept K 3) is kept. The text of c2v001 follows.

S1-only kept-K-3 successor of wrapper v002 q5b1 (Claude2 root workflow s1_successors_c2, c2v001; A150 R-S1-3 (2)).

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

MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
PREDECESSOR = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',
               '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d')
CB_PIN = {'path': ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
          'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}
S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')
S1_C3T_KEPT_K = 3
GRID = 'numerics.composite_grid_spec'
GUARD_KS5 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/certificate_guard_b1_ks5_c2v001.py', 'e394ae94c6f48ff9e0919e9b186103d2f7c5b00077967579029e8404a62215d6')   # c2v002
# c2v003 (A175): the S1_UA_C3T lo slot's rho contract (KS2 shell_plan(unit=False) at kept K 3; KS6 adapter _rho_contract).
RESPONSE_KS2 = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py', 'sha256': '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'}
RHO_COVERAGE_S1 = [3.0, 182.0]
RHO_PARTITION_S1 = [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                    [64.0, 128.0], [128.0, 182.0]]


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
G_B1 = W.G                                     # c2v002: q5b1 L30's guard, b1 9e3fc109, unchanged
G_KS5 = _load(GUARD_KS5[0], '_ks5_guard_for_s1k3_c2v002', GUARD_KS5[1])
_GUARD = contextvars.ContextVar('s1k3_c2v002_guard', default=None)


class _GuardDispatch(object):
    """c2v002: q5b1's module-global G. b1 outside a KS5 scope; KS5 inside one (see the module docstring)."""

    def __getattr__(self, name):
        g = _GUARD.get()
        return getattr(G_B1 if g is None else g, name)


W.G = _GuardDispatch()


def _policy_binds_ks5(cfg):
    """c2v002: True iff the C1's certificate policy review binds KS5's sha (the q5b1 L73 guard_sha256)."""
    try:
        doc = M.pin_doc(cfg['tail_readiness']['certificate_policy_review'], 'certificate policy review')
        return isinstance(doc, dict) and doc.get('guard_sha256') == GUARD_KS5[1]
    except Exception:
        return False

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


def s1_rho_slot_problems(rho):
    """c2v003 (A175): the S1_UA_C3T lo slot rho against the K=3 contract. Returns the problems (empty: it is the contract)."""
    if not isinstance(rho, dict):
        return ['S1_RHO_SLOT_NOT_AN_OBJECT']
    bad = []
    if rho.get('coverage_complete') is not True or rho.get('required_coverage_inverse_kpc') != RHO_COVERAGE_S1:
        bad.append('S1_RHO_SLOT_COVERAGE_NOT_3_TO_182')
    shells = rho.get('shells') if isinstance(rho.get('shells'), list) else []
    if [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] != RHO_PARTITION_S1:
        bad.append('S1_RHO_SLOT_PARTITION_NOT_THE_10_SHELLS_FROM_3')
    if rho.get('producer') != RESPONSE_KS2:
        bad.append('S1_RHO_SLOT_PRODUCER_NOT_KS2')
    else:
        try:
            O.read_pinned(dict(RESPONSE_KS2), 'S1_UA_C3T rho producer (KS2)')
        except Exception as exc:
            bad.append('S1_RHO_SLOT_PRODUCER_BYTES_NOT_KS2: %s: %s' % (type(exc).__name__, exc))
    return bad


class Context(W.Context):
    """q5b1's Context; S1_UA_C3T specs only take the two overrides below (c2v002: and the KS5 guard scope)."""

    def __init__(self, config):
        cfg = O.load_json_file(config, 'config') if isinstance(config, (str, Path)) else config
        self._s1_guard_ks5 = _policy_binds_ks5(cfg)                    # c2v002: the Context's own guard scope
        token = _GUARD.set(G_KS5 if self._s1_guard_ks5 else G_B1)
        try:
            super().__init__(config)
        finally:
            _GUARD.reset(token)

    def certificate_policy_gate(self):
        if _GUARD.get() is not None:                                   # c2v002: inside a spec (or init) scope
            return super().certificate_policy_gate()
        token = _GUARD.set(G_KS5 if getattr(self, '_s1_guard_ks5', False) else G_B1)
        try:
            return super().certificate_policy_gate()
        finally:
            _GUARD.reset(token)

    def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
        if not s1_c3t_identified(spec):
            gtoken = _GUARD.set(G_B1)                                  # c2v002: every other spec meets b1
            try:
                return super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
            finally:
                _GUARD.reset(gtoken)
        validate_s1_c3t_block(spec['numerics'])
        token = _S1_BLOCK.set(spec['numerics'])
        gtoken = _GUARD.set(G_KS5)                                     # c2v002: S1_UA_C3T meets KS5
        try:
            g = super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        finally:
            _GUARD.reset(gtoken)
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
            bad = s1_rho_slot_problems(M.pin_doc(rec['lo_certificate'], 'S1_UA_C3T registered rho record'))   # c2v003
            if bad:
                raise Error('S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT: ' + '; '.join(bad))
        except (Error, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            return {'ok': False, 'blockers': [type(exc).__name__ + ': ' + str(exc)]}
        return g

    def prelaunch_check(self, spec, recovery=False):
        if not s1_c3t_identified(spec):
            gtoken = _GUARD.set(G_B1)                                  # c2v002: every other spec meets b1
            try:
                return super().prelaunch_check(spec, recovery=recovery)
            finally:
                _GUARD.reset(gtoken)
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
