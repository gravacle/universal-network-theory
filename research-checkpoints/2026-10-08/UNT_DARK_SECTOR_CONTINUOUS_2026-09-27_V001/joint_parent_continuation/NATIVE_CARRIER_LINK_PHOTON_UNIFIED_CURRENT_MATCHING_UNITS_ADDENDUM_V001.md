# Native carrier/link/photon current matching: units addendum V001

This narrow addendum corrects the units wording in Section4 of the preserved matching V001. No action, current, normalization, parameter or physical state is changed. All equations there are interpreted in the frozen producer units below; its symbol k_phys in those normalized weak rows means the producer q, not an unscaled inverse length.

Set c_p=1 for the physical-to-code formulas. The fixed unit is Hstar; tau=Hstar*t_proper, q=k_phys/Hstar, Q=X/Hstar, sigma=sigma_phys/Hstar, u_b=Hstar*v_b and V=Hstar*V_phi,phys. Overdots in those weak rows are tau derivatives. The density unit is rho_star=2 M_bare^2 Hstar^2 and w=W_phys/rho_star, where W_phys=rho_phi+P. Cbar=C/2. These follow the hierarchy's Sec1 and the reduced-chart normalization, and bg's literal w=1.5*OA*qbar*d/rG.

Thus the normalized full-current locking condition remains u_b−V=Cbar Q sigma/(w q). Its unscaled physical form is v_b−V_phi,phys=M_bare^2 C X sigma_phys/(W_phys k_phys). The physical current remains J_phi=n_phi v_phi−M_bare^2 C sigma_vector with the actual multiplier projection; a normalized w is not substituted for physical enthalpy in this covariant current.

The Section4 phrase w=rho_phi+P therefore means w=(rho_phi+P)/rho_star. Likewise Q/w=1/n_phi holds only after the consistent normalized charge dictionary: physically W_phys=X n_phi, so Q/w=2 M_bare^2 Hstar/n_phi. This fixed global factor does not change the logarithmic derivative d ln[Q/(w q)]/d tau=4h used in the locking tangent. That tangent and the nonlocking conclusion are unchanged.

No producer, background, helper, state or numerical function was evaluated. The four exact inputs were byte-verified before and after exclusive creation; all preserved sources remain unchanged.

| Input relative to J | SHA256 |
|---|---|
| NATIVE_CARRIER_LINK_PHOTON_UNIFIED_CURRENT_MATCHING_V001.md | 7b215502059b680391554346d6adc8d4c74138819ddaf6f4bc69755f9d406ecf |
| constrained_u_clock_gradient_early_transfer_v005.py | bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20 |
| CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md | 1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2 |
| CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md | 5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b |
