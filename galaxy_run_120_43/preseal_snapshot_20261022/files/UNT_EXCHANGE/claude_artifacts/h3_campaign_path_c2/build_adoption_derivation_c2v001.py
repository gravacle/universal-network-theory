"""Build the C4-6 adoption derivation of the campaign config at the verdict (Claude2 h3_campaign_path_c2, c2v001; V006 A188).

The adoption gate (parent c75a889f check_adoption L1828-1926, plus wrapper q5b1 L213-227) needs a pinned document that names
what the config regenerates from the adopted case.  Every field is read from bytes; nothing is chosen here:
  * verdict_artifact_sha256, adopted_case_id, adopted_call_spec_sha256, compare_sha256, sealed_prereg_sha256: the numerics
    gate's own `adopted` record of the CANDIDATE config (it must pass);
  * base_spec_sha256, seed_spec_sha256: the candidate Context (the seed spec carries the registry's certificate slots);
  * capability_evidence_sha256, certificate_registry, driver_sha256: the candidate config / the wrapper's driver pin;
  * timing_model: a new document {adopted_call_spec_sha256, base_spec_sha256, wall_rule_record} naming root's FINAL wall rule
    record (A140 N4 / A177 / Claude4 0243 N2; W1_RUN_SHEET section 2);
  * source_receipts: root's list of {case_id, path, sha256}; each case must be a grid case of the numerics gate and each
    receipt must verify with the pinned monitor as that case's FINISHED / COMPLETED receipt (the parent's own rule L1881-1899);
    the adopted case is required (L1909-1910);
  * per_call (wall, RSS, output) and disk_guard.per_call_bytes: the candidate config's values; each cap must be above the
    largest measured use of the receipts (L1913-1918) and the guard at or above the largest output (L1923-1924), else refused;
  * disk_guard.measured_per_call_bytes = the largest final / peak output over those receipts (L1905-1908; run sheet section 3,
    C4-6).  The config must carry the same value: the printed delta sets it with adoption_derivation in one apply step.
The candidate is the H3 config with every field except adoption_derivation and measured_per_call_bytes (apply_h3_fields).
usage: python3 -I -B build_adoption_derivation_c2v001.py --entry E --entry-sha256 H --config CANDIDATE --config-sha256 H
          --wall-rule-record R --wall-rule-record-sha256 H --source-receipt CASE PATH SHA256 [...] --out-dir NEW_DIR
Writes TIMING_MODEL_H3.json, ADOPTION_DERIVATION_H3.json and ADOPTION_DELTA_H3.json into NEW_DIR (exclusive create).
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

NEEDED_GATES = ('numerics_verdict', 'deciding_test', 'driver_capability', 'certificate_policy')


class Refused(Exception):
    pass


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def load_entry(path, sha256):
    raw = Path(path).read_bytes()
    if sha_b(raw) != sha256:
        raise Refused('ENTRY_PIN_MISMATCH')
    sp = importlib.util.spec_from_file_location('_h3_derivation_entry', path)
    E = importlib.util.module_from_spec(sp)
    exec(compile(raw, str(path), 'exec'), E.__dict__)
    M = E.load_wrapper()
    E.check_patch(M)
    return E, M


def finite_positive(x):
    return type(x) in (int, float) and math.isfinite(x) and x > 0


def write_x(path, obj):
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return {'path': str(Path(path).resolve()), 'sha256': sha_b(raw)}


def build(M, *, config_path, config_sha256, wall_rule, receipts, out_dir):
    O = M.O
    raw = Path(config_path).read_bytes()
    if sha_b(raw) != config_sha256:
        raise Refused('CONFIG_PIN_MISMATCH')
    cfg = json.loads(raw)
    ctx = M.Context(config_path)
    bad = [k for k in NEEDED_GATES if not ctx.gates.get(k, {}).get('ok')]
    if bad:
        raise Refused('CANDIDATE_GATES_NOT_PASSED: %s' % bad)
    if O.sha256_bytes(Path(wall_rule['path']).read_bytes()) != wall_rule['sha256']:
        raise Refused('WALL_RULE_RECORD_PIN_MISMATCH')
    ng = ctx.gates['numerics_verdict']
    ad, inputs = ng['adopted'], ng.get('grid_case_inputs') or {}
    used = {'elapsed_seconds': 0.0, 'peak_rss_bytes': 0, 'output_bytes': 0}
    rs, seen = [], set()
    for case_id, path, sha in receipts:
        inp = inputs.get(case_id)
        if inp is None:
            raise Refused('SOURCE_RECEIPT_CASE_NOT_ON_THE_ADOPTED_GRID: %s' % case_id)
        O.read_pinned({'path': path, 'sha256': sha}, 'source receipt %s' % case_id)
        v = ctx.M.verify_receipt(path, spec_sha256=inp['call_spec_sha256'], driver_sha256=inp['driver_sha256'])
        rc = v.get('receipt') or {}
        if not v.get('ok') or rc.get('status') != 'FINISHED' or rc.get('driver_status') != 'COMPLETED' or \
                (rc.get('result') or {}).get('sha256') != inp['result_sha256']:
            raise Refused('SOURCE_RECEIPT_NOT_THE_VERDICT_INPUT: %s (%s)' % (case_id, v.get('reasons')))
        for k in ('elapsed_seconds', 'peak_rss_bytes'):
            if finite_positive(rc.get(k)):
                used[k] = max(used[k], rc[k])
        for k in ('final_output_bytes', 'peak_output_bytes'):
            if finite_positive(rc.get(k)):
                used['output_bytes'] = max(used['output_bytes'], rc[k])
        seen.add(case_id)
        rs.append({'case_id': case_id, 'path': path, 'sha256': sha})
    if ad['case_id'] not in seen:
        raise Refused('ADOPTED_CASE_RECEIPT_REQUIRED: %s' % ad['case_id'])
    pc, dg = cfg['per_call'], cfg['disk_guard']
    caps = {k: pc[k] for k in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')}
    low = [k for k, uk in zip(caps, ('elapsed_seconds', 'peak_rss_bytes', 'output_bytes')) if not caps[k] > used[uk]]
    if low or dg['per_call_bytes'] < used['output_bytes']:
        raise Refused('CAPS_NOT_ABOVE_MEASURED: %s guard %s measured %s' % (low, dg['per_call_bytes'], used))
    measured = int(used['output_bytes'])
    out = Path(out_dir)
    out.mkdir(exist_ok=False)
    tm = write_x(out / 'TIMING_MODEL_H3.json', {
        'schema': 'DDO154_H3_TIMING_MODEL_C2V001', 'adopted_call_spec_sha256': ad['call_spec_sha256'],
        'base_spec_sha256': ctx.base_sha256, 'wall_rule_record': dict(wall_rule), 'per_call': caps,
        'rule': 'A140 N4 / A177 two-step / Claude4 0243 N2: the FINAL wall rule record of W1_RUN_SHEET section 2'})
    doc = {'schema': O.SCHEMA_ADOPTION, 'verdict_artifact_sha256': ad['verdict_sha256'], 'adopted_case_id': ad['case_id'],
           'adopted_call_spec_sha256': ad['call_spec_sha256'], 'base_spec_sha256': ctx.base_sha256,
           'seed_spec_sha256': ctx.seed_spec_sha256, 'capability_evidence_sha256': cfg['capability_evidence']['sha256'],
           'timing_model': tm, 'source_receipts': rs, 'per_call': caps,
           'disk_guard': {'per_call_bytes': dg['per_call_bytes'], 'measured_per_call_bytes': measured},
           'measured_max': used, 'driver_sha256': M.DRIVER_SHA,
           'certificate_registry': cfg['tail_readiness']['certificate_registry'], 'reading': 'ADOPT_TAIL',
           'compare_sha256': ad['compare_sha256'], 'sealed_prereg_sha256': ad['prereg_sha256'],
           'candidate_config': {'path': str(Path(config_path).resolve()), 'sha256': config_sha256}}
    dp = write_x(out / 'ADOPTION_DERIVATION_H3.json', doc)
    delta = {'set': {'adoption_derivation': dp, 'disk_guard.measured_per_call_bytes': measured},
             'append': {'notes': ' | H3 adoption (V006 A188; C4-6): adoption_derivation %s; measured_per_call_bytes %d = '
                                 'largest output over the derivation source receipts.' % (dp['sha256'][:16], measured)}}
    dl = write_x(out / 'ADOPTION_DELTA_H3.json', delta)
    return {'status': 'OK', 'timing_model': tm, 'adoption_derivation': dp, 'delta': dl, 'measured_max': used}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('--entry', '--entry-sha256', '--config', '--config-sha256', '--wall-rule-record', '--wall-rule-record-sha256',
              '--out-dir'):
        ap.add_argument(k, required=True)
    ap.add_argument('--source-receipt', nargs=3, action='append', required=True, metavar=('CASE', 'PATH', 'SHA256'))
    a = ap.parse_args(argv)
    try:
        E, M = load_entry(a.entry, a.entry_sha256)
        out = build(M, config_path=a.config, config_sha256=a.config_sha256,
                    wall_rule={'path': os.path.abspath(a.wall_rule_record), 'sha256': a.wall_rule_record_sha256},
                    receipts=[tuple(x) for x in a.source_receipt], out_dir=a.out_dir)
    except Exception as exc:                       # noqa: BLE001 -- Refused, OrchestratorError, OSError, ...: never a pass
        out = {'status': 'REFUSED', 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}
    print(json.dumps(out, indent=1, sort_keys=True, default=str))
    return 0 if out['status'] == 'OK' else 3


if __name__ == '__main__':
    sys.exit(main())
