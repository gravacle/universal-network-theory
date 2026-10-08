# C8 record interaction resolvent V001

QUALIFIED_ARITHMETIC. Arithmetic controls 260/260; failed 0.

All six rows, all signed operators and all three record differences per carrier sector are retained in the committed JSON/NPZ. Real full inverses were not taken. The common ARpop shift remains source energy.

| Sector | s | zbar | Sigma diagonal range | Sigma offdiagonal range | Frobenius norm | Analytical operator ceiling |
|---|---:|---:|---|---|---:|---:|
| reference | 0 | 9.5 | [-0.0229228011328,-0.0201007563501] | [-0.00114901982371,-2.07846070753e-11] | 0.0590863193692 | 0.0242424242424 |
| reference | 1 | 9.5 | [-0.017809489914,-0.0160514470854] | [-0.000713523065955,-3.27404409024e-12] | 0.0467612268327 | 0.0186046511628 |
| reference | 2 | 9.5 | [-0.0145631264773,-0.0133630620973] | [-0.00048597812625,-7.31371381905e-13] | 0.0387118279804 | 0.0150943396226 |
| tagged | 0 | 11 | [-0.0321480177604,-0.0202049257885] | [-0.00185022200468,-0] | 0.17863453786 | 0.04 |
| tagged | 1 | 11 | [-0.0229155876653,-0.0161039731831] | [-0.00102278414267,-0] | 0.136493001146 | 0.0266666666667 |
| tagged | 2 | 11 | [-0.0178066365733,-0.0133932155625] | [-0.000649322899374,-0] | 0.110711365384 | 0.02 |

| Sector | Loading increment | Signed diagonal range | Signed offdiagonal range | Frobenius norm | Operator ceiling |
|---|---|---|---|---:|---:|
| reference | 0 to 1 | [+0.00404930926468,+0.00511331121874] | [+1.75105629851e-11,+0.00043549675775] | 0.0123627980125 | 0.00563777307963 |
| reference | 0 to 2 | [+0.00673769425278,+0.00835967465546] | [+2.00532356934e-11,+0.000663041697455] | 0.0204263139126 | 0.00914808461978 |
| reference | 1 to 2 | [+0.0026883849881,+0.00324636343672] | [+2.54267270833e-12,+0.000227544939705] | 0.00806571342344 | 0.00351031154015 |
| tagged | 0 to 1 | [+0.00410095260537,+0.00923243009508] | [+0,+0.000827437862008] | 0.0426171221492 | 0.0133333333333 |
| tagged | 0 to 2 | [+0.00681171022604,+0.0143413811871] | [+0,+0.00120089910531] | 0.0685452728904 | 0.02 |
| tagged | 1 to 2 | [+0.00271075762066,+0.00510895109199] | [+0,+0.000373461243298] | 0.0259627416277 | 0.00666666666667 |

| s | E0 | E1 | E2 | B_s | B_s minus B_0 | dB/du |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 7.98019609728 | 9.27979936278 | 10.3981866726 | -0.181215955726 | +0 | -0.000174519168109 |
| 1 | 7.98410110988 | 9.28384927191 | 10.4023149653 | -0.181282468617 | -6.6512890986e-05 | -9.97694635546e-05 |
| 2 | 7.98672540496 | 9.2865516216 | 10.4050562173 | -0.181321620906 | -0.000105665180044 | -6.08879863137e-05 |

B_0 retains the direct interaction. Loading increments and slopes are not sign selected. B_s is clamped-q equilibrium addition curvature, not a mature prepared-state reaction or gravity. The negative virtual shift becomes less negative with record loading at the fixed subthreshold arguments. Pole normalization is not a physical metric.
