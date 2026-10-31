#!/usr/bin/env python3
"""工程标准门禁入口。

用法：
    python3 gates/run.py <运行目录> --all
    python3 gates/run.py <运行目录> --stage 04
    python3 gates/run.py <运行目录> --next
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _lib  # noqa: E402
import spec  # noqa: E402

MODULE_BY_PRODUCT = {
    "requirements": "gate01_requirements",
    "design": "gate02_design",
    "ui-design": "gate03_ui_design",
    "tasks": "gate04_plan",
    "implementation": "gate05_implement",
    "test-report": "gate06_test_report",
    "review-report": "gate06_review_report",
    "delivery": "gate07_delivery",
    "retro": "gate08_retro",
}


class Context:
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self.artifacts: dict[str, _lib.Artifact] = {}
        self.issues: list[_lib.Issue] = []

    def art(self, product: str) -> _lib.Artifact | None:
        return self.artifacts.get(product)

    def issue(self, art: _lib.Artifact, line: int, message: str) -> None:
        self.issues.append(_lib.Issue(art.name, line, message))


def load(ctx: Context) -> None:
    for entry in spec.ARTIFACTS:
        art = _lib.check_file(ctx.issues, ctx.run_dir, entry)
        if art is not None:
            ctx.artifacts[entry["product"]] = art
    seen: dict[str, str] = {}
    for art in ctx.artifacts.values():
        number = art.fm.get("编号", "")
        if not number:
            continue
        if number in seen:
            ctx.issues.append(_lib.Issue(art.name, art.line_of("编号"),
                                         f"编号 {number} 与 {seen[number]} 重复"))
        else:
            seen[number] = art.name


def validate_artifact(ctx: Context, entry: dict) -> None:
    art = ctx.art(entry["product"])
    if art is None:
        return
    _lib.check_frontmatter(ctx.issues, art)
    _lib.check_dependency(ctx.issues, ctx.run_dir, entry, _by_name(ctx))

    if _lib.na_check(ctx.issues, art):
        _lib.check_status(ctx.issues, art, entry["signoff"] in ("human", "conditional"))
        return

    _lib.check_anchors(ctx.issues, art)
    module = importlib.import_module(MODULE_BY_PRODUCT[entry["product"]])
    human_required = module.check(ctx, art)
    _lib.check_status(ctx.issues, art, human_required)


def _by_name(ctx: Context) -> dict[str, _lib.Artifact]:
    return {art.name: art for art in ctx.artifacts.values()}


def check_all_frozen(ctx: Context, entries: list[dict]) -> None:
    for entry in entries:
        art = ctx.art(entry["product"])
        if art is None:
            continue
        status = art.status()
        if status == "已废弃":
            ctx.issues.append(_lib.Issue(art.name, art.line_of("状态"),
                                         "产物已废弃：本次运行应整体归档，不要继续推进"))
        elif status != "已冻结":
            ctx.issues.append(_lib.Issue(art.name, art.line_of("状态"),
                                         f"尚未冻结（当前 `{status or '未知'}`），全链校验要求 9 份产物全部冻结"))


def print_issues(issues: list[_lib.Issue], run_dir: Path) -> int:
    if not issues:
        print(f"✓ 全链通过：{run_dir}")
        return 0
    for issue in issues:
        print(issue)
    print(f"\n✗ 共 {len(issues)} 个问题")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="工程标准门禁")
    parser.add_argument("run_dir", help="运行目录，例如 docs/engineering/coupon-import")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="全链校验并要求全部冻结（默认）")
    group.add_argument("--stage", help="只校验某一段，例如 04")
    group.add_argument("--next", action="store_true", help="找出下一段未冻结的阶段并校验")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir)
    if not run_dir.is_dir():
        print(f"运行目录不存在：{run_dir}", file=sys.stderr)
        return 2

    entries = spec.ARTIFACTS
    if args.stage:
        code = args.stage.zfill(2)
        entries = [e for e in spec.ARTIFACTS if e["code"] == code]
        if not entries:
            print(f"未知阶段：{args.stage}", file=sys.stderr)
            return 2

    ctx = Context(run_dir)
    load(ctx)

    if args.next:
        pending = None
        for entry in spec.ARTIFACTS:
            art = ctx.art(entry["product"])
            if art is None or art.status() != "已冻结":
                pending = entry
                break
        if pending is None:
            print("✓ 8 个阶段全部冻结，没有待办")
            return 0
        print(f"→ 下一步：{pending['code']} {spec.STAGE_TITLES[pending['code']]}（{pending['file']}）")
        entries = [e for e in spec.ARTIFACTS if e["code"] == pending["code"]]

    for entry in entries:
        validate_artifact(ctx, entry)

    if not args.stage and not args.next:
        check_all_frozen(ctx, spec.ARTIFACTS)

    return print_issues(ctx.issues, run_dir)


if __name__ == "__main__":
    raise SystemExit(main())
