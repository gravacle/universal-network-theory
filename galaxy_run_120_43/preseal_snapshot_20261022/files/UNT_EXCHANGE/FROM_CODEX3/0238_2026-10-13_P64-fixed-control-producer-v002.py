"""P64 fixed source/input/actual-return custody. SOURCE ONLY; root executes.
External reviewed supervisor required. No native inputs, child spawning or network.
"""
import argparse
import hashlib
import json
import os
import numpy as np
from pathlib import Path

SOURCE=Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0225_2026-10-13_P64-current-history-method-source-v002.py')
PIN='693448ad4a3568b7bae1b981404bc586dacae84302951e8959dd14e9c4598892'


def encode(x):
    if isinstance(x,np.bool_):return x.item()  # exact NumPy boolean -> builtin bool
    if isinstance(x,complex):return {'real':x.real,'imag':x.imag}
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if x is None or type(x) in (str,int,float,bool):return x
    raise TypeError(type(x).__name__)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('source pin mismatch')
    args.output.mkdir(exist_ok=False)
    def save(name,value):
        with (args.output/name).open('x') as f:
            json.dump(encode(value),f,indent=2,allow_nan=False)
            f.write('\n');f.flush();os.fsync(f.fileno())
    save('START.json',{'source':str(SOURCE),'source_sha256':PIN,
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'P64_FIXED_MANUFACTURED_CURRENT_HISTORY_METHOD_ONLY',
        'tolerance':1e-9,'dimension':2,'native_motion_release':False})
    try:
        with (args.output/'SOURCE_SNAPSHOT.py').open('xb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        module={'__name__':'p64_reviewed_method','__file__':str(SOURCE)}
        exec(compile(raw,str(SOURCE),'exec'),module)
        names=[];pending={}
        def audit(event,name,value):
            if event=='PRE':
                if name in names or pending:raise ValueError('duplicate or nested fixed call')
                index=len(names);names.append(name);pending[name]=index
                save('CALL_%02d_PRE.json'%index,{'name':name,'inputs':value})
            elif event=='RETURN':
                if name not in pending:raise ValueError('return without preinput')
                index=pending[name]
                save('CALL_%02d_RETURN.json'%index,{'name':name,'actual':value})
                del pending[name]
            else:raise ValueError('unknown audit event')
        result=module['proposed_controls'](tolerance=1e-9,audit=audit)
        if pending:raise ValueError('unfinished call')
        save('RESULTS.json',result)
        save('FINISH.json',{'status':'AWAITING_DISTINCT_SAVED_CHECKER',
            'call_names':names,'call_count':len(names),'native_motion_release':False,
            'producer_check_flag':result['all_method_checks'],
            'resource_acceptance':'EXTERNAL_ROOT_SUPERVISOR_REQUIRED'})
        return 0 if result['all_method_checks'] else 1
    except BaseException as error:
        save('FAILURE.json',{'exception':type(error).__name__,'message':str(error)})
        raise


if __name__=='__main__':
    raise SystemExit(main())
