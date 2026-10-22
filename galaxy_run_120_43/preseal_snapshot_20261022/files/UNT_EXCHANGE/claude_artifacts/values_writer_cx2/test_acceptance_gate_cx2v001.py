"""Synthetic acceptance-gate tests for A159/A211; no producer, solver or real call is run."""
import argparse, ast, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
SCHEMA='UNT_NGC_LO_ACCEPTANCE_RECORD_C2V005'
HANDOFF='7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1'
ROUTE='NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(d,f,sort_keys=True);f.write('\n')
    return {'path':str(p.resolve()),'sha256':sha(p)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--module',required=True);ap.add_argument('--work',required=True)
    a=ap.parse_args();work=Path(a.work).resolve();work.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('writer_gate_test',a.module);W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
    checks=[]
    def check(name,ok,detail=None):checks.append({'name':name,'ok':bool(ok),'detail':detail})
    def refuse(name,code,fn):
        try:fn();check(name,False,'no refusal')
        except W.Refused as exc:check(name,exc.code==code,exc.code)
        except Exception as exc:check(name,False,type(exc).__name__+': '+str(exc))
    check('literal schema/sha pair from handoff bytes',W.MEMBER_ACCEPTANCE_PRODUCERS==((SCHEMA,HANDOFF),))
    check('O1 exact accepted readings',W.MEMBER_ACCEPTANCE_READINGS==('ACCEPTED','LO_UNCERTIFIED_TRANSIENT'))
    check('A152 section unchanged',W.ROOT_RULING['sha256']=='5aee4cc0f3ae64e5ea630d5a6459fdccc4cf2e3d55061d57e9214b1f002b074f')
    qids=['SYN-Q%02d'%i for i in range(43)]
    rows=[{'id':q,'valid':i!=0,'speed_km_s':None if i==0 else 20.0+i,'reason':'SYN_INVALID' if i==0 else None} for i,q in enumerate(qids)]
    cpins={}
    for status,valid in [('COMPLETED',True),('COMPLETED_INVALID',False),('FAILED',True)]:
        call=work/status;out=call/'out'
        r={'status':status,'valid':valid,'galaxy':'NGC3198','driver_sha256':W.DRIVER_SHA256,'call_spec_sha256':'a'*64,
           'rows':rows,'speeds_km_s':{r['id']:r['speed_km_s'] for r in rows}}
        rp=put(out/'result.json',r);put(out/'finish.json',dict(status=status,valid=valid,result_path=rp['path'],result_sha256=rp['sha256']))
        cpins[status]=(call,rp)
    def record(status,reading,tag,edit=None):
        call,rp=cpins[status]
        rec={'schema':SCHEMA,'route':ROUTE,'handoff':{'path':'/synthetic/handoff.py','sha256':HANDOFF},
             'call_dir':str(call),'result':rp,'reading':reading}
        if edit is not None:rec=edit(rec)
        return put(work/'acceptance'/('%s.json'%tag),rec)
    def point(status,kind,acceptance):
        return W.values_point(kind=kind,role='u_A' if kind=='phase1_values' else 'member',theta_key='b'*64,query_ids=qids,
                              call_dir=str(cpins[status][0]),call_spec_sha256='a'*64,log_index=4,acceptance=acceptance)[0]
    for status in cpins:
        for reading in ['ACCEPTED','LO_UNCERTIFIED_TRANSIENT','INCOMPLETE','ACCEPTED_PASS_FLAGGED','NON_LAPSE_TAIL_MATERIAL','BOUND_INSUFFICIENT','UNDECIDABLE_FLAGGED',None]:
            ref=record(status,reading,status+'_'+str(reading)) if reading else None
            for kind in ['phase1_values','phase2_members']:
                p=point(status,kind,ref)
                accepted=reading in ('ACCEPTED','LO_UNCERTIFIED_TRANSIENT')
                want=[status=='COMPLETED' and i!=0 and (accepted or kind=='phase2_members') for i in range(43)]
                ok=p['valid']==want and p['speeds_km_s']==[r['speed_km_s'] for r in rows]
                if kind=='phase2_members':ok=ok and p['member_valid']==(status=='COMPLETED' and accepted)
                else:ok=ok and 'member_valid' not in p
                check('truth '+status+' '+kind+' '+str(reading),ok)
    mutations=[
        ('wrong_schema','ACCEPTANCE_SCHEMA',lambda r:dict(r,schema='UNT_NGC_LO_ACCEPTANCE_RECORD_C2V004')),
        ('DDO_schema','ACCEPTANCE_SCHEMA',lambda r:dict(r,schema='DDO154_TAIL_ACCEPTANCE_RECORD_C2V001')),
        ('wrong_handoff','ACCEPTANCE_PRODUCER_NOT_REVIEWED',lambda r:dict(r,handoff=dict(r['handoff'],sha256='0'*64))),
        ('missing_route','ACCEPTANCE_ROUTE',lambda r:{k:v for k,v in r.items() if k!='route'}),
        ('wrong_route','ACCEPTANCE_ROUTE',lambda r:dict(r,route='DDO_ROUTE')),
        ('other_result','ACCEPTANCE_NOT_OF_THIS_CALL',lambda r:dict(r,result=dict(r['result'],sha256='f'*64))),
        ('other_call','ACCEPTANCE_NOT_OF_THIS_CALL',lambda r:dict(r,call_dir=str(work/'other'))),
        ('unknown_reading','ACCEPTANCE_READING_UNKNOWN',lambda r:dict(r,reading='PASS'))]
    for name,code,edit in mutations:
        ref=record('COMPLETED','ACCEPTED',name,edit)
        for kind in ['phase1_values','phase2_members']:
            refuse(name+' '+kind,code,lambda kind=kind,ref=ref:point('COMPLETED',kind,ref))
    d={'schema':'CX2_VALUES_WRITER_ACCEPTANCE_GATE_TESTS_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),
       'label':'TESTED','module':{'path':str(Path(a.module).resolve()),'sha256':sha(a.module)},'script':{'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},
       'n':len(checks),'passed':sum(c['ok'] for c in checks),'tests':checks,'synthetic_only':True,
       'flags':{'isolated':sys.flags.isolated,'dont_write_bytecode':sys.flags.dont_write_bytecode}}
    put(work/'RESULT_GATE_TESTS_CX2V001.json',d)
    print(json.dumps({'n':d['n'],'passed':d['passed'],'failures':[x for x in checks if not x['ok']]}))
    return 0 if d['n']==d['passed'] else 1
if __name__=='__main__':sys.exit(main())
