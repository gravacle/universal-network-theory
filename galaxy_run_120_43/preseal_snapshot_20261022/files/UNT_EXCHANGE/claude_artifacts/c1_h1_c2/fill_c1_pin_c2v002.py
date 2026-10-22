"""Fill C1 (H1) from draft C2V002: set tail_readiness.certificate_policy_review to the signed review's {path, sha256},
after checking every binding from bytes. Nothing else in tail_readiness changes. Writes one file by exclusive create;
read-only otherwise. The written C1 becomes the frozen C1 when root records it in V006 after the c3v005 verify of record
passes (A209 item 4; A134 Q9(b)3). Never edit it.

v002 = v001 (680a27f4) hardened per A209 item 6 (verifier N2/N3/N5):
- `ok` must be the JSON boolean true (`is True`), and every binding and custody field is compared as canonical JSON bytes
  (sort_keys, separators (',', ':'), allow_nan False). So 1 never equals true, 1.0 never equals 1, and list order counts.
- The review and Codex3's check script: canonical absolute path under claude_artifacts (real mode), no symlink component,
  no component that contains ngc3198 or starts with uvt_ (case-folded), a regular file with one link, at most 8 MiB, sha256
  from bytes. Lexical checks run before anything is opened. The draft and the output path get the same path checks.
- JSON is parsed strictly: a duplicate key, NaN or Infinity refuses.
- Real mode refuses any key named `synthetic` or `synthetic_fixture` at any depth, and any template marker.
- --synthetic-test needs --synthetic-root (an existing canonical folder outside claude_artifacts) in place of
  claude_artifacts, and writes schema UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002, never the C1 schema.

python3 -I -B fill_c1_pin_c2v002.py --draft D --draft-sha256 H --review R --review-sha256 H --out OUT \
    --utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
Exit 0: written. Exit 2: refused, and nothing was written.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import sys

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
EIGHT_MIB = 8 * 1024 * 1024
DRAFT_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_DRAFT_C2V002'
C1_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_C2V001'
SYNTHETIC_SCHEMA = 'UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002'
TR_DIGEST_EXCLUDING_REVIEW = '6dc87838fc0e44ff5a8bd8067281644cf2bc2ddab0e367baca180eddeee335aa'   # draft v001 = v002
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'           # core dc895f8a; guard011 L10
GUARD_PIN = {'path': ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py',
             'sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'}         # wrapper q5b1 L30
SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'                            # wrapper q5b1 L74
HANDOFF = 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'                                                   # wrapper q5b1 L75
POLICY_SCHEMA = 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001'                                        # wrapper q5b1 L40
SENTINEL_PREFIX = '__PENDING_CERTIFICATE_POLICY_REVIEW_PIN__'
CHECK_IDS = tuple('C%02d' % i for i in range(1, 13))                                              # request v002 section 3
UTC_RE = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ')
TEMPLATE_MARKERS = ('<FILL', 'TEMPLATE_NOT_A_REVIEW')
SYNTHETIC_KEYS = ('synthetic', 'synthetic_fixture')


class Refused(Exception):
    pass


def need(cond, code):
    if not cond:
        raise Refused(code)


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(o):
    return hashlib.sha256(canonical(o)).hexdigest()


def same(a, b):
    """Canonical-bytes equality (A209 item 6): 1 != true, 1.0 != 1, order of lists counts."""
    try:
        return canonical(a) == canonical(b)
    except (TypeError, ValueError):
        return False


def _pairs(items):
    d = {}
    for k, v in items:
        need(k not in d, 'DUPLICATE_JSON_KEY: ' + str(k))
        d[k] = v
    return d


def _no_constant(s):
    raise Refused('NONFINITE_JSON: ' + s)


def strict_json(raw, label):
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=_no_constant)
    except (UnicodeDecodeError, ValueError) as exc:
        raise Refused('JSON_INVALID: %s: %s' % (label, exc))


def lexical(path, root, label):
    """Checks that need no filesystem access: absolute, normalized, inside root, no ngc3198 or uvt_ component."""
    need(isinstance(path, str) and os.path.isabs(path), 'PATH_NOT_ABSOLUTE: ' + label)
    need(os.path.normpath(path) == path and '/./' not in path + '/' and '/../' not in path + '/', 'PATH_NOT_NORMALIZED: ' + label)
    for comp in path.split('/'):
        f = comp.casefold()
        need('ngc3198' not in f, 'NGC3198_COMPONENT_REFUSED: ' + label)
        need(not f.startswith('uvt_'), 'UVT_COMPONENT_REFUSED: ' + label)
    need(path.startswith(root.rstrip('/') + '/'), 'OUTSIDE_ALLOWED_ROOT %s: %s' % (root, label))


def no_symlink_component(path, label):
    parts = path.split('/')
    for i in range(2, len(parts) + 1):
        prefix = '/'.join(parts[:i])
        need(not stat.S_ISLNK(os.lstat(prefix).st_mode), 'SYMLINK_COMPONENT: ' + label)
    need(os.path.realpath(path) == path, 'NONCANONICAL_PATH: ' + label)


def read_file(pin_path, sha, root, label):
    """Lexical checks, then no symlink component, regular file, one link, <= 8 MiB, sha256 from the bytes read."""
    lexical(pin_path, root, label)
    no_symlink_component(pin_path, label)
    st = os.lstat(pin_path)
    need(stat.S_ISREG(st.st_mode), 'NOT_A_REGULAR_FILE: ' + label)
    need(st.st_nlink == 1, 'NOT_A_SINGLE_LINK_FILE: ' + label)
    need(st.st_size <= EIGHT_MIB, 'FILE_EXCEEDS_8_MIB: ' + label)
    with open(pin_path, 'rb') as f:
        raw = f.read(EIGHT_MIB + 1)
    need(len(raw) == st.st_size and len(raw) <= EIGHT_MIB, 'FILE_CHANGED_WHILE_READING: ' + label)
    need(isinstance(sha, str) and hashlib.sha256(raw).hexdigest() == sha, 'SHA_MISMATCH: ' + label)
    return raw


def walk_keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk_keys(v)


def walk_strings(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from walk_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk_strings(v)
    elif isinstance(o, str):
        yield o


def is_pin(x):
    return (isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str)
            and isinstance(x['sha256'], str) and re.fullmatch('[0-9a-f]{64}', x['sha256']) is not None)


def check_review(rv, tr, *, draft_pin, tr_digest, synthetic):
    """Every content check on the parsed review. Returns nothing; raises Refused. Importable for unit tests."""
    need(isinstance(rv, dict), 'REVIEW_NOT_AN_OBJECT')
    need(not any(m in s for s in walk_strings(rv) for m in TEMPLATE_MARKERS), 'REVIEW_IS_AN_UNFILLED_TEMPLATE')
    if synthetic:
        need(isinstance(rv.get('synthetic'), str) and rv['synthetic'], 'SYNTHETIC_TEST_NEEDS_A_SYNTHETIC_REVIEW')
    else:
        need(not any(k in SYNTHETIC_KEYS for k in walk_keys(rv)), 'SYNTHETIC_KEY_IN_REVIEW')
        need(same(rv.get('reviewer_lane'), 'Codex3'), 'REVIEWER_NOT_CODEX3')
    # the seven bindings (wrapper q5b1 L70-75 via core checked_gate L66-82; final-spec producer v004 L747-756; verify c3v005
    # L380-388) plus schema, status and ok, compared as canonical bytes
    want = {'schema': POLICY_SCHEMA, 'status': 'TESTED', 'ok': True, 'driver_sha256': DRIVER_SHA,
            'custody_deriver': tr['custody_deriver'], 'state_enumerator': tr['state_enumerator'],
            'approved_certificate_producers': tr['approved_certificate_producers'], 'guard_sha256': GUARD_PIN['sha256'],
            'driver_slot_rule': SLOT_RULE, 'post_state_handoff': HANDOFF}
    bad = [k for k, v in want.items() if k not in rv or not same(rv[k], v)]
    need(not bad, 'REVIEW_BINDING_MISMATCH: ' + ','.join(bad))
    need(rv['ok'] is True, 'REVIEW_OK_IS_NOT_TRUE')
    # root custody fields (request v002 section 2b-2c)
    custody = {'c1_tail_readiness_digest_excluding_review': tr_digest, 'reviewed_c1_draft': draft_pin,
               'blocking_findings': [], 'distinct_from_producer_lane': True,
               'certificate_registry': tr['certificate_registry'],
               'trusted_source_producers': tr['trusted_source_producers'],
               'trusted_row_policy_review_sha256': tr['trusted_row_policy_review_sha256']}
    bad = [k for k, v in custody.items() if k not in rv or not same(rv[k], v)]
    need(not bad, 'REVIEW_CUSTODY_MISMATCH: ' + ','.join(bad))
    need(isinstance(rv.get('signed_utc'), str) and UTC_RE.fullmatch(rv['signed_utc']) is not None, 'REVIEW_SIGNED_UTC_MISSING')
    checks = rv.get('checks')
    need(isinstance(checks, list) and checks and all(isinstance(c, dict) and isinstance(c.get('id'), str)
                                                     and c.get('result') in ('PASS', 'FAIL') for c in checks),
         'REVIEW_CHECKS_MALFORMED')
    need(all(c['result'] == 'PASS' for c in checks), 'REVIEW_HAS_A_FAILED_CHECK')
    need(set(CHECK_IDS) <= {c['id'] for c in checks}, 'REVIEW_CHECKS_MISSING: ' +
         ','.join(sorted(set(CHECK_IDS) - {c['id'] for c in checks})))
    need(isinstance(rv.get('files_opened'), list) and all(isinstance(x, str) for x in rv['files_opened']),
         'REVIEW_FILES_OPENED_MISSING')
    need(is_pin(rv.get('check_script')), 'REVIEW_CHECK_SCRIPT_PIN_MISSING')


def main(argv=None):
    ap = argparse.ArgumentParser()
    for a in ('--draft', '--draft-sha256', '--review', '--review-sha256', '--out', '--utc'):
        ap.add_argument(a, required=True)
    ap.add_argument('--synthetic-test', action='store_true')
    ap.add_argument('--synthetic-root')
    a = ap.parse_args(argv)
    try:
        need(UTC_RE.fullmatch(a.utc) is not None, 'UTC_FORMAT')
        if a.synthetic_test:
            root = a.synthetic_root
            need(isinstance(root, str) and os.path.isabs(root) and os.path.normpath(root) == root, 'SYNTHETIC_ROOT_REQUIRED')
            need(not (root == ART or root.startswith(ART + '/')), 'SYNTHETIC_ROOT_INSIDE_CLAUDE_ARTIFACTS')
            need(os.path.isdir(root) and os.path.realpath(root) == root, 'SYNTHETIC_ROOT_MUST_EXIST_AND_BE_CANONICAL')
        else:
            need(a.synthetic_root is None, 'SYNTHETIC_ROOT_ONLY_WITH_SYNTHETIC_TEST')
            root = ART
        lexical(a.out, root, 'out')                                  # before anything is opened
        lexical(a.draft, root, 'draft')
        lexical(a.review, root, 'review')
        draft_raw = read_file(a.draft, a.draft_sha256, root, 'draft')
        rv_raw = read_file(a.review, a.review_sha256, root, 'review')
        read_file(GUARD_PIN['path'], GUARD_PIN['sha256'], ART, 'guard b1')
        draft = strict_json(draft_raw, 'draft')
        rv = strict_json(rv_raw, 'review')
        need(isinstance(draft, dict) and draft.get('schema') == DRAFT_SCHEMA, 'DRAFT_SCHEMA')
        tr = draft.get('tail_readiness')
        need(isinstance(tr, dict), 'DRAFT_TAIL_READINESS')
        need(isinstance(tr.get('certificate_policy_review'), str)
             and tr['certificate_policy_review'].startswith(SENTINEL_PREFIX), 'DRAFT_PLACEHOLDER_ABSENT')
        dig = digest({k: v for k, v in tr.items() if k != 'certificate_policy_review'})
        need(dig == TR_DIGEST_EXCLUDING_REVIEW, 'DRAFT_TAIL_READINESS_DIGEST_IS_NOT_6DC87838')
        need(same((draft.get('placeholder') or {}).get('c1_tail_readiness_digest_excluding_review'), dig), 'DRAFT_DIGEST_DRIFT')
        draft_pin = {'path': a.draft, 'sha256': a.draft_sha256}
        check_review(rv, tr, draft_pin=draft_pin, tr_digest=dig, synthetic=a.synthetic_test)
        cs = rv['check_script']
        read_file(cs['path'], cs['sha256'], root if a.synthetic_test else ART + '/cert_policy_reviews_cx3', 'check script')
        out_dir = os.path.dirname(a.out)
        need(os.path.isdir(out_dir), 'OUT_DIR_MISSING')
        no_symlink_component(out_dir, 'out dir')
        out = json.loads(json.dumps(draft))
        review_pin = {'path': a.review, 'sha256': a.review_sha256}
        out['tail_readiness']['certificate_policy_review'] = review_pin
        out.pop('placeholder')
        with open(os.path.realpath(__file__), 'rb') as f:
            tool_pin = {'path': os.path.realpath(__file__), 'sha256': hashlib.sha256(f.read()).hexdigest()}
        if a.synthetic_test:
            out['schema'] = SYNTHETIC_SCHEMA
            out['status'] = 'SYNTHETIC_TEST_NOT_C1: a fill-tool test output. Never pin, cite, copy into a config or publish it.'
            out['synthetic_fixture'] = 'fill_c1_pin_c2v002 --synthetic-test output; not a C1'
        else:
            out['schema'] = C1_SCHEMA
            out['status'] = ('C1 (H1), filled from the signed review. It is the frozen C1 once root records it in V006 after '
                             'the registry_assembler_c3v005 verify of record passes 31/31 (A209 item 4; A134 Q9(b)3). '
                             'Never edited (A134 Q9).')
        out['frozen'] = {'utc': a.utc, 'from_draft': draft_pin, 'certificate_policy_review': review_pin,
                         'check_script': cs, 'fill_tool': tool_pin, 'synthetic_test': bool(a.synthetic_test),
                         'c1_tail_readiness_digest_excluding_review': dig,
                         'c1_tail_readiness_digest': digest(out['tail_readiness'])}
        need({k: v for k, v in out['tail_readiness'].items() if k != 'certificate_policy_review'} ==
             {k: v for k, v in tr.items() if k != 'certificate_policy_review'}, 'TAIL_READINESS_WOULD_CHANGE')
        data = json.dumps(out, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'
        with open(a.out, 'xb') as f:
            f.write(data)
        print(json.dumps({'status': 'WRITTEN', 'schema': out['schema'],
                          'c1': {'path': a.out, 'sha256': hashlib.sha256(data).hexdigest()},
                          'c1_tail_readiness_digest': out['frozen']['c1_tail_readiness_digest']}))
        return 0
    except (Refused, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': '%s: %s' % (type(exc).__name__, exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
