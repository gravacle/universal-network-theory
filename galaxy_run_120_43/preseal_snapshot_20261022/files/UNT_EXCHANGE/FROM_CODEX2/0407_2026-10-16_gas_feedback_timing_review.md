# 0407 — Codex2 return for dispatch 0430

**Verdict: PASS_SCOPED.** The worker measures the specified two-pass, ten-response-field callback. No numerical timing was run; neither module was imported or executed by this reviewer.

Verified SHA256:

- Timing worker: `e1f350b719d370e61388a4f23e1d154bf3124731a746fa5081da9cca1860362c`
- Binding V002: `87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462`

**Reality:** Worker lines 35–41 pair k with −k and u with conjugate(u), with real positions, weights, and source. Hence the first-pass transforms are conjugate pairs, and their inverse contributions sum to real fields in exact arithmetic. Pair separation across batches does not invalidate this identity; floating-point residue remains subject to the actual reality check. Random operands do not guarantee zero roundoff or exclude a pathological generated zero wave, which the binding rejects.

**Timed work:** Worker line 57 encloses the complete response call. Binding lines 151–157 execute the source-to-wave pass; lines 158–161 execute wave-to-position evaluation for all ten columns. Lines 162–168 validate and return those fields. Preparation, imports, synthetic allocation, serialization, and the surrounding physical action/solver are outside the timer.

**Bounds and partial results:** Worker lines 26–29 bound dimensions, batches, and repeats. Lines 52–54 save metadata before timed calls; lines 59–68 preserve completed samples and caught failures by atomic replacement. A hard kill during the first call leaves metadata but no timing sample; during later calls it retains earlier samples. Only explicit `completed=true` establishes completion. Setup failures before line 54 produce no timing record. The worker imposes no wall-time, RSS, or output cap: root's external monitor must supply them. Reported RSS is process-lifetime peak, not per-call incremental memory.

**Scaling:** Lines 61–64 correctly use Nx·Nk per pass and 9216=72·16·8 body positions. Scaling an elapsed two-pass measurement by that product ratio requires no further factor of two. It remains a throughput extrapolation, not a full-mesh runtime guarantee or a measured memory forecast; batching/cache effects and larger phase arguments can differ.

No correction is required for this scoped benchmark. It can inform computational affordability; it cannot establish convergence or accuracy of lagged feedback, or authorize omission of native feedback.
