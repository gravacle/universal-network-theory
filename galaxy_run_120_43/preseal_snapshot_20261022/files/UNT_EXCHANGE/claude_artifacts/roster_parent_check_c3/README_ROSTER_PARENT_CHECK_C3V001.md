# Backlog #7: roster-builder `--out-dir` checks before the step-7 ledger commit. README C3V001 (A272 hardening; D038)

**Author:** Claude3. **Reviewer:** Codex1 (narrow, as offered in 0288/0293), else Claude4. Not adopted until root rules.

- `roster_builder_parent_check_c3v001.py` — `27b55142649d9e9d87b5fe1ea02acaca0b3ca5efc2ebb627c87f66acff57e2f7`
- `test_roster_parent_check_c3v003.py` — `0ea8ebafac3699685e641f8ba62984d292a6a69748e6e597f630bc6dab1ee599` (the selected suite)
- `TEST_RECORD_ROSTER_PARENT_CHECK_C3V001.json` — `42e3938e4445a6046a4beb418ccb42f70cf7763c03aec4ced254dc2fcb2af37d` (36/36; 5 of 5 mutants killed; `$PY` 3.12.14)
- Preserved drafts, not for use: test v001 `8980e647` (aborted on the uncaught custody exception) and test v002 `e3919a6a` (its no-read window included the test's own read).
- Base, unchanged: `cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` `f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11`.

## The hazard (shown on the unchanged base with real commits; tests H1–H3)

`step7` and `custody` write the ledger entry `STEP7_<seq>.json` (base L2039 "the commit point", L3466) **before** `main` creates `--out-dir` (L2347, L4506). So a bad `--out-dir` fails **after** the commit: the ledger has advanced, and `STEP7_RESULT.json` / `CUSTODY_RESULT.json` / `REPLAY_PLAN.json` are missing.

| Command | `--out-dir` exists | parent missing | parent is a file | parent read-only |
|---|---|---|---|---|
| step7 (base) | commit, then refused `OUT_DIR_EXISTS` (rc 2) | commit, then `internal_error FileNotFoundError` (rc 1) | commit, then `NotADirectoryError` (rc 1) | commit, then `PermissionError` (rc 1) |
| custody (base) | refused before the commit (the base already checks this) | commit, then the exception **escapes `main`** (the custody main catches only Stop/Refused: a traceback) | the same, `NotADirectoryError` | the same, `PermissionError` |

## The fix: a thin pre-commit wrapper

The wrapper loads the base from its pinned bytes (O_NOFOLLOW, regular file, full sha) with the base's own `__file__`. For a well-formed `step7` or `custody` call (exactly `--input`, `--input-sha256`, `--out-dir`), it refuses first, printing the base's own refusal form `{"refused": CODE, "detail": OUT_DIR}` to stderr with rc 2:
- `OUT_DIR_EXISTS` when `--out-dir` exists (lexists, so a dangling symlink too);
- `OUT_DIR_PARENT_MISSING` when the parent of `abspath(--out-dir)` is missing or is not a directory;
- `OUT_DIR_PARENT_NOT_WRITABLE` when the parent is not writable and searchable.

Otherwise it runs the **unchanged base `main`** with the same argv. Every other command, and any malformed call, goes straight to the base.

**Why a wrapper and not an edited copy:** the base bytes and sha stay `f710334b`, so `own_pin()`, every record the base writes, and every consumer that pins the base (for example the schedule-ceiling writer and root's TOOL_PIN) are unchanged. An edited copy would change the sha that those consumers check.

**No new honest-path refusal.** Each check is a condition under which the base's post-commit `os.mkdir` must fail (rows above). Valid absolute, relative and symlinked-parent `--out-dir` values pass (W2, W4, W5).

## Root command form (step7 and custody only; other commands may stay on the base)

```bash
R=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3/roster_builder_parent_check_c3v001.py
"$PY" -I -B "$R" step7   --input <STEP7_INPUT.json>   --input-sha256 <H> --out-dir <NEW_DIR>
"$PY" -I -B "$R" custody --input <CUSTODY_INPUT.json> --input-sha256 <H> --out-dir <NEW_DIR>
```

## Tests (36): `test_roster_parent_check_c3v003.py`, on Codex3's cw8 inherited world (`test_inherited_cx3v003.py` `7d3afc1f`)

The world supplies real FULL builds, real PASS_ONE/PASS_K drivers and real step7 commits through the pinned base. A real custody breach is made with chmod 000 on one registered result and on a private custody-copy folder; nothing is deleted or overwritten, and permissions are restored.
- **C1–C3** (real CLI subprocesses): no-argument and unknown-command output is identical to the base. A wrapper refusal of an existing `--out-dir` happens before the (absent) input is read.
- **H1–H3:** the hazard rows above, each with exactly one ledger entry committed. **V1/V2:** valid base runs (NO_NEW_DISCREPANCY seq 1; NEW_UNEVALUATED seq 1).
- **W1/W6** (step7/custody): each of the four conditions is refused with the exact code, empty stdout, **no ledger entry and zero file reads**. **W2/W7:** the next valid wrapper run on the same build is the **first** commit (seq 1), with stdout equal to the base's. **W3/W8:** the out-dir result bytes equal the ledger entry bytes. **W4/W5:** relative and symlinked-parent `--out-dir` pass.
- **D1:** four malformed or other calls give (rc, stdout, stderr) identical to the base. **P1:** the real loader keeps `own_pin() == {base path, f710334b}`. **P2/P3:** a tampered or symlinked base refuses `BASE_PIN`.
- **Mutants:**
  - M1 (no exists check) and M3 (no access check) each let a commit happen;
  - M2 (no isdir check) changes the code to `NOT_WRITABLE`, still before the commit, because `access()` is false for a missing parent;
  - M4 (custody not covered) lets a commit happen;
  - M6 (no `abspath`) refuses a valid relative `--out-dir`.
  - All 5 are killed.

## Residual (not fixed here)
- A race between the check and the post-commit `mkdir` (root runs serially).
- Post-commit failures the check cannot foresee (ENOSPC, EIO). For those, the base custody main still lets an OSError escape uncaught. A base successor could catch it; that is outside this hardening.
- Codex1's abandoned draft (`c8c38ee4`, an edited full copy) is unrelated to this code. Claude3 read only the first 40 lines of its draft tests, to see which fixture they used.
