"""阶段 06（上）：测试报告。"""

from __future__ import annotations

import re

import _lib

PRODUCT = "test-report"

RESULT_VALUES = ("通过", "失败")
TYPE_VALUES = ("单元", "集成", "e2e", "手工")


def check(ctx, art) -> bool | None:
    failures = _cases(ctx, art)
    _failures(ctx, art, failures)
    _coverage(ctx, art)
    _matrix(ctx, art)
    _uncovered(ctx, art)
    _conclusion(ctx, art, failures)
    return False


def _cases(ctx, art) -> list:
    sec = _lib.section_ok(ctx.issues, art, "用例与结果")
    if sec is None:
        return []
    table = _lib.need_table(ctx.issues, art, sec, "用例与结果", min_rows=1)
    if table is None:
        return []
    rows = _lib.rows_where_filled(
        ctx.issues, art, table, ["编号", "对应验收标准", "类型", "命令", "结果", "证据"], "用例与结果"
    )
    failures = []
    for row in rows:
        result = table.cell(row, "结果")
        if result not in RESULT_VALUES:
            ctx.issue(art, row.line, f"结果列只能填 通过/失败，当前为 `{result}`")
        if result == "失败":
            failures.append(row)
        kind = table.cell(row, "类型")
        if kind not in TYPE_VALUES:
            ctx.issue(art, row.line, f"类型列只能填 {TYPE_VALUES}，当前为 `{kind}`")
    return failures


def _failures(ctx, art, failures: list) -> None:
    sec = _lib.section_ok(ctx.issues, art, "失败与修复")
    if sec is None:
        return
    if not failures:
        return
    table = sec.tables()[0] if sec.tables() else None
    if table is None:
        ctx.issue(art, sec.line, "存在失败用例，但「失败与修复」没有表格")
        return
    if len(table.rows) < len(failures):
        ctx.issue(art, table.line, f"失败用例 {len(failures)} 个，失败与修复只记录了 {len(table.rows)} 行")
    for row in table.rows:
        if table.cell(row, "复验结果") != "通过":
            ctx.issue(art, row.line, "失败用例必须有复验，且复验结果填「通过」")


def _coverage(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "覆盖率")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 10:
        ctx.issue(art, sec.first_line(), "覆盖率过于简略：给出命令与数值，或说明覆盖盲区")


def _matrix(ctx, art) -> dict[str, str]:
    sec = _lib.section_ok(ctx.issues, art, "矩阵审计")
    if sec is None:
        return {}
    table = _lib.need_table(ctx.issues, art, sec, "矩阵审计", min_rows=1)
    if table is None:
        return {}
    mapping = {}
    for row in table.rows:
        ac = table.cell(row, "验收标准")
        flag = table.cell(row, "是否有已执行用例")
        if not ac:
            continue
        mapping[ac] = flag
        if flag not in ("是", "否"):
            ctx.issue(art, row.line, f"「是否有已执行用例」只能填 是/否，当前为 `{flag}`")
        elif flag == "否":
            ctx.issue(art, row.line, f"验收标准 {ac} 没有已执行的用例（跳过不算覆盖）")

    requirements = ctx.art("requirements")
    if requirements is None:
        return mapping
    req_sec = requirements.section("验收标准")
    if req_sec is None or not req_sec.tables():
        return mapping
    for row in req_sec.tables()[0].rows:
        ac = req_sec.tables()[0].cell(row, "编号")
        if not ac:
            continue
        if ac not in mapping:
            ctx.issue(art, sec.line, f"矩阵审计缺少验收标准 {ac}（来自 01 需求）")
    return mapping


def _uncovered(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "未覆盖与风险")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 5:
        ctx.issue(art, sec.first_line(), "未覆盖与风险过于简略：写清跳过原因与可能影响")


def _conclusion(ctx, art, failures: list) -> None:
    sec = _lib.section_ok(ctx.issues, art, "结论")
    if sec is None:
        return
    match = re.search(r"结论[:：]\s*(可发布|不可发布)", sec.text)
    if not match:
        ctx.issue(art, sec.line, "结论必须写明「可发布」或「不可发布」")
        return
    if match.group(1) == "可发布" and failures:
        ctx.issue(art, sec.line, f"存在 {len(failures)} 个失败用例，不能判定为可发布")
