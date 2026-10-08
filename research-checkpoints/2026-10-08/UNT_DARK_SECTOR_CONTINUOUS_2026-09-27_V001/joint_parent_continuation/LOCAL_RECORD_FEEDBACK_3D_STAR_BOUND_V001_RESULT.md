# Current 3D parent: exact overlapping-star envelopes V001

Controls: 101/101; failed 0.
Status: EXACT_ARITHMETIC_PASS.
Bounds: VOLUME_UNIFORM_Q1_SECTOR_ENVELOPES_CERTIFIED.

| local comparison a | exact ground lower | exact ground upper | width | precision |
|---|---:|---:|---:|---|
| 0/1 | -212839666383313/1593629889921956 | -221908836047304943167546066164908843/1661534994731144827481114925195531225 | 630138010617234752019800702386191517/2647871830754872073864000688400776521366355211076100 | TARGET_WIDTH_EARNED |
| 1/2 | -16589973420664287/81538513921255630 | -18781050733285466445406933199682507/92307499707285820771629957312474610 | 2147758876864245647180982229161749433/376330817495941244413181685527384925021591684727715 | TARGET_WIDTH_EARNED |

| matching/control or volume-uniform bound | exact lower | exact upper |
|---|---:|---:|
| blank_BOND_matching_trial_density | -465635680151790856673511/24178516392292583494123520 | -46563568015179085667351/2417851639229258349412352 |
| occupied_BOND_matching_trial_density_control | -32096001382780485697583/4835703278458516698824704 | -80240003456951214243957/12089258196146291747061760 |
| full_q1_sector_ground_energy_density_envelope_raw | -212839666383313/1593629889921956 | -46563568015179085667351/2417851639229258349412352 |
| b_interval_raw | 18781050733285466445406933199682507/92307499707285820771629957312474610 | 16589973420664287/81538513921255630 |
| D_expectation_per_vertex_upper_raw | 0 | 18157685145546979727022803661238753568447/49287007386206406762150180258303117885440 |
| delta_squared_expectation_per_vertex_upper_raw | 0 | 18157685145546979727022803661238753568447/24643503693103203381075090129151558942720 |
| nonice_probability_average_upper_raw | 0 | 18157685145546979727022803661238753568447/24643503693103203381075090129151558942720 |

All records remain occupiedq1; blank/occupied labels distinguish matching BOND bits. Full degrees0..4, feedback and common identity are retained. The blank-bond primary trial was chosen prospectively and the occupied-bond alternative remains an explicit control.
The local stars overlap and need not commute. Summed operator inequalities are valid without a compatible product of star ground states; no such global state is asserted.
Raw defect bounds remain untrimmed. Independent exact ranges are D0..5, delta-squared0..4 and nonice probability0..1. A loose bound remains loose; no parameter selection/refinement is authorized.
These are energy/defect envelopes for the supplied periodic diamond and declaredNc0q1 sector. They establish neither actual preparation/global record selection nor a Coulomb phase, GNS state, transverse dynamic weight, matter pole, rank-three transport, physical metric/clock/ruler, gravity/volume law, observed superiority or Stage3 completion.
Each positive trial came from oneNEW16-state NumPy calculation. Exact integer CW/Rayleigh certificates and rational sqrt bounds earn the result; no old producer/action/eigensolve/inertia/evolution is replayed.

Elapsed seconds: 0.008292375016026199; native peak RSS: 34537472.
