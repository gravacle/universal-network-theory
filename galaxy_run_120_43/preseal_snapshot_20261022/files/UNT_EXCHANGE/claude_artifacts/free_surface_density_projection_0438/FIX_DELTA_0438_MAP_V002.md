# FIX DELTA 0438 MAP V002: map c2v001 → c2v002 (review note 1)

Role: fix author. I am not the map author or the reviewer. Date: 2026-10-16. UNT 0441, Claude2 lane.

The fix covers synthetic stubs only. It used no project data, ran nothing at project scale, and wrote nothing under `/Users/bgm/Research/Universal Network Theory`.

## Inputs (sha256 computed from bytes; all match the commissioning hashes)
| File | sha256 |
|---|---|
| `free_surface_density_projection_map_c2v001.py` (base, unchanged) | 1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee |
| `INTERFACE_0438_MAP_V001.md` | e71e7468df814746d597038a1ad60de45e6c1c8c211110e006ce9e5bcaa9741d |
| `REVIEW_0438_MAP_V001.md` (PASS_WITH_NOTES) | 1013905ba262e807ad7e551c160760facf6fdb876a6ce1bbd49282232e9e9976 |
| `fixtures_0438_map_c2v001.py` (fixture helper script) | b6cecb2363383ec6f9aca32af14927a8a07ea5fed133046d81142b9803ab148f |

## Outputs (exclusive create)
| File | sha256 |
|---|---|
| `free_surface_density_projection_map_c2v002.py` | 7015470d186acab3ffe6cb21aa105ae60e0c0b4d96effa3a79f15c4c14019947 |
| `INTERFACE_0438_MAP_V002.md` | 66995a129565e19b2a4a1a034554ab4895a51c853d6dec6437581fc3f6491293 |

## The defect (review note 1)
In c2v001, lines 379–380 ran before the per-block finiteness test at line 388:

```
store["B"][:, c0:c1] = Bk
out["B_assembled_batches"].append(k)
```

Suppose a batch's B overflowed without an exception, under the default errstate. The batch was then listed in `B_assembled_batches`, and `partial_B` held its non-finite values. That contradicted two statements in the interface:
- "partial entries are NaN unless they completed and passed their checks";
- "B columns of batch k are valid if k is in B_assembled_batches".

Reproduced on c2v001 with the reviewer's exact R7d input:
- `B_assembled_batches` = [0, 1, 2];
- 576 non-finite entries in `partial_B[:, 4]`.

## The change
The store and the append now run only if the whole batch's B passes an explicit isfinite test (c2v002 lines 389–391):

```python
if np.all(np.isfinite(Bk)):
    store["B"][:, c0:c1] = Bk
    out["B_assembled_batches"].append(k)
```

**Code only.** Docstrings and comments were stripped and the two versions compared by AST, using `ast.unparse` plus difflib. The entire difference is:

```
-        store['B'][:, c0:c1] = Bk
-        out['B_assembled_batches'].append(k)
+        if np.all(np.isfinite(Bk)):
+            store['B'][:, c0:c1] = Bk
+            out['B_assembled_batches'].append(k)
```

**Text changes:**
- the module docstring names c2v002, the c2v001 sha and the reason;
- the retention paragraph states the new `B_assembled_batches` meaning;
- a four-line comment sits above the test;
- the `project_density_map` docstring says "NaN where not completed and checked".

## Rationale: why this form
Three properties make this form the right one:
- **It meets the requirement literally.** Retention and bookkeeping of a batch's B now happen only after that batch's B passes an isfinite test. Nothing goes under `partial_B` without a check. The optional `failed_batch_B_unvalidated` key was not used, so the set of retention keys is c2v001's.
- **The stop decision is untouched.** The new test only decides retention. When it fails, the existing per-block test at line 399 is guaranteed to stop the batch at or before the first block whose B is non-finite. An earlier singular or non-finite solve can also stop it first. So status, reason, `failed_stage`, `failed_batch`, `failed_block`, `completed_block_batch` and `completed_batches` are exactly c2v001's. This was checked bitwise.
- **Valid B is still kept.** If a batch's B is finite and a later solve fails, as with a singular block or an injected error, its B is still retained and listed, as in c2v001.

Two alternatives were rejected:
- **Store B after the block loop finishes.** This would discard finite, valid B for a batch whose later block solve fails. In the helper's C5 singular-block cases, `partial_B` for batch 0 would become NaN, while C5 `retained_B_for_completed_batches` (fixture lines 1124–1129) compares that batch with the reference. This follows from the fixture code; it was not executed.
- **Return immediately when the new test fails.** This would move the failure from ("block solves", block 0) to ("assembly of B", block None) and change the reason. That would alter the statuses and locations that the task required to stay the same.

**Unchanged:**
- the equations and their grouping;
- every einsum (all `optimize=False`);
- no BLAS and no `@`;
- no warning or errstate suppression;
- validation;
- the exception handlers;
- the statuses;
- every other retention key.

**Cost:** one boolean temporary of 576 B per batch column, created after the B-term arrays are released.

## Residual caveats (not fixed; outside note 1)
- **Under-reporting for the failing batch.** A batch whose B is non-finite only in later blocks still has its earlier blocks solved and recorded in `completed_block_batch`. Its `partial_B` is NaN in full, so B is under-reported for that batch, which is the safe direction. This was demonstrated at full size (D4: failure at block 40 of batch 2, with 40 pairs completed).
- **Interrupt window (review note 3).** An asynchronous KeyboardInterrupt between the store (390) and the append (391) can leave finite, checked values in `partial_B` for an unlisted batch. That is also the safe direction.
- **Author fixture T8b.** The author's T8b in `scratchpad/r0441/author/fixtures_0441_map.py` asserts `B_assembled_batches == [0, 1, 2]`, which encodes the defect. That fixture is therefore 185/186 on c2v002, with T8b as the only FAIL. Every other T8b conjunct holds, as `t8b_conjuncts_run1.out` shows. A successor of the author fixture should expect [0, 1].
- **einsum overflow is silent.** On numpy 2.0.2 / arm64, the D4 einsum overflow raised no RuntimeWarning under the default errstate, so only the explicit isfinite tests catch it. This is an observation, not a change.

## Evidence (all on c2v002; `/usr/bin/python3 -I -B`, numpy 2.0.2, python 3.9.6)
Runs were made in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0441v2/fix`.

| Run | Result | sha256 |
|---|---|---|
| fixture helper `fixtures_0438_map_c2v001.py … --expect-sha256 7015470d…` → `fixture_run_c2v002.out` | pass=549 fail=0 unresolved=0 info=58, ALL_PASS, exit 0; output differs from the reviewer's c2v001 run only in the C0 isfinite count (11 → 12) | 2e62fe4a165aafaaf1d0f13bded33f897eaf55cfa51ca8151dc1459555850fa7 |
| `fixture_run_c2v002.json` | counts and verdict as above | f5c490db39d1877a57af4fae24740d06e06b9cc135c14745d4b40d96d55087bf |
| `repro_note1_c2v002.py` | the script itself | e6496bc12478e72ce7cd0b6af964c7f301ff58e1bbe840dd2af7e3d1773c3871 |
| `repro_note1_c2v002_run1.out` | 75 PASS, 0 FAIL, 8 INFO | ce725715a0d6ecacb257b7c0fc9506d17650b6d17cafd9a5179ec6cd2672413e |
| author `fixtures_0441_map.py` (b24a7ced…) → `author_fixture_on_c2v002.out` | 185/186; only T8b fails, because it encodes the defect | 7e4f29bf0ca98b93b23ace553bd27c49df95396ee160852dd632cc1339bba0c6 |
| `t8b_conjuncts.py` | the script itself | c5bf3dcb468ff066299abf0c84ec18b714863b6388aed22463048ae412a7bd41 |
| `t8b_conjuncts_run1.out` | T8b conjuncts evaluated on both versions | af81792cf3e9594760f6c01f0600ecbd0709b8b9b5b25978af4f15e588bf533d |

### The reviewer's default-errstate batch-2 overflow
The input is R7d: `make_stub(11)`, `make_xi(41, 7)`, mode 3, bs 2, `xi_R[70, 4] = 1e308`.

| | c2v001 | c2v002 |
|---|---|---|
| status / reason | failed_closed_solve / "non-finite M block or B block [stage: block solves; batch: 2; block: 0]" | identical |
| `B_assembled_batches` | [0, 1, 2] | **[0, 1]** |
| `completed_batches` | [0, 1] | [0, 1] |
| `partial_B[:, 4:6]` (batch 2) | column 4 has 576 non-finite entries; column 5 has 576 finite entries | **all 1152 entries NaN in both parts** |
| `partial_B[:, 0:4]` | good run, bitwise | good run, bitwise |
| every other key | — | bitwise equal to c2v001 |
| RuntimeWarnings reaching the caller | 1 | 1 (nothing suppressed) |

The other cases are each bitwise equal to c2v001 on every key, and in each the c2v002 invariants hold:
- **D2, D3:** the same input under `errstate(all='raise')` and under a warnings "error" filter;
- **F1–F6:** a non-finite solve, KeyboardInterrupt, LinAlgError, ValueError, a singular block, and an interrupt in M assembly;
- **G:** good runs at bs 1, 2 and 7.

The invariants are:
- `partial_B` is finite for listed batches;
- `partial_B` is NaN for unlisted batches;
- `completed_batches` ⊆ `B_assembled_batches`;
- there is no unvalidated key.

After all runs, the c2v001 module was unchanged (1422ace7…) and so was c2v002 (7015470d…). No `__pycache__` was written in the artifact directory.

## diff -u free_surface_density_projection_map_c2v001.py free_surface_density_projection_map_c2v002.py
```diff
--- free_surface_density_projection_map_c2v001.py	2026-10-16 13:23:09.262563436 -0500
+++ free_surface_density_projection_map_c2v002.py	2026-10-16 13:38:11.696512358 -0500
@@ -1,4 +1,8 @@
-"""UNT 0441 -- batched density-projection MAP on the reviewed 32-point free-surface mesh (Claude2, map c2v001).
+"""UNT 0441 -- batched density-projection MAP on the reviewed 32-point free-surface mesh (Claude2, map c2v002).
+
+Successor of map c2v001 (sha256 1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee), fixing note 1
+of REVIEW_0438_MAP_V001: a batch's B is now stored in the retained B array, and the batch appended to
+B_assembled_batches, only after the whole batch's B passes an explicit isfinite test. Everything else is c2v001.
 
 The 0438 conservative density projection applied column-wise to root-supplied displacement maps (task 0441).
 It is the same specified linear projection, not a new physical equation. The 0438 vector API (project_density in
@@ -39,8 +43,10 @@
 / escalated RuntimeWarning -> "failed_closed_floating_point"; KeyboardInterrupt -> "interrupted", returned and not
 re-raised; any other exception -> "failed_closed_internal") returns completed_block_batch (n_blocks, n_batches),
 B_assembled_batches, completed_batches, failed_stage / failed_batch / failed_block and partial_<key> arrays that
-are NaN wherever the entry was not completed and checked. The primary result keys are then None. An interruption
-during validation, before any work exists, propagates unchanged.
+are NaN wherever the entry was not completed and checked. B_assembled_batches lists batch k only after all of
+B[:, batch k] passed an isfinite test; a non-finite B is never stored, so its partial_B columns stay NaN. The
+primary result keys are then None. An interruption during validation, before any work exists, propagates
+unchanged.
 
 Explicit assumptions of the supplied weak domain (stated, NOT verified by this routine):
   * physical-vacuum vanishing density on the free surfaces (no surface term in the weak form);
@@ -376,8 +382,13 @@
         del X
         Bk = b_radial + b_azimuthal + b_vertical
         del b_radial, b_azimuthal, b_vertical
-        store["B"][:, c0:c1] = Bk
-        out["B_assembled_batches"].append(k)
+        # Retain B for this batch, and list the batch in B_assembled_batches, only after the whole batch's B
+        # passes this explicit isfinite test. A non-finite B is never stored (its partial_B columns stay NaN).
+        # This test decides retention only: the stop is still decided by the per-block test below, so the
+        # status, reason, failed_stage and failed_block are those of c2v001.
+        if np.all(np.isfinite(Bk)):
+            store["B"][:, c0:c1] = Bk
+            out["B_assembled_batches"].append(k)
 
         prog["stage"] = "block solves"
         Ck = np.empty((n_cols, c1 - c0), dtype=np.complex128)
@@ -470,8 +481,9 @@
     plus batch bookkeeping. Otherwise status "rejected_input", "failed_closed_solve",
     "failed_closed_floating_point", "failed_closed_internal" or "interrupted"; after validation the failure
     statuses keep completed_block_batch (72, n_batches), B_assembled_batches, completed_batches, failed_stage /
-    failed_batch / failed_block and partial_<key> arrays (NaN where not completed), with the primary result keys
-    None. There is no physical acceptance flag.
+    failed_batch / failed_block and partial_<key> arrays (NaN where not completed and checked; a batch enters
+    B_assembled_batches and partial_B only after its whole B is finite), with the primary result keys None.
+    There is no physical acceptance flag.
     """
     return _project_density_map_sized(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                       radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
```
