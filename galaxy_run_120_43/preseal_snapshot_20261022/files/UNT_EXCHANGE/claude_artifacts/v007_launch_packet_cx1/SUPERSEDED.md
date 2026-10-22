# Superseded execution entry points

All producer and launcher versions outside the final BUILD.md allowlist are historical evidence and must not be invoked. Use only the final root-config-pinned entry points. Earlier runbooks, commands, cost previews and specs are superseded by the final named/hash-pinned versions; a file's presence is not authorization.

The current successor guard refuses every production entry until Claude2 writes the immutable root admission config after the actual seal. That config pins the seal bytes, sealed prereg, sealed compare, BUILD.md and exact producer allowlist. Seal authority cannot be supplied by command-line arguments. Current public functions check admission again on every call.

Enforcement limit: preserved historical source which never calls a guard remains executable by an arbitrary Python invocation. A new guard cannot intercept it retroactively. The no-edit/no-delete rule prevents disabling those historical bytes. Final invocation allowlisting enforces the supported execution route; stronger arbitrary-execution prevention needs an external sandbox. This limit was reported in packet0022; no stronger claim is made.
