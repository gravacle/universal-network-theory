"""Definitions only: full axisymmetric metric instantaneous circular balances.
Caller supplies np, math, Fraction and G (the resident full geodesic component).
No field solving, source changes, observational fitting or persistent-orbit claim.
"""
DYNAMIC_CIRCLE_AUTHOR_DRAFT=True

def full_dynamic_circle_coefficients(geometry,azimuth,meridional):
 g,dg=geometry['g'],geometry['dg']
 assert azimuth in (1,2,3) and tuple(meridional)==tuple(i for i in (1,2,3) if i!=azimuth)
 assert np.all(dg[azimuth]==0),'Axisymmetric circle interface required'
 a,b,c=(float(g[0,0]),float(g[0,azimuth]),float(g[azimuth,azimuth]))
 at,bt,ct=(float(dg[0,0,0]),float(dg[0,0,azimuth]),float(dg[0,azimuth,azimuth]))
 C_exact=Fraction.from_float(a)*Fraction.from_float(c)-Fraction.from_float(b)**2
 C=float(C_exact);assert math.isfinite(C) and c>0 and C_exact<0 and C<0,'Resolved timelike circle subspace required'
 f=np.array(((2*b*bt-c*at)/(2*C),b*ct/C,c*ct/(2*C)))
 Gcoef=np.array(((b*at-2*a*bt)/(2*C),-a*ct/C,-b*ct/(2*C)))
 coefficients=[]
 for m in meridional:
  fixed=np.array((dg[0,m,0]-.5*dg[m,0,0],dg[0,m,azimuth]-dg[m,0,azimuth],-.5*dg[m,azimuth,azimuth]))
  coefficients.append(fixed+g[m,0]*f+g[m,azimuth]*Gcoef)
 rows=np.asarray(coefficients);assert np.all(np.isfinite(rows)) and np.all(np.isfinite(f)) and np.all(np.isfinite(Gcoef))
 return dict(f=f,G=Gcoef,meridional_coefficients=rows,circle_determinant=C,exact_circle_determinant=dict(numerator=str(C_exact.numerator),denominator=str(C_exact.denominator)),azimuth=azimuth,meridional=tuple(meridional))

def full_dynamic_polynomial_roots(coefficients):
 q=np.asarray(coefficients,dtype=float);assert q.shape==(3,) and np.all(np.isfinite(q))
 c,b,a=map(float,q);scale=max(abs(c),abs(b),abs(a))
 if scale==0:return dict(kind='identically_zero_no_unique_circle',roots=[],discriminant=None,coefficient_power2_scale=None)
 exponent=math.frexp(scale)[1];q=np.ldexp(q,-exponent)
 assert np.all(np.isfinite(q)) and all(old==0 or new!=0 for old,new in zip((c,b,a),q)),'Polynomial scaling underflow'
 assert np.array_equal(np.ldexp(q,exponent),np.asarray(coefficients,dtype=float)),'Polynomial scaling not exactly reversible'
 c,b,a=map(float,q)
 if a==0:
  if b==0:return dict(kind='constant_nonzero_no_circle',roots=[],discriminant=None,coefficient_power2_scale=exponent)
  root=-c/b;assert math.isfinite(root);return dict(kind='linear',roots=[root],discriminant=None,coefficient_power2_scale=exponent)
 disc=Fraction.from_float(b)**2-4*Fraction.from_float(a)*Fraction.from_float(c)
 contact=dict(numerator=str(disc.numerator),denominator=str(disc.denominator))
 if disc<0:return dict(kind='negative_discriminant_no_circle',roots=[],discriminant=contact,coefficient_power2_scale=exponent)
 if disc==0:roots=[-b/(2*a)]
 else:
  d=float(disc);assert math.isfinite(d) and d>0,'Positive discriminant not resolved in binary64'
  stable=-.5*(b+math.copysign(math.sqrt(d),b));assert stable!=0
  roots=[stable/a,c/stable]
 assert all(math.isfinite(x) for x in roots)
 return dict(kind='quadratic_double_root' if disc==0 else 'quadratic_two_real_roots',roots=sorted(roots),discriminant=contact,coefficient_power2_scale=exponent)

def full_dynamic_circle_candidates(geometry,*,azimuth,meridional,radial):
 assert radial in meridional
 coeff=full_dynamic_circle_coefficients(geometry,azimuth,meridional)
 roots=full_dynamic_polynomial_roots(coeff['meridional_coefficients'][tuple(meridional).index(radial)])
 candidates=[];rejected=[]
 for omega in roots['roots']:
  f=float(np.polynomial.polynomial.polyval(omega,coeff['f']));Gvalue=float(np.polynomial.polynomial.polyval(omega,coeff['G']));omega_dot=Gvalue-omega*f
  D=float(geometry['g'][0,0]+2*omega*geometry['g'][0,azimuth]+omega*omega*geometry['g'][azimuth,azimuth])
  if not math.isfinite(D) or D>=0:
   rejected.append(dict(Omega=omega,D=D,reason='nonfinite_or_nontimelike'));continue
  w=np.zeros(3);w[azimuth-1]=omega;axis=np.zeros(3);axis[azimuth-1]=1.
  circle=G.dynamic_circle_residual(geometry,omega,omega_dot,azimuth,meridional)
  observer=G.normal_observer(geometry,w,'timelike',axis)
  rhs=G.geodesic_rhs(geometry,w,'timelike')
  candidates.append(dict(Omega=omega,Omega_dot=omega_dot,normal_axial_velocity=observer['axis_projection'],coordinate_velocity=w,derived_f=f,derived_G=Gvalue,circle=circle,observer=observer,geodesic=rhs))
 return dict(coefficients=coeff,root_diagnostics=roots,candidates=candidates,rejected=rejected,prediction_kind='local_metric_circular_snapshot',physical_metric_admitted=False,persistent_orbit_or_stability_claimed=False,observational_translation_qualified=False)
