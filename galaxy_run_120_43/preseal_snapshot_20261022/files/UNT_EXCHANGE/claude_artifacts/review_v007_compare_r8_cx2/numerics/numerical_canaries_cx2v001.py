"""Independent synthetic r8 noise and R-PAIR canaries; no scientific run or context builder."""
import argparse, copy, hashlib, importlib.util, json, math, os, resource, sys, time
from fractions import Fraction as F
from pathlib import Path

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
CTRL = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
TARGET = ART/'v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py'
EXPECTED = 'bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
SOURCES = [TARGET, ART/'v007_compare_c2/r8/tests_kmax_tail_compare_c2v007_r8.py',
 ART/'v007_compare_c2/r8/FIELDS_R8.md', ART/'v007_compare_c2/r8/COMPARE_V007_IMPL_R8.md',
 ART/'v007_final_prereg_c4/r2/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json',
 ART/'v007_final_prereg_c4/r2/CLAUSE_SOURCE_MAP.md',
 CTRL/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
 CTRL/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md',
 Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0558_2026-10-18_codex2_crosslineage_review_compare_r8.md'),
 Path(__file__)]

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, x):
    with Path(p).open('x') as f: json.dump(x, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')

def audit(event, args):
    if event.startswith(('subprocess.', 'socket.', 'os.system', 'os.exec', 'os.spawn')):
        raise RuntimeError('NO_LAUNCH_OR_NETWORK:'+event)
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if '/runs_ext/' in p or '/.codex/sessions/' in p or 'KMAX_A2F10_C5H_RUN' in p:
            raise RuntimeError('PROHIBITED_READ:'+p)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--date-u',required=True)
    ar=ap.parse_args(); out=Path(ar.out); out.mkdir(exist_ok=False)
    start=time.monotonic(); sys.addaudithook(audit)
    pins_before=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in SOURCES]
    assert pins_before[0]['sha256']==EXPECTED
    ms=importlib.util.spec_from_file_location('reviewed_r8_noise',TARGET); M=importlib.util.module_from_spec(ms); ms.loader.exec_module(M)
    ids=['SYNTH_ROW_%02d'%i for i in range(12)]
    tau={i:1.0 for i in ids}; ctx={'ids':ids,'tau':tau,'sigma':{i:2.0 for i in ids}}
    results=[]; saved={}
    def check(name, ok, detail=None):
        results.append({'name':name,'pass':bool(ok),'detail':detail})
    def run(increments, scale=1.0, base=0.0):
        cur={i:float(base) for i in ids}; rows=[dict(cur)]
        for inc in increments:
            vals=inc if isinstance(inc,list) else [inc]*12
            cur={i:cur[i]+float(vals[j])*scale for j,i in enumerate(ids)}; rows.append(dict(cur))
        return {'present':True,'pass_rows':rows,'adapted':{'rows':dict(rows[-1])}}
    def oracle(r, tt=tau):
        # Independent exact rational arithmetic on the represented row bytes, no target helpers.
        rows=r['pass_rows'][-4:]
        if len(rows)<2: return None,'NO_INCREMENT'
        inc=[[F(rows[k][i])-F(rows[k-1][i]) for i in ids] for k in range(1,len(rows))]
        norms=[max(abs(x)/F(tt[i]) for i,x in zip(ids,d)) for d in inc]
        if len(inc)==1: return {i:F(tt[i])*norms[-1] for i in ids},None
        ratios=[]
        for a,b in zip(norms,norms[1:]):
            if a==0 and b>0:return None,'NORM_GE1'
            ratios.append(b/a if a else F(0))
        if any(q>=1 for q in ratios):return None,'NORM_GE1'
        q=max(ratios); ans={}
        for j,i in enumerate(ids):
            previous,current=inc[-2][j],inc[-1][j]
            norm=F(tt[i])*norms[-1]*q/(1-q)
            if current==0: row=F(0)
            elif previous==0 or abs(current)>=abs(previous):return None,'ROW_GE1'
            else:
                qi=abs(current/previous)
                same=(current>0)==(previous>0)
                row=abs(current)*qi/(1-qi if same else 1+qi)
            ans[i]=max(norm,row)
        return ans,None
    def compare(name,r,extra=None):
        e,c,d=M.picard_noise_detail(r,ids,tau); oe,oc=oracle(r)
        codes={'NO_INCREMENT':M.E_UNAVAILABLE,'NORM_GE1':M.E_UNAVAILABLE_NONCONTRACTING,'ROW_GE1':M.E_UNAVAILABLE_ROW_RATIO}
        ok=(c==codes.get(oc)) and ((oe is None and e is None) or (oe is not None and all(math.isclose(e[i],float(oe[i]),rel_tol=2e-13,abs_tol=0.0) for i in ids)))
        if extra:ok=ok and extra(e,c,d)
        check(name,ok,{'code':c,'oracle_code':oc,'E':e,'detail':d}); saved[name]=r
        return e,c,d
    compare('uncapped_norm_q_31_32',run([1,F(31,32),F(961,1024)]),lambda e,c,d:d['q']==31/32 and min(e.values())>28)
    mixed=run([[1,F(1,16)]+[0]*10,[F(1,4),F(31,512)]+[0]*10,[F(1,16),F(961,16384)]+[0]*10],scale=1/16)
    compare('uncapped_same_sign_hidden_by_fast_norm',mixed,lambda e,c,d:ids[1] in d['rows_where_per_row_bound_exceeds_norm_bound'] and e[ids[1]]>1/16)
    alt=run([[1,F(1,1024)]+[0]*10,[F(1,128),F(31,32768)]+[0]*10,[F(1,16384),-F(961,1048576)]+[0]*10])
    compare('alternating_hidden_by_fast_norm',alt,lambda e,c,d:ids[1] in d['rows_where_per_row_bound_exceeds_norm_bound'] and d['per_row_bound_kind'][ids[1]]=='ALTERNATING')
    compare('NEW7_earlier_ratio_ge1_last_contracting',run([F(1,2),1,F(1,4)]))
    compare('NEW7_last_ratio_ge1',run([1,F(1,2),F(1,2)]))
    compare('row_ratio_one_same_sign',run([[1,F(1,16)]+[0]*10,[F(1,2),F(1,16)]+[0]*10]))
    compare('row_ratio_one_alternating',run([[1,F(1,16)]+[0]*10,[F(1,2),-F(1,16)]+[0]*10]))
    compare('row_zero_previous_nonzero_last',run([[1,0]+[0]*10,[F(1,2),F(1,16)]+[0]*10]))
    compare('last_row_zero',run([[1,F(1,16)]+[0]*10,[F(1,2),0]+[0]*10]))
    compare('all_zero_ratio_zero',run([0,0,0]),lambda e,c,d:all(x==0 for x in e.values()))
    compare('one_increment_norm_bound',run([[F(1,16),F(1,64)]+[0]*10]),lambda e,c,d:all(x==1/16 for x in e.values()))
    compare('one_pass_unavailable',run([]))
    # Deterministic distinct histories: dyadic q, mixed signs, unequal tau, and moving norm dominance.
    for j in range(32):
        inc=[]
        for k in range(3):
            inc.append([F((n%3)+1,64)*F(2+(j+n)%5,8)**k*((-1)**k if (j+n)%3==0 else 1) for n in range(12)])
        compare('rational_history_%02d'%j,run(inc))
    good=run([F(1,64),F(1,128),F(1,256)])
    vzero={c:{'_uvt_info':{'E_A_rows_km_s':[0.0]*12}} for c in ('C4T','C6T')}
    def pn(a,b,vs=None,ea=None,context=ctx):return M.pair_noise('C4T','C6T',{'C4T':a,'C6T':b},vs or vzero,ea,context)
    for name,change,code in [('gap',lambda r:r.update(pass_rows_gap={'synthetic':True}),M.PASS_ROW_GAP),
       ('S9',lambda r:r.update(pass_rows_s9='SYNTH_S9'), 'SYNTH_S9'),
       ('missing_row',lambda r:r['pass_rows'][1].pop(ids[0]),'PASS_ROWS_NONFINITE_OR_MISSING'),
       ('nonfinite',lambda r:r['pass_rows'][1].update({ids[0]:math.nan}),'PASS_ROWS_NONFINITE_OR_MISSING'),
       ('final_mismatch',lambda r:r['adapted']['rows'].update({ids[0]:2.0}),'FINAL_ROWS_NOT_LAST_PASS_ROWS')]:
        r=copy.deepcopy(good); change(r); e,c,d=M.picard_noise_detail(r,ids,tau); nz=pn(r,good)
        check('record_'+name,c==code and nz['decidable'] is (False if name=='gap' else None),{'code':c,'pair':nz})
    edge=run([1/16]); above=run([math.nextafter(1/16,math.inf)])
    check('pair_threshold_equality',pn(edge,edge)['decidable'] is True)
    check('pair_threshold_next_float',pn(above,above)['decidable'] is False)
    check('slow_same_sign_forces_RPAIR',pn(mixed,mixed)['rpair_branch']=='PICARD' and pn(mixed,mixed)['decidable'] is False,pn(mixed,mixed))
    va={c:{'_uvt_info':{'E_A_rows_km_s':[.125]+[0]*11}} for c in vzero}
    check('EA_dominates_worst_row_route_a',pn(good,good,va)['rpair_branch']=='ROUTE_A')
    tie={c:{'_uvt_info':{'E_A_rows_km_s':[.125]*12}} for c in vzero}
    tie_run=run([.125]); check('branch_exact_tie_picard',pn(tie_run,tie_run,tie)['rpair_branch']=='PICARD')
    check('unavailable_forces_picard_even_huge_EA',pn(run([]),good,tie)['rpair_branch']=='PICARD')
    check('EA_absent_is_unknown',M.pair_noise('C4T','C6T',{'C4T':good,'C6T':good},{},None,ctx)['decidable'] is None)
    vt={c:{'_uvt_info':{'E_A_rows_km_s':[.125,1.0]+[0]*10}} for c in vzero}
    ctw=dict(ctx,tau={i:(.125 if j==0 else 4.0) for j,i in enumerate(ids)})
    nz=pn(run([0]),run([0]),vt,context=ctw)
    check('branch_uses_normalized_worst_not_absolute',nz['rpair_branch_row']==ids[0],nz)
    # Own persisted manifests and protocol reads; no main/context builder or scientific records.
    manifest={'schema':M.MANIFEST_SCHEMA,'cases':{},'identity_runs':{},'gates':{},'rpair':{'T1_H':{'branch':'PICARD','members':{'C4T':'SYNTH_C4T','C6T':'SYNTH_C6T'}}},'note':'Independent numerical synthetic fixture; no scientific run.'}
    write(out/'manifest_picard.json',manifest); check('manifest_picard_load',M.load_manifest(out/'manifest_picard.json')==manifest)
    badm=copy.deepcopy(manifest);badm['rpair']={'RB_FP':{'branch':'ROUTE_A','members':{'C4T':'SYNTH_C4T','C4T-A':'SYNTH_A'}}};write(out/'manifest_rb_wrong_branch.json',badm)
    refused=False
    try:M.load_manifest(out/'manifest_rb_wrong_branch.json')
    except M.Refused:refused=True
    check('RB_FP_route_a_branch_manifest_refused',refused)
    R={'C4T':mixed,'C6T':mixed};RP={'T1_H':{'branch':'PICARD','_runs':{'C4T':good,'C6T':good}}}
    RPV={c+'@RPAIR:T1_H':dict(vzero[c],valid_all=True) for c in vzero}
    def pair(RP_=RP,RPV_=RPV,flags=lambda x:False):return M.evaluate_pair_test('T1_H',R,vzero,RP_,RPV_,flags,{},ctx,.5,True)
    check('trigger_missing_members_pending',pair({})['status']=='RPAIR_PENDING')
    check('clean_picard_pair_reads_member_rows',pair()['status']=='PASS' and pair()['source']=='RPAIR')
    wrong=copy.deepcopy(RP);wrong['T1_H']['branch']='ROUTE_A';check('wrong_branch_incomplete',pair(wrong)['status']=='INCOMPLETE')
    inv=copy.deepcopy(RPV);inv['C4T@RPAIR:T1_H']['valid_all']=False;check('invalid_member_incomplete',pair(RPV_=inv)['status']=='INCOMPLETE')
    floor=copy.deepcopy(RP);floor['T1_H']['_runs']={'C4T':mixed,'C6T':mixed};check('unresolved_member_iteration_floor',pair(floor)['status']=='UNDECIDABLE_AT_ITERATION_FLOOR')
    gap=copy.deepcopy(RP);gap['T1_H']['_runs']['C4T']['pass_rows_gap']={'synthetic':True};check('member_gap_incomplete',pair(gap)['status']=='INCOMPLETE')
    check('picard_base_flag_retained',pair(flags=lambda x:x=='C4T')['status']=='PASS_FLAGGED')
    check('picard_member_only_flag_not_substituted',pair(flags=lambda x:'@RPAIR:' in x)['status']=='PASS')
    untr=M.rpair_untriggered(RP,{'C4T':good,'C6T':good},vzero,{},ctx);check('untriggered_pair_detected',untr==['T1_H'])
    check('triggered_pair_not_untriggered',M.rpair_untriggered(RP,R,vzero,{},ctx)==[])
    eag={'status':'PASS','_record_json':{'per_case':{'C4T':{'E_A_rows_km_s':[1]*12,'result_sha256':'a'*64},'C4T@RPAIR:T1_H':{'E_A_rows_km_s':[0]*12,'result_sha256':'b'*64}}}}
    check('PICARD_EA_substitution_rejected',M.picard_ea_entry_code(eag,'C4T@RPAIR:T1_H')==M.PICARD_EA_ENTRY_CODE)
    check('PICARD_EA_view_retains_base',M._rpair_ea_view(eag,'T1_H',True)['_record_json']['per_case']['C4T']['E_A_rows_km_s']==[1]*12)
    # RB_FP independent arithmetic and unavailable path.
    gates={'EPS':{'status':'PASS','derived':{'eps_max':1/1024}},'RB_FP':{'status':'PASS','_record_json':{'eps_max':1/1024,'shells':['SYNTH_S1','SYNTH_S2'],'dV_static_shells_km_s':{'SYNTH_S1':[2]*12,'SYNTH_S2':[-1]*12}}}}
    rbR={'C4T':good,'C4T-A':good}; rb=M.rb_fp(rbR,gates,ctx,lambda x:False)
    E=oracle(good)[0][ids[0]];expected=float(F(2,1024)*(2*E)/F(.05)*3)
    check('RB_FP_noise_and_kappa_oracle',rb['status']=='PASS' and all(math.isclose(v['RB_FP_km_s'],expected,rel_tol=2e-15) and v['kappa']==3 for v in rb['rows'].values()),rb)
    rbBad={'C4T':run([]),'C4T-A':good};check('RB_FP_unavailable_pending',M.rb_fp(rbBad,gates,ctx,lambda x:False)['status']=='RPAIR_PENDING')
    rbRP={'RB_FP':{'branch':'PICARD','_runs':rbR}}; rbV={c+'@RPAIR:RB_FP':{'valid_all':True} for c in rbR}
    rb=M.rb_fp(rbBad,gates,ctx,lambda x:False,rbRP,rbV);check('RB_FP_resolved_from_own_members',rb['status']=='PASS' and rb['source']=='RPAIR')
    unresolved=copy.deepcopy(rbRP);unresolved['RB_FP']['_runs']['C4T']=run([]);check('RB_FP_unresolved_incomplete',M.rb_fp(rbBad,gates,ctx,lambda x:False,unresolved,rbV)['status']=='INCOMPLETE')
    zeroG=copy.deepcopy(gates);zeroG['RB_FP']['_record_json']['dV_static_shells_km_s']['SYNTH_S2']=[-2]*12
    check('RB_FP_zero_shell_sum_incomplete',M.rb_fp(rbR,zeroG,ctx,lambda x:False)['status']=='INCOMPLETE')
    check('RB_FP_available_base_untriggered',M.rpair_untriggered(rbRP,rbR,{},gates,ctx)==['RB_FP'])
    # Full actual case_validity, synthetic records; only V4/V5/I1T are explicit protocol seams.
    num={'picard':{'passes':4,'speed_change_bound_km_s':.0125,'observe_every_pass':True},'brackets':{'synthetic':True},'composite_grid_spec':'SYNTH_G4','truncation':{'shape':'cube','kmax_inverse_kpc':None},'route_a':{'max_iterations':32,'column_workers':8},'uv_tail':{'source_rule':{'rule':'continuum_v001'},'enabled':True}}
    ns={'galaxy':'SYNTH_DDO154','physical':{'synthetic':1},'coefficients':{'synthetic':2},'numerics':num}
    driver=M.PIN_DRIVER[1] if hasattr(M,'PIN_DRIVER') else 'd'*64
    reg={'drivers_allowed':[driver],'tail':True,'ro1_required':True,'normalized_spec_equal':{'/numerics':copy.deepcopy(num)},'uv_tail_config_sha256':'c'*64}
    vctx=dict(ctx,case_block={'cases':{'C4T':reg},'key_equivalence_map':{}},anchor=dict(ns,picard=copy.deepcopy(num['picard'])),ra4_block=num['brackets'],grids={'G4':'SYNTH_G4'},route_a_mode='parallel8',tau_picard=.0125,row_radii_m=list(range(1,13)))
    validrun=run([F(1,512),F(1,1024),F(1,2048)])
    result={'schema':M.RESULT_SCHEMA,'status':'COMPLETED','driver_sha256':driver,'call_spec_sha256':'s'*64,'normalized_spec':ns}
    raw=canonical_bytes=json.dumps(result,sort_keys=True).encode(); resultsha=hashlib.sha256(raw).hexdigest()
    resultpath=str(out/'synthetic_result.json')
    with Path(resultpath).open('xb') as f:f.write(raw)
    validrun.update(result=result,result_sha256=resultsha,result_path=resultpath,adapted_sha_equal=True,raw_row_ids=ids,read_codes=[],finish={'result_sha256':resultsha},receipt={'schema':M.RECEIPT_SCHEMA,'result':{'path':resultpath,'sha256':resultsha},'pins':{'spec':{'sha256':'s'*64},'driver':{'sha256':driver}},'driver_status':'COMPLETED','status':'FINISHED','exit_code':0,'stop_reason':None},route_a_outcome={'classification':'CONVERGED','converged_iteration':3,'result_sha256':'a'*64,'ro1':{'rule':'RO1','fired':False,'events':[],'armed':True,'worker_sha256':M.PIN_RO1_CUSTODY['worker_parallel'][1],'binding_sha256':M.PIN_RO1_CUSTODY['binding'][1]}},uvt_record={'schema':M.UVT_RA_RECORD_SCHEMA,'outcome':'CONVERGED_FINITE_FIXED_POINT','production_admissible':True,'admissibility':'production','config_sha256':'c'*64,'flags':[],'monitor_status':'M_T_WITHIN_THRESHOLD','M_T_threshold':.25,'M_T_accepted':0.0,'accepted_iteration':3,'E_A_rows_km_s_accepted':[0.0]*12,'probe_R_m':list(range(1,13))})
    validrun['adapted'].update(schema=M.RESULT_SCHEMA,status='COMPLETED',valid=True,last_change_km_s=1/2048,route_a_identity_sha256='b'*64)
    member=copy.deepcopy(validrun);member['result']['normalized_spec']['numerics']['route_a']['column_workers']=1;member['result']['normalized_spec']['numerics']['picard']=copy.deepcopy(M.RPAIR_PICARD)
    key='C4T@RPAIR:T1_H';par={'base':'C4T','branch':'PICARD','base_run':validrun}
    def validity(r=member,p=par):return M.case_validity(key,r,vctx,packet={'V4':True,'V5':True},i1t={'status':'PASS','per':{key:'PASS'}},rpair=p)
    vv=validity();check('R3_4_parallel_base_planning_one_positive',vv['valid_all'] and vv['ro1']['worker_kind_from']=='ADMITTED_BASE_ATTEMPT_A53_R3_4',vv)
    for name,mut,code in [('serial_worker_substitution',lambda r:r['route_a_outcome']['ro1'].update(worker_sha256=M.PIN_RO1_CUSTODY['worker'][1]),'RPAIR_PICARD_MEMBER_RO1_RECORD_NOT_THE_BASE_RECORD_A53_R3_4'),('different_base_result',lambda r:r['route_a_outcome'].update(result_sha256='e'*64),'V6_ROUTE_A_OUTCOME_RESULT_SHA256_NOT_THE_BASE_A53'),('different_base_identity',lambda r:r['adapted'].update(route_a_identity_sha256='f'*64),'V6_ROUTE_A_IDENTITY_NOT_THE_BASE_IDENTITY'),('tail_record_substitution',lambda r:r['uvt_record'].update(M_T_accepted=.1),'V6_ROUTE_A_TAIL_RECORD_NOT_THE_BASE_RECORD'),('unregistered_numerics_drift',lambda r:r['result']['normalized_spec']['numerics'].update(synthetic_unauthorized=True),'RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES')]:
        r=copy.deepcopy(member);mut(r); vv=validity(r); allcodes=vv.get('V3_mismatch',[])+vv.get('V6_codes',[]);check('R3_4_'+name,not vv['valid_all'] and any(code in c for c in allcodes),vv)
    route=copy.deepcopy(validrun);route['result']['normalized_spec']['numerics']['route_a']['seed_source_rtol_factor']=.1
    vv=validity(route,{'base':'C4T','branch':'ROUTE_A','base_run':validrun});check('route_a_branch_cannot_reuse_identity',not vv['valid_all'] and any('NOT_RECOMPUTED' in c for c in vv['V3_mismatch']),vv)
    write(out/'synthetic_histories.json',saved)
    write(out/'synthetic_rpair_records.json',{'context':vctx,'base':validrun,'member':member,'explicit_seams':{'packet_V4_V5':'asserted synthetic True, not computed','I1T':'asserted synthetic PASS, not computed','scientific_adoption':'UNTESTED'}})
    pins_after=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in SOURCES]
    check('review_target_unchanged',sha(TARGET)==EXPECTED)
    report={'schema':'UNT_CX2_R8_NUMERICAL_CANARIES_V001','date_u':ar.date_u,'label':'TESTED_SYNTHETIC_ONLY','sealed_or_scientific_adoption':'UNTESTED','pass':all(r['pass'] for r in results),'passed':sum(r['pass'] for r in results),'total':len(results),'tests':results,'pins_before':pins_before,'pins_after':pins_after,'open_addendum_changed':pins_before[-3]!=pins_after[-3],'runtime_seconds':time.monotonic()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'resource_contract':{'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'BLAS_threads':os.environ.get('OPENBLAS_NUM_THREADS'),'priority':'default under dispatch 0514 waiver','launches':0},'limits':['No build_context, real input records, external runs, solver, full CLI or global adoption evaluation.','The comparator module is imported unmodified; no monkeypatches.','Independent Fraction oracle operates on actual represented synthetic row values.','case_validity positive controls assert synthetic V4/V5/I1T seams; these establish only R3-4/V6 protocol behavior.']}
    write(out/'NUMERICAL_CANARIES_CX2V001.json',report)
    print(json.dumps({'passed':report['passed'],'total':report['total'],'pass':report['pass'],'failed':[r for r in results if not r['pass']],'runtime_seconds':report['runtime_seconds'],'peak_rss_bytes':report['peak_rss_bytes'],'report_sha256':sha(out/'NUMERICAL_CANARIES_CX2V001.json')},allow_nan=False))
    return 0 if report['pass'] else 1

if __name__=='__main__':raise SystemExit(main())
