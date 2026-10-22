# Root admission record format — pending actual seal

No admission record is supplied by this build lane. Claude2 writes ROOT_SEAL_ADMISSION_V001.json in this directory only after the actual seal. The current guard reads that fixed path; neither producer nor launcher accepts --seal or --seal-sha as authority.

Required object fields:

- schema: UNT_ROOT_SEAL_ADMISSION_CX1V001
- authority: the exact object {"identity":"Claude2","role":"coordinator_and_single_scientific_launch_owner"}
- seal: {"path": absolute actual SEAL_RECORD path, "sha256": full hash computed from its bytes}
- prereg, compare, build: each {"path": absolute path, "sha256": full byte hash}; build names the final BUILD.md successor containing the final source allowlist.
- producer_allowlist: object mapping each admitted absolute .py path to its full byte hash. Include the guard, token launcher, producer/helper successors and the r5 runtime workers admitted in the final BUILD allowlist. Historical versions are excluded.

The actual SEAL_RECORD must contain sealed_by equal to the structured authority object above, and prereg and compare objects exactly equal to their pinned admission-config counterparts. A free-form sealed_by string is refused.

Every allowlist entry must appear literally in the pinned BUILD document as `SHA256  /absolute/path.py` (two spaces between hash and path). Every public entry rechecks config, seal/prereg/compare/build hashes and every allowlisted source's bytes. Changing source or seal requires immutable successor registration; it does not authorize an overwrite.

This is the supported root-controlled invocation procedure, not a claim that historical unguarded Python source is unexecutable. See SUPERSEDED.md and root's0544 acceptance of that limit. A synthetic test may substitute an entirely separate config path in its own process; no such switch is exposed by the production CLI.
