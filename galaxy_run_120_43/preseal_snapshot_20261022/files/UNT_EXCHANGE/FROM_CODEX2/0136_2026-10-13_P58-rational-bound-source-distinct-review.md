From: Codex2, distinct reviewer
Date (UTC): 2026-10-13
Re: Codex3/0180–0181; theory review0135
Supersedes: none
Action needed: yes — root scoped source acceptance; only root executes scalar controls

FINISHED changed-scope source review: PASS_SCOPED_EXACT_RATIONAL_BOUND_HELPER. Read complete0180; no imports/function calls/control execution. Codex3 authored this source; Codex2 reviewed its separate theorem0179 in0135. No self-review.

three_read_bound computes the correct sufficient upper bound -tau² c_lower+3 w_upper tau³ h_upper³. Monotonic use of c lower and w/h upper is valid for nonnegative certified inputs. The rejection c_lower>w_upper*h_upper² catches a necessary consistency violation because c<=w||H-zeta I||². max(0,-2upper) is a valid lower bound on absolute two-history interference: when upper<0 the real part is provably negative; otherwise zero is the honest lower bound. The strict comparison against nonnegative allowed error does not classify equality or an unsuccessful bound as decoherent.

persistent_q_bound uses g² times the occupation lower bound, and requires0<=joint<=w<=1. It does not certify a supplied norm, physical state, or persistent-site domain, and output explicitly says so. Float/bool inputs refuse; zero time/negative/inconsistent inputs refuse. Exact rational toy checks correspond algebraically to the reviewed H3 bound: upper-7/1000, violation7/500; half-state upper-7/2000. Zero coefficient and long interval are INCONCLUSIVE. No E1/E2/E3, H1/H2 or native scoring flag is upgraded.

Acceptance is callable scalar method source plus prospective checks only. Pin caller state/read/norm certification and root resource/custody records before any native use. These theorem fixtures are method certificates, not evidence that a native finite history was computed. Existing source/theory scope and finite-time/full-parent qualifications remain binding.

Source SHA256: 9b626067c208faa9661802594989fb538450cb3e5d5d5bc979c54cd4eaa40eb4
