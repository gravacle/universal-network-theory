# Spherical-shadow stdout publisher review V001

2026-09-29. Independent complete source read, no import or execution.

Reviewed `publish_spherical_shadow_v001.py`, SHA256
`a4af36e5f0bfbaf7a252aca004b360e8a01c0cc727bc271ee271466cc56f728a`.
The pinned scientific source is `spherical_dust_shadow_v001.py`, SHA256
`ba928eafe25c870ea872027389ecff1a45425f6f3ea613562e65d67bd9c853ed`.

Accepted: exactly two fixed jobs (freeze/run); project, source and path guards
precede execution; existing/dangling-link destinations are refused; the
reviewed exclusive atomic publisher is pinned; captured stdout survives a
producer exception, interruption, invalid JSON or receipt-hash mismatch in
a separate immutable attempt artifact. Successful wrappers authenticate the
payload and exact freeze bytes. Nonempty scientific failures return status 2
without erasing the produced result. Publication rechecks the final bytes.

The narrow change from the reviewed generic publisher is the fixed spherical
job table and failure-exit policy, not any equation, numerical tolerance,
state or source work. This review certifies the receipt-custody mechanism,
not physical qualification of the finite-pressure release. No modification
to the publisher or its frozen scientific producer was requested or made.
