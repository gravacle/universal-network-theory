"""A283 stage-a register publisher. Metadata only; never admits a call or runs science.
Root authenticates the input-document SHA out of band. Referenced pins are opaque
here: the L2_DIRECT native START snapshot authenticates their file bytes before
launch. This writer does not open call roots, specs, captures, or scientific data.
"""
import argparse, hashlib, json, os, stat
from pathlib import Path

ROWS = {28,29,30,31,300,301,302}
PIN_FIELDS = ('spec','launcher','guard','binder','dbp','runtime_capture')
FIELDS = {'row','key','call_root','attempt',*PIN_FIELDS}
class Refusal(ValueError): pass
def need(ok, why):
    if not ok: raise Refusal(why)
def sha(x):
    return type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x)
def absolute(x):
    return type(x) is str and x.startswith('/') and '\x00' not in x and '..' not in Path(x).parts
def pin(x):
    return type(x) is dict and set(x)=={'path','sha256'} and absolute(x['path']) and sha(x['sha256'])
def no_duplicates(pairs):
    obj={}
    for k,v in pairs:
        need(k not in obj,'DUPLICATE_JSON_KEY'); obj[k]=v
    return obj
def validate(obj):
    need(type(obj) is dict and set(obj)=={'schema','entries'} and obj['schema']=='SPECULATIVE_REGISTER_L2_V001','REGISTER_SCHEMA')
    need(type(obj['entries']) is list and len(obj['entries'])==7,'SEVEN_CALLS')
    rows=set(); keys=set(); roots=set(); path_hashes={}
    for e in obj['entries']:
        need(type(e) is dict and set(e)==FIELDS,'ENTRY_SCHEMA')
        need(type(e['row']) is int and e['row'] in ROWS and e['row'] not in rows,'ROW')
        need(sha(e['key']) and e['key'] not in keys,'KEY')
        need(type(e['attempt']) is int and e['attempt']>=1,'ATTEMPT')
        need(absolute(e['call_root']) and e['call_root'] not in roots,'CALL_ROOT')
        need(Path(e['call_root']).name=='DDO154_JACOBIAN_R%d_%s_A%d'%(e['row'],e['key'][:16],e['attempt']),'CALL_ROOT_NAME')
        for f in PIN_FIELDS:
            need(pin(e[f]),'PIN:'+f)
            p=e[f]; need(p['path'] not in path_hashes or path_hashes[p['path']]==p['sha256'],'CONFLICTING_PIN')
            path_hashes[p['path']]=p['sha256']
        rows.add(e['row']);keys.add(e['key']);roots.add(e['call_root'])
    need(rows==ROWS,'ROW_SET')
    return obj
def read_input(path, expected):
    need(absolute(path) and sha(expected),'INPUT_PIN')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        before=os.fstat(fd);need(stat.S_ISREG(before.st_mode),'INPUT_REGULAR')
        need(before.st_size<=1024*1024,'INPUT_TOO_LARGE')
        chunks=[];total=0
        while True:
            b=os.read(fd,65536)
            if not b:break
            chunks.append(b);total+=len(b);need(total<=1024*1024,'INPUT_TOO_LARGE')
        after=os.fstat(fd)
        need(all(getattr(before,k)==getattr(after,k) for k in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns')),'INPUT_CHANGED')
    finally:os.close(fd)
    raw=b''.join(chunks);need(hashlib.sha256(raw).hexdigest()==expected,'INPUT_SHA')
    return validate(json.loads(raw,object_pairs_hook=no_duplicates))
def publish(input_path,input_sha,output):
    obj=read_input(input_path,input_sha)
    need(absolute(output),'OUTPUT_ABSOLUTE')
    raw=(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    # O_EXCL preserves existing files, including dangling symlinks. Parent must exist.
    with open(output,'xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    return {'path':output,'sha256':hashlib.sha256(raw).hexdigest()}
def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',required=True);ap.add_argument('--input-sha256',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args(argv)
    try:
        print(json.dumps(publish(args.input,args.input_sha256,args.output),sort_keys=True));return 0
    except (ValueError,OSError) as e:
        print('REFUSED: '+str(e));return 2
if __name__=='__main__':raise SystemExit(main())
