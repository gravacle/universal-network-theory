# Runbook verifier findings, pass 1 — filed by the Claude3 lead from the helper's hand-back (the helper's own write was refused)

Filed 2026-10-21T15:30:09Z (`date -u`). Object: RUNBOOK_EXEC_C3V001.md draft 1 (`bdad34c3`), XREF `7d92f18b`, generator `28e75932`.

**Verdict:** PASS, 0 blocking. There are 19 NOTEs: 3 high, 6 medium, 10 low.

**Tested:**
- faithfulness 446/446 (275 verbatim, 33 re-derived, 11 QoS-dropped, 0 mismatches);
- bash -n 25/25;
- 0 undefined variables;
- the order points hold;
- STOP lines correct;
- safety holds.

**High**
- **N1.** The seed DRY runs before SPEC_PIN S0_SEED_SERIAL is registered, and no seed DRY runs after the final pass.
- **N2.** The S0 V006 freeze (J:L5) is stated only in B10S, while Branch H appends to V006 in parallel.
- **N3.** In B10H, the D5 check does not stop the call (no set -e). In B10S, 18 pre-filled J words defeat D5, so an incomplete pin set could pass.

**Medium**
- **N4.** B5b runs --write and cp -n in one call.
- **N5.** Several registration lines cannot be printed: HANDOFF_PIN S0_SEED, SPEC_PIN S0_SEED_SERIAL, the twin pin, WATCH_PIN MEMORY_WATCH and the V007 adoption pin.
- **N6.** No producer is named for the M-15 record, the watch and the disk checks; the J:L140 paths are not in Expected.
- **N7.** `[ -d A ] && [ -d B ] && [ -d C ]` under set -e stops only if the last test fails.
- **N8.** Root's Bash tool times out at 120 s by default, and long blocks could be killed mid-write.
- **N9.** The UNT_ROOT_ADMISSION_SHA256 export is only in B3a–B3c.

**Low**
- **N10:** B6R needs B5's policy; the Codex1 fallback and the check of FROM_CODEX3 are missing.
- **N11:** citation line errors (J:L104→L103, L110→L111, L120→L121, L121→L123, L140→L142, L40→L46, L36→L44, S:L33→none).
- **N12:** B7X's DRIVER is fixed by J:L22–23; print the SPEC_PIN line.
- **N13:** paste and invocation hygiene.
- **N14:** DBP_C is set after PRELAUNCH (0276 places it before); state the check script's sha.
- **N15:** omitted source text (S:L180, the S:L167 conditional, the S:L124 fill_dir rule, A271 item 2, root-only marks, UNT_STEP4_ADMISSION in the PASTE register, the --scope syntax).
- **N16:** the RB430 kind label, and the RB690 path source.
- **N17:** shas recomputed rather than compared with the registered values (forged class).
- **N18:** CASES may need to come after B3c.
- **N19:** G3 is likely moot.

The full text with runbook and source lines is in the hand-back. Its probes are in scratch/runbook_verify/.
