"""Build the worm-loop pilot V003 packet files from their reviewed predecessors by explicit edits.

Reads (never edits) recipe V001, worker V002 and monitor V002 of the current-graph cycle packet;
writes, exclusively ('x'), next to this script:
  owned_L4_worm_loop_recipe_v003.py, owned_L4_worm_loop_root_worker_v003.py,
  owned_L4_worm_loop_monitor_v003.py, and unified diffs DELTA_*.diff against the predecessors.
Every edit is an exact unique anchor replacement listed below (the delta IS this list).  Nothing is
launched; the monitor's output directory is only checked to be absent.
Usage: python3 -I -B build_worm_pilot_packet_v003.py
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
AI = UPC / 'helpers/admission_integration'
PRED = {
    'recipe': (AI / 'owned_L4_current_graph_cycle_recipe_v001.py', '76781f18e852a1368ec2216b15a04c3525435efe2e11cded3155417a239eb203'),
    'worker': (AI / 'owned_L4_current_graph_cycle_root_worker_v002.py', '2237a1551bc70dc3e0690d7156c1de47e6131b1eb7c9c30476f7f3a919f68b13'),
    'monitor': (AI / 'owned_L4_current_graph_cycle_monitor_v002.py', 'fb194dfb2cbbb39a610d127cbba6d39575f0b7fb6330534c53f6bcee11519f36'),
}
WORM = HERE / 'owned_worm_loop_whole_path_c2v001.py'
DURABILITY = HERE / 'owned_worm_committed_capture_durability_v002.py'
OUT = {'recipe': HERE / 'owned_L4_worm_loop_recipe_v003.py',
       'worker': HERE / 'owned_L4_worm_loop_root_worker_v003.py',
       'monitor': HERE / 'owned_L4_worm_loop_monitor_v003.py'}
RUN_DIR = UPC / 'CODEX1' / 'OWNED_L4_WORM_LOOP_RUN_V001'
SEED = 2026101701


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def apply(src, edits, label):
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            raise ValueError(label + ': anchor occurs %d times: %r' % (n, old[:120]))
        src = src.replace(old, new)
    return src


def recipe_edits(worm_sha):
    return [
        ('''"""Inert current-graph cycle successor of the reviewed admission-residence recipe.
Fixed total mixture .25 current-graph occupancy, .10 current-graph even cycles, .20 Birth residence, .20 admission residence,
.25 prior base; all original model/response diagnostics retained. No adaptation.
Whole-path resource transport does not add physical events or physical rates.
"""''', '''"""Inert worm-loop successor (V003) of owned_L4_current_graph_cycle_recipe_v001.py (76781f18...).
DELTA ONLY: the .10 current-graph even-cycle slot is replaced by the occupancy-guided long
alternating-loop ("worm") whole-path move owned_worm_loop_whole_path_c2v001.py at the SAME weight
(2/15 of the .75 base wrapper = .10 total) and the SAME uniform-u branch thresholds; every other
branch, module, pin, owner roster, target and diagnostic is unchanged.
Fixed total mixture .25 current-graph occupancy, .10 worm loop, .20 Birth residence, .20 admission residence,
.25 prior base; all original model/response diagnostics retained. No adaptation.
Whole-path resource transport does not add physical events or physical rates.
"""'''),
        ("CYCLE_SHA='6761d843a658b803354f67d08908342869f272a4ca39d4bb964355fd21815340'\n",
         "WORM_SHA='" + worm_sha + "'\nWORM_MODULE_VERSION='worm_c2v001'\nWORM_MAX_WALK_STEPS=1024\nWORM_LOOKAHEAD=True\n"),
        ("def prepare(*,family_recipe,cycle_module,birth_module,admission_module,",
         "def prepare(*,family_recipe,worm_module,birth_module,admission_module,"),
        ("_pin(admission_module,ADMISSION_SHA);_pin(family_recipe,FAMILY_RECIPE_SHA);_pin(cycle_module,CYCLE_SHA);_pin(birth_module,BIRTH_SHA)\n    prepared=",
         "_pin(admission_module,ADMISSION_SHA);_pin(family_recipe,FAMILY_RECIPE_SHA);_pin(worm_module,WORM_SHA);_pin(birth_module,BIRTH_SHA)\n    prepared="),
        ("    if tuple(cycle_module.LENGTHS)!=(4,6,8):raise ValueError('Fixed cycle length mixture changed')\n",
         "    if (worm_module.MODULE_VERSION!=WORM_MODULE_VERSION or worm_module.MAX_WALK_STEPS!=WORM_MAX_WALK_STEPS\n"
         "            or worm_module.LOOKAHEAD is not WORM_LOOKAHEAD):raise ValueError('Fixed worm-loop walk rule changed')\n"),
        ("""    prepared['current_cycle_binding']={'module':cycle_module,'family_recipe':family_recipe,'state_labels':operator_module.state_labels,
      'birth_module':birth_module,'admission_module':admission_module,'owner_roster':original_vertices,'counters':{},'scope':'Uniform fixed original anchor and length4/6/8; uniform all simple current-graph cycles through anchor, never occupancy eligibility; exact native guards and weights.'}""",
         """    prepared['worm_binding']={'module':worm_module,'family_recipe':family_recipe,'state_labels':operator_module.state_labels,
      'birth_module':birth_module,'admission_module':admission_module,'owner_roster':original_vertices,'counters':{},'scope':'Uniform fixed original A+B start, uniform viable occupied first edge, uniform viable alternating continuation on the whole-path eligible graph until the first revisit; exact reverse-walk Hastings factor; exact native guards, event replay and weights.'}"""),
        ("""def _admission_diagnostic_update(run, old_path, new_path, diag):""",
         """def branch_of(u):
    \"\"\"V001 thresholds unchanged: [0,2/15) worm loop (was current_cycle), [2/15,6/15) Birth, [6/15,10/15) admission, else base.\"\"\"
    return 'worm_loop' if u<2./15. else ('birth_residence' if u<6./15. else ('admission_residence' if u<10./15. else 'prior_base'))


def _admission_diagnostic_update(run, old_path, new_path, diag):"""),
        ("""    b=prepared['current_cycle_binding'];recipe=b['family_recipe'];cyclemod=b['module'];sampler=prepared['sampler_module']
    _pin(b['admission_module'],ADMISSION_SHA);_pin(recipe,FAMILY_RECIPE_SHA);_pin(cyclemod,CYCLE_SHA);_pin(b['birth_module'],BIRTH_SHA)
    if getattr(sampler,'_current_cycle_recipe_active',False) or getattr(sampler,'_recipe_occupancy_mixture_active',False):raise RuntimeError('Concurrent/nested recipe patch forbidden')""",
         """    b=prepared['worm_binding'];recipe=b['family_recipe'];wormmod=b['module'];sampler=prepared['sampler_module']
    _pin(b['admission_module'],ADMISSION_SHA);_pin(recipe,FAMILY_RECIPE_SHA);_pin(wormmod,WORM_SHA);_pin(b['birth_module'],BIRTH_SHA)
    if (getattr(sampler,'_worm_loop_recipe_active',False) or getattr(sampler,'_current_cycle_recipe_active',False)
            or getattr(sampler,'_recipe_occupancy_mixture_active',False)):raise RuntimeError('Concurrent/nested recipe patch forbidden')"""),
        ("""    def cycle_mixture(run,path,rng,diag):
        sampler._budget_check(run,'before','current-graph cycle/base mixture')
        u=float(rng.random());branch='current_cycle' if u<2./15. else ('birth_residence' if u<6./15. else ('admission_residence' if u<10./15. else 'prior_base'));tick(branch+'_selected')
        try:
            if branch=='current_cycle':answer=cyclemod.move(run,path,rng,diag,sampler,b['owner_roster'],b['state_labels'])""",
         """    def worm_mixture(run,path,rng,diag):
        sampler._budget_check(run,'before','worm-loop/base mixture')
        u=float(rng.random());branch=branch_of(u);tick(branch+'_selected')
        try:
            if branch=='worm_loop':answer=wormmod.move(run,path,rng,diag,sampler,b['owner_roster'],b['state_labels'])"""),
        ("    sampler._current_cycle_recipe_active=True;sampler._move=cycle_mixture\n",
         "    sampler._worm_loop_recipe_active=True;sampler._move=worm_mixture\n"),
        ("""        result['current_cycle_binding']={'module_sha256':CYCLE_SHA,'family_recipe_sha256':FAMILY_RECIPE_SHA,
          'fixed_cycle_lengths':cyclemod.LENGTHS,'fixed_cycle_anchor_roster':b['owner_roster'],'cycle_selection':'Uniform anchor, uniform length, uniform graph-only simple cycle; empty roster rejects without resampling','maximum_enumeration_visits':cyclemod.MAX_ENUMERATION_VISITS,'maximum_cycles_per_anchor_length':cyclemod.MAX_CYCLES_PER_ANCHOR_LENGTH,'birth_module_sha256':BIRTH_SHA,'fixed_birth_owner_roster':b['owner_roster'],'fixed_admission_owner_roster':b['owner_roster'],
          'total_cycle_probability':.10,""",
         """        result['worm_binding']={'module_sha256':WORM_SHA,'module_version':WORM_MODULE_VERSION,'family_recipe_sha256':FAMILY_RECIPE_SHA,
          'fixed_start_roster':b['owner_roster'],'walk_selection':'Uniform original start, uniform viable occupied first edge, uniform viable alternating continuation until first revisit; empty start/dead end/cap reject without resampling','maximum_walk_steps':wormmod.MAX_WALK_STEPS,'lookahead':wormmod.LOOKAHEAD,'birth_module_sha256':BIRTH_SHA,'fixed_birth_owner_roster':b['owner_roster'],'fixed_admission_owner_roster':b['owner_roster'],
          'total_worm_loop_probability':.10,"""),
        ("        sampler._move=original;del sampler._current_cycle_recipe_active",
         "        sampler._move=original;del sampler._worm_loop_recipe_active"),
    ]


def worker_edits(recipe_sha, worm_sha, durability_sha):
    X = "X/'worm_move_c2_0467/"
    return [
        ('''"""Inert root-only current-graph cycle/admission/family-pair capture worker.
Requires external 4500s/4GiB RSS/2GiB output guard; inherited soft4400s/3.5GiB.
Same physical TRIAL, 512 warmup,1024 measurements,2 chains,5 moves/sweep.
Fixed mixture: .25 occupancy,.10 current-graph cycles,.20 Birth residence,.20 admission residence,.25 prior base. Fresh seed2026101612
is bound after preparation and before any sampling. No acceptance or retries.
"""''', '''"""Inert root-only worm-loop/admission/family-pair capture worker V003 (delta of cycle worker V002 2237a155...).
Requires external 4500s/4GiB RSS/2GiB output guard; inherited soft4400s/3.5GiB.
Same physical TRIAL, 512 warmup,1024 measurements,2 chains,5 moves/sweep.
Fixed mixture: .25 occupancy,.10 worm loop (replaces the current-graph cycle slot),.20 Birth residence,.20 admission residence,.25 prior base. Fresh seed2026101701
is bound after preparation and before any sampling. No acceptance or retries.
Durable rows additionally carry the reference-dwell canonical key, Birth census and defect content U (durability V002).
"""'''),
        ("    'durability': (B/'helpers/admission_integration/owned_current_cycle_committed_capture_durability_v001.py', '5cb29e780fd956d1247de6047a097087da82f43b31cfaa57f661ff255076c0da'),\n",
         "    'durability': (" + X + "owned_worm_committed_capture_durability_v002.py', '" + durability_sha + "'),\n"),
        ("    'recipe': (B/'helpers/admission_integration/owned_L4_current_graph_cycle_recipe_v001.py', '76781f18e852a1368ec2216b15a04c3525435efe2e11cded3155417a239eb203'),\n",
         "    'recipe': (" + X + "owned_L4_worm_loop_recipe_v003.py', '" + recipe_sha + "'),\n"),
        ("    'cycle_module': (B/'helpers/admission_integration/owned_current_graph_cycle_occupancy_v001.py', '6761d843a658b803354f67d08908342869f272a4ca39d4bb964355fd21815340'),\n",
         "    'worm_module': (" + X + "owned_worm_loop_whole_path_c2v001.py', '" + worm_sha + "'),\n"),
        ("                    cycle_module=modules['cycle_module'],birth_module=",
         "                    worm_module=modules['worm_module'],birth_module="),
        ("                args['chain_generators']=[np.random.default_rng(s) for s in np.random.SeedSequence(2026101612).spawn(2)]\n                prepared['reweighting_capture_record']['rng_entropy']=2026101612\n                result['rng_binding']={'prepared_recipe_entropy':old_seed,'actual_entropy':2026101612,",
         "                args['chain_generators']=[np.random.default_rng(s) for s in np.random.SeedSequence(%d).spawn(2)]\n                prepared['reweighting_capture_record']['rng_entropy']=%d\n                result['rng_binding']={'prepared_recipe_entropy':old_seed,'actual_entropy':%d," % (SEED, SEED, SEED)),
        ("""                result['current_cycle_request']={'probability_within_base':2./15.,
                    'total_current_cycle_probability':.75*(2./15.),'total_occupancy_probability':.25,'total_admission_residence_probability':.20,
                    'total_birth_residence_probability':.20,'total_prior_base_probability':.25,
                    'fixed_anchor_roster':prepared['current_cycle_binding']['owner_roster'],'fixed_lengths':modules['cycle_module'].LENGTHS,'selection':'Uniform fixed original anchor; uniform length; uniform graph-only cycle, no eligibility resampling'}""",
         """                result['worm_loop_request']={'probability_within_base':2./15.,
                    'total_worm_loop_probability':.75*(2./15.),'total_occupancy_probability':.25,'total_admission_residence_probability':.20,
                    'total_birth_residence_probability':.20,'total_prior_base_probability':.25,
                    'fixed_start_roster':prepared['worm_binding']['owner_roster'],'maximum_walk_steps':modules['worm_module'].MAX_WALK_STEPS,'lookahead':modules['worm_module'].LOOKAHEAD,'selection':'Uniform fixed original start; uniform viable occupied first edge; uniform viable alternating continuation until first revisit; exact reverse-walk Hastings factor; no eligibility resampling'}"""),
        ("                print('Sampling two chains with fixed current-cycle/occupancy/family-pair mixture', flush=True)",
         "                print('Sampling two chains with fixed worm-loop/occupancy/family-pair mixture', flush=True)"),
        ("                    clean=clean,pins=result['source_pins'])\n",
         "                    clean=clean,pins=result['source_pins'],state_labels=modules['operator'].state_labels,\n                    dstar=modules['family_recipe'].TRIAL['dstar'])\n"),
        ("            result['current_cycle_counters']=dict(prepared['current_cycle_binding']['counters'])\n",
         "            result['worm_counters']=dict(prepared['worm_binding']['counters'])\n"),
    ]


def monitor_edits(worker_sha, recipe_sha, worm_sha, durability_sha):
    w = str(OUT['worker'])
    pins = {w: worker_sha,
            '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py': '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7',
            str(OUT['recipe']): recipe_sha, str(WORM): worm_sha, str(DURABILITY): durability_sha}
    old_pins = "pins={Path(p):s for p,s in {'/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/admission_integration/owned_L4_current_graph_cycle_root_worker_v002.py': '2237a1551bc70dc3e0690d7156c1de47e6131b1eb7c9c30476f7f3a919f68b13', '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py': '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7', '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/admission_integration/owned_L4_current_graph_cycle_recipe_v001.py': '76781f18e852a1368ec2216b15a04c3525435efe2e11cded3155417a239eb203'}.items()}"
    return [
        ("worker=x/'owned_L4_current_graph_cycle_root_worker_v002.py'\n", "worker=Path(" + repr(w) + ")\n"),
        (old_pins, "pins={Path(p):s for p,s in " + repr(pins) + ".items()}"),
        ("out=b/'OWNED_L4_CURRENT_GRAPH_CYCLE_RUN_V001'\n", "out=b/'OWNED_L4_WORM_LOOP_RUN_V001'\n"),
        ("'scope':'Targeted current-graph cycle occupancy transport with fixed original-anchor roster and unchanged native target; actual response-observable mixing required.'",
         "'scope':'Occupancy-guided long alternating-loop (worm) whole-path transport replacing the current-graph cycle slot, fixed original start roster and unchanged native target; actual response-observable mixing required.'"),
        ("record['root_acceptance']='Root selected current-graph cycles to replace the measured dead fixed graph0 hex proposal; seed2026101612,2chains512warmup1024measurements,5moves. Same physical target,25%occupancy/10%current-graph-cycle/20%Birth/20%admission/25%base. Hard4500s/4GiB/output2GiB; soft4400s/3.5GiB;1.6millioncalls/2.4millionevents. Preserve old failed pilots; no tail truncation, exact restart or mixing guarantee. Durable16-row capture unchanged. Exact-byte distinct review is separately required before root launch; acceptance counts alone do not establish improved response mixing.'",
         "record['root_acceptance']='Root decision A2 (ROOT_DECISIONS_A1_A2_2026-10-17_V001) selected the occupancy-guided long alternating-loop whole-path move to replace the current-graph cycle slot; seed%d,2chains512warmup1024measurements,5moves. Same physical target,25%%occupancy/10%%worm-loop/20%%Birth/20%%admission/25%%base. Hard4500s/4GiB/output2GiB; soft4400s/3.5GiB;1.6millioncalls/2.4millionevents. Preserve old failed pilots; no tail truncation, exact restart or mixing guarantee. Durable16-row capture plus reference key, Birth census and U per row (durability V002). Exact-byte distinct review is separately required before root launch; acceptance counts alone do not establish improved response mixing.'" % SEED),
    ]


def write_x(path, text):
    with Path(path).open('x') as f:
        f.write(text)


def diff(a_path, b_text, b_name):
    a = Path(a_path).read_text().splitlines(keepends=True)
    b = b_text.splitlines(keepends=True)
    return ''.join(difflib.unified_diff(a, b, fromfile=str(a_path), tofile=b_name))


def main():
    for k, (p, s) in PRED.items():
        if sha(p) != s:
            raise ValueError('predecessor changed: ' + str(p))
    if RUN_DIR.exists():
        raise ValueError('pilot output directory already exists: ' + str(RUN_DIR))
    worm_sha, durability_sha = sha(WORM), sha(DURABILITY)
    recipe = apply(PRED['recipe'][0].read_text(), recipe_edits(worm_sha), 'recipe')
    write_x(OUT['recipe'], recipe)
    recipe_sha = sha(OUT['recipe'])
    worker = apply(PRED['worker'][0].read_text(), worker_edits(recipe_sha, worm_sha, durability_sha), 'worker')
    write_x(OUT['worker'], worker)
    worker_sha = sha(OUT['worker'])
    monitor = apply(PRED['monitor'][0].read_text(), monitor_edits(worker_sha, recipe_sha, worm_sha, durability_sha), 'monitor')
    write_x(OUT['monitor'], monitor)
    report = {'predecessors': {k: {'path': str(p), 'sha256': s} for k, (p, s) in PRED.items()},
              'generated': {k: {'path': str(v), 'sha256': sha(v)} for k, v in OUT.items()},
              'worm_module_sha256': worm_sha, 'durability_sha256': durability_sha,
              'edit_counts': {'recipe': len(recipe_edits(worm_sha)),
                              'worker': len(worker_edits(recipe_sha, worm_sha, durability_sha)),
                              'monitor': len(monitor_edits(worker_sha, recipe_sha, worm_sha, durability_sha))},
              'pilot_output_directory': str(RUN_DIR), 'pilot_output_directory_absent_at_build': True,
              'fresh_seed': SEED}
    for k in OUT:
        d = diff(PRED[k][0], Path(OUT[k]).read_text(), str(OUT[k]))
        dp = HERE / ('DELTA_' + OUT[k].stem + '.diff')
        write_x(dp, d)
        report['generated'][k]['delta_diff'] = {'path': str(dp), 'sha256': sha(dp)}
    durability_pred = AI / 'owned_current_cycle_committed_capture_durability_v001.py'
    d = diff(durability_pred, DURABILITY.read_text(), str(DURABILITY))
    dp = HERE / 'DELTA_owned_worm_committed_capture_durability_v002.diff'
    write_x(dp, d)
    report['durability_delta_diff'] = {'path': str(dp), 'sha256': sha(dp),
                                       'predecessor': {'path': str(durability_pred), 'sha256': sha(durability_pred)}}
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
