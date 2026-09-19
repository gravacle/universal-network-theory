# Stage 3 fixed data-lineage replay — DEVELOPMENT only

This packet implements the bounded recovery from the failed first L12 launch.
It removes the rejected runtime historical-interface adapter from the route.
No existing physics executable, solver, tolerance, or target Stage-2 record is
changed.

The exact missing obligation is transitive: the current A18 L10 cross-gate
must bind the same target freeze, independent audit, consumer, L10 gate, and
L12 cache manifest named by the hostile cache-build authorization.  The first
launch proved that the old A18 comparison did not enforce that equality.

The coordinator performs only the following fixed successor transaction:

1. authenticate and owner-once preserve the seven stale hostile A17 roots,
   current A18, and twelve failed-launch records;
2. replace the four retired target hashes in the hostile build gate with the
   current Stage-2-certified hashes;
3. rebuild L4, L6, L8, L10, and L12 cache records through the unchanged frozen
   hostile builder;
4. perform the bounded L12 cache semantic audit;
5. authorize and run the unchanged hostile L10 consumer, then reconstruct its
   27-check gate;
6. reconstruct the existing 65-check A18 and enforce the new exact transitive
   target-interface equality; and
7. stop before L12 launch, leaving the unchanged launcher able to republish
   its canonical V001 controls.

Non-mutating commands:

```sh
python3 -B stage3_data_lineage_replay.py plan
python3 -B stage3_data_lineage_replay.py dry-run
python3 -B test_stage3_data_lineage_replay.py
```

The sole live mode requires the literal authorization printed by plan mode.
It is not authorized merely because this DEVELOPMENT packet exists.  No live
mode was run while preparing or testing this packet.

Claim boundary: this is a finite data-lineage replay and L10 recertification
mechanism only.  It does not contain an L12 result, spectrum, continuum result,
or gravity claim.
