# -*- coding: utf-8 -*-
"""Generate the step description table template (8 columns) and the BP-PKG-01
sample step table for #2195 deliverable. Fictional data only."""
import sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEADERS = [
    "步骤编号 step_no",
    "步骤名称 step_name",
    "执行角色 executing_role",
    "输入 input",
    "输出 output",
    "托管模块 hosting_module",
    "时限（SLA） time_limit",
    "异常处理 exception_handling",
]

thin = Side(style="thin", color="999999")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
head_font = Font(bold=True, size=10)
head_fill = PatternFill("solid", fgColor="DDEBF7")
note_font = Font(italic=True, size=9, color="808080")

def style_sheet(ws):
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = head_font
        cell.fill = head_fill
        cell.border = border
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = 26
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"

# --- 1. template workbook: header only (exactly 8 columns) + usage note row ---
wb = Workbook()
ws = wb.active
ws.title = "Step Description Table"
style_sheet(ws)
note = ws.cell(row=2, column=1,
    value="使用说明：第 2 行起逐行填写；列数恒为 8，禁止增删列；executing_role 必须逐字拷贝规范 §2 泳道名；input/output 用 object.field 形式。本行为说明，填写时删除。")
note.font = note_font
wb.save("template/step-description-table-template.xlsx")
print("saved template/step-description-table-template.xlsx")

# --- 2. sample step table for BP-PKG-01 ---
wb2 = Workbook()
ws2 = wb2.active
ws2.title = "Step Description Table"
style_sheet(ws2)

ROWS = [
    ["BP-PKG-01S01", "提交领取请求", "访客/潜在客户（外部）",
     "pickup_request.form_data", "pickup_request.status=submitted",
     "miniprogram-portal", "即时",
     "表单校验失败：小程序内联提示，未提交"],
    ["BP-PKG-01S02", "校验请求并生成领取凭证", "会员空间平台（系统）",
     "pickup_request.status=submitted", "pickup_pass.code=generated",
     "member-data-crm", "≤1分钟（自动）",
     "校验失败：pickup_request.status=rejected，回执推送访客"],
    ["BP-PKG-01S03", "核对访客身份", "前台",
     "pickup_pass.code + visitor.id_document", "identity.check=passed",
     "member-data-crm", "5分钟",
     "证件无效：转 BP-PKG-01S08 驳回并通知"],
    ["BP-PKG-01S04", "确认套餐权益与数量", "会员经理",
     "package_entitlement.quota [Client to confirm]", "package.allocation=confirmed",
     "member-data-crm", "1个工作日 [Client to confirm]",
     "权益不足：线下沟通调整配额后重新确认"],
    ["BP-PKG-01S05", "出库扫码并登记", "前台",
     "package.allocation=confirmed", "package.checked_out=logged",
     "member-data-crm", "10分钟",
     "扫码失败：手工登记并备注，事后补录"],
    ["BP-PKG-01S06", "签收确认", "访客/潜在客户（外部）",
     "package.checked_out=logged", "pickup.signature_captured",
     "miniprogram-portal", "即时",
     "访客拒签：转 BP-PKG-01S08 驳回并通知"],
    ["BP-PKG-01S07", "归档领取记录并回写CRM", "会员空间平台（系统）",
     "pickup.signature_captured", "pickup_record.archived=true",
     "member-data-crm", "≤5分钟（自动）",
     "回写失败：进入 review_queue 重试（≤3次），仍失败告警运营"],
    ["BP-PKG-01S08", "驳回并生成通知", "前台",
     "identity.check=failed", "notice.sent=true",
     "miniprogram-portal", "10分钟",
     "通知发送失败：电话通知访客并人工备注"],
]
for r, row in enumerate(ROWS, 2):
    for c, v in enumerate(row, 1):
        cell = ws2.cell(row=r, column=c, value=v)
        cell.border = border
        cell.alignment = Alignment(vertical="center", wrap_text=True, horizontal="left")
        cell.font = Font(size=10)
    ws2.row_dimensions[r].height = 42

ws3 = wb2.create_sheet("Annotations 标注清单")
ann_headers = ["标注编号", "类型", "挂在步骤", "内容说明"]
ann_rows = [
    ["红圈①", "痛点 Pain point", "BP-PKG-01S03", "人工核对证件效率低、易漏查黑名单，可由平台人脸/证件 OCR 承接"],
    ["绿圈①", "系统化机会 Opportunity", "BP-PKG-01S07", "归档回写 CRM 已系统化，可进一步自动生成会员权益使用报告"],
    ["黄问号①", "待客户确认 [Client to confirm]", "BP-PKG-01S04", "套餐权益配额阈值与确认时限（1个工作日）待客户拍板"],
]
for c, h in enumerate(ann_headers, 1):
    cell = ws3.cell(row=1, column=c, value=h)
    cell.font = head_font; cell.fill = head_fill; cell.border = border
for r, row in enumerate(ann_rows, 2):
    for c, v in enumerate(row, 1):
        ws3.cell(row=r, column=c, value=v).border = border
for c, w in zip(range(1, 5), [12, 22, 18, 70]):
    ws3.column_dimensions[get_column_letter(c)].width = w

ws4 = wb2.create_sheet("Change Log 变更日志")
cl_headers = ["版本", "日期", "修订人", "修订内容", "评审状态"]
cl_rows = [["v0.1", "2026-11-24", "daoye-data-agent", "初稿（含完整 8 步说明表）", "Draft"]]
for c, h in enumerate(cl_headers, 1):
    cell = ws4.cell(row=1, column=c, value=h)
    cell.font = head_font; cell.fill = head_fill; cell.border = border
for r, row in enumerate(cl_rows, 2):
    for c, v in enumerate(row, 1):
        ws4.cell(row=r, column=c, value=v).border = border
for c, w in zip(range(1, 6), [10, 14, 18, 40, 12]):
    ws4.column_dimensions[get_column_letter(c)].width = w

wb2.save("example/BP-PKG-01-step-description-table.xlsx")
print("saved example/BP-PKG-01-step-description-table.xlsx")
