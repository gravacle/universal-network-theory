"""Final BUILD custody/claim review; metadata and source bytes only."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
D=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3')
date_u=subprocess.check_output(['date','-u'],text=True).strip()
seen={};checks=[]
def read(p):
    s=str(p)
    assert s.startswith('/Users/bgm/Research/UNT_EXCHANGE/')
    assert not any(x in s.casefold() for x in ('/runs_ext/','kmax_a2f10_c5h_run_v001','/.codex/','/.codex-alt/'))
    raw=p.read_bytes();seen[s]={'path':s,'sha256':hashlib.sha256(raw).hexdigest()};return raw
def pin(p):read(p);return seen[str(p)]
def load(p):return json.loads(read(p))
def ck(name,truth,detail=None):checks.append({'name':name,'passed':bool(truth),'detail':detail})
build=BASE/'BUILD_V007.md';text=read(build).decode()
ck('selected_BUILD_exact_pin',seen[str(build)]['sha256']=='94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de')
allow=read(BASE/'ALLOWLIST_DRAFT_V006_CX3V001.txt').decode().splitlines()
index=load(BASE/'PRODUCER_INDEX_V009_CX3V001.json')
section=text.split('## Supported runtime entry allowlist\n',1)[1].split('## Byte-pinned selected packaging and evidence',1)[0]
rows=re.findall(r'^([0-9a-f]{64})  (/[^\n]+)$',section,re.M)
ck('exact15_literal_supported_lines',len(rows)==15 and [h+'  '+p for h,p in rows]==allow)
ck('BUILD_index_exact_path_hash_order',[{'path':p,'sha256':h} for h,p in rows]==index['supported_entries'])
ck('index_names_final_BUILD',index['build']==build.name)
oldallow=read(BASE/'ALLOWLIST_DRAFT_V005.txt').decode().splitlines()
ck('first13_supported_pairs_exact_V006',allow[:13]==oldallow[:13])
ck('only_selected_two_replacements',[Path(p).name for h,p in rows[13:]]==['postseal_records_cx1v006_cx3v001.py','srb_rot_record_cx1v008_cx3v001.py'])
citations=re.findall(r'^([0-9a-f]{64})  (/[^\n]+)$',text,re.M)
ck('BUILD_citation_paths_unique',len(citations)==len({p for _,p in citations}))
for expected,path in citations:ck('BUILD_citation_'+path,pin(Path(path))['sha256']==expected)
custody=load(D/'PARENT_CUSTODY_VERIFICATION_CX3V001.json')
ck('parent_custody_exact_pin',seen[str(D/'PARENT_CUSTODY_VERIFICATION_CX3V001.json')]['sha256']=='3a42862255ecc48ce37754098cabc55fd322151039ed595bdcd5be8b7c33239d')
ck('parent186_claim_and_status',custody['status']=='TESTED_PASS' and custody['count_unique_files']==len(custody['files'])==len({r['path'] for r in custody['files']})==186)
for row in custody['files']:ck('custody_'+row['path'],pin(Path(row['path']))['sha256']==row['sha256'])
baseline=load(D/'BASELINE_CUSTODY_CX3V001.json')
ck('baseline43_membership',baseline['count']==len(baseline['files'])==custody['baseline_count']==43 and all({'path':r['path'],'sha256':r['sha256']} in custody['files'] for r in baseline['files']))
focused=load(HERE.parent/'implementation/run_v001/RESULTS_CX3V001.json')
repro=load(HERE.parent/'implementation/repro_v001/RESULTS_CX3V001.json')
ind=load(D/'docs_plans/s1_independent/RESULTS_CX3V001.json')
delta=load(D/'docs_plans/s1_independent/SOURCE_DELTA_CX3V002.json')
docs=load(D/'docs_plans/VERIFICATION_CX3V001.json')
own=load(HERE/'RESULTS_CX3V001.json')
for name,obj,expected,key in [('author_main',focused,92,'tests_passed'),('predecessor_repro',repro,14,'checks_passed'),('independent_runtime',ind,37,'passed'),('source_delta',delta,6,'passed'),('author_docs',docs,181,'passed'),('independent_docs',own,136,'passed')]:
    ck('BUILD_suite_claim_'+name,obj['status']=='TESTED_PASS' and obj[key]==expected and all(x['passed'] if 'passed' in x else x['pass'] for x in obj['checks']))
rss=[focused['rss_bytes_macos'],ind['peak_rss_bytes'],docs['peak_rss_bytes'],own['rss_bytes_macos']]
ck('observed_RSS_claim_under41MB',max(rss)<41_000_000,rss)
for name,needles in {
 'test_scope':('separate suites with overlapping coverage','not one count of independent scientific checks','explicitly stubbed comparator admission/gates','extracted parser/publication statements'),
 'historical_test_counts':('historical 21/28/56/7/11 totals were not rerun',),
 'pending_authority':("Claude4's external delta review",'Claude2\'s scientific acceptance remain pending','UNTESTED: production scientific execution'),
 'publication_limit':('does not promise atomicity against operating-system failure',),
 'operational_limit':('unbound PENDING templates','root must verify its final internal output filesystem','hardware SSD properties were not independently queried successfully'),
 }.items():ck('BUILD_scope_'+name,all(n in text for n in needles))
ck('no_cyclic_BUILD_reference_in_cited_docs',all(seen[str(build)]['sha256'] not in read(BASE/n).decode() for n in ('RUNBOOK_V008_CX3V001.md','ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md')))
ck('BUILD_unchanged_after_review',pin(build)['sha256']=='94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de')
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
result={'date_u':date_u,'status':'TESTED_PASS','checks_passed':len(checks),'checks_total':len(checks),'checks':checks,'BUILD':pin(build),'harness':pin(Path(__file__)),'direct_BUILD_citation_count':len(citations),'parent_custody_unique_count':186,'baseline_count':43,'observed_claims_only':'Suites are verified from pinned final evidence, not rerun. No production imports or executable invocation. Embedded legacy run strings are never followed.','all_read_pins':list(seen.values())}
result['harness_note']='Initial v001 verifier assumed every check uses passed; other author evidence uses pass. v002 then compared entire baseline entries although those include extra size metadata. Both stopped before output. v003 reads each explicit check schema and compares baseline path/SHA pairs. No source, evidence or BUILD changed. Parent separately corrected an absolute-index-name assumption; this verifier accepts the established relative BUILD_V007.md convention.'
p=HERE/'FINAL_BUILD_VERIFICATION_CX3V003.json'
with p.open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'BUILD_citations':len(citations),'result_path':str(p),'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'harness_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}))
