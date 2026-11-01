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

# 开发计划：默认直接实现当前需求

## 任务清单

### 任务 1：替换默认兼容规则

- 文件：`policies/compatibility-migration.md`、`AGENTS.md`、`README.md`、`policies/project-context.md`、`CHANGELOG.md`
- 依赖：无
- 验收方法：文档走查AC-1及`python3 -m unittest discover gates/tests`与样例通过。
- 对应需求：FR-1

### 任务 2：同步模板和诊断

- 文件：`templates/02-design.md`、`templates/05-implementation.md`、`templates/06-review-report.md`、`gates/gate02_design.py`
- 依赖：任务 1
- 验收方法：文档走查AC-1及`python3 -m unittest discover gates/tests`与样例通过。
- 对应需求：FR-1

### 任务 3：同步阶段执行要求

- 文件：`skills/org-design/SKILL.md`、`skills/org-implement/SKILL.md`、`skills/org-test-review/SKILL.md`
- 依赖：任务 2
- 验收方法：文档走查AC-1及`python3 -m unittest discover gates/tests`与样例通过。
- 对应需求：FR-1

### 任务 4：同步角色评审要求

- 文件：`skills/org-role-architect/SKILL.md`、`skills/org-role-dev/SKILL.md`、`skills/org-role-reviewer/SKILL.md`、`policies/security.md`
- 依赖：任务 3
- 验收方法：文档走查AC-1及`python3 -m unittest discover gates/tests`与样例通过。
- 对应需求：FR-1

## 里程碑与顺序

先替换冲突策略，再同步模板、阶段和角色，最后验证并记录自审。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 默认和例外依据 | 任务 1、任务 2、任务 3、任务 4 | 手工 | AC-1 |
| 模板与直接契约 | 任务 2 | 单元 | AC-2 |

## 风险与回退

只修改本次标准约定；保留前一任务未提交变更，不修改任何真实业务系统或冻结历史文档。
