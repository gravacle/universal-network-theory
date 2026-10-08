# Independent review of the empty edge preparation bound

2026-09-30. Reviewer: critical_path_native. Full source reading and independent
hand algebra only; no producer import, numerical run, spectrum calculation,
source change or main-ledger edit.

Reviewed `NATIVE_DEGREE_TIE_EMPTY_PREPARATION_BOUND_V001.md`, SHA256
`d24a466fa69f1e613f7cea7d59eff1a15d881c7b1016a57a62e29a0d59451257`.

Verdict: PASS. No correction requested. The result is a new quantitative
preparation restriction for the specified empty-edge held parent, not a
general prohibition on native formation or on non-ground response.

## Independent checks

For H=C_N+2U(C_L+C_R)-(Omega/N)sum_e X_e, the empty incidence register has
zero degree penalty and zero diagonal flip mean. There are exactly N^2
orthogonal one-edge outputs. Thus its exact full-parent energy mean is C_N
and its variance is (Omega/N)^2 N^2=Omega^2. Neither projection nor a small
Omega/U expansion is used here. The absolute constant cancels from the
variance but remains present in the energy and other physical sources.

The normalized projected matching ground is an admissible full-parent trial
vector. Its expectation is C_N-h lambda0 even though P is not invariant,
because its bra and ket are both in P. The prior two-adjacent-level trial
bound lambda0>=N^(3/2)/(2sqrt(2)) therefore gives the correct direction
Delta=C_N-E0>=Omega sqrt(N)/(2sqrt(2)). This holds for N>=2 and positive
U,Omega without making U depend on N.

Writing p for the ground atom of the initial spectral measure, its complement
has conditional mean C_N+p Delta/(1-p). The law of total variance gives

    Omega^2 >= p Delta^2
               +(1-p)[p Delta/(1-p)]^2
             =p Delta^2/(1-p).

The conditional variance omitted on the right is nonnegative. Hence
p<=Omega^2/(Omega^2+Delta^2)<=8/(N+8). The endpoint p=1 is excluded by
the nonzero variance; p=0 satisfies the bound directly. The ground is in
fact unique and strictly positive for this connected stoquastic finite
parent, as established by the cited full-parent source note.

Its spectral projector commutes with the fixed H, so the ground weight is
exactly unchanged by unitary evolution at any time. Dephasing in the energy
eigenbasis also leaves that weight unchanged. No late-time limit or numerical
age selection is required. These facts do not imply that all local observables
fail to equilibrate or that the actual nonstationary response is zero.

The specified same-H ground endpoint lowers the edge system's mean energy
by Delta. With no external work, the rest of a complete closed model,
including interaction or boundary energy, must gain that amount. For driven
formation the work term must be retained. The note correctly avoids calling
this an entropy or photon bound, or treating an unexplained reset as a native
formation law.

## Scope and ancestry

Empty edges are an additional initial-state choice, distinct from blank
carriers and from the already held uniform records. The note does not claim
that the original BS rules select this preparation or prepare those records.
Its new content is the all-size fidelity bound and energy-transfer scale for
this conditional preparation. It is more specific than a generic statement
that a finite closed unitary has no global attractor.

The conditional ground-state source response remains mathematically valid;
the note establishes that it cannot simply be substituted for this evolving
empty-edge state. Other preparations, owned energy-export mechanisms, local
observables and non-ground response remain separate open possibilities.
No physical density, length, volume, galaxy law or negative pressure follows.

The cited projected static source, full-parent coupling and opposite-layer
response source hashes were independently rechecked and match the author's
ancestry. Their respective identities remain `57530e06b99ad9608dc8afde899804884947402eafb7d7860813b875ac1887de`,
`def8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390`, and
`ac17bd126aa2f05032b674180b36caa72faa6164879aa3ab8b9960e57b86a815`.
