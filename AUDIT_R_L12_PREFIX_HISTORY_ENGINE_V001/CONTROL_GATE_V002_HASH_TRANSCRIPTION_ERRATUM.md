# Control-gate hash-transcription erratum

The first execution of `adjudicate_controls_v002.py` produced a failed gate with
SHA-256 `81894b05f9f04244f3533951030c17f1a087de24f5edebb6bdd6c78d144efa03`.
It passed all 233 numerical, structural, convergence, custody, and resource
checks, but failed the three hostile-output hash checks because the adjudicator
contained incorrectly transcribed completions of the eight-character hashes
reported by the independent implementer.

The failed record is preserved as
`CONTROL_GATE_V002_FAILED_HASH_TRANSCRIPTION.json`.  Before another execution,
only the three expected hostile-output hash constants were corrected to the
locally measured full SHA-256 values.  No engine, control history, tolerance,
observable, numerical result, or other adjudication predicate changed.

Claim boundary: this is a clerical correction.  It does not promote L=10 or
L=12, a spectral result, z=1 scaling, continuum behavior, or gravity.
