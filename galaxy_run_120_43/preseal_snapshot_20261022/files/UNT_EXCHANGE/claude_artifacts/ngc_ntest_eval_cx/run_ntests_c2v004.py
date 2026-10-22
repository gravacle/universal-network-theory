"""NE5: replay-only case allowlist. Never executes prep/respond/assemble/forward/route-A/route-B.
Usage: run_ntests_c2v001.py CASE OUTPUT [START END]. Existing outputs are refused.
NQ_BASE/NQ_FINE are the NQ pair. N1 uses CUBE16, N2/N4 use SPHERE16 and CUBE16; N3 CUBE8/16/32.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v004 as L
from ringeval_uvt_c2v004 import replay
CASES={'N0':(2.,'cube',False),'CUBE8':(8.,'cube',False),'CUBE16':(16.,'cube',False),
       'CUBE32':(32.,'cube',False),'SPHERE16':(16.,'sphere',False),
       'NQ_BASE':(16.,'cube',False),'NQ_FINE':(16.,'cube',True)}
if __name__=='__main__':
    case,name=sys.argv[1:3]
    if case not in CASES:raise SystemExit('REPLAY_CASE_NOT_ALLOWED')
    dest=L.HERE/name
    if not dest.resolve().is_relative_to(L.HERE.resolve()) or dest.exists():raise SystemExit('OUTPUT_REFUSED')
    bounds=tuple(map(int,sys.argv[3:]))
    if len(bounds) not in (0,2):raise SystemExit('START END required together')
    r=replay(*CASES[case],*bounds);r['case']=case
    print(L.write(name,r),flush=True)
