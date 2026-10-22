import copy,hashlib,json,os,subprocess,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
base=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1');out=base/'selected_helper_semantics_v001';out.mkdir()
selection=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/SELECTED_SEAL_PRESTAGE_C3SA.json');sb=selection.read_bytes();sel=json.loads(sb)
hp=base/'provisional_snapshot_v002/helper.py';hb=hp.read_bytes();assert sha(hb)==sel['selected_tuple']['helper']['sha256']=='000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3'
inputs=[]
for p in [selection,Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0640_2026-10-18_claude4_claude3_D05_rule_and_contract.md'),Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0641_2026-10-18_claude3_N1_nonblocking_publish.md'),Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0107_2026-10-18_ack_0640_PV-D05-1_and_0637.md')]:
 b=sb if p==selection else p.read_bytes();q=out/p.name
 with q.open('xb') as f:f.write(b)
 inputs.append({'source':str(p),'snapshot':str(q),'sha256':sha(b)})
ns={'__name__':'selected_helper_inert_semantics','__file__':str(hp)};exec(compile(hb,str(hp),'exec'),ns)
old82=b'## A82: Inert cited rule\nBaseline wording ORIGINAL_SENTINEL.\n'
new82=b'## A82: Inert cited rule\nBaseline wording CHANGED_SENTINEL.\n'
stable83=b'## A83: Inert cited stable rule\nUnchanged fixture text.\n'
later84=b'## A84: Inert later entry\nAdditional fixture text.\n'
old=old82+stable83;new=new82+stable83+later84
checks=[]
def run_case(name,mut=None,accept=True,code=None,category='mechanical'):
 d=out/name;d.mkdir();refs=[]
 def put(name,b):
  b=b.encode() if isinstance(b,str) else b;p=d/name
  with p.open('xb') as f:f.write(b)
  refs.append({'path':str(p),'sha256':sha(b)});return str(p),sha(b)
 rev,rh=put('synthetic_revision.json','{"revision":"inert only"}\n');osp,osh=put('old_section.md',old82)
 data={'old':old,'new':new,'anchor':sha(old),'table_sha_override':None,'rows':[{'entry':'A82','section_sha256':sha(old82),'section_bytes':len(old82),'decision':'NO_CHANGE','reason':'Inert original table row.'},{'entry':'A83','section_sha256':sha(stable83),'section_bytes':len(stable83),'decision':'NO_CHANGE','reason':'Inert stable table row.'}],'entries':[{'entry':'A82','disposition':'no_change_after_change','section_sha256':sha(new82),'changed_text':'CHANGED_SENTINEL','why_no_prereg_effect':'Synthetic changed text has no prereg effect in this fixture.'},{'entry':'A84','disposition':'no_change','section_sha256':sha(later84),'reason':'Inert later entry.'}],'revision':{'path':rev,'sha256':rh},'old_section':{'path':osp,'sha256':osh}}
 if mut:mut(data)
 tp,th=put('table_bytes.md',data['old']);fp,fh=put('frozen.md',data['new'])
 doc={'sources':['A82','A83'],'entries_after_A81':{'addendum_read':{'sha256_at_generation':data['anchor']},'rows':data['rows']}}
 pp,ph=put('prereg.json',json.dumps(doc));obj={'schema':'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001','frozen_addendum_sha256':fh,'entries':data['entries']};dp,dh=put('dispositions.json',json.dumps(obj))
 a=types.SimpleNamespace(dispositions=dp,dispositions_sha=dh,prereg=pp,prereg_sha=ph,frozen=fp,frozen_sha=fh,table_bytes=tp,table_bytes_sha=data['table_sha_override'] or th)
 orig=ns['read_nofollow'];readpaths=[]
 def spy(path,label):readpaths.append(path);return orig(path,label)
 ns['read_nofollow']=spy
 try:res=ns['_dispositions'](a);actual=True;detail='ACCEPT';returned=res
 except ns['Refuse'] as e:actual=False;detail=str(e);returned=None
 except Exception as e:actual=None;detail='UNEXPECTED '+type(e).__name__+': '+str(e);returned=None
 finally:ns['read_nofollow']=orig
 passed=actual==accept and (code is None or detail.startswith(code))
 checks.append({'id':name,'category':category,'expected_accept':accept,'actual_accept':actual,'passed':passed,'detail':detail,'returned':returned,'files':refs,'read_paths':readpaths,'revision_file_read':rev in readpaths,'old_section_file_read':osp in readpaths})
def rowpatch(**kw):
 def mutate(d):d['entries'][0].update(kw)
 return mutate
run_case('positive_exact_new_minus_old_excerpt')
run_case('plain_no_change_on_changed_cited',rowpatch(disposition='no_change'),False,'DISPOSITION_NO_CHANGE_ON_CHANGED_ENTRY')
run_case('excerpt_present_both_old_new',rowpatch(changed_text='Baseline wording'),False,'DISPOSITION_CHANGED_TEXT_IN_OLD_BYTES')
run_case('excerpt_only_old',rowpatch(changed_text='ORIGINAL_SENTINEL'),False,'DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_BYTES')
run_case('excerpt_absent_both',rowpatch(changed_text='NOT_PRESENT_ANYWHERE'),False,'DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_BYTES')
run_case('excerpt_empty',rowpatch(changed_text='  '),False,'DISPOSITION_CHANGED_TEXT_EMPTY')
run_case('why_empty',rowpatch(why_no_prereg_effect='  '),False,'DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY')
run_case('revised_pointer_missing',rowpatch(disposition='revised'),False,'DISPOSITION_REVISED_NEEDS_PREREG_REVISION_POINTER')
run_case('revised_pointer_empty',rowpatch(disposition='revised',prereg_revision='  '),False,'DISPOSITION_REVISED_NEEDS_PREREG_REVISION_POINTER')
run_case('revised_pointer_nonstring',rowpatch(disposition='revised',prereg_revision=17),False,'DISPOSITION_REVISED_NEEDS_PREREG_REVISION_POINTER')
run_case('revised_string_pointer_to_existing_file',lambda d:d['entries'][0].update(disposition='revised',prereg_revision=d['revision']['path']),True)
run_case('revised_nonexistent_string_pointer',rowpatch(disposition='revised',prereg_revision='/Users/inert_missing_revision.json'),True,category='validation_limit_observation')
run_case('table_file_wrong_sha',lambda d:d.update(table_sha_override='0'*64),False,'PIN_BYTES_MISMATCH')
run_case('prereg_anchor_wrong',lambda d:d.update(anchor='0'*64),False,'TABLE_BYTES_NOT_THE_PREREG_TABLE_SOURCE')
run_case('table_row_wrong_sha',lambda d:d['rows'][0].update(section_sha256='0'*64),False,'TABLE_BYTES_DO_NOT_REHASH')
run_case('table_row_wrong_length',lambda d:d['rows'][0].update(section_bytes=1),False,'TABLE_BYTES_DO_NOT_REHASH')
run_case('substituted_old_source_anchor_unchanged',lambda d:d.update(old=d['old'].replace(b'ORIGINAL_SENTINEL',b'SUBSTITUTED_OLD')),False,'TABLE_BYTES_NOT_THE_PREREG_TABLE_SOURCE')
def reanchor(d):d['old']=d['old'].replace(b'ORIGINAL_SENTINEL',b'SUBSTITUTED_OLD');d['anchor']=sha(d['old'])
run_case('substituted_old_source_reanchored_rows_unchanged',reanchor,False,'TABLE_BYTES_DO_NOT_REHASH')
run_case('wrong_new_section_sha',rowpatch(section_sha256='0'*64),False,'DISPOSITION_WRONG_SECTION_SHA')
run_case('changed_row_omitted',lambda d:d['entries'].pop(0),False,'DISPOSITION_ENTRIES')
run_case('duplicate_changed_row',lambda d:d['entries'].append(copy.deepcopy(d['entries'][0])),False,'DISPOSITION_DUPLICATE')
run_case('bad_optional_change_old_pin',rowpatch(change={'from_section_sha256':'0'*64,'to_section_sha256':sha(new82),'what_changed':'Synthetic replacement'}),False,'DISPOSITION_CHANGE_OBJECT')
run_case('announced_revision_object_pointer',lambda d:d['entries'][0].update(disposition='revised',prereg_revision=d['revision']),True,category='announced_v003_alignment')
run_case('announced_nca_old_section_pin',lambda d:d['entries'][0].update(old_section=d['old_section']),True,category='announced_v003_alignment')
summary={}
for cat in sorted(set(c['category'] for c in checks)):
 rows=[c for c in checks if c['category']==cat];summary[cat]={'passed':sum(c['passed'] for c in rows),'total':len(rows)}
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_SELECTED_HELPER_SEMANTICS_SCOPED','helper':{'path':str(hp),'sha256':sha(hb)},'authority_inputs':inputs,'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'checks':checks,'summary':summary,'nice':os.getpriority(os.PRIO_PROCESS,0),'scope':'Own runtime, exact selected helper buffer and invented text only. No real scientific data, original root script or comparator. Announced0107 author interface differs from0640 coordinator minimum; it is not yet published v003 source. B1/B2/envelope unchanged evidence reused rather than repeated.'}
p=out/'RESULTS.json'
with p.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'path':str(p),'sha256':sha(p.read_bytes()),'summary':summary,'unexpected':[c['id'] for c in checks if c['actual_accept'] is None]}))
