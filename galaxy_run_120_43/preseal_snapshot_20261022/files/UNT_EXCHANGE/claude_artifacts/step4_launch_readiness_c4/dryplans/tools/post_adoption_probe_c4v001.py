"""Claude4 0587 part 2: POST-ADOPTION probe (synthetic config in this folder; plan-only). The V007 adoption check
(adoption_policy_cx2v006r7 L102-103) requires config numerics.block == the adopted C4T call spec's numerics EXACTLY; TESTED here:
the r9 block equals C4T TEMPLATE numerics and differs from C4T FILLED only in uv_tail.eps_certificate/lo_certificate. So the
adoption fills the block's two certificate slots with the sealed C4T's slots. This probe sets them to the C4T FILLED slots
(the A70 records, as the current launch packet registers), rebuilds every tail-ON step-4 spec the way the orchestrator / the
static check would after adoption, and checks per spec: validate_block, sensitivity gate, prelaunch_check, driver
normalize_spec with no pending certificate, deciding-row numerics identity, and that the capability-probe spec shas change only
through the slot fill. PROVISIONAL: valid only if the sealed C4T slots are exactly these records and no per-point registry is
used (a registry makes Mapper.build override the slots for mapper-built specs). Nothing here is a launch.
Usage: python3 -I -B post_adoption_probe_c4v001.py OUTDIR"""
import os
import sys
_C = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c4common_v001.py')
G = {'__file__': _C, '__name__': 'c4common_v001'}
exec(compile(open(_C, 'rb').read(), _C, 'exec'), G)
FENCE = G['install_fence']()
OPENS = []


def _log(event, args):
    if event == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0]) if not isinstance(args[0], str) else args[0]
        OPENS.append(os.path.realpath(os.path.abspath(p)))


sys.addaudithook(_log)
import copy
import importlib.util
import itertools
import json
import time

G['neutralize_platform_subprocess']()
out = os.path.abspath(sys.argv[1])
os.mkdir(out)
os.mkdir(os.path.join(out, 'specs_PROVISIONAL'))
C4T_FILLED = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json',
              'de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738')
C4T_TEMPLATE = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.TEMPLATE.json',
                '13cfe988dd48accb69c1df591db9fadfb818cb47b23491ca44065682116ee55f')
for p, s in (C4T_FILLED, C4T_TEMPLATE):
    assert G['sha_file'](p) == s, p
filled = json.load(open(C4T_FILLED[0]))
templ = json.load(open(C4T_TEMPLATE[0]))
cfg = json.loads(open(G['CONFIG_R9'][0], 'rb').read())
assert G['sha_file'](G['CONFIG_R9'][0]) == G['CONFIG_R9'][1]
rec = {'schema': 'C4_0587_POST_ADOPTION_PROBE_V001', 'launches_performed': 0, 'status': 'PROVISIONAL_SYNTHETIC_CONFIG',
       'tool': {'path': os.path.abspath(__file__), 'sha256': G['sha_file'](os.path.abspath(__file__))},
       'fence': {'path': FENCE.__file__, 'sha256': G['sha_file'](FENCE.__file__)},
       'c4t_filled': {'path': C4T_FILLED[0], 'sha256': C4T_FILLED[1]}, 'c4t_template': {'path': C4T_TEMPLATE[0], 'sha256': C4T_TEMPLATE[1]}}
rec['block_equals_c4t_template_numerics'] = cfg['numerics']['block'] == templ['numerics']
nb = copy.deepcopy(cfg['numerics']['block'])
for k in ('eps_certificate', 'lo_certificate'):
    nb['uv_tail'][k] = copy.deepcopy(filled['numerics']['uv_tail'][k])
rec['filled_block_equals_c4t_filled_numerics'] = nb == filled['numerics']
rec['slots'] = {k: nb['uv_tail'][k] for k in ('eps_certificate', 'lo_certificate')}
local = copy.deepcopy(cfg)
local['numerics']['block'] = nb
wd = os.path.join(out, 'UNCREATED_ORCH_CONTEXT')
local.update(work_dir=wd, work_dir_volume=None,
             work_dir_identity={'resolved': os.path.realpath(wd), 'volume': None, 'volume_uuid': None, 'symlinks': []})
wp, wsha = G['ORCH_R9']
raw = open(wp, 'rb').read()
assert G['sha_bytes'](raw) == wsha
sp_ = importlib.util.spec_from_file_location('_c4_r9_orch_post', wp)
M = importlib.util.module_from_spec(sp_)
sys.modules[sp_.name] = M
exec(compile(raw, wp, 'exec'), M.__dict__)
O = M.O
ctx = M.Context(local)
rec['context'] = {'cache_id': ctx.cache_id, 'base_spec_sha256': ctx.base_sha256, 'seed_spec_sha256': ctx.seed_spec_sha256,
                  'gate_reasons': {k: v.get('reasons') for k, v in ctx.gate_report().items()},
                  'layer1_normalize_ok': ctx.gates['driver_capability'].get('layer1_normalize_ok')}
inv = json.load(open(os.path.join(G['ROOT'], 'specs_v001/SPEC_INVENTORY_C4V001.json')))
pre_shas = {r['name']: r['sha256'] for r in inv['specs']}
template = copy.deepcopy(ctx.template)
coords = json.loads(open(G['CX2'] + '/DDO154_COORDINATES_CX2V006.json', 'rb').read())
by = {c['name']: c for c in coords['engine_coordinates']}
specs = {}
NOTE = '; C4 0587 POST-ADOPTION PROVISIONAL (slots = C4T FILLED A70 records); not a launch spec'


def hand(update, label):
    s = copy.deepcopy(template)
    s['numerics'] = copy.deepcopy(nb)
    s['physical'].update(update)
    s['label'] = label
    return O.json_bytes(s)


specs['TAIL_REANCHOR'] = ('TAIL_REANCHOR', hand({}, 'DDO154 TAIL_REANCHOR A2F10 registered anchor, config numerics' + NOTE))
specs['WORKERS_8_CANDIDATE_ANCHOR'] = ('WORKERS_8', hand({}, 'DDO154 deciding workers_8 candidate at the A2F10 anchor point, config numerics' + NOTE))
for label, th in ctx.probe_points():
    b = ctx.mapper.build(th)
    nm = 'HEADLINE_' + ('TRIAL' if label == 'trial' else 'CORNER_' + ''.join(
        '1' if '=hi' in part else '0' for part in label[len('corner '):].split(',')))
    specs[nm] = ('HEADLINE_CORNER', b['raw'])
free = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m')
for bits in itertools.product((0, 1), repeat=3):
    th = {n: by[n]['upper' if b else 'lower'] for n, b in zip(free, bits)}
    for mode, edge in (('LO', 'lower'), ('HI', 'upper')):
        specs['SENS_CORNER_C%s_D%s' % (''.join(map(str, bits)), mode)] = ('SENS_CORNER', hand(
            {'common_scale_s': th['common_scale_s'], 'gamma': th['gamma_over_Eref'] * by['Eref_base_J']['trial_value'],
             'ell_F_m': th['ell_F_m'], 'distance_Mpc': by['distance_Mpc'][edge]},
            'DDO154 sensitivity corner C%s D_%s' % (''.join(map(str, bits)), mode) + NOTE))
for edge in ('lower', 'upper'):
    specs['SENS_DISTANCE_%s' % edge.upper()] = ('SENS_DISTANCE', hand({'distance_Mpc': by['distance_Mpc'][edge]},
                                                                      'DDO154 sensitivity distance plan D %s' % edge + NOTE))
specs['CAMPAIGN_W1_SEED'] = ('CAMPAIGN_W1', ctx.mapper.build(ctx.seed_theta)['raw'])
rows = {}
for name, (fam, rawb) in specs.items():
    p = os.path.join(out, 'specs_PROVISIONAL', name + '.PROVISIONAL.json')
    with open(p, 'xb') as f:
        f.write(rawb)
    s = json.loads(rawb)
    r = {'family': fam, 'path': p, 'sha256': G['sha_bytes'](rawb), 'pre_adoption_sha256': pre_shas.get(name)}
    try:
        M.validate_block(s['numerics'])
        r['validate_block'] = 'PASS'
    except Exception as exc:
        r['validate_block'] = '%s: %s' % (type(exc).__name__, exc)
    r['sensitivity_gate'] = ctx.sensitivity_gate(s).get('status')
    try:
        ctx.prelaunch_check(s)
        r['prelaunch_check'] = 'PASS'
    except Exception as exc:
        r['prelaunch_check'] = ('%s: %s' % (type(exc).__name__, exc))[:300]
    try:
        n = ctx.D.normalize_spec(copy.deepcopy(s))
        r['driver_normalize'] = 'PASS'
        r['pending_certificates'] = ctx.D.uvt_info(n['numerics']['uv_tail'])['pending_certificates']
    except Exception as exc:
        r['driver_normalize'] = ('%s: %s' % (type(exc).__name__, exc))[:300]
    r['numerics_identity_equals_config_block'] = (M.M.canonical(M.M.deciding_numerics_identity(s['numerics'])) ==
                                                  M.M.canonical(M.M.deciding_numerics_identity(nb)))
    old = json.load(open([x['path'] for x in inv['specs'] if x['name'] == name][0])) if name in pre_shas else None
    if old is not None:
        a = copy.deepcopy(old)
        b2 = copy.deepcopy(s)
        for x in (a, b2):
            x.pop('label', None)
            for k in ('eps_certificate', 'lo_certificate'):
                x['numerics']['uv_tail'].pop(k, None)
        r['equals_pre_adoption_spec_except_label_and_slots'] = a == b2
    rows[name] = r
rec['specs'] = rows
rec['summary'] = {
    'n': len(rows),
    'all_validate_block': all(r['validate_block'] == 'PASS' for r in rows.values()),
    'all_driver_normalize_no_pending': all(r.get('driver_normalize') == 'PASS' and r.get('pending_certificates') == [] for r in rows.values()),
    'prelaunch_pass': sorted(n for n, r in rows.items() if r['prelaunch_check'] == 'PASS'),
    'prelaunch_refused': {n: r['prelaunch_check'][:120] for n, r in rows.items() if r['prelaunch_check'] != 'PASS'},
    'all_equal_pre_adoption_except_label_slots': all(r.get('equals_pre_adoption_spec_except_label_and_slots') for r in rows.values()),
    'all_numerics_identity_equal_config_block': all(r['numerics_identity_equals_config_block'] for r in rows.values())}
rec['blocked'] = list(FENCE.BLOCKED)
rec['runs_ext_opens'] = sorted(set(p for p in OPENS if '/runs_ext' in p))
rec['utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
w = G['write_json_x'](os.path.join(out, 'POST_ADOPTION_PROBE_C4V001.json'), G['jsonable'](rec))
print(json.dumps({'summary': {k: (v if not isinstance(v, (list, dict)) else len(v)) for k, v in rec['summary'].items()},
                  'blocked': rec['blocked'], 'out': w['sha256'][:16]}))
