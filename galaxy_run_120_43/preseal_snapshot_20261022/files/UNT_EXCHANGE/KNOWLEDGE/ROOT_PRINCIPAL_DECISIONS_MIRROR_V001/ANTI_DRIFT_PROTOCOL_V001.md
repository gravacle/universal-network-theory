# Anti-drift protocol (V001)

Adopted by the principal on 2026-10-12 (all eight points; register entry D7). It binds every agent: Codex root, Codex2, Codex3, Claude, every reviewer or delegated model, and every fresh chat.

**Why it exists.** On 2026-10-12 the 120/43 work drifted into standard-physics framing and lost contact with the program's own results. The causes were:
- no shared foundation;
- tasks framed in standard-physics shapes;
- dispatch driven by volume;
- lineages that did not connect;
- no write-back of results;
- reviews that checked correctness but not framing;
- principal premises scattered across messages.

The rules below address each cause.

1. **One entry point and a grounding receipt.** Before any work, and again after every context reset or fresh chat, an agent reads `KNOWLEDGE/UNT_START_HERE` (current version) and its originals: the program charter, CORE, REGISTER and status ledger. It then completes the comprehension check and files a receipt in `GROUNDING_REGISTER`. No receipt, no science.

2. **Principal-premise register.** `KNOWLEDGE/PRINCIPAL_PREMISES_REGISTER` holds every principal premise and decision, verbatim and dated. Tasks cite the entries they rely on. No agent may override or reinterpret an entry.

3. **Framing gate before dispatch.** Every task states:
   - (a) the question, in the program's own terms (charter, ALLOW/REQUIRE, Γ by function, collective emergence, Records all the way down);
   - (b) its **lineage**: A (Γ, C-77 onward), B (Gravity Formation) or C (dark sector / V005);
   - (c) a **PRIOR-WORK LEDGER**: what it builds on, ports, contradicts or supersedes, with path:line;
   - (d) a **CLASSICAL-IMPORT LEDGER** plan, in which nothing may be load-bearing;
   - (e) what each possible outcome would mean for UNT.

   **Foundational or new-direction tasks require the principal's sign-off before dispatch.** Claude enforces the gate, including on its own assignments, and bounces any task that fails it.

4. **Reviews check framing as well as correctness.** Every review verdict covers grounding (the prior-work ledger), imports (the classical-import ledger) and premise compliance, alongside the mathematics.

5. **Write-back on every acceptance.** An accepted result goes into the program `REGISTER_V001.md` and `ledger/status_ledger.tsv`; root owns those writes. It also gets one line in `KNOWLEDGE/LEARNED_INDEX`. Retired framings get D- or X-style entries.

6. **Idle is acceptable.** Lanes wait rather than invent work. "Keep all lanes working" means working on framed, grounded questions.

7. **Drift checkpoints.** At each new direction, and at least daily while science is active, Claude compares active work against the charter, the premise register and the current plan (now line A, D6). Claude reports any deviation to the principal at once, not afterwards.

8. **Lineage bridge.** `KNOWLEDGE/LINEAGE_BRIDGE` maps lines A, B and C: which results correspond, which conflict, and which are missing a link. Each lane declares its lineage, and any cross-lineage claim reconciles with the bridge.
