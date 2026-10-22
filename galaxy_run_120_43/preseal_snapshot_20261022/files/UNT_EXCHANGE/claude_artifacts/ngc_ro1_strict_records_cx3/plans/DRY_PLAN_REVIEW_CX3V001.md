# cx3r006 dry-plan identity and registry

Date -u: Sun Oct 18 16:49:52 UTC 2026

**PASS (TESTED): 78/78 case outcomes and every emitted artifact agree with r005 under the closed identity-only substitution rule.** These comprise 61 nonempty dry plans and 17 equal refusals; refusals are not counted as plan passes. All 78 fresh baseline outputs also match the previously reviewed r005 outputs.

The exact ordered case set is preserved, with 78 source-file byte hashes rechecked. Canonical set SHA256: `155b1095984c393426c90b43ec744e74a7d05f0f3628b26d017926d448caa875`. Each case retains its name, path, source class, galaxy, aliases and hash; only the old execution-output directory is excluded from this canonical identity.

Compared 934 artifacts: 377 raw-equal, 557 equal after identity substitutions, zero residuals. The only seed substitutions are the successor self path/hash and per-case output root (containing the report tree and the harness log). A derived hash is admitted only after the corresponding same-relative-path artifact is already byte-equal under proved substitutions; every proof and usage is recorded. No fields are ignored and no arbitrary identity digest is normalized. No short-hash substitutions were needed. Exit values, exception text, stdout/stderr, read and write sets, simulated Ctx modes agree. The 14 inactive-context RO1 traces contain exactly one additional r006 delegating-wrapper call per old outer-wrapper call; the comparator proves the previous function ASTs unchanged, verifies the new wrapper directly returns the old function with identical arguments when inactive, and checks the remaining trace exactly. This documented internal-call difference is separate from emitted-artifact identity. Traceback function/source-line sequences also agree; source line numbers are not an artifact identity requirement.

The new registry names r006 and preserves exactly the eight prior NGC source-readiness fixture specs. This registry is not a prediction or scientific-launch approval.

Audit: zero blocked events, zero overwrites, zero scientific stages. Python used the prescribed isolated runtime, numpy/stdlib, single-thread BLAS, six bounded cases per driver. Peak RSS was 349945856 bytes, below 8 GB. macOS rejected RLIMIT_AS before driver import in the first wrapper attempt; immutable v002 records that host limitation and checks observed RSS during calls and at completion. The failed v001 run is preserved and excluded from test counts. The first comparison already found all emitted artifacts equal; it separately flagged harness-log output paths and added wrapper calls. Comparator v003 applies the documented output-root mapping and exact inactive-wrapper trace mapping, without rerunning or changing driver outputs. These are harness metadata corrections, not scientific-source changes. RSS evidence is measured, not a guaranteed hard address-space cap.

**UNTESTED here:** scientific runs/predictions, malformed-record RO1 correctness (owned by the parallel review lane), and specs outside this exact 78-case set.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/galaxy_m0_forward_c2v011_cx3v005_cx3r005.py` — SHA256 `f85746f0bdfd3c108771225eff7c8a55a81e5d6634ee0e5403cf68aa9fa3dd6b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` — SHA256 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/SPEC_SET_78_CX3V001.json` — SHA256 `6b91a8f2c2b226402b34d5c1cc863027cde4d27ddece9a1d22fa96f3e32f87bd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/DRY_PLAN_IDENTITY_CX3V002.json` — SHA256 `ac6bb90215a5dcfdd81e4d27f02b34015fa835c767c99e5aee9816322257488a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/SPEC_REGISTRY_CX3R006_V001.json` — SHA256 `3c42ca07a4e2469bcb2be8b5a6ea69e3d696d8f5aca1b1ebadecd20242af90c1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/INPUT_HASHES_CX3V001.json` — SHA256 `4df52124abc4da057c658d1bb5ace7b0bfe675ebb7f5fa98170148613d8c4933`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/DECISION_CX3V001.json` — SHA256 `7714088f447b34c56031132d1ed1577cf7ad17e45dcadee02e06068c9cd94b64`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/RUN_P_CX3V001.json` — SHA256 `56fdb8bd266cd9326649741b86ca2eca44f58f325ab1c57100e6fdbd511bba80`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/RUN_P_CX3V002.json` — SHA256 `c3ab76e638f77b36f1cb21d0fb799af678451799f2045ff27c5fced7570337e1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/RUN_S_CX3V002.json` — SHA256 `2664d65fb3db5efa269aa9235ec602c46c07befb2231b90be47ad8e6426f17c5`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/dry_one_cx3v002.py` — SHA256 `45cf87159ee3227167e7623ef4fb9a4f6f0a77b436f569409c2f5bfd8b635045`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/compare_cx3v003.py` — SHA256 `c88186c751bc8468b97bda137d8e7ea6f0a293eeda32ebc77d93f05edd2133ea`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/plans/seal_cx3v002.py` — SHA256 `c57c64dfad85df42af1ec1e71b5eaff08bbae0cf38aa46f62b66107b7edfc28b`.
