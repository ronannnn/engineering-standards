# 工程标准（engineering-standards）

一套**自研、全中文**的软件工程流程标准：8 个阶段、根目录 9 份冻结产物、可选多层模块资料、机器门禁 + 人工签收。目标是让 agent 能独立推进「需求 → 设计 → 计划 → 实现 → 测试评审 → 交付」，人只在关键节点签收。

## 它解决什么问题

Agent 写代码最大的问题不是不会写，而是**声称做完了但没验证**：测试没跑、验收标准没对、评审自己给自己过。本仓库用三样东西对抗它：

1. **固定产物**：每个阶段必须产出固定标题结构的文档，缺节就是缺节，脚本能判。
2. **冻结与签收**：产物一旦冻结只读；人没签收，下游不许开工。
3. **证据契约**：声明完成必须带命令与输出；评审默认不相信实现者报告。

## 第一次使用

在开发工具中打开要开发的业务项目，把本仓库 GitHub 上的 `SETUP.md` 链接交给 Agent：

> 阅读 `https://github.com/<owner>/<repo>/blob/<ref>/SETUP.md`，按其中说明把工程标准接入当前项目。

把占位符替换为实际链接即可，无需提供电脑目录。Agent 会检查项目、只问缺失信息、说明改动、完成接入并验证。具体流程见 [SETUP.md](SETUP.md)。

默认将标准放入业务项目的 `.engineering-standards/`，项目配置放入 `docs/engineering/_custom/project.md`，保留原规则和代码。标准随业务仓库保存，供团队与 CI 使用同一版本；技能入口和 CI 按项目实际能力接入，验证结果分别说明。

本仓库不限定开发语言、框架或设计风格，已有项目从下一项实际需求开始使用，不必重写全部历史资料。

默认按当前需求直接修改，不主动保留旧接口、旧字段、双写或额外兜底。只有用户或项目明确要求时才做必要兼容，避免代码因假设性保护持续膨胀；相关规则见[直接变更与迁移](policies/compatibility-migration.md)。

## 日常怎么说

**自然语言是默认入口，快捷指令可选，脚本负责实际操作。** 不用记住八阶段或所有角色名称。

| 你可以这样说 | Agent 会按规范处理 |
|---|---|
| 开始“优惠券导入”需求，先分析现有代码 | 建立需求目录，从需求和验收标准开始 |
| 继续 coupon-import | 核对进度、暂停和修订后，从未完成处继续 |
| 需求补充：导入时需要识别重复优惠券 | 关联原任务，必要时修订冻结需求和下游资料 |
| 看看现在做到哪了 | 说明阶段、正在做或等什么、证据和缺口 |
| 检查 coupon-import 是否可以交付 | 执行交付检查，报告未通过项和待人工签收项 |
| 先别改，帮我看一下问题 | 在授权范围内只检查和说明，保留暂停条件 |
| 把本项目的标准更新到指定版本 | 对照迁移说明更新标准，保留项目配置和历史产物 |

这些是自然语言示例，不是已经注册的斜杠命令。明确调用技能时也可说“使用 org-requirements 处理 coupon-import”。处理规则详见 [使用约定](policies/usage.md)。

Agent 在需求确认、重大设计、关键页面和最终交付等必要节点交人确认；已有授权能覆盖的操作不重复询问。接入成功不等于未来需求或最终交付已签收。

## 手动执行已有命令

下列命令均在**业务项目根目录**执行，假设 Agent 已从 GitHub 获取标准并按 SETUP 放好 `.engineering-standards/`。路径相对业务项目，不依赖任何人的电脑目录。

```bash
# 创建需求：九份草稿和运行索引
bash .engineering-standards/scripts/init-docs.sh coupon-import

# 填写资料后检查当前阶段
python3 .engineering-standards/gates/run.py docs/engineering/coupon-import --stage 01

# 检查下一阶段；该命令不会自动执行开发
python3 .engineering-standards/gates/run.py docs/engineering/coupon-import --next

# 合并前检查 01–07；上线观察和复盘后再完整归档
python3 .engineering-standards/gates/run.py docs/engineering/coupon-import --delivery
python3 .engineering-standards/gates/run.py docs/engineering/coupon-import --all
```

新建文件都是草稿，未填写或缺签收时检查失败是正常现象。`--stage` 当前内容自检通过不等于已冻结；交付和归档还会检查签收及依赖。先填写并按规则冻结，不为“全绿”编造签收或验证结果。

需求 slug 使用小写字母或数字分段，段间一个连字符，例如 `coupon-import`；不能使用连续或结尾连字符，以保证初始化目录也能被 CI 识别。

示例以 Bash 和 Python 3.12 为验证环境，门禁只依赖 Python 标准库。标准仓库自身维护时，脚本路径直接使用 `scripts/` 和 `gates/`，不加快照前缀。

## 目录导航

| 路径 | 内容 |
|---|---|
| [SETUP.md](SETUP.md) | Agent 接入业务项目、验证、升级和移除的操作说明 |
| [使用约定](policies/usage.md) | 自然语言、可选快捷指令与实际脚本的分工 |
| [AGENTS.md](AGENTS.md) | 常驻规则索引：流程、产物契约、状态机、门禁、角色写权限 |
| `skills/` | 14 个技能：8 个阶段技能 + 6 个角色技能 |
| `templates/` | 9 份产物模板 + 可选模块清单（固定锚点） |
| `policies/` | 质量、安全、兼容、交付、项目接入、生命周期与实际试跑 |
| `gates/` | 门禁脚本（Python 3 标准库，零依赖）+ 自测 |
| `adapters/` | 各技术栈与设计体系的接入说明（不搬上游正文） |
| `scripts/` | 脚手架：生成运行目录 |
| `examples/sample-run/` | 一份完整填好的样例（同时是门禁的测试基线） |
| `.github/workflows/` | PR 上检查 01–07，归档另跑全链 |

## 流程

```
01 需求分析  requirements.md       人签收
02 技术设计  design.md             重大设计才签收
03 UI/UX     ui-design.md          关键页面才签收
04 开发计划  tasks.md              自动
05 编码实现  implementation.md     自动（需 RED/GREEN 证据）
06 测试与评审 test-report.md + review-report.md  自动（风险升级）
07 集成与交付 delivery.md          人签收
08 维护与复盘 retro.md             按需
```

## 按模块组织大需求

复杂需求默认从需求分析就拆成“总览 → 功能 → 子功能”：总文档保留范围和导航，具体行为、异常及验收在对应功能文件展开。先看功能树，再逐项确认，避免生成一篇难审阅的产品长文。小需求可保留单文件，细则见 [需求拆分与阅读](policies/requirements-organization.md)。

可先看[短文档需求树示例](examples/requirements-tree/README.md)：总览只管整体，搜索和收藏各自说明用户价值、优先级和独立验收，根保留组合路径检查。拆分后还要核对原始诉求是否有归属，不能只把长文移动成几个文件。

支持 `modules/users/access/` 这样的多层模块目录。需求、设计、任务、实现、测试评审和维护记录按同一路径对应；公共架构和设计规范在根维护，07 统一交付。旧的九文件目录继续可用。

以下仍从已接入的业务项目根目录执行；04 检查需先完成该模块上游资料。

```bash
python3 .engineering-standards/scripts/init-module.py docs/engineering/coupon-import users/access
python3 .engineering-standards/gates/run.py docs/engineering/coupon-import --module users/access --stage 04
```

目录、引用、依赖和迁移见 [模块资料规则](policies/modular-artifacts.md)，完整示例见 [多层模块样例](examples/modular-run/README.md)。

## 长期使用

更新标准时告诉 Agent 目标版本，按 [SETUP 更新流程](SETUP.md#升级与移除) 比较差异、验证和合并。当前没有自动升级命令；业务配置、需求、暂停与签收历史必须保留。

按 [生命周期说明](policies/lifecycle.md) 派任务、交接、换会话续做、处理故障和安排后续迭代。小改动可以简写，复杂改动增加分析；角色按需承担，不要求全部并行运行。

补充消息先交原任务负责人，避免重复开工；记录授权范围和人工暂停。八阶段说明做到哪一步，运行状态说明在做什么或等谁。模板提供记录位置，自动接单、消息发送和实际权限隔离由项目选用的工具实现。

用 [三类实际任务](policies/workflow-evaluation.md) 试跑标准，记录真实结果。门禁通过与真实 Agent 试跑分别报告。

## 与上游的关系

本仓库不含上游正文。借鉴结构与方法：Superpowers（MIT，铁律 + 不信报告 + 修复上限）、BMAD（MIT，step-file 与自定义覆盖层）、Vercel web-interface-guidelines（MIT，可判定的检查清单形态）、DeepSeek Harness 的工程实践（规则索引 + 预推送证据选择 + AI 参与度声明）。各来源和具体文件声明见 [第三方登记](THIRD_PARTY_NOTICES.md)；不包含上游正文或代码。

另参考 [DSH Superagent 原型](https://github.com/deepseek-ai/dsh-superagent-prototype) 的任务归属、授权边界、等待状态和恢复方法，已中文重述到生命周期、项目接入和模板；未接入其运行平台。

## 维护

- 改门禁 = 同时改模板与对应技能（三处同源）。
- 任何改动跑 `python3 -m unittest discover gates/tests`。
- 变更记录写 [CHANGELOG.md](CHANGELOG.md)。

## 许可

自有内容，可内部分发与改造。第三方归属见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
