# q4 diagonal initial-data compatibility V001

EXACT_DIAGONAL_INITIAL_DATA_AND_SYMBOLIC_COMPATIBILITY_REPORTED

All 51,840 representative incoming bases retained; integer diagonal checks only. Full rows are in three sealed checkpoint bundles. No physical background, pressure, state or unknown energy is selected.

| Background | Bases | Native energy range | Exact native sum | Census centroid |
|---|---:|---|---|---|
| 0 | 17280 | [[193, 1], [271, 1]] | [3992000, 1] | [12475, 54] |
| 1 | 17280 | [[575, 4], [218, 1]] | [3110080, 1] | [9719, 54] |
| 2 | 17280 | [[3, 2], [39, 4]] | [78080, 1] | [122, 27] |

Full energy retains AR Q + 54 Sself and unresolved donor/precursor/support/additional-field/other inventories. Census centroids are bookkeeping, not an adopted mixed or thermal state.

- E0(b;m,g): Eunit*(E4/4+AR*Q+54*Sself)+E_donor(b;m,g)+E_precursor(b;m,g)+E_support(b;m,g)+E_additional_field(b;m,g)+E_other(b;m,g)
- rho0: E0/(27*nu)
- k_req: 8*pi*G_total*E0/(81*nu*c_p^4)+Lambda/3
- P_req: -E0/(81*nu)-p_b0+c_p^4*Lambda/(12*pi*G_total)-c_p^2*m*epsilon_phys^2/(162*pi*G_total*hbar^2)
- a_acceleration0: 2*m*epsilon_phys^2/(81*hbar^2)
- DAE_denominator: 324*pi*G_total/c_p^2
- fixed_proper_conditional_source: p_b0=0 only if complete admitted bare inventory is held independent of a
- epsilon_units: epsilon_phys=Eunit*epsilon_native
- flat_Lambda0_old_only_condition: FULL E0=0, not native intercept alone

Exact check count: 52220. Raw SHA256: 55a779630bac6903d0006067d6e316c876458fde771bb02c78f32363abc2da95. Both m=1 and m=2 unit-donor conditions are reported; physical q4 placement/ruler/covariant stress remains open.
