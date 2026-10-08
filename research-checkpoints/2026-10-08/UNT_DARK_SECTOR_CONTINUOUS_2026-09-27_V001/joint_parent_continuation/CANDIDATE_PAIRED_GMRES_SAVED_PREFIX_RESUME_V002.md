HELD paired GMRES resume V002 adds an optional containing iteration checkpoint.
Exact parent V001 fa1cf19a/544319d9 remains protected; all eight support definitions and all numerical statements are unchanged.
The ninth signature adds iteration_checkpoint=None. Its only new call follows a completed next-basis append, after original candidate decisions and before the next forward action.
The callback receives iteration index, the completed new basis pair and copies of small H/QR/Givens/rotated-RHS/history/Arnoldi arrays plus authoritative-prefix/proxy-suffix scope. It owns publication, not numerical updates.
Callback omission retains V001 behavior. Callback failure preserves a completed state and refuses before the next action; containing exception custody remains necessary.
Original total cap80, one cycle/no restart, paired MGS/QR associations, compression, 20/40/80 candidates and all six original1e-10 gates are unchanged.
Candidate progress and final state handle admitted/breakdown/cap branches where no next basis is appended. A final cap80 state is terminal and cannot be relabeled a resumable j80 prefix.
Prefix and sampled coefficient proof tuples remain None/HELD. The latter supplements original16047 coefficient provenance; it does not replace it.
No action, factor, solver or numerical function was executed by the author.
