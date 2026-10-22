"""Assemble only completed immutable 0595 evidence; no numerical code import."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
ART=ROOT.parent
PINS={}
def snapshot(p):
    p=Path(p);r=str(p.resolve()).lower()
    if '/runs_ext/uvt_' in r or 'kmax_a2f10_c5h_run_v001' in r or '/.codex/' in r or '/.codex-alt/' in r:raise ValueError('PROTECTED_PATH')
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest();PINS[str(p)]={'sha256':h,'bytes':len(b)};return b,h

def pin(p):return snapshot(p)[1]
def read(p):return json.loads(snapshot(p)[0])

def exclusive(p,obj):
    b=(json.dumps(obj,indent=1,allow_nan=False)+'\n').encode()
    with Path(p).open('xb') as f:f.write(b)
    print(str(p),hashlib.sha256(b).hexdigest())

now=subprocess.check_output(['date','-u'],text=True).strip()
matrices=[];threads=[]
EXPECTED={
'SYNTH_K032_V002':('synthetic',32,[2,6,12],[]),
'SYNTH_K128_V001':('synthetic',128,[2,6,12],[]),
'C4R3_K032_V001':('c4r3',32,[2,6,12],[]),
'C4R3_K128_V001':('c4r3',128,[2,6,12],[]),
'C4R3_K256_V001':('c4r3',256,[2,6,12],[(6,0)]),
'SYNTH_K032_COMBINED_V001':('synthetic',32,[2],[(6,0)]),
}
def roster(rows,keys,expected,label):
    if type(rows) is not list or len(rows)!=len(expected):raise ValueError('INCOMPLETE_ROSTER '+label)
    actual=[]
    for row in rows:
        if type(row) is not dict or any(type(row.get(k)) is not int for k in keys):raise ValueError('TYPED_ROSTER '+label)
        actual.append(tuple(row[k] for k in keys))
    wanted=[(x,) if type(x) is int else tuple(x) for x in expected]
    if sorted(actual)!=sorted(wanted):raise ValueError('WRONG_ROSTER '+label)
def flags(obj,keys,label):
    if any(type(obj.get(k)) is not bool for k in keys):raise ValueError('TYPED_FLAGS '+label)
def array_flags(items,key,label):
    if type(items) is not list or not items:raise ValueError('EMPTY_ARRAY_COMPARISON '+label)
    names=[a.get('name') for a in items]
    if any(type(n) is not str for n in names) or len(set(names))!=len(names):raise ValueError('ARRAY_NAMES '+label)
    if any(not any(n.startswith(prefix) for n in names) for prefix in ('table:','jet1:','jet2:')):raise ValueError('ARRAY_FAMILY_MISSING '+label)
    for a in items:flags(a,[key],label)

for tag in ['SYNTH_K032_V002','SYNTH_K128_V001','C4R3_K032_V001','C4R3_K128_V001','C4R3_K256_V001','SYNTH_K032_COMBINED_V001']:
    folder=ROOT/'runs'/tag;summary=read(folder/'SUMMARY_V001.json');inputs=read(folder/'INPUTS_V001.json');serial=read(folder/'SERIAL_V001.json')
    case,kbig,expected_workers,expected_threads=EXPECTED[tag]
    if (summary['case'],summary['kbig'])!=(case,kbig) or (inputs['case'],inputs['kbig'])!=(case,kbig):raise ValueError('CASE_IDENTITY '+tag)
    if type(inputs['workers']) is not list or any(type(n) is not int for n in inputs['workers']) or sorted(inputs['workers'])!=expected_workers:raise ValueError('INPUT_WORKER_ROSTER '+tag)
    roster(summary['rows'],['workers'],expected_workers,tag+' processes')
    roster(summary.get('thread_rows',[]),['threads','ordinal'],expected_threads,tag+' threads')
    if summary['serial']!=serial or serial.get('production_admissible') is not False:raise ValueError('SERIAL_IDENTITY_OR_PRODUCTION '+tag)
    for item in list(inputs['pins'].values())+[inputs['runner']]:
        if pin(item['path'])!=item['sha256']:raise ValueError('PIN_CHANGED '+item['path'])
    if any(v!='1' for v in inputs['env'].values()):raise ValueError('PROCESS_BLAS1_RECORD_REQUIRED')
    if summary['case']=='c4r3' and (len(summary['rows'])!=3 or {r['workers'] for r in summary['rows']}!={2,6,12}):raise ValueError('SAVED_WORKER_MATRIX_INCOMPLETE')
    variants=[]
    for row in summary['rows']:
        f=folder/('N%02d_V001.json'%row['workers']);d=read(f);cmp=d['comparison'];prep=d['prototype']['preparation'];work=prep['work']
        if d['workers']!=row['workers'] or prep['workers']!=row['workers'] or d['status']!=row['status'] or d['measured']!=row['measured']:raise ValueError('PROCESS_RECORD_JOIN '+str(f))
        flags(cmp,['all_byte_equal','record_equal','state_digest_equal'],str(f));array_flags(cmp['arrays'],'equal',str(f))
        if d['status'] not in ('TESTED_PASS','TESTED_FAIL'):raise ValueError('PROCESS_STATUS')
        passed=cmp['all_byte_equal'] and cmp['record_equal'] and cmp['state_digest_equal'] and all(a['equal'] for a in cmp['arrays'])
        if (d['status']=='TESTED_PASS')!=bool(passed):raise ValueError('STATUS_INCONSISTENCY '+str(f))
        variants.append({'workers_cap':d['workers'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'wall_speedup':d['wall_speedup'],'cpu_speedup':1/d['total_cpu_ratio'],'cpu_cost_ratio':d['total_cpu_ratio'],'comparison_wall_s':d['comparison_wall_s'],'compared_array_count':len(cmp['arrays']),'parent_peak_rss_bytes':d['peak_parent_rss_after_comparison'],'worker_peak_rss_bytes':prep['peak_worker_rss_bytes'],'per_pass':[{'component':w['component'],'doubling_multiplier':w['doubling_multiplier'],'task_count':len(w['blocks']),'unique_task_pid_count':len({b['pid'] for b in w['blocks']}) if all('pid' in b for b in w['blocks']) else None,'node_count':w['node_count'],'scratch_estimate_bytes':w['scratch_estimate_bytes']} for w in work],'source':str(f)})
    matrices.append({'run':tag,'case':summary['case'],'kbig':summary['kbig'],'scope':summary['scope'],'serial':serial,'variants':variants,'source':str(folder/'SUMMARY_V001.json')})
    for row in summary.get('thread_rows',[]):
        f=folder/('THREADS6_REPEAT%d_V001.json'%row['ordinal']);d=read(f)
        if (d['threads'],d['ordinal'])!=(row['threads'],row['ordinal']) or d['status']!=row['status'] or d['measured']!=row['measured']:raise ValueError('THREAD_RECORD_JOIN '+str(f))
        flags(d,['all_arrays_byte_equal','record_equal','digest_equal'],str(f));array_flags(d['arrays'],'byte_equal',str(f))
        threads.append({'run':tag,'case':summary['case'],'kbig':summary['kbig'],'threads_configured':d['threads'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'baseline_wall_s':serial['wall_s'],'baseline_total_cpu_s':serial['total_cpu_s'],'all_arrays_byte_equal':d['all_arrays_byte_equal'],'record_equal':d['record_equal'],'digest_equal':d['digest_equal'],'differing_arrays':[a['name'] for a in d['arrays'] if not a['byte_equal']],'child_peak_rss_bytes':d['measured']['peak_after_jet_rss_bytes'],'parent_peak_rss_bytes':d['parent_peak_after_compare_rss_bytes'],'env':d['env'],'backend':d['backend'],'source':str(f)})
for tag in ['C4R3_K032_THREADS_V001','C4R3_K128_THREADS_V001']:
    folder=ROOT/'runs'/tag;s=read(folder/'SUMMARY_V001.json');expected_k=32 if tag=='C4R3_K032_THREADS_V001' else 128
    if s['case']!='c4r3' or s['kbig']!=expected_k:raise ValueError('STANDALONE_THREAD_CASE')
    roster(s['rows'],['threads','ordinal'],[(1,0),(6,1)],tag+' standalone threads')
    base=next(r for r in s['rows'] if (r['threads'],r['ordinal'])==(1,0))
    for row in s['rows']:
        f=folder/('THREADS%d_REPEAT%d_V001.json'%(row['threads'],row['ordinal']));d=read(f)
        for item in d['pins'].values():
            if pin(item['path'])!=item['sha256']:raise ValueError('PIN_CHANGED '+item['path'])
        if (d['threads'],d['ordinal'])!=(row['threads'],row['ordinal']) or d['status']!=row['status'] or d['measured']!=row['measured']:raise ValueError('STANDALONE_THREAD_RECORD_JOIN')
        flags(d,['all_arrays_byte_equal','record_equal','digest_equal'],str(f));array_flags(d['arrays'],'byte_equal',str(f))
        if row['threads']==1:
            if d['status']!='TESTED_PASS' or not all(d[k] for k in ('all_arrays_byte_equal','record_equal','digest_equal')) or not all(a['byte_equal'] for a in d['arrays']):raise ValueError('THREAD_BASELINE_FAILED')
            if any(v!='1' for v in d['env'].values()):raise ValueError('THREAD_BASELINE_ENV')
            matching=next(m for m in matrices if m['case']==s['case'] and m['kbig']==s['kbig'])
            if d['state_digest']!=matching['serial']['state_digest']:raise ValueError('THREAD_BASELINE_NOT_SAME_PROCESS_BUILD')
            continue
        if (d['threads'],d['ordinal'])!=(row['threads'],row['ordinal']) or d['status']!=row['status'] or d['measured']!=row['measured']:raise ValueError('THREAD_RECORD_JOIN '+str(f))
        flags(d,['all_arrays_byte_equal','record_equal','digest_equal'],str(f));array_flags(d['arrays'],'byte_equal',str(f))
        threads.append({'run':tag,'case':s['case'],'kbig':s['kbig'],'threads_configured':d['threads'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'baseline_wall_s':base['measured']['wall_s'],'baseline_total_cpu_s':base['measured']['total_cpu_s'],'all_arrays_byte_equal':d['all_arrays_byte_equal'],'record_equal':d['record_equal'],'digest_equal':d['digest_equal'],'differing_arrays':[a['name'] for a in d['arrays'] if not a['byte_equal']],'child_peak_rss_bytes':d['measured']['peak_after_jet_rss_bytes'],'parent_peak_rss_bytes':d['parent_peak_after_compare_rss_bytes'],'env':d['env'],'backend':d['backend'],'source':str(f)})
    if pin(ROOT/'threading_tail_cx3v003.py')!=s['runner_sha256']:raise ValueError('THREAD_RUNNER_PIN')
if sorted((t['case'],t['kbig'],t['threads_configured']) for t in threads)!=sorted([('synthetic',32,6),('c4r3',32,6),('c4r3',128,6),('c4r3',256,6)]):raise ValueError('FULL_THREAD_MATRIX_INCOMPLETE')
for t in threads:
    if t['status'] not in ('TESTED_PASS','TESTED_FAIL'):raise ValueError('THREAD_STATUS')
    if t['env'].get('VECLIB_MAXIMUM_THREADS')!='6' or any(v!='1' for k,v in t['env'].items() if k!='VECLIB_MAXIMUM_THREADS'):raise ValueError('THREAD_CONFIGURATION_MISMATCH')
    ok=t['all_arrays_byte_equal'] and t['record_equal'] and t['digest_equal'] and not t['differing_arrays']
    if (t['status']=='TESTED_PASS')!=bool(ok):raise ValueError('THREAD_STATUS_INCONSISTENCY')
prior_path=ART/'tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json';prior=read(prior_path)
if PINS[str(prior_path)]['sha256']!='3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925':raise ValueError('A89_MODEL_PIN_MISMATCH')
if pin(ART/'tail_scheme_impl_c2/kbig_timing_v003/tools/assemble_timing_v003.py')!='a154e3b22c25bc9fb4c6c95255c081d75981f683dc4e44355b781b27f6a9875d':raise ValueError('A89_ASSEMBLER_PIN_MISMATCH')
k256=next(m for m in matrices if m['case']=='c4r3' and m['kbig']==256)
projection=[]
process_data_passed=all(v['status']=='TESTED_PASS' for m in matrices for v in m['variants'])
for name,P in [('C4T-KHI_expected_I7_P3',3),('C4T-KHI_upper_I32_P6',6)]:
    scenario=prior['scenarios'][name];B=prior['measured']['256']['route_b_rot']['solo_estimate']['cold_s'];count=2+2*P
    original=[(b+scenario['tail_solo_estimate']['total_s'])/3600 for b in scenario['baseline_tail_off_full_call_s']]
    for v in k256['variants']:
        if not process_data_passed or v['status']!='TESTED_PASS':continue
        ratio=v['wall_s']/k256['serial']['wall_s'];saving=count*B*(1-ratio)/3600
        projection.append({'status':'UNTESTED_PROJECTION','scenario':name,'workers_cap':v['workers_cap'],'rotation_equivalent_count':count,'prior_rotation_solo_cold_s':B,'measured_k256_wall_ratio':ratio,'prior_full_hours':original,'projected_hours':[h-saving for h in original],'projected_saving_hours':saving,'formula':'T_projected = T_prior - (2+2P)*B_solo_cold*(1 - T_measured_N/T_measured_serial)/3600; all other terms unchanged','assumptions':['Transfer one measured saved rotation-case wall ratio to each inherited rotation-equivalent cold-build term.','The prior A89 full-call hours are a component-based model using measured components, not a measured complete KHI run.','Preserve inherited iteration/pass counts and all non-rotation costs.','Ambient load, resource contention, gas/source states, source profile and future hardware may differ.','No persistent-cache saving is added. No full KHI was run.']})
for f in [ROOT/'SOURCE_ANALYSIS_V002.md',ROOT/'independent_projection_cx3/REVIEW_PROJECTION_CX3V001.md',ROOT/'independent_cx3/REVIEW_CX3V001.md',ROOT/'independent_parent/COMBINED_HARNESS_REVIEW_CX3V001.md',ROOT/'independent_combined_cx3/REVIEW_CX3V001.md',ROOT/'parallel_stars_prototype_cx3v002.py',ROOT/'benchmark_tail_cx3v007.py',Path(sys.executable),Path(__file__),ART/'tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py']:
    pin(f)
for name in ['0595_2026-10-18_codex3_parallel_tail_build_feasibility.md','0601_2026-10-18_all_KHI_measured_r6_no_delay_rule_A89.md','0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md','0617_2026-10-18_all_lanes_multi_agent_concurrent_workstreams.md']:
    pin(ART.parent/'FROM_CODEX'/name)
limits=['Single samples per setting under uncontrolled ambient load; own numerical matrices execute sequentially.','Pool N and VECLIB6 are configured caps; task PIDs do not measure simultaneous workers and actual thread utilization was not instrumented.','RSS is an observed lifetime peak after allocation, not an OS hard memory limit; scratch limits are estimates.','Every state uses TEST_ONLY certificates and production_admissible false. No scientific launch, protected run or target read.','Saved C4R3 prior I1T PASS is carried from the pinned prior evidence, not independently rerun here.','One registered stellar component and rotation-stage grid were numerically exercised; other source/stage classes and spherical residual are UNTESTED.','v003 persistent-cache behavior is source-only; current store rename/cleanup conflicts with immutable-write policy.','Process timings include pool startup/teardown and full cold star preparation plus native build; thread child timings exclude fresh interpreter startup/imports/jets/IPC.','Thread verdict is read from result/summary status; process exit0 alone is not a numerical pass.','All table arrays and returned jet keys were directly byte-compared, plus record/digest; finite218-probe coverage does not prove all possible query points.']
all_proc=all(v['status']=='TESTED_PASS' for m in matrices for v in m['variants']);all_thread=all(t['status']=='TESTED_PASS' for t in threads)
max_parent=max([v['parent_peak_rss_bytes'] for m in matrices for v in m['variants']]+[t['parent_peak_rss_bytes'] for t in threads]);max_worker=max([v['worker_peak_rss_bytes'] for m in matrices for v in m['variants']]+[t['child_peak_rss_bytes'] for t in threads])
if max(max_parent,max_worker)>=8*2**30:raise ValueError('OBSERVED_MEMORY_BOUND_FAILED')
if all_proc:
    fastest=min([{'workers_cap':1,'wall_s':k256['serial']['wall_s']}]+k256['variants'],key=lambda v:v['wall_s'])
    recommendation=('Retain the sealed r5 lineage. For a later reviewed successor, an optional default1 cold-star process count can be integrated into the native cache-miss path, preserving256-batch arithmetic/order/certificates and BLAS1. The fastest setting in this single K256 experiment was cap%d; this is not a general scheduling guarantee. Cache-hit and parallel savings overlap. Estimated development/review cost: one narrow implementation pass and one independent review/byte-replay pass plus measured replay runtime; not a promised elapsed time. No production adoption in this study.'%fastest['workers_cap'])
else:
    recommendation='Do not adopt this prototype: at least one required process byte comparison failed. Diagnose and independently revalidate an immutable successor before performance-based adoption. No usable KHI projection is computed from failed process evidence.'
result={'date_u':now,'status':'STUDY_COMPLETE','process_byte_verdict':'TESTED_PASS' if all_proc else 'TESTED_FAIL','configured_thread_byte_verdict':'TESTED_PASS' if all_thread else 'TESTED_FAIL','matrices':matrices,'thread_comparisons':threads,'projection':projection,'limitations':limits,'observed_peak_rss_bytes':{'parent':max_parent,'worker_or_thread_child':max_worker},'r6_build_names_at_assembly':sorted(p.name for p in (ART/'tail_scheme_impl_c2/driver_r6').glob('BUILD*')),'projection_status':'UNTESTED_PROJECTION' if process_data_passed else 'NOT_COMPUTED_FAILED_PROCESS_BYTES','recommendation':recommendation}
exclusive(ROOT/'MEASUREMENTS_FINAL_V001.json',result)
text='# 0595 parallel-tail feasibility\n\n`date -u`: '+now+'.\n\n'
text+='Process matrix overall verdict: **'+result['process_byte_verdict']+'** across the complete saved C4R3 K32/K128/K256 N2/6/12 matrix. Individual case verdicts remain in the data artifact. Configured VECLIB1-versus6: **'+result['configured_thread_byte_verdict']+'** on the listed finite experiments. All table arrays, records, state digests and order1/order2 jets at218 probes were compared directly. This is nonproduction component evidence, not launch admission.\n\n'
text+='| Saved C4R3 K | Worker cap | Wall s | Wall speedup | Total CPU s | CPU speedup |\n|---:|---:|---:|---:|---:|---:|\n'
for m in matrices:
    if m['case']!='c4r3':continue
    b=m['serial'];text+=f"|{m['kbig']}|1 serial|{b['wall_s']:.3f}|1.000|{b['total_cpu_s']:.3f}|1.000|\n"
    for v in m['variants']:text+=f"|{m['kbig']}|{v['workers_cap']}|{v['wall_s']:.3f}|{v['wall_speedup']:.3f}|{v['total_cpu_s']:.3f}|{v['cpu_speedup']:.3f}|\n"
text+='\nVECLIB configuration comparisons (native build timing; startup/IPC excluded):\n\n| Case | K | 1-config wall s | 6-config wall s | Byte verdict |\n|---|---:|---:|---:|---|\n'
for t in threads:text+=f"|{t['case']}|{t['kbig']}|{t['baseline_wall_s']:.3f}|{t['wall_s']:.3f}|{t['status']}|\n"
text+=f"\nMaximum observed RSS: parent {max_parent/2**30:.3f} GiB; worker/thread child {max_worker/2**30:.3f} GiB. These are measured lifetime peaks; no hard allocation-limit claim.\n\n"
text+='The prototype splits existing independent256-frequency star batches. It retains full-grid nodes, original matrix shapes, component/doubling order, each +=, the global doubling certificate and native cache key. Native gas/source contractions and ring/corner/shell assembly remain unchanged. Full process timing includes preparation and worker creation/teardown. Radius and shell splitting remain source-analysis proposals; changing shapes or reduction grouping needs separate byte proof.\n\n'
text+='KHI projections below are **UNTESTED**. The prior A89 approximately7.84–13.86h values are a component-based full-call model using measured components, not a measured complete KHI run. When process byte validation passes, only the inherited rotation-equivalent cold-build term is scaled by measured K256 wall ratio. Other costs and counts remain fixed; cache savings are not added. Future load and different source/stage states can invalidate the estimate.\n\n| Scenario | Worker cap | Prior modeled full h | Projected full h | Saving h |\n|---|---:|---:|---:|---:|\n'
for x in projection:text+=f"|{x['scenario']}|{x['workers_cap']}|{x['prior_full_hours'][0]:.2f}–{x['prior_full_hours'][1]:.2f}|{x['projected_hours'][0]:.2f}–{x['projected_hours'][1]:.2f}|{x['projected_saving_hours']:.2f}|\n"
text+='\nProjection status: '+result['projection_status']+'.\n'
text+='\n'+result['recommendation']+'\n\n'
text+='Limitations:\n\n'+''.join('- '+x+'\n' for x in limits)
text+='\nFile pins (SHA256 read from bytes):\n\n'
for path,d in sorted(PINS.items()):text+=f"- `{path}` — `{d['sha256']}`.\n"
fp=ROOT/'REPORT_FINAL_V001.md'
with fp.open('x') as f:f.write(text)
print(str(fp),hashlib.sha256(fp.read_bytes()).hexdigest())
pin(ROOT/'MEASUREMENTS_FINAL_V001.json');pin(fp)
exclusive(ROOT/'HASHES_FINAL_V001.json',{'date_u':now,'files':PINS,'scope':'Self-excluding manifest; all hashes from bytes.'})
