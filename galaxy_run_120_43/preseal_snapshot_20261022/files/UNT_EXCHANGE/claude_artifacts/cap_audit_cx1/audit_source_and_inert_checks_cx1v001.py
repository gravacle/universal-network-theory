from pathlib import Path
import ast, hashlib, json, datetime, copy
B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
paths={
'monitor':B/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
's0':B/'s0_launch_kit_c2/s0_kit_c2v003a.py',
's0_serial':B/'s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh',
's0_twin':B/'s0_launch_kit_c2/launch_twin_root_c2v003a.sh',
's0_watch':B/'s0_launch_kit_c2/twin_kill_watch_c2v003a.sh',
'p112':B/'phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py',
'guard':B/'s1_successors_c2/step4_guard_c2v014.py',
'launcher':B/'s1_successors_c2/step4_launcher_c2v015.py',
'binder':B/'s1_successors_c2/step4_bind_c2v011.py',
'dbp':B/'sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json',
'prelaunch':B/'step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py',
's1':B/'s1_successors_c2/s1_path_lib_c2v002c.py',
's1_fill':B/'s1_successors_c2/s1_fill_c2v002c.py',
's1_launch':B/'s1_successors_c2/s1_launch_root_c2v002c.py',
's1_read':B/'s1_successors_c2/s1_read_c2v002c.py',
'h3_entry':B/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py',
'h3_wrapper':B/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py',
'h3_accept':B/'h3_campaign_path_c2/h3_accept_call_c2v004.py',
'orchestrator':B/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
'campaign':B/'calibration_orchestrator_c2/v005/campaign_c2v005.py',
'campaign_sched':B/'sched_s45_c2/v003/campaign_s45_c2v003.py',
'caps':B/'sched_s45_c2/v004/caps_s45_c2v004.py',
'params':B/'sched_s45_c2/v004/build_params_s45_c2v004.py',
'w1_rule':R/'W1_RUN_SHEET/w1_wall_rule_v001.py',
'w1_rebuild':R/'W1_RUN_SHEET/w1_rebuild_v001.py',
'w1_dry':R/'W1_RUN_SHEET/w1_dry_plan_v001.py',
'w1_entry':R/'W1_RUN_SHEET/w1_campaign_entry_v001.py',
'builder':B/'runbook_v002_c2/roster_builder_c2v006.py',
'ngc':B/'ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
'ddo':B/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
'solver':B/'tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py',
'parallel':B/'tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py',
'worker':B/'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py',
'rulings':R/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'}
raw={k:p.read_bytes() for k,p in paths.items()}
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={k:{'path':str(paths[k]),'sha256':sha(v),'bytes':len(v)} for k,v in raw.items()}
rows=[]
def row(id,refs,value,effect,change,large,dependency=''):
 rows.append(dict(id=id,references=refs,value=value,hit_behavior=effect,minimal_change=change,accepts_40_days=large,dependencies=dependency,launch_owner='Claude2 root only; no automatic retry'))
row('MONITOR',['monitor:110-199','monitor:50','monitor:95-107','monitor:28'],'Positive wall; positive integer RSS/output; poll 1s default, <=60s. MAX_SAMPLES=20000. ps timeout20s; TERM grace15s then KILL.', 'Wall/RSS/output exceedance kills group; STOPPED_* with exit/status/result digest. Sample limit only stops receipt sampling; ps failure loses RSS observation. Final wait is unbounded.','Supply finite remaining-phase seconds at each launch; retain machine limits. Add pinned finish and structured cause evidence for A245; do not use infinity.','YES: 3456000 is accepted, only if <= remaining deadline.','Elapsed counter starts at launch; serially queued calls need fresh remaining time. Poll/scan latency means not a precise hard deadline. Monitor does not implement stall alerts.')
row('S0_FIXED',['s0:83-117','s0:363-374','s0:408','s0:674','s0:749-781','s0:867-874','s0:1016-1055'],'Serial wall610324/output146028888064; twin wall22752/output34359738368; RAM137438953472, twin11*RAM. Parse300s/poll.2; max attempt99; reserve21474836480.','Caps enforced via monitor; fixed source-file and argv equality. Kit retry is MISLAUNCH-only; science retries transfer to P112. Parse failure is MISLAUNCH.','Reviewed successor kit/caps source/shell pins accepting root deadline and escalating output, with unlimited nonphysics attempt numbering. Alternate launch requires explicit root-reviewed path; never edit bound argv after preflight.','NO: exact constants reject it.','Keep freeze/spec identity, D9 free space, and twin designed truncation. Raised output cannot bypass reserve.')
row('S0_SHELL_WATCH',['s0_serial:82','s0_serial:202-230','s0_twin:62','s0_twin:151-178','s0_watch:38-89','s0:923'],'Launch-file wait120s; post-mislaunch receipt wait60s; qualified TERM15s then KILL; twin watch poll30s/maxwait30000s; kill qualification ps20s.','Some waits stop controller only, potentially leaving monitor alive. Twin iteration0001+sidecar existence triggers planned stop. Watch timeout alone ends watch, not run.','Separate control waits from physics; reconcile qualified process before retry. Watch until planned stop/receipt/deadline; retain qualified kill. No orphan launch after a controller timeout.','Watch numeric setting configurable; S0 wall remains fixed until successor.','Never treat any STOPPED_* as proof of planned twin truncation; require bound watch reason/evidence.')
row('P112',['p112:33-35','p112:409-436','p112:471-529','p112:773','p112:1213-1220','p112:1280-1320','p112:1360-1450','p112:1848-1861','p112:2103','p112:2178','p112:2228','p112:2337'],'Initial S0 constants; counted retry wall2*FIRST, OUTPUT_CAP output2*FIRST; RSS RAM or11*RAM. Parse300s; stop15+15s; sampler5s(<=10), monitor-gone60s; firstsample60s, receipt60s; kill-target30s.','Two CAP/FAILED statuses can terminalize RULE_C_INVALID; repeated refusals terminalize UNEVALUATED_INFRA_REPEAT; any twin STOPPED_* maps PLANNED_STOP. Generic NONE|EXIT maps FAILED.','cx2v004: model-only identical stage/status/code pair with pinned vocabulary/cause; all nonphysics solo and uncounted; refusal hold; output2*PREVIOUS after every cap; wall fresh ceiling; remove wall ratio; planned twin requires bound stop; retain D6 ownership and residual evidence.','Numeric command validator YES, current policy NO: fixed first/2*first calculations.','Control timeouts are not scientific failures. Caps and wall remain recorded roles; no attempt-count terminal before deadline.')
row('DIRECT_BATCH',['guard:310-313','guard:373','guard:390-392','launcher:19-40','launcher:70-141','binder:1-60','prelaunch:12-59','dbp:1'],'DBP HEADLINE11/SENS9+9/POST_S1 wall100800/output85899345920; DIII4 wall46800/output103079215104; RAM137438953472. Guard maxactive1..6; launcher poll60s, taskpolicy10s.','Safety/refusal/signal drains pending queue; active calls finish. No auto retry or invalidating pair in launcher. Passed requires receipt success. Wall stops can also halt predecessor admission.','New pinned DBP/root-bound config/plan/admission and PRELAUNCH/binder checks. Retry failed call solo with fresh output path. To avoid queued calls overrunning phase, rebind remaining wall at admission or conservatively use remaining time at latest scheduled start.','YES in caps validator with consistent new bindings; immutable old DBP cannot be changed in place.','max_active counts route-A only, not total live calls (A247). PRELAUNCH005 expects guard011 candidate; final guard014 chain needs authorized bridge, not silent substitution. Output sum+reserve stays.')
row('W1_PARENT',['orchestrator:1740-1780','orchestrator:1912-1917','orchestrator:2640-2776','orchestrator:3725-3813','campaign:137-260','campaign_sched:174-317','h3_entry:12-60','h3_wrapper:614-651'],'Positive finite per-call wall/RSS/output; campaign admission wall; orphan default21600s/poll30s/grace120s. Config disk_guard>=output.','Monitor CAP is INFRA; orphan timeout returns ORPHANS_STILL_RUNNING without killing. Campaign wall stops new admissions; active calls drain; pending NOT_STARTED. H3 resolve invalid is disabled for tail-on; reviewed F6 reingest invalid is separate.','New root config/adoption binding, schedule gate and reviewed successor chain. Set per-call and admission ceilings coherently; preserve unfinished calls for root solo retry. Keep orphan control bound independent of science wall via root ruling.','YES numeric per-call and campaign; config/adoption per_call exact match must be regenerated.','Cache identity omits caps but adoption/config pin does not. Do not reuse stale admission just because cache id unchanged. No active process before resolve; never use resolve invalid for infrastructure.')
row('W1_DERIVATION',['caps:21-44','params:122-147','w1_rule:22-25','w1_rule:112-129','w1_rebuild:112-176','w1_dry:143'],'Historical A204 wall144000/orphan144600; static caps source100800 (DDO-off46800); orphan wall+600; campaign172800. kappa1.25*max(1,B/(N-F)),B17; margin1.5; round up hour.','Scheduler estimates and orphan lifetime grow with wall; large per-call wall does not remove separate 2-day admission cutoff.','Root separate expected runtime/slot estimate from enforcement ceiling. Retain measured kappa for planning and expected stage times. Successor caps + adoption/config; orphan independent reconciler. Rebuild only whole-hour values: round DOWN<=deadline or successor accepts seconds.','40days YES to rebuild; arbitrary remaining seconds NO due whole-hour constraint.','A204 is registered historical value, not verified live config. Do not turn a 40-day ceiling into expected runtime or stage-stall threshold.')
row('H3_F6',['h3_accept:96-119','h3_accept:255','h3_wrapper:614-651'],'MAX_PASSES2; only INCOMPLETE rerunnable; second incomplete halts for root; third refused.','Nonphysics interruption may consume acceptance pass and hit limit; does not itself certify model invalid. F6 only named NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT with guarded reading can certify invalid.','Reviewed repair/retry successor for nonphysics acceptance interruptions without consuming physics allowance; preserve F6 predicate and root hold. Never treat cap as F6 invalid.','No own scientific wall.','Keep F6 numerical certificate semantics separate from A245 interruption-pair logic.')
row('S1',['s1:98-102','s1:940-987','s1:1088','s1:1303-1332','s1:1495','s1:1650-1683','s1_fill:66-82'],'POST_S1 DBP caps; launch wrapper timeout600s; ps30s; fill --params successor supported.','Monitor stop requests fresh cap-raised path; OTHER_FAILED second identical described as deterministic defect for review. Spawn timeout may leave detached launcher alive. No automatic invalidating pair here.','Pass new pinned DBP via --params; fresh plan/admission. Reconcile detached worker before retry. Amend generic-failure guidance for source-proven model stage/code only; all nonphysics solo.','YES caps from new DBP; no runtime maximum in lib.','600s is controller timeout, not intended call lifetime. CLI wrappers pin lib; successor pins must propagate.')
row('ROSTER',['builder:114-124','builder:660-694','builder:697-767','builder:1328'],'FAILURE_CLASSES includes CAP/OUTPUT_CAP; pair requires same raw/spec, both solo, RSS RAM, wall2*FIRST, output raised.','Terminal pair closes prefix (CAP disposition distinct from MEMBER_INVALID); generic FAILED can participate without cause evidence.','c2v007 must exclude all nonphysics, pin code-of-record and cause evidence, match stage/status/failure code and science spec across model pair; remove wall ratio; retain wall_cap_s receipt role; twin RSS11*RAM; DN5 UNEVALUATED_SCHEDULE_CEILING; refusal hold never INFRA_REPEAT terminal.','Ceiling wall record can be numeric but OLD pair validator rejects non-doubled wall.','Unpublished c2v007 is UNTESTED. Preserve existing budget/DN5/custody rules except explicit A244-246 changes.')
row('DRIVER_INTERNAL',['ngc:1825-1964','ddo:1825-1964','ngc:6362-6397','parallel:412-414','parallel:926'],'Stage child wait unbounded; NGC metadata digest64MiB; worker close joins2/5/5 seconds. Solver iteration budget fixed by scientific spec.','Any nonzero stage child becomes FAILED_AT_STAGE, including signals. NGC digest cap is Refusal. Pool transport is ColumnPoolError. Worker joins are cleanup, not run wall.','Do not extend solver iteration budget under cap rule. Metadata refusal needs root-reviewed fix; transport and cleanup failures uncounted. Pin child failure and stage exit evidence.','No extra arbitrary scientific wall identified in scanned drivers/solvers.','No transitive HI-physics exception-message allowlist certified in this audit; unknown causes hold uncounted.')
# Exhaustive syntactic raise inventory of the two requested driver source files and inspected solver/pool/worker.
inv=[]; statuses=[]
for key in ['ngc','ddo','solver','parallel','worker']:
 tree=ast.parse(raw[key]); src=raw[key].decode()
 for n in ast.walk(tree):
  if isinstance(n,ast.Raise):
   ex=n.exc; name=ast.unparse(ex.func) if isinstance(ex,ast.Call) else ast.unparse(ex) if ex else 'reraise'
   classification='NONPHYSICS' if name in ['Refusal','Blocked','ColumnPoolError','OSError','MemoryError'] else 'UNRESOLVED_UNCOUNTED'
   if name=='RouteANoFixedPoint':classification='MODEL_CANDIDATE_REQUIRES_OUTCOME_AND_CAUSE'
   inv.append({'source':key,'line':n.lineno,'exception':name,'expression':ast.get_source_segment(src,n),'classification':classification})
  if isinstance(n,ast.Assign):
   if any(isinstance(t,ast.Name) and t.id=='status' for t in n.targets):
    statuses.append({'source':key,'line':n.lineno,'expression':ast.get_source_segment(src,n)})
# Execute ONLY five extracted pure functions, with inert dict inputs and constants. Never import source modules.
tree=ast.parse(raw['p112']); wanted={'raw_status','terminal_prefix','first_caps','caps_of','next_attempt'}
ns={'RAM':137438953472,'TWIN':'S0_SEED_CW8_TWIN'}
ns['CAPS']={'serial':{'wall_cap_s':610324,'rss_cap_bytes':ns['RAM'],'output_cap_bytes':146028888064},'twin':{'wall_cap_s':22752,'rss_cap_bytes':ns['RAM']*11,'output_cap_bytes':34359738368}}
ns['STATUS_CLASSES']=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='STATUS_CLASSES' for t in n.targets))
def need(c,*a):
 if not c:raise ValueError(a)
ns['need']=need
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted],type_ignores=[]),'<extracted-pure-p112>','exec'),ns)
base={'status_class':'CAP','raw_status':'STOPPED_RSS_CAP|NONE','spec_sha256':'a'*64,'other_ngc_processes_max':0,'solo_mode':True,'host_ram_bytes':ns['RAM'],**ns['CAPS']['serial']}
second={**base,'wall_cap_s':2*base['wall_cap_s']}
tests=[]
def check(name,got,want):
 assert got==want,(name,got,want)
 tests.append({'name':name,'observed':got,'expected_existing_behavior':want,'reproduced':True})
check('CAP pair wrongly terminal',ns['terminal_prefix']([base,second],'J1')['disposition'],'RULE_C_INVALID')
check('Twin arbitrary cap wrongly planned',ns['raw_status']({'status':'STOPPED_RSS_CAP'},name=ns['TWIN'],attempt=1,outdir='inert',receipt='inert',launch_pin={},child_pid=1)[0],'TWIN_PLANNED_STOP')
f={**base,'status_class':'INFRA','raw_status':'CHILD_FAILED|REFUSED'}
check('Repeated refusal wrongly terminal',ns['terminal_prefix']([f,copy.deepcopy(f)],'J1')['disposition'],'UNEVALUATED_INFRA_REPEAT')
check('No-finish normal exit wrongly FAILED',ns['raw_status']({'status':'CHILD_FAILED','driver_status':None,'exit_code':1},name='J1',attempt=1,outdir='inert',receipt='inert',launch_pin={},child_pid=1)[1],'FAILED')
check('CAP retry counted',ns['next_attempt']('J1',[],[base],[])['counted_rerun'],True)
# Avoid early pair termination with different raw stops; demonstrate ceiling stuck at 2*FIRST rather than rolling escalation.
third={**second,'raw_status':'STOPPED_WALL_CAP|NONE'}
check('Later CAP wall still twice first',ns['next_attempt']('J1',[],[base,third],[])['caps']['wall_cap_s'],1220648)
vocab={
 'schema':'CX1_A245_SOURCE_VOCABULARY_REVIEW_DRAFT_V001',
 'adoption':'ROOT REVIEW REQUIRED; audit vocabulary is not launch or invalidation authority',
 'driver_finish_statuses':{
 'COMPLETED':'SUCCESS; not interruption', 'COMPLETED_INVALID':'Completed result validity route; not automatically a failure pair',
 'REFUSED':'NONPHYSICS; hold root fix', 'BLOCKED':'NONPHYSICS; hold root fix',
 'FAILED':'UNRESOLVED_UNCOUNTED unless affirmative source-bound model code and identical solo reproduction',
 'FAILED_AT_STAGE':'UNRESOLVED_UNCOUNTED; stage nonzero includes signals and tooling faults',
 'ROUTE_A_NO_FIXED_POINT':'MODEL_CANDIDATE: authenticate solver outcome; same stage/status/code solo reproduction required'},
 'model_candidates':[
 {'status':'ROUTE_A_NO_FIXED_POINT','outcome':'ITERATION_BUDGET_EXHAUSTED','decision':'MODEL only for clean solver-return path with no infrastructure cause, authenticated stage and unchanged scientific iteration budget, reproduced solo','refs':['solver:241-243','parallel:358-360','ngc:1883-1964','ddo:1883-1964']},
 {'status':'ROUTE_A_NO_FIXED_POINT','outcome':'FAILED_SOURCE_PREPARATION','decision':'CONDITIONAL, DEFAULT UNCOUNTED: catches ValueError in HI column solve/metric; exact exception source must be reviewed to establish physical/numerical origin; generic ValueError is insufficient','refs':['solver:187-200','parallel:300-313']}],
 'nonphysics_codes':['MASK_NOT_FIRED','ROUTE_A_RESULT_UNREADABLE','ROUTE_A_RESULT_INCONSISTENT','NGC_RECORD_DIGEST_CAP','ColumnPoolError','UNREADABLE_FINISH','RESULT_HASH_MISMATCH','MISLAUNCH','NONE|EXIT','signals','OSError','MemoryError','IO/disk-full','monitor/volume loss','operator stop','all CAP'],
 'inventory_note':'All syntactic raises and status assignments in pinned requested drivers are inventoried, including superseded clones; inventory is not an assertion each clone executes. Imported transitive physics exceptions and dynamically formatted code suffixes are not an exhaustive runtime vocabulary. Unknowns remain uncounted.',
 'live_ngc_refs':['ngc:8989-9102','ngc:9183-9216'], 'live_ddo_refs':['ddo:3477-3597'],
 'required_evidence':['pinned finish and result bytes with exact association','driver/code-of-record list digest','stage name','solver outcome/failure code','exception type and source origin','stage exit/signal','pinned worker failure/log evidence where needed','identical science spec across attempts','both solo with qualified process samples','same model stage/status/code in rerun; wall is not evidence']}
gaps=[
 {'id':'CAP-01','finding':'S0 fixed caps and attempt99 bound cannot implement ceiling and unlimited nonphysics retries','blocks':'S0 conforming successor launch'},
 {'id':'CAP-02','finding':'P112 class/terminal/retry policy contradicts A244-246, including false twin planned stop','blocks':'P112 closure/rerun and terminal accounting'},
 {'id':'CAP-03','finding':'Builder c2v006 counts nonphysics and requires doubled wall','blocks':'conforming roster freeze until c2v007 reviewed'},
 {'id':'CAP-04','finding':'Monitor/driver records lack directly pinned complete stage/cause vocabulary evidence for ambiguous failures','blocks':'counting ambiguous FAILED/FAILED_AT_STAGE or generic solver ValueError as model'},
 {'id':'CAP-05','finding':'Static DBP, W1 wall/orphan/admission budgets and S1 defaults remain arbitrary; no absolute phase freeze deadline supplied in reviewed dispatches','blocks':'root ceiling-bound plans and coherent scheduling'},
 {'id':'CAP-06','finding':'H3 acceptance two-pass limit and controller timeout residue need explicit nonphysics repair procedure; stall-watch alerts not implemented by these launchers','blocks':'automatic conformance claim; root procedure required'}]
report={'schema':'CAP_AUDIT_CX1V001','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dispatches':[796,797,799],'verdict':'FAIL','blocking_count':len(gaps),'meaning':'Implementation conformance FAIL; read-only audit delivered, not a scientific verdict','pins':pins,'paths':rows,'findings':gaps,'driver_vocabulary':vocab,'raise_inventory':inv,'status_assignment_inventory':statuses,'inert_reproductions':tests,'TESTED':['source bytes hashed; Python AST parsed','six pure P112 inert reproductions; no source imports or subprocess launches'],'UNTESTED':['production launch/seal/runs/target data','future P112 cx2v004 and builder c2v007','full transitive HI physical exception vocabulary','actual non-content ps/stage signals, performance and real retries','verdict-day command sheet 0801 pending']}
# Confirm the immutable code/config inputs are byte-identical to snapshot. Root journal is append-only/mutable: do not carry its hash forward silently.
for k,p in paths.items():
 if k!='rulings':assert p.read_bytes()==raw[k],('changed source',k)
report['source_identity_recheck']='PASS for all code/config inputs; root rulings hash is snapshot only'
md=['# Combined cap and interruption audit — CX1V001','', 'FAIL — 6 implementation-conformance blockers. Audit scope: dispatches 0796, 0797, 0799; A244–A246. This is not launch approval or a scientific outcome. All launches and stops remain root-owned.','', 'A246 supersedes A244 wall doubling: use finite remaining time to the actual phase freeze deadline at launch. Forty days is a numeric compatibility probe, not a registered deadline. Output doubles after a CAP end; RSS stays at RAM (twin 11×RAM). Other nonphysics retries stay solo with the same machine settings and a freshly bounded wall. Repeated gate refusals are held for repair. Only the schedule ceiling makes them UNEVALUATED_SCHEDULE_CEILING / FREEZE_INCOMPLETE.','', '## Blocking findings','']
for g in gaps:md.append(f"- **{g['id']}**: {g['finding']}. Blocks: {g['blocks']}.")
md+=['','## Per-path table','','Each source key resolves to an absolute path and SHA-256 below; line references identify current source bytes.','', '| Path | Caps / waits | Hit and next step | 40-day compatibility / minimum change |','|---|---|---|---|']
for r in rows:md.append('| '+r['id']+' ('+', '.join(r['references'])+') | '+r['value']+' | '+r['hit_behavior']+' | '+r['accepts_40_days']+' '+r['minimal_change']+' |')
md+=['','## Dependencies and stall watch','']
for r in rows:md.append(f"- {r['id']}: {r['dependencies']}")
md+=['', 'All monitor-backed paths expose child PID and command/spec identity in launch receipts. Root can sample cumulative CPU time for the qualified process tree (not just an idle parent), and stage directory names/mtimes. Directory stages are coarse signals: a long stage may have no new directory while workers are busy. Neither sampling implementation nor real process/stage accessibility was tested here. Root must bind ps identity against PID reuse, treat missing signals as infrastructure uncertainty, and obtain the expected stage duration from a permitted finished sibling. Alert after CPU stagnation for 2 h or no new stage for 3× expected duration; no automatic stop. Record root evidence and decision in V006 before any stop and notify the principal. No protected run was inspected for this audit.', '', '## Driver vocabulary and counted-pair evidence','', 'The JSON includes every syntactic raise and status assignment in the two pinned driver source files plus the inspected serial solver, parallel solver and worker. Superseded driver clones are retained with locations, not represented as live. NGC live dispatch is ngc:9183–9216 to strict clone 8989–9102; DDO live handlers are ddo:3558–3597.', '', 'COMPLETED and COMPLETED_INVALID are completed outcomes, not interruption failures. REFUSED and BLOCKED are nonphysics. FAILED and FAILED_AT_STAGE are uncounted unless affirmative cause evidence establishes a named model outcome. Both drivers aggregate any stage-child nonzero exit, including signals, into StageFailed (1825–1864). Their generic catch records exception type/message and traceback in result, while finish contains status/reasons/result SHA but no structured stage/failure code. Route-A mapping treats any converged flag other than True as ROUTE_A_NO_FIXED_POINT (1883–1964), so that label alone must not authenticate malformed or missing evidence.', '', 'Clean ITERATION_BUDGET_EXHAUSTED is a model nonconvergence candidate under the unchanged scientific iteration budget. FAILED_SOURCE_PREPARATION catches ValueError from column solve/metric; it is only a conditional candidate until the exact exception origin is reviewed. Unknown transitive errors remain uncounted. The vocabulary is a root-review draft: no generic ValueError or FAILED allowlist is certified. The requested complete runtime model-code certification therefore remains limited by CAP-04; the syntactic inventory is complete for its declared files.', '', 'Monitor receipt pins driver/spec/monitor and result bytes, records exit code (negative values identify POSIX signals), stop reason and driver status. It does not hash finish or stdout/stderr; driver stage_records carry exit and request pin but do not hash stage logs. A245 pair evidence must authenticate finish/result association, named model stage/status/code and exception origin, plus solo/spec identity, on both attempts. Pin a cause record and any consulted worker failure/log bytes. A printed stderr tail without a source digest is insufficient. Monitor/result custody loss is never model invalidation.', '', '## Verification','', 'TESTED: source-byte SHA-256 and identity recheck; AST inventory; six extracted pure-function inert reproductions of existing P112 defects (all reproduced). No source module import, monitor, solver, launch, seal, production fixture or protected data access. UNTESTED: successor implementations, full imported HI exception vocabulary, production behavior, stall watch and live deadlines. The accompanying JSON contains exact reproduction outputs and all hashes.', '', '## Source pins','']
for k,v in pins.items():md.append(f"- `{k}`: `{v['path']}` — SHA-256 `{v['sha256']}` ({v['bytes']} bytes).")
D=Path('/private/tmp/cx1_cap_audit0796_prepared');D.mkdir(exist_ok=False)
for name,data in [('CAP_AUDIT_CX1V001.json',json.dumps(report,indent=2)+'\n'),('CAP_AUDIT_CX1V001.md','\n'.join(md)+'\n'),('A245_DRIVER_VOCABULARY_CX1V001.json',json.dumps({'pins':{k:pins[k] for k in ['ngc','ddo','solver','parallel','worker']},**vocab},indent=2)+'\n')]:
 with (D/name).open('x') as f:f.write(data)
print(json.dumps({'prepared':str(D),'rows':len(rows),'raises':len(inv),'statuses':len(statuses),'tests':tests,'hashes':{p.name:sha(p.read_bytes()) for p in D.iterdir()}},indent=2))
