# Same-parent collective-cycle continuation V001

2026-10-05 UTC. Prospective protocol only. Root owns launch after full source/protocol reviews and a fresh ownership check. Saving this file authorizes neither execution nor an automatic continuation. The first pilot closed naturally with 22393/22393 arithmetic controls and all four conditions MIXING_UNQUALIFIED. This fixed follow-on recovers all sixteen terminal paths and PCG64 states; it changes the sampler, not the Hamiltonian, graph, temperatures or scientific preparation.

## Sealed parent and exact recovery

All paths below are relative to this joint_parent_continuation directory.

| Parent file | SHA256 |
|---|---|
| local_record_feedback_3d_worldline_pilot_v001.py | 48030f615a9a54a2235fd4619e3084a2f5bfd6c9674a13029b6836081f96c6ef |
| LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001.md | f8f06d205be72bec8ca51e17162814a2caa9b0799ffa5dc0678b0e4c38ec0591 |
| LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001_RESULT.json | dde8be234ce35ede08fa3fb9efe2b0e06b02ef9406f3996d5df703598e6c8827 |
| LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001_RESULT.md | 7ae9c39e89320818b267a4488f9cb74bfa94bb4a34ed884025c055329ce44b42 |
| LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001_RECEIPT.json | 2fb94e9b5c9f22eb9161013024d542b03bf5822eed1736e1ba883aa1e1cf730c |

Parent result canonical SHA256 is c54e61975c230464ebf1a3bad90168195e6fd9fafd1504ef8efa7cf71a31f0b7. Parent checkpoint directory is `local_record_feedback_3d_worldline_pilot_v001_checkpoints/`; its controls.json SHA is 581e5886c8e912258c2ac65e6e1a331bfea8a9bfd256b072e7ca15770f933657 and manifest.json SHA is 2b50e6c7d044380630ee45400d03447f106572fe6e6e5b243f2fce913da7c3ce. Parent journal prefix, excluding its final receipt_complete line, has SHA 0b7cda8c9de8e11cb174149487be0c588930f1b418e1ef99c5f5fde3477c1a20.

Authenticate the parent raw/canonical result, report and receipt, the receipt's source/protocol/three note inputs, manifest/start commit, controls stage, journal prefix and final receipt_complete commit. Require failed=0, passed=check_count=22393, sixteen unique chains and four conditions; retain the parent's unqualified mixing status. Require all 48 prior enumeration cases and their passing control records. Verify the raw-result terminal references agree with the receipt's checkpoint map and actual bundle/metadata SHA values, and that both have matching journal commits. Do not merely trust a filename or a quiet process.

The terminal filenames are exactly `<id>_production256.json` and `<id>_production256.npz` in the parent checkpoint directory:

| id | Terminal metadata SHA256 | Terminal bundle SHA256 |
|---|---|---|
| c0_I01 | ea8c8290a3097b4d5b6dafe33d94f8efb3fb2954ae22af4eac16c9bc861efb6c | b48f6782bb39922efc4118e92d4fa357e48508cc539759dd156660f9ffb5f7a1 |
| c0_I02 | 0a2e428c0d3e77a73e3b9f0f63e9391708a7a8c3fb8130a7155edd5a3c79bc04 | 48dcc4f15f19bff6f7ac8f76e33446abf6b9224e2139c1c613b1a58d7637f9ac |
| c0_B | ca24bb1e44c5230dbb33567362fc51b7f81de306d2ab55a7b21d0e233b432957 | 3777c8716caf865661a7677bc09d6de4ea0a324272ddf5a495c6da856dd3b1c7 |
| c0_R | 4069712095fb8750bc84a9d075c267e03ac767c56f5160e03a28be2608907d3a | e92f4a3d8d7472d313eb6a4f8318df5fb53a6495d1201da5c8e9f82898874c58 |
| c1_I01 | b035c753eaf4b9d09f49d1851196895ac511fc90ad9109daf1abb30384e73b80 | 8eb21af64f4911cb48140a3470d40e8a27330cdeb0b66df43e83d2f3ae3f2a52 |
| c1_I02 | 4b19c992f2c64f3a6b0d6389a9dc75c8394b4618db5708a5b464603e5d462893 | 6178d6dd7a57d4cacf83f79912031f524ebe1abc046a7ef53a6d88fdc345be51 |
| c1_B | a592eea4d0768f5ff6244c6f810dc24e4f277cd61fb21a16caa2884bbcd670e7 | 0c16928eb79188b7aae791814de1539f83cb10f517e8758b21dfa8413a7e9441 |
| c1_R | 1a2d024a5052936593a34276028b74e89790363288303c3f32686b90f47ddac0 | ab1aa359187284ab90db923c265b4504431b1045ba1ffaea97bbd9d5c70af944 |
| c2_I01 | c5de9d592f2a9c58caa24efbb2e86ff2ee45126573782c86b76e49773e240b55 | feb6d5d8d40dbdcba148fd35e0e6f8462edbe6a9266f37a2e65576674cf77f7a |
| c2_I02 | b245d5d3a796469d53bd99ca8a5072a3eec7c301f6b783d39fcb99f28c9754d1 | 94c031d691c856b171ef08819bef8d89bc1353b624a8e125bcb9f71f2d5cbd5d |
| c2_B | 7cf33a6fd4b7531ef4314acfd5a78fd183d6ec03eaa05231c64eff8688ac4330 | 2ce8c91cf09f0e7e217a2b60ecfebbd0b498c619fddad86e393b9d6d26282bcc |
| c2_R | 5e4810aa9d3c07dbcf37109bc89b85793b0f84f12544a1f205de1386e467fdd9 | 7eb0772e0e9eb60ac6880d90557d464eb0e9baf7b812a93dd0e3d00257372bd6 |
| c3_I01 | 5561452b540a5ee733187572577174b62719afd5ee328443013f87f01f0e50f0 | d9a3bd8015be9955fd3d51918e77f77e880a5871efc0c885d06f91d85c26df4e |
| c3_I02 | 566712b072a43080adbd1d3c3e69d104b28baea444014b1b1d508c60d9e249a5 | b4c466612dc1c0dde6e8426e12ee0a3f089cd16dab5c3802561e05bb1c9f69c1 |
| c3_B | 86eeb2dc94c3672b68df9967657070986d6539788a28cf55834e46f42e63a71f | 3b92d56c5c3e85b99ffc2a3393e7fc85e5fa499f87c21f060935a2487e8f7017 |
| c3_R | a1422f26d8ef6cc5413a6b37defec686acad8e94e484e43ecd5091790f29f73e | 7b9189386cefb0c8cf906ce87bd2165fad08d4475e003eb2d8c50178f3d8d2b6 |

Metadata must have completed_burn_sweeps=64, completed_production_sweeps=256, phase=production256 and matching id/configuration/input hashes. Load only this terminal bundle's `bits` with allow_pickle=False; require uint8, binary values and shape (M,27,4). Restore the entire saved PCG64 state, including has_uint32 and uinteger. There are no new initial-word draws, seed resets or skipped parent chains. Verify the recovered array and RNG-state identity before any sweep. Keep the original seed/start as lineage labels, not instructions to reconstruct an initial preparation. Only bits and RNG initialize the new segment; old measurements remain sealed separately.

## Same finite-M law and fixed census

Retain the complete supplied diamond L3 graph, q_record=1, Nc=0, all source L=1 and h=1/5. Cells r are lexicographic Z3^3, ports s=(0,e1,e2,e3); (r,a) joins A_r to B_(r+s_a). There are 54 vertices and 108 eligible links. With delta=d-2,

    D=sum_v [delta_v^2-delta_v/2], H=D-h sum_e X_e,
    W(n)=exp[-epsilon sum_tau D(n_tau)] product_(e,tau) C(n_e,tau,n_e,tau+1),
    C_same=cosh(epsilon h), C_flip=sinh(epsilon h), tau+M=tau.

Keep the full common 54I and longitudinal field. This is not a projected ring action or a physical clock/volume law.

| Condition | beta | epsilon | M | Recovered chains in order |
|---:|---:|---:|---:|---|
| 0 | 4 | 1/16 | 64 | c0_I01,c0_I02,c0_B,c0_R |
| 1 | 4 | 1/32 | 128 | c1_I01,c1_I02,c1_B,c1_R |
| 2 | 8 | 1/16 | 128 | c2_I01,c2_I02,c2_B,c2_R |
| 3 | 8 | 1/32 | 256 | c3_I01,c3_I02,c3_B,c3_R |

One resident path at a time, in this condition/chain order. Each new segment has exactly 64 burn-in and 256 production sweeps, measurement after every complete sweep, sixteen blocks of sixteen production sweeps. Save the segment's initial recovered state, burn64 and production32,64,...,256. Preserve both original completed counters and new segment counters. This is one expressly bounded follow-on, not adaptive extension or evidence of future resumption.

## Fixed 54 cycle proposals

Keep the original whole-worldline Gibbs sweep in color order 0,1,2,3. Immediately after it, visit all 54 cycles once in the fixed order below; measure only after both parts complete.

The six lexicographic port pairs are (0,1),(0,2),(0,3),(1,2),(1,3),(2,3). For each a<b let d=s_a-s_b mod3. It has order three. Partition the 27 cells into nine orbits {r,r+d,r+2d}; choose each orbit's lexicographically smallest representative and sort those nine representatives lexicographically. For representative r0 put r_j=r0+j d and use the six edge tuples

    (r_j,a), (r_j+d,b), j=0,1,2.

They trace A_(r_j) -> B_(r_j+s_a) -> A_(r_j+d): six distinct edges and six distinct vertices. Each cycle vertex has two selected cycle edges and two unselected incident edges. Save the full ordered cycle edge/vertex arrays and canonical pair/orbit labels.

The proposal F_C complements all six selected bits at EVERY imaginary-time slice. It is an involution defined independently of the current path; it has no flippability, ice, charge, energy or acceptance filter. Selection probability is the same forward/backward. Since C(1-i,1-j)=C(i,j), all selected edges retain their temporal factors and kink counts, including periodic closure. Unselected temporal factors are unchanged. Therefore

    ell=log[W(F_C n)/W(n)]=-epsilon sum_tau [D(F_C n_tau)-D(n_tau)],
    a(n,C)=min(1,exp(ell)).

Always consume exactly one scalar rng.random() for each of the 54 proposals, even when ell>=0. Accept iff u=0 or log(u)<min(0,ell); no adaptive representation, extra draw or proposal omission. A rejected move leaves bits unchanged. The log rule avoids underflow and preserves tiny probabilities without clipping. Record nonfinite arithmetic as failure. The ideal MH kernel has detailed balance because ell_reverse=-ell and a_forward/a_reverse=exp(ell). A fixed composition of the Gibbs and MH kernels preserves the SAME finite-M measure, though the full fixed-order sweep need not itself be reversible. This is a Monte Carlo update, not a native Hamiltonian transition or real-time creation event.

Compute the difference from the six affected vertices, without copying the full graph for every proposal. At a vertex let r=0,1,2 be its selected-edge occupation count and c=0,1,2 its other-edge occupation count. Complementing gives r'=2-r and

    delta=c+r-2, delta'=c-r,
    Delta f=f(delta')-f(delta), f(x)=x^2-x/2.

The exact nine entries are:

| c | r=0 | r=1 | r=2 |
|---:|---:|---:|---:|
| 0 | -5 | 0 | 5 |
| 1 | -1 | 0 | 1 |
| 2 | 3 | 0 | -3 |

Sum these integer contributions over all six vertices and every slice. Use signed integer counts so uint8 subtraction cannot wrap. At a strict ice slice a balanced r=1 cycle costs zero, but wholly blank/occupied cycle proposals can cost 18/30 respectively. At beta8 such changes can be strongly suppressed. A cycle move can help mixing and is not a mixing guarantee.

## New controls; reuse of prior Gibbs certification

Do not execute/import the old producer or rerun its 48 enumeration controls. Authenticate those completed control bytes instead. The new source must contain byte-identical and AST-identical copies of the old named functions `degrees`, `diagonal`, `transfer`, `suffixes`, `probability`, `next_probability`, `inverse_cdf`, `sample_lines`, and `sweep`; inspect function bytes using original line-ending-preserving source spans and AST dumps without attributes. Read AST/bytes only, never execute the parent source. New cycle logic wraps the preserved Gibbs sweep. Keep `measure`, `estimates`, `summarize`, `ess`, `rhat` likewise byte/AST-identical, so the measurement and diagnostic convention is unchanged. Custody/chain/report code may add only the declared new recovery/cycle fields.

Before any new-chain sweep run these fixed NEW controls:

1. Enumerate all 54 canonical cycles and check six distinct edges/vertices, two selected incidences at each cycle vertex, order-three orbits, nine per port pair and no duplicate edge set. Check bitwise complement twice is identity and all temporal same/flip indicators, kink parity/counts and positive C factors are unchanged.
2. Exhaust all nine (c,r) entries against two direct full endpoint f evaluations. Reverse r to 2-r gives the negative difference. Check the log-MH identity min(0,ell)-min(0,-ell)=ell at epsilon=1/16,1/32 for those differences and the summed toy-path differences.
3. Use all 54 cycles on each of twenty fixed native graph words: ports01, ports02, blank, full, plus the original sixteen deterministic words n_(r,a)=bit_((r1+3r2+9r3+27a) mod8)(w), w=0..15. Compare the six-vertex formula with an independent complete D before/after complement and check reverse differences exactly.
4. On the same native graph use periodic toy paths M=2,3,4 and w=0..15, with slice word (w+3*tau) mod16 from that deterministic family. For every cycle compare the summed local difference with the full path D difference, temporal C/kink invariance and forward/reverse log-MH identity. These are fixed algebraic sampler controls, not an additional physical simulation or parameter survey.
5. Check the actual acceptance helper on deterministic u=0,1/2 and representative ell=-1,0,1, keeping the production stream untouched. On the named I01 word the nine (1,2) cycles are balanced, each costs zero and their full sequence maps I01 to I02; verify this exact control without running a physical trajectory.

Full-degree/involution/local-difference controls are integer exact. For positive temporal-factor/log identities use absolute tolerance 3e-13; native D comparisons can be exact dyadic arithmetic. Any failed control prevents chain continuation, preserving the controls/error and exact partial context. No arithmetic repair or second attempt.

## Statistics and interpretation retained

Use exactly the parent's seven characters, Fourier 1/sqrt27 normalization, full complex ET and zero-Matsubara covariances, beta times coordination covariance and even/odd combinations, E_M/54 with both terms, degrees/delta/oriented-charge histograms, unconditional cuts and ice-only labels. All source/metric caveats remain. Retain raw first/second moments and sufficient block sums before connected subtraction, both cut histories, all per-chain estimates, equal four-chain raw pooling and separate Re/Im jackknife errors. Do not append the old production traces to the new equilibrium estimate or discard a failed start.

Keep original ESS positive-pair lags0..126, eight-half-chain unranked split Rhat, thresholds ESS>=16/Rhat<=1.10, structural k0-odd null exclusion, undefined diagnostics and no-changes-in-any-cut-component qualification. Arithmetic failures have priority. Passage earns only FINITE_GRID_PILOT_DIAGNOSTICS_PASSED; otherwise preserve MIXING_UNQUALIFIED. Use the same four signed dt/beta comparisons and declared block diagnostics, with no zero-step, beta-infinity or size extrapolation.

Add acceptance attempts, accepted counts and rates for EACH cycle and each of the six port pairs per chain, separately for burn-in and production, and production per-sweep counts. Exactly 64/256 attempts per cycle and nine times those per pair are required. Save the initial recovered cut/degree summary and signed old-segment/new-segment per-chain and pooled differences. Old/new segments share recovered state/RNG and are correlated: show each segment's component SE separately; NEVER quadrature-combine them as independent. New dt/beta comparisons still use distinct PCG streams and their declared independent-chain block diagnostic convention. Supplied graph axis/port permutation symmetry requires equal equilibrium mean cut components1,2,3; retained differences are relaxation diagnostics, not finite-volume symmetry-breaking/phase evidence. No new pass threshold is added for this observation.

## Exclusive custody and boundary

Reserve only NEW `local_record_feedback_3d_collective_cycle_continuation_v001.py`, this protocol, `LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001_RESULT.json`, `_RESULT.md`, `_RECEIPT.json`, and `local_record_feedback_3d_collective_cycle_continuation_v001_checkpoints/`. Refuse existing new results/report/receipt/checkpoint directory. Keep every original input, checkpoint and failed attempt unchanged.

Authenticate all parent/terminal/source/protocol pins and helper identity before controls and again before final sealing. Use one manifest, controls, append-only journal and exclusive fsynced initial/partial/completed bundles and metadata. Save recovered bits/RNG, source terminal reference, segment counters, original counters, raw traces/block sums, cycle attempts/acceptances and active seed/beta/dt/M/color/cycle/slice/proposal context before its hash journal commit. Save each completed chain before the next; retain partial proposed lines and RNG state on failure, with nonfinite-safe error evidence. No automatic resume/reseed/rerun. Final receipt seals raw/canonical result/report, input/terminal hashes, all checkpoint hashes and journal prefix. Report ALL16 chains, ALL4 conditions, all54 acceptance rows per chain (or an explicitly complete attached JSON table with per-pair report summaries), old/new differences with separate errors, grid contrasts and limitations.

Root may authorize one modest local single-thread --execute process only after complete preflights and ownership verification. The fixed endpoint is a scoped sampler result, not selection of a ground coordination pole, a physical 3D phase, an interaction range, a universal matter/source vertex, a mechanical/count law, galaxies or expansion. No background resumption is implied.
