"""N-test-only compare. R1 thresholds + A17 C1prime + A52 readout-coupled LO.
No galaxy adoption follows this compare. Missing/malformed/unknown data -> INCOMPLETE.
Outcome labels N1_FAIL/N2_FAIL denote precisely the failed registered N statistic, not new physics claims.
N3 ambiguity: also enforce literal |delta(S/theta)| <= theta/4, the stricter reading, pending coordinator ruling.
Input manifest: {record_name:{path,sha256}}, names N0,N1,N2,N3,N4,NQ,LO_NGC,I1T_NGC.
All numerical record values are raw (not rounded), with operator_sha256 and theta custody.
"""
import json,math,sys,hashlib
from pathlib import Path
import numpy as np
THETA=3.3657664138980042e-09
OP_SHA='e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'
SHAPE=(1,2,3,4,5,6,7,8,10,13,14,15)
REQUIRED=('N0','N1','N2','N3','N4','NQ','LO_NGC','I1T_NGC')
OUTCOMES=('INCOMPLETE','IMPLEMENTATION_DEFECT','NON_LAPSE_TAIL_MATERIAL','NUMERICS_UNCERTIFIED',
          'N1_FAIL','SHAPE_DISAGREEMENT','KBIG_NOT_CONVERGED','PASS_N_TESTS')

class Missing(ValueError):pass

def need(b,msg):
    if not b:raise Missing(msg)

def num(x):
    need(type(x) in (int,float) and math.isfinite(x) and x>=0,'nonfinite/non-numeric/negative statistic')
    return float(x)

def array(x,shape):
    need(isinstance(x,list),'array absent')
    a=np.asarray(x)
    need(a.dtype.kind in 'fi' and a.shape==shape and bool(np.all(np.isfinite(a))),'array shape or values')
    return a.astype(float)

def compare(records):
    result=dict(schema='NGC_NTEST_COMPARE_C2V001',label='TESTED',outcome='INCOMPLETE',tests_read=False,
                theta=THETA,scope='saved-operator N-tests only; NGC fixed points UNTESTED; no adoption')
    try:
        need(isinstance(records,dict) and set(records)==set(REQUIRED),'missing or unknown records')
        for n in REQUIRED:
            r=records[n];need(isinstance(r,dict),'invalid '+n)
            if n.startswith('N'):
                need(r.get('test')==n and r.get('schema')=='NGC_NTEST_RECORD_C2V001','unknown schema/test '+n)
                need(r.get('operator_sha256')==OP_SHA and r.get('theta')==THETA,'wrong state/threshold '+n)
                need(r.get('label')=='TESTED','untested '+n)
        lo=records['LO_NGC'];i1=records['I1T_NGC']
        need(lo.get('gate')=='LO_NGC' and lo.get('operator_sha256')==OP_SHA and lo.get('theta')==THETA,'LO custody')
        need('readout-coupled' in lo.get('defining_quantity','').lower(),'LO must be readout coupled')
        need(lo.get('verdict') in ('PASS','FAIL') and i1.get('verdict') in ('PASS','FAIL'),'unknown gate verdict')
        need(i1.get('gate')=='I1T_NGC' and i1['pins']['ngc_T120L_operator']['sha256']==OP_SHA,'I1T custody')
        builds={b['case']:b for b in i1['builds']}
        need(set(builds)=={'NGC_T120L_fixed','NGC_T120L_initial_gas','NGC_T120L_current'},'I1T coverage')
        i1good=i1['verdict']=='PASS'
        for b in builds.values():
            need(b.get('nodes')==4096 and b.get('verdict') in ('PASS','FAIL'),'I1T nodes/verdict')
            i1good &= b['verdict']=='PASS' and num(b['max_rel'])<=1e-12
        shells=lo['shells'];ranges=[s['range_inverse_kpc'] for s in shells]
        need(all(s in ranges for s in [[2.,3.],[3.,4.],[4.,6.],[6.,8.],[8.,12.],[12.,16.]]),'LO coverage')
        lovals=[num(s['readout_coupled_over_theta']) for s in shells]
        lototal=num(lo['summed_max_over_theta'])
        logood=lo['verdict']=='PASS' and max(lovals)<=.005 and lototal<=.05 and sum(lovals)<=.05
        n0=records['N0'];need(type(n0.get('bitwise_equal')) is bool,'N0 bool')
        need(n0.get('ring_count')==156 and n0.get('azimuths')==32 and n0.get('heights')==7,'N0 coverage')
        n0good=n0['bitwise_equal'] and num(n0['mismatches'])==0
        nq=records['NQ'];need(nq.get('ring_count')>=100 and nq.get('azimuths')==32 and nq.get('heights')==7,'NQ coverage')
        need(nq.get('base_quadrature')==[.005,.007,8] and nq.get('fine_quadrature')==[.0025,.0035,12],'NQ doubling')
        nqgood=max(num(nq['max_delta_lnN0']),num(nq['max_delta_dL']))<=THETA/20
        n1=records['N1'];sp=array(n1['spread'],(100,));cp=array(n1['c1prime_spread'],(100,));ref=array(n1['reference_check_spread'],(100,))
        need(n1.get('c1prime_reference')=='G160L' and n1.get('reference_checked_against')=='G120L','C1prime reference')
        n1good=bool(np.all(sp[list(SHAPE)]<THETA) and np.all(cp<THETA) and np.all(ref<THETA))
        n2=records['N2'];need(n2.get('ring_count')>=100 and n2.get('azimuths')==32 and n2.get('heights')==7,'N2 coverage')
        n2good=max(num(n2['max_delta_lnN0']),num(n2['max_delta_dL']))<=THETA/4
        n3=records['N3'];need(set(n3['pairs'])=={'8_vs_16','32_vs_16'},'N3 pairs')
        n3good=True
        for pair in n3['pairs'].values():
            need(pair.get('same_kept_packet') is True and pair.get('arithmetic')=='1.+(n_kept+t)','N3 arithmetic')
            need(pair.get('ring_count')>=100 and pair.get('azimuths')==32,'N3 coverage')
            n3good &= max(num(pair['max_delta_S']),num(pair['max_delta_dL']))<=THETA/4
            # Literal R1 dimensionless wording is stricter than dimensional interpretation.
            n3good &= num(pair['max_delta_S'])/THETA<=THETA/4
        n4=records['N4'];num(n4['e4_z95']);need(n4.get('ring_count')>=100 and n4.get('azimuths')==32,'N4 coverage')
        if not n0good or not i1good:result['outcome']='IMPLEMENTATION_DEFECT'
        elif not logood:result['outcome']='NON_LAPSE_TAIL_MATERIAL'
        elif not nqgood:result['outcome']='NUMERICS_UNCERTIFIED'
        else:
            result['tests_read']=True
            result['outcome']='N1_FAIL' if not n1good else 'SHAPE_DISAGREEMENT' if not n2good else 'KBIG_NOT_CONVERGED' if not n3good else 'PASS_N_TESTS'
        result['checks']=dict(N0=n0good,I1T_NGC=i1good,LO_NGC=logood,NQ=nqgood,N1=n1good,N2=n2good,N3=n3good,N4='REPORTED_ONLY')
        result['N4_e4_z95']=n4['e4_z95']
        result['N3_wording']='Stricter literal normalized-S clause enforced; needs coordinator clarification before relaxing.'
    except (Missing,KeyError,TypeError,ValueError,IndexError,OverflowError) as e:
        result.update(outcome='INCOMPLETE',tests_read=False,reason=str(e))
    return result

def read_manifest(path):
    m=json.loads(Path(path).read_text());out={}
    for k,v in m.items():
        p=Path(v['path']);parts=p.resolve().parts
        if any(s.startswith('UVT_') or s=='KMAX_A2F10_C5H_RUN_V001' for s in parts):raise ValueError('PROHIBITED_PATH')
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('HASH_MISMATCH')
        out[k]=json.loads(raw)
    return out

if __name__=='__main__':
    try:r=compare(read_manifest(sys.argv[1]))
    except Exception as e:r=dict(outcome='INCOMPLETE',tests_read=False,reason=str(e))
    dest=Path(sys.argv[2]);root=Path(__file__).resolve().parent
    if not dest.resolve().is_relative_to(root):raise SystemExit('OUTPUT_SCOPE')
    with dest.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
    print(r)
