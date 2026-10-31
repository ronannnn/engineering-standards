"""阶段 04：开发计划。"""

from __future__ import annotations

import re

import _lib

PRODUCT = "tasks"

TASK_RE = re.compile(r"^任务\s*(\d+)")


def task_numbers(art) -> list[int]:
    sec = art.section("任务清单")
    if sec is None:
        return []
    numbers = []
    for line, title, _ in sec.blocks(""):
        match = TASK_RE.match(title)
        if match:
            numbers.append(int(match.group(1)))
    return numbers


def check(ctx, art) -> bool | None:
    _tasks(ctx, art)
    _milestones(ctx, art)
    _matrix(ctx, art)
    _risks(ctx, art)
    return False


def _tasks(ctx, art) -> None:
    sec = art.section("任务清单")
    if sec is None:
        return
    numbers = task_numbers(art)
    if not numbers:
        ctx.issue(art, sec.line, "任务清单至少写一个 `### 任务 1：<标题>`")
        return
    if numbers != list(range(1, len(numbers) + 1)):
        ctx.issue(art, sec.line, f"任务编号必须从 1 连续递增，当前为 {numbers}")
    for line, title, lines in sec.blocks(""):
        if not TASK_RE.match(title):
            continue
        text = _lib.block_text(lines)
        for field in ("文件", "依赖", "验收方法"):
            if f"{field}：" not in text and f"{field}:" not in text:
                ctx.issue(art, line, f"{title} 缺少「{field}」")
        if len(title) < 8:
            ctx.issue(art, line, f"{title} 标题过于简略（至少 8 个字，写清做什么）")
        mentioned = re.findall(r"`([^`]+)`", text)
        file_like = [m for m in mentioned if "/" in m or "." in m]
        if not file_like:
            ctx.issue(art, line, f"{title} 的「文件」没有给出具体路径")


def _milestones(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "里程碑与顺序")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "里程碑与顺序过于简略")


def _matrix(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "验证矩阵")
    if sec is None:
        return
    table = _lib.need_table(ctx.issues, art, sec, "验证矩阵", min_rows=1)
    if table is None:
        return
    _lib.rows_where_filled(ctx.issues, art, table, ["场景", "覆盖任务", "验证类型", "对应验收标准"], "验证矩阵")


def _risks(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "风险与回退")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "风险与回退过于简略")
