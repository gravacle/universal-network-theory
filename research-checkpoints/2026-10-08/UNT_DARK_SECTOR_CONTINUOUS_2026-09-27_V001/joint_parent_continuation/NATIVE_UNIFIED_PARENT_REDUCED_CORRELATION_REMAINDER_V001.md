# One native parent: saved reduced-density correlation remainders V001

2026-10-06 UTC. Prospective root-only SAVED-state reader. No producer/helper import,trajectory,state change,eigensolve,SVD,temperature selection,EOS or phase-budget allocation. All27 original trials,135 spectral/Taylor vector pairs,90 cutoff comparisons and both3348/3528 stored control payloads remain bound and retained. Existing workers and artifacts stay untouched.

## Same operators and exact density indexing

Use the unchanged H16,H=HN tensor I+I tensor B+n tensor W with the inherited three (g,lambda_R) arms,(1,.5),(1,0),(0,.5),kappa0,+/-.001,Omega1,M8/12/16,tau0,.25,.5,1,2. The literal native/field operators are reconstructed from their owned formulas,without calling the producer. Parent/component receipt,source,input,census,PASS and lineage bindings are checked before any vector is used.

For native-by-field amplitudes V[a,j],rhoN=V V_dagger and rhoGamma=V_transpose V_conjugate,NOT V_dagger V. Weighted densities are rho_W=V W_transpose V_dagger and rho_n=V_transpose n_transpose V_conjugate. The joint rho is outer(flat V,conjugate flat V);chi=rho-rhoN tensor rhoGamma. Retain the actual saved vectors without renormalization. Tiny norm deviations stay visible: Tr chi=norm-norm^2 and its marginal traces=(1-norm)rho_a are independently controlled; no zero residual is created by projecting a vector.

The full chi is stored exactly in compact form: each complete joint amplitude matrix and both complete marginal matrices,with the literal outer-minus-Kronecker reconstruction rule. Expanded chi is transiently constructed independently for all partial-trace/weighted-source checks. This avoids hundreds of MB of repeated low-rank matrices without discarding any correlation or coherence. All15 complete marginal,weighted-correlation,mean-field,remainder,total/direct-rate,interaction-rate and bare-field-generator matrices are saved for BOTH methods.

## Sources, norms and interpretation

In native tau units define meanW=Tr(W rhoGamma),meann=Tr(n rhoN),

    chiN,W=Tr_gamma[(I tensor W)chi],
    chiGamma,n=Tr_N[(n tensor I)chi],
    DN=-i[n,chiN,W], Dgamma=-i[W,chiGamma,n],
    MN=-i[HN+meanW n,rhoN], Mgamma=-i[B+meann W,rhoGamma].

Save all these matrices and MN+DN,Mgamma+Dgamma. Independent complete-H amplitude derivatives Vdot=-i(HN V+V B_transpose+n V W_transpose) and direct partial traces of the full interaction commutator check both identities. Explicit weighted traces of expanded chi independently check the Gram-based contractions. Save N_gamma=2j=B-2I and its direct,mean-field and correlation-source rates,with an independent scalar sum control. Mean fields persist even if a remainder or scalar power vanishes. Bare stationarity ||[rhoGamma,B]||F is descriptive and is neither a Gibbs gate nor sufficient fluid closure. The scalar split evaluates all terms along the saved exact state; it does not integrate a separate mean-field trajectory or fit a small-time law.

No eigensolve or singular-value calculation is required: use Frobenius norms,||A||1<=sqrt(dim A)||A||F,chi trace upper sqrt(16(M+1))||chi||F and ||W||infinity<=||W||F. Each computed correlation trace upper is checked against2||W||F sqrt(16(M+1))||chi||F,using the Frobenius partial-trace inequality; this is a conservative arithmetic majorant,not a physical decoupling threshold. Save raw purities and linear entropies without clipping tiny signed rounding errors. In physical time,density rates multiply Eunit/hbar under the ONE inherited unit; the associated physical energy powers multiply Eunit^2/hbar. No global physical unit is fitted.

Exactly6345 arithmetic controls use fixed inherited tolerance1e-11 with floor1; the declared operation bound is max(1,||HN||F+||B||F+||W||F),or its square for rates,mixed method comparisons and remainder-majorant arithmetic. Census:5 operator controls per27 trials,22 per each270 method-state pairs,and2 per135 spectral/Taylor comparisons. Controls cover literal Hermiticity/projector,shape/finite/norm,Gram versus full partial trace,marginal traces,chi normalization identities,independent weighted/correlation sources,complete reduced-rate equalities,interaction decomposition,all matrix Hermiticity,all rate traces,conservative norm bounds,reproduced original energies,mean expectation imaginary residuals,photon-number rate split and spectral/Taylor agreement. No zero-correlation,zero-stationarity,zero-entanglement,thermal or physical success predicate is added. Every saved scalar and matrix remains available even when nonzero.

All90 matched cutoff pairs save full signed embedded-field/native matrix differences,the common low-field block and complete high-field row/column tails,Frobenius and maximum absolute errors,signed scalar differences,the full embedded joint-vector difference,and connected-density Frobenius/trace-upper differences for both methods. All135 same-cutoff spectral/Taylor pairs likewise save complete signed matrix/scalar/vector differences and matrix error norms. The marginal matrices are phase invariant; raw vector differences retain the producer's declared phase convention. These empirical differences are descriptive,not rigorous state-error bounds or a physical cutoff certificate. Field embedding follows the SAME declared Galerkin basis; the native dimension stays16.

## Custody and limits

Authenticate all nine listed inputs plus this protocol and the reader's own bytes before and after evaluation. Refuse duplicate/incomplete descriptors,wrong parent/component source/owner/PID/census/lineage or changed inputs. No historical model replay. Exclusive RESULT.json,REPORT.md,RECEIPT.json are the only outputs; no checkpoints/resume framework. Existing outputs refuse execution; a partial prefix is preserved for review. Canonical JSON is encoded before exclusive creation,all outputs become0444 and the root PID/time/input/source/output hashes are checked again after publication.

Numerical PASS qualifies only this saved arithmetic. Exact microscopic product factorization is not required for approximately autonomous fluids; conversely vanishing mean power alone supplies no current/stress/memory closure. The reader does not derive a native Gibbs state,photon escape,cold P(X),baryon fraction or cosmology. All new physical flags remain FALSE,with every inherited disposition retained.

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001_RESULT.json | d2ad69ba985d5b5ef21ecd2caa687578231c621a79c0d4eb34cdefb344ad90d3 |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001_RECEIPT.json | 91bc8a7feafdbf6bc72ab8e072e7a1575ae0641c64d9c8b91eb1c6c7e64dd073 |
| native_unified_parent_component_exchange_v001.py | 2da75f9a6c20643a7d6b4288a821fe64e72ceb9961495f9dc167949d3d2459a2 |
| NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001.md | c83dbcbbdb8cbb62c459cb8ffdbed49edfc7a2a9148c3c913057dedfc9507072 |
| NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001_RESULT.json | e47f1ec7031dc540412b185cf6c2d0e6441131f3b59befdc1c254eb49b8fae8b |
| NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001_RECEIPT.json | cf88622b4c2c7806577f8cd3c74ac81a5bb3a0b57faeb143265b12d5acac6688 |
| NATIVE_UNIFIED_PARENT_CORRELATION_SOURCE_AND_PRODUCT_INTERVAL_V001.md | f62a63f3230ba90cbf645090f007c39c5b4ae3ae00c1d7459726efe388ccff9f |
