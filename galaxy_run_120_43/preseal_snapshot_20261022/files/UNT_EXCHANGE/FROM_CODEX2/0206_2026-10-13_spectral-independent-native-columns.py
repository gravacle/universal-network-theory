"""SOURCE ONLY independent literal N2 Q1/A1 column and preparation reconstruction.
Exact integer Gaussian units1/560; no producer imports, source calls or NumPy.
"""
from fractions import Fraction as F


def need(ok,label):
    if not ok:raise ValueError(label)


def pop(x):return bin(x).count('1')


def expected_parameters():
    phases=[['1','0'],['0','-1'],['-1','0'],['0','1']]
    return {'real':{'h':'1/5','Delta':'4','Ud':'1','epsilon_c':'1','t':'1',
      'epsilon_r':'7/8','g':'1/2','lambda_R':'1/8','lambda_J':'1/4',
      'E_I':'2/5','E_R':'7/10','E_S':'11/10','identity_offset':'0'},
      'dstar':'3','epsilon_B':['1/8','-1/4'],'kappa':[['2/7','3/7'] for _ in range(4)],
      'old_hop_phases':phases,'born_hop_phases':[list(z) for z in phases for _ in range(2)]}


def universe():
    result=[]
    for sector,nv,ne in ((0,2,4),(1,4,8)):
        configurations=[(1<<v,0,1) for v in range(nv)]+[(0,1,0)]
        for inc in range(1<<ne):
            for carrier,ready,spent in configurations:
                for q in range(1<<nv):result.append((sector,inc,carrier,q,ready,spent))
    return result


def literal_column(state,index):
    sector,inc,p,q,r,s=state;nv=2 if sector==0 else 4
    edges=[(0,1)]*4 if sector==0 else [(0,3),(2,1)]*4
    phases=[(1,0),(0,-1),(-1,0),(0,1)]
    if sector:phases=[z for z in phases for _ in range(2)]
    degree=[0]*nv
    for e,(a,b) in enumerate(edges):
        if inc>>e&1:degree[a]+=1;degree[b]+=1
    # All actual parameters independently frozen from the accepted literal card.
    diagonal=(2240*pop(inc)+560*sum((d-3)**2 for d in degree)+560*pop(p)+490*pop(q)
      -70*sum(d*((q>>v)&1) for v,d in enumerate(degree))
      +140*sum(d*((p>>v)&1) for v,d in enumerate(degree))
      +224*(nv-pop(r|s))+392*pop(r)+616*pop(s))
    column={}
    def add(target,a,b=0):
        need(target in index,'complete native target domain')
        key=index[target];old=column.get(key,(0,0));new=(old[0]+a,old[1]+b)
        if new==(0,0):column.pop(key,None)
        else:column[key]=new
    add(state,diagonal)
    for e,(a,b) in enumerate(edges):
        add((sector,inc^(1<<e),p,q,r,s),-112)
        if inc>>e&1 and ((p>>a)&1)!=((p>>b)&1):
            re,im=phases[e]
            # phase multiplies b->a; conjugate multiplies a->b.
            add((sector,inc,p^(1<<a)^(1<<b),q,r,s),-560*re,560*im if p>>a&1 else -560*im)
    for v in range(nv):
        bit=1<<v
        if p&bit:add((sector,inc,p,q^bit,r,s),280)
        if r&bit and not p&bit:add((sector,inc,p|bit,q,r^bit,s|bit),160,240)
        if s&bit and p&bit:add((sector,inc,p^bit,q,r|bit,s^bit),160,-240)
    if sector==0 and pop(inc)==2:
        lifted=sum(3<<(2*e) for e in range(4) if inc>>e&1)
        add((1,lifted,p,q,r,s),70,-140)
    elif sector==1 and not (p|q|r|s)&12:
        pairs=[(inc>>(2*e))&3 for e in range(4)]
        if all(v in (0,3) for v in pairs) and pairs.count(3)==2:
            old=sum(1<<e for e,v in enumerate(pairs) if v==3)
            add((0,old,p,q,r,s),70,140)
    return column


def reconstruct(lines,selected,component_record):
    states=universe();index={s:i for i,s in enumerate(states)}
    need(len(states)==20672,'independent entire state enumeration')
    stream=iter(lines);first=next(stream)
    need(first['kind']=='basis' and first['index']==0,'initial complete basis')
    basis=first['payload']
    need(basis['states']==[list(s) for s in states],'actual exact ordered basis')
    need(basis['parameters']==expected_parameters(),'all literal parameter fields')
    edges=[[[0,1]]*4,[[0,3],[2,1]]*4]
    need(basis['graph_edges']==edges and basis['cuts']==[0,1,2,3],'actual literal graph and cuts')
    columns=[]
    for j,state in enumerate(states):
        record=next(stream)
        need(record['kind']=='column' and record['index']==j and record['payload']['state']==list(state),'full source column census')
        expected=literal_column(state,index);given={}
        for entry in record['payload']['entries']:
            target=entry['target'];re,im=map(F,entry['value'])
            need(type(target) is int and target not in given and (re*560).denominator==1 and (im*560).denominator==1,'exact unique native coefficient')
            given[target]=(int(re*560),int(im*560))
        need(given==expected,'independent all-owner native column '+str(j))
        diagonal=expected.get(j,(0,0))
        need(list(map(F,record['payload']['diagonal']))==[F(diagonal[0],560),F(diagonal[1],560)],'column diagonal')
        need(F(record['payload']['H2_diagonal'])==sum(F(a*a+b*b,560*560) for a,b in expected.values()),'column squared norm')
        columns.append(expected)
    last=next(stream);need(last['kind']=='summary' and next(stream,None) is None,'complete source stream ends')
    for j,c in enumerate(columns):
        for i,(a,b) in c.items():need(columns[i].get(j)==(a,-b),'every complete native Hermitian mate')
    groups=[];owner={}
    for start in range(len(states)):
        if start in owner:continue
        label=len(groups);todo=[start];owner[start]=label;members=[]
        while todo:
            j=todo.pop();members.append(j)
            for i in columns[j]:
                if i not in owner:owner[i]=label;todo.append(i)
        groups.append(sorted(members))
    need(groups==[v['members'] for v in component_record['literal_components']],'all independently reconstructed components')
    need(sorted(map(len,groups))==[2048,2048,3072,3072,10432],'complete component dimensions')
    other=[tuple(s) for s in selected['states']]
    need(selected['Q']==1 and selected['active_mask']==1 and len(other)==20672 and set(other)==set(states),'whole selected-census bijection')
    reverse={s:i for i,s in enumerate(other)}
    seed=index[(0,3,1,3,0,1)];active=groups[owner[seed]];local={j:i for i,j in enumerate(active)}
    need(seed==39 and len(active)==10432 and owner[seed]==0,'fixed seed whole active component')
    rows=[{} for _ in active]
    for j in active:
        for i,(a,b) in columns[j].items():rows[local[i]][local[j]]=(a,b)
    for j,row in enumerate(rows):
        a,b=row.get(j,(0,0));a-=14847
        if a or b:row[j]=(a,b)
        else:row.pop(j,None)
    bound=F(max(sum(abs(a)+abs(b) for a,b in row.values()) for row in rows),560)
    need(bound==F(10207,560),'independently derived shifted row norm')
    packet={'shifted_row_norm':str(bound),'full_states':[list(s) for s in states],
      'native_to_selected_census':[reverse[s] for s in states],
      'selected_census_to_native':[index[s] for s in other],'components':groups,
      'all_component_weights':[1,0,0,0,0],'active_to_native':active,
      'active_states':[list(states[i]) for i in active],'seed_index':local[seed],
      'rows':[[[j,a,b] for j,(a,b) in sorted(row.items())] for row in rows],
      'shift':'2121/80','coefficient_denominator':560,'exact_all_component_invariance':True,
      'native_input_authentication':'EXTERNAL_ROOT_RECEIPTS_REQUIRED'}
    names=['OLD_CARRIER_SITE0','OLD_CARRIER_SITE1','OLD_READY_SITE0','OLD_COHERENT_PLUS_I','OLD_COHERENT_MINUS_I']
    a=(0,3,1,3,0,1);b=(0,3,2,3,0,1);ready=(0,3,0,3,1,0)
    kets=[[(a,'1','0')],[(b,'1','0')],[(ready,'1','0')],
          [(a,'3/5','0'),(b,'0','4/5')],[(a,'3/5','0'),(b,'0','-4/5')]]
    preps={};seeds={}
    for name,ket in zip(names,kets):
        entries=[];vector=[0j]*len(active)
        for state,re,im in ket:
            i=index[state];entries.append({'index':i,'state':list(state),'amplitude':[re,im]})
            vector[local[i]]=complex(float(F(re)),float(F(im)))
        preps[name]={'entries':entries,'all_component_weights':['1','0','0','0','0'],
          'sharp_Q':1,'active_mask':1,'old_q_word':'11','energy_distribution_matching':'NOT_ESTABLISHED',
          'S1_physical_preparation':'NOT_DERIVED'}
        seeds[name]=vector
    ss=[states[i] for i in active];words=['00','01','10','11']
    reads={w:[int(str(s[3]&1)+str((s[3]>>1)&1)==w) for s in ss] for w in words}
    reads.update(old_presence=[int(s[0]==0) for s in ss],born_presence=[int(s[0]==1) for s in ss],
      carriers=[pop(s[2]) for s in ss],Ready=[pop(s[4]) for s in ss],
      Nq_old=[pop(s[3]&3) for s in ss],Nq_all=[pop(s[3]) for s in ss])
    matrix=[[(j,complex(a/560,b/560)) for j,(a,b) in sorted(row.items())] for row in rows]
    return packet,preps,matrix,seeds,reads,float(bound),float(F(2121,80))
