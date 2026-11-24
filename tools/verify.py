# -*- coding: utf-8 -*-
"""Reproducible verification for #2195 deliverables (per proposal Evidence section).

Checks:
  1. Spec text lists >=10 fixed swimlanes in the published top-down order.
  2. Template .drawio XML contains every symbol from the spec, three color
     pairs, 11 lanes in order, and the custom review_queue marked "custom".
  3. Step-table template header has exactly 8 columns with exact names.
  4. Sample diagram: >=8 tasks, >=1 XOR gateway, 1:1 step-to-row mapping,
     executing_role copied verbatim from lane names, rejected branch exits
     to a notice step (not a dead end).

Exit code 0 = all pass; any failure prints FAIL and exits 1.
"""
import re, sys, zipfile, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("  | " + detail) if detail else ""))

# ---------- shared ----------
LANE_ORDER = [
    "会员企业（外部）", "访客/潜在客户（外部）", "前台", "运营", "会员经理",
    "商务拓展（BD）", "BD主管", "财务", "管理层", "会员空间平台（系统）",
    "员工AI助手/管家（AI）",
]
EXPECTED_8 = ["步骤编号 step_no", "步骤名称 step_name", "执行角色 executing_role",
              "输入 input", "输出 output", "托管模块 hosting_module",
              "时限（SLA） time_limit", "异常处理 exception_handling"]

# ---------- 1. spec ----------
spec_all = (ROOT / "spec" / "swimlane-drawing-spec.md").read_text(encoding="utf-8")
sec2 = spec_all.split("## 2.", 1)[1].split("## 3.", 1)[0]  # only the swimlane section
spec = sec2
lane_rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", spec, re.M)
lane_rows = [(int(n), name.strip()) for n, name in lane_rows if 1 <= int(n) <= 11]
lane_names = [name for _, name in sorted(lane_rows)]
check("1a. spec lists >=10 lanes", len(lane_names) >= 10, f"count={len(lane_names)}")
check("1b. lane order matches published list", lane_names == LANE_ORDER,
      "->".join(lane_names[:3]) + "...")

# ---------- 2. template drawio ----------
tpl = ET.parse(ROOT / "template" / "bp-template.drawio").getroot()
all_cells = tpl.iter("mxCell")
styles = [c.get("style", "") or "" for c in all_cells]
values = [ (c.get("value") or "") for c in tpl.iter("mxCell") ]
joined_values = " ".join(values)

symbol_ids = [f"SYM-{i:02d}" for i in range(1, 13)]
missing = [s for s in symbol_ids if s not in joined_values]
check("2a. all 12 symbol IDs present in template", not missing, "missing: " + ",".join(missing) if missing else "SYM-01..SYM-12")

color_pairs = {
    "manual #dae8fc/#6c8ebf": ["fillColor=#dae8fc", "strokeColor=#6c8ebf"],
    "auto #d5e8d4/#82b366": ["fillColor=#d5e8d4", "strokeColor=#82b366"],
    "AI #ffe6cc/#d79b00": ["fillColor=#ffe6cc", "strokeColor=#d79b00"],
}
for label, pair in color_pairs.items():
    ok = all(any(p in s for s in styles) for p in pair)
    check(f"2b. color pair present: {label}", ok)

check("2c. custom review_queue marked 'custom'",
      "review_queue" in joined_values and "custom" in joined_values)

tpl_lanes = [c.get("value") for c in tpl.iter("mxCell")
             if (c.get("style") or "").startswith("swimlane;horizontal=0")
             and c.get("parent") and c.get("parent").startswith("pool")]
tpl_lanes = [v for v in tpl_lanes if v]
check("2d. template pool has 11 lanes in fixed order", tpl_lanes == LANE_ORDER,
      f"count={len(tpl_lanes)}")

# ---------- 3. xlsx template header ----------
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

def _cell_value(c, shared):
    t = c.get("t")
    if t == "inlineStr":
        tnode = c.find(f"{M}is/{M}t")
        return tnode.text if tnode is not None and tnode.text else ""
    v = c.find(f"{M}v")
    raw = v.text if v is not None else ""
    if t == "s" and raw.isdigit():
        return shared[int(raw)]
    return raw

def _load_shared(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    sx = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(f"{M}t")) for si in sx.findall(f"{M}si")]

def xlsx_header(path):
    with zipfile.ZipFile(path) as z:
        shared = _load_shared(z)
        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    row1 = root.find(f".//{M}sheetData/{M}row[@r='1']")
    return [_cell_value(c, shared) for c in row1.findall(f"{M}c")]

hdr = xlsx_header(ROOT / "template" / "step-description-table-template.xlsx")
check("3a. template header has exactly 8 columns", len(hdr) == 8, f"count={len(hdr)}")
check("3b. header names match verbatim", hdr == EXPECTED_8, " | ".join(hdr[:2]) + "...")

# ---------- 4. sample diagram ----------
sample_path = ROOT / "example" / "BP-PKG-01-package-receiving-pickup-v0.1.drawio"
sample = ET.parse(sample_path).getroot()
cells = list(sample.iter("mxCell"))
def style_of(c): return c.get("style") or ""
def val_of(c): return c.get("value") or ""

steps = [c for c in cells if re.search(r"BP-PKG-01S\d{2}", val_of(c)) and "edge" != c.get("edge")]
step_ids = sorted({m for c in cells for m in re.findall(r"BP-PKG-01S\d{2}", val_of(c))})
check("4a. sample has >=8 task steps", len(step_ids) >= 8, f"steps={len(step_ids)}: {','.join(step_ids)}")

xor_gates = [c for c in cells if "rhombus" in style_of(c) and "edge" != c.get("edge") and re.search(r"G\d{2}", val_of(c))]
check("4b. sample has >=1 XOR gateway", len(xor_gates) >= 1, f"count={len(xor_gates)}")

# lane order of sample is a subset of fixed order kept in order
sample_lanes = [c.get("value") for c in cells
                if (style_of(c).startswith("swimlane;horizontal=0")) and c.get("parent", "").startswith("pool")]
sample_lanes = [v for v in sample_lanes if v]
fixed_idx = [LANE_ORDER.index(v) for v in sample_lanes]
check("4c. sample lanes are an in-order subset of fixed list",
      fixed_idx == sorted(fixed_idx), " -> ".join(sample_lanes))

# 1:1 step-to-row mapping against sample xlsx
def xlsx_rows(path, sheet=1):
    with zipfile.ZipFile(path) as z:
        shared = _load_shared(z)
        names = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n))
        xml = ET.fromstring(z.read(names[sheet - 1]))
    rows = []
    for row in xml.findall(f".//{M}sheetData/{M}row"):
        rows.append([_cell_value(c, shared) for c in row.findall(f"{M}c")])
    return rows

srows = xlsx_rows(ROOT / "example" / "BP-PKG-01-step-description-table.xlsx", sheet=1)
data_rows = srows[1:]
table_steps = [r[0] for r in data_rows if r and r[0]]
check("4d. 1:1 step-to-row mapping", sorted(table_steps) == step_ids,
      f"diagram={len(step_ids)} table={len(table_steps)}")

# header of sample table also exactly 8
check("4e. sample table header exactly 8 columns", len(srows[0]) == 8)

# executing_role verbatim from lane names
roles_ok = all(r[2] in LANE_ORDER for r in data_rows if r and r[0])
check("4f. executing_role copied verbatim from lane list", roles_ok)

# rejected branch: G01 -> S08 edge exists (not a dead end)
s08_cells = [c for c in cells if c.get("id") == "s08"]
edges_from_g01 = [c for c in cells if c.get("edge") == "1" and c.get("source") == "g01"]
edge_targets = {c.get("target") for c in edges_from_g01}
check("4g. rejected branch exits G01 to notice step S08 (no dead end)",
      "s08" in edge_targets and len(edge_targets) >= 2)

# object.field form in input/output columns
of_ok = all(("=" in r[3] or "." in r[3]) and ("=" in r[4] or "." in r[4])
            for r in data_rows if r and r[0])
check("4h. input/output written in object.field form", of_ok)

# ---------- summary ----------
fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
