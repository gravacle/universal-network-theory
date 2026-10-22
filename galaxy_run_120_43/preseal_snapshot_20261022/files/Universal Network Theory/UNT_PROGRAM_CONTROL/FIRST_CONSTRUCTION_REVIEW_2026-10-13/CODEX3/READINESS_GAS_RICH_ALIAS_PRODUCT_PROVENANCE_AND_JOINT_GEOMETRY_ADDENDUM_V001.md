# Gas-rich candidate aliases, product provenance and joint geometry — V001

2026-10-14. Codex3 local helper recovered_packet_audit. Bounded source-contract preparation, proposed for root review. Companion to READINESS_GAS_RICH_CALIBRATION_ROSTER_AND_FORWARD_READ_CONTRACT_PROPOSED_V001.md (ae2733b1942066af814d3d52eec71afe694dd07088cd1d75016c2d303533d4d3). No arrays retrieved, fit, numerical producer or empirical role adoption.

## Alias and role check

The official CDS [SIMBAD DDO154 identifier record](https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=DDO+154) resolves to NGC4789A, with UGC8024 and LEDA43869. The [NGC3741 record](https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=NGC+3741) lists UGC6572 and LEDA35878. Use those exact alias groups with optional whitespace/leading zeros; do not confuse NGC4789A with NGC4789. DDO125 is not established as an alias of NGC3741 and is not included. These are official catalogue identity metadata, not new primary measurements of distance or mass.

Searched the current UNT_PROGRAM_CONTROL Markdown records for these main names/aliases, plus JSON filenames containing ADOPTION, REGISTRY, MANIFEST, ROLE, CALIBRATION or VALIDATION. The only Markdown candidate-name match was the proposed roster itself; the selected JSON search had no match. Therefore no conflicting adopted calibration/validation assignment for these aliases was found in that bounded control-record search. This is not an exhaustive claim about every scientific archive or future selection. No separate finalized observational roster was found. The source plan explicitly reserves NGC3198's historical43 velocities for the declared development comparison and retains future lensing/cosmology roles without naming datasets. Do not invent a pre-existing lensing/cosmology object registry; future role assignment must preserve non-reuse and shared-systematic custody. Both candidates remain PROPOSED, not adopted calibration systems.

## DDO154: concrete available products and missing interfaces

The [NRAO DDO154 page](https://science.nrao.edu/science/surveys/littlethings/data/d154.html) links its HI observations directly to the [official directory](https://things.cv.nrao.edu/littlethings/ddo154/HI/), also exposed through bulk.cv.nrao.edu. The directory lists:

- DDO154_NA_X0_P_R.FITS and DDO154_R_X0_P_R.FITS;
- DDO154_NA_ICL001.FITS and DDO154_R_ICL001.FITS;
- DDO154_NA_XMOM1.FITS / DDO154_R_XMOM1.FITS;
- DDO154_NA_XMOM2.FITS / DDO154_R_XMOM2.FITS.

The [survey product description](https://science.nrao.edu/science/surveys/littlethings/data) identifies NA as natural weighting, R as robust0.5, ICL001 as the HI cube, X0_P_R as beam-corrected integrated flux, XMOM1 as intensity-weighted velocity, and XMOM2 as dispersion. It describes Hanning smoothing. Only directory and documentation text were read, not FITS headers or pixels. Therefore the exact DDO154 beam, mask, units and cube-specific processing still need confirmation; generic new-survey processing must not silently override this inherited object's provenance.

For angular gas-source extraction the integrated-flux product is concrete and public; a radial profile and its mask/geometry covariance are not provided by the directory listing. Conversion still needs beam/unit, helium/opacity and missing-flux custody. Natural/robust products are correlated reductions of the same observations, not independent measurements. The cubes and moment1/2 products are prospective calibration-read and pressure/kinematic ingredients, not source-only measurements to be opened during roster selection. A dispersion map is neither a full velocity likelihood nor an automatic pressure-support correction.

The same object page links U, B, V images and calibration parameters (Hunter/Elmegreen), and links LVL IRAC products. [IRSA LVL overview](https://irsa.ipac.caltech.edu/data/SPITZER/LVL/overview.html), dataset DOI10.26131/IRSA414, documents IRAC3.6/4.5/5.8/8-micron images and DR5 delivery documentation. These supply a concrete stellar-light route; no object image or ready angular stellar-profile array was retrieved. Stellar mass requires an explicit population/dust conversion, not a velocity-fitted mass-to-light ratio. The DDO page explicitly says no JHK images there; do not assume availability from the survey's generic list.

Distance: the earlier inspected Watts2018 Table1 cites Jacobs2009, whose CMD/TRGB catalogue is an independent stellar-distance method. The exact object record and posterior/error budget remain to be admitted. SIMBAD currently displays a kinematic distance entry, which is NOT the independently established TRGB likelihood and is not substituted for it. Geometry: Walter/de Blok tilted-ring products and their reduction are the identified lineage; the full angular geometry/read covariance has not been located as a ready product. The inspected directory contains eight cube/moment files, no separately named covariance matrix. Absence from that directory is not proof no covariance exists elsewhere. FITS availability alone does not settle correlated noise, beam coupling, flux calibration, inclination/PA or pressure errors.

## NGC3741 reserve: exact provenance ceiling

The already inspected Begum2005 GMRT source and FIGGS survey description identify the HI imaging lineage. The primary FIGGS catalogue metadata identifies a resolved-stellar/RGB distance route, while the bar paper cites an adopted distance. The official SIMBAD page displays a Tully-Fisher-labelled distance entry; it cannot be promoted to an independent TRGB observation. Distance-method reconciliation remains necessary before using a value. This audit did not locate a verified public object-level GMRT cube/moment directory, ready source-only angular HI/stellar profile with errors, or joint read/geometry covariance. These remain unavailable-to-this-contract, not asserted nonexistent. No author was contacted and no substitute halo/mass-model table was imported. Reserve status is retained precisely to avoid starting an expensive new reduction before DDO154's contract is usable.

## Joint geometry clarification and smallest next read

Kinematically inferred inclination or PA is NOT automatically unusable for calibration. Source-only selection means selecting systems by ordinary-source provenance/coverage without judging response success; it does not require every nuisance to be measured independently of allocated calibration velocities. A joint observation model can infer geometry with the velocity read, provided source deprojection and read projection share that geometry, retain covariance/degeneracies, and do not reuse a fitted feature as independent validation. One must not freeze a kinematic inclination as an independent prior and count the same velocities again. External photometric/distance information can assist without making such double counting valid.

For a declared inclination i, even the simple circular read v_los−v_sys=v_c sin(i) cos(phi) shows why geometry and response cannot be separated by assertion; real pressure, noncircular and beam terms still belong in the forward read. This illustrative equation does not adopt a circular state or supply its missing constraints.

The next bounded data-admission question is therefore whether a DDO154 source profile plus an owned existing read reduction/joint uncertainty model can be assembled from these identified products without a new full-cube campaign. It is not whether all geometry is independent of velocities. No download or ingestion is authorized by this addendum. Root can separately approve the exact products and split when the contract is concrete. State/exterior and relevant coupled-validity obligations remain those already stated; no full-mode reconstruction or laboratory-only requirement is added.

## Exposure

Metadata retrieval incidentally displayed systemic velocities, catalog distances, and search snippets containing kinematic/halo-fit descriptions (including a harmonic plot summary). None was adopted, used to select the roster, or fitted. No raw target velocity array was retrieved. No NGC3198 target values were sought. Catalogue alias verification does not make either system a blind validation sample.
