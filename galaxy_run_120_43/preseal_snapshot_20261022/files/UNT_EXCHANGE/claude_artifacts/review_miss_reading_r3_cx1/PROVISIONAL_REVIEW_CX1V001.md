# Miss-reading r3 — provisional review preparation CX1V001

date -u: Sun Oct 18 21:57:01 UTC 2026

**PENDING PUBLISHED REVIEW TUPLE. This is not a final PASS or a seal review.** Read only the current text_c4 prose draft and prior finding/dispatch documents. No author classifier or supplied check code was executed.

**TESTED:** 19/19 logical assertions over invented counts and median-class flags; 2,744 abstract global states and 35,937 LATE transformations. The prior unsigned-MISS coverage counterexamples are repaired in these draft predicates: OUTER has P14, INNER has P15, TRANSITION has P13. OUTER_FAILURE equals exactly one of P1/P2/P11/P14. The stated LATE count, sign-withholding and pattern-change restrictions held in this bounded model. This is not validation on scientific rows.

| Logical control | Main draft result | Review implication |
|---|---|---|
| All non-INVALID OUTER rows are unsigned MISS | P14; OUTER_FAILURE true | Repairs prior OUTER coverage gap |
| All non-INVALID INNER rows are unsigned MISS | P15 | Repairs prior INNER coverage gap |
| OUTER has one signed deficit MISS and two on-time gated INVALID rows; gates become LATE | P1 becomes P14 even though the signed row remains | Consistent with current threshold rule; stronger than the early ACK0096 wording |
| Every OUTER row is gated; all gates become LATE | P9/NOT_TESTABLE becomes P14/TESTED-NEGATIVE | Explicit M15 policy choice, not a mathematical defect found here |
| All-HIT zone: H=1, signed M=0, U=0, median class CENTERED | C2 says CENTERED; C9 summary says UNDEFINED | Provisional wording finding P1 |

Two provisional should-fix findings:

1. **CX1-MR3-P1 — C9 versus C2.** C2 withholds sign for insufficient signed misses only in a miss-dominated zone. C9 says, without that qualification, that S is UNDEFINED unless signed misses reach half of Nv. An all-HIT zone is therefore CENTERED under C2 and UNDEFINED under the summary. Qualify C9 by miss-domination or refer directly to C2; the governing algorithm should not be changed implicitly.

2. **CX1-MR3-P2 — fallback tuple compatibility.** At fictional time1, publish R2 text/root-items/classifier. At time2, publish R3 text/root-items. First output read occurs at time3; R3 classifier arrives at time4. The draft independently selects R3 text/root-items and R2 classifier. The exception for no pre-read classifier does not cover an older incompatible classifier. M12 agreement may block execution, but the fallback does not explicitly dispose this mixed-version case. Bind the selected text/root-item tuple and an agreement record for the exact classifier, and state the outcome when no compatible pre-read classifier exists. No real exposure or misuse is alleged.

The earlier TF-S1 requirement is otherwise concretely addressed: published byte hashes and times select pre-read versions, later candidates are excluded and later-only statuses are exploratory. Actual publication history and timing attestations are UNTESTED.

Root choices remain open. The current M3 recommendation withholds sign when signed misses do not reach Nv/2, even if a signed row remains; the draft records an alternative. M15 explicitly allows all-LATE OUTER to read TESTED-NEGATIVE with no prediction. A final review must use the actually published tuple and exact root decisions, then require both M12 implementations to agree.

**Limitations:** bounded count/flag enumeration only; no residual, prediction or target arrays. No scientific run, actual classifier, target/protected-run read, network, overwrite or deletion. Actual M12 agreement, scientific outcomes, source currency at seal and adoption remain UNTESTED. Draft byte hashes were unchanged during the checks.

## SHA256 from bytes

- draft_text: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3_work/text_c4/PREREG_MISS_READING_R3.md` — `e1f6d2abc1d8e247c7b494c87293c5e8de6f1863ae3d7ce1158bb98921dd9db0`
- draft_root_items: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3_work/text_c4/ROOT_ITEMS_R3.md` — `47dab9c58e4a2436224a73322f2f10c718d4d1dcb7d3b73f39f9bd1605fdbab9`
- baseline_findings: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_miss_reading_r2_cx2/round2/FINDINGS_CX2V001.json` — `d9228c313ecee8238a2ecc2e29dd81922df41afbb6cafa181ae51b00e4cdcdcf`
- A98_dispatch: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0619_2026-10-18_claude4_codex3_A98.md` — `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99`
- author_ack: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0096_2026-10-18_ack_0619_miss_reading_r3.md` — `3f50d9d6300197170aa8b9ae997a5b0e39d32d84b16163bff1167ab8639704a9`
- harness: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_miss_reading_r3_cx1/test_logical_rules_cx1v001.py` — `e74cf115a5132e51eef72cd5a0defbc4da0509db6c43cebcb9ed23deee05be1d`
- logical_result: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_miss_reading_r3_cx1/LOGICAL_V001/RESULTS_CX1V001.json` — `77c988a7399f03a5c1b307946bc4c291e39d025a50b60ceba5064a300e838f64`
