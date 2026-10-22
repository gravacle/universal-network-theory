"""Cross-lineage prereg r5 custody/text checks; no reviewed code execution."""
from pathlib import Path
import copy,hashlib,json,os,re,resource,subprocess,sys
HERE=Path(__file__).resolve().parent
E=Path('/Users/bgm/Research/UNT_EXCHANGE');B=E/'claude_artifacts/v007_final_prereg_c4/r5'
DATE=subprocess.check_output(['date','-u'],text=True).strip();pins={};checks=[];denials=[]
def blocked(s):
    s=str(s).casefold()
    return '/runs_ext/' in s or 'kmax_a2f10_c5h_run_v001' in s or '/.codex/' in s or '/.codex-alt/' in s
def audit(event,args):
    if event in ('subprocess.Popen','os.system','socket.__new__','socket.connect'):denials.append(event);raise PermissionError('NO_EXECUTION')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        s=os.fsdecode(args[0]);assert not blocked(s)
        flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):assert str(Path(s).absolute()).startswith(str(HERE)+'/') and flags&os.O_EXCL
sys.addaudithook(audit)
def read(p):
    assert str(p).startswith(str(E)+'/') and not blocked(p)
    raw=p.read_bytes();pins[str(p)]={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)};return raw
def pairs(items):
    out={}
    for k,v in items:
        if k in out:raise ValueError('DUPLICATE_KEY')
        out[k]=v
    return out
def load(p):return json.loads(read(p),object_pairs_hook=pairs)
def ck(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
def section_map(raw):
    headings=list(re.finditer(rb'^## (A\d+):[^\n]*',raw,re.M));out={}
    for h in headings:
        at=raw.find(b'\n## ',h.end());end=len(raw) if at<0 else at+1
        key=h.group(1).decode();assert key not in out
        out[key]=(h.group().decode(),raw[h.start():end])
    return out
def validate_entries(obj,raw):
    table=obj['entries_after_A81'];rows=table['rows'];expected=['A'+str(i) for i in range(82,102)]
    if [r['entry'] for r in rows]!=expected:raise ValueError('ENTRY_COVERAGE_OR_ORDER')
    if hashlib.sha256(raw).hexdigest()!=table['addendum_read']['sha256_at_generation'] or len(raw)!=table['addendum_read']['bytes']:raise ValueError('SNAPSHOT_CUSTODY')
    secs=section_map(raw)
    for r in rows:
        heading,sec=secs[r['entry']]
        if r['heading']!=heading or hashlib.sha256(sec).hexdigest()!=r['section_sha256'] or len(sec)!=r['section_bytes']:raise ValueError('ENTRY_SECTION_HASH')
        if r['decision']=='NO_CHANGE':
            if not r.get('reason','').startswith('no change, because ') or r['revised_clauses']:raise ValueError('NO_CHANGE_REASON')
        elif r['decision']=='REVISED_HERE':
            if not r.get('scope') or not r['revised_clauses']:raise ValueError('REVISED_SCOPE_CLAUSES')
        else:raise ValueError('ENTRY_DECISION')
    return True
def resolve(obj,path):
    tokens=re.findall(r'[^.\[\]]+',path);cur=obj
    for t in tokens:
        if isinstance(cur,list):cur=next(x for x in cur if x.get('id')==t) if not t.isdigit() else cur[int(t)]
        else:cur=cur[t]
    return cur
def expected_fail(name,fn):
    try:fn()
    except (ValueError,KeyError,AssertionError) as e:ck(name,True,type(e).__name__+': '+str(e));return
    ck(name,False,'Mutation accepted')

dispatch=E/'FROM_CODEX/0628_2026-10-18_codex3_next_prereg_r5_tools_v002_review.md';read(dispatch)
ck('dispatch_pin',pins[str(dispatch)]['sha256']=='9586ad51802e8f5cdce79e35d09c29b331f8381a6f4e0cfb641bee98fe9c0628')
jpath=B/'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json';obj=load(jpath);md=read(B/'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md').decode();tablemd=read(B/'ENTRY_TABLE_R5.md').decode();checklist=read(B/'SEAL_CHECKLIST_R5.md').decode();rootitems=read(B/'ROOT_ITEMS_R5.md').decode();sourcemap=read(B/'CLAUSE_SOURCE_MAP_R5.md').decode();delta=read(B/'DELTA_R4_R5.md').decode();erratum=read(B/'DELTA_R4_R5_ERRATUM_E1.md').decode()
ck('selected_json_pin',pins[str(jpath)]['sha256']=='3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393')
ck('selected_md_pin',pins[str(B/'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md')]['sha256']=='2ed287717a831b422d93ad62339a85aa5b1ffbc570d39bd3ddc6066e8989c208')
snapshot=read(B/'addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md');sections=section_map(snapshot)
ck('all20_entries_verified',validate_entries(obj,snapshot))
ck('snapshot_exact_headers82_101',{a for a in sections if 82<=int(a[1:])<=101}=={'A'+str(i) for i in range(82,102)})
ck('no_missing_decimal_entry',not re.search(rb'^## A(?:8[2-9]|9\d|10[01])\.\d',snapshot,re.M))
for readmeta in obj['assembly']['rulings_read']['V005_addendum_reads']:
    if 'copy' in readmeta:
        raw=read(Path(readmeta['copy']));ck('snapshot_copy_'+Path(readmeta['copy']).name,hashlib.sha256(raw).hexdigest()==readmeta['sha256'])
rows=obj['entries_after_A81']['rows'];ck('16revised_4nochange',sum(r['decision']=='REVISED_HERE' for r in rows)==16 and [r['entry'] for r in rows if r['decision']=='NO_CHANGE']==['A84','A85','A95','A98'])
old=load(Path(obj['assembly']['base']['path']))
for r in rows:
    key=r['entry'];sec=sections[key][1];ck(key+'_heading_hash_length',hashlib.sha256(sec).hexdigest()==r['section_sha256'] and len(sec)==r['section_bytes'])
    words='revised here' if r['decision']=='REVISED_HERE' else 'no change'
    ck(key+'_entry_markdown_row',f"| {key} | {words} | `{r['section_sha256']}` |" in tablemd and (r.get('scope') or r.get('reason')) in tablemd)
    ck(key+'_prereg_markdown_row',f"| {key} | {words} | `{r['section_sha256'][:16]}...` |" in md)
    for clause in r['revised_clauses']:
        if clause.startswith('SEAL_CHECKLIST_R5'):
            ck(key+'_checklist_named_'+clause,all(re.search(r'\b'+re.escape(step)+r'\.',checklist) or step=='DONE' for step in re.findall(r'\b(?:A\d+|B\d+[a-z]?|DONE)\b',clause)))
        else:
            value=resolve(obj,clause);ck(key+'_clause_present_'+clause,value is not None)
            try:before=resolve(old,clause);changed=before!=value
            except (KeyError,IndexError,StopIteration):changed=True
            ck(key+'_named_clause_changed_'+clause,changed)

# MD is an explicitly partial rendering of the full JSON. Verify all clauses it
# actually renders, rather than pretending it independently contains the full text.
ck('markdown_admits_full_text_in_json','The full clause text is in the JSON' in md)
ck('status_MD_JSON_exact',obj['status'] in md and obj['revision']=='r5' and 'NOT SEALED' in obj['status'])
for key,slot in obj['seal_slots'].items():
    ck('MD_JSON_slot_'+key,f'**{key}**' in md and f"value `{slot['value']}`" in md and slot['rule'] in md)
for i,row in enumerate(obj['seal_record_requirements']):ck('MD_JSON_seal_requirement_'+str(i),row['text'] in md and '; '.join(row['sources']) in md)
ck('cache_explicit_r5_not_sealed',obj['seal_slots']['cache_directory_r6_only']['value']=='NOT_APPLICABLE_R5' and all(v['value']=='PENDING_ROOT_AT_SEAL_ASSEMBLY' for k,v in obj['seal_slots'].items() if k!='cache_directory_r6_only'))

launch=obj['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']
build=launch['build'];ck('BUILD_required_full_hash',build['sha256']=='94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de' and hashlib.sha256(read(Path(build['path']))).hexdigest()==build['sha256'] and build['sha256'] in md)
for k,v in launch.items():
    if isinstance(v,dict) and set(v)=={'path','sha256'}:ck('launch_named_pin_'+k,hashlib.sha256(read(Path(v['path']))).hexdigest()==v['sha256'])
blockpin=obj['binding_inputs']['case_block'];blockraw=read(Path(blockpin['path']));block=json.loads(blockraw,object_pairs_hook=pairs)
ck('caseblock_required_full_hash',blockpin['sha256']=='76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71' and hashlib.sha256(blockraw).hexdigest()==blockpin['sha256'] and blockpin['sha256'] in md)
plan=load(Path(launch['template_plan']['path']));labels={x['case'] for x in plan['calls']}
ck('caseblock_ten_T_and_declaration_only',len(labels)==10 and set(block['cases'])==labels|{'C5H'} and block['schema']=='UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003' and block['route_a_mode']=='parallel8' and block['key_equivalence_map']==[])
for c in labels:
    value=block['cases'][c];ni=value['normalized_spec_equal']['/numerics']
    ck('caseblock_'+c+'_r5_tail_ms128',value['tail'] is True and value['ro1_required'] is True and value['drivers_allowed']==['b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'] and ni['uv_tail']['gas']['M_s']==128)
ck('caseblock_C5H_only_spec_metadata',block['cases']['C5H']['call_spec_sha256'].startswith('60b46130') and block['cases']['C5H']['drivers_allowed'][0].startswith('999331af'))

# Cross-check the complete per-entry semantic disposition against the inspected
# pinned ruling text; no source programs or comparison gates run here.
semantic={
 'A82':('seal_slots.compare',('reviewed source','only in those pin lines','A82')),
 'A83':('seal_slots.identity_comparator',('Codex2','check of record','stopped')),
 'A86':('gates_before_any_T_result.GQ',('GQ_CERT_V006','5a1b39f8')),
 'A87':('gates_before_any_T_result.DOUBLING',('DOUBLING_MERGED_C3V001','ea48ac2b')),
 'A88':('tests.SR_K',('after the seal','before any T')),
 'A89':('run_list.cpu_hours_estimate_UNTESTED',('7.84','13.86','UNTESTED')),
 'A90':('gates_before_any_T_result.LO_NGC',('LO_NGC_K32_CERT_V001','LO_NGC_CERT_V002')),
 'A91':('seal_slots.identity_comparator',('identity_sha256','caller.sha256','present')),
 'A92':('seal_slots.identity_gate_records',('R5_V001','c2v007r2')),
 'A93':('not_v007_text_scope',('cd30429c','A93')),
 'A94':('gates_before_any_T_result.B2',('le3 for every case','P16','ROOT_ITEM')),
 'A96':('fixed_across_all_cases.production_tail.tail_table_cache',('r5','moot','A96')),
 'A97':('gates_before_any_T_result.B2',('0.05','INCOMPLETE','fails B2')),
 'A99':('seal_record_requirements[11]',('A82','A101','section sha256','quotes it')),
 'A100':('gates_before_any_T_result.B2',('0.0301','0.0356','0.0384','does not prove shared physical correctness')),
 'A101':('seal_record_requirements[12]',('C3V003-RI-1','3.83e-11','erratum')),
}
for key,(path,tokens) in semantic.items():
    text=json.dumps(resolve(obj,path),ensure_ascii=False)
    ck(key+'_semantic_clause_trace',all(t in text for t in tokens),{'path':path,'required':tokens})
for key,tokens in {'A84':('schedules','A96'),'A85':('RUNBOOK','BUILD_V007','A72'),'A95':('preferred','single-thread','RUNBOOK'),'A98':('NGC','step 5','step-6')}.items():
    row=next(r for r in rows if r['entry']==key);ck(key+'_no_change_reason_trace',all(t in row['reason'] for t in tokens))

authoraudit=load(B/'out/AUDIT_R5_VS_R4_C4V001.json')
ck('historical_delta_failure_disclosed',authoraudit['verdict']=='FAIL' and len(authoraudit['uncovered_differing_leaves'])==3 and all(s in erratum for s in ('revision','supersedes_draft.path','supersedes_draft.sha256','1039','1036','JSON is unchanged')))
ck('r5_root_pending_not_adopted','OPEN: RI-28' in md and 'PENDING_ROOT_RULING' in checklist and 'Claude4 delta check and Claude2 adoption pending' in md)
for line in read(B/'HASHES_R5.txt').decode().splitlines():
    h,p=line.split('  ',1);ck('r5_manifest_'+Path(p).name,hashlib.sha256(read(Path(p))).hexdigest()==h)

# In-memory integrity canaries for this independent checker; not claimed as
# seal-tool tests. Every mutation must fail before any output/production access.
for tag,mutate in [('missing_entry',lambda x:x['entries_after_A81']['rows'].pop()),('duplicate_entry',lambda x:x['entries_after_A81']['rows'].__setitem__(1,copy.deepcopy(x['entries_after_A81']['rows'][0]))),('wrong_section_hash',lambda x:x['entries_after_A81']['rows'][0].__setitem__('section_sha256','0'*64)),('unknown_decision',lambda x:x['entries_after_A81']['rows'][0].__setitem__('decision','PASS')),('nochange_no_reason',lambda x:x['entries_after_A81']['rows'][2].__setitem__('reason','')),('revised_no_clauses',lambda x:x['entries_after_A81']['rows'][0].__setitem__('revised_clauses',[]))]:
    x=copy.deepcopy(obj);mutate(x);expected_fail('MUST_FAIL_'+tag,lambda x=x:validate_entries(x,snapshot))
expected_fail('MUST_FAIL_changed_snapshot',lambda:validate_entries(obj,snapshot+b' '))
for tag,raw,expected in [('BUILD',read(Path(build['path'])),build['sha256']),('caseblock',blockraw,blockpin['sha256'])]:
    ck('MUST_FAIL_'+tag+'_byte_tamper',hashlib.sha256(raw+b' ').hexdigest()!=expected)
ck('no_audit_denials',not denials)
result={'date_u':DATE,'status':'TESTED_PASS' if all(x['passed'] for x in checks) else 'TESTED_FAIL','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'entry_semantics':'All20 A82-A101 sections manually read against their table explanations and operative JSON clauses. Four no-change rows are operational/out-of-scope decisions, not omitted obligations.','scope':'Source-independent metadata/Markdown/JSON/custody checks and in-memory checker canaries. No reviewed source, case-block builder, comparator, seal tool or numerical code executed. C5H declaration stayed inert metadata.','harness_correction':'V001 matched a JSON-style token section_sha256 against prose section sha256. That single semantic spelling assertion failed (318/319); V002 corrects only the expected prose spelling and output filename. Prereg bytes unchanged.', 'input_pins':list(pins.values()),'harness':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'audit_denials':denials}
with (HERE/'RESULTS_CX3V002.json').open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:result[k] for k in ('status','passed','total','rss_bytes_macos')}));print(json.dumps([x for x in checks if not x['passed']]))
assert result['status']=='TESTED_PASS'
