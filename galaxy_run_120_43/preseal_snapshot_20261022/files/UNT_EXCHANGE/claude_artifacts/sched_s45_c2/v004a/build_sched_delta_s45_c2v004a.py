"""Builder for sched_s45 v004a (Claude2 sched_s45_c2, c2v004a; V006 addendum A172: "max_concurrent: 8, the campaign's own
design value").  One scheduling leaf on the v004 config, applied (not hand-typed) by the unchanged apply tool
apply_sched_delta_s45_c2v002 (2a18b280; max_concurrent is in its ALLOWED_SET).  Writes, by exclusive create, in v004a/:
  * SCHED_DELTA_S45_C2V004A.json                    set max_concurrent = the design value read from the campaign v005
                                                    config bytes (RUN_CONFIG_DDO154_V005.json L78), cross-checked against
                                                    LAUNCH_V005.md L182 and A172's 8; notes are APPENDED, never set;
  * RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004A.json    the v004 config (cbc36b7a) + that delta;
  * DELTA_REPORT_S45_C2V004_TO_S45_C2V004A.json     the apply tool's report.
The delta sets no other leaf and names no predecessor value, so the same file applied by the same tool to the A140 N4
rebuild of the v004 builder re-sets max_concurrent 8 there too (tests row Y04A).  DIRECT_BATCH_PARAMS, the caps module, the
wall cap and every physics input are not read for writing and not changed.  The v004 builder is not copied: it always
rebuilds from R9 and also emits DIRECT_BATCH_PARAMS / CAPS, which this item must not change.
usage: python3 -I -B build_sched_delta_s45_c2v004a.py [--out-dir DIR]
"""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # sched_s45_c2/v004a
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
TAG = 'S45_C2V004A'
PRED = ART / 'sched_s45_c2/v004/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004.json'
PRED_SHA = 'cbc36b7af83fdde102290f1e6d33f100925ce47ac31394968988b59771edf751'
APPLY = ART / 'sched_s45_c2/v002/apply_sched_delta_s45_c2v002.py'                 # unchanged tool (v002)
APPLY_SHA = '2a18b280cb3a20ec5fb2668ff9798fe41fa02121f8003dc4e3164d7c2a9277f8'
V005 = ART / 'calibration_orchestrator_c2/v005'
LAUNCH_V005 = V005 / 'LAUNCH_V005.md'
LAUNCH_V005_SHA = '0745e70ea8d09445b189663ed51640e695d39d61a69b3e7251b1fc0e4a4ae6b6'
CFG_V005 = V005 / 'RUN_CONFIG_DDO154_V005.json'
CFG_V005_SHA = 'e3351c8fbb7b23848a09f552b5ce85ffaff1cabf6fa8bfe6c432ded69f58dd3b'
CAMP_V005 = V005 / 'campaign_c2v005.py'
CAMP_V005_SHA = 'd35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2'
A172_VALUE = 8                                            # V006 A172, cross-check only: the value is read from CFG_V005


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def xwrite(path, obj=None, raw=None):
    data = raw if raw is not None else (json.dumps(obj, indent=1, sort_keys=True) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(data)
    return sha_b(data)


def pinned_bytes(p, want):
    b = Path(p).read_bytes()
    if sha_b(b) != want:
        raise SystemExit('PIN_MISMATCH %s' % p)
    return b


def line(b, n):
    return b.decode('utf-8').splitlines()[n - 1]


def design_value():
    """max_concurrent of the campaign's own design, from bytes: config L78 (value), LAUNCH L182 (text), A172 (8)."""
    cb, lb = pinned_bytes(CFG_V005, CFG_V005_SHA), pinned_bytes(LAUNCH_V005, LAUNCH_V005_SHA)
    v = json.loads(cb)['max_concurrent']
    l78, l182 = line(cb, 78), line(lb, 182)
    if type(v) is not int or l78 != ' "max_concurrent": %d,' % v or ('max_concurrent %d' % v) not in l182 \
            or 'process budget 17' not in l182 or v != A172_VALUE:
        raise SystemExit('design value not confirmed from bytes: %r %r %r' % (v, l78, l182))
    cs = pinned_bytes(CAMP_V005, CAMP_V005_SHA).decode('utf-8').splitlines()
    l200, l203 = cs[199].strip(), cs[202].strip()
    if l200 != 'while pending and len(running) < n and time.monotonic() - t0 < cap:' or \
            l203 != 'if cur + specs[i][2] > budget:':
        raise SystemExit('campaign_c2v005 L200 / L203 differ')
    return v, {'RUN_CONFIG_DDO154_V005.json': {'path': str(CFG_V005), 'sha256': CFG_V005_SHA, 'line': 78, 'text': l78,
                                               'value': v},
               'LAUNCH_V005.md': {'path': str(LAUNCH_V005), 'sha256': LAUNCH_V005_SHA, 'line': 182, 'text': l182},
               'campaign_c2v005.py': {'path': str(CAMP_V005), 'sha256': CAMP_V005_SHA, 'L200': l200, 'L203': l203}}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out-dir', default=str(HERE))
    a = ap.parse_args(argv)
    out_dir = Path(a.out_dir)
    if not out_dir.is_absolute() or not out_dir.is_dir():
        raise SystemExit('--out-dir must be an existing absolute directory')
    pred_b = pinned_bytes(PRED, PRED_SHA)
    raw = pinned_bytes(APPLY, APPLY_SHA)
    sp = importlib.util.spec_from_file_location('apply_s45_c2v002', str(APPLY))
    A = importlib.util.module_from_spec(sp)
    exec(compile(raw, str(APPLY), 'exec'), A.__dict__)
    if 'max_concurrent' not in A.ALLOWED_SET:
        raise SystemExit('apply tool v002 does not allow max_concurrent')
    mc, src = design_value()
    pred = json.loads(pred_b)
    delta = {'schema': 'SCHED_DELTA_%s' % TAG,
             'predecessor': {'path': str(PRED), 'sha256': PRED_SHA},
             'set': {'max_concurrent': mc},
             'append': {'notes': ' s45 c2v004a (sched_s45_c2, Claude2 2026-10-19, V006 A172): max_concurrent %d, the '
                                 'campaign\'s own design value (calibration_orchestrator_c2/v005 RUN_CONFIG_DDO154_V005.json '
                                 'L78, LAUNCH_V005.md L182); this replaces "max_concurrent as R9" above. At %d the process '
                                 'budget %d decides concurrency (campaign_c2v005 L200, L203). Scheduling leaf only: the '
                                 'cache id does not read it and no value changes; this delta sets no other leaf.' % (
                                     mc, mc, pred['process_budget'])},
             'basis': {'ruling': 'V006 addendum A172 (2026-10-19 19:58:19Z): "max_concurrent: 8, the campaign\'s own design '
                                 'value"; "Build sched v004a with this one leaf. W1 needs only this config"',
                       'design_value_from_bytes': src,
                       'concurrency': 'campaign_c2v005 starts the head call only while fewer than max_concurrent calls run '
                                      '(L200) and only if the accounted processes plus its peak fit process_budget (L203). '
                                      'R9 numerics give each call peak 8 (route_a.column_workers) and 2 after route A '
                                      '(column_workers), so a start needs <= 9 accounted processes and at most 5 calls can '
                                      'run at once (4 x 2 + 8 = 16 <= 17): with max_concurrent >= 5 the process budget %d '
                                      'alone binds' % pred['process_budget'],
                       'value_effect': 'none: max_concurrent is not an input of the parent cache id (c75a889f L1774-1780) '
                                       'or of any call spec; the parent validates it at L1724-1733 (int, 1..process_budget) '
                                       'and passes it to the campaign only (L2638)'},
             'unchanged_on_purpose': {
                 'every_other_config_leaf': 'the predecessor\'s (v004 cbc36b7a): campaign c2v005 d35d5d4a, process_budget 17, '
                                            'stage_aware_budget, campaign_wall_cap_s 172800, per_call (wall 100800 s '
                                            'PROVISIONAL A140 N4, RSS = RAM, output 80 GiB), disk_guard, orphan_wait '
                                            '(wall + 600 s, ratified A172), numerics and every physics pin',
                 'DIRECT_BATCH_PARAMS': 'DIRECT_BATCH_PARAMS_S45_C2V004 (7c3ceae5) is not touched; its successor '
                                        'C2V004B is a separate A172 item',
                 'wall_cap': 'not re-derived (A140 N4 at W1)'},
             'reuse_at_W1': 'predecessor-agnostic: applied by apply_sched_delta_s45_c2v002 (2a18b280) to any config of the '
                            'R9 family it sets max_concurrent %d and appends this note, nothing else (tests row Y04A: on '
                            'the A140 N4 rebuild of build_params_s45_c2v004 it leaves wall, orphan wait and notes as the '
                            'only leaves differing from this config)' % mc}
    dsha = xwrite(out_dir / ('SCHED_DELTA_%s.json' % TAG), delta)
    out, rep = A.apply(pred_b, delta)
    if out is None:
        raise SystemExit('delta refused: %s' % rep)
    ssha = xwrite(out_dir / ('RUN_CONFIG_DDO154_CX2V006R9_%s.json' % TAG), raw=out)
    rep['delta_sha256'] = dsha
    rep['apply_tool'] = {'path': str(APPLY), 'sha256': APPLY_SHA}
    rep['predecessor'] = {'path': str(PRED), 'sha256': PRED_SHA}
    xwrite(out_dir / ('DELTA_REPORT_S45_C2V004_TO_%s.json' % TAG), rep)
    print(json.dumps({'out_dir': str(out_dir), 'tag': TAG, 'predecessor_sha256': PRED_SHA, 'delta_sha256': dsha,
                      'successor_sha256': ssha, 'max_concurrent': [pred['max_concurrent'], mc],
                      'changed': sorted(rep['changed_paths'])}, indent=1))


if __name__ == '__main__':
    main()
