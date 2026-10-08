# Independent switch-graph implementation preflight

2026-09-29. Full source/protocol/quotient review; **accepted with no requested
correction**. No module import, enumeration, eigensolver or evolution was run
by this reviewer. This does not replace a saved-output audit.

Reviewed SHA-256:

- `native_switch_graph_v001.py`:
  `f7ae8c25871e760db0e1c9cc48912657e4168bc1ffbf93e71005b4330c82670a`
- `NATIVE_SWITCH_GRAPH_PROTOCOL_V001.md`:
  `2aec6a54f8b0f29a4bd2f74160c1fd770dff67882bb40bf56dee613d3da2e527`
- `NATIVE_SWITCH_GRAPH_QUOTIENT_V001.md`:
  `5b6120546f55951784897c30ca38cff8221422199d032be4ddfcd197dd87a738`

The six row patterns and exact column-degree filter retain the entire90-state
manifold. Rectangle patterns, XOR targets and common-neighbor/four-cycle
checks give the intended simple symmetric switch adjacency. The topology
census18D+72C and neighbor counts D->C16, C->D4, C->C8 imply the normalized
quotient [[0,8],[8,8]] and Tr(A^2)=1152. Configuration-space connectivity is
checked separately from the physical incidence topology.

The exact quotient Perron eigenvalue4+4sqrt(5), coherent-orbit amplitudes and
per-configuration C/D probability ratio agree with the full-space comparison.
Connected weight(1+1/sqrt(5))/2 is correctly compared with counting weight.8:
it is a relative enhancement of disconnected configurations, not a claim of
connectivity selection. The common identity energy is omitted only from the
dimensionless transition calculation.

With H_eff=-g4*A, the full propagator exp(+i*tau*A) has the correct sign.
Its coherent-D transfer formula .8 sin^2(4sqrt(5)*tau) and initial coefficient
64 agree with the quotient. The separately retained incoherent mixture and
individual-D controls instead have initial coefficient16; their equal mean
energy does not imply equal coherence or energy variance. All90 probabilities,
all18 individual-D connection probabilities and all seven prospective times
are retained without physical sign selection. Integer and floating checks,
source pins and stdout publication follow the protocol.

This is a qualified candidate implementation of the leading induced native
operator. It does not execute full2^16 incidence dynamics, adopt changed
microscopic coefficients, supply formation, or establish a physical ruler,
large-N reduction, gravity or cosmology.
