# CP-1 list rho registration and slot staging — cx1v004

Candidate for Codex3 review and root verification under dispatch0819. No launch authority. Selected helper: `cp1_list_rho_slot_cx1v004.py`; v001–v003 are retained development versions, not selected.

The helper reads pinned source bytes for the existing registration checks and CP1 list loader; it reuses their table-agnostic rho validation, canonical anchor comparison, identity calculation and list validation. A memoized snapshot opens each input once and validates every repeated expected hash against that buffer. Strict JSON rejects duplicate keys and nonfinite constants. Only named RHO_NUMERIC, EPS_NUMERIC, EPS_PROOF and GQ_PROOF records are read in selected point folders. It never imports a producer, computes physics, invokes slot proofs, assembles bundles or launches a process. The canonical three producer pins and root ruling pins remain required. An inert-fixture out-root under this package is also allowed for tests; no production claim follows from synthetic records.

`register` validates all selected points and the pinned original anchor registration, then writes a new registration candidate. Root reviews and pins those bytes. `stage` independently rebuilds the expected registration and requires equality with the supplied root-pinned record before writing FILLED specs, SLOT_ARGS and commands. Stage changes exactly the two certificate slots. Existing outputs are refused; failed validation creates no output directory. A write error can leave a prefix; preserve it and choose a new directory.

All eleven tests passed, including CLI register/stage, wrong selected key, wrong identity key, table key, table alias, missing anchor pair, list SHA mismatch, unregistered rho, mismatched filled slot and OS audit-event single-read verification. Production record handling and the generated downstream proof/bundle commands remain UNTESTED. Tests used invented records, real source pins, root rulings and the published anchor spec template only.

## Root W3 commands

Wait for all selected points' attempt-a rho, EPS numeric and EPS/GQ proof records to finish. Only folder names P300–P302 were listed during this build; no live CP1 record content was opened. Existing registration/approved metadata files were read for their hashes. These commands have not been run.

```sh
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/cp1_list_rho_slot_cx1v004.py register --points-list /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/future_wave_points_cx1/NOMINAL_W3_MINUS_DRAFT/POINTS_LIST.json --points-list-sha256 9cfa8787934f2748482e30bbc15f57dcabfbf80b77d27c115cdc9478b54074d1 --out-root /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b --anchor-registration /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/rho_registration_c2v001/RHO_REGISTRATION_CP1_C2V001.json --anchor-registration-sha256 be6dcb35d6f28c3d23e77550b9bb6fd16ebb1e687336f6efad9ce2901e05f2d6 --approved-producers /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/rho_registration_c2v001/APPROVED_PRODUCERS_CP1_REGISTRY_C2V001.json --approved-producers-sha256 10867036b8f11b85c8a45e7510de862d4b291597cf620418f567c776d682ab8a --key 06c3e863688de6359029405bf1bed5ded75edd8d3aee1e169843b5afbce27d15 --key 95540f067efd4a1439a1073977b09eeb4d03d1362413b02ca3da26328a1345db --key 6f4604efe6d7fe348d9ca4986d9042234ed54d5df63b254b4e8c3b6c43861ee1 --output-dir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/W3_REGISTRATION_V001
```

Review `W3_REGISTRATION_V001/RHO_REGISTRATION.json` and obtain its SHA from the returned output pin, independently verifying it. Substitute that exact SHA for `ROOT_REVIEWED_REGISTRATION_SHA256` below; the placeholder is intentionally non-executable as a valid pin.

```sh
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/cp1_list_rho_slot_cx1v004.py stage --points-list /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/future_wave_points_cx1/NOMINAL_W3_MINUS_DRAFT/POINTS_LIST.json --points-list-sha256 9cfa8787934f2748482e30bbc15f57dcabfbf80b77d27c115cdc9478b54074d1 --out-root /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b --anchor-registration /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/rho_registration_c2v001/RHO_REGISTRATION_CP1_C2V001.json --anchor-registration-sha256 be6dcb35d6f28c3d23e77550b9bb6fd16ebb1e687336f6efad9ce2901e05f2d6 --approved-producers /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/rho_registration_c2v001/APPROVED_PRODUCERS_CP1_REGISTRY_C2V001.json --approved-producers-sha256 10867036b8f11b85c8a45e7510de862d4b291597cf620418f567c776d682ab8a --key 06c3e863688de6359029405bf1bed5ded75edd8d3aee1e169843b5afbce27d15 --key 95540f067efd4a1439a1073977b09eeb4d03d1362413b02ca3da26328a1345db --key 6f4604efe6d7fe348d9ca4986d9042234ed54d5df63b254b4e8c3b6c43861ee1 --output-dir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/W3_STAGING_V001 --registration /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/W3_REGISTRATION_V001/RHO_REGISTRATION.json --registration-sha256 ROOT_REVIEWED_REGISTRATION_SHA256 --slot-out-root /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/lo_slot_W3_cx1v001 --bundle-out-root /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_W3_cx1v001
```

After reviewing staging outputs, create these two fresh directories (no overwrite):

```sh
mkdir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/lo_slot_W3_cx1v001 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_W3_cx1v001
```

`W3_STAGING_V001/COMMANDS.txt` contains the exact per-key slot-proof command (including SLOT_ARGS SHA) followed by its list-mode bundle command. Root executes one at a time after pin review. Leave at least one second between slot-proof calls because the downstream result filename uses UTC seconds. The helper does not create these downstream directories or execute the commands. A refusal stops the sequence; do not infer a proof from staged slots.

## Production W3 rebind (A257)

At natural W3, run entry004 `points-manifest --config PRODUCTION_CONFIG --out-dir NEW_MANIFEST_DIR`. Use that newly returned POINTS_LIST pin, not the earlier draft wave or pending SHA. Retain the existing exact-identity bundles; if identities differ, stop and recertify rather than relabel them.

Using `cp1_points_assembler_c2v001.py`, run:

```text
records --points-list PRODUCTION_LIST --points-list-sha256 LIST_SHA --out-root NEW_REGISTRY_ROOT --bundle BUNDLE_P300 --bundle BUNDLE_P301 --bundle BUNDLE_P302 --approved-producers APPROVED_FILE --genesis-registry GENESIS --genesis-registry-sha256 GENESIS_SHA
verify --points-list PRODUCTION_LIST --points-list-sha256 LIST_SHA --records RECORDS --records-sha256 RECORDS_SHA --c1 C1 --c1-sha256 C1_SHA --genesis-registry GENESIS --genesis-registry-sha256 GENESIS_SHA
```

Run `verify` under `taskpolicy -b` with the isolated Python. Only after a successful verification, run entry004 `ledger-append --config PRODUCTION_CONFIG --records RECORDS --records-sha256 RECORDS_SHA`. This rebinds production theta/pending-spec SHA/wave and checks the production mapper/prelaunch chain. Actual production config, genesis and C1 pins must come from root; they were not opened here. These are command templates for future outputs, not fabricated current pins.

No code in existing tools was edited. Root remains the sole launch owner.
