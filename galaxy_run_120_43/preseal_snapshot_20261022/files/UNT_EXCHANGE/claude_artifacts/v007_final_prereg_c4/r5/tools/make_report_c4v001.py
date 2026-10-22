"""Claude4 r5 helper: write REPORT_R5_C4V001.md and RESULTS_R5_C4V001.json (exclusive create). Every sha256 is read from bytes here.
usage: UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ) python3 -I -B make_report_c4v001.py"""
import hashlib, json, os
from pathlib import Path
R5 = Path(__file__).resolve().parent.parent
UTC = os.environ['UTC']
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
F = {k: R5 / v for k, v in {
    'case_block': 'case_block/CASE_BLOCK_V007_C4V001.json', 'case_block_build_record': 'out/CASE_BLOCK_BUILD_C4V001.json',
    'prereg_r5_json': 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json', 'prereg_r5_md': 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md',
    'seal_checklist_r5': 'SEAL_CHECKLIST_R5.md', 'root_items_r5': 'ROOT_ITEMS_R5.md', 'delta_r4_r5': 'DELTA_R4_R5.md',
    'delta_erratum_e1': 'DELTA_R4_R5_ERRATUM_E1.md', 'clause_source_map_r5': 'CLAUSE_SOURCE_MAP_R5.md', 'entry_table_r5': 'ENTRY_TABLE_R5.md',
    'hashes_r5': 'HASHES_R5.txt', 'addendum_byte_copy': 'addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md',
    'generator_of_record_p3': 'tools/make_v007_final_draft_c4v005_p3.py', 'generator_c4v005_first_draft': 'tools/make_v007_final_draft_c4v005.py',
    'generator_p2': 'tools/make_v007_final_draft_c4v005_p2.py', 'patch_p2': 'tools/patch_gen_c4v005_p2.py', 'patch_p3': 'tools/patch_gen_c4v005_p3.py',
    'case_block_builder': 'tools/build_case_block_c4v001.py', 'r12_loader': 'tools/load_r12_c4r5.py', 'fenced_runner': 'tools/run_fenced_c4r5.py',
    'fence_c4v001_copy': 'tools/fence_c4v001.py', 'fence_c4v002': 'tools/fence_c4v002.py', 'fence_maker': 'tools/make_fence_c4v002.py',
    'fence_diff': 'out/FENCE_C4V001_TO_C4V002.diff', 'fence_note': 'tools/FENCE_C4V002_NOTE.md',
    'r5_case_block_path_check': 'out/R5_PREREG_CASE_BLOCK_PATH_CHECK_C4V001.json', 'path_checker': 'tools/check_r5_case_block_path_c4v001.py',
    'audit_r5_vs_r4': 'out/AUDIT_R5_VS_R4_C4V001.json', 'auditor': 'tools/audit_r5_vs_r4_c4v001.py',
    'console_cb1': 'out/CB1_BUILD_CASE_BLOCK.console.txt', 'console_cb2': 'out/CB2_R5_CASE_BLOCK_PATH.console.txt', 'console_t1': 'out/T1_R5_DRY_TOOL1.console.txt',
    'partial': 'PARTIAL.md'}.items()}
S = {k: sha(p) for k, p in F.items()}
pre = json.loads(F['prereg_r5_json'].read_bytes())
cbr = json.loads(F['case_block_build_record'].read_bytes())
chk = json.loads(F['r5_case_block_path_check'].read_bytes())
aud = json.loads(F['audit_r5_vs_r4'].read_bytes())
rows = pre['entries_after_A81']['rows']
nrh = sum(1 for r in rows if r['decision'] == 'REVISED_HERE')
lp = pre['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']
b7 = lp['build']
open_ri = [r for r in pre['root_items'] if r['status'] == 'OPEN']
L = []
w = L.append
w('# REPORT: prereg r5 and the V007 case block (Claude4 r5 helper, A99 seal path)')
w('')
w('UTC %s (`date -u`). Folder `claude_artifacts/v007_final_prereg_c4/r5/`. Labels: **TESTED** (run or read from bytes here), **FORMAL** (follows from code or text read here), **UNTESTED**.' % UTC)
w('')
w('## Result')
w('')
w('- **The V007 case block is built and reads valid under r12\'s own `validate_case_block` (TESTED).**')
w('  - `case_block/CASE_BLOCK_V007_C4V001.json`, sha256 `%s`, %d bytes.' % (S['case_block'], cbr['case_block']['bytes']))
w('  - Codex2 0507 checked it: PASS, zero findings. A101 rules it the case block of record, pinned as `binding_inputs.case_block` in r5.')
w('- **Prereg r5 is built (TESTED: generated from bytes; audited against r4).**')
w('  - `KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json`, sha256 `%s`.' % S['prereg_r5_json'])
w('  - It carries `binding_inputs.case_block`.')
w('  - The BUILD of record is BUILD_V007, filled from bytes: `%s`.' % b7['sha256'])
w('  - Its entry table covers A82-A101 (%d revised here, %d no change).' % (nrh, len(rows) - nrh))
w('  - The compare slot rule is set for r12 cx3v002, the driver is r5, and `ngc_gas_M_s` is 96.')
w('  - The seal checklist, root items, delta, clause map and hashes follow.')
w('- **The seal is still not ready.** %d root items are open (RI-28 to RI-37). The most important:' % len(open_ri))
w('  - **RI-28, BLOCKING for the seal:** Claude3\'s r12 delta review of record (0083) reports 1 BLOCKING item (A-B1). Under A81 RI-20, r12 does not clear the compare slot until root rules.')
w('  - **RI-29:** BUILD_V007\'s Claude4 delta check and Claude2 adoption are pending.')
w('')
w('## 1. The case block (A99.2)')
w('')
w('**What r12 requires (FORMAL, from code).**')
w('- Requirements come from `validate_case_block` (r12 L1469-1583, with `tail_content_codes` L1402-1459) and from FIELDS_R12_CX3V002 section 4.')
w('- The schema is UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003.')
w('- Exactly 11 cases: the ten T-cases plus C5H.')
w('- Each T-case carries:')
w('  - its grid and truncation;')
w('  - `tail` and `ro1_required` true;')
w('  - `drivers_allowed` = [the sealed driver];')
w('  - its `/numerics` registered whole;')
w('  - `uv_tail_config_sha256`, the pinned library\'s `normalize_config` sha;')
w('  - the A54 S8 tail content: P = 128, KLO 64 and KHI 256, cube K_out 5 for C5c, lambda 1.05 for C4T-A, nodes_v001 with the G5 ext_grid for D5, every other uv_tail key equal to C4T\'s, and gas M_s 128.')
w('- C4T-D5\'s numerics equal the C5H reference outside `composite_grid_spec` and `uv_tail` (RA1, A50 S1).')
w('- C5H carries tail and ro1_required false, call 60b46130 and drivers [999331af].')
w('- In sealed mode the compare reads the block only from `binding_inputs.case_block` (L5706).')
w('')
w('**Inputs, each verified from bytes (TESTED).**')
w('- SPEC_REGISTRY_R5_MS128_CX1V004 `c7023846`: the ten FILLED specs.')
w('- Plan template LAUNCH_PLAN_V010 `26f1ebf9`: the same ten FILLED shas.')
w('- DRY_R5_MS128_V004 `ff60cd6b` and its ten dry reports: driver r5, no blockers, no unexplained refusals, each dry report naming its FILLED spec.')
w('- All of these are byte-pinned in BUILD_V005 `46bc5b5d`.')
w('')
w('**The recipe is Claude3\'s** (`validate_registry_r11_c3v001.py`; its r12 successors `validate_registry_r12_c3v001/_c3v002.py`).')
w('- Each T-case registers its driver-r5 dry-run `normalized_spec.numerics`. The dry normalization only adds `/truncation/kmax_inverse_kpc`, on 9 cases. It changes or removes no spec leaf (TESTED).')
w('- `route_a_mode` is parallel8 (A47 I4, A51).')
w('- `key_equivalence_map` is [].')
w('- The pinned-library uv_tail sha equals the driver-side `normalized_sha256` of every dry run (TESTED, 10/10).')
w('- Both certificates are the A70 slots (EPS 598c8fa3, LO 1c384f76), and their files hash to their pins (TESTED).')
w('')
w('**Validation (TESTED, under fence_c4v002).**')
w('- r12 cx3v002 was exec\'d unmodified in-process by `tools/load_r12_c4r5.py`.')
w('- `validate_case_block` returns [] on the in-memory block, and [] again on the written bytes read back with r12\'s own `load_strict_file`.')
w('- P = 128 and the registered gas M_s = 128.')
w('- %d of %d build checks pass.' % (sum(1 for v in cbr['checks'].values() if v['ok']), len(cbr['checks'])))
w('- %d of %d must-refuse mutations refuse, for example a schema change, a missing case, a retired label, an r4 driver, M_s 64, a KLO/KHI swap, a C4T-A alias, a tampered tail sha, a seed factor of 0.1, D5 numerics that differ from C5H, a bad key map, and S4T truncated as a cube.' % (sum(1 for x in cbr['mutations_must_refuse'] if x['refused']), len(cbr['mutations_must_refuse'])))
w('- Record: `out/CASE_BLOCK_BUILD_C4V001.json` `%s`.' % S['case_block_build_record'])
w('')
w('**The sealed-mode path (TESTED).**')
w('- I replayed r12\'s L5705-L5729 steps with r12\'s own functions.')
w('- **On r5:** CASE_BLOCK_ACCEPTED (`%s`).' % chk['r5']['case_block']['sha256'])
w('- **On r4:** `%s`.' % chk['r4_control']['code'])
w('- **A CLI `--route-a-mode serial_with_exemption`** refuses with `%s`. So root\'s B6 commands must pass no route-A mode, or exactly parallel8.' % chk['r5_with_cli_mode_serial_must_refuse']['code'])
w('- Record: `out/R5_PREREG_CASE_BLOCK_PATH_CHECK_C4V001.json` `%s`.' % S['r5_case_block_path_check'])
w('')
w('**Why the draft `6bf4ce5a` reads CASE_BLOCK_INVALID (TESTED, in layers, on in-memory copies).**')
w('1. Its schema is C2V002, but r12 needs C2V003. This is the first refusal, and on its own it stops validation.')
w('2. With the schema fixed, the case labels still include the retired C4T-K16 and C4T-K64 (A54, A56 require KLO and KHI).')
w('3. With the labels fixed, 37 reasons remain:')
w('   - every T-case has drivers_allowed = v010 r3 `4c14552f`, not r5 `b5cc62af`;')
w('   - uv_tail_config_sha256 is a PENDING string, written before the specs were FILLED;')
w('   - the pinned library refuses each uv_tail (UV_TAIL_CONFIG_INVALID);')
w('   - C4T-D5 is "NOT_BUILDABLE", with unknown keys `refusal` and `status` and no `/numerics`;')
w('   - K_big is 32 where A55 needs 128, and gas M_s is 64 where A57 needs 128;')
w('   - the KLO, KHI and C4T-A tails are not distinct from C4T\'s.')
w('')
w('The draft predates A54/A55/A57, the FILLED specs and driver r5.')
w('')
w('## 2. Prereg r5')
w('')
w('**The generator** is `tools/make_v007_final_draft_c4v005_p3.py` (`%s`), in my folder `r5/tools/` because I may write only inside r5/.' % S['generator_of_record_p3'])
w('- The first draft, `make_v007_final_draft_c4v005.py` (`%s`), refused in its own row/edit consistency check before writing anything: it compared `x[2]` with a logged `x.2`.' % S['generator_c4v005_first_draft'])
w('- `p2` (`%s`) fixed that; its dry run was inspected.' % S['generator_p2'])
w('- `p3` added cosmetics, the registry V009 candidate and RI-37.')
w('- p3 was chained patch, then dry run, then real run. Its dry run and real run gave the same prereg sha.')
w('')
w('**What it does.**')
w('- It reads r4 `e3b6b5b2` and every input from bytes; a prefix mismatch refuses.')
w('- It reads the open V005 file once from bytes (`70a48f51`; byte copy `addendum_read/`) and builds the entry table.')
w('- It refuses any entry from A82 onward that has no row.')
w('- It finds BUILD_V007 by name and checks it:')
w('  - exactly 15 distinct supported sources, each verified from bytes;')
w('  - launcher v007 and guard v008 among them;')
w('  - the predecessor BUILD_V006 `fb9e6a4a`;')
w('  - the selected template LAUNCH_PLAN_V011_CX3V001 (`%s`) launches exactly the case block\'s ten FILLED specs, with driver r5 and registry c7023846;' % lp['template_plan']['sha256'])
w('  - the template differs from V010 only in %d output-path strings.' % lp['build_v007_check_at_r5_generation']['template_vs_V010']['differing_leaves'])
w('')
w('**The changes, each traced in `DELTA_R4_R5.md`** (47 edits, plus erratum E1 for three header bookkeeping leaves):')
w('- **A99.2, D-03:** `binding_inputs.case_block` {path, sha256}, plus `case_block_rule`.')
w('- **A99.1, D-02:** the launch-packet BUILD of record is BUILD_V007. `seal_record_requirements[10]` and `run_list.limits` name its launcher, guard and 15 sources; checklist B8 binds the same.')
w('- **A99.3, D-05, R-02:** `entries_after_A81`, one row per entry A82-A101, each "revised here" (with clauses) or "no change, because ...", each with its section sha256 from bytes. A83 is "revised here": the compare rule\'s rechecks of record and the comparator\'s check of record. A99 and A101 are "revised here". The section rule is stated, and two shas were re-derived independently with sed and shasum.')
w('- **A83, A86, A90, A91, A96:** the compare slot names r12 cx3v002 (`4bd7b262`; SELECTED 91aa9747; FIELDS 5cc95a06; IMPL ef0db32d; HASHES 3eb2912d) and its delta reviews of record, Claude3\'s and Codex2\'s, 0 blocking each. Its state is PENDING_ROOT_RULING, because Claude3 0083 reports A-B1.')
w('- **A96:** the driver is v010 r5 and r6 is not a candidate. RI-24 and the cache slot are moot (`cache_directory_r6_only` = `NOT_APPLICABLE_R5`). The r6 branch text is removed from successors, the role table, memory guard, tail cache, identity gates, run list, the seal record requirements, the outcome tests and scope_untested.')
w('- **ngc_gas_M_s = 96** (`fixed_across_all_cases.production_tail.ngc_gas_M_s`, value 96). It cites A81 RI-23 and Codex1 0032 (`3e8c9fc9`); the record `GQ_NGC_91_MS96_V001` (`be148bab`) reads PASS for NGC_T120L, M_s 96 against 192 on [2, 91]: 1.219e-15 and 2.335e-14 P0, both below 1e-12 (TESTED from bytes; rehearsal R-08).')
w('- **A86:** GQ record of record GQ_CERT_V006 `5a1b39f8`.')
w('- **A87:** the B3 record of record is the JSON `83c853b9`; DOUBLING is ea48ac2b with its M_s field `ddo_gas_M_s` (R-13, D-01); LO_NGC is V002 33bc2190.')
w('- **A88:** SR_K moves after the seal.')
w('- **A89:** the measured KHI cost.')
w('- **A92:** c2v007r2 and the R5_V001 identity records.')
w('- **A93:** the NGC registry named in the scope note.')
w('- **A94, A97, A100, A101:** B2 follows its text exactly; the A97 decision rule; the A100 disposition and values of record; the C3V003 record of record. `seal_record_requirements[12]` repeats the B2 disclosure and the A101 erratum.')
w('- **A82:** RI-27 resolved; no write to the open V005 file after the freeze.')
w('- **Registry:** the candidate is C3V009 `32ddadcb` (Claude3 0087: V008 plus BUILD_V007\'s four post-seal producer pins). C3V008 `f189cd3f` stays as A101\'s baseline. The slot value stays PENDING for root.')
w('- **SEAL_CHECKLIST_R5 adds:**')
w('  - B2a, the driver BUILD record creation step. The template is the rehearsal\'s REHEARSAL DRAFT `2a3e4308` (D-06).')
w('  - A6, with the 0598 B0 record `c2cec35b` as candidate (R-09).')
w('  - The explicit later-entry list in B1 (D-05).')
w('  - B8, bound to BUILD_V007\'s 15 sources.')
w('  - A11-A14: the case block, BUILD_V007, B2 C3V003, and B0_N3/B0_RO1/I4.')
w('- **Unchanged.** Every untouched r4 rule is byte-identical (TESTED by the audit: 1039 leaves differ from r4, and 1036 lie inside logged clauses). The other 3 are `revision` and `supersedes_draft`, recorded in erratum E1. By id, root items changed only RI-24 and RI-27.')
w('- **No value is guessed.** Every value that waits on root carries PENDING_ROOT_AT_SEAL_ASSEMBLY or PENDING_ROOT_RULING (census in `out/AUDIT_R5_VS_R4_C4V001.json`).')
w('')
w('**Seal tool 1 v001 on r5 (TESTED, dry-run mode, against the generation byte copy):** PASS. A46-A101 are cited (56 entries), all present, with no uncovered later entry.')
w('')
w('**Seal tool 3 v001** is pinned to r4 and cannot check r5 by design. Seal tools v002 (a separate helper) should:')
w('- pin r5 `%s`;' % S['prereg_r5_json'])
w('- read `ddo_gas_M_s` (D-01);')
w('- read the named build BUILD_V007 `%s`.' % b7['sha256'])
w('')
w('## 3. The fence')
w('')
w('`tools/fence_c4v002.py` (`%s`) is the exact copy `tools/fence_c4v001.py` (`%s`) plus two read-only exceptions, documented in `tools/FENCE_C4V002_NOTE.md`:' % (S['fence_c4v002'], S['fence_c4v001_copy']))
w('- (a) uvt_*.py sources outside every runs_ext tree;')
w('- (b) the CLAUDE2 V00*_ADDENDUM*.md decision records.')
w('')
w('Every other block is kept. The diff is `out/FENCE_C4V001_TO_C4V002.diff` (`%s`).' % S['fence_diff'])
w('')
w('Three fenced runs were made: CB1 (the build), CB2 (the path check) and T1 (seal tool 1). In each, selftest gave 8/8, selftest_v002 gave 17/17, and **BLOCKED after the selftests was []** (TESTED; console captures in `out/`). The loader\'s stat guard refused 0.')
w('')
w('## 4. Open items (root and lanes)')
w('')
for r in open_ri:
    w('- **%s, %s.** %s' % (r['id'], r['kind'], r['issue'][:400]))
w('')
w('## 5. Rules kept, and process notes')
w('')
w('**Rules kept.**')
w('- No launch and no compare `main()`. `--validity-only` was never run.')
w('- No read, list or stat of `runs_ext/KMAX_A2F10_C5H_RUN_V001`. Nothing under `runs_ext/UVT_*` was opened. No NGC3198 target or observed-velocity data was opened. No recursive content search over broad trees.')
w('- Writes were made only inside r5/. Every new file was created exclusively, by Python `open(\'x\')`. Console captures were piped into an exclusive-create writer. The only appends were to my PARTIAL.md.')
w('- No deletes, moves or network.')
w('- Python: `-I -B`, numpy only, single-thread BLAS. `taskpolicy -b` was accepted.')
w('')
w('**Disclosures.**')
w('- One `echo =====` line tripped zsh `=` expansion (rule 6). It errored before running anything and wrote nothing.')
w('- The fence\'s own selftest trial `read_runs_ext` (unchanged from v001) realpaths a nonexistent probe under the runs_ext root, and the fence refuses it. It stats neither the C5H run nor any UVT_* path (FORMAL).')
w('- An `ls` of the CLAUDE2 control folder printed `runs_ext` as an entry name. Nothing inside it was listed.')
w('- The open V005 file changed twice while I worked:')
w('  - A100 was added between 20:22Z and 20:41Z;')
w('  - A101 was added by 20:46Z.')
w('  - Each change was copied by exclusive create (scratch copies 1-3), read in full, and integrated. It was unchanged at 21:04Z.')
w('- **The state moved while I worked:**')
w('  - BUILD_V007 landed at 20:44:19Z;')
w('  - registry V008, then V009;')
w('  - B2 C3V003;')
w('  - Claude3 0083 (A-B1);')
w('  - Codex2 0507 PASS on the case block.')
w('  - r5 integrates all of these from bytes.')
w('')
w('## Files (sha256 from bytes)')
w('')
w('| file | sha256 |')
w('|---|---|')
for k, p in F.items():
    w('| `%s` | `%s` |' % (p.relative_to(R5), S[k]))
w('')
REPORT = R5 / 'REPORT_R5_C4V001.md'
with open(REPORT, 'x') as f:
    f.write('\n'.join(L) + '\n')
res = {'schema': 'UNT_V007_R5_AND_CASE_BLOCK_RESULTS_C4V001', 'utc': UTC, 'folder': str(R5),
       'case_block': {'path': str(F['case_block']), 'sha256': S['case_block'], 'validate_case_block_r12': 'VALID ([] in memory and on bytes)', 'label': 'TESTED',
                      'mutations_refused': '%d/%d' % (sum(1 for x in cbr['mutations_must_refuse'] if x['refused']), len(cbr['mutations_must_refuse'])),
                      'codex2_check': 'Codex2 0507 PASS zero findings (cited)', 'ruling': 'A101: pinned as binding_inputs.case_block in prereg r5'},
       'draft_6bf4ce5a_diagnosis': cbr['draft_diagnosis']['layers'],
       'prereg_r5': {'path': str(F['prereg_r5_json']), 'sha256': S['prereg_r5_json'], 'entry_table': ['%s %s %s' % (r['entry'], r['decision'], r['section_sha256']) for r in rows],
                     'build_v007': b7, 'compare_slot_state': pre['seal_slots']['compare']['named_candidates_verified_from_bytes']['state_at_r5_generation'],
                     'ngc_gas_M_s': pre['fixed_across_all_cases']['production_tail']['ngc_gas_M_s']['value'],
                     'registry_candidate': pre['seal_slots']['producer_registry']['named_candidates_verified_from_bytes']['C3V009_candidate']['sha256'],
                     'open_root_items': [r['id'] for r in open_ri]},
       'verification': {'sealed_mode_case_block_path_r5': chk['r5']['reading'], 'sealed_mode_case_block_path_r4': chk['r4_control']['code'],
                        'seal_tool_1_dry_run_r5': 'PASS (A46-A101 cited, 56 entries)', 'audit_vs_r4': {'differing_leaves': aud['differing_leaves'],
                        'uncovered': aud['uncovered_differing_leaves'], 'erratum': 'DELTA_R4_R5_ERRATUM_E1.md', 'root_items_changed_by_id': aud['root_items_changed_by_id'],
                        'entry_rows_rehash_ok': aud['entry_rows_rehash_ok']}},
       'fence': {'fence_c4v002_sha256': S['fence_c4v002'], 'fence_c4v001_copy_sha256': S['fence_c4v001_copy'], 'diff_sha256': S['fence_diff'],
                 'runs': {'CB1': 'selftest 8/8, v002 17/17, BLOCKED []', 'CB2': 'selftest 8/8, v002 17/17, BLOCKED []', 'T1': 'selftest 8/8, v002 17/17, BLOCKED []'}},
       'files': {str(p.relative_to(R5)): S[k] for k, p in F.items()}}
with open(R5 / 'RESULTS_R5_C4V001.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
print('report', sha(REPORT), '| results', sha(R5 / 'RESULTS_R5_C4V001.json'))
