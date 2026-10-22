# Cause-producer cxv002 review — Codex3 CX3V001

`date -u`: Wed Oct 21 09:51:43 UTC 2026

**PASS — 0 blocking findings** within the four criteria of 0808, with its pre-seal receipt boundary settled explicitly by 0809. This is a review of the producer candidate, not adoption or launch approval. [0808_2026-10-21_codex3_review_cause_producer_cxv002.md](</Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0808_2026-10-21_codex3_review_cause_producer_cxv002.md>) [dispatch] [0809_2026-10-21_codex3_preseal_receipt_read_allowed.md](</Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0809_2026-10-21_codex3_preseal_receipt_read_allowed.md>) [scope_ruling]

The reviewed candidate is [cause_record_cxv002.py](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py>) [producer] (sha256 `4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3`), with the byte-pinned selector and vocabulary in the source register below. The assignment's generic c2v001 name resolves to this cxv002 file through Codex1's numbered report. [0173_2026-10-21_0807_cause_site_set_PASS.json](</Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0173_2026-10-21_0807_cause_site_set_PASS.json>) [builder_report]

## Findings against the four criteria

1. **TESTED / FORMAL — scalar and pre-seal boundary passes.** The reader permits exact scalar paths, refuses a container at a selected scalar, and skips unselected string/numeric values without decoding them. Tests include forbidden selection, duplicate keys, selected containers, missing/non-object stage records and an independent decoding spy. The raw file is hashed and syntax-scanned; object keys are decoded for path selection and duplicate-key detection, as the stated reader contract discloses. This is not a claim of zero physical byte access to skipped data. No scientific array/object is materialized. [metadata_selector_cx1v002.py:16](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/metadata_selector_cx1v002.py:16>) [selector] [metadata_selector_cx1v002.py:55](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/metadata_selector_cx1v002.py:55>) [selector] [CAUSE_PROTOCOL_CX1V001.txt:12](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/CAUSE_PROTOCOL_CX1V001.txt:12>) [parent_protocol]

   Producer line 59 reads the receipt first. It gates NGC result and finish before opening either at lines 67–71. The independent test confirms that a missing attestation opens only the synthetic receipt. I raised the literal “any read” question in 0671; root's 0809 explicitly permits receipt metadata solely for identifying driver/run class and forbids result/finish reads before the attestation. The observed behavior therefore passes the clarified criterion. No real NGC record was used to test it. [cause_record_cxv002.py:59](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:59>) [producer] [0809_2026-10-21_codex3_preseal_receipt_read_allowed.md](</Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0809_2026-10-21_codex3_preseal_receipt_read_allowed.md>) [scope_ruling]

2. **TESTED / FORMAL — no demonstrated non-model admission.** The vocabulary is hash-pinned in the CLI path. Every listed module is rehashed; the selected token's set must be nonempty and all entries must have model_outcome=true. Empty, mixed, incomplete, changed-module and absent-site cases refuse. Clean exhaustion has priority and does not fall back after a failed site-set test. Generic FAILED, FAILED_SOURCE_PREPARATION, a signalled/nonzero stage and missing stage evidence are excluded. The pair operation requires two distinct receipt hashes, equal spec/driver and stage/status/code/class/site, and separately bound solo declarations with integer zero other-process count. [cause_record_cxv002.py:39](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:39>) [producer] [cause_record_cxv002.py:72](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:72>) [producer] [cause_record_cxv002.py:110](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:110>) [producer]

   The classification emission at driver line 1916 covers nonconverged source records. Its use in the reviewed set depends on the producer's explicit FAILED_SOURCE_PREPARATION exclusion; that exclusion is exercised in both the supplied and independent tests. This review does not relabel source-preparation or generic numerical exceptions as model outcomes. [galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py:1905](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py:1905>) [NGC_driver] [cause_record_cxv002.py:81](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:81>) [producer]

3. **TESTED source census / FORMAL origin review — no missing specified model site found.** I independently parsed and hashed all 145 distinct declared source modules, verified closure of the declared pin edges and compared every exact-token literal outside comparisons with the vocabulary. The DDO conservative union contains 121 modules and the NGC union 144. The four NGC status handlers at 3566, 6107, 7853 and 9066 are inside RouteANoFixedPoint handlers; the classification emission at 1916 is also present. The five ITERATION_BUDGET_EXHAUSTED emissions are terminal _finish calls after the bounded source loop, with converged_finite_fixed_point=false, outside loop/exception-handler bodies. No omitted exact emission was found within this source union. All four inert combinations of the actual pinned driver vocabulary and the two allowed tokens count as expected. [galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py:3566](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py:3566>) [NGC_driver] [CAUSE_VOCABULARY_CXV002.json](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_VOCABULARY_CXV002.json>) [vocabulary] [INDEPENDENT_CX3V001.json](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/INDEPENDENT_CX3V001.json>) [independent_result]

   The complete 145-file byte-pin list and source expressions are preserved in the independent result, including the five solver paths/hashes and the controller/library inventory. This is a static source-union review, not a claim that every historical/optional branch executes in one attempt, nor a proof about arbitrary dynamic imports or future code.

4. **TESTED / FORMAL — single-read and binding pass.** OneRead uses the same byte buffer for hashing and selection, caches by inode and checks file metadata before/after reads and aliases. The finish's result_path, result_sha256 and status must match the pinned monitor receipt; a mismatch in any one of these is independently tested to refuse before result access. The result's status must then match. This implements A251's specified authentication through association; it does not invent an independent monitor pin for finish. [metadata_selector_cx1v002.py:116](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/metadata_selector_cx1v002.py:116>) [selector] [cause_record_cxv002.py:77](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py:77>) [producer]

## Validation and limits

**TESTED:** supplied synthetic suite 43/43; actual-pinned-source inert cases 4/4; mutants 7/7 killed; 20 additional independent checks; 145 source byte hashes and exact-token AST census. The seven published mutant files were byte-compared with their specified single edits before running them. Each Python subprocess used the required interpreter with -I -B and single-thread environment. Fixtures are retained under new names. No scientific module was imported/executed; source files were read and parsed only. [SUITE_CX3V001.json](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/SUITE_CX3V001.json>) [suite] [check_cause_cx3v001.py](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/check_cause_cx3v001.py>) [independent_checker] [INDEPENDENT_CX3V001.json](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/INDEPENDENT_CX3V001.json>) [independent_result]

**UNTESTED:** first real failure classification; actual seal attestation authority; downstream P-112/builder integration and the final invalidating-pair decision. The producer accepts trusted root-pinned metadata, cause outputs and solo declarations, with no signature or independent seal-execution proof. Python dependency injection is an inert-test interface, not exposed by the CLI. The reader's 16 MiB limit, parent-directory symlink allowance and non-strict Unicode validation of skipped strings are disclosed contract limits; no honest pinned-producer blocker from these was demonstrated in this pass. [CAUSE_PROTOCOL_CX1V001.txt:13](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/CAUSE_PROTOCOL_CX1V001.txt:13>) [parent_protocol] [CAUSE_PROTOCOL_CXV002.txt:21](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_PROTOCOL_CXV002.txt:21>) [protocol]

The A252 output is a set of reviewed possible origins, not a traced executed traceback. Downstream consumers must accept the canonical SITE_SET and, where applicable, CLASS_SET strings. No actual attempt pair was consumed here. [CAUSE_PROTOCOL_CXV002.txt:16](</Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_PROTOCOL_CXV002.txt:16>) [protocol]

Authorship: Codex1 built the cause producer; Codex3 independently reviewed it. Codex3 also authored the NGC driver lineage, so source-lineage checks here are not an independent scientific revalidation. Verdict-time review remains first priority.

## Byte-pinned evidence

Every named citation above is bound to these full hashes computed from bytes. The independent JSON contains the additional 145-source manifest.

- **dispatch**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0808_2026-10-21_codex3_review_cause_producer_cxv002.md`
  SHA-256 `c95cdf2076d5bb70dacb6ff380c6741a34cc0923f7067417a8fdd29e85957caa`; 1612 bytes.

- **scope_ruling**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0809_2026-10-21_codex3_preseal_receipt_read_allowed.md`
  SHA-256 `48f571540c6dcc229a7d3e956c0bd1e30b2a65c17540e0f834d06e4d6000a59a`; 926 bytes.

- **builder_report**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0173_2026-10-21_0807_cause_site_set_PASS.json`
  SHA-256 `27824158c6a80c4219cee19ba17f118a488a19509ee52e463d4334758be19413`; 6213 bytes.

- **producer**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py`
  SHA-256 `4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3`; 10231 bytes.

- **selector**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/metadata_selector_cx1v002.py`
  SHA-256 `86a71335a13457ce92c1bb0caa6632d17c5a8c5c27252f08777dabe9a975d90f`; 7664 bytes.

- **vocabulary**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_VOCABULARY_CXV002.json`
  SHA-256 `839c75774c28c6c8213180df7e204ba5b9d0fbc63531591d22d9912149f8df37`; 417976 bytes.

- **protocol**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_PROTOCOL_CXV002.txt`
  SHA-256 `dcd08ad11f23b12a0bbb38d6baceff54e878b02f7864c1940d7fdea6f701098e`; 4576 bytes.

- **parent_protocol**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/CAUSE_PROTOCOL_CX1V001.txt`
  SHA-256 `97d8e043acf8a95489e4048348560fd8b1b7294442cc0cb466e6115a5fb54976`; 4539 bytes.

- **builder_tests**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/test_cause_cxv002.py`
  SHA-256 `9d71e5c3b3e28835bf63cbb05307a7839ed25c9fec457b2d501884cff2810146`; 7660 bytes.

- **pinned_tests**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/test_pinned_vocabulary_cxv002.py`
  SHA-256 `858511d5f1a3bdf41b7b54f3082957808f22b22b5a0894f6dc3e589fad7dba9d`; 1555 bytes.

- **vocabulary_builder**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/build_vocabulary_cx1v002.py`
  SHA-256 `882087e84624205776a3c636ca04a186186d5fe343fa188713342125771c2319`; 2015 bytes.

- **pin_scanner**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/scan_pins_v002.py`
  SHA-256 `84679b172eb057e599b4ca0bb2f1f43736bb5c7ce1e58a566a21642a2267a4a1`; 4642 bytes.

- **suite**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/SUITE_CX3V001.json`
  SHA-256 `c620b2b7dd695efc9e64dde5df09f92c62030339a9b54b4e5114e9d063ba816a`; 17435 bytes.

- **independent_checker**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/check_cause_cx3v001.py`
  SHA-256 `4c2b97dcf0f41a3cf007e523aa7e0d7ae9361d1c23d2a6b30db257b964de3d57`; 10570 bytes.

- **independent_result**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/INDEPENDENT_CX3V001.json`
  SHA-256 `80065403fda37d56a217c6dab06d941e78eab29e638f08c4291a2124de9e9711`; 56667 bytes.

- **DDO_driver**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py`
  SHA-256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`; 350370 bytes.

- **NGC_driver**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py`
  SHA-256 `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`; 669113 bytes.

