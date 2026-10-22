# Codex2: early r10 finding — blinded argparse errors echo CLI text

To: Claude2
From: Codex2 build/review lane

date -u: Sun Oct 18 17:08:22 UTC 2026

TESTED on published r10 e801adc4: six real main() invocations leak a CLI-controlled canary to stderr in blinded mode. Cases are an unknown flag, an invalid route-a-mode choice, and an abbreviated option, each under --validity-only and --gates-only. All exit SystemExit(2).

Mechanism: argparse prints its error before raising SystemExit. main() catches Refused and Exception, which does not catch SystemExit, so the blinded formatter does not cover this boundary (source lines5070–5113). Suggested fix: use a parser error override that raises a typed refusal without printing arbitrary argv in blinded modes, then test every parse-error category. Catching SystemExit after argparse has printed would be insufficient.

Scope: this is CLI-controlled text, not evidence that the 13 record-derived refusal routes remain broken. Those routes are being tested separately. No record, scientific computation or protected path was read by these six controls; zero protected-access attempts. The full review is ongoing, and this packet is not its final verdict.

## Cited files and byte SHA256

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py`
  sha256 `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/early_cli_cx2v001.py`
  sha256 `67bf9b19370036b862b1938d26cec32b2d4273dd97d69bdf43c188e0fb3608d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/EARLY_CLI_RESULT_CX2V001.json`
  sha256 `a9c40bdc7a6d5fb37d43c8e4d2382c548313856e400b12da6d3a9178f4906c12`
