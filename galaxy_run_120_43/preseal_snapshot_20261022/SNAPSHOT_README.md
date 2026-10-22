# UNT program — public snapshot, 2026-10-22 (pre-NGC3198)

Curated by Claude3 for root (Claude2), under dispatches 0872 and 0873 (V006 A311, A313), at 2026-10-22T15:32:59Z. Every file is a **copy**; nothing in the program was moved or changed. **Root pushes this folder only with the principal's explicit OK.** No git command was run here.

## Blinding state at this snapshot
- **No NGC3198 observational value has been read** by any lane: no rotation-curve, target, sigma or slot file. **None is included.** Their paths only, to be added after the seal (A313), are in `NGC3198_INPUTS_POST_SEAL.md`.
- **The S4T R3 run finished** at 2026-10-22T15:07Z (root 0874). **The verdict comparison (S4T) and the NGC seal steps are pending.** This snapshot contains no verdict.
- **Registered NGC3198 geometry** (distance and inclination as preregistered) and NGC3198 query identifiers appear in the preregistration texts, specs and decision records as registered design, not as observations. Every included file that mentions NGC3198 together with numbers is listed in `SCAN_REPORT.json` → `ngc3198.kept_list`, so root can withhold any of them.
- **DDO154** is the calibration galaxy and is not blinded. Its pinned inputs are included (0873 item 1).

## What is here (`files/` mirrors the original absolute paths)
| Category | Files | MB |
|---|---|---|
| Top-level files of every `claude_artifacts/` folder (tools, READMEs, reviews, records) | 4,121 | 105.1 |
| Exchange: dispatches `FROM_CODEX`, lane outboxes `FROM_*`, `PLAN.md`, `README.md`, `STATUS.md`, `KNOWLEDGE/` (without the execution block), `plan/`, `bin/` | 3,685 | 14.1 |
| Deeper files cited by absolute path in those texts (adopted tools, certification records, runbooks, sheets, DBP params) | 8,114 | 182.7 |
| CP-1 ρ certification records (`LO_RHO_SLOT_PROOF_*`) | 31 | 0.1 |
| READMEs beside cited code | 15 | 0.2 |
| DDO154 inputs pinned by the run config and specs | 36 | 1.2 |
| Decision registers V005, V005 (frozen) and V006 | 3 | 0.8 |
| Preregistration texts: the r3a family and siblings, kmax prereg v002–v005, v007 final | 2,409 | 44.9 |
| **Total** | **18,414** | **349.2** |

## Left out (by rule, before any file was read)
- Run trees and outputs: UNT_INTERNAL_RUNS, External1 paths, any `out/` or `stages/` folder, and run payload names such as `result.json` and `finish.json`.
- Step-2 outputs, `~/.codex`, caches, inert fixture runs, mutation and test scratch, and files over 20 MB.
- NGC3198-data-like files, the multi-galaxy source tables that include NGC 3198 rows (SPARC Lelli 2016, Leroy 2008), and local machine-state dumps (`ps`, `lsof`).
- `lanes/` (earlier computational outputs) and binary files other than the DDO154 inputs.

## Scan results (`SCAN_REPORT.json`)
- **Credentials, tokens and keys:** 0.
- **Emails:** 0 personal. All 20 pattern matches are code expressions such as `a.t@u-np.eye`. Nothing was redacted, so every file is byte-identical to its source.
- **Absolute home paths:** they appear in 10,751 files. Prefixes and counts are listed; they are allowed per 0872.

## Integrity
- `MANIFEST.tsv` gives every file's path, size and sha256. `MANIFEST_SHA256.txt` gives the sha256 of `MANIFEST.tsv`'s bytes.
- Pins in the records name the original absolute paths; each file sits at that path under `files/`.
- See `REPRODUCE.md` for the regeneration path and hash checks, and `ENVIRONMENT_MANIFEST.json` for the interpreter and package identities.
