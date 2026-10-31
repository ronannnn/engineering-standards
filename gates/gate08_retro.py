"""阶段 08：维护与复盘。"""

from __future__ import annotations

import _lib

PRODUCT = "retro"

ALLOWED_TARGETS = (
    "skills/", "templates/", "gates/", "policies/", "adapters/",
    "scripts/", "AGENTS.md", "README.md", "CHANGELOG.md",
)


def check(ctx, art) -> bool | None:
    _comparison(ctx, art)
    _deviation(ctx, art)
    _rulings(ctx, art)
    _improvements(ctx, art)
    _actions(ctx, art)
    _signoff(ctx, art)
    return None  # 按需签收


def _comparison(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "结果对照")
    if sec is None:
        return
    table = _lib.need_table(ctx.issues, art, sec, "结果对照", min_rows=1)
    if table is None:
        return
    for col in ("目标", "实际结果", "差距"):
        if not any(col in header for header in table.header):
            ctx.issue(art, table.line, f"结果对照缺少「{col}」列（现有列：{table.header}）")


def _deviation(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "过程偏差")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 8:
        ctx.issue(art, sec.first_line(), "过程偏差过于简略：写返工、延误、门禁误报或漏报的具体事实")


def _rulings(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "决策与裁定清单")
    if sec is None or _lib.is_section_na(sec):
        return
    if _lib.only_none(sec.text):
        return
    _lib.need_table(ctx.issues, art, sec, "决策与裁定清单", min_rows=1)


def _improvements(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "标准改进项")
    if sec is None:
        return
    if _lib.only_none(sec.text):
        if "：" not in sec.text:
            ctx.issue(art, sec.first_line(), "标准改进项写「无」要说明理由：`无：<为什么这次流程完全适配>`")
        return
    table = _lib.need_table(ctx.issues, art, sec, "标准改进项", min_rows=1)
    if table is None:
        return
    rows = _lib.rows_where_filled(ctx.issues, art, table, ["目标文件", "现状", "建议改动", "优先级"], "标准改进项")
    for row in rows:
        target = table.cell(row, "目标文件").strip("` ")
        if not target.startswith(ALLOWED_TARGETS):
            ctx.issue(art, row.line, f"目标文件必须指向本仓库内的路径（{ALLOWED_TARGETS[0]}…），当前为 `{target}`")
        priority = table.cell(row, "优先级")
        if priority not in ("高", "中", "低"):
            ctx.issue(art, row.line, f"优先级只能填 高/中/低，当前为 `{priority}`")


def _actions(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "后续行动")
    if sec is None or _lib.is_section_na(sec):
        return
    if _lib.only_none(sec.text):
        return
    _lib.need_table(ctx.issues, art, sec, "后续行动", min_rows=1)


def _signoff(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "签收")
    if sec is None:
        return
    if len(sec.text) < 2:
        ctx.issue(art, sec.first_line(), "签收不能留空：写确认人与确认时间，或 `不适用：<理由>`")
