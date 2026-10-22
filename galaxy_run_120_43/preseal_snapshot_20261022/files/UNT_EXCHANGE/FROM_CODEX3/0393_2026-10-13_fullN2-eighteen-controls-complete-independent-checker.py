"""SOURCE ONLY. Root complete44-file eighteen-control independent comparison.
CLI --archive ORIGINAL_ABS --output FRESH_ROOT_ABS. No producer science oracle.
All fixtures/events/values/refusals/metadata/closing compared, not selected flags.
"""
import argparse,hashlib,json,os,resource,sys,time
from pathlib import Path
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ROLE='KRYLOV_FULL_N2_MANUFACTURED_CONTROLS_V001'
CAPS={'cpu':1,'rss_bytes':256*2**20,'seconds':60,'output_bytes':16*2**20,'scientific_reserve_bytes':8*2**20}
CALLER = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/krylov_full_n2_manufactured_controls_root_caller_v003.py')
CALLER_SHA = '9e31445945b1b3bafae39271a752d485687bca712307c486354b2c81e3126b90'
SOURCES = {'controls': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/krylov_full_n2_manufactured_controls_v002.py', 'sha256': 'ee6f223bf453856725e6b7a6a6d83ea3171050bc87da70299a5e5e555eea1b69', 'bytes': 8792}, 'caller': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/krylov_full_n2_chunk_root_caller_v003.py', 'sha256': '23052084a42144f3d79ad7955dac0da9c7fe3f57787be3fa4aefe0d2f9cb69a9', 'bytes': 26626}, 'math': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/krylov_full_n2_chunk_math_v001.py', 'sha256': '4453effcdf73f109193c364c1f4caaf354f406d0f8d8c53d4d5eeb042bb5dc3c', 'bytes': 4773}, 'reads': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/history_interval_propagator_v003.py', 'sha256': '72b71831c33ab5ae3a3f0c44bb5d36a5d8797c76cd7797b09b8347653a0e2307', 'bytes': 10410}}
HELPERS = {'custody': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'), 'reads': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0378_2026-10-13_fullN2-independent-reads-and-quadrature.py', 'ffdf91ae5e60adf94e6fbaee6e83d99a5e0a7540de3b98a37882bc7eccd9b471'), 'binding': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0387_2026-10-13_fullN2-independent-original-bindings.py', '10d872ed5bcefa5aa8890539d857bc69919cafd21ec96165ad157ac914169e18'), 'pins': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0390_2026-10-13_fullN2-compatible-frozen-checker-pins.py', '42779dc6e7e924d7fb37b082595abacb0dddf92893ffb7ed9a621e0d865532ed'), 'analytic': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0392_2026-10-13_fullN2-controls-independent-analytic-math.py', '283144e71e55625f242afe48277a9283e3f73663eabc968bb4c99174cf1faac2')}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();start=time.monotonic()
    def guard():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-start>60 or rss>256*2**20:raise RuntimeError('whole checker60s256MiB cap')
    modules={}
    for label,(filename,sha) in HELPERS.items():
        path=Path(filename)
        if not path.is_absolute() or path.resolve()!=path or path.is_symlink() or path.stat().st_size>65536:raise ValueError('plain helper')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('exact helper SHA')
        ns={'__name__':'root_chunk_controls_distinct_'+label,'__file__':filename}
        exec(compile(raw,filename,'exec'),ns);modules[label]=SimpleNamespace(**ns);guard()
    C,R,F,P,A=(modules[k] for k in ('custody','reads','binding','pins','analytic'))
    need,exact,decode=C.need,C.exact,C.decode;I=C.Inputs(guard)
    for path,sha in HELPERS.values():I.read(Path(path),sha,65536)
    I.read(Path(__file__).resolve(),cap=65536)
    root,out=args.archive,args.output
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal original controls archive')
    need(out.is_absolute() and out.resolve()==out and not out.exists() and B in out.parents,'fresh root checker output')
    FILES={'START.json','ROOT_CONFIG.json','SOURCE_SNAPSHOTS.json','SOURCE_GATE.json','FIXTURE.json','RESULTS.json','INPUT_MANIFEST.json','FINISH.json'}|{
        'CALL_%02d_%s.json'%(i,event) for i in range(18) for event in ('PRE','RETURN')}
    need({p.name for p in root.iterdir()}==FILES,'complete44file success census')
    data,filemeta={},{}
    for name in sorted(FILES):
        data[name]=decode(I.read(root/name,cap=8*2**20));pin=I.pins[str(root/name)]
        filemeta[name]={'sha256':pin['sha256'],'bytes':pin['bytes']}
    need(sum(v['bytes'] for v in filemeta.values())<=8*2**20,'whole source output reserve')
    manifest=data['INPUT_MANIFEST.json'];inputlist=manifest['complete_consumed_input_files']
    need(type(inputlist)is list and inputlist and len({x['path'] for x in inputlist})==len(inputlist),'whole unique consumed inputs')
    cp=inputlist[0];need(Path(cp['path']).parent==B,'original root config first input')
    producer_paths=[]
    def pp(pin):
        raw=I.pin(pin,cap=2*2**20)
        if pin['path'] not in producer_paths:producer_paths.append(pin['path'])
        return raw
    cfg=decode(pp(cp));exact(data['ROOT_CONFIG.json'],cfg,'whole configuration snapshot')
    need(set(cfg)=={'schema','role','released_by','execute','output','caps','source_gate'},'closed control release')
    need(cfg['schema']=='KRYLOV_FULL_N2_MANUFACTURED_CONTROLS_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
        and cfg['execute'] is True and cfg['output']==str(root),'actual root control release')
    exact(cfg['caps'],CAPS,'frozen manufactured caps')
    need(Path(cfg['source_gate']['path']).parent==B,'actual root source gate')
    sg=decode(pp(cfg['source_gate']));exact(data['SOURCE_GATE.json'],sg,'whole source gate snapshot')
    callerraw=pp({'path':str(CALLER),'sha256':CALLER_SHA})
    need(sg['acceptor']=='/root' and str(sg['status']).startswith('PASS') and sg['role']==ROLE,'root whole source acceptance')
    exact(sg['source_pins'],SOURCES,'whole fixed source set')
    hits=[r for r in sg['allowed_runners'] if r['path']==str(CALLER) and r['sha256']==CALLER_SHA and r['role']=='producer']
    need(len(hits)==1 and hits[0]['source_author']=='Codex2' and hits[0]['reviewer_id'] not in (None,'Codex2'),'distinct actual source review')
    texts={'root_caller':callerraw.decode()}
    for name,pin in SOURCES.items():texts[name]=pp(pin).decode()
    exact(data['SOURCE_SNAPSHOTS.json'],texts,'whole original source bytes')
    st=data['START.json'];pid=st['pid'];need(type(pid)is int and pid>0,'actual producer PID syntax only')
    exact(st,{'role':ROLE,'executor':'/root','pid':pid,'caps':CAPS,'manufactured_only':True,'scientific_acceptance':False},'completeSTART')
    fixture=A.fixture(P,F,R,SOURCES['caller']);exact(data['FIXTURE.json'],fixture,'every deliberately non-native fixture field')
    fixturepin={'path':str(root/'FIXTURE.json'),**filemeta['FIXTURE.json']}
    outcomes={}
    for index,name in enumerate(A.NAMES):
        exact(data['CALL_%02d_PRE.json'%index],{'case':name,'function':'manufactured_controls.invoke','fixture':fixturepin,
            'source_pins':SOURCES,'phase':'BEFORE_ACTUAL_CALL','manufactured_only':True},'every complete PRE '+name)
        outcome=A.expected(name,fixture,F,R,C)
        exact(data['CALL_%02d_RETURN.json'%index],outcome,'every complete RETURN/refusal '+name)
        outcomes[name]=outcome;guard()
    result={'cases':[{'case':name,'expectation_met':True} for name in A.NAMES],
        'all18_manufactured_expectations_met':True,'distinct_complete_comparison_required':True,
        'native_propagation_executed':False,'original_checkpoint_accepted':False}
    exact(data['RESULTS.json'],result,'all18 exact manufactured outcomes')
    exact(manifest,{'complete_consumed_input_files':[I.pins[p] for p in producer_paths],'root_runtime_custody_required':True},'complete ordered input manifest')
    exact(data['FINISH.json'],{'files_before_finish':{k:v for k,v in filemeta.items() if k!='FINISH.json'},'pid':pid,
        'status':'RAW_COMPLETE_CONTROLS','all_consumed_input_closing_bytes_match':True,'scientific_acceptance':False},'wholeFINISH')
    need({p.name for p in root.iterdir()}==FILES,'closing44files');I.close();guard()
    report={'schema':'KRYLOV_FULL_N2_MANUFACTURED_COMPLETE_INDEPENDENT_COMPARISON_V001',
        'status':'PASS_COMPLETE_SAVED_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY','archive':str(root),
        'producer_author':'Codex2','checker_author':'Codex3','self_review':False,'all44_scientific_files':filemeta,
        'all18_actual_PRE_RETURN_pairs_compared':True,'all_fixture_fields_independently_reconstructed':True,
        'nonlinear_closed_form':'alternating deterministic00/11 endpointcovariance0; averagedlawcovariance1/4',
        'all_refusal_messages_compared':True,'complete_result':result,'complete_checker_input_pins':I.pins,
        'all_opened_input_closing_pins_match':True,'original_runtime_custody_verified_here':False,
        'native_propagation_executed':False,'original_checkpoint_accepted':False,'physical_release':False}
    raw=(json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=8*2**20,'whole checker reserve');out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    guard();print(json.dumps({'status':report['status'],'report_sha256':hashlib.sha256(raw).hexdigest()}),flush=True)


if __name__=='__main__':main()
