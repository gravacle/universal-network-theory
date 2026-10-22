"""Package independent saved-record checks. No project imports or run traversal."""
import os,sys,json,hashlib,collections
B='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/reconcile/'
R=B+'run_20261018T200716Z_108/RESULTS_CX2V001.json'
D='/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md'
def h(p):
 with open(p,'rb') as f:return hashlib.sha256(f.read()).hexdigest()
r=json.load(open(R));assert h(R)=='5164627e173c29715abce35bc62e5a5cc39162a59c4a2c33eaa97a247969af2b'
safe=set(r['input_pins'])|{R,D,__file__,B+'check_reconciliation_cx2v001.py',B+'check_reconciliation_cx2v002.py',B+'PARTIAL_CHECKPOINT_CX2V001.md'}
out={B+x for x in ('NORMALIZATION_DEFAULT_CHECK_CX2V001.json','REVIEW_RECONCILIATION_CX2V001.md','HASHES_RECONCILIATION_CX2V001.jsonl')}
def ban(p):
 if isinstance(p,int) or p is None:return
 p=os.path.abspath(os.fsdecode(p));parts=p.lower().split('/')
 if any(x in ('runs','runs_ext','.codex') or x.startswith('uvt_') or 'c5h' in x for x in parts):raise PermissionError('PROTECTED')
def audit(e,a):
 if e=='open' and isinstance(a[0],(str,bytes,os.PathLike)):
  p=os.path.abspath(os.fsdecode(a[0]));ban(p)
  if p not in safe|out:raise PermissionError('EXACT_REVIEW_SCOPE')
  if a[2]&(os.O_WRONLY|os.O_RDWR) and (p not in out or not a[2]&os.O_EXCL):raise PermissionError('EXCLUSIVE_WRITES')
 if e in ('os.listdir','os.scandir') or e.startswith(('subprocess.','socket.')):raise PermissionError('NO_EXTERNAL_WORK')
sys.addaudithook(audit)
for name in ('stat','lstat','readlink'):
 old=getattr(os,name)
 def wrap(p,*a,_old=old,**kw):ban(p);return _old(p,*a,**kw)
 setattr(os,name,wrap)
normal=[]
for p in sorted(r['input_pins']):
 if p.endswith('/DRYRUN_REPORT.json'):
  x=json.load(open(p));s=json.load(open(x['call_spec']))
  nd=x['normalized_spec']['numerics']['truncation']
  normal.append({'path':p,'pass':nd==dict(s['numerics']['truncation'],kmax_inverse_kpc=None) and 'kmax_inverse_kpc' not in s['numerics']['truncation']})
assert len(normal)==34 and all(x['pass'] for x in normal)
with open(B+'NORMALIZATION_DEFAULT_CHECK_CX2V001.json','x') as f:json.dump({'date_u':sys.argv[1],'checks':normal,'passed':34,'total':34,'scope':'Saved normalization default only; no normalizer execution'},f,indent=1,sort_keys=True);f.write('\n')
current={p:h(p) for p in sorted(safe)}
changed=[{'path':p,'observed_sha256':old,'seal_sha256':current[p]} for p,old in r['input_pins'].items() if current[p]!=old]
text='''# Step-4 inventory / dry-plan reconciliation — CX2 v001

date -u: `{date}`

**TESTED saved-record reconciliation: PASS. Final package and launchability: UNTESTED.** This review is limited to the named document/spec/dry-plan snapshot read at 20:07:16Z. It does not authorize launches, certify the pending scientific certificates, or review a future guarded launch packet. No supplied tool, Context, driver, normalizer, scientific stage, or producer was executed or imported.

The independent suite passed **769/769 checks**, including byte pins/rechecks and the following substantive reconciliation. A separate bounded saved-normalization check passed **34/34**; these counts are separate suites.

- All **253 builder pair checks** were independently recomputed from the saved bytes. This total includes **250 checks over 34 matched planned records and three explicit no-plan dispositions** (two contingent r6 entries and the unregistered post-calibration S1 entry). Those three dispositions are not executed dry plans.
- The inventory has **37 run entries**. Its 33 direct-run entries plus the campaign's first seed call match all **34 saved plan records** exactly once. No planned record or inventory entry is silently lost.
- There are **34 spec pathnames but 32 distinct spec byte contents**: each exact-D deciding pair has equal spec bytes under its two driver-labelled filenames. The builder's “32 distinct spec files” is read as a content count, not a pathname count.
- All **27 available inventory-template/prototype comparisons** differ only in `/label`. This comprises 26 corner/distance templates plus the anchor prototype. The other seven planned records have separate fixed-spec or generated-role checks; no template-only assertion is invented for them.
- There are **30 tail-ON records and 28 independently computed certificate-point hashes**. Reanchor, headline trial and workers candidate share the anchor identity. The campaign's log/exp seed is a distinct 28th identity. Each identity binds driver, physical values, coefficients and numerics with only EPS/LO certificate slots removed, matching the inspected core definition.
- All saved reports bind their exact raw spec path/hash and driver hash, preserve physical/coefficient values, and declare zero executed stages. The only raw-to-normalized structural difference in all 34 is the added `numerics.truncation.kmax_inverse_kpc: null` default, independently checked. These are archived report observations; the review did not rerun or independently monitor the original processes.
- All 30 provisional post-adoption specs change only label and EPS/LO slots, preserving point identities. Filled slot pins do not establish point-dependent scientific approval. Later per-point registry substitution can change final spec bytes while retaining the point key.
- The 93 blocker entries are exactly 30 V007-adoption entries plus 63 other-root-item entries. The six non-V007 blocker codes and seven campaign-gate entries all map into the final root-item traceability. The 31 original item IDs are retained among 36 final IDs, with five declared new items. These mapping checks do not prove every prose explanation or recommended successor correct.

**Gate/adoption boundary:** the inspected config still has null adoption inputs, null certificate registry/review and no approved certificate producers; the inspected policy has an empty seal allowlist. The saved campaign plan has `gates_ok: false`. Thus archived PLANNED status and zero pending slot pins after a synthetic fill cannot be promoted to scientific admission or launch readiness. Alternate-D evidence remains per-D; pending policy and certificate work remain explicit.

**Separate live policy delta:** dispatch 0620 removes the unguarded fallback and requires the R-C8 cache-id prose to match its evidence. The inspected root-item Markdown still includes the “zero-build fallback” text and the old cache-prefix claim. Those are known coordinator-directed changes, not newly accepted launch paths. This component review leaves their final correction and guarded-packet enforcement UNTESTED. Codex2's no-launch rule is unconditional; any builder assertion about pre-seal tail-OFF eligibility is not authorization for Codex2.

**Publication scope:** final-named launch/root documents changed before this run. Every consumed file was rehashed unchanged during the successful run; this is a snapshot result, not a claim that staged publication is immutable. The packaging recheck found {nchanged} changed consumed files; details, if any, are below. The supplied broad HASHES manifest was not traversed. No embedded production run/receipt, NGC target or generated NGC template was opened.

Harness history: the checkpointed v001 was never executed. Before execution, v002 corrected its pending-slot literal to the actual schema string and added the newly available launch Markdown to custody. The source/saved-data suite then passed directly, with zero protected-path attempts. Own negative controls confirm label-only allowance, physical-distance change detection, signed-zero/type distinction, empty-container difference detection and duplicate-JSON rejection.

Evidence:

| File | SHA256 |
| --- | --- |
| `{result}` | `{result_sha}` |
| `{harness}` | `{harness_sha}` |
| `{default}` | `{default_sha}` |
| `{ruling}` | `{ruling_sha}` |

Core snapshot pins (observed at test time):

| File | SHA256 |
| --- | --- |
'''.format(date=sys.argv[1],nchanged=len(changed),result=R,result_sha=current[R],harness=B+'check_reconciliation_cx2v002.py',harness_sha=current[B+'check_reconciliation_cx2v002.py'],default=B+'NORMALIZATION_DEFAULT_CHECK_CX2V001.json',default_sha=h(B+'NORMALIZATION_DEFAULT_CHECK_CX2V001.json'),ruling=D,ruling_sha=current[D])
for p,sh in sorted(r['input_pins'].items()):
 if p.endswith(('INVENTORY_C4V001.json','DRYPLANS_C4V002.json','RECONCILE_C4V002.json','LAUNCH_ORDER_C4V001.json','LAUNCH_ORDER_C4V001.md','ROOT_ITEMS_FINAL_C4V001.json','ROOT_ITEMS_FINAL_C4V001.md')):text+='| `'+p+'` | `'+sh+'` |\n'
if changed:text+='\nChanged since test snapshot (no current-match claim for old hash):\n\n'+json.dumps(changed,indent=2)+'\n'
else:text+='\nAll 175 consumed input hashes still matched their test snapshot at packaging. Future publication revisions require their own delta review.\n'
with open(B+'REVIEW_RECONCILIATION_CX2V001.md','x') as f:f.write(text)
paths=safe|{B+'REVIEW_RECONCILIATION_CX2V001.md',B+'NORMALIZATION_DEFAULT_CHECK_CX2V001.json'}
mp=B+'HASHES_RECONCILIATION_CX2V001.jsonl'
with open(mp,'x') as f:
 for p in sorted(paths):
  entry={'path':p,'sha256':h(p),'kind':'review' if p.startswith(B) else 'input_at_packaging'}
  if p in r['input_pins']:entry['test_snapshot_sha256']=r['input_pins'][p];entry['matches_test_snapshot']=entry['sha256']==entry['test_snapshot_sha256']
  f.write(json.dumps(entry)+'\n')
entries=[json.loads(x) for x in open(mp)];assert all(h(x['path'])==x['sha256'] for x in entries)
print(json.dumps({'report_sha256':h(B+'REVIEW_RECONCILIATION_CX2V001.md'),'manifest_sha256':h(mp),'entries':len(entries),'changed_since_test':changed,'normalization_checks':34,'date_u':sys.argv[1]}))
