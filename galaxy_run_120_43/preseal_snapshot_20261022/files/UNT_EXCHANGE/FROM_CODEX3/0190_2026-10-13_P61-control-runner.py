"""Source only. Root runs with independently reviewed external supervisor.
No arbitrary inputs; fixed 8-dimensional method fixtures, three times, single process.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SOURCE = Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0189_2026-10-13_P61-coherent-probe-method-source-v002.py')
PIN = '9a1af0dfb23bfdef9151d89500500460676b7a603c5ea3ffa876022ca92223a9'


def encode(x):
    if isinstance(x,complex):
        return {"real":x.real,"imag":x.imag}
    if isinstance(x,dict):
        return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [encode(v) for v in x]
    if x is None or type(x) in (str,int,float,bool):
        return x
    raise TypeError(type(x).__name__)


def save(directory,name,data):
    with (directory/name).open('x') as f:
        json.dump(encode(data),f,indent=2,allow_nan=False)
        f.write('\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest()!=PIN:
        raise ValueError('source pin mismatch')
    args.output.mkdir(exist_ok=False)
    save(args.output,'START.json',{
        'utc':datetime.now(timezone.utc).isoformat(),
        'source':str(SOURCE),'source_sha256':PIN,
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'FRESH_MANUFACTURED_P61_METHOD_ONLY',
        'native_scoring_release':False,
        'controls_tolerance':1e-9,'valid_dimensions':[8],
        'time_count':3,'generic_time_cap':32})
    try:
        with (args.output/'SOURCE_SNAPSHOT.py').open('xb') as f:
            f.write(source)
        module={'__name__':'p61_reviewed_method','__file__':str(SOURCE)}
        exec(compile(source,str(SOURCE),'exec'),module)
        result=module['proposed_probe_controls'](tol=1e-9)
        save(args.output,'RESULTS.json',result)
        save(args.output,'FINISH.json',{
            'utc':datetime.now(timezone.utc).isoformat(),
            'status':'AWAITING_DISTINCT_SAVED_OUTPUT_CHECK',
            'producer_method_checks':result['all_method_checks'],
            'native_scoring_release':False,
            'resource_evidence':'EXTERNAL_SUPERVISOR_REQUIRED'})
        return 0 if result['all_method_checks'] else 1
    except Exception as error:
        save(args.output,'FAILURE.json',{'exception':type(error).__name__,'message':str(error)})
        raise


if __name__=='__main__':
    raise SystemExit(main())
