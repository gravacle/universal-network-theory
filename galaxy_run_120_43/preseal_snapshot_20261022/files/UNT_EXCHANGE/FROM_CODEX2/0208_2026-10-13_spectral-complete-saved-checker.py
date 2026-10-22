"""SOURCE ONLY: independently reconstruct complete12/15-file saved spectra.
Root alone executes after distinct review; full runtime/custody adjudication separate.
CLI --input ABS_DIRECTORY --output NEW_REPORT_JSON. No producer imports/calls.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from types import SimpleNamespace
import numpy as np
SOURCES = {'method': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_SPECTRAL_CODEX3/spectral_comparator_v003.py', 'sha256': 'ad4b3f0e7d9abd9f05e8989578fea82772ae6586c016435c1df9998a29e5ed56'}, 'binding': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_SPECTRAL_CODEX3/native_binding_py39_v001.py', 'sha256': 'c414a39f2bebfd613fc3ae4b1e53440bd0bc37987c7c7385b5091bc9548775d6'}, 'inventory': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_SPECTRAL_CODEX3/owned_runtime_inventory_v001.py', 'sha256': 'f6ada63431a5cde326532307068e15a453c299dd8500e18f64c4596dc59625d0'}, 'original_binding': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/history_interval_binding_and_sink_v003.py', 'sha256': 'c7ed5b97f0e77a456c8450ffc6e86f3e34156006c71f09f77c458972e0bd8347'}, 'original_preparations': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/old_history_word_prospect_v001.py', 'sha256': '8ffff770abd5f5799d77911f08657eef620464f0789d1e00215e3d1a8affc5d1'}}
INPUTS = {'INPUT_EMITS.jsonl': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/FULL_INTERFACE_EMITS.jsonl', 'sha256': '0b236c5a4b17ce48f5877b14eb427319d57a9fc98eea7af50c0574df4ad5ecd2'}, 'INPUT_SELECTED.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/ACCEPTED_PARENT_SELECTED_CENSUS.json', 'sha256': '39436da4bbc696e9a790b129f4501e94e4cb6cbae700e0419bf012e586068ab8'}, 'INPUT_COMPONENTS.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/COMPLETE_STRUCTURAL_COMPONENTS.json', 'sha256': 'f9902ade8feb0dbd69f1ac90a3552a98c3f6ed0b3694105601875ca20a998635'}}
OWN_MODULES = {'native': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0206_2026-10-13_spectral-independent-native-columns.py', 'sha256': 'b01730794f6596ab1681e49875a95c8c5fcde524732391ce4652f4a98b167a47'}, 'math': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0207_2026-10-13_spectral-independent-full-array-math.py', 'sha256': '73abf9edbe6197eaa93040e775ab20780c91aee86e602ec81ba0f9ffeca0ceae'}}
HISTORY = {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_STAGE2_SCIENTIFIC_ACCEPTANCE_V001.json', 'sha256': '2b0675e9d33df995341ebe861f3d586ec1bdbd1b911ffa61073d992d4bec8a39'}
ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
RUNNER_PIN = '904bc49aba285a1d50ac6a84f45dcee55279901182fa2bb518e73f0269664f91'
CAPS={'feasibility':{'cpu':1,'rss_bytes':2*2**30,'seconds':600,'output_bytes':128*2**20},
      'native':{'cpu':1,'rss_bytes':16*2**30,'seconds':43200,'output_bytes':6*2**30}}
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
COUNTS={'compared_numeric_leaves':0,'largest_absolute_difference':0.0}


def need(ok,label):
    if not ok:raise ValueError(label)


def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'duplicate JSON');out[k]=v
        return out
    def bad(value):raise ValueError('nonfinite JSON '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)


def wire(v):
    if isinstance(v,complex):return {'real':v.real,'imag':v.imag}
    if isinstance(v,dict):return {k:wire(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [wire(x) for x in v]
    return v


def compare(actual,expected,path):
    if type(expected) is dict:
        need(type(actual) is dict and set(actual)==set(expected),path+' fields')
        for k in expected:compare(actual[k],expected[k],path+'/'+k)
    elif type(expected) is list:
        need(type(actual) is list and len(actual)==len(expected),path+' census')
        for i,(a,b) in enumerate(zip(actual,expected)):compare(a,b,path+'/'+str(i))
    elif type(expected) is float:
        need(type(actual) in (int,float) and math.isfinite(actual) and math.isfinite(expected),path+' finite')
        difference=abs(actual-expected)
        need(difference<=2e-10+2e-12*abs(expected),path+' independently reconstructed number')
        COUNTS['compared_numeric_leaves']+=1
        COUNTS['largest_absolute_difference']=max(COUNTS['largest_absolute_difference'],difference)
    else:need(type(actual)==type(expected) and actual==expected,path+' exact literal')


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()


def plain(path):
    need(path.is_absolute() and path.resolve()==path and path.is_file() and not path.is_symlink(),'plain absolute artifact')


def usage(value,cap):
    need(type(value) is dict and set(value)=={'rss_peak_bytes','user_seconds','system_seconds'},'complete usage')
    need(type(value['rss_peak_bytes']) is int and 0<value['rss_peak_bytes']<=cap,'owned RSS within cap')
    for k in ('user_seconds','system_seconds'):need(type(value[k]) in (int,float) and math.isfinite(value[k]) and value[k]>=0,'finite owned CPU usage')


def inventory(record,cap,pid=None):
    fields={'pid','python_literal','python_canonical','python_version','uname','numpy_version',
      'numpy_module_path','numpy_build_config','thread_environment','own_loaded_images','own_usage','scope'}
    need(type(record) is dict and set(record)==fields,'complete runtime inventory')
    need(type(record['pid']) is int and record['pid']>0 and (pid is None or record['pid']==pid),'owned PID consistency')
    need(record['numpy_version']=='2.0.2','pinned actual NumPy version')
    need(record['numpy_module_path']=='/Users/bgm/Library/Python/3.9/lib/python/site-packages/numpy/__init__.py','actual pinned NumPy location')
    need(type(record['python_literal']) is str and os.path.realpath(record['python_literal'])==record['python_canonical'],'literal/canonical interpreter inventory')
    need(record['thread_environment']=={k:'1' for k in THREADS},'all five requested singlethread env')
    need(type(record['numpy_build_config']) is dict and record['numpy_build_config'],'actual build config')
    need(type(record['own_loaded_images']) is list and 0<len(record['own_loaded_images'])<=4096 and all(type(v) is str and v for v in record['own_loaded_images']),'complete bounded actual dyld inventory')
    need(record['scope']=='CURRENT_PROCESS_ONLY_NO_HOST_LOAD_OR_HARD_CORE_QUOTA_CLAIM','runtime scope')
    usage(record['own_usage'],cap)


def load_array(path,n,which,meta):
    with path.open('rb') as f:
        version=np.lib.format.read_magic(f)
        need(version==(1,0),'frozen NumPy array format1.0')
        shape,fortran,dtype=np.lib.format.read_array_header_1_0(f,max_header_size=4096)
        headerbytes=f.tell()
    expectedshape=(n,) if which=='E' else (n,n)
    expectedtype=np.dtype('<f8') if which=='E' else np.dtype('<c16')
    need(shape==expectedshape and dtype==expectedtype and type(fortran) is bool,'bounded complete array shape/type')
    size=headerbytes+math.prod(shape)*dtype.itemsize
    need(path.stat().st_size==size,'no truncated or extra array bytes')
    compare(meta,{'shape':list(shape),'dtype':dtype.str,'bytes':size,'sha256':digest(path)},'complete array metadata')
    return np.load(path,mmap_mode='r',allow_pickle=False,max_header_size=4096)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();folder=args.input
    need(folder.is_absolute() and folder.resolve()==folder and folder.is_dir() and not folder.is_symlink(),'literal input directory')
    names={'START.json','ROOT_CONFIG.json','SOURCE_SNAPSHOTS.json','GATE_SNAPSHOTS.json',
      'RUNTIME_INVENTORY.json','PROGRESS.jsonl','ACTUAL_PRE.json','SHIFTED_EIGENVALUES.npy',
      'ALL_EIGENVECTORS.npy','ACTUAL_RETURN.json','RUNTIME_FINAL.json','FINISH.json'}
    files=list(folder.iterdir());need(all(p.is_file() and not p.is_symlink() for p in files),'plain complete files')
    need((folder/'ROOT_CONFIG.json').stat().st_size<=2**20,'bounded config')
    configraw=(folder/'ROOT_CONFIG.json').read_bytes();config=decode(configraw)
    need(set(config)=={'schema','phase','size','output','caps','released_by','execute','source_acceptance',
      'control_acceptance','feasibility_acceptance','history_acceptance','root_confirms_all_required_gates'},'root config schema')
    phase=config['phase'];n=config['size'];need(phase in CAPS and type(n) is int,'fixed phase and dimension')
    need(n in ((256,512,1024) if phase=='feasibility' else (10432,)),'frozen dimensions')
    need(config['schema']=='P49_SPECTRAL_HELD_RELEASE_V001' and config['released_by']=='/root' and config['execute'] is True and config['root_confirms_all_required_gates'] is True,'root semantic release assertion')
    need(config['output']==str(folder) and config['caps']==CAPS[phase],'original path/caps')
    if phase=='native':names|=set(INPUTS);need(config['history_acceptance']==HISTORY,'fixed original history ancestry')
    else:need(config['history_acceptance'] is None and config['feasibility_acceptance'] is None,'synthetic scope')
    need({p.name for p in files}==names,'whole12or15file census')
    need(sum(p.stat().st_size for p in files)<=CAPS[phase]['output_bytes'],'complete artifact cap')
    original={p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in files}
    docs={p.name:decode(p.read_bytes()) for p in files if p.suffix=='.json'}
    start=docs['START.json'];pin=start['config_pin'];need(set(pin)=={'path','sha256'},'originalconfig pin')
    rootconfig=Path(pin['path']);plain(rootconfig);need(rootconfig.parent==ROOT,'root-owned actual release')
    need(rootconfig.read_bytes()==configraw and hashlib.sha256(configraw).hexdigest()==pin['sha256'],'original root config exactbytes')
    compare(start,{'schema':'P49_SPECTRAL_FIXED_WORKER_START_V001','config_pin':pin,'sources':SOURCES,
      'phase':phase,'size':n,'caps':CAPS[phase],'runner_sha256':RUNNER_PIN,
      'exact_DE_certified':False,'physical_state_selected':False},'START')
    snapshots=docs['SOURCE_SNAPSHOTS.json'];need(set(snapshots)==set(SOURCES),'all source snapshots')
    for role,pin in SOURCES.items():need(type(snapshots[role]) is str and hashlib.sha256(snapshots[role].encode()).hexdigest()==pin['sha256'],'whole source snapshot '+role)
    gates=docs['GATE_SNAPSHOTS.json'];keys={k for k in ('source_acceptance','control_acceptance','feasibility_acceptance','history_acceptance') if config[k] is not None}
    need(set(gates)==keys and {'source_acceptance','control_acceptance'}<=keys,'complete prerequisite gates')
    if phase=='native':need(keys=={'source_acceptance','control_acceptance','feasibility_acceptance','history_acceptance'},'native actual feasibility gate')
    gateoriginal={}
    for k in keys:
        gp=config[k];need(type(gp) is dict and set(gp)=={'path','sha256'},'exact actualgate pin')
        p=Path(gp['path']);plain(p);need(p.parent==ROOT,'rootowned actual gate')
        raw=gates[k].encode();need(len(raw)<=8*2**20 and hashlib.sha256(raw).hexdigest()==gp['sha256'] and type(decode(raw)) is dict,'whole gate snapshot')
        need(p.read_bytes()==raw,'actual original gate exactbytes');gateoriginal[p]=raw
    modules={};ownraw={}
    for role,pin in OWN_MODULES.items():
        p=Path(pin['path']);plain(p);raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'independent module pin')
        env={'__name__':'independent_spectral_'+role,'__file__':str(p)}
        exec(compile(raw,str(p),'exec'),env);modules[role]=SimpleNamespace(**env);ownraw[p]=raw
    if phase=='native':
        for name,pin in INPUTS.items():need(original[name]['sha256']==pin['sha256'],'whole accepted native input '+name)
        def stream():
            with (folder/'INPUT_EMITS.jsonl').open() as f:
                for line in f:yield decode(line)
        packet,preps,rows,seeds,reads,scale,shift=modules['native'].reconstruct(stream(),docs['INPUT_SELECTED.json'],docs['INPUT_COMPONENTS.json'])
        expectedpre={'phase':phase,'input_pins':INPUTS,'complete_native_packet':packet,'all_preparations':preps,'function':'native_solve','diagnostic_scope_only':True}
        need(docs['ACTUAL_PRE.json']==expectedpre,'complete independently reconstructed native PRE packet')
    else:
        rows=[]
        for i in range(n):
            row=[(i,complex(i/n))]
            if i:row.append((i-1,complex(-.25,-.125)))
            if i<n-1:row.append((i+1,complex(-.25,.125)))
            rows.append(row)
        seeds={'e0':[1]+[0]*(n-1)};reads={'P0':[1]+[0]*(n-1)};scale=2.;shift=0.
        pre={'phase':phase,'size':n,'rows':rows,'seeds':seeds,'diagonal_reads':reads,'row_scale':scale,'shift':shift,'function':'eigh_then_analyse','physical_carrier':False}
        need(docs['ACTUAL_PRE.json']==wire(pre),'exact synthetic PRE')
    actual=docs['ACTUAL_RETURN.json'];need(set(actual)=={'phase','exception','value','elapsed_method_seconds','complete_arrays'} and actual['phase']==phase and actual['exception'] is None,'complete successful actual return')
    elapsed=actual['elapsed_method_seconds'];need(type(elapsed) in (int,float) and math.isfinite(elapsed) and 0<=elapsed<=CAPS[phase]['seconds'],'actual elapsed cap')
    meta=actual['complete_arrays'];need(set(meta)=={'SHIFTED_EIGENVALUES.npy','ALL_EIGENVECTORS.npy'},'all fullarrays')
    E=load_array(folder/'SHIFTED_EIGENVALUES.npy',n,'E',meta['SHIFTED_EIGENVALUES.npy'])
    V=load_array(folder/'ALL_EIGENVECTORS.npy',n,'V',meta['ALL_EIGENVECTORS.npy'])
    def progress(event,a,b):print(json.dumps({'event':event,'lo':a,'hi':b}),flush=True)
    expected=modules['math'].reconstruct(rows,seeds,reads,scale,shift,E,V,progress,phase=='native')
    compare(actual['value'],wire(expected),'ALL_RECONSTRUCTED_SPECTRAL_OUTPUTS')
    compare(docs['FINISH.json'],{'status':'COMPLETE_FLOAT_COMPARATOR_AWAITING_DISTINCT_SAVED_CHECKER','phase':phase,'size':n,'complete_arrays':meta,
      'diagnostics_passed':expected['diagnostics_passed'],'exact_DE_certified':False,'physical_state_selected':False,'all_pinned_inputs_closing_bytes_match':True},'FINISH')
    events=[('before_complete_eigh',n,n),('complete_eigenarrays_saved',n,n)]
    events.extend(('all_column_residual_and_gram',lo,min(n,lo+64)) for lo in range(0,n,64))
    partitions=[[[j,j+1] for j in range(n)]]+[g['groups_half_open'] for g in expected['coherent_group_comparators']]
    for groups in partitions:
        events.extend(('coherent_group',lo,hi) for lo,hi in groups if hi-lo>1)
        count=sum(hi-lo==1 for lo,hi in groups)
        events.extend(('singleton_read_block',lo,min(count,lo+64)) for lo in range(0,count,64))
    journal=[decode(line) for line in (folder/'PROGRESS.jsonl').read_bytes().splitlines()]
    need(len(journal)==len(events),'whole progress event census');last=-math.inf
    for row,event in zip(journal,events):
        need(set(row)=={'event','lo','hi','monotonic_seconds','usage'} and (row['event'],row['lo'],row['hi'])==event,'complete ordered progress')
        t=row['monotonic_seconds'];need(type(t) in (int,float) and math.isfinite(t) and t>=last,'monotonic progress');last=t;usage(row['usage'],CAPS[phase]['rss_bytes'])
    initial=docs['RUNTIME_INVENTORY.json'];final=docs['RUNTIME_FINAL.json'];need(set(final)=={'inventory','survey'},'whole runtimefinal')
    inventory(initial,CAPS[phase]['rss_bytes']);inventory(final['inventory'],CAPS[phase]['rss_bytes'],initial['pid'])
    survey=final['survey'];need(set(survey)=={'samples','sample_seconds_requested','owned_peak_thread_count_sampled','thread_scope','initial_usage','final_usage','elapsed_seconds','hard_RSS_storage_core_quota_claim','external_parent_timeout_and_RSS_storage_monitor_required'},'complete survey')
    need(type(survey['samples']) is int and survey['samples']>=2 and type(survey['owned_peak_thread_count_sampled']) is int and survey['owned_peak_thread_count_sampled']>=1,'actual owned thread samples')
    need(survey['sample_seconds_requested']==.05 and survey['hard_RSS_storage_core_quota_claim'] is False and survey['external_parent_timeout_and_RSS_storage_monitor_required'] is True,'honest monitor scope')
    need(survey['thread_scope']=='ALL_OWN_THREADS_INCLUDING_MONITORS_NOT_NUMBER_OF_ACTIVE_BLAS_CORES','ownedthread meaning')
    need(type(survey['elapsed_seconds']) in (int,float) and math.isfinite(survey['elapsed_seconds']) and elapsed<=survey['elapsed_seconds']<=CAPS[phase]['seconds'],'whole survey elapsed')
    for val in (survey['initial_usage'],survey['final_usage']):usage(val,CAPS[phase]['rss_bytes'])
    for k in survey['initial_usage']:need(survey['final_usage'][k]>=survey['initial_usage'][k],'monotone own usage')
    need(rootconfig.read_bytes()==configraw,'closing root config')
    for p,raw in {**gateoriginal,**ownraw}.items():need(p.read_bytes()==raw,'closing source/gate original')
    for name,pin in original.items():need((folder/name).stat().st_size==pin['bytes'] and digest(folder/name)==pin['sha256'],'closing whole savedfile '+name)
    report={'status':'INDEPENDENT_COMPLETE_SPECTRAL_SAVED_COMPARISON_PASS','author':'Codex2','phase':phase,'size':n,
      'complete_files':len(original),'original_files':original,'independent_modules':OWN_MODULES,
      'comparison':dict(COUNTS,tolerance='2e-10+2e-12*abs(expected)',whole_columns=True,whole_Gram=True,whole_eigenarrays=True),
      'diagnostics_passed':expected['diagnostics_passed'],'exact_DE_certified':False,'physical_state_selected':False,
      'original_owned_pid':initial['pid'],'requires_root_full_original_process_runtime_and_final_adjudication':True,
      'backend_dependency':'INDEPENDENT_SOURCE_SAME_PINNED_NUMPY_BLAS_NUMERICAL_PRIMITIVES',
      'native_prediction_release':False}
    with args.output.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

if __name__=='__main__':main()
