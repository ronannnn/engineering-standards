# 短文档需求树示例

全部内容为虚构草稿，没有真实签收，只演示01阶段，不提前创建或冻结02–08。

建议阅读顺序：[总览与原始诉求](01-requirements.md) → [搜索技能](modules/skills/search/01-requirements.md) → [维护收藏](modules/skills/favorites/01-requirements.md)。

| 功能 | 用户价值 | 来源覆盖 | 独立验收 |
|---|---|---|---|
| 搜索 | 快速找到可用技能 | INPUT-1 | 已有目录即可验证 |
| 收藏 | 回访并管理常用技能 | INPUT-2 | 已有详情即可验证 |

总览只定义公共约束与跨功能AC；每个叶子维护自己的规则和AC。搜索和收藏分别独立验收，组合闭环还要检查根AC-1，不因拆文件漏掉整体路径。

从标准仓库根执行：

```bash
python3 gates/run.py examples/requirements-tree --stage 01
```

内容自检通过不等于已冻结或可交付。`--delivery` 应拒绝此草稿示例；模块清单预留02/03修订1不代表对应阶段已完成。更多写法见[需求组织规则](../../policies/requirements-organization.md)。
