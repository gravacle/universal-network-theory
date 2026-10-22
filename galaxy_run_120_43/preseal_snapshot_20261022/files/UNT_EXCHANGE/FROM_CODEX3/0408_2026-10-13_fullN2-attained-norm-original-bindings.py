"""SOURCE ONLY. Independent original C150 and checkpoint mathematical binding.
Root invocation; exact metadata custody supplied by checker, no producer oracle.
"""
from fractions import Fraction as Q
from pathlib import Path
import struct
S=1<<80
SEEDS=('OLD_CARRIER_SITE0','OLD_CARRIER_SITE1','OLD_READY_SITE0','OLD_COHERENT_PLUS_I','OLD_COHERENT_MINUS_I')
NAMES=('00','01','10','11','old_presence','born_presence','carriers','Ready','Nq_old','Nq_all')
PHASE='exp(-i(H-(2121/80)I)t), hbar=1'


def wire(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {k:wire(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [wire(x) for x in v]
    return v


def rational_read(read):
    # Only interval endpoints used by add_trapezoid; preserve other wire fields.
    out={**read}
    for group in ('words','diagonal'):
        out[group]={k:{**v,'interval':list(map(Q,v['interval']))} for k,v in read[group].items()}
    return out


def journal(pp,ig,seed,stage,C):
    item=ig['journals'][seed+':'+str(stage)]
    raw=pp(item['journal']);closure=C.decode(pp(item['closure']))
    C.need(closure['returncode']==0 and closure['cap_stop'] is None and closure['all_opening_pins_checked'] is True
        and closure['all_closing_pins_match'] is True,'original whole successful closure')
    prefix='NATIVE_PAYLOAD/' if seed==SEEDS[0] and stage==0 else ''
    C.exact(closure['outputs'][prefix+'OPERANDS.jsonl'],{'sha256':item['journal']['sha256'],'bytes':len(raw)},'whole original journal closure member')
    if not prefix:C.need(closure['payload_root']==str(Path(item['journal']['path']).parent),'same original payload root')
    C.need(raw.endswith(b'\n') and all(raw.splitlines()),'complete original journal lines')
    return [C.decode(line) for line in raw.splitlines()],closure,prefix,item


def vector(pp,item,closure,prefix,meta,C,guard):
    C.need(set(meta)=={'file','sha256','bytes','dimension','fractional_bits','endpoint_signed_bits','fields'},'complete original vector metadata')
    C.exact({k:meta[k] for k in ('dimension','fractional_bits','endpoint_signed_bits','fields')},
        {'dimension':10432,'fractional_bits':80,'endpoint_signed_bits':96,
         'fields':['real_lower','real_upper','imag_lower','imag_upper']},'frozen original I80 format')
    name=meta['file'];C.need(Path(name).name==name,'original vector basename')
    rec={'path':str(Path(item['journal']['path']).parent/name),'sha256':meta['sha256'],'bytes':meta['bytes']}
    C.exact(closure['outputs'][prefix+name],{'sha256':rec['sha256'],'bytes':rec['bytes']},'whole vector closure member')
    raw=pp(rec);C.need(len(raw)==500752 and raw[:8]==b'UNTI80V1' and struct.unpack('<II',raw[8:16])==(10432,4),'whole original vector binary')
    bounds=[]
    for index in range(10432):
        v=[int.from_bytes(raw[16+48*index+12*k:28+48*index+12*k],'little',signed=True) for k in range(4)]
        C.need(v[0]<=v[1] and v[2]<=v[3],'ordered all original coordinates');bounds.append(v)
        if index%256==0:guard()
    return bounds,rec


def initial(pp,ig,seed,states,C,R,guard):
    C.need(seed in SEEDS,'original five only');lookup={tuple(s):i for i,s in enumerate(states)}
    a,b,r=(0,3,1,3,0,1),(0,3,2,3,0,1),(0,3,0,3,1,0)
    if seed==SEEDS[0]:terms=[(a,Q(1),Q(0))]
    elif seed==SEEDS[1]:terms=[(b,Q(1),Q(0))]
    elif seed==SEEDS[2]:terms=[(r,Q(1),Q(0))]
    else:terms=[(a,Q(3,5),Q(0)),(b,Q(0),Q(4 if seed==SEEDS[3] else -4,5))]
    C.need(sum(x*x+y*y for _,x,y in terms)==1,'exact complete initial normalization')
    center=[[0,0] for _ in states];error=Q(0);entries=[]
    for state,re,im in terms:
        index=lookup[state]
        xr=re.numerator*S//re.denominator;xi=im.numerator*S//im.denominator
        center[index]=[xr,xi];error+=(re-Q(xr,S))+(im-Q(xi,S))
        entries.append({'active_index':index,'state':list(state),'amplitude':[re,im]})
    C.need(0<=error<Q(2,S),'floor initial L1 radius')
    rows,closure,prefix,item=journal(pp,ig,seed,0,C)
    pres=[x for x in rows if x.get('kind')=='microstep_pre' and x['index']==0]
    ledgers=[x['value'] for x in rows if x.get('kind')=='microstep_ledger' and x['index']==0]
    C.need(len(pres)==len(ledgers)==1 and Q(pres[0]['time'])==0 and Q(ledgers[0]['previous_L2_error'])==error,'actual same initial time/error')
    bounds,pin=vector(pp,item,closure,prefix,ledgers[0]['vector_files']['left'],C,guard)
    C.exact(bounds,[[re,re,im,im] for re,im in center],'all original exact initial point coordinates')
    if seed!=SEEDS[0]:
        starts=[x for x in rows if x.get('kind')=='stage_initial'];C.need(len(starts)==1,'unique initial preparation record')
        C.exact(starts[0]['center'],center,'whole original preparation');C.need(Q(starts[0]['L2_error'])==error and Q(starts[0]['time'])==0,'original preparation radius/time')
    binding={'seed':seed,'exact_entries':entries,'rounding_L2_upper':error,'original_journal':item,
        'original_initial_vector':pin,'all_initial_coordinates_compared':True}
    read=R.readout(states,center,error,guard)
    state={'center':center,'L2_error':str(error),'readout':wire(read),'integrals':{k:['0','0'] for k in NAMES},'step':0,'time':'0'}
    return state,wire(binding)


def average(seed,step,integrals,read,error,R,C):
    # Independent helper supplies ten exact intervals, using rational internal prefix.
    T=Q(step,512);items=R.average_intervals([integrals[k] for k in NAMES],step,R.operator_norms(read))
    words=dict(zip(NAMES[:4],items[:4]));diagonal=dict(zip(NAMES[4:],items[4:]))
    half=max((v['interval'][1]-v['interval'][0])/2 for v in words.values())
    return {'schema':'KRYLOV_FULL_N2_AVERAGE_V001','seed':seed,'step':step,'T':T,'panels':step,
        'averaged_words':words,'averaged_diagonal':diagonal,
        'statistics':R.statistics({k:v['interval'] for k,v in words.items()}),
        'max_word_half_width':half,'word_halfwidth_target_met':half<=Q(1,1024),'final_L2_error':Q(error),
        'quadrature':'UNIFORM_COMPOSITE_TRAPEZOID_LH_OVER_4','finite_window_only':True,'DE':False,'physical_preparation':False}


def horizon(pp,ig,seed,step,center,error,read,integrals,states,C,R,guard):
    stage=(64,128,256,512).index(step);rows,closure,prefix,item=journal(pp,ig,seed,stage,C)
    point=[x for x in rows if x.get('kind')=='readout' and Q(x['time'])==Q(step,512)]
    averages=[x['value'] for x in rows if x.get('kind')=='final_result_before_adjudication']
    C.need(len(point)==len(averages)==1,'unique whole original horizon read/average')
    original_read=point[0]['value'];oldaverage=averages[0]
    ledger=[x['value'] for x in rows if x.get('kind')=='microstep_ledger' and x['index']==point[0]['index']]
    C.need(len(ledger)==1,'unique complete endpoint ledger');ledger=ledger[0]
    bounds,pin=vector(pp,item,closure,prefix,ledger['vector_files']['final'],C,guard)
    C.need(all((a+b)%2==0 and (c+d)%2==0 for a,b,c,d in bounds),'all symmetric original final centers')
    oldcenter=[[(a+b)//2,(c+d)//2] for a,b,c,d in bounds];olderror=Q(ledger['accumulated_L2_error'])
    radius=(olderror.numerator*S+olderror.denominator-1)//olderror.denominator
    C.exact(bounds,[[re-radius,re+radius,im-radius,im+radius] for re,im in oldcenter],'every final coordinate certified radius')
    C.need(Q(original_read['L2_error'])==olderror and Q(oldaverage['T'])==Q(step,512)
        and Q(oldaverage['final_L2_error'])==olderror,'same complete original time/radius')
    reconstructed=R.readout(states,oldcenter,olderror,guard)
    C.exact(original_read,wire(reconstructed),'all original endpoint reads independently reconstructed')
    avg=average(seed,step,integrals,read,error,R,C)
    difference=Q(sum((a-c)**2+(b-d)**2 for (a,b),(c,d) in zip(center,oldcenter)),S*S)
    radius=Q(error)+olderror;avrows=[];ptrows=[]
    def compare(name,new,old):
        lo,hi=map(Q,new);ol,oh=map(Q,old)
        return {'observable':name,'krylov_interval':[lo,hi],'C150_interval':[ol,oh],
            'signed_difference_interval':[lo-oh,hi-ol],'nonempty_intersection':not(hi<ol or oh<lo)}
    for name in NAMES:
        group='averaged_words' if name in NAMES[:4] else 'averaged_diagonal'
        avrows.append(compare(name,avg[group][name]['interval'],oldaverage[group][name]['interval']))
        group='words' if name in NAMES[:4] else 'diagonal'
        ptrows.append(compare(name,read[group][name]['interval'],original_read[group][name]['interval']))
    comparison={'schema':'KRYLOV_FULL_N2_C150_COMPARISON_V001','endpoint_center_difference_squared':difference,
        'sum_L2_radii':radius,'squared_sum_L2_radii':radius*radius,'full_endpoint_bound_met':difference<=radius*radius,
        'all_ten_continuous_average_comparisons':avrows,'all_ten_endpoint_read_comparisons':ptrows,
        'all_average_intersections':all(x['nonempty_intersection'] for x in avrows),
        'all_endpoint_read_intersections':all(x['nonempty_intersection'] for x in ptrows),
        'same_midpoint_trajectories_claimed':False,'scientific_acceptance':False}
    return wire({'step':step,'time':Q(step,512),'original_journal':item,'original_endpoint_vector':pin,
        'new_average':avg,'original_average':oldaverage,'original_endpoint_read':original_read,'comparison':comparison})
