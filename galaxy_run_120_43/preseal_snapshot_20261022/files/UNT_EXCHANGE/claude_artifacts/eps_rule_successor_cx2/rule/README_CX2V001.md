# A296 saved EPS rule successor — review candidate CX2V003

Date: `Wed Oct 21 17:35:14 UTC 2026` (`/bin/date -u`).

Current candidate: `eps_negligible_rule_cx2v003.py`. This standalone standard-library tool performs only saved-record arithmetic. It does not search an envelope, import a scientific project module, run a solver, launch a monitor or admit a scientific run.

R1 requires exactly one originally failing shell, refinements=2; every other shell must still certify under the saved original1.1 comparison. The input must be a byte-pinned, canonical-producer EPS record with registered settings, TESTED status and all178 contiguous unit shells covering[4,182]. It requires10*measured_shell_eps<=0.1*original_eps_max, abs(L2-L1)<=1e-6, and an authenticated registered dense audit for the same record, point and shell with dense/production<=1.05. Multiple originally failing shells refuse under R1(d).

R2 changes only that shell's consumed eps to10*the stored measured eps and discloses `eps_measured_before_negligible_substitution`. It preserves the original eps_max, eps_max_shell, shell certified=False, refinements=2 and record registered_discrete_verdict=EPS_UNCERTIFIED. This preserves the original discrete result honestly. All other shell dictionaries are unchanged.

R3 sets overall verdict to `NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED`, adds successor_rule_verdict=ACCEPTED_NEGLIGIBLE and accepted_shells, and explicitly requires approved-signer review. The new producer pin identifies this tool; predecessor record and original producer pins remain disclosed. production_admissible=False and rigorous_supremum=False remain unchanged. Root adoption is still required. Old adapters/guards must reject until a separately reviewed successor explicitly supports this branch.

R4: an already certified original returns UNCHANGED and writes no new EPS record. The rule has no row-number special case. Invalid/missing metadata, nonfinite or Boolean numeric values, gaps, inconsistent levels/maxima, wrong byte pins or audit identities, and multiple failing shells refuse. Output uses exclusive xb; existing paths refuse. A failed output write can leave a partial new file, which must be preserved and a new output name chosen.

Dense audit contract (the audit producer performs the separate scientific work; this tool does not):
- schema UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001; status TESTED; settings registered.
- source_record {path,sha256}; point_sha256; original_producer {path,sha256}; audit_producer {path,sha256}; range_inverse_kpc.
- production equals the saved shell.envelope.estimate; dense equals dense_search.estimate; dense_over_production equals dense/production.
- dense_search has registered torus_m20, direction_count400, starts16, n_grid16000000 and radial_fractions[0,.25,.5,.75,1]. Additional provenance/validation fields are preserved in the separately pinned audit artifact. No seed value is invented by this consumer.
- The CLI independently hashes the audit artifact and the audit producer source against explicit caller pins. Byte identity is not signer approval: the audit producer's pinned bytes must be scientifically reviewed/adopted by the authorized owner. The consumer does not execute or import that producer.

CLI: pass --record, --record-sha256, --output; for a failing record also pass --audit, --audit-sha256 and --audit-producer-sha256. Run with the required isolated Python, six single-thread environment variables and nice-n10. All outputs are new files; no input is modified.

TESTED:89/89 checks passed, including31 real genesis in-process CLI calls that returned UNCHANGED, created no output and left source bytes unchanged; missing-audit refusal for real rows302,501,504; in-memory SYNTHETIC audit-contract substitution checks; exact/adjacent-float boundaries for fraction, absolute floor and audit ratio; malformed/nonfinite/Boolean/coverage/identity/multiple-failure cases; refusal of existing output or wrong supplied hashes. The synthetic positive audit objects are never saved or claimed as real audit evidence. No successor for a real point was written by these tests. Runtime: nice unavailable (sandbox);0514 waiver; requested Python isolation and six thread variables applied.

UNTESTED: actual dense-audit execution/results, real-point accepted successors, downstream admission support, independent review, root adoption and any scientific launch. These remain separate work.

The first immutable test report exposed an overly strict assumption that eps_envelope always equals the production envelope estimate. Saved records can replace eps_envelope with the larger registered dense audit estimate. Current candidate correctly checks eps_envelope>=production and stored measured eps>=eps_envelope. Earlier candidate files remain immutable and are not the reviewed candidate.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/rule/eps_negligible_rule_cx2v003.py` — sha256 `669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/rule/test_eps_negligible_rule_cx2v002.py` — sha256 `e4169e7649586d74db7f81135224e4a251f599f078de88837db48bfc547410c7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/rule/TESTS_CX2V002.json` — sha256 `3b0220d5f4d0a3d06e2a9259ffcd4a6a3556b69d36c95c78775bc346de47b4a6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/A296_AUTHORITY_CX2V001.json` — sha256 `d1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0855_2026-10-21_codex2_claude3_A296_final_text_build_now_and_F5_gap_proposal.md` — sha256 `1541dad07b9d14d994fc7f595c8276f2f0555f38b67f1c8fd1142d883fa36b5a`.

The test report records byte pins for every real certification input it reads.
