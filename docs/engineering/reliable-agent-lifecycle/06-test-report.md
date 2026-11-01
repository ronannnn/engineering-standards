---
产物: test-report
阶段: 06-测试与评审
编号: TST-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-10-31
依据: 05-implementation.md
修订: 2
不适用: -
---

# 测试报告：回归与文档契约

## 测试范围

覆盖本次 AC-1 至 AC-14。自动检查 51 项；文档行为以逐项阅读和场景走查检查，未执行模型 API 或真实业务验收。

## 环境与版本

本地 Python 3 标准库；具体运行时版本见 evidence/environment.txt。样例来自 examples/sample-run，所有反例隔离在临时目录。

## 用例与结果

| 编号 | 对应验收标准 | 类型 | 命令 | 结果 | 证据 |
|---|---|---|---|---|---|
| T-1 | AC-1 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-2 | AC-2 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-3 | AC-3 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-4 | AC-4 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-5 | AC-5 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-6 | AC-6 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-7 | AC-7 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-8 | AC-8 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |
| T-9 | AC-9 | 手工 | `逐项阅读对应模板、策略与技能，按场景走查` | 通过 | evidence/manual-review.md（流程走查，不是实际 Agent 试跑） |
| T-10 | AC-10 | 手工 | `逐项阅读对应模板、策略与技能，按场景走查` | 通过 | evidence/manual-review.md（流程走查，不是实际 Agent 试跑） |
| T-11 | AC-11 | 手工 | `逐项阅读对应模板、策略与技能，按场景走查` | 通过 | evidence/manual-review.md（流程走查，不是实际 Agent 试跑） |
| T-12 | AC-12 | 手工 | `逐项阅读对应模板、策略与技能，按场景走查` | 通过 | evidence/manual-review.md（流程走查，不是实际 Agent 试跑） |
| T-13 | AC-13 | 手工 | `逐项阅读对应模板、策略与技能，按场景走查` | 通过 | evidence/manual-review.md（流程走查，不是实际 Agent 试跑） |
| T-14 | AC-14 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt：51 项通过；evidence/red.txt：旧代码反例失败 |

## 失败与修复

无失败用例。基线 RED 用于验证回归能抓住旧问题，不作为修复后测试失败；详情见 evidence/red.txt。实际开发中修正了样例对未覆盖 AC-1 的 T-5 的错误引用，以及待签收交付内容自检要求提前填写验收的问题，现均通过。

## 覆盖率

不适用：本仓库未配置覆盖率工具，使用可重现的合法/违规输入、依赖场景与文档契约检查，不能据此宣称行覆盖率。

## 矩阵审计

| 验收标准 | 是否有已执行用例 | 依据用例 |
|---|---|---|
| AC-1 | 是 | T-1 |
| AC-2 | 是 | T-2 |
| AC-3 | 是 | T-3 |
| AC-4 | 是 | T-4 |
| AC-5 | 是 | T-5 |
| AC-6 | 是 | T-6 |
| AC-7 | 是 | T-7 |
| AC-8 | 是 | T-8 |
| AC-9 | 是 | T-9 |
| AC-10 | 是 | T-10 |
| AC-11 | 是 | T-11 |
| AC-12 | 是 | T-12 |
| AC-13 | 是 | T-13 |
| AC-14 | 是 | T-14 |

## 未覆盖与风险

远端 Actions 未运行，专用安全扫描未配置，真实 Agent 的三类试跑未执行。静态走查不能替代实际并发、生产发布或多会话恢复验证；使用政策中的试跑场景逐步验证。

## 结论

- 结论：可发布
- 依据：本地回归和文档走查通过；此结论仅表示可提交给维护者验收，不代表已经发布或人工签收。
