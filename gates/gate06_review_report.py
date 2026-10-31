"""阶段 06（下）：评审报告。"""

from __future__ import annotations

import re

import _lib

PRODUCT = "review-report"

SEVERITIES = {"严重": "严重（必须修）", "重要": "重要（应修）", "轻微": "轻微（可延后）"}


def check(ctx, art) -> bool | None:
    compliance = _compliance(ctx, art)
    findings = _findings(ctx, art)
    _security(ctx, art)
    _compat(ctx, art)
    conclusion = _conclusion(ctx, art, findings, compliance)
    _disagreement(ctx, art)
    del conclusion
    return False


def _compliance(ctx, art) -> str:
    sec = _lib.section_ok(ctx.issues, art, "规格符合性")
    if sec is None:
        return ""
    match = re.search(r"结论[:：]\s*(符合|不符合|无法判定)", sec.text)
    if not match:
        ctx.issue(art, sec.line, "规格符合性必须写明「符合 / 不符合 / 无法判定」")
        return ""
    return match.group(1)


def _findings(ctx, art) -> dict[str, str]:
    sec = art.section("发现")
    if sec is None:
        return {}
    blocks = {title: lines for _, title, lines in sec.blocks("")}
    found = {}
    for key in SEVERITIES:
        matches = [title for title in blocks if title.startswith(key)]
        if not matches:
            ctx.issue(art, sec.line, f"发现缺少三级标题：### {key}（如 {SEVERITIES[key]}）")
            continue
        text = _lib.block_text(blocks[matches[0]])
        if text and not _lib.only_none(text):
            for lineno, line in blocks[matches[0]]:
                if line.strip().startswith("-") and "`" not in line and ".ts" not in line and ".go" not in line and ".vue" not in line and ".py" not in line:
                    ctx.issue(art, lineno, "发现必须带 file:line 定位（用反引号包路径）")
                    break
        found[key] = text
    return found


def _security(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "安全性检查")
    if sec is None or _lib.is_section_na(sec):
        return
    for keyword in ("注入", "越权"):
        if keyword not in sec.text:
            ctx.issue(art, sec.first_line(), f"安全性检查必须覆盖「{keyword}」类问题")


def _compat(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "兼容性与迁移检查")
    if sec is None or _lib.is_section_na(sec):
        return
    if len(sec.text) < 8:
        ctx.issue(art, sec.first_line(), "兼容性与迁移检查过于简略")


def _conclusion(ctx, art, findings: dict[str, str], compliance: str) -> str:
    sec = _lib.section_ok(ctx.issues, art, "结论")
    if sec is None:
        return ""
    match = re.search(r"结论[:：]\s*(可合并|需修改)", sec.text)
    if not match:
        ctx.issue(art, sec.line, "结论必须写明「可合并」或「需修改」")
        return ""
    verdict = match.group(1)
    severe = findings.get("严重", "")
    important = findings.get("重要", "")
    has_blocker = bool(severe and not _lib.only_none(severe)) or bool(
        important and not _lib.only_none(important)
    )
    if verdict == "可合并" and has_blocker:
        ctx.issue(art, sec.line, "存在严重或重要发现，不能判定为可合并")
    if verdict == "可合并" and compliance == "不符合":
        ctx.issue(art, sec.line, "规格符合性为「不符合」，不能判定为可合并")
    if verdict == "需修改" and not has_blocker and compliance != "不符合":
        ctx.issue(art, sec.line, "判定为需修改，但严重/重要都没有问题、规格也符合；要写清依据")
    return verdict


def _disagreement(ctx, art) -> None:
    sec = _lib.section_ok(ctx.issues, art, "分歧记录")
    if sec is None:
        return
    if len(sec.text) < 4:
        ctx.issue(art, sec.first_line(), "分歧记录不能留空：没有就写 `无`，有则列出你主动不判定的部分")
