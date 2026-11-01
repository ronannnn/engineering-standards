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

# 开发计划：优惠券批量导入

## 任务清单

### 任务 1：数据库迁移与批次表

- 文件：`migrations/20261101_coupon_import_batch.sql`、`internal/coupon/model.go`
- 依赖：无
- 验收方法：`go test ./internal/coupon/... -run TestMigrationUpDown`（期望：迁移与回滚各一次后表结构一致）
- 对应需求：FR-3

### 任务 2：CSV 解析与逐行校验

- 文件：`internal/coupon/import/parser.go`、`internal/coupon/import/validate.go`、`internal/coupon/import/parser_test.go`
- 依赖：任务 1
- 验收方法：`go test ./internal/coupon/import/... -run TestValidate`（期望：3 类错误各自命中，错误行号正确）
- 对应需求：FR-2

### 任务 3：预览与确认接口

- 文件：`internal/coupon/handler/import_handler.go`、`internal/coupon/service/import_service.go`、`internal/coupon/handler/import_handler_test.go`
- 依赖：任务 2
- 验收方法：`go test ./internal/coupon/handler/... -run TestImport`（期望：400/403/409/422 分支全绿，成功路径幂等）
- 对应需求：FR-2、FR-3

### 任务 4：前端导入页

- 文件：`apps/operator/pages/coupon/import.vue`、`apps/operator/components/coupon/ImportPreviewTable.vue`
- 依赖：任务 3
- 验收方法：`pnpm --filter operator test -- ImportPage`（期望：上传、错误展示、确认三态断言通过）
- 对应需求：FR-1、FR-2

## 里程碑与顺序

- 第一批（任务 1、2）：迁移可回滚、解析与校验单测全绿后暂停一次，由我确认错误文案。
- 第二批（任务 3、4）：接口契约测试与页面测试全绿后合并。
- 任一任务验收命令失败即停下修，不带失败进入下一批。

## 验证矩阵

| 场景 | 覆盖任务 | 验证类型 | 对应验收标准 |
|---|---|---|---|
| 模板下载 | 任务 4 | 单元 | AC-1 |
| 含 3 行错误的 CSV 预览 | 任务 2、3 | 集成 | AC-2 |
| 500 行确认与批次查询 | 任务 3 | 集成 | AC-3 |
| 撤回后全部失效 | 任务 3 | 集成 | AC-3 |
| 重复确认幂等 | 任务 3 | 集成 | AC-4 |
| 页面关键状态渲染 | 任务 4 | e2e | AC-1、AC-2 |

## 风险与回退

- 风险：发放服务批量接口限流，导致 500 行导入超时 → 回退为分批 200 条并在设计里补一条限流说明。
- 风险：CSV 编码（GBK）导致乱码 → 任务 2 加编码探测，失败时返回明确错误。
- 任务 1 独立可回滚，任务 2–4 未上线前不影响存量。
