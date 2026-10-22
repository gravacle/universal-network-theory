# INDEX: c3v009 pre-stage (Claude3); nothing here is published

Written 2026-10-19T02:41:56Z (`date -u`).
- **Nothing here is published.** SELECTED c3v008 (`f30fd48c…`) and every file it pins are untouched.
- **v004 status at 02:41Z:** `seal_tools_v004/` has no SELECTED file yet.

## (a) One MUST_FAIL test per && site, on a COPY of the production script
Harness: `tools/e1_sites_mustfail_c3v002.py` (`7f09a07e…`). **The one variable is TARGET** (argv 2).

**Locating sites.** The harness locates each site by its statement text, not by line number. It reads TARGET's own pins and picks the matching dry-run generator:
- c3v009 for c3v019;
- c3v010 for a wired c3v020;
- c3v008 for the c3v016 contrast.

**What each copy changes.** Each copy is the production script plus four changes:
- the published dry-run scratch substitutions;
- exactly ONE fixture edit, so that only the first operand is wrong;
- one marker line after the site, which prints only if the script got past the check;
- the step calls cut after the NEXT step: step 1 for step-0 sites, step 3a for step-3 sites. Step 9 can never run.

**Results.** Run `e1_sites_20261019T022505Z/` (results `0e3c3b6a…`): target c3v019 12/12 refuse; the c3v016 contrast reproduces the defect at 9/9 sites.

| site | c3v016 line (0109 / 0118) | c3v019 line | first operand made wrong | c3v019 | c3v016 | covered before by |
|---|---|---|---|---|---|---|
| S01 | L298 | L331 | HELPER bytes (a byte-modified copy; HELPER_SHA unchanged) | REFUSE "the helper or runner bytes differ", exit 1, stopped at step 0, step 1 never reached | went past, ran step 1 | E1-1 |
| S02 | L325 | L359 | the case_block path in a synthetic r6 + SELECTED | REFUSE "the text of record does not bind the case block" | **REFUSES too: never defective (CONTROL)** | (none) |
| S03 | L355 | L396 | draft driver.path | REFUSE "the slot draft's driver is not DRIVER" | went past, ran step 1 | E1-2 |
| S04 | L356 | L398 | draft producer_registry.path | REFUSE "…producer_registry is not REGISTRY" | went past, ran step 1 | (none) |
| S05 | L357 | L400 | draft launch_packet.build.path | REFUSE "…launch_packet.build is not BUILD" | went past, ran step 1 | (none) |
| S06 | L358–359 | L402 | draft admission_entry.launcher.path | REFUSE "…admission_entry is not LAUNCHER and GUARD" | went past, ran step 1 | E1-3 |
| S07 | L360–361 | L405 | draft identity_gate_records.Z2.sha256 | REFUSE "…identity_gate_records are not…" | went past, ran step 1 | E1-4 |
| S08 | L363–364 | L415 | draft frozen_addendum.path (DRAFT_PATHS_MUST_MATCH=1, as in production) | REFUSE "…documented output paths are not this script's" | went past, ran step 1 | (none) |
| S09 | L454 | L507 | binder plan.path (fixture binder: the real one plus a wrapper changing only that path) | REFUSE "the binder's plan or command path…", stopped at step 3, 3a never reached | went past, ran step 3a to the end | (none) |
| S10 | L455 | L509 | binder driver.path (fixture binder; the real binder refuses any other driver) | REFUSE "the binder's driver or frozen addendum path…" | went past, ran step 3a to the end | (none) |
| S11 | not in c3v016 | L410 | draft driver_check_record.path (A111; had its fallback from the start) | REFUSE | n/a | disclosures suite S-8 |
| S12 | not in c3v016 | L413 | draft EPS_NGC path (A111 loop) | REFUSE | n/a | disclosures suite S-9 |

**Correction to the 0109 site list.**
- **L325 was never defective.** It has had its `|| REFUSE` fallback (L326) since c3v016, and the S02 run proves it on the c3v016 copy.
- **The ninth real site is L363–364,** the DRAFT_PATHS chain, which 0109 left out.
- The nine defect sites are therefore L298, L355, L356, L357, L358, L360, L363, L454 and L455.

**Re-pointing check.** The same harness, pointed by TARGET alone at a smoke c3v020, again gives 12/12 and 9/9: `smoke_c3v020_20261019T023613Z/e1_sites_on_smoke_c3v020_20261019T023742Z/` (`735545d7…`).

## (b) The three v004 checks, parameterized on the v004 SELECTED file
1. **Imports.** `tools/check_tool4_imports_c3v003.py` (`272d9cf5…`) checks four things:
   - tool 4's non-stdlib imports, closed transitively over the runner modules, EQUAL the T4_RUN `--module` set;
   - each module name is its file's basename;
   - each module pin is the file a SELECTED role stores (v004 first, then v003 as fallback);
   - every flag the script passes is a tool-4 flag, and both A110 flags are defined.
   Smoke on synthetic look-alikes: 11/11 (`smoke_imports_20261019T022907Z/`, `d27b7bd6…`).
2. **Dry run with BOTH flags.** Three pieces:
   - generator `tools/make_dry_run_c3sa_c3v010.py` (`ab01df67…`): no S24/S25, and it refuses a target that is still PENDING or lacks the flags;
   - successor generator `tools/make_root_script_c3v020.py` (`62318ef6…`): wires P13 from the SELECTED file (`--tools-from auto|v003|v004`), uses helper c3v018 and adds the step-11 check;
   - setup `tools/setup_dry_run_c3sa_c3v012.sh` (`50107743…`): gated on check 1, it shows both flags on step 10 in every pass, plus the step-11 verdict.
3. **Verbatim in the SEAL_RECORD.** Helper `tools/seal_steps_c3sa_c3v018.py` (`a28327ec…`) is c3v017 plus `check-seal-record-disclosures`.
   - Forms: object, text, base64, pin_content_raw_text and locate.
   - The script pins `DISCLOSURES_RECORD_KEY`, `_FORM` and `SEAL_RECORD_SCHEMA`, all defaulting to the explicit placeholder `PENDING_V004_RECORD_FORMAT`. Step 0 and the check both refuse while any of them is PENDING.
   - Smoke: 18/18 (`smoke_record_20261019T023217Z/`, `4fc33e20…`). It confirms the c3v008 dry-run record carries no disclosures.

**End-to-end MUST_FAIL smoke.** I used a synthetic look-alike: v003 tool 4 plus the two A110 flags, which embeds nothing.
- Run: `smoke_c3v020_20261019T023613Z/dry_run_20261019T023625Z`.
- The gate passes. Both passes run steps 0–11 with both flags on tool 4's step-10 call.
- Step 11 refuses `SEAL_RECORD_DISCLOSURES_KEY_PATH_MISSING` in both passes.

**One-command landing driver:** `tools/run_on_v004_landing_c3v002.sh` (`3a3d6d88…`).
- Run order: check 1 against c3v019, then generate c3v020 into a new `v004_landing_<UTC>/`, then dry runs A and B with step 11, then the per-site harness.
- `discover` mode makes a labelled DIAGNOSTIC script, with step 11 in locate form. `pinned` mode takes KEY, FORM and RECORD_SCHEMA as read from the SELECTED bytes.
- Its smoke run is `v004_landing_20261019T023932Z/` (labelled SMOKE inside), done on the look-alike.

## Observed in the UNSELECTED v004 bytes (read only; nothing is pinned from them)
- `seal_tools_v004/build_seal_record_c4v004.py` `9787cf58…` takes `--manual-disclosures` and `--manual-disclosures-sha256`.
- It writes a top-level `manual_disclosures` = {pin {path, sha256}, content, raw_text}, with record schema `UNT_V007_SEAL_RECORD_C4V004`.
- It imports the c4v003 modules unchanged; tools 1, 2, 3, 5 and seal_common are byte-identical to v003 (DELTA `6e52ebd5…`).
- If the SELECTED bytes say the same, `pinned manual_disclosures pin_content_raw_text UNT_V007_SEAL_RECORD_C4V004` is the expected wiring.

## Kept, never used or superseded (nothing deleted)
- **Superseded tool versions:**
  - e1 harness c3v001 `3c56a87f`: never run;
  - import check c3v001 `aedbf340` and c3v002 `4aac9cea`: PINS-line parse and looped add_argument;
  - smoke c3v001 versions `b95318ce` and `2c550625`;
  - landing driver c3v001 `a6abe49a`: never run; a stray one-argument pin call.
- **Failed smoke folders:** `smoke_imports_20261019T022753Z`, `smoke_imports_20261019T022810Z` and `smoke_record_20261019T023205Z`.
