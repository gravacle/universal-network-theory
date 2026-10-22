import ast,copy,hashlib,json,os,subprocess,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
b=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1');out=b/'helper010_controls_v001';out.mkdir();hp=b/'provisional_helper010_snapshot_v001/helper.py';hb=hp.read_bytes();assert sha(hb)=='823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2'
ns={'__name__':'helper010_inert_review','__file__':str(hp)};exec(compile(hb,str(hp),'exec'),ns);checks=[];files=[]
def put(name,raw):
 raw=raw.encode() if isinstance(raw,str) else raw;p=out/name
 with p.open('xb') as f:f.write(raw)
 files.append({'path':str(p),'sha256':sha(raw)});return str(p),sha(raw)
def ck(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
def refuse(name,fn,prefix):
 try:fn();ck(name,False,'ACCEPT')
 except ns['Refuse'] as e:ck(name,str(e).startswith(prefix),str(e))
 except Exception as e:ck(name,False,'UNEXPECTED '+type(e).__name__+': '+str(e))
def oa(path,mode='check',**kw):return types.SimpleNamespace(path=str(path),mode=mode,min_free_gib='0',expect_dev='',expect_ino='',**kw)
# RP-S1: actual kernel directory operations only on small owned fixtures, never the production output root.
root=out/'rp_fresh';args=oa(root)
try:r=ns['c_output_root'](args);ck('RP_absent_check_no_creation',r['output_root']['created'] is False and not root.exists())
except Exception as e:ck('RP_absent_check_no_creation',False,type(e).__name__+': '+str(e))
try:r=ns['c_output_root'](oa(root,'create'));rec=r['output_root'];ck('RP_exclusive_create_empty_real_directory',root.is_dir() and rec['empty'] and rec['realpath']==str(root) and rec['on_data_volume'],{'st_dev':rec['st_dev'],'st_ino':rec['st_ino'],'realpath':rec['realpath']})
except Exception as e:rec=None;ck('RP_exclusive_create_empty_real_directory',False,type(e).__name__+': '+str(e))
if rec:
 a=oa(root,'verify');a.expect_dev=str(rec['st_dev']);a.expect_ino=str(rec['st_ino']);r=ns['c_output_root'](a);ck('RP_verify_recorded_identity',r['output_root']['st_ino']==rec['st_ino'])
 a.expect_ino=str(rec['st_ino']+1);refuse('RP_wrong_recorded_inode_refuses',lambda:ns['c_output_root'](a),'OUTPUT_ROOT_IS_NOT_THE_RECORDED_DIRECTORY')
 refuse('RP_existing_directory_refuses_create',lambda:ns['c_output_root'](oa(root,'create')),'OUTPUT_ROOT_EXISTS')
 with (root/'inert_marker').open('xb') as f:f.write(b'fixture only')
 a.expect_ino=str(rec['st_ino']);refuse('RP_nonempty_root_refuses_verify',lambda:ns['c_output_root'](a),'OUTPUT_ROOT_NOT_EMPTY')
fp,_=put('rp_existing_file',b'keep these bytes');refuse('RP_existing_file_refuses',lambda:ns['c_output_root'](oa(fp,'create')),'OUTPUT_ROOT_EXISTS');ck('RP_existing_file_preserved',Path(fp).read_bytes()==b'keep these bytes')
link=out/'rp_dangling';link.symlink_to(out/'never_created');refuse('RP_dangling_link_refuses',lambda:ns['c_output_root'](oa(link,'create')),'PATH_HAS_SYMLINK_COMPONENT')
full=out/'rp_space_floor';a=oa(full,'create');a.min_free_gib='999999999999';refuse('RP_free_space_floor_refuses_without_creation',lambda:ns['c_output_root'](a),'FREE_BELOW_THE_ROOT_FLOOR');ck('RP_space_floor_no_output',not full.exists())
parented=out/'rp_new_parent'/'root'
try:r=ns['c_output_root'](oa(parented,'create'));ck('RP_one_missing_parent_created_exclusively',r['output_root']['parent_created'] and r['output_root']['empty'])
except Exception as e:ck('RP_one_missing_parent_created_exclusively',False,type(e).__name__+': '+str(e))
# W7-S1: fifteen inert unique source pins and an invented BUILD table; real guard and science are never loaded.
rows=[]
for i in range(15):
 p,h=put('source_%02d.py'%i,'# INERT SOURCE %02d\nVALUE=%d\n'%(i,i));rows.append((p,h))
lines=[h+'  '+p for p,h in rows];build='# INERT BUILD\n\n'+ns['BUILD_HEADER']+'\n\n```text\n'+'\n'.join(lines)+'\n```\n\n## Outside table\n'+'f'*64+'  /Users/inert/outside.py\n'
bp,bh=put('BUILD_INERT.md',build);buildpin={'path':bp,'sha256':bh};cfg={'build':buildpin,'producer_allowlist':dict(rows)}
ck('W7_exact15_build_rows',ns['_build_table'](build)==rows)
ck('W7_exact15_config_bytes',ns['_check_config_bytes'](json.dumps(cfg).encode(),build,buildpin)==15)
refuse('W7_build14_refuses',lambda:ns['_build_table'](build.replace(lines[-1]+'\n','')),'W7_BUILD_TABLE_COUNT')
refuse('W7_build16_refuses',lambda:ns['_build_table'](build.replace('\n```\n','\n'+'e'*64+'  /Users/inert/extra.py\n```\n')),'W7_BUILD_TABLE_COUNT')
refuse('W7_duplicate_build_row_refuses',lambda:ns['_build_table'](build.replace(lines[-1],lines[0])),'W7_BUILD_TABLE_DUPLICATE')
for name,items,prefix in [('config14',rows[:-1],'W7_ALLOWLIST_COUNT'),('config16',rows+[('/Users/inert/extra.py','e'*64)],'W7_ALLOWLIST_COUNT'),('reordered',list(reversed(rows)),'W7_ALLOWLIST_ORDER_DIFFERS_FROM_TABLE'),('wrong_sha',[(rows[0][0],'0'*64)]+rows[1:],'W7_ALLOWLIST_ROW_SHA_NOT_BYTE_EQUAL'),('wrong_path',[('/Users/inert/wrong.py',rows[0][1])]+rows[1:],'W7_ALLOWLIST_ROW_NOT_IN_TABLE')]:
 c={'build':buildpin,'producer_allowlist':dict(items)};refuse('W7_'+name+'_refuses',lambda c=c:ns['_check_config_bytes'](json.dumps(c).encode(),build,buildpin),prefix)
# Duplicate serialized row cannot disappear silently in dict parsing.
raw=json.dumps(cfg);needle=json.dumps(rows[0][0])+': '+json.dumps(rows[0][1]);dup=raw.replace(needle,needle+', '+needle,1)
try:ns['_check_config_bytes'](dup.encode(),build,buildpin);ck('W7_duplicate_serialized_key_refuses',False)
except ns['DuplicateKey']:ck('W7_duplicate_serialized_key_refuses',True)
# Integration: c_make_config preserves table order and invokes exact byte-check before and after exclusive create.
alp,alh=put('allowlist.txt','\n'.join(lines)+'\n');ip,ih=put('index.json',json.dumps({'supported_entries':[{'path':p,'sha256':h} for p,h in rows]}));seal={'sealed_by':ns['AUTHORITY']}
for k in ('prereg','compare','driver','frozen_addendum'):
 p,h=put('seal_'+k+'.txt','INERT '+k+'\n');seal[k]={'path':p,'sha256':h}
sp,sh=put('seal.json',json.dumps(seal));cp=out/'admission_config.json'
a=types.SimpleNamespace(seal=sp,seal_sha=sh,build=bp,build_sha=bh,allowlist=alp,allowlist_sha=alh,producer_index=ip,producer_index_sha=ih,guard=rows[0][0],guard_sha=rows[0][1],launcher=rows[1][0],launcher_sha=rows[1][1],out=str(cp))
old_exec=ns['_exec_module'];old_check=ns['_check_config_bytes'];seen=[]
def mockload(path,h,name):
 return types.SimpleNamespace(CONFIG=cp,AUTHORITY=ns['AUTHORITY'],__file__=path,admission=lambda launcher:{'_verified_seal':seal,'_verified_config_sha256':sha(cp.read_bytes())})
def checkspy(raw,bt,pin):seen.append({'sha256':sha(raw),'config_exists':cp.exists()});return old_check(raw,bt,pin)
ns['_exec_module']=mockload;ns['_check_config_bytes']=checkspy
try:r=ns['c_make_config'](a);ck('W7_make_config_exact_order',list(json.loads(cp.read_bytes())['producer_allowlist'].items())==rows);ck('W7_serialized_and_written_bytes_checked',len(seen)==2 and not seen[0]['config_exists'] and seen[1]['config_exists'] and seen[0]['sha256']==seen[1]['sha256'],seen)
finally:ns['_exec_module']=old_exec;ns['_check_config_bytes']=old_check
r=ns['c_check_config_allowlist'](types.SimpleNamespace(config=str(cp),config_sha=sha(cp.read_bytes()),build=bp,build_sha=bh));ck('W7_written_config_recheck',r['w7_s1_allowlist']['rows']==15)
# Mutated serialization is refused before any output is created; the real guard is unreachable.
old_dumps=ns['dumps'];badout=out/'mutated_serialization_config.json';a.out=str(badout)
def bad_dumps(o):
 v=copy.deepcopy(o);v['producer_allowlist']=dict(reversed(list(v['producer_allowlist'].items())));return old_dumps(v)
ns['dumps']=bad_dumps
try:refuse('W7_mutated_serialization_refuses_prewrite',lambda:ns['c_make_config'](a),'W7_ALLOWLIST_ORDER_DIFFERS_FROM_TABLE');ck('W7_mutation_emits_no_config',not badout.exists())
finally:ns['dumps']=old_dumps
ck('priority_nice10',os.getpriority(os.PRIO_PROCESS,0)>=10)
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'PROVISIONAL_TESTED_HELPER010_0642_ONLY','source':{'path':str(hp),'sha256':sha(hb)},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'fixture_files':files,'scope':'Actual kernel directory operations on owned fixtures only. Build/config fixtures invented; guard admission explicitly mocked for allowlist writer integration. No production output root, native guard, real script/comparator/science/watchdog/notification/process executed. B1/B2/N1 and unchanged disposition semantics not repeated.'}
rp=out/'RESULTS.json'
with rp.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'path':str(rp),'sha256':sha(rp.read_bytes()),'passed':result['passed'],'total':result['total'],'failures':[x for x in checks if not x['passed']]}))
