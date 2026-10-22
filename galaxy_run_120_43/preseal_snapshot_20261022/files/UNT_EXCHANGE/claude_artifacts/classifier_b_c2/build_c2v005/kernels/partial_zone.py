"""Additional count-only deductions from prereg C-2 and C-1.1.
The printed S itself remains separately masked under row defects.
"""
from partial_counts import reachable_counts,count_features

def extended_features(state):
    f=count_features(state)
    signed=f['M']-f['U'];defined=f['H']+signed
    undefined=defined==0 or (f['miss_dominated'] and 2*signed<f['N_v'])
    f.update(sign_is_undefined=undefined,unsigned_zone_pattern=f['miss_dominated'] and undefined,
             any_invalid=f['I']>0,no_valid_rows=f['N_v']==0)
    return f

def partial_zone(options):
    states=reachable_counts(options)
    possibilities={}
    for state in states:
        for key,value in extended_features(state).items():possibilities.setdefault(key,set()).add(value)
    return {key:next(iter(values)) for key,values in possibilities.items() if len(values)==1}, sorted(key for key,values in possibilities.items() if len(values)>1)
