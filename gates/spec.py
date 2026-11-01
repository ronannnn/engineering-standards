"""阶段与产物规格：本仓库唯一的流程定义源。

改这里必须同步改 templates/ 与对应 skills/（AGENTS.md §8 三处同源）。
"""

from __future__ import annotations

ANCHORS = {
    "requirements": [
        "背景与目标", "现有系统分析", "术语", "功能需求", "非功能需求",
        "验收标准", "范围外", "依赖与假设", "风险与开放问题", "签署",
    ],
    "design": [
        "方案概述", "变更影响面", "架构与模块", "接口契约", "数据模型与迁移",
        "安全与权限", "兼容性", "性能与容量", "可观测性", "备选方案",
        "决策记录", "验证方式",
    ],
    "ui-design": [
        "页面清单", "关键流程", "设计系统与复用", "布局与响应式",
        "交互与状态", "可访问性", "视觉验收标准", "交付说明",
    ],
    "tasks": ["任务清单", "里程碑与顺序", "验证矩阵", "风险与回退"],
    "implementation": ["实现摘要", "任务执行记录", "变更文件", "未完成项"],
    "test-report": [
        "测试范围", "环境与版本", "用例与结果", "失败与修复",
        "覆盖率", "矩阵审计", "未覆盖与风险", "结论",
    ],
    "review-report": [
        "评审范围", "规格符合性", "发现", "安全性检查",
        "兼容性与迁移检查", "结论", "分歧记录",
    ],
    "delivery": [
        "变更清单", "CI 检查结果", "部署方案", "回滚方案",
        "健康检查与监控", "AI 参与度", "交付确认", "遗留与后续",
    ],
    "retro": ["结果对照", "过程偏差", "决策与裁定清单", "标准改进项", "后续行动", "签收"],
}

# signoff: "human" 必须人签收；"conditional" 条件触发后人签收；"auto" 可机器签收
ARTIFACTS = [
    dict(code="01", title="需求分析", product="requirements", file="01-requirements.md",
         prefix="REQ", depends=None, signoff="human", na_allowed=True, gate="gate01_requirements"),
    dict(code="02", title="技术设计", product="design", file="02-design.md",
         prefix="DES", depends="01-requirements.md", signoff="conditional", na_allowed=True, gate="gate02_design"),
    dict(code="03", title="UI/UX 设计", product="ui-design", file="03-ui-design.md",
         prefix="UIX", depends="02-design.md", signoff="conditional", na_allowed=True, gate="gate03_ui_design"),
    dict(code="04", title="开发计划", product="tasks", file="04-tasks.md",
         prefix="TSK", depends="03-ui-design.md", signoff="auto", na_allowed=False, gate="gate04_plan"),
    dict(code="05", title="编码实现", product="implementation", file="05-implementation.md",
         prefix="IMP", depends="04-tasks.md", signoff="auto", na_allowed=False, gate="gate05_implement"),
    dict(code="06", title="测试与评审", product="test-report", file="06-test-report.md",
         prefix="TST", depends="05-implementation.md", signoff="auto", na_allowed=False, gate="gate06_test_report"),
    dict(code="06", title="测试与评审", product="review-report", file="06-review-report.md",
         prefix="REV", depends="05-implementation.md", signoff="auto", na_allowed=False, gate="gate06_review_report"),
    dict(code="07", title="集成与交付", product="delivery", file="07-delivery.md",
         prefix="DLV", depends="06-test-report.md", also_depends=("06-review-report.md",),
         signoff="human", na_allowed=False, gate="gate07_delivery"),
    dict(code="08", title="维护与复盘", product="retro", file="08-retro.md",
         prefix="RTR", depends="07-delivery.md", signoff="auto", na_allowed=True, gate="gate08_retro"),
]

STAGE_TITLES = {
    "01": "需求分析", "02": "技术设计", "03": "UI/UX设计", "04": "开发计划",
    "05": "编码实现", "06": "测试与评审", "07": "集成与交付", "08": "维护与复盘",
}

STATUSES = ("草稿", "待签收", "已冻结", "已废弃")
SIGNOFF_MACHINE = "机器门禁"
DELIVERY_CODES = ("01", "02", "03", "04", "05", "06", "07")
MODULE_CODES = ("01", "02", "03", "04", "05", "06", "08")
COMMON_CODES = ("01", "02", "03")
REQUIRED_CI_CHECKS = ("单元测试", "构建", "静态检查", "安全扫描", "标准门禁")
AI_LEVELS = ("人工独立", "人工主导", "人工引导", "人工把关", "模型自主", "不适用")


def by_product(product: str) -> dict:
    for art in ARTIFACTS:
        if art["product"] == product:
            return art
    raise KeyError(product)


def by_code(code: str) -> list[dict]:
    return [a for a in ARTIFACTS if a["code"] == code]


def dependencies(entry: dict) -> tuple[str, ...]:
    primary = (entry["depends"],) if entry["depends"] else ()
    return primary + tuple(entry.get("also_depends", ()))
