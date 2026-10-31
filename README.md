# 工程标准（engineering-standards）

一套**自研、全中文**的软件工程流程标准：8 个阶段、9 份冻结产物、机器门禁 + 人工签收。目标是让 agent 能独立推进「需求 → 设计 → 计划 → 实现 → 测试评审 → 交付」，人只在关键节点签收。

## 它解决什么问题

Agent 写代码最大的问题不是不会写，而是**声称做完了但没验证**：测试没跑、验收标准没对、评审自己给自己过。本仓库用三样东西对抗它：

1. **固定产物**：每个阶段必须产出固定标题结构的文档，缺节就是缺节，脚本能判。
2. **冻结与签收**：产物一旦冻结只读；人没签收，下游不许开工。
3. **证据契约**：声明完成必须带命令与输出；评审默认不相信实现者报告。

## 三步上手

```bash
# 1) 把技能接入你的 agent（DSH 默认读取 ~/.agents/skills）
ln -s "$PWD/skills"/* ~/.agents/skills/

# 2) 在项目里初始化一个需求的运行目录
./scripts/init-docs.sh coupon-import

# 3) 在 agent 里说：用 org-requirements 开始处理 coupon-import
```

门禁：

```bash
python3 gates/run.py docs/engineering/coupon-import --all
```

## 目录导航

| 路径 | 内容 |
|---|---|
| [AGENTS.md](AGENTS.md) | 常驻规则索引：流程、产物契约、状态机、门禁、角色写权限 |
| `skills/` | 14 个技能：8 个阶段技能 + 6 个角色技能 |
| `templates/` | 9 份产物模板（机器锚点 + 「不适用」规则） |
| `policies/` | 四份策略：质量门禁、安全、兼容性与迁移、交付 |
| `gates/` | 门禁脚本（Python 3 标准库，零依赖）+ 自测 |
| `adapters/` | 各技术栈与设计体系的接入说明（不搬上游正文） |
| `scripts/` | 脚手架：生成运行目录 |
| `examples/sample-run/` | 一份完整填好的样例（同时是门禁的测试基线） |
| `.github/workflows/` | PR 上强制跑全链门禁 |

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

## 与上游的关系

本仓库不含上游正文。借鉴结构与方法：Superpowers（MIT，铁律 + 不信报告 + 修复上限）、BMAD（MIT，step-file 与自定义覆盖层）、Vercel web-interface-guidelines（MIT，可判定的检查清单形态）、DeepSeek Harness 的工程实践（规则索引 + 预推送证据选择 + AI 参与度声明）。`vercel-labs/agent-skills` 与 `impeccable` 无许可证或无声明，只借思路、不搬正文。

## 维护

- 改门禁 = 同时改模板与对应技能（三处同源）。
- 任何改动跑 `python3 -m unittest discover gates/tests`。
- 变更记录写 [CHANGELOG.md](CHANGELOG.md)。

## 许可

自有内容，可内部分发与改造。第三方归属见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
