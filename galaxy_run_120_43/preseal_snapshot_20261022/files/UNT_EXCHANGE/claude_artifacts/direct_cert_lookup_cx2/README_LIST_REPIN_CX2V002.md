# CP-1 list/common c3v005 repin — review unit 1 of 0831

UTC (`date -u`): Wed Oct 21 12:36:49 UTC 2026

TESTED: 17/17 in-process checks. Three synthetic W3 points traverse the actual list loader, records assembler, c3v005 C1 policy gate, unchanged wrapper slot block and b1 guard under the six producer pins read from frozen C1. Synthetic custody is explicitly supplied; there is no physical producer execution or production certificate claim. The old list path refuses the same six-producer C1 with exactly three canonical-producer blockers. Existing three-producer compatibility remains. Wrong-point rho slot, unknown producer, nonboolean policy OK, reordered review and wrong genesis are refused.

FORMAL and TESTED AST equivalence: common changes only ASSEMBLER (to adopted c3v005); assembler changes only COMMON2 (to the new common). A leading comment identifies each successor. All other AST nodes are identical. The legacy `c3v004_assembler` JSON field name is preserved; its value is now the exact c3v005 pin. The list/records/verify schemas, bundle/registry logic and all 31 table rows remain unchanged. RUNNER and COMMON pins are unchanged; the live CP-1 runner is unaffected. No HEADLINE11 source is changed.

Use the new assembler path with the existing bundle/records/verify CLI and list flags. In particular, the full `verify` report (not the short stdout summary) is obtained with its existing `--out-root` option. Existing records produced by the old list assembler retain their pins and can be verified by this successor. No regeneration of existing numeric records, proofs or bundles is required by this repin.

The original read behavior is retained exactly; this narrow repin does not claim a new single-read contract. The forthcoming direct lookup will snapshot its inputs once. No subprocess, network operation, deletion, rename or overwrite occurred in these tests. All test outputs were exclusive creates below LIST_REPIN_TESTS_CX2V001. No actual point data, run tree or NGC file was read. UNTESTED: physical custody, actual CP-1 proofs, production CLI execution and launch admission. Root adoption remains pending.

## Byte pins
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/cp1_points_common_cx2v002.py` — SHA256 `658593278f428a1937daa0a40837cd3d8e10e6ad7acf0e479508bdbb04362934`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/cp1_points_assembler_cx2v002.py` — SHA256 `1b701591714c11856d525631f946d19a64f76f28041da21c6e9f1a62863b0e88`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/test_list_repin_cx2v001.py` — SHA256 `43b20f84b973edb0e22b11bcfd4cd92bad045d09dfd47c9c0d5ad8e3898e7c3d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/LIST_REPIN_TESTS_CX2V001/TEST_REPORT.json` — SHA256 `75628e203026d0d3b9e7d8bbd9616e115ca6d869e5c1b606821ae4baa47defb8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/cp1_points_common_c2v001.py` — SHA256 `302abdad6b076190f7bc8e79cc71cf4de91402a1a216eb94c254acf2be22c27e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/cp1_points_assembler_c2v001.py` — SHA256 `951e7203a676afe3cdf566d54970cf5a7d574fbb4cc4c485cd628aca2c0da3af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py` — SHA256 `7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json` — SHA256 `4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1`
