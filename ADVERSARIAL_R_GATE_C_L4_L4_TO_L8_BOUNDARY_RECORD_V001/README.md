# Adversarial L4 + L4 to L8 equal-time boundary-record screen

This packet independently attacks the lower-order equal-time record in the
frozen composition protocol. It does not modify the target, audit, ledger, or
authority documents and does not execute L6 or L12.

Run from the repository root:

```sh
PYTHONWARNINGS=error python3 -B \
  ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/adversarial_equal_time_record.py
```

The script reconstructs the six-owner surgery, proves the exact rank and
nullity of the candidate equal-time record, constructs two positive trace-one
collision roots, and evolves their one-particle joined outputs under the
declared L8 owner action.

The collision roots are lawful states in the complete finite block algebra.
The packet does not claim that the conditional uniform source selects them.
