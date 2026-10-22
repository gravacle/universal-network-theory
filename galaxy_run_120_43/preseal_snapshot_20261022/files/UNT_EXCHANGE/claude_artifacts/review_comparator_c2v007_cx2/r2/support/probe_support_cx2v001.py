"""Independent r2 support-bundle audit: bytes and AST only, no candidate execution."""
from pathlib import Path
import ast,hashlib,json,os,re,stat
HERE=Path(__file__).parent
G=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007')
R=G/'r2'
rows=[];refs={}
def raw(p):
 s=str(p)
 assert '/runs_ext/' not in s and '/runs/' not in s and '/.codex/' not in s
 assert stat.S_ISREG(p.lstat().st_mode),s
 b=p.read_bytes();refs[s]=hashlib.sha256(b).hexdigest();return b
def sh(p):return hashlib.sha256(raw(p)).hexdigest()
def check(name,ok,detail=None):rows.append({'name':name,'pass':bool(ok),'detail':detail})
def txt(p):return raw(p).decode()
supported=json.loads(raw(R/'SUPPORTED_FILES_R2.json'))
check('supported_status_frozen',supported['status']=='FROZEN_FOR_CODEX2_DELTA_REVIEW_NOT_ADOPTED')
paths=[x['path'] for x in supported['files']]
check('supported_paths_unique',len(paths)==len(set(paths)),len(paths))
for x in supported['files']:
 p=Path(x['path']);check('supported_byte_pin:'+str(p.relative_to(R)),sh(p)==x['sha256'])
for name in ['fill_picard_member_c2v003.py','r5_gate_check_c2v007.py','a71_inventory_c2v007.py']:
 check('unchanged_tool:'+name,raw(G/'tools'/name)==raw(R/'tools'/name))
for p in sorted((R/'tokens').glob('*.json')):
 if str(p) in paths:check('unchanged_tokens:'+p.name,raw(p)==raw(G/'tokens'/p.name))
old=txt(G/'tools/write_identity_records_c2v007.py');new=txt(R/'tools/write_identity_records_c2v007_r2.py')
check('writer_only_G7_constant_changes',new==old.replace("gates_v007')","gates_v007/r2')"))
tree=ast.parse(new)
check('writer_G7_is_r2',any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='G7' for t in n.targets) and str(R) in ast.unparse(n.value) for n in tree.body))
oldsh=txt(G/'R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh');newsh=txt(R/'R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2.sh')
expected=oldsh.replace('G7='+str(G)+'\n','G7='+str(R)+'\n').replace(sh(G/'run_identity_compare_c2v007.py'),sh(R/'run_identity_compare_c2v007.py')).replace('write_identity_records_c2v007.py','write_identity_records_c2v007_r2.py').replace(sh(G/'tools/write_identity_records_c2v007.py'),sh(R/'tools/write_identity_records_c2v007_r2.py'))
check('command_only_declared_paths_and_pins_change',newsh==expected)
cmp_pin=re.search(r'^CMP_SHA=([a-f0-9]{64})$',newsh,re.M).group(1)
check('command_comparator_pin',cmp_pin==sh(R/'run_identity_compare_c2v007.py'))
pins=re.findall(r'^pin \$G7/(\S+) ([a-f0-9]{64}|\$CMP_SHA)$',newsh,re.M)
check('command_pin_count_six',len(pins)==6,len(pins))
for rel,h in pins:check('command_pin:'+rel,(cmp_pin if h=='$CMP_SHA' else h)==sh(R/rel))
pos_receipt=newsh.index('r5_gate_check_c2v007.py receipts')
comparisons=[m.start() for m in re.finditer(r'run_identity_compare_c2v007.py --gate ',newsh)]
pos_verdict=newsh.index('r5_gate_check_c2v007.py verdicts');pos_writer=newsh.index('write_identity_records_c2v007_r2.py --driver')
check('N6_three_comparisons',len(comparisons)==3)
check('N6_receipts_before_all_comparisons',all(pos_receipt<p for p in comparisons))
check('N6_all_comparisons_before_verdict_check',all(p<pos_verdict for p in comparisons))
check('N6_verdicts_before_writer',pos_verdict<pos_writer)
check('N6_each_wait_status_reaches_verdict_check',all(x in newsh for x in ['wait $P1; C1=$?','wait $P2; C2=$?','wait $P3; C3=$?','Z2=$O/Z2.json=$C1 Z2_OFF_RO1=$O/Z2_OFF_RO1.json=$C2 B0P_RERUN=$O/B0P_RERUN.json=$C3']))
gen=txt(R/'tools/write_r5_script_c2v007_r2.py')
t=ast.parse(gen)
opens=[n for n in ast.walk(t) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='open']
check('generator_exclusive_create',len(opens)==1 and len(opens[0].args)>1 and isinstance(opens[0].args[1],ast.Constant) and opens[0].args[1].value=='x')
check('generator_pins_supported_writer','tools/write_identity_records_c2v007_r2.py' in gen and 'tools/write_identity_records_c2v007.py' not in gen)
check('generator_names_supported_script',"p = G7 / 'R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2.sh'" in gen)
check('generator_pins_read_from_bytes','hashlib.sha256(Path(p).read_bytes()).hexdigest()' in gen)
res={'date_u':os.environ['UNT_CX2_PACKET_UTC'],'scope':'TESTED static bytes/AST only; candidate command, generator and writer NOT executed','tested':len(rows),'passed':sum(x['pass'] for x in rows),'cases':rows,'references':[{'path':p,'sha256':h} for p,h in sorted(refs.items())]}
with (HERE/'RESULTS_SUPPORT_CX2V001.json').open('x') as f:json.dump(res,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'tested':res['tested'],'passed':res['passed'],'failed':[x for x in rows if not x['pass']]}))
