from pathlib import Path
import hashlib,json,os,subprocess
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001')
assert os.getpriority(os.PRIO_PROCESS,0)>=10
src=(ROOT/'watchdog_source.sh').read_bytes();test=(ROOT/'author_test_source.sh').read_bytes()
assert hashlib.sha256(src).hexdigest()=='bd0d9bab0854627957781e1666c7f5eacd1e10cd03bfde0dd2efe2e27a5a2c28'
assert hashlib.sha256(test).hexdigest()=='696bfc9b3bb4e514dad0aac0c304d390f5044b39b1b59c3c1cbf0cf8375ecfe4'
s=src.decode();t=test.decode();rows=[]
notify=s[s.index('notify() {'):s.index('echo "$(utc) START')]
branch=s[s.index('if [ "$TEST_NOTIFY" = 1 ]; then'):s.index('poll=0\n')]
for stub_rc in [0,7]:
 log=ROOT/'fixtures'/('notify_stub_rc_'+str(stub_rc)+'.log')
 with log.open('x'):pass
 prefix='utc(){ printf SYNTHETIC; }; osascript(){ return '+str(stub_rc)+'; }; LOG="$1"; NOTIFY_STUB=0; TEST_NOTIFY=1;\n'
 r=subprocess.run(['/bin/bash','-c',prefix+notify+branch,'owned-function-slices',str(log)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1)
 content=log.read_text();good=(r.returncode==0) if stub_rc==0 else (r.returncode!=0)
 rows.append({'name':'test-notify exact branch with owned osascript function double rc '+str(stub_rc),'expected':'exit zero' if stub_rc==0 else 'nonzero exit','actual_exit':r.returncode,'passed':good,'log':content,'real_notification_used':False})
ending=t[t.index('[ $ok_all = 1 ] && rec "ALL PASS"'):]
for flag in [1,0]:
 shell='ok_all="$1"; T=OWNED_INERT_PATH; RES="$2"; rec(){ printf "%s\\n" "$1" >> "$RES"; };\n'+ending
 log=ROOT/'fixtures'/('author_status_'+str(flag)+'.txt')
 with log.open('x'):pass
 r=subprocess.run(['/bin/bash','-c',shell,'owned-author-tail-slice',str(flag),str(log)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1)
 rows.append({'name':'author test status tail ok_all='+str(flag),'expected':'exit zero' if flag==1 else 'nonzero exit','actual_exit':r.returncode,'passed':r.returncode==0 if flag==1 else r.returncode!=0,'stdout':r.stdout.decode()})
res={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'scope':'Exact notification-function/test-notify branch and author status-tail slices only; osascript is an owned shell-function double. No real notification, watcher, df or poll loop.','checks':rows,'checks_passed':sum(x['passed'] for x in rows),'checks_total':len(rows)}
with (ROOT/'STATUS_SLICE_RESULTS_CX1V001.json').open('x') as f:json.dump(res,f,indent=2);f.write('\n')
print(json.dumps({'checks_passed':res['checks_passed'],'checks_total':res['checks_total'],'failures':[x['name'] for x in rows if not x['passed']]}))
