"""A97 fresh C3 le3 reference join, reductions only. Prior results unchanged."""
import os,sys,json,hashlib,math
B='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/'
P=B+'reductions/run_20261018T200537Z_93548/RESULTS_CX2V001.json'
Q=B+'adv_le3/RESULTS_CX2V001.json'
OUT=B+'reductions/'
safe={P,Q,__file__}
outputs={OUT+x for x in ('C3_FRESH_REFERENCE_JOIN_CX2V002.json','C3_FRESH_REFERENCE_JOIN_CX2V002.md','HASHES_C3_JOIN_CX2V002.jsonl')}
def guard(e,a):
 if e=='open' and isinstance(a[0],(str,bytes,os.PathLike)):
  p=os.path.abspath(os.fsdecode(a[0]));parts=p.lower().split('/')
  if any(x in ('runs','runs_ext','.codex') or x.startswith('uvt_') or 'c5h' in x for x in parts) or p not in safe|outputs:raise PermissionError('EXACT_ALLOWED_ARTIFACTS_ONLY')
  if a[2]&(os.O_WRONLY|os.O_RDWR) and (p not in outputs or not a[2]&os.O_EXCL):raise PermissionError('EXCLUSIVE_WRITES')
 if e in ('os.listdir','os.scandir') or e.startswith(('subprocess.','socket.')):raise PermissionError('NO_EXTERNAL_WORK')
sys.addaudithook(guard)
def h(p):
 with open(p,'rb') as f:return hashlib.sha256(f.read()).hexdigest()
assert h(P)=='0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3'
assert h(Q)=='513c117295a43a6ec6ef778e35476eb3520b6032c0c0217c14ee624f59e16bf4'
p=json.load(open(P));q=json.load(open(Q));s=p['per_state']['C3R3'];v=s['rebuilt_rows'];ids=s['row_ids'];tests=[]
def ck(n,b,d=None):tests.append({'name':n,'pass':bool(b),'detail':d})
def minus(a,b):return [x-y for x,y in zip(a,b)]
def mx(x):return max(map(abs,x))
def vec(x):
 i=max(range(len(x)),key=lambda i:abs(x[i]));return {'per_row_km_s':x,'max_abs_km_s':abs(x[i]),'argmax_row_id':ids[i],'signed_at_argmax_km_s':x[i]}
def close(n,a,b,tol):d=mx(minus(a,b));ck(n,len(a)==len(b) and d<=tol,{'max_abs':d,'tolerance':tol})
ck('12_same_row_ids',len(ids)==12 and ids==q['row_ids'])
ck('fresh_status_tested',q['status']=='TESTED' and q['all_input_pins_unchanged'] is True)
ck('source_inputs_share_IND',q['inputs']['ind']['sha256']=='fdbacd7de467c10924d5201b0b168f974a8206d59ee2100473b9340623cfcbce')
ck('evaluation_OFF_same_bytes',q['inputs']['eval']['sha256']==s['baseline_source_pin']['sha256'])
close('IND_discrete_rows_same',v['discrete_total'],q['comparison']['IND_discrete_total_rows_km_s'],2e-11)
close('fresh_P16_discrete_control',q['rows_P16_km_s'],v['discrete_total'],1e-10)
seq=[q['rows_P16_km_s'],v['discrete_total'],v['mixed_gas_cont_stars_disc'],v['B2_continuum_v001_linear'],v['B2_continuum_v001'],v['production']]
names=['reference_quadrature_implementation_remainder','gas_rule_unnamed','star_roster_named','exact_minus_linear_force_unnamed','production_implementation_remainder']
steps={n:vec(minus(b,a)) for n,a,b in zip(names,seq,seq[1:])}
raw=minus(v['production'],q['rows_P16_km_s']);total=[sum(steps[n]['per_row_km_s'][i] for n in names) for i in range(12)]
close('fresh_chain_telescope',total,raw,2e-14)
named=minus(v['B2_continuum_v001_linear'],v['mixed_gas_cont_stars_disc'])
close('named_residual_unchanged',named,s['same_le3_named_star_residual_gas_matched_linear']['per_row_km_s'],0.)
exact_vs_linear=minus(v['production'],v['mixed_gas_cont_stars_disc'])
alias=minus(q['rows_P16_km_s'],q['rows_m0_km_s'])
close('alias_saved_control',alias,q['comparison']['P16_minus_m0_km_s'],0.)
o={'schema':'A97_C3_FRESH_REFERENCE_JOIN_CX2V002','date_u':sys.argv[1],'tests':tests,'passed':sum(t['pass'] for t in tests),'total':len(tests),
 'row_ids':ids,'fresh_C3_raw_sanity':vec(raw),'gas_first_chain':steps,'named_only_common_linear_force':vec(named),
 'production_exact_minus_gas_matched_linear_reference':vec(exact_vs_linear),'fresh_ADV_P16_minus_m0_diagnostic_only':vec(alias),
 'actual_P16_to_P16_alias_contribution':vec([0.]*12),'allowance_km_s':0.05,
 'named_residual_le_allowance':mx(named)<=0.05,'raw_sanity_le_allowance':mx(raw)<=0.05,
 'sources':[{'path':x,'sha256':h(x)} for x in (P,Q,__file__)],
 'limits':['Reference quadrature was executed in the independent adv_le3 lane, not rerun here. This suite checks its pinned row vectors and exact state-input hash join.',
 'Common-linear-force named-only interpretation is unchanged. A mixed-source exact-denominator potential is not invented.',
 'No old C3 le4 row is used anywhere in the fresh chain.','No gate/admission verdict or allowance change.']}
assert all(t['pass'] for t in tests)
with open(OUT+'C3_FRESH_REFERENCE_JOIN_CX2V002.json','x') as f:json.dump(o,f,indent=1,sort_keys=True);f.write('\n')
text=f'''# A97 fresh C3 le3 reference — component join

date -u: `{sys.argv[1]}`

**TESTED: {o['passed']}/{o['total']} reduction/join checks passed.** The independent fresh ADV box12/O6/width0.25/P16 evaluation uses the same le3 OFF array and IND input pins as the component calculation. No old le4 reference is used in this chain. The quadrature was performed in the independent `adv_le3` lane; this join performs only saved-vector reductions.

Fresh C3 raw production-minus-ADV sanity maximum: **{mx(raw):.17g} km/s**, at {vec(raw)['argmax_row_id']}. It exceeds the unchanged 0.05 raw allowance. The same-state discrete-reference remainder is **{steps[names[0]]['max_abs_km_s']:.17g} km/s**; this is a combined quadrature/implementation remainder, not uniquely attributed to one mechanism.

The exact per-row chain now closes from fresh same-le3 ADV through discrete IND, gas-continuum/discrete-star, common-linear-force full continuum, exact denominator and production. Named-only common-linear-force stellar residual remains **{mx(named):.17g} km/s**. Actual alias contribution is zero because both compared channels are P16. The separate fresh P16-minus-m0 diagnostic is **{mx(alias):.17g} km/s** and is not subtracted from the matched-P16 comparison.

Production exact versus the gas-matched discrete-star linear-force reference is **{mx(exact_vs_linear):.17g} km/s**, including tiny readout/implementation terms; it is not labeled pure stellar-only. All signed row vectors are in the JSON. No scientific reading is advocated and no gate record is modified.

Byte pins:

| File | SHA256 |
| --- | --- |
'''
for x in o['sources']:text+='| `'+x['path']+'` | `'+x['sha256']+'` |\n'
jp=OUT+'C3_FRESH_REFERENCE_JOIN_CX2V002.json';text+='| `'+jp+'` | `'+h(jp)+'` |\n'
with open(OUT+'C3_FRESH_REFERENCE_JOIN_CX2V002.md','x') as f:f.write(text)
mp=OUT+'HASHES_C3_JOIN_CX2V002.jsonl'
with open(mp,'x') as f:
 for x in sorted(safe|{jp,OUT+'C3_FRESH_REFERENCE_JOIN_CX2V002.md'}):f.write(json.dumps({'path':x,'sha256':h(x),'kind':'input' if x in (P,Q) else 'review'})+'\n')
entries=[json.loads(x) for x in open(mp)];assert all(h(x['path'])==x['sha256'] for x in entries)
print(json.dumps({'json_sha256':h(jp),'report_sha256':h(OUT+'C3_FRESH_REFERENCE_JOIN_CX2V002.md'),'manifest_sha256':h(mp),'entries':len(entries),'checks':len(tests),'fresh_C3_raw':mx(raw),'named_only':mx(named),'reference_remainder':steps[names[0]]['max_abs_km_s']}))
