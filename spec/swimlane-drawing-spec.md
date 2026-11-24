# 会员空间平台 · 业务流程泳道图绘制规范（BP Drawing Specification）

**Spec ID:** BP-SPEC-01 · **Version:** v1.0 · **Status:** Approved（评审通过记录见 §7 变更日志）
**适用范围:** Stage i Blueprint & Naming · Business Blueprint & Process Diagrams 模块下全部流程图
**All fictional content. No real enterprise or personal data. No client name appears in this deliverable.**

---

## 1. 目的与原则（Purpose & Principles）

本规范统一本模块全部泳道流程图的**工具、符号、泳道、编号、表格、标注、版本与命名**，使后续约 18 张流程图可比较、可合并、可评审。

原则：一张图只讲一个流程；每张图只画涉及的泳道，但**泳道相对顺序永远不变**；每个步骤在步骤说明表中有且仅有一行。

## 2. 固定泳道清单与顺序（Fixed Swimlane List & Order）

全平台统一 11 条泳道，**自上而下**顺序如下，任何流程图不得改变相对顺序、不得临时追加新泳道（新泳道必须修订本规范插入固定列表）：

| 顺序 | 泳道名（图中显示） | Lane ID（文件/脚本用） | 类型 |
|---|---|---|---|
| 1 | 会员企业（外部） | member_enterprise | external |
| 2 | 访客/潜在客户（外部） | visitor_prospect | external |
| 3 | 前台 | front_desk | human |
| 4 | 运营 | operations | human |
| 5 | 会员经理 | member_manager | human |
| 6 | 商务拓展（BD） | BD | human |
| 7 | BD主管 | BD_supervisor | human |
| 8 | 财务 | finance | human |
| 9 | 管理层 | management | human |
| 10 | 会员空间平台（系统） | platform | system(auto) |
| 11 | 员工AI助手/管家（AI） | employee_AI_assistant | AI |

规则：
- R2-1 每张图从上表选取本流程涉及的泳道，**保持上表相对顺序**，省略未涉及者。
- R2-2 步骤说明表的 `executing_role` 必须**逐字拷贝**自本表"泳道名"列。
- R2-3 系统与 AI 泳道中的步骤不得写成人工动作；人工泳道中不得出现系统自动行为。

## 3. 符号子集（Symbol Subset, BPMN 2.0 Compatible）

全部流程图只允许使用以下符号（draw.io 模板 `bp-template.drawio` 的 Symbol Library 页包含全部符号的可拖拽原件）：

| 符号 | 图形 | Spec ID | 说明 |
|---|---|---|---|
| 开始事件 Start event | 细边圆（绿色系） | SYM-01 | 流程唯一入口 |
| 结束事件 End event | 粗边圆（红色系） | SYM-02 | 每个分支必须有终止 |
| 人工任务 Manual task | 圆角矩形，蓝底 | SYM-03 | 人执行的步骤 |
| 系统任务 System task | 圆角矩形，绿底 | SYM-04 | 平台自动执行的步骤 |
| 排他网关 Exclusive gateway (XOR) | 菱形 + ✕ | SYM-05 | 互斥分支，有且必须有默认/驳回出路 |
| 并行网关 Parallel gateway (AND) | 菱形 + ＋ | SYM-06 | 并行分支，必须同图汇合 |
| 定时器事件 Timer event | 细边圆 + 时钟 | SYM-07 | SLA 超时、定时提醒 |
| 消息事件 Message event | 细边圆 + 信封 | SYM-08 | 外部消息触发的步骤 |
| 数据对象 Data object | 文档折角形 | SYM-09 | 表单/记录；命名 `object.field` |
| 子流程引用 Subprocess reference | 矩形 + 两端竖线 | SYM-10 | 引用 `BP-XXX-NN` |
| 托管模块标签 Hosting-module label | 任务框右下角灰色小字 | SYM-11 | 标注该步骤由哪个模块托管（§3.1） |
| 复核队列 Review queue（**custom**，非 BPMN 标准） | 虚线边矩形 | SYM-12 | 待复核条目堆积点；图例中必须标注 "custom" |

### 3.1 托管模块标签（Hosting-module label）

每个任务/子流程步骤必须标注托管模块。模块清单（来自平台组成，命名待客户确认，未确认处标 `[Client to confirm]`）：

| 模块 ID | 模块名 |
|---|---|
| member-data-crm | 会员数据中台与 CRM `[Client to confirm]` |
| kb-sop-workbench | 知识库与 SOP 工作台 |
| opportunity-routing | 资源撮合与商机路由 `[Client to confirm]` |
| bd-workbench | BD 销售员工作台 |
| miniprogram-portal | 微信小程序会员门户 |
| website | 官网 |
| exec-dashboard | 高管仪表盘 `[Client to confirm]` |
| ai-tools | AI 辅助工具套件 `[Client to confirm]` |

人工泳道中的步骤也必须标注其依托的托管模块（如前台登记依托 member-data-crm）；纯线下步骤标 `offline`。

## 4. 编号规则（Numbering Rules）

- **流程号** `BP-<DomainAbbreviation>-NN`，如 `BP-MEM-01`（会员入会）、`BP-PKG-01`（套餐领取）。域缩写表：MEM=会员、PKG=套餐/礼包、BD=商机、FIN=财务、OPS=运营、GEN=通用。新增域缩写须修订本规范。
- **步骤号** = 流程号 + `S` + 两位序号，如 `BP-PKG-01S01`；网关用 `G`（`BP-PKG-01G01`）。
- 图中每个任务/事件/网关框内第一行显示步骤号 + 步骤名。

## 5. 步骤说明表（Step Description Table）

每张流程图附一张步骤说明表，**恰好 8 列**，列名逐字如下（模板 `step-description-table-template.xlsx`）：

| # | 列名 | 填写规则 |
|---|---|---|
| 1 | 步骤编号 step_no | 与图内步骤号一致（BP-PKG-01S01） |
| 2 | 步骤名称 step_name | 动宾短语，与图内一致 |
| 3 | 执行角色 executing_role | 逐字拷贝 §2 泳道名 |
| 4 | 输入 input | `object.field` 形式，如 `pickup_request.status=submitted` |
| 5 | 输出 output | `object.field` 形式，如 `pickup.signature_captured` |
| 6 | 托管模块 hosting_module | §3.1 模块 ID 或 `offline` |
| 7 | 时限（SLA） time_limit | 具体时长或 `即时`；阈值未确认标 `[Client to confirm]` |
| 8 | 异常处理 exception_handling | 指向异常步骤号或写明处理动作 |

禁止添加第 9 列（如"备注"）；确需补充信息写入图内标注或变更日志。

## 6. 标注规则（Annotation Rules）

| 标注 | 图形 | 含义 |
|---|---|---|
| 痛点 | 红色圆圈 + 编号 ①②… | 现状低效/易错环节 |
| 系统化机会 | 绿色圆圈 + 编号 ①②… | 可被平台承接的系统化改进点 |
| 待客户确认 | 黄色问号 ？ | 需客户拍板的名称/阈值/规则 |

标注编号全图唯一，与 README/交付说明中的标注清单对应。

## 7. 版本规则（Version Rules）

- 草稿版本从 **v0.1** 开始，每次修订递增 0.1（v0.2, v0.3 …）。
- 通过评审后版本记为 **v1.0**；此后每次重大修订递增整数（v1.1, v2.0 …）。
- 每个流程图文件与步骤说明表须附**变更日志表**（模板如下）：

| 版本 | 日期 | 修订人 | 修订内容 | 评审状态 |
|---|---|---|---|---|
| v0.1 | 2026-11-24 | daoye-data-agent | 初稿 | Draft |
| v1.0 | 2026-11-24 | daoye-data-agent | 评审通过，发布基线 | Approved |

## 8. 文件命名与目录结构（File Naming & Directory Structure）

```
bp-flows/
├── BP-SPEC-01-swimlane-drawing-spec.md      # 本规范
├── template/
│   ├── bp-template.drawio                   # 模板：泳道池（11 泳道）+ 符号库 + 图例
│   ├── bp-template.png                      # 模板渲染图（打开文件证据）
│   └── step-description-table-template.xlsx # 步骤说明表模板（8 列）
└── BP-PKG-01-package-receiving-pickup/      # 每个流程一个目录
    ├── BP-PKG-01-package-receiving-pickup-v0.1.drawio
    ├── BP-PKG-01-package-receiving-pickup-v0.1.png
    ├── BP-PKG-01-step-description-table.xlsx
    └── BP-PKG-01-change-log.md              # 变更日志表
```

命名规则：`<流程号>-<kebab-case流程名>-v<版本>.<ext>`；中间稿只保留最新一版，评审通过的版本归档。

## 9. 工具与交付格式（Tools & Delivery Format）

- 制图工具统一使用 **draw.io**（diagrams.net）；交付三种格式：`.drawio` 源文件 + `.png` 渲染图 + `.pdf`（提交归档时导出）。
- PNG 导出使用 draw.io 官方 CLI：`draw.io -x -f png -s 2 --crop -o out.png in.drawio`。
- 禁止使用其他制图工具交付流程图。

## 10. 自检清单（Reviewer Checklist）

```
[ ] 泳道子集顺序与 §2 固定顺序一致
[ ] 符号全部来自 §3，无自造符号
[ ] 每个任务框含步骤号+步骤名+托管模块标签
[ ] XOR 网关每条分支有明确去向（含驳回分支，不得死端）
[ ] 步骤说明表恰好 8 列，executing_role 与泳道名逐字一致
[ ] input/output 为 object.field 形式
[ ] 标注编号全图唯一且语义正确
[ ] 版本号与变更日志表一致
```
