# DESIGN_C3V001: relocation with custody, a successor of `storage_check move` (root 0866, V006 A306)

From: Claude3 (design only, no build). 2026-10-22T11:36:19Z (`date -u`). Principle (A306): bookkeeping yields to wall-clock time, and physics and evidence integrity are preserved. **Nothing here changes a byte of evidence.** Only *where* verified bytes are read from changes.

**Labels:**
- FORMAL comes from source. Line numbers marked ✓ were re-checked by Claude3 from bytes.
- Claims marked "map" come from the helper's reader map `relocation_custody_c3/READER_MAP_HELPER.md` (`08e35a54`; 10 named files, read-only). The builder re-verifies them.
- Estimates are UNTESTED.

## 0. Recommendation

**R1 (recommended): in-campaign relocation through a supplemental relocation-aware layer, installed the same way as the L2 importer.**
- It keeps **cache_id and the ledger genesis unchanged**: no wrapper, core or entry byte changes, which is the A265 item-3 precedent.
- It moves only finished, accepted (VALID) call dirs of completed waves.
- Each move has a root relocation record and a chained index.
- Every post-acceptance reader re-verifies bytes at the new location against the record.

**R2 (fallback): a phase-boundary successor.** If R1's open items (§7) prove invasive, freeze the campaign at a wave boundary and start a new work dir, with a new cache identity and ledger genesis. Its importer admits prior accepted results by reference from their relocated location, verified by the same records.

## 1. Facts the design rests on

- **Only the work dir is identity-checked** (path, symlinks, mount, VolumeUUID, inode): ORCH (`c75a889f`) L631–718 and L3022–3061. No call dir's volume, UUID or inode is checked (map).
- **Call dirs** are `<WD>/waves/wave_%04d/campaign/call_%04d` (map: ORCH L3008, L3508). Absolute call-dir paths are written into sha-pinned bytes, and cache entries are self-hashed and never rewritten (map). They appear in:
  - receipts, `finish.json`, `request.json` and result manifests;
  - the spec's certificate-slot pins, so spec shas depend on slot paths (map: CORE L256–259);
  - cache entries, F6 entries, acceptance records and ACCEPT step records.
- **Every command's cache open re-verifies every cached entry** (ORCH L2319–2322 ✓). One moved dir therefore stops the campaign, exit 3.
- **Every cache hit re-checks the certificate:** `forward` calls `check_cached_certificate` (WRAP `db0d1646` L539–545 ✓).
- **cache_id has no call-dir path:**
  - the parent cache_id covers template, base spec, driver, taxonomy, rows, engines and coordinates (ORCH L1774–1779 ✓);
  - the wrapper adds `tail_readiness`, including the ledger path under WD, plus the adapter and guard shas (WRAP L136–139 ✓);
  - **so a change to the wrapper's bytes changes cache_id.**
- **The ledger genesis** = digest(registry pin + ledger {schema, path}). Lines are chained by `prev_sha256`, and no ledger field holds a call-dir path (map: WRAP L372–375, L422–433).
- **Resume hazard:** an interrupted wave relaunches any **absent** call dir (CAMP `d35d5d4a` L175–185 ✓).
- **`storage_check move` refuses every call dir by construction:** the WD contains the candidate (`e0b3a89a` L136 ✓).
- **The roster builder and G26 read the NGC and S0 step-5 runs,** never the DDO154 `call_%04d` dirs (map). They are therefore unaffected by this design. Their G16 custody model (copies under a custody root, byte-equal, a different (st_dev, st_ino), restore rather than reinterpret) is the template followed here.

## 2. Eligibility: which call dirs may move

A call dir is relocatable only when all of these hold:
1. its cache entry is **VALID and accepted**: not F6, invalid, INCOMPLETE, HALT or unverified;
2. its wave has a WAVE_RESULT, so it is complete (the resume hazard);
3. no gate re-reads it by pin (deciding, A32 capability, adoption) and the ledger names no file inside it;
4. the L2_DIRECT phase has ENDed. The relocation layer joins the installed process only after the envelope END (D002), so the importer's phase pin set never changes mid-phase. L2 ends early (W2/W3), and the overflow risk is late (waves 15–16).

Everything else stays on UNT_CAMPAIGN.

## 3. The relocation record (root writes it; exclusive create)

`WD/RELOCATIONS/<entry_key>.json`, schema `RELOCATION_CUSTODY_V001`, on UNT_CAMPAIGN (small):
- **The entry:** `entry_key`, and `entry_self_sha256` (the cache entry's own self-hash).
- **Old and new dirs:** `old_call_dir` (the absolute string as recorded); `new_call_dir` (absolute, on External1, under a declared custody root such as `/Volumes/External1/DDO154_RELOCATED_V001/`).
- **Volumes:** `old_volume` and `new_volume`, with mount points and VolumeUUIDs read by ORCH's own `volume_uuid()` (L672).
- **Files:** `files`, the exact sorted list of `{rel, size, mode, sha256}` taken from the old dir before the copy. `new_files` is the same list taken from the new dir after the copy, and it must be equal.
- **Provenance:** `tool` (the relocation tool's pin), `utc`, and `root_ruling` (the V006 or dispatch pin authorizing the batch).
- **Chaining:** `prev_index_sha256`, chained into `WD/RELOCATIONS/INDEX.jsonl` the same way as the certificate ledger, so a removed or rolled-back record is detectable.

**The root tool `relocate_with_custody`:**
1. Refuse while the work-dir lock is held, so the campaign must be stopped.
2. Check eligibility (§2).
3. Copy (`ditto`), fsync, and verify the full file set and every sha.
4. Write the record and append the index.
5. Only then remove the old dir.
6. Report the bytes freed. There is no partial-success state.

## 4. Readers: who must accept relocated dirs, and how each verifies

| Reader | When | R1 behaviour |
|---|---|---|
| Cache open `_verify` (ORCH L2319–2322 ✓, impl L2361–2399 map) | every command | **In scope.** Old path absent, no symlink, valid record in the index: re-hash every file at `new_call_dir` against the record and the entry. Otherwise refuse, as today. |
| Cache hit `forward` → `check_cached_certificate` (WRAP L539–545 ✓) and what it opens (handoff pin WRAP L214/L567; guard `verify_bundle`; custody deriver; map) | every probe and replay hit | **In scope.** Same mapping; every opened byte verified against the record. |
| F6 checks (WRAP L470–488 map) | every open, put, reuse | **Excluded:** F6 entries are not eligible (§2.1). |
| Latest-pass rule and ENTRY reingest guards (WRAP L108–117, ENTRY L119–134 map) | reingest | **Excluded:** only non-accepted entries are reingested. |
| ACCEPT second pass (L228–232 map) | INCOMPLETE only | **Excluded.** |
| Interrupted-wave resume (CAMP L175–185 ✓) | resume | **Excluded:** only completed waves are eligible (§2.2). |
| Roster builder, G26 | NGC and S0 runs | **Not a reader** of DDO154 call dirs (map). |
| storage_check `move` | root | Replaced, for eligible dirs, by `relocate_with_custody` (§3). `move` itself is unchanged. |

**Path strings stay the OLD absolute paths** in every pinned record. The layer remaps reads only and never rewrites an entry, receipt, spec or record. That is why spec shas, cache entries and cache_id are untouched.

## 5. Cache identity and the ledger genesis

**Both are unchanged under R1:**
- the layer is a separately pinned supplemental installer, so the wrapper, core and entry bytes are byte-identical (WRAP L136–139 includes the wrapper's own sha, so the layer must not live in the wrapper);
- no ledger line names a call dir;
- the records live under WD/RELOCATIONS, outside the ledger.

**Under R2:** a new cache_id and a new ledger genesis are created at the phase boundary, and prior results come in by reference (the L2 importer pattern).

## 6. Tests and MUST_FAILs

**MUST_FAIL:**
1. a **tampered copy** (one byte changed in one file): sha mismatch, refuse;
2. a **partial copy** (a missing file, or an extra file): file-set mismatch, refuse;
3. **moved but unrecorded** (old path absent, no record): refuse, as today;
4. a **symlink at the old path**, even to a byte-equal copy: refuse with `RELOCATION_SYMLINK`, before any realpath logic, because today's generic checks would pass a link (map);
5. **both old and new present:** ambiguous, refuse;
6. a **record for an ineligible entry** (F6, INCOMPLETE, HALT, an incomplete wave, or before the L2 END);
7. a **record whose new volume** is undeclared, has a UUID mismatch, or is UNT_CAMPAIGN or the internal disk;
8. an **index-chain tamper** (a record removed or reordered);
9. a **record replayed** for another entry (the self-sha binds it);
10. the **new volume unmounted:** refuse. The campaign stops until External1 is remounted, which is the A305 standing rule.

**Positive:**
- a relocated VALID entry passes cache open and cache hit;
- **whole-engine equivalence:** a full inert campaign replay with K relocated entries gives byte-identical results and request sequences, the same test shape as Codex1's importer v023/v025;
- mutants removing each guard are killed.

## 7. Open items for the builder

1. **Readers outside the map** (monitor `verify_receipt`, state enumerator, guard `verify_bundle`, custody deriver, replay-input writer, LO/SRB adapters, evidence and row producers): confirm that they touch a VALID entry's call dir after acceptance only through `check_cached_certificate`. Any other path joins §4's in-scope set.
2. **One installer:** compose with the L2 importer's `importer_installation` (`75977551`), which already subclasses Cache `_verify_impl` and `forward`, in one installed class, so there is a single InstalledCache. Install it only after the L2_DIRECT END (§2.4).
3. **Path authority:** the custody root and the declared volume set are root's, in the config or the invocation, never read from a candidate record.

## 8. Build size, builder and reviewer

- **Size (UNTESTED estimate):**
  - layer, about 250–350 lines (hooks and the record and index verifier);
  - root tool, about 200 lines;
  - tests, about 400 lines (MUST_FAILs, the engine-equivalence replay, mutants).
  - Roughly 1–1.5 builder-days, plus about 0.5 day of review.
- **Builder:** Codex1, after its Oct 27 01:00 CDT reset. It built the importer's installer, which is the same installation family (backlog #1).
- **Reviewer:** Claude4 (cross-family) or Claude3, with Codex3 for a narrow pass.
- **Adoption:** root's, at a wave boundary after the L2 END. Use it only when the 85 % rule fires (0352).
