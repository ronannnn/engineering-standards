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

# 计划：模块化全流程资料

## 任务清单

### 任务 1：先建立模块化反例与样例夹具

- 文件：`gates/tests/test_modular.py`；同一契约对应模板、技能和样例同步。
- 依赖：无
- 验收方法：`python3 -m unittest discover gates/tests`，旧和新增测试全绿；样例 `--all` 与 `--delivery`。
- 对应需求：FR-1、FR-2、FR-3

### 任务 2：实现模块清单、引用与阶段树校验

- 文件：`gates/modular.py`、`gates/run.py`、`gates/spec.py`、`gates/gate04_plan.py`、`gates/gate06_test_report.py`；同一契约对应模板、技能和样例同步。
- 依赖：任务 1
- 验收方法：`python3 -m unittest discover gates/tests`，旧和新增测试全绿；样例 `--all` 与 `--delivery`。
- 对应需求：FR-1、FR-2、FR-3

### 任务 3：实现模块初始化与索引

- 文件：`scripts/init-module.py`、`scripts/init-docs.sh`；同一契约对应模板、技能和样例同步。
- 依赖：任务 2
- 验收方法：`python3 -m unittest discover gates/tests`，旧和新增测试全绿；样例 `--all` 与 `--delivery`。
- 对应需求：FR-1

### 任务 4：同步模板技能、说明与运行证据

- 文件：`policies/modular-artifacts.md`、`README.md`、`AGENTS.md`、`CHANGELOG.md`、`THIRD_PARTY_NOTICES.md`；同一契约对应模板、技能和样例同步。
- 依赖：任务 3
- 验收方法：`python3 -m unittest discover gates/tests`，旧和新增测试全绿；样例 `--all` 与 `--delivery`。
- 对应需求：FR-4

## 里程碑与顺序

先测试与 RED，再实现与 GREEN，再逐项核对模板和技能，最后准备交付；同一契约的文档同步由任务 4 统一记录，避免重复事实。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 模块验收 1 | 任务 2 | 单元 | AC-1 |
| 模块验收 2 | 任务 2 | 单元 | AC-2 |
| 模块验收 3 | 任务 2 | 单元 | AC-3 |
| 模块验收 4 | 任务 2 | 单元 | AC-4 |
| 模块验收 5 | 任务 2 | 单元 | AC-5 |
| 模块验收 6 | 任务 2 | 单元 | AC-6 |
| 模块验收 7 | 任务 2 | 单元 | AC-7 |
| 模块验收 8 | 任务 2 | 单元 | AC-8 |
| 模块验收 9 | 任务 2 | 单元 | AC-9 |
| 模块验收 10 | 任务 2 | 单元 | AC-10 |

## 风险与回退

模块清单和发布汇总较复杂，先保留旧模式并用旧测试兜底；失败回退本次模块扩展，不改动上一轮尚未提交的修改。最终人工验收与远端 CI 不伪造。
