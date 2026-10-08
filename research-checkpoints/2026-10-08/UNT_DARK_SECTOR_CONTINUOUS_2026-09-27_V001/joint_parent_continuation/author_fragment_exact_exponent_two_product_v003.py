"""Held arithmetic adapter: preserve the inherited two-product where admitted.
Globals np, P and an explicit capture supplied to install_exact_exponent_product.
No import, scientific producer, payload, caller or invocation. Only a product
outside the inherited conservative splitter range receives exact power-of-two
normalization. Every restored product word must reverse exactly; true overflow
or irreducible underflow is a refusal, never a discarded active contribution.
The inherited two-product polynomial and all physical gates remain unchanged.
"""
EXACT_EXPONENT_PRODUCT_AUTHOR_DRAFT=True
EXACT_EXPONENT_PRODUCT_AUTHORING_IN_PROGRESS=False

def exact_exponent_two_product(x,y):
 x=np.asarray(x,dtype=np.float64);y=np.asarray(y,dtype=np.float64)
 safe=lambda a:(a==0)|((abs(a)>=2.**-450)&(abs(a)<=2.**450))
 if np.all(safe(x)) and np.all(safe(y)):return EXACT_EXPONENT_PRODUCT_ORIGINAL(x,y)
 capture=EXACT_EXPONENT_PRODUCT_CAPTURE;prefix=EXACT_EXPONENT_PRODUCT_LABEL;xb,yb=np.broadcast_arrays(x,y)
 capture(prefix+'_unsafe_input_broadcast_both',np.stack((xb,yb),axis=0))
 capture(prefix+'_input_x',x.copy());capture(prefix+'_input_y',y.copy())
 assert np.all(np.isfinite(x)) and np.all(np.isfinite(y))
 x,y=xb,yb;admitted=safe(x)&safe(y)
 high=np.zeros(x.shape,dtype=np.float64);low=np.zeros_like(high)
 capture(prefix+'_inherited_domain_mask',admitted.astype(np.int64))
 if np.any(admitted):high[admitted],low[admitted]=EXACT_EXPONENT_PRODUCT_ORIGINAL(x[admitted],y[admitted])
 zero=(~admitted)&((x==0)|(y==0));active=(~admitted)&(~zero)
 # An exact zero factor has an exact zero product; signed high zero is retained.
 high[zero]=x[zero]*y[zero]
 capture(prefix+'_exact_zero_factor_mask',zero.astype(np.int64));capture(prefix+'_balanced_active_mask',active.astype(np.int64))
 if np.any(active):
  xa,ya=x[active],y[active];mx,ex=np.frexp(xa);my,ey=np.frexp(ya);exponent=ex.astype(np.int64)+ey.astype(np.int64)
  for n,a in (('active_x',xa),('active_y',ya),('mantissa_x',mx),('mantissa_y',my),('exponent_x',ex),('exponent_y',ey),('product_exponent',exponent)):capture(prefix+'_'+n,np.asarray(a).copy())
  backx=np.ldexp(mx,ex);backy=np.ldexp(my,ey)
  capture(prefix+'_input_round_trip_x',backx.copy());capture(prefix+'_input_round_trip_y',backy.copy())
  assert np.array_equal(backx,xa) and np.array_equal(backy,ya),'Input power-of-two normalization must be exact'
  ph,pl=EXACT_EXPONENT_PRODUCT_ORIGINAL(mx,my)
  capture(prefix+'_normalized_product_hi',ph.copy());capture(prefix+'_normalized_product_lo',pl.copy())
  # Retain attempted restoration before refusing nonfinite or lost low words.
  with np.errstate(over='ignore',under='ignore',invalid='ignore'):
   rh=np.ldexp(ph,exponent);rl=np.ldexp(pl,exponent)
   bh=np.ldexp(rh,-exponent);bl=np.ldexp(rl,-exponent)
  capture(prefix+'_restoration_attempt_all_words',np.stack((rh,rl,bh,bl),axis=0))
  for n,a in (('restored_product_hi',rh),('restored_product_lo',rl),('product_round_trip_hi',bh),('product_round_trip_lo',bl)):capture(prefix+'_'+n,np.asarray(a).copy())
  assert np.all(np.isfinite(rh)) and np.all(np.isfinite(rl)),'Exponent-balanced product restoration overflow'
  assert np.array_equal(bh,ph) and np.array_equal(bl,pl),'Exponent-balanced product restoration lost a word'
  high[active]=rh;low[active]=rl
 capture(prefix+'_product_hi',high.copy());capture(prefix+'_product_lo',low.copy())
 return high,low

def install_exact_exponent_product(arithmetic_scope,provider,capture,label):
 # Existing a_mul/a_mul64/a_div64 share this exact definition namespace.
 global EXACT_EXPONENT_PRODUCT_ORIGINAL,EXACT_EXPONENT_PRODUCT_CAPTURE,EXACT_EXPONENT_PRODUCT_LABEL
 original=arithmetic_scope['a_prod'];assert original is provider.a_prod
 assert original.__globals__ is arithmetic_scope and original is not exact_exponent_two_product
 EXACT_EXPONENT_PRODUCT_ORIGINAL=original;EXACT_EXPONENT_PRODUCT_CAPTURE=capture;EXACT_EXPONENT_PRODUCT_LABEL=label
 arithmetic_scope['a_prod']=exact_exponent_two_product;provider.a_prod=exact_exponent_two_product
 return original
