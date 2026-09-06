# Post-output reporting repair

The first authorized L10/L12 run resolved and classified successfully, but a
hostile telemetry read found that `compute_phase_screen.py` computed each
checkpoint's Ritz values without serializing the requested lowest five.  This
is a protocol-compliance failure in reporting, not in the sparse action,
Krylov recurrence, response weights, or classifier.

Pre-repair custody:

```text
solver                    1baa5f55ccbcf36894978345879d116edc9faec88bd64f0b8786226cf0872982
target L10 q5 raw         23b5250ffd9a15668afab4e61eb72baddae85b55feafacbb8cf2a05635ef8c32
target L12 q6 raw         e2e0e9c3c18bf4352e58653dd6d0637412a60fa683997de52e12b964470581f5
aggregate result          0dea9b4625fa53ed7dd6e24b47d9c767eb828e3f9878c70b41422424cbc97ece
blind L10 q5 raw          3989879720404d6bd5cb1238788f4f31eb8e5b19d09c61ce604b26fa3ae5345b
blind L12 q6 raw          dff0bc6f9c5f4eeacfd7f56485dd0c27812d226dc866f4225d9803ec37a5d8a5
classification            CENTERLINE_Z1_REJECTED_L4_L12
```

The permitted repair adds only `lowest_five_ritz_values` fields to the ground
and response checkpoint dictionaries.  Every previously defined observable,
residual, guard, and fitted decision must reproduce within the frozen
target/blind tolerances.  Any change in classification fails closed.

Post-repair replay custody:

```text
solver                    e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7
target L10 q5 raw         c8ce97913795f46b493b1aab328d93cc61eeeefd167407c283e4137847e2dcb9
target L12 q6 raw         0e04d2286b3c1669078dc5cd8ff68180c7a989b8741c9f3da772605ca49dde49
aggregate result          dcaefd6259fe653676cd6da181f4ee341c2d6e14409b6cc5146a9cdc9c5d056a
classification            CENTERLINE_Z1_REJECTED_L4_L12
```

All target checkpoints now contain an ordered list of up to five Ritz values;
each final target ground/response checkpoint contains exactly five.  The
maximum target/blind relative disagreement in ground energy, `Delta_act`,
`chi_tau`, or `R_low` remains `6.972e-15`.  All controls and guards remain
resolved.  Independent hostile promotion is still required.
