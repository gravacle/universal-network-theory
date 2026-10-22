# Backlog #7: roster-builder `--out-dir` checks before the step-7 ledger commit. README C3V003 (A272 hardening; D038)

**Author:** Claude3. **Reviewer:** Codex1 (narrow, as offered in 0288/0293), else Claude4. Not adopted until root rules.

- **`roster_builder_parent_check_c3v003.py` — `ea1a40fa43d69a9cfda20099cb37be0e53e5933808869a7ebe995f7f62652610`** (the wrapper to use)
- `test_roster_parent_check_c3v007.py` — `8b0e15c34bbdf40f9ef03621f20a2c8f28b55afd75f35d8966aaf293b65d9df5` (the selected suite)
- `TEST_RECORD_ROSTER_PARENT_CHECK_C3V003.json` — `8e1d76032ea4381600614efd73292daf85455b5a5af3a7438c4053f0dc1ce2f0` (51/51; 9 of 9 mutants killed; `$PY` 3.12.14)
- **c3v002 (`77509a08`) is NOT FOR USE:** Codex1 delta review B7-2 (0297). It refused a dangling symlink named with a trailing slash even when the link target's parent exists. The base's `mkdir` then follows the link, creates the target and succeeds. c3v003 resolves that target with `os.path.realpath`, which follows symlinks and `..` in kernel order, and checks the target's own parent. In K1, its `preflight` gives the same outcome as the kernel's `mkdir` on 14 symlink and trailing-slash shapes.
- **c3v001 (`27b55142`) is NOT FOR USE:** Codex1 review B7-1 (0295). It used `os.path.abspath`, which collapses `..` before symlink traversal. With `--out-dir` = `lexical/link/../X/out`, where `link` points elsewhere, it refused a valid call when only the real parent existed, and admitted a call whose real parent was missing, so the base committed and then failed. c3v002 checks the kernel's resolution of the RAW prefix (`dirname(name) or '.'`, with `name = out_dir.rstrip('/')`), with no `abspath` or `normpath`.
- Preserved drafts, not for use: tests v001 `8980e647`, v002 `e3919a6a`, v003 `0ea8ebaf` (c3v001), v004 `6390730f` (its M1 still matched c3v001 text, so it was a no-op), v005 `85bbd2cb` (c3v002), and v006 `2cce901a` (a stale explicit assert of c3v002 text).
- Base, unchanged: `cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` `f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11`.

## The hazard (shown on the unchanged base with real commits; tests H1–H3)

`step7` and `custody` write the ledger entry `STEP7_<seq>.json` (base L2039 "the commit point", L3466) **before** `main` creates `--out-dir` (L2347, L4506). So a bad `--out-dir` fails **after** the commit: the ledger has advanced, and `STEP7_RESULT.json` / `CUSTODY_RESULT.json` / `REPLAY_PLAN.json` are missing.

| Command | `--out-dir` exists | parent missing | parent is a file | parent read-only |
|---|---|---|---|---|
| step7 (base) | commit, then refused `OUT_DIR_EXISTS` (rc 2) | commit, then `internal_error FileNotFoundError` (rc 1) | commit, then `NotADirectoryError` (rc 1) | commit, then `PermissionError` (rc 1) |
| custody (base) | refused before the commit (the base already checks this) | commit, then the exception **escapes `main`** (the custody main catches only Stop/Refused: a traceback) | the same, `NotADirectoryError` | the same, `PermissionError` |

## The fix: a thin pre-commit wrapper

The wrapper loads the base from its pinned bytes (O_NOFOLLOW, regular file, full sha) with the base's own `__file__`. For a well-formed `step7` or `custody` call (exactly `--input`, `--input-sha256`, `--out-dir`), it refuses first, printing the base's own refusal form `{"refused": CODE, "detail": OUT_DIR}` to stderr with rc 2:
- `OUT_DIR_EXISTS` when any entry exists at the name, by lstat of `--out-dir` without trailing slashes. The exception is a symlink named WITH a trailing slash: `mkdir` follows it and creates its final target, so the wrapper resolves that target (`os.path.realpath`) and checks it instead. Such a link is `OUT_DIR_EXISTS` only if it resolves to an existing entry or does not resolve (a loop);
- `OUT_DIR_PARENT_MISSING` when the raw parent (`dirname(name) or '.'`, resolved by the kernel exactly as `mkdir` resolves it) is missing or is not a directory;
- `OUT_DIR_PARENT_NOT_WRITABLE` when the parent is not writable and searchable.

Otherwise it runs the **unchanged base `main`** with the same argv. Every other command, and any malformed call, goes straight to the base.

**Why a wrapper and not an edited copy:** the base bytes and sha stay `f710334b`, so `own_pin()`, every record the base writes, and every consumer that pins the base (for example the schedule-ceiling writer and root's TOOL_PIN) are unchanged. An edited copy would change the sha that those consumers check.

**No new honest-path refusal.** Each check is a condition under which the base's post-commit `os.mkdir` must fail (rows above). Valid absolute, relative and symlinked-parent `--out-dir` values pass (W2, W4, W5).

## Root command form (step7 and custody only; other commands may stay on the base)

```bash
R=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3/roster_builder_parent_check_c3v003.py
"$PY" -I -B "$R" step7   --input <STEP7_INPUT.json>   --input-sha256 <H> --out-dir <NEW_DIR>
"$PY" -I -B "$R" custody --input <CUSTODY_INPUT.json> --input-sha256 <H> --out-dir <NEW_DIR>
```

## Tests (51): `test_roster_parent_check_c3v007.py`, on Codex3's cw8 inherited world (`test_inherited_cx3v003.py` `7d3afc1f`)

The world supplies real FULL builds, real PASS_ONE/PASS_K drivers and real step7 commits through the pinned base. A real custody breach is made with chmod 000 on one registered result and on a private custody-copy folder; nothing is deleted or overwritten, and permissions are restored.
- **C1–C3** (real CLI subprocesses): no-argument and unknown-command output is identical to the base. A wrapper refusal of an existing `--out-dir` happens before the (absent) input is read.
- **H1–H3:** the hazard rows above, each with exactly one ledger entry committed. **V1/V2:** valid base runs (NO_NEW_DISCREPANCY seq 1; NEW_UNEVALUATED seq 1).
- **W1/W6** (step7/custody): each of the four conditions is refused with the exact code, empty stdout, **no ledger entry and zero file reads**. **W2/W7:** the next valid wrapper run on the same build is the **first** commit (seq 1), with stdout equal to the base's. **W3/W8:** the out-dir result bytes equal the ledger entry bytes. **W4/W5:** relative and symlinked-parent `--out-dir` pass.
- **B7-1 controls (Codex1 0295):**
  - **L1/L1c:** `lexical/link/../only_actual/out`, where only the real parent exists, is valid for step7 and for custody and gives the first commit.
  - **L2/L2c:** `lexical/link/../only_lexical/out`, where only the lexical parent exists, is refused with no commit and zero reads, for step7 and custody.
  - **L3:** `nope/../out`, with a missing intermediate, is refused.
  - **L5:** a dangling symlink with a trailing slash whose target parent is missing is refused (`OUT_DIR_PARENT_MISSING`).
  - **L6/L6c (B7-2):** a dangling symlink with a trailing slash whose target parent exists is valid for step7 and custody; the outputs land in the created target.
  - **L7:** a symlink loop with a trailing slash is refused (`OUT_DIR_EXISTS`).
  - **K1:** `preflight` itself is compared with the kernel's `mkdir` on 14 shapes: dangling (relative, absolute, chained), loops, links to an existing dir or file, read-only targets, `..` after a symlinked dir, a target string with a trailing slash, a dangling parent link, a plain name, and a regular file. All 14 give the same outcome.
  - **H_L2/H_L3/H_L5/H_L7:** on the unchanged base, each of those four commits and then fails.
  - **L4:** a trailing-slash `--out-dir` is valid.
- **D1:** four malformed or other calls give (rc, stdout, stderr) identical to the base. **P1:** the real loader keeps `own_pin() == {base path, f710334b}`. **P2/P3:** a tampered or symlinked base refuses `BASE_PIN`.
- **Mutants:**
  - M1 (no exists check) and M3 (no access check) each let a commit happen;
  - M2 (no isdir check) changes the code to `NOT_WRITABLE`, still before the commit, because `access()` is false for a missing parent;
  - M4 (custody not covered) lets a commit happen;
  - M6 (no `or '.'`) refuses a valid relative `--out-dir`;
  - M7 (the existence check on the raw string with its trailing slash) lets a commit happen for L5;
  - M8 (the c3v001 lexical parent restored) lets a commit happen for L2;
  - M9 (no unresolved-chain check) lets the loop commit;
  - M10 (no trailing-link branch) refuses the valid L6.
  - All 9 are killed. Every mutant asserts that its replacement applies exactly once. The `os.path.exists(name)` line inside the link branch is redundant with the unresolved-chain check, since both return `OUT_DIR_EXISTS` for a link to an existing entry. Its mutant would be equivalent, so it is not counted.

## Residual (not fixed here)
- A race between the check and the post-commit `mkdir` (root runs serially).
- Post-commit failures the check cannot foresee (ENOSPC, EIO). For those, the base custody main still lets an OSError escape uncaught. A base successor could catch it; that is outside this hardening.
- Codex1's abandoned draft (`c8c38ee4`, an edited full copy) is unrelated to this code. Claude3 read only the first 40 lines of its draft tests, to see which fixture they used.
