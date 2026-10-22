"""0558 isolated decision-order controls. Explicit synthetic subordinate statuses, not scientific acceptance."""
import copy
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_ind_priority_support',HERE/'priority_support_cx2v001.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
M=C.M;run=C.run;check=C.check;write=C.write
cb=json.loads((HERE/'run_20261018T153234_27448/CASE_BLOCK.json').read_bytes())
ctx=M.build_context(case_block=cb)
man={'schema':M.MANIFEST_SCHEMA,'cases':{},'identity_runs':{},'gates':{},'rpair':{}}
mp=write(run/'OWN_EMPTY_MANIFEST.json',man)
R,ID,RP,pack=M.read_all(ctx,M.load_manifest(mp['path']),with_packets=False)
gates=M.read_gates(ctx,man,R,ID)
ev=M.evaluate_v007(ctx,R,ID,gates,RP,pack)
check('Actual readers and validators give INCOMPLETE for empty synthetic manifest',
      ev['decision']['outcome']=='INCOMPLETE' and ev['decision']['tests_read'] is False,ev['decision'])

# Boundary isolation: keep the actual evaluate_v007, named/priority/provisional logic,
# flag rulings, cross-label alias checks, uncertainty aggregation, and pending bookkeeping.
# Replace only upstream validity and numerical test producers by transparent statuses.
PATCHED=('case_validity','identity_run_validity','t1_test','evaluate_pair_test','rb_fp','sr_k','srb_rot_readable')
original={k:getattr(M,k) for k in PATCHED}
world={}
def validity(label,run,ctx,*args,**kwargs):
    bad=label in world.get('invalid',[])
    return {'label':label,'present':True,'valid_all':not bad,'failed':['V1'] if bad else [],
            'reading':'SYNTHETIC_INVALID' if bad else None,'V1_codes':['SYNTHETIC_INVALID'] if bad else [],
            'uvt':{'flagged':label in world.get('flags',[])},'ro1':{'fired':False}}
def idvalid(label,run,ctx=None):
    return {'valid':label not in world.get('bad_identity',[]),'codes':[],
            'ro1_codes':[],'ro1_fired':label in world.get('fired_identity',[])}
def unit(name):
    status=world.get('units',{}).get(name,'PASS')
    return {'status':status,'flagged_runs':['C4T'] if status=='UNDECIDABLE_FLAGGED' else [],
            'stat':{'delta_over_tau':{i:world.get('t2c_delta',0.01) for i in ctx['ids']}},'source':'BASE'}
def t1(*args):
    return dict(unit('T1'),floor_like=world.get('floor_like',False),fail_by=['SYNTHETIC_CONTRACTION'],Dhat_2_3=0.1,Dhat_3_4=0.1)
def pair(pid,*args,**kwargs):return unit(pid)
def rb(*args,**kwargs):
    return dict(unit('RB_FP'),rows={i:{'RB_FP_km_s':0.001} for i in ctx['ids']})
def sr(*args,**kwargs):
    return {'status':'PASS','SOURCE_QUADRATURE_MATERIAL':world.get('sqm',False),
            'pairwise_within_quarter_tau':world.get('srk_quarter',True),
            'SR_term_km_s':{i:0.001 for i in ctx['ids']}}
M.case_validity=validity;M.identity_run_validity=idvalid;M.t1_test=t1;M.evaluate_pair_test=pair
M.rb_fp=rb;M.sr_k=sr;M.srb_rot_readable=lambda *a:(not world.get('srb_pending',False),'SYNTHETIC_PENDING')
specimens=[]
def test(name,w,expected,*,provisional=None,tests_read=None,also=None,named=None):
    global world
    world=copy.deepcopy(w)
    RR={label:{'present':True,'result_sha256':C.hashlib.sha256(label.encode()).hexdigest(),
               'adapted':{'rows':{i:50.0 for i in ctx['ids']}}} for label in M.REGISTERED}
    II={label:{'present':True,'result_sha256':C.hashlib.sha256(label.encode()).hexdigest()} for label in M.IDENTITY_RUNS}
    if w.get('alias'):RR['C6T']['result_sha256']=RR['C4T']['result_sha256']
    if w.get('pass_gap'):RR[w['pass_gap']]['pass_rows_gap']='E_UNAVAILABLE_PASS_ROW_GAP'
    GG={g:{'gate':g,'status':'PASS','codes':[],'derived':{}} for g in M.ALL_GATES}
    for g,status in w.get('gates',{}).items():GG[g]['status']=status;GG[g]['codes']=['SYNTHETIC_'+status]
    if w.get('mt_flags'):
        GG['MT']['status']='FAIL';GG['MT']['derived']['mt_failed_runs']=w['mt_flags']
    if w.get('ruling'):
        GG['FLAG_RULINGS']['derived']['rulings']=[{'flag':M.FLAG_TSU,'run':'C4T',
             'disposition':w['ruling'],'root_decision':'INVENTED_TEST_DECISION'}]
    report=M.evaluate_v007(ctx,RR,II,GG)
    dec=report['decision'];ok=dec['outcome']==expected
    if provisional is not None:ok=ok and dec['provisional'] is provisional
    if tests_read is not None:ok=ok and dec['tests_read'] is tests_read
    if also is not None:ok=ok and also in dec.get('also_named',[])
    if named is not None:ok=ok and all(x in dec['named']['next_steps'] for x in named)
    check('Priority unit: '+name,ok,dec)
    specimens.append({'name':name,'world':w,'expected':expected,'observed':dec})

try:
    test('all resolved and unflagged','' if False else {},'ADOPT_TAIL')
    test('invalid base blocks adoption',{'invalid':['C4T']},'INCOMPLETE',tests_read=False)
    test('invalid identity blocks adoption',{'bad_identity':['Z2']},'INCOMPLETE',tests_read=False)
    test('alias blocks adoption',{'alias':True},'INCOMPLETE',tests_read=False)
    test('identity RO1 fired takes NO_RUN',{'fired_identity':['Z2']},'NO_RUN',tests_read=False)
    test('NO_RUN before missing and names all',{'gates':{'B0':'FAIL','GQ':'MISSING'},'invalid':['C4T']},'NO_RUN',tests_read=False,named=['C4T','GQ'])
    test('record defect before missing',{'gates':{'LO':'RECORD_DEFECT','EPS':'MISSING'}},'NO_RUN',tests_read=False,named=['LO','EPS'])
    test('optional record defect also NO_RUN',{'gates':{'HARMONICS':'RECORD_DEFECT'}},'NO_RUN',tests_read=False)
    test('missing required before certificate fail',{'gates':{'I1T':'MISSING','EPS':'FAIL'}},'INCOMPLETE',tests_read=False)
    test('I4 failed parallel admission',{'gates':{'I4':'FAIL'}},'INCOMPLETE',tests_read=False)
    test('numerics certificate fail',{'gates':{'GQ':'FAIL'}},'NUMERICS_UNCERTIFIED',tests_read=False)
    test('lapse certificate fail',{'gates':{'LO':'FAIL'}},'NON_LAPSE_TAIL_MATERIAL',tests_read=False)
    test('both certificate classes named',{'gates':{'EPS':'FAIL','LO':'FAIL'}},'NUMERICS_UNCERTIFIED',tests_read=False,also='NON_LAPSE_TAIL_MATERIAL')
    test('T2I failure before pending T3',{'gates':{'T2I':'FAIL'},'units':{'T3_KLO':'RPAIR_PENDING'}},'IMPLEMENTATION_DEFECT',provisional=False)
    test('T2 failure before pending T3',{'units':{'T2':'FAIL','T3_KHI':'RPAIR_PENDING'}},'IMPLEMENTATION_DEFECT',provisional=False)
    test('T3 failure with earlier T2 pending',{'units':{'T2':'RPAIR_PENDING','T3_KHI':'FAIL'}},'KBIG_NOT_CONVERGED',provisional=True)
    test('T2 failure before source rule failure',{'units':{'T2':'FAIL','T2c':'FAIL'}},'IMPLEMENTATION_DEFECT')
    test('source rule failure before Kbig failure',{'units':{'T2c':'FAIL','T3_KLO':'FAIL'}},'SOURCE_RULE_MATERIAL')
    test('Kbig failure before bound failure',{'units':{'T3_KHI':'FAIL','RB_FP':'FAIL'}},'KBIG_NOT_CONVERGED')
    test('bound failure before undecidable floor',{'units':{'RB_FP':'FAIL','T2':'UNDECIDABLE_AT_ITERATION_FLOOR'}},'BOUND_INSUFFICIENT')
    test('floor-like classification',{'units':{'T1':'FAIL'},'floor_like':True},'FLOOR_LIKE')
    test('T1 residual split with no flags',{'units':{'T1':'FAIL'},'srk_quarter':True},'NOT_UV_RESIDUAL')
    test('T1 K-dependent split',{'units':{'T1':'FAIL'},'srk_quarter':False},'SOURCE_REPRESENTATION_K_DEPENDENT')
    test('higher-K disagreement',{'units':{'T1_H':'FAIL'}},'HIGHER_K_DISAGREEMENT')
    test('shape disagreement',{'units':{'T1_S':'FAIL'}},'SHAPE_DISAGREEMENT')
    test('flagged undecidable before iteration floor',{'units':{'T2':'UNDECIDABLE_FLAGGED','T1_H':'UNDECIDABLE_AT_ITERATION_FLOOR'}},'UNDECIDABLE_ROUTE_A_TAIL',also='UNDECIDABLE_AT_ITERATION_FLOOR')
    test('iteration floor blocks adoption',{'units':{'T2':'UNDECIDABLE_AT_ITERATION_FLOOR'}},'UNDECIDABLE_AT_ITERATION_FLOOR')
    test('pending pair blocks adoption',{'units':{'T3_KLO':'RPAIR_PENDING'}},'INCOMPLETE')
    test('pending pair before unruled flag',{'units':{'T3_KLO':'RPAIR_PENDING'},'flags':['C4T']},'INCOMPLETE')
    test('uncomputed material flag blocks adoption',{'sqm':None},'INCOMPLETE')
    test('SRB prerequisites pending block adoption',{'srb_pending':True},'INCOMPLETE')
    test('B4 gap blocks adoption despite passing unit statuses',{'pass_gap':'C4T'},'INCOMPLETE')
    test('unruled tail flag blocks adoption',{'flags':['C4T']},'FLAG_PENDING_RULING')
    test('MT failed run creates flag',{'mt_flags':['C4T']},'FLAG_PENDING_RULING')
    test('material flag blocks adoption',{'sqm':True},'FLAG_PENDING_RULING')
    test('rerun ordered is not clearance',{'flags':['C4T'],'ruling':'RERUN_ORDERED'},'FLAG_PENDING_RULING')
    test('clearance enables otherwise resolved adoption',{'flags':['C4T'],'ruling':'CLEARED'},'ADOPT_TAIL')
    test('reported optional LO_NGC failure does not decide DDO',{'gates':{'LO_NGC':'FAIL'}},'ADOPT_TAIL')
    test('defensive I1T not passing blocks adoption',{'gates':{'I1T':'FAIL'}},'INCOMPLETE')
finally:
    for k,v in original.items():setattr(M,k,v)
check('Every injected function restored',all(getattr(M,k) is v for k,v in original.items()))
check('Candidate bytes unchanged',C.sha(C.SOURCE)==C.EXPECTED)
check('No forbidden read or process attempted',not C.BLOCKED,C.BLOCKED)
worldpin=write(run/'OWN_DECISION_WORLDS.json',specimens)
res={'status':'TESTED','passed':sum(x['pass'] for x in C.rows),'total':len(C.rows),'rows':C.rows,
     'source_before':{'path':str(C.SOURCE),'sha256':C.EXPECTED},'source_after':C.pin(C.SOURCE),
     'worlds':worldpin,'harness':C.pin(Path(__file__)),'support':C.pin(HERE/'priority_support_cx2v001.py'),
     'scope':'One actual empty-manifest end-to-end reader/validator decision, plus isolated actual evaluate_v007 priority controls with explicit synthetic upstream validity and test producers. ADOPT controls do not establish full record/certificate admission or science.'}
out=write(run/'PRIORITY_RESULTS.json',res)
print(json.dumps({'result':out,'passed':res['passed'],'total':res['total'],'failed':[x['name'] for x in C.rows if not x['pass']]}))
