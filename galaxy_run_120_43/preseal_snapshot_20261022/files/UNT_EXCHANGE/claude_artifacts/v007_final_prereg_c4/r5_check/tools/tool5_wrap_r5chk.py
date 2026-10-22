# tool5_wrap_r5chk.py -- calls seal tool 5 v002 r2 record_bytes() unmodified and writes the printed record by exclusive create.
# usage (under run_fenced_r5chk.py): tool5_wrap_r5chk.py TOOL5.py REVIEWED.py REVIEWED_SHA CHECK_RECORD OUT_RECORD.json
import sys, json, hashlib, importlib.util
t5, rev, rsha, chkrec, outp = sys.argv[1:6]
sys.path.insert(0, __import__('os').path.dirname(t5))
s = importlib.util.spec_from_file_location('print_driver_build_record_c4v002', t5)
T5 = importlib.util.module_from_spec(s); s.loader.exec_module(T5)
res, text = T5.record_bytes(rev, rsha, chkrec)
print(json.dumps(res, indent=1, sort_keys=True))
if text is not None:
    with open(outp, 'x') as f:
        f.write(text)
    print('WROTE', outp, hashlib.sha256(open(outp, 'rb').read()).hexdigest())
sys.exit(0 if text is not None else 2)
