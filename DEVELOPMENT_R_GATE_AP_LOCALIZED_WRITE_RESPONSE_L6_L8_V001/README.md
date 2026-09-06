# Direct localized-write response at L6 and L8 V001

This packet executes the authenticated `W_R=1/2`, `Phi=pi/4` write on one
baseline-blank even carrier site, then compares the source-off connected
history with the sealed unperturbed baseline. L6 and L8 use the complete
`2^(2L)` component space and serve as both response records and the direct
reference for later marked-source compression.

Run each size with warnings promoted to errors:

```sh
PYTHONWARNINGS=error python3 -B compute_direct_response.py --length 6
PYTHONWARNINGS=error python3 -B compute_direct_response.py --length 8
```

Each run must pass `24/24`. Runtime and maximum RSS are process observations,
not complexity laws.

After both canonical rows exist, run:

```sh
PYTHONWARNINGS=error python3 -B compile_results.py
```

The compilation must pass `16/16`.

Complete signed site and edge records are retained. Radial bins use shortest
path on the finite support graph only. No physical grid/distance, locality or
scaling law, boundary reflection, continuum, Ward structure, phase, graviton,
or gravity is claimed.
