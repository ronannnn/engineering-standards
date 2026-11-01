#!/usr/bin/env python3
"""工程标准门禁：阶段自检、合并前检查、完整归档与下一步。"""

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
    "requirements": "gate01_requirements", "design": "gate02_design",
    "ui-design": "gate03_ui_design", "tasks": "gate04_plan",
    "implementation": "gate05_implement", "test-report": "gate06_test_report",
    "review-report": "gate06_review_report", "delivery": "gate07_delivery",
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


def dependency_scope(entries: list[dict]) -> list[dict]:
    """展开注册表依赖，按阶段原顺序返回，未来阶段不参与当前自检。"""
    by_name = {e["file"]: e for e in spec.ARTIFACTS}
    needed = set()

    def visit(entry):
        if entry["file"] in needed:
            return
        needed.add(entry["file"])
        for name in spec.dependencies(entry):
            visit(by_name[name])

    for entry in entries:
        visit(entry)
    return [e for e in spec.ARTIFACTS if e["file"] in needed]


def load(ctx: Context, entries: list[dict] | None = None) -> None:
    for entry in entries if entries is not None else spec.ARTIFACTS:
        art = _lib.check_file(ctx.issues, ctx.run_dir, entry)
        if art is not None:
            ctx.artifacts[entry["product"]] = art
    seen = {}
    for art in ctx.artifacts.values():
        number = art.fm.get("编号", "")
        if number and number in seen:
            ctx.issue(art, art.line_of("编号"), f"编号 {number} 与 {seen[number]} 重复")
        seen[number] = art.name


def validate_artifact(ctx: Context, entry: dict) -> None:
    art = ctx.art(entry["product"])
    if art is None:
        return
    _lib.check_frontmatter(ctx.issues, art)
    if art.fm_error:
        return
    _lib.check_dependency(ctx.issues, ctx.run_dir, entry, _by_name(ctx))
    if _lib.na_check(ctx.issues, art):
        _lib.check_status(ctx.issues, art, True)
        return
    _lib.check_anchors(ctx.issues, art)
    module = importlib.import_module(MODULE_BY_PRODUCT[entry["product"]])
    _lib.check_status(ctx.issues, art, module.check(ctx, art))


def _by_name(ctx: Context) -> dict[str, _lib.Artifact]:
    return {**{art.path.name: art for art in ctx.artifacts.values()},
            **getattr(ctx, 'external_dependencies', {})}


def check_all_frozen(ctx: Context, entries: list[dict]) -> None:
    for entry in entries:
        art = ctx.art(entry["product"])
        if art is None:
            continue
        if art.status() == "已废弃":
            ctx.issue(art, art.line_of("状态"), "产物已废弃：本次运行应整体归档，不要继续推进")
        elif art.status() != "已冻结":
            ctx.issue(art, art.line_of("状态"), f"尚未冻结（当前 `{art.status() or '未知'}`），所选范围要求全部冻结")


def print_issues(issues: list[_lib.Issue], run_dir: Path, label="全链") -> int:
    if not issues:
        print(f"✓ {label}通过：{run_dir}")
        return 0
    for issue in issues:
        print(issue)
    print(f"\n✗ 共 {len(issues)} 个问题")
    return 1


def next_stage(run_dir: Path) -> int:
    # 按阶段验证有效性，遇到第一个未完成或不合法的阶段即返回。
    # 未开始的后续阶段不读取，不能让未来草稿阻塞当前阶段。
    ctx = Context(run_dir)
    validated = set()
    for code in dict.fromkeys(e["code"] for e in spec.ARTIFACTS):
        entries = spec.by_code(code)
        scope = dependency_scope(entries)
        load(ctx, [e for e in scope if e["product"] not in ctx.artifacts])
        for entry in scope:
            if entry["product"] not in validated:
                validate_artifact(ctx, entry)
                validated.add(entry["product"])
        pending = ctx.issues or any(ctx.art(e["product"]) is None or
                                   ctx.art(e["product"]).status() != "已冻结" for e in entries)
        if pending:
            print(f"→ 下一步：{code} {spec.STAGE_TITLES[code]}（完成内容校验与冻结）")
            return print_issues(ctx.issues, run_dir, f"阶段 {code} 自检")
    print("✓ 8 个阶段全部冻结且校验有效，没有待办")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="工程标准门禁")
    parser.add_argument("run_dir", help="运行目录")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="完整归档：九份产物全部冻结（默认）")
    group.add_argument("--delivery", action="store_true", help="合并前：01–07 全部冻结，不要求 08")
    group.add_argument("--stage", help="当前阶段内容及上游依赖校验，不要求未来阶段存在")
    group.add_argument("--next", action="store_true", help="找出第一个未完成或校验无效的阶段")
    parser.add_argument("--module", help="模块路径或目录组，配合 --stage/--next 使用")
    args = parser.parse_args(argv)
    run_dir = Path(args.run_dir)
    if not run_dir.is_dir():
        print(f"运行目录不存在：{run_dir}", file=sys.stderr)
        return 2
    import modular
    if args.module or modular.enabled(run_dir):
        return modular.main(run_dir, args, sys.modules[__name__])
    if args.next:
        return next_stage(run_dir)
    entries = spec.ARTIFACTS
    label = "全链"
    if args.stage:
        entries = spec.by_code(args.stage.zfill(2))
        label = f"阶段 {args.stage.zfill(2)} 自检"
        if not entries:
            print(f"未知阶段：{args.stage}", file=sys.stderr)
            return 2
    elif args.delivery:
        entries = [e for e in spec.ARTIFACTS if e["code"] in spec.DELIVERY_CODES]
        label = "合并前检查"
    scope = dependency_scope(entries)
    ctx = Context(run_dir)
    load(ctx, scope)
    for entry in scope:
        validate_artifact(ctx, entry)
    if args.stage:
        upstream = [e for e in scope if e not in entries]
        check_all_frozen(ctx, upstream)
    else:
        check_all_frozen(ctx, scope)
    return print_issues(ctx.issues, run_dir, label)


if __name__ == "__main__":
    raise SystemExit(main())
