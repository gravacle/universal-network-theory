import sys, importlib.util, numpy as np, json
spec=importlib.util.spec_from_file_location('sp','/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/tests/syn_env/syn_problem_c2v001.py'); sp=importlib.util.module_from_spec(spec); spec.loader.exec_module(sp)
def walk(a,b,path,out,limit=12):
    if len(out)>=limit: return
    if type(a)!=type(b): out.append((path,'TYPE',type(a).__name__,type(b).__name__)); return
    if isinstance(a,dict):
        if list(a)!=list(b): out.append((path,'KEYS',list(a)[:8],list(b)[:8]))
        for k in a:
            if k in b: walk(a[k],b[k],path+'/'+str(k),out)
    elif isinstance(a,(list,tuple)):
        if len(a)!=len(b): out.append((path,'LEN',len(a),len(b))); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f'{path}[{i}]',out)
    elif isinstance(a,np.ndarray):
        if a.dtype!=b.dtype or a.shape!=b.shape: out.append((path,'ARR',str(a.dtype)+str(a.shape),str(b.dtype)+str(b.shape)))
        elif a.tobytes()!=b.tobytes(): out.append((path,'ARRBYTES',float(np.max(np.abs(a-b))) if a.dtype.kind in 'fc' else '?',''))
    else:
        if isinstance(a,float) and isinstance(b,float):
            if a!=b and not (np.isnan(a) and np.isnan(b)): out.append((path,'VAL',a,b))
        elif a!=b: out.append((path,'VAL',str(a)[:60],str(b)[:60]))
if __name__=='__main__':
    mods=sp.modules(); build=dict(vertical=True,n_radii=2,n_phi=4); cfg=dict(max_iterations=2,source_rtol=0.0)
    p=sp.build(mods,**build); ref=mods['reviewed_solver'].solve(**dict(p,**cfg))
    p=sp.build(mods,**build); par=mods['parallel_solver'].solve(**dict(p,**cfg),column_workers=3)
    out=[]; walk({k:v for k,v in ref.items() if k!='checkpoint'},{k:v for k,v in par.items() if k!='checkpoint'},'',out)
    print('differences (first 12):'); [print(' ',o) for o in out]
    print('top keys', list(ref))
