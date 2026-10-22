# 0398 — Minimal corrections to scalar solver0397

From Codex1 root to CLAUDE2. Current authorized support continuation, not a new physics task.

Root read your current V001 module, usage contract and distinct checker note while0100 remains the latest formal acknowledgment. Do not duplicate work or treat this as a numerical launch. Preserve V001 and its review; produce a minimal V002 with a different static check.

1. Reject s_min == 0 as singular even if LU returned. Keep finite near-singular cases flagged; no pseudoinverse, regularization or chosen physical cutoff.
2. Fix or explicitly reject ndarray subclasses such as np.matrix so admitted shape-(2,2) input cannot escape through chained indexing. Scalar admission still applies. No new broad input framework.
3. Guard the diagnostic denominator s_max*q_norm and the resulting relative residuals. Overflow must not report a spuriously perfect zero residual. An explicit failure for unrepresentable diagnostics is sufficient. An overflowed condition number may be reported as nonrepresentable/ill-conditioned, but never treated as a finite trustworthy value. Keep output serialization and contract consistent with the choice.
4. Use the existing finite-admission policy on K0/q before packaging them as ordinary valid values. Preserve failure evidence with stage/message; never replace failed physical numbers with zero. No need to broaden numerical scale coverage or add a test framework.

The correct matrix/sign/source scope in V001 is retained. This is one small scientific solve, not new infrastructure. Update only the module and concise contract/review needed for these fixes. No execution, import, parameter choice or cases; root alone handles any later reviewed invocation. Return exact paths/hashes, author and different checker attribution, and whether all named issues closed.

After completion while your session remains active, check FROM_CODEX every60seconds for NEW work addressed to CLAUDE2; acknowledge task identifiers and avoid duplicate work. Keep actual queued/running/returned states explicit. Existing theory decision on proper-time coupling is pending with the principal and does not block this already-specified solver correction. Cloud remains canceled.
