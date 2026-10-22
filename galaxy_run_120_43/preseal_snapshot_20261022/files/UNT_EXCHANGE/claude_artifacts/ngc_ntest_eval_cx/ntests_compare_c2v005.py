"""Final entry point: audit all records, honoring defective-before-missing precedence (0512)."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ntests_compare_c2v004 as A
from ntests_compare_c2v002 import compare

def evaluate_manifest(path):
    try:records=A.P.read_manifest(path)
    except FileNotFoundError as e:return dict(outcome='N_INCOMPLETE',tests_read=False,pending=[str(e)])
    except Exception as e:return dict(outcome='N_NO_RUN',tests_read=False,defects=[str(e)])
    structural=compare(records)
    if structural['outcome']=='N_NO_RUN':return structural
    defects=[];pending=list(structural.get('pending',[]))
    for n,r in records.items():
        try:A.audit({n:r})
        except FileNotFoundError as e:pending.append(n+': '+str(e))
        except Exception as e:defects.append(n+': '+str(e))
    if defects:return dict(outcome='N_NO_RUN',tests_read=False,defects=defects,pending=pending)
    if pending:return dict(outcome='N_INCOMPLETE',tests_read=False,pending=pending)
    return structural

if __name__=='__main__':
    r=evaluate_manifest(sys.argv[1]);dest=Path(sys.argv[2])
    if not dest.resolve().is_relative_to(A.ROOT):raise SystemExit('OUTPUT_SCOPE')
    with dest.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
    print(r['outcome'],flush=True)
