"""Pure pattern preparation from prereg section2; no external record reader.
Rows within each zone must already be in ascending frozen radius order.
Flagged rows are normalized rows, not target records.
"""
from zone_kernel_v002 import summarize,median

def patterns(inner,transition,outer,flagged=()):
    zones=[tuple(inner),tuple(transition),tuple(outer)]
    i,t,o=map(summarize,zones)
    ratios=[r.ratio for r in zones[2] if r.ratio is not None]
    delta=median(ratios[len(ratios)//2:])-median(ratios[:len(ratios)//2]) if len(ratios)>=2 else None
    far=median(ratios[len(ratios)//2:]) if len(ratios)>=2 else None
    trend=delta is not None and delta<0 and t['m'] is not None and o['m'] is not None and t['m']>o['m']
    growing=o['S']=='DEFICIT' and trend
    crossing=o['S']=='CENTERED' and trend and far is not None and far < -1
    p={'P0':any(z['I']>0 for z in [i,t,o]),
       'P1':o['miss_dominated'] and o['S']=='DEFICIT',
       'P2':o['miss_dominated'] and o['S']=='EXCESS',
       'P3':i['miss_dominated'] and i['S']=='EXCESS',
       'P4':i['miss_dominated'] and i['S']=='DEFICIT',
       'P5':i['hit_dominated'] and o['miss_dominated'] and t['N_v']>0 and not t['hit_dominated'],
       'P6':i['S']==t['S']==o['S'] and i['S'] in ('DEFICIT','EXCESS'),
       'P7':sum(z['M'] for z in [i,t,o])>0 and not any(z['miss_dominated'] for z in [i,t,o]),
       'P8':sum(z['N_v'] for z in [i,t,o])>0 and sum(z['M'] for z in [i,t,o])==0,
       'P9':o['N_v']==0,
       'P10':any(r.kind=='MISS' for r in flagged),
       'P11':o['miss_dominated'] and o['S']=='CENTERED',
       'P12':i['miss_dominated'] and i['S']=='CENTERED',
       'P13':t['miss_dominated'],
       'P14':o['miss_dominated'] and o['S']=='UNDEFINED',
       'P15':i['miss_dominated'] and i['S']=='UNDEFINED'}
    p['P1g']=p['P1'] and growing
    p['P11g']=p['P11'] and crossing
    minority=[any(z['miss_dominated'] for z in [i,t,o]) and not z['miss_dominated'] and any(r.kind=='MISS' for r in rows) for z,rows in zip([i,t,o],zones)]
    e3='TESTED-NEGATIVE (A15 E3 scope)' if o['miss_dominated'] else ('NOT_NEGATIVE_AT_OUTER' if o['N_v'] else 'NOT_TESTABLE')
    return {'patterns':p,'zones':[i,t,o],'outer_failure':o['miss_dominated'],'delta':delta,
            'growing':growing,'crossing':crossing,'minority_miss':minority,'e3':e3}
