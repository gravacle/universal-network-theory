"""Deterministic builder of the C1 successor DRAFT (A298; root 0856 item 3, 0857 item 2). Claude3, root deputy (A292).

From the frozen C1_H1_C2V001 (40159322, read by exact pin), and nothing else:
- tail_readiness.approved_certificate_producers: the six entries unchanged and in order, then the A296 EPS bridge
  point_response_admission_a296_bridge_cx2v002.py (1eb94a51) as entry 7;
- tail_readiness.certificate_policy_review: the explicit placeholder (root fills Codex3's re-signed C1 policy review pin
  at freeze with fill_c1_pin_c2v003_c3v001.py);
- top level: the `frozen` block is removed; schema, status, supersedes, drafted_by, drafted_utc and placeholder are set.
  Every other top-level key and every other tail_readiness field is v001's, value for value.
Same --drafted-utc -> same bytes. Writes two files by exclusive create in a NEW absolute --out-dir; read-only otherwise.
usage: python3 -I -B build_c1_successor_draft_c3v001.py --out-dir /ABS/NEW_DIR --drafted-utc YYYY-MM-DDTHH:MM:SSZ"""
import argparse, copy, hashlib, json, os, re, sys
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
C1 = {'path': ART + '/c1_h1_c2/C1_H1_C2V001.json', 'sha256': '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}
BRIDGE = {'path': ART + '/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py',
          'sha256': '1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'}
OLD_DIGEST_EXCL = '6dc87838fc0e44ff5a8bd8067281644cf2bc2ddab0e367baca180eddeee335aa'
DRAFT_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_DRAFT_C2V003'
SENTINEL = '__PENDING_CERTIFICATE_POLICY_REVIEW_PIN__ (Codex3 re-signs for A298; root fills {path, sha256} at freeze)'
OUT_NAME, DIFF_NAME = 'C1_H1_DRAFT_C2V003.json', 'LEAF_DIFF_C1_H1_DRAFT_C2V003.json'
UTC_RE = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ')
def refuse(code): raise SystemExit('REFUSED ' + code)
def canonical(o): return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def digest(o): return hashlib.sha256(canonical(o)).hexdigest()
def pinned(ref):
    if os.path.islink(ref['path']) or os.path.realpath(ref['path']) != ref['path']: refuse('PIN_PATH_NOT_CANONICAL')
    raw = open(ref['path'], 'rb').read()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']: refuse('PIN_MISMATCH ' + ref['path'])
    return raw
def flat(o, pre=''):
    if isinstance(o, dict) and o:
        r = {}
        for k, v in o.items(): r.update(flat(v, pre + k + '.'))
        return r
    if isinstance(o, list) and o:
        r = {}
        for i, v in enumerate(o): r.update(flat(v, pre + '[%d].' % i))
        return r
    return {pre[:-1]: o}
def excl(tr): return {k: v for k, v in tr.items() if k != 'certificate_policy_review'}
def build(c1_raw, drafted_utc):
    if not UTC_RE.fullmatch(drafted_utc): refuse('NONCANONICAL_UTC')
    if hashlib.sha256(c1_raw).hexdigest() != C1['sha256']: refuse('C1_PIN_MISMATCH')
    old = json.loads(c1_raw)
    otr = old['tail_readiness']
    if digest(excl(otr)) != OLD_DIGEST_EXCL: refuse('OLD_DIGEST_RULE_DOES_NOT_REPRODUCE')
    six = otr['approved_certificate_producers']
    if len(six) != 6 or any(set(p) != {'path', 'sha256'} for p in six) or BRIDGE in six: refuse('OLD_SIX_UNEXPECTED')
    new = copy.deepcopy(old)
    new.pop('frozen')
    tr = new['tail_readiness']
    tr['approved_certificate_producers'] = copy.deepcopy(six) + [dict(BRIDGE)]
    tr['certificate_policy_review'] = SENTINEL
    dig = digest(excl(tr))
    new['schema'] = DRAFT_SCHEMA
    new['status'] = ('DRAFT_FOR_ROOT (v003; A296-A298, root 0856 item 3 and 0857 item 2): complete except '
                     'tail_readiness.certificate_policy_review (explicit placeholder). Not frozen, not an approval. '
                     'tail_readiness is C1_H1_C2V001\'s, value for value, except that approved_certificate_producers gains the '
                     'A296 EPS bridge 1eb94a51 as entry 7 (digest without the review %s).' % dig[:8])
    new['supersedes'] = {'c1': dict(C1), 'changes': [
        'tail_readiness.approved_certificate_producers: the six C1_H1_C2V001 entries unchanged and in order, then the A296 '
        'EPS bridge point_response_admission_a296_bridge_cx2v002.py (1eb94a51) as entry 7 (A298; root 0856 item 3)',
        'tail_readiness.certificate_policy_review: the placeholder; root fills Codex3\'s re-signed C1 policy review '
        '(guard_sha256 3939bc47, the ordered seven) at freeze',
        'the frozen block is removed (root writes a new one at freeze); placeholder names the v003 fill tool',
        'every other tail_readiness field and every other top-level field: no change']}
    new['drafted_by'] = ('Claude3 (root deputy, A292; root 0857 item 2), by build_c1_successor_draft_c3v001.py from the '
                         'pinned C1_H1_C2V001; root rules and freezes')
    new['drafted_utc'] = drafted_utc
    new['placeholder'] = {
        'c1_tail_readiness_digest_excluding_review': dig,
        'digest_rule': 'sha256 of canonical JSON (sort_keys, separators (",",":"), allow_nan False) of tail_readiness '
                       'without certificate_policy_review',
        'fill_tool': 'fill_c1_pin_c2v003_c3v001.py (constants-only successor of fill_c1_pin_c2v002 3faf4a6c), published '
                     'beside this draft',
        'fill_with': '{path, sha256} of Codex3\'s signed DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001 under '
                     'claude_artifacts/cert_policy_reviews_cx3/ that binds guard_sha256 3939bc47 and the ordered seven',
        'key': 'tail_readiness.certificate_policy_review',
        'value_now': SENTINEL,
        'why_not_null': old.get('placeholder', {}).get('why_not_null') or
                        'explicit; a non-dict reads CERTIFICATE_POLICY_PENDING in the wrapper and the verifier alike'}
    # scope check: exactly the declared leaves change
    fa, fb = flat(old), flat(new)
    changed = sorted(k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>'))
    allowed_prefix = ('frozen.', 'placeholder.', 'supersedes.', 'tail_readiness.approved_certificate_producers.[6].',
                      'tail_readiness.certificate_policy_review')
    allowed_exact = {'schema', 'status', 'drafted_by', 'drafted_utc'}
    if any(not (k in allowed_exact or k.startswith(allowed_prefix)) for k in changed): refuse('LEAF_DIFF_SCOPE')
    if excl(tr) != dict(excl(otr), approved_certificate_producers=six + [BRIDGE]): refuse('TAIL_SCOPE')
    raw = json.dumps(new, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'
    diff = {'schema': 'LEAF_DIFF_C1_H1_DRAFT_C2V003_C3V001', 'base': dict(C1), 'draft_sha256': hashlib.sha256(raw).hexdigest(),
            'c1_tail_readiness_digest_excluding_review': dig, 'old_digest_excluding_review': OLD_DIGEST_EXCL,
            'n_changed': len(changed), 'changed_leaves': changed,
            'tail_changed_leaves': [k for k in changed if k.startswith('tail_readiness.')]}
    return raw, (json.dumps(diff, sort_keys=True, indent=1) + '\n').encode(), dig
def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--out-dir', required=True); ap.add_argument('--drafted-utc', required=True)
    a = ap.parse_args(argv)
    if not os.path.isabs(a.out_dir) or os.path.normpath(a.out_dir) != a.out_dir: refuse('OUT_DIR_MUST_BE_ABSOLUTE_NORMAL')
    if not (a.out_dir == ART or a.out_dir.startswith(ART + '/')): refuse('OUT_DIR_OUTSIDE_CLAUDE_ARTIFACTS')
    pinned(BRIDGE)
    raw, draw, dig = build(pinned(C1), a.drafted_utc)
    try: os.mkdir(a.out_dir)
    except FileExistsError: refuse('OUT_DIR_MUST_BE_NEW')
    for name, data in ((OUT_NAME, raw), (DIFF_NAME, draw)):
        with open(os.path.join(a.out_dir, name), 'xb') as f: f.write(data)
    print(json.dumps({'status': 'WRITTEN', 'draft': {'path': os.path.join(a.out_dir, OUT_NAME), 'sha256': hashlib.sha256(raw).hexdigest()},
                      'c1_tail_readiness_digest_excluding_review': dig}))
if __name__ == '__main__': main()
