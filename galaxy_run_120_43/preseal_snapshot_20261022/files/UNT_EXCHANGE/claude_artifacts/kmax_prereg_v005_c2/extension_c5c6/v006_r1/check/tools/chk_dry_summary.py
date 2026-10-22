import json,hashlib,sys
from pathlib import Path
L=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
C=L/'v006_r1/check'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def leaves(o,p=''):
    if isinstance(o,dict):
        out={}
        for k,v in o.items(): out.update(leaves(v,p+'/'+k))
        return out or {p:'{}'}
    if isinstance(o,list):
        out={}
        for i,v in enumerate(o): out.update(leaves(v,p+'/'+str(i)))
        return out or {p:'[]'}
    return {p:json.dumps(o)}
res={}
for j,a in [('C5R3_A2F10_EXT_N8','C5_N8'),('C5R3_A2F10_EXT_N1','C5_N1'),('C6R3_A2F10_EXT_N8','C6_N8'),('C6R3_A2F10_EXT_N1','C6_N1')]:
    mine=C/'dry'/j; auth=L/'v006_r1/dryrun/dry'/('v009_%s_M32'%a); m16=L/'dryrun_b2/dry'/('v009_%s'%a)
    r=json.loads((mine/'DRYRUN_REPORT.json').read_text())
    e={k:r.get(k) for k in ('stages_planned','binding_blockers','unexplained_refusals','pin_problems')}
    e['remaining_refusals_by_class']=r.get('remaining_refusals_by_class')
    seed=mine/'simulated_call/inputs/seed_c2v001.json'
    e['seed_sha256']=sha(seed); e['author_seed_sha256']=sha(auth/'simulated_call/inputs/seed_c2v001.json')
    s=json.loads(seed.read_text()); e['seed_max_iterations']=s['numerical_inputs']['max_iterations']; e['fourier_points_per_axis']=s['numerical_inputs'].get('fourier_points_per_axis')
    if m16.is_dir():
        o=json.loads((m16/'simulated_call/inputs/seed_c2v001.json').read_text())
        ln,lo=leaves(s),leaves(o); e['seed_leafdiff_vs_M16']={k:(lo.get(k),ln.get(k)) for k in sorted(set(ln)|set(lo)) if ln.get(k)!=lo.get(k)}
    eq={}
    for f in sorted((mine/'simulated_call/inputs').iterdir()):
        a_=f.read_text().replace(str(mine),'<RD>'); b_=(auth/'simulated_call/inputs'/f.name).read_text().replace(str(auth),'<RD>')
        eq[f.name]=a_==b_
    e['inputs_equal_author_after_RD_subst']=eq
    pa=(mine/'DRYRUN_PLAN.txt').read_text().replace(str(mine),'<RD>'); pb=(auth/'DRYRUN_PLAN.txt').read_text().replace(str(auth),'<RD>')
    e['plan_equal_author_after_RD_subst']=pa==pb
    if not e['plan_equal_author_after_RD_subst']:
        e['plan_diff_lines']=[(x,y) for x,y in zip(pa.splitlines(),pb.splitlines()) if x!=y][:5]
    res[a]=e
print(json.dumps(res,indent=1))
