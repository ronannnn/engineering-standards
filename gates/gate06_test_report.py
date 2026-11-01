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
    seen = set()
    for row in rows:
        number = table.cell(row, "编号")
        if number in seen:
            ctx.issue(art, row.line, f"用例编号重复：{number}")
        seen.add(number)
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
    rows = _lib.rows_where_filled(ctx.issues, art, table,
                                  ["用例", "失败原因", "修复方式", "复验结果"], "失败与修复")
    for row in rows:
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
    rows = _lib.rows_where_filled(ctx.issues, art, table,
                                  ["验收标准", "是否有已执行用例", "依据用例"], "矩阵审计")
    case_sec = art.section("用例与结果")
    case_table = case_sec.tables()[0] if case_sec and case_sec.tables() else None
    cases = dict(getattr(ctx, 'external_cases', {}))
    if case_table:
        cases.update({case_table.cell(r, "编号"): {
            'result': case_table.cell(r, '结果'),
            'acs': set(split_refs(case_table.cell(r, '对应验收标准'))),
        } for r in case_table.rows})
    for row in rows:
        ac = table.cell(row, "验收标准")
        flag = table.cell(row, "是否有已执行用例")
        if ac in mapping:
            ctx.issue(art, row.line, f"矩阵审计验收标准重复：{ac}")
        mapping[ac] = flag
        if flag not in ("是", "否"):
            ctx.issue(art, row.line, f"「是否有已执行用例」只能填 是/否，当前为 `{flag}`")
        elif flag == "否":
            ctx.issue(art, row.line, f"验收标准 {ac} 没有已执行的用例（跳过不算覆盖）")
        references = split_refs(table.cell(row, "依据用例"))
        if not references:
            ctx.issue(art, row.line, f"{ac} 没有有效的依据用例编号")
        for number in references:
            case = cases.get(number)
            if case is None:
                ctx.issue(art, row.line, f"{ac} 引用的用例不存在：{number}")
            elif case['result'] != "通过":
                ctx.issue(art, row.line, f"{ac} 的依据用例 {number} 未通过")
            elif ac not in case['acs']:
                ctx.issue(art, row.line, f"依据用例 {number} 没有覆盖 {ac}")

    requirements = ctx.art("requirements")
    if requirements is None or (requirements.is_na() and not getattr(ctx, 'acceptance_ids', set())):
        return mapping
    req_sec = requirements.section("验收标准")
    if not hasattr(ctx, 'acceptance_ids') and (req_sec is None or not req_sec.tables()):
        return mapping
    known = ctx.acceptance_ids if hasattr(ctx, 'acceptance_ids') else {
        req_sec.tables()[0].cell(row, '编号') for row in req_sec.tables()[0].rows
        if req_sec.tables()[0].cell(row, '编号')
    }
    for ac in known:
        if ac not in mapping:
            ctx.issue(art, sec.line, f"矩阵审计缺少验收标准 {ac}（来自 01 需求）")
    for ac in mapping.keys() - known:
        ctx.issue(art, sec.line, f"矩阵审计引用未知验收标准：{ac}")
    return mapping


def split_refs(value: str) -> list[str]:
    return [v.strip("` ") for v in re.split(r"[、,，;；\s]+", value) if v.strip("` ")]


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
    value = _lib.verdict(art, "结论", ("可发布", "不可发布"))
    if value is None:
        ctx.issue(art, sec.line, "结论必须写明「可发布」或「不可发布」")
        return
    if value == "可发布" and failures:
        ctx.issue(art, sec.line, f"存在 {len(failures)} 个失败用例，不能判定为可发布")
