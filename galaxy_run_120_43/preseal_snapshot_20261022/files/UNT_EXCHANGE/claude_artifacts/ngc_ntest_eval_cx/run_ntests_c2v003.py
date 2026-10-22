"""Design NE5 public runner. Verifies frozen build pins; allows only the two replay evaluators.
Usage: run_ntests_c2v003.py ringeval_uvt_c2v003.py|sphere_eval_uvt_c2v003.py ARGS...
"""
import json,runpy,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ALLOWED=('ringeval_uvt_c2v003.py','sphere_eval_uvt_c2v003.py')
if __name__=='__main__':
    tool=sys.argv[1]
    if tool not in ALLOWED:raise SystemExit('REPLAY_TOOL_NOT_ALLOWED')
    pins=json.loads((HERE/'CODE_PINS_V001.json').read_text())
    for name,want in pins.items():
        p=HERE/name
        if not p.resolve().is_relative_to(HERE) or hashlib.sha256(p.read_bytes()).hexdigest()!=want:raise SystemExit('BUILD_PIN_MISMATCH '+name)
    sys.path.insert(0,str(HERE));sys.argv=[str(HERE/tool)]+sys.argv[2:];runpy.run_path(str(HERE/tool),run_name='__main__')
