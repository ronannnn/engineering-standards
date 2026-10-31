"""阶段 07：集成与交付。"""

from __future__ import annotations

import re

import _lib
import spec

PRODUCT = "delivery"

AI_ROWS = ["需求拆解", "方案设计", "验收测试", "技术实现", "评审处理"]


def check(ctx, art) -> bool | None:
    _changes(ctx, art)
    _ci(ctx, art)
    _deploy(ctx, art)
    _rollback(ctx, art)
    _monitoring(ctx, art)
    _ai_usage(ctx, art)
    _confirm(ctx, art)
    _upstream_verdicts(ctx, art)
    return True  # 交付必须由人签收


def _changes(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "变更清单")
    if sec is None:
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "变更清单过于简略：逐条列出功能、修复、配置、数据、依赖变更")


def _ci(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "CI 检查结果")
    if sec is None:
        return
    table = _lib.need_table(ctx.issues, art, sec, "CI 检查结果", min_rows=1)
    if table is None:
        return
    rows = _lib.rows_where_filled(ctx.issues, art, table, ["检查项", "结果", "证据"], "CI 检查结果")
    names = [table.cell(row, "检查项") for row in rows]
    if "标准门禁" not in names:
        ctx.issue(art, table.line, "CI 检查结果必须包含一行「标准门禁」（本次门禁的结论）")
    for row in rows:
        result = table.cell(row, "结果")
        if result not in ("通过", "失败", "跳过"):
            ctx.issue(art, row.line, f"结果列只能填 通过/失败/跳过，当前为 `{result}`")
        elif result == "通过" and not table.cell(row, "证据"):
            ctx.issue(art, row.line, "结果为通过时必须有证据（日志或链接）")
    gate_rows = [row for row in rows if table.cell(row, "检查项") == "标准门禁"]
    if gate_rows and table.cell(gate_rows[0], "结果") != "通过":
        ctx.issue(art, gate_rows[0].line, "标准门禁未通过，不能交付")


def _deploy(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "部署方案")
    if sec is None:
        return
    for keyword in ("步骤", "负责人"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"部署方案缺少「{keyword}」")


def _rollback(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "回滚方案")
    if sec is None:
        return
    for keyword in ("触发条件", "步骤", "预估耗时"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"回滚方案缺少「{keyword}」")


def _monitoring(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "健康检查与监控")
    if sec is None:
        return
    for keyword in ("健康检查", "关键指标", "观察窗口"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"健康检查与监控缺少「{keyword}」")


def _ai_usage(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "AI 参与度")
    if sec is None:
        return
    table = _lib.need_table(ctx.issues, art, sec, "AI 参与度", min_rows=5)
    if table is None:
        return
    for col in ("环节", "等级", "说明"):
        if col not in table.header:
            ctx.issue(art, table.line, f"AI 参与度表格缺少列：`{col}`")
            return
    seen = []
    for row in table.rows:
        item = table.cell(row, "环节")
        level = table.cell(row, "等级")
        note = table.cell(row, "说明")
        seen.append(item)
        if level not in spec.AI_LEVELS:
            ctx.issue(art, row.line, f"等级只能填 {list(spec.AI_LEVELS)}，当前为 `{level}`")
        if level != "不适用" and len(note) < 2:
            ctx.issue(art, row.line, f"{item} 的说明不能为空（写清人做了什么、AI 做了什么）")
    missing = [item for item in AI_ROWS if item not in seen]
    if missing:
        ctx.issue(art, table.line, f"AI 参与度缺少环节：{missing}")


def _confirm(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "交付确认")
    if sec is None:
        return
    for field in ("验收人", "确认时间"):
        match = re.search(rf"{field}[:：]\s*(\S+)", sec.text)
        if not match or match.group(1) in ("-", "无"):
            ctx.issue(art, sec.first_line(), f"交付确认缺少「{field}」")
    date = re.search(r"确认时间[:：]\s*(\S+)", sec.text)
    if date and not _lib.DATE_RE.match(date.group(1)):
        ctx.issue(art, sec.first_line(), f"确认时间必须是 YYYY-MM-DD，当前为 `{date.group(1)}`")


def _upstream_verdicts(ctx, art) -> None:
    tests = ctx.art("test-report")
    if tests is not None and tests.status() == "已冻结":
        sec = tests.section("结论")
        if sec is not None and "不可发布" in sec.text:
            ctx.issue(art, art.section("交付确认").line if art.section("交付确认") else 1,
                      "06 测试报告结论为「不可发布」，不能进入交付")
    review = ctx.art("review-report")
    if review is not None and review.status() == "已冻结":
        sec = review.section("结论")
        if sec is not None and "需修改" in sec.text:
            ctx.issue(art, art.section("交付确认").line if art.section("交付确认") else 1,
                      "06 评审报告结论为「需修改」，不能进入交付")
