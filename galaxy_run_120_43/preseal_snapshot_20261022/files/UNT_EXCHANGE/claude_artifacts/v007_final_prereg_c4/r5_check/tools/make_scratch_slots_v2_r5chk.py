# make_scratch_slots_v2_r5chk.py -- v002-schema slot JSONs (UNT_V007_SEAL_SLOTS_C4V002) for the scratch rehearsal (r5_check helper).
# usage: python3 -I -B make_scratch_slots_v2_r5chk.py REHEARSAL_DIR
# Adds the two v002 keys to SLOTS_A/B_R5CHK.json: cascade_map_r5_addendum (A: PENDING; B: a GAP placeholder file naming the r5
# cascade map sha, NOT an inventory addendum) and admission_entry (BUILD_V007's launcher v007 and guard v008, from bytes).
import sys, os, json, hashlib
R = sys.argv[1]
def sha_f(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def xwrite(name, text):
    p = os.path.join(R, name)
    with open(p, 'x') as f:
        f.write(text)
    return p
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
L = A + '/v007_launch_packet_cx1/route_a_token_launcher_cx1v007.py'; G = A + '/v007_launch_packet_cx1/producer_guard_cx1v008.py'
assert sha_f(L) == '861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d' and sha_f(G) == '294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731'
adm = {'launcher': {'path': L, 'sha256': sha_f(L)}, 'guard': {'path': G, 'sha256': sha_f(G)}}
ph = xwrite('CASCADE_MAP_R5_ADDENDUM_GAP_PLACEHOLDER_R5CHK.md',
            '# GAP placeholder (r5_check rehearsal) -- NOT the A69 immutable inventory addendum\n\n'
            'Stands in for CASCADE_MAP_R5_ADDENDUM (A69; seal_record_requirements[9]; rehearsal GAP-18; ROOT_ITEMS_R5 RI-32), which has no owner and is not on disk.\n'
            'It names the r5 cascade map it would extend: CASCADE_MAP_R5_C2V001.json a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880.\n')
out = {}
for tag in ('A', 'B'):
    s = json.load(open(os.path.join(R, 'SLOTS_%s_R5CHK.json' % tag)))
    s['schema'] = 'UNT_V007_SEAL_SLOTS_C4V002'
    s['admission_entry'] = adm
    s['cascade_map_r5_addendum'] = ({'path': 'PENDING_ROOT_CASCADE_MAP_R5_ADDENDUM (A69; no owner, RI-32)', 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}
                                    if tag == 'A' else {'path': ph, 'sha256': sha_f(ph)})
    p = xwrite('SLOTS_%s_V2_R5CHK.json' % tag, json.dumps(s, indent=1, ensure_ascii=False) + '\n')
    out[tag] = {'path': p, 'sha256': sha_f(p)}
print(json.dumps(out), 'placeholder', sha_f(ph))
