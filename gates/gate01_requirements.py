"""阶段 01：需求分析。"""

from __future__ import annotations

import re

import _lib

PRODUCT = "requirements"


def check(ctx, art) -> bool:
    issues = ctx.issues
    _background(ctx, art)
    _existing_system(ctx, art)
    _functional(ctx, art)
    _nonfunctional(ctx, art)
    _acceptance(ctx, art)
    _risks(ctx, art)
    return True  # 需求必须由人签收


def _background(ctx, art) -> None:
    sec = art.section("背景与目标")
    if sec is None or _lib.is_section_na(sec):
        return
    blocks = _lib.require_h3(ctx.issues, art, sec, ["问题", "目标", "非目标"])
    for title, lines in blocks.items():
        if title in ("问题", "目标") and _lib.only_none(_lib.block_text(lines)):
            ctx.issue(art, lines[0][0] if lines else sec.line, f"### {title} 不能只写「无」")


def _existing_system(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "现有系统分析")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 20:
        ctx.issue(art, sec.first_line(), "现有系统分析过于简略：存量项目要写清架构、依赖、可复用点与冲突点")


def _functional(ctx, art) -> None:
    sec = art.section("功能需求")
    if sec is None:
        return
    blocks = _lib.require_h3(ctx.issues, art, sec, [])
    reqs = [(line, title, lines) for line, title, lines in sec.blocks("") if re.match(r"^FR-\d+", title)]
    if not reqs:
        ctx.issue(art, sec.line, "功能需求：至少写一条 `### FR-1 <名称>`")
        return
    for line, title, lines in reqs:
        text = _lib.block_text(lines)
        if "描述" not in text or "优先级" not in text:
            ctx.issue(art, line, f"{title} 缺少「描述」或「优先级」")
        for keyword in ("Given", "When", "Then"):
            if keyword not in text:
                ctx.issue(art, line, f"{title} 的场景缺少 {keyword}")


def _nonfunctional(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "非功能需求")
    if sec is None or _lib.is_section_na(sec):
        return
    if not re.search(r"\d", sec.text):
        ctx.issue(art, sec.first_line(), "非功能需求缺少可判定指标（至少要有一个数字，例如 P95 < 300ms）")


def _acceptance(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "验收标准")
    if sec is None:
        return
    if _lib.is_section_na(sec):
        ctx.issue(art, sec.first_line(), "验收标准不允许整节不适用：没有验收标准的需求不可开工")
        return
    table = _lib.need_table(ctx.issues, art, sec, "验收标准", min_rows=1)
    if table is None:
        return
    rows = _lib.rows_where_filled(ctx.issues, art, table, ["编号", "对应需求", "判定方式", "可自动化"], "验收标准")
    seen = set()
    for row in rows:
        number = table.cell(row, "编号")
        if number in seen:
            ctx.issue(art, row.line, f"验收标准编号重复：{number}")
        seen.add(number)
        flag = table.cell(row, "可自动化")
        if flag not in ("是", "否"):
            ctx.issue(art, row.line, f"可自动化列只能填 是/否，当前为 `{flag}`")


def _risks(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "风险与开放问题")
    if sec is None or _lib.is_section_na(sec):
        return
    if sec.text.startswith("无") and len(sec.text) < 6:
        ctx.issue(art, sec.first_line(), "风险与开放问题写「无」时要给一句理由（`无未决问题：<理由>`）")
