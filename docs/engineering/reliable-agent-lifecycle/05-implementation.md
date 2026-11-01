---
产物: implementation
阶段: 05-编码实现
编号: IMP-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-10-31
依据: 04-tasks.md
修订: 2
不适用: -
---

# 实现记录：可靠门禁与持续生命周期

## 实现摘要

修复八处已确认问题，并补充空字段、重复标识、无效结论、格式读取错误及待签收内容自检的回归。同步项目接入、交接、续做、返工、紧急修复与长期维护方法，保留语言和设计系统由项目决定。所有代码仅使用 Python 标准库。

## 任务执行记录

### 任务 1：修复解析与检查范围

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 2：修复实现证据与验收关联

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 3：修复交付前置和工程检查

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 4：修复 CI 目录识别

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 5：补齐生命周期策略与入口说明

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 6：同步计划实现及测试评审契约

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 7：同步交付维护及角色工作方法

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

### 任务 8：补齐来源迁移与试跑资料

- 提交：本地工作区，尚未提交或发布
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests`（基线提交加本次回归测试，见 evidence/red.txt）
  - 输出摘要：50 项中 25 failures、11 errors，退出 1；解析、覆盖、交付及新增生命周期资料契约未满足
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：51 项全部通过，退出 0，详见 evidence/green.txt
- 与计划的偏差：首轮代码 RED 在实现前执行（evidence/red-initial.txt）；为可复核又在原始 HEAD 重放最终测试。文档任务的基线证据仅证明配套资料缺失，语义和交接可用性由 evidence/manual-review.md 逐项走查，不伪称纯文档严格 TDD。

## 变更文件

| 文件 | 变更类型 | 对应任务 |
|---|---|---|
| `.github/workflows/standards-gate.yml` | 修改 | 任务 4 |
| `AGENTS.md` | 修改 | 任务 5 |
| `CHANGELOG.md` | 修改 | 任务 8 |
| `README.md` | 修改 | 任务 5 |
| `THIRD_PARTY_NOTICES.md` | 修改 | 任务 8 |
| `examples/sample-run/05-implementation.md` | 修改 | 任务 1 |
| `examples/sample-run/06-test-report.md` | 修改 | 任务 1 |
| `examples/sample-run/07-delivery.md` | 修改 | 任务 1 |
| `examples/sample-run/08-retro.md` | 修改 | 任务 1 |
| `examples/sample-run/README.md` | 新增 | 任务 1 |
| `gates/_lib.py` | 修改 | 任务 1 |
| `gates/changed_runs.py` | 新增 | 任务 4 |
| `gates/gate05_implement.py` | 修改 | 任务 2 |
| `gates/gate06_review_report.py` | 修改 | 任务 3 |
| `gates/gate06_test_report.py` | 修改 | 任务 2 |
| `gates/gate07_delivery.py` | 修改 | 任务 3 |
| `gates/run.py` | 修改 | 任务 1 |
| `gates/spec.py` | 修改 | 任务 1 |
| `gates/tests/test_document_contracts.py` | 新增 | 任务 1 |
| `gates/tests/test_regressions.py` | 新增 | 任务 1 |
| `policies/delivery.md` | 修改 | 任务 7 |
| `policies/lifecycle.md` | 新增 | 任务 5 |
| `policies/project-context.md` | 新增 | 任务 5 |
| `policies/quality-gates.md` | 修改 | 任务 5 |
| `policies/workflow-evaluation.md` | 新增 | 任务 8 |
| `skills/org-deliver/SKILL.md` | 修改 | 任务 7 |
| `skills/org-design/SKILL.md` | 修改 | 任务 5 |
| `skills/org-implement/SKILL.md` | 修改 | 任务 5 |
| `skills/org-plan/SKILL.md` | 修改 | 任务 5 |
| `skills/org-requirements/SKILL.md` | 修改 | 任务 5 |
| `skills/org-retro/SKILL.md` | 修改 | 任务 7 |
| `skills/org-role-architect/SKILL.md` | 修改 | 任务 5 |
| `skills/org-role-dev/SKILL.md` | 修改 | 任务 5 |
| `skills/org-role-pm/SKILL.md` | 修改 | 任务 5 |
| `skills/org-role-qa/SKILL.md` | 修改 | 任务 5 |
| `skills/org-role-reviewer/SKILL.md` | 修改 | 任务 5 |
| `skills/org-role-ux/SKILL.md` | 修改 | 任务 5 |
| `skills/org-test-review/SKILL.md` | 修改 | 任务 5 |
| `skills/org-ui-design/SKILL.md` | 修改 | 任务 5 |
| `templates/04-tasks.md` | 修改 | 任务 6 |
| `templates/05-implementation.md` | 修改 | 任务 6 |
| `templates/06-review-report.md` | 修改 | 任务 6 |
| `templates/06-test-report.md` | 修改 | 任务 6 |
| `templates/07-delivery.md` | 修改 | 任务 7 |
| `templates/08-retro.md` | 修改 | 任务 7 |

## 未完成项

代码、规则、模板、样例和本地自动验证已完成。最终人工签收、远端 CI 与真实 Agent 三场景试跑未执行；后者是采用标准时的验证，不是这次脚本测试的结果。

### 续做与交接记录

- 当前任务与执行者：八项实现已完成，由同一代理继续核对与交付准备。
- 工作区：本仓库当前工作区，未提交。
- 输入修订：01/02/03/04 均为修订 1。
- 已完成与证据：evidence/ 下 RED、GREEN、样例和静态检查日志。
- 下一步与接收方：最终交付材料供维护者审阅，真实项目采用时按试跑说明验证。
- 外部操作及结果：未执行提交、合并、发布、生产迁移或写入，无需重放外部操作。
