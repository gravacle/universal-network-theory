"""Claude4 0587 part 2: derive every step-4 spec from the v006r9 orchestrator (24abe3bc), its config (721c7230) and its
generators, independently of any other agent's list. Plan-only: Context construction, Mapper.build, no stage, no solver.

Families (code citations are to the pinned bytes):
  TAIL_REANCHOR    core L84-103/L149-157 + 0557 N-1: registered A2F10 template physical + config numerics block, fresh.
  WORKERS_8        core L129-131/L142-148: a second fresh DDO154 D=4.04 run with config numerics (NO registered spec;
                   candidate here = anchor point, distinct label).
  HEADLINE_CORNER  v005 Context.probe_points L2041-2053 + capability_probe L2055-2113: 'trial' + 2^3 box corners, built by
                   ctx.mapper.build (exact launch bytes, certificate slots still PENDING).
  SENS_CORNER      0533 B4-1 / check_static_dry_cx2v006r9.py L27-32: 16 alternate-D corners (template + block).
  SENS_DISTANCE    check_static_dry_cx2v006r9.py L33-34: anchor template at D lower/upper (2).
  CAMPAIGN_W1      v005 Context L1786-1788 + plan_only: the engine seed call (mapper-built), wave 1 of the campaign.
  DECIDING_III     v006r7 DECIDING_III_PAIR_PLAN_CX2V006R7_V002 (cb42a5a3): registered files, referenced not copied.
Usage: python3 -I -B make_step4_specs_c4v001.py OUTDIR"""
import os
import sys
_C = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c4common_v001.py')
G = {'__file__': _C, '__name__': 'c4common_v001'}
exec(compile(open(_C, 'rb').read(), _C, 'exec'), G)
FENCE = G['install_fence']()            # fence_c4v002 (18510e3a), first
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
sd = os.path.join(out, 'specs')
os.mkdir(sd)
t_start = time.time()
rec = {'schema': 'C4_0587_STEP4_SPEC_INVENTORY_V001', 'utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
       'launches_performed': 0, 'tool': {'path': os.path.abspath(__file__), 'sha256': G['sha_file'](os.path.abspath(__file__))},
       'fence': {'path': FENCE.__file__, 'sha256': G['sha_file'](FENCE.__file__)}}

# 1. the orchestrator, from verified bytes, under its real path (its relative pinned loads resolve from there)
wp, wsha = G['ORCH_R9']
raw = open(wp, 'rb').read()
assert G['sha_bytes'](raw) == wsha, 'orchestrator pin'
spec_ = importlib.util.spec_from_file_location('_c4_r9_orch_gen', wp)
M = importlib.util.module_from_spec(spec_)
sys.modules[spec_.name] = M
exec(compile(raw, wp, 'exec'), M.__dict__)
O = M.O
cfgraw = open(G['CONFIG_R9'][0], 'rb').read()
assert G['sha_bytes'](cfgraw) == G['CONFIG_R9'][1], 'config pin'
cfg = json.loads(cfgraw)
# HARNESS adaptation (as Codex2's check_static_dry_cx2v006r9.py L22): an uncreated local work dir inside this folder, no
# volume. Changes only config_sha256 and the work-dir records; cache_id, base spec, mapper and every spec are unaffected.
local = copy.deepcopy(cfg)
wd = os.path.join(out, 'UNCREATED_ORCH_CONTEXT')
local['work_dir'] = wd
local['work_dir_volume'] = None
local['work_dir_identity'] = {'resolved': os.path.realpath(wd), 'volume': None, 'volume_uuid': None, 'symlinks': []}
t0 = time.time()
ctx = M.Context(local)
rec['context_seconds'] = time.time() - t0
rec['context'] = {'cache_id': ctx.cache_id, 'base_spec_sha256': ctx.base_sha256, 'seed_spec_sha256': ctx.seed_spec_sha256,
                  'template_sha256': ctx.template_sha256, 'driver': ctx.driver, 'coordinate_mode': ctx.coordinate_mode['mode'],
                  'varying_names': list(ctx.es['varying_names']), 'gates_ok': ctx.gates_ok(),
                  'gate_report': G['jsonable'](ctx.gate_report()), 'work_dir_created': os.path.exists(wd)}
template = copy.deepcopy(ctx.template)
block = copy.deepcopy(cfg['numerics']['block'])
coords = json.loads(open(G['CX2'] + '/DDO154_COORDINATES_CX2V006.json', 'rb').read())
by = {c['name']: c for c in coords['engine_coordinates']}
rows = []


def put(name, family, raw_bytes, construction, exact_launch_bytes, extra=None):
    p = os.path.join(sd, name + '.json')
    with open(p, 'xb') as f:
        f.write(raw_bytes)
    s = json.loads(raw_bytes)
    r = {'name': name, 'family': family, 'path': p, 'sha256': G['sha_bytes'](raw_bytes), 'construction': construction,
         'exact_launch_bytes': exact_launch_bytes, 'physical': s['physical'], 'tail_on': 'uv_tail' in s['numerics'],
         'certificate_slots': {k: s['numerics'].get('uv_tail', {}).get(k) for k in ('eps_certificate', 'lo_certificate')},
         'numerics_equal_config_block': s['numerics'] == block, 'admit': s.get('admit'), 'label': s.get('label')}
    if extra:
        r.update(extra)
    rows.append(r)
    return r


def hand_spec(physical_update, label):
    s = copy.deepcopy(template)
    s['numerics'] = copy.deepcopy(block)
    s['physical'].update(physical_update)
    s['label'] = label
    return s


NOTE = '; C4 0587 dry-plan TEMPLATE (EPS/LO pending); not a launch spec'
# 2. TAIL_REANCHOR: exact registered template physical (registered_anchor L88-92 binds template physical == registration)
s = hand_spec({}, 'DDO154 TAIL_REANCHOR A2F10 registered anchor, config numerics' + NOTE)
assert s['physical'] == cfg['anchor']['physical'] and s['coefficients'] == cfg['anchor']['coefficients']
put('TAIL_REANCHOR', 'TAIL_REANCHOR', O.json_bytes(s), 'template a93c95b9 + config numerics.block; label only changed', False,
    {'deciding_row': 'reanchor'})
# 3. WORKERS_8 candidate (unregistered)
s = hand_spec({}, 'DDO154 deciding workers_8 candidate at the A2F10 anchor point, config numerics' + NOTE)
put('WORKERS_8_CANDIDATE_ANCHOR', 'WORKERS_8', O.json_bytes(s),
    'CANDIDATE: template + config block (no registered workers_8 spec exists)', False, {'deciding_row': 'workers_8'})
# 4. HEADLINE corners: the orchestrator's own probe points and mapper
probe = []
for label, th in ctx.probe_points():
    b = ctx.mapper.build(th)
    nm = 'HEADLINE_' + ('TRIAL' if label == 'trial' else 'CORNER_' + ''.join(
        '1' if '=hi' in part else '0' for part in label[len('corner '):].split(',')))
    r = put(nm, 'HEADLINE_CORNER', b['raw'], 'ctx.mapper.build(probe point %r)' % label, True,
            {'probe_label': label, 'theta_key': b['key'], 'certificate_point_key': b['certificate_point_key'],
             'theta': {k: th[k] for k in ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')},
             'mapper_sha256_matches_written': b['sha256'] == G['sha_bytes'](b['raw'])})
    probe.append(r['name'])
rec['probe_points'] = probe
# 5. sensitivity corners and distance plans (Codex2 static-check construction, my labels)
free = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m')
for bits in itertools.product((0, 1), repeat=3):
    th = {n: by[n]['upper' if b else 'lower'] for n, b in zip(free, bits)}
    for mode, edge in (('LO', 'lower'), ('HI', 'upper')):
        d = by['distance_Mpc'][edge]
        s = hand_spec({'common_scale_s': th['common_scale_s'], 'gamma': th['gamma_over_Eref'] * by['Eref_base_J']['trial_value'],
                       'ell_F_m': th['ell_F_m'], 'distance_Mpc': d},
                      'DDO154 sensitivity corner C%s D_%s' % (''.join(map(str, bits)), mode) + NOTE)
        put('SENS_CORNER_C%s_D%s' % (''.join(map(str, bits)), mode), 'SENS_CORNER', O.json_bytes(s),
            'template + block; physical s, gamma=r*Eref_base trial, ell_F, D=%s (check_static_dry_cx2v006r9 L27-32)' % edge, False,
            {'distance_hex': float(d).hex(), 'bits': ''.join(map(str, bits))})
for edge in ('lower', 'upper'):
    d = by['distance_Mpc'][edge]
    s = hand_spec({'distance_Mpc': d}, 'DDO154 sensitivity distance plan D %s' % edge + NOTE)
    put('SENS_DISTANCE_%s' % edge.upper(), 'SENS_DISTANCE', O.json_bytes(s),
        'anchor template + block, D=%s (check_static_dry_cx2v006r9 L33-34)' % edge, False, {'distance_hex': float(d).hex()})
# 6. campaign wave 1: the engine seed call
b = ctx.mapper.build(ctx.seed_theta)
put('CAMPAIGN_W1_SEED', 'CAMPAIGN_W1', b['raw'], 'ctx.mapper.build(ctx.seed_theta) (to_natural at trial_u)', True,
    {'theta_key': b['key'], 'equals_ctx_seed_spec_sha256': b['sha256'] == ctx.seed_spec_sha256,
     'theta': {k: ctx.seed_theta[k] for k in ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')}})
# 7. deciding (iii): registered files (not copied)
plan = json.loads(open(G['CX2'] + '/v006r7/DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json', 'rb').read())
assert G['sha_file'](G['CX2'] + '/v006r7/DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json') == \
    'cb42a5a3bf8e26d0aa2a3a4c35784c2301fde7ff6c60170da7536ba8cfd95656'
dec = []
for key, pair in sorted(plan['pairs'].items()):
    tag = 'HIGH' if pair['distance_mpc'] > 4.04 else 'LOW'
    for role in ('new', 'reference'):
        p = pair[role]['spec']['path']
        sp = json.loads(open(p, 'rb').read())
        dec.append({'name': 'DECIDING_III_%s_%s' % (tag, 'R5' if role == 'new' else 'V009GEO'), 'family': 'DECIDING_III',
                    'path': p, 'sha256': G['sha_file'](p), 'sha256_registered': pair[role]['spec']['sha256'],
                    'driver': pair[role]['driver'], 'role': role, 'distance_hex': key, 'distance_mpc': pair['distance_mpc'],
                    'physical': sp['physical'], 'tail_on': 'uv_tail' in sp['numerics'], 'exact_launch_bytes': True,
                    'construction': 'registered v006r7 file (pair plan cb42a5a3)'})
rows.extend(dec)
# cross-checks of my construction against the registered/v006r7 artifacts
xc = {}
anchor = json.loads(open(G['R9'] + '/static_dry_v001/ANCHOR_SPEC.json', 'rb').read())
mine = json.loads(open(os.path.join(sd, 'TAIL_REANCHOR.json'), 'rb').read())
xc['tail_reanchor_vs_codex2_r9_anchor_spec_differs_only_in_label'] = (
    {k: v for k, v in anchor.items() if k != 'label'} == {k: v for k, v in mine.items() if k != 'label'})
r7 = G['CX2'] + '/v006r7/dryplans_v001'
r7cmp = {}
for r in rows:
    if r['family'] not in ('HEADLINE_CORNER', 'SENS_CORNER', 'SENS_DISTANCE'):
        continue
    if r['family'] == 'HEADLINE_CORNER' and r['name'] != 'HEADLINE_TRIAL':
        cand = 'P128_MS128_C%s_HEADLINE.json' % r['name'][-3:]
    elif r['family'] == 'SENS_CORNER':
        cand = 'P128_MS128_C%s_SENSITIVITY_%s.json' % (r['bits'], 'HI' if r['name'].endswith('DHI') else 'LO')
    elif r['family'] == 'SENS_DISTANCE':
        cand = 'P128_MS128_DISTANCE_%s.json' % r['name'].split('_')[-1]
    else:
        continue
    cp = os.path.join(r7, cand)
    if not os.path.isfile(cp):
        r7cmp[r['name']] = 'NO_R7_FILE ' + cand
        continue
    a = json.loads(open(cp, 'rb').read())
    m = json.loads(open(r['path'], 'rb').read())
    r7cmp[r['name']] = {'r7_file': cp, 'r7_sha256': G['sha_file'](cp),
                        'equal_except_label': {k: v for k, v in a.items() if k != 'label'} == {k: v for k, v in m.items() if k != 'label'},
                        'physical_equal': a.get('physical') == m.get('physical'), 'numerics_equal': a.get('numerics') == m.get('numerics')}
xc['vs_v006r7_dryplans_v001'] = r7cmp
trial = [r for r in rows if r['name'] == 'HEADLINE_TRIAL'][0]
seed = [r for r in rows if r['name'] == 'CAMPAIGN_W1_SEED'][0]
xc['trial_point_physical_equals_anchor'] = trial['physical'] == cfg['anchor']['physical']
xc['seed_physical_equals_anchor'] = seed['physical'] == cfg['anchor']['physical']
xc['seed_theta_key_equals_trial_theta_key'] = seed['theta_key'] == trial['theta_key']
xc['physical_diffs_trial_vs_anchor'] = {k: [trial['physical'][k], cfg['anchor']['physical'][k]] for k in trial['physical']
                                        if trial['physical'][k] != cfg['anchor']['physical'][k]}
xc['physical_diffs_seed_vs_anchor'] = {k: [seed['physical'][k], cfg['anchor']['physical'][k]] for k in seed['physical']
                                       if seed['physical'][k] != cfg['anchor']['physical'][k]}
dist = {r['distance_hex'] for r in rows if r['family'] in ('SENS_CORNER', 'SENS_DISTANCE')}
xc['sensitivity_distances_equal_pair_plan_keys'] = sorted(dist) == sorted(plan['pairs'])
rec['cross_checks'] = xc
rec['specs'] = rows
rec['counts'] = {f: sum(1 for r in rows if r['family'] == f) for f in sorted({r['family'] for r in rows})}
rec['blocked'] = list(FENCE.BLOCKED)
rec['opens_outside_folder'] = sorted(set(p for p in OPENS if not p.startswith(G['ROOT']) and '/python3.12/' not in p))
rec['runs_ext_opens'] = [p for p in rec['opens_outside_folder'] if '/runs_ext' in p]
rec['seconds'] = time.time() - t_start
rec['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
w = G['write_json_x'](os.path.join(out, 'SPEC_INVENTORY_C4V001.json'), G['jsonable'](rec))
print(json.dumps({'counts': rec['counts'], 'context_s': rec['context_seconds'], 'blocked': rec['blocked'],
                  'runs_ext_opens': rec['runs_ext_opens'], 'inventory': w}, default=str))
