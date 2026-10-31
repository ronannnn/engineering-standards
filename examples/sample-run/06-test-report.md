---
产物: test-report
阶段: 06-测试与评审
编号: TST-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-03
依据: 05-implementation.md
修订: 1
不适用: -
---

# 测试报告：优惠券批量导入

## 测试范围

覆盖 AC-1 到 AC-4；不覆盖真实发放服务的线上压测（需生产配额），以预发环境的 500 行样本代替。

## 环境与版本

macOS 15 / Go 1.23 / Node 24 / pnpm 10；预发数据库 MySQL 8.4；发放服务预发实例；使用预发测试账号，密钥来自环境变量。

## 用例与结果

| 编号 | 对应验收标准 | 类型 | 命令 | 结果 | 证据 |
|---|---|---|---|---|---|
| T-1 | AC-1 | 单元 | `go test ./internal/coupon/import/... -run TestTemplate` | 通过 | `ok 0.221s — 3 passed` |
| T-2 | AC-2 | 集成 | `go test ./internal/coupon/handler/... -run TestImportPreview` | 通过 | `ok 0.988s — 5 passed`，错误行号断言通过 |
| T-3 | AC-3 | 集成 | `go test ./internal/coupon/handler/... -run TestImportCommit` | 通过 | 500 行导入后批次计数 500，撤回后失效 500 |
| T-4 | AC-4 | 集成 | `go test ./internal/coupon/handler/... -run TestImportCommitIdempotent` | 通过 | 连续两次确认，批次数量为 1 |
| T-5 | AC-2、AC-3 | e2e | `pnpm --filter operator test:e2e -- coupon-import` | 通过 | Playwright 3/3 通过，截图 artifacts/e2e-import.png |

## 失败与修复

无失败用例

## 覆盖率

`go test ./... -coverprofile=cover.out` 后 `go tool cover`：新增包 `internal/coupon/import` 94.2%，`internal/coupon/handler` 91.7%；前端导入页 `vitest --coverage` 88.1%。盲区在 `parser.go` 的 GBK 分支（预发未提供 GBK 样本）。

## 矩阵审计

| 验收标准 | 是否有已执行用例 | 依据用例 |
|---|---|---|
| AC-1 | 是 | T-1、T-5 |
| AC-2 | 是 | T-2、T-5 |
| AC-3 | 是 | T-3、T-5 |
| AC-4 | 是 | T-4 |

## 未覆盖与风险

- GBK 编码分支未用真实文件验证，风险为低（运营侧样本均为 UTF-8），已记入 08 的观察项。
- 未在生产配额下压测，P95 只在预发测得 12 秒。

## 结论

- 结论：可发布
- 依据：AC-1 至 AC-4 全部有用例通过，覆盖率均在 88% 以上，无失败用例
