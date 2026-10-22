from pathlib import Path
import json,hashlib,sys,subprocess,datetime,re,resource
B=Path('/Users/bgm/Research/UNT_EXCHANGE');O=B/'claude_artifacts/cp1_eps_reviews_cx3'
D=B/'FROM_CODEX/0763_2026-10-20_codex3_EPS_reviews_rows10_31_signer_approved.md'
CL=B/'claude_artifacts/s4rc1_c3/build_c3v001/templates/REVIEWER_CHECKLIST_C3V001.md'
AD=B/'claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
assert sha(AD.read_bytes())=='4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'
assert sha(CL.read_bytes())=='d4ed05028d784999c7fde42a3a34cc2fe7571248899d968082c2915a31a3f1ee'
rows={int(r):f for r,f,_,_ in re.findall(r'\| (\d+) \| (P[^ ]+) \| `([a-f0-9]+)` \| `([a-f0-9]+)` \|',D.read_text())}
which=sys.argv[1];selected=[28,29,30,31] if which=='batch1' else list(range(10,28))
refs=[pin(D),pin(B/'FROM_CODEX/0765_2026-10-20_codex3_EPS_adapter_path_and_checklist.md'),pin(CL),pin(AD),pin(Path(__file__)),pin(O/'independent_checks_cx3v002.py')]
reviews=[]
for row in selected:
 key=rows[row].split('_')[1];cp=O/('CHECKS_CX3_'+key+'_V002.json');c=json.loads(cp.read_bytes());assert not c['failed_checks'] and all(c['checks'].values())
 inputs={}
 for ip in c['inputs']:
  path=Path(ip['path']);raw=path.read_bytes();assert sha(raw)==ip['sha256'] and len(raw)==ip['bytes']
  kind=path.name[:-len('_'+key+'.json')];inputs[kind]=json.loads(raw)
 req=inputs['EPS_REVIEW_REQUEST'];num=inputs['EPS_NUMERIC'];ctx=inputs['STAGE_CONTEXT'];stage=inputs['STAGE_EPS'];bindings=req['bindings'];m=c['metrics']
 assert bindings['adapter_sha256']==sha(AD.read_bytes())
 assert 'Codex3' not in req['excluded_reviewer_lanes'] and ctx['checks_info']['source_pins_match_anchor'] is True
 assert m['context_kind']=='PRESENT'
 # The observed ratios deviate from unity by less than 3e-7 on every point.
 assert 0.9999997 < m['dense_ratio_min'] <= m['dense_ratio_max'] < 1.0000003
 flagged=row in {10,14,18,22}
 now=subprocess.check_output(['/bin/date','-u'],text=True).strip();utc=subprocess.check_output(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],text=True).strip()
 e6=f"TESTED. eps_max={m['eps_max']!r} on {m['eps_max_shell']}; {m['ratio_to_approx_anchor_2_05e_4']:.12g} times the approximate 2.05e-4 anchor cited in the dispatch. "
 e6+=('FLAGGED for root Q10: approximately 80 times that anchor, 25.6 times the checklist anchor 6.4e-4, and 1.31 times the cited corner_00 sample 0.0125. No rejection on magnitude alone.' if flagged else 'No E6 large-value flag: this value is comparable to or below the cited anchor; no magnitude gate was applied.')
 checklist={
 'E1':f"TESTED. Row {row} folder prefix, request point_sha256, numeric point_sha256, context point_sha256/key and EPS stage key agree. Canonical sorted compact JSON of custody hashes to {bindings['custody_sha256']}, equal to the context and request; custody objects agree. Numeric dependencies equal context source pins. The declared producer pin is canonical a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231. UNTESTED: independent opening of the full 31-point table and producer source; membership relies on the root-dispatched row and the runner point_sha256_is_key check, within the permitted read scope.",
 'E2':'TESTED. Registered settings, full_registered_search_executed and coverage_complete true. Exactly 178 contiguous unit shells [4,5] through [181,182] and 14 distinct dense audits. Recorded production searches use 12^3 x 200 x 3 nodes, 8 starts plus the previous-shell solution; dense searches use 20^3 x 400 x 5 with 16 starts. Optimization was not rerun.',
 'E3':f"TESTED. CERTIFIED discrete verdict; every shell certified; refinements are integers in {{0,1}}. Refinements=1 on {m['refined_shells']}; all other shells have 0.",
 'E4':'TESTED. Every shell has eps >= eps_envelope >= 0. Envelope values include the dense audit where present; eps equals the maximum of the recorded actual, discrete and envelope estimates. Actual estimates equal max(dense_max, local_max). eps_max and its shell match both the numeric record and stage record.',
 'E5':f"TESTED. Across 14 audits dense_over_production ranges from {m['dense_ratio_min']!r} to {m['dense_ratio_max']!r}. Every ratio recomputes exactly as dense/production; production matches the shell envelope estimate, dense matches its search estimate, and shell eps dominates dense. The observed deviations from unity are below 3e-7, so no well-above-one under-resolution flag is warranted by these records.",
 'E6':e6,
 'E7':'NOT_APPLICABLE. This is not the anchor; context says PRESENT. Only the anchor carries the cross-check, per the allowed root notice. No anchor cross-check file was opened or revalidated.',
 'E8':f"TESTED. STAGE_EPS ok=true; all {len(stage['checks'])} EPS checks and all {len(ctx['checks'])} context checks true. Numeric pin matches bytes ({len((Path(bindings['numeric_ref']['path'])).read_bytes())} bytes); context source_pins_match_anchor=true. Wall {stage['seconds']!r} s, CPU {stage['cpu_seconds']!r} s and producer peak RSS {stage['producer_peak_rss_bytes']} bytes are present as information only.",
 'E9':'TESTED. rigorous_supremum=false, production_admissible=false and covers_all_consumed_states=false remain explicit in the numeric record. Approved solely as the registered numerical convention: finite searches provide lower bounds on the continuous supremum. No rigorous-supremum or future-state coverage claim is made.',
 'E10':f"TESTED. Codex3 is root-approved in the dispatch and differs from the excluded lanes Claude2 and Codex2. Exact request schema, numeric_ref, point_sha256, custody_sha256 and adapter_sha256 are copied. Adapter SHA256 was recomputed from bytes as {bindings['adapter_sha256']}. FORMAL: the inspected adapter lines 182–188 require the approved review pin, schema/verdict, exact numeric/scope binding, numerical-convention acknowledgment and adapter byte hash. adapt-eps itself was not executed."
 }
 review={k:bindings[k] for k in ['schema','numeric_ref','point_sha256','custody_sha256','adapter_sha256']}
 review.update({'verdict':'APPROVED','accepts_registered_numerical_estimate_not_rigorous_sup':True,'reviewer_lane':'Codex3','distinct_from_producer_lane':True,'reviewed_utc':utc,'date_u':now,'checklist_results':checklist,'findings':(['NOTE E6: large eps_max; flag for root Q10, no magnitude-only rejection.'] if flagged else []),'signature':'Codex3, '+now,'evidence':{'checks':pin(cp),'inputs':c['inputs'],'references':refs},'E6_flagged':flagged})
 if 10<=row<=25:
  review['findings'].append('NOTE N1: the corresponding C0xx/C1xx pair has byte-identical 178-shell and 14-audit arrays. By-construction explanation is outside this review; root assigned it separately to Codex2.')
  review['evidence']['N1']=pin(O/'N1_PAIR_COMPARISON_CX3V001.json')
 raw=(json.dumps(review,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();assert b'<FILL' not in raw and b'TEMPLATE_NOT_A_REVIEW' not in raw
 dest=O/('EPS_REVIEW_CX3_'+key+'.json')
 with dest.open('xb') as f:f.write(raw)
 check=json.loads(dest.read_bytes())
 assert all(check[k]==bindings[k] for k in ['schema','numeric_ref','point_sha256','custody_sha256','adapter_sha256'])
 assert check['verdict']=='APPROVED' and check['reviewer_lane']=='Codex3' and check['accepts_registered_numerical_estimate_not_rigorous_sup'] is True
 item={'row':row,'key16':key,'review':pin(dest),'eps_max':m['eps_max'],'eps_max_shell':m['eps_max_shell'],'E6_flagged':flagged,'verdict':check['verdict']};reviews.append(item)
 print(json.dumps(item))
manifest={'schema':'CX3_EPS_BATCH_HANDOFF_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'batch':which,'reviews':reviews,'references':refs,'scope':'Offline saved EPS records only; no producer, adapter, launcher or forward execution.','peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
mp=O/('HANDOFF_'+which.upper()+'_CX3V001.json')
with mp.open('x') as f:json.dump(manifest,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
print(json.dumps({'handoff':pin(mp)}))
