#!/usr/bin/env python3
"""给已初始化的运行目录增加一个模块；不移动或覆盖已有产物。"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'gates'))
import _lib
import modular
import spec

INDEX_MARKER = '<!-- engineering-standards:modules -->'


def initialize(root, name, dependencies):
    if not root.is_dir() or not modular.safe_path(name):
        raise ValueError('运行目录必须存在，模块路径必须是多层 kebab-case 相对路径')
    base = root / 'modules'
    target = base / name
    if not base.resolve().is_relative_to(root.resolve()) or not target.resolve().is_relative_to(base.resolve()):
        raise ValueError('模块路径不能越界或通过符号链接指向外部')
    if target.exists() or target.is_symlink():
        raise ValueError('模块目录已存在，拒绝覆盖')
    manifest_path = root / 'modules.json'
    original = manifest_path.read_bytes() if manifest_path.exists() else None
    modules = {}
    if original is not None:
        issues = []
        registry = modular.Registry.load(root, issues)
        if issues:
            raise ValueError('\n'.join(map(str, issues)))
        modules = registry.modules
    elif modular.enabled(root):
        raise ValueError('存在未登记模块产物，请先补齐清单，拒绝覆盖')
    if name in modules:
        raise ValueError('模块已登记，拒绝覆盖')
    if len(dependencies) != len(set(dependencies)) or any(d not in modules for d in dependencies):
        raise ValueError('依赖必须是已登记且不重复的模块路径')
    baseline = {}
    for code in spec.COMMON_CODES:
        entry = spec.by_code(code)[0]
        art = _lib.Artifact(root / entry['file'], entry)
        if art.fm_error or not art.fm.get('修订', '').isdigit() or int(art.fm['修订']) < 1:
            raise ValueError(f'根公共产物格式或修订无效：{entry["file"]}')
        baseline[code] = int(art.fm['修订'])
    index = base / 'README.md'
    if index.exists() and INDEX_MARKER not in index.read_text(encoding='utf-8'):
        raise ValueError('modules/README.md 是自定义文件，拒绝覆盖；请先迁移索引')
    modules = {**modules, name: {'path': name, 'depends_on': dependencies, 'baseline': baseline}}
    # 先准备全部模板，再修改目标目录和清单。
    with tempfile.TemporaryDirectory(prefix='.module-init-', dir=root) as tmp:
        staged = Path(tmp) / 'module'
        staged.mkdir()
        for entry in spec.ARTIFACTS:
            if entry['code'] not in spec.MODULE_CODES:
                continue
            text = (REPO / 'templates' / entry['file']).read_text(encoding='utf-8')
            if entry['code'] == '08':
                relative = Path(os.path.relpath(root / '07-delivery.md', target)).as_posix()
                text = text.replace('依据: 07-delivery.md', '依据: ' + relative, 1)
            (staged / entry['file']).write_text(text, encoding='utf-8')
        payload = {'version': 1, 'modules': list(modules.values())}
        manifest_tmp = Path(tmp) / 'modules.json'
        manifest_tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if (manifest_path.read_bytes() if manifest_path.exists() else None) != original:
            raise ValueError('模块清单已被其他操作修改，请重新运行')
        target.parent.mkdir(parents=True, exist_ok=True)
        staged.rename(target)
        try:
            manifest_tmp.replace(manifest_path)
        except OSError:
            shutil.rmtree(target)
            raise
    content = INDEX_MARKER + '\n# 本次需求的模块索引\n\n由 modules.json 生成；目录层级不代表业务依赖。\n\n| 模块路径 | 资料 | 依赖 |\n|---|---|---|\n'
    for module_name, item in sorted(modules.items()):
        content += f'| {module_name} | [需求]({module_name}/01-requirements.md) | '+('、'.join(item['depends_on']) or '无')+' |\n'
    index.write_text(content, encoding='utf-8')
    print(f'已创建模块：{target}\n公共基线：{baseline}\n模块 07 由根目录统一交付；模块 08 已指向根 07。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir')
    parser.add_argument('module_path')
    parser.add_argument('--depends-on', action='append', default=[], help='已登记模块路径，可重复指定')
    args = parser.parse_args()
    try:
        initialize(Path(args.run_dir).resolve(), args.module_path, args.depends_on)
    except (OSError, ValueError) as exc:
        print(f'初始化失败：{exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
