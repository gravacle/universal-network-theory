"""SOURCE ONLY. Root-only exact spectral control caller, one frozen case/job.
CLI --config ABS --config-sha256 SHA --output FRESH_ABS. Every actual case is RAW;
source/compiler/runtime and distinct complete saved-result gates remain external.
"""
import argparse
from fractions import Fraction as Q
import hashlib,json,os,resource,sys,time
from pathlib import Path
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ROLE='P49_EXACT_SPECTRAL_COMPLETE_CONTROLS_V001'
CAPS={'cpu':1,'rss_bytes':2*(1<<30),'seconds':1200,'output_bytes':128*(1<<20),
      'scientific_reserve_bytes':120*(1<<20),'failure_reserve_bytes':1<<20,'runtime_reserve_bytes':7*(1<<20)}
SOURCES={'reference': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0402_2026-10-13_exact-binary64-spectral-reference.py', 'bytes': 8442, 'sha256': '46c428da1bd85ef762e3478b8e088adb890031ccf8814b7f8dda25b5bf472cca'}, 'abi': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0421_2026-10-13_exact-spectral-kernel-abi-v003.py', 'bytes': 9508, 'sha256': '1a2093685fd85af606f63776c0256759c57bbb2767c30e908a809c669f783684'}, 'bounds': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0415_2026-10-13_complete-certified-cluster-bound-math-v003.py', 'bytes': 14761, 'sha256': '6d903d01da2570cef2e3216db319a674ad7826834eededb5581a416ccb26b8f1'}, 'engine': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0439_2026-10-13_exact-spectral-complete-call-custody-controls-engine-v002.py', 'bytes': 42122, 'sha256': 'de291dd3e7aa01193e2b63a61d92143c349dda33b9a1d0b3a41a5c63d4af70c1'}, 'independent_abi': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0438_2026-10-13_independent-integer-control-abi-status-v003.py', 'bytes': 6333, 'sha256': 'e3e9af849b683751a57e426b4e4c76d03f39be064606ac929965e114bc67604c'}, 'producer_kernel': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0383_2026-10-13_exact-spectral-integer-kernel.cpp', 'bytes': 9890, 'sha256': 'b05161ddc7b7b321470cf858d1c0afcb925040c53f68c530bd17040dcfa357e6'}, 'independent_reference': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/p49_integer_reference_controls_v001.py', 'bytes': 5766, 'sha256': 'c7accf7e958d653ec364af1c5fccbf917ec44c2ab305f1457c88544d4e2a6b6d'}, 'independent_kernel': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/p49_independent_integer_primitives_v002.cpp', 'bytes': 10378, 'sha256': '1eb2d8651feafe61a8841d42b18a125c9f58672992f69c2e63886e55fc2b88c2'}, 'independent_binary64': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/p49_independent_binary64_reference_v001.py', 'bytes': 6552, 'sha256': '04598db4c4b80581584d7da3ef96d22228b1be5d8b5bd77eacff19d2301f0229'}}

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
        self.binaries={}

    def guard(self):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-self.started>CAPS['seconds'] or rss>CAPS['rss_bytes']:
            raise ResourceRefusal('whole control1200s2GiB cap')
        if self.size>CAPS['scientific_reserve_bytes']:
            raise ResourceRefusal('whole control120MiB scientific cap')

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
        need(name in ('KERNEL_EVENTS.jsonl','PROGRESS.jsonl','INDEPENDENT_EVENTS.jsonl','CONTROL_EVENTS.jsonl'),'fixed live journal')
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

    def blob(self,name,raw):
        handle=self.binary(name,b'')
        self.binary_append(handle,raw)
        return self.binary_close(handle)

    def binary(self,name,header):
        need(Path(name).name==name and name not in self.files and name not in self.binaries and name not in self.journals,'fresh binary name')
        self.guard()
        handle={'name':name,'file':(self.root/name).open('xb'),'hash':hashlib.sha256(),'bytes':0}
        self.binaries[name]=handle
        self.binary_append(handle,header)
        return handle

    def binary_append(self,handle,raw):
        self.guard()
        need(handle['name'] in self.binaries and type(raw)is bytes,'live binary bytes')
        if self.size+len(raw)>CAPS['scientific_reserve_bytes']:
            raise ResourceRefusal('full binary output cap before write')
        f=handle['file'];f.write(raw);f.flush();os.fsync(f.fileno())
        handle['hash'].update(raw);handle['bytes']+=len(raw);self.size+=len(raw)

    def binary_close(self,handle):
        name=handle['name'];need(self.binaries.get(name)is handle,'owned binary handle')
        handle['file'].close()
        pin={'path':str(self.root/name),'sha256':handle['hash'].hexdigest(),'bytes':handle['bytes']}
        self.files[name]=pin
        del self.binaries[name]
        return pin

    def close_all(self):
        for handle in list(self.binaries.values()):
            self.binary_close(handle)
        self.close_journals()


def main():
    if hasattr(sys,'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--config-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();sink=Sink(args.output)
    try:
        cp={'path':str(args.config),'sha256':args.config_sha256,'bytes':args.config.stat().st_size}
        cfg=decode(sink.pin(cp))
        need(set(cfg)=={'schema','role','released_by','execute','output','caps','case','source_gate',
                       'compiler_gates','libraries','resource_reservation'},'closed control release')
        need(cfg['schema']=='P49_EXACT_SPECTRAL_CONTROL_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
             and cfg['execute']is True and cfg['output']==str(args.output) and cfg['caps']==CAPS,'actual bounded root control release')
        own=Path(__file__).resolve();raw=own.read_bytes()
        ownpin={'path':str(own),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)};sink.pin(ownpin)
        def gate(pin):
            need(Path(pin['path']).parent==B,'root control gate namespace')
            value=decode(sink.pin(pin))
            need(value['acceptor']=='/root' and str(value['status']).startswith('PASS'),'actual root gate')
            return value
        source=gate(cfg['source_gate']);resource_gate=gate(cfg['resource_reservation'])
        need(source['role']==ROLE and source['sources']==SOURCES and source['caller']==ownpin
             and source['caller_author']=='Codex3' and source['caller_distinct_reviewer']not in (None,'Codex3')
             and source['complete_control_source_review']is True,'whole distinct control source gate')
        need(set(cfg['compiler_gates'])==set(cfg['libraries'])=={'producer','independent'},'both distinct compiled sources')
        compiler_gates={key:gate(pin) for key,pin in cfg['compiler_gates'].items()}
        for key,value in compiler_gates.items():
            need(value['kernel_source']==SOURCES[key+'_kernel'] and value['library']==cfg['libraries'][key]
                 and value['bounded_owned_build_closed']is True and value['integer_widths_target_and_signatures_bound']is True,
                 'exact complete compiler gate before control ABI qualification')
            for label in ('compiler_binary','compiler_stdout','compiler_stderr'):
                sink.pin(value[label],retain=False)
        need(resource_gate['role']==ROLE and resource_gate['output']==str(args.output) and resource_gate['caps']==CAPS
             and resource_gate['case']==cfg['case'] and resource_gate['actual_disk_and_all_other_reservations_checked']is True
             and resource_gate['root_pool_required']is True,'actual complete control reservation')
        modules={key:sink.module(key) for key in ('reference','abi','bounds','engine','independent_abi','independent_reference','independent_binary64')}
        need(cfg['case'] in modules['engine'].CASES,'exact frozen case')
        snapshots={'caller':raw.decode()}
        for key,pin in SOURCES.items():snapshots[key]=sink.pin(pin).decode()
        sink.save('START',{'role':ROLE,'pid':os.getpid(),'executor':'/root','case':cfg['case'],'caps':CAPS,
                          'external_watchdog_required':True,'scientific_acceptance':False})
        sink.save('ROOT_CONFIG',cfg)
        sink.save('GATE_SNAPSHOTS',{'source':source,'compiler_gates':compiler_gates,'resource':resource_gate})
        sink.save('SOURCE_SNAPSHOTS',snapshots)
        result=modules['engine'].run(cfg['case'],modules,sink,cfg['libraries'])
        sink.save('RESULTS',result);sink.close_all()
        for pin in list(sink.inputs.values()):sink.pin(pin,retain=False)
        sink.save('INPUT_MANIFEST',{'complete_consumed_input_files':list(sink.inputs.values())})
        sink.save('PROFILE',{'whole_elapsed_before_profile':time.monotonic()-sink.started,
                  'case':cfg['case'],'future_native_throughput_guarantee':False})
        sink.save('FINISH',{'role':ROLE,'case':cfg['case'],'pid':os.getpid(),'status':result['status'],
                  'files_before_finish':dict(sink.files),'all_consumed_closing_bytes_match':True,
                  'scientific_acceptance':False,'distinct_complete_saved_comparison_and_runtime_custody_required':True})
        print(json.dumps({'case':cfg['case'],'status':result['status'],'scientific_acceptance':False}),flush=True)
    except BaseException as error:
        sink.close_all()
        raw=encoded({'role':ROLE,'status':'RESOURCE_REFUSAL' if isinstance(error,ResourceRefusal) else 'FAILED_PREFIX',
                     'exception':type(error).__name__,'message':str(error),'scientific_acceptance':False,
                     'recorded_scientific_bytes':sink.size,'partial_results_not_accepted':True})
        if len(raw)<=CAPS['failure_reserve_bytes']:
            with (sink.root/'FAILURE.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        raise


if __name__=='__main__':main()
