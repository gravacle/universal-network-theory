"""Independent B terminal output forms and stop aggregation, no IO.
Shared output schema name is contractual; producer identity stays B.
"""
import copy
SCHEMA='CLASSIFIER_A_OUTPUT_C4V001'
NAME='classifier_b_cx1_preparation'
NOTES={'NO_NGC_CALL':'no NGC call: no classification (engine terminal status or NO_IDENTIFIED_DIRECTION; A133 1.3)','AT0A_FAILED':'AGREEMENT_DEFECT (prefix): no Phase-1 classification','HALTED':'Phase 2 reported HALTED (A133 3 rule (c))'}
def refusal(reason):
    return {'schema':SCHEMA,'classifier':NAME,'refused':True,'reason':reason}
def no_classification(mode,phase,status,run_status_code):
    if mode not in ('score','prescore') or phase not in ('PHASE_1','PHASE_2'):raise ValueError('phase/mode')
    if status not in NOTES or (status=='AT0A_FAILED' and phase!='PHASE_1') or (status=='HALTED' and phase!='PHASE_2'):raise ValueError('RUN_STATUS_NOT_OF_PHASE')
    return {'schema':SCHEMA,'classifier':NAME,'mode':mode,'phase':phase,'status':'NO_CLASSIFICATION','status_code':status,'run_status_code':run_status_code,'note':NOTES[status]}
def merged_stops(stops):
    groups={}
    for s in stops:
        key=(s['code'],s['class'],s['alternative'])
        details,rows=groups.setdefault(key,(set(),set()))
        details.update(s['detail']);rows.update(s['rows'])
    return [{'code':k[0],'class':k[1],'alternative':k[2],'detail':sorted(groups[k][0]),'rows':sorted(groups[k][1])} for k in sorted(groups,key=lambda k:(k[0],k[1],k[2] or ''))]
def prescore(phase,derived,stops,load_status,field_map):
    stops=merged_stops(stops)
    roles=('l1_record','agree_record','phase1_classification','commitment_status')
    return {'schema':SCHEMA,'classifier':NAME,'mode':'prescore','phase':phase,'manifest_phase_derived':derived,'result':'CLASSIFICATION_INPUT_DEFECT' if stops else 'PASS','stops':stops,'not_stop_inputs':{r:load_status[r] for r in roles},'field_map':field_map}
