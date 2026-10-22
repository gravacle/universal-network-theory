"""Build the worm + channel-bearing Birth pilot V004 packet from the worm V003 packet by explicit edits.

Reads (never edits) recipe V003, worker V003 and monitor V003 of worm_move_c2_0467; writes,
exclusively ('x'), next to this script:
  owned_L4_worm_birthk_recipe_v004.py, owned_L4_worm_birthk_root_worker_v004.py,
  owned_L4_worm_birthk_monitor_v004.py, unified diffs DELTA_*.diff against V003, and
  PACKET_BUILD_REPORT_V004.json.
Every edit is an exact unique-anchor replacement listed below (the delta IS this list):
  recipe  : Birth slot pin -> owned_worldline_birth_residence_transport_c2v002.py, its MODULE_VERSION
            checked in prepare, result binding names the new owner selection; nothing else.
  worker  : recipe/Birth source pins; fresh seed 2026101702; warmup 512 -> 1024 (1024 measurements
            unchanged); time-proportional caps x2 with the hard wall (soft wall 4400 -> 8800 s,
            soft/enumeration calls 1.6M -> 3.2M, total events 2.4M -> 4.8M); max_sweeps 3072 -> 4096
            (= 2 chains x 2048 sweeps); memory, output and per-path caps unchanged.
  monitor : worker V004 path and pins (+ Birth c2v002 pin); output OWNED_L4_WORM_BIRTHK_RUN_V001;
            hard wall 4500 -> 9000 s; RSS/output caps unchanged; scope/root text.
Nothing is launched; the output directory is only checked to be absent.
Usage: python3 -I -B build_worm_birthk_packet_v004.py
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
W3 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467')
PRED = {
    'recipe': (W3 / 'owned_L4_worm_loop_recipe_v003.py', '8eb46fff1f29d83fed676f7f61b469cb53495baa62d69a1ee4cfedb68aeab8ef'),
    'worker': (W3 / 'owned_L4_worm_loop_root_worker_v003.py', '3b408fb40791a60e8fa2e81083b0377e25ef7e076ee0d2a21f3148db14dd53f2'),
    'monitor': (W3 / 'owned_L4_worm_loop_monitor_v003.py', 'e7eb2622dda3adbea07494d765537af026bdaf32b308d4fc3ce5f9405fb94d64'),
}
BIRTH = HERE / 'owned_worldline_birth_residence_transport_c2v002.py'
WORM = W3 / 'owned_worm_loop_whole_path_c2v001.py'
DURABILITY = W3 / 'owned_worm_committed_capture_durability_v002.py'
FAMILY = UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py'
OUT = {'recipe': HERE / 'owned_L4_worm_birthk_recipe_v004.py',
       'worker': HERE / 'owned_L4_worm_birthk_root_worker_v004.py',
       'monitor': HERE / 'owned_L4_worm_birthk_monitor_v004.py'}
RUN_DIR = UPC / 'CODEX1' / 'OWNED_L4_WORM_BIRTHK_RUN_V001'
OLD_SEED, SEED = 2026101701, 2026101702
BIRTH_VERSION = 'birth_residence_c2v002'
SELECTION = ('Uniform among fixed-roster owners with a Birth/reverse mark at the reference dwell '
             '(one union palette enumeration); uniform mark; exact owner-count and roster Hastings factors')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def apply(src, edits, label):
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            raise ValueError(label + ': anchor occurs %d times: %r' % (n, old[:120]))
        src = src.replace(old, new)
    return src


def recipe_edits(birth_sha):
    return [
        ('''"""Inert worm-loop successor (V003) of owned_L4_current_graph_cycle_recipe_v001.py (76781f18...).
DELTA ONLY:''', '''"""Inert worm-loop + channel-bearing Birth successor (V004) of owned_L4_worm_loop_recipe_v003.py (8eb46fff...).
V004 DELTA ONLY: the .20 Birth-residence slot runs owned_worldline_birth_residence_transport_c2v002.py
(owner drawn uniformly among the owners WITH a Birth/reverse mark at the reference dwell, exact
owner-count Hastings factor) instead of the reviewed V001 transport (6f866bda...); same weight, thresholds,
owner roster and target.  V003 text follows.
V003 DELTA:'''),
        ("BIRTH_SHA='6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8'\n",
         "BIRTH_SHA='" + birth_sha + "'\nBIRTH_MODULE_VERSION='" + BIRTH_VERSION + "'\n"),
        ("            or worm_module.LOOKAHEAD is not WORM_LOOKAHEAD):raise ValueError('Fixed worm-loop walk rule changed')\n",
         "            or worm_module.LOOKAHEAD is not WORM_LOOKAHEAD):raise ValueError('Fixed worm-loop walk rule changed')\n"
         "    if getattr(birth_module,'MODULE_VERSION',None)!=BIRTH_MODULE_VERSION:raise ValueError('Channel-bearing-owner Birth transport c2v002 required')\n"),
        ("'birth_module_sha256':BIRTH_SHA,'fixed_birth_owner_roster':b['owner_roster'],",
         "'birth_module_sha256':BIRTH_SHA,'birth_module_version':BIRTH_MODULE_VERSION,'birth_owner_selection':'"
         + SELECTION + "','fixed_birth_owner_roster':b['owner_roster'],"),
    ]


def worker_edits(recipe_sha, birth_sha):
    return [
        ('''"""Inert root-only worm-loop/admission/family-pair capture worker V003 (delta of cycle worker V002 2237a155...).
Requires external 4500s/4GiB RSS/2GiB output guard; inherited soft4400s/3.5GiB.
Same physical TRIAL, 512 warmup,1024 measurements,2 chains,5 moves/sweep.
Fixed mixture: .25 occupancy,.10 worm loop (replaces the current-graph cycle slot),.20 Birth residence,.20 admission residence,.25 prior base. Fresh seed2026101701
is bound after preparation and before any sampling. No acceptance or retries.''',
         '''"""Inert root-only worm-loop/channel-bearing-Birth/admission/family-pair capture worker V004 (delta of worm worker V003 3b408fb4...).
Requires external 9000s/4GiB RSS/2GiB output guard; soft8800s/3.5GiB/3.2million calls (time-proportional caps x2).
Same physical TRIAL, 1024 warmup (doubled),1024 measurements,2 chains,5 moves/sweep; max_sweeps 4096.
Fixed mixture: .25 occupancy,.10 worm loop,.20 Birth residence (c2v002: owner uniform among channel-bearing owners),.20 admission residence,.25 prior base. Fresh seed2026101702
is bound after preparation and before any sampling. No acceptance or retries.'''),
        ("import math\nfrom pathlib import Path\n", "import math\nfrom pathlib import Path\nimport resource\n"),
        ("    'recipe': (X/'worm_move_c2_0467/owned_L4_worm_loop_recipe_v003.py', '8eb46fff1f29d83fed676f7f61b469cb53495baa62d69a1ee4cfedb68aeab8ef'),\n",
         "    'recipe': (X/'birth_kinetics_c2/owned_L4_worm_birthk_recipe_v004.py', '" + recipe_sha + "'),\n"),
        ("    'birth_module': (B/'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py', '6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8'),\n",
         "    'birth_module': (X/'birth_kinetics_c2/owned_worldline_birth_residence_transport_c2v002.py', '" + birth_sha + "'),\n"),
        ("""                    raise ValueError('Frozen sampling schedule mismatch')
                old_seed=prepared['reweighting_capture_record']['rng_entropy']
""", """                    raise ValueError('Frozen sampling schedule mismatch')
                if (args['caps']!={'max_events_per_path':10000,'max_total_events':2400000,'max_sweeps':3072,'max_channel_enumerations':1600000}
                    or prepared['reweighting_capture_record']['burn_in_per_chain']!=512):
                    raise ValueError('Frozen caps/capture record mismatch')
                # V004: warmup doubled to 1024 (measurements stay 1024); time-proportional caps scaled x2 with
                # the hard wall (4500s->9000s); RSS, output and per-path caps unchanged; max_sweeps=2*(1024+1024).
                args['burn_in_sweeps']=1024
                prepared['reweighting_capture_record']['burn_in_per_chain']=1024
                args['caps']={'max_events_per_path':10000,'max_total_events':4800000,'max_sweeps':4096,'max_channel_enumerations':3200000}
                clock=prepared['counters']
                def budget_state():
                    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    rb=rss if sys.platform=='darwin' else rss*1024
                    elapsed=time.monotonic()-clock['start']
                    return {'elapsed_seconds':elapsed,'peak_rss_bytes':rb,'primitive_calls':clock['primitive_calls'],
                            'stop_requested':elapsed>=8800. or rb>=3584*1024**2 or clock['primitive_calls']>=3200000}
                prepared['budget_state']=budget_state
                args['budget_hook']=lambda: bool(budget_state()['stop_requested'])
                result['schedule_binding']={'burn_in_sweeps':1024,'measurement_sweeps':1024,'chains':2,'moves_per_sweep':5,
                    'prepared_burn_in_sweeps':512,'caps':dict(args['caps']),'prepared_caps':{'max_events_per_path':10000,
                    'max_total_events':2400000,'max_sweeps':3072,'max_channel_enumerations':1600000},
                    'soft_budget':{'wall_seconds':8800.,'peak_rss_bytes':3584*1024**2,'primitive_calls':3200000},
                    'prepared_soft_budget':{'wall_seconds':4400.,'peak_rss_bytes':3584*1024**2,'primitive_calls':1600000},
                    'method':'replaced after preparation and before sampling; budget clock and guarded call counter are the prepared ones'}
                old_seed=prepared['reweighting_capture_record']['rng_entropy']
"""),
        ("""                args['chain_generators']=[np.random.default_rng(s) for s in np.random.SeedSequence(%d).spawn(2)]
                prepared['reweighting_capture_record']['rng_entropy']=%d
                result['rng_binding']={'prepared_recipe_entropy':old_seed,'actual_entropy':%d,""" % (OLD_SEED, OLD_SEED, OLD_SEED),
         """                args['chain_generators']=[np.random.default_rng(s) for s in np.random.SeedSequence(%d).spawn(2)]
                prepared['reweighting_capture_record']['rng_entropy']=%d
                result['rng_binding']={'prepared_recipe_entropy':old_seed,'actual_entropy':%d,""" % (SEED, SEED, SEED)),
        ("                print('Sampling two chains with fixed worm-loop/occupancy/family-pair mixture', flush=True)\n",
         "                result['birth_residence_request']={'module_version':modules['birth_module'].MODULE_VERSION,\n"
         "                    'total_birth_residence_probability':.20,'fixed_owner_roster':prepared['worm_binding']['owner_roster'],\n"
         "                    'selection':'" + SELECTION + "'}\n"
         "                print('Sampling two chains with fixed worm-loop/channel-bearing-Birth/occupancy/family-pair mixture', flush=True)\n"),
    ]


def monitor_edits(worker_sha, recipe_sha, birth_sha, monitor_src):
    import ast
    import re
    old_line = re.search(r"^pins=\{Path\(p\):s for p,s in \{.*?\}\.items\(\)\}$", monitor_src, re.M).group(0)
    pins = {str(OUT['worker']): worker_sha, str(FAMILY): sha(FAMILY), str(OUT['recipe']): recipe_sha,
            str(WORM): sha(WORM), str(DURABILITY): sha(DURABILITY), str(BIRTH): birth_sha}
    old_pins = ast.literal_eval(old_line[len('pins={Path(p):s for p,s in '):-len('.items()}')])
    assert old_pins[str(FAMILY)] == pins[str(FAMILY)] and old_pins[str(WORM)] == pins[str(WORM)]
    assert old_pins[str(DURABILITY)] == pins[str(DURABILITY)]
    return [
        ("worker=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_L4_worm_loop_root_worker_v003.py')\n",
         "worker=Path(" + repr(str(OUT['worker'])) + ")\n"),
        (old_line, "pins={Path(p):s for p,s in " + repr(pins) + ".items()}"),
        ("out=b/'OWNED_L4_WORM_LOOP_RUN_V001'\n", "out=b/'OWNED_L4_WORM_BIRTHK_RUN_V001'\n"),
        ("'scope':'Occupancy-guided long alternating-loop (worm) whole-path transport replacing the current-graph cycle slot, fixed original start roster and unchanged native target; actual response-observable mixing required.'",
         "'scope':'Worm V003 mixture with the Birth-residence slot drawing its owner uniformly among channel-bearing owners (exact owner-count Hastings factor), doubled warmup, unchanged native target; actual census/U stationarity and response-observable mixing required.'"),
        ("'wall_cap_seconds':4500.0,", "'wall_cap_seconds':9000.0,"),
        ("record['root_acceptance']='Root decision A2 (ROOT_DECISIONS_A1_A2_2026-10-17_V001) selected the occupancy-guided long alternating-loop whole-path move to replace the current-graph cycle slot; seed%d,2chains512warmup1024measurements,5moves. Same physical target,25%%occupancy/10%%worm-loop/20%%Birth/20%%admission/25%%base. Hard4500s/4GiB/output2GiB; soft4400s/3.5GiB;1.6millioncalls/2.4millionevents. Preserve old failed pilots; no tail truncation, exact restart or mixing guarantee. Durable16-row capture plus reference key, Birth census and U per row (durability V002). Exact-byte distinct review is separately required before root launch; acceptance counts alone do not establish improved response mixing.'" % OLD_SEED,
         "record['root_acceptance']='Reviewed WORM_PILOT_EVALUATION_V001 (section 7) next remedy on the worm V003 packet: the Birth-residence slot draws its owner uniformly among owners with a Birth/reverse mark at the reference dwell, exact owner-count Hastings factor (owned_worldline_birth_residence_transport_c2v002); warmup doubled. Seed%d,2chains1024warmup1024measurements,5moves,max_sweeps4096. Same physical target,25%%occupancy/10%%worm-loop/20%%Birth/20%%admission/25%%base. Hard9000s/4GiB/output2GiB; soft8800s/3.5GiB;3.2millioncalls/4.8millionevents (time-proportional caps x2). Preserve old pilots; no tail truncation, exact restart or mixing guarantee. Durable16-row capture plus reference key, Birth census and U per row (durability V002, unchanged). Exact-byte distinct review is separately required before root launch; acceptance counts alone do not establish census/U stationarity or improved response mixing.'" % SEED),
    ]


def write_x(path, text):
    with Path(path).open('x') as f:
        f.write(text)


def diff(a_path, b_text, b_name):
    a = Path(a_path).read_text().splitlines(keepends=True)
    return ''.join(difflib.unified_diff(a, b_text.splitlines(keepends=True), fromfile=str(a_path), tofile=b_name))


def main():
    for k, (p, s) in PRED.items():
        if sha(p) != s:
            raise ValueError('predecessor changed: ' + str(p))
    if RUN_DIR.exists():
        raise ValueError('pilot output directory already exists: ' + str(RUN_DIR))
    birth_sha = sha(BIRTH)
    recipe = apply(PRED['recipe'][0].read_text(), recipe_edits(birth_sha), 'recipe')
    write_x(OUT['recipe'], recipe)
    recipe_sha = sha(OUT['recipe'])
    worker = apply(PRED['worker'][0].read_text(), worker_edits(recipe_sha, birth_sha), 'worker')
    write_x(OUT['worker'], worker)
    worker_sha = sha(OUT['worker'])
    msrc = PRED['monitor'][0].read_text()
    medits = monitor_edits(worker_sha, recipe_sha, birth_sha, msrc)
    write_x(OUT['monitor'], apply(msrc, medits, 'monitor'))
    report = {'predecessors': {k: {'path': str(p), 'sha256': s} for k, (p, s) in PRED.items()},
              'generated': {k: {'path': str(v), 'sha256': sha(v)} for k, v in OUT.items()},
              'birth_module': {'path': str(BIRTH), 'sha256': birth_sha, 'module_version': BIRTH_VERSION},
              'unchanged_worm_module_sha256': sha(WORM), 'unchanged_durability_sha256': sha(DURABILITY),
              'edit_counts': {'recipe': len(recipe_edits(birth_sha)), 'worker': len(worker_edits(recipe_sha, birth_sha)),
                              'monitor': len(medits)},
              'pilot_output_directory': str(RUN_DIR), 'pilot_output_directory_absent_at_build': True,
              'fresh_seed': SEED, 'burn_in_sweeps': 1024, 'measurement_sweeps': 1024}
    for k in OUT:
        d = diff(PRED[k][0], Path(OUT[k]).read_text(), str(OUT[k]))
        dp = HERE / ('DELTA_' + OUT[k].stem + '.diff')
        write_x(dp, d)
        report['generated'][k]['delta_diff'] = {'path': str(dp), 'sha256': sha(dp)}
    d = diff(Path(UPC / 'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py'),
             BIRTH.read_text(), str(BIRTH))
    dp = HERE / 'DELTA_owned_worldline_birth_residence_transport_c2v002.diff'
    write_x(dp, d)
    report['birth_delta_diff'] = {'path': str(dp), 'sha256': sha(dp)}
    rp = HERE / 'PACKET_BUILD_REPORT_V004.json'
    write_x(rp, json.dumps(report, indent=1) + '\n')
    print(json.dumps({'ok': True, 'report': str(rp)}))


if __name__ == '__main__':
    main()
