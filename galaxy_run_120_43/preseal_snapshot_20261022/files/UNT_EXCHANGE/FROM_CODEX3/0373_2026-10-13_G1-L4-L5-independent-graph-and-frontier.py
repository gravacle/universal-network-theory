"""SOURCE ONLY. Independent L4/L5 joined graph and capped fixed-point census.
Arithmetic radix coordinates and unpacked byte degree vectors; no producer
source imports, packed two-bit degrees, or base-radix winding keys. Root only.
"""


def need(ok,why):
    if not ok:raise ValueError(why)


def graph(L,sector,axes):
    need(type(L)is int and L in (4,5) and sector in ('old','Born') and
        type(axes)is list and axes in ([0,1,2],[0,2,1],[1,0,2],[2,1,0]),'sixteen frozen G1 operands')
    n=L**3;places=[L*L,L,1];cuts=[0,4*L*L,4*L,4];records=[]
    # ID edge=4*cell+colour, cell=x L²+y L+z; advance only its colour coordinate.
    for edge in range(4*n):
        cell,colour=divmod(edge,4)
        if sector=='Born' and edge in cuts:continue
        destination=cell
        if colour:
            stride=places[colour-1];coordinate=(cell//stride)%L
            destination+=stride if coordinate<L-1 else -(L-1)*stride
        records.append([edge,cell,n+destination])
    if sector=='Born':
        for slot,edge in enumerate(cuts):
            cell=edge//4
            records.extend([[4*n+2*slot,cell,2*n+1],[4*n+2*slot+1,2*n,n+cell]])
    records.sort();nv=2*n+(2 if sector=='Born' else 0)
    def permute_vertex(v):
        if v>=2*n:return v
        side,cell=divmod(v,n)
        return side*n+sum(((cell//places[a])%L)*places[axes[a]] for a in range(3))
    vertex_map=[permute_vertex(v) for v in range(nv)]
    need(sorted(vertex_map)==list(range(nv)),'full independent vertex permutation')
    lookup={(a,b):edge for edge,a,b in records}
    need(len(lookup)==len(records),'simple literal endpoint domain')
    image={edge:lookup[vertex_map[a],vertex_map[b]] for edge,a,b in records}
    need(set(image)==set(image.values()),'full independent edge bijection')
    remaining=set(image);orbits=[]
    while remaining:
        start=min(remaining);orbit=[start];cur=image[start]
        while cur!=start:
            need(cur not in orbit and cur in remaining,'disjoint closed edge orbit')
            orbit.append(cur);cur=image[cur]
        remaining.difference_update(orbit);orbits.append(sorted(orbit))
    boundary=[set() for _ in range(3)]
    for edge,a,b in records:
        if edge<4*n:
            cell,colour=divmod(edge,4)
            if colour and (cell//places[colour-1])%L==L-1:boundary[colour-1].add(edge)
    degree=[0]*nv
    for edge,a,b in records:degree[a]+=1;degree[b]+=1
    need(all(v==4 for v in degree),'entire four-valent bipartite graph')
    need(all(len(row)==L*L for row in boundary),'complete winding boundary planes')
    return {'L':L,'sector':sector,'axes':axes,'vertices':nv,'records':records,'image':image,
        'vertex_map':vertex_map,'orbits':orbits,'boundary':boundary,'cuts':cuts}


def reconstruct(g,guard):
    L,sector,axes,nv=(g[k] for k in ('L','sector','axes','vertices'))
    records,image,orbits,boundary,cuts=(g[k] for k in ('records','image','orbits','boundary','cuts'))
    endpoints={edge:(a,b) for edge,a,b in records};last=[-1]*nv;increments=[]
    for index,orbit in enumerate(orbits):
        inc={}
        for edge in orbit:
            for v in endpoints[edge]:inc[v]=inc.get(v,0)+1;last[v]=index
        increments.append(tuple(inc.items()))
    need(all(v>=0 for v in last),'no isolated degree constraint')
    retire=[[] for _ in orbits]
    for v,index in enumerate(last):retire[index].append(v)
    # Each key is an ordinary monomial exponent: full byte vertex degrees,
    # explicit K tuple, y exponent. Positive integer coefficients count all
    # orbit-subsets yielding that monomial. Retired vertex exponent must be2.
    table={(bytes(nv),(0,0,0),0):1};peak=1;progress=[]
    for index,orbit in enumerate(orbits):
        orbitset=set(orbit);dk=tuple(len(orbitset&boundary[a]) for a in range(3))
        dy=len(orbitset&set(cuts)) if sector=='old' else 0;output={}
        for ordinal,((degrees,k,y),coefficient) in enumerate(table.items()):
            if ordinal%256==0:guard()
            for selected in (0,1):
                d=bytearray(degrees);valid=True
                if selected:
                    for vertex,amount in increments[index]:
                        value=d[vertex]+amount
                        if value>2:valid=False;break
                        d[vertex]=value
                if not valid:continue
                for vertex in retire[index]:
                    if d[vertex]!=2:valid=False;break
                    d[vertex]=0
                if not valid:continue
                winding=tuple(k[a]+selected*dk[a] for a in range(3))
                if any(v>L*L for v in winding):continue
                marked=y+selected*dy;need(0<=marked<=4,'four original marked cuts')
                key=(bytes(d),winding,marked)
                if key not in output and len(output)==65536:
                    return {'schema':'P60_EXACT_ICE_FIXEDPOINT_V001','status':'COUNT_CAP_REFUSAL',
                        'L':L,'sector':sector,'axis_permutation':axes,
                        'message':'complete coefficient live-table cap65536','completed_orbits':index,
                        'total_orbits':len(orbits),'peak_completed_live_keys':peak,'live_cap':65536,
                        'dimension_inferred_from_partial_table':False,'spectrum_authorized':False,
                        'physical_release':False},progress
                output[key]=output.get(key,0)+coefficient
        table=output;peak=max(peak,len(table))
        progress.append({'kind':'EXACT_COEFFICIENT_FRONTIER','completed_orbits':index+1,
            'total_orbits':len(orbits),'live_keys':len(table),'live_cap':65536,
            'partial_table_is_dimension':False})
        guard()
    counts,eligible={},{}
    for (degree,k,y),coefficient in table.items():
        need(not any(degree),'every final vertex constraint discharged')
        key=','.join(map(str,k));counts[key]=counts.get(key,0)+coefficient
        if sector=='old' and y==2:eligible[key]=eligible.get(key,0)+coefficient
    # Full graph complement preserves each fixedness constraint and maps
    # K -> L²-K and y ->4-y, hence also the eligible y2 subset.
    for census in (counts,eligible):
        for key,value in census.items():
            opposite=','.join(str(L*L-int(k)) for k in key.split(','))
            need(census.get(opposite,0)==value,'whole complement bijection')
    return {'schema':'P60_EXACT_ICE_FIXEDPOINT_V001','status':'COMPLETE_EXACT_COUNT','L':L,
        'sector':sector,'axis_permutation':axes,'all_edges_stable_ids':records,
        'edge_permutation':[[edge,image[edge]] for edge in sorted(image)],'complete_edge_orbits':orbits,
        'all_K_fixed_counts':counts,'all_K_eligible_old_fixed_counts':eligible,
        'total_fixed_configurations':sum(counts.values()),'peak_live_keys':peak,'completed_orbits':len(orbits),
        'scope':'S3_SUBGROUP_ICE_FIXEDPOINTS_NOT_COMPLETE_OLD_RING_MOMENTUM_IRREPS','physical_release':False},progress
