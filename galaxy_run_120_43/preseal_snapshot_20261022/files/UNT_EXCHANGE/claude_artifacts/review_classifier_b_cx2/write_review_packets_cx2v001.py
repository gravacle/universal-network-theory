"""Exclusive-create final review artifacts. A material stays in A_SIDE."""
import hashlib
import json
import subprocess
from pathlib import Path

E=Path('/Users/bgm/Research/UNT_EXCHANGE')
A=E/'claude_artifacts'
R=A/'review_classifier_b_cx2'
SIDE=R/'A_SIDE'
B=A/'classifier_b_c2/build_c2v005'
AC=A/'classifier_a_c4'
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def cite(p,line=None):
    return '`%s%s` — sha256 `%s`'%(p,(':'+str(line)) if line else '',sha(p))

def put(p,d):
    with p.open('x') as f:
        if isinstance(d,str):f.write(d)
        else:json.dump(d,f,indent=2);f.write('\n')

shared=json.loads((SIDE/'SHARED_BLACKBOX_RESULTS_CX2V001.json').read_bytes())
own=[json.loads((SIDE/('OWN_BLACKBOX_RESULTS_CX2V%03d.json'%v)).read_bytes()) for v in (1,2)]
different=[r for r in shared['rows'] if not r['equal_except_identity']]
assert [r['id'] for r in different]==['B352','B407','B412','B419']
assert shared['n']==368 and shared['agree']==364
assert all(x['differences']==0 for x in own) and sum(x['n'] for x in own)==14
assert all(run['exit']==0 for rec in [shared]+own for row in rec['rows'] for run in row['runs'])

reasons={
 'B352':('C-6.3 receipt rule; producer STAGE0 validator L3999-L4009',
          'The frozen block says EVALUATED_BEFORE_FREEZE while the declared/scored STAGE0 alternative remains NOT_EVALUATED_BEFORE_FREEZE and unscored. The producer rejects the inconsistent block/alternative status. This is not an honest producer output.'),
 'B407':('C-1.1 reference member; A190 ruling 1; v003g scorer L4228',
          'The frozen reference member ID is absent from the frozen member list. A verified producer manifest cannot supply this form. The difference is the exception class printed for synthetic-score construction.'),
 'B412':('C-4 and A190 ruling 1; v003g _score_members L4040-L4045',
          'The score registered_reason differs from the frozen row_registration reason. The producer copies that exact frozen reason into the score. The difference is downstream placement of the unavailable per-reason count.'),
 'B419':('C-1.1 L1 column; A190 ruling 2; full phase1 producer pin',
          'The supplied tool hash is a fabricated prefix-only pin (7d891ff7 followed by ab pairs), and the L1 file hash is also fabricated. The difference concerns precedence of two malformed-pin diagnostic words. No correct pinned producer form has either defect.')
}
note='# Shared differences: reviewer-only A-side record\n\n'
note+=f'date -u: {DATE}\n\nTESTED: 368 shared unmodified-CLI comparisons; 364 agree and four differ. Only the top-level classifier identity was masked. All four are forged-only A115 NOTEs; no honest-form disagreement was found. No producer was executed.\n\n'
note+='Aggregate: '+cite(SIDE/'SHARED_BLACKBOX_RESULTS_CX2V001.json')+'\n\n'
for row in different:
    cid=row['id'];clause,why=reasons[cid]
    note+=f'## {cid}: forged-only NOTE\n\nContract: {clause}. {why}\n\n'
    note+='TESTED differences:\n\n```json\n'+json.dumps(row['differences'],indent=2)+'\n```\n\n'
    note+='Bundle: '+cite(Path(row['bundle']['path']))+'\n\n'
    note+='A output: '+cite(Path(row['A']['path']))+'\n\nB output: '+cite(Path(row['B']['path']))+'\n\n'
note+='Producer and contract evidence:\n\n'
for p in [A/'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
          A/'stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py',
          AC/'build_c4v001/basis/PREREG_MISS_READING_R3A.md',R/'AUTHORIZED_RULINGS_CX2V001.json']:
    note+='- '+cite(p)+'\n'
put(SIDE/'FORGED_ONLY_NOTES_CX2V001.md',note)

anote='# A-side review note for Claude4 only\n\n'
anote+=f'date -u: {DATE}\n\nA_DEFECT count: **0**. TESTED: all 14 independently authored classifier-form cases agree between the unmodified CLIs. Four shared-suite differences are forged-only; see '+cite(SIDE/'FORGED_ONLY_NOTES_CX2V001.md')+'.\n\n'
anote+='One reporting contract ambiguity (CA1) remains for root to rule in contract terms. The text asks for the STAGE0 member distribution, especially for an invalid twin, whereas the adopted output schema fixes a twin-row-count object. These probes do not demonstrate a changed classification, row reading, gate or blinding outcome. This is not counted as an A_DEFECT before the contract is resolved.\n\n'
for row in own[1]['rows']:
    anote+='Case '+row['id']+': '+cite(Path(row['bundle']['path']))+'\n\nA output: '+cite(Path(row['A']['path']))+'\n\n'
    data=json.loads(Path(row['A']['path']).read_bytes())
    anote+='TESTED A stage0 reporting fields:\n\n```json\n'+json.dumps({
        'status':data['stage0']['status'],'twin':data['stage0'].get('twin'),
        'stage0_within_error_distribution':data['stage0'].get('stage0_within_error_distribution'),
        'alternative_entry':data['alternatives'][-1]},indent=2)+'\n```\n\n'
anote+='Independent comparison records:\n\n'
for v in (1,2):anote+='- '+cite(SIDE/('OWN_BLACKBOX_RESULTS_CX2V%03d.json'%v))+'\n'
anote+='\nContract: '+cite(AC/'build_c4v001/basis/PREREG_MISS_READING_R3A.md',521)+'; '+cite(AC/'schema_c4v003/OUTPUT_SCHEMA_C4V003.json',6832)+'.\n'
put(SIDE/'A_DEFECTS_FOR_CLAUDE4_CX2V001.md',anote)

# Only counts cross from the A-side comparisons into the root-facing records.
counts={'shared_cases':shared['n'],'shared_agree':shared['agree'],'shared_forged_only_differences':len(different),
        'own_cases':sum(x['n'] for x in own),'own_agree':sum(x['agree'] for x in own),
        'honest_form_disagreements':0,'A_DEFECT':0,'B_DEFECT':0,'CONTRACT_AMBIGUITY':1,'blocking':0}
suite=[]
for v in (1,2):
    p=R/('B_suite_run_%d_cx2v001/SUITE_RESULTS_CX2V001.json'%v)
    d=json.loads(p.read_bytes());assert d['n_cases']==d['n_pass']==327
    log=R/('B_suite_run_%d_cx2v001/READ_LOG_CX2V001.json'%v)
    ld=json.loads(log.read_bytes());assert ld['refused_opens']==[] and ld['exit_code']==0
    suite.append({'run':v,'n':327,'pass':327,'results':{'path':str(p),'sha256':sha(p)},
                  'read_log':{'path':str(log),'sha256':sha(log)}})
checks=json.loads((R/'OWN_CONTRACT_CHECKS_CX2V001.json').read_bytes())
assert checks['checks']==checks['passed']==158 and not checks['failed']
audit=json.loads((R/'READ_LOG_AND_KERNEL_AUDIT_CX2V001.json').read_bytes())
assert audit['all_kernels_match'] and len(audit['kernel_checks'])==15 and not audit['forbidden_A_code_or_outputs_logged']

evidence=[
 B/'classifier_b_c2v005.py',B/'README_CLASSIFIER_B_C2V005.md',B/'READ_LOG.txt',
 B/'OUTPUT_SCHEMA_C2V005_DERIVED.json',B/'suite/run_suite_c2v005.py',B/'suite/case_defs_c2v005_v8.py',
 AC/'build_c4v001/basis/PREREG_MISS_READING_R3A.md',
 AC/'build_c4v001/basis/ROOT_ITEMS_R3A.md',AC/'build_c4v001/basis/CLAUSE_SOURCE_MAP_R3A.md',
 AC/'contracts_c4v004/INPUT_CONTRACTS_C4V004.md',AC/'schema_c4v003/OUTPUT_SCHEMA_C4V003.json',
 A/'miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md',
 A/'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
 A/'phase1_c2/phase1_c2v003b.py',A/'phase1_c2/phase1_c2v002.py',
 A/'stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py',
 E/'FROM_CODEX/0767_2026-10-20_codex2_A205_queue_P106_classifierB_launcher_v004_G26.md',
 R/'AUTHORIZED_RULINGS_CX2V001.json',R/'READ_LOG_AND_KERNEL_AUDIT_CX2V001.json',
 R/'run_B_suite_guarded_cx2v001.py',R/'build_own_bundles_cx2v001.py',
 R/'build_own_bundles_cx2v002.py',R/'build_own_bundles_cx2v003.py',
 R/'build_member_distribution_cases_cx2v001.py',R/'check_own_contract_cx2v001.py',
 R/'OWN_BUNDLE_INDEX_CX2V001.json',R/'OWN_BUNDLE_INDEX_CX2V002.json',R/'OWN_CONTRACT_CHECKS_CX2V001.json'
]
for x in suite:evidence.extend([Path(x['results']['path']),Path(x['read_log']['path'])])
for name in ['own_bundles_cx2v001','own_bundles_cx2v002','B_shared_outputs']:
    evidence.extend(p for p in (R/name).rglob('*') if p.is_file())
manifest={'date_u':DATE,'label':'TESTED byte hashes',
          'files':[{'path':str(p),'sha256':sha(p)} for p in sorted(set(evidence))],
          'barrier':'Contains no A output or per-bundle comparison. A_SIDE is excluded.'}
put(R/'B_EVIDENCE_MANIFEST_CX2V001.json',manifest)

ca1={
 'id':'CA1','classification':'CONTRACT_AMBIGUITY','blocking':False,
 'title':'STAGE0 member distribution disclosure versus the fixed twin-count output form',
 'contract':'C-6.1 requires the scored member distribution when the twin is invalid. C-6.3 final sentence asks for the STAGE0 member within-error distribution. The adopted output schema instead defines stage0_within_error_distribution as n=8 and the reference twin HIT count, and omits it on TWIN_INVALID.',
 'producer_form':'score.alternatives[] carries member_within_error_counts from the distribution over all scored members (v003g L4289-L4294).',
 'tested':'Two member counts [8,3] give producer-form n=2,min=3,median=5.5,max=8; B reports only n=8,within_error=8. For an invalid reference twin with member counts [0,3], B reports TWIN_INVALID and no member distribution. Both are classified without stops; R-DRIFT remains OPEN in the invalid-twin case.',
 'B_locations':[{'path':str(B/'classifier_b_c2v005.py'),'sha256':sha(B/'classifier_b_c2v005.py'),'line':2222},
                {'path':str(B/'classifier_b_c2v005.py'),'sha256':sha(B/'classifier_b_c2v005.py'),'line':2208}],
 'ruling_needed':'Clarify whether C-6 requires echoing the all-member distribution, with a synchronized text/schema correction or report field if so. The existing twin-row count may remain separately named.',
 'A115':'Nonblocking reporting ambiguity: no wrong classification, reason, row reading, physics/gate/blinding effect demonstrated.',
}
result={
 'date_u':DATE,'label':'TESTED plus FORMAL code/contract review',
 'verdict':'PASS_FOR_CLASSIFICATION_WITH_NONBLOCKING_CONTRACT_AMBIGUITY',
 'counts':counts,'B_source':{'path':str(B/'classifier_b_c2v005.py'),'sha256':sha(B/'classifier_b_c2v005.py')},
 'suite_runs':suite,'independent_clause_checks':{'n':158,'passed':158,
  'path':str(R/'OWN_CONTRACT_CHECKS_CX2V001.json'),'sha256':sha(R/'OWN_CONTRACT_CHECKS_CX2V001.json')},
 'B_DEFECTs':[],'CONTRACT_AMBIGUITIES':[ca1],
 'A_DEFECT_note':{'count':0,'path':str(SIDE/'A_DEFECTS_FOR_CLAUDE4_CX2V001.md'),
                  'sha256':sha(SIDE/'A_DEFECTS_FOR_CLAUDE4_CX2V001.md')},
 'kernel_and_barrier_audit':{'kernels_unchanged':15,'logged_forbidden_A_code_or_output_reads':0,
  'path':str(R/'READ_LOG_AND_KERNEL_AUDIT_CX2V001.json'),'sha256':sha(R/'READ_LOG_AND_KERNEL_AUDIT_CX2V001.json')},
 'disclosures':[
  'Codex2 wrote neither classifier, these kernels nor these producer modules; same model family as Codex1 kernels, different lane.',
  'v003g L188 takes its FORBIDDEN set from prior Codex2 P46 code; this review did not open that older harness.',
  'B suite uses its declared seams for 311 cases and 16 as-shipped cases; all 368 shared and 14 own comparisons ran unmodified CLI binaries.',
  'B suite compare path redirected only to the byte-identical permitted B340 suite copy; original compare file was not opened.',
  'Own fixtures reuse permitted root-control scaffolding; substantive member/score/band/AT1 records are hand-built. No producer executed.',
  'Builder v001 and v002 were never executed; v003 preserves control bytes and producer canonical JSON. Original drafts retained.',
  'Exact isolated Python and six one-thread environment variables used. nice -n 10 was attempted but setpriority was denied by the sandbox.',
 ],
 'UNTESTED':[
  'No actual run, receipt, real manifest, real score, observed or target velocities were opened.',
  'Synthetic fixtures are honest classifier record forms, not a claim of full production freeze custody verification.',
  'Supplied historical READ_LOG audit is not independent historical process telemetry; suite guard covers parent, not child process opens.',
  'No scientific launch, production scoring or adoption decision was performed.',
 ],
 'evidence_manifest':{'path':str(R/'B_EVIDENCE_MANIFEST_CX2V001.json'),'sha256':sha(R/'B_EVIDENCE_MANIFEST_CX2V001.json')}}
put(R/'RESULT_CX2V001.json',result)

review='# Classifier B c2v005 — Codex2 distinct-lane review\n\n'
review+=f'date -u: {DATE}\n\n**PASS for classification; zero blocking findings.** One nonblocking contract ambiguity (CA1) requires a reporting ruling. B_DEFECT count 0; CONTRACT_AMBIGUITY count 1; A_DEFECT count 0. This record makes no adoption or launch decision.\n\n'
review+='Object: '+cite(B/'classifier_b_c2v005.py')+'. Dispatch: '+cite(E/'FROM_CODEX/0767_2026-10-20_codex2_A205_queue_P106_classifierB_launcher_v004_G26.md')+'.\n\n'
review+='## Evidence\n\n'
review+='- TESTED: B suite 327/327 twice. The suite retains its declared 311 seamed and 16 as-shipped cases. The wrapper only redirects the compare input to byte-identical permitted suite bytes; both parent read logs have zero refused opens.\n'
review+='- TESTED: shared unmodified CLI runs agree on 364/368 cases; four differences are forged-only A115 NOTEs. Independent hand-built classifier-form cases agree on 14/14; zero honest-form disagreements. All per-case comparisons and all A outputs remain in A_SIDE.\n'
review+='- TESTED: 158/158 independent B clause checks across 14 own cases: thresholds, null-ratio unsigned misses, per-row registration, global/mixed patterns, L1 availability/noise/inclusive overlap, eight-row STAGE0 comparison, invalid twin, no successor and AT1 failure consequences.\n'
review+='- TESTED static: 15/15 Codex1 kernels match their V089 pins and current upstream bytes. The supplied 894-entry B read log records zero forbidden A-code/suite-code/output reads. This is an audit of the supplied record, not historical process telemetry.\n\n'
review+='## Focused code review\n\n'
review+='FORMAL: reviewed B against the contract and pinned producer bytes, with attention to score alternatives[]/NON_PRIMARY, full-length frozen row_registration, scoped STAGE0 score arrays, exact successor block/member keys, receipt-time equality, L1 source/full-hash binding and column-only failures, and AT1 record forms/Phase-2 precedence. Source producer code was read, never imported or executed. B reads the frozen registered reason and gate status per member; null ratios remain unsigned misses; a twin gets neither NEAR nor TSR. STAGE0 comparison uses only jointly valid signed rows and does not alter the headline. The below reporting ambiguity is the sole unresolved item identified.\n\n'
review+='## CA1 — nonblocking reporting contract ambiguity\n\n'
review+=ca1['contract']+'\n\n'+ca1['producer_form']+'\n\nTESTED: '+ca1['tested']+'\n\n'
review+='B locations: '+cite(B/'classifier_b_c2v005.py',2222)+'; invalid-twin early return at line 2208. Contract basis: '+cite(AC/'build_c4v001/basis/PREREG_MISS_READING_R3A.md',521)+' and line 581; fixed form: '+cite(AC/'schema_c4v003/OUTPUT_SCHEMA_C4V003.json',6832)+'. The seal-candidate text also retains the member-distribution wording: '+cite(A/'miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md',579)+'.\n\n'
review+=ca1['ruling_needed']+' '+ca1['A115']+'\n\n'
review+='B-only reproductions and expected input counts: '+cite(R/'OWN_BUNDLE_INDEX_CX2V002.json')+'; '+cite(R/'OWN_CONTRACT_CHECKS_CX2V001.json')+'. All input and output hashes are in the evidence manifest below.\n\n'
review+='## Barrier and limits\n\n'
review+='A_DEFECT count: **0**. Claude4-only note: '+cite(SIDE/'A_DEFECTS_FOR_CLAUDE4_CX2V001.md')+'. Root and any B successor builder must not open A_SIDE.\n\n'
review+='Disclosures: Codex2 is a different lane but the same model family as Codex1, who wrote the kernels. v003g L188 depends on the FORBIDDEN name set from prior Codex2 P46 work. Neither dependency is claimed independent lineage. The own cases reuse permitted root-record scaffolding; their member, score, band and AT1 records were independently authored from source forms. Full production freeze custody is UNTESTED. No producer execution or real scientific data access occurred. Exact isolated Python with six thread variables set to one was used; nice was attempted but the sandbox denied setpriority.\n\n'
review+='The root-facing artifacts contain only comparison counts; forged-only details and every per-bundle comparison are confined to A_SIDE. No reviewed file was edited. Builder drafts v001/v002 remain unexecuted and immutable; v003 generated the final case set. Suite parent guards logged zero refusals; child CLI opens were not independently traced.\n\n'
review+='## Hash-linked records\n\n'
for p in [R/'RESULT_CX2V001.json',R/'B_EVIDENCE_MANIFEST_CX2V001.json',
          R/'READ_LOG_AND_KERNEL_AUDIT_CX2V001.json',R/'AUTHORIZED_RULINGS_CX2V001.json',
          R/'OWN_BUNDLE_INDEX_CX2V001.json',R/'OWN_BUNDLE_INDEX_CX2V002.json',
          R/'OWN_CONTRACT_CHECKS_CX2V001.json']+[
          Path(x[k]['path']) for x in suite for k in ('results','read_log')]:
    review+='- '+cite(p)+'\n'
put(R/'REVIEW_CLASSIFIER_B_C2V005_CX2V001.md',review)

packet=f"""# 0537 — A205 part 2 classifier B review finished

date -u: {DATE}

To: Claude2 (coordinator). From: Codex2.

**PASS for classification; 0 blocking.** TESTED: B's suite 327/327 twice; shared CLI comparisons 364/368 agree, with 4 forged-only A115 NOTEs; 14/14 own classifier-form comparisons agree; 158/158 independent B clause checks; 15/15 kernel pins unchanged. B's supplied read log records no forbidden A source/suite/output reads. B_DEFECT count 0; CONTRACT_AMBIGUITY count 1.

**CA1, nonblocking, contract terms only.** C-6.1 requires the scored member distribution when the alternative twin is invalid; C-6.3 calls for the STAGE0 member within-error distribution. B's fixed output instead prints only the reference twin's hit count at line 2222 and omits the distribution on its invalid-twin return at line 2208. The adopted schema explicitly describes that twin-count form. TESTED with honest classifier-form member counts [8,3] and [0,3]; classification and invalid-twin OPEN behavior remain correct. Please rule whether the text requires the all-member distribution and align the reporting contract/schema accordingly. No classification, reason, row-reading, physics, gate or blinding effect demonstrated; no Phase-1 hold asserted.

{cite(B/'classifier_b_c2v005.py',2222)}

{cite(AC/'build_c4v001/basis/PREREG_MISS_READING_R3A.md',521)}

{cite(AC/'schema_c4v003/OUTPUT_SCHEMA_C4V003.json',6832)}

A_DEFECT count: **0**. Claude4-only path: {cite(SIDE/'A_DEFECTS_FOR_CLAUDE4_CX2V001.md')}. Root and B successor builders do not open A_SIDE.

Review: {cite(R/'REVIEW_CLASSIFIER_B_C2V005_CX2V001.md')}

Result: {cite(R/'RESULT_CX2V001.json')}

B-only evidence hashes: {cite(R/'B_EVIDENCE_MANIFEST_CX2V001.json')}

Disclosures: same model family as the Codex1 kernel author; v003g's FORBIDDEN set derives from prior Codex2 P46 work. Suite seams and reused synthetic control scaffolding are disclosed in the review. No producer executed. Production custody/scientific runs remain UNTESTED. nice was attempted but setpriority denied.

Parts 1, 2 and 4 are finished. Awaiting both part-3 start conditions and the scheduled part-5 build; minute inbox polling continues. No launches.
"""
out=E/'FROM_CODEX2/0537_2026-10-20_classifier_B_review_finished_zero_blocking_CA1.md'
put(out,packet)
print(json.dumps({'packet':str(out),'sha256':sha(out),'review_sha256':sha(R/'REVIEW_CLASSIFIER_B_C2V005_CX2V001.md'),
                  'result_sha256':sha(R/'RESULT_CX2V001.json'),'counts':counts}))
