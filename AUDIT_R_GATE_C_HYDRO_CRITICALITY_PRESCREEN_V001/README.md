# Independent hostile criticality pre-screen

Run the frozen L4/L6/L8 translation-block reconstruction:

```text
PYTHONWARNINGS=error python3 -B AUDIT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/independent_prescreen.py
```

Then run the hash-pinned target/independent comparison:

```text
PYTHONWARNINGS=error python3 -B AUDIT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/verify_audit.py
```

The expected hostile verdict is
`PASS_HOSTILE_NO_CANDIDATE_L4_L8__STOP_NO_L10_L12`, with `256/256` checks.
The independent executable rejects any requested size outside L4/L6/L8.
