# REVIEW: BUILD_V006 delta against BUILD_V005 (Codex1 0055), Claude4 for dispatch 0602 item 1

Claude4. Written 2026-10-18T20:18:03Z (`date -u`). One refute-by-default delta lens, then a refuter for each of its two leading should-fix findings. No launches; no target, C5H or `UVT_*` reads.

## VERDICT: PASS_WITH_FINDINGS. 0 BLOCKING, 3 SHOULD_FIX, 8 NOTE

The tests of record pass 228 of 231. The 3 failures are the three should-fix findings. The real guard v008 was loaded under its real name with only CONFIG and REGISTERED patched, and the fence blocked nothing.

**What holds:**
- **(a)** All 180 V005-pinned paths are byte-identical, and all 38 V006 pins match. The 4 supersessions are BUILD, ALLOWLIST_DRAFT, PRODUCER_INDEX and RUNBOOK V005→V007, each justified by 0599/A87, 0600/A88 or 0601/A89. The one exception is an unjustified prose edit (V6-N5).
- **(b)** The new producers refuse before the seal across a 14-variant admission matrix and at every entry call. There are no import-time writes, process events or network events.
- **(c)** 88/88 output-path refusals pass. `check_run_path(out, False)` runs immediately before the single exclusive open.
- **(d)** r11's own `evaluate_gate` reads the records as expected, apart from the SRB boundary note (V6-N1).
- **(e)** The allowlist grows 13→15 with the prior 13 entries identical.
- **(g)** The rulings writer adds no decision.

## SHOULD_FIX (both leading ones reproduced by their refuters)

| id | finding | fix (owner Codex1) |
|---|---|---|
| V6-S1 | `postseal_records_cx1v006` accepts an overflowing literal (1e999 → inf). It streams `json.dump(..., allow_nan=False)` into the already-created exclusive file, so a ValueError mid-write leaves a truncated, unparseable file at the exclusive output path. The same streaming pattern exists in srb L114. | Reject non-finite parsed numbers; serialize to a string first; then `check_run_path` and `open(out, 'x').write(text)`. Same in srb. |
| V6-S2 | RUNBOOK_V007 omits the A85 items 2–4 launch steps: T-runs at normal QoS, non-critical processes under -b, step-2 outputs on the internal SSD, and `caffeinate -i -w <launcher pid>`. The pending r5 template P128/LAUNCH_PLAN_V010.json names External1 runs_ext 51 times, which A85.3 rules out. | A RUNBOOK successor with the A85.2–4 steps; root's output-location choice before the plan is bound (RI-25). |
| V6-S3 | RUNBOOK_V007 L15 still says "allowlist remains13 sources". A root config built that way refuses all four post-seal writers, so I1T and SRB_ROT would read INCOMPLETE. | A successor text naming BUILD_V006's 15 rows; the root config producer_allowlist equals them exactly. |

## NOTE (8)

- V6-N1: the SRB writer's `<= tau/10` versus r11's `> 0.1*tau`, one ulp apart at exactly 0.1·τ; it fails closed.
- V6-N2: A88's "one-line" r12 change is not enough, because r11 also lists SR_K in GATE_RECORD_SHA_REQUIRED.
- V6-N3: cross-references are checked only against the writer's own manifest.
- V6-N4: Claude3's registries do not yet list the two new producers.
- V6-N5: a runbook prose edit with no ruling behind it.
- V6-N6: admission is re-hashed per JSON object (cost only).
- V6-N7: an index key renamed (cosmetic).
- V6-N8: `.pyc` precedence over the hashed `.py` sources (none exist now).

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `delta/REVIEW_V006_DELTA_C4V001.md` | `df893f1e106a2e68ca0bee47b69aab0b91e3e359c810c90aa38c03c1095c78e0` |
| `delta/RESULTS_V006_DELTA_C4V001.json` | `80fa261f483994b0a2916ef899a863a8d3a4e2522555c3f89fdf4b29a74735c6` |
| `delta/HASHES.txt` | `b577e8a44538b6a02850fec169ecb2df1c7b5d2034dddf8a1e71a76b00f624d5` |
| `verify_1/VERIFY.md` | `93e07d11b7b6d83c2d421cf0deb4760eb0c3e98c638905ae07cf6df123f8ef51` |
| `verify_2/VERIFY.md` | `c79c61774eff41b9c6a831f26fa0b9bdfdef5c6b5298a51b21387ea4af79feb2` |
