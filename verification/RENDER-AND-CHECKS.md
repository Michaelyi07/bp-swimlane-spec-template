# Verification Log 验证记录（真实命令与原始输出）

环境：Windows 11 Pro (win32) · Python 3.13.12 · openpyxl 3.1.5 · draw.io desktop 32.7.4 (CLI, official SHA256-verified build)

## 1. PNG rendering by official draw.io CLI

```
$ draw.io -x -f png -s 2 --crop -o "template/bp-template.png" "template/bp-template.drawio"

template/bp-template.drawio -> template/bp-template.png      (exit code 0)

$ draw.io -x -f png -s 2 --crop -o "example/BP-PKG-01-package-receiving-pickup-v0.1.png" "example/BP-PKG-01-package-receiving-pickup-v0.1.drawio"

example/BP-PKG-01-package-receiving-pickup-v0.1.drawio -> example/BP-PKG-01-package-receiving-pickup-v0.1.png   (exit code 0)
```

Rendered sizes: template PNG 2845x3665, sample PNG 2845x1033 (scale=2).

## 2. Acceptance checks

```
$ python tools/verify.py
```

See `verification/verify-output.txt` for the full raw output (18/18 checks passed, exit code 0).

## 3. Excel generation

```
$ python tools/make_xlsx.py
saved template/step-description-table-template.xlsx
saved example/BP-PKG-01-step-description-table.xlsx
```

## 4. PDF export (scope item 1: drawio + PNG + PDF)

```
$ draw.io -x -f pdf --crop -o "template/bp-template.pdf" "template/bp-template.drawio"
template/bp-template.drawio -> template/bp-template.pdf      (exit code 0)

$ draw.io -x -f pdf --crop -o "example/BP-PKG-01-package-receiving-pickup-v0.1.pdf" "example/BP-PKG-01-package-receiving-pickup-v0.1.drawio"
example/BP-PKG-01-package-receiving-pickup-v0.1.drawio -> example/BP-PKG-01-package-receiving-pickup-v0.1.pdf   (exit code 0)
```

PDF sizes: template 272632 bytes, sample 164137 bytes (vector, cropped to content).

## 5. Revision v1.1 (rework of 2026-11-27: lane 6/7 renamed to 订单原文)

Order #2195 rework request: fixed swimlane list rows 6/7 must use the order's original wording 「招商」「招商主管」(Lane ID: investment_promotion / investment_promotion_supervisor) instead of 「商务拓展（BD）」「BD主管」. Changes: spec §2 rows 6/7, spec version v1.0 → v1.1 (+ change-log row), template pool lanes 06/07, symbol-library page title v1.1, `tools/verify.py` LANE_ORDER. The other 9 lanes and the order are unchanged. The sample diagram and both step tables do not use lanes 6/7 (their executing_role values are unchanged).

Re-runs after the rename:

```
$ draw.io -x -f png -s 2 --crop -o "template/bp-template.png" "template/bp-template.drawio"

template/bp-template.drawio -> template/bp-template.png      (exit code 0)

$ draw.io -x -f pdf --crop -o "template/bp-template.pdf" "template/bp-template.drawio"

template/bp-template.drawio -> template/bp-template.pdf      (exit code 0)

$ python tools/verify.py
18/18 checks passed   (exit code 0)
```

`template/bp-template-opened-screenshot.png` re-captured after the rename: template opened in draw.io desktop 32.7.4 — left shape panel, canvas (symbol library + 11-lane pool with 招商/招商主管 in rows 6/7) and the "BP-SPEC-01 Template" page tab visible.
