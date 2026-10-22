from pathlib import Path
import hashlib, json, os, subprocess
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001')
assert os.getpriority(os.PRIO_PROCESS,0)>=10
src=(ROOT/'watchdog_source.sh').read_bytes()
assert hashlib.sha256(src).hexdigest()=='bd0d9bab0854627957781e1666c7f5eacd1e10cd03bfde0dd2efe2e27a5a2c28'
text=src.decode()
# This exact leading source slice ends before the notification function, start log and poll loop.
prefix=text[:text.index('utc() {')]
assert 'osascript -e' not in prefix and 'while :;' not in prefix and 'out="$(df' not in prefix
fixtures=ROOT/'fixtures'; fixtures.mkdir()
rows=[]
def record(name,expected,actual,passed,**detail):
 rows.append(dict(name=name,expected=expected,actual=actual,passed=passed,**detail))
def run(args,source=prefix,timeout=0.4):
 try:
  r=subprocess.run(['/bin/bash','-c',source,'owned-inert-source-slice',*map(str,args)],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=timeout)
  return r.returncode
 except subprocess.TimeoutExpired:
  return 'TIMEOUT_CHILD_KILLED'
for name in ['watchdog_source.sh','author_test_source.sh']:
 r=subprocess.run(['/bin/bash','-n'],input=(ROOT/name).read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 record('syntax '+name,0,r.returncode,r.returncode==0,stderr=r.stderr.decode()[:200])
for opt in ['--log','--threshold-gib','--interval-s','--max-polls','--df-stub']:
 rc=run([opt])
 record('missing value '+opt,'finite refusal rc 2',rc,rc==2)
ordinary=fixtures/'ordinary.log'
rc=run(['--log',ordinary]);record('ordinary exclusive log',0,rc,rc==0 and ordinary.read_bytes()==b'')
existing=fixtures/'existing.log'; existing.write_bytes(b'OWNED INERT SENTINEL\n')
old=hashlib.sha256(existing.read_bytes()).hexdigest();rc=run(['--log',existing])
record('existing log preserved',2,rc,rc==2 and hashlib.sha256(existing.read_bytes()).hexdigest()==old)
restricted=fixtures/'runs_ext'/'inert_only';restricted.mkdir(parents=True)
rc=run(['--log',restricted/'direct.log'])
record('direct lexical restricted fixture',2,rc,rc==2 and not (restricted/'direct.log').exists())
alias=fixtures/'innocent_alias'; alias.symlink_to(restricted,target_is_directory=True)
rc=run(['--log',alias/'alias.log'])
record('symlink ancestor into restricted fixture','refuse without creating log',rc,rc==2 and not (restricted/'alias.log').exists(),created_target=(restricted/'alias.log').exists(),real_tree_used=False)
dangling=fixtures/'dangling.log';target=fixtures/'dangling_target.log';dangling.symlink_to(target)
rc=run(['--log',dangling])
record('dangling final symlink',2,rc,rc==2 and not target.exists(),target_created=target.exists())
linked=fixtures/'existing_link.log'; linked.symlink_to(existing)
rc=run(['--log',linked])
record('existing final symlink',2,rc,rc==2 and hashlib.sha256(existing.read_bytes()).hexdigest()==old)
rc=run(['--log',fixtures/'badnum.log','--threshold-gib','8O'])
record('nonnumeric threshold',2,rc,rc==2 and not (fixtures/'badnum.log').exists())
# Test the unchanged threshold arithmetic expression alone. No log, df, notify or watchdog code is present.
expr='[ "$avail_kb" -lt $((THRESH_GIB * 1048576)) ]'
assert expr in text
arith='THRESH_GIB="$1"; avail_kb="$2"; '+expr
for label,th,kb,want in [('normal below','80','83886079',0),('normal exact','80','83886080',1),('leading-zero accepted by parser','080','83886079',0),('overflow accepted by parser','8796093022208','83886079',0)]:
 rc=run([th,kb],source=arith)
 record('threshold arithmetic '+label,want,rc,rc==want,threshold_gib=th,available_kib=kb)
# An isolated exact awk parse from the source; use invented text only.
parse='awk -v v="$VOL" \'NR==2 && $NF==v && $4 ~ /^[0-9]+$/ {print $4}\''
assert parse in text
for label,mount,avail,want in [('valid','/System/Volumes/Data','83886079','83886079'),('wrong mount','/Volumes/Inert','83886079',''),('invalid available','/System/Volumes/Data','x','')]:
 data='Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/inert 100000000 1000 '+avail+' 50% '+mount+'\n'
 r=subprocess.run(['/bin/bash','-c','VOL=/System/Volumes/Data; '+parse],input=data.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 got=r.stdout.decode().strip();record('df parser '+label,want,got,got==want and r.returncode==0)
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'source_sha256':hashlib.sha256(src).hexdigest(),'scope':'Exact bounded source slices and bash syntax only. No original watchdog/test run; no real df/notify/sleep loop. Timeout children killed by subprocess.run. All writes within owned fixtures.','nice':os.getpriority(os.PRIO_PROCESS,0),'checks':rows,'checks_passed':sum(r['passed'] for r in rows),'checks_total':len(rows),'failed_controls':[r['name'] for r in rows if not r['passed']]}
with (ROOT/'SLICE_RESULTS_CX1V001.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['checks_passed','checks_total','failed_controls']}))
