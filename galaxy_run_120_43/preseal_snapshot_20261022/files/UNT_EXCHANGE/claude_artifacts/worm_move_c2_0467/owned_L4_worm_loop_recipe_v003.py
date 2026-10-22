"""Inert worm-loop successor (V003) of owned_L4_current_graph_cycle_recipe_v001.py (76781f18...).
DELTA ONLY: the .10 current-graph even-cycle slot is replaced by the occupancy-guided long
alternating-loop ("worm") whole-path move owned_worm_loop_whole_path_c2v001.py at the SAME weight
(2/15 of the .75 base wrapper = .10 total) and the SAME uniform-u branch thresholds; every other
branch, module, pin, owner roster, target and diagnostic is unchanged.
Fixed total mixture .25 current-graph occupancy, .10 worm loop, .20 Birth residence, .20 admission residence,
.25 prior base; all original model/response diagnostics retained. No adaptation.
Whole-path resource transport does not add physical events or physical rates.
"""
import hashlib
import math
from pathlib import Path

ADMISSION_SHA='5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653' # Frozen Claude3 release, independently reviewed by Claude4
FAMILY_RECIPE_SHA='86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7'
BIRTH_SHA='6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8'
WORM_SHA='9fef6042eb1e13157d19a4d4381b4c73ef6e26d779f49ad7c477f1d44b9f470d'
WORM_MODULE_VERSION='worm_c2v001'
WORM_MAX_WALK_STEPS=1024
WORM_LOOKAHEAD=True


def _pin(module,expected):
    if hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()!=expected:raise ValueError('Frozen module changed: '+str(module.__file__))


def prepare(*,family_recipe,worm_module,birth_module,admission_module,
            operator_module,sampler_module,diamond_adapter,progress_stream,
            occupancy_module,statistics_module,accepted_sampler_sha256):
    _pin(admission_module,ADMISSION_SHA);_pin(family_recipe,FAMILY_RECIPE_SHA);_pin(worm_module,WORM_SHA);_pin(birth_module,BIRTH_SHA)
    prepared=family_recipe.prepare(operator_module=operator_module,sampler_module=sampler_module,
      diamond_adapter=diamond_adapter,progress_stream=progress_stream,occupancy_module=occupancy_module,
      statistics_module=statistics_module,accepted_sampler_sha256=accepted_sampler_sha256)
    original_vertices=tuple(prepared['binding']['graph0']['A'])+tuple(prepared['binding']['graph0']['B'])
    if not original_vertices or len(set(original_vertices))!=len(original_vertices):
        raise ValueError('Original A+B labels must be nonempty and unique')
    if set(original_vertices)!={v for e in prepared['edge_roster'] for v in e}:
        raise ValueError('Edge endpoints do not cover precisely the original A+B vertices')
    palette=prepared['arguments'].get('palette_parameters')
    if not isinstance(palette,dict) or tuple((w,tuple(vs)) for w,vs in palette['palettes'])!=tuple((1.,(v,)) for v in original_vertices):
        raise ValueError('Full original A+B palette binding required')
    if (worm_module.MODULE_VERSION!=WORM_MODULE_VERSION or worm_module.MAX_WALK_STEPS!=WORM_MAX_WALK_STEPS
            or worm_module.LOOKAHEAD is not WORM_LOOKAHEAD):raise ValueError('Fixed worm-loop walk rule changed')
    if not callable(getattr(operator_module,'state_labels',None)):raise ValueError('Public native state_labels required')
    prepared['worm_binding']={'module':worm_module,'family_recipe':family_recipe,'state_labels':operator_module.state_labels,
      'birth_module':birth_module,'admission_module':admission_module,'owner_roster':original_vertices,'counters':{},'scope':'Uniform fixed original A+B start, uniform viable occupied first edge, uniform viable alternating continuation on the whole-path eligible graph until the first revisit; exact reverse-walk Hastings factor; exact native guards, event replay and weights.'}
    return prepared


def branch_of(u):
    """V001 thresholds unchanged: [0,2/15) worm loop (was current_cycle), [2/15,6/15) Birth, [6/15,10/15) admission, else base."""
    return 'worm_loop' if u<2./15. else ('birth_residence' if u<6./15. else ('admission_residence' if u<10./15. else 'prior_base'))


def _admission_diagnostic_update(run, old_path, new_path, diag):
    """Pure observer of successful transport using existing D and Da segment values.

    Integrals are over the sampler's imaginary-time circle, not physical rates.
    No source, state, event, acceptance, RNG, or sampler error threshold is changed.
    Values are calculated fully before updating any additional diagnostic key.
    """
    if old_path['times']!=new_path['times'] or len(old_path['events'])!=len(new_path['events']):
        raise ValueError('Admission observer requires preserved times and event count')
    ends=[0.]+list(old_path['times'])+[float(run['beta'])]
    old=old_path['segments'];new=new_path['segments']
    if len(old)!=len(new) or len(old)!=len(ends)-1:
        raise ValueError('Admission observer dwell shape mismatch')
    n=len(old[0]['Da'])
    if any(len(s['Da'])!=n for s in old+new):
        raise ValueError('Admission observer derivative shape mismatch')
    dt=[ends[i+1]-ends[i] for i in range(len(old))]
    delta_D=math.fsum(t*(float(b['D'])-float(a['D'])) for t,a,b in zip(dt,old,new))
    delta_Da=[math.fsum(t*(float(b['Da'][j])-float(a['Da'][j])) for t,a,b in zip(dt,old,new)) for j in range(n)]
    old_D=math.fsum(t*float(a['D']) for t,a in zip(dt,old))
    new_D=math.fsum(t*float(b['D']) for t,b in zip(dt,new))
    if not all(math.isfinite(v) for v in [delta_D,old_D,new_D]+delta_Da):
        raise ValueError('Nonfinite admission segment diagnostic')
    pending={}
    scopes=['all_moves']
    if diag['sweeps_completed']>=run['burn_in_sweeps']:scopes.append('measurement_moves')
    for scope in scopes:
        prefix='admission_segment_'+scope+'_'
        pending[prefix+'changed_transports']=diag.get(prefix+'changed_transports',0)+1
        for name,value in [('D_integral_change',delta_D),('absolute_D_integral_change',abs(delta_D))]:
            pending[prefix+name+'_sum']=diag.get(prefix+name+'_sum',0.)+value
        for name,values in [('Da_integral_change',delta_Da),('absolute_Da_integral_change',[abs(v) for v in delta_Da])]:
            prior=diag.get(prefix+name+'_sum',[0.]*n)
            if len(prior)!=n:raise ValueError('Admission diagnostic coordinate shape changed')
            pending[prefix+name+'_sum']=[a+b for a,b in zip(prior,values)]
        finite=[v for k,v in pending.items() if not isinstance(v,list)]+[a for v in pending.values() if isinstance(v,list) for a in v]
        if not all(math.isfinite(v) for v in finite):raise ValueError('Nonfinite cumulative admission diagnostic')
    pending['admission_segment_last_changed']={'stage':run['stage'],'old_D_integral':old_D,
        'new_D_integral':new_D,'D_integral_change':delta_D,'Da_integral_change':delta_Da}
    pending['admission_segment_scope']='Accepted transport integrals of existing D and Da over imaginary time; no physical rates or mixing claim. Native read-integral change remains independently reported and may be exactly zero.'
    pending['admission_segment_derivative_coordinates']=run['coords']
    diag.update(pending)


def _observed_admission_move(module, run, path, rng, diag, sampler, owner_roster):
    answer=module.move(run,path,rng,diag,sampler,owner_roster)
    if answer[1]=='changed':_admission_diagnostic_update(run,path,answer[0],diag)
    return answer


def run_prepared(*,prepared):
    b=prepared['worm_binding'];recipe=b['family_recipe'];wormmod=b['module'];sampler=prepared['sampler_module']
    _pin(b['admission_module'],ADMISSION_SHA);_pin(recipe,FAMILY_RECIPE_SHA);_pin(wormmod,WORM_SHA);_pin(b['birth_module'],BIRTH_SHA)
    if (getattr(sampler,'_worm_loop_recipe_active',False) or getattr(sampler,'_current_cycle_recipe_active',False)
            or getattr(sampler,'_recipe_occupancy_mixture_active',False)):raise RuntimeError('Concurrent/nested recipe patch forbidden')
    original=sampler._move;counts=b['counters']
    def tick(k):counts[k]=counts.get(k,0)+1
    def worm_mixture(run,path,rng,diag):
        sampler._budget_check(run,'before','worm-loop/base mixture')
        u=float(rng.random());branch=branch_of(u);tick(branch+'_selected')
        try:
            if branch=='worm_loop':answer=wormmod.move(run,path,rng,diag,sampler,b['owner_roster'],b['state_labels'])
            elif branch=='birth_residence':answer=b['birth_module'].move(run,path,rng,diag,sampler,b['owner_roster'])
            elif branch=='admission_residence':answer=_observed_admission_move(b['admission_module'],run,path,rng,diag,sampler,b['owner_roster'])
            else:answer=original(run,path,rng,diag)
        except BaseException:tick(branch+'_interrupted');raise
        if answer[1] not in ('changed','identity','rotation','rejected'):raise RuntimeError('Unknown sampler outcome')
        tick(branch+'_'+answer[1]);return answer
    sampler._worm_loop_recipe_active=True;sampler._move=worm_mixture
    try:
        # Existing recipe wraps THIS base with its .25 occupancy.
        result=recipe.run_prepared(prepared=prepared)
        result['worm_binding']={'module_sha256':WORM_SHA,'module_version':WORM_MODULE_VERSION,'family_recipe_sha256':FAMILY_RECIPE_SHA,
          'fixed_start_roster':b['owner_roster'],'walk_selection':'Uniform original start, uniform viable occupied first edge, uniform viable alternating continuation until first revisit; empty start/dead end/cap reject without resampling','maximum_walk_steps':wormmod.MAX_WALK_STEPS,'lookahead':wormmod.LOOKAHEAD,'birth_module_sha256':BIRTH_SHA,'fixed_birth_owner_roster':b['owner_roster'],'fixed_admission_owner_roster':b['owner_roster'],
          'total_worm_loop_probability':.10,'total_birth_residence_probability':.20,'total_occupancy_probability':.25,'total_admission_residence_probability':.20,'admission_module_sha256':ADMISSION_SHA,
          'total_prior_base_probability':.25,'outcomes':dict(counts),
          'counter_scope':'full chain including warmup; actual read-change vectors follow existing tracked labels',
          'scope':'Same target; new reversible proposal only. Changed accepts do not establish mixing; retain all original failures/error-withholding.'}
        return result
    finally:
        sampler._move=original;del sampler._worm_loop_recipe_active
