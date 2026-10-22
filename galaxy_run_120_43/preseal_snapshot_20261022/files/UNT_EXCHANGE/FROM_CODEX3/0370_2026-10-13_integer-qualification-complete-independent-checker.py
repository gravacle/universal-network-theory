"""SOURCE ONLY. Root-only complete integer qualification saved checker.
CLI --case controls|replay|profile --archive ORIGINAL_ABS --output FRESH_ABS.
No producer science imports, no Decimal regeneration on native cases.
Same single whole-job guard covers complete input/H/certificate and closing.
All original process/runtime and historical namespace custody remain root-owned.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
LANE=Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2')
CALLER=LANE/'krylov_integer_qualification_root_caller_v001.py'
CALLER_SHA='8a761bebbc7080798527f4e1cf1673478da9d08cbf809b488ff67856a232711b'
CONTRACT=LANE/'KRYLOV_INTEGER_QUALIFICATION_CONTRACT_V001.txt'
CONTRACT_SHA='14f47c3e0931b9da9a909a62b82ce268f61cd79498fb1bdb4131afd47e21fa37'
ROLE='SHARED_KRYLOV_INTEGER_QUALIFICATION_V001'
HELPERS = {'custody': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'), 'native': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0336_2026-10-13_native-Krylov-independent-H.py', 'c65b7c6ad4b4cd41a9ef31c45eeae3c282600b3f4207f9173e80a017f8ad9985'), 'certificate': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0337_2026-10-13_native-Krylov-independent-integer-certificate.py', 'c7096f7bcea6a75e726fa82ea2e78859228bc7f0346393aeddc05b2f242f623f'), 'pins': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0338_2026-10-13_native-Krylov-frozen-checker-pins.py', '54c9d635a82703beffdc1e571fa3a361ff8f0f009b16f4f7745720116ca623a0'), 'analytic': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0316_2026-10-13_shared-Krylov-complete-independent-checker.py', '44e18b999dce223362b4d14189c05a2586ee6dcf91cdebd70d22d5635f723cc6'), 'support': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0368_2026-10-13_integer-qualification-independent-support.py', '236fb812de16b07df19c3a8f0a0bdedbac2413c0a146ffb30e3f7d28e74a4822'), 'native_audit': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0369_2026-10-13_integer-native-complete-archive-audit.py', '337d08333a03f5dc005d61f2e432404a720280d4f75619171d0485924536942a')}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=['controls','replay','profile'],required=True)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();case=args.case;started=time.monotonic()
    seconds=60 if case=='controls' else 600
    rss_limit=256*2**20 if case=='controls' else 8*2**30
    science_cap=8*2**20 if case=='controls' else 120*2**20
    caps={'cpu':1,'rss_bytes':rss_limit,'seconds':seconds,
        'output_bytes':16*2**20 if case=='controls' else 128*2**20,'scientific_reserve_bytes':science_cap}
    def guard():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-started>seconds or rss>rss_limit:raise ValueError('complete owned integer checker role cap')
    modules={}
    for label,(filename,sha) in HELPERS.items():
        path=Path(filename)
        if not path.is_absolute() or path.resolve()!=path or path.is_symlink() or path.stat().st_size>65536:
            raise ValueError('plain bounded independent source')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('independent helper SHA')
        ns={'__name__':'root_integer_independent_'+label,'__file__':str(path)}
        exec(compile(raw,str(path),'exec'),ns);modules[label]=SimpleNamespace(**ns)
        guard()
    C,U,A,N=(modules[k] for k in ('custody','support','analytic','native_audit'))
    need,exact,decode=C.need,C.exact,C.decode;I=C.Inputs(guard)
    for path,sha in HELPERS.values():I.read(Path(path),sha,65536)
    I.read(Path(__file__).resolve(),cap=65536);I.read(CONTRACT,CONTRACT_SHA,65536)
    root,out=args.archive,args.output
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal original root archive')
    need(out.is_absolute() and out.resolve()==out and not out.exists() and B in out.parents,'fresh root checker output')
    result={};native=None
    if case=='profile':
        native=N.audit(root,I,guard,modules,profile=True)
        filemeta=native['all_scientific_files'];result=native['result'];profile=native['profile']
        FILES=set(filemeta)
    else:
        FILES={'START.json','CONFIG.json','SOURCES.json','GATES.json','PROFILE.json','INPUT_MANIFEST.json','FINISH.json'}
        if case=='controls':
            FILES|={'RESULTS.json'}|{'CALL_%02d_%s.json'%(i,e) for i in range(10) for e in ('PRE','RETURN')}
        else:FILES|={'INPUTS.json','ACTUAL_PRE.json','ACTUAL_RETURN.json'}
        need({p.name for p in root.iterdir()}==FILES,'complete28 or10 scientific files')
        data,filemeta={},{}
        for name in sorted(FILES):
            data[name]=decode(I.read(root/name,cap=science_cap))
            pin=I.pins[str(root/name)];filemeta[name]={'bytes':pin['bytes'],'sha256':pin['sha256']}
        need(sum(v['bytes'] for v in filemeta.values())<=science_cap,'complete scientific reserve')
        producer_paths=[]
        def pp(pin,cap=32*2**20):
            raw=I.pin(pin,cap=cap)
            if pin['path'] not in producer_paths:producer_paths.append(pin['path'])
            return raw
        start=data['START.json'];pid=start['pid'];configpin=start['config']
        need(type(pid)is int and pid>0,'recorded PID syntax only')
        need(Path(configpin['path']).parent==B,'original root-owned config')
        cfg=decode(pp(configpin))
        need(set(cfg)=={'schema','role','case','released_by','execute','output','caps','source_gate','original_namespace_custody'},'closed whole config')
        need(cfg['schema']=='KRYLOV_INTEGER_QUALIFICATION_RELEASE_V001' and cfg['role']==ROLE and cfg['case']==case
            and cfg['released_by']=='/root' and cfg['execute'] is True and cfg['output']==str(root),'exact root release')
        exact(cfg['caps'],caps,'fixed whole caps');exact(data['CONFIG.json'],cfg,'complete config snapshot')
        exact(start,{'schema':'KRYLOV_INTEGER_QUALIFICATION_START_V001','executor':'/root','pid':pid,
            'case':case,'config':configpin,'caps':caps,'external_supervisor_required':True,'scientific_acceptance':False},'complete START')
        caller=pp({'path':str(CALLER),'sha256':CALLER_SHA},65536)
        gates={}
        for name in ('source_gate','original_namespace_custody'):
            need(Path(cfg[name]['path']).parent==B,'root gate namespace')
            gates[name]=decode(pp(cfg[name]))
        exact(data['GATES.json'],gates,'whole gate snapshots')
        sg,ig=gates['source_gate'],gates['original_namespace_custody']
        need(sg['acceptor']=='/root' and str(sg['status']).startswith('PASS') and sg['role']==ROLE,'actual source acceptance')
        exact(sg['source_pins'],U.SOURCES,'literal full source set')
        hits=[r for r in sg['allowed_runners'] if r['path']==str(CALLER) and r['sha256']==CALLER_SHA and r['role']=='producer']
        need(len(hits)==1 and hits[0]['source_author']=='Codex2' and hits[0]['reviewer_id'] not in (None,'Codex2'),'distinct complete source review')
        need(ig['acceptor']=='/root' and str(ig['status']).startswith('PASS') and ig['role']==ROLE and ig['case']==case
            and ig['complete_original_opening_checked'] is True and ig['complete_original_closing_root_obligation'] is True,'complete original root custody gate')
        exact(ig['input_pins'],U.QUAL_INPUTS[case],'entire frozen input set')
        docs={k:decode(pp(pin)) for k,pin in U.QUAL_INPUTS[case].items()}
        snapshots={'caller':caller.decode()}
        for name,pin in U.SOURCES.items():snapshots[name]=pp(pin,65536).decode()
        exact(data['SOURCES.json'],snapshots,'whole source bytes')
        if case=='controls':
            old=docs['c161']
            need(old['acceptor']=='/root' and old['all8_calls_all16_events_exactly_compared'] is True
                and old['complete_original_runtime_custody'] is True,'actual original C161 acceptance')
            result=U.controls(data,A,exact,need,guard)
        else:
            accepted=docs['c170']
            need(accepted['acceptor']=='/root' and accepted['claim']=='C-170'
                and accepted['all13_scientific_files_compared'] is True and accepted['complete_original_runtime_custody'] is True,'whole C170 accepted ancestor')
            historical=Path(U.QUAL_INPUTS['replay']['pre']['path']).parent
            need(Path(U.QUAL_INPUTS['replay']['return']['path']).parent==historical,'one original native archive')
            # Full13-file original scientific audit, full20672 H and full initial
            # point, then direct H*w-next_w for actual saved proposal, no D*c.
            native=N.audit(historical,I,guard,modules,profile=False)
            exact(docs['pre'],native['certificate_pre'],'entire authenticated original PRE')
            exact(docs['return'],{'exception':None,'value':native['certificate']},'every original certificate field independently rebuilt')
            exact(data['INPUTS.json'],{'fixed_inputs':U.QUAL_INPUTS[case],
                'whole_original_certificate_return':docs['return']},'whole replay input record')
            exact(data['ACTUAL_PRE.json'],docs['pre'],'every replay argument and candidate entry')
            exact(data['ACTUAL_RETURN.json'],docs['return'],'whole new actual certificate equals full original and independent reconstruction')
            result={'full_original_C170_archive_reconstructed':True,'whole_certificate_type_exact_equal':True,
                'all_candidate_entries_used':True,'candidate_regenerated':False,
                'step_target_2_minus_64_met':native['certificate']['step_target_2_minus_64_met'],
                'original_cumulative_cap_2_minus_51_met':native['certificate']['original_cumulative_cap_2_minus_51_met']}
        profile=U.profile(data['PROFILE.json'],pid,case,exact,need,seconds)
        exact(data['INPUT_MANIFEST.json'],{'complete_consumed_input_files':[I.pins[p] for p in producer_paths],
            'complete_original_namespace_closing_root_obligation':True,'selected_inputs_are_original_process_custody':False},'entire ordered producer consumed-input manifest')
        exact(data['FINISH.json'],{'schema':'KRYLOV_INTEGER_QUALIFICATION_FINISH_V001','pid':pid,'case':case,
            'files_before_finish':{k:v for k,v in filemeta.items() if k!='FINISH.json'},
            'all_consumed_input_closing_bytes_match':True,
            'status':'RAW_QUALIFICATION_REQUIRES_DISTINCT_COMPLETE_COMPARISON_AND_ROOT_CUSTODY',
            'physical_release':False,'full_N2_released':False},'whole FINISH')
    need({p.name for p in root.iterdir()}==FILES,'closing full original census')
    I.close();guard()
    report={'schema':'KRYLOV_INTEGER_COMPLETE_INDEPENDENT_COMPARISON_V001',
        'status':'PASS_COMPLETE_EXACT_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY','case':case,
        'producer_author':'Codex2','checker_author':'Codex3','self_review':False,'archive':str(root),
        'all_scientific_files':filemeta,'complete_scientific_result':result,'whole_original_profile':profile,
        'all10_controls_all20_events_exactly_compared':case=='controls',
        'full_C170_saved_candidate_certificate_equal':case=='replay',
        'all_native_H_initial_state_and_certificate_fields_reconstructed':case in ('replay','profile'),
        'candidate_decimal_regenerated_by_checker':False,
        'independent_arithmetic':'analytic tiny powers/scalar Taylor sums; full native H*w-next_w integer defect; minimal outward roots by bisection',
        'complete_checker_input_pins':I.pins,'all_opened_input_closing_pins_match':True,
        'original_runtime_and_whole_historical_namespaces_verified_here':False,
        'phase_timing_values_independently_recomputed':False,'timing_authentication_requires_root_runtime':True,
        'speedup_claim':False,'full_N2_released':False,'N4_released':False,'physical_release':False}
    if native is not None:
        report['native_ancestor_or_profile_archive_files']=native['all_scientific_files']
    raw=(json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=science_cap,'whole checker report reserve')
    out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    guard()
    print(json.dumps({'status':report['status'],'case':case,'report_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}),flush=True)


if __name__=='__main__':main()
