"""SOURCE ONLY. Complete independent forty-file C181 bounds comparison.
Root CLI --archive ORIGINAL_ABS --output FRESH_ROOT_ABS;512MiB120s64MiB.
Rebuilds domain and every analytic layer bound, not any DP coefficient frontier.
"""
import argparse,hashlib,json,os,resource,sys,time
from pathlib import Path
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ROLE='P60_C181_SUPPORTED_PROJECTION_V001'
CAPS={'cpu':1,'rss_bytes':512*2**20,'seconds':120,'output_bytes':64*2**20,'scientific_reserve_bytes':56*2**20}
CALLER = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_c181_projection_root_caller_v001.py')
CALLER_SHA = 'dd109569efdc610664f70c12680091a96156e0821a5ed2b2e4ee3ed50442809f'
HELPER = {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_c181_projection_bounds_v001.py', 'sha256': '9f3c0bdd9a01ecc4c775caab5a4c4ed0fa04cedcc9946b1f0303d83ae5c95803', 'bytes': 5150}
RECEIPT = {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/P60_C181_DOCUMENTARY_PROGRESS_RECEIPT_V001.json', 'sha256': 'b1bee0a07cb16723ca9fa2926b86b31c495e670a310181f060bc12e793dcc52d', 'bytes': 158124}
HELPERS = {'custody': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'), 'graph': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0373_2026-10-13_G1-L4-L5-independent-graph-and-frontier.py', 'c02b0f35fd6b039d38d817f412864d2bf31660a4fe1410e4f947e6bfcc767ba7'), 'domain': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0374_2026-10-13_G1-L4-L5-complete-independent-checker.py', 'b25b4e779a5fa2237aa77be9d2a0e4344bf5d7b02f2e600d1dc2713387a50229'), 'bounds': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0397_2026-10-13_C181-independent-all-layer-bounds.py', '75a2e389e6cc63b6a3fdf2893fa630557ce6fca739f4797d29d7a791a219bc0c')}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();start=time.monotonic()
    def guard():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-start>120 or rss>512*2**20:raise RuntimeError('whole120s512MiB projection checker cap')
    modules={}
    for name,(filename,sha) in HELPERS.items():
        path=Path(filename)
        if not path.is_absolute() or path.resolve()!=path or path.is_symlink() or path.stat().st_size>65536:raise ValueError('plain independent helper')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('independent helper SHA')
        ns={'__name__':'root_projection_independent_'+name,'__file__':filename}
        exec(compile(raw,filename,'exec'),ns);modules[name]=SimpleNamespace(**ns);guard()
    C,G,D,M=(modules[k] for k in ('custody','graph','domain','bounds'))
    need,exact,decode=C.need,C.exact,C.decode;I=C.Inputs(guard)
    for path,sha in HELPERS.values():I.read(Path(path),sha,65536)
    I.read(Path(__file__).resolve(),cap=65536)
    root,out=args.archive,args.output
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal original root projection archive')
    need(out.is_absolute() and out.resolve()==out and not out.exists() and B in out.parents,'fresh root checker output')
    FILES={'START.json','ROOT_CONFIG.json','SOURCE_SNAPSHOTS.json','GATE_SNAPSHOTS.json','EVIDENCE_RECEIPT.json',
        'RESULTS.json','INPUT_MANIFEST.json','FINISH.json'}|{'CASE_%02d_%s.json'%(i,e) for i in range(16) for e in ('PRE','RETURN')}
    need({p.name for p in root.iterdir()}==FILES,'complete40file success census')
    filemeta={}
    def saved(name):
        raw=I.read(root/name,cap=56*2**20);pin=I.pins[str(root/name)]
        filemeta[name]={'sha256':pin['sha256'],'bytes':pin['bytes']};return decode(raw)
    manifest=saved('INPUT_MANIFEST.json');records=manifest['complete_consumed_input_files']
    need(type(records)is list and records and len({x['path'] for x in records})==len(records),'all unique consumed original inputs')
    cp=records[0];need(Path(cp['path']).parent==B,'root config first original input')
    producer_paths=[]
    def pp(pin):
        raw=I.pin(pin,cap=4*2**20)
        if pin['path'] not in producer_paths:producer_paths.append(pin['path'])
        return raw
    cfg=decode(pp(cp));exact(saved('ROOT_CONFIG.json'),cfg,'entire configuration')
    need(set(cfg)=={'schema','role','released_by','execute','output','caps','source_gate','original_custody_gate'},'closed projection release')
    need(cfg['schema']=='P60_C181_PROJECTION_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
        and cfg['execute'] is True and cfg['output']==str(root),'actual bounded root release')
    exact(cfg['caps'],CAPS,'same frozen role caps');gates={}
    for name in ('source_gate','original_custody_gate'):
        need(Path(cfg[name]['path']).parent==B,'root gate ownership');gates[name]=decode(pp(cfg[name]))
        g=gates[name];need(g['acceptor']=='/root' and str(g['status']).startswith('PASS') and g['role']==ROLE,'actual root PASS gate')
    exact(saved('GATE_SNAPSHOTS.json'),gates,'whole original gates')
    callerraw=pp({'path':str(CALLER),'sha256':CALLER_SHA})
    sg,cg=gates['source_gate'],gates['original_custody_gate']
    exact(sg['helper'],HELPER,'exact producer bound helper');exact(sg['documentary_receipt'],RECEIPT,'literal documentary input')
    hits=[x for x in sg['allowed_runners'] if x['path']==str(CALLER) and x['sha256']==CALLER_SHA and x['role']=='producer']
    need(len(hits)==1 and hits[0]['source_author']=='Codex2' and hits[0]['reviewer_id'] not in (None,'Codex2'),'distinct complete source review')
    exact(cg['documentary_receipt'],RECEIPT,'whole root original receipt binding')
    need(cg['complete_C181_opening_checked'] is True and cg['complete_C181_closing_root_obligation'] is True,'actual whole32process custody gate')
    receipt=decode(pp(RECEIPT));accept=decode(pp(receipt['acceptance']));pp(receipt['custody']);pp(receipt['producer_spec'])
    need(receipt['schema']=='P60_C181_DOCUMENTARY_PROGRESS_RECEIPT_V001' and receipt['author']=='Codex2'
        and receipt['scientific_computation_performed'] is False,'documentary evidence scope')
    exact(saved('EVIDENCE_RECEIPT.json'),receipt,'all documentary receipt fields')
    need(accept['acceptor']=='/root' and accept['claim']=='C-181' and accept['status']=='PASS_COMPLETE_SIXTEEN_COUNT_CAP_REFUSALS','actual full C181 acceptance')
    accepted={(r['case']['L'],r['case']['sector'],r['case']['axes']):r['complete_actual_return'] for r in accept['cases']}
    cartesian={(L,s,a) for L in (4,5) for s in ('old','Born') for a in ('012','021','102','210')}
    need(len(accept['cases'])==len(accepted)==len(receipt['records'])==16 and set(accepted)==cartesian,'complete original sixteen cases')
    helperraw=pp(HELPER)
    exact(saved('SOURCE_SNAPSHOTS.json'),{'caller':callerraw.decode(),'helper':helperraw.decode()},'whole producer source bytes')
    st=saved('START.json');pid=st['pid'];need(type(pid)is int and pid>0,'actual producer PID syntax')
    exact(st,{'role':ROLE,'executor':'/root','pid':pid,'caps':CAPS,'count_DP_executed':False,'scientific_acceptance':False},'wholeSTART')
    summaries=[];seen=set();coverage=[]
    for index,rec in enumerate(receipt['records']):
        need(set(rec['source_evidence'])=={'DOMAIN_RETURN.json','ACTUAL_RETURN.json','PROGRESS.jsonl','FINISH.json','CONFIG.json'},'complete selected original science record set')
        need(set(rec['runtime_evidence'])=={'SUPERVISOR_RESULT.json','CHILD_FINISH.json','JOB.json'},'complete selected original runtime records')
        source={k:pp(v) for k,v in rec['source_evidence'].items()}
        runtime={k:decode(pp(v)) for k,v in rec['runtime_evidence'].items()}
        original_root=Path(rec['archive'])
        need(all(Path(v['path'])==original_root/name for name,v in rec['source_evidence'].items()),'same exact original archive for all selected files')
        dom=decode(source['DOMAIN_RETURN.json']);ret=decode(source['ACTUAL_RETURN.json'])
        need(set(dom)==set(ret)=={'exception','value'} and dom['exception'] is None and ret['exception'] is None,'whole accepted original returns')
        d,r=dom['value'],ret['value'];key=(d['L'],d['sector'],''.join(map(str,d['axis_permutation'])))
        need(key in cartesian and key not in seen,'unique frozen original case');seen.add(key)
        exact(r,accepted[key],'literal entire C181 accepted refusal')
        reconstructed=D.domain(G.graph(key[0],key[1],list(map(int,key[2]))))
        exact(d,reconstructed,'all original graph action polynomial factors reconstructed without DP')
        progressraw=source['PROGRESS.jsonl'];need(progressraw.endswith(b'\n') and all(progressraw.splitlines()),'complete original progress JSONL')
        progress=[decode(row) for row in progressraw.splitlines()]
        exact(progress,rec['literal_completed_progress'],'every copied accepted progress row');exact(ret,rec['literal_actual_return'],'entire copied refusal')
        rt=runtime['SUPERVISOR_RESULT.json'];exact(rt,rec['literal_runtime'],'all original runtime copied fields')
        need(rt['complete_success'] is True and rt['exit_code']==0 and rt['memory_breach'] is False and rt['output_breach'] is False,'actual successful original owned process')
        oldcfg=decode(source['CONFIG.json']);exact(oldcfg['case'],{'L':key[0],'sector':key[1],'axes':key[2]},'same original actual config case')
        finish=decode(source['FINISH.json'])
        for name in ('DOMAIN_RETURN.json','ACTUAL_RETURN.json','PROGRESS.jsonl','CONFIG.json'):
            pin=rec['source_evidence'][name];exact(finish['files_before_finish'][name],{'sha256':pin['sha256'],'bytes':pin['bytes']},'original complete prefinish member')
        exact(saved('CASE_%02d_PRE.json'%index),{'phase':'BEFORE_ACTUAL_CALL','function':'project','case':list(key),
            'complete_argument_files':rec['source_evidence'],'runtime_argument_file':rec['runtime_evidence']['SUPERVISOR_RESULT.json'],
            'domain_selector':['value'],'refusal_selector':['value'],'progress_encoding':'allJSONLrows','complete_fields_required':True},'whole actual projection PRE')
        value=M.reconstruct(d,progress,r,rt,C,guard)
        exact(saved('CASE_%02d_RETURN.json'%index),{'exception':None,'value':value},'all independently reconstructed layer bounds and scope fields')
        summaries.append({'case':list(key),'peak_lower':value['complete_algorithm_peak_live_keys_lower'],
            'peak_upper':value['complete_algorithm_peak_live_keys_upper'],'feasibility':value['resource_feasibility']})
        coverage.append({'case':list(key),'layers':len(value['all_layer_bounds']),'all_layer_fields_compared':True,'full_domain_independently_rebuilt':True})
        guard()
    need(seen==cartesian,'all16 complete cases')
    result={'all16_cases':summaries,'count_DP_executed':False,'resource_bounds_are_not_RSS_or_wall_time_bounds':True,
        'higher_cap_release':False,'distinct_complete_comparison_required':True}
    exact(saved('RESULTS.json'),result,'all sixteen summary entries')
    exact(manifest,{'complete_consumed_input_files':[I.pins[p] for p in producer_paths],'whole_C181_original_closing_root_obligation':True},'entire ordered input manifest')
    prefinish=dict(filemeta)
    exact(saved('FINISH.json'),{'files_before_finish':prefinish,'pid':pid,'status':'RAW_COMPLETE_ANALYTIC_BOUNDS',
        'all_consumed_input_closing_bytes_match':True,'scientific_acceptance':False},'all39 complete prefinish hashes')
    need(set(filemeta)==FILES and sum(v['bytes'] for v in filemeta.values())<=56*2**20,'whole forty-file output reserve')
    need({p.name for p in root.iterdir()}==FILES,'closing whole archive census');I.close();guard()
    report={'schema':'P60_C181_COMPLETE_INDEPENDENT_BOUNDS_COMPARISON_V001','status':'PASS_COMPLETE_SAVED_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY',
        'archive':str(root),'producer_author':'Codex2','checker_author':'Codex3','self_review':False,
        'all40_scientific_files':filemeta,'all16_complete_layer_coverages':coverage,'complete_result':result,
        'independent_degree_superset':'zero;one iff unit incidence;two iff double incidence or two unit incidences',
        'conditional_payload_model_checked_against_current_CPython_digit_and_tuple_ABI':True,
        'DP_frontier_regenerated':False,'whole_original32process_namespaces_and_actual_runtime_verified_here':False,
        'all_opened_input_closing_pins_match':True,'complete_checker_input_pins':I.pins,
        'resource_feasibility':'UNDETERMINED','program_cap_infeasibility_proved':False,'higher_cap_run_authorized':False,'physical_release':False}
    raw=(json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=56*2**20,'complete checker science reserve');out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    guard();print(json.dumps({'status':report['status'],'sha256':hashlib.sha256(raw).hexdigest()}),flush=True)


if __name__=='__main__':main()
