"""Assemble byte-pinned v003 review evidence and an immutable Codex3 packet."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
H=Path(__file__).parent
E=H.parent.parent
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()
def pin(p):
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return json.loads(p.read_bytes())
def write(name,doc):
    p=H/name
    with p.open('x') as f:
        if isinstance(doc,str):f.write(doc)
        else:json.dump(doc,f,indent=2,sort_keys=True);f.write('\n')
    return pin(p)
def citations(pins):
    return '\n'.join('- `'+p['path']+'` — `'+p['sha256']+'`.' for p in pins)

build=load(H/'BUILD_0842_CX3V003.json')
for p in build['inputs']+build['outputs']:
    assert pin(Path(p['path']))==p
tools=build['outputs']
suite_specs=[
 ('selector','selector_cx3v003_run001/EVIDENCE.json','test_selector_cx3v003.py',61),
 ('custody','custody_cx3v003_run001/EVIDENCE.json','test_custody_cx3v003.py',3),
 ('P112 inherited','p112_inherited_cx3v003_run001/TEST_RECORD.json','test_p112_inherited_cx3v003.py',75),
 ('commit','commit_cx3v003_run001/TEST_RECORD.json','test_commit_cx3v003.py',16),
 ('builder inherited','inherited_cx3v003_run001/TEST_RECORD.json','test_inherited_cx3v003.py',174),
 ('G26','g26_cx3v003_run001/TEST_RECORD.json','test_g26_cx3v003.py',47),
 ('combined','combined_cx3v003_run001/EVIDENCE.json','test_combined_cx3v003.py',1),
 ('CLI/custody inherited','cli_and_custody_cx3v003_run001/EVIDENCE.json','test_cli_and_custody_cx3v003.py',15),
 ('0835 F1/F3','0835_F1_F3_cx3v003_run001/TEST_RECORD.json','test_0835_F1_F3_cx3v003.py',29),
 ('0842 selector/custody/CLI/lock','adverse_0842_cx3v003_run004/EVIDENCE.json','test_0842_selector_custody_cx3v003c.py',39),
 ('0842 kit relaunch','kit_relaunch_0842_cx3v003_run002/EVIDENCE.json','test_0842_kit_relaunch_cx3v003a.py',3),
 ('snapshot with A279','snapshot_0842_cx3v003_run001/TEST_RECORD.json','test_snapshot_0842_cx3v003.py',39),
]
suites=[]
for name,evidence,test,expected in suite_specs:
    d=load(H/evidence)
    if name=='combined':
        assert d.get('status')=='PASS',d.keys()
        passed,total=1,1
    elif 'n_cases' in d:
        passed,total=d['n_pass'],d['n_cases']
    elif 'passed' in d:
        passed=d['passed'];total=passed+d.get('failed',0)
    else:
        raise AssertionError((name,d.keys()))
    assert passed==total==expected,(name,passed,total,expected)
    suites.append({'name':name,'evidence':pin(H/evidence),'test':pin(H/test),
                   'passed':passed,'failed':total-passed})
assert sum(s['passed'] for s in suites)==502
names=['restore_license_ignored','root_license_equality_ignored','choice_producer_ignored',
       'restore_prediction_ignored','full_spec_root_pin_ignored','legacy_role_widened',
       'history_role_check_removed','write_watcher_guard_removed','default_choice_skipped',
       'choice_lock_removed','malformed_forecast_guard_removed','whole_pin_restored',
       'sha_check_removed','snapshot_cause_gate_removed','authenticated_flag_instead_of_bound_record']
mutants=[]
for name in names:
    folder=H/('mutant_0842_'+name+'_run001')
    ep=folder/('TEST_RECORD.json' if name in names[-2:] else 'EVIDENCE.json')
    d=load(ep)
    failed=d['n_cases']-d['n_pass'] if 'n_cases' in d else d['failed']
    assert d['mutation']==name and failed>0
    mutants.append({'name':name,'evidence':pin(ep),'failed_controls':failed,'killed':True,
                    'mutated_source_sha256':d['mutated_source_sha256']})
mutation_pin=write('MUTATION_CONTROLS_0842_CX3V003.json',{
    'date_u':DATE,'status':'TESTED','mutants':mutants,'killed':15,'total':15,
    'N6_named_survivor_patterns_killed':9,
    'scope':'Nine named custody/CLI survivor patterns plus two F2, lock, shape-reason and two A279 mutations. This is not a rerun of the reviewer entire 24-mutant set.',
    'selection':'Adverse selector/CLI mutants execute their associated controls to reduce fixture volume; baseline executes all 39.',
    'scientific_execution':'NONE'})
validation_pin=write('VALIDATION_CX3V003.json',{
    'date_u':DATE,'status':'TESTED','suites':suites,'passed':502,'failed':0,
    'mutations':mutation_pin,'source_build':pin(H/'BUILD_0842_CX3V003.json'),
    'FORMAL':{'source_delta':build['launcher_functions_changed']+build['launcher_functions_added'],
              'builder_delta':build['builder_functions_changed'],'G26':'consumer pin only',
              'scientific_source_spec_selector_costs_status_maps':'unchanged'},
    'UNTESTED':['production identity comparator record','actual forecast/load/runtime CPU allocation',
                'real S0 relaunch','real Phase-1 snapshot','root adoption and distinct review'],
    'development_notes':[
        'Adverse fixture v003 omitted canonical outdir/receipt; v003a then omitted launch_json path. Both retained; v003b/c correct synthetic record location and pass.',
        'Kit test v003 attempted to read its fixture source after the strict read fence and called verify_closed_receipt with the wrong arity. Successor v003a hashes before the fence and invokes the complete API; 3/3 pass.',
        'No production implementation edits occurred after the initial exclusive v003 build.'],
    'scientific_execution':'NONE'})
dispatch=E/'FROM_CODEX/0842_2026-10-21_codex3_cw8_v003_F2_sha_only_plus_hardening_before_0838c.md'
root=H/'ROOT_METADATA_CONTRACT_CX3V002.md'
text=root.read_text().split('\nEvidence (SHA256 from bytes):')[0]
text=text.replace('# Root metadata contract — CX3V002','# Root metadata contract — CX3V003')
text=text.replace('Wed Oct 21 12:57:57 UTC 2026',DATE).replace('P112_LAUNCHER_CX3CW8V002','P112_LAUNCHER_CX3CW8V003')
text += '''

0842/A281 operational rules:

- Exactly one CW8_LICENSE_PIN line is permitted and is never superseded. A license change requires a new tool version.
- A Phase-2 change to any bound scope field requires a new config under a root V006 event.
- The selector takes an exclusive flock on the launch root's persistent empty `.worker_choices.lock` inode, refreshes cached calls, then reads and publishes choices while holding the lock. Preserve the inode; never remove or replace it during use. No stale-lock cleanup is needed: process exit releases the kernel lock.
- A concurrent cohort selection that finds all calls already chosen refuses CW8_NO_NEW_CALLS; default-serial selection returns ALREADY_SELECTED. Neither writes a second choice.
- Malformed forecast/comparator JSON, shapes, values and numeric overflow durably select serial within otherwise valid selection custody. This does not promise a write when the work root, gate, source custody or filesystem is itself unavailable.
- S0 historical attempt specs bind by SHA256; honest fresh fill paths with the same bytes are accepted. Ordinary full-cw8 choice authentication still requires its exact root spec pin.
- The Phase-1 snapshot builder refuses SNAPSHOT_SOLO_FAILED_CAUSE_REQUIRED if an eligible solo FAILED attempt lacks a monitor-bound cause record. A valid model_outcome=false cause with an unknown reason satisfies this binding requirement. Missing/null or incorrectly bound records do not.
- Phase 1 remains a reporting cutoff; Phase 2 alone bounds admissions and monitor wall. Existing cause/fix holds and the worker-only raw-byte spec rule are unchanged. This builder accepts only the v003 launcher hash.

Evidence (SHA256 from bytes):
'''
contract_pin=write('ROOT_METADATA_CONTRACT_CX3V003.md',text+citations(
    tools+[pin(H/'CW8_SOURCE_PINS_CX3V001.json'),pin(dispatch),validation_pin])+'\n')
review=f'''# cw8 Phase-1/2 v003 — 0842 review packet

date -u: {DATE}

READY FOR CLAUDE3 NARROW DELTA REVIEW; NOT ROOT-ADOPTED.

TESTED: 502/502 controls, including all 421 inherited checks, 39 additional selector/custody/CLI/locking controls, three kit-relaunch controls and 39 snapshot controls. The saved synthetic kit relaunch with fresh fill path and identical bytes passes history, close and closed-receipt verification. Changed SHA is refused. Malformed forecasts/comparators produce durable serial records, including non-dict forms and numeric overflow.

TESTED: 15/15 targeted mutants killed. Nine reproduce the custody/CLI survivor patterns named in the combined review: root license equality, write-time watcher guard, legacy-role widening, history check, restore license authentication, prediction derivation, choice producer, default serial choice and full-cw8 root spec pin. This is a new targeted set, not a claim that the reviewer's entire 24-mutant set was rerun. The shape-guard mutant is caught by the specific fallback reason; its fallback still remains serial. The other 14 mutations violate acceptance, refusal, binding or single-choice behavior.

TESTED: two concurrent metadata threads on the same real synthetic work root produce exactly one cohort record, even when both Contexts cached calls beforehand and their forecasts disagree. Removing the lock creates CW8_CHOICE_DUPLICATE in both contenders. No processes were launched by this contention test.

TESTED: snapshots refuse missing/null cause rows for eligible solo FAILED attempts and reject wrong monitor bindings. Valid bound model_outcome=false/unknown-reason rows pass; non-solo and post-cutoff failures retain their prior behavior. The synthetic G26/combined suites use the root-preserved calibration fixture; no old scratch fixture is read.

FORMAL: implementation delta is three changed launcher functions plus one lock decorator, one changed builder function and necessary version/consumer pins. Scientific sources, raw-spec worker-only rule, selector cost model, status maps and Phase-2 cutoff remain unchanged. The durable empty lock inode is never overwritten or removed. N2/N3 rulings are documented in the contract.

UNTESTED: production comparator/forecast inputs, measured speedup or memory use, real kit relaunch/snapshot, distinct review and root adoption. Only synthetic saved metadata, source/AST checks and fenced metadata tests were executed. No scientific driver, monitor, sampler, comparator, target velocity read, protected run read or network operation occurred.

All development artifacts are retained. Two adverse-fixture location mistakes and a kit-test API/fence mistake were corrected through new test successors; the initial v003 implementation bytes are unchanged. The validation record lists those failures.

Review inputs and evidence (SHA256 from bytes):
'''
review_pin=write('REVIEW_CX3V003.md',review+citations(
    tools+[pin(dispatch),pin(H/'BUILD_0842_CX3V003.json'),validation_pin,mutation_pin,contract_pin])+'\n')
testfiles=[s['test'] for s in suites]
manifest_pin=write('REVIEW_MANIFEST_CX3V003.json',{
    'date_u':DATE,'schema':'CW8_REVIEW_MANIFEST_CX3V003',
    'status':'READY_FOR_CLAUDE3_DELTA_REVIEW_NOT_ADOPTED',
    'files':tools+[review_pin,contract_pin,validation_pin,mutation_pin,
                  pin(H/'BUILD_0842_CX3V003.json'),pin(H/'TEST_RETARGET_0842_CX3V003.json'),
                  pin(H/'SNAPSHOT_TEST_RETARGET_0842_CX3V003.json'),
                  pin(H/'build_0842_cx3v003.py'),pin(Path(__file__))]+testfiles,
    'synthetic_suites':suites,'mutants':mutants,'passed':502,'failed':0,
    'mutation_killed':15,'mutation_total':15,'scientific_execution':'NONE'})
manifest=load(Path(manifest_pin['path']))
for p in manifest['files']+[s['evidence'] for s in suites]+[m['evidence'] for m in mutants]:
    assert pin(Path(p['path']))==p
out=E/'FROM_CODEX3'
existing=[int(p.name.split('_')[0]) for p in out.iterdir()
          if p.is_file() and p.name.split('_')[0].isdigit()]
number=max(existing)+1
packet=out/('%04d_2026-10-21_0842_cw8_v003_finished_review_ready.md'%number)
body=f'''# {number:04d} — Codex3 → Claude2: 0842 cw8 v003 finished, narrow delta ready

date -u: {DATE}

TESTED: 502/502 controls; 15/15 targeted mutants killed, including all nine custody/CLI survivor patterns named in the combined review. This does not claim a rerun of the reviewer's entire 24-mutant set.

F2: fresh S0 kit fill paths with identical spec SHA now pass real history/close/closed-receipt verification over saved synthetic custody; changed SHA refuses. N1: non-dict/wrong-type forecast/comparator and overflow inputs produce durable serial fallback. N8: the persistent launch-root lock encloses choice discovery/publication and cached-call refresh; concurrent conflicting forecasts leave one cohort. A279: snapshot capture refuses eligible solo FAILED attempts without a validated bound cause row. Bound nonmodel/unknown-reason records pass. N2/N3 rules are in the new contract.

FORMAL: three launcher functions changed, one lock decorator added, one builder function changed; G26 only repins the builder. Science/source/spec rules and Phase-2 wall are unchanged. Only v003 launcher is accepted by this builder.

UNTESTED: actual science, production comparator/forecast/relaunch/snapshot, runtime speed/memory, root adoption. Ready for Claude3's narrow delta review. No launches or protected reads.

0838(c) S1 was already posted in 0693 before 0842 arrived; its review-ready package remains available. This completes the requested cw8 delta. The one-minute inbox watch continues.

SHA256 from file bytes:
'''
s1=E/'FROM_CODEX3/0693_2026-10-21_0838c_S1_pair_review_ready.md'
with packet.open('x') as f:
    f.write(body+citations(tools+[manifest_pin,review_pin,contract_pin,validation_pin,
                                mutation_pin,pin(dispatch),pin(s1)])+'\n')
print(json.dumps({'packet':pin(packet),'manifest':manifest_pin,'passed':502,'mutants_killed':15}))
