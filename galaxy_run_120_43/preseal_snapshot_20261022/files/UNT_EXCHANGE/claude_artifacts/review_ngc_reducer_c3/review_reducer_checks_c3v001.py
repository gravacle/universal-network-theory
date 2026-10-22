"""Claude3 independent checks for dispatch 0476 (reducer V003 / NGC3198 truncated source). Exact rational arithmetic. Read-only."""
import json, hashlib, math, sys, itertools
from fractions import Fraction as Fr
R='claude_artifacts/ngc_route_impl_c2/reducer'
PROF="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json"
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def J(p): return json.load(open(p))
E={'inputs':{}}
for p in (PROF, f'{R}/segment_monotone_bernstein_source_controls_v003.py', f'{R}/NGC3198_SEGMENT_MONOTONE_SOURCE_TRUNCATED_RUN_V001/source.json', f'{R}/DDO154_V003_REPRODUCTION_DRYRUN_V001/source.json'):
    E['inputs'][p]=sha(p)
prof=J(PROF); full=prof['galaxies']['NGC3198']['HI_plus_He']
src=J(f'{R}/NGC3198_SEGMENT_MONOTONE_SOURCE_TRUNCATED_RUN_V001/source.json'); rec=src['source_record']
fm=[Fr(x) for x in full['annular_means_Msun_pc2']]; fe=[Fr(x) for x in full['s_edges_kpc2']]
# ---- (5) truncation
k=next(i for i,m in enumerate(fm) if m==0)
E['truncation']={'full_bins':len(fm),'first_zero_bin':k,'kept_bins':len(rec['annular_means_Msun_pc2']),
 'edges_bitwise_prefix': rec['s_edges_kpc2']==full['s_edges_kpc2'][:k+1], 'means_bitwise_prefix': rec['annular_means_Msun_pc2']==full['annular_means_Msun_pc2'][:k],
 'outer_edge_s_kpc2': full['s_edges_kpc2'][k], 'outer_edge_kpc_float_sqrt': math.sqrt(full['s_edges_kpc2'][k]),
 'outer_edge_equals_66.90428799311597': math.sqrt(full['s_edges_kpc2'][k])==66.90428799311597,
 'record_outer_edge_kpc': rec['truncation']['outer_edge_kpc'], 'record_support_radius_kpc': rec['support_radius_kpc'],
 'q43_44.08_inside': 44.08**2 < full['s_edges_kpc2'][k]}
mass=[(fe[i+1]-fe[i])*fm[i] for i in range(len(fm))]  # pi*1e6 factor cancels in the fraction
tot=sum(mass); kept=sum(mass[:k]); E['truncation']['dropped_mass_fraction_exact']=float((tot-kept)/tot); E['truncation']['dropped_mass_fraction_recorded']=rec['truncation']['dropped_mass_fraction']
E['truncation']['zero_bins_after_first']=[i for i,m in enumerate(fm) if m==0]
# ---- (2) annular means exact (stored controls, rational)
d=[Fr(x) for x in rec['boundary_controls_Msun_pc2']]; b=[Fr(x) for x in rec['middle_controls_Msun_pc2']]; m=[Fr(x) for x in rec['annular_means_Msun_pc2']]
n=len(m); assert len(d)==n+1 and len(b)==n
res=[(d[i]+b[i]+d[i+1])/3 - m[i] for i in range(n)]
E['annular_means']={'n_bins':n,'max_abs_rational_residual_stored_controls':float(max(abs(r) for r in res)),'max_rel_rational_residual':float(max(abs(r)/m[i] for i,r in enumerate(res))),
 'bins_exact_zero_residual':sum(1 for r in res if r==0),
 'b_recomputed_from_means_gives_exact_mean': all(((d[i]+(3*m[i]-d[i]-d[i+1])+d[i+1])/3)==m[i] for i in range(n)),
 'min_control': float(min(d+b)), 'all_controls_positive': min(d+b)>0}
# ---- (3) humps: quadratic Bernstein derivative sign at left (b-d_i) and right (d_{i+1}-b); strict flip iff product<0
q=Fr(44.08)**2
humps=[]
for i in range(n):
    L=b[i]-d[i]; Rr=d[i+1]-b[i]
    if L*Rr<0:
        # excursion of the parabola extremum above/below the nearer endpoint, relative to the mean
        # Σ(u)=d_i(1-u)^2+2b u(1-u)+d_{i+1}u^2; extremum at u*=(d_i-b)/(d_i-2b+d_{i+1})
        den=d[i]-2*b[i]+d[i+1]; u=(d[i]-b[i])/den; val=d[i]*(1-u)**2+2*b[i]*u*(1-u)+d[i+1]*u**2
        exc=min(abs(val-d[i]),abs(val-d[i+1]))
        humps.append({'bin':i,'inner_edge_kpc':math.sqrt(float(fe[i])),'outer_edge_kpc':math.sqrt(float(fe[i+1])),'inside_44.08':fe[i]<q,'left_slope':float(L),'right_slope':float(Rr),'excursion_over_mean':float(exc/m[i])})
E['humps']={'strict_sign_flip_bins_exact':[h['bin'] for h in humps],'inside_44.08_bins':[h for h in humps if h['inside_44.08']],'max_excursion_over_mean_inside_44.08':max([h['excursion_over_mean'] for h in humps if h['inside_44.08']] or [0.0]),
 'file_within_bin_hump_bins_strict_sign':src['within_bin_hump_bins_strict_sign'],'bins_overlapping_44.08':[i for i in range(n) if fe[i]<q]}
# ---- (4) exact chain feasibility (own derivation): F: 2d_i+d_{i+1}>=3m, d_i+2d_{i+1}<=3m; R: reversed; X: d_i+d_{i+1}<=3m; all d>=0
def step(iv,mm,kd):
    lo,hi=iv
    if kd=='F':
        a,bb=max(lo,mm),min(hi,3*mm)
        return None if a>bb else (max(Fr(0),3*mm-2*bb),(3*mm-a)/2)
    if kd=='R':
        a,bb=max(lo,Fr(0)),min(hi,mm)
        return None if a>bb else ((3*mm-bb)/2,3*mm-2*a)
    if kd=='X':
        a,bb=max(lo,Fr(0)),min(hi,3*mm)
        return None if a>bb else (Fr(0),3*mm-a)
def feasible(kinds):
    iv=(Fr(0),None)
    for i,(mm,kd) in enumerate(zip(m,kinds)):
        lo,hi=iv; hi=hi if hi is not None else 10**9*max(m)
        iv=step((lo,hi),mm,kd)
        if iv is None: return False,i
    return True,None
t=[m[0]]+[(m[i]+m[i+1])/2 for i in range(n-1)]+[m[-1]]
rule=''.join('R' if t[i+1]>t[i] else 'F' for i in range(n))
E['directions']={'rule_exact':rule,'rule_in_file':src['direction_declaration']['rule_directions'],'equal':rule==src['direction_declaration']['rule_directions'],'ties_t_equal':[i for i in range(n) if t[i+1]==t[i]],
 'means_22_23':[float(m[22]),float(m[23])],'F_chain_needs_nonincreasing_means_violated_at':[i for i in range(n-1) if rule[i]=='F' and rule[i+1]=='F' and m[i]<m[i+1]]}
def with_exc(s):
    r=list(rule)
    for i in s: r[i]='X'
    return ''.join(r)
f0=feasible(rule); E['feasibility']={'no_exception':{'feasible':f0[0],'first_empty_bin':f0[1]}}
singles=[i for i in range(n) if feasible(with_exc([i]))[0]]
E['feasibility']['feasible_single_exception_sets']=singles
pairs=[list(c) for c in itertools.combinations(range(n),2) if feasible(with_exc(c))[0]]
E['feasibility']['n_feasible_pairs']=len(pairs); E['feasibility']['minimal_size']=0 if f0[0] else (1 if singles else (2 if pairs else '>2'))
E['feasibility']['file_all_minimal_sets']=src['direction_declaration']['all_minimal_exception_sets']; E['feasibility']['file_minimal_size']=src['direction_declaration']['minimal_exception_size']
E['feasibility']['final_directions_feasible']=feasible(src['directions'])[0]
# ---- (4b) objective comparison via bounds: upper bound {23} = stored point objective; lower bound {22} = Hildreth dual value (weak duality)
import importlib.util
spec=importlib.util.spec_from_file_location('red',f'{R}/segment_monotone_bernstein_source_controls_v003.py'); red=importlib.util.module_from_spec(spec); spec.loader.exec_module(red)
r22=red.reduce_source(record=rec,directions=with_exc([22]),max_sweeps=200000,kkt_tolerance=1e-10)
r23=red.reduce_source(record=rec,directions=with_exc([23]),max_sweeps=200000,kkt_tolerance=1e-10)
# own objective from stored controls, exact targets
x=[(d[i]-t[i])/t[i] for i in range(n+1)]; obj23_stored=float(sum(v*v for v in x)/2)
E['objective']={'file_objective_by_minimal_set':src['direction_declaration']['objective_by_minimal_set'],
 'own_objective_of_stored_23_controls':obj23_stored,'rerun_23_status':r23['status'],'rerun_23_objective':r23['diagnostics']['objective'],'rerun_23_dual':r23['diagnostics']['dual_objective'],'rerun_23_primal_violation':r23['diagnostics']['normalized_primal_violation'],
 'rerun_22_status':r22['status'],'rerun_22_objective':r22['diagnostics']['objective'],'rerun_22_dual_lower_bound':r22['diagnostics']['dual_objective'],'rerun_22_min_control':min(r22.get('candidate_controls_not_admitted',{}).get('d',[0])+r22.get('candidate_controls_not_admitted',{}).get('b',[0])) if 'candidate_controls_not_admitted' in r22 else None,
 'rerun_23_controls_bitwise_equal_stored': r23['source_record']['boundary_controls_Msun_pc2']==rec['boundary_controls_Msun_pc2'] and r23['source_record']['middle_controls_Msun_pc2']==rec['middle_controls_Msun_pc2']}
E['objective']['lower_bound_22_exceeds_upper_bound_23']= r22['diagnostics']['dual_objective'] > obj23_stored
json.dump(E,open(sys.argv[1],'w'),indent=1); print(json.dumps({k:v for k,v in E.items() if k!='inputs'},indent=1)[:6000])
