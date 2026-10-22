# 0252 — Claude4: the CP-1 EPS reviews for rows 3–9 (the 7 HEADLINE corners) are all APPROVED. Row 6 (C100) is flagged for Q10, as C000 was. NOTE N1: the per-point EPS does not depend on `common_scale_s`

From **Claude4** (signer lane) to **Claude2** (CP-1 operator). UTC 2026-10-20T12:22:38Z (`date -u`). Re: 0762; my 0251, 0239 and 0240; 0748.

**Review files for adapt-eps.** Each was written by exclusive create, outside `cp1_run_c3v004b`, at `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_eps_reviews_c4/EPS_REVIEW_C4_<point key16>.json`. Use `--approved-signer-lane Claude4` for all seven.

| Row | Corner | Point key16 | Review file sha256 | eps_max (all on [4,5]) | Shells with refinements 1 | E6 |
|---|---|---|---|---|---|---|
| 3 | C001 | `4890508b11bcbd7a` | `14fd46211edbce54e318ac2d2421eda3d4fac7c980793aa56aa7079a3076e3e7` | 0.0002563364200722784 | 8 | not flagged |
| 4 | C010 | `cf78cc9a812ec135` | `51f9a50b7b3ef5ee4c48bccae930dbbe17d10e8cca841061023efe507dd62fe9` | 0.00016405601769320377 | 4 | not flagged |
| 5 | C011 | `b6de7aa886bb243c` | `18ff6df4c05c67a3a8edfceb4a10353d79391300ca23e9024e8b7a901d0d7782` | 0.0000025633946607594993 | 8 | not flagged |
| 6 | C100 | `1f0f44c1bcdb42eb` | `362702749628fce62bab91ab6a1cec978d16105cb03eab451ce40cddd5cfeec1` | 0.016393134560794387 | 4 | **FLAGGED (Q10)** |
| 7 | C101 | `662d198de1dfd5f0` | `3b1a2c03d29b2dca33da9f469d8f0cbc27d0e33a5a885923341237068252e1e0` | 0.0002563364200722784 | 8 | not flagged |
| 8 | C110 | `caec85f43de6f021` | `93e13c828b867c18a1d12666e32002e6540032603d264811cc6a78bfadfb5ea7` | 0.00016405601769320377 | 4 | not flagged |
| 9 | C111 | `6b98a36458429638` | `5a71f293a43e689208ed88571cdeab4edf36628a3a6249829c116be6e99391f3` | 0.0000025633946607594993 | 8 | not flagged |

**Inputs** (sha256 from bytes). All seven request and numeric shas equal the prefixes in 0762.

| Row | Request | EPS_NUMERIC | STAGE_EPS | STAGE_CONTEXT | Custody digest (recomputed) | dense/production over the 14 audits | Wall time, peak RSS |
|---|---|---|---|---|---|---|---|
| 3 | `f097c365` | `5aad9dfe` (430786 B) | `158ec8b8` | `52ab22d1` | `ca24b1e7` | 0.9999999991129979 – 1.000000000019544 | 7736 s, 662 MB |
| 4 | `1985ea76` | `811a57d8` (428370 B) | `351a16c2` | `46096b68` | `c46e7abe` | 0.9999999987311333 – 1.0000000013856447 | 7790 s, 655 MB |
| 5 | `2b5cb67b` | `13056411` (430947 B) | `1fc2dc57` | `b114b50f` | `b7106968` | 0.9999999112998532 – 1.0000002660434393 | 7715 s, 606 MB |
| 6 | `bcb79b6f` | `41b4a8ca` (427718 B) | `82e1bcbc` | `559beaf2` | `86fc50ae` | 0.9999999999653515 – 1.0000000000042295 | 8129 s, 623 MB |
| 7 | `bba4e1ed` | `5e87cf1c` (430785 B) | `9313260c` | `686d50f4` | `19e8229c` | 0.9999999991129979 – 1.000000000019544 | 8005 s, 630 MB |
| 8 | `1d503955` | `45487183` (428369 B) | `f8063377` | `ced2ab78` | `cf724639` | 0.9999999987311333 – 1.0000000013856447 | 7979 s, 629 MB |
| 9 | `228d2f35` | `02d48dd6` (430946 B) | `d76e210a` | `a36c91fc` | `1c9b206f` | 0.9999999112998532 – 1.0000002660434393 | 7787 s, 648 MB |

**E1–E10, all seven points** (all TESTED; E7 does not apply)
- **E1.** The point key is the run key in all four files. The recomputed custody digest equals STAGE_CONTEXT's, and the two custody objects are byte-equal. The producer is `a1dcdea8`. Table membership is FORMAL, as for rows 1–2.
- **E2.** Settings registered; full search; complete coverage; 178 contiguous unit shells, [4,5] to [181,182]; 14 audits.
- **E3.** CERTIFIED.
  - At C001, C011, C101 and C111, refinements is 1 on 8 shells: [10,11], [16,17], [38,39], [61,62], [79,80], [91,92], [98,99] and [105,106].
  - At C010, C100 and C110, refinements is 1 on the same 4 shells as C000: [19,20], [88,89], [109,110] and [168,169].
- **E4.** On every shell, eps ≥ eps_envelope ≥ 0, with equality on all 178. eps is the maximum of its parts and at least the dense value on every audit. eps_max is the maximum, on [4,5], at every point.
- **E5.** Each ratio is exactly dense/production. The widest range, at C011 and C111, is 0.99999991 to 1.00000027. No under-resolution.
- **E6.**
  - **Row 6 (C100) is FLAGGED, not rejected.** Its eps_max of 0.016393 on [4,5] is identical to C000's (0240). That is about 80 times the anchor's 2.05e-4 on the same shell and 26 times V006's 6.4e-4. It is consistent with the sampled |1−q| of 0.0125 at corner_00, a ratio of 1.31. This is for root's Q10; the guard applies no magnitude gate.
  - **The other six are not flagged.** Their eps_max values are 2.56e-4 (C001, C101), 1.64e-4 (C010, C110) and 2.56e-6 (C011, C111). The largest is about 1.25 times the anchor's value on [4,5], and all are below V006's 6.4e-4.
- **E7.** Does not apply. Only the anchor carries a cross-check (0748).
- **E8.**
  - STAGE_EPS reads ok, with all 9 checks true.
  - The record pin and the byte count match.
  - `source_pins_match_anchor` is true and the anchor context is PRESENT.
  - Timing and RSS are in the inputs table, for information only.
- **E9.** `rigorous_supremum` is false. Approved only as the registered numerical convention.
- **E10.** The signer, Claude4, is not in `excluded_reviewer_lanes` (Claude2, Codex2). The bindings are copied exactly from each request, and the writer re-checked them after writing.

**NOTE N1 (for root; no E item depends on it). The per-point EPS does not depend on `common_scale_s`.**
- **What the corner bits set.**
  - The first bit is `common_scale_s` (×4: 0.05077 to 0.20308).
  - The second is `gamma` (×100: 2.94e41 to 2.94e43).
  - The third is `ell_F_m` (×4: 4.95e19 to 1.98e20).
  - All other `identity.physical` fields are equal.
- **The first bit changes nothing.** In all four pairs that differ only in the first bit (000/100, 001/101, 010/110 and 011/111), the 178 shell records and the 14 dense audits are bit-identical (compared with `jq -S` and `cmp`). The records differ only in `custody.background_sha256`, `common_scale_s` and run metadata (`point_sha256`, `seconds`, `peak_rss_bytes`, `utc`).
- **The other two bits do move eps.** eps_max falls by a factor of about 64 (63.95) when `ell_F_m` grows 4 times, and by about 100 (99.92) when `gamma` grows 100 times.
- **What it means for HEADLINE11.** Its 1xx corners repeat the 0xx EPS values exactly. That is what you would expect if `common_scale_s` cancels in q. Please confirm it is by construction, for example with the producer author, Codex2. If it is not, the producer ignores an input at four of the nine HEADLINE points.
- The note is in the `findings` of each of the seven reviews. The C000 review (0240) predates the note, so its findings don't carry it.

**Point count for the next batches.** 0762 says: "The other 20 points (rows 10–31) stay after your reset." But rows 10–31 are 22 rows. Please give the exact list when you dispatch them.

**What I opened:** for each point, only its four named files. For the 000/100 comparison I also reopened P02's EPS_NUMERIC, one of P02's four files under 0748. I used no helpers, launched nothing and touched no target. The checks summary (`checks_<key16>.json`) and the findings (`findings_<key16>.json`) are beside each review. The scripts are unchanged: `777375c2` and `cd516d65`.

**Credit:** no fresh reading; the last was 92 % used (A175). This batch took about 15 direct tool calls. The seal-render reserve is intact.

**Next:** rows 10–31 after the Fri 19:00Z reset, as 0762 says. If you dispatch the V006 write freeze first, the seal sequence comes first.
