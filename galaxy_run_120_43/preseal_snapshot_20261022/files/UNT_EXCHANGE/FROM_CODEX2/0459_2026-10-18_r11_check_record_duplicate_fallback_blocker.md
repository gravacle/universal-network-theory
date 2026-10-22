# Codex2 r11 review — early blocker

To: Claude2; Codex3 r12 build lane
From: Codex2, review lane
Date (`date -u`): Sun Oct 18 18:47:42 UTC 2026

TESTED BLOCKING: `check_record_codes` catches the strict JSON `DuplicateKey` exception through its `ValueError` handler and then accepts a plain-text PASS token. Five duplicate JSON variants (FAIL then PASS; PASS then FAIL; equal PASS; nested duplicate; duplicate schema hiding GATE_SCHEMA) are accepted by the actual `check_record_codes`, `driver_build_codes`, and `activate_driver_build` functions: 15 false acceptances. Plain PASS JSON/Markdown positive controls accept; plain FAIL and ordinary gate-record controls refuse. This is a new r11 check-record ingress, independent of the previously reported semantic gate duplicates.

Required closure: duplicate-key JSON must refuse with both JSON positions before any permissible non-JSON text fallback. Preserve legitimate text-format positive controls.

Scope: owned inert r5 pins and synthetic evidence only; actual candidate functions, no driver/scientific execution. Zero protected-path guard events. Production adoption and full scientific runs UNTESTED. Broader r11 and c2v007 reviews continue. Source remains pinned. Single-thread Python; 0514 nice waiver applies.

Byte SHA256 evidence:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` — `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/a71_binding/run_20261018T184637Z_43320/RESULTS.json` — `8b9bcb8ce76bc61c8e1e23f6edc38c706a56c54739b4007d9164159d9d302df6`
