# L14 targeted-scout run disposition

Date: 2026-09-16

Status: `INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`

## Disposition

The paid L14 Target/Hostile execution was intentionally stopped after its
compact scientific and operational records were preserved and verified. It
did not produce an authenticated Target result, an authenticated Hostile
result, a merged Phase-2 decision, a Phase-3 result, or a final finite-scout
gate decision. Consequently:

- there is no L14 value to add to the L08/L10/L12 progression table;
- the partial work cannot be interpreted as a pass or rejection of the L14
  physics gate;
- no partial event may be substituted for a completed branch result; and
- the L14 run is not a premise of the L4--L12 extendible record-envelope
  theorem.

The former status `PENDING_AUTHENTICATED_RESULT` is therefore closed as
`INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`, not left as an indefinitely
running or pending computation.

## Preserved branch boundary

The preservation record contains completed rough-stage event files only:

| branch lineage | completed rough events | final scientific result |
|:---|:---|:---|
| Target V003R6 clean restart | 1--13 of 14 | none |
| Hostile V003R5, untouched by the Target restart | 1--12 of 14 | none |
| superseded Target V003R5 attempt | 1--9 of 14 | none; execution stopped on strict JSON serialization of a non-finite diagnostic |

Target V003R5's serializer refusal was a software/numerical-diagnostic
failure, not an AWS hardware failure and not an L14 physics result. Target
V003R6 repaired that capacity/serialization path without migrating the old
checkpoint. Target V003R6 and Hostile V003R5 remained scientifically
right-censored when the paid run was stopped.

## Custody

Two compact preservation archives were copied from AWS and independently
verified against per-file manifests before the compute, volumes, buckets, and
stack were removed:

| archive | SHA-256 | manifest-verified files |
|:---|:---|---:|
| Target preservation | `02cdbd0ce0e6a66bb3a5440d05cb9b9f3686906d491ed5c5857fc5f64d51af22` | 1,109 |
| Hostile preservation | `f9042afa8e4d901a0533900129b983ff140dbb2306c3738c0eab9c28c0615d46` | 863 |

The full private custody bundle, AWS teardown receipts, and raw preservation
archives are intentionally outside this Git worktree. They are not candidates
for the public repository or the bounded Zenodo proof capsule. A future L14
experiment must start from an explicitly authorized protocol and may cite
these hashes as attempt history; it may not promote the partial event files as
completed evidence.

## Scientific consequence

Closing this run does not alter any L4--L12 result. In particular, it does not
alter:

- the exact 1156/1156 L12 numerical adjudication;
- the strict common-lineage progression through L12;
- the exact and hostile-audited L4--L12 extendible record-envelope theorem;
- the authenticated majority mass
  `0.56956498393327842 > 0.50` at L12; or
- the adopted `ARGER-GATE-1` finite `z=1` classification, whose third input
  is the independently authenticated positive finite visibility of all 13
  selected sectors.

The incomplete L14 run neither adds to nor weakens that established bounded
result. L14 remains optional future finite-size evidence, not a missing proof
premise.
