"""HELD temporal-direction adapter to the independent105 cached rational oracle.
The105 algebra is general in its supplied paired direction; this adapter changes
only the input map to NEW scalar temporal phase words, with configuration zero.
No EOS/current/normal value or original chi-direction numerical body is called.
Globals np,P, chi_cached_contact_reference and its separately pinned definitions.
"""
PHASE_RATE_FRACTION_AUTHOR_DRAFT=True
PHASE_RATE_FRACTION_AUTHORING_IN_PROGRESS=False

def phase_rate_fraction_reference(prepared,phase_rate,normal_cache,f,b,point=None,bounds=False,keep=None,label=None):
 assert not PHASE_RATE_FRACTION_AUTHOR_DRAFT and not PHASE_RATE_FRACTION_AUTHORING_IN_PROGRESS
 p=prepared['s']['phi'][0].shape[0];assert all(a.shape==(p,) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in phase_rate)
 direction={n:P.a_dd(np.zeros(pair[0].shape)) for values in (prepared['s'],prepared['c']) for n,pair in values.items()}
 zero=P.a_dd(np.zeros(p));direction['phi']=P.a_stack([phase_rate,zero,zero,zero],1)
 return chi_cached_contact_reference(prepared,direction,normal_cache,f,b,point=point,bounds=bounds,keep=keep,label=label)
