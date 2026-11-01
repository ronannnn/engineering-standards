"""阶段 05：编码实现（证据台账）。"""

from __future__ import annotations

import re

import _lib

PRODUCT = "implementation"

TASK_RE = re.compile(r"^任务\s*(\d+)")


def check(ctx, art) -> bool | None:
    _summary(ctx, art)
    _tasks(ctx, art)
    _files(ctx, art)
    _unfinished(ctx, art)
    return False


def _summary(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "实现摘要")
    if sec is None:
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "实现摘要过于简略：写清实际改动范围与额外发现")


def _tasks(ctx, art) -> None:
    sec = art.section("任务执行记录")
    if sec is None:
        return
    numbers = []
    blocks = []
    for line, title, lines in sec.blocks(""):
        match = TASK_RE.match(title)
        if match:
            numbers.append(int(match.group(1)))
            blocks.append((line, title, lines))
    if not blocks:
        ctx.issue(art, sec.line, "任务执行记录至少写一个 `### 任务 1：<标题>`")
        return

    plan = ctx.art("tasks")
    if plan is not None:
        planned = []
        plan_sec = plan.section("任务清单")
        if plan_sec is not None:
            for _, title, _ in plan_sec.blocks(""):
                match = TASK_RE.match(title)
                if match:
                    planned.append(int(match.group(1)))
        if planned and planned != numbers:
            ctx.issue(art, sec.line, f"实现记录的任务编号 {numbers} 与 04 开发计划 {planned} 不一致")

    for line, title, lines in blocks:
        text = _lib.block_text(lines)
        command = re.search(r"^-\s*测试命令[:：][ \t]*([^\n]*)$", text, re.M)
        if not command or not command.group(1).strip("` -"):
            ctx.issue(art, line, f"{title} 缺少「测试命令」")
        segments = {}
        # 每个顶层列表项都是边界；RED 不能读取 GREEN 或计划偏差的字段。
        items = list(re.finditer(r"^-\s+([^\n]+)", text, re.M))
        for i, item in enumerate(items):
            heading = re.split(r"[:：]", item.group(1), maxsplit=1)[0].strip()
            end = items[i + 1].start() if i + 1 < len(items) else len(text)
            if heading in segments:
                ctx.issue(art, line, f"{title} 重复的证据段：{heading}")
            segments[heading] = text[item.end():end]
        for phase in ("RED 证据", "GREEN 证据"):
            if phase not in segments:
                ctx.issue(art, line, f"{title} 缺少「{phase}」")
                continue
            for field in ("命令", "输出摘要"):
                values = re.findall(rf"^\s+-\s*{field}[:：][ \t]*([^\n]*)$", segments[phase], re.M)
                if len(values) != 1 or not values[0].strip("` -"):
                    ctx.issue(art, line, f"{title} 的 {phase} 缺少非空且唯一的{field}")


def _files(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "变更文件")
    if sec is None:
        return
    table = _lib.need_table(ctx.issues, art, sec, "变更文件", min_rows=1)
    if table is None:
        return
    _lib.rows_where_filled(ctx.issues, art, table, ["文件", "变更类型", "对应任务"], "变更文件")


def _unfinished(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "未完成项")
    if sec is None:
        return
    if not sec.text.strip():
        ctx.issue(art, sec.first_line(), "未完成项不能留空：没有就写 `无`")
