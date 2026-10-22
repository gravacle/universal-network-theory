"""0512 successor. First-applicable N_NO_RUN, N_INCOMPLETE, N_FAIL_NQ/N0/N1/N2/N3, N_PASS.
Unknown/missing/untested input is N_INCOMPLETE. Malformed known records or contradictions are N_NO_RUN.
N4 is reported only. No result licenses a scientific launch. Input manifest pins every record by bytes.
"""
import json,math,sys,hashlib
from pathlib import Path
import numpy as np
THETA=3.3657664138980042e-09
OP_SHA='e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'
SHAPE=(1,2,3,4,5,6,7,8,10,13,14,15)
REQUIRED=('N0','N1','N2','N3','N4','NQ','LO_NGC','I1T_NGC')
ORDER=('NQ','N0','N1','N2','N3')
OUTCOMES=('N_NO_RUN','N_INCOMPLETE',*(f'N_FAIL_{n}' for n in ORDER),'N_PASS')
class Defect(ValueError):pass
class Pending(ValueError):pass

def need(b,msg):
    if not b:raise Defect(msg)

def num(x):
    need(type(x) in (int,float) and math.isfinite(x) and x>=0,'invalid statistic')
    return float(x)

def arr(x,shape):
    a=np.asarray(x);need(a.dtype.kind in 'fi' and a.shape==shape and bool(np.all(np.isfinite(a))),'array shape/values')
    return a.astype(float)

def compare(records):
    result=dict(schema='NGC_NTEST_COMPARE_C2V002',label='TESTED',outcome='N_INCOMPLETE',tests_read=False,
        theta=THETA,scope='saved-operator only; N_PASS licenses nothing; fixed points UNTESTED',failures=[])
    bad=[];pending=[];checks={};current='manifest'
    if not isinstance(records,dict):return dict(result,outcome='N_NO_RUN',defects=['manifest: not an object'])
    for n in set(records)-set(REQUIRED):pending.append('unknown record '+n)
    for n in REQUIRED:
        if n not in records:pending.append(n+': missing')
    # Validate each provided known record, even when another record is missing (N_NO_RUN precedence).
    for n in REQUIRED:
        if n not in records:continue
        r=records[n];current=n
        try:
            need(isinstance(r,dict),'not an object')
            if n.startswith('N'):
                if r.get('schema')!='NGC_NTEST_RECORD_C2V001' or r.get('test')!=n:raise Pending('unknown schema/test')
                if r.get('label')!='TESTED':raise Pending('not tested')
                need(r.get('operator_sha256')==OP_SHA and r.get('theta')==THETA,'state/threshold mismatch')
            if n=='N0':
                need(type(r.get('bitwise_equal')) is bool,'bitwise flag type')
                need(r.get('ring_count')==156 and r.get('azimuths')==32 and r.get('heights')==7,'coverage')
                mismatch=num(r['mismatches']);need(r['bitwise_equal']==(mismatch==0),'flag contradicts mismatch count')
                checks[n]=r['bitwise_equal']
            elif n=='NQ':
                need(r.get('ring_count')>=100 and r.get('azimuths')==32 and r.get('heights')==7,'coverage')
                need(r.get('base_quadrature')==[.005,.007,8] and r.get('fine_quadrature')==[.0025,.0035,12],'not registered doubling')
                ov=r.get('memory_cap_override')
                if ov is not None:need(ov=={'bytes':4*2**30,'reason':'replay-only resource guard, 0513',
                    'module_sha256':'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22'},'unregistered memory override')
                checks[n]=max(num(r['max_delta_lnN0']),num(r['max_delta_dL']))<=THETA/20
            elif n=='N1':
                sp=arr(r['spread'],(100,));need(bool(np.all(sp>=0)),'negative spread')
                if any(k not in r for k in ('c1prime_spread','reference_check_spread','c1prime_reference','reference_checked_against')):
                    raise Pending('C1prime G160L/G120L evidence absent')
                cp=arr(r['c1prime_spread'],(100,));ref=arr(r['reference_check_spread'],(100,))
                need(bool(np.all(cp>=0) and np.all(ref>=0)),'negative reference spread')
                need(r['c1prime_reference']=='G160L' and r['reference_checked_against']=='G120L','reference mismatch')
                checks[n]=bool(np.all(sp[list(SHAPE)]<THETA) and np.all(cp<THETA) and np.all(ref<THETA))
                result['S_over_theta']=(sp/THETA).tolist()
            elif n=='N2':
                need(r.get('ring_count')>=100 and r.get('azimuths')==32 and r.get('heights')==7,'coverage')
                checks[n]=max(num(r['max_delta_lnN0']),num(r['max_delta_dL']))<=THETA/4
            elif n=='N3':
                need(set(r['pairs'])=={'8_vs_16','32_vs_16'},'pairs')
                good=True;reported={}
                for name,v in r['pairs'].items():
                    need(v.get('same_kept_packet') is True and v.get('arithmetic')=='1.+(n_kept+t)','kept/arithmetic')
                    need(v.get('ring_count')>=100 and v.get('azimuths')==32,'coverage')
                    ds=num(v['max_delta_S']);dl=num(v['max_delta_dL'])
                    good &= max(ds,dl)<=THETA/4;reported[name]=dict(delta_S_over_theta=ds/THETA,delta_dL_over_theta=dl/THETA)
                checks[n]=bool(good);result['N3_reported_theta_units']=reported
            elif n=='N4':
                need(r.get('ring_count')>=100 and r.get('azimuths')==32,'coverage')
                result['N4_e4_z95']=num(r['e4_z95']);checks[n]='REPORTED_ONLY'
            elif n=='LO_NGC':
                need(r.get('gate')==n and r.get('operator_sha256')==OP_SHA and r.get('theta')==THETA,'custody')
                need('readout-coupled' in r.get('defining_quantity','').lower(),'wrong defining quantity')
                if r.get('verdict') not in ('PASS','FAIL'):raise Pending('unknown verdict')
                ranges=[s['range_inverse_kpc'] for s in r['shells']]
                need(all(s in ranges for s in [[2.,3.],[3.,4.],[4.,6.],[6.,8.],[8.,12.],[12.,16.]]),'coverage')
                vals=[num(s['readout_coupled_over_theta']) for s in r['shells']];total=num(r['summed_max_over_theta'])
                good=max(vals)<=.005 and total<=.05 and sum(vals)<=.05
                need((r['verdict']=='PASS')==good,'verdict contradicts data')
                checks[n]=good
                if not good:raise Pending('readout-coupled LO_NGC has not passed; N tests unread')
            else:
                need(r.get('gate')=='I1T_NGC' and r['pins']['ngc_T120L_operator']['sha256']==OP_SHA,'custody')
                if r.get('verdict') not in ('PASS','FAIL'):raise Pending('not passed/unknown verdict')
                builds={b['case']:b for b in r['builds']}
                need(len(builds)==len(r['builds']) and set(builds)=={'NGC_T120L_fixed','NGC_T120L_initial_gas','NGC_T120L_current'},'build coverage')
                good=True
                for b in builds.values():
                    need(b.get('nodes')==4096,'node coverage')
                    if b.get('verdict') not in ('PASS','FAIL'):raise Pending('unknown build verdict')
                    ok=num(b['max_rel'])<=1e-12;need((b['verdict']=='PASS')==ok,'build verdict contradicts data');good &= ok
                need((r['verdict']=='PASS')==good,'verdict contradicts builds');checks[n]=bool(good)
                if not good:raise Pending('NGC I1-T has not passed')
        except Pending as e:pending.append(n+': '+str(e))
        except (Defect,KeyError,TypeError,ValueError,IndexError,OverflowError) as e:bad.append(n+': '+str(e))
    result['checks']=checks
    if bad:result.update(outcome='N_NO_RUN',defects=bad,pending=pending)
    elif pending:result.update(outcome='N_INCOMPLETE',pending=pending)
    else:
        fail=[n for n in ORDER if not checks[n]]
        result.update(tests_read=True,failures=['N_FAIL_'+n for n in fail],outcome='N_FAIL_'+fail[0] if fail else 'N_PASS')
    return result

def read_manifest(path):
    m=json.loads(Path(path).read_text());out={}
    for k,v in m.items():
        p=Path(v['path'])
        if any(s.startswith('UVT_') or s=='KMAX_A2F10_C5H_RUN_V001' for s in p.resolve().parts):raise ValueError('PROHIBITED_PATH')
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('HASH_MISMATCH '+k)
        out[k]=json.loads(raw)
    return out
if __name__=='__main__':
    try:r=compare(read_manifest(sys.argv[1]))
    except Exception as e:r=dict(outcome='N_NO_RUN',tests_read=False,defects=[str(e)])
    dest=Path(sys.argv[2]);root=Path(__file__).resolve().parent
    if not dest.resolve().is_relative_to(root):raise SystemExit('OUTPUT_SCOPE')
    with dest.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
    print(r['outcome'])
