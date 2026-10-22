# README_PINNED_INPUT_ENVELOPE_C2V002: errata E1 (root, 2026-10-20T19:29:46Z from date -u). The README is not edited

1. **F1, shell.** The README's command blocks rely on word splitting of variables such as `$C1_SCOPED`, which zsh (this host's shell) does not do. **Run every README command block with `/bin/bash`**, or write the arguments out, or use zsh's `${=VAR}`. Root runs them under `/bin/bash`.
2. **F2, the S0 row.** Replace the shortened `<5e688882…>` with the full sha256 `5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042`. The independent verifier hashed it from bytes, and it matches V006 L1245.
3. **Operating rules that follow from D4:**
   - **Root never chmods a pinned input.** A chmod, or an added hard link, now reads INVALIDATE.
   - **No pinned input is opened in a GUI app during a phase.** An xattr value rewrite reads INVALIDATE.
