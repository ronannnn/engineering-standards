"""可选模块树：目录登记、公共基线、限定引用和统一交付。仅标准库。"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re

import _lib
import spec

PATH_RE = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*')
ARTIFACT_NAMES = {e['file'] for e in spec.ARTIFACTS}


def safe_path(value):
    return isinstance(value, str) and PATH_RE.fullmatch(value) is not None


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'JSON 字段重复：{key}')
        result[key] = value
    return result


@dataclass
class Registry:
    root: Path
    modules: dict

    @classmethod
    def load(cls, root: Path, issues: list):
        manifest = root / 'modules.json'
        def error(message, line=1):
            issues.append(_lib.Issue('modules.json', line, message))
        if not manifest.is_file():
            error('模块产物必须在 modules.json 登记')
            return None
        try:
            data = json.loads(manifest.read_text(encoding='utf-8'), object_pairs_hook=_unique_object)
        except (OSError, UnicodeError, ValueError) as exc:
            error(f'无法读取模块清单：{exc}', getattr(exc, 'lineno', 1))
            return None
        if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
            error('清单必须是 version 为 1 的 JSON 对象')
            return None
        if set(data) - {'version', 'modules'}:
            error('清单存在未知字段')
        entries = data.get('modules')
        if not isinstance(entries, list) or not entries:
            error('modules 必须是非空列表')
            return None
        modules = {}
        resolved_paths = set()
        base = (root / 'modules').resolve()
        if not base.is_relative_to(root.resolve()):
            error('modules 路径不能指向运行目录之外')
            return None
        for item in entries:
            if not isinstance(item, dict) or not safe_path(item.get('path')):
                error('模块 path 必须是安全的多层 kebab-case 相对路径')
                continue
            name = item['path']
            if name in modules:
                error(f'模块重复登记：{name}')
                continue
            if set(item) - {'path', 'name', 'depends_on', 'baseline'}:
                error(f'{name} 存在未知模块字段')
            target = root / 'modules' / name
            if not target.resolve().is_relative_to(base):
                error(f'{name} 模块路径越界')
                continue
            if not target.is_dir():
                error(f'{name} 模块目录不存在')
            if target.resolve() in resolved_paths:
                error(f'{name} 模块路径与其他模块指向同一目录')
            resolved_paths.add(target.resolve())
            deps = item.get('depends_on', [])
            if not isinstance(deps, list) or any(not safe_path(d) for d in deps):
                error(f'{name} depends_on 必须是模块路径列表')
                deps = []
            if len(deps) != len(set(deps)):
                error(f'{name} 依赖模块重复')
            baseline = item.get('baseline')
            if not isinstance(baseline, dict) or set(baseline) != set(spec.COMMON_CODES) or any(
                type(v) is not int or v < 1 for v in baseline.values()
            ):
                error(f'{name} baseline 必须包含 01、02、03 的正整数修订')
            modules[name] = {**item, 'depends_on': deps}
        for name, item in modules.items():
            for dep in item['depends_on']:
                if dep not in modules:
                    error(f'{name} 引用未知依赖模块：{dep}')
        registry = cls(root, modules)
        if not issues:
            try:
                registry.order(set(modules))
            except ValueError as exc:
                error(str(exc))
        # 只扫描产物路径，未来阶段的正文不会提前读取。
        for path in (root / 'modules').rglob('*.md'):
            if path.name not in ARTIFACT_NAMES:
                continue
            name = path.parent.relative_to(root / 'modules').as_posix()
            if name not in modules:
                error(f'未登记的模块产物：{path.relative_to(root).as_posix()}')
            elif path.name == '07-delivery.md':
                error(f'{name} 不应单独放 07，统一交付记录位于根目录')
        return registry

    def order(self, selected):
        done, visiting, result = set(), set(), []
        def visit(name):
            if name in visiting:
                raise ValueError(f'模块依赖存在循环：{name}')
            if name in done:
                return
            visiting.add(name)
            for dep in self.modules[name]['depends_on']:
                visit(dep)
            visiting.remove(name)
            done.add(name)
            result.append(name)
        for name in sorted(selected):
            visit(name)
        return result

    def select(self, value):
        if value is None:
            return set(self.modules)
        if not safe_path(value):
            return set()
        return {name for name in self.modules if name == value or name.startswith(value + '/')}


def enabled(root):
    return (root / 'modules.json').exists() or any(
        p.name in ARTIFACT_NAMES for p in (root / 'modules').rglob('*.md'))


def acceptance(art):
    if art is None or art.is_na():
        return set()
    sec = art.section('验收标准')
    if not sec or not sec.tables():
        return set()
    table = sec.tables()[0]
    return {table.cell(r, '编号') for r in table.rows if table.cell(r, '编号')}


def tasks(art):
    if art is None:
        return set()
    import gate04_plan
    return {f'任务 {n}' for n in gate04_plan.task_numbers(art)}


def cases(ctx, namespace):
    art = ctx.art('test-report')
    sec = art.section('用例与结果') if art else None
    if not sec or not sec.tables():
        return {}
    import gate06_test_report
    table = sec.tables()[0]
    return {namespace + '#' + table.cell(row, '编号'): {
        'result': table.cell(row, '结果'),
        'acs': {namespace + '#' + ac for ac in gate06_test_report.split_refs(table.cell(row, '对应验收标准'))},
    } for row in table.rows}


def _module_entries(folder, root, code):
    entries = [dict(e) for e in spec.ARTIFACTS if e['code'] in spec.MODULE_CODES and e['code'] <= code]
    for entry in entries:
        if entry['code'] == '08':
            entry['depends'] = Path(os.path.relpath(root / '07-delivery.md', folder)).as_posix()
    return entries


def validate(root, registry, code, gate, selector=None, require_frozen=False):
    selected = registry.select(selector)
    if not selected:
        return [_lib.Issue('modules.json', 1, f'没有匹配的模块：{selector}')], False
    selected = set(registry.order(selected))
    # 模块 08 依赖统一发布；检验根 07 时必须核对整次发布。
    names = registry.order(set(registry.modules) if selector and code == '08' else selected)
    root_entries = [e for e in spec.ARTIFACTS if e['code'] <= code]
    if selector:
        root_entries = [e for e in root_entries if e['code'] in spec.COMMON_CODES or (code == '08' and e['code'] <= '07')]
    root_ctx = gate.Context(root)
    gate.load(root_ctx, root_entries)
    contexts, scopes = {}, {}
    for name in names:
        folder = root / 'modules' / name
        local_code = '06' if code == '07' or (code == '08' and name not in selected) else code
        scope = _module_entries(folder, root, local_code)
        ctx = gate.Context(folder)
        # 拒绝通过文件符号链接读取模块树以外的文档。
        safe_scope = []
        for entry in scope:
            if not (folder / entry['file']).resolve().is_relative_to((root / 'modules').resolve()):
                ctx.issues.append(_lib.Issue(entry['file'], 1, '产物路径越界'))
            else:
                safe_scope.append(entry)
        gate.load(ctx, safe_scope)
        for art in ctx.artifacts.values():
            art.name = f'modules/{name}/{art.path.name}'
        if local_code == '08':
            delivery = root_ctx.art('delivery')
            if delivery:
                ctx.external_dependencies = {Path(os.path.relpath(root / '07-delivery.md', folder)).as_posix(): delivery}
        contexts[name], scopes[name] = ctx, scope
    root_ctx.acceptance_ids = acceptance(root_ctx.art('requirements'))
    root_ctx.task_ids = tasks(root_ctx.art('tasks'))
    root_ctx.external_cases = {}
    for name, ctx in contexts.items():
        root_ctx.acceptance_ids.update(f'{name}#{a}' for a in acceptance(ctx.art('requirements')))
        root_ctx.task_ids.update(f'{name}#{t}' for t in tasks(ctx.art('tasks')))
        root_ctx.external_cases.update(cases(ctx, name))
        ctx.acceptance_ids = acceptance(ctx.art('requirements'))
        ctx.task_ids = tasks(ctx.art('tasks'))
        for dep in registry.order({name}):
            if dep != name and dep in contexts:
                ctx.task_ids.update(f'{dep}#{t}' for t in tasks(contexts[dep].art('tasks')))
    for entry in root_entries:
        gate.validate_artifact(root_ctx, entry)
    root_required = root_entries if require_frozen or selector else [e for e in root_entries if e['code'] < code]
    gate.check_all_frozen(root_ctx, root_required)
    issues = root_ctx.issues
    for name, ctx in contexts.items():
        for common in spec.COMMON_CODES:
            if common > code:
                continue
            art = root_ctx.art(spec.by_code(common)[0]['product'])
            expected = registry.modules[name]['baseline'][common]
            if art and art.fm.get('修订') != str(expected):
                ctx.issues.append(_lib.Issue('modules.json', 1, f'{name} 公共 {common} 基线修订 {expected} 已过期，当前为 {art.fm.get("修订")}'))
        for entry in scopes[name]:
            gate.validate_artifact(ctx, entry)
        frozen = scopes[name] if require_frozen or code == '07' else [e for e in scopes[name] if e['code'] < code]
        gate.check_all_frozen(ctx, frozen)
        dep_code = '06' if code in ('07', '08') else code
        for dep in registry.modules[name]['depends_on']:
            dep_ctx = contexts[dep]
            for entry in spec.by_code(dep_code):
                art = dep_ctx.art(entry['product'])
                if art is None or art.status() != '已冻结':
                    ctx.issues.append(_lib.Issue('modules.json', 1, f'{name} 依赖模块 {dep} 的阶段 {dep_code} 尚未冻结'))
        for issue in ctx.issues:
            if issue.file in ARTIFACT_NAMES:
                issue.file = f'modules/{name}/{issue.file}'
        issues.extend(ctx.issues)
    if code >= '07':
        _release(root_ctx, contexts, issues)
    pending = any(a.status() != '已冻结' for a in root_ctx.artifacts.values()) or any(
        a.status() != '已冻结' for ctx in contexts.values() for a in ctx.artifacts.values())
    return issues, pending


def _release(root_ctx, contexts, issues):
    art = root_ctx.art('delivery')
    sec = art.section('遗留与后续') if art else None
    tables = sec.tables() if sec else []
    matching = [t for t in tables if {'模块', '测试修订', '评审修订'} <= set(t.header)]
    if len(matching) != 1:
        issues.append(_lib.Issue('07-delivery.md', sec.line if sec else 1, '必须有一份模块交付清单：模块、测试修订、评审修订'))
        return
    table = matching[0]
    seen = set()
    for row in table.rows:
        name = table.cell(row, '模块').strip('` ')
        if name in seen or name not in contexts:
            issues.append(_lib.Issue(art.name, row.line, f'模块交付清单重复或未知：{name}'))
            continue
        seen.add(name)
        for product, column, expected in (('test-report', '测试修订', '可发布'), ('review-report', '评审修订', '可合并')):
            report = contexts[name].art(product)
            if not report or report.status() != '已冻结' or _lib.verdict(report, '结论', (expected,)) != expected:
                issues.append(_lib.Issue(art.name, row.line, f'{name} 的 {product} 必须有效冻结且明确{expected}'))
            elif table.cell(row, column) != report.fm.get('修订'):
                issues.append(_lib.Issue(art.name, row.line, f'{name} {column} 与实际报告修订不一致'))
    for name in contexts.keys() - seen:
        issues.append(_lib.Issue(art.name, table.line, f'模块交付清单缺少：{name}'))


def main(root, args, gate):
    issues = []
    registry = Registry.load(root, issues)
    if issues:
        return gate.print_issues(issues, root, '模块清单')
    if args.module and not (args.stage or args.next):
        return gate.print_issues([_lib.Issue('modules.json', 1, '--module 仅与 --stage 或 --next 配合，交付和归档必须检查整体')], root)
    if args.stage and (args.stage.zfill(2) not in spec.STAGE_TITLES or (args.module and args.stage.zfill(2) == '07')):
        return gate.print_issues([_lib.Issue('modules.json', 1, '阶段无效或模块不能单独执行统一交付 07')], root)
    codes = spec.MODULE_CODES if args.module else tuple(spec.STAGE_TITLES)
    if args.next:
        for code in codes:
            issues, pending = validate(root, registry, code, gate, args.module)
            if issues or pending:
                print(f'→ 下一步：{code}（模块树的首个未完成或无效阶段）')
                return gate.print_issues(issues, root, f'阶段 {code} 模块自检')
        subject = f'模块 {args.module} 及依赖' if args.module else '模块树'
        print(f'✓ {subject}全部冻结且有效，没有待办')
        return 0
    code = args.stage.zfill(2) if args.stage else '07' if args.delivery else '08'
    issues, _ = validate(root, registry, code, gate, args.module, require_frozen=not args.stage)
    return gate.print_issues(issues, root, '模块树检查' if not args.module else f'模块 {args.module} 自检')
