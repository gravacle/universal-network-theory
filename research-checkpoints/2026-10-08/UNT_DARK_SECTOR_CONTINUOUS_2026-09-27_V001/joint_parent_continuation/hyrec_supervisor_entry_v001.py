"""Pinned entry for lossless stdout paging; no output-file writes."""
import hashlib
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
source = Path(__file__).resolve().parent / 'hyrec_inputs_v001' / 'hyrec_full_supervisor_v001.py'
expected = '3c491288b8803dc001f6de7794df66be03d1c59ea65fa829aa3870a3f9f55800'
if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
    raise RuntimeError('Reviewed supervisor source changed')
sys.argv = [str(source), *sys.argv[1:]]
runpy.run_path(str(source), run_name='__main__')
