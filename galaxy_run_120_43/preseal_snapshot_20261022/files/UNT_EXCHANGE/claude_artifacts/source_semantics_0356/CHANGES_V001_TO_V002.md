# 0356 changes, V001 to V002

All V001 files are retained unchanged. V002 is a fresh set of files in the same directory. The changes respond to the distinct provenance check of V001 (PASS_WITH_NOTES, F1–F7).

| Finding | Change in V002 |
|---|---|
| F1 (MEDIUM) literal values | The distance, the .sfb error-column range, the .sfb radius tokens (key names included) and the kpc radius ranges are removed from every V002 file. They are replaced by pointers into the 0341/0346/0352 products, or by structural descriptions such as "the last two lines of the file". The probe now compares radius tokens against texts it parses from crosswalk_0341 at run time and emits booleans only. Ledger items are carried as id, state and pointer. A literal scan in the builder fails the build, and the deploy, on any decimal outside the allowed classes: hashes, timestamps, format codes, arXiv ids, the band label 3.6-micron, the flag literals 1.0/0.0 and the F5.1 quantum statements 0.05/0.1. |
| F2 | Replaced "only SigmaHI is nullable". The "?" flag is carried by SigmaHI, SigmaH2, e_SigmaH2, FUV+24, FUV and 24. The narrower correct point: Sigma* and e_Sigma* carry no "?", and Note (3) on e_Sigma* is the stellar-limit encoding the ReadMe gives. The probe adds a per-label null-flag map. The ambiguous phrase is removed. |
| F3 | e = 0.0 now states both cases: rounding means values below 0.05; truncation means values below 0.1. Both are kept as hypotheses. |
| F4 | The S4 crosswalk quote is replaced by its pointer plus the stated row counts, with the elision marked ("quote replaced by pointer, radius values not reproduced"). |
| F5 | The SPARC paper PDF is labelled "CANDIDATE; CONTENT UNVERIFIED (hashed only, not opened)". |
| F6 | The H2 blank-encoding statement is scoped to the secondary note's single NGC 628 example. |
| F7 | The name-only searches are now part of the probe, with roots, patterns, matches and a count of forbidden-name matches (not listed). The PDF sidecar is pinned by sha256. Added Q4, which qualifies the crosswalk wording "not zero uncertainty" for e = 0.0. Class labels are added to the D1 entry (program product, root-retained) and to the contract line-140 entry (program adapter vocabulary). |

The statuses are unchanged: two RESOLVED_DOCUMENTARY, three PARTIAL, two UNRESOLVED_MISSING_DOCUMENT.
