# Targeted L14 geometry scout V001

This packet contains the orchestration and fail-closed early-stop gate for a
two-phase L14 scout. It does **not** launch a numerical L14 solver.

## Mass-ledger feasibility result

The proposed sector funnel works for the independent response-spectrum rows,
but it does not by itself prune the exact history mass calculation. In the
frozen prefix representation, admission into `q` depends on the old `q` and
`q-1` shards. Therefore:

- exact Phase-1 mass for `q=4..7` requires evolving `q=0..7`; its L14
  admission peak lower bound is `67,119,641,280` bytes (`62.510 GiB`), above
  the frozen `20 GiB` scratch guard;
- exact `q=8,9` mass requires `q=0..9`; its peak lower bound is
  `259,065,155,040` bytes (`241.273 GiB`);
- the full exact preterminal representation has a `345.810 GiB` admission
  peak lower bound.

These are shape identities, not runtime extrapolations. They are recorded in
`MASS_FEASIBILITY.json` by `l14_mass_feasibility.py`.

A tempting covariance/Gaussian reduction was also implemented and tested by
`l14_mass_ledger.py`. Its two internal constructions agree, but it fails the
preserved L4--L12 many-body sector ledgers (maximum discrepancy
`0.13113501157205804`). The frozen graph engine is sign-free hard-core
hopping, so the free-fermion covariance shortcut is not the same physics.
`MASS_REDUCTION_AUDIT.json` therefore marks that reduction rejected and does
not expose its L14 candidate values as sector masses.

Accordingly, the execution harness remains intentionally launch-inert until
one of these is explicitly adopted and validated:

1. an exact compact hard-core-history representation that reproduces the
   preserved L4--L12 ledgers, or
2. a separately labelled exploratory approximation with certified mass-error
   intervals and a revised gate that propagates those intervals.

## Density correction

The literal charge label is not invariant as `L` changes. The L12 `q=5`
sector is centered at `5/24` and has the exact density cell

```text
[3/16, 11/48).
```

At L14, the `q=5/q=6` boundary is `11/56`, which splits that cell. Therefore
L14 `q=5` alone mostly revisits the lower shoulder. The harness logs the
requested literal-q5 status, but continuation additionally requires:

1. a consensus geometry hit in L14 `q=6`, and
2. one exactly contiguous consensus-passing atom block covering the complete
   former L12-q5 density cell `[3/16, 11/48)`.

This is the physical bridge test. A favorable atom disconnected from either
side does not count as a formed bridge.

## Phase sequence

1. Phase 1 requests only spectrum/geometry sectors `q=4,5,6,7`. Its result
   must also provide an independently authenticated probability-mass ledger
   for `q=4..9`. Measuring a sector's scalar mass is not authorization to
   execute its spectrum solver. The current exact prefix engine cannot yet
   produce that ledger within its frozen resource guard, as documented above.
2. The harness independently applies inclusive `z,y in [0.90,1.10]` to both
   Target and Blind results. It sums each passing `q` once.
3. It halts if literal q5 is sterile, the physical q6 core is sterile, the
   density bridge is not contiguous, or

   ```text
   phase1_passing_mass + mass(q8) + mass(q9) < 0.50.
   ```

   The last expression is an optimistic mathematical upper bound: it assumes
   every unopened tail sector will pass.
4. Only a passing gate creates the Phase-3 request for `q=8,9`.

Numerical nonconvergence, failed original predicates, failed Target/Blind
authentication, or absence of an authenticated L14 mass ledger are
obstructions—not scientific rejections. They cause a refusal before the gate
is evaluated.

## Solver adapter contract

The adapter is invoked without a shell:

```text
python3 -B SOLVER.py --request REQUEST.json --output RESULT.json
```

It must publish the result path owner-once. The result schema is:

```json
{
  "schema": "L14_TARGETED_SCOUT_SOLVER_RESULT_V001",
  "length": 14,
  "phase": "bridge",
  "computed_sectors": [4, 5, 6, 7],
  "sector_masses": {
    "4": 0.0,
    "5": 0.0,
    "6": 0.0,
    "7": 0.0,
    "8": 0.0,
    "9": 0.0
  },
  "validation": {
    "all_original_numerical_predicates_pass": true,
    "target_blind_authenticated": true
  },
  "atoms": [
    {
      "atom_id": "L14A000",
      "q": 5,
      "density_interval": [[3, 16], [11, 56]],
      "target": {"resolved": true, "z": 1.0, "y": 1.0},
      "blind": {"resolved": true, "z": 1.0, "y": 1.0}
    }
  ]
}
```

For Phase 3, `phase` is `conditional_tail`, `computed_sectors` is `[8,9]`,
and its mass ledger must include at least q8 and q9. Those masses must exactly
match the Phase-1 ledger.

## Commands

Safe preflight (does not allocate a workspace or launch anything):

```sh
python3 -B l14_scout_harness.py \
  --workspace /absolute/fresh/L14_SCOUT_V001 \
  --preflight
```

Production form, once an authenticated sector-selective adapter exists:

```sh
python3 -B l14_scout_harness.py \
  --workspace /absolute/fresh/L14_SCOUT_V001 \
  --solver /absolute/path/to/l14_sector_solver.py
```

Evaluate an existing Phase-1 artifact without launching a solver:

```sh
python3 -B l14_scout_harness.py \
  --workspace /absolute/fresh/L14_GATE_REPLAY_V001 \
  --phase1-result /absolute/path/to/PHASE1_RESULT.json
```

Exit codes are `0` for a completed threshold hit, `10` for Phase 3 authorized
but not executed, `20` for an early scientific halt, `21` for a completed
scout below threshold, and `2` for a contract/numerical obstruction.

## Current integration boundary

The existing L12 process-parallel history engine has no authenticated
sector-selective L14 adapter. Its prefix history is coupled and cannot be made
sector-selective merely by filtering the terminal output. Connecting that
engine directly would falsely claim compute pruning. The harness therefore
refuses to invent an adapter and remains launch-inert until a genuine L14
sector solver publishes the contract above.
