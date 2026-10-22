"""Document the pre-evaluation framing gate; no scientific response evaluation."""
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent
X=H.parent.parent
P=Path('/Users/bgm/Research/Universal Network Theory')
C=P/'UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
D=P/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics'
sources={
 'DISPATCH':X/'FROM_CODEX/0519_2026-10-18_codex2_bhd_step3_prereg_and_lensing_readiness.md',
 'CURRENT':P/'UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md',
 'PRIMER':X/'KNOWLEDGE/UNT_COORDINATOR_PRIMER_V002.md',
 'BH_FRAMING':H.parent/'bind_history_framing_c2/BIND_HISTORY_FRAMING_V001.md',
 'BH_CHECK':H.parent/'bind_history_framing_c2/check/CHECK_V001.md',
 'STEP1':H.parent/'bhd_step1_c2/BHD_STEP1_V001.md',
 'PREREG1':H.parent/'bhd_step1_c2/PREREG_BHD_STEP1_V001.md',
 'STEP2':H.parent/'bhd_step2_c2/BHD_STEP2_V001.md',
 'PREREG2':H.parent/'bhd_step2_c2/PREREG_BHD_STEP2_V001.md',
 'TAYLOR2':H.parent/'bhd_step2_c2/code/exact_taylor.py',
 'BACKEND':H.parent/'bhd_step2_c2/code/pinned/canonical_join_backend_v002.py',
 'READ2':H.parent/'bhd_step2_c2/code/common.py',
 'ROSTER_CODE':H.parent/'bhd_step1_c2/code/graph_roster.py',
 'ROSTER':H.parent/'bhd_step1_c2/results/ROSTER_V001.json',
 'PC1':D/'FIRST_CHUNK_V006_S01_DIAGNOSTIC_V001/FIRST_CHUNK_PREMISE_CARD_V006.md',
 'V005':D/'PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/CANONICAL_MODEL_7_PROPOSAL_V005.txt',
 'AWH':C/'CODEX1/READINESS_ACTUAL_WRITER_HEX_SUPPORT_AND_COLLECTIVE_INPUT_PROPOSED_V001.md',
 'LR':C/'CODEX3/READINESS_LINE_A_BIND_NATIVE_ROUTE_RECOVERY_V001.md',
 'WR2':C/'CODEX1/NATIVE_WRITE_EVACUATION_INTERFACE_PROPOSED_V002.md',
 'A1':C/'CODEX1/ACTUAL_WRITER_TO_INCIDENCE_COEFFICIENT_PROPOSED_V001.md',
 'HXR':C/'CODEX1/READINESS_P26_NATIVE_HEX_READ_AND_GAMMA_QUALIFICATION_PROPOSED_V001.md',
 'BIND0351_NOTES':H.parent/'bind_coupling_0351/producer_A/IMPLEMENTATION_NOTES_V002.md',
 'BIND0351_SPEC':H.parent/'bind_coupling_0351/producer_A/BIND_COUPLING_REFERENCE_FROZEN_SPEC_V001.json',
 'FRAMING_PRODUCER':Path(__file__)}
pins={k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in sources.items()}
utc=os.environ['UNT_CX2_PACKET_UTC']
def put(name,data):
 with (H/name).open('x') as f:
  if isinstance(data,str):f.write(data)
  else:json.dump(data,f,indent=1,sort_keys=True);f.write('\n')
put('SOURCES_CX2V001.json',{'date_u':utc,'sources':pins,'reading_scope':'Targeted text/source inspection; hashing is byte custody, not a claim of full reading. No prior producer was executed.'})
ray={'schema':'BHD3_RAY_DECLARATION_UNSEALED_CX2V001','date_u':utc,
 'status':'UNSEALED_INCOMPLETE_NO_RECORD_EVALUATION','basis':'PC1 DP-h and DP-r copied as benchmark declarations, not fitted or physically calibrated values.',
 'scale':'Every Hamiltonian energy amplitude x=s*xhat; T/hbar=1. dstar and phase/profile labels are held fixed. theta=0 is exact; no undeclared nonzero-phase extension.',
 'known_direction':{'h':'1/5','Delta':'4','Ud':'1','epsilon_c':'1','epsilon_r':'7/8','t':'1','g':'1/2','lambda_R':'1/8','lambda_J':'1/4','epsilon_B_re':'1/8','epsilon_B_im':'0'},
 'fixed_labels':{'dstar':'3','theta':'0','old_hop_phases':'all 1+0i','born_hop_phases':'all 1+0i'},
 'unresolved':{'kappa_profile_and_complex_amplitudes':None,'E_I':None,'E_R':None,'E_S':None,'common_identity_offset':None,'level1_read_rule_R0_or_R1':None,'root_AWH35_custody_ruling':None},
 'no_defaults':'Missing is not zero. WR2 comparison resonance is not promoted to an actual ray. A common offset may cancel analytically, but the relative2E_I Born contact must remain.',
 'sources':{k:pins[k] for k in ['PC1','V005','WR2','STEP2','AWH']}}
put('RAY_DECLARATION_UNSEALED_CX2V001.json',ray)
s=f'''# BH-D step3 framing gate — unsealed

date -u: **{utc}**

Status: **TESTED source inspection; UNSEALED, record evaluation not authorized.** This gate precedes computation-code execution. Claude2 seals and launches. This lane supplies preregistration and synthetic/toy tests only, with "nice unavailable (sandbox); 0514 waiver". No0351/0360 retry or producer execution.

**Lineage.** The target is STEP2 §7 U1-M: the LR:29 controlled-error exit for the V005 literal-7 old/one-Born Hjoin and sparse WR2 W/C. It is not an owned-parent, concurrent-Birth, Gamma-protection, tension, baryon-map or galaxy result. Original Line A writer pricing is not identified with g. History/collective response is to be tested, not prescribed. The principal's Bind-history accounting requirement is DECLARED-PREMISE; the Bullet Cluster interpretation is HYPOTHESIS. This lane does not evaluate that observation.

**Prior work and corrections.** A1 gives the exact+1/448 edge monomial; AWH gives sparse-read support lower bounds only for the epsilon_B-independent family, names mixed diagonal owners and a later full degree-two collective family. STEP1/STEP2 computed exact restricted monomials; they did not sum the full declared-ray coefficient or control its remainder. STEP2 finds which-path, C-arm and Born/read-rule leakage competitors at relevant orders. Retain all of them in Delta_B=Delta-Delta|g=0. BIND0351 is an earlier static ring/Feshbach calculation, not the same real-time sparse-witness calculation; never retry it. BH_CHECK corrects overclaims: coarse history reductions remain open, retained collective state is a possible history carrier, no forced species-weight form, no inferred classical census or assumed universal history effect.

**Premises used.** DECLARED-PREMISE: V005 finite complete old/one-Born generator, both reverses/off-image states and relative2E_I contact; mathematical sparse WR2 preparation with common Q=M=1/active-cell pattern; full step1 L4 graph-derived roster, every cycle retained; qualified coherent read norm/read protocol. Blank q is a mathematical control under S1, not physical empty space. No equal spectral-energy preparation is asserted. R0/R1 is an unresolved instrument declaration and cannot be selected for its result. A1/STEP1/STEP2 coefficient results are FORMAL-RESULT at their stated scopes, not empirical success. Parent transfer and LR:29 record margin are UNTESTED.

**Ray fixed where the record declares it.** PC1 DP-h fixes h/Ud=1/5; DP-r fixes the benchmark ratios listed in RAY_DECLARATION. Use those exact rationals unchanged, dstar3 and theta0. All Hamiltonian amplitudes scale together with s, while dimensionless structural labels and zero hopping phases remain fixed. PC1 does not supply the later admission profile or cell energies. V005 explicitly leaves them declarations. WR2's comparison values do not supply actual values. Thus kappa profile, E_I/E_R/E_S, common-offset convention, R0/R1 and AWH35 custody are PENDING Claude2's prospective declaration; no zeros or favorable choices are inserted. The exact direction must be fully pinned before the prereg seal and before any record coefficient or deciding inequality is evaluated.

**Imports ledger.** No external physical law supplies an owner, coefficient, sign, target or desired outcome. Existing Hilbert-space/unitary mathematics and canonical operators are counted inherited model premises. Exact rational arithmetic, nested commutators, operator norms and positive majorant sums are mathematical tools, not new physical premises. GR is at most a comparator and is not used in this computation. No LambdaCDM fractions, empirical lensing maps, target velocities, fitted weights, toric criticality, macroscopic tension law or classical memory kernel enters. Resource caps change execution completeness labels, never scientific outcomes.

**Proof obligations before record admission.** Complete all-owner leading-degree census including mixed lambda_J*g and diagonal/contact terms; no inference from restricted monomial families. Derive and review a local term/support representation of complete Hjoin, including the cut-fiber Birth map and both sectors, with volume-independent norm-density bound. A global Hilbert-space norm or unproved shared-sector-flag locality is insufficient. Exact/safely enclosed arithmetic must cover coefficients and remainder; the floating inflation factors in TAYLOR2 alone are not an audited all-orders remainder proof. Finite toy validation does not discharge these record obligations.

Every positive, zero, cancellation, insufficient-margin, unresolved-proof, invalid-input and resource-limited outcome will be named in the prereg. A failure names the next uncomputed order, not another ray. No emergence shape or sign is imposed.

Byte pins for every cited source:

'''
for k,v in pins.items():s+=f'- **{k}**: `{v["path"]}`; SHA256 `{v["sha256"]}`.\n'
rp=H/'RAY_DECLARATION_UNSEALED_CX2V001.json'
s+=f'- **RAY_DECLARATION**: `{rp}`; SHA256 `{hashlib.sha256(rp.read_bytes()).hexdigest()}`.\n'
put('FRAMING_GATE_CX2V001.md',s)
print(json.dumps({'framing':str(H/'FRAMING_GATE_CX2V001.md'),'sources':len(pins),'record_evaluations':0}))
