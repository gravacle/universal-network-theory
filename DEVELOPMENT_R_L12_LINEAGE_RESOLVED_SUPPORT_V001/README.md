# L12 lineage-resolved q5 support reconstruction V001

This packet is an independent, read-only diagnostic. It reconstructs the
event-6-through-event-12 q5 residence mass of complete record histories from
the hash-authenticated Target and Hostile prefix-11 sharp states. It does not
modify or supersede Stage-6R2, the record-flow topology sidecar, or Stage-6R3.

The strict support measure counts a history only when its fifth acceptance
(q4 to q5) and sixth acceptance (q5 to q6) both occur in events 6 through 12.
The support is measured separately at each native event and averaged in the
same way as the Stage-5 `pbar_q` sector mass. A complete three-way q5
decomposition and terminal sector reconstruction are mandatory fail-closed
audit checks.

Run focused tests:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_l12_lineage_resolved_support.py
```

Run the authenticated reconstruction exactly once:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 l12_lineage_resolved_support.py
```

The report is created with exclusive-create semantics and mode `0444`.

Verify the sealed report and the preserved predecessor hashes:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_lineage_resolved_support.py
```
