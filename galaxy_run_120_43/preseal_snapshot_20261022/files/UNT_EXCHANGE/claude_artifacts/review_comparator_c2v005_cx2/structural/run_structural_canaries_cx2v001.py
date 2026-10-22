"""Own c2v005 structural canaries. Run only with the final candidate pin supplied."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_structural_support',HERE/'common_structural_cx2v002.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
ap=argparse.ArgumentParser()
ap.add_argument('--comparator',required=True)
ap.add_argument('--sha256',required=True)
a=ap.parse_args()
candidate=Path(a.comparator).resolve()
cmp=C.load(candidate,'_ind_c2v005_structural',a.sha256)
cm=C.load(cmp.CKPT[0],'_ind_structural_checkpoint',cmp.CKPT[1])
reference_path=str(C.ART/'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py')
reference=(reference_path,cmp.REFERENCE_DRIVERS[reference_path])
new=tuple(cmp.DRIVER)
run=C.OUT/('run_'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'_%d'%os.getpid())
run.mkdir()
cases=[
 ('P01_tiny_full_saved_tree','PASS',None,None,False,False,'Independent scratch fixture; no old checker tree copied.'),
 ('P02_result_object_key_order','PASS',None,None,True,False,'Whole result object order varies; old order case was a stage JSON.'),
 ('P03_result_ended_clock','PASS',None,'result_clock_only',False,False,'Full result comparator must retain the declared ended-time mask.'),
 ('P04_equal_nested_input_extension','PASS',None,None,False,True,'Equal additional input filename and nested contents on both sides.'),
 ('F01_collision_earlier_partial_body','FAIL',None,'duplicate_body_first',False,False,'Partial extra body before legitimate body; not a copied whole-stage test.'),
 ('F02_collision_later_partial_body','FAIL',None,'duplicate_body_last',False,False,'Partial extra body after legitimate body, testing the opposite winner order.'),
 ('F03_collision_both_sides_equal','FAIL','paired_duplicate_body','paired_duplicate_body',False,False,'Both sides contain identical collisions: ambiguous inventory must still refuse.'),
 ('F04_collision_middle_of_three','FAIL',None,'triple_body_collision',False,False,'Tampered middle alias between equal outer aliases; four total body directories.'),
 ('F05_empty_extra_stage','FAIL',None,'empty_extra_stage',False,False,'An extra empty stage has no files for a file-only inventory to detect.'),
 ('F06_missing_body_stage','FAIL',None,'missing_body',False,False,'A complete required compared stage disappears.'),
 ('F07_renamed_stage_suffix','FAIL',None,'renamed_body',False,False,'Unknown stage suffix preserves files but changes semantic directory name.'),
 ('F08_body_nested_payload','FAIL',None,'body_payload',False,False,'Nested scientific body payload differs.'),
 ('F09_result_unknown_nested_ulp','FAIL',None,'result_nested_pressure',False,False,'Previously unlisted result subtree numeric leaf differs by one ULP.'),
 ('F10_result_unknown_nested_key_removed','FAIL',None,'result_key_removed',False,False,'Unknown nested result-key presence, distinct from old scalar substitutions.'),
 ('F11_result_unknown_nested_key_added','FAIL',None,'result_key_added',False,False,'Additional nested scientific result constraint.'),
 ('F12_input_nested_contract','FAIL',None,'input_nested_contract',False,False,'Nested contract string in independently named input.'),
 ('F13_input_binary_last_byte','FAIL',None,'input_raw_byte',False,False,'Non-JSON input binary bytes; old input probes were JSON.'),
 ('F14_input_binary_missing','FAIL',None,'input_missing_raw',False,False,'Missing non-JSON source input.'),
 ('F15_input_extra_admission','FAIL',None,'input_extra',False,False,'One-side extra admission input; category control, not claimed novel category.'),
 ('F16_finish_nested_residual','FAIL',None,'finish_nested_residual',False,False,'Nested completion measure while status/hash/path remain well formed.'),
 ('F17_finish_failed_status','FAIL',None,'finish_status',False,False,'Contradictory final status with the same completed result.'),
 ('F18_attempt_nested_entropy_ulp','FAIL',None,'attempt_entropy',False,False,'One-ULP attempt scientific scalar; independent field and tree.'),
 ('F19_attempt_subrecord_missing','FAIL',None,'attempt_key_removed',False,False,'Route-A attempt result subrecord removed rather than value changed.'),
]
rows=[]
for name,want,rd,nd,reorder,both_input,unique in cases:
    folder=run/name
    ref=C.build_tree(folder/'REF',reference,cmp,cm,defect=rd,both_input=both_input)
    nxt=C.build_tree(folder/'NEW',new,cmp,cm,defect=nd,reorder=reorder,both_input=both_input)
    tokens=C.write(folder/'TOKENS.json',{'declared':[]})
    report=folder/'REPORT.json';stdout=io.StringIO();code=None;error=None
    try:
        with contextlib.redirect_stdout(stdout):
            code=cmp.main(['--gate','Z2_OFF','--reference',str(ref),'--new',str(nxt),
                '--tokens',tokens['path'],'--out',str(report)])
    except BaseException as exc:
        error={'type':type(exc).__name__,'message':str(exc)}
    rep=json.loads(report.read_bytes()) if report.is_file() else None
    verdict=rep.get('verdict') if isinstance(rep,dict) else None
    if want=='PASS':ok=code==0 and verdict=='PASS_BITWISE_EQUAL' and error is None
    else:ok=code not in (0,None) and verdict=='FAIL' and error is None
    rows.append({'case':name,'expect':want,'pass':ok,'exit_code':code,'verdict':verdict,
        'exception':error,'failing':rep.get('failing') if isinstance(rep,dict) else None,
        'report':C.pin(report) if report.is_file() else None,'uniqueness':unique,'stdout':stdout.getvalue()[:2000]})
summary={'schema':'CX2_C2V005_STRUCTURAL_REVIEW_V001','status':'TESTED','comparator':C.pin(candidate),
    'harness':C.pin(__file__),'support':C.pin(HERE/'common_structural_cx2v002.py'),
    'reference_driver':{'path':reference[0],'sha256':reference[1]},'new_driver':{'path':new[0],'sha256':new[1]},
    'passed':sum(r['pass'] for r in rows),'total':len(rows),'cases':rows,'blocked_attempts':C.BLOCKED,
    'scope':'Synthetic saved-output comparison only. No solver launches or real runs. P/F controls include category overlap explicitly identified.'}
out=C.write(run/'STRUCTURAL_RESULTS.json',summary)
print(json.dumps({'result':out,'passed':summary['passed'],'total':summary['total'],
                  'failed':[r['case'] for r in rows if not r['pass']]}))
