"""Compare's own gate functions on real fixture records and clearly labelled schema fixtures.
A mapped C4R3 fixture tests C5H contract shape only; it is not a C5H measurement.
"""
import copy,hashlib,importlib.util,json,sys
from pathlib import Path
R=Path(__file__).parent
P=R.parent/'v007_compare_c2/r6/kmax_tail_compare_c2v007_r6.py'
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
    s=importlib.util.spec_from_file_location('compare_contract',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    ea=json.loads((R/'ea_replay_cx1v003_C4R3_V001.json').read_bytes());ctx={'row_radii_m':ea['per_case']['C4R3']['row_radii_m']}
    checks=[]
    def check(name,gate,obj,expected,runsha=None):
        p=R/('CONTRACT_'+name+'_V002.json')
        with p.open('x') as f:json.dump(obj,f,indent=1)
        got=m.evaluate_gate(gate,str(p),ctx,runsha)
        checks.append({'name':name,'expected':expected,'actual':got['status'],'passed':got['status']==expected,'codes':got['codes'],'input':pin(p)})
        assert checks[-1]['passed'],checks[-1]
    check('EA_actual_C4R3_not_C5H','EA',ea,'RECORD_DEFECT')
    fake=copy.deepcopy(ea);fake['per_case']={'C5H':fake['per_case']['C4R3']};fake['label']='SYNTHETIC contract mapping only; actual measurements from C4R3'
    check('EA_contract_valid','EA',fake,'PASS',{'C5H':fake['per_case']['C5H']['result_sha256']})
    wrong=copy.deepcopy(fake);wrong['per_case']['C5H']['row_radii_m'][0]*=1.01
    check('EA_wrong_radius','EA',wrong,'RECORD_DEFECT')
    t=json.loads((R/'T2I_C4R3_FIXTURE_V002.json').read_bytes())
    check('T2I_actual_C4R3_not_C5H','T2I',t,'RECORD_DEFECT')
    t['case']='C5H';t['region']='G5\\G4';t['c5h_result_sha256']=t['actual_result']['sha256'];t['label']='SYNTHETIC contract mapping only; actual G4 minus G3 measurements from C4R3'
    check('T2I_contract_valid','T2I',t,'PASS',{'C5H':t['c5h_result_sha256']})
    t['components']['route_a_updated']=1e-8;t['max_rel']=1e-8
    check('T2I_contradictory_PASS','T2I',t,'RECORD_DEFECT')
    t['verdict']='FAIL';check('T2I_registered_FAIL','T2I',t,'FAIL')
    h=json.loads((R/'ra10_checkpoint_cx1v002_C4R3_V001.json').read_bytes());check('HARMONICS_actual_C4R3','HARMONICS',h,'PASS')
    for case in ('C5R3','C6R3'):
        t=json.loads((R/f'T2I_{case}_FIXTURE_V00{1 if case=="C5R3" else 2}.json').read_bytes());check('T2I_missing_'+case,'T2I',t,'RECORD_DEFECT')
    report={'label':'TESTED contract checks; mapped fixtures are not scientific gate evidence','compare':pin(P),'producer':pin(Path(__file__)),'checks':checks,'passed':len(checks),'failed':0}
    with (R/'COMPARE_CONTRACT_TESTS_V002.json').open('x') as f:json.dump(report,f,indent=1)
    print('compare gate checks',len(checks),'PASS')
if __name__=='__main__':main()
