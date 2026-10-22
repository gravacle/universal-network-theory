"""Independent partial reading relation, C-1.1 and C-3.
None means unavailable. Conservative enumeration respects registered precedence.
This helper does not license deductions outside the closed prereg list.
"""
from itertools import product

def possibilities(value):
    if value is None:return (False,True)
    if type(value) is not bool:raise ValueError('expected boolean or unavailable')
    return (value,)

def tri_any(values):
    values=tuple(values)
    for value in values:possibilities(value)
    if True in values:return True
    return None if None in values else False

def tri_all(values):
    values=tuple(values)
    for value in values:possibilities(value)
    if False in values:return False
    return None if None in values else True

def partial_relation(trigger,against=False,scope_codes=(None,)):
    # scope None denotes within sign scope; strings are NOT_ADDRESSED codes.
    scope_codes=tuple(scope_codes)
    allowed={None,'SIGN_SCOPE_EXCESS','SIGN_SCOPE_UNSIGNED','SIGN_SCOPE_NO_DEFICIT_MISS'}
    if not scope_codes or any(code not in allowed for code in scope_codes):raise ValueError('scope')
    outcomes=set()
    for fires,opposes,scope in product(possibilities(trigger),possibilities(against),scope_codes):
        if not fires:outcomes.add(('NOT_ADDRESSED','PATTERN_NOT_HELD'))
        elif opposes:outcomes.add(('INCONSISTENT',None))
        elif scope is not None:outcomes.add(('NOT_ADDRESSED',scope))
        else:outcomes.add(('CONSISTENT',None))
    relations={r for r,c in outcomes};codes={c for r,c in outcomes}
    return {'relation':next(iter(relations)) if len(relations)==1 else None,
            'code':next(iter(codes)) if len(codes)==1 else None,
            'relation_available':len(relations)==1,'code_available':len(codes)==1}
