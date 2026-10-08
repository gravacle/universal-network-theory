# Serialization-only repair of the local-pole diagnostic

2026-10-05 UTC. The V001 numerical calculation exited with a NumPy boolean
JSON serialization TypeError. Its partial JSON and source are preserved.
The partial file's initial status text is NOT a qualified durable result.

V001 source SHA256:
6a6cf2d38c3c9f59dc82a1329082348705480b65273676cc41311f2b487dcef6

Partial JSON SHA256:
aa2c47d787de77e3673d60da4856305725ff92b60e4b86282ea25ea954bd110d

The separate V002 wrapper authenticates these bytes and imports the inspected
V001 module (whose execution is guarded by __main__). It changes only output
destination and JSON conversion of NumPy scalars to their Python equivalents.
No equations, inputs, numerical criteria or physical conclusions are changed.
The interrupted subsecond diagnostic is rerun once, not previous science.
Its new complete result contains this repair provenance and source hash.
