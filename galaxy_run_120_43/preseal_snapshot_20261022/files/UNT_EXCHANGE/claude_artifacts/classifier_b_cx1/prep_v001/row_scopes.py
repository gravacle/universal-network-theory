"""Pure row citation scope, prereg section3. Input rows are (id, Row).
Adapter must validate unique ids/zone membership and the TSR flagged-id set.
"""
from reading_relations import ORDER
ZONES=('INNER','TRANSITION','OUTER')

def citation_scopes(result,zone_rows,flagged_ids=()):
    p=result['patterns'];minor=result['minority_miss']
    scopes={name:set() for name in ORDER}
    def add(names,zones):
        for name in names:scopes[name].update(zones)
    if result['outer_failure']:
        add(('R-MF','R-UT1','R-REACH','R-HIST','R-DRIFT'),('OUTER',))
    if any(p[k] for k in ('P3','P4','P12','P15')):
        add(('R-MF','R-NAX','R-GEFF','R-ML','R-SPEC','R-GEO'),('INNER',))
    if p['P13']:add(('R-MF','R-HIST','R-NAX'),('TRANSITION',))
    if p['P6']:add(('R-MF','R-HIST','R-S1','R-GEO'),ZONES)
    if p['P7']:add(('R-MF','R-HIST','R-NAX'),ZONES)
    if p['P2'] or p['P11']:add(('R-S1','R-GRID'),('OUTER',))
    if p['P11'] or p['P14']:add(('R-NAX',),('OUTER',))
    for zone,holds in zip(ZONES,minor):
        if holds:add(('R-MF','R-SPEC' if zone=='INNER' else 'R-HIST'),(zone,))
    if p['P10']:
        for zone,rows in zip(ZONES,zone_rows):
            if any(q in flagged_ids and row.kind=='MISS' for q,row in rows):add(('R-TSR',),(zone,))
    output={}
    for name in ORDER:
        cited=[]
        for zone,rows in zip(ZONES,zone_rows):
            if zone not in scopes[name]:continue
            for q,row in rows:
                if row.kind=='MISS' and (name!='R-TSR' or q in flagged_ids):cited.append(q)
        output[name]={'scope_zones':[z for z in ZONES if z in scopes[name]],'cited_miss_rows':cited}
    return output
