# Practice: Verification Subagent + Observability

In this practice you will extend the E2E Test Orchestrator with a **verification subagent** that checks key-term coverage in the generated tests, and add **telemetry configuration** so you can observe the agent's tool usage in an OTEL provider.

---

## Repository layout

```
agent-observability-verification-practice/
├── .claude/
│   └── agents/
│       ├── e2e_test_generator.md            ← already complete
│       └── term_verifier.md.template        ← copy → term_verifier.md and fill in
├── app/
│   └── index.html                           ← Observability Dashboard (app under test)
├── data/
│   └── tickets/
│       └── 3.json                           ← golden ticket
├── memory/
│   └── test_cases.md.template               ← copy → test_cases.md and fill in
├── observability/                           ← create otel.env.example here (Task 1)
├── evidence/                                ← add observability.png here (Task 1)
├── skills/
│   ├── get_ticket/get_ticket.py
│   └── post_comment/post_comment.py
├── tests/
│   └── e2e/                                 ← generated spec goes here
├── CLAUDE.md                                ← orchestrator (already complete)
├── playwright.config.ts
└── package.json
```

---

## Step 0 — Setup

```bash
npm install
npx playwright install chromium
```

Verify the skills work:

```bash
python3 skills/get_ticket/get_ticket.py "#3"
python3 skills/post_comment/post_comment.py "#3" "hello"
```

---

## Task 1 — Add telemetry config

Create `observability/otel.env.example` with the environment variables needed to enable Claude Code telemetry. Use **placeholders only** — no real API keys.

Minimum config (from [Claude Code monitoring docs](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage)):

| Variable | Value |
|---|---|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `1` |
| `OTEL_METRICS_EXPORTER` | `otlp` |
| `OTEL_LOGS_EXPORTER` | `otlp` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `<your-otel-endpoint>` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `<your-auth-headers>` |

Add a comment at the top explaining that this file is an example and that real values go in `otel.env.local` (which must not be committed).

---

## Task 2 — Create the term_verifier subagent

Copy the template and fill in every `[TODO]`:

```bash
cp .claude/agents/term_verifier.md.template \
   .claude/agents/term_verifier.md
```

Fill in:

| Section | What to write |
|---|---|
| **Your role** | One-sentence identity |
| **Purpose** | What the subagent reads and what report it produces |
| **What to do** | Key-term extraction logic, case-insensitive matching, ≥ 5 terms |
| **Output format** | Markdown table of terms with ✓/✗ status and missing-terms list |
| **Guardrails** | Read-only, no test modification, always report all terms |

---

## Step 3 — Create the memory file

```bash
cp memory/test_cases.md.template memory/test_cases.md
```

Fill in the `[TODO]` rule: the agent must never generate a test whose ID already appears in the table.

---

## Step 4 — Run the agent

Start Claude Code:

```bash
claude
```

Send the ticket ID:

```
#3
```

Confirm the agent:
- fetches ticket #3
- invokes `e2e_test_generator` and writes `tests/e2e/generated.spec.ts` with ≥ 5 tests
- invokes `term_verifier` and shows the coverage report
- updates `memory/test_cases.md`
- **waits** — does not call `post_comment`

---

## Step 5 — Run the tests

```bash
npx playwright test
```

All tests must pass.

---

## Step 6 — Capture evidence

1. Copy `observability/otel.env.example` → `otel.env.local` and fill in real values.
2. Load the env and start Claude Code:
   ```bash
   env $(cat observability/otel.env.local | xargs) claude
   ```
3. Run the agent again on ticket `#3`.
4. Save a screenshot as `evidence/observability.png` showing either a LangSmith trace (tool calls + timings) or terminal telemetry output.
5. Create `observability/NOTES.md` and answer (briefly):
   - What tool was called first?
   - What step took the longest?
   - One thing you'd optimize based on the trace (cost, latency, or tool usage)

---

## Submission checklist

- [ ] `.claude/agents/term_verifier.md` exists with all `[TODO]` sections filled in
- [ ] `observability/otel.env.example` exists (placeholders only, no secrets)
- [ ] `memory/test_cases.md` exists with a "no duplicate test cases" rule
- [ ] `tests/e2e/generated.spec.ts` exists with ≥ 5 test cases
- [ ] `npx playwright test` exits green
- [ ] `evidence/observability.png` exists (trace evidence)
- [ ] `observability/NOTES.md` exists (3 short observations)
- [ ] No API keys committed
- [ ] Changes committed and pushed to `main`
