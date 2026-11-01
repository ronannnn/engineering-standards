---
产物: tasks
阶段: 04-开发计划
编号: TSK-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-10-31
依据: 03-ui-design.md
修订: 1
不适用: -
---

# 开发计划：可靠门禁和持续生命周期

## 任务清单

### 任务 1：修复解析与检查范围

- 文件：`gates/_lib.py`、`gates/run.py`、`gates/spec.py`；对应阶段技能与样例同步更新。
- 依赖：无
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-5、AC-6、AC-7 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-1、FR-2

### 任务 2：修复实现证据与验收关联

- 文件：`gates/gate05_implement.py`、`gates/gate06_test_report.py`；对应阶段技能与样例同步更新。
- 依赖：任务 1
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-1、AC-2 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-1

### 任务 3：修复交付前置和工程检查

- 文件：`gates/gate07_delivery.py`、`gates/gate06_review_report.py`；对应阶段技能与样例同步更新。
- 依赖：任务 2
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-3、AC-4 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-1

### 任务 4：修复 CI 目录识别

- 文件：`gates/changed_runs.py`、`.github/workflows/standards-gate.yml`；对应阶段技能与样例同步更新。
- 依赖：任务 3
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-8 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-2

### 任务 5：补齐生命周期策略与入口说明

- 文件：`AGENTS.md`、`README.md`、`policies/lifecycle.md`、`policies/project-context.md`、`policies/quality-gates.md`；对应阶段技能与样例同步更新。
- 依赖：任务 4
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-9、AC-10、AC-11、AC-12 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-3、FR-4、FR-5

### 任务 6：同步计划实现及测试评审契约

- 文件：`templates/04-tasks.md`、`templates/05-implementation.md`、`templates/06-test-report.md`、`templates/06-review-report.md`；对应阶段技能与样例同步更新。
- 依赖：任务 5
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-9、AC-10、AC-11 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-3、FR-4

### 任务 7：同步交付维护及角色工作方法

- 文件：`templates/07-delivery.md`、`templates/08-retro.md`、`policies/delivery.md`；对应阶段技能与样例同步更新。
- 依赖：任务 6
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-10、AC-12 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-4、FR-5

### 任务 8：补齐来源迁移与试跑资料

- 文件：`THIRD_PARTY_NOTICES.md`、`CHANGELOG.md`、`policies/workflow-evaluation.md`；对应阶段技能与样例同步更新。
- 依赖：任务 7
- 验收方法：`python3 -m unittest discover gates/tests` 全绿，并按 AC-13、AC-14 检查内容；纯文档用逐项阅读和链接检查验证。
- 对应需求：FR-6

## 里程碑与顺序

先完成任务 1–4 的 RED/GREEN 回归，再完成任务 5–8 文档、样例和迁移同步。用户已明确要求本次连续完成，不重复请求阶段确认；最终交付记录保留待签收，不伪造人工最终验收。关联技能与样例变更作为同一契约同步，不独立引入无关功能。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| AC-1 对应需求判据 | 任务 2 | 单元 | AC-1 |
| AC-2 对应需求判据 | 任务 2 | 单元 | AC-2 |
| AC-3 对应需求判据 | 任务 3 | 单元 | AC-3 |
| AC-4 对应需求判据 | 任务 3 | 单元 | AC-4 |
| AC-5 对应需求判据 | 任务 1 | 单元 | AC-5 |
| AC-6 对应需求判据 | 任务 1 | 单元 | AC-6 |
| AC-7 对应需求判据 | 任务 1 | 单元 | AC-7 |
| AC-8 对应需求判据 | 任务 4 | 单元 | AC-8 |
| AC-9 对应需求判据 | 任务 5 | 手工 | AC-9 |
| AC-10 对应需求判据 | 任务 5 | 手工 | AC-10 |
| AC-11 对应需求判据 | 任务 5 | 手工 | AC-11 |
| AC-12 对应需求判据 | 任务 5 | 手工 | AC-12 |
| AC-13 对应需求判据 | 任务 8 | 手工 | AC-13 |
| AC-14 对应需求判据 | 任务 8 | 手工 | AC-14 |

## 风险与回退

证据检查和依赖闭包收紧可能使旧样例失败；同步迁移和样例。修改前先记录反例失败，纯文档使用检查清单，不伪造测试先行历史。回退以本次变更差异逐文件恢复，不碰用户已有工作。
