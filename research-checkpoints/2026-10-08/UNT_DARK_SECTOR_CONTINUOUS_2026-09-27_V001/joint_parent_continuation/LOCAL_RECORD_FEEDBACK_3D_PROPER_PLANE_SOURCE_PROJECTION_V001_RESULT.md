# Proper-plane source projection V001

All seven supplied modes, both beta4 discretizations, full finite-M contact and correlated128-block errors retained. Qhat retains per-cell channel normalization; Qtilde uses per-node channel normalization. Nonzero wavelength=4ell; no continuum/long-wave qualification or gravitational field solve.

|M|k|R_phys|correlated SE|
|---|---|---:|---:|
|64|[0, 0, 0]|-0.0796159504534|0.00425545336203|
|64|[1, 0, 0]|-0.0700011705502|0.00254117484439|
|64|[-1, 0, 0]|-0.0700011705502|0.00254117484439|
|64|[0, 1, 0]|-0.0778527493545|0.00270560328522|
|64|[0, -1, 0]|-0.0778527493545|0.00270560328522|
|64|[0, 0, 1]|-0.0790205621853|0.00277039834843|
|64|[0, 0, -1]|-0.0790205621853|0.00277039834843|
|128|[0, 0, 0]|-0.0826167203946|0.00466803201376|
|128|[1, 0, 0]|-0.077160476738|0.00270394369329|
|128|[-1, 0, 0]|-0.077160476738|0.00270394369329|
|128|[0, 1, 0]|-0.0790492546006|0.00287966300563|
|128|[0, -1, 0]|-0.0790492546006|0.00287966300563|
|128|[0, 0, 1]|-0.0718743744382|0.00249527528975|
|128|[0, 0, -1]|-0.0718743744382|0.00249527528975|

All signs and full mixed-source outputs are in JSON. The two M values represent one environment. Calibrated total G reference matching, physical body loading and mixed/spatial action remain required for the two-potential common-field calculation.
