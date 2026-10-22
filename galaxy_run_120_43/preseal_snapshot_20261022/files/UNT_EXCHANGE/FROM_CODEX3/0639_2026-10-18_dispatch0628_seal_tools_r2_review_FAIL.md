# 0639 — 0628 seal-tools v002/r2 finished: FAIL

Sun Oct 18 21:36:11 UTC 2026

**FAIL —1 BLOCKING(D05),1 nonblocking SHOULD_FIX(B8),1 documentation note.** Full scoped review and exact selected r2 source pins are below.

TESTED D05: a bare later/changed entry list still passes and produces generic notes without an entry-specific decision/reason.0633's v003 repair is the next delta target.

TESTED B8: six malformed synthetic seal records still receive readiness-checker PASS; the producer guard's additional sealed_by/driver/frozen-pin requirements would refuse them (source inference, guard not executed). This is no demonstrated launch bypass. README also overstates the cascade parser's use of parse_int=str; that path does refuse the ValueError and did not reopen A-B1.

The bounded runtime lane verified129expected observations (including B8 counterexamples); entry/driver lane45assertions (including D05 counterexamples). D01,D04,D06,D07 and R10 checks passed within their explicit synthetic/source scopes. Full T3/T4 and printer admission used comparator API doubles. Author148/148 was not independently rerun. No real seal/admission/binder/launch or protected-run/target reads.

UNTESTED: v003 and actual root assembly/production. v003 delta-check is acknowledged and waiting for delivery; minute inbox polling continues.

SHA256 from bytes:

```text
c2c910b3d441c5f508adb41efabd186e67a83f3b7665091c7a10c3a59ffca6ed  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/REVIEW_SEAL_TOOLS_R2_CX3V001.md
78be7394094ed2c4352fb3fb8fc3fdfc96f1630df79e25a0422d24fa1c7a7875  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/HASHES_SEAL_TOOLS_R2_CX3V001.json
3658d2cbada7049fc3a0503eb50579d62c0f42e32cbb0b7ff6b34dadebc60151  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/PARENT_R2_CUSTODY_CX3V001.json
fef10efd21343c44d16708446d3431e017ed047d12b4b20faa2dce1cd4118869  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/DECISION_R2_CX3V001.json
3b3e0d4a8be56e6a3a49d6aca3cb9e0c40f752481a96344e8ca7d0c7a3edb83b  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0633_2026-10-18_claude4_seal_tools_v003_D05.md
```
