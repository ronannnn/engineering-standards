# 第三方来源与许可

本仓库的正文全部为自研；下列项目仅作为结构、方法与检查项来源。凡吸收内容均改写为中文并在此登记。

| 项目 | 许可 | 本仓库借鉴了什么 | 是否含其正文 |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | 阶段硬 gate 与「冻结」概念；实现者交 RED/GREEN 证据、评审不信实现者报告；修复循环需有上限并显式裁定；技能用「触发时机」写 description、按需加载 references | 否，全部重写 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | MIT | step-file 式分步执行与 checkpoint 停人；`customize.toml` 三层覆盖与按形状合并（标量覆盖、数组追加、按 code 替换、不可删除）；角色 = 固定身份 + 可覆盖层 | 否，全部重写 |
| [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines) | MIT | 前端检查清单的形态：短句、可判定、按类分组 | 否，改写为 12 条最低要求 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **无许可证** | 只借鉴「一条规则一文件 + 正反例 + 索引按需加载」的结构思路 | 否，未复制任何正文 |
| `impeccable` 技能（本地安装） | **无许可声明** | 只借鉴「按页面模式决定设计强度」的方法 | 否，未复制任何正文 |
| DeepSeek Harness 仓库公开的工程实践（`AGENTS.md`、`.agents/skills/`、`docs/defensive-patterns/`、Agent Notes、PR 的 AI 参与度声明） | 仓库公开，许可未显式声明 | 规则索引形态、预推送按改动面选证据、AI 参与度分级、防御性模式的组织方式 | 否，全部按本仓库场景重写 |

## 使用注意

- 若将来需要直接引入上述 MIT 项目的正文片段，必须保留其版权声明与许可文本，并在本文件登记具体文件与改动。
- 无许可证的项目（Vercel agent-skills、impeccable）不得复制正文；如需引用，只引用公开链接与自己的转述。
- 本仓库不包含任何第三方代码依赖；`gates/` 仅使用 Python 标准库。
