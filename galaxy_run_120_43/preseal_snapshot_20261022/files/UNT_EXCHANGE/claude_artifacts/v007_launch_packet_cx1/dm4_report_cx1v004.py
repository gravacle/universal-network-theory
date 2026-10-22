"""Report existing D_m4 diagnostics; missing data remains unavailable, never zero.
RUN LABEL OUTPUT. No source solve, targets or run launches.
"""
import hashlib,json,sys
from pathlib import Path
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).parent))
    import producer_guard_cx1v003 as guard
    guard.authorize(sys.argv,'run')
    run,label,out=sys.argv[1:];p=Path(run)/'result.json';r=json.loads(p.read_bytes())
    h=(r.get('residual_diagnostics') or {}).get('azimuthal_harmonics') or {};rs=h.get('radial_nodes_m');per=h.get('per_radius_max')
    ok=isinstance(rs,list) and isinstance(per,list) and len(rs)==len(per) and len(rs)>0 and all('m4' in x for x in per)
    rec={'schema':'UNT_V007_DM4_REPORT_CX1V001','case':label,'producer':pin(Path(__file__)),'result':pin(p),'label':'TESTED extraction',
         'status':'REPORTED' if ok else 'UNAVAILABLE','quantity':h.get('quantity'),
         'radial_nodes_m':rs if ok else None,'D_m4':[x['m4'] for x in per] if ok else None}
    with open(out,'x') as f:json.dump(rec,f,indent=1)
    print(label,rec['status'])
