# Independent review of dispatch 0581 — selected cx3r007 v004

`date -u`: Sun Oct 18 17:48:17 UTC 2026

**TESTED PASS within the delegated source/synthetic-record scope.** Selected driver SHA256 `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69`; parent r006 SHA256 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`. No remaining observed defect in the required launch-record strictness boundaries. This is an internal Codex3 review, not scientific launch authorization.

| Independent suite | Result |
|---|---:|
| Named launch-path readers, deep JSON, changing reads, contexts | 130/130 PASS |
| Actual finalization, legacy producer, checkpoint duplicate, identity fence, source census | 25/25 PASS |
| Speed types and malformed prediction/manifest containers | 66/66 PASS |
| Exact escaped/array duplicate paths and role controls | 30/30 PASS |
| Real pinned checkpoint validator with canonical and transient A→B→A streams | 2/2 PASS |
| Outside-NGC RO1 parity, plain and Stage0-only inactive contexts | 15,200/15,200 bytewise comparisons PASS |

The targeted total is **253/253**; the 15,200 parity cells are reported separately. Harnesses were written independently of the builder's generator/checker. They used inert module imports, synthetic owned records, actual production readers, and AST-extracted record/finalization statements. They did not execute a scientific chain or worker main.

TESTED coverage includes both headline and Stage0 contexts for column-mean results; rotation/column/tail-manifest finishes; `uvt_stage_records`; both admitted-route-A finish branches; route-A reader finishes/manifests/results; and both legacy/v011 producer-custody start reads. Additional reachable helpers include column_H, merged_brackets, bracket_check, and uvt_admitted_record_check. A duplicate in the actual post-chain finalization statement sets status REFUSED, valid false, and a typed reason. Duplicate diagnostics distinguish both occurrence paths through escaped member names and array indices. Separate objects with equal key names remain legal.

TESTED deep JSON either reconstructs iteratively or refuses with the typed depth boundary. Parse→hash, hash→parse, and parse→parse changing byte streams refuse. The real chain's first route-A result read and its later outcome read cannot disagree silently. The lexical-name/resolved-target fence was tested with synthetic identity injection; no real symlink was changed. Context state restores after these cases, pin tables remain unchanged, and global json functions are not monkeypatched.

TESTED checkpoint protection retains the original pinned canonical/integrity validator. A synthetic formatting-only A→B→A stream exposed a v001 gap: before/after reads saw A, while the actual validator consumed canonical B with equal decoded values. The selected build compares the reconstructed canonical byte SHA with the first snapshot and now produces NGC_CHECKPOINT_READER_SNAPSHOT_MISMATCH. The canonical control still passes. Historical failure evidence is retained without alteration.

TESTED row validation rejects bool/string/list/dict speed values with typed refusals before reader acceptance or column-mean arithmetic. It also rejects malformed conditional column-mean prediction containers and row containers. Numeric finite values, None, NaN, and Inf retain the existing caller's numerical validity treatment; this review does not declare them all numerically valid. Failure-status column-mean records may omit prediction. Registered N1 null-speed rows remain accepted by the structural boundary, and fired RO1 records may remain rowless. The v003 evidence records the earlier 24 failures, including boolean route-A valid=True and untyped TypeError/KeyError; all those cases pass their corrected expectations on the selected build.

TESTED source preservation: exact r006 prefix and main suffix remain byte-identical. An independent AST census covers all 48 strict clones and finds no remaining direct plain json.loads/json.load or Path read_text/read_bytes calls in those bodies. Selected serial/parallel RO1, outcome, and reader controls are exactly equal to r006. The broad outside-NGC parity domain covers worker roles, malformed worker pins, duplicate-last-wins starts/bindings, event/convergence states and binding shapes. Exact serialized returns or exception type/message are compared; traceback frame identity is not claimed. The inactive Stage0-only domain is also checked. Parent-owned full 78-spec dry-plan identity and registry checks are not counted as this lane's independent evidence.

UNTESTED: scientific launches, solver execution, full route-A/route-B stage replay, full saved-run checkpoint admission, calibration and observed/target velocities. No protected run, target-velocity, network, or session-log reads were used. All fixtures/evidence were written exclusively to new names. Required isolated Python with single-thread BLAS was used; largest measured RSS among the measured selected suites was 123,224,064 bytes.

Every file cited by this review is pinned below from its bytes. Result records also pin read sources and their synthetic fixtures where recorded.

- dispatch: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0581_2026-10-18_codex3_cx3r007_strict_launch_path.md` — SHA256 `3e6ea8a721e32546cc88703486edbca5b871bbffdc7cd66f1d3fa7d394371132`.
- selected driver: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py` — SHA256 `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69`.
- r006 parent: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` — SHA256 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`.
- build inventory: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/BUILD_CX3R007_V004.json` — SHA256 `4d5685d181f29a7a63081ffe0f1b0d103ce20fb2b9d23be3fb94b78c2b007c2b`.
- C2 strictness requirements: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r006_c2/strictness/REVIEW_RESULTS_STRICTNESS_C2V001.json` — SHA256 `48dee6b034ba0920d09ef14590e9212a2928fe534996607c4fdb6c3818263eb6`.
- C2 parity requirements: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r006_c2/parity/FINDINGS_INPUT_V001.json` — SHA256 `45a07af92329d135d62bab271b45cfb41b33e2002b2b270edc5e5511916c6ec9`.
- C2 parity review: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r006_c2/parity/REVIEW_RESULTS_V001.json` — SHA256 `21350654edee4b2505249a052437fd7acb201580a3f11fcd50626e32105f7385`.
- independent r006 read census: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/R006_JSON_READ_CENSUS_V001.json` — SHA256 `1ebf580a47e7dc26a817932628e5507a247ed911938d4a26687d52b3a4d74025`.
- selected strict clone census: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/edges_v004/CLONE_CENSUS_V001.json` — SHA256 `418fecf9a61d0ab43cae525d726168d55b2b069da5248fe354dd1a2d9f594662`.
- launch record results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/run_v004/RESULTS_V001.json` — SHA256 `e8ca3e6a432c94efeeecb36ad810b6f5e71d9f295d3f548b10a559659d206b84`.
- launch record outcomes: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/run_v004/OUTCOMES_V001.json` — SHA256 `b12fe0d6056c7792c46532add52d408f63a55fbe17a24e9559607a6e23a21b62`.
- edge results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/edges_v004/RESULTS_V001.json` — SHA256 `5f71fd7d37a9e71954810e8cc9f2f4bdb9408f0f3c38d82dc712a5b001920a66`.
- row type results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/row_shapes_v004/RESULTS_V001.json` — SHA256 `9039186ec3c24c5367127c4587a14d787079d92273b2818fbff6ffdf5a97e6a5`.
- exact path and role results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/path_edges_v004/RESULTS_V001.json` — SHA256 `fe209cfbb197e249d39aa5154b170d71b20eebc3f1574fa5eab45308a4e7c499`.
- checkpoint results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/checkpoint_v004/RESULTS_V001.json` — SHA256 `0248719d5f697d78775aed78172a0a2c9b750b8a2ba0eb71fcadcee60d91da36`.
- outside parity results: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/parity_v004/RESULTS_V001.json` — SHA256 `6f9e5a4ffabea21d113a9c0aba64a4339825dac0610b311dfda98a8108dca875`.
- checkpoint source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` — SHA256 `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114`.
- historical v001 checkpoint failure: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/checkpoint_v001/RESULTS_V001.json` — SHA256 `6df7489374f01b82e075dee8be3ebf3735ac771612999329240c4644ffda2621`.
- historical v003 row failures: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/row_shapes_v003/RESULTS_V001.json` — SHA256 `1c9b9732ba1104357d5c090e3b2374a56565ed22d8ead29de86b29283ad5124d`.
- audit_launch_records_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/audit_launch_records_cx3v001.py` — SHA256 `b30b29adc2a6c8e790fd0a7593773036c93ae6836c66fb79b133f92f3aa08f5b`.
- audit_edges_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/audit_edges_cx3v001.py` — SHA256 `baf70227374db403aedbb1b31f32c0353a950a3323e48ff68affef6e78d93919`.
- row_shapes_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/row_shapes_cx3v001.py` — SHA256 `3150cdaac010b1b21f394ff7ac242c5f5f08ebd8414c05bb224b4a889c7f5a3d`.
- path_and_role_edges_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/path_and_role_edges_cx3v001.py` — SHA256 `4671f4f99b3e89c3a89739375b3827ef57cfd69916848a6f291b0c4030a817e1`.
- checkpoint_aba_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/checkpoint_aba_cx3v001.py` — SHA256 `8d8f5fa67e39d656f4d79bd7bb3f020c947025f500efb11e10f5397fbf4fcbe9`.
- outside_parity_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/outside_parity_cx3v001.py` — SHA256 `33fe2a01190c35553e433a2ff65c9799e98f63bfc890f30373c9fde4088cbebe`.
- synthetic_io_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/synthetic_io_cx3v001.py` — SHA256 `513ebcc91fcc0a7d000d6669a58eb9eaa8a1285a76e0edb0178a893445e57c6d`.
- seal_review_cx3v001.py: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/independent/seal_review_cx3v001.py` — SHA256 `c20b9df24ff69edd2a16d3de736ddd7cdc223f02c1b6230307be1ba5f12a99f8`.
