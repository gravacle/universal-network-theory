# make_results_v2_r5chk.py -- RESULTS_R5CHK_C4V002.json = RESULTS V001 + A103 (21:43Z) and the seal tools v003 context; file shas
# recomputed from bytes at write time. V001 is kept (superseded).
import sys, os, json, hashlib
D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check'
UTC = sys.argv[1]
def sha(p):
    q = p if p.startswith('/') else os.path.join(D, p)
    return hashlib.sha256(open(q, 'rb').read()).hexdigest()
r = json.load(open(os.path.join(D, 'RESULTS_R5CHK_C4V001.json')))
r['schema'] = 'R5CHK_RESULTS_C4V002'
r['utc'] = UTC
r['supersedes'] = {'path': os.path.join(D, 'RESULTS_R5CHK_C4V001.json'), 'sha256': sha('RESULTS_R5CHK_C4V001.json'),
                   'why': 'A103 (21:43Z) was added to the open V005 after V001 was written; every test result is unchanged'}
r['verdict'] = ('CASE_BLOCK_CONFIRMED (TESTED); PREREG_R5_TRACED (TESTED); CASE_BLOCK_ABSENT_GONE on r12 and r13 (TESTED); '
                'SEAL_NOT_READY on r5 as written: 1 BLOCKING (A102 and A103 postdate r5 and touch its text), 3 SHOULD_FIX')
r['report_path'] = os.path.join(D, 'REPORT_R5CHK_C4V002.md')
r['report_sha256'] = sha('REPORT_R5CHK_C4V002.md')
F = {x['id']: x for x in r['findings']}
F['F-01']['claim'] = (
    'A102 (21:22Z) and A103 (21:43Z) postdate prereg r5 (open V005 now 643ef6ef) and touch its text. A102: r13 replaces r12 as the final compare '
    'round and "prereg r5\'s compare slot takes r13". A103: Codex1 substitutes for Codex2 as the r13 cross-lineage delta reviewer of record '
    '(A81 RI-20 named Codex2), and cx3r008 replaces cx3r007 as the step-5 NGC driver. r5\'s entry table ends at A101 (A99.3 requires every '
    'entry to the freeze; seal tool 1 v002 refuses UNCOVERED_LATER_ENTRY A102; my extractor finds A102 and A103 without rows), and three r5 '
    'sentences are now false: "The final compare round is r12 cx3v002", "delta reviews of record, Claude3\'s and Codex2\'s", and the scope '
    'note "the step-5 launch registry is SPEC_REGISTRY_CX3R007"; RI-28 is no longer open. Seal tool 3 v002 does not read rule text. Fix: '
    '(i) prereg r6 after r13\'s delta reviews (A102 and A103 rows revised; compare rule generic; RI-28 resolved), or (ii) root\'s seal tools '
    'v003 dispositions JSON (0633, 0105) with A102 and A103 marked revised, each reason naming the r5 sentence it supersedes, root accepting '
    'that the sealed text keeps them (as RI-35 does for the status line); a no_change row for either would be untrue. Owner: Claude2 (route), '
    'then Claude4. TESTED and FORMAL.')
F['F-01']['reproduction'] = F['F-01']['reproduction'].replace('(uncovered A102)', '(uncovered A102); the same on scratch/V005_ADDENDUM_READ_COPY_3_R5CHK.md (uncovered A102, A103)')
F['F-02']['claim'] = F['F-02']['claim'].replace('A81 RI-20 as applied by A83, A86, A91, A96, A102) with r12 superseded and r13 the candidate.',
                                                'A81 RI-20 as applied by A83, A86, A91, A96, A102, A103) with r12 superseded and r13 the candidate, its reviews of record Claude3 and Codex1 (A103).')
F['F-08']['claim'] += (' The bare-name coverage T1b shows (`--covered-later A102` passes tool 1) is Codex3\'s D-05 counterexample (0637); '
                       'root ordered seal tools v003 (0633/0634: a root-written, byte-pinned dispositions JSON; B8 readiness), now being built, with Codex1 as its delta reviewer (0638).')
r['open_items'][0] = ('F-01 / GAP-22: Claude2 rules the route for A102 and A103: prereg r6 (A102/A103 rows, generic compare rule naming r13 and '
                      'its reviews of record Claude3 and Codex1), or v003 dispositions rows marked revised that name the superseded r5 sentences.')
r['open_items'][1] = 'GAP-06: r13 f5adfd11 delta reviews by Claude3 and Codex1 (A103 substitutes Codex1 for Codex2; 0635); then the compare slot takes r13.'
r['open_items'][6] = 'GAP-24: seal tools v003 (D-05 dispositions JSON, B8 readiness; 0633/0634) being built by Claude4; delta by Codex1 (0638).'
r['files'] = [{'path': os.path.join(D, x), 'sha256': sha(x)} for x in (
    'REPORT_R5CHK_C4V002.md', 'REPORT_R5CHK_C4V001.md', 'RESULTS_R5CHK_C4V001.json', 'out/CASE_BLOCK_CHECK_R5CHK.json', 'out/DIFF_R4_R5_R5CHK.json',
    'out/DIFF_R4_R5_R5CHK.txt', 'out/ENTRY_SHAS_R5CHK.json', 'out/ENTRY_SHAS_ON_COPY2_R5CHK.json', 'out/ENTRY_SHAS_ON_COPY3_R5CHK.json',
    'out/PIN_VERIFY_R5_PREREG_R5CHK.json', 'out/G_S2_SEALED_B_GATES_ONLY/GATES_ONLY.json', 'out/FENCE_C4V001_TO_C4V002_R5CHK.diff',
    'scratch/rehearsal_r12/SCRATCH_INPUTS_R5CHK.json', 'scratch/V005_ADDENDUM_READ_COPY_1_R5CHK.md', 'scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md',
    'scratch/V005_ADDENDUM_READ_COPY_3_R5CHK.md', 'tools/fence_c4v001.py', 'tools/fence_c4v002.py', 'tools/run_fenced_r5chk.py',
    'tools/case_block_check_r5chk.py')]
p = os.path.join(D, 'RESULTS_R5CHK_C4V002.json')
with open(p, 'x') as fh:
    json.dump(r, fh, indent=1)
print('wrote', p, sha(p))
