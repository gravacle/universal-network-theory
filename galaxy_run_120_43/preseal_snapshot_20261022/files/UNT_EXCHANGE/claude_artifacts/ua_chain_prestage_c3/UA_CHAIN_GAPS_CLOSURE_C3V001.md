# UA_CHAIN_GAPS_CLOSURE_C3V001: four u_A command gaps closed from tool bytes (G-11, G-12, G-13, G-14)

From: Claude3 (lead). 2026-10-22T08:24:38Z (`date -u`). This adds to `UA_CHAIN_GAPS_C3V001.md` (`90fc5605`) and replaces nothing. Each form is copied from the adopted tool's own usage text or argparse.

**Labels:** FORMAL (from bytes). UNTESTED (not executed). Root executes, and values in `<…>` are root's pastes.

## G-11. The S1 `fill`

Source: `s1_fill_c2v002c.py` (`2b120b89`), usage L7. Pins are written `PATH@SHA256`.
```bash
"$PY" -I -B "$S/s1_fill_c2v002c.py" fill --u-a "<UA>@<UA_SHA>" --base-spec "<BASE_SPEC>@<SHA>" --campaign-config "<CAMPAIGN_CONFIG>@<SHA>" \
  --c3t-registry "<C3T_REGISTRY>@<SHA>" --out-dir "<NEW_FILL_DIR>"
```

## G-12. Child plans and binds

Plans: usage L9–10. `--params` takes DBP **C2V004D** (A291), and `--overlap` writes guard014's overlap admission fields (L14).
```bash
"$PY" -I -B "$S/s1_fill_c2v002c.py" plan --fill-record "<FILL_RECORD>@<SHA>" --case S1_UA_C3T --prelaunch "<PRELAUNCH>@<SHA>" \
  --params "<DBP_C2V004D>@<SHA>" --overlap --out "<NEW_PLAN_C3T>"   # add --dry first; exit 3 = refused
"$PY" -I -B "$S/s1_fill_c2v002c.py" plan --fill-record "<FILL_RECORD>@<SHA>" --case S1_UA_C4T --prelaunch "<PRELAUNCH>@<SHA>" \
  --params "<DBP_C2V004D>@<SHA>" --overlap --out "<NEW_PLAN_C4T>"   # add --dry first; exit 3 = refused
```
- **Binder011** (`step4_bind_c2v011.py` `d3d9702e`, L58). It has exactly five required flags, takes plain paths, and its outputs are exclusive.
```bash
"$PY" -I -B "$S/step4_bind_c2v011.py" --final-plan "<FINAL_PLAN>" --admission-candidate "<ADMISSION_CANDIDATE>" \
  --plan-out "<NEW_BOUND_PLAN>" --admission-out "<NEW_BOUND_ADMISSION>" --command-out "<NEW_COMMAND>"
```
- **Still root's:** the PRELAUNCH pin (G-08: whether PRELAUNCH005, which pins guard011, can serve the S1 children).

## G-13. The S1 launch config

Source: `s1_path_lib_c2v002c.py` (`99e2be17`), L1174–1182, L242 and L210. There is no exact-key-set check, so these are the keys it reads:
```json
{"schema": "UNT_S1_LAUNCH_CONFIG_C2V002", "campaign_state": "ACTIVE", "step2_route_a_state": "INACTIVE", "campaign_window": "<SINGLE_CALL_WAVE_START | NO_CAMPAIGN_HEAD_PENDING>"}
```
- **`campaign_window` is required only when `campaign_state` is `ACTIVE`,** and is refused otherwise. The value is root's window attestation (registration §11 rule 4).
- With W1 running at u_A, `ACTIVE` applies.

## G-14. Envelope START and END for the S1 pair

Source: the pinned envelope tool (`9d531381`; collect L1062–1077, snapshot L1078–1082, compare L1083–1088). The form copies the runbook's B10H (C3V002 L476).
```bash
T="$ART/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py"; E="<NEW S1 envelope folder>"; PHASE=S1_PAIR
"$PY" -I -B "$T" collect --phase "$PHASE" --max-depth 0 "${S1_SOURCE_ARGS[@]}" --v006 "$V006" --out "$E/PINSET.json"   # S1_SOURCE_ARGS: root's --doc-pin SHA PATH list for both children
PINSET_SHA=$(shasum -a 256 "$E/PINSET.json" | cut -c1-64)
"$PY" -I -B "$T" snapshot --pins "$E/PINSET.json" --pins-sha256 "$PINSET_SHA" --label start --out "$E/START.json"
# after both children finish:
"$PY" -I -B "$T" snapshot --pins "$E/PINSET.json" --pins-sha256 "$PINSET_SHA" --label end --out "$E/END.json"
"$PY" -I -B "$T" compare --start "$E/START.json" --start-sha256 <START_SHA> --end "$E/END.json" --end-sha256 <END_SHA> --out "$E/COMPARE.json"   # exit 3 INVALIDATE stops the phase
```
- **The pin list is root's** (A284 N10). It covers both children's specs, plans, admissions, DBP C2V004D, guard, launcher, binder and driver.
- **`--max-depth 0`** follows no nested pins, as in B10H. Whether nested pins should be followed is still the open N10 question.
- **The tool writes a `.sha256` sidecar next to each output** (see 0338).

## Still open (unchanged)

- **Root rulings:** G-01, G-02, G-04, G-08, G-18, G-22.
- **Unbuilt:** G-06, the S1 C1 freeze tool, on S8's critical path.
- **Not in any named source:** G-10 (row-32 middle steps), G-20, G-21, G-23 to G-26.
