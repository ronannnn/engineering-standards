"""阶段 03：UI/UX 设计。"""

from __future__ import annotations

import _lib

PRODUCT = "ui-design"

STATE_LABELS = ["空状态", "加载状态", "错误状态", "无权限状态", "成功反馈", "危险操作确认"]


def check(ctx, art) -> bool | None:
    key_page = _pages(ctx, art)
    _flow(ctx, art)
    _states(ctx, art)
    _a11y(ctx, art)
    _visual_acceptance(ctx, art)
    _handoff(ctx, art)
    return key_page


def _pages(ctx, art) -> bool:
    sec = _lib.section_ok(ctx.issues, art, "页面清单")
    if sec is None:
        return False
    table = _lib.need_table(ctx.issues, art, sec, "页面清单", min_rows=1)
    if table is None:
        return False
    for col in ("页面", "关键", "复用组件"):
        if col not in table.header:
            ctx.issue(art, table.line, f"## 页面清单 表格缺少列：`{col}`（现有列：{table.header}）")
            return False
    has_key = False
    for row in table.rows:
        flag = table.cell(row, "关键")
        if flag not in ("是", "否"):
            ctx.issue(art, row.line, f"「关键」列只能填 是/否，当前为 `{flag}`")
            continue
        if flag == "是":
            has_key = True
        if not table.cell(row, "复用组件"):
            ctx.issue(art, row.line, "「复用组件」不能为空：要么写现有组件，要么写 `新增：<组件名>`")
    return has_key


def _flow(ctx, art) -> None:
    for anchor, minimum in (("关键流程", 20), ("设计系统与复用", 20), ("布局与响应式", 10), ("交付说明", 10)):
        sec = _lib.section_ok(ctx.issues, art, anchor)
        if sec is None or _lib.is_section_na(sec):
            continue
        if len(sec.text) < minimum:
            ctx.issue(art, sec.first_line(), f"## {anchor} 过于简略（少于 {minimum} 字）")


def _states(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "交互与状态")
    if sec is None:
        return
    missing = [label for label in STATE_LABELS if label not in sec.text]
    if missing:
        ctx.issue(art, sec.line, f"交互与状态缺少：{missing}")
    for label in STATE_LABELS:
        for lineno, text in sec.lines:
            if label in text and text.split(label, 1)[1].strip(" ：:") == "":
                ctx.issue(art, lineno, f"「{label}」没有写出具体表现")


def _a11y(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "可访问性")
    if sec is None or _lib.is_section_na(sec):
        return
    for keyword in ("键盘", "对比度"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"可访问性必须覆盖「{keyword}」")


def _visual_acceptance(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "视觉验收标准")
    if sec is None:
        return
    _lib.need_table(ctx.issues, art, sec, "视觉验收标准", min_rows=1)


def _handoff(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "交付说明")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "交付说明过于简略：写清组件/token/文案/资源位置")
