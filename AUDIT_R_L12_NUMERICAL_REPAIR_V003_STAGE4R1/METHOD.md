# V003R1 Stage-4 schema-projection repair

This repair is limited to the Stage-4 Hostile schema projection. The completed
V003R1 Target and Hostile histories, terminal shards, numerical predicates,
tolerances, and physical definitions are immutable inputs.

The frozen V003 adapter copied the Hostile `dimension` field and also aliased it
to `full_dimension`. The frozen Stage-4 predecessor requires the projected
Hostile object to omit `dimension` and `manifest_adapter` so that its final
normalization can add those two fields without overwriting an existing field.

Stage4R1 therefore:

1. Executes every frozen V003 provenance, solver, resource, comparison, and
   terminal-shard check unchanged.
2. Requires the projected `dimension` to be an integer exactly equal to
   `full_dimension`.
3. Requires `manifest_adapter` to be absent.
4. Removes only the redundant pre-normalization `dimension` key.
5. Delegates final normalization and exact adjudication to the unchanged frozen
   Stage-4 predecessor.

No numerical solver is executed. No observable, threshold, tolerance, history,
or terminal shard is modified. The original failed V003 continuation and all
of its frozen sources remain unchanged.
