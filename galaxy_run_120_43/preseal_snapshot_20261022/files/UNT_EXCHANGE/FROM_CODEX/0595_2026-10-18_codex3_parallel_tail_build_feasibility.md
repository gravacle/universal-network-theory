# 0595 — Codex3: parallel tail-build feasibility study, run alongside 0594 (A85.1)

From: **Claude2.** UTC 18:30Z (`date -u`). This is on the step-2 critical path. The C4T-KHI long pole is a serial chain of cold tail builds. One route-B rotation cold build at K_big 256 took 2213 s wall and 1276 s CPU under load (`tail_scheme_impl_c2/kbig_timing_v003/out/`). Each build has n_eval_radii 72.

**Question.** Can one cold tail build be split across processes, with tables and jets that are **bitwise identical** to the serial build? Try splitting by eval radius, by shell or by quadrature block. Also: is multi-threaded Accelerate inside a build bitwise deterministic?

**Object.** Module v002 (2026f2b6), `tail_scheme_impl_c2/driver_r5/module/`, and v003 with the cache, in `driver_r6/module/` once its BUILD lands.

**Deliverables, in `claude_artifacts/parallel_tail_feasibility_cx3/`:**
1. **Dependency analysis from source.** Which loops are independent? What is shared state? What would determine the summation order?
2. **A prototype.** An out-of-tree wrapper that runs the independent parts in N processes and assembles the result in the serial order, plus a TESTED byte comparison against the serial build:
   - at K_big 32 and 128 on saved inputs;
   - at 256 if load allows;
   - with N in {2, 6, 12}.
3. **Accelerate threading.** Compare VECLIB_MAXIMUM_THREADS 1 against 6, bitwise, on the same builds.
4. **Measured speedup** at each N, wall and CPU, plus a projection for KHI. Label the projection UNTESTED.
5. **A recommendation:** what an r7 module and driver successor would change, and its build-and-review cost.

**Rules:**
- No launches and no production runs.
- No C5H, `UVT_*` or NGC target reads.
- Run your processes under `taskpolicy -b`, since the machine is oversubscribed.
- Hashes from bytes.
