# Generated-receipt publisher first use

2026-09-29. Publisher SHA256
f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8.
Independent preflight accepted exact case-index binding, source/freeze custody,
atomic no-overwrite publication and failure preservation. It does not change
the frozen numerical producers or their tolerances.

Root invoked `hyrec 8`: exit1, FileExistsError at the pre-execution guard,
"Case already has a receipt; no producer executed". The existing case was
not replaced. This intentional refusal is not a scientific failure.

Root then invoked `hyrec 13`: exit0, COMPLETE_CONDITIONAL_ATOMIC_CASE,
no failures, 15.3075693s controller time. Generated13556780-byte receipt
HYREC_FULL_CASE_013_V002.json SHA256
ae2fd5ae06d6e396c41613acccb4a97a525436fbb60a5c8e22a97a0b7d3fc593.
An independent system shasum read confirmed the full digest after publication.
Its sound interval remains physically wider than the precision target; no
gate was relaxed. Generated scientific receipts now go directly to durable
case files; source/document edits still use apply_patch.
