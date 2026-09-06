# Hostile audit report: L14 feasibility screen

## Verdict

**PASS, with a strict engineering-only reading.** The target packet remains unchanged. Its exact finite group count and its conditional fixed-width numeric-array arithmetic independently reproduce. The screen supports only eligibility for a guarded implementation trial; it does not certify that an L14 process fits, finishes, or produces an accumulation result.

## Independent reconstruction

The audit rebuilt all 28 site permutations directly in prism coordinates, without importing the target program or trusting its `RESULT.json`. The independently obtained cycle census is `6(14,14)`, `6(7,7,7,7)`, `8(2^14)`, `7(1^4,2^12)`, and the identity. Thus the Burnside numerator is

`6*4 + 6*16 + 8*16384 + 7*65536 + 268435456 = 269025400`,

and division by 28 gives exactly `9,608,050` binary-word orbits.

## Transition-ceiling attack

For one representative, each of the 42 owner-once edges specifies at most one deterministic swap attempt and therefore at most one unaggregated destination slot. Hence `9,608,050 * 42 = 403,538,100` is a valid allocation upper bound. It is not the actual number of distinct quotient destinations or nonzero matrix entries: inactive swaps, coincident quotient destinations, and cancellation/aggregation may reduce those counts. The target's words “unaggregated transition” and “ceiling” preserve this distinction, so no correction is required.

## Payload attack

All nine terms were rebuilt from dimensions and fixed element widths. Their sum is exactly `11,325,552,642` bytes, or `10.547742845490575 GiB`. This is conditional on the listed candidate arrays being the relevant simultaneously retained numeric payload. It excludes allocator/interpreter overhead, compiled code, temporary workspace, mapping/build structures not listed, and other process memory. Consequently the `37.452257154490575 GiB` subtraction from 48 GiB is raw-array arithmetic, not usable RSS headroom or a fit guarantee.

The two raw-current-kernel term is internally consistent: two kernels times `2^27` active words per kernel times `(int32 + int32 + float64) = 16` bytes gives `4,294,967,296` bytes.

## Pins and claim ceiling

The four target artifacts and five inherited L12/prism inputs match their declared SHA-256 pins. The target validator passes `18/18` under warnings-as-errors and preserves its canonical result. L12 runtime/RSS remain sealed empirical inputs only; neither is extrapolated. The target explicitly leaves L14 construction, process RSS, runtime, evolution, currents, retained record, and ledger residual open, and disclaims grid, continuum, Ward, phase, graviton, gravity, scaling, and complexity claims.

No target edit was necessary.
