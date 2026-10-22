"""SOURCE ONLY. Root-only complete control engine; no acceptance authority.
The root caller supplies pinned modules/libraries and bounded exclusive Sink.
Every result is RAW and requires a distinct whole saved comparison. No native
library or source is imported here; modules are explicit authenticated inputs.
"""
from array import array
from fractions import Fraction as Q
import ctypes as C
import math
import struct

TINY=('ONE_EXACT','ONE_ZERO','COMPLEX_TWO','SIGNED_BOUND_THREE','PHASE_PERMUTATION_SIXTEEN')
CASES=TINY+('DENSE_256','DENSE_512','DENSE_1024','QUANTIZER','BOUNDS_SEPARATED','BOUNDS_DEGENERATE','BOUNDS_BAD_GRAM','BOUNDS_CLUSTER4','REFUSALS')


def need(ok,why):
    if not ok:
        raise ValueError(why)


def column_major(w):
    n=len(w)
    return array('q',(w[i][j][z] for j in range(n) for i in range(n) for z in (0,1)))


def hrows(rows):
    return [[[i,z[0],z[1]] for i,z in row] for row in rows]


def fixture_metadata(fixture):
    w=fixture['w'];n=len(w)
    cols=[]
    for j in range(n):
        values=[abs(w[i][j][z]) for i in range(n) for z in (0,1)]
        cols.append({'column':j,'max_abs_integer_component':max(values),'component_l1_integer':sum(values)})
    return cols,[sum(abs(z[0])+abs(z[1]) for i,z in row) for row in fixture['rows']]


def compare_kernel(case,mods,sink,libraries):
    Ref,A,I=mods['independent_reference'],mods['abi'],mods['independent_abi']
    fixture=Ref.dense_control(int(case.split('_')[1])) if case.startswith('DENSE_') else next(x for x in Ref.tiny_controls() if x['name']==case)
    n=Ref.validated(fixture['w'],fixture['lam'],fixture['rows'])
    sink.save('FIXTURE',{'name':case,'dimension':n,'lambda_integers':fixture['lam'],'H_rows':fixture['rows'],
                        'matrix_wire':'W_INTEGER.bin row-major signed64 complex; G/R column-major signed128 complex'})
    wf=sink.binary('W_INTEGER.bin',b'UNTW64V1'+struct.pack('<II',n,2))
    for row in fixture['w']:
        sink.binary_append(wf,b''.join(struct.pack('<qq',*z) for z in row))
        sink.guard()
    wpin=sink.binary_close(wf)
    metadata,row_l1=fixture_metadata(fixture)
    mpin=sink.save('EXACT_COLUMN_METADATA',{'columns':metadata,'H_row_l1':row_l1})
    producer=A.Kernel(libraries['producer'],sink.pin,n,column_major(fixture['w']),array('q',fixture['lam']),sink.guard,
                     lambda name,value:sink.append('KERNEL_EVENTS.jsonl',{'name':name,'value':value}),
                     lambda value:sink.append('PROGRESS.jsonl',value))
    gram=producer.gram();residual=producer.residual(hrows(fixture['rows']))
    sink.save('PRODUCER_NORMS',{'gram':gram,'residual':residual})
    independent=I.Independent(libraries['independent'],sink.pin,fixture,sink.guard)
    gf=sink.binary('GRAM_INTEGER.bin',b'UNTI128G'+struct.pack('<II',n,2))
    rf=sink.binary('RESIDUAL_INTEGER.bin',b'UNTI128R'+struct.pack('<II',n,2))
    gnorms,rnorms=[],[]
    for j in range(n):
        sink.append('INDEPENDENT_EVENTS.jsonl',{'kind':'PRE','column':j,'fixture_W':wpin,
                    'metadata_reference':mpin,'functions':['p49i_gram_column','p49i_residual_column','exact_column']})
        g=independent.column(j,'gram');r=independent.column(j,'residual')
        # Full actual C++ output is retained, independent of subsequent equality.
        gbytes=b''.join(int(x).to_bytes(16,'little',signed=True) for z in g['entries'] for x in z)
        rbytes=b''.join(int(x).to_bytes(16,'little',signed=True) for z in r['entries'] for x in z)
        sink.binary_append(gf,gbytes);sink.binary_append(rf,rbytes)
        expected=Ref.exact_column(fixture['w'],fixture['lam'],fixture['rows'],j)
        flat=[]
        for item in metadata:
            v=item['component_l1_integer'];flat.extend([item['max_abs_integer_component'],v&((1<<64)-1),v>>64])
        comparisons={
            'all_gram_entries':g['entries']==[list(z) for z in expected['gram']],
            'all_residual_entries':r['entries']==[list(z) for z in expected['residual']],
            'gram_squared_norm':g['squared_norm']==expected['gram_norm_squared']==gram['squared_column_numerators'][j],
            'residual_squared_norm':r['squared_norm']==expected['residual_norm_squared']==residual['squared_column_numerators'][j],
            'all_gram_metadata':g['metadata']==flat,
            'all_H_row_l1':r['metadata']==row_l1}
        sink.append('INDEPENDENT_EVENTS.jsonl',{'kind':'RETURN','column':j,'status_gram':g['status'],'status_residual':r['status'],
            'gram_squared_norm':g['squared_norm'],'residual_squared_norm':r['squared_norm'],
            'full_actual_matrix_column_byte_offset':16+32*n*j,'matrix_column_bytes':32*n,
            'metadata_reference':mpin,'complete_in_process_comparisons':comparisons,
            'distinct_saved_comparison_required':True})
        if not all(comparisons.values()):
            sink.save('FIRST_MISMATCH',{'column':j,'gram_actual':g,'residual_actual':r,'full_python_expected':expected})
            raise ValueError('complete control comparison mismatch')
        gnorms.append(g['squared_norm']);rnorms.append(r['squared_norm']);sink.guard()
    gp,rp=sink.binary_close(gf),sink.binary_close(rf)
    need(gram['complete_column_metadata']==metadata and residual['all_row_l1_integers']==row_l1,'all producer metadata')
    return {'status':'RAW_COMPLETE_CONTROL_PENDING_DISTINCT_COMPARISON','case':case,'dimension':n,
            'complete_W':wpin,'complete_Gram':gp,'complete_residual':rp,'all_columns':n,
            'all_gram_column_squares':gnorms,'all_residual_column_squares':rnorms,
            'complete_reference_and_two_compiled_implementations_compared':True,'scientific_acceptance':False}


def npy_bytes(bits,shape,descr,fortran):
    # Tiny fixtures only: exact NPY1 header and literal IEEE scalar words.
    header=repr({'descr':descr,'fortran_order':fortran,'shape':shape}).encode('latin1')
    header+=b' '*((-10-len(header)-1)%64)+b'\n'
    raw=b'\x93NUMPY'+bytes((1,0))+struct.pack('<H',len(header))+header
    order='little' if descr[0]=='<' else 'big'
    return raw+b''.join(int(b).to_bytes(8,order) for b in bits)


def quantizer(mods,sink):
    D=mods['reference'];words=[0,1,0x000fffffffffffff,0x0010000000000000,
        0x3fefffffffffffff,0x3ff0000000000000,0x3ff0000000000001,0x3fffffffffffffff,
        0x4000000000000000,0x4034000000000000]
    words=words+[x|(1<<63) for x in words]
    records=[]
    for bits in words:
        value=struct.unpack('<d',bits.to_bytes(8,'little'))[0]
        numerator,denominator=value.as_integer_ratio()
        for scale,floor in ((55,False),(48,True)):
            scaled=Q(numerator*(1<<scale),denominator)
            expected=scaled.numerator//scaled.denominator if floor else int(scaled)
            actual=D.scaled_binary64(bits,scale,floor)
            record={'bits':bits,'scale':scale,'floor':floor,'exact_original_ratio':[numerator,denominator],
                    'actual':actual,'independent_ratio_expected':expected}
            sink.append('CONTROL_EVENTS.jsonl',record);need(actual==expected,'every exact scalar quantizer case')
            records.append(record)
    for bits in (0x7ff0000000000000,0xfff0000000000000,0x7ff8000000000000,0xfff8000000000001):
        try:
            D.scaled_binary64(bits,55)
        except ValueError as error:
            sink.append('CONTROL_EVENTS.jsonl',{'bits':bits,'exception':'ValueError','message':str(error)})
        else:
            raise ValueError('nonfinite quantizer did not refuse')
    n=3
    # Full row-major complex bit pairs include signed zeros and subnormals.
    pairs=[(words[(2*j)%len(words)],words[(2*j+1)%len(words)]) for j in range(n*n)]
    # Keep every vector component within two, independently of scalar energy cases.
    pairs=[(a if (a&((1<<63)-1))<=0x4000000000000000 else 0,
            b if (b&((1<<63)-1))<=0x4000000000000000 else 0) for a,b in pairs]
    energies=[0xbff0000000000000,0,0x3ff0000000000001]
    variants=[]
    for endian in ('<','>'):
        for fortran in (False,True):
            name=('LE' if endian=='<' else 'BE')+('_F' if fortran else '_C')
            order=[i*n+j for j in range(n) for i in range(n)] if fortran else list(range(n*n))
            vb=npy_bytes([x for i in order for x in pairs[i]],(n,n),endian+'c16',fortran)
            eb=npy_bytes(energies,(n,),endian+'f8',fortran)
            vp=sink.blob('V_'+name+'.npy',vb);ep=sink.blob('E_'+name+'.npy',eb)
            w,lam,meta=D.reconstruct(vp,ep,n,sink.guard,lambda x:sink.append('PROGRESS.jsonl',{'variant':name,**x}))
            expected=[]
            for j in range(n):
                for i in range(n):
                    for bits in pairs[i*n+j]:
                        a,b=struct.unpack('<d',bits.to_bytes(8,'little'))[0].as_integer_ratio()
                        expected.append(int(Q(a*(1<<55),b)))
            lexpected=[]
            for bits in energies:
                a,b=struct.unpack('<d',bits.to_bytes(8,'little'))[0].as_integer_ratio()
                lexpected.append((a*(1<<48))//b)
            record={'variant':name,'actual_W_integers':list(w),'actual_lambda_integers':list(lam),
                    'reference_metadata':meta,'independent_W':expected,'independent_lambda':lexpected}
            sink.save('CONVERSION_'+name,record)
            need(list(w)==expected and list(lam)==lexpected,'all complete endian/order conversions')
            variants.append(name)
    refusals=[]
    base_v=[x for pair in pairs for x in pair]
    cases=[('unsorted_E',base_v,[energies[2],0,energies[0]],(n,n),'<c16',b''),
           ('nonfinite_E',base_v,[energies[0],0,0x7ff0000000000000],(n,n),'<c16',b''),
           ('lambda_bound',base_v,[energies[0],0,0x4034000000000001],(n,n),'<c16',b''),
           ('nonfinite_W',[0x7ff8000000000000]+base_v[1:],energies,(n,n),'<c16',b''),
           ('W_bound',[0x4000000000000001]+base_v[1:],energies,(n,n),'<c16',b''),
           ('wrong_shape',base_v,energies,(n,n+1),'<c16',b''),
           ('wrong_dtype',base_v,energies,(n,n),'<f8',b''),
           ('trailing_payload',base_v,energies,(n,n),'<c16',b'X')]
    for name,vbits,ebits,shape,dtype,tail in cases:
        vp=sink.blob('REFUSE_V_'+name+'.npy',npy_bytes(vbits,shape,dtype,False)+tail)
        ep=sink.blob('REFUSE_E_'+name+'.npy',npy_bytes(ebits,(n,),'<f8',False))
        sink.append('CONTROL_EVENTS.jsonl',{'PRE':{'refusal':name,'vectors':vp,'values':ep}})
        try:D.reconstruct(vp,ep,n,sink.guard,lambda x:sink.append('PROGRESS.jsonl',{'refusal':name,**x}))
        except ValueError as error:
            record={'name':name,'exception':'ValueError','message':str(error)}
            sink.append('CONTROL_EVENTS.jsonl',{'RETURN':record});refusals.append(record)
        else:raise ValueError('invalid original-array fixture accepted '+name)
    return {'status':'RAW_COMPLETE_CONTROL_PENDING_DISTINCT_COMPARISON','case':'QUANTIZER',
            'scalar_cases':len(records),'nonfinite_refusals':4,'whole_array_variants':variants,'full_array_refusals':refusals,'scientific_acceptance':False}


def bounds_case(case,mods,sink,libraries):
    M,A,Ref=mods['bounds'],mods['abi'],mods['independent_reference']
    n=4 if case=='BOUNDS_CLUSTER4' else 2;s=1<<55
    w=tuple(tuple((s if i==j and case!='BOUNDS_BAD_GRAM' else 0,0) for j in range(n)) for i in range(n))
    separated=case=='BOUNDS_SEPARATED'
    levels=(0,1,1,2) if n==4 else (0,1) if separated or case=='BOUNDS_BAD_GRAM' else (0,0)
    lam=tuple(x*(1<<48) for x in levels)
    rows=tuple(((i,(560*x,0)),) if x else () for i,x in enumerate(levels))
    fixture={'w':w,'lam':lam,'rows':rows}
    sink.save('FIXTURE',{'name':case,'w':w,'lam':lam,'rows':rows,'manufactured_only':True})
    kernel=A.Kernel(libraries['producer'],sink.pin,n,column_major(w),array('q',lam),sink.guard,
                   lambda name,value:sink.append('KERNEL_EVENTS.jsonl',{'name':name,'value':value}),
                   lambda value:sink.append('PROGRESS.jsonl',value))
    gram,residual=kernel.gram(),kernel.residual(hrows(rows))
    # Independent exact complete columns retained, never only expected-zero flags.
    reference=list(Ref.complete_columns(w,lam,rows));sink.save('FULL_PYTHON_REFERENCE',reference)
    need(gram['squared_column_numerators']==[x['gram_norm_squared'] for x in reference] and
         residual['squared_column_numerators']==[x['residual_norm_squared'] for x in reference],'whole control norms')
    seeds={M.SEEDS[0]:[[0,5,0]],M.SEEDS[1]:[[1,5,0]],M.SEEDS[2]:[[0,5,0]],
           M.SEEDS[3]:[[0,3,0],[1,0,4]],M.SEEDS[4]:[[0,3,0],[1,0,-4]]}
    # Complete non-native read fixture, all ten read names/ranges retained.
    words=['00','11'] if n==2 else ['00','01','10','11']
    diagonals={name:[int(word==name) for word in words] for name in M.WORDS}
    diagonals.update({'old_presence':[int(i%2==0) for i in range(n)],'born_presence':[int(i%2==1) for i in range(n)],
        'carriers':[int(i%2==0) for i in range(n)],'Ready':[int(i%2==1) for i in range(n)],
        'Nq_old':[word.count('1') for word in words],'Nq_all':[word.count('1')+2*int(i%2==1) for i,word in enumerate(words)]})
    dp=sink.save('DIAGONALS_AND_SEEDS',{'identity':[1]*n,'reads':diagonals,'seeds':seeds,'manufactured_only':True})
    products=M.seed_products(column_major(w),n,seeds,sink.guard);sink.save('ALL_SEED_PRODUCTS',products)
    single=[[j,j+1] for j in range(n)]
    parts={'singleton':single,'original_tau_1e-10':[[0,1],[1,3],[3,4]] if n==4 else single,
           'original_tau_1e-8':[[0,1],[1,3],[3,4]] if n==4 else [[0,n]],'all_spectrum':[[0,n]]}
    sink.save('PARTITIONS',parts)
    result=M.certify(n,array('q',lam),gram,residual,parts,products,diagonals,dp,kernel,sink.save,sink.guard)
    expected={}
    for name,terms in seeds.items():
        weights=[Q(0) for _ in range(n)]
        for i,a,b in terms:
            weights[i]+=Q(a*a+b*b,25)
        expected[name]={read:sum(weights[i]*diagonals[read][i] for i in range(n)) for read in M.READS}
    # Known diagonal H and diagonal reads have these exact dephased values even
    # in the degenerate case. Broad fallback remains honest/inconclusive there.
    for name in M.SEEDS:
        for read in M.READS:
            lo,hi=result['intersections'][name][read]
            need(lo<=expected[name][read]<=hi,'all fifty exact control targets enclosed')
            if separated:
                need(lo==hi==expected[name][read],'all singleton exact answers')
    if case in ('BOUNDS_DEGENERATE','BOUNDS_BAD_GRAM'):
        need(result['partitions']['singleton']['status']=='UNCERTIFIED' and result['status']=='CERTIFICATE_INCONCLUSIVE','genuine gap/polar refusal and broad fallback')
    if n==4:
        need(result['partitions']['singleton']['status']=='UNCERTIFIED' and result['partitions']['original_tau_1e-10']['status']=='CERTIFIED_OUTER_BOUND','unresolved internal cluster retained with complete rank2 compression')
    return {'status':'RAW_COMPLETE_CONTROL_PENDING_DISTINCT_COMPARISON','case':case,
            'complete_bound_result':result,'all_fifty_exact_targets':expected,'scientific_acceptance':False}


def run(case,mods,sink,libraries):
    need(case in CASES,'fixed complete control case')
    if case in TINY or case.startswith('DENSE_'):
        return compare_kernel(case,mods,sink,libraries)
    if case=='QUANTIZER':
        return quantizer(mods,sink)
    if case.startswith('BOUNDS_'):
        return bounds_case(case,mods,sink,libraries)
    return refusals(mods,sink,libraries)


def refusals(mods,sink,libraries):
    A,I,M,D=mods['abi'],mods['independent_abi'],mods['bounds'],mods['reference']
    s=1<<55
    producer=A.Kernel(libraries['producer'],sink.pin,1,array('q',[s,0]),array('q',[0]),sink.guard,
        lambda name,value:sink.append('KERNEL_EVENTS.jsonl',{'name':name,'value':value}),
        lambda value:sink.append('PROGRESS.jsonl',value))
    fixture={'w':(((s,0),),),'lam':(0,),'rows':(((0,(560,0)),),)}
    independent=I.Independent(libraries['independent'],sink.pin,fixture,sink.guard)
    sink.save('FIXTURE',fixture)
    results=[]
    weights_pin=sink.save('CANCELLATION_WEIGHTS',{'identity':[1]})
    # Safe invalid-dimension guards are before all input dereferences in these
    # exact pinned C++ functions. Other cases own full correctly typed buffers.
    def raw_case(name,n=1,j=0,wvalue=s,lamvalue=0,offsets=(0,1),indices=(0,),values=(560,0),nnz=1,kind='residual'):
        count=n if 1<=n<=10432 else 1
        w=(A.I64*(2*count*count))();w[0]=wvalue
        lam=(A.I64*count)(*[lamvalue]*count)
        off=(A.U64*len(offsets))(*offsets);ix=(A.U32*max(1,len(indices)))(*indices)
        val=(A.I64*max(1,len(values)))(*values)
        sums,meta=(A.U32*(16*count))(),(A.U64*(3*count))()
        mag,sign,norm,imeta=(I.U64*(4*count))(),(I.I32*(2*count))(),(I.U64*8)(),(I.U64*(3*count))()
        pre={'name':name,'n':n,'j':j,'W':list(w),'lambda':list(lam),
             'offsets':offsets,'indices':indices,'values':values,'nnz':nnz,'kind':kind}
        sink.append('CONTROL_EVENTS.jsonl',{'PRE':pre})
        if kind=='gram':
            a=producer.gram_function(n,w,sums,meta,producer.callback)
            b=independent.g(n,j,w,mag,sign,norm,imeta,independent.hook)
        else:
            a=producer.residual_function(n,w,lam,off,ix,val,nnz,sums,meta,producer.callback)
            b=independent.r(n,j,w,lam,nnz,off,ix,val,mag,sign,norm,imeta,independent.hook)
        out={'name':name,'producer_status':a,'independent_status':b,'all_output_buffers_discarded':True}
        sink.append('CONTROL_EVENTS.jsonl',{'RETURN':out});results.append(out)
        need(a!=0 and b!=0,'both literal compiled guards must refuse '+name)
    raw_case('n_zero',n=0,kind='gram')
    raw_case('n_above_limit',n=10433,kind='gram')
    raw_case('W_above_limit',wvalue=(1<<56)+1,kind='gram')
    raw_case('W_below_limit',wvalue=-(1<<56)-1,kind='gram')
    raw_case('lambda_above_limit',lamvalue=20*(1<<48)+1)
    raw_case('CSR_start',offsets=(1,1))
    raw_case('CSR_end',offsets=(0,0))
    raw_case('CSR_column',indices=(1,))
    raw_case('CSR_decreasing',n=2,offsets=(0,2,1),indices=(0,),values=(560,0))
    raw_case('H_row_bound',values=(10208,0))
    raw_case('nnz_limit',offsets=(0,65),indices=tuple(0 for _ in range(65)),values=tuple(x for _ in range(65) for x in (1,0)),nnz=65)
    mag,sign,norm,meta=(I.U64*4)(),(I.I32*2)(),(I.U64*8)(),(I.U64*3)()
    status=independent.g(1,1,independent.w,mag,sign,norm,meta,independent.hook)
    record={'name':'independent_column_outside','n':1,'j':1,'status':status,'all_output_buffers_discarded':True}
    sink.append('CONTROL_EVENTS.jsonl',record);need(status!=0,'j=n must refuse');results.append(record)
    # Independent CSR has stronger canonical-input checks than producer kernel.
    # Producer wrapper rejects duplicate/unsorted/zero rows before foreign calls.
    for name,rows in (('duplicate_H',[[[0,1,0],[0,1,0]]]),('zero_H',[[[0,0,0]]])):
        try:
            producer.residual(rows)
        except ValueError as error:
            out={'name':name,'producer_wrapper_exception':'ValueError','message':str(error)}
            sink.append('CONTROL_EVENTS.jsonl',out);results.append(out)
        else:
            raise ValueError('noncanonical H wrapper accepted '+name)
        bad={'w':(((s,0),),),'lam':(0,), 'rows':tuple(tuple((i,(a,b)) for i,a,b in row) for row in rows)}
        target=I.Independent(libraries['independent'],sink.pin,bad,sink.guard)
        try:target.column(0,'residual')
        except ValueError as error:
            out={'name':'independent_'+name,'full_fixture':bad,'exception':'ValueError','message':str(error)}
            sink.append('CONTROL_EVENTS.jsonl',out);results.append(out)
        else:raise ValueError('independent noncanonical H accepted '+name)

    producer.callback=A.TICK(producer._tick)
    for name,weight,first,rank in (('weight_above_range',5,0,1),('zero_rank',1,0,0),('first_outside',1,1,1)):
        weights=(A.U32*1)(weight);mag=(A.U64*4)();sign=(A.I32*2)()
        status=producer.compression_function(1,producer.wp,weights,first,rank,mag,sign,producer.callback)
        record={'name':name,'weights':[weight],'first':first,'rank':rank,'status':status,'all_output_buffers_discarded':True}
        sink.append('CONTROL_EVENTS.jsonl',record);need(status!=0,'invalid compression domain must refuse');results.append(record)
    bad={'w':(((s,0),(0,0)),((0,0),(s,0))),'lam':(0,0),'rows':(((1,(1,0)),(0,(1,0))),())}
    target=I.Independent(libraries['independent'],sink.pin,bad,sink.guard)
    try:target.column(0,'residual')
    except ValueError as error:
        record={'name':'independent_unsorted_H','full_fixture':bad,'exception':'ValueError','message':str(error)}
        sink.append('CONTROL_EVENTS.jsonl',record);results.append(record)
    else:raise ValueError('independent unsorted H accepted')
    for kind,phases in (('gram',(0,1,2)),('residual',(3,4)),('compression',(5,))):
        for phase in phases:
            seen=[]
            def cancel(p,c):
                try:
                    sink.guard();seen.append([int(p),int(c)])
                    return int(p==phase)
                except BaseException as error:
                    producer.exception=error
                    return 1
            producer.callback=A.TICK(cancel)
            try:
                if kind=='gram':producer.gram()
                elif kind=='residual':producer.residual([[[0,560,0]]])
                else:producer.compression([1],0,1,'cancel',{'file':weights_pin,'field':['identity']})
            except ValueError as error:
                need(any(p==phase for p,c in seen),'requested producer cancellation phase reached')
                out={'name':'producer_cancel_'+kind+'_'+str(phase),'trace':seen,'exception':'ValueError','message':str(error)}
                sink.append('CONTROL_EVENTS.jsonl',out);results.append(out)
            else:raise ValueError('producer cancellation accepted')
    for kind,phases in (('gram',(0,1,2,3,4)),('residual',(1,10,11,12,13,14))):
        for phase in phases:
            seen=[]
            def cancel(p,j,k):
                try:
                    sink.guard();seen.append([int(p),int(j),int(k)])
                    return int(p==phase)
                except BaseException as error:
                    independent.exception=error
                    return 1
            independent.hook=I.HOOK(cancel)
            try:independent.column(0,kind)
            except ValueError as error:
                need(any(p==phase for p,j,k in seen),'requested independent cancellation phase reached')
                out={'name':'independent_cancel_'+kind+'_'+str(phase),'trace':seen,'exception':'ValueError','message':str(error)}
                sink.append('CONTROL_EVENTS.jsonl',out);results.append(out)
            else:raise ValueError('independent cancellation accepted')
    for name,masses,costs in (('LP_empty_box',[(Q(3,4),Q(1,2))],[Q(0)]),
                            ('LP_insufficient_mass',[(Q(0),Q(1,2))],[Q(0)]),
                            ('LP_excess_lower',[(Q(3,4),Q(1)),(Q(3,4),Q(1))],[Q(0),Q(1)])):
        try:M.extremize(masses,costs,False)
        except ValueError as error:
            out={'name':name,'masses':masses,'costs':costs,'exception':'ValueError','message':str(error)}
            sink.append('CONTROL_EVENTS.jsonl',out);results.append(out)
        else:raise ValueError('infeasible LP accepted')
    roots=[]
    for value in (0,1,2,(1<<220)-1,1<<220,(1<<220)+1):
        lo,hi,den=mods['independent_reference'].root_bracket(value,1<<110)
        actual=M.normroot(value,1<<110)
        need(actual==Q(hi,den) and lo*lo<=value<<256<=hi*hi,'full integer root bracket control')
        roots.append({'square':value,'lower':lo,'upper':hi,'denominator':den,'actual_upper':actual})
    sink.save('ROOT_BRACKETS',roots)
    # Exact LP extrema with nontrivial lower weights, caps and tied costs.
    masses=[(Q(1,8),Q(1,2)),(Q(1,4),Q(3,4)),(Q(0),Q(1,2))]
    costs=[Q(-1),Q(2),Q(2)]
    low=M.extremize(masses,costs,False);high=M.extremize(masses,costs,True)
    sink.save('LP_TIE_WITNESSES',{'masses':masses,'costs':costs,'lower':low,'upper':high})
    need(low['value']==Q(1,2) and high['value']==Q(13,8),'analytic complete LP extrema')
    return {'status':'RAW_COMPLETE_CONTROL_PENDING_DISTINCT_COMPARISON','case':'REFUSALS',
            'all_refusal_records':results,'root_brackets':len(roots),'scientific_acceptance':False}
