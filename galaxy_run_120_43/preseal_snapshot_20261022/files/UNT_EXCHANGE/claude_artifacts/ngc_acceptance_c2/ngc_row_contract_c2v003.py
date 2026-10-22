"""NGC row contract builder c2v003 (V006 A162 item 3; A155 S8 as amended; A153 S7/S8). Root build (Claude2 workflow);
nothing here is adopted until root rules and Claude3 reviews c2v003. The S10 row-reference policy review of the contract
is Codex1's (A162 item 3), single pass, bound to the contract's sha256.

A162 item 3, verbatim: "The NGC row contract (A155 S8 amended) is built by root from the manifest `a2936517` radii and
order: query ids, R_i, rule id TI_B_SCALE_R_V001, θ hex, c hex. **One contract.**"

Output NGC_ROW_CONTRACT_C2V001.json, the shape adapter c2v002 check_row_contract reads (schema
UNT_NGC_LO_ROW_CONTRACT_C2V002, exact keys):
  schema, query_ids (manifest order), manifest {path, sha256 a2936517}, manifest_radius_scale 1.0,
  R_m[i] = float(Rad_text_i) * KPC_M          (the driver's own query-row arithmetic, cx3r008 L5215, KPC_M L183),
  rule_id TI_B_SCALE_R_V001, theta_hex 0x1.ce9660bc22098p-29, c_hex = float.hex(299792458.0), binding null.
It holds NO velocity, NO t_i, NO sigma, NO tau, NO eps and NO N_min (A155 S8 amended; adapter token scan).
The manifest is the target-free query manifest (NGC_DATA['manifest'] of the driver, L4297): it is read for ids, radii and
order only (its emitted columns are data_row_index, query_id, source_line_number, Rad_text, Rad_unit; no velocity column).
Self-check before writing: the adapter c2v002's own check_row_contract on the REGISTERED registry must read BOUND.
U-b3 (whether a call's S7 column-mean radii equal these bits) stays UNTESTED; deciding test: the first NGC acceptance
(the adapter's bitwise S7 check reads NGC_ROW_CONTRACT_MISMATCH, never a PASS, if they differ).
Usage: python3 -I -B ngc_row_contract_c2v003.py --out-dir <dir>   (writes NGC_ROW_CONTRACT_C2V001.json and its build record)
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
MANIFEST = {'path': CTRL + '/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json',
            'sha256': 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'}   # driver NGC_DATA['manifest']
MANIFEST_SCHEMA = 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001'
MANIFEST_COLUMNS = ['data_row_index', 'query_id', 'source_line_number', 'Rad_text', 'Rad_unit']
ADAPTER = (os.path.join(HERE, 'ngc_lo_state_adapter_c2v002.py'),
           'ce33b526c38490687744d6b9a4b383cb540c1af6a8da7d8d4f0298807ce43047')
V006 = CTRL + '/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
A155 = {'heading': '## A155', 'section_sha256': 'ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d'}
A162 = {'heading': '## A162', 'section_sha256': '49ef90da0bf2de4237c241aef2dd275ca51f794513c72357d362896dc1fa902d'}
KPC_M = 3.085677581491367e19                              # driver cx3r008 L183
SCHEMA = 'UNT_NGC_LO_ROW_CONTRACT_C2V002'                 # adapter c2v002 ROW_CONTRACT_SCHEMA
RULE_ID = 'TI_B_SCALE_R_V001'                             # A155
THETA_HEX = '0x1.ce9660bc22098p-29'                       # A155 / E_A155_1 item 7
C_M_S = 299792458.0
N_ROWS = 43
CONTRACT_NAME = 'NGC_ROW_CONTRACT_C2V001.json'
BUILD_RECORD_NAME = 'NGC_ROW_CONTRACT_C2V001_BUILD_RECORD_C2V003.json'
BUILD_SCHEMA = 'UNT_NGC_ROW_CONTRACT_BUILD_RECORD_C2V003'


class Refusal(ValueError):
    pass


def need(ok, msg):
    if not ok:
        raise Refusal(msg)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def section_bytes(raw, heading):
    lines = raw.split(b'\n')
    hits = [i for i, ln in enumerate(lines) if ln.startswith(heading.encode() + b':') or ln == heading.encode()]
    if len(hits) != 1:
        return None
    j = hits[0] + 1
    while j < len(lines) and not lines[j].startswith(b'## '):
        j += 1
    return b'\n'.join(lines[hits[0]:j])


def strict(raw, label):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(Refusal('NONFINITE')))


def build_contract(manifest_pin=None):
    """The contract dict from the manifest bytes (exact pin). Refuses anything but the target-free manifest shape."""
    mp = dict(MANIFEST if manifest_pin is None else manifest_pin)
    with open(mp['path'], 'rb') as f:
        raw = f.read()
    need(sha(raw) == mp['sha256'], 'MANIFEST_BYTE_PIN_MISMATCH')
    man = strict(raw, 'manifest')
    need(isinstance(man, dict) and man.get('schema') == MANIFEST_SCHEMA, 'MANIFEST_SCHEMA')
    need(man.get('emitted_columns') == MANIFEST_COLUMNS and man.get('no_other_columns_emitted') is True,
         'MANIFEST_COLUMNS (ids and radii only; no velocity column)')
    rows = man.get('rows')
    need(isinstance(rows, list) and len(rows) == N_ROWS, 'MANIFEST_ROW_COUNT')
    ids, R = [], []
    for i, r in enumerate(rows):
        need(isinstance(r, dict) and sorted(r) == sorted(MANIFEST_COLUMNS), 'MANIFEST_ROW_KEYS %d' % i)
        need(r['query_id'] == 'NGC3198-Q%02d' % (i + 1), 'MANIFEST_ORDER %d' % i)
        need(r['Rad_unit'] == 'kpc' and isinstance(r['Rad_text'], str), 'MANIFEST_RADIUS_UNIT %d' % i)
        x = float(r['Rad_text']) * KPC_M                                  # driver L5215
        need(math.isfinite(x) and x > 0, 'MANIFEST_RADIUS %d' % i)
        ids.append(r['query_id'])
        R.append(x)
    return {'schema': SCHEMA, 'query_ids': ids, 'manifest': mp, 'manifest_radius_scale': 1.0, 'R_m': R,
            'rule_id': RULE_ID, 'theta_hex': THETA_HEX, 'c_hex': C_M_S.hex(), 'binding': None}


def _load_adapter():
    with open(ADAPTER[0], 'rb') as f:
        raw = f.read()
    need(sha(raw) == ADAPTER[1], 'ADAPTER_PIN_MISMATCH')
    spec = importlib.util.spec_from_file_location('ngc_row_contract_c2v003_adapter', ADAPTER[0])
    mod = importlib.util.module_from_spec(spec)
    sys.modules['ngc_row_contract_c2v003_adapter'] = mod
    exec(compile(raw, ADAPTER[0], 'exec'), mod.__dict__)
    return mod


def check_against_sources():
    """theta hex and rule id verbatim in the pinned A155 section; the A162 section pinned; the adapter's constants agree."""
    with open(V006, 'rb') as f:
        raw = f.read()
    out = {}
    for name, pin in (('A155', A155), ('A162', A162)):
        sec = section_bytes(raw, pin['heading'])
        need(sec is not None and sha(sec) == pin['section_sha256'], name + '_SECTION_NOT_FOUND_OR_CHANGED')
        out[name] = dict(pin, path=V006)
        if name == 'A155':
            need(RULE_ID.encode() in sec and THETA_HEX.encode() in sec, 'A155_RULE_OR_THETA_NOT_VERBATIM')
    A = _load_adapter()
    need(A.RULE_ID == RULE_ID and A.THETA_HEX == THETA_HEX and A.C_HEX == C_M_S.hex() and A.ROW_CONTRACT_SCHEMA == SCHEMA
         and A.MANIFEST == MANIFEST and tuple(A.CONTRACT_KEYS) == ('schema', 'query_ids', 'manifest', 'manifest_radius_scale',
                                                                   'R_m', 'rule_id', 'theta_hex', 'c_hex', 'binding'),
         'ADAPTER_C2V002_CONSTANTS_DISAGREE')
    return A, out


def adapter_check(A, contract_pin):
    """The adapter c2v002's own S8 check on the REGISTERED registry (binding null: no point or call is read)."""
    reg = A.real_registry()
    c, csha, status, detail = A.check_row_contract(contract_pin, reg, A.make_reader(reg), None, None, A.RULE_ID)
    need(status == 'BOUND' and csha == contract_pin['sha256'], 'ADAPTER_CHECK_NOT_BOUND: %s %s' % (status, detail))
    return status


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args(argv)
    out = os.path.realpath(a.out_dir)
    need(os.path.isdir(out), 'OUT_DIR_MISSING')
    A, sources = check_against_sources()
    contract = build_contract()
    raw = (json.dumps(contract, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    back = json.loads(raw)
    need(back == contract and all(float(x).hex() == float(y).hex() for x, y in zip(back['R_m'], contract['R_m'])),
         'CONTRACT_JSON_ROUND_TRIP')
    p = os.path.join(out, CONTRACT_NAME)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    pin = {'path': p, 'sha256': sha(raw)}
    status = adapter_check(A, pin)
    with open(os.path.realpath(__file__), 'rb') as f:
        me = {'path': os.path.realpath(__file__), 'sha256': sha(f.read())}
    rec = {'schema': BUILD_SCHEMA, 'builder': me, 'contract': pin, 'manifest': dict(MANIFEST), 'sources': sources,
           'adapter': {'path': ADAPTER[0], 'sha256': ADAPTER[1]}, 'adapter_check_row_contract': status,
           'radius_rule': 'R_m[i] = float(Rad_text_i) * 3.085677581491367e19 (driver cx3r008 L5215, KPC_M L183); '
                          'manifest_radius_scale 1.0',
           'never': 'no velocity, t_i, sigma, tau, eps or N_min; ids, radii and order only',
           'U_b3': 'UNTESTED: whether a call S7 column-mean query-support radii equal these bits; deciding test: the first '
                   'NGC acceptance (bitwise S7 check; a mismatch reads NGC_ROW_CONTRACT_MISMATCH, never a PASS)',
           'S10': 'row-reference policy review: Codex1, single pass, bound to this contract sha256 (A162 item 3)'}
    rraw = (json.dumps(rec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    rp = os.path.join(out, BUILD_RECORD_NAME)
    fd = os.open(rp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(rraw)
    print(json.dumps({'contract': pin, 'build_record': {'path': rp, 'sha256': sha(rraw)}, 'adapter_check': status}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
