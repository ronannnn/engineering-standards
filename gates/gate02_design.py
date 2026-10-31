"""阶段 02：技术设计。"""

from __future__ import annotations

import _lib

PRODUCT = "design"

IMPACT_LABELS = [
    "数据库 schema 变更",
    "权限模型变更",
    "跨模块接口变更",
    "新增第三方依赖",
    "性能基线变化",
]


def check(ctx, art) -> bool | None:
    issues = ctx.issues
    impacts = _impact(ctx, art)
    _architecture(ctx, art)
    interface_na = _interface(ctx, art)
    _data_model(ctx, art, schema_changed=impacts.get("数据库 schema 变更", False))
    _security(ctx, art)
    _compat(ctx, art)
    _perf_observability(ctx, art)
    _alternatives(ctx, art)
    _decision(ctx, art)
    _verification(ctx, art)
    del interface_na
    return True if any(impacts.values()) else False


def _impact(ctx, art) -> dict[str, bool]:
    sec = art.section("变更影响面")
    if sec is None:
        ctx.issue(art, 1, "缺少固定标题：## 变更影响面")
        return {}
    boxes = sec.checkboxes()
    labels = [label for _, label, _ in boxes]
    missing = [label for label in IMPACT_LABELS if label not in labels]
    if missing:
        ctx.issue(art, sec.line, f"变更影响面缺少勾选项：{missing}")
    return {label: checked for _, label, checked in boxes}


def _architecture(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "架构与模块")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 30:
        ctx.issue(art, sec.first_line(), "架构与模块过于简略：要写清涉及模块、职责、调用方向")


def _interface(ctx, art) -> bool:
    sec = _lib.section_ok(ctx.issues, art, "接口契约")
    if sec is None:
        return False
    if _lib.is_section_na(sec):
        return True
    _lib.need_table(ctx.issues, art, sec, "接口契约", min_rows=1)
    return False


def _data_model(ctx, art, schema_changed: bool) -> None:
    sec = _lib.section_ok(ctx.issues, art, "数据模型与迁移")
    if sec is None:
        return
    if _lib.is_section_na(sec):
        if schema_changed:
            ctx.issue(art, sec.first_line(), "勾选了「数据库 schema 变更」，数据模型与迁移不允许写不适用")
        return
    text = sec.text
    for keyword in ("迁移步骤", "回滚"):
        if keyword not in text:
            ctx.issue(art, sec.first_line(), f"数据模型与迁移缺少「{keyword}」")


def _security(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "安全与权限")
    if sec is None or _lib.is_section_na(sec):
        return
    for keyword in ("认证", "授权", "敏感数据"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"安全与权限必须覆盖「{keyword}」")


def _compat(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "兼容性")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "兼容性写得太简略：写清 API/客户端/schema/配置的兼容窗口")


def _perf_observability(ctx, art) -> None:
    for anchor in ("性能与容量", "可观测性"):
        sec = _lib.section_ok(ctx.issues, art, anchor)
        if sec is None or _lib.is_section_na(sec):
            continue
        if len(sec.text) < 10:
            ctx.issue(art, sec.first_line(), f"## {anchor} 过于简略")


def _alternatives(ctx, art) -> None:
    sec = art.section("备选方案")
    if sec is None:
        return
    if _lib.is_section_na(sec):
        ctx.issue(art, sec.first_line(), "备选方案不允许不适用：少于两个真实备选说明没想过别的做法")
        return
    plans = [t for _, t, _ in sec.blocks("") if t.startswith("方案")]
    if len(plans) < 2:
        ctx.issue(art, sec.line, f"备选方案至少两个（当前 {len(plans)} 个）")
    for _, title, lines in sec.blocks(""):
        if not title.startswith("方案"):
            continue
        if _lib.only_none(_lib.block_text(lines)):
            ctx.issue(art, sec.line, f"{title} 内容为空")
            continue
        for keyword in ("做法", "优点", "缺点", "为何未选"):
            if keyword not in _lib.block_text(lines):
                ctx.issue(art, sec.line, f"{title} 缺少「{keyword}」")


def _decision(ctx, art) -> None:
    sec = art.section("决策记录")
    if sec is None or _lib.is_section_na(sec):
        return
    _lib.need_table(ctx.issues, art, sec, "决策记录", min_rows=1)


def _verification(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "验证方式")
    if sec is None:
        return
    if _lib.is_section_na(sec):
        ctx.issue(art, sec.first_line(), "验证方式不允许不适用：设计必须说明如何被验证")
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "验证方式过于简略：写契约测试/迁移演练/压测/灰度对比等具体手段")
