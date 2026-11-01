---
产物: implementation
阶段: 05-编码实现
编号: IMP-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 04-tasks.md
修订: 3
不适用: -
---

# 编码实现：项目接入与使用说明

## 实现摘要

### 修订 3：参考上游 SETUP 的引导写法

用户要求参考 DSH SETUP 重写。改为检查、询问信息、说明方案、执行、验证交接五步，采用少量必要问题与默认值，保留已有授权内连续执行的约定。README 精简首次接入段落，继续使用 GitHub URL，不要求个人目录。实际修改为文档，87 项测试重新通过，没有执行上游安装命令或实际发布。

### 修订 2：改为 GitHub 接入

依据用户“不要本地目录，我也会上传至github”更正接入方式：GitHub SETUP 链接作为入口，同仓库下载完整标准并核实提交，所有使用命令为业务项目相对路径。尚未设置 Git remote，地址明确留占位，不编造已发布 URL。重新运行 87 项测试通过；没有执行 GitHub 发布或真实远端获取。

新增 Agent 接入流程和使用约定，重写 README 的业务项目使用路径与自然语言示例；不实现新命令或修改门禁。

## 任务执行记录

### 任务 1：补充项目接入和用法

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：python3（本次准备脚本末尾对 SETUP.md 和 policies/usage.md 的 Path.exists 检查）
  - 输出摘要：两文件均 False，确认文档缺口；这是修改前走查记录，不是新增代码的失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：87 tests，OK；临时业务快照按 README 的实际脚本和模块命令验证通过。
- 与计划的偏差：仅文档，不声称代码 TDD；CI 和技能自动发现尚未实际接入。

### 任务 2：补充项目接入和用法

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：python3（本次准备脚本末尾对 SETUP.md 和 policies/usage.md 的 Path.exists 检查）
  - 输出摘要：两文件均 False，确认文档缺口；这是修改前走查记录，不是新增代码的失败测试。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：87 tests，OK；临时业务快照按 README 的实际脚本和模块命令验证通过。
- 与计划的偏差：仅文档，不声称代码 TDD；CI 和技能自动发现尚未实际接入。

## 变更文件

| 文件 | 变更类型 | 对应任务 |
|---|---|---|
| SETUP.md | 新增 | 任务 1 |
| policies/usage.md | 新增 | 任务 1 |
| policies/project-context.md | 修改 | 任务 1 |
| README.md | 修改 | 任务 2 |
| AGENTS.md | 修改 | 任务 2 |
| THIRD_PARTY_NOTICES.md | 修改 | 任务 2 |
| CHANGELOG.md | 修改 | 任务 2 |
| docs/engineering/project-usage-guide/ 与 docs/engineering/README.md | 新增及修改 | 任务 2 |

## 未完成项

本次文档范围无未完成。远端 CI、开发工具技能自动发现和真实多会话试跑未执行，SETUP 明确分别验证。

### 续做与交接记录

- 任务与执行者：project-usage-guide / 根 / 任务 2，同一代理顺序承担角色。
- 原始请求与授权：本聊天“补充，然后readme写一下怎么用”，沿用批量执行授权；不安装到真实业务项目或对外发布。
- 工作区：当前本地工作区，保留此前所有未提交修改。
- 输入：01–04 修订 1。
- 状态：05 完成，准备评审；本次范围无人工暂停。
- 验证：87 tests OK、两份样例通过；临时目录含空格路径的快照验证通过。
- 外部操作：无；临时项目已清理。
- 下一步：QA 与同一执行者自审，然后待最终验收。
