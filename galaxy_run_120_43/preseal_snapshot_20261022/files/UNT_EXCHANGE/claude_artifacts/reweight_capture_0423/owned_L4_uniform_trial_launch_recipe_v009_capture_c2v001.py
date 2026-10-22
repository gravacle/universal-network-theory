"""INERT V009 CAPTURE C2V001 (UNT 0423): V009 plus ONLY the pairallk V002 reweighting_capture.
Base V009 sha256 44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697.
INERT V009: root occupancy plus pair/all-k attempt; final sampler pin required.
Run fails closed until root supplies the accepted final sampler SHA256.
Fixed state-independent outer mixture: occupancy .50, existing base _move .50.
Base pair/rotation/palette/full probabilities remain unchanged. No W2/open sector.
Physical trial, seeds, two chains64warmup/256measure,5moves/sweep unchanged.
Root-declared changed algorithm: pair.50,rotation.10,palette.35,full.05;
local pair palette and insertion/deletion .50/.50. Soft1740s/900MiB,
hard1800s/1GiB. This is NOT the abandoned unchanged longer V007 trial.
No import, compile, execution or sampling by author.
0423: sampler must be pairallk V002 (the only reviewed capture bytes); its existing
reweighting_capture binds statistics V001 and the SAME operator V003 module; sampler,
occupancy, statistics, operator and adapter are re-hashed from __file__ bytes before
sampling. Amplitudes are abs(TRIAL[x]), x in h,t,g,kappa,epsilon (same trial, no new
values); explicit uniform-profile attestation; rate_tolerance 1e-12. Trial, registration,
seeds, chains, sweeps, mixture, moves, caps, budgets, journal and helpers are unchanged.
Raw rows are evidence only: no reweighting, overlap, mixing or calibration acceptance.
"""
import time
import resource
import sys
import json
import os
import hashlib
import numpy as np

FINAL_MERGED_SAMPLER_SHA256=None  # root supplies accepted pin via prepare argument
OCCUPANCY_SHA256="7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5"
DRAFT_SOURCE_PINS={
 'pair_feature_v001':'080153ee3ef69c470b9302570852c8ae612462ae32df62e99393ae0ec608f523',
 'allk_feature_v001':'c37bca61b35579492d5a306519288762a596d787ed7c62d2fe0df2599a4ecbdd',
 'operator_v003':'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07',
 'sampler_v004':'6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea',
 'diamond_adapter_v001':'0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77',
 'prior_recipe_v004':'23d9ea3f1c622c2d16b98704510ea366ed647628f07c26ad8caf68bf72448500'}
# UNT 0423 capture pins (author verified from bytes; run_prepared re-hashes __file__ bytes).
BASE_RECIPE_V009_SHA256='44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697'
CAPTURE_SAMPLER_SHA256='bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba'  # pairallk V002
STATISTICS_SHA256='85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a'  # reweighting statistics V001
OPERATOR_SHA256=DRAFT_SOURCE_PINS['operator_v003']
ADAPTER_SHA256=DRAFT_SOURCE_PINS['diamond_adapter_v001']
CAPTURE_AMPLITUDE_ORDER=('h','t','g','kappa','epsilon')
CAPTURE_RATE_TOLERANCE=1e-12
CAPTURE_PROFILE_ATTESTATION=(
 'UNT 0423 declared uniform-amplitude family (a premise, not empirical evidence): model from '
 'diamond adapter V001 build_inputs(L=4, coefficients=TRIAL); h, t and theta are adapter '
 'UniformEdgeProfile accessors returning the single TRIAL scalar for every ordered A-B edge '
 '(class, L and value checked in prepare); g and kappa are uniform maps over every vertex and '
 'epsilon a uniform map over every original owner, of the same TRIAL scalars (checked by '
 'statistics configure on the validated model); uniform lapse factors, zero uniform pair '
 'sources, fixed dstar, registration and gauge phases. Marked-event weights are compared '
 'with lapse times amplitude at rate_tolerance.')
TRIAL=dict(Ud=1.,dstar=2.,Delta=1.,lambda_J=.1,lambda_R=.1,
 epsilon_c=.3,epsilon_r=.3,E_R=.1,E_S=.1,E_I=.1,e_R=.1,e_I=.1,
 C_identity=0.,h=.1,t=.1,g=.1,kappa=.1,epsilon=.1,theta=0.)


def prepare(*,operator_module,sampler_module,diamond_adapter,progress_stream,
            occupancy_module,statistics_module,accepted_sampler_sha256=None):
    if progress_stream is None:
        raise ValueError('Caller must supply an open durable progress journal')
    def progress_sink(*,record):
        progress_stream.write(json.dumps(documentary_payload(record),allow_nan=False)+'\n')
        progress_stream.flush()
        os.fsync(progress_stream.fileno())
    binding=diamond_adapter.build_inputs(L=4,coefficients=dict(TRIAL),port_cache_entries=4096)
    reg=binding['registration']
    frame=tuple(tuple(v/2. for v in p) for p in diamond_adapter.PROTOTYPES4)
    reg['port_vectors']={'A':frame,'B':tuple(tuple(-v for v in r) for r in frame)}
    reg['whitening']=tuple(tuple(diamond_adapter.W if i==j else 0. for j in range(3)) for i in range(3))
    reg['max_cached_graphs']=4
    edge_roster=tuple(tuple(e) for e in binding['graph0']['edges'])
    if not edge_roster or len(set(edge_roster))!=len(edge_roster):
        raise ValueError('Frozen graph0 edge roster must be nonempty and unique')
    A=set(binding['graph0']['A']); B=set(binding['graph0']['B'])
    if any(len(e)!=2 or e[0] not in A or e[1] not in B for e in edge_roster):
        raise ValueError('Frozen graph0 edges must be ordered A-to-B')
    for name in ('h','t','theta'):  # 0423: declared uniform accessor family, structural only
        prof=binding['model'][name]
        if type(prof) is not diamond_adapter.UniformEdgeProfile or prof.L!=4 or prof.value!=TRIAL[name]:
            raise ValueError('0423 capture: model '+name+' is not the declared uniform TRIAL accessor')
    if tuple(statistics_module.AMPS)!=CAPTURE_AMPLITUDE_ORDER:
        raise ValueError('0423 capture: statistics amplitude order is not h,t,g,kappa,epsilon')
    cells=reg['cells']; clock={'start':time.monotonic(),'primitive_calls':0}
    def budget_state():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rb=rss if sys.platform=='darwin' else rss*1024
        elapsed=time.monotonic()-clock['start']
        return {'elapsed_seconds':elapsed,'peak_rss_bytes':rb,
                'primitive_calls':clock['primitive_calls'],
                'stop_requested':elapsed>=1740. or rb>=900*1024**2 or clock['primitive_calls']>=300000}
    def guarded(name):
        fn=getattr(operator_module,name)
        def call(**kw):
            if name in ('primitive_channels','palette_channels'): clock['primitive_calls']+=1
            # V004 polls the dedicated hook before/after operator calls.
            return fn(**kw)
        return call
    api={name:guarded(name) for name in ('validate_owned_model','canonical_state_key',
         'primitive_channels','palette_channels','diagonal_terms','read_rows')}
    phi={c:1. for c in cells}; profile='uniform_phi1'
    dirs=[{'id':'N','kind':'lapse_direction','profile_id':profile,'cell_weights':dict(phi)}]
    fields=[(('whitened_R',i),1.) for i in range(3)]
    fields += [(('whitened_S',i,j),1. if i==j else float(np.sqrt(2.)))
               for i,j in ((0,0),(1,1),(2,2),(1,2),(0,2),(0,1))]
    for a,(field,factor) in enumerate(fields):
        dirs.append({'id':('Q',a),'kind':'source_direction','profile_id':profile,
                     'cell_weights':dict(phi),'label_weights':{field:factor}})
    pair={'adapter':diamond_adapter,'operator_module':operator_module,'binding':binding,
          'source_frame':'whitened','j_R':{c:[0.,0.,0.] for c in cells},
          'j_S':{c:[[0.,0.,0.] for _ in range(3)] for c in cells},
          'source_consistency_tolerance':1e-12}
    owners=tuple(binding['graph0']['A'])+tuple(binding['graph0']['B'])
    capture_args={'module':statistics_module,'operator_module':operator_module,
        'uniform_amplitudes':[float(abs(TRIAL[name])) for name in CAPTURE_AMPLITUDE_ORDER],
        'uniform_profile_attestation':CAPTURE_PROFILE_ATTESTATION,
        'rate_tolerance':CAPTURE_RATE_TOLERANCE}
    capture_record={'sampler_sha256':CAPTURE_SAMPLER_SHA256,'statistics_sha256':STATISTICS_SHA256,
        'operator_sha256':OPERATOR_SHA256,'adapter_sha256':ADAPTER_SHA256,
        'base_recipe_sha256':BASE_RECIPE_V009_SHA256,
        'amplitude_order':list(CAPTURE_AMPLITUDE_ORDER),
        'amplitude_source':'abs(TRIAL[name]) of the same trial; no new values',
        'uniform_amplitudes':list(capture_args['uniform_amplitudes']),
        'uniform_profile_attestation':CAPTURE_PROFILE_ATTESTATION,
        'rate_tolerance':CAPTURE_RATE_TOLERANCE,
        'scope':'raw per-path capture binding only; no reweighting, overlap, mixing or calibration acceptance'}
    seeds=np.random.SeedSequence(2026101601).spawn(2)
    args=dict(operator_api=api,graph0=binding['graph0'],model=binding['model'],registration=reg,
        initial_paths=[{'x0':binding['seed_state'],'events':[]} for _ in range(2)],
        beta=1.,lapse_factors={c:1. for c in cells},source_coefficients={},
        volume_gradient_coefficients={},volume_multiplier=0.,
        gauge_phases={'admission_phase':0.,'birth_phase':0.},derivative_coordinates=dirs,
        # V003 automatically appends its nine uniform corrected background moments.
        tracked_read_labels=[],diagonal_read_source_callback=pair,
        chain_generators=[np.random.default_rng(s) for s in seeds],
        move_parameters={'moves_per_sweep':5,'rotation_probability':.1,
            'whole_circle_probability':.05,'length_components':[(9.,.02),(1.,1.)]},
        palette_parameters={'selection_probability':.35,'palettes':[(1.,(o,)) for o in owners],
                            'verify_against_full_enumeration':False},
        caps={'max_events_per_path':10000,'max_total_events':300000,
              'max_sweeps':640,'max_channel_enumerations':300000},
        burn_in_sweeps=64,measurement_sweeps=256,
        error_parameters={'batches_per_chain':8,'sokal_window_constant':5.,'rhat_max':1.1,
            'min_batch_length_over_tau':5.,'max_explicit_covariance_dimension':128},
        numerical_tolerances={'gauge_phase':1e-12,'weight_partition':1e-12,'reverse_rate':1e-12},
        all_momentum={'L':4,'cell_coordinates':{c:tuple(c) for c in cells}},
        pair_move_parameters={'schedule':{'pair':.50,'rotation':.10,
            'palette_regrowth':.35,'full_regrowth':.05},
            'insertion_probability':.50,'deletion_probability':.50,'local_palette':True},
        implicit_closure=None,budget_hook=lambda: bool(budget_state()['stop_requested']),
        progress_sink=progress_sink,reweighting_capture=capture_args)
    return {'arguments':args,'sampler':sampler_module.owned_collective_worldline_static_response,
        'binding':binding,'budget_state':budget_state,'counters':clock,'cell_count':64,
        'sampler_module':sampler_module,'occupancy_module':occupancy_module,
        'statistics_module':statistics_module,'reweighting_capture_record':capture_record,
        'accepted_sampler_sha256':accepted_sampler_sha256,'edge_roster':edge_roster,
        'mixture_counters':{},
        'cooperative_binding_status':'FINAL_ACCEPTED_SAMPLER_PIN_REQUIRED_BEFORE_RUN',
        'hard_monitor_required':{'wall_seconds':1800,'rss_bytes':1073741824},
        'scope':'same exploratory full-owned L4 uniform equilibrium response; no fit or predictions'}


def _verified_module(module, expected, label):
    if not isinstance(expected,str) or len(expected)!=64 or any(c not in '0123456789abcdef' for c in expected):
        raise RuntimeError(label+': root accepted SHA256 is not assigned')
    filename=getattr(module,'__file__',None)
    if not filename:
        raise RuntimeError(label+': source file provenance required')
    with open(filename,'rb') as stream:
        actual=hashlib.sha256(stream.read()).hexdigest()
    if actual!=expected:
        raise RuntimeError(label+': source pin mismatch')


def run_prepared(*,prepared):
    """Root-only call. Patch the accepted ordinary closed-path _move temporarily.
    No concurrent calls or alternate patches of this same sampler module allowed.
    Preserve the entire returned sampler dictionary, including partial arrays;
    the worker serializes documentary_payload(result) without requiring estimates.
    Source-byte checks assume modules were loaded from those unchanged files.
    0423: only the pairallk V002 pin is admitted; statistics, operator and adapter bytes
    are checked too. Capture rows stay inside the returned sampler dictionary verbatim.
    """
    sampler=prepared['sampler_module']; occupancy=prepared['occupancy_module']
    expected=prepared['accepted_sampler_sha256'] or FINAL_MERGED_SAMPLER_SHA256
    if expected!=CAPTURE_SAMPLER_SHA256:
        raise RuntimeError('0423 capture binds only the reviewed pairallk V002 sampler bytes')
    _verified_module(sampler,expected,'final merged sampler')
    _verified_module(occupancy,OCCUPANCY_SHA256,'occupancy V002')
    args=prepared['arguments']
    capture=args.get('reweighting_capture'); callback=args['diagonal_read_source_callback']
    if (not isinstance(capture,dict) or capture.get('module') is not prepared['statistics_module']
            or capture.get('operator_module') is not callback['operator_module']
            or capture.get('uniform_amplitudes')!=[float(abs(TRIAL[n])) for n in CAPTURE_AMPLITUDE_ORDER]
            or capture.get('uniform_profile_attestation')!=CAPTURE_PROFILE_ATTESTATION
            or capture.get('rate_tolerance')!=CAPTURE_RATE_TOLERANCE):
        raise RuntimeError('0423 capture must bind prepared modules, TRIAL amplitudes, attestation, tolerance')
    _verified_module(capture['module'],STATISTICS_SHA256,'uniform reweighting statistics V001')
    _verified_module(capture['operator_module'],OPERATOR_SHA256,'operator V003')
    _verified_module(callback['adapter'],ADAPTER_SHA256,'diamond adapter V001')
    if args.get('implicit_closure') is not None or any(k in args for k in ('two_hop_parameters','w2_parameters')):
        raise RuntimeError('Occupancy recipe admits only ordinary closed-path sampling')
    if prepared['sampler'] is not sampler.owned_collective_worldline_static_response:
        raise RuntimeError('Prepared sampler function/module mismatch')
    if getattr(sampler,'_recipe_occupancy_mixture_active',False):
        raise RuntimeError('Concurrent/nested occupancy patch is forbidden')
    base_move=sampler._move
    roster=prepared['edge_roster']  # fixed graph0 tuple, never current-state selection
    counts=prepared['mixture_counters']
    def tick(key): counts[key]=counts.get(key,0)+1
    def mixed_move(run,path,rng,diag):
        sampler._budget_check(run,'before','fixed occupancy/base mixture')
        branch='occupancy' if float(rng.random())<.50 else 'base'
        tick(branch+'_selected')
        try:
            if branch=='occupancy':
                new_path,outcome=occupancy.move(run,path,rng,diag,sampler,roster)
            else:
                new_path,outcome=base_move(run,path,rng,diag)
        except BaseException:
            tick(branch+'_interrupted')
            raise
        if outcome not in ('changed','identity','rotation','rejected'):
            raise RuntimeError('Unexpected merged sampler move outcome')
        tick(branch+'_'+outcome)
        return new_path,outcome
    sampler._recipe_occupancy_mixture_active=True
    sampler._move=mixed_move
    try:
        result=prepared['sampler'](**args)
        # Add provenance/counters only. Never alter status, ok, mixing or estimates.
        result['recipe_occupancy_mixture']={
            'probability':.50,'base_probability':.50,
            'occupancy_sha256':OCCUPANCY_SHA256,'sampler_sha256':expected,
            'frozen_graph0_edge_roster':roster,'outcomes':dict(counts),
            'scope':'ordinary closed paths; full raw sampler result retained'}
        result['recipe_reweighting_capture']=dict(prepared['reweighting_capture_record'])
        return result
    finally:
        sampler._move=base_move
        del sampler._recipe_occupancy_mixture_active


def documentary_payload(value):
    """Serialize COMPLETE result recursively, including incomplete/partial fields.
    Never access estimates unconditionally or label partial evidence accepted.
    Tagged nonfinite diagnostics retain information without invalid JSON numbers.
    """
    if isinstance(value,np.ndarray): return documentary_payload(value.tolist())
    if isinstance(value,np.generic): return documentary_payload(value.item())
    if isinstance(value,dict): return {str(k):documentary_payload(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [documentary_payload(v) for v in value]
    if isinstance(value,float) and not np.isfinite(value): return {'nonfinite_diagnostic':repr(value)}
    if value is None or isinstance(value,(str,int,float,bool)): return value
    raise TypeError('Unbound serialization type '+type(value).__name__)


def normalize_complete_derivatives(*,F_gradient,F_hessian):
    """Uniform phi=1 gives S=64. Apply only to supplied actual derivatives and
    likewise each available joint replicate; partial status is not changed.
    Background outputs are SUMS: use convert_uniform_background below, separately.
    """
    g=np.asarray(F_gradient,dtype=float); h=np.asarray(F_hessian,dtype=float)
    if g.shape!=(10,) or h.shape!=(10,10) or not np.all(np.isfinite(g)) or not np.all(np.isfinite(h)):
        raise ValueError('Expected finite ten-direction derivatives')
    return {'F_gradient':g/64.,'F_hessian':h/64.}


def convert_uniform_background(*,labels,cell_sum_means,cell_sum_replicates=None):
    """V004 L23: nine whitened SUMS, off-diagonal S is raw (not Mandel).
    Reorder by label, divide by 64, and form C=M-mu mu^T. Apply the SAME nonlinear
    conversion to each supplied joint jackknife replicate; do not centralize
    individual cells first, average covariances, or repair SPD. No status upgrade.
    """
    expected=[('uniform_whitened_R',i) for i in range(3)]
    pairs=((0,0),(1,1),(2,2),(1,2),(0,2),(0,1))
    expected += [('uniform_whitened_S',i,j) for i,j in pairs]
    labs=[tuple(x) for x in labels]
    if len(labs)!=9 or len(set(labs))!=9 or set(labs)!=set(expected):
        raise ValueError('Exactly the nine V004 uniform background labels required')
    order=[labs.index(x) for x in expected]
    def convert(rows):
        arr=np.asarray(rows,dtype=float)
        if arr.shape[-1:]!=(9,) or not np.all(np.isfinite(arr)):
            raise ValueError('Finite nine-column cell sums required')
        avg=arr[...,order]/64.
        mu=avg[...,:3]
        M=np.zeros(avg.shape[:-1]+(3,3),dtype=float)
        for a,(i,j) in enumerate(pairs):
            M[...,i,j]=avg[...,3+a]; M[...,j,i]=avg[...,3+a]
        return {'mu':mu,'M':M,'C':M-mu[..., :,None]*mu[...,None,:]}
    point=np.asarray(cell_sum_means,dtype=float)
    if point.shape!=(9,): raise ValueError('Point means must have shape (9,)')
    out={'point':convert(point),'replicates':None,'n_cells':64,
         'off_diagonal_convention':'raw S, no Mandel factor',
         'status_note':'Conversion only; preserves caller completion/error status'}
    if cell_sum_replicates is not None:
        reps=np.asarray(cell_sum_replicates,dtype=float)
        if reps.ndim!=2 or reps.shape[1]!=9:
            raise ValueError('Joint replicate sums must have shape (n_replicates,9)')
        out['replicates']=convert(reps)
    return out


def background_from_completed_outputs(*,uniform_moments,errors):
    """Call only when uniform_moments contains actual cell_sum_means. An incomplete
    result may contain uniform_moments metadata WITHOUT cell_sum_means. Caller
    must gate on that key (and retain completion/error status); otherwise retain
    diagnostic prefixes without fabricating estimates.
    errors may be None (no admitted joint uncertainty); no replicate is invented.
    """
    if not isinstance(uniform_moments,dict) or 'cell_sum_means' not in uniform_moments:
        return None  # incomplete metadata is not measured background
    if uniform_moments['n_cells']!=64: raise ValueError('Recipe is fixed L4/64 cells')
    reps=None
    if errors is not None:
        all_reps=np.asarray(errors['jackknife_replicates'],dtype=float)
        positions=np.asarray(uniform_moments['error_layout_positions'],dtype=int)
        if all_reps.ndim!=2 or positions.shape!=(9,) or np.any(positions<0) or np.any(positions>=all_reps.shape[1]):
            raise ValueError('Invalid actual sampler joint replicate positions')
        reps=all_reps[:,positions]
    return convert_uniform_background(labels=uniform_moments['labels'],
        cell_sum_means=uniform_moments['cell_sum_means'],cell_sum_replicates=reps)


def background_from_allk_outputs(*,result):
    """All-k feature-specific nine SUM labels and JOINT background replicas.
    Incomplete metadata is never promoted to an estimate. Mixing failure leaves
    a diagnostic point with status preserved and no invented replicate/error.
    The shared partition is returned to keep all modes/background aligned.
    """
    packet=result.get('all_momentum')
    if not isinstance(packet,dict) or packet.get('status')!='analysed': return None
    bg=packet.get('background')
    if not isinstance(bg,dict) or 'cell_sum_time_average_means' not in bg: return None
    meta=packet.get('metadata',{})
    if meta.get('n_cells')!=64: raise ValueError('Expected actual L4 all-k metadata')
    labels=[]
    for raw in bg['labels']:
        label=tuple(raw)
        if not label or not isinstance(label[0],str) or not label[0].startswith('background_cell_sum_'):
            raise ValueError('Unexpected all-k background label')
        labels.append(('uniform_'+label[0][len('background_cell_sum_'):],)+label[1:])
    reps=None
    errors=bg.get('errors')
    if errors is not None:
        # Actual all-k background _analyze uses n_u=0,n_r=9: y contains only means.
        reps=np.asarray(errors['jackknife_replicates'],dtype=float)
        partition=packet.get('partition')
        if not isinstance(partition,list) or reps.ndim!=2 or reps.shape!=(len(partition),9):
            raise ValueError('Joint background replica/partition shape mismatch')
        if [entry['omission_index'] for entry in partition]!=list(range(len(partition))):
            raise ValueError('Unexpected common omission order')
    converted=convert_uniform_background(labels=labels,
        cell_sum_means=bg['cell_sum_time_average_means'],cell_sum_replicates=reps)
    converted['joint_partition']=packet.get('partition')
    converted['identity_check']=packet.get('identity_check')
    converted['run_status']=result.get('status')
    converted['run_ok']=result.get('ok')
    converted['joint_mixing']=packet.get('mixing')
    converted['scope']='Conversion only; point/replicates never override sampler or root acceptance'
    return converted
