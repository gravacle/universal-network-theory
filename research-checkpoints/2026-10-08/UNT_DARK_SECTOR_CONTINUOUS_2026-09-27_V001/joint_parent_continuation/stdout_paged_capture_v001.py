"""Lossless stdout paging for one unchanged small scientific command; no files written."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
source = Path(sys.argv[1]).resolve(strict=True)
if source.parent != Path(__file__).resolve().parent:
    raise RuntimeError('Only a producer in this exact packet may be captured')
sys.argv = [str(source), *sys.argv[2:]]
buffer = io.StringIO()
code = 0
with contextlib.redirect_stdout(buffer):
    try:
        runpy.run_path(str(source), run_name='__main__')
    except SystemExit as stopped:
        code = stopped.code or 0
        if not isinstance(code, int):
            raise
raw = buffer.getvalue()
digest = hashlib.sha256(raw.encode()).hexdigest()
width = 32768
pages = max(1, (len(raw) + width - 1) // width)
for index in range(pages):
    print(json.dumps(dict(kind='unt_stdout_page', index=index, pages=pages,
        stdout_sha256=digest, characters=len(raw), producer_exit_code=code,
        data=raw[index*width:(index+1)*width]), separators=(',', ':')), flush=True)
    if index + 1 < pages:
        if input().strip() != 'NEXT':
            raise RuntimeError('Exact NEXT acknowledgment required; remaining stdout not emitted')
sys.exit(code)
