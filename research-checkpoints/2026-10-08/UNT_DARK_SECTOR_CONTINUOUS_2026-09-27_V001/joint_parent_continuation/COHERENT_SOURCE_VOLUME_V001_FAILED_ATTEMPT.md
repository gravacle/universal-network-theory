# V001 startup failure preserved

2026-09-29. Exit 1 before any scientific calculation: `RuntimeError:
Prospective freeze differs` at worker line 92. The freeze was generated in
Python, parsed by the orchestration layer and saved as JSON through apply_patch.
That serialization wrote integral-valued floats such as `0.0` as `0`.
V001 compared byte-canonicalized JSON encodings, so numerically identical
configuration values differed in representation. Source hashes were not the
cause. No scientific case was executed or accepted.

V001 source and freeze remain unchanged. V002 changes only the new freeze
filename and compares the parsed freeze with the generated snapshot using
structural numeric equality. Worker configuration values, source identities,
parent authentication, all equations, census and tolerances remain unchanged.
The worker uses its frozen source constants, never arbitrary numbers imported
from the freeze. This is a technical retry under the user's continuation
authority, not a scientific parameter or tolerance revision.
