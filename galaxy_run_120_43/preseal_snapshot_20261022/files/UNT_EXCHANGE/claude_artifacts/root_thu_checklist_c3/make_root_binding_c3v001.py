"""Write root's ROOT_BOUND A296 certificate binding (successor of the unbound template A296_BINDING_TEMPLATE_CX2V002 b882a15f)
and validate it with the pinned a296_binding_cx2v002.validate_binding (141c1cd2) through a read-only exact-pin snapshot.
Claude3, root deputy (A292; root 0857 item 3). Root runs it. Exclusive create; nothing else is written.
usage: python3 -I -B make_root_binding_c3v001.py --c1 ABS --c1-sha256 H --policy ABS --policy-sha256 H --out ABS_NEW_JSON
       python3 -I -B make_root_binding_c3v001.py --check-only --binding ABS --binding-sha256 H
Exit 0: written and/or validated. Exit 2: refused (nothing written)."""
import argparse, hashlib, json, os, sys, types
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
TEMPLATE = {'path': ART + '/eps_rule_successor_cx2/integration/lookup/A296_BINDING_TEMPLATE_CX2V002.json',
            'sha256': 'b882a15f934140f228b32caecc208586984511e7295928384c45042ced9767ca'}
VALIDATOR = {'path': ART + '/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py',
             'sha256': '141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43'}
def refuse(code): raise ValueError(code)
def read_exact(ref):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}: refuse('EXACT_PIN_REQUIRED')
    p = ref['path']
    if not os.path.isabs(p) or os.path.realpath(p) != p or os.path.islink(p): refuse('PIN_PATH_NOT_CANONICAL: ' + str(p))
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f: raw = f.read()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']: refuse('BYTE_PIN_MISMATCH: ' + p)
    return raw
class Snap:
    def read(self, ref): return read_exact(ref)
    def doc(self, ref):
        def hook(pairs):
            d = {}
            for k, v in pairs:
                if k in d: refuse('DUPLICATE_KEY')
                d[k] = v
            return d
        return json.loads(read_exact(ref), object_pairs_hook=hook, parse_constant=lambda c: refuse('NONFINITE'))
def validator():
    raw = read_exact(VALIDATOR); m = types.ModuleType('a296_binding_pinned'); m.__file__ = VALIDATOR['path']
    exec(compile(raw, VALIDATOR['path'], 'exec'), m.__dict__); return m
C1_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_C2V002'
def walk_keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(o, list):
        for v in o: yield from walk_keys(v)
def real_c1_checks(s, c1, policy):
    """Hardening outside the pinned validator: the bound C1 is the fill-v003 successor, not a synthetic or draft file."""
    d = s.doc(c1); rv = s.doc(policy)
    if d.get('schema') != C1_SCHEMA: refuse('C1_SCHEMA_NOT_THE_SUCCESSOR: %r' % d.get('schema'))
    fz = d.get('frozen') or {}
    if fz.get('synthetic_test') is not False or fz.get('certificate_policy_review') != policy: refuse('C1_FROZEN_BLOCK')
    if 'placeholder' in d: refuse('C1_IS_A_DRAFT')
    for o, name in ((d, 'C1'), (rv, 'POLICY')):
        if any(k in ('synthetic', 'synthetic_fixture') for k in walk_keys(o)): refuse(name + '_HAS_SYNTHETIC_KEY')
    if rv.get('reviewer_lane') != 'Codex3': refuse('POLICY_REVIEWER_NOT_CODEX3')
def build(c1, policy):
    t = Snap().doc(TEMPLATE)
    if t.get('status') != 'UNBOUND_TEMPLATE' or t.get('c1') is not None or t.get('certificate_policy_review') is not None: refuse('TEMPLATE_UNEXPECTED')
    b = dict(t); b['status'] = 'ROOT_BOUND'; b['c1'] = dict(c1); b['certificate_policy_review'] = dict(policy)
    return b
def main(argv=None):
    ap = argparse.ArgumentParser()
    for a in ('--c1', '--c1-sha256', '--policy', '--policy-sha256', '--out', '--binding', '--binding-sha256'): ap.add_argument(a)
    ap.add_argument('--check-only', action='store_true')
    a = ap.parse_args(argv)
    try:
        H = validator(); s = Snap()
        if a.check_only:
            ref = {'path': a.binding, 'sha256': a.binding_sha256}
        else:
            if not (a.out and os.path.isabs(a.out) and os.path.normpath(a.out) == a.out and a.out.startswith(ART + '/')): refuse('OUT_PATH')
            c1 = {'path': a.c1, 'sha256': a.c1_sha256}; policy = {'path': a.policy, 'sha256': a.policy_sha256}
            read_exact(c1); read_exact(policy); real_c1_checks(s, c1, policy)
            b = build(c1, policy)
            data = (json.dumps(b, indent=1, sort_keys=True) + '\n').encode()
            tmp_ref = {'path': a.out, 'sha256': hashlib.sha256(data).hexdigest()}
            # validate the exact bytes before writing: an in-memory snapshot entry for the not-yet-written file
            class Pre(Snap):
                def doc(self, ref):
                    if ref == tmp_ref: return json.loads(data)
                    return Snap.doc(self, ref)
            H.validate_binding(Pre(), tmp_ref)
            with open(a.out, 'xb') as f: f.write(data)
            ref = tmp_ref
        out = H.validate_binding(s, ref)
        real_c1_checks(s, out['c1'], out['document']['certificate_policy_review'])
        print(json.dumps({'status': 'VALID', 'binding': ref, 'c1': out['c1'], 'policy_review': out['document']['certificate_policy_review'],
                          'n_producers': len(out['tail_readiness']['approved_certificate_producers'])}, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as e:
        print(json.dumps({'status': 'REFUSED', 'reason': '%s: %s' % (type(e).__name__, e)})); return 2
if __name__ == '__main__': raise SystemExit(main())
