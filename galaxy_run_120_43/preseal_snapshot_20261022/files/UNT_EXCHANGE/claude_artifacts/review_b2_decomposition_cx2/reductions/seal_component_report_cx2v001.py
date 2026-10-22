"""Package already computed A97 component evidence; no producer execution."""
import os,sys,json,hashlib
B='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/'
RP=B+'run_20261018T200537Z_93548/RESULTS_CX2V001.json'
def h(p):
 with open(p,'rb') as f:return hashlib.sha256(f.read()).hexdigest()
r=json.load(open(RP));assert h(RP)=='0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3'
allowed={x['path'] for x in r['input_pins']}|{RP,__file__,B+'decompose_saved_components_cx2v001.py',B+'decompose_saved_components_cx2v002.py',B+'run_20261018T200537Z_93548/ACCESS_LOG_CX2V001.json'}
outputs={B+n for n in ('EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json','REVIEW_COMPONENTS_CX2V001.md','HASHES_COMPONENTS_CX2V001.jsonl')}
def guard(e,a):
 if e=='open' and isinstance(a[0],(str,bytes,os.PathLike)):
  p=os.path.abspath(os.fsdecode(a[0]));parts=p.lower().split('/')
  if any(x.startswith('uvt_') or 'c5h' in x or x=='.codex' for x in parts):raise PermissionError('PROTECTED')
  if p not in allowed|outputs:raise PermissionError('EXACT_SCOPE_ONLY')
  if a[2]&(os.O_WRONLY|os.O_RDWR) and (p not in outputs or not a[2]&os.O_EXCL):raise PermissionError('EXCLUSIVE_OUTPUTS_ONLY')
 if e in ('os.listdir','os.scandir') or e.startswith(('subprocess.','socket.')):raise PermissionError('NO_EXTERNAL_WORK')
sys.addaudithook(guard)
for x in r['input_pins']:assert h(x['path'])==x['sha256']
def vec(x,ids):
 i=max(range(len(x)),key=lambda i:abs(x[i]));return {'per_row_km_s':x,'max_abs_km_s':abs(x[i]),'signed_at_argmax_km_s':x[i],'argmax_row_id':ids[i]}
supp={'date_u':sys.argv[1],'scope':'Production exact minus gas-matched discrete-star linear-force reference; NOT pure named-only contrast','per_state':{}}
for st,s in r['per_state'].items():
 a=s['rebuilt_rows']['production'];b=s['rebuilt_rows']['mixed_gas_cont_stars_disc'];supp['per_state'][st]=vec([x-y for x,y in zip(a,b)],s['row_ids'])
with open(B+'EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json','x') as f:json.dump(supp,f,indent=1,sort_keys=True);f.write('\n')
text='''# A97 B2 saved-component decomposition — CX2 v001

date -u: `{date}`

**TESTED:** the saved-component/readout decomposition passed 37/37 checks. This is a computational component report, not a B2 admission verdict. The 0.05 km/s allowance is unchanged. The fresh independent C3R3 le3 ADV reference is being computed in a separate lane; the old C3 ADV remains explicitly off-state here.

The excess in the same-state C2/C4 comparison is dominated by the unnamed gas-rule difference. The table shows maximum absolute values across 12 rows; these maxima must never be added.

| Quantity (km/s) | C2R3 | C3R3 | C4R3 |
| --- | ---: | ---: | ---: |
| Original production minus archived ADV P16 | 0.08213990321575437 | 0.09792780979164206 (le4/off-state) | 0.10832626088468089 |
| IND discrete minus archived ADV P16 | 1.1262102361797588e-11 | 0.0028638312519575493 (off-state) | 1.3713474800169934e-12 |
| Gas discrete → continuum, stars held discrete | 0.07899770395344774 | 0.0953735724132514 | 0.11137130880039336 |
| Stars discrete → continuum, gas held continuum | 0.030115450568374058 | 0.0356225797997638 | 0.03835728930356197 |
| Exact denominator force minus linear force | 2.6874328895587496e-7 | 1.9808299356327552e-7 | 1.2984194697196472e-7 |
| Named star contrast with gas held discrete (alternate order) | 0.030160704319449394 | 0.03568531612788206 | 0.038434533343675525 |
| Actual P16-to-P16 alias change | 0 | 0 | 0 |

**Named-only, same-le3 result:** the gas-matched stellar-roster contrasts 0.03011545 / 0.03562258 / 0.03835729 are each below 0.05. Both sides explicitly use the same linear lapse-force prescription `c² d_R t`, P16 azimuth average, continuum gas, and saved le3 state. The row readout itself remains nonlinear: it updates Omega², takes the square root, computes emissivity-weighted column means, then interpolates to rows and applies inclination. This is a directly computed common-force intervention, not a subtraction of scalar error maxima.

The independent saved-component calculation reconstructs five variants from the pinned `tR` arrays: both discrete; continuum gas/discrete stars; discrete gas/continuum stars; both continuum with linear force; both continuum with the exact kept-plus-tail denominator. It independently recomputes the exact force from the allowed saved OFF full fields and `t_total`, and computes the rows using saved readout weights. The zero-force baseline, all five saved row variants, exact force, source-force addition, and telescoping closure pass. No project module or producer is imported or executed.

The explicit gas-first chain is:

`archived ADV P16 → IND discrete → continuum gas/discrete stars → continuum gas/continuum stars (linear force) → exact denominator force → production`.

Every signed 12-row contribution and each intermediate row vector is saved. The first step is a combined reference-representation residual: Cartesian quadrature/implementation/roundoff and any remaining custody mismatch are not uniquely separated by this contrast. It is at most 1.13e-11 km/s for same-state C2/C4. For C3 it additionally contains the le4-to-le3 state change and cannot be treated as a same-state integration error.

At the raw worst row (row 08), C2's gas contribution is +0.07899770395344774 and star contribution +0.0031421700682443543 km/s; C4's are +0.11137130880039336 and −0.003045050246086589. Their signs explain why scalar-max summation is wrong. All other contributions and all rows appear in the result JSON.

The gas-first and star-first stellar contrasts differ by at most 9.0621e-5 / 1.30352e-4 / 1.69615e-4 km/s, respectively, from the nonlinear square-root row mapping. Both orders remain reported; no unique order-free additive attribution is claimed.

**Distinct mixed-force comparison:** production exact versus the gas-matched discrete-star *linear-force* reference has maxima 0.030115525466314352 / 0.03562262986638132 / 0.038357306548249426 km/s. These include the tiny nonlinear-denominator and implementation terms and are **not pure stellar-only residuals**. Full crossed exact-denominator references would require discrete-source tail-potential arrays, which these archives do not contain (`t_total` is continuum-only). That uncomputed variant is not needed for the explicit common-linear-force contrast and is not fabricated.

The original ADV `P16 − m0` vectors are saved only as diagnostics. Both actual compared channels use P16, so there is no m16-alias intervention in this chain. In particular the old C3 alias diagnostic is le4 and is not relabeled le3.

No production/shared-input error was detected in the tested force/readout relationships and byte joins. This does not prove all shared physical definitions correct, independently regenerate source quadrature, or replace the parallel method/provenance review. Same-state full-box discrete C2/C4 agreement and production-versus-independent continuum agreement are separately visible; neither is used to waive the fixed allowance.

Execution: 0.230138 s, peak RSS 172802048 bytes, zero protected-path attempts in the successful run. Three exact C2/C3/C4 le3 OFF NPZ files were admitted only for this new A97 task; their canonical paths were checked component by component before reads. No C5H, UVT, target velocities, broad run listing, network, or scientific launch occurred. The earlier stricter B2 record review is unchanged.

Harness history: v001 stopped before component computation because the strict guard blocked lazy loading of the standard-library ZIP filename codec. Immutable v002 preloads `encodings.cp437` before installing the input guard; it passed. This was a harness issue, not a scientific finding. No previous artifact was edited.

Evidence:

- Harness: `{harness}` — SHA256 `{harness_sha}`.
- Result (37/37): `{result}` — SHA256 `{result_sha}`.
- Exact-versus-linear supplemental vectors: `{supp}` — SHA256 `{supp_sha}`.

Input pins below were rechecked unchanged at report sealing. They are explicit admitted files; embedded production pointers were not traversed automatically.

| Input | SHA256 |
| --- | --- |
'''.format(date=sys.argv[1],harness=B+'decompose_saved_components_cx2v002.py',harness_sha=h(B+'decompose_saved_components_cx2v002.py'),result=RP,result_sha=h(RP),supp=B+'EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json',supp_sha=h(B+'EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json'))
for x in sorted(r['input_pins'],key=lambda x:x['path']):text+='| `'+x['path']+'` | `'+x['sha256']+'` |\n'
with open(B+'REVIEW_COMPONENTS_CX2V001.md','x') as f:f.write(text)
paths=allowed|{B+'REVIEW_COMPONENTS_CX2V001.md',B+'EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json'}
mp=B+'HASHES_COMPONENTS_CX2V001.jsonl'
with open(mp,'x') as f:
 for p in sorted(paths):f.write(json.dumps({'path':p,'sha256':h(p),'kind':'review' if p.startswith(B) else 'input'})+'\n')
entries=[json.loads(x) for x in open(mp)];assert all(h(x['path'])==x['sha256'] for x in entries)
print(json.dumps({'report_sha256':h(B+'REVIEW_COMPONENTS_CX2V001.md'),'supplement_sha256':h(B+'EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json'),'manifest_sha256':h(mp),'manifest_entries':len(entries),'date_u':sys.argv[1]}))
