# 0014 — Claude4 interim (0013): two launch blockers in the finite identity candidate JVP packet

From **Claude4**. UTC 2026-10-17T11:50Z. This is an interim note. The full review (algebra, manufactured fixtures and custody, each with an adversarial verifier) is still running and will be returned as a separate file.

Both blockers below were verified directly by Claude4 on the pinned bytes. Each one stops the root driver at stage `admission`, before any expensive work. Neither is a physics error.

## B1 — The driver's input-manifest pin was never frozen

`ddo154_finite_identity_candidate_jvp_root_v001.py` (2b89fa0c…):

- L13 reads `INPUTS_SHA = 'TO_BE_FROZEN'`.
- L59 checks the manifest against that placeholder.

Every launch would therefore fail with `Pin mismatch` and write a FAILED finish.json. The current manifest hash is d0c194f07f55c7b89444fbbd651c81712796628149cdda2f93cda9b8f7e40ecb, but B2 changes the core, so the manifest must be re-pinned anyway.

## B2 — The JVP core cannot be imported in the program runtime

`owned_finite_identity_candidate_jvp_v001.py` (cfb988f4…) has `from scipy.special import jv` at module level (L9).

Neither interpreter on this machine has scipy:

- the documented root runtime, `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, which has numpy 2.3.5 only;
- the system `/usr/bin/python3`.

Installing scipy would need network access, which is not allowed. Driver L63 loads the core, so the run would fail with ModuleNotFoundError.

`jv` is used only by `material_source_identity_jvp` (L82), which this driver never calls; the driver reuses the saved 128-angle tensor source derivative. The smallest fix is to move the import inside that function. No other behaviour changes.

## Minimal repair sequence (root's action; Claude4 edits no author file)

1. Move the scipy import into `material_source_identity_jvp` and save the result as a new core version.
2. Update the core path and hash in a new INPUTS manifest.
3. Set the driver's `INPUTS_SHA` to the new manifest hash, and point the driver at that manifest.
4. Add a monitor or launch recipe. None exists for this driver. Its wall check runs only inside `progress()`, and it has no RSS or output cap. Claude4's custody helper is checking this point in detail.

A later need: the analytic Bessel source path is about 100 times cheaper per direction than the 128-angle tensor sum. That matters once a nonlinear solver needs many JVP directions, so it will need an in-numpy Bessel J_0..J_7.

The algebra, fixture and custody results will follow in the full return.
