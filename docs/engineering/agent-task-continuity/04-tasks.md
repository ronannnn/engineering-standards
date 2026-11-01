---
产物: tasks
阶段: 04-开发计划
编号: TSK-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 03-ui-design.md
修订: 1
不适用: -
---

# 开发计划：任务持续执行补充

## 任务清单

### 任务 1：补充共享工作规则

- 文件：`policies/lifecycle.md`、`policies/project-context.md`、`policies/workflow-evaluation.md`
- 依赖：无
- 验收方法：文档走查 AC-1；`python3 -m unittest discover gates/tests` 及两份样例 `--all` 通过。
- 对应需求：FR-1

### 任务 2：同步记录模板

- 文件：`templates/04-tasks.md`、`templates/05-implementation.md`、`templates/06-review-report.md`
- 依赖：任务 1
- 验收方法：文档走查 AC-1；`python3 -m unittest discover gates/tests` 及两份样例 `--all` 通过。
- 对应需求：FR-1

### 任务 3：同步阶段技能

- 文件：`skills/org-requirements/SKILL.md`、`skills/org-plan/SKILL.md`、`skills/org-implement/SKILL.md`、`skills/org-test-review/SKILL.md`
- 依赖：任务 2
- 验收方法：文档走查 AC-1；`python3 -m unittest discover gates/tests` 及两份样例 `--all` 通过。
- 对应需求：FR-1

### 任务 4：更新入口与来源

- 文件：`AGENTS.md`、`README.md`、`THIRD_PARTY_NOTICES.md`、`CHANGELOG.md`
- 依赖：任务 3
- 验收方法：文档走查 AC-1；`python3 -m unittest discover gates/tests` 及两份样例 `--all` 通过。
- 对应需求：FR-1



## 里程碑与顺序

先核对原有文档缺口，再依次更新规则、模板、技能与入口，完成验证和自审后准备交付。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 持续协作规则走查 | 任务 1、任务 2、任务 3、任务 4 | 手工 | AC-1 |
| 旧契约兼容 | 任务 4 | 单元 | AC-2 |

## 风险与回退

只撤回本次新增段落，不覆盖已有未提交修改；最终交付保留待签收，实际运行平台行为尚未试跑。
