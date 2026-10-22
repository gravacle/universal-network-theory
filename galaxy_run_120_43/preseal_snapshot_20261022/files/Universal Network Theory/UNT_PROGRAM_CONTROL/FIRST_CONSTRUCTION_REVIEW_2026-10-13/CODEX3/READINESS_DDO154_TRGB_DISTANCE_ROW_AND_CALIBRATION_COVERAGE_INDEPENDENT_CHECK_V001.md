# DDO154 TRGB distance: independently checked row and observation contract

2026-10-14. Codex3 local helper recovered_packet_audit. Primary-text check, not a fit or parameter adoption. No images, photometry arrays, target-response data or datasets downloaded; no numerical evaluation.

## Verified observation

[Jacobs et al. 2009, Table1 and §§III,VIII,X](https://arxiv.org/html/0902.3675v2): the header ends E(B-V), D M, Lo, Hi. Row PGC43869 / NGC4789A / GO10905 / ACS gives E(B-V)=0.009 and distance modulus DM=28.03, Lo=28.00, Hi=28.07 mag. §§III/X define the low/high entries as68percent confidence limits. This independently confirms the coordinator's row identification using the previously verified DDO154 alias. The paper uses maximum-likelihood TRGBTOOL and artificial-star tests for completeness/crowding/color spread. It adopts Rizzi calibration and Schlegel foreground extinction. §VIII explicitly says target-galaxy internal extinction cannot be estimated from these observations. No internal-extinction bound is supplied by that statement. The apparent TipI conversion inconsistency was not resolved; that column is not used to reconstruct the modulus. The final published DM block is the verified input summary.

## Calibration coverage

[Rizzi et al. 2007, abstract and §§III–V](https://arxiv.org/html/astro-ph/0701518v2) derives a color-dependent calibration with M_I(TRGB)=−4.05±0.02 at (V−I)=1.6. Its abstract characterizes the zero-point accuracy as statistical, conditional on the horizontal-branch magnitude scale. §IV adopts Carretta2000's M_V(HB)=(0.13±0.09)([Fe/H]+1.5)+(0.54±0.04), on the stated metallicity scale. HB calibrator metallicities, reddening and photometric-system conversions enter the calibration. Cepheid comparisons are compatibility checks, not its independent zero-point anchor. Thus ±0.02 is not demonstrated to cover every distance-scale systematic or DDO154-specific extinction. The paper also provides flight-system color relations; using them does not justify counting an additional independent ground-system calibration of the same stars.

## Usable contract and remaining limited uncertainty task

Register the datum as a conditional TRGB distance-modulus summary for the prospective DDO154 CALIBRATION source normalization, retaining the exact object/program/camera and calibration lineage. Preserve the asymmetric68percent limits as reported. They are neither deterministic support bounds nor a complete posterior/likelihood; a Gaussian, split-normal, or truncated distribution would be an additional explicit approximation requiring its own declared scope.

Use D(pc)=10^[(mu+5)/5] only after the observation-error interpretation is declared. This is the distance-modulus definition, not a newly evaluated distance. Carry a shared calibration offset across all data using this zero-point, plus any separately supported object extinction/photometry terms, with correlations retained. Do not add the Rizzi ±0.02 or HB errors in quadrature to the published row until the row's existing propagation is established; that could double count calibration uncertainty. Conversely, do not declare those terms absent because the row has a narrow confidence interval.

The now-closed input gap is the existence and exact location of an independent stellar distance measurement for DDO154, with stated statistical coverage. The narrower remaining task is to establish the published row's calibration-error inclusion and own the residual common-scale/extinction uncertainty for the intended inference. This does not require a new distance measurement by default. It also does not make all galaxy geometry independent of the allocated kinematic read or settle the collective state/exterior. No conventional halo mass or expansion fraction enters this contract.

## Access and exposure custody

Both versioned arXiv HTML sources fetched successfully in this check. No PDF was fetched here; the coordinator's reported PDF-text search failure is acknowledged as inherited, not a successful independent PDF read. The SAO4.04Mpc display was not independently opened in this check and is not used as a second independent distance or uncertainty. Browser excerpts incidentally exposed neighboring distance-table rows and calibration-galaxy comparisons; none was selected or imported. No NGC3198 velocity values were sought. This check verifies source content, not adoption of its values into a scientific run.
