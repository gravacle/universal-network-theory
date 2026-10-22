# A102 README/source distinction

`date -u`: Sun Oct 18 21:33:56 UTC 2026

**NOTE; source-tested documentation discrepancy, 0 blocking findings.** README line26 describes both the driver check and cascade addendum JSON probes as parsing integers as strings. The driver check does so through `json_or_text(... parse_int=str)`. The cascade path at tool3 lines263–272 instead calls `strict_json_bytes`, whose integer parser is unchanged.

The cascade handler permits text fallback only for `json.JSONDecodeError`. A different `ValueError`, including the oversized-integer limit, records `CASCADE_MAP_R5_ADDENDUM_JSON` and prevents successful seal assembly. Thus the README overstates the uniformity of parsing; **no A-B1 admission bypass is implied**. Correct the wording or deliberately align that parser in a reviewed successor. No new runtime execution was needed or performed.

Byte SHA256 pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md` — `da29c008064ae51673dfe7106f72dfcb789f674b4c0a36e3a5daf017c7967af8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_slot_fill_c4v002.py` — `806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/seal_common_c4v002.py` — `f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10`
