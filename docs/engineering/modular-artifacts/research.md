# 模块化组织的学习记录

先阅读官方资料，再确定本次实现。以下为方法摘要，没有复制上游正文或代码。

| 来源 | 读到的方法 | 本次采用方式 |
|---|---|---|
| [OpenSpec 概念](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) | 按领域组织需求，区分现状规范与一次变更 | 模块路径组织本次变更；未来迭代另建运行目录，不把变更目录当永久规范库 |
| [OpenSpec 需求编写](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md) | capability-path 可以有 identity/user-auth 这样的多层目录；需求描述可观察行为 | 支持多层模块路径，保持需求与设计分开、验收可检查 |
| [arc42 Building Block View](https://docs.arc42.org/section-5/) | 总体分解与细节逐层展开，说明每块职责和依赖 | 根写公共架构，模块写具体设计，目录层级不替代显式依赖 |
| [C4 组件视图](https://c4model.com/diagrams/component) | 在明确边界内展开组件细节及关系 | 根与模块明确范围，不强迫所有层都复制同一说明 |
| [BMAD UX 与架构](https://docs.bmad-method.org/plan/design-ux-and-architecture/) | 跨 epic 共享架构决策，让后续工作能找到这些输入 | 固定公共修订，模块工作保留依赖和引用，统一检查集成与发布 |

modules.json、path#编号、基线修订和统一交付快照是本仓库结合现有冻结制度作出的实现选择，不宣称其他来源也使用完全相同的格式。未引入 OpenSpec/BMAD 或任何其他第三方运行库。
