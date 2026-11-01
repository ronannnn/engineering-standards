---
产物: implementation
阶段: 05-编码实现
编号: IMP-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 04-tasks.md
修订: 1
不适用: -
---

# 编码实现：默认直接实现当前需求

## 实现摘要

默认当前契约直接修改，明确要求时才保留兼容和必要范围；替换强制旧版本窗口及双写，清理假设性保护。同步设计、实现、评审与角色说明和模板，必要安全和真实数据处理仍保留。

## 任务执行记录

### 任务 1：同步当前契约直接实现规则

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读原 policies/compatibility-migration.md 并检索模板技能中的兼容要求
  - 输出摘要：旧策略强制两个发布周期、前后端双向兼容、双写，架构师技能要求数据兼容窗口；这是文档冲突走查，不是代码失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK，完整普通及模块样例、需求阶段示例通过；临时设计夹具明确无旧版支持亦通过阶段02。
- 与计划的偏差：04修订2纳入安全策略迁移恢复措辞同步；未改变门禁条件，仅更新诊断提示。

### 任务 2：同步当前契约直接实现规则

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读原 policies/compatibility-migration.md 并检索模板技能中的兼容要求
  - 输出摘要：旧策略强制两个发布周期、前后端双向兼容、双写，架构师技能要求数据兼容窗口；这是文档冲突走查，不是代码失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK，完整普通及模块样例、需求阶段示例通过；临时设计夹具明确无旧版支持亦通过阶段02。
- 与计划的偏差：04修订2纳入安全策略迁移恢复措辞同步；未改变门禁条件，仅更新诊断提示。

### 任务 3：同步当前契约直接实现规则

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读原 policies/compatibility-migration.md 并检索模板技能中的兼容要求
  - 输出摘要：旧策略强制两个发布周期、前后端双向兼容、双写，架构师技能要求数据兼容窗口；这是文档冲突走查，不是代码失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK，完整普通及模块样例、需求阶段示例通过；临时设计夹具明确无旧版支持亦通过阶段02。
- 与计划的偏差：04修订2纳入安全策略迁移恢复措辞同步；未改变门禁条件，仅更新诊断提示。

### 任务 4：同步当前契约直接实现规则

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读原 policies/compatibility-migration.md 并检索模板技能中的兼容要求
  - 输出摘要：旧策略强制两个发布周期、前后端双向兼容、双写，架构师技能要求数据兼容窗口；这是文档冲突走查，不是代码失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK，完整普通及模块样例、需求阶段示例通过；临时设计夹具明确无旧版支持亦通过阶段02。
- 与计划的偏差：04修订2纳入安全策略迁移恢复措辞同步；未改变门禁条件，仅更新诊断提示。

## 变更文件

| 文件 | 变更类型 | 对应任务 |
|---|---|---|
| policies/compatibility-migration.md、AGENTS.md、README.md、policies/project-context.md、CHANGELOG.md | 修改 | 任务 1 |
| templates/02-design.md、templates/05-implementation.md、templates/06-review-report.md、gates/gate02_design.py | 修改 | 任务 2 |
| skills/org-design/SKILL.md、skills/org-implement/SKILL.md、skills/org-test-review/SKILL.md | 修改 | 任务 3 |
| skills/org-role-architect/SKILL.md、skills/org-role-dev/SKILL.md、skills/org-role-reviewer/SKILL.md、policies/security.md | 修改 | 任务 4 |
| docs/engineering/simple-changes/ 与运行索引 | 新增及修改 | 任务 4 |

## 未完成项

本次规范范围无未完成；远端CI与最终交付未执行，未修改任何业务项目或清理无关历史实现。

### 续做与交接记录

- 任务：simple-changes / 根 / 任务4；同一代理执行与自审。
- 请求：用户要求默认不加过度保护和兼容；仅本地规则修改，没有发布或删除数据授权。
- 输入：01–03修订1，04修订2。
- 状态：实现完成待评审；无本次范围人工暂停。
- 验证：95项OK，三份示例、当前契约设计和diff检查通过。
- 下一步：06自审与准备交付；没有执行提交或外部操作。
