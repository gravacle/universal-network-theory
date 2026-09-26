# Prospective L8 lineage-order Ollivier--Ricci protocol V001

Date frozen: 2026-09-25

Status: `FROZEN_FOR_REVIEW__NO_CURVATURE_OR_ASSOCIATION_OUTPUT_OPENED`

## 1. Question and ceiling

Using only the already completed owner-once `L=8` state, ask whether terminal
spent-record concentration is positively associated with Ollivier--Ricci
curvature of the **formation-order lineage graph** defined below.

A pass is only a finite association on a schedule-derived graph.  It does not
show that records caused the graph or its curvature, that this graph is an
emergent spatial metric, that its curvature is spacetime Ricci curvature, or
that gravity has been derived.  A failure or null is retained unchanged.

## 2. Frozen input and cheap reconstruction

The sole physical input is the authenticated `L=8` sharp terminal precursor:

`DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json`

with its eight immutable `prefix_07/q_00.npy` through `q_07.npy` shards.  The
history JSON gives each shard's path, shape, byte count, and SHA-256.  The
analysis must authenticate those records before loading an array.  The
independently produced L4--L8 joint-witness result is read only to verify the
nine terminal sector weights; it does not define the graph or the record
observable.

Each retained shard row is a prefix-seven spent-lineage mask `S` and its
columns are carrier configurations.  At the last admission (`e=7`,
`phi=pi/4`), for row probability split `b_S` on carrier configurations blank
at target 7 and `o_S` occupied there, reconstruct

`P_8(S) = o_S + cos(phi)^2 b_S`,

`P_8(S union {7}) = sin(phi)^2 b_S`.

The following transport is block diagonal in `S`, so it preserves these row
norms.  No evolution, diagonalization, fitting, thresholding, support pruning,
or checkpoint machinery is needed.

## 3. Graph fixed independently of record concentration

Vertices are the frozen event labels `V={0,...,7}`.  The owner-once schedule
is the total order `0<1<...<7`; its unique transitive reduction, with direction
forgotten only for the metric calculation, is the undirected path

`E={{0,1},{1,2},...,{6,7}}`.

Every edge has length and adjacency weight exactly `1`.  No edge, length,
weight, orientation, threshold, or vertex inclusion is obtained from
`P_8(S)`, from a record one- or two-point function, from carrier occupation,
or from the eventual correlation.  This prevents the proposed response from
being used twice to manufacture both curvature and its source.  The cost is
explicit: this is a chronology-native diagnostic graph, not a claim that the
parent dynamics has selected spatial geometry.  The periodic carrier edge
`{7,0}` is excluded because it is not an edge of the transitive reduction of
the first-pass formation order; adding it would answer a different carrier-
geometry question.

## 4. Ollivier--Ricci convention

Use the unit shortest-path distance `d` on the undirected path and idleness
`alpha=1/2`.  For every vertex `x`,

`m_x = alpha delta_x + (1-alpha)/deg(x) sum_{z~x} delta_z`.

For each graph edge `{x,y}`,

`kappa_xy = 1 - W_1(m_x,m_y)/d(x,y)`,

where `W_1` uses the same path metric.  Compute it by the exact path cut
formula, not an approximate optimal-transport solver.  The frozen vertex
summary is the unweighted mean of incident edge curvatures,

`K_x = (1/deg(x)) sum_{y~x} kappa_xy`.

No alternate idleness, directed curvature, weighted distance, scalar
aggregation, or best-looking convention may replace this one after execution.

## 5. Record-concentration observable and prediction

The primary terminal record concentration is

`R_x = sum_S P_8(S) 1[x in S]`.

This is the spent-lineage probability at event label `x`; carrier occupation
is not substituted.  The directional prediction is **positive**: larger
`K_x` is predicted to align with larger `R_x`.

The fixed statistic is Spearman's rank correlation `rho_S(K,R)` with average
ranks for ties.  Pearson correlation, a selected subset, sector selection,
absolute value, sign flip, or post-hoc normalization may not rescue it.

## 6. Exact scrambled null and disposition

Enumerate all `8! = 40320` permutations of the eight `R` labels while leaving
the graph and `K` fixed.  Let

`p_plus = #{pi: rho_S(K,R_pi) >= rho_observed}/40320`,

`p_minus = #{pi: rho_S(K,R_pi) <= rho_observed}/40320`.

Comparisons use a fixed floating guard `1e-12`.  Report exactly one:

- `POSITIVE_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8` iff
  `rho_observed >= 0.5` and `p_plus <= 0.05`;
- `OPPOSITE_SIGN_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8` iff
  `rho_observed <= -0.5` and `p_minus <= 0.05`;
- `NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8` otherwise;
- `LINEAGE_ORDER_CURVATURE_TEST_UNRESOLVED_L8` only for custody,
  normalization, nonfinite, zero-variance, or implementation-control failure.

The output must include all edge curvatures, `K_x`, `R_x`, the observed
statistic, both exact tail counts/probabilities, reconstruction residuals, and
input/source hashes.  No outcome may be called evidence for gravity.

## 7. Numerical, custody, and runtime gates

Before evaluation require:

- exact SHA-256, shape, byte count, and read-only mode for all eight shards;
- reconstructed total probability within `1e-12` of one;
- reconstructed terminal sector weights within `1e-10` of both the history
  result and the frozen joint-witness result;
- finite `P_8`, `K`, `R`, and correlations, with no probability below
  `-1e-15`;
- exactly 8 vertices, 7 edges, and 40320 null permutations; and
- authentication of `PROTOCOL.md`, `FREEZE.json`, and the implementation by
  `SOURCE_HASHES.sha256` before any physical input is opened.

Preflight class: `SHORT_READ_ONLY_POSTPROCESS__NO_EVOLUTION__NO_CHECKPOINT`.
The input payload is under 4 MiB and the null has only 40320 permutations.
Budget: at most 5 minutes wall time and 512 MiB RSS.  Exceeding either returns
`LINEAGE_ORDER_CURVATURE_TEST_UNRESOLVED_L8`; it does not trigger a restart or
resume framework.

Execution is prohibited until an independent review accepts this freeze and
the explicit `--authorize-frozen-analysis` guard is supplied.
