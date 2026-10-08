# Trace–coordination saved acceptance check V002

PASS: 69799 assertions; all20 datasets/1024 paired replicas.

V001 failed at the float nonlinear covariance reconstruction and remains preserved. V002 uses Decimal50 on the exact binary parent-input values for every nonlinear field/covariance and residual oracle. The original3e-11 criterion, primitive controls, paired errors and all inverse/mixing refusals are unchanged. This is an authored acceptance check, peer-reviewed before root execution.

Maximum normalized residual: 2.61216595259e-11. No H, sampler, RNG or producer import/replay.
