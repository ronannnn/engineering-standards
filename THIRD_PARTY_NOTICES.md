# 第三方来源与许可

本仓库的流程正文为中文重述，不包含下列项目的原文或代码。引用指向本次学习的官方文件；上游会变化，今后直接引入内容前应按实际文件和版本核对声明，保留必要的归属信息。

| 来源 | 本次核对的声明或范围 | 吸收的方法 | 具体资料 |
|---|---|---|---|
| obra/superpowers | 仓库 MIT | 任务拆分、先验证失败再修复、完成前验证、评审与修复循环 | [调试](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)、[完成验证](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) |
| bmad-code-org/BMAD-METHOD | 仓库 MIT；本次参考公开主分支，可能含预览内容 | 角色职责、默认/团队/个人覆盖、按工作规模组织流程 | [角色定制](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/customize/customize-bmad.md)、[合并实现](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad/scripts/config_utils.py) |
| vercel-labs/web-interface-guidelines | 仓库 MIT | 具体、可核对的界面检查 | [检查清单](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md) |
| vercel-labs/agent-skills | 按具体技能核对：react-best-practices 的 SKILL.md 标注 MIT，不据此推断整个仓库所有文件 | 按主题和优先级拆分规则，具体框架规则按项目选用 | [React 技能声明](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) |
| pbakaus/impeccable | 官方仓库 LICENSE 为 Apache-2.0；不将本地安装包与上游仓库混为同一版本 | 按页面用途调整设计力度、先读项目上下文、实际渲染验证 | [技能入口](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md)、[LICENSE](https://github.com/pbakaus/impeccable/blob/main/LICENSE) |
| deepseek-ai/deepseek-harness | 官方仓库声明 MIT | 相关改动选择验证、证据与评审范围、防御性模式 | [预推送检查](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-pre-push-checks/SKILL.md)、[评审](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-code-review/SKILL.md) |
| deepseek-ai/dsh-superagent-prototype | 官方研究原型，仓库 MIT；2026-11-01 核对，参考提交 6337fc823ce20251c8de8085948165c81aaa701e | 原任务处理追问、授权边界、运行等待原因、人工暂停保留、恢复与通知回执；只中文重述方法，未引入运行平台 | [授权](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/002-authorization.md)、[执行](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/003-execution.md)、[暂停与恢复](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/prompts/team/scope.md)、[发送记录实现](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/src/app/outbox.ts)、[许可](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/LICENSE) |
| Anthropic | 官方文章和示例，仅参考方法 | 清晰派发任务、持久进度、以实际结果评估 Agent | [长期工作](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)、[评估](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) |
| Fission-AI/OpenSpec 与 GitHub Spec Kit | 仅参考官方工作方法，不引入代码 | 变更记录、持续维护需求、项目自定义与返工 | [OpenSpec 流程](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)、[Spec Kit](https://github.com/github/spec-kit) |
| Google Engineering Practices 与 Google SRE | 仅参考官方公开文档 | 评审区分必要问题和建议、紧急修复后补审、发布观察 | [评审标准](https://google.github.io/eng-practices/review/reviewer/standard.html)、[紧急评审](https://google.github.io/eng-practices/review/emergencies.html)、[小范围发布](https://sre.google/workbook/canarying-releases/) |
| PagerDuty | 仅参考公开故障处理文档 | 协调/修复/记录分工、复盘与后续任务分别跟踪 | [角色](https://response.pagerduty.com/before/different_roles/)、[复盘](https://response.pagerduty.com/after/post_mortem_process/) |
| LangGraph | 仅参考官方文档与测试，不引入运行框架 | 中断续做、防止恢复时重复执行外部操作 | [中断](https://docs.langchain.com/oss/python/langgraph/interrupts)、[恢复测试](https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/tests/test_interruption.py) |
| Agent Skills 与 DORA | 仅参考官方公开文档 | 有/无技能对照试跑，记录交付速度、失败、恢复及返工 | [技能试跑](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/evaluating-skills.mdx)、[交付指标](https://dora.dev/guides/dora-metrics/) |

本轮模块化另参考 [OpenSpec 多层 capability-path](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md)、[arc42 分层构件视图](https://docs.arc42.org/section-5/)、[C4 组件视图](https://c4model.com/diagrams/component) 和 [BMAD 共享架构决策](https://docs.bmad-method.org/plan/design-ux-and-architecture/)。只中文重述方法；模块清单、限定引用及修订快照为本仓库自己的设计选择，没有引入上游代码或正文。

旧版本关于 Impeccable“无许可声明”、DeepSeek Harness“未显式声明许可”，以及把整个 Vercel Agent Skills 一概视为无许可证的描述不再作为当前结论。此处记录事实范围，不包含对未检查文件的授权推断。

## 使用注意

需求细分另参考 [OpenSpec 行为规格](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md)、[OpenSpec 审阅顺序](https://github.com/Fission-AI/OpenSpec/blob/main/docs/reviewing-changes.md)、[BMAD V6.12 用户价值分组](https://github.com/bmad-code-org/BMAD-METHOD/blob/bab9082c3e884e0d72c759bcd1a6d90bcc01be84/src/bmm-skills/plan/bmad-create-epics-and-stories/steps/step-02-design-epics.md)、[BMAD 覆盖检查](https://github.com/bmad-code-org/BMAD-METHOD/blob/bab9082c3e884e0d72c759bcd1a6d90bcc01be84/src/bmm-skills/plan/bmad-create-epics-and-stories/steps/step-04-final-validation.md)、[Spec Kit 用户故事模板](https://github.com/github/spec-kit/blob/main/templates/spec-template.md)及[持久化选择](https://github.com/github/spec-kit/blob/main/docs/concepts/spec-persistence.md)、[Superpowers 独立规格与计划](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)。只中文重述方法，没有复制原文、程序或自动归并行为；BMAD 所核对的步骤将故事汇入 epics.md，不将其描述成自动按功能拆目录的实现。需求树和虚构示例沿用本仓库自己的产物契约。

项目接入另参考 [DSH SETUP](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/SETUP.md) 的 Agent 引导与检查交接、[BMAD 接入](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/start/install-bmad.md) 的项目配置分离、[OpenSpec 工具入口](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)、[Spec Kit 存量项目](https://github.com/github/spec-kit/blob/main/docs/guides/existing-projects.md) 和 [Superpowers 安装说明](https://github.com/obra/superpowers#installation)。仅中文重述接入思路；本仓库 SETUP 的快照路径、流程和自然语言使用约定为本仓库设计，不复制安装脚本或引入上游运行平台。

- 目前仅链接和中文重述，不复制上游正文或代码。
- 若以后引入具体内容，先记录文件、版本、来源及对应许可要求；不能认为改写成中文就自动免除来源要求。
- 本仓库门禁继续仅依赖 Python 3 标准库。
