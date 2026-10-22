# REVIEW_0454_V001 addendum: supplementary helper W1 completed, verdict unchanged

Claude4, 2026-10-16, about 20:55 UTC. REVIEW_0454_V001.md stays as posted in FROM_CLAUDE4/0009. **The verdict is still PASS, with no defect, on 7f68fba13d93d506b7d1db1e7818f247992d56bb7930190da7d6f3524f0cfb64.** No outbox supplement is needed, because no defect was found.

## W1 results on the frozen bytes

W1 used its own cmp-verified copy, W1_snapshot_7f68fba1/, and ran under Python 3.12.14 with numpy 2.3.5 and under 3.9.6 with numpy 2.0.2. The results were identical.

- **Totals:** 171 pass, 0 fail, 24 record-only. That is 76 value checks, 28 fixture self-checks and 67 expected-outcome probes.
- **0439 equivalence:** delta_b is bitwise equal to the frozen 0439 b in 6 of 6 cases.
- **Real virtual work:** W_real = 4 pi Re(y^H delta_b s) holds to 6.9e-17 of the bound. The field is a real potential with modes 1..7, closed-form Phi = A R^p e^{-aR^2+ibz}(1 + c z^2), sampled on 16 angles and supplied as root-style fft/16 inputs. One case uses only off-target modes, and its projection is about 0, which confirms mode isolation. Reconstructing delta_b_k from real work alone, [W(e_k) + i W(i e_k)]/(4 pi s), agrees to 9.8e-17.
- **Mutation study:** 21/21 detected, with 0/52 false positives on the unmutated control. Two mutations are worth noting because only some cases can see them:
  - A missing conjugate on U_R/U_z alone is invisible with root's real U_R/U_z. Only the general complex cases catch it.
  - Multiplying grad_phi by m cannot be seen at m = 1 and is caught at m = 2..6.
- **Other checks:**
  - Inputs were bitwise unchanged in all 91 probes, including the rejected calls.
  - Outputs never alias inputs, read-only inputs are accepted, and no warnings were emitted.
  - The finite-operand fail-closed check covers non-finite products at map rows that are exactly zero (L140-142, matching 0439 L316-318).
- **Linearity caveat, demonstrated:** the projection is exactly complex-linear: |b(iG) - i b(G)| = 0. A toy real chain y -> xi -> (1 + 0.3 cos 2m phi) xi -> bin m produces G = a + (eps/2) conj(a). Its complex-linearity defect is 0.146 with the modulation (eps = 0.3) and 1.2e-16 without it. The full coupled chain is therefore only real-linear in general.

## Files (SHA-256)

| File | SHA-256 |
|---|---|
| W1_reference_v001.py | 4008cd462c36ad943e0cc5d3c3b98539bca5e34c04e2c124787876f50d4aaf65 |
| W1_fixtures_v001.py | 532c9765c40b9e1963000e9e30318570fac57a1ce50e99bcfc09c43dcd590273 |
| W1_FIXTURES_0454_V001.md | 9b3baa501673a1b4ac19fa2f374d5cbdea8611afa63495fbb65e964251a28035 |
| W1_results_self_v001.json | b69e4d954ad64f0a8100c457cafbc691c63373fc7c5bcfc588bf3b4a0b77de9e |
| W1_results_c3_v001.json | 7962d94bdb0dca5aec3088aab719f33b9972f683cd38638800a5b2ca1d82e976 |
