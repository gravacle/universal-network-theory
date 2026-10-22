"""SOURCE ONLY. Root-only native exact-reference infinite-time bound producer.
CLI --config ABS --config-sha256 SHA --output FRESH_ABS. New compiler/runtime/
whole-source/control/resource gates required. No launch at import.
"""
import argparse
from fractions import Fraction as Q
import hashlib, json, os, resource, sys, time
from pathlib import Path
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ROLE='P49_CERTIFIED_INFINITE_TIME_NATIVE_V001'
CAPS={'cpu':1,'rss_bytes':16*(1<<30),'seconds':86400,'output_bytes':1<<30,
      'scientific_reserve_bytes':960*(1<<20),'failure_reserve_bytes':1<<20,'runtime_reserve_bytes':63*(1<<20)}
SOURCES = {'reference': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0402_2026-10-13_exact-binary64-spectral-reference.py', 'bytes': 8442, 'sha256': '46c428da1bd85ef762e3478b8e088adb890031ccf8814b7f8dda25b5bf472cca'}, 'abi': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0421_2026-10-13_exact-spectral-kernel-abi-v003.py', 'bytes': 9508, 'sha256': '1a2093685fd85af606f63776c0256759c57bbb2767c30e908a809c669f783684'}, 'bounds': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0415_2026-10-13_complete-certified-cluster-bound-math-v003.py', 'bytes': 14761, 'sha256': '6d903d01da2570cef2e3216db319a674ad7826834eededb5581a416ccb26b8f1'}, 'native': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0336_2026-10-13_native-Krylov-independent-H.py', 'bytes': 8233, 'sha256': 'c65b7c6ad4b4cd41a9ef31c45eeae3c282600b3f4207f9173e80a017f8ad9985'}, 'statistics': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0407_2026-10-13_fullN2-independent-attained-norms-and-quadrature.py', 'bytes': 6248, 'sha256': '6a03e818a79e608162622c5c78489896f6b1adceb912362346b25868dfaa36b3'}, 'kernel': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0383_2026-10-13_exact-spectral-integer-kernel.cpp', 'bytes': 9890, 'sha256': 'b05161ddc7b7b321470cf858d1c0afcb925040c53f68c530bd17040dcfa357e6'}}
INPUTS = {'c153': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_FLOAT_COMPARISON_ACCEPTANCE_V001.json', 'bytes': 2486, 'sha256': '48405948dd46eef4253146dc08f97017e3c6759f452d2548bbcabf150626a522'}, 'packet': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_OUTPUT_V001/ACTUAL_PRE.json', 'bytes': 10998891, 'sha256': '42b9c9106beaa841ed98892caa0cf115d24bee71eca57af3b60d9e0a82a1f272'}, 'original_result': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_OUTPUT_V001/ACTUAL_RETURN.json', 'bytes': 9109945, 'sha256': 'ff407f0488773fb28eb75e6140f647fe2faa6f6307f01d6b2610cb1a1512f412'}, 'original_finish': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_OUTPUT_V001/FINISH.json', 'bytes': 719, 'sha256': 'd159638d750e24ff2a0650c61f09dfef4559a9b884f2d05abafca34a370716e6'}, 'selected': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/ACCEPTED_PARENT_SELECTED_CENSUS.json', 'bytes': 1404745, 'sha256': '39436da4bbc696e9a790b129f4501e94e4cb6cbae700e0419bf012e586068ab8'}, 'emits': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/FULL_INTERFACE_EMITS.jsonl', 'bytes': 28932964, 'sha256': '0b236c5a4b17ce48f5877b14eb427319d57a9fc98eea7af50c0574df4ad5ecd2'}, 'vectors': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_OUTPUT_V001/ALL_EIGENVECTORS.npy', 'sha256': '690ee75633a58e7f76f4b29462f6a502bd8d1d207e3f00f2e0e763e8236bb301', 'bytes': 1741226112}, 'values': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_SPECTRAL_NATIVE_OUTPUT_V001/SHIFTED_EIGENVALUES.npy', 'sha256': '5ae2b69e3ddf16e41b663e269e532def903f80d42b9bdf06eab203ece04dcf32', 'bytes': 83584}}


class ResourceRefusal(RuntimeError):
    pass


def need(ok, why):
    if not ok:
        raise ValueError(why)


def wire(value):
    if isinstance(value,Q):
        return str(value)
    if isinstance(value,dict):
        return {str(k):wire(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [wire(v) for v in value]
    return value


def encoded(value):
    return (json.dumps(wire(value),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON key')
            out[k]=v
        return out
    def bad(v):
        raise ValueError('nonfinite JSON '+v)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)


class Sink:
    def __init__(self,root):
        need(root.is_absolute() and root.resolve()==root and B in root.parents and not root.exists(),'fresh root-owned output')
        root.mkdir(exist_ok=False)
        self.root=root
        self.started=time.monotonic()
        self.files={}
        self.inputs={}
        self.size=0
        self.journals={}

    def guard(self):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-self.started>CAPS['seconds'] or rss>CAPS['rss_bytes']:
            raise ResourceRefusal('whole native24h16GiB cap')
        if self.size>CAPS['scientific_reserve_bytes']:
            raise ResourceRefusal('whole960MiB scientific cap')

    def pin(self,record,retain=True):
        need(set(record)=={'path','sha256','bytes'},'full literal input pin')
        p=Path(record['path'])
        need(p.is_absolute() and p.resolve()==p and not p.is_symlink() and p.is_file(),'plain input path')
        need(type(record['bytes'])is int and 0<=record['bytes']<=2*(1<<30),'input size cap')
        need(not retain or record['bytes']<=64*(1<<20),'retained input RAM bound')
        digest=hashlib.sha256();size=0;blocks=[]
        with p.open('rb') as f:
            while True:
                block=f.read(1<<20)
                if not block:
                    break
                size+=len(block);need(size<=record['bytes'],'complete input size')
                digest.update(block)
                if retain:
                    blocks.append(block)
                self.guard()
        need(size==record['bytes'] and digest.hexdigest()==record['sha256'],'complete input hash')
        if str(p) in self.inputs:
            need(self.inputs[str(p)]==record,'unchanged consumed input')
        self.inputs[str(p)]=dict(record)
        return b''.join(blocks) if retain else dict(record)

    def save(self,name,value):
        name=name+'.json'
        need(Path(name).name==name and name not in self.files and name not in self.journals,'exclusive output name')
        raw=encoded(value)
        self.guard()
        if self.size+len(raw)>CAPS['scientific_reserve_bytes']:
            raise ResourceRefusal('scientific output cap before exclusive write')
        with (self.root/name).open('xb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        pin={'path':str(self.root/name),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        self.files[name]=pin;self.size+=len(raw)
        self.guard()
        return pin

    def append(self,name,value):
        # One exclusively created journal; append complete records to the same
        # still-open descriptor. Never reopen/overwrite any existing artifact.
        need(name in ('KERNEL_EVENTS.jsonl','PROGRESS.jsonl'),'fixed live journal')
        raw=encoded(value)
        self.guard()
        if self.size+len(raw)>CAPS['scientific_reserve_bytes']:
            raise ResourceRefusal('journal scientific cap before append')
        if name not in self.journals:
            self.journals[name]=[(self.root/name).open('xb'),hashlib.sha256(),0,0]
        f,h,size,count=self.journals[name]
        f.write(raw);f.flush();os.fsync(f.fileno());h.update(raw)
        self.journals[name][2:]=[size+len(raw),count+1]
        self.size+=len(raw)

    def close_journals(self):
        for name,(f,h,size,count) in self.journals.items():
            f.close()
            self.files[name]={'path':str(self.root/name),'bytes':size,'sha256':h.hexdigest()}
        self.journals={}

    def module(self,key):
        raw=self.pin(SOURCES[key]);ns={'__name__':'root_exact_infinite_'+key,'__file__':SOURCES[key]['path']}
        exec(compile(raw,SOURCES[key]['path'],'exec'),ns)
        return SimpleNamespace(**ns)


def main():
    if hasattr(sys,'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--config-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    sink=Sink(args.output)
    try:
        cp={'path':str(args.config),'sha256':args.config_sha256,'bytes':args.config.stat().st_size}
        cfg=decode(sink.pin(cp))
        need(set(cfg)=={'schema','role','released_by','execute','output','caps','source_gate',
             'compiler_gate','library','controls_acceptance','original_custody','resource_reservation'},'closed native release')
        need(cfg['schema']=='P49_EXACT_INFINITE_NATIVE_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
             and cfg['execute']is True and cfg['output']==str(args.output) and cfg['caps']==CAPS,'literal root native release')
        own=Path(__file__).resolve();raw=own.read_bytes()
        ownpin={'path':str(own),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
        sink.pin(ownpin)
        gates={}
        for key in ('source_gate','compiler_gate','controls_acceptance','original_custody','resource_reservation'):
            need(Path(cfg[key]['path']).parent==B,'root-owned gate')
            gates[key]=decode(sink.pin(cfg[key]))
            need(gates[key]['acceptor']=='/root' and str(gates[key]['status']).startswith('PASS'),'actual root gate PASS')
        source=gates['source_gate']
        need(source['role']==ROLE and source['sources']==SOURCES and source['producer']==ownpin
             and source['source_author']=='Codex3' and source['distinct_reviewer']not in (None,'Codex3')
             and source['complete_package_reviewed']is True,'complete distinct source gate')
        compiler=gates['compiler_gate']
        need(compiler['kernel_source']==SOURCES['kernel'] and compiler['library']==cfg['library']
             and compiler['signed128_and_abi_qualified']is True and compiler['stack_667648_bytes_qualified']is True
             and compiler['complete_compiler_runtime_custody']is True,'compiled kernel ABI/runtime gate')
        for key in ('compiler_binary','compiler_stdout','compiler_stderr'):
            sink.pin(compiler[key],retain=False)
        need(type(compiler['argv'])is list and all(type(x)is str for x in compiler['argv']) and compiler['argv'],'complete compiler argv')
        control=gates['controls_acceptance']
        need(control['qualified_producer_sources']=={k:SOURCES[k] for k in ('reference','abi','bounds','kernel')}
             and control['producer_kernel']==SOURCES['kernel'] and control['library']==cfg['library']
             and control['tiny_and_256_512_1024_complete']is True
             and control['exact_quantizer_controls_complete']is True and control['complete_cluster_mass_read_LP_controls']is True
             and control['complete_saved_corruption_refusals']is True
             and control['distinct_whole_comparison']is True and control['complete_runtime_custody']is True,'all prior full controls qualified')
        custody=gates['original_custody']
        need(custody['input_pins']==INPUTS and custody['complete_original_opening_checked']is True
             and custody['complete_original_closing_root_obligation']is True,'whole original namespace custody')
        reservation=gates['resource_reservation']
        need(reservation['role']==ROLE and reservation['output']==str(args.output) and reservation['caps']==CAPS
             and reservation['actual_disk_and_all_other_reservations_checked']is True
             and reservation['root_pool_required']is True and reservation['new_dense_scratch_files']==0,'actual complete resource gate')
        sink.save('START',{'role':ROLE,'executor':'/root','pid':os.getpid(),'caps':CAPS,
                          'external_watchdog_required':True,'scientific_acceptance':False})
        sink.save('ROOT_CONFIG',cfg);sink.save('GATE_SNAPSHOTS',gates)
        snapshots={'caller':raw.decode()}
        for key,pin in SOURCES.items():
            snapshots[key]=sink.pin(pin).decode()
        sink.save('SOURCE_SNAPSHOTS',snapshots)
        mods={key:sink.module(key) for key in ('reference','abi','bounds','native','statistics')}
        D,A,M,N,T=(mods[k] for k in ('reference','abi','bounds','native','statistics'))
        docs={key:decode(sink.pin(INPUTS[key])) for key in ('c153','packet','original_result','original_finish','selected')}
        for key in ('emits','vectors','values'):
            sink.pin(INPUTS[key],retain=False)
        original=docs['original_result'];accepted=docs['c153'];finish=docs['original_finish']
        need(accepted['acceptor']=='/root' and accepted['claim']=='C-153' and
             accepted['whole_raw_actual_return']['path']==INPUTS['original_result']['path'] and
             accepted['whole_raw_actual_return']['sha256']==INPUTS['original_result']['sha256'],'same original C153 full result')
        need(original['exception']is None and original['phase']=='native' and original['value']['dimension']==10432,
             'complete original floating comparator')
        need(original['value']['seed_names']==list(M.SEEDS) and original['value']['read_names']==list(M.READS),'exact original seed/read naming and order')
        for key,shape,dtype in (('vectors',[10432,10432],'<c16'),('values',[10432],'<f8')):
            pin=INPUTS[key];name=Path(pin['path']).name
            expected={'shape':shape,'dtype':dtype,'bytes':pin['bytes'],'sha256':pin['sha256']}
            need(finish['complete_arrays'][name]==expected and original['complete_arrays'][name]==expected,'full original array closure')
        sink.save('ORIGINAL_BINDING',{'inputs':INPUTS,'seed_names':list(M.SEEDS),'read_names':list(M.READS),
                  'C153_float_only':True,'original_backend_warnings_not_waived':True})
        need(docs['packet']['phase']=='native','original native packet')
        with Path(INPUTS['emits']['path']).open('rb') as f:
            native=N.reconstruct(docs['packet']['complete_native_packet'],docs['selected'],(decode(line) for line in f),sink.guard)
        sink.save('NATIVE',native)
        diagonals,seeds,extrema=M.complete_reads_and_seeds(native['active_states'])
        dref=sink.save('DIAGONALS_AND_SEEDS',{'identity':[1]*10432,'reads':diagonals,'seed_integer_terms':seeds,
                       'seed_amplitude_denominator':5,'complete_actual_extrema':extrema,'theorem_uses_declared_global_caps':True})
        parts=M.partitions(original,10432);sink.save('PARTITIONS',parts)
        progress=lambda record:sink.append('PROGRESS.jsonl',record)
        w,lambdas,reference=D.reconstruct(INPUTS['vectors'],INPUTS['values'],10432,sink.guard,progress)
        sink.save('EXACT_REFERENCE',reference)
        kernel=A.Kernel(cfg['library'],sink.pin,10432,w,lambdas,sink.guard,
                        lambda name,value:sink.append('KERNEL_EVENTS.jsonl',{'name':name,'value':value}),progress)
        gram=kernel.gram();sink.save('GRAM_NORMS',gram)
        expected=[{k:v for k,v in item.items() if k!='nonzero_integer_components'} for item in reference['columns']]
        need(gram['complete_column_metadata']==expected,'whole quantizer/kernel max-L1 identity')
        residual=kernel.residual(native['rows']);sink.save('RESIDUAL_NORMS',residual)
        products=M.seed_products(w,10432,seeds,sink.guard);sink.save('ALL_SEED_PRODUCTS',products)
        result=M.certify(10432,lambdas,gram,residual,parts,products,diagonals,dref,kernel,sink.save,sink.guard)
        laws={seed:{name:result['intersections'][seed][name] for name in M.WORDS} for seed in M.SEEDS}
        result['averaged_word_statistics']={seed:T.statistics(laws[seed]) for seed in M.SEEDS}
        pairs=[]
        for i,left in enumerate(M.SEEDS):
            for right in M.SEEDS[i+1:]:
                distances=[T.distance(laws[left][name],laws[right][name]) for name in M.WORDS]
                pairs.append({'left':left,'right':right,
                    'TV_interval':[max(Q(0),sum(x[0] for x in distances)/2),min(Q(1),sum(x[1] for x in distances)/2)],
                    'energy_matched_causal_memory_claim':False})
        result['all_ten_seed_pair_word_TV']=pairs
        result['read_identities']={'sum_four_words':'1','old_plus_born_presence':'1','carrier_plus_Ready':'1',
                                   'Nq_old':'q0+q1','intervals_not_renormalized':True}
        sink.save('RESULTS',result)
        sink.close_journals()
        for pin in list(sink.inputs.values()):
            sink.pin(pin,retain=False)
        sink.save('INPUT_MANIFEST',{'complete_consumed_input_files':list(sink.inputs.values()),
                  'whole_original_namespace_closing_root_obligation':True})
        sink.save('PROFILE',{'whole_elapsed_before_profile':time.monotonic()-sink.started,
                  'all_kernel_calls':kernel.serial,'new_dense_files':0,'dense_W_RAM_bytes':16*10432**2,
                  'future_native_throughput_guarantee':False})
        sink.save('FINISH',{'role':ROLE,'pid':os.getpid(),'status':result['status'],'files_before_finish':dict(sink.files),
                  'all_consumed_closing_bytes_match':True,'scientific_acceptance':False,
                  'distinct_complete_comparison_and_root_runtime_custody_required':True})
        print(json.dumps({'status':result['status'],'scientific_acceptance':False}),flush=True)
    except BaseException as error:
        sink.close_journals()
        failure={'role':ROLE,'status':'RESOURCE_REFUSAL' if isinstance(error,ResourceRefusal) else 'FAILED_PREFIX',
                 'exception':type(error).__name__,'message':str(error),'scientific_acceptance':False,
                 'no_partial_certificate_accepted':True,'recorded_scientific_bytes':sink.size}
        raw=encoded(failure)
        if len(raw)<=CAPS['failure_reserve_bytes']:
            with (sink.root/'FAILURE.json').open('xb') as f:
                f.write(raw);f.flush();os.fsync(f.fileno())
        raise


if __name__=='__main__':
    main()
