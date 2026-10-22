"""SOURCE ONLY. Complete independent fullN2 fixed64-step checkpoint checker.
ROOT CLI --archive ORIGINAL_ABS --output FRESH_ABS --seed ORIGINAL --chunk 0..7.
One whole2h8GiB guard,256MiB science/64MiB runtime. No producer science imports.
Arbitrary saved candidate theorem, exact H/state/error/reads/integrals/ancestry.
Success or mathematical refusal compared fully; resource prefixes not accepted.
"""
import argparse
from fractions import Fraction as Q
import hashlib,json,math,os,resource,sys,time
from pathlib import Path
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
LANE=Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2')
CALLER=LANE/'krylov_full_n2_chunk_root_caller_v002.py'
CALLER_SHA='515c14f8fd0fb5a91f572672c305f015fd67f197de7e2b9bbe4694c293740df8'
CONTRACT=LANE/'KRYLOV_FULL_N2_CHUNK_CONTRACT_V002.txt'
CONTRACT_SHA='6232437ee00d5f8ef268483dde1a0a4ce4427a8062b45ff83f6e186b61fc290a'
ROLE='SHARED_KRYLOV_FULL_N2_CHUNK_V001'
PRODUCER_CAPS={'cpu':1,'rss_bytes':8*2**30,'seconds':43200,'scientific_reserve_bytes':4*2**30,
    'runtime_reserve_bytes':64*2**20,'output_bytes':4*2**30+64*2**20,
    'step_seconds':600,'step_scientific_bytes':64*2**20}
HELPERS = {'custody': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'), 'native': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0336_2026-10-13_native-Krylov-independent-H.py', 'c65b7c6ad4b4cd41a9ef31c45eeae3c282600b3f4207f9173e80a017f8ad9985'), 'oldpins': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0338_2026-10-13_native-Krylov-frozen-checker-pins.py', '54c9d635a82703beffdc1e571fa3a361ff8f0f009b16f4f7745720116ca623a0'), 'certificate': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0377_2026-10-13_fullN2-independent-continuation-certificate.py', 'aafc41d3df131edef496248f90a0d24f0b138af3bdf77b53dcd918533d02386b'), 'reads': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0378_2026-10-13_fullN2-independent-reads-and-quadrature.py', 'ffdf91ae5e60adf94e6fbaee6e83d99a5e0a7540de3b98a37882bc7eccd9b471'), 'pins': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0386_2026-10-13_fullN2-frozen-checker-pins.py', 'b5482620b5471e94735932a96cdd0097c6d77571ec426272c75bf10e74aba6da'), 'binding': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0387_2026-10-13_fullN2-independent-original-bindings.py', '10d872ed5bcefa5aa8890539d857bc69919cafd21ec96165ad157ac914169e18')}


def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seed',required=True);ap.add_argument('--chunk',type=int,choices=range(8),required=True)
    a=ap.parse_args();begin=time.monotonic()
    def guard():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-begin>7200 or rss>8*2**30:raise RuntimeError('whole independent2h8GiB chunk checker cap')
    modules={}
    for name,(filename,sha) in HELPERS.items():
        path=Path(filename)
        if not path.is_absolute() or path.resolve()!=path or path.is_symlink() or path.stat().st_size>65536:raise ValueError('plain independent helper')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('literal independent helper pin')
        ns={'__name__':'root_fulln2_distinct_'+name,'__file__':filename}
        exec(compile(raw,filename,'exec'),ns);modules[name]=SimpleNamespace(**ns);guard()
    C,N,OP,M,R,P,F=(modules[k] for k in ('custody','native','oldpins','certificate','reads','pins','binding'))
    need,exact,decode=C.need,C.exact,C.decode;I=C.Inputs(guard)
    for path,sha in HELPERS.values():I.read(Path(path),sha,65536)
    I.read(Path(__file__).resolve(),cap=65536);I.read(CONTRACT,CONTRACT_SHA,65536)
    seed,chunk=a.seed,a.chunk;need(seed in F.SEEDS,'fixed original seed')
    root,out=a.archive,a.output
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal whole producer root')
    need(out.is_absolute() and out.resolve()==out and not out.exists() and B in out.parents,'fresh root checker output')
    actual_files={p.name for p in root.iterdir()}
    need(15<=len(actual_files)<=333 and 'FAILURE.json' not in actual_files,'complete mathematical outcome census size')
    need(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),'all plain scientific files')
    need(sum(p.stat().st_size for p in root.iterdir())<=4*2**30,'entire original science cap')
    filemeta={}
    def saved(name):
        need(name in actual_files,'required complete artifact '+name)
        raw=I.read(root/name,cap=64*2**20)
        pin=I.pins[str(root/name)];filemeta[name]={'sha256':pin['sha256'],'bytes':pin['bytes']}
        return decode(raw)
    def reference(name,field):
        need(name in filemeta,'complete retained referenced file')
        return {'file':{'path':str(root/name),**filemeta[name]},'field':field}
    manifest=saved('INPUT_MANIFEST.json');entries=manifest['complete_consumed_input_files']
    need(type(entries)is list and len(entries)>0 and len({x['path'] for x in entries})==len(entries),'unique ordered full input manifest')
    cp=entries[0];need(Path(cp['path']).parent==B,'actual config first consumed input')
    producer_paths=[]
    def pp(pin,cap=64*2**20):
        raw=I.pin(pin,cap=cap)
        if pin['path'] not in producer_paths:producer_paths.append(pin['path'])
        return raw
    def gate(pin):
        need(Path(pin['path']).parent==B,'root-owned acceptance gate')
        doc=decode(pp(pin));need(doc['acceptor']=='/root' and str(doc['status']).startswith('PASS'),'actual root PASS')
        return doc
    cfg=decode(pp(cp,2*2**20));exact(saved('ROOT_CONFIG.json'),cfg,'whole original configuration')
    need(set(cfg)=={'schema','role','released_by','execute','output','caps','seed','chunk','source_gate',
        'original_namespace_custody','resource_reservation','predecessor_acceptances'},'closed whole config')
    need(cfg['schema']=='KRYLOV_FULL_N2_CHUNK_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
        and cfg['execute'] is True and cfg['output']==str(root),'actual root chunk release')
    exact(cfg['seed'],seed,'same selected seed');exact(cfg['chunk'],chunk,'same selected chunk');exact(cfg['caps'],PRODUCER_CAPS,'whole producer caps')
    callerraw=pp({'path':str(CALLER),'sha256':CALLER_SHA},128*2**10)
    ownpin={'path':str(CALLER),'sha256':CALLER_SHA,'bytes':len(callerraw)}
    gates={k:gate(cfg[k]) for k in ('source_gate','original_namespace_custody','resource_reservation')}
    exact(saved('GATE_SNAPSHOTS.json'),gates,'every original root gate snapshot')
    sg,cg,rg=(gates[k] for k in ('source_gate','original_namespace_custody','resource_reservation'))
    need(sg['role']==ROLE,'source gate role');exact(sg['source_pins'],P.SOURCES,'every immutable science source pin')
    matches=[x for x in sg['allowed_runners'] if x['path']==str(CALLER) and x['sha256']==CALLER_SHA and x['role']=='producer']
    need(len(matches)==1 and matches[0]['source_author']=='Codex2' and matches[0]['reviewer_id'] not in (None,'Codex2'),'distinct complete caller review')
    need(cg['role']==ROLE and cg['seed']==seed and type(cg['chunk'])is int and cg['chunk']==chunk
        and cg['complete_original_opening_checked'] is True and cg['complete_original_closing_root_obligation'] is True,'whole original and predecessor custody')
    exact(cg['input_pins'],P.INPUTS,'full original input domain');exact(cg['predecessor_acceptances'],cfg['predecessor_acceptances'],'all causal predecessor pins')
    need(rg['role']==ROLE and rg['output']==str(root) and rg['seed']==seed and type(rg['chunk'])is int and rg['chunk']==chunk
        and rg['actual_disk_and_all_other_reservations_checked'] is True and rg['root_pool_required'] is True,'actual root resource attestation')
    exact(rg['caps'],PRODUCER_CAPS,'reserved complete producer caps');exact(rg['max_concurrent_workers'],5,'wave count')
    exact(rg['max_concurrent_rss_bytes'],40*2**30,'global wave RSS')
    sources={'caller':callerraw.decode()}
    for name,pin in P.SOURCES.items():sources[name]=pp(pin,128*2**10).decode()
    exact(saved('SOURCE_SNAPSHOTS.json'),sources,'all caller/helper source bytes')
    inputs={k:decode(pp(pin)) for k,pin in P.INPUTS.items()}
    ig,qa,pa=(inputs[k] for k in ('original_input_gate','qualification','profile'))
    need(qa['acceptor']=='/root' and str(qa['status']).startswith('PASS') and qa['integer_sha256']==P.SOURCES['integer']['sha256']
        and qa['all10_controls_all20_events_complete'] is True and qa['full_C170_saved_candidate_certificate_equal'] is True
        and qa['distinct_complete_comparison'] is True and qa['complete_original_runtime_custody'] is True,'actual full C179 qualification')
    need(pa['acceptor']=='/root' and pa['claim']=='C-180' and pa['status']=='PASS_COMPLETE_UNCHANGED_NATIVE_ONE_STEP_PROFILE'
        and pa['all14_scientific_files_compared'] is True and pa['full_independent_native_certificate'] is True
        and pa['complete_original_runtime_custody'] is True,'actual complete C180 profile acceptance')
    need(ig['acceptor']=='/root' and str(ig['status']).startswith('PASS') and ig['all_original_namespaces_authenticated'] is True
        and ig['all_original_closing_pins_root_obligation'] is True,'whole original C150 native gate')
    for name in ('c150','c153','packet'):
        need(ig[name]['path']==P.INPUTS[name]['path'] and ig[name]['sha256']==P.INPUTS[name]['sha256'],'original exact native ancestry')
    c150=inputs['c150'];audit=decode(pp(c150['audit']));closures=ig['original_archive_closures']
    bypath={x['path']:x for x in closures}
    need(len(closures)==len(bypath)==39 and set(bypath)==set(audit['complete_archives']),'all39 original closure bindings')
    for rec in c150['records']:
        for name in ('producer_closure','reader_closure'):
            need(bypath[rec[name]['path']]['sha256']==rec[name]['sha256'],'same original accepted final closure')
    for pin in closures:
        doc=decode(pp(pin));need(doc['returncode']==0 and doc['cap_stop'] is None and doc['all_opening_pins_checked'] is True
            and doc['all_closing_pins_match'] is True,'whole original successful process closure')
    start=saved('START.json');pid=start['pid'];need(type(pid)is int and pid>0,'producer PID metadata')
    exact(start,{'schema':'KRYLOV_FULL_N2_CHUNK_START_V001','executor':'/root','pid':pid,'seed':seed,'chunk':chunk,
        'start_step':64*chunk,'stop_step':64*(chunk+1),'caps':PRODUCER_CAPS,'external_supervisor_required':True,'scientific_acceptance':False},'wholeSTART')
    native=inputs['packet'];need(native['phase']=='native','original native packet phase')
    selected=decode(I.pin(OP.PARENT_SELECTED));I.pin(OP.PARENT_EMITS,False)
    with Path(OP.PARENT_EMITS['path']).open('rb') as stream:
        rebuilt=N.reconstruct(native['complete_native_packet'],selected,(decode(line) for line in stream),guard)
    states,rows=rebuilt['active_states'],rebuilt['rows']
    exact(saved('NATIVE.json'),{'full_dimension':20672,'active_dimension':10432,'active_to_native':rebuilt['active_to_native'],
        'active_states':states,'rows':rows,'denominator':560,'shift':'2121/80','row_norm':'10207/560','native_packet':P.INPUTS['packet']},'complete independently reconstructed native H and basis')
    initial,binding=F.initial(pp,ig,seed,states,C,R,guard)
    exact(saved('ORIGINAL_BINDING.json'),binding,'whole exact original preparation binding')
    chain=cfg['predecessor_acceptances'];need(type(chain)is list and len(chain)==chunk,'complete ordered accepted prefix')
    state=initial;seen=[];last_error=Q(initial['L2_error'])
    for j,pin in enumerate(chain):
        g=gate(pin)
        need(g['schema']=='KRYLOV_FULL_N2_CHUNK_ACCEPTANCE_V001' and g['role']==ROLE
            and g['seed']==seed and type(g['chunk'])is int and g['chunk']==j
            and g['start_step']==64*j and g['stop_step']==64*(j+1)
            and g['complete_distinct_all_steps_comparison'] is True and g['complete_original_runtime_custody'] is True
            and g['complete_C150_ancestry_opening_and_closing'] is True and g['checkpoint_reusable'] is True,'full causal accepted predecessor')
        exact(g['source_pins'],P.SOURCES,'same predecessor helpers');exact(g['producer'],ownpin,'same immutable caller')
        exact(g['native_packet'],P.INPUTS['packet'],'same original H');exact(g['predecessor_acceptances'],seen,'whole prefix acceptance list')
        checkpoint=decode(pp(g['checkpoint']))
        need(set(checkpoint)=={'schema','seed','chunk','step','time','center','L2_error','readout','integrals','phase',
            'native_packet','source_pins','predecessor_acceptances','root_acceptance_required_before_reuse'},'entire accepted checkpoint schema')
        need(checkpoint['schema']=='KRYLOV_FULL_N2_CHECKPOINT_V001' and checkpoint['seed']==seed and type(checkpoint['chunk'])is int and checkpoint['chunk']==j
            and checkpoint['step']==64*(j+1) and Q(checkpoint['time'])==Q(64*(j+1),512)
            and checkpoint['phase']==F.PHASE and checkpoint['root_acceptance_required_before_reuse'] is True,'exact accepted checkpoint identity')
        exact(checkpoint['native_packet'],P.INPUTS['packet'],'checkpoint native ancestry');exact(checkpoint['source_pins'],P.SOURCES,'checkpoint source ancestry')
        exact(checkpoint['predecessor_acceptances'],seen,'checkpoint whole prior acceptance list')
        error=Q(checkpoint['L2_error']);need(last_error<=error<Q(1,1<<51),'retained monotone certified error')
        checkread=R.readout(states,checkpoint['center'],error,guard)
        exact(checkpoint['readout'],F.wire(checkread),'all accepted incoming read fields')
        need(set(checkpoint['integrals'])==set(F.NAMES),'all ten accepted integral intervals')
        T=Q(checkpoint['step'],512)
        for name in F.NAMES:
            pair=checkpoint['integrals'][name];need(type(pair)is list and len(pair)==2,'whole accumulator pair')
            lo,hi=map(Q,pair);cap=1 if name in R.WORDS else R.CAPS[name]
            need(0<=lo<=hi<=cap*T,'proven integral range')
        state={k:checkpoint[k] for k in ('center','L2_error','readout','integrals','step','time')};last_error=error;seen.append(pin)
    exact(saved('INPUT_STATE.json'),state,'every incoming center/error/read/integral/time field')
    center=state['center'];error=Q(state['L2_error']);read=R.readout(states,center,error,guard)
    integrals={k:list(map(Q,state['integrals'][k])) for k in F.NAMES}
    centerref=reference('INPUT_STATE.json',['center'])
    status='RAW_COMPLETE_CHUNK';refusal=None;completed=0;attempted=0;step_summaries=[];expected_phases=[]
    for step in range(64*chunk+1,64*(chunk+1)+1):
        prefix='STEP_%04d_'%step;attempted+=1
        common={'rows':reference('NATIVE.json',['rows']),'center':centerref,'denominator':560}
        exact(saved(prefix+'CANDIDATE_PRE.json'),{'function':'candidate_lanczos','arguments':{**common,'max_columns':16},
            'argument_encoding':'PINNED_FULL_FILE_FIELD_REFERENCES','phase':'BEFORE_ACTUAL_CALL','step':step,'time_before':str(Q(step-1,512))},'whole candidate PRE '+str(step))
        cr=saved(prefix+'CANDIDATE_RETURN.json');need(type(cr)is dict and set(cr)=={'exception','value'} and cr['exception'] is None,'whole successful arbitrary candidate')
        proposal=cr['value']
        exact(saved(prefix+'CERTIFICATE_PRE.json'),{'function':'certificate','arguments':{**common,'input_L2_error':str(error),
            'proposal':reference(prefix+'CANDIDATE_RETURN.json',['value']),'tau':'1/512','degree':32},
            'argument_encoding':'PINNED_FULL_FILE_FIELD_REFERENCES','phase':'BEFORE_ACTUAL_CALL','step':step},'entire actual certificate operands '+str(step))
        cert=M.reconstruct(rows,center,proposal,guard,str(error))
        exact(saved(prefix+'CERTIFICATE_RETURN.json'),{'exception':None,'value':cert},'every complete independent exact certificate field '+str(step))
        expected_phases.extend([(step,'candidate'),(step,'certificate')])
        passed=cert['step_target_2_minus_64_met'] and cert['original_cumulative_cap_2_minus_51_met']
        step_summaries.append({'step':step,'incoming_L2_error':str(error),'step_added_L2_error':cert['step_added_L2_error'],
            'outgoing_L2_error':cert['accumulated_L2_error'],'all_certificate_fields_compared':True,'both_precision_predicates_met':passed})
        if not passed:
            status='RAW_CERTIFICATE_BUDGET_REFUSAL';refusal={'step':step,'certificate':reference(prefix+'CERTIFICATE_RETURN.json',['value'])}
            need(sum(v['bytes'] for k,v in filemeta.items() if k.startswith(prefix))<=64*2**20,'entire failed step science cap')
            break
        center=cert['endpoint_I80'];error=Q(cert['accumulated_L2_error']);newread=R.readout(states,center,error,guard)
        summed=R.add_trapezoid([integrals[k] for k in F.NAMES],read,newread)
        integrals=dict(zip(F.NAMES,summed));read=newread
        exact(saved(prefix+'READOUT.json'),F.wire({'step':step,'time':Q(step,512),'value':read,'integrals':integrals}),
            'all ten reads/statistics and accumulated integrals '+str(step))
        need(sum(v['bytes'] for k,v in filemeta.items() if k.startswith(prefix))<=64*2**20,'entire completed step science cap')
        completed+=1;centerref=reference(prefix+'CERTIFICATE_RETURN.json',['value','endpoint_I80'])
        print(json.dumps({'independent_progress':'COMPLETE_STEP','seed':seed,'chunk':chunk,'step':step}),flush=True);guard()
    stop=64*chunk+completed;horizon=None
    if refusal is None and stop in (64,128,256,512):
        horizon=F.horizon(pp,ig,seed,stop,center,error,read,integrals,states,C,R,guard)
        exact(saved('WINDOW_COMPARISON.json'),horizon,'all original/new endpoint and continuous-window fields')
        comp=horizon['comparison']
        if not(comp['full_endpoint_bound_met'] and comp['all_average_intersections'] and comp['all_endpoint_read_intersections']
            and horizon['new_average']['word_halfwidth_target_met']):status='RAW_C150_COMPARISON_REFUSAL'
    if status=='RAW_COMPLETE_CHUNK':
        expected_checkpoint=F.wire({'schema':'KRYLOV_FULL_N2_CHECKPOINT_V001','seed':seed,'chunk':chunk,'step':stop,'time':Q(stop,512),
            'center':center,'L2_error':error,'readout':read,'integrals':integrals,'phase':F.PHASE,'native_packet':P.INPUTS['packet'],
            'source_pins':P.SOURCES,'predecessor_acceptances':chain,'root_acceptance_required_before_reuse':True})
        exact(saved('CHECKPOINT.json'),expected_checkpoint,'every outgoing checkpoint field')
    result=F.wire({'schema':'KRYLOV_FULL_N2_CHUNK_RESULTS_V001','seed':seed,'chunk':chunk,'status':status,'attempted_steps':attempted,
        'completed_steps':completed,'start_step':64*chunk,'last_successful_step':stop,'final_L2_error':error,'refusal':refusal,
        'checkpoint_written':status=='RAW_COMPLETE_CHUNK','distinct_all_steps_comparison_required':True,
        'full_N2_validation_completed':False,'physical_release':False})
    exact(saved('RESULTS.json'),result,'entire success or mathematical refusal result')
    profile=saved('PROFILE.json')
    need(set(profile)=={'actual_call_phases','whole_elapsed_before_profile','profile_and_finish_serialization_excluded','dense_later_throughput_guarantee'},'complete profile fields')
    exact(profile['profile_and_finish_serialization_excluded'],True,'profile measurement phase')
    exact(profile['dense_later_throughput_guarantee'],False,'no throughput extrapolation')
    elapsed=profile['whole_elapsed_before_profile'];need(type(elapsed)is float and math.isfinite(elapsed) and 0<=elapsed<=43200,'actual recorded whole elapsed bound')
    phases=profile['actual_call_phases'];need(type(phases)is list and len(phases)==len(expected_phases),'every actual call phase')
    step_times={}
    for row,(step,name) in zip(phases,expected_phases):
        need(set(row)=={'step','call','wall_seconds','cpu_seconds'},'closed actual phase row')
        exact(row['step'],step,'phase step');exact(row['call'],name,'phase function')
        for label in ('wall_seconds','cpu_seconds'):
            value=row[label];need(type(value)is float and math.isfinite(value) and 0<=value<=600,'finite bounded actual call duration')
        step_times[step]=step_times.get(step,0)+row['wall_seconds']
    need(all(v<=600 for v in step_times.values()) and sum(step_times.values())<=elapsed,'call times within steps and whole process')
    exact(manifest,{'complete_consumed_input_files':[I.pins[p] for p in producer_paths],'original_static_inputs':P.INPUTS,
        'whole_original_namespace_closing_root_obligation':True,'selected_inputs_are_original_process_closure':False},'all ordered original consumed input pins')
    prefinish=dict(filemeta)
    exact(saved('FINISH.json'),{'schema':'KRYLOV_FULL_N2_CHUNK_FINISH_V001','pid':pid,'status':status,
        'files_before_finish':prefinish,'all_consumed_closing_bytes_match':True,
        'scientific_acceptance':False,'checkpoint_reusable_without_root_acceptance':False},'whole exact FINISH and complete prefinish hashes')
    expected={'START.json','ROOT_CONFIG.json','SOURCE_SNAPSHOTS.json','GATE_SNAPSHOTS.json','NATIVE.json','ORIGINAL_BINDING.json','INPUT_STATE.json',
        'RESULTS.json','PROFILE.json','INPUT_MANIFEST.json','FINISH.json'}
    for step in range(64*chunk+1,64*chunk+completed+1):
        expected.update('STEP_%04d_%s.json'%(step,suffix) for suffix in ('CANDIDATE_PRE','CANDIDATE_RETURN','CERTIFICATE_PRE','CERTIFICATE_RETURN','READOUT'))
    if refusal is not None:
        expected.update('STEP_%04d_%s.json'%(refusal['step'],suffix) for suffix in ('CANDIDATE_PRE','CANDIDATE_RETURN','CERTIFICATE_PRE','CERTIFICATE_RETURN'))
    if horizon is not None:expected.add('WINDOW_COMPARISON.json')
    if status=='RAW_COMPLETE_CHUNK':expected.add('CHECKPOINT.json')
    need(actual_files==set(filemeta)==expected,'every success/refusal file exactly once, no extras or missing records')
    need({p.name for p in root.iterdir()}==expected,'closing entire original output census')
    I.close();guard()
    report={'schema':'KRYLOV_FULL_N2_COMPLETE_INDEPENDENT_CHUNK_COMPARISON_V001',
        'status':'PASS_COMPLETE_SAVED_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY','archive':str(root),'seed':seed,'chunk':chunk,
        'producer_author':'Codex2','checker_author':'Codex3','self_review':False,'actual_scientific_status':status,
        'all_scientific_files':filemeta,'all_actual_steps':step_summaries,'complete_result':result,
        'whole_profile':profile,'whole_horizon_comparison':horizon,'all20672_parent_columns_independently_rebuilt':True,
        'all10432_active_H_rows_and_initial_coordinates_exact':True,'all_actual_PRE_RETURN_fields_compared':True,
        'every_certificate_power_defect_endpoint_and_error_field_compared':True,'all_ten_reads_and_prefix_integrals_reconstructed':True,
        'entire_accepted_predecessor_chain_authenticated':True,'candidate_decimal_regenerated':False,
        'old_C150_midpoint_history_recomputed_here':False,'old_C150_values_bound_to_accepted_original_whole_journals_and_closures':True,
        'root_complete_original_process_ancestry_and_runtime_verified_here':False,
        'timing_values_independently_recomputed':False,'all_opened_input_closing_pins_match':True,'complete_checker_input_pins':I.pins,
        'checkpoint_reusable_without_root_acceptance':False,'full_N2_validation_completed':False,'N4_released':False,'physical_release':False}
    raw=(json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=256*2**20,'whole checker science reserve');out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    guard();print(json.dumps({'status':report['status'],'scientific_status':status,'seed':seed,'chunk':chunk,
        'completed_steps':completed,'report_sha256':hashlib.sha256(raw).hexdigest()}),flush=True)


if __name__=='__main__':main()
