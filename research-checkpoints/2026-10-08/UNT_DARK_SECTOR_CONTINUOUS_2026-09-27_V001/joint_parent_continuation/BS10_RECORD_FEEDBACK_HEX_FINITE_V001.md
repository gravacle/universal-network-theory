# Held occupied-record hexagon at finite native coupling V001

Prospective protocol, 2026-10-05 UTC. PREPARED; no worker launched. Own only this new `.md`, `bs10_record_feedback_hex_finite_v001.py`, `_RESULT.json`, `_RESULT.md`, `_RECEIPT.json`, and `bs10_record_feedback_hex_finite_v001_checkpoints/`. Root alone launches once after root and both independent source preflights, frozen hashes/output absence and fresh live-ownership verification. No replay, repair/rerun, installation, remote job or scheduler.

## Recovery and scientific scope

A narrow read-only search found no equivalent completed/running q1/Nc0 full64/Q62 finite six-link h=1/5 gate. Resident FK finite matrix identities concern the compressed leading qblank ring; GL6AN/AO/AR concern formal or projected models. The newly sealed9222 hex gate supplies leading coefficients and13471 diagonal gate supplies homogeneous formal coefficients, not this finite-coupling result. Old BS11 full64 Nc3 h=.08,.10,.14 is a different model. No old source is imported or executed. The preparation lane's direct ps read was sandbox-denied; root independently found no science worker at15:06 UTC and owns the launch check.

Fix the actual six-cycle incidence bits n_i, i=0,...,5. At each vertex there is exactly one occupied and one blank outside eligible link; outside flips are held off. Ud=1,d*=2,ER=1,lambda_R=1/2,Nc=0 and conserved uniform q1. Copy vanishes in Nc0; no writer/port/bath is introduced. Retain ALL64 internal bit words, with

    D(n)=sum_v[(n_(v-1)+n_v-1)^2+(1-n_(v-1)-n_v)/2],
    H(h)_(n,n)=D(n), H(h)_(n,n xor 2^i)=-h, h=1/5.     (1)

This subtracts only the shared fixed exterior-collar identity. Exterior/support absolute energy and work remain owned; negative reference-relative levels are not negative absolute total energy claims. Each D is an integer. A second construction uses the gap law relative to alternating n=21: delta_v=(n_(v-1)+n_v-1), Delta=sum(delta^2-delta/2). P is the two alternating words21,42; Q contains the other62. At h=0,D|Q>=1 and PHP=0. The full64 matrix is not a Q truncation; Q is used only as its exact principal compression. This is a held-cell diagnostic, not an autonomous/bulk dressed phase, thermodynamic remainder, record-writing/matter pole, physical clock/ruler, gravity or cosmic history result.

## Formal controls, kept separate

The actual held-cell common diagonal is formally

    E_diag=-4h^2+(4/9)h^4-(80/9)h^6,
    J6=(2504/81)h^6=2504/1265625 at h=1/5.             (2)

Both reviewers independently confirmed (2) before outcomes. The new worker also independently confirms its common diagonal by an exact Q-only intermediate-normalized coefficient recurrence through order6 and by assembling the SEALED linked data:3 addition singles+3 removal singles,6 mixed adjacent pairs,3 ARA paths+3 RAR paths. Reference P coefficients are fixed to the chosen basis vector; the opposite P state first appears offdiagonally at6 and does not enter the lower folds. q1 global homogeneous c6 is not substituted for this held-cell diagonal. The leading offdiagonal coefficient is read from the sealed all-record-word hex result; no720 path replay occurs.

No expectation that the formal J or midpoint agrees to a chosen percentage is an acceptance gate. Save outward intervals for the finite half-splitting and midpoint, the signed half-splitting difference and ratio to (2), and the signed midpoint difference to (2), whichever outcome occurs. No midpoint ratio is promised. No post-outcome coupling retune or alternate reference.

## Exact certificate with numerical seeds only

NumPy `eigh` runs once on the full64 matrix and once on Q62 solely to supply candidate seeds for E0,E1 and lambda_min(Q). No rounded eigenvalue is a certificate, and no eigenvector is used for a physical residue. Exact integer matrix construction independently retains (1). At rational shift x, multiply H-xI by a positive common denominator to obtain an integer symmetric matrix.

Use fraction-free symmetric Bareiss elimination with NO pivot/row swaps. Record each exact leading principal minor. Check every division remainder zero. If any leading minor is zero, reject that candidate before using the zero pivot/divisor; save the zero-minor event and try only the frozen next rational candidate. For nonzero minors, the negative inertia is the sign-change count in `1,D1,...,Dn`; this is Jacobi's signature theorem. Positive scaling preserves inertia. A singular final determinant is also rejected.

Deterministic rational bracket policy, frozen independently of outcomes:

1. Set denominator S=10^12 and center `floor(seed*S)/S`. For attempts j=0,...,23 use radius2^j/S. Candidate endpoint offsets are exactly0,+1,-1,+2,-2 divided by17S, in that order. Lower candidates start at center-radius; upper at center+radius. At each side take the first nonzero-minor candidate; if its inertia count does not have the required value, retain the attempt and expand to the next j. A successful pair has inertia k at the lower endpoint and k+1 at the upper for k=0,1 (fullH) and k=0 (Q). If no bracket succeeds within24 attempts, preserve all attempted data and stop unresolved.
2. Target width is1/10^11. If the obtained bracket is wider, perform at most32 refinement steps. At each step try interior fractions of the current interval1/2,1/3,2/3,2/5,3/5 in that order until a nonzero-minor candidate is obtained. Counts<=k update the lower endpoint; counts>=k+1 update the upper. If every candidate has a zero minor or target width is not reached, preserve unresolved and stop. No new ordering or unlimited refinement.
3. Every exact inertia result/candidate attempt is fsynced to its own checkpoint and journal event before further work. The final brackets also seal their exact endpoint-minor/inertia evidence. Missing/zero/nonzero-minor outcomes remain distinct; no skipped candidate is silently treated as a certificate.

The integer Bareiss algorithm is independently checked against direct permutation determinants of all leading minors of frozen symmetric matrices: [[2,1],[1,-1]], [[0,1],[1,2]], [[2,1,0],[1,3,1],[0,1,-1]]. The zero-leading-minor case must be rejected even though its full determinant is nonzero. Matrix/control determinants are tiny exact arithmetic, not old scientific producers. Exact rational endpoints are authoritative; directed Decimal20 lower/upper displays use ROUND_FLOOR/CEILING.

## What the certified endpoint earns

If exact brackets give E0<E1<0 and Q floor mu_L>0, then fullH has exactly two negative levels: Q>0 and the zero-energy Schur block `-W Q^-1 W†` is negative definite because

    WW†=6h^2 P.                                      (3)

The third level obeys lambda3(H)>=lambda_min(Q)>=mu_L by principal interlacing. Q(h) is affine between Q(0)>=I and the certified Q(1/5)>=mu_L I. Thus on0<h<=1/5 it stays bounded below by `min(1,mu_L)>0`, and (3) keeps exactly two negative levels isolated from the positive sector. The pair is continuously matched to P as h->0, not a certified many-cell ice phase. Source-free negative levels and their split are native reference-relative held-cell outcomes, with the fixed collar energy retained separately.

For a normalized eigenstate with certified E in[L_E,U_E], block elimination gives

    ||Qpsi|| <= sqrt(6h^2)/(mu_L-U_E) ||Ppsi||,
    Pweight >= (mu_L-U_E)^2 / [(mu_L-U_E)^2+6h^2].      (4)

Report this bound for both low levels and a common pair bound. It is bare alternating-word projection weight, not a generic physical matter residue. No >1/2 claim unless the exact lower bound is >1/2; a lower value remains a valid saved bound.

Finite half-splitting and common midpoint intervals are

    Jfinite in[(L1-U0)/2,(U1-L0)/2],
    Mfinite in[(L0+L1)/2,(U0+U1)/2].                   (5)

If mu_L or the low-pair conditions fail, retain all exact data and report the failure without rescaling h or substituting formal coefficients. Such failure limits THIS held candidate, not all native models.

## Complete homogeneous source

Only a uniform full-action source L is included: H_L=L H, including all gaps, internal flips and the fixed collar identity. In the reference-relative representation the eigenvalue intervals, midpoint, split and Q bound all scale by positive L; direct second source contact is zero. Exact matrix entries are checked at L=1/2 and2. There is no nonuniform node/edge source partition, no record-only source, and no source-dependent re-zeroing. The physical collar absolute energy would scale with the same L and must be restored for an inclusive total-work claim.

## Frozen inputs and custody

Pin the10 unchanged inputs of the13471 diagonal packet, plus its source/protocol/result/receipt. The source's explicit INPUTS dictionary supplies each exact path/hash; these14 pairs are also saved in the exclusive manifest and verified before and after. Root's new complete-sixth/finite companion is contextual, not a numerical input. Additional anchors:

| Relative filename in joint_parent_continuation | SHA256 |
|---|---|
| bs10_record_feedback_diagonal_sixth_v001.py | b4ec2a9dede18d6a0d2e286da7a5a1ea35a73f3f60bcd5d89aac43f06407e89f |
| BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001.md | b95c3f22a0693985ded173d1a0986bf02a92938b723b8ff7cd8e3af460621911 |
| BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001_RESULT.json | 386cad65ddd80cc01ffd5c49ac9b56827c6fd7c25450772f630c5412e7f51c11 |
| BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001_RECEIPT.json | 4c49ad2737a5b818d593d1b27c5eb56114647c4d2b6d407289cec649dfe181ba |

Parent and peer reviews already authenticate the sealed13471 packet. This worker additionally checks its raw/canonical receipt, source/protocol and input-map equality; it imports no ancestor. NumPy is available in the existing bundled runtime; no install. Supply one-BLAS-thread environment before import. The worker refuses existing result/report/receipt/checkpoint paths, creates an exclusive manifest/PID and stage journal, fsyncs structures/formal/seeds/every inertia/each final bracket before advancing, and preserves partial/ERROR output. No automatic resume/rerun or replacement coordination is created.

Arithmetic/control gates: independent physical-bit/gap diagonals; symmetric64 and62 dimensions; two zero diagonal reference words only; Q diagonal floor1; exact P/Q separation and WW†; Bareiss/direct-determinant controls and zero handling; full source scaling; recovered formal controls; exact endpoint inertia counts and finite attempts; negative isolated pair/positiveQ only if certified; consistent interval and projection formulas; all input/source/protocol bytes unchanged; complete staged seals and deterministic report keys. Signed finite-vs-formal differences are scientific outcomes, not accuracy acceptance gates. Save passed/failed counts, elapsed time, routine RSS, raw/canonical result, report, receipt and journal-prefix hashes. Parent is the sole launch owner.
