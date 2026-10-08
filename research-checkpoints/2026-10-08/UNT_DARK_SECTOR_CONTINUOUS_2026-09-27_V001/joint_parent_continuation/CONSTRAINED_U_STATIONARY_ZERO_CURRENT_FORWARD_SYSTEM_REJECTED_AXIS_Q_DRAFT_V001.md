# Same-action stationary zero-current forward system V001

2026-10-06 UTC. Analytical continuation of the frozen spherical action78/ADM94. Root/native/readonly independently counterderived the following stationary reductions from those full equations. No numerical field, source inversion, solver or parameter value is evaluated/adopted. This is a conditional branch for an actual source calculation; exact FLRW matching remains a separate part of its boundary problem. The shared-epsilon measured-data result removes the particular narrow-band obstacle for its wider variants but does not solve this system.

## Exact spherical equations, after full variation

Use ds²=-N(r)²dt²+L(r)²dr²+r²dOmega² and phi=omega*t+psi(r). All retained mode/vector profiles are stationary. Put c=cosh(chi), s=sinh(chi), q=omega/N, Z=sum_j w_j z_j. The ADM phase spatial jet and pressure chart are
    p=(Z-s*q)/c, X²=q²-p², n=P_X(X), Q=(q+s*Z)/c.
Holonomy reconstructs p; it is not a fitted phase-gradient profile. A regular spherical centre forces the conserved stationary radial phase flux to zero. The exact reaction is therefore
    sigma=-n*p/(g_sigma*X*c), J_normal=n*Q/(c*X), J_radial=0,
    g_sigma=M²C, C=1.98, KB=.02.
Retain the admitted X/n chart and absolute P reference. Reconstruct psi by integrating L*p; additive phase origin is redundant. A coordinate rescaling of t and omega does not supply a second physical clock normalization.

Define A=c*N'/(N*L)+s*chi'/L, T=M²KB*A+g_sigma*Z, K_j=ell²*c²-s²/omega_j², and V_j=z_j²/2+z_j⁴/(4gc²xi_j⁴). The exact normalized stationary mode and vector rows are
    -[N*r²*K_j*z_j'/L]'/(N*L*r²)+z_j+z_j³/(gc²xi_j⁴)
                 +2ell²*c²*z_j/(L²*r²)=A+sigma,
    s*(T'+2*T/r)/L
       =g_sigma*s*c*sum_j w_j[(omega_j^(-2)-ell²)*(z_j'/L)²
                                     -2ell²*z_j²/(L²*r²)]-g_sigma*Q*sigma.
Keep the vector row undivided at s=0. K_j=0 is an actual characteristic/compatibility condition, not a denominator to regularize or a reason to discard a mode. The mode kinetic energy survives through convective U derivatives even though coordinate-time derivatives vanish.

On holonomy the complete material density is
    L_D=M²KB*A²/2+P+g_sigma*sum_j w_j[-K_j*(z_j'/L)²/2
                       -V_j-ell²*c²*z_j²/(L²*r²)+A*z_j].
The once-only Hilbert sources reduce to
    rho=-L_D+q*J_normal+(N*r²*c*T)'/(N*L*r²),
    p_r=P-M²KB*A²/2+g_sigma*sum_j w_j[K_j*(z_j'/L)²/2
                                      -V_j+ell²*c²*z_j²/(L²*r²)],
    p_perp=L_D+[N*r*g_sigma*ell²*c²*sum_j w_j*z_j²/L]'/(N*L*r²).
Using the independent vector equation, the complete momentum source is EXACTLY j_e=q*J_radial=0. This identity retains all acceleration/modal/metric contacts; setting them separately zero would not derive it. Add the actual ordinary rho,p_r,p_perp once. The metric obeys
    rho_total=M²*[r*(1-L^(-2))]'/r²,
    p_r,total=M²[(L^(-2)-1)/r²+2L^(-2)*N'/(r*N)],
plus the complete angular Einstein row from the frozen reduction, not an imposed Phi=Psi. Regular centre has L(0)=1 and chi,z_j,p=O(r), N'=O(r); an outward positive lapse gradient is a solved attractive-branch property, not prescribed. Full phase/angular/gravitational constraints and ordinary support must be retained.

## Axisymmetric observed source and current matching

NGC3198 requires its actual disk geometry and all four exposed measured-density source variants. In a zero-shift static spatial metric, let U=c*n_ADM+u with |u|²=c²-1, q=omega/N and p=d_spatial psi. An explicitly chosen zero-spatial-current branch gives
    sigma_spatial=-n*p/(g_sigma*X),
    sigma_normal=-n*(u.p)/(g_sigma*X*c),
    p=(I-u tensor u/c²)Z_spatial-q*u/c, Q=(q+u.Z_spatial)/c.
Enforce curl(p)=0 in addition to all poloidal/vector/modal/metric equations. General stationary axisymmetry permits divergence-free circulation, so zero spatial current is a branch assumption rather than a consequence of centre regularity. Keep the actual vector connection terms; spherical scalar equations do not automatically describe a disk. Modal stationary principal eigenvalues are ell² transverse to u and ell²*c²-|u|²/omega_j² along u after normalization. Ellipticity of those eigenvalues alone does not qualify the full coupled system or its non-axisymmetric stability.

An actual cosmological worldtube must match induced geometry/extrinsic curvature, the complete normal/tangential stress flux and phase J.s_worldtube. Homogeneous FLRW has nonzero advective J^r=n*H*r in areal coordinates. A positive static zero-spatial-flux interior cannot directly join at a cosmologically comoving moving wall to that exterior without a transition layer or an explicitly supplied exterior-current state: interior relative flux includes its charge density times wall velocity while the comoving FLRW relative flux is zero. A finite frozen boundary is therefore a conditional local response experiment, not an exact galaxy-and-expansion junction. No phase surface layer, reflected wall, selected incoming halo or hidden density offset is supplied here.

The constructive next problem is the observed-source field response together with that actual transition/current or a declared evolving Cauchy preparation. Current ingredients specify its equations and eliminate a free stationary phase-density profile. They do not yet select a unique physical history/exterior or demonstrate an observed rotation curve, joint superiority, microscopic matching or completion.

## Actual protected parents

| File relative to J | SHA256 |
|---|---|
| CONSTRAINED_U_SPHERICAL_ADM_SOURCES_AND_CANONICAL_EVOLUTION_V001.md | cafaff537e994e1c71f24f3786f5f74850de689837012e147c011ad8356b5e1a |
| CONSTRAINED_U_SPHERICAL_FLRW_CURRENT_MODE_AND_HILBERT_SYSTEM_V001.md | 110b2f23ae79c808090f79c60655b7c64c7b38e2edd7773e6aa4965ed4e399b1 |
| CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json | e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f |
