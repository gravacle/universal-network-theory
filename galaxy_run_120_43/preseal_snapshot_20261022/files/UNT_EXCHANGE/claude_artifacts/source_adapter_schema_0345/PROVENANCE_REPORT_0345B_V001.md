# 0345-B provenance of SPARC_Lelli2016c.mrt (read-only report)

Author: CLAUDE2 helper 0345-B, a read-only Claude helper. Packaged unchanged in substance by the CLAUDE2 main lane. The machine-readable summary is SCHEMA_PROVENANCE_EVIDENCE_0345B_V001.json.

## Bottom line

The file's bytes trace to the SPARC distributor URL, pinned by the download sidecar's sha. That provenance does **not** justify the field boundaries.

- The in-file header describes a layout that is internally consistent, abutting, with no separators, and 113 bytes long. The data rows contradict it.
- The CDS ReadMe describes a different, blank-separated layout. The rows also contradict that for fields 5–7.
- No local document explains a "one leading blank per field" serialization.
- For both target rows, the seven-token structure in bytes 1–41 is **observed only**.

No geometry was adopted.

## Q1. Download/creation provenance

**Copy B (sidecar-backed):** `joint_parent_continuation/sparc_official_sample_2026-10-06_v001.mrt`
- Sidecar `…mrt.SOURCE.json` (sha bacfd875…2a88, lines 1–8) records:
  - url and final_url: `https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt`
  - retrieved_utc: 2026-10-06T17:22:50.189319+00:00
  - bytes: 28259
  - sha256: 5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243
  - content_type: null
- The observed file has the same sha and is 28259 bytes. Its local mtime is consistent with the retrieval time.

**Copy A (the target):** `external_ddo154_v001/SPARC_Lelli2016c.mrt`
- sha 5aa0501f…8243, 28259 bytes, mtime 2026-09-28. It is byte-identical to Copy B.
- It has no sidecar and no retrieval record in any allowed file in its directory:
  - SOURCE_HEADER_AND_RETRIEVAL.md covers THINGS/NRAO only.
  - README.md is generic.
  - SOURCE_FROZEN.json does not list SPARC.
  - nrao_hi_index_retrieval.txt is a 19-byte "404 page not found".
- Its hash, with no URL, is recorded in:
  - SCORING_FROZEN.json, key `files["SPARC_Lelli2016c.mrt"]`
  - SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json, `files`
- The URL is cited (as a citation, not a retrieval record) in:
  - NGC3198_OBSERVATION_INFERENCE_AUDIT_V001.md line 16 (2026-09-27)
  - FRONTIER_UPDATE_V254.md line 15
- Its own retrieval record is probably in ROTATION_* files, which the helper may not open (R4).

**Distributor page:** sparc_official_index_2026-10-06_v001.html
- sha ee7e3eab…, 7895 bytes. Its sidecar records `https://astroweb.case.edu/SPARC/`, retrieved 2026-10-06T17:22:50.492499Z, with a matching sha.
- It links the file as "Galaxy Sample: Table1.mrt" and says "Last update: 29 May 2020".
- It gives no format or byte-layout statement.

**CDS ReadMe:** external_ddo154_v001/SPARC_ReadMe.html
- sha 457f61cd…, 19951 bytes. No sidecar or URL is recorded; SCORING_FROZEN lists its hash.
- It is J/AJ/152/157, "Prepared by [AAS]; Sylvain Guehenneux [CDS] 13-Feb-2017", History: "From electronic version of the journal".

**MassModels (context only):**
- The external copy and sparc_official_massmodels_2026-10-06_v001.mrt are both 9108994b…, 269518 bytes.
- Sidecar: `https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt`, retrieved 2026-10-06T17:22:49.804161Z, with matching sha and bytes.

## Q2. Copies and counterparts

- **Working-tree copies with sha 5aa0501f:** exactly two, A and B. Both match the sample sidecar's sha and byte count.
- **By name:** a find under /Users/bgm/Research for `*Lelli2016c*`, `*sparc*sample*`, `*table1*.mrt`, `table1.dat(.gz)`, `*152_157*` and `*.mrt` found only four .mrt files: the two sample copies and the two MassModels copies.
- **By size:** there are 7 files of 28259 bytes. Besides A and B, the other five are unrelated program files with different hashes (CP_04400.json, STATE.npz, PATH.npz and two more STATE.npz checkpoints).
- **Git:**
  - The identical blob 8cdfb503c58b… exists in the UNT root .git, but only in two `refs/codex/turn-diffs/checkpoints/…` trees. It is not an independent copy.
  - It is absent from the program-worktree objects. program-worktree/research-checkpoints contains no .mrt file.
- **CDS table1.dat:** no local copy exists. Only the CDS ReadMe is present. The two other CDS ReadMe files under P53 RAW are Leroy 2008 (cbd9a431…).
- **Related, hashed only:** ngc3198_sparc_excerpt_v001.txt (58a303f7…, 2849 bytes), which matches the SCORING_FROZEN entry. It was not opened for display.

## Q3. Serialization/transformation evidence

**Header internal consistency** (header text only, lines 10–28):
- The 19 ranges tile bytes 1–113 contiguously, and every width equals its format width.
- So the implied record length is 113. No Lrecl is stated in the MRT. The header is self-consistent and describes an abutting layout with no separators.
- The file has 98 header lines (separator lines 5 "=", and 7, 9, 29, 98 "-") followed by 175 data rows (lines 99–273), the same as the CDS record count.

**CDS ReadMe layout:**
- table1.dat has blank separators: Name 1–11, Type 13–14, Dist 16–21, e_Dist 23–27, f_Dist 29 (I1, against the MRT's I2), i 31–34, e_i 36–39, L3.6 41–47 … Lrecl 130 (112 field bytes plus 18 separators).
- This documents that a blank-separated re-serialization exists. Its positions for fields 5–7 do not match the rows.

**No local document** (distributor page, MRT header, CDS ReadMe, sidecars, DDO154 docs) describes adding a one-byte leading blank to each MRT field. Call that layout H+1: T 13–14, D 16–21, e_D 23–27, f_D 29–30, Inc 32–35, e_Inc 37–40, separator 41, L 42–48, …, implied record 131. **H+1 is an inference with no documentation.**

**Program-side record (not provenance):** SPARC_EFFECTIVE_TRANSFER_V001_PREPARSE_FAILURE.json (0af04553…, 2026-10-04).
- It records "whitespace-expanded data rows that do not obey its displayed byte-column offsets", and that header-based fixed-width parsing found zero objects.
- Its repair was to use the 19 whitespace-delimited fields.
- This documents the mismatch as observed, without explaining where it came from.

**Other header defect:** CODEX3/READINESS_DDO154_FINITE_READ_BIBLIOGRAPHY_CORRECTION_V001.md line 5 records a defective CB89 locator in the same header. The header text has known errors, though this one is not about layout.

**Same-author cross-check (root manifest, allowed keys only):**
- `crosscheck_massmodels`: status MATCH; rows_found 43; text_equal and numeric_equal true; no mismatches; reference distance unique.
- This is about MassModels rows, not table1 byte layout. It does give one numerical anchor. The helper compared the withheld reference distance text (never displayed) against the NGC3198 prefix tokens:
  - Token 3 (span 17–21, mask 99.99) is float-equal to it.
  - Tokens 2 and 4–7 are not.
  - The header-as-written D slice (bytes 14–19, mask 9__99.) is not a valid F6.2.
- For NGC3198 this supports token 3 = D and contradicts the as-written D range. No equivalent check is available for DDO154.

## Q4. Prefix-only token contract (bytes 1–41 of the two target rows)

Rows were located by comparing bytes 1–11 only: DDO154 is line 104 (data row 6), NGC3198 is line 152 (data row 54). There is no CR or TAB in the prefix.

```
ruler    12345678901234567890123456789012345678901
DDO154   _____AAA999_99___9.99__9.99__9_99.9__9.9_
NGC3198  ____AAA9999__9__99.99__9.99__9_99.9__9.9_
```

| tok | DDO154 span / shape | NGC3198 span / shape | expected | conforms |
|---|---|---|---|---|
| 1 | 6–11 AAA999 | 5–11 AAA9999 | Galaxy | yes (right-justified) |
| 2 | 13–14 99 | 14 9 | I | yes |
| 3 | 18–21 9.99 | 17–21 99.99 | F.2 | yes |
| 4 | 24–27 9.99 | 24–27 9.99 | F.2 | yes |
| 5 | 30 9 | 30 9 | I | yes |
| 6 | 32–35 99.9 | 32–35 99.9 | F.1 | yes |
| 7 | 38–40 9.9 | 38–40 9.9 | F.1 | yes |

- **(a)** Masks are shown above.
- **(b)** Exactly 7 tokens in both rows. Byte 41 is blank and token 7 ends at 40, so it is complete.
- **(c)** All shapes conform.
- **(d)** Neither name has an internal blank.

**Layout tests:**
- Header as written: only Galaxy fits.
- CDS: Galaxy, T, D and e_D fit; it fails at f_D/i/e_i.
- H+1: all seven fit, and every H+1 separator byte (12, 15, 22, 28, 31, 36, 41) is blank in both rows.

**What a proof that the 1–41 whitespace contract isolates exactly the seven fields with a complete final token would need:**
1. **Field order:** PROVENANCE-BACKED by the header and corroborated by CDS.
2. **The 8th field starts after byte 41:** NOT provenance-backed. The header puts L at 35–41 and CDS at 41–47; only undocumented H+1 puts it at 42.
3. **At least one blank between fields, and no internal blanks in values:** NOT provenance-backed (the header says the fields abut). Observed for both targets.
4. **None of the seven fields is blank:** OBSERVED ONLY.
5. **Token 7 is complete:** OBSERVED.
6. **Shape conformance:** formats are provenance-backed; conformance is observed. D and e_D share a shape, so order relies on item 1.
7. **The bytes are the distributor's bytes:** PROVENANCE-BACKED by the sidecar sha.

No layout is declared authoritative.

## Q5. Remaining evidence requirements

- **R1.** AAS/IOP electronic Table 1 of AJ 152, 157. It must show its byte-by-byte header and the data positions of fields 1–7, or byte identity with the SPARC-site file. It is not local; obtaining it needs the network.
- **R2.** CDS J/AJ/152/157 table1.dat, for a boolean token-to-field equality test of the two rows against CDS positions 1–39. Only the ReadMe is local.
- **R3.** A distributor or author statement that the file is blank-delimited, or that its header ranges are nominal or wrong. The saved index page has none.
- **R4.** The 2026-09-28 retrieval record of Copy A. It is likely in ROTATION_* files, which may not be opened by name. This affects only that copy's URL and time, not its bytes.
- **R5.** An observational census by a permitted lane: separator bytes blank and 7 conforming tokens in all 175 rows, plus a row-length census (H+1 implies 131, the header 113, CDS 130). This is generalization, still not provenance.
- **R6.** The MassModels MRT header compared with its own data offsets. Not done, because it would touch MassModels data-row bytes.

## Paths read (sha256; scope)

JPC = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`; EXT = JPC/external_ddo154_v001.

**SOURCE.json sidecars:**
- sample bacfd875aa818b3e74712009da6e18b36e4941bebe4e2c576358aa5620512a88 (1–8)
- massmodels 2c9b80c5bd6afefab410ce860853811785e4cb3fe24dd54ed0cb71ba5c2a1e20 (1–8)
- index 031e7e7a9d0ec0ce6c4b8b4a1a922c0be25fc4122af5bf974d0dc20ac2c60efd (1–8)
- pdf 0413b81940409e9bba28c4956b1683259084b3b4f227f50868725ce263a850f4 (1–10)
- BulgeDiskDec e097262eb3693a83376d8ae48b88fa197efd05fa81cfed0228727f5a5c074cec (1–8)
- sfb 274993d0ab0cd1805ba6fea2d7327bd7ba9a8aab9849116e6ac6bc396b6e440c (1–8)
- Rotmod zip sidecar d15290003f4bfc6687ebd871bc8b42a3b60563c3177a1071a4a50d3e31497075 (1–8; incidental by name, metadata only)

**Documentation pages:**
- JPC/sparc_official_index_2026-10-06_v001.html ee7e3eab…: whole, tag-stripped
- EXT/SPARC_ReadMe.html 457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666: whole, tag-stripped (1–287)

**The target:** EXT/SPARC_Lelli2016c.mrt 5aa0501f…
- header lines 1–98
- bytes 1–11 of every line, compared only
- bytes 1–41 of lines 104 and 152

**Root manifest:** NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494
- top-level key names, `crosscheck_massmodels`, `checks`
- `reference_distance_texts` was used for a boolean comparison only and never displayed

**EXT docs (matching lines only):**
- README.md b72d1778… (1–7)
- nrao_hi_index_retrieval.txt b16e1576… (1)
- SOURCE_FROZEN.json a7102b85… (1–52)
- SOURCE_HEADER_AND_RETRIEVAL.md 6a511b74… (13–15, 19–20, 23–24, 30, 35, 39, 42–44, 48, 53, 85, 95, 105)
- SOURCE_EXTRACTION_PROTOCOL.md 5eff00e2… (9, 36)
- INDEPENDENT_HEADER_REVIEW.md 8154127f… (6, 11, 45, 50–52, 61)
- SOURCE_EXTRACTION_RESULT.md 78f72b5e… (4)
- SCIENTIFIC_RESULT.md 8e33860b… (19, 69, 77)
- SCORING_FROZEN.json a4ec7082… (5, 75–77 plus top keys)
- SUBBIN_SENSITIVITY_V001_RESULT.json c02d045a… (3617 plus top keys)
- subbin_sensitivity_v001.py 5f7ea65b… (50, 83)
- SOURCE_RESULTS.json 32921f5e… and extract_source.py 934f25d9… (regex scan, nothing displayed)
- SOURCE_FACTORY_AND_FIELD_PREFLIGHT_REVIEW.md e9362eba… (10, 58, 71, 93; incidental by name)

**Program docs:**
- JPC/SPARC_EFFECTIVE_TRANSFER_V001_PREPARSE_FAILURE.json 0af04553… (string fields)
- JPC/SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json a3cf6c73… (files SPARC entries plus top keys)
- JPC/SPARC_EFFECTIVE_TRANSFER_V001.md 9fd0c1a0… (40)
- JPC/GALAXY_INPUT_READINESS.md 6e23d981… (38, 39, 58 partial)
- NGC3198_OBSERVATION_INFERENCE_AUDIT_V001.md 7c0ee068… (10, 16)
- FRONTIER_UPDATE_V254.md 612713b2… (15, partial)
- JPC/HALO_COMPARATOR_PROPOSAL_V001.md 0a4df12f… (33, partial)
- JPC/CROSS_U_NGC3198_SPARC_JOINT_EPS_V001_MANIFEST.json 7d9db107… (input_sha256 sample entries)
- CODEX3/READINESS_DDO154_LOCAL_SOURCE_PRODUCT_INVENTORY_AND_MINIMAL_REUSE_MANIFEST_V001.md da73994a… (22, 27 partial)
- CODEX3/READINESS_DDO154_FINITE_READ_BIBLIOGRAPHY_CORRECTION_V001.md 5fa10b41… (5 partial)
- P53 RAW Leroy ReadMe.html cbd9a431… (54–63)
- claude_artifacts/galaxy_source_metadata_0336/INVENTORY_V001.json 182ac029… (one entry plus top keys)
- lanes/P46_CODEX2/INPUT_PINS_V001.json d05b584b… (sample pins)

**Git (read-only):** cat-file -e, log, for-each-ref, ls-tree -r filtered, count-objects. No blob content was read.

## Files hashed (whole file)

- Copies A and B: 5aa0501f…
- Both MassModels copies: 9108994b…
- SPARC_ReadMe.html
- The index page
- The five other 28259-byte files
- ngc3198_sparc_excerpt_v001.txt
- Every file in the read list

## Reads NOT performed

- Every file named ROTATION, FIELD_, Newton, FIT, TRIAL, RESPONSE, rotmod or MOM1, except the two incidental cases below.
- Rotmod, sfb and BulgeDiskDec zip members.
- .dens and .sfb files.
- The SPARC PDF.
- Leroy table4.
- MassModels header and rows.
- Any data row other than the two targets, and any byte beyond 41 of the targets.
- Row lengths.
- The quarantined V001 geometry output and the 0344 diagnosis.
- Other manifest keys.
- The excerpt file contents.
- The network.

## Incidental exposure (honest record)

1. **An initial grep over EXT was not filtered by file name**, so it ran over forbidden-name files.
   - Its 34 KB result file was not opened.
   - The 2 KB preview showed prose lines from FIELD_V002_RESULTS_REVIEW.md:97 and ROTATION_COMPARISON_PREFLIGHT_REVIEW.md:11 (no numbers), and INDEPENDENT_HEADER_REVIEW.md:45, which carries a THINGS DDO154 centre and distance.
2. **SOURCE_FROZEN.json** (allowed) shows DDO154 distance, inclination, PA and centre. Seen; not reproduced or adopted.
3. **PREPARSE_FAILURE.json** quotes two short slices of the non-target CamB row. Seen; not reproduced.
4. **A Rotmod-named SOURCE.json sidecar** (metadata) and **4 prose lines of a FIELD_-named review** were read.
5. **Regex count scans** read many manifest, result and code files in-program under a name guard. Only counts were displayed.
6. **The CDS ReadMe** shows column min/max annotations (documentation).

No velocity values and no validation outcomes were inspected.

## Constraint confirmation

- **Read-only:** yes. Scratch went only to scratchpad/helperB/. Git ran with GIT_OPTIONAL_LOCKS=0.
- **No network:** yes.
- **No project scripts run:** yes.
- **Prefix bytes only:** yes. Bytes 1–11 were used for row location, and bytes 1–41 of the two targets only.
- **Forbidden files:** two incidental breaches by name, plus the unfiltered grep whose output was not opened beyond its preview.
- **Masks, not values:** yes.
- **Hashing and headers:** yes.
- **When unsure, skip:** yes (R4–R6).
