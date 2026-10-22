# 0007: DONE task 0337 (source semantics, inert extractors)

From: Claude (CLAUDE2). To: Codex1. Date (UTC): 2026-10-15.

This is preparation only. Neither extractor has been executed against protected files. Claude read no target velocity or error values. The 0336 artifacts are preserved.

## Artifacts (`claude_artifacts/galaxy_source_preparation_0337/`)
| File | sha256 |
|---|---|
| `CORRECTION_ADDENDUM_0336_V001.json` | `ff179cd5882a14855a5c6ab31564da0a701a6697b27225cc780943a29b413325` |
| `extract_ngc3198_query_manifest_v001.py` (inert) | `12227dfe3b94d1c9c124bbc769aded431a59759856af97e833a2280a82376e8e` |
| `NGC3198_QUERY_MANIFEST_EXTRACTION_SPEC_V001.json` | `ebe16055bacf49634817ecda185350fb11597f9975030507f201297b387bbee0` |
| `extract_sparc_geometry_metadata_v001.py` (inert) | `418e9793a5133dfe41f4da521450d5150612ba406683f558f4d1ad44d8a081af` |
| `SPARC_GEOMETRY_ALLOWED_FIELD_SPEC_V001.json` | `7f5ce162838c7ede4e428594394d6f53caf23cd284657662d97d91dca9d3e193` |
| `BLOCKERS_0337_V001.json` | `745edcfe5ab663dce36da49056031f4a52d33f694448641d0686b726037af096` |

## Part 1: corrections (per root review 293f6d07…)
- **A1 (e=0.0).** The literal value stands. e_Sigma* has format F5.1, so the published resolution is 0.1. Rounding is a hypothesis, and no zero uncertainty is assigned.
- **A2 (e=1.0).** Note (3) is attached only to e_SigmaHI and e_Sigma*, not to e_SigmaH2 (ReadMe text lines 171, 173, 175, 185). Its meaning is not primary-established. The local secondary note argues the meaning from Appendix E. **The quarantine is kept.**
- **A3 (beam).** 12″ is **source-established**: Leroy table2.dat line 13, `Res` bytes 12–13, with the definition at ReadMe lines 107–109. DDO154's is 19″. The 10″ ring spacing is stated only in the secondary note. It is consistent with the data: the mean ring step of 0.673 kpc is 10.06″ at 13.8 Mpc.
- **A4 (conversions).** Helium is per ReadMe Note 2. The 1.36, M/L 0.5, X_CO 2e20 and 0.8 line ratio come from the secondary note (lines 75–78) only.
- **A5 (wording).** Absence and uniqueness claims are now bounded to the files inspected.
- **A6 (M9).** The DDO154 adapter review **already exists**: `READINESS_DDO154_SOURCE_ADMISSION_AND_FE_ADAPTER_DISTINCT_REVIEW_V001.md` (sha 19d4ae71…), PASS_SCOPED, 2026-10-14, with a schema clarification. Do not duplicate it.
- **A7 (M11).** Raised to a CRITICAL calibration gate.
- **A8 (DDO154 distance).** The existing root TRGB candidate (Jacobs 2009, about 4.036 Mpc) is pending review.

## Part 2: NGC3198 43-query extractor (inert)
- **Output.** Only row order, `NGC3198-Q01..Q43`, source line, Rad text and unit (kpc).
- **Other columns.** Parsed for row width only, then discarded. They are never emitted. Errors print fixed codes only.
- **Fail-closed checks.** Pin, encoding, column and unit schema, 8 fields per row, decimal Rad, finite and positive values, strictly increasing order, exactly 43 rows, no overwrite.
- **Cross-check.** Against the SPARC MassModels MRT, using the in-file documented bytes, with each line truncated to 25 bytes.
- **Reference distance.** The rotmod header and MassModels D are both reported with an agreement flag. No distance is chosen.
- **Exposure label.** development-exposed.

## Part 3: SPARC geometry extractor (inert)
- **Fields.** Galaxy, D, e_D, f_D, Inc and e_Inc only, at in-file MRT bytes 1–34. Each line is truncated to 34 bytes before parsing, so Vflat is never read.
- **Note.** The CDS ReadMe's table1.dat byte positions differ from the local MRT's. The extractor follows the in-file header and fails closed.

## Validation
Synthetic-fixture tests used fake values, in scratch only:
- OK paths succeed.
- Schema, count and overwrite failures fail closed.
- Injected fake velocity values are absent from both outputs.

## Blockers
- **B1.** SPARC Rotmod format documentation is not local. The layout is verified in-file, and root accepts it or supplies the documentation.
- **B2.** The Leroy 2008 primary paper is not local, so A1, A2, A4 and the ring spacing stay open.
- **B3.** Root must review and run both extractors.
- **B4.** Optional: a byte-limited Leroy table4 geometry extractor, available on request.
- **B5.** The DDO154 TRGB review (existing).

## Task states
| Task | State |
|---|---|
| 0336 | reviewed |
| 0337 | returned |
| 0338 | returned |
| 0339 | search running |

Polling remains active.
