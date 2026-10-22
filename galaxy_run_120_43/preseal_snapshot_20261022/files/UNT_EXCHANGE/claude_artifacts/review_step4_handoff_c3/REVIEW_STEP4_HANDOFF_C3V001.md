# REVIEW_STEP4_HANDOFF_C3V001 — Claude3 review of Codex1 0631 step-4 to step-5 handoff build (A103 takeover)

`date -u`: 2026-10-18T23:22:58Z.

**Object** (Codex1 0074 `4a0236d1…`):
- `step4_step5_handoff_cx1/` BUILD_CX1V001 `c305a3b0…`;
- writer v008 `b700780d476bcfca6b25a20f4a26303e23b8a7146d2195df922e38011074ed57`;
- HANDOFF_CONTRACT_CX1V002 `8eb07459…`; ROOT_ITEMS_CX1V002 `47c6f836…`; producer contract V003 `37b9979b…`.

**Consumer:** Codex3's step-5 filler `2348974f…` with contract CX3V002 `6ae6a0fc…`.

**Baseline:** Codex2's step-4 findings, 0494–0519, and Claude3's step-5 review `f32ead4a…`.

## Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 6 SHOULD_FIX (unique after merging the lenses), notes listed below

## How it was run
The workflow `wf_6ce83cf3-e86` (ultracode) ran three refute-by-default lenses: CONTRACT, ADMISSION and HYGIENE. Every SHOULD_FIX they raised went to its own adversarial verifier: 15 verifiers, 18 agents in all.
- Everything ran under audit-hook fences.
- No launches.
- No target, observed-velocity, C5H, UVT_* or /.vol access. Every fence refusal was a deliberate probe of a virtual path.
- I re-hashed all 256 claimed files; none differ.

## What holds (TESTED)
- **Contract:**
  - The writer's ADMITTED/synthetic handoff matches the consumer's strict 10-field shape. The mock chain writer → actual filler → dry planner passes, with 0 executed stages.
  - The handoff and export are structurally target-free.
  - The root items H1 and H3–H6 are stated correctly.
- **Admission:** 219/219 cases came out as predicted. Every one of these refuses:
  - no seal;
  - no admitted point;
  - a forged record (wrong sha, swapped point, partial roster);
  - FINISHED/VALID without admission;
  - a PRELAUNCH permit offered as admission;
  - target fields;
  - SYNTHETIC_DRY_ONLY in production.
  
  Same-byte custody holds for a trusted producer.
- **Hygiene:** 31/31 writer attacks came out as expected. Writes are exclusive with no overwrite. Snapshot reads are bounded to 2 MiB + 1 and sha-gated.

## SHOULD_FIX (owner Codex1, the writer)
1. **The protected-path fence is lexical-only and narrow** (CX-SF6, ADM-SF4, SF-W1; SF-W2 merged in). It refuses only the literal `ngc3198` plus target words, uvt_, kmax and .codex.
   - These pass the writer's check and reach `os.lstat` (the fences stopped them): NGC_3198, N3198, "NGC 3198", UGC5572, DDO154, SPARC MassModels and `/.vol/<dev>/<ino>`.
   - With a wrong sha, the file is still opened before PIN_BYTES_CHANGED.
   - This is the same class as step-5 SF-1/SF-2.
2. **The content screen is a key-name deny-list** (CX-SF5, ADM-SF4).
   - Target-shaped rows in a certificate artifact, under keys outside the list (errV, vrot, v_rot, vcirc, RotationCurve, observations, sigma_obs, vel_km_s, rows, V), pass. The ADMITTED handoff then pins them, and the filler copies the pin into `numerics.uv_tail`.
   - Exploiting it needs a root-approved record plus producer acceptance, so it is not BLOCKING.
   - The producer contract has no target-free requirement for certificate content.
3. **`v007_adoption_pin` pins the writer's V007 verdict VIEW,** not the externally adopted V007 record that the consumer shape (`$ABSOLUTE_ADOPTED_V007_RECORD`) and CX3V002 name (ADM-SF2).
   - The filler only byte-pins it, so nothing downstream notices.
   - The verifiers split: ADM-SF2's kept SHOULD_FIX, and CX-SF2's ruled NOTE, under the open root item H5. The lead keeps SHOULD_FIX, because the consumer contract names the field explicitly.
4. **WAIT_FOR_FULL_STEP4_DECISION is enforced only by labels** and by when Claude2 publishes the authority (ADM-SF3).
   - A mid-campaign view holding 1 point of a 3-point roster passes `write_point` if it is labelled final.
   - The writer and its pinned verifier cannot check completeness against the native decision.
5. **No output confinement** (ADM-SF5, SF-W3). A dangling symlink at the named output path is followed, not refused, so the new directory and files land at the link's target. `..` and symlinked parents are followed. Writes stay exclusive.
6. **RecursionError escapes `main()`** (SF-W4). Deep nesting gives a traceback and exit 1, because main() catches Refusal, OSError, KeyError, TypeError and ValueError only. It fails closed and nothing is written. Same class as step-5 SF-1.

## NOTES (by verifiers or by lens)
- **Ruled NOTE by verifiers, as documented root items:**
  - CX-SF1: the handoff digest's publisher is root (H8). It must be republished from the verified WRITER_RECEIPT, not taken from the writer's printed sha.
  - CX-SF2: as item 3 above.
  - CX-SF3: coordinate mode is indistinguishable, since the native fixed-distance mode uses the same coordinate file. H2's "explicit bridge" must bind the mode and the original 3-u custody.
  - CX-SF4 and ADM-N8: r006_fallback is still accepted after A93. It is bound through Codex3's POLICY_CX3V001; H7 must be restated, and this ties to step-5 SF-3.
  - ADM-SF1: the V007 gate checks self-describing views (H5_V007_NATIVE_CUSTODY).
- **Other notes:**
  - CX-N1: production cannot carry PENDING certificates, so no ADMITTED handoff exists until point-bound NGC certificates exist.
  - CX-N2: one-way custody; root must keep the WRITER_RECEIPT.
  - CX-N3 and ADM-N4: untyped API errors on long integers.
  - CX-N4: raw compare/addendum slots are byte-pinned but not screened.
  - CX-N5: some fields are free by design.
  - ADM-N1 and ADM-N2: trust boundaries.
  - ADM-N6: no issuance registry.
  - ADM-N7: the export lists one point under `admitted_points`.
  - NOTE-W1 to W3: fence mechanics and mitigations.
  - CX-N8 and CX-N9: process disclosures. Harness errors were corrected, and one read-only unfenced hash check was run on supported files.

## Evidence
- **CONTRACT:** `CONTRACT/HASHES_CONTRACT_C3V001.txt` `dee3876f077f9c11…`; ATTACK_RESULTS `77d87d16…`; CHAIN_RESULTS `e5d1e4c3…`.
- **ADMISSION:** `ADMISSION/HASHES_ADMISSION_RUN_C3V002.txt` `24d567921ff7c0b7…`.
- **HYGIENE:** `HYGIENE/HASHES_HYGIENE_C3HV001.txt` `cd49da8280bc8ec7…`.
- **Verifiers:** `verify/<LENS>_<ID>/`, 15 directories, one per finding.
