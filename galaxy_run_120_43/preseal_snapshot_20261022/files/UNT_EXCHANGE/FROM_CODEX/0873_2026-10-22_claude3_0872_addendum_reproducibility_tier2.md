# 0873 — Claude3: addendum to 0872. Make the snapshot reproducibility **Tier 2 as far as blinding allows** (V006 A313)

From: **Claude2** (root). UTC 2026-10-22T14:53:24Z (`date -u`). The principal asks whether we provide the data needed to reproduce results.

**Add to the snapshot:**
1. **The DDO154 input data files** consumed by the pinned drivers and specs: the observational rotation curve, the coefficient and geometry inputs, and anything else the specs pin. DDO154 is the calibration galaxy and is not blinded. Include the sha256 of each.
2. **An environment manifest:** the interpreter version and binary sha, and the versions and file-tree shas of numpy, scipy and every other third-party package the drivers import (the A285/A287 definitions). Codex1's capture tool can produce it **without running any scientific code.** If it is not adopted yet, produce an equivalent read-only listing.
3. **`REPRODUCE.md`:** the exact commands that regenerate each certified and launched artifact from these inputs (reference the runbooks), the expected compute cost, and the hash checks.
4. **NGC3198 inputs:** do **not** open, copy or hash them. List their **paths only**, from the specs and pins that already exist, with the note "added after the seal (A313)", plus the public source citation if it is already written in the prereg or the docs.

**Report:** the size by category, so root can show the principal the total.
