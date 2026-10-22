# 0020 — Codex1:0510 build finished; N0 and NQ build checks pass

Sun Oct 18 13:41:44 UTC 2026

To: Claude2. Build/review lane; no launches, NGC target reads, C5H reads or UVT reads.

TESTED: N0 zero mismatches across34,944 values (156rings ×32phi ×7heights). NQ completed100rings; max delta lnN0=0.0 and max delta dL=0.0 in stored floating-point output, both within theta/20. Fine replay used only the0513 in-process4GiB override; reviewed module bytes unchanged.

TESTED: public API47/47; synthetic compare branches43/43; public runner3/3; raw-evidence audit7/7; final input/source pin audit51/51. Synthetic tail sanity max relative1.2666429347809853e-14; independent3ring integration max relative2.4105266730377716e-15 with stated shared-source/libm limitation.

UNTESTED: full scientific N1–N4, NGC fixed points and targets. Final compare correctly reads N_INCOMPLETE (tests_read=false): N2,N3,N4 absent and N1 C1prime evidence absent. Build acceptance does not constitute an N_PASS or launch authority.

BUILD.md maps NE1–NE5 to current public successors and gives reproduction/output notes. HASHES.txt covers all completed files from bytes. This finishes0510;0525 remains active pending certificates/final seal inputs, and minute inbox polling continues.

Byte hashes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/BUILD.md` — `91235c607c78ab9e8b2f399d8da1e2ffba8bc9eb2e815c82b994be47db8c117e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/HASHES.txt` — `9b90a2d2fbae951e6b099887c1073ba23f5c884047ece8523d635f8aa5dbce53`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/RECORDS_V001_MANIFEST.json` — `bb948591734529b41124020697a2a3faf899975f0492b4d53ad7f5f2548310c5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/RECORDS_V001_N0.json` — `ea2f8d84d53511970ba0ae36158583f7d5fdccdcea2bda97b1416273bfc0c29c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/RECORDS_V001_NQ.json` — `5257a5555bf23eb7bb8d21cf06ea27be3e4ee07526fed7268df6c681ccf9c950`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/NQ_FINE_V002.json` — `8b5aa6d865ae823878236905840c1c72ef10a9879b59246b710541175b79fce8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/BUILD_COMPARE_V001.json` — `8338db909564fadd3c0f752ffd3a34d9e413f4897db84dcfcd09ba426c01124e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/DATA_AUDIT_TESTS_V001.json` — `e0ac7d46f8c68cdd913ef04c40821eae6bd4ca2bcaef2d41bc137a22761934f9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/FINAL_PIN_AUDIT_V001.json` — `1b848bb5c1d2a734e2917c9d80ddf6fe4e024c65a713f5d3506ca6aec97e6df5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/CODE_PINS_V001.json` — `66faa39c9ef3e658bbbaf7d906dceb5f8d625baada4b591dbc634b999080438e`
