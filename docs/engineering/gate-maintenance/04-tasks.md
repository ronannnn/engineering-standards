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

# 开发计划：初始化与增量校验优化

## 任务清单

### 任务 1：修复初始化命名与索引

- 文件：`scripts/init-docs.sh`、`gates/tests/test_scaffold.py`、`README.md`、`CHANGELOG.md`
- 依赖：无
- 验收方法：`python3 -m unittest discover gates/tests -p test_scaffold.py`，反例先失败后通过。
- 对应需求：FR-1

### 任务 2：增量读取与验证下一阶段

- 文件：`gates/run.py`、`gates/tests/test_regressions.py`、`gates/tests/test_document_contracts.py`
- 依赖：任务 1
- 验收方法：`python3 -m unittest discover gates/tests` 全绿及样例 --all 通过。
- 对应需求：FR-2

## 里程碑与顺序

先建立命名、索引和读取次数回归，再实现，最后同步迁移说明、复核契约并提交。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 命名与CI | 任务 1 | 单元 | AC-1 |
| 索引短名称 | 任务 1 | 单元 | AC-2 |
| 单次读取检查 | 任务 2 | 单元 | AC-3 |
| 旧行为 | 任务 2 | 集成 | AC-4 |

## 风险与回退

不改文件冻结和签收判据，若阶段结果变化回退增量校验；只提交本次明确范围，不推送。
