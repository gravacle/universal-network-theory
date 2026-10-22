# RI45-24 (PAR8-SF1) and RI45-25 (ST8-N2): the V006 entry, draft for root (s0_launch_kit_c2 C2V003)

**Who and what.** A Claude2 root-workflow lane built this at Mon Oct 19 17:58:16 UTC 2026 for root. It says what RI45-24 requires root to state in V006 before T0, and what RI45-25 requires before the first step-5 result, and gives the recommended entry text. Nothing is adopted until root writes V006. Nothing was launched, and V006 was not written.

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. UNTESTED: not run; the deciding test is named. CHOICE: a decision this draft made, which root may overrule.

## Bottom line

- **Deadlines (FORMAL).** RI45-24 is root's V006 entry before T0, and RI45-25 comes before the first step-5 result (V006 `73663c84` L564, A135 item 8). T0 is the step-3 verdict, Mon 19 Oct 17:00 CDT = 22:00Z (A133 L295).
- **One heading carries both.** Each V006 heading written before the seal needs a row in r3a's V006 table and a re-render (RI45-27, ROOT_ITEMS L778), so fewer headings cost less. Append it at the end of V006.
- **The quoted lines are verbatim from bytes (TESTED).** The six source lines come from the r007 (`e4f5864a`) and r008 (`577f8c94`) drivers, L5145-5147. The caret lines were reproduced under Python 3.12.14 with a real EACCES on look-alike modules built from those driver bytes. They are byte-equal to Claude4's verify_parity_1/VERIFY.md L130-133 (`7b9818d9`).
- **The entry adds no pin line (TESTED).** On a scratch copy of V006, the kit's parser finds no pin under it.
- **Its section sha256 is stable (TESTED).** The command in section 3 gives the same value before and after a later entry is appended (6a67edc7 on the scratch copy; the real value depends on root's text). Root records it in the next entry; the pin entry draft has a line for it.

## 1. What RI45-24 and RI45-25 require root to state (ROOT_ITEMS_STEP45_V002.md `417de6fe`)

| # | Requirement | Source | Where in the text |
|---|---|---|---|
| 1 | Pin the class in a V006 entry: both source lines | RI45-24 (a), L496; recommendation L499 | "Source lines, verbatim" |
| 2 | The caret line, verbatim | L496, L499 | "Traceback frame text" |
| 3 | The scope (top-level dry-run diagnostics; exception class and text identical) | L496 | "Scope" |
| 4 | Cited by its own section sha256 (V006 is an open file) | L499 | section 3; the pin entry's RI45-24 line |
| 5 | Name the record a later parity check reads: disposition `a9ae801f` together with this entry | L499 | "Record of record" |
| 6 | Optional: the inside-NGC classes (a)-(e) follow from ST7-SF1/SF2 and lie outside PAR-TB scope | L499 | "Inside-NGC frame classes" |
| 7 | No waiver: option (c) is a blanket waiver, which A98.1 forbids | RI45-24 reasoning, L500 | "Not waived" |
| 8 | RI45-25: record ST8-N2 as intended, and state how a REFUSED step-5 run enters the freeze (a structured failure, 43 rows kept, never dropped; RI45-11) | RI45-25 (a), L511 | the RI45-25 paragraph |

## 2. Text for root to paste

````
## A<n>: RI45-24 (PAR8-SF1): the r008 frame class at cmd_dry_run L5147 is enumerated and pinned; RI45-25 (ST8-N2): r008's inside-NGC strictness is recorded as intended (<DATE_U_STAMP>)

**RI45-24, PAR8-SF1 (Claude4 0104; REVIEW_NGC_V011_CX3R008_C4V001.md `7ff20c1d`, SHOULD_FIX; both refuters reproduced it).** A98 says "Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver" (as quoted from V005 by Claude4 verify_parity_1 L51), and dispatch 0619 (`238858d1`) L15 says "Pin any r008-specific frame class before closure." The A98.1 disposition (`PAR_TB_A98_1_DISPOSITION_CX3V001.json` `a9ae801f`; mapping `ab5afb0e`) pins two r008-specific classes, the L5145 dispatch line and the guard move 9220 to 9329. This entry pins the third, with no code, driver-sha, registry or value change.

- **Class:** `cmd_dry_run` L5147 source line and its caret line.
- **Source lines, verbatim from the driver bytes** (r007 `e4f5864a`, r008 `577f8c94`; each line's bytes follow the colon, indentation included; L5145-5147 are the only lines of `cmd_dry_run` (L5144-5163) that differ):

```
r007 L5145:    code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir)
r007 L5146:    rp=Path(report_dir)/'DRYRUN_REPORT.json'
r007 L5147:    if code==0 and rp.is_file():
r008 L5145:    code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir,_ngc_post=_ngc_finalize_dry_cx3r008)
r008 L5146:    if isinstance(code,tuple):return code[0]
r008 L5147:    if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():
```

- **Traceback frame text of the class** (source line and caret line, exactly as Python 3.12.14 prints them when `is_file()` raises; Claude4 verify_parity_1 C4, reproduced from the driver bytes at this build):

```
r007:
    if code==0 and rp.is_file():
                   ^^^^^^^^^^^^
r008:
    if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

- **Scope:** top-level dry-run exception source/caret diagnostics only, the scope A98.1 gives its L5145 class; that text also lands in saved direct-call harness tracebacks and in hashes derived only from it (verify_parity_1 VP1-N3). It shows only when `Path.is_file()` raises an OSError that pathlib does not ignore (EACCES, EPERM, EIO, ENAMETOOLONG) after the planner has written the report, or when a `--report-dir` spelling makes the literal path longer than PATH_MAX (VP1-N1). Exception class and text, errno, exit code, stdout, frame count and every emitted file are identical in r007 and r008. `cmd_dry_run` is on no run-mode or stage stack (VP1 C8).
- **Asynchronous exceptions** (VP1-N2, TESTED by proxy, not a finding): an interrupt can also surface the r008 spellings of L5146 (`if isinstance(code,tuple):return code[0]` against r007's `rp=Path(report_dir)/'DRYRUN_REPORT.json'`) and of the dispatch def line L9194 (`def _ngc_v011_dispatch(fn, spec_path, *args, _ngc_post=None):` against r007's `def _ngc_v011_dispatch(fn, spec_path, *args):`). They are pinned here by line and source text, with the same scope.
- **Not waived:** everything A98.1 excludes (values, rows, validity, status, decision branches, exception class or message, refusal reasons, recursion-limit behaviour, new active NGC strict frames, future source changes).
- **Inside-NGC frame classes (a)-(e)** of the closure lens follow from ST7-SF1 and ST7-SF2 and lie outside PAR-TB scope (verify_closure_1/VERIFY.md `a5e8169d` section 4); no entry is needed for them.
- **Record of record for a later parity check:** the disposition `a9ae801f` together with this entry, cited by its section sha256 (the bytes from this heading line to the next line starting "## "), which root records in the next V006 entry. PAR-TB-1 is closed for r008.

**RI45-25, ST8-N2 (REVIEW `7ff20c1d` NOTES): r008's inside-NGC strictness changes are intended.** Inside NGC, r008 raises a typed `NGC_JSON_DEPTH_REFUSED` where r007 raised an untyped RecursionError, and a `final_rows_check` refusal in run mode reads REFUSED (exit 3) where r007 read COMPLETED_INVALID (exit 0). None of the 8 registered NGC specs reaches them; whether a filled step-5 spec can is UNTESTED (deciding test: that call's own dry plan under RI45-13 and its receipt). A REFUSED step-5 call follows A133 section 3 rule (c) (in force from A142): the identical spec is rerun with the RSS cap at RAM and the wall cap doubled, and it is marked invalid only after two identical deterministic failures that are not INFRA. It enters the freeze as a structured failure (RI45-14 list, first_pass.saves[1]): the member and all 43 query rows are kept, each row INVALID with the refusal code as its reason, never dropped (RI45-11 (a)); under A152 W-3 its rows and the member read invalid because its status is not COMPLETED.
````

## 3. After pasting: the section sha256

The section runs from the heading line to the next line that starts with `## ` (or the end of the file), with trailing whitespace stripped and one newline added, so a later entry does not change it. TESTED on the scratch copy: before 6a67edc7, after 6a67edc7, root command 6a67edc7.

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
V006='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
$PY -I -B -c 'import hashlib,re,sys; b=open(sys.argv[1],"rb").read(); m=re.search(rb"(?m)^## "+re.escape(sys.argv[2].encode())+rb"(?=[\s:.(])",b); n=re.search(rb"(?m)^## ",b[m.end():]); e=m.end()+n.start() if n else len(b); print(hashlib.sha256(b[m.start():e].rstrip()+b"\n").hexdigest())' "$V006" A<n>
```

## 4. CHOICES (root may overrule each)

- **R1. The entry also pins the L5145/L5146 lines and the L9194 def line.** VP1-N2 (verify_parity_1, TESTED by proxy, not a finding) shows that an asynchronous exception can surface r008's L5146 and L9194 spellings, and the verifier recommends pinning the whole block "at the same cost". RI45-24's minimum is the L5147 class; delete that bullet to keep only the minimum.
- **R2. The scope wording follows VP1-N3:** A98.1's own L5145 wording, plus the saved direct-call harness tracebacks. "Top-level dry-run stderr only" would be narrower than where the text lands.
- **R3. RI45-25's REFUSED handling** reads the rules already in force: A133 section 3 rule (c) for the rerun (A133 L218; in force from A142, V006 L738); RI45-11 (a) for keeping all 43 rows (ROOT_ITEMS L240); and A152 W-3 for validity (V006 L1065). It adds no new rule.
- **R4. RI45-24 and RI45-25 share one heading.** They can be split; each extra heading costs an r3a re-render.

## 5. What stays UNTESTED or unread

- Whether a filled step-5 spec can reach an r008 inside-NGC refusal. The deciding test is each call's own RI45-13 dry plan and its receipt.
- The caret text under an interpreter other than Python 3.12.14. The kit and the driver runs use that interpreter.
- **Not read: V005**, the closed decisions file that holds A98 and A98.1 (NGC3198-named; lane rule). The quoted sentence is attributed to A98 by Claude4's verify_parity_1 (L51, read from V005 bytes) and to A98.1 by ROOT_ITEMS RI45-24 (L494). The entry follows verify_parity_1. Root can check it against V005.

## 6. Sources (sha256 from bytes at this build)

| Source | File | sha256 |
|---|---|---|
| review | `REVIEW_NGC_V011_CX3R008_C4V001.md` | `7ff20c1d` |
| verify_parity_1 | `VERIFY.md` | `7b9818d9` |
| verify_closure_1 | `VERIFY.md` | `a5e8169d` |
| parity_review | `REVIEW.md` | `361040c8` |
| disposition | `PAR_TB_A98_1_DISPOSITION_CX3V001.json` | `a9ae801f` |
| disposition_md | `A98_1_DISPOSITION_ADDENDUM_CX3V001.md` | `f9632697` |
| dispatch_0619 | `0619_2026-10-18_claude4_codex3_A98.md` | `238858d1` |
| r007 | `galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py` | `e4f5864a` |
| r008 | `galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` | `577f8c94` |
| root_items | `ROOT_ITEMS_STEP45_V002.md` | `417de6fe` |
| a133 | `A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef91` |
| V006 at build | `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` | `73663c84` |
