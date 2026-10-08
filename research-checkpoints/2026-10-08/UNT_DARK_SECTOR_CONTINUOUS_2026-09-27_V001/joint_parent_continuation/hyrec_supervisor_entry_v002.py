"""Pinned additive supervisor entry for lossless stdout paging."""
import hashlib
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
source = Path(__file__).resolve().parent / 'hyrec_inputs_v001' / 'hyrec_full_supervisor_v002.py'
expected = '7884b0d55beb131b285753ec4144f3d5851b9f6a5235d0af18d026ad359fde13'
if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
    raise RuntimeError('Reviewed additive supervisor source changed')
sys.argv = [str(source), *sys.argv[1:]]
runpy.run_path(str(source), run_name='__main__')
