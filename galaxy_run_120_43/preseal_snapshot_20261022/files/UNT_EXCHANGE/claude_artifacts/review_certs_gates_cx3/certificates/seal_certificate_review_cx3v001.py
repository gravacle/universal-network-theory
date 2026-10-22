"""Seal only this certificate review, exclusively creating report, decision and manifest."""
import json, hashlib, datetime
from pathlib import Path
D=Path(__file__).resolve().parent
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
C=A/'tail_scheme_impl_c2/certificates_v002'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def put(p,value):
    with open(D/p,'x') as f:
        f.write(value if isinstance(value,str) else json.dumps(value,indent=2,allow_nan=False)+'\n')
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
names=['EPS_REVIEW_V002.json','LO_REVIEW_V001.json','I1T_NGC_REVIEW_V001.json','GQ_REVIEW_V001.json','LO_NGC_READOUT_REVIEW_V001.json','CONTRACT_AND_LO_RHO_REVIEW_V001.json']
r={name:read(D/name) for name in names}
deps={}
for item in r.values():
    for dep in item['read_dependencies']:
        p=Path(dep['path']);got=sha(p);assert got==dep['sha256'],p
        deps[str(p)]=pin(p)
sources=[C/'gates'/f'{n}.json' for n in ['EPS_CERT_V006','LO_CERT_V002','LO_NGC_CERT_V002','I1T_NGC_T120L_V001','GQ_CERT_V002','GQ_CERT_V003_KB128','GQ_CERT_V003_KB256_MS128']]
sources += [C/'CERTIFICATES_V002.md',C/'check/CHECK.md',C.parent/'certificates_v001/check/CHECK.md',C/'tools/lo_cert_c2v002.py',C/'tools/eps_cert_c2v005.py',C/'tools/gq_cert_split_c2v001.py',Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0529_2026-10-18_codex3_laneB_crosslineage_review_certificates_and_comparator.md')]
for p in sources:deps[str(p)]=pin(p)
eps=r[names[0]];lo=r[names[1]];i1=r[names[2]];gq=r[names[3]];ng=r[names[4]];contract=r[names[5]]
assert all(x['pass_gate'] for x in i1['results']) and i1['H2_omission_negative_control']['correctly_refused']
assert lo['pass_gate'] and contract['LO']['pass_gate']
assert not gq['results'][0]['in_domain_pass'] and gq['results'][1]['in_domain_pass']
assert all(c['max_relative_reported']==c['max_relative_reaggregated'] and c['max_abs_reported']==c['max_abs_reaggregated'] and c['every_roster_has_relative'] for c in gq['record_arithmetic'].values())
findings=[
 dict(id='CX3-C1',classification='FIELD_SEMANTICS',status='TESTED',owner='Claude2 certificate consumers',
      finding='EPS CERTIFIED satisfies the recorded registered refinement rule. Correct envelope estimates are published separately. For first3 shells eps and eps_max represent actual-set estimates, not the cardinal-torus envelope.',
      deciding_step='A consumer requiring the full torus-envelope bound must use eps_envelope / envelope_bound.eps_max_envelope_all_shells (or max of actual/envelope), not the low-shell eps alone.'),
 dict(id='CX3-C2',classification='NUMERICAL_QUALIFICATION',status='TESTED',owner='Claude2 scientific acceptance',
      finding='Search results are numerical maximum estimates. At shell300 the independent value exceeds the record by1.52264e-8 relative (5.55e-16 absolute). No rigorous global upper-bound proof is furnished.',
      deciding_step='Retain numerical-estimate labeling and the registered acceptance convention; do not promote these to proved suprema.'),
 dict(id='CX3-C3',classification='CONDITIONAL_ADMISSION_GAP',status='UNTESTED',owner='Claude2 certificate build/admission',
      finding='LO V002 is built from the saved C4R3 le3 source at M_s64. Changing to M_s128 changes S_T, hence its absolute shell integral. The recorded bound has no demonstrated mathematical transfer to M_s128, even though M_s128 GQ passes.',
      deciding_step='Before using this LO record to qualify a different M_s128 source, recompute matched-source LO integrals or supply a certified bound on their difference. This is not a failure of the reviewed Ms64 arithmetic.'),
 dict(id='CX3-C4',classification='READOUT_SCOPE',status='TESTED',owner='Claude2 LO_NGC interpretation',
      finding='Non-lapse share of lnN is zero for valid metric evaluations. Non-lapse changes can still fail SPD/other guards; zero share is not unconditional admission.',
      deciding_step='Preserve valid-metric qualification. Synthetic invalid-SPD control is correctly refused.'),
 dict(id='CX3-C5',classification='I1T_SCOPE',status='UNTESTED',owner='Claude2 source/readout admission',
      finding='Honest NGC I1-T certifies stored T120L iteration-zero represented stars+H2+initialHI only. Continuum tail-source representation and downstream consumer enforcement are not tested by this review.',
      deciding_step='Retain exact scope and require any separately registered continuum/source admission evidence before making that different claim.'),
]
decision=dict(schema='CERTIFICATE_REVIEW_CX3V001',verdict='PASS_WITH_FINDINGS',date_u='Sun Oct 18 12:58:54 UTC 2026',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='0529 certificate-only cross-lineage review. Existing certificate bytes, saved permitted C4R3/T120L inputs and synthetic arithmetic. P128 coverage primary; P64 coverage supporting.',
    not_launch_authorization=True,source_build_or_scientific_run_started=False,forbidden_run_reads=False,NGC_observed_or_target_reads=False,
    reviewed_evidence=[pin(D/name) for name in names],findings=findings,
    verdict_meaning='Requested independent checks reproduce claimed numerical quantities within stated precision and confirm GQ negative/positive controls. This does not certify an entire P128 production stack or transfer Ms64 LO to Ms128.',
    coverage=dict(required_P128=2*128*2**.5,required_P64=2*64*2**.5,EPS_LO_end=363.,
        GQ='GQ labels reach362 but generator samples a cylinder with k_perp and |k_z| up to362; it therefore contains the physical cylinder256. Do not interpret362 as a spherical truncation.'),
    errors_corrected_without_overwrite=[
        'Initial LO helper refused platform metadata subprocess before creation. Immutable successor uses direct libm J0 with no subprocess.',
        'EPS V001 blind search missed high-shell global candidate. V002 adds own low-shell optimum as a high-shell start; prior files retained.',
        'LO blind rho search found a smaller local maximum. Supplement independently evaluates producer extremum and locally attempts to refute it; no claim of rigorous global supremum.'],
    peak_rss_bytes=max(x['peak_rss_bytes'] for x in r.values()))
put('REVIEW_DECISION_V001.json',decision)
lines=[
 '# Codex3 certificate review — PASS_WITH_FINDINGS',
 '',
 'date -u: `Sun Oct 18 12:58:54 UTC 2026`.',
 '',
 'The requested independent numerical checks reproduce the reviewed certificates within the stated precision. This is a certificate review, not scientific launch authority or a complete P128 admission certificate. Transfer of the Ms64 LO bound to an Ms128 source remains UNTESTED.',
 '',
 'TESTED: saved-state arithmetic and synthetic checks only; one isolated Python process at a time, single-thread BLAS, NumPy/stdlib only. Maximum measured RSS: %.3f MiB. No forbidden UVT/C5H run, NGC observed/target velocity, network, or scientific launch was used. All outputs were created under new names.'%(decision['peak_rss_bytes']/2**20),
 '',
 '## Independent checks',
 '',
 '| Item | Independent result | Reading |',
 '|---|---|---|',
 '| EPS (2,3] | %.16g | Matches published envelope; envelope/eps %.12f. |'%(eps['shells'][0]['maximum'],eps['shells'][0]['ratio_to_eps']),
 '| EPS (30,31] | %.16g | Matches published envelope. |'%eps['shells'][1]['maximum'],
 '| EPS (300,301] | %.16g | %.3g relative above published estimate; numerical-search/roundoff qualification. |'%(eps['shells'][2]['maximum'],eps['shells'][2]['ratio_to_envelope']-1),
 '| EPS/LO coverage | 363 /kpc | >= sqrt(2)*256 = %.14f; also covers P64. EPS361 consecutive unit shells verified. |'%(math_sqrt:=2**.5*256),
 '| LO (64,128] B1 | %.16g /m | Relative difference %.4g vs record; independent integration and refined panel check. |'%(lo['integrals'][-1]['B1'],lo['B1_relative_difference']),
 '| LO (64,128] share/tau | %.16g | < 0.005, with production-module reevaluation and local perturbation of producer rho extremum. |'%contract['LO']['rederived_max_over_tau'],
 '| NGC I1-T fixed/gas/sum, 50 nodes | %.4g / %.4g / %.4g | All < 1e-12. Independent profile/Bernstein rings and angular-integral J0. |'%tuple(x['max_relative'] for x in i1['results']),
 '| H2 omission canary | %.8g relative | Correctly refused at same 1e-12 tolerance. |'%i1['H2_omission_negative_control']['max_relative'],
 '| LO_NGC valid readout perturbations | 50/50 unchanged | Lapse perturbation changes lnN; invalid SPD refuses. |',
 '| GQ Ms64→128, inside cylinder256 | %.8g /P0 | Correctly fails 1e-12. |'%gq['results'][0]['all_kp_le256_max_abs_over_P0'],
 '| GQ Ms128→256, 50 nodes | %.8g /P0 | Passes sampled nodes; max relative change %.8g. |'%(gq['results'][1]['max_abs_over_P0'],gq['results'][1]['max_relative']),
 '',
 'EPS `CERTIFIED` is the registered refinement/convergence decision: all361 records satisfy eps_refined <= 1.1*eps_base and at most one refinement. Both eps_max and envelope_bound.eps_max_envelope_all_shells reaggregate exactly. The producer correctly exposes the envelope in every shell and labels the first3 eps values as actual-set estimates. The low-shell ratio is a field-meaning distinction, not a failed registered convergence test. A stronger all-shell envelope consumer must use the envelope fields. A numerical search is not a proof of a global supremum.',
 '',
 'LO integral was evaluated with two independent cylindrical quadratures, widths0.5/0.25 and orders10/12. The refined B1 differs from the record by3.02e-6 relative; vertical interpolation validation error is%.3g. The blind rho search and the producer-point verification are both retained. The latter reconstructs the physical symbol through pinned production modules, without importing certificate/checker evaluators. All recorded LO shell thresholds and the summed threshold reaggregate successfully.'%lo['vertical_interpolation_max_relative'],
 '',
 'GQ uses independently implemented cubic Lagrange radial factors in normalized GL coordinates and direct vertical mass contraction; saved gas column elements and the system libm J0 are shared. Its50 nodes differ from the original4096 samples and include k_perp256 and362. The three original GQ records correctly reaggregate their own max-relative and P0-normalized maxima. The high-reach Ms64 failure is preserved; Ms128 is a separate positive datum. The GQ generator uses cylinder bounds, so its362 label contains cylinder256 and does not imply a gap at spherical radius362.03867.',
 '',
 'NGC I1-T reconstructs1072 stellar rings,176 H2 rings and156 HI rings independently, preserving the finite prep H2 mass normalization. The stored component1–9 maxima are zero at checked nodes. LO_NGC pins the honest4096-node iteration-zero I1-T record from bytes and correctly separates that represented source from the untested continuum auxiliary roster. The50-node review is additional evidence, not a replacement for the declared4096-node sample.',
 '',
 '## Findings and deciding owners',
 '',
]
for f in findings:
    lines.extend([f"- **{f['id']} — {f['status']} ({f['classification']}).** {f['finding']} Owner: {f['owner']}. Deciding step: {f['deciding_step']}"])
lines.extend([
 '',
 '## Earlier check F1–F6',
 '',
 '- F1: the high-k directional underestimation is addressed by the new torus-envelope estimates; own shells30/300 reproduce them. Low-shell field semantics remain explicit above.',
 '- F2: honest NGC iteration-zero I1-T is now present, byte-pinned and independently reproduced at50 nodes. Continuum tail representation remains a separate scope.',
 '- F3: historical missing-FIELDS documentation error is not evidence of a current certificate numerical failure; no new comparison-engine audit was performed.',
 '- F4: readout-coupled LO_NGC is0 for valid lnN evaluations; the synthetic SPD refusal demonstrates the scope qualification.',
 '- F5: EPS/LO endpoints are363, satisfying exact P128/P64 endpoint requirements. Source/config qualification remains separate.',
 '- F6: max-relative GQ changes are present and aggregate correctly; they are reported separately from the P0 gate.',
 '',
 'UNTESTED: all production launches, forbidden run evidence, complete scientific-stage execution, rigorous supremum proof, full GQ4096-sample reproduction, continuum NGC I1-T and downstream consumer enforcement. The separate identity comparator review belongs to the parent lane.',
 '',
 'The initial LO wrapper stopped before spawning platform metadata. A new immutable script bypasses that metadata call. Earlier EPS blind-search evidence is preserved, as is the blind LO rho lower maximum; targeted successors resolve those limited-search results. No reviewed file was edited.',
 '',
 '## Evidence and byte hashes',
 '',
 'Paths below are relative to this report directory; each hash is from current file bytes.',
 '',
 '| File | sha256 |',
 '|---|---|',
])
for name in names+['REVIEW_DECISION_V001.json','review_certificates_cx3v001.py','review_certificates_cx3v002.py','review_certificates_cx3v003.py','review_readout_cx3v001.py','review_contracts_cx3v001.py','seal_certificate_review_cx3v001.py']:
    lines.append(f'| `{name}` | `{sha(D/name)}` |')
lines.extend(['','Reviewed source citations (full paths and byte hashes):',''])
for p in sources:lines.append(f'- `{p}` — sha256 `{sha(p)}`.')
lines.extend(['','All transitively opened research dependencies are listed with byte hashes in the accompanying hash manifest. This report does not repeat their numerical contents.',''])
put('CERTIFICATE_REVIEW_V001.md','\n'.join(lines))
outputs=[pin(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=dict(schema='CERTIFICATE_REVIEW_HASHES_CX3V001',date_u=decision['date_u'],outputs=outputs,read_dependencies=sorted(deps.values(),key=lambda x:x['path']),self_hash='External packet only; no self-referential hash')
put('HASH_MANIFEST_V001.json',manifest)
for name in ['CERTIFICATE_REVIEW_V001.md','REVIEW_DECISION_V001.json','HASH_MANIFEST_V001.json']:
    print(name,sha(D/name))
print('outputs',len(outputs)+1,'bytes',sum(x['bytes'] for x in outputs)+(D/'HASH_MANIFEST_V001.json').stat().st_size,'deps',len(deps))
