"""Adversarial successor comparator checks; all inputs synthetic."""
import copy
import importlib.util
import json
from pathlib import Path

O=Path(__file__).parent
def load(name):
    s=importlib.util.spec_from_file_location(name,O/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    old=load('ngc_readiness_tools_v002');new=load('ngc_readiness_tools_v003')
    a=json.loads((O/'SYNTHETIC_V009_RESULT_V001.json').read_text())
    b=json.loads((O/'SYNTHETIC_V010_RESULT_V001.json').read_text())
    tests=[]
    def check(name,condition):
        tests.append({'name':name,'pass':bool(condition)})
        assert condition,name
    def passes(t,x,y,**kw):return t.compare_ngc_results(x,y,**kw)['verdict']=='PASS_RESULT_ASSEMBLY_EQUAL'
    check('original_synthetic_AST_assembly_still_equal',passes(new,a,b))
    for label,mutate in [
        ('missing_normalized_specs',lambda x:x.pop('normalized_spec')),
        ('missing_global_valid',lambda x:x.pop('valid')),
        ('false_global_valid',lambda x:x.update(valid=False)),
        ('missing_row_valid',lambda x:x['rows'][0].pop('valid')),
        ('integer_row_valid',lambda x:x['rows'][0].update(valid=1)),
    ]:
        x,y=copy.deepcopy(a),copy.deepcopy(b);mutate(x);mutate(y)
        # Both equal malformed inputs must fail, not pass by equality.
        check('v002_gap_demonstrated_'+label,passes(old,x,y))
        check('v003_rejects_'+label,not passes(new,x,y))
    x=copy.deepcopy(b);x['uv_tail']={'domain_empty_all_stages':True}
    check('v002_vacuous_empty_tail_gap',passes(old,a,x,gate='EMPTY_TAIL_IDENTITY'))
    check('v003_rejects_no_expected_coverage',not passes(new,a,x,gate='EMPTY_TAIL_IDENTITY'))
    check('v003_rejects_absent_stage_records',not passes(new,a,x,gate='EMPTY_TAIL_IDENTITY',expected_tail_stages=['reference']))
    x['uv_tail']['stage_records']=[{'stage':'reference','empty':True}]
    check('v003_accepts_exact_declared_empty_coverage',passes(new,a,x,gate='EMPTY_TAIL_IDENTITY',expected_tail_stages=['reference']))
    check('v003_rejects_missing_expected_stage',not passes(new,a,x,gate='EMPTY_TAIL_IDENTITY',expected_tail_stages=['reference','body']))
    x['uv_tail']['stage_records'].append({'stage':'reference','empty':True})
    check('v003_rejects_duplicate_stage',not passes(new,a,x,gate='EMPTY_TAIL_IDENTITY',expected_tail_stages=['reference']))
    for label,mutate in [
        ('speed',lambda x:x['rows'][4].update(speed_km_s=999.)),
        ('missing',lambda x:x['rows'].pop()),
        ('reorder',lambda x:x['rows'].reverse()),
        ('invalid_finite',lambda x:x['rows'][4].update(valid=False)),
        ('stray_tail_off',lambda x:x.update(uv_tail={})),
        ('RO1_fired',lambda x:x['route_a_outcome']['ro1'].update(fired=True)),
    ]:
        x=copy.deepcopy(b);mutate(x);check('v003_rejects_'+label,not passes(new,a,x))
    c=new.truncate_roster([{'id':'a','R_kpc':1.,'HI_mass_kg':2.,'confinement':'CONFINED'},
        {'id':'b','R_kpc':2.,'HI_mass_kg':8.,'confinement':'CERTIFIED_UNCONFINED'}],
        [{'id':'q','radius_kpc':3.,'valid':True,'speed_km_s':10.}])
    check('v003_cut_mass_and_reason',c['dropped_HI_mass_fraction']==.8 and c['query_rows'][0]['reason']=='QUERY_BEYOND_FIRST_UNCONFINED_RADIUS')
    check('v003_stage_array_identity',new.compare_stage_arrays(O/'SYNTHETIC_STAGE_a_V001.npz',O/'SYNTHETIC_STAGE_b_V001.npz'))
    check('v003_stage_array_tamper',not new.compare_stage_arrays(O/'SYNTHETIC_STAGE_a_V001.npz',O/'SYNTHETIC_STAGE_tamper_V001.npz'))
    new.write_x(O/'COMPARATOR_V003_TEST_RESULTS_V001.json',{'label':'TESTED','tests':tests,'passed':len(tests),'total':len(tests),
        'scope':'Synthetic comparator review regressions; no stages launched.'})
    print(f'{len(tests)}/{len(tests)} PASS')

if __name__=='__main__':main()
