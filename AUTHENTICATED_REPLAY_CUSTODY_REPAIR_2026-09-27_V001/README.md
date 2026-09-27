# Authenticated replay custody repair V001

Date: 2026-09-27. Status: `AURFT_ADDITIVE_REPLAY_REPAIRED__MISSING_PMICS_GL6BQ_CUSTODY_UNRESOLVED`.

The original AURFT verifier selects a repository-root file before a packet-local
file with the same manifest name. Thus the repository README shadows three
different authenticated packet READMEs. All three packet-local manifests match
their hashes, but the original replay reports 71/74 because A36/A40/A41 use the
wrong bytes. The original verifier and all historical seals remain unchanged.

`verify_axiomatic_urft_closure_v002.py` is an additive successor. It verifies the
original source SHA-256 before executing the original check payload. That
payload is byte-identical from its checks declaration onward except for the
manifest resolver. The successor delegates that function to
`manifest_resolution.py`, whose seven known manifests each have an explicit
local or repository-root base. There is no fallback or hash-based search. A
repository README is not a candidate for a manifest declared packet-local.
Unknown bases, mixed-base entries, duplicates, traversal, symlinks, missing
files, and hash disagreements are refused.

Run from the checkout root:

```sh
python3 -B AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001/verify_axiomatic_urft_closure_v002.py
python3 -B AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001/test_manifest_resolution.py
```

The successor passes **74/74 original checks** and all **15 regression/refusal
tests** pass. `ORIGINAL_REPLAY_2026-09-27.txt` and
`SUCCESSOR_REPLAY_2026-09-27.txt` preserve the actual original failure and
successor success. The regression suite also checks the original source hash
and unchanged scientific check payload. The original script is not silently
replaced in existing callers; historical executions must still name their
actual implementation.

This repairs execution reproducibility, not a scientific theorem. Natural
U-DCL validity remains a falsifiable adopted physical proposition; no alpha
selection, gravity emergence, or numerical constant follows from this repair.

## Exact source-recovery disposition

Only the nine explicit missing manifest-listed PMICS/GL6BQ paths were inspected
in the known original checkout
`/Users/bgm/PerInfo/where-atoms-come-from/audited-386ee2c`. All nine were absent
there too. **Zero files were recovered.** No broader search, generated
replacement, seal rewrite, or source modification occurred.

`REPAIR_RECEIPT.json` records every missing path, its expected SHA-256, its
authenticating manifest/hash, and its exact origin-path disposition. PMICS still
cannot complete its independent replay without two EV inputs. GL6BQ still has
only its theorem out of eight manifest-listed files and remains on custody and
publication hold. These gaps are not waived by AURFT's repaired replay.
