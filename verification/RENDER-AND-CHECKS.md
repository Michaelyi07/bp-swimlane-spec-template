# Verification Log 验证记录（真实命令与原始输出）

环境：Windows 11 Pro (win32) · Python 3.13.12 · openpyxl 3.1.5 · draw.io desktop 32.7.4 (CLI, official SHA256-verified build)

## 1. PNG rendering by official draw.io CLI

```
$ "D:/tmp/drawio-cli/app/draw.io.exe" -x -f png -s 2 --crop -o "template/bp-template.png" "template/bp-template.drawio"

template/bp-template.drawio -> template/bp-template.png      (exit code 0)

$ "D:/tmp/drawio-cli/app/draw.io.exe" -x -f png -s 2 --crop -o "example/BP-PKG-01-package-receiving-pickup-v0.1.png" "example/BP-PKG-01-package-receiving-pickup-v0.1.drawio"

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
