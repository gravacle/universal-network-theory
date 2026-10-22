"""Independent source-method census and bounded DDO stellar-rule arithmetic.
No imported producer/library, no original run-tree access, no saved-row replay.
"""
from pathlib import Path
import hashlib, json, math
from datetime import datetime, timezone
import numpy as np

E=Path('/Users/bgm/Research/UNT_EXCHANGE'); A=E/'claude_artifacts'
O=A/'review_b2_decomposition_cx2/method'
P={
 'authority':E/'FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md',
 'adv_source':A/'uv_tail_study_c2/check/adv_tail_check_v001.py',
 'adv_c2':A/'uv_tail_study_c2/check/ADV_TAIL_CHECK_C2_KB12_W025_O6_V001.json',
 'adv_c3c4':A/'uv_tail_study_c2/check/ADV_TAIL_CHECK_C3C4_KB12_W025_O6_V001.json',
 'ind_source':A/'gate_b2_c3/scripts/b2_independent_c3v001.py',
 'record':A/'gate_b2_c3/out/B2_GATE_RECORD_C3V002.json',
 'input_map':A/'gate_b2_c3/out/B2_RECORD_INPUT_MAP_C3V002.json',
 'path1_source':A/'gate_b2_c3/scripts/b2_path1_replay_c3v001.py',
 'path1b_source':A/'gate_b2_c3/scripts/b2_path1b_module_components_c3v001.py',
 'roster_source':A/'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py',
 'library_source':A/'tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
 'profile':Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'),
}
expected={
 'adv_source':'67a6eeb66b1f94fe356272a31294be012fa448f6c8c03b75cdab66fb540e896a',
 'adv_c2':'82a84edd0f952077c39a6b652618b951f1d300d97db17b692671d725083658c5',
 'adv_c3c4':'63dc4c7dd313f21c6e3638027b3511bfa134169e19189db86abf471a76710954',
 'ind_source':'6c013801d8b86255c9ca042deb9de2a95adaa37a11fad06ea23abe104c6089d5',
 'record':'d4b41ffcab00a05bf0bead8c943b8f3555fdeb91beda2cba430efa65431315d7',
 'input_map':'63bb11908a1884ea38dd9e738d00d5e2cabd6144b9f935f1ca487a39aae1ffe4',
 'path1_source':'8344c99852e28cad3206e2d24d474be6b42a0d77a6a8674245d2083fda49fb1f',
 'path1b_source':'086346feb343c7c4b454a51cb2bd049d33430936af533121240d55862f8df877',
 'roster_source':'4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2',
 'library_source':'2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54',
 'profile':'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b',
}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def parse(raw):return json.loads(raw,object_pairs_hook=strict_pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
raw={}
for k,p in P.items():
 assert not any(x in ('runs','runs_ext') for x in p.parts)
 raw[k]=p.read_bytes()
 if k in expected:assert sha(raw[k])==expected[k],k
pins={k:{'path':str(P[k]),'sha256':sha(v),'bytes':len(v)} for k,v in raw.items()}
profile=parse(raw['profile'])['galaxies']['DDO154']['stellar_reference']
r=np.array(profile['radius_kpc'],float);sig=np.array(profile['surface_density_Msun_pc2'],float)
a=float(profile['outer_scale_kpc']); h=float(profile['height_kpc'])
# Exact integrals of Sigma(R)*R over the piecewise-linear profile and exponential tail.
base=sig[0]*r[0]**2/2
for lo,hi,sl,sh in zip(r[:-1],r[1:],sig[:-1],sig[1:]):
 b=(sh-sl)/(hi-lo); c=sl-b*lo
 base+=c*(hi**2-lo**2)/2+b*(hi**3-lo**3)/3
tail=sig[-1]*a*(r[-1]+a)
total=base+tail
def tail_after(t):return sig[-1]*a*math.exp(-t)*(r[-1]+a*(t+1))
x,w=np.polynomial.legendre.leggauss(4)
z=2*h*np.arctanh(x)
vertical=[]
for kz in (0.0,2.0,3.0,4.0,12.0):
 xx=math.pi*h*kz
 continuous=1.0 if xx==0 else xx/math.sinh(xx)
 discrete=float(np.dot(w/2,np.cos(kz*z)))
 vertical.append({'kz_inverse_kpc':kz,'GL4_vertical_transform':discrete,'sech2_vertical_transform':continuous,'difference':discrete-continuous})
# Independent GL4 u-tail zero-mode mass, compared to analytic profile integral.
core_gl4=0.0
for lo,hi in zip(np.r_[0.0,r][:-1],np.r_[0.0,r][1:]):
 xx=(lo+hi)/2+(hi-lo)*x/2;ww=(hi-lo)*w/2
 core_gl4+=float(np.dot(ww,np.interp(xx,r,sig)*xx))
u=(x+1)/2
rr=r[-1]-a*np.log(u)
tail_gl4=float(np.dot(a*w/(2*u),sig[-1]*u*rr))
stellar={
 'units':'radii kpc; mass in solar masses; normalized transform values dimensionless',
 'source_profile_only':True,
 'analytic_registered_stellar_mass_Msun':float(2*math.pi*1e6*total),
 'GL4_discrete_zero_mode_mass_Msun':float(2*math.pi*1e6*(core_gl4+tail_gl4)),
 'GL4_discrete_mass_relative_bias':float((core_gl4+tail_gl4-total)/total),
 'GL4_u_tail_max_node_kpc':float(max(rr)),
 'GL4_vertical_max_abs_node_kpc':float(max(abs(z))),
 'continuum_t40_endpoint_kpc':float(r[-1]+40*a),
 'independent_t44_endpoint_kpc':float(r[-1]+44*a),
 'registered_phase_extent_Rlast_plus12a_kpc':float(r[-1]+12*a),
 'production_t_above40_mass_fraction':float(tail_after(40)/total),
 'independent_t_above44_mass_fraction':float(tail_after(44)/total),
 'continuum_mass_fraction_between_t40_t44':float((tail_after(40)-tail_after(44))/total),
 'vertical_transform_samples':vertical,
 'interpretation':'GL4 support is a quadrature-node extent, not a literal sharp cutoff in the registered profile. Tail-mass fraction bounds omitted radial transform magnitude divided by continuum zero mode using |J0|<=1; it is not a row-error bound, quadrature-error bound or attribution of the B2 residual.'}
adv=parse(raw['adv_c2']); adv34=parse(raw['adv_c3c4']); record=parse(raw['record'])
assert adv['Kb']==adv34['Kb']==12.0 and adv['width']==adv34['width']==0.25 and adv['order']==adv34['order']==6
methods=[
 {'item':'domain and symbol','ADV':'box(12) minus cube(K), Tinf=1/(4 gamma k^2)','B2':'same declared outer/kept region and symbol','difference':'none in the compared box_discrete variant; optional disk variant is not the gated basis; measured q diagnostic is not applied to either tail'},
 {'item':'gas radial rule','ADV':'discrete rings at represented source rotation radial nodes','B2':'cubic Lagrange in s=R^2 through GL4 columns, integrated over each annulus; production Ms128, independent R-GL24 base/36 refined/16 coarse','difference':'unnamed radial source-representation difference; same annular support and element-height basis when source state matches'},
 {'item':'stellar representation','ADV':'box_discrete uses GL4 radial segments/u-tail and GL4 vertical quadrature','B2':'registered profile radial integration and analytic sech2 vertical transform','difference':'named star-roster difference; independent discrete variants recreate the ADV rule'},
 {'item':'m16 alias','ADV':'rows_P16 and rows_m0 both saved; gate uses P16','B2':'actual16-azimuth P16','difference':'no P16-versus-m0 difference in original gated comparison; P16-minus-m0 is a separate named diagnostic, not an automatic subtraction'},
 {'item':'Cartesian integration','ADV':'quadrant kx,ky multiplied4 using D4, both kz signs; width0.25/order6','B2':'independent full signed box; base width0.25/order12, refined0.2/order14, coarse0.5/order8; production cylindrical/harmonic cube decomposition order8 widths0.05/0.02','difference':'quadrature and implementation; symmetry reduction is source-method difference, not by itself evidence of a wrong integral'},
 {'item':'stellar tail quadrature extents','ADV':'GL4 u-map for full source; continuum diagnostic uses48 radial/200 u nodes','B2':'production exponential t panels to40; independent to44 with own panel/order rule','difference':'same infinite exponential profile approximated by different rosters; computed mass/extent contrast attached, no row-bound inference'},
 {'item':'source and evaluation state','ADV':'Case uses last=result.passes[-1], its field/source rotation, rotation and columns','B2':'fixed le3 at feedback17, columns18, rotation19, column mean20; gas from rotation15','difference':'C2/C4 baselines reported equal; C3 ADV is le4 and B2 le3. Underlying identity not verified by this source-only slice'},
 {'item':'rotation readout','ADV':'linear deltaPR=c^2 mean_phi(t_R), then exact Omega^2 update and sqrt','B2':'production nonlinear deltaPR includes1/(1+f0+t) perphi; independent broadcasts angular means of t/tR before nonlinear denominator; P1b diagnostics are linear','difference':'readout correction; mean-before-nonlinearity impact not independently bounded by current saved linear-channel comparisons'},
 {'item':'observation','ADV':'same observation module and column-mean adapter, R sqrt(Omega^2), rho weights and binding inclinations','B2':'same described row pipeline','difference':'metadata provenance strings differ; source-state geometry/weights differ at C3 le4 versus le3; no target input'},
 {'item':'J0 implementation','ADV':'system libm via ctypes','B2':'independent periodic trapezoid J0, libm crosscheck only; production pinned libm provider','difference':'implementation approximation; saved crosschecks do not replace source-custody verification'},
]
end={k:sha(p.read_bytes()) for k,p in P.items()}
assert all(end[k]==v['sha256'] for k,v in pins.items())
out={'schema':'CX2_A97_B2_METHOD_CENSUS_V001','utc':datetime.now(timezone.utc).isoformat(),
 'policy':'nice unavailable (sandbox); 0514 waiver','pins_start':pins,'pins_end':end,'method_differences':methods,'stellar_rule_arithmetic':stellar,
 'C3_missing_artifact':'Same-le3 ADV-like m0/J1 reference (and exact ADV order6 P16 reference) is not in the current declared artifacts. IND_C3R3_BASE already has same-le3 discrete_total P16 and mixed source variants. No saved le3 raw input has been shown missing. Old ADV C3 final-le4 P16/m0 cannot be reused as same-le3 alias.',
 'TESTED':'Source hashes, safe JSON metadata, independent analytic profile mass and NumPy GL4 arithmetic only; all source bytes unchanged.',
 'SOURCE_OBSERVATION':'Method census from source; source array custody and exact stage identity not independently verified.',
 'UNTESTED':'No production or independent full tail integral replay, no original archive or target access, no final row-decomposition decision.'}
payload=(json.dumps(out,indent=2,allow_nan=False)+'\n').encode()
with (O/'METHOD_RESULTS_CX2V001.json').open('xb') as f:f.write(payload)
print(json.dumps({'result_sha256':sha(payload),'stellar_rule_arithmetic':stellar},indent=1))
