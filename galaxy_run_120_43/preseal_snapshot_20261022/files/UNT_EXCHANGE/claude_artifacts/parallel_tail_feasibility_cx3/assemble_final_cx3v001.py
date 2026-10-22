"""Assemble only completed immutable 0595 evidence; no numerical code import."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
ART=ROOT.parent
PINS={}
def pin(p):
    p=Path(p);r=str(p.resolve()).lower()
    if '/runs_ext/uvt_' in r or 'kmax_a2f10_c5h_run_v001' in r or '/.codex/' in r or '/.codex-alt/' in r:raise ValueError('PROTECTED_PATH')
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest();PINS[str(p)]={'sha256':h,'bytes':len(b)};return h

def read(p):
    pin(p);return json.loads(Path(p).read_bytes())

def exclusive(p,obj):
    b=(json.dumps(obj,indent=1,allow_nan=False)+'\n').encode()
    with Path(p).open('xb') as f:f.write(b)
    print(str(p),hashlib.sha256(b).hexdigest())

now=subprocess.check_output(['date','-u'],text=True).strip()
matrices=[];threads=[]
for tag in ['SYNTH_K032_V002','SYNTH_K128_V001','C4R3_K032_V001','C4R3_K128_V001','C4R3_K256_V001','SYNTH_K032_COMBINED_V001']:
    folder=ROOT/'runs'/tag;summary=read(folder/'SUMMARY_V001.json');inputs=read(folder/'INPUTS_V001.json');serial=read(folder/'SERIAL_V001.json')
    for item in list(inputs['pins'].values())+[inputs['runner']]:
        if pin(item['path'])!=item['sha256']:raise ValueError('PIN_CHANGED '+item['path'])
    variants=[]
    for row in summary['rows']:
        f=folder/('N%02d_V001.json'%row['workers']);d=read(f);cmp=d['comparison'];prep=d['prototype']['preparation'];work=prep['work']
        passed=cmp['all_byte_equal'] and cmp['record_equal'] and cmp['state_digest_equal'] and all(a['equal'] for a in cmp['arrays'])
        if (d['status']=='TESTED_PASS')!=bool(passed):raise ValueError('STATUS_INCONSISTENCY '+str(f))
        variants.append({'workers_cap':d['workers'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'wall_speedup':d['wall_speedup'],'cpu_speedup':1/d['total_cpu_ratio'],'cpu_cost_ratio':d['total_cpu_ratio'],'comparison_wall_s':d['comparison_wall_s'],'compared_array_count':len(cmp['arrays']),'parent_peak_rss_bytes':d['peak_parent_rss_after_comparison'],'worker_peak_rss_bytes':prep['peak_worker_rss_bytes'],'per_pass':[{'component':w['component'],'doubling_multiplier':w['doubling_multiplier'],'task_count':len(w['blocks']),'unique_task_pid_count':len({b['pid'] for b in w['blocks']}) if all('pid' in b for b in w['blocks']) else None,'node_count':w['node_count'],'scratch_estimate_bytes':w['scratch_estimate_bytes']} for w in work],'source':str(f)})
    matrices.append({'run':tag,'case':summary['case'],'kbig':summary['kbig'],'scope':summary['scope'],'serial':serial,'variants':variants,'source':str(folder/'SUMMARY_V001.json')})
    for row in summary.get('thread_rows',[]):
        f=folder/('THREADS6_REPEAT%d_V001.json'%row['ordinal']);d=read(f)
        threads.append({'run':tag,'case':summary['case'],'kbig':summary['kbig'],'threads_configured':d['threads'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'baseline_wall_s':serial['wall_s'],'baseline_total_cpu_s':serial['total_cpu_s'],'all_arrays_byte_equal':d['all_arrays_byte_equal'],'record_equal':d['record_equal'],'digest_equal':d['digest_equal'],'differing_arrays':[a['name'] for a in d['arrays'] if not a['byte_equal']],'child_peak_rss_bytes':d['measured']['peak_after_jet_rss_bytes'],'parent_peak_rss_bytes':d['parent_peak_after_compare_rss_bytes'],'env':d['env'],'backend':d['backend'],'source':str(f)})
for tag in ['C4R3_K032_THREADS_V001','C4R3_K128_THREADS_V001']:
    folder=ROOT/'runs'/tag;s=read(folder/'SUMMARY_V001.json');base=s['rows'][0]
    for row in s['rows']:
        f=folder/('THREADS%d_REPEAT%d_V001.json'%(row['threads'],row['ordinal']));d=read(f)
        for item in d['pins'].values():
            if pin(item['path'])!=item['sha256']:raise ValueError('PIN_CHANGED '+item['path'])
        if row['threads']==1:continue
        threads.append({'run':tag,'case':s['case'],'kbig':s['kbig'],'threads_configured':d['threads'],'status':d['status'],'wall_s':d['measured']['wall_s'],'total_cpu_s':d['measured']['total_cpu_s'],'baseline_wall_s':base['measured']['wall_s'],'baseline_total_cpu_s':base['measured']['total_cpu_s'],'all_arrays_byte_equal':d['all_arrays_byte_equal'],'record_equal':d['record_equal'],'digest_equal':d['digest_equal'],'differing_arrays':[a['name'] for a in d['arrays'] if not a['byte_equal']],'child_peak_rss_bytes':d['measured']['peak_after_jet_rss_bytes'],'parent_peak_rss_bytes':d['parent_peak_after_compare_rss_bytes'],'env':d['env'],'backend':d['backend'],'source':str(f)})
    if pin(ROOT/'threading_tail_cx3v003.py')!=s['runner_sha256']:raise ValueError('THREAD_RUNNER_PIN')
for t in threads:
    ok=t['all_arrays_byte_equal'] and t['record_equal'] and t['digest_equal'] and not t['differing_arrays']
    if (t['status']=='TESTED_PASS')!=bool(ok):raise ValueError('THREAD_STATUS_INCONSISTENCY')
prior_path=ART/'tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json';prior=read(prior_path)
pin(ART/'tail_scheme_impl_c2/kbig_timing_v003/tools/assemble_timing_v003.py')
k256=next(m for m in matrices if m['case']=='c4r3' and m['kbig']==256)
projection=[]
for name,P in [('C4T-KHI_expected_I7_P3',3),('C4T-KHI_upper_I32_P6',6)]:
    scenario=prior['scenarios'][name];B=prior['measured']['256']['route_b_rot']['solo_estimate']['cold_s'];count=2+2*P
    original=[(b+scenario['tail_solo_estimate']['total_s'])/3600 for b in scenario['baseline_tail_off_full_call_s']]
    for v in k256['variants']:
        ratio=v['wall_s']/k256['serial']['wall_s'];saving=count*B*(1-ratio)/3600
        projection.append({'status':'UNTESTED_PROJECTION','scenario':name,'workers_cap':v['workers_cap'],'rotation_equivalent_count':count,'prior_rotation_solo_cold_s':B,'measured_k256_wall_ratio':ratio,'prior_full_hours':original,'projected_hours':[h-saving for h in original],'projected_saving_hours':saving,'formula':'T_projected = T_prior - (2+2P)*B_solo_cold*(1 - T_measured_N/T_measured_serial)/3600; all other terms unchanged','assumptions':['Transfer one measured saved rotation-case wall ratio to each inherited rotation-equivalent cold-build term.','Preserve inherited iteration/pass counts and all non-rotation costs.','Ambient load, resource contention, gas/source states, source profile and future hardware may differ.','No persistent-cache saving is added. No full KHI was run.']})
for f in [ROOT/'SOURCE_ANALYSIS_V002.md',ROOT/'independent_cx3/REVIEW_CX3V001.md',ROOT/'independent_parent/COMBINED_HARNESS_REVIEW_CX3V001.md',ROOT/'independent_combined_cx3/REVIEW_CX3V001.md',ROOT/'parallel_stars_prototype_cx3v002.py',ROOT/'benchmark_tail_cx3v007.py',Path(sys.executable),Path(__file__),ART/'tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py']:
    pin(f)
for name in ['0595_2026-10-18_codex3_parallel_tail_build_feasibility.md','0601_2026-10-18_all_KHI_measured_r6_no_delay_rule_A89.md','0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md','0617_2026-10-18_all_lanes_multi_agent_concurrent_workstreams.md']:
    pin(ART.parent/'FROM_CODEX'/name)
limits=['Single samples per setting under uncontrolled ambient load; own numerical matrices execute sequentially.','Pool N and VECLIB6 are configured caps; task PIDs do not measure simultaneous workers and actual thread utilization was not instrumented.','RSS is an observed lifetime peak after allocation, not an OS hard memory limit; scratch limits are estimates.','Every state uses TEST_ONLY certificates and production_admissible false. No scientific launch, protected run or target read.','Saved C4R3 prior I1T PASS is carried from the pinned prior evidence, not independently rerun here.','One registered stellar component and rotation-stage grid were numerically exercised; other source/stage classes and spherical residual are UNTESTED.','v003 persistent-cache behavior is source-only; current store rename/cleanup conflicts with immutable-write policy.','Process timings include pool startup/teardown and full cold star preparation plus native build; thread child timings exclude fresh interpreter startup/imports/jets/IPC.','Thread verdict is read from result/summary status; process exit0 alone is not a numerical pass.','All table arrays and returned jet keys were directly byte-compared, plus record/digest; finite218-probe coverage does not prove all possible query points.']
all_proc=all(v['status']=='TESTED_PASS' for m in matrices for v in m['variants']);all_thread=all(t['status']=='TESTED_PASS' for t in threads)
max_parent=max([v['parent_peak_rss_bytes'] for m in matrices for v in m['variants']]+[t['parent_peak_rss_bytes'] for t in threads]);max_worker=max([v['worker_peak_rss_bytes'] for m in matrices for v in m['variants']]+[t['child_peak_rss_bytes'] for t in threads])
if max(max_parent,max_worker)>=8*2**30:raise ValueError('OBSERVED_MEMORY_BOUND_FAILED')
result={'date_u':now,'status':'STUDY_COMPLETE','process_byte_verdict':'TESTED_PASS' if all_proc else 'TESTED_FAIL','configured_thread_byte_verdict':'TESTED_PASS' if all_thread else 'TESTED_FAIL','matrices':matrices,'thread_comparisons':threads,'projection':projection,'limitations':limits,'observed_peak_rss_bytes':{'parent':max_parent,'worker_or_thread_child':max_worker},'r6_build_names_at_assembly':sorted(p.name for p in (ART/'tail_scheme_impl_c2/driver_r6').glob('BUILD*')),'recommendation':'Retain the sealed r5 lineage. For a later reviewed successor, integrate an optional default1 cold-star process count into the native cache-miss path, preserving256-batch arithmetic/order/certificates and BLAS1. Choose an operational cap only after resource-aware review; six is a candidate balance, twelve is a measured faster setting. Cache-hit and parallel savings overlap. Estimated development/review cost: one narrow implementation pass and one independent review/byte-replay pass plus measured replay runtime; not a promised elapsed time. No production adoption in this study.'}
exclusive(ROOT/'MEASUREMENTS_FINAL_V001.json',result)
text='# 0595 parallel-tail feasibility\n\n`date -u`: '+now+'.\n\n'
text+='Process splitting: **'+result['process_byte_verdict']+'** on every completed saved C4R3 K32/K128/K256 N2/6/12 comparison. Configured VECLIB1-versus6: **'+result['configured_thread_byte_verdict']+'** on the listed finite experiments. All table arrays, records, state digests and order1/order2 jets at218 probes were compared directly. This is nonproduction component evidence, not launch admission.\n\n'
text+='| Saved C4R3 K | Worker cap | Wall s | Wall speedup | Total CPU s | CPU speedup |\n|---:|---:|---:|---:|---:|---:|\n'
for m in matrices:
    if m['case']!='c4r3':continue
    b=m['serial'];text+=f"|{m['kbig']}|1 serial|{b['wall_s']:.3f}|1.000|{b['total_cpu_s']:.3f}|1.000|\n"
    for v in m['variants']:text+=f"|{m['kbig']}|{v['workers_cap']}|{v['wall_s']:.3f}|{v['wall_speedup']:.3f}|{v['total_cpu_s']:.3f}|{v['cpu_speedup']:.3f}|\n"
text+='\nVECLIB configuration comparisons (native build timing; startup/IPC excluded):\n\n| Case | K | 1-config wall s | 6-config wall s | Byte verdict |\n|---|---:|---:|---:|---|\n'
for t in threads:text+=f"|{t['case']}|{t['kbig']}|{t['baseline_wall_s']:.3f}|{t['wall_s']:.3f}|{t['status']}|\n"
text+=f"\nMaximum observed RSS: parent {max_parent/2**30:.3f} GiB; worker/thread child {max_worker/2**30:.3f} GiB. These are measured lifetime peaks; no hard allocation-limit claim.\n\n"
text+='The prototype splits existing independent256-frequency star batches. It retains full-grid nodes, original matrix shapes, component/doubling order, each +=, the global doubling certificate and native cache key. Native gas/source contractions and ring/corner/shell assembly remain unchanged. Full process timing includes preparation and worker creation/teardown. Radius and shell splitting remain source-analysis proposals; changing shapes or reduction grouping needs separate byte proof.\n\n'
text+='KHI projections below are **UNTESTED**. Only the inherited rotation-equivalent cold-build term is scaled by measured K256 wall ratio. Other costs and counts remain fixed; cache savings are not added. Future load and different source/stage states can invalidate the estimate.\n\n| Scenario | Worker cap | Prior full h | Projected full h | Saving h |\n|---|---:|---:|---:|---:|\n'
for x in projection:text+=f"|{x['scenario']}|{x['workers_cap']}|{x['prior_full_hours'][0]:.2f}–{x['prior_full_hours'][1]:.2f}|{x['projected_hours'][0]:.2f}–{x['projected_hours'][1]:.2f}|{x['projected_saving_hours']:.2f}|\n"
text+='\n'+result['recommendation']+'\n\n'
text+='Limitations:\n\n'+''.join('- '+x+'\n' for x in limits)
text+='\nFile pins (SHA256 read from bytes):\n\n'
for path,d in sorted(PINS.items()):text+=f"- `{path}` — `{d['sha256']}`.\n"
fp=ROOT/'REPORT_FINAL_V001.md'
with fp.open('x') as f:f.write(text)
print(str(fp),hashlib.sha256(fp.read_bytes()).hexdigest())
pin(ROOT/'MEASUREMENTS_FINAL_V001.json');pin(fp)
exclusive(ROOT/'HASHES_FINAL_V001.json',{'date_u':now,'files':PINS,'scope':'Self-excluding manifest; all hashes from bytes.'})
