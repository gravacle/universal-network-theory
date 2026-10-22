from pathlib import Path
import subprocess,json,hashlib,os
R=Path(__file__).resolve().parent.parent;OUT=R/'selftest/MKDIR_0608_V001';OUT.mkdir()
p=R/'R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2_V002.sh';text=p.read_text();lines=text.splitlines();fragment='\n'.join(l for l in lines if l.startswith('mkdir '));assert len(fragment.splitlines())==2
rows=[]
def test(name,path,expected):
 r=subprocess.run(['/bin/zsh','-c',fragment],env=dict(os.environ,O=str(path)),capture_output=True,text=True)
 rows.append(dict(name=name,exit_code=r.returncode,expected=expected,passed=r.returncode==expected,stderr=r.stderr,output_path=str(path)))
test('missing_parent_and_spaces',OUT/'new parent'/'new output',0)
test('existing_output_refuses',OUT/'new parent'/'new output',1)
with open(OUT/'parent_is_file','x') as f:f.write('synthetic blocker')
test('parent_is_file_refuses',OUT/'parent_is_file'/'child',1)
(OUT/'existing parent').mkdir();test('existing_parent_new_output',OUT/'existing parent'/'new output',0)
assert all(r['passed'] for r in rows)
assert 'OUTPUT DIRECTORY EXISTS' not in text
old=(R/'R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2.sh').read_text();oldline='mkdir $O || { echo "OUTPUT DIRECTORY EXISTS: $O"; exit 1; }'
assert old.replace(oldline,fragment)==text
report=dict(status='TESTED',scope='Only extracted two mkdir commands on synthetic directories; no full command file, comparator or production read executed.',rows=rows,script={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},all_other_script_bytes_unchanged=True)
with open(OUT/'RESULTS.json','x') as f:json.dump(report,f,indent=1)
print('4/4 PASS; exact two-line delta')
