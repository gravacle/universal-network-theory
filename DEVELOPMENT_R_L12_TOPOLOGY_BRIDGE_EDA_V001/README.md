# Strict L12 topology-bridge analysis

`l12_topology_bridge.py` is a read-only analyzer for the proposed
q=4 -> q=5 -> q=6 bridge. It accepts only explicit atom-ID-to-atom-ID
relations stored in JSON under recognized edge/adjacency fields. It never
constructs edges from sector order, density intervals, list position, or atom
identifier order.

The default inputs and expected SHA-256 digests are pinned in the script:

- Stage 6R2 adjudication
- Stage 5 authenticated sector manifest
- Target L12 V003R1 history
- Hostile L12 V003R1 history
- Target L12 cache manifest, including its physical `edge_layout`
- Hostile L12 cache manifest, including its independent `edge_layout`

Run it from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 l12_topology_bridge.py
```

An additional topology JSON is accepted only with its expected digest:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 l12_topology_bridge.py \
  --topology /absolute/path/to/topology.json \
  --topology-sha256 EXPECTED_64_HEX_DIGEST
```

The geometry window and mass threshold remain adjustable with `--lower`,
`--upper`, and `--threshold`. `--geometry-source` selects `consensus`,
`target`, or `blind` geometry.

## Current L12 result

The six pinned inputs authenticate, and 24 atom records are discovered. The
Target and Hostile histories each contain `$.edges = 36`, but that value is a
scalar edge count rather than an atom-level edge array. Their cache manifests
do contain explicit 36-edge `$.edge_layout` arrays, but those endpoints are
physical vertex integers 0 through 23. The Stage-5 A000--A023 objects are
independently generated rational density intervals, so the integer endpoints
cannot be renamed to atom IDs. No `edges`, `edge_layout`, `neighbors`,
`links`, `adjacencies`, `connections`, `relations`, or `orbit_relations`
array/mapping yields a known atom-ID pair.

The analyzer therefore returns exit status 20 and prints:

```text
AUTHENTICATION_FAILURE: No explicit atom-level topology found in schema.
```

It deliberately stops before endpoint traversal and before summing q=4,
q=5, and q=6 sector mass. Consequently, the existing L12 JSON does not prove
or disprove the proposed bridge; it lacks the atom-level topology needed to
test it. `STRICT_TOPOLOGY_REPORT_V005.json` is the immutable machine-readable
record of this result.

This failure is about missing topology, not missing geometry. A separate
read-only inspection of the already-adjudicated values confirms geometry-pass
atoms A011 (q=4) and A016 (q=6). The existing sector ledger also has a
conditional q=4+q=5+q=6 sum of 0.5695649839332784. That sum is deliberately
not emitted as an authenticated macroscopic block because no explicit q=5
bridge path is present in the supplied JSON.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_l12_topology_bridge.py
```

The gateway suite covers absent topology, invalid endpoints, a forbidden
q=4-to-q=6 bypass, disconnected q=5 subgraphs, a direct shared q=5 node, a
multi-node q=5 path, and an explicit adjacency mapping.
