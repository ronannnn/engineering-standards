---
产物: tasks
阶段: 04-开发计划
编号: TSK-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 03-ui-design.md
修订: 2
不适用: -
---

# 开发计划：按功能细分需求并方便审阅

## 任务清单

### 任务 1：明确细分方法与需求填写

- 文件：`policies/requirements-organization.md`、`templates/01-requirements.md`、`skills/org-requirements/SKILL.md`、`skills/org-role-pm/SKILL.md`
- 依赖：无
- 验收方法：人工核对AC-1；模板与链接契约通过。
- 对应需求：FR-1

### 任务 2：同步入口与原模块约定

- 文件：`README.md`、`AGENTS.md`、`CHANGELOG.md`、`policies/modular-artifacts.md`、`THIRD_PARTY_NOTICES.md`
- 依赖：任务 1
- 验收方法：`python3 -m unittest discover gates/tests`；两份样例--all通过。
- 对应需求：FR-1

### 任务 3：编写可校验的短需求树示例

- 文件：`examples/requirements-tree/01-requirements.md`、`examples/requirements-tree/modules.json`、`examples/requirements-tree/modules/skills/search/01-requirements.md`、`examples/requirements-tree/modules/skills/favorites/01-requirements.md`
- 依赖：任务 2
- 验收方法：`python3 gates/run.py examples/requirements-tree --stage 01`，根与两份叶子草稿通过内容自检；不宣称已冻结。
- 对应需求：FR-1

### 任务 4：登记示例入口和回归

- 文件：`examples/requirements-tree/README.md`、`gates/tests/test_document_contracts.py`
- 依赖：任务 3
- 验收方法：全量测试验证实际示例、完整旧样例和链接，无业务文件改动。
- 对应需求：FR-1

## 里程碑与顺序

先明确拆分粒度、根与叶子职责和审阅顺序，再同步模板技能及导航，最后测试和自审。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 细分与用户阅读 | 任务 1、任务 2、任务 3 | 手工 | AC-1 |
| 旧契约与需求示例 | 任务 2、任务 4 | 单元 | AC-2 |

## 风险与回退

只调整标准、虚构示例及对应回归，避免触碰其他业务工作区；新增写作项不宣称有机器验证，旧资料按明确迁移流程处理。
