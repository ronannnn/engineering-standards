---
产物: implementation
阶段: 05-编码实现
编号: IMP-0001
状态: 已冻结
签收: 机器门禁
签收时间: 2026-11-01
依据: 04-tasks.md
修订: 2
不适用: -
---

# 编码实现：按功能细分需求并方便审阅

## 实现摘要

### 修订2：学习上游后补齐验证与示例

研究OpenSpec、BMAD V6.12、Spec Kit和Superpowers，新增单条行为、优先级理由、独立验收、来源覆盖及组合闭环；提供两叶子虚构草稿示例。04修订2增加示例和回归任务，来源登记同步。

新增需求组织说明，复杂需求按功能和子功能细分；根写总览与导航，叶子写完整用户行为、边界和AC；同步模板、需求与PM技能、原模块说明和入口。未修改业务项目。

## 任务执行记录

### 任务 1：同步需求组织规范

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读修改前 org-requirements、01模板及 modular-artifacts
  - 输出摘要：模块拆分仅为可选组织说明，缺少先功能树、根导航、叶子闭环及用户审阅顺序；文档走查发现缺口，不冒充运行代码失败。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：94项通过；人工核对技能模板和入口已覆盖AC-1，两份样例--all通过。
- 与计划的偏差：无运行代码或新门禁字段，未新增只匹配文字的测试。

### 任务 2：同步需求组织规范

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：阅读修改前 org-requirements、01模板及 modular-artifacts
  - 输出摘要：模块拆分仅为可选组织说明，缺少先功能树、根导航、叶子闭环及用户审阅顺序；文档走查发现缺口，不冒充运行代码失败。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：94项通过；人工核对技能模板和入口已覆盖AC-1，两份样例--all通过。
- 与计划的偏差：无运行代码或新门禁字段，未新增只匹配文字的测试。

### 任务 3：编写短需求树示例

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests -p test_document_contracts.py`
  - 输出摘要：示例目录不存在，1项失败；见 evidence/red-example.txt。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK；示例01内容自检通过，--delivery按草稿与缺未来产物预期拒绝；见 evidence/green-example.txt。
- 与计划的偏差：只验证需求阶段，不提前补完设计或虚构签收；95项替代此前94项结果。

### 任务 4：登记示例与回归

- 提交：本地工作区，未提交
- 测试命令：`python3 -m unittest discover gates/tests`
- RED 证据：
  - 命令：`python3 -m unittest discover gates/tests -p test_document_contracts.py`
  - 输出摘要：示例目录不存在，1项失败；见 evidence/red-example.txt。
- GREEN 证据：
  - 命令：`python3 -m unittest discover gates/tests`
  - 输出摘要：95项OK；示例01内容自检通过，--delivery按草稿与缺未来产物预期拒绝；见 evidence/green-example.txt。
- 与计划的偏差：只验证需求阶段，不提前补完设计或虚构签收；95项替代此前94项结果。

## 变更文件

| 文件 | 变更类型 | 对应任务 |
|---|---|---|
| policies/requirements-organization.md | 新增 | 任务 1 |
| templates/01-requirements.md、skills/org-requirements/SKILL.md、skills/org-role-pm/SKILL.md | 修改 | 任务 1 |
| policies/modular-artifacts.md、README.md、AGENTS.md、CHANGELOG.md | 修改 | 任务 2 |
| examples/requirements-tree/（根和两份叶子、清单） | 新增 | 任务 3 |
| examples/requirements-tree/README.md、gates/tests/test_document_contracts.py | 新增及修改 | 任务 4 |
| THIRD_PARTY_NOTICES.md | 修改 | 任务 2 |
| docs/engineering/requirements-navigation/ 与运行索引 | 新增及修改 | 任务 2 |

## 未完成项

本次标准修改无未完成项；业务项目更新标准及拆分现有长文未执行，不属于本次工作区范围。

### 续做与交接记录

- 当前任务与执行者：requirements-navigation / 根 / 任务2，同一代理。
- 请求与授权：用户说明标准生成需求过长，要求分析细分并便于阅读；只改标准，不改业务文件，不提交新任务。
- 输入修订：01–03修订1，04修订2。
- 状态：规则与模板完成；准备评审，无本次有效暂停。
- 验证：95项OK，两份完整样例和需求阶段示例通过；真实模型按新规则试跑未执行。
- 外部操作：无；下一步评审后准备交付，不代签最终验收。
