"""Pinned saved-arithmetic collector entry; stdout only."""
import hashlib
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
source = Path(__file__).resolve().parent / 'hyrec_inputs_v001' / 'hyrec_bao_interval_v001.py'
if hashlib.sha256(source.read_bytes()).hexdigest() != 'c35a24011a92462d725824eff0a96bdfca7ae11a5935e462a5dce3f7ce85fdb3':
    raise RuntimeError('Reviewed interval collector changed')
sys.argv = [str(source), *sys.argv[1:]]
runpy.run_path(str(source), run_name='__main__')
