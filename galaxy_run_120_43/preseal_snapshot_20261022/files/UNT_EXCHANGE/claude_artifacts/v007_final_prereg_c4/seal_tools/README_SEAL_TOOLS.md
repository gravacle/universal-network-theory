# seal_tools: root-side V007 seal checks (Claude4, dispatch 0584)

UTC 2026-10-18T18:10:19Z (`date -u`).

Four small scripts that root runs at seal assembly. **Each one only reads and checks.** None writes a file, starts a process or touches the network. The SEAL_RECORD builder prints bytes; root creates the file. Every JSON input is parsed strictly, and a duplicate key refuses (A71). The command line refuses abbreviations and repeated flags. Run them with the pinned isolated Python: `python3 -I -B <script> ...`. A verdict JSON goes to stdout (stderr for tool 4). Exit 0 means PASS; exit 2 means REFUSE.

## When root runs each tool (SEAL_CHECKLIST_R4 order)

| Step | Tool | What it refuses |
|---|---|---|
| after B1 (freeze) | `check_frozen_addendum_c4v001.py --prereg <sealed prereg> --frozen <..._V005_ADDENDUM_FROZEN.md> --covered-later A82[,...]` | a cited A-entry missing from the frozen bytes; a duplicate entry heading; a file that is not the separate FROZEN copy; a sha differing from the slot; the sealed prereg's own sha inside the frozen text (RI-27 / A82); an entry after the last cited one that the no-change list does not cover (A81 RI-26) |
| after B4 (sealed prereg) | `check_slot_fill_c4v001.py --slots <slots.json> --prereg <sealed prereg> --text-of-record r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json` | any PENDING or null value; pin bytes that differ; the sealed prereg differing from r4 outside `seal_slots.<k>.value`; slot values differing from the prereg's; bound plan or command not as the binder made them; launcher or guard not BUILD_V005's; identity records not on the driver slot; certificate M_s wrong; under r6, a missing or non-empty cache directory; under r5, a cache directory named |
| after B5 (sealed compare) | `check_sealed_compare_c4v001.py --reviewed <reviewed source> --sealed <sealed compare> --slots <slots.json> --prereg <sealed prereg>` | any differing line other than the five pin lines; a changed comment or line ending; a pin not equal to its slot; a pin assigned more than once anywhere; a reviewed source other than the slot; a cited addendum whose bytes do not hash to PIN_ADDENDUM_V005 |
| B7 (SEAL_RECORD) | `build_seal_record_c4v001.py` with all inputs (see `--help`) | everything above (it runs tools 1-3 first), plus E-SEAL1 outputs containing a decimal row-like value and missing seal-record inputs. On PASS it prints the exact record bytes; the sha256 goes to stderr. |

Root creates the record with exclusive create:

```sh
python3 -I -B build_seal_record_c4v001.py ... --covered-later A82 | python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" SEAL_RECORD.json
```

Compare the written file's sha256 with the one printed on stderr.

## Forms the tools expect

- **Sealed prereg:** `r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json` (e3b6b5b2) with each `seal_slots.<k>.value` replaced by the slot value. Nothing else may change.
- **Mapping from slot to prereg:** compare → `compare_reviewed_source`; every other slot keeps its own name. Under r5, `cache_directory_r6_only` is the string `NOT_APPLICABLE_R5`.
- **Sealed compare:** the reviewed source with exactly the five lines `V007_PREREG_SHA256`, `PIN_ADDENDUM_V005`, `PIN_DRIVER_BUILD_RECORD`, `PIN_V010_R5_CHECK` and `PIN_PRODUCER_REGISTRY` changed (A82), each on its own single line with its comment unchanged.
  - The two sha pins are 64-hex strings.
  - The three file pins are `(path, sha256)` tuples.
  - `V007_PREREG_SHA256` is the sealed prereg's sha.
- **Path strings:** the bound plan pins resolved absolute paths (the binder resolves them). Every slot must use the identical strings, because launcher v007 compares the plan's driver and frozen_addendum pins with the SEAL_RECORD's byte for byte (r4 N7).
- **Slot JSON** (schema `UNT_V007_SEAL_SLOTS_C4V001`), all keys required:

```json
{
 "schema": "UNT_V007_SEAL_SLOTS_C4V001",
 "driver_branch": "r5",
 "ngc_gas_M_s": 96,
 "frozen_addendum": {
  "path": "<abs path of ..._V005_ADDENDUM_FROZEN.md, exactly as the bound plan pins it>",
  "sha256": "<64 hex>"
 },
 "driver": {
  "path": "<the bound plan's driver path, exactly>",
  "sha256": "<64 hex>"
 },
 "driver_build_record": {
  "path": "<driver BUILD record (PIN_DRIVER_BUILD_RECORD)>",
  "sha256": "<64 hex>"
 },
 "driver_check_record": {
  "path": "<driver check record (PIN_V010_R5_CHECK or the r6 counterpart)>",
  "sha256": "<64 hex>"
 },
 "compare_reviewed_source": {
  "path": "<final round source, seal-time pins unset>",
  "sha256": "<64 hex>"
 },
 "identity_comparator": {
  "path": "...",
  "sha256": "..."
 },
 "identity_gate_records": {
  "Z2": {
   "path": "...",
   "sha256": "..."
  },
  "Z2_OFF_RO1": {
   "path": "...",
   "sha256": "..."
  },
  "B0prime_RERUN": {
   "path": "...",
   "sha256": "..."
  }
 },
 "launch_packet": {
  "build": {
   "path": ".../v007_launch_packet_cx1/BUILD_V005.md",
   "sha256": "46bc5b5d..."
  },
  "bound_plan": {
   "path": "...",
   "sha256": "..."
  },
  "bound_command": {
   "path": "...",
   "sha256": "..."
  }
 },
 "certificates": {
  "EPS": {
   "path": "...",
   "sha256": "..."
  },
  "LO": {
   "path": "...",
   "sha256": "..."
  },
  "GQ": {
   "path": "...",
   "sha256": "..."
  },
  "DOUBLING": {
   "path": "...",
   "sha256": "..."
  },
  "EPS_NGC": {
   "path": "...",
   "sha256": "..."
  },
  "LO_NGC": {
   "path": "...",
   "sha256": "..."
  },
  "I1T_NGC": {
   "path": "...",
   "sha256": "..."
  }
 },
 "producer_registry": {
  "path": "...",
  "sha256": "..."
 },
 "cache_directory_r6_only": "NOT_APPLICABLE_R5  (under r6: {\"path\": \"<fresh empty directory>\"})"
}
```

## Notes for root

- **The compare hashes the open addendum path.** Compare r10 sets `ADDENDUM_V005_CITED` to the open `..._V005_ADDENDUM.md` (r10 L149), not the frozen copy, and checks it against PIN_ADDENDUM_V005. The sealed compare is therefore valid only while the open file's bytes equal the frozen copy's. Any later write to the open V005 file makes the sealed compare refuse. That is fail-closed, but it would stall the verdicts. Either the final compare round cites the frozen copy, or root writes no further entry into the open V005 file after the freeze, putting new entries into a V006 addendum instead. Tool 2 reports this as `CITES_OPEN_ADDENDUM_PATH` and refuses if the bytes already differ.
- **Certificate M_s:** DDO values must be 128. Values inside a roster, name or geometry naming NGC, or under a key naming NGC, must equal the slot's `ngc_gas_M_s`: 96, or 128 under A81 RI-23. EPS records state no M_s (A68). LO, GQ and DOUBLING must state theirs.
- **Identity records:** the new side must name the driver slot's sha. `result_json_driver_sha256` values must equal it, and `NEW_DRIVER_PIN` must pass. The reference side may carry its own driver.

## Tests

`tests/test_seal_tools_c4v001.py` builds its fixtures under `tests/run_<UTC>/`:
- the real r4 text;
- a FROZEN copy of the current open addendum;
- the real compare r10 source as the reviewed source;
- the real BUILD_V005, template V010, r5 driver and certificates (read only);
- a plan bound by the real binder, with its HERE patched to the run folder.

A local audit hook refuses process starts, network, deletes and any write outside the run folder.

Latest run: `tests/run_20261018T180907Z`, **40/40**: genuine inputs pass, and every tamper refuses with its own code. The record is `TEST_RESULTS_C4V001.json` (`8e09138aabc75282c6ed74ad46f420c6a6a25b0a371c31e064e4f8151a39922c`).

The integration cases load the real guard v008 and launcher v007, with CONFIG and REGISTERED patched in-process:
- the guard admits the SEAL_RECORD that tool 4 built;
- `validate()` accepts the bound plan (nothing is started);
- a SEAL_RECORD naming another driver is refused (`PLAN_SEALED_DRIVER_MISMATCH`).

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `seal_common_c4v001.py` | `43d8f8eb610106c61be197defba59cff7f357bb31c70ca9c9136a44b5d267c25` |
| `check_frozen_addendum_c4v001.py` | `c4ebbb5bf69bb8b9c2ea82046c3553897a246cefc417f2d8bc556b10c62381e2` |
| `check_sealed_compare_c4v001.py` | `b339a8f6051ffe7a596179216ec3ba6e103a14356ed13befa51cf3529110b3ed` |
| `check_slot_fill_c4v001.py` | `7f3cf07da0d92fef0a1cc592cb644eafca2737e90b917e83ea9ffa5fc367187b` |
| `build_seal_record_c4v001.py` | `3091fc2afa2e16f74d8c634d8605205c792788924f078b5aae806351a1d18c70` |
| `tests/test_seal_tools_c4v001.py` | `9011e82532d9e5a2149a1125db527f16cae8568218e7a3a3f2be6ecaaacd9960` |
