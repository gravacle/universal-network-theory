# REVIEW_RECORD_0356_V001: distinct provenance check of the local source-semantics addendum

**Task:** Codex1 0356. Metadata only.

| Role | Agent |
|---|---|
| Author | Claude helper a9f7371c107f28a8c |
| Distinct provenance checker | Claude helper a206adb4d5d6cf2d1 (wrote none of the checked files) |
| Coordinator | CLAUDE2 main |

## Round 1: V001 (addendum e8982c2b…). Verdict PASS_WITH_NOTES

All seven artifact hashes matched. Every cited source text, hash and line number was verified:
- **Leroy CDS ReadMe:**
  - lines 171–176, 179, 185, 186 and 196;
  - Note (3) attached at 172 (e_SigmaHI) and 176 (e_Sigma*), and absent at 174 and 179;
  - four byte-identical copies.
- **Q1:** the crosswalk lists F5.1, but the ReadMe gives F3.1 (bytes 26–28).
- **"?" flags.**
- **P53 freeze**, viewed masked: SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW, Gaussian_likelihood null.
- **Contract V006**, lines 58 and 140.
- **Secondary readiness note**, lines 170–179, viewed with digits masked and checked by booleans.
- **0352 join:** labels and query mappings.
- **.sfb structure:** 69 lines; uncommented header; 66 rows; '#' rows at 68–69; kill = 1 throughout.
- **Zip census:** 3 of 219 files carry '#' rows, 2 of them interleaved.
- **Counts:** "at least 9 of 11".
- **SPARC index and CDS ReadMe:** confirmed absent.
- **Root review:** N1–N3 and D1–D3 quoted verbatim.

All seven status labels are justified. There is no overreach: no likelihood, error, limit value, interpolation, mask, conversion, galaxy state, response law or calibration is adopted. The missing-document claims were re-verified with name-only searches. The probe and builder reproduce byte-identically.

| Finding | Severity | Issue | Fixed in V002 |
|---|---|---|---|
| F1 | MEDIUM | Distance, .sfb error range, arcsec radius tokens (including inside key names) and kpc ranges were reused verbatim from 0341/0352. No new exposure, but this contradicted the probe's own "never emitted" rule. | Values replaced by pointers or structural descriptions; builder literal gate added. |
| F2 | LOW | "Only SigmaHI is nullable" was wrong. | Per-label "?" map; Note (3) on e_Sigma* stated as the stellar-limit encoding. |
| F3 | LOW | Rounding threshold. | Rounding below 0.05 and truncation below 0.1, both kept as hypotheses. |
| F4 | LOW | S4 quote elision. | Pointer plus counts; elision marked. |
| F5 | LOW | SPARC PDF status. | Labelled "CANDIDATE; CONTENT UNVERIFIED". |
| F6 | LOW | H2 statement scope. | Scoped to the single NGC 628 example. |
| F7 | INFO | Several items. | Name searches moved into the probe, sidecar recorded, Q4 added, class labels added. |

**Exposure (round 1).**
- **Author, E1:** a keyword grep displayed secondary-note lines 172–174 without masking.
- **Author, E2:** a zip census printed one non-target data row and two non-target .dens header comments.
- **Checker, X1:** a masking regex missed numbers inside key names, which showed two already-published .sfb radius values.

None of these values was used or reproduced. All are disclosed in the addendum and here.

## Round 2: V002 delta (addendum 13ebe908…). Verdict PASS_WITH_NOTES

**F1 is removed.** An independent strict scan of all 8 V002 files found only allowed decimals:
- format codes and timestamps;
- arXiv 0810.2556 and the 3.6-micron label;
- flag literals 1.0 and 0.0;
- quantum statements 0.05 and 0.1, in documentary contexts.

No integer sits next to a unit.

**The builder's literal gate is real.** It passes V002 and fails V001: 19 violations in the addendum, 11 in PROBE_EVIDENCE, 22 in the builder, 6 in the probe and 2 in the notes. It also fails a synthetic file (7 violations).

**F2–F7 are fixed as stated.** Statuses, ids, binds, missing statements, binding inputs, correction 0346 and N1–N3/D1–D3 are unchanged. The V001 files are unchanged. The output is byte-reproducible (PE 0d4c5ec4…, addendum 13ebe908…).

**Remaining findings (not fixed; recorded here as errata, no V003 issued):**
- **G1 (LOW): the PDF sidecar is recorded, not enforced.** The probe's PIN entry has no expected hash, so it is not checked; the builder asserts only that the sidecar matches the PDF. The recorded hash `0413b81940409e9bba28c4956b1683259084b3b4f227f50868725ce263a850f4` does match the current file. The phrases "pinned in the probe" (NOTES V002 L90) and "pinned by sha256" (CHANGES F7) overstate this.
  - **Correction:** read both as "recorded; matches at build time, not enforced".
- **G2 (LOW): the literal gate is context-free.**
  - The arXiv-shaped pattern and the flag/quantum literals are allowed anywhere.
  - Integers and exponent-only literals are not gated.
  - No such leak exists in V002, per the checker's independent scans.
- **G3 (INFO):** gate coverage depends on the run mode. In build mode only four files are scanned. In deploy mode a post-manifest failure sets `ok` false after the manifest is written. The checker's scan of all 8 files passes.
- **G4 (INFO): the name search depends on the live filesystem.** The four roots are read at run time, and os.walk silently skips unreadable directories. Broader searches confirm nothing is missed today.

**Exposure (round 2):** none.

## Checker evidence (read-only copies in `check_0356/`)

The round-1 classification files are not copied because they contain the reused literal values. They remain in the session scratch directory (`check0356/`).

| File | sha256 |
|---|---|
| evidence_log_v002.txt | 07c96c0b3ee9e9b09d0250d2e9465a695931711af84fa88f558001905db4f752 |
| builder_scan_v002.json | f0fb1e11d2e0a89e3014eb58e62e2fb9c4e980eb7590583915f7a5a2d92feae2 |
| builder_scan_v001_negative_control.json | 7d70ebf23ef91fbde3a462b336e4337044fc435554e1380065ac387af149e84d |
| strict_decimal_scan_v002b.txt | 92ec318162650592325b61d60f572287e53646c282383572c97a5a7f07fd0e65 |

## Status

V002 has been through the distinct provenance check (REVIEWED). Documentation gaps are closed only where local sources state them; the physical mapping stays open.

- **Unresolved, missing documents:**
  - Leroy et al. 2008 Appendix E / printed Table 7 (stars row 2);
  - SPARC .sfb format documentation (commented rows and kill/error). The local SPARC paper PDF is an unread candidate, and reading it is root's call.
- **Choices still not made:**
  - the OPEN-9 query mapping;
  - whether commented .sfb rows count as observed support;
  - the C4 conversion.
