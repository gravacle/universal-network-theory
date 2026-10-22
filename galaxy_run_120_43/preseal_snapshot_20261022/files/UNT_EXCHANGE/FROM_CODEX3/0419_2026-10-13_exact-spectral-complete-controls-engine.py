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
CASES=TINY+('DENSE_256','DENSE_512','DENSE_1024','QUANTIZER','BOUNDS_SEPARATED','BOUNDS_DEGENERATE','REFUSALS')


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
    return {'status':'RAW_COMPLETE_CONTROL_PENDING_DISTINCT_COMPARISON','case':'QUANTIZER',
            'scalar_cases':len(records),'nonfinite_refusals':4,'whole_array_variants':variants,'scientific_acceptance':False}


def bounds_case(case,mods,sink,libraries):
    M,A,Ref=mods['bounds'],mods['abi'],mods['independent_reference']
    n=2;s=1<<55
    w=(((s,0),(0,0)),((0,0),(s,0)))
    separated=case=='BOUNDS_SEPARATED'
    lam=(0,(1<<48) if separated else 0)
    rows=((),((1,(560,0)),)) if separated else ((),())
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
    diagonals={name:([1,0] if k%2==0 else [0,cap]) for k,(name,cap) in enumerate(zip(M.READS,M.CAPS))}
    dp=sink.save('DIAGONALS_AND_SEEDS',{'identity':[1]*n,'reads':diagonals,'seeds':seeds,'manufactured_only':True})
    products=M.seed_products(column_major(w),n,seeds,sink.guard);sink.save('ALL_SEED_PRODUCTS',products)
    parts={'singleton':[[0,1],[1,2]],'original_tau_1e-10':[[0,1],[1,2]],
           'original_tau_1e-8':[[0,2]],'all_spectrum':[[0,2]]}
    sink.save('PARTITIONS',parts)
    result=M.certify(n,array('q',lam),gram,residual,parts,products,diagonals,dp,kernel,sink.save,sink.guard)
    expected={}
    for name,terms in seeds.items():
        weights=[Q(0),Q(0)]
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
    if not separated:
        need(result['partitions']['singleton']['status']=='UNCERTIFIED' and result['status']=='CERTIFICATE_INCONCLUSIVE','genuine zero-gap refusal and broad fallback')
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
