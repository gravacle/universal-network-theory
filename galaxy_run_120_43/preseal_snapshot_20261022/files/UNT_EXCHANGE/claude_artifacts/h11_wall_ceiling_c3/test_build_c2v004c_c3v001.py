"""Synthetic tests for build_params_s45_c2v004c_c3v001 (Claude3, 0836). Reads the pinned C2V004B bytes read-only.
usage: python3 -I -B test_build_c2v004c_c3v001.py BUILDER_PATH WORK_DIR   (WORK_DIR must not exist)"""
import hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
builder, work = Path(sys.argv[1]), Path(sys.argv[2])
os.mkdir(work)
spec = importlib.util.spec_from_file_location('b', builder); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
base_raw = B.BASE.read_bytes(); base = json.loads(base_raw)
results = []
def check(name, cond, detail=None):
    results.append({'id': name, 'pass': bool(cond), 'detail': detail})
    if not cond: raise AssertionError(name)
def flat(o, pre=''):
    if isinstance(o, dict) and o:
        out = {}
        for k, v in o.items(): out.update(flat(v, pre + k + '.'))
        return out
    return {pre[:-1]: o}
def refused(fn, code):
    try: fn()
    except SystemExit as e: return str(e).startswith('REFUSED ' + code)
    return False
# 1. the reference build and an independent leaf diff
raw, draw, wall = B.build(base_raw, '2026-10-22T09:30:00Z')
check('wall_is_seconds_to_phase2_ceiling', wall == 3443340, wall)
doc = json.loads(raw); fa, fb = flat(base), flat(doc)
changed = sorted(k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>'))
walls = sorted('batches.HEADLINE.caps_per_case.%s.wall_cap_s' % c for c in base['batches']['HEADLINE']['case_order'])
check('exactly_11_headline_wall_leaves_plus_provenance', set(changed) == set(walls) | {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a271'}, changed)
check('every_headline_wall_is_W', all(fb[k] == 3443340 for k in walls))
check('rss_output_and_other_walls_unchanged', all(fb[k] == fa[k] for k in fa if k.endswith(('.rss_cap_bytes', '.output_cap_bytes')) or (k.endswith('.wall_cap_s') and k not in walls)))
check('rss_is_ram_everywhere', all(v == 137438953472 for k, v in fb.items() if k.endswith('.rss_cap_bytes')))
check('serialization_matches_dbp_convention', raw == (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode())
check('supersedes_binds_c2v004b', doc['supersedes']['sha256'] == B.BASE_SHA and doc['schema'] == 'DIRECT_BATCH_PARAMS_S45_C2V004C')
d = json.loads(draw); check('leaf_diff_record_consistent', d['n_changed'] == 16 and d['n_wall_leaves'] == 11 and d['successor_sha256'] == hashlib.sha256(raw).hexdigest())
# 2. determinism
check('deterministic', B.build(base_raw, '2026-10-22T09:30:00Z')[0] == raw)
# 3. refusals
check('fill_too_late_refused', refused(lambda: B.build(base_raw, '2026-11-30T05:59:00Z'), 'FILL_TOO_LATE'))
check('fill_after_ceiling_refused', refused(lambda: B.build(base_raw, '2026-12-02T00:00:00Z'), 'FILL_TOO_LATE'))
check('noncanonical_utc_refused', refused(lambda: B.build(base_raw, '2026-10-22 09:30:00'), 'BAD_UTC') and refused(lambda: B.build(base_raw, '2026-10-22T9:30:00Z'), 'NONCANONICAL_UTC'))
check('tampered_base_refused', refused(lambda: B.build(base_raw.replace(b'100800', b'100801', 1), '2026-10-22T09:30:00Z'), 'BASE_PIN_MISMATCH'))
# 4. CLI: new absolute out dir only; exclusive outputs
py = sys.executable
out1 = work / 'run1'
r = subprocess.run([py, '-I', '-B', str(builder), '--fill-utc', '2026-10-22T09:30:00Z', '--out-dir', str(out1)], capture_output=True, text=True)
check('cli_writes_two_files', r.returncode == 0 and sorted(os.listdir(out1)) == ['DIRECT_BATCH_PARAMS_S45_C2V004C.json', 'LEAF_DIFF_S45_C2V004C.json'], r.stdout + r.stderr)
check('cli_bytes_equal_build', (out1 / 'DIRECT_BATCH_PARAMS_S45_C2V004C.json').read_bytes() == raw)
r2 = subprocess.run([py, '-I', '-B', str(builder), '--fill-utc', '2026-10-22T09:30:00Z', '--out-dir', str(out1)], capture_output=True, text=True)
check('cli_existing_out_dir_refused', r2.returncode != 0 and 'OUT_DIR_MUST_BE_NEW' in (r2.stdout + r2.stderr))
r3 = subprocess.run([py, '-I', '-B', str(builder), '--fill-utc', '2026-10-22T09:30:00Z', '--out-dir', 'relative_dir'], capture_output=True, text=True, cwd=str(work))
check('cli_relative_out_dir_refused', r3.returncode != 0 and not (work / 'relative_dir').exists())
# 5. restoring mutants: each removes one guard; an independent check must catch it
src = builder.read_text()
mutants = {
 'M1_skip_scope_check_and_change_sens_wall': ("    if not set(walls) <= set(changed) or not set(changed) <= allowed:\n        refuse('LEAF_DIFF_SCOPE')\n",
     "    pass\n", "doc['batches']['SENS_LO']['caps_per_case']['SENS_DISTANCE_LOWER']['wall_cap_s'] = wall\n    "),
 'M2_allow_shorter_wall': ("    if wall <= OLD_WALL:\n        refuse('FILL_TOO_LATE')", "    if False:\n        refuse('FILL_TOO_LATE')", None),
 'M3_skip_base_pin': ("    if sha_b(base_raw) != BASE_SHA:\n        refuse('BASE_PIN_MISMATCH')", "    if False:\n        refuse('BASE_PIN_MISMATCH')", None),
 'M4_round_wall_up': ("    wall = int((ceiling - fill).total_seconds())", "    wall = int((ceiling - fill).total_seconds()) + 86400", None),
}
killed = {}
for name, (old, new, inject) in mutants.items():
    assert src.count(old) == 1, name
    msrc = src.replace(old, new)
    if inject:
        anchor = "    doc['schema'] = SCHEMA\n"; assert msrc.count(anchor) == 1
        msrc = msrc.replace(anchor, "    " + inject + anchor.lstrip(' ') if False else anchor.replace("    doc['schema']", "    " + inject.strip() + "\n    doc['schema']"))
    mp = work / (name + '.py'); mp.write_text(msrc)
    ms = importlib.util.spec_from_file_location(name, mp); M = importlib.util.module_from_spec(ms); ms.loader.exec_module(M)
    caught = False
    try:
        if name == 'M2_allow_shorter_wall':
            M.build(base_raw, '2026-11-30T05:59:00Z'); caught = False
        elif name == 'M3_skip_base_pin':
            M.build(base_raw.replace(b'100800', b'100801', 1), '2026-10-22T09:30:00Z'); caught = False
        else:
            mraw, _, mwall = M.build(base_raw, '2026-10-22T09:30:00Z')
            mf = flat(json.loads(mraw)); mchanged = {k for k in set(fa) | set(mf) if fa.get(k, '<absent>') != mf.get(k, '<absent>')}
            caught = (mchanged != set(changed)) or (mwall != 3443340)
    except (SystemExit, Exception) as e:
        caught = not (name in ('M2_allow_shorter_wall', 'M3_skip_base_pin'))
    # for M2/M3 the mutant must NOT refuse (guard removed) -> caught by the original test's refusal expectation
    if name in ('M2_allow_shorter_wall', 'M3_skip_base_pin'):
        caught = not refused(lambda: M.build(base_raw if name == 'M2_allow_shorter_wall' else base_raw.replace(b'100800', b'100801', 1), '2026-11-30T05:59:00Z' if name == 'M2_allow_shorter_wall' else '2026-10-22T09:30:00Z'), 'FILL_TOO_LATE' if name == 'M2_allow_shorter_wall' else 'BASE_PIN_MISMATCH')
    killed[name] = caught
check('all_mutants_killed', all(killed.values()), killed)
rec = {'schema': 'TEST_RECORD_C2V004C_C3V001', 'builder_sha256': hashlib.sha256(builder.read_bytes()).hexdigest(), 'base_sha256': B.BASE_SHA,
       'n': len(results), 'passed': sum(r['pass'] for r in results), 'results': results, 'mutants': killed}
(work / 'TEST_RECORD.json').write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'mutants_killed': sum(killed.values()), 'of': len(killed)}))
