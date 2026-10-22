D034 diagnostic-only select-workers entry

Entry: select_workers_diagnostic_cx1v001.py. Only select-workers is exposed. Supply the unchanged launcher CLI config/pins and optionally --refusal-record /absolute/existing-parent/new-record.json. No path is invented; no launch command is exposed. Exact pinned cw8 v003 remains unchanged. ROOT/FILE/IDENTITY lock refusals retain their original code after diagnostic publication. Other refusals produce no diagnostic. Invalid diagnostic destination refuses before selector execution. OS errors during publication retain the existing CLI OS-error refusal behavior; no choice is published.

Schema and fields follow D034. tool_pin binds this successor entry; its source pins the unchanged underlying launcher. No worker selection or launch authority is conveyed. Diagnostic files use O_EXCL, O_NOFOLLOW and fsync; their parent must already exist, resolve without symlinks, and contain no worker_choices component. The missing launch root is never created.

Validation: test_comparator_form_cx1v001.py RUN_DIR (six exact-code controls, six isolated comparator-guard mutants); test_lock_diagnostic_cx1v003.py RUN_DIR (three actual lock refusal controls, six invalid destinations, one in-memory entry mutant detected by no-choice oracle, full Context CLI serial selection positive control). Each RUN_DIR must be new; use the fixed runtime with -I -B. Inert fixtures and denied-read/process/network audit remain active. No scientific launches.

Review requested separately from backlog4. Root adoption is outstanding. Earlier test v002 is retained with its failed AST anchor; final v003 is selected by the packet.
