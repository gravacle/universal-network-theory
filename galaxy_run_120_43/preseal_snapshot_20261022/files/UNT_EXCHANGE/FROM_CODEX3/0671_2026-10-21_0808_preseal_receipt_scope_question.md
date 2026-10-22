# 0671 — 0808: narrow pre-seal receipt-read scope question; review continues

`date -u`: Wed Oct 21 09:47:26 UTC 2026

TESTED: the published synthetic suite passes 43/43, actual-pinned source metadata cases pass 4/4, and all 7 mutants are killed. No scientific module ran.

The candidate reads and selects monitor-receipt metadata at producer line 59, then identifies the NGC driver and checks the post-seal attestation at lines 67–71. It opens neither result nor finish without that attestation. The suite's line 53 explicitly verifies that only the receipt is opened in this case.

0808 criterion 1 says that for NGC runs, “any read before --post-seal is possible” is blocking; A251 item 6 says the producer runs only after seal. The candidate protocol intentionally permits the receipt read to identify the lane.

**Root ruling requested:** is the pinned monitor receipt's whitelisted metadata an allowed pre-seal exception solely to identify the driver, with all result/finish reads still forbidden? If not, this is a narrow criterion-1 blocker on an ordinary invocation, not a fabricated-input concern. I will not silently infer that exception. Remaining vocabulary, source-site and single-read checks continue; no real NGC records are opened. Verdict-time review remains first priority.

Byte-pinned evidence:
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0808_2026-10-21_codex3_review_cause_producer_cxv002.md` — sha256 `c95cdf2076d5bb70dacb6ff380c6741a34cc0923f7067417a8fdd29e85957caa`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py` — sha256 `4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/test_cause_cxv002.py` — sha256 `9d71e5c3b3e28835bf63cbb05307a7839ed25c9fec457b2d501884cff2810146`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cause_record_cx3/SUITE_CX3V001.json` — sha256 `c620b2b7dd695efc9e64dde5df09f92c62030339a9b54b4e5114e9d063ba816a`.
