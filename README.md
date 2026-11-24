# BP-SPEC-01 Swimlane Drawing Specification & draw.io Template

Deliverable for ticket S1-BP-001 (Member Space Platform · Business Blueprint & Process Diagrams).
All content is **fictional** — no real enterprise or personal data, no client name, no secrets.

## Contents 交付清单

| File | Purpose |
|---|---|
| `spec/swimlane-drawing-spec.md` | Drawing specification: 11 fixed swimlanes & order, BPMN-compatible symbol subset, numbering, 8-column step table, annotation rules, version rules, file naming |
| `template/bp-template.drawio` | draw.io template: full symbol library (SYM-01…SYM-12 incl. custom `review_queue`), three-color legend, annotation legend, 11-lane pool |
| `template/bp-template.png` | Rendered view of the template (exported by official draw.io CLI) |
| `template/step-description-table-template.xlsx` | Step description table template — exactly 8 columns |
| `example/BP-PKG-01-package-receiving-pickup-v0.1.drawio` | Sample swimlane diagram: fictional "Package Receiving and Pickup" flow, 8 steps + 1 XOR gateway |
| `example/BP-PKG-01-package-receiving-pickup-v0.1.png` | Rendered PNG of the sample |
| `example/BP-PKG-01-step-description-table.xlsx` | Complete step table for the sample (8 rows, 1:1 with diagram) + annotations list + change log |
| `tools/make_xlsx.py` | Regenerates both .xlsx files |
| `tools/verify.py` | Reproducible acceptance checks (see below) |
| `template/bp-template-opened-screenshot.png` | Screenshot of the template opened in draw.io desktop |

## How to view

- Open `.drawio` files with draw.io (https://github.com/jgraph/drawio-desktop or app.diagrams.net).
- Open `.xlsx` with Excel / WPS / LibreOffice.

## How to verify

```bash
python tools/verify.py
```

Real command and raw output recorded in the delivery text and in `verification/verify-output.txt`.

Environment used: Windows 11 Pro, Python 3.13.12, draw.io desktop 32.7.4 (CLI export).

## Acceptance criteria mapping

1. *Specification lists no fewer than 10 fixed swim lanes and their arrangement order* → spec §2 lists 11 lanes with top-down order; `verify.py` check 1a/1b asserts count ≥ 10 and exact order.
2. *draw.io template contains all symbols with three-color annotations, accompanied by a screenshot of the opened file* → template Symbol Library page holds SYM-01…SYM-12 + legend; checks 2a–2d assert symbols, three color pairs (#dae8fc/#6c8ebf, #d5e8d4/#82b366, #ffe6cc/#d79b00), `review_queue (custom)`, 11 lanes in order; screenshot included.
3. *Step description table template contains exactly 8 columns* → checks 3a/3b assert exact count and verbatim header names (步骤编号 step_no … 异常处理 exception_handling).
4. *Sample swim lane diagram drawn per spec, ≥8 steps and 1 exclusive gateway, complete step table* → BP-PKG-01 has steps S01–S08 + XOR gateway G01 (verified / not verified), rejected branch exits to notice step S08 (no dead end); checks 4a–4h assert step count, XOR, 1:1 step-to-row mapping, verbatim executing_role, object.field form.
