# Frontier V018 — actual-state response and its interpretation

2026-09-27. **Progress; the dark-sector goal is incomplete.** The preceding
research work yielded new exact response kernels and a prospective diagnostic;
the diagnostic has now completed successfully. The intervening handoff
clarification was communication, not a scientific result or a verified wait.
No remote execution is confirmed. No failed production job was retried, no
L8 ran, and no infrastructure, packages, credits or GitHub state changed.

## Completed actual-state diagnostic

Packet: `actual_response/`. Its protocol and code were independently reviewed,
then frozen before its single execution. The state comes from the resident
native-correlation result at SHA256
`aeb8f9ee23ec9a591752f3a9f452889a53ec5db5dd2f50e9acc8a63142f5457d`.
Its writer-traced density and original readouts were checked against the
resident independently assembled minimal-join result at
`223974db8482527821acf71521024f9d2694627fd372cef92c03fa6463a8ac30`.
No dataless parent or earlier two-band artifact was hydrated. This checks
the saved-state relationship, not a new independent formation run.

The complete 36-dimensional equal F0/F1 mixture and all excited populations
were retained. For the source −f n, the exact retarded response is
i Tr ρ[n(t),n(t')] in native ℏ=1 units. The frozen 25 waiting-time/lag pairs
were calculated by a full-matrix commutator, an analytic four-block formula,
and an exact projector-kick identity. The latter uses opposite finite pulses
and denominator 2 sin ε; because n²=n this has no finite-difference bias.

All **236 comparisons** passed the frozen 10⁻¹¹ numerical tolerance.
The largest recorded residual was 3.003×10⁻¹⁵. Runtime was 0.04045 s,
with observed self peak RSS 40,714,240 bytes, under a 30-second wall alarm
and 30-second CPU cap. One worker, one numerical thread, no children or
retries. RSS is not a hard memory cap. The process returned exit code zero;
it is complete, not a live handle to poll.

Sealed result SHA256:
`cfa11736c200aa793765fe560526f7047107a2f4776785e48745fb9ddd87c773`.
The root and two Astra reviewers checked the source/result; details are in
`actual_response/INDEPENDENT_REVIEW.md`. Source and protocol hashes still
match their prelaunch freeze.

## New scientific consequences

The stationary energy-dephased comparator preserves the actual 13.05%
upper-band population, energy 3.5655634501834923, all sector populations
and exact degeneracy coherences. This comparator is mathematical, not a
performed cooling or decoherence operation. Its four response population
differences are approximately 0.12404, 0.14692, 0.20471 and 0.26324.
All four distinct n-channel absorption residues are positive and present.

Its moments are M0=0.07119602512106689, M2=0.010257565079199945,
M4=0.0015644551004654213. The low-frequency inverse coefficients are
D=14.0457279504 and Z_t=2.0236378125. A population-matched ground
replacement would instead give M0=0.1011721475 and change the state.

The ratio M0 M4/M2²=1.0585960985 excludes an EXACT single-oscillator
closure. Nevertheless positivity of the measured residues gives the exact
analytic bound in independent-review equation R1. Instantiated with these
moments, 1/(D−Z_t ω²) approximates the stationary susceptibility to less
than 0.009% relative error over |ω|≤0.5, below every physical pole.
This is a controlled OFF-RESONANT approximation; its apparent pole is not a
new clock mode. Binary64 input uncertainty has the stated verification
scope, not a rigorous forward-error enclosure.

`ACTUAL_FORMED_STATE_RESPONSE_KERNEL_V001.md` proves that this same
positive M0 gives negative shared-source curvature on a population-preserving
adiabatic branch. It does not establish a sudden binary insertion cost or
the energy curvature of the actual unaveraged coherent trajectory.

The actual coherent kernel is demonstrably nonstationary. At lag 1 it is
+0.1912400961 at launch 0 but −0.1030318525 at launch 0.5. The stationary
comparator is +0.0693680494 at both launches. The largest sampled coherence
contribution is 0.1723999019. Time averaging has an explicit response-specific
error bound in the analytical note; waiting alone does not destroy coherence.
Negative time-domain values are not by themselves evidence of negative
stationary absorption, since a passive response can oscillate.

## Clock window: useful, but not universality

`LOW_FREQUENCY_CLOCK_WINDOW_V001.md` derives an exact cutoff at 1/2
that separates the two lower carrier lines from upper/interband lines at
these fixed parameters. This filters an observable, not the state. The
new coefficients verify that both upper lines actually have nonzero readout
amplitudes. The existing failure of a pure common rescaling of both band
frequencies is therefore not hidden by zero amplitudes in the saved state.

For predeclared symmetric boxcar widths 1,4,16,64, the relative spectral
RMS errors against the original lower signal are 15.72%, 9.27%, 26.95%
and 113.73%. Width 4 is best among those four only. This is neither an
optimized filter nor an instantaneous probability or finite-record estimator
error. Longer averaging erases the slow signal as well as unwanted lines.
Only one clock gap per q sector lies in the lower window; link occupation
provides no independent second oscillating clock there. Universal clock or
metric coupling is not established.

## Continuation and other-Mac status

`NATIVE_RECORD_SELECTED_GRAPH_VIRTUAL_RESPONSE_V001.md` is completed and
root-reviewed. The root and two agents independently checked its coefficient,
global gap and sign. Fixed record occupations leave the classical energy of
every d0-regular graph equal. Virtual native flips nevertheless induce

    E2(G)=C+K L11(G),
    L11=number of occupied links joining two occupied records.

This is a second-order consequence of existing terms, not an inserted pair
interaction. For c=Delta+4U(d0−d_*), positive gaps, and nonzero flip/feedback,
sign K=−sign(c−lambda). It favors MORE record-record links if c>lambda,
FEWER if c<lambda, and has no second-order preference at c=lambda. The
source cannot be declared universally attractive. A four-edge switch compares
these arrangements while preserving all node degrees and record counts.

The sufficient global classical gap is 2g, with
g=U−max(|c/2|,|c/2−lambda|)>0. For v=hN² below one quarter of that gap,
the note bounds the ground Feshbach correction beyond second order by
4v⁴/(2g)³, including link-number parity's elimination of the third-order
term. It consequently bounds the reduced-ground weight outside the preferred
L11 sector. This is static weak-flip selection, not preparation or relaxation.

A prospective, UNADOPTED finite-size witness U=1, Delta=4, lambda=1/2,
epsilon_r=1, d0=1, d_*=7/4 has positive record cost 1/2 and
K=−2h²/15. The original d_*=1 mission instead prefers degree zero.
The witness is not a rerun, parameter fit or rescue of that existing mission.
With the actual h=Omega/N normalization, the formal second-order arrangement
range is only O(Omega²/N) at fixed d0, and the crude perturbative norm bound
is not uniform in N. Macroscopic survival, spatial locality and the
realization of a selected structure remain open, not inferred from the finite
arrangement preference.

The user reported that the other Mac interpreted the handoff as a proposal.
We supplied one short corrective execution message for the USER to paste on
that Mac. We did not send it remotely or observe a running job. The old
completed L6 queue remains complete; matched-dephasing execution status is
unknown here. No remote job, budget use or result is inferred from the prompt.

Physical spatial maps, complete stress/volume/clock matching, universal probe
coupling, a realized cosmological population and applicable observational
predictions remain incomplete. Neither the successful finite response nor
the restricted clock window closes those requirements.
