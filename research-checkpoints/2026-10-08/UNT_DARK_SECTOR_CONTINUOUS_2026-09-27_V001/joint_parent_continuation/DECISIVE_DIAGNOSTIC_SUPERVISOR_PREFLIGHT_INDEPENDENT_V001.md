# Independent review of the single diagnostic supervisor

2026-09-30. Reviewer: `short_path_adversarial`. Source-only **PASS** for
`decisive_diagnostic_supervisor_v001.py`, SHA-256
`8c290066d3e5d3aadfe68b6a1f9ec6be4252e3fb8511b169e1163a2568f42436`.
No import, syntax compilation, freeze, child execution or numerical audit was
performed by this reviewer. This verdict concerns the capture wrapper, not a
new independent review of the native algebra or a scientific result.

The complete wrapper, the reused monitor's actual `invoke` implementation and
top-level import behavior, the publisher's actual `publish` implementation,
the prior finite-gap capture wrapper, both child publication contracts and
the native protocol were read. Actual source hashes and the manifest's
environment dictionary shape were checked using read-only tools.

Reviewed helper identities are monitor
`d88f84a3a8fa3187ff1dd128bc2e18c3606830d54966789a3ab96c619c2f7778`,
publisher `f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8`
and environment manifest
`ab8f3dddd2663864e1d5957f3a36341e657d737110f3bc377da566f2b61732bd`.
The native source/protocol pins are
`e701bcfec5328caa2a32e30b1dcc1e17c86c6e7e5e047a55aa64942292b575e9` /
`e3932a026d963527150b68d6e439d8e5e922ddc8f3ef95e83f385d2b9a25c17f`;
the thermal auditor/protocol pins are
`25f0381e2c5e5833dd40f12458831c0fceddbb0de8a3fa1e24259686f128358e` /
`8850f8ea9ea34a10d85521d9010227377eda9d5268101c06fb3f4bf6e057044a`.

Exactly one named lane is required per invocation. No lane loop, queued work,
automatic freeze, retry, compiler call or scientific import exists. Non-main
`runpy` loads only the pinned monitor/publication definitions; the publisher's
top-level thread environment settings are inherited, not a model run. The
in-place monitor CONFIG update reaches the function's shared configuration.
Native 45-second and thermal 15-second targets, each with 256 MiB sampled
process-group RSS, are checked against the corresponding child freeze.

Before launch, the wrapper refuses any pre-existing wrapper or child intent or
result, verifies reviewed sources and all child freeze file hashes, and saves
an exclusive intent containing source/freeze identities, argv and resource
settings. The established publisher uses no-overwrite links and fsync. Child
stdout/stderr and monitor metadata are retained even for nonzero exit,
malformed output, watchdog failure or a caught validation error. A present
child result is retained by hash before clean-process checks. Hard controller
termination may leave only an intent; that is not a success or permission to
retry silently.

Success requires a clean process and monitor, empty stderr, bounded summary
stdout, the exact expected child status, canonical payload and freeze hashes,
child intent artifact, raw stdout publication identity and unchanged end
inputs. Physical, thermal, propagation and Stage-3 promotion remain false.

The monitor uses 0.25-second samples, an external `ps` query with its own
timeout and a five-second termination grace. These are sampled resource
guards, not strict unsampled-memory or instantaneous wall guarantees. The
wrapper launches one numerical child per invocation; it does not implement a
global concurrency lock across separately invoked lanes. Root must continue
to serialize launches. No extra qualification or numerical tolerance follows
from this source review.
