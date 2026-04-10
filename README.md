In this task, you'll extend the E2E Test Orchestrator with a verification subagent and telemetry configuration.
You'll add a subagent that checks key-term coverage in generated tests and set up telemetry so you can observe the agent's tool usage in an OTEL provider.

👩‍💻 Workflow at a glance
1. Set up your environment
2. Add telemetry config
3. Create the `term_verifier` subagent
4. Create the memory file
5. Run the agent
6. Run the tests
7. Capture observability evidence
8. Submit your task

Let's go!

## 1. Set up your environment

Once you log in to your GitHub account, the repository for this task will be added automatically.

1. Confirm that `agent-observability-verification-practice` appears in your GitHub account.
2. Clone the repo and open it in your editor.
3. Install dependencies:
    
    ```
    npm install
    npx playwright install chromium
    ```
    
4. Verify that the skills work:
    
    ```
    python3 skills/get_ticket/get_ticket.py "#3"
    python3 skills/post_comment/post_comment.py "#3" "hello"
    ```
    

### Repository layout

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
├── evidence/                                ← add observability.png here
├── skills/
│   ├── get_ticket/get_ticket.py
│   └── post_comment/post_comment.py
├── agent_tests/
│   └── e2e/                                 ← generated spec goes here
├── CLAUDE.md                                ← orchestrator (already complete)
├── playwright.config.ts
└── package.json
```

## 2. Add telemetry config

Create `observability/otel.env.example` with the environment variables needed to enable Claude Code telemetry.

Use placeholders only — no real API keys.

### Minimum config

| **Variable** | **Value** |
| --- | --- |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `1` |
| `OTEL_METRICS_EXPORTER` | `otlp` |
| `OTEL_LOGS_EXPORTER` | `otlp` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `<your-otel-endpoint>` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `<your-auth-headers>` |

Add a comment at the top explaining that this file is an example and that real values should go in `otel.env.local` (which must not be committed).

## 3. Create the `term_verifier` subagent

Copy the template and fill in every `[TODO]`:

```
cp .claude/agents/term_verifier.md.template \
   .claude/agents/term_verifier.md
```

### Requirements

| **Section** | **What to write** |
| --- | --- |
| Your role | One-sentence identity |
| Purpose | What the subagent reads and what report it produces |
| What to do | Key-term extraction logic, case-insensitive matching, ≥ 5 terms |
| Output format | Markdown table of terms with ✓/✗ status and a list of missing terms |
| Guardrails | Read-only, no test modification, always report all terms |

## 4. Create the memory file

Copy the template:

```
cp memory/test_cases.md.template memory/test_cases.md
```

Fill in the `[TODO]` rule: the agent must never generate a test whose ID already exists in the table.

## 5. Run the agent

Start Claude Code:

```
claude
```

Send the ticket ID:

```
Run the agent and get ticket #3
```

Confirm that the agent:

- Fetches ticket `#3`
- Invokes `e2e_test_generator` and writes `agent_tests/e2e/generated.spec.ts` with ≥ 5 tests
- Invokes `term_verifier` and shows the coverage report
- Updates `memory/test_cases.md`
- Waits without calling `post_comment`

## 6. Run the tests

Run:

```
npx playwright test
```

All tests must pass.

## 7. Capture evidence

Copy `observability/otel.env.example` → `otel.env.local` and fill in real values.

Load the env and start Claude Code:

```
env $(cat observability/otel.env.local | xargs) claude
```

Run the agent again on ticket `#3`.

Save a screenshot as `evidence/observability.png` showing either a LangSmith trace (tool calls and timings) or terminal telemetry output.

Create `observability/NOTES.md` and answer briefly:

- What tool was called first?
- What step took the longest?
- One thing you'd optimize based on the trace (cost, latency, or tool usage)

## 8. Submit your task

Before submitting, review the checklist.

### ✅ Submission checklist

- [ ]  `.claude/agents/term_verifier.md` exists with all `[TODO]` sections are filled in
- [ ]  `observability/otel.env.example` exists (placeholders only, no secrets)
- [ ]  `memory/test_cases.md` exists with a "no duplicate test cases" rule
- [ ]  `agent_tests/e2e/generated.spec.ts` exists with ≥ 5 test cases
- [ ]  `npx playwright test` exits green
- [ ]  `evidence/observability.png` exists (trace evidence)
- [ ]  `observability/NOTES.md` exists (3 short observations)
- [ ]  No API keys are committed
- [ ]  Changes are committed and pushed to `main`

1. Commit your changes.
2. Push to GitHub.
3. Return to the lesson and click "Submit."
