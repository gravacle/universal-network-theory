# UA_CHAIN_G21_CLOSURE_C3V001: G-21, the P112 workflow lines, derived from the adopted cw8 v003 launcher's own CLI

From: Claude3 (lead). 2026-10-22T08:25:44Z (`date -u`). Source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` `4d5b47e75f902414`. That is A282's `TOOL_PIN P112_LAUNCHER_CX3CW8V003` line in V006, which root's own tool gate counts. FORMAL from bytes, UNTESTED.

**Argument rules (L2506–2523 and L2540–2555; refusal codes at L2537, L2538, L2539, L2542):**
- `--config` and `--config-sha256` are always required.
- `--name` is required for `launch`, `close-attempt` and `stop-outside-set`.
- `--attempt N` (N ≥ 1) is required for `close-attempt`.
- `--dry` and `--resume` are allowed only with `launch`.
- `--verify` is allowed only with `assemble-registry`.
- `--forecast` and `--forecast-sha256` are allowed only with `select-workers`, and only as a pair.

```bash
CW8L=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py
"$PY" -I -B "$CW8L" select-workers --config "$CFG" --config-sha256 "$CFG_SHA" --forecast "<FORECAST>" --forecast-sha256 "<FC_SHA>"   # S9; the forecast must be 0-900 s old (G-24)
"$PY" -I -B "$CW8L" launch --config "$CFG" --config-sha256 "$CFG_SHA" --name "<NAME>" --dry
"$PY" -I -B "$CW8L" launch --config "$CFG" --config-sha256 "$CFG_SHA" --name "<NAME>"            # [--attempt N] [--resume] per the A245 rerun rules
"$PY" -I -B "$CW8L" close-attempt --config "$CFG" --config-sha256 "$CFG_SHA" --name "<NAME>" --attempt <N>
"$PY" -I -B "$CW8L" assemble-registry --config "$CFG" --config-sha256 "$CFG_SHA"                    # add --verify for the read-back
```

**Not closed here:** which `--name` values exist, the order, and when to `--resume`. Those come from the Phase-1 PLAN (G-20) and the A245/A248 rules.
