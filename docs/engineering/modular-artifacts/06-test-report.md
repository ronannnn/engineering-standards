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

# 测试报告：多层目录、关联与统一交付

## 测试范围

覆盖 AC-1 至 AC-10：旧模式、多层模块、清单错误、依赖与公共基线、限定引用、统一发布及模块复盘。自动回归 87 项；新增功能初始 RED 的失败和最终 GREEN 分开保留。

## 环境与版本

本地 Python 3.12 标准库；测试在临时目录复制虚构样例，未调用模型 API、生产系统或网络。静态检查见 evidence/static.txt。

## 用例与结果

| 编号 | 对应验收标准 | 类型 | 命令 | 结果 | 证据 |
|---|---|---|---|---|---|
| T-1 | AC-1 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-2 | AC-2 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-3 | AC-3 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-4 | AC-4 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-5 | AC-5 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-6 | AC-6 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-7 | AC-7 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-8 | AC-8 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-9 | AC-9 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |
| T-10 | AC-10 | 单元 | `python3 -m unittest discover gates/tests` | 通过 | evidence/green.txt；AC-10 的资料对应另见 evidence/manual-review.md |

## 失败与修复

无失败用例。开发中修正了矩阵夹具的表格空行、原样例任务编号简写兼容，并补齐根不适用情况下的子模块覆盖及局部复盘对发布快照的检查。初始功能缺失的 RED 不作为最终失败，当前 87 项全绿。

## 覆盖率

不适用：未配置行覆盖率工具，不将通过计数等同于覆盖率。当前检查合法模块、重复/越界/循环、错误 JSON、失效基线、跨模块错引、遗漏 AC、未知任务、过期发布、归档和初始化保护。

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

## 未覆盖与风险

未执行真实团队或多 Agent 长期工作，未运行远端 Actions；静态/引用校验不能保证真实业务设计和集成测试质量。清单是本次变更范围，永久规范库自动合并不在本次范围。

## 结论

- 结论：可发布
- 依据：本地测试、旧/新样例、静态检查通过，可交维护者验收；不是已经发布或最终签收。
