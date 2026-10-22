"""Independent score-relation preparation, prereg section3/6.3.
No prior-evidence formatting or row-scope/output-contract adapter yet.
"""
ORDER=('R-MF','R-UT1','R-REACH','R-HIST','R-DRIFT','R-S1','R-GRID','R-NAX','R-GEFF','R-ML','R-SPEC','R-GEO','R-TSR')

def relations(result,outer_deficit_miss,stage0='NOT_EVALUATED_BEFORE_FREEZE'):
    p=result['patterns'];minor=result['minority_miss'];outer=result['outer_failure']
    inner=any(p[k] for k in ('P3','P4','P12','P15'))
    glob=p['P6'] or p['P7']
    triggers={'R-MF':outer or inner or p['P13'] or glob or any(minor),
              'R-UT1':outer,'R-REACH':outer,
              'R-HIST':outer or p['P13'] or glob or minor[1] or minor[2],
              'R-DRIFT':outer,'R-S1':p['P2'] or p['P11'] or p['P6'],
              'R-GRID':p['P2'] or p['P11'],
              'R-NAX':p['P11'] or p['P14'] or inner or p['P13'] or p['P7'],
              'R-GEFF':inner,'R-ML':inner,'R-SPEC':inner or minor[0],
              'R-GEO':inner or p['P6'],'R-TSR':p['P10']}
    answers={}
    for name in ORDER:
        relation='CONSISTENT';code=None;test='OPEN'
        if name=='R-MF':test=result['e3']
        if name=='R-DRIFT':
            if stage0 in ('CONSISTENT','AGAINST'):test=stage0+' (DT-S0G)'
            elif stage0=='NOT_DECIDED':test='OPEN (NOT_DECIDED)'
            else:test='OPEN ('+stage0+')'
        if not triggers[name]:relation='NOT_ADDRESSED';code='PATTERN_NOT_HELD'
        elif name=='R-DRIFT' and stage0=='AGAINST':relation='INCONSISTENT'
        elif name in ('R-UT1','R-REACH'):
            sign=result['zones'][2]['S']
            if sign=='EXCESS':relation='NOT_ADDRESSED';code='SIGN_SCOPE_EXCESS'
            elif sign=='UNDEFINED':relation='NOT_ADDRESSED';code='SIGN_SCOPE_UNSIGNED'
            elif not outer_deficit_miss:relation='NOT_ADDRESSED';code='SIGN_SCOPE_NO_DEFICIT_MISS'
        answers[name]={'relation':relation,'code':code,'deciding_test':test}
    return answers
