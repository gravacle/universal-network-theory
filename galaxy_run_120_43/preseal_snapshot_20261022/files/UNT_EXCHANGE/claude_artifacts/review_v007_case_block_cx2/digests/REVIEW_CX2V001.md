# V007 case-block tail configuration digests — TESTED PASS

`date -u`: Sun Oct 18 20:42:56 UTC 2026. Controls ran Sun Oct 18 20:42:38 UTC 2026.

All10 declared `uv_tail_config_sha256` values match the exact r12-pinned normalizer and an independent SHA256 calculation of the canonical normalized dictionary without its sha256 field. 83/83 checks pass; all5 input/source byte pins are unchanged at completion.

| Cases | Recomputed SHA256 |
|---|---|
| C2T, C3T, C4T, C6T, S4T | `6d5606ed30fa4654284e3650e00f7312c7fcb58c380bd24e33e1e974b63e572d` |
| C4T-D5 | `0e7414ea427ff413963e72b5e98af4f59d921f97a0a59cc8a6bb8b882e98251d` |
| C4T-C5c | `65b8062c355d46c9fd974c900dd31e0d420804f8548226939f4362bdcdfa9934` |
| C4T-KLO | `5ed423eaf1830bda9d4277f21b93e5f71ff19fdd2f3b03ef9ddfaf9d74f98c3e` |
| C4T-KHI | `7af84faa3c34656438e5aa1aab06bc9514885981c830aef39bafb21fbab0947c` |
| C4T-A | `c957cadf4f66e36830c40c3574a1cfdee6104d4f25189786c5318aaaf48e1c72` |

The library identity is verified from r12's actual `PIN_UVT_LIB` tuple: `tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py`, SHA256 `c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22`. Its bytes match that pin. Only Refusal, _canon, _sha, _pos_float, _strict, normalize_config and the two literal configuration constants were selected by AST. No whole module, scientific evaluator, driver, project pipeline or compare executed.

Per-case controls show: no file reads during normalization; unchanged input; canonical identity invariant under reversed dictionary insertion order; one representable domain-value change alters the hash; changing a literal certificate hash alters the hash. Unknown top-level keys and boolean/nonfinite lambda values refuse. Certificate paths were never followed.

Evidence hashes from bytes:
- CASE_BLOCK_V007_C4V001.json: `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`.
- Builder metadata CASE_BLOCK_BUILD_C4V001.json (read only): `bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad`.
- Selected r12 compare source: `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`.
- RESULTS_CX2V001.json: `8613840bc3c6393aefc43f1abc30fa1866e0514914e7c2302a4e001a08318f87`.
- probe_digests_cx2v001.py: `466ab4f16993878afc0962b8f133bc3c8cf9f2741b1812a319889acfabe13a1d`.
- INPUT_PINS_CX2V001.json (full paths): `e8819e4f056bd5866b0bdd8caf32cc57f04e7e3a6899d1df7c1186056cb83c48`.

Scope limits: this slice does not establish case-block structure, spec/dry-report joins, certificate byte validity or admission; other lanes own those checks. A config digest binds the literal certificate path/hash, not proof of its contents. No actual run path or NGC target was opened, and no scientific launch occurred. Guards were installed before selected code execution and recorded zero denied access attempts.
