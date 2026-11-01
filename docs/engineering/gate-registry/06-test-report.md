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

# 测试与评审：统一门禁注册并删除未用代码

## 测试范围

AC-1注册驱动真实阶段执行及错误定位；AC-2旧判据、示例、链接与被删代码调用检查。

## 环境与版本

macOS、Python3.12，本地a993d7f基础上的工作区；临时自定义检查只存在于测试patch，不新增生产阶段。

## 用例与结果

| 编号 | 对应验收标准 | 类型 | 命令 | 结果 | 证据 |
|---|---|---|---|---|---|
| T-1 | AC-1、AC-2 | 单元 | python3 -m unittest discover gates/tests | 通过 | evidence/green.txt：96项OK，新增登记模块实际调用，主动报错时文件行号被正确输出 |
| T-2 | AC-2 | 集成 | python3 gates/run.py examples/sample-run --all；python3 gates/run.py examples/modular-run --all；python3 gates/run.py examples/requirements-tree --stage 01 | 通过 | 三份示例通过对应检查 |
| T-3 | AC-2 | 手工 | 检索旧映射、5个被删助手与未用变量；git diff --check | 通过 | 无残余调用，无空白错误，原有96项回归覆盖模板和行为 |

## 失败与修复

RED为新登记产物仍触发KeyError，两个子场景见evidence/red.txt；直接读取gate字段后96项GREEN见evidence/green.txt。

## 覆盖率

不适用：不引入覆盖率依赖，按注册执行与原行为回归验证。

## 矩阵审计

| 验收标准 | 是否有已执行用例 | 依据用例 |
|---|---|---|
| AC-1 | 是 | T-1 |
| AC-2 | 是 | T-1、T-2、T-3 |

## 未覆盖与风险

未运行远端CI或外部模型；移除的是仓库无调用内部API，没有保留未要求的兼容别名。自定义登记需明确填写gate。

## 结论

- 结论：可发布
- 依据：实际注册行为、96项回归及三份示例通过，最终交付仍待人确认。
