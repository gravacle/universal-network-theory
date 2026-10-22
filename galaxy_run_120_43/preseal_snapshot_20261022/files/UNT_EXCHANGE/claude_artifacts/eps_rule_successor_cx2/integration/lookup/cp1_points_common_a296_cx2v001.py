# A296: only the registry bridge pin changes; original list/table rules retained.
# 0828 successor: only the assembler pin changes; c3v005 carries adopted A209 six-producer policy.
"""CP-1 list-of-points common (Claude2 h3_campaign_path_c2, c2v001; V006 A192 item 2; design map section 1 and 3.3).

The CP-1 list-of-points successor is three files: this common, cp1_points_runner_c2v001 and cp1_points_assembler_c2v001.
They load Claude3's c3v004 runner, common and assembler BY PATH AND SHA and never change a byte of them: every stage, check,
gate, producer, format and record is c3v004's.  The only new thing is where the points come from:
  * table mode (no --points-list): the successor CLI is the c3v004 CLI itself (main(argv) of the pinned module), so rows 1-31
    behave byte-identically;
  * list mode (--points-list L --points-list-sha256 H): the rows are a root-written list of point specs, the next wave's
    planned points, as the entry's `points-manifest` writes them (schema H3_CAMPAIGN_POINTS_LIST_C2V003).  Each list row has
    the c3v004 row shape {row, key, label, names, spec_path, spec_sha256, distance_Mpc, q_inf} and is handed to the unchanged
    c3v004 functions (run_point, adapt_point, plan, assemble_bundle, verify_point), which take a row as an argument.
List rules (all before anything runs): the list's bytes hash to H; every point spec is an exact pin under claude_artifacts,
canonical, whose bytes hash to its pin; its key, recomputed from the spec bytes with the core recipe (c3v004
point_identity), equals the listed key; no list key or label is one of the 31 table rows; rows are > 31 and unique; keys are
unique.  The anchor (row 1) is never a list point: list points start only after the anchor's AGREE in the SAME out-root,
exactly as rows 2-31 do (runner c3v004 Scheduler._gate, run_point F6 hold), i.e. a list run continues on CP-1's out-root.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
BUILD = ART + '/s4rc1_c3/build_c3v004'
RUNNER = (BUILD + '/cp1_runner_c3v004.py', '3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48')
COMMON = (BUILD + '/s4rc1_common_c3v004.py', '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083')
ASSEMBLER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_assembler_a296_cx2v002.py', '0f9283b86f47a1382c9c00173d70d8a4fd34fa20664400ca55ed3bbf3c9cf548')
LIST_SCHEMA = 'H3_CAMPAIGN_POINTS_LIST_C2V003'           # h3_campaign_entry_c2v003 points-manifest
RECORDS_SCHEMA = 'CP1_POINTS_LEDGER_RECORDS_C2V001'      # cp1_points_assembler_c2v001 records -> entry ledger-append
LABEL = re.compile(r'[A-Z0-9_]{1,64}')
HEX = re.compile(r'[0-9a-f]{64}')


def load_module(path, sha256, name):
    """A c3v004 module from its exact bytes, registered under `name`; its __file__ is its own path (so its HERE and its
    common load are c3v004's)."""
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise SystemExit('REFUSED: c3v004 pin mismatch: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def pin_of_self(path):
    p = os.path.realpath(path)
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def load_points_list(C, ref):
    """-> (document, rows).  C is the c3v004 common instance of the calling module.  Every refusal is C.Refusal."""
    if not C.is_pin(ref) or not os.path.isabs(ref['path']):
        raise C.Refusal('POINTS_LIST_PIN_REQUIRED: an absolute {path, sha256}')
    raw = C.read_bytes_pinned(ref, (C.ART,), 'points list', max_bytes=None)
    doc = json.loads(raw)
    if not isinstance(doc, dict) or doc.get('schema') != LIST_SCHEMA:
        raise C.Refusal('POINTS_LIST_SCHEMA: %s required' % LIST_SCHEMA)
    wave, pts = doc.get('wave'), doc.get('points')
    if type(wave) is not int or wave < 1 or not isinstance(pts, list) or not 1 <= len(pts) <= 99:
        raise C.Refusal('POINTS_LIST_SHAPE: wave >= 1 and 1..99 points required')
    table = C.point_rows()
    tkeys = {r['key'] for r in table}
    tnames = {n for r in table for n in r['names']}
    rows, keys, nums = [], set(), set()
    for i, p in enumerate(pts):
        where = 'point %d' % i
        if not isinstance(p, dict):
            raise C.Refusal('POINTS_LIST_ITEM_NOT_AN_OBJECT: ' + where)
        row, key, label, spin, theta = p.get('row'), p.get('key'), p.get('label'), p.get('spec'), p.get('theta')
        if type(row) is not int or row <= len(table) or row in nums:
            raise C.Refusal('POINTS_LIST_ROW_MUST_BE_UNIQUE_AND_ABOVE_%d: %s' % (len(table), where))
        if not isinstance(label, str) or LABEL.fullmatch(label) is None or label in tnames:
            raise C.Refusal('POINTS_LIST_LABEL_INVALID_OR_A_TABLE_NAME: %s %r' % (where, label))
        if not isinstance(key, str) or HEX.fullmatch(key) is None or key in keys:
            raise C.Refusal('POINTS_LIST_KEY_INVALID_OR_DUPLICATE: ' + where)
        if key in tkeys:
            raise C.Refusal('POINTS_LIST_KEY_IS_A_31_POINT_TABLE_ROW (use c3v004 table mode): %s %s' % (where, key[:16]))
        if not isinstance(theta, dict) or not theta:
            raise C.Refusal('POINTS_LIST_THETA_REQUIRED: ' + where)
        if not C.is_pin(spin):
            raise C.Refusal('POINTS_LIST_SPEC_PIN_REQUIRED: ' + where)
        C.require_canonical(C.require_policy(spin['path'], (C.ART,), 'list spec'))
        spec = json.loads(C.read_bytes_pinned(spin, (C.ART,), 'list spec', max_bytes=None))
        if C.point_key(spec) != key:
            raise C.Refusal('POINTS_LIST_POINT_KEY_MISMATCH (core recipe from the spec bytes): %s %s' % (where, key[:16]))
        if p.get('pending_spec_sha256') != spin['sha256']:
            raise C.Refusal('POINTS_LIST_PENDING_SPEC_SHA_IS_NOT_THE_SPEC_PIN: ' + where)
        keys.add(key)
        nums.add(row)
        rows.append({'row': row, 'key': key, 'label': label, 'names': [label], 'spec_path': spin['path'],
                     'spec_sha256': spin['sha256'], 'distance_Mpc': (spec.get('physical') or {}).get('distance_Mpc'),
                     'q_inf': None, 'theta': theta, 'pending_spec_sha256': spin['sha256'], 'wave': wave})
    return doc, rows


def select_list_rows(C, rows, selection=None):
    """c3v004 select_points semantics over the list rows only: tokens are a row number, a label or a >= 8-hex key prefix."""
    if not selection:
        return list(rows)
    chosen = set()
    for tok in [t.strip() for t in selection.split(',') if t.strip()]:
        hit = [r for r in rows if tok == str(r['row']) or tok in r['names']
               or (len(tok) >= 8 and re.fullmatch('[0-9a-f]+', tok) and r['key'].startswith(tok))]
        if len(hit) != 1:
            raise C.Refusal('POINT_SELECTION_UNRESOLVED: ' + tok)
        chosen.add(hit[0]['key'])
    return [r for r in rows if r['key'] in chosen]
