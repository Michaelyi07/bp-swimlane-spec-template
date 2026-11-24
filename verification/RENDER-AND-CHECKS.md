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
