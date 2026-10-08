# Independent source preflight: saved consistent-inertia states

Verdict: **PASS for one bounded root-owned saved-state audit**, subject to root's separate syntax check. This is a source review, not an executed audit or physical qualification.

Reviewed completely:

- `spherical_consistent_saved_audit_v001.py`, SHA256 `e8f2119f8580556e889387d88b2570a1d3087389f4ce362a41efcb9b9372fa0d`.
- `SPHERICAL_CONSISTENT_SAVED_AUDIT_PROTOCOL_V001.md`, SHA256 `4de96b72446950bdc5e67ad0d505aebbee037f179d9b831cac24fdf1588cddeb`.
- Relevant authenticated producer initialization/read, state-chart, and exact-inertia interfaces used by the auditor.

The dense shell assembly and quotient-rule derivatives independently express the finite inertia arithmetic. The constrained origin term, canonical relation `p=A Mv`, mesh-direction derivative `Mdot`, geometric force signs, peculiar-velocity acceleration, and instantaneous geometric-work cancellation are consistent. The audit uses retained states; it calls no trajectory, RHS, producer main, snapshot, or integrator entry point. Material and gravity readouts are deliberately reused, not independently derived.

The two cases, five methods, four times, eight fine snapshots, pressure-on/off signed profiles, physical-chart comparisons, and inherited arithmetic/material/work criteria are fixed. Partial or failed producers cannot be promoted by successful reconstruction of a subset. Fine snapshot and method-journal comparisons bind saved quantities to actual raw states. Nonfinite values and resource/custody failures remain failures.

Custody checks distinguish pinned file identities from canonical payload identities. Case and invocation payloads are recanonicalized; exact captured stdout is bound to the corresponding raw case result. The science-freeze members and final input bytes are rehashed. Exclusive intent/result publication, bounded inputs/output, single-thread requirements, CPU/wall guards and sampled RSS are explicit; reported resources precede final serialization.

The producer and auditor share an author. Independent source review plus different dense arithmetic does **not** become independently authored replication. All physical, continuum, metric, formation, observation and Stage 3 qualification flags remain false. No scientific run, compilation, producer import or numerical postprocessing was performed by this reviewer.
