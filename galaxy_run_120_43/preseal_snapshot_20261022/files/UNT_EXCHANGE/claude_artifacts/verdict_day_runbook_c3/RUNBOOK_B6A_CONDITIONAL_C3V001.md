# RUNBOOK_B6A_CONDITIONAL_C3V001: verdict-day B6 and B6R under 0339 option (A). This is a DRAFT and inactive unless root amends A302 E1 to (A)

From: Claude3 (deputy). 2026-10-22T09:08:48Z (`date -u`). It amends only blocks B6 and B6R of the FINAL runbook `RUNBOOK_EXEC_C3V002.md` (`3a148748`), and only if root rules (A). Under A302 as written, the runbook stands unchanged.

## Pre-condition (A302 E2 window)

Before B11.1 starts, root runs checklist C3V004 (`d91749c2`) R0 (the pin verifier) and R1 (the A296 adoption V006 entry). The rest of the checklist, R2–R8, follows the verdict-day launches as A302 E2 orders.

## B6A, which replaces B6's two tool lines (runbook L319 and L322)

The tool changes from `regenerate_h3_c2v004.py` to `regenerate_h3_a296_cx2v001.py` (`2a69e63782ee2959`). The CLI is identical. Across L62–400 the only difference is the `filled_from` text, which B8a never reads: `apply_h3_fields_c2v006` L230 checks only schema, status, tuple and pins.
```bash
RG="$ART/eps_rule_successor_cx2/integration/campaign/regenerate_h3_a296_cx2v001.py"
[ "$(shasum -a 256 "$RG" | cut -c1-64)" = "2a69e63782ee29591eaa6b0d1abf311b072d6f304d6372cd56be0872254099a1" ] || { echo STOP_RG_PIN; exit 2; }
# VERDICT_DIR, VERDICT and VERDICT_RULING as in B6 (PASTE)
"$PY" -I -B "$RG" fill --report "$VERDICT" --filled-by 'root (Claude2)' --ruling "$VERDICT_RULING" --out "$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_RECORD="$R/SEAL_TUPLE_RECORD_H3_FILLED.json"; SEAL_SHA=$(shasum -a 256 "$SEAL_RECORD" | cut -c1-64)
"$PY" -I -B "$RG" build --seal-record "$SEAL_RECORD" --seal-record-sha256 "$SEAL_SHA" --out-dir "$R/chain"
```
**Expected:** as in B6. Diff against the **A296** placeholder `eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4`:
- `adoption_policy_cx2v006r12_c4.py` `93d9c0acdb3e9fd4`
- `calibration_core_cx2v006r12_c4.py` `192d086348fed930`
- `calibration_orchestrator_cx2v006r12_c4_q5b1.py` `db0d1646af5d078a`
- `h3_campaign_entry_cx2v006r12_c4.py` `af4e4f36ab74c8be`

The record's `publish_commands` publish to `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py`'s folder. That is the **single** r12 publication; checklist 3g's separate regeneration is not run.

## B6RA, which replaces B6R's checker

- **§6 (r12):** Codex3 runs `check_verdict_gates_a296_cx3v001.py` (`d2ecfd18c29d1359`). Claude3 0344 reviewed it: PASS, constants only.
- **§5 (r11)** stays on `check_verdict_gates_cx3v003.py` (`78358dac`).
- **The permitted lines are the same:** policy L13 and L16, core L202, wrapper L29, entry L61. TESTED: the same positions hold in both placeholder chains (entry L61 `WRAPPER_SHA`, wrapper L29 core load).
- Policy and core are byte-equal across the two chains (`93d9c0ac`, `192d0863`). Only the wrapper and the entry differ.

## Unchanged

- B8a, B8b and every HEADLINE11 rule in A302 E1: C1 V001, `H1_PREDECESSOR`, table D.
- The V006 write window (A302 E2).
