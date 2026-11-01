---
产物: test-report
阶段: 06-测试与评审
编号: TST-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 05-implementation.md
修订: 1
不适用: -
---

# 测试与评审：初始化与增量校验优化

## 测试范围

AC-1至AC-4：初始化、CI一致性、索引、自定义备注、完整单次读取及既有校验行为。

## 环境与版本

本地 macOS、Bash、Python3.12，b673936基础上的工作区；测试使用临时文件和虚构样例，不访问生产或外部模型。

## 用例与结果

| 编号 | 对应验收标准 | 类型 | 命令 | 结果 | 证据 |
|---|---|---|---|---|---|
| T-1 | AC-1、AC-2 | 单元 | python3 -m unittest discover gates/tests -p test_scaffold.py | 通过 | 全套94项中包括5项脚手架回归：非法无副作用、CI识别、索引短名称与备注、拒绝覆盖、自定义索引格式 |
| T-2 | AC-3、AC-4 | 单元 | python3 -m unittest discover gates/tests | 通过 | evidence/green.txt：94项OK，包含两次 --next 之间修改必须重新检查的回归 |
| T-3 | AC-4 | 集成 | python3 gates/run.py examples/sample-run --all；python3 gates/run.py examples/modular-run --all | 通过 | 两份样例均通过 |
| T-4 | AC-3 | 手工 | 对b673936和当前 next_stage 包装 Artifact 读取计数 | 通过 | 同一完整样例：优化前39次，优化后9次；没有耗时结论 |

## 失败与修复

初始93项4个失败见evidence/red.txt；索引备注次序反例见evidence/red-index.txt。统一名称、精确表格插入和单次上下文复用后94项通过。

## 覆盖率

不适用：本次使用行为与读取计数回归，不新增覆盖率工具或依赖。

## 矩阵审计

| 验收标准 | 是否有已执行用例 | 依据用例 |
|---|---|---|
| AC-1 | 是 | T-1 |
| AC-2 | 是 | T-1 |
| AC-3 | 是 | T-2、T-4 |
| AC-4 | 是 | T-2、T-3 |

## 未覆盖与风险

未在原生 Windows 或远端 CI 执行；没有修改模块 --next 的读取策略，未处理脚手架多进程事务。交付仍要求最终人签收。

## 结论

- 结论：可发布
- 依据：94项回归、两份样例和命令语法检查通过；指代码变更就绪，不代替最终交付。
