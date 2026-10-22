"""Independent reachable count sets for C-1.1 defective rows.
Only H/M/U/I,N_v and dominance here; sign and cross-zone deductions are separate.
Each input is a nonempty collection of allowed normalized kinds.
"""
VECTORS={'HIT':(1,0,0,0),'SIGNED_MISS':(0,1,0,0),
         'NULL_MISS':(0,1,1,0),'LATE':(0,1,1,0),'INVALID':(0,0,0,1)}

def reachable_counts(options):
    states={(0,0,0,0)}
    for choices in options:
        choices=tuple(choices)
        if not choices or any(c not in VECTORS for c in choices):raise ValueError('row kinds')
        increments={VECTORS[c] for c in choices}
        states={tuple(a+b for a,b in zip(state,inc)) for state in states for inc in increments}
    return states

def count_features(state):
    h,m,u,i=state;n=h+m
    return {'N_v':n,'H':h,'M':m,'U':u,'I':i,
            'miss_dominated':n>0 and 2*m>=n,'hit_dominated':n>0 and 2*h>n}

def fixed_counts(options):
    states=reachable_counts(options)
    features=[count_features(s) for s in states]
    fixed={};ambiguous=[]
    for key in features[0]:
        values={f[key] for f in features}
        if len(values)==1:fixed[key]=next(iter(values))
        else:ambiguous.append(key)
    return fixed,ambiguous
