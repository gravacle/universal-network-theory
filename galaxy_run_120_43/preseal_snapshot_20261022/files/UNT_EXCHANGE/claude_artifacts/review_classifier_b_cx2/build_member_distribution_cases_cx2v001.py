"""Additional hand-built STAGE0 member-distribution probes; no producer execution."""
import copy
import json
import runpy
import subprocess
from pathlib import Path

ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2')
H=runpy.run_path(str(ROOT/'build_own_bundles_cx2v003.py'),run_name='cx2_hand_builder')
base=ROOT/'own_bundles_cx2v001/H09_stage0_improves'
rows=[]
for cid,invalid in [('H13_unequal_stage0_members',False),('H14_invalid_stage0_twin',True)]:
    out=ROOT/'own_bundles_cx2v002'/cid
    bundle=json.loads((base/'BUNDLE.json').read_bytes())
    docs={role:json.loads((base/pin['path']).read_bytes())
          for role,pin in bundle['inputs'].items() if pin}
    m,s=docs['freeze_manifest'],docs['score']
    members=m['alternative_results']['STAGE0_GRID_OUTER']['members']
    for i in range(38,43):
        members[1]['speeds_km_s'][i]=80.0
    if invalid:
        members[0].update(member_valid=False,forward_valid_flag=False,
                          reasons=['SYNTHETIC_FORWARD_REFUSAL'],
                          row_valid=[False]*43,speeds_km_s=[None]*43)
    a=next(x for x in s['alternatives'] if x['name']=='STAGE0_GRID_OUTER')
    a['members']=[H['ladder'](x,range(35,43),[100.0]*43,[5.0]*43) for x in members]
    a['member_within_error_counts']=H['dist']([x['within_error_count'] for x in a['members']])
    m.pop('manifest_sha256')
    m['manifest_sha256']=H['sha'](H['enc'](m))
    mpin=H['put'](out/'freeze_manifest.json',m)
    bundle['inputs']['freeze_manifest']=mpin
    for k in ('manifest_file_sha256_actual','manifest_file_sha256_expected','manifest_file_sha256_registered'):
        s[k]=mpin['sha256']
    s['manifest_sha256_self']=m['manifest_sha256']
    bundle['inputs']['score']=H['put'](out/'score.json',s)
    copied={'freeze_manifest.json','score.json'}
    for group in ('inputs','rosters','sealed'):
        for pin in bundle[group].values():
            if isinstance(pin,dict) and set(pin)=={'path','sha256'} and pin['path'] not in copied:
                raw=(base/pin['path']).read_bytes()
                assert H['sha'](raw)==pin['sha256']
                H['put'](out/pin['path'],raw=raw)
                copied.add(pin['path'])
    bp=H['put'](out/'BUNDLE.json',bundle)
    rows.append(dict(id=cid,bundle=str(out/'BUNDLE.json'),sha256=bp['sha256'],
                     input_member_counts=a['member_within_error_counts'],
                     clause='C-6.1 invalid twin; C-6.3 final sentence; source scorer L4289-L4294'))
H['put'](ROOT/'OWN_BUNDLE_INDEX_CX2V002.json',
         dict(date_u=subprocess.check_output(['/bin/date','-u'],text=True).strip(),
              label='TESTED construction; classifier-form synthetic fixtures',cases=rows,n=len(rows)))
print(json.dumps({'n':len(rows)}))
