import json,hashlib,sys
raw=open(sys.argv[1],'rb').read(); assert hashlib.sha256(raw).hexdigest()==sys.argv[2],'DBP_C2V004C_PIN'
d=json.loads(raw); assert d['schema']=='DIRECT_BATCH_PARAMS_S45_C2V004C'
h=d['batches']['HEADLINE']; caps=h['caps_per_case']
plan=json.load(open(sys.argv[3])); adm=json.load(open(sys.argv[4]))
assert [c['case'] for c in plan['calls']]==h['case_order']==adm['case_order'],'CASE_ORDER'
for c in plan['calls']:
    want=caps[c['case']]; got={k:c[k] for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')}
    assert got==want,('PLAN_CAPS',c['case'],got,want)
    assert adm['caps'][c['case']]==want,('ADMISSION_CAPS',c['case'])
print('HEADLINE caps == DBP C2V004C for %d calls; wall_cap_s %d' % (len(plan['calls']),plan['calls'][0]['wall_cap_s']))
