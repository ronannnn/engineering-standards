# AGENTS.md — 工程标准仓库常驻规则

本仓库是一套**自研、全中文**的软件工程流程标准：把「从需求到交付」拆成 8 个阶段，每个阶段必须先产出固定格式的**冻结产物**，再由脚本门禁校验。目标是让 agent 能独立推进，人只在少数节点签收。

> 本文件是常驻规则索引，保持精简。每个阶段的执行细节在 `skills/`，产物字段在 `templates/`，门禁判据在 `gates/`。

## 1. 流程不可跳

```
01 需求分析 → 02 技术设计 → 03 UI/UX 设计 → 04 开发计划
   → 05 编码实现 → 06 测试与评审 → 07 集成与交付 → 08 维护与复盘
```

- 顺序不可跳；上一阶段产物未冻结，不得进入下一阶段（门禁检查依赖链）。
- 允许把某阶段标为 `不适用：<理由>`，理由必须非空，且该产物同样要冻结。
- 编码前必须有 04 的 `tasks.md`；声明完成前必须有 05 的 RED/GREEN 证据；合并前必须有 06 的测试与评审证据。

## 2. 产物清单（9 份文件）

| 阶段 | 产物文件 | 编号前缀 | 技能 | 校验器 | 人签收 |
|---|---|---|---|---|---|
| 01 需求分析 | `01-requirements.md` | `REQ` | `org-requirements` | `gate01_requirements.py` | **必须** |
| 02 技术设计 | `02-design.md` | `DES` | `org-design` | `gate02_design.py` | 重大设计 |
| 03 UI/UX 设计 | `03-ui-design.md` | `UIX` | `org-ui-design` | `gate03_ui_design.py` | 关键页面 |
| 04 开发计划 | `04-tasks.md` | `TSK` | `org-plan` | `gate04_plan.py` | 自动 |
| 05 编码实现 | `05-implementation.md` | `IMP` | `org-implement` | `gate05_implement.py` | 自动 |
| 06 测试与评审 | `06-test-report.md`、`06-review-report.md` | `TST`、`REV` | `org-test-review` | `gate06_test_report.py`、`gate06_review_report.py` | 自动，风险升级 |
| 07 集成与交付 | `07-delivery.md` | `DLV` | `org-deliver` | `gate07_delivery.py` | **必须** |
| 08 维护与复盘 | `08-retro.md` | `RTR` | `org-retro` | `gate08_retro.py` | 按需 |

## 3. 产物契约

### 3.1 frontmatter（每个产物首行起，`---` 包裹）

```yaml
---
产物: requirements
阶段: 01-需求分析
编号: REQ-0001
状态: 草稿
签收: -
签收时间: -
依据: -
修订: 1
不适用: -
---
```

- `产物` 取值固定（见上表文件名去掉序号与后缀）。
- `编号` 形如 `REQ-0001`，前缀必须与阶段匹配；同一运行目录内编号唯一。
- `依据` 填上一阶段产物文件名（`-` 表示无依赖）；门禁会核对被依赖文件的 `状态` 必须为 `已冻结`。
- `修订` 从 1 开始；每次重新冻结递增。
- `不适用` 取 `-` 或理由。填理由表示整份产物不适用：跳过内容检查，但必须 `已冻结` 且有人签收；04/05/06/07 不允许整份不适用。

### 3.2 状态机

```
草稿 → 待签收 → 已冻结 → 已废弃（终态，不可回到其他状态）
```

- **只有人**能把 `待签收` 改为 `已冻结`，并填写 `签收` 与 `签收时间`。
- 自动阶段（04/05/06）：门禁全部通过后由 agent 直接置 `已冻结`，`签收: 机器门禁`。
- 已冻结产物**只读**。要改：把状态改回 `待签收`、`修订` +1、重新走签收；不得直接改正文。
- `已废弃` 必须补一行 `废弃理由: <原因>`。

### 3.3 固定标题

模板里的二级标题（`## `）是**机器锚点**，不得改名、不得删除；内容可以改。新增内容请加在对应锚点之下，或使用三级标题。

## 4. 门禁

```bash
python3 gates/run.py docs/engineering/<slug> --all      # 全链校验
python3 gates/run.py docs/engineering/<slug> --stage 04 # 单段校验
python3 gates/run.py docs/engineering/<slug> --next     # 只校验「下一段应该做什么」
```

- 门禁只做**可判定**的检查：字段齐全、锚点齐全、证据存在、依赖已冻结、条件签收是否满足。设计好不好，门禁不管，人管。
- 失败时输出 `文件名:行号: 原因`，agent 必须修到全绿才能声明该阶段完成。
- CI（`.github/workflows/standards-gate.yml`）在 PR 上跑全链校验；缺产物、未签收、依赖未冻结都会红。

## 5. 角色与写权限

| 角色 | 技能 | 可写产物 |
|---|---|---|
| 产品经理 | `org-role-pm` | 01 |
| 架构师 | `org-role-architect` | 02 |
| UX 设计师 | `org-role-ux` | 03 |
| 开发 | `org-role-dev` | 04、05 |
| QA | `org-role-qa` | 06 测试报告 |
| 评审 | `org-role-reviewer` | 06 评审报告 |

- 角色只写自己拥有的产物；跨角色修改必须先由该产物的拥有者改，或由人显式授权并在产物里记录。
- 07 由产品经理与开发共同完成、由人签收；08 由全体参与、由人按需确认。
- **角色是可覆盖层**：项目可在 `docs/engineering/_custom/roles/<role>.toml` 追加团队规范（职责补充、原则、菜单、`file:` 常驻事实），不改本仓库的 SKILL.md。合并规则：标量覆盖、数组追加、带 `code` 的表按 code 替换、不允许删除基础项。个人偏好放 `_custom/roles/<role>.user.toml` 并自行 gitignore。

## 6. 命名与目录

- 运行目录：`docs/engineering/<需求 slug>/`，slug 用 kebab-case（如 `coupon-import`）。
- 一个需求一个目录，不要在目录里放与本需求无关的文件。
- 项目根 `docs/engineering/README.md` 由脚手架生成，列出所有运行目录与状态。

## 7. 允许的妥协

- 小改动可以走轻量路径：01/02/03 写清 `不适用：<理由>`（填在 frontmatter 的 `不适用` 字段），但 04/05/06/07 不可省。
- 单节不适用时，在该节正文写 `不适用：<非空理由>`；门禁只检查理由非空，不判断理由是否成立——理由是否成立由评审把关。
- 禁止用「已口头确认」「之前讨论过」替代签收字段；没有字段就等于没有发生。

## 8. 修改本仓库的规则

1. 三处同源：改门禁判据必须同步改模板与对应 `SKILL.md`；改模板锚点必须同步改门禁。
2. 收紧规则要在 `CHANGELOG.md` 写明理由与迁移方式。
3. 新增阶段或角色只加目录与门禁注册项，不改 `gates/run.py` 的核心流程。
4. `gates/` 只允许 Python 3 标准库，禁止第三方依赖。
5. 任何改动都要跑 `python3 -m unittest discover gates/tests`，全绿才算完成。

## 9. 上游来源与许可

本仓库不含上游正文。可借鉴的 MIT 项目（[Superpowers](https://github.com/obra/superpowers)、[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)、[web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines)）吸收时改写为中文并注明出处；[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) 与 `impeccable` 无许可证或无声明，只借鉴结构与思路，不搬运正文。
