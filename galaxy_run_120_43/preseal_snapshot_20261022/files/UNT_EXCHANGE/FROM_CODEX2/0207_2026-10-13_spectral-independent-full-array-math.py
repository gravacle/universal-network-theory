"""SOURCE ONLY: whole-eigenarray reconstruction, no eigensolve/producer imports.
NumPy matrix products share the pinned backend but not producer source/flags.
All columns/Gram entries/seed/read outputs consumed, no sampled substitutes.
"""
import math
import numpy as np


def need(ok,label):
    if not ok:raise ValueError(label)


def reconstruct(rows,seeds,reads,scale,shift,E,V,progress,native=False):
    n=len(rows);names=list(seeds);labels=list(reads)
    need(E.shape==(n,) and V.shape==(n,n),'complete eigenarray shape')
    need(E.dtype==np.dtype('float64') and V.dtype==np.dtype('complex128'),'literal lossless array dtypes')
    need(np.isfinite(E).all() and np.all(E[1:]>=E[:-1]),'finite sorted complete eigenvalues')
    psi=np.array([seeds[k] for k in names],dtype=complex).T
    read=np.array([reads[k] for k in labels],dtype=float)
    need(psi.shape==(n,len(names)) and read.shape==(len(labels),n),'complete independent seed/read census')
    # Matrix elements are independently reconstructed before entry; verify all
    # mates again to make the sparse action convention explicit.
    maps=[dict(row) for row in rows]
    need(all(len(row)==len(mapping) for row,mapping in zip(rows,maps)),'unique matrix columns')
    for i,row in enumerate(maps):
        for j,z in row.items():need(maps[j].get(i,0)==z.conjugate(),'exact stored Hermiticity')
    def action(x):
        y=np.zeros_like(x)
        for i,row in enumerate(rows):
            if row:
                indices=[j for j,z in row];values=np.array([z for j,z in row])
                y[i]=values @ x[indices]
        need(np.isfinite(y).all(),'finite independent matrix action')
        return y
    C=np.empty((n,len(names)),dtype=complex);residual=[];gram_records=[]
    # Independent 128-row Gram blocks. Original records group64 columns;
    # Hermitian Gram defect has equal row/column squared norms, so split these
    # independently computed rows into matching64 records. No flag substitution.
    for lo in range(0,n,128):
        hi=min(n,lo+128);block=V[:,lo:hi]
        need(np.isfinite(block).all(),'every full eigenvector finite')
        adj=block.conj().T
        C[lo:hi]=adj@psi
        R=action(block)-block*E[lo:hi]
        residual.extend(np.sqrt(np.sum(np.abs(R)**2,axis=0)).tolist())
        G=adj@V
        G[np.arange(hi-lo),np.arange(lo,hi)]-=1
        for start in range(0,hi-lo,64):
            end=min(start+64,hi-lo)
            squared=float(np.sum(np.abs(G[start:end])**2,dtype=np.longdouble))
            gram_records.append({'lo':lo+start,'hi':lo+end,'squared_frobenius':squared})
        progress('INDEPENDENT_COMPLETE_GRAM_AND_RESIDUAL',lo,hi)
    gram2=math.fsum(r['squared_frobenius'] for r in gram_records)
    rf=math.sqrt(math.fsum(v*v for v in residual));gf=math.sqrt(gram2)
    norms=np.sum(np.abs(psi)**2,axis=0);modeweights=np.abs(C)**2
    need(np.isfinite(C).all() and np.isfinite(modeweights).all(),'finite reconstructed amplitudes')
    hp=action(psi)+shift*psi
    energies=np.sum(psi.conj()*hp,axis=0);seconds=np.sum(np.abs(hp)**2,axis=0)
    need(np.isfinite(energies).all() and np.isfinite(seconds).all(),'finite energies/seconds')
    def projector_statistics(groups):
        total=np.zeros((len(labels),len(names)),float);weights=[];single=[]
        for lo,hi in groups:
            weights.append(np.sum(modeweights[lo:hi],axis=0).tolist())
            if hi-lo==1:single.append(lo)
            else:
                projected=V[:,lo:hi]@C[lo:hi]
                total+=read@(projected.real**2+projected.imag**2)
        for start in range(0,len(single),128):
            indices=single[start:start+128];block=V[:,indices]
            diagonal_read=read@(block.real**2+block.imag**2)
            total+=diagonal_read@modeweights[indices]
        need(np.isfinite(total).all(),'all reconstructed spectral readouts finite')
        return {'values_by_read_then_seed':total.tolist(),'groups_half_open':groups,
                'weights_by_group_then_seed':weights,'exact_block_certificate':False}
    singleton=projector_statistics([[j,j+1] for j in range(n)])
    grouped=[]
    for tau in (1e-10,1e-8):
        threshold=tau*max(1.,scale);cuts=[0]
        cuts.extend(j for j in range(1,n) if float(E[j])-float(E[j-1])>threshold);cuts.append(n)
        result=projector_statistics([[a,b] for a,b in zip(cuts,cuts[1:])])
        result.update(tau=tau,absolute_threshold=threshold,grouping_scope='FLOAT_GAP_SENSITIVITY_ONLY_NOT_CERTIFIED_DEGENERACY')
        grouped.append(result);progress('INDEPENDENT_ALL_GROUP_READS',len(grouped),len(cuts)-1)
    passed=rf/max(1.,scale)<=1e-9 and gf<=1e-8
    answer={'status':'NUMERICAL_COMPARATOR_ONLY_EXACT_DE_UNRESOLVED' if passed else 'NUMERICAL_DIAGNOSTICS_FAILED',
      'seed_names':names,'read_names':labels,'dimension':n,'shifted_eigenvalues':E.tolist(),
      'absolute_eigenvalues':(E+shift).tolist(),'energy_shift_undone':shift,
      'residual_column_l2':residual,'residual_frobenius':rf,'full_gram_frobenius':gf,
      'full_gram_block_records':gram_records,'residual_relative_target':1e-9,'gram_target':1e-8,
      'diagnostics_passed':bool(passed),'diagnostic_matrix':'ROUNDED_STORED_H','seed_norms':norms.tolist(),
      'all_eigenmode_weights':modeweights.tolist(),'eigenmode_weight_sums':np.sum(modeweights,axis=0).tolist(),
      'original_energy':energies.tolist(),'original_second_moment':seconds.tolist(),
      'singleton_basis_diagonal_comparator':singleton,'coherent_group_comparators':grouped,
      'normalized_reference_read_ranges':[[float(min(read)),float(max(read))] for read in reads.values()],
      'reference_range_scope':'CONDITIONAL_ON_EXTERNALLY_AUTHENTICATED_EXACT_NORMALIZED_STATE_AND_EXACT_READ',
      'ranges_apply_to_rounded_supplied_seed':False,'desired_certified_word_half_width':'1/1024',
      'desired_certified_word_precision_met':False,'exact_DE_certified':False,'exact_degeneracy_certified':False,
      'Bohr_spacing_certified':False,'physical_state_selected':False,'EOS_claim':False,
      'native_prediction_release':False,'error_scope':'FLOAT_DIAGNOSTICS_WITHOUT_OUTWARD_ROUNDING_NOT_PROOF'}
    if native:
        words=['00','01','10','11']
        for result in [singleton]+grouped:
            statistics={};values=result['values_by_read_then_seed']
            for j,name in enumerate(names):
                law={w:values[i][j] for i,w in enumerate(words)};a=law['10']+law['11'];b=law['01']+law['11']
                statistics[name]={'words':law,'marginals':[a,b],'q0q1':law['11'],
                  'connected_covariance_of_averaged_state':law['11']-a*b,
                  'averaged_instantaneous_covariance_not_computed':True}
            pairs=[]
            for i,a in enumerate(names):
                for b in names[i+1:]:pairs.append({'a':a,'b':b,'TV_comparator_only':math.fsum(abs(statistics[a]['words'][w]-statistics[b]['words'][w]) for w in words)/2})
            result['persistent_word_statistics']=statistics;result['all_ten_seed_pairs']=pairs
        answer['normalized_reference_connected_covariance_range']=['-1/4','1/4']
    return answer
