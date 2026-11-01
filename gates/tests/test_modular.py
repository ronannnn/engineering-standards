"""多层模块的真实产物、跨模块引用、发布和脚手架回归。"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import test_gates as fixtures


class ModularTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'run'
        shutil.copytree(fixtures.SAMPLE, self.root)
        self.names = ['users/access', 'orders/refund']
        entries = []
        for name in self.names:
            folder = self.root / 'modules' / name
            folder.mkdir(parents=True)
            for path in fixtures.SAMPLE.glob('*.md'):
                if path.name not in ('07-delivery.md', 'README.md'):
                    shutil.copyfile(path, folder / path.name)
            p = folder / '08-retro.md'
            p.write_text(p.read_text().replace('依据: 07-delivery.md',
                '依据: ' + os.path.relpath(self.root / '07-delivery.md', folder)))
            entries.append({'path': name, 'depends_on': [], 'baseline': {'01': 1, '02': 1, '03': 1}})
        self.manifest = {'version': 1, 'modules': entries}
        self.save()
        for name in self.names:
            p = self.root / '04-tasks.md'
            p.write_text(p.read_text().replace(
                '\n\n## 风险与回退', '\n' + ''.join(
                    f'| {name} 验收 {i} | {name}#任务 1 | 单元 | {name}#AC-{i} |\n'
                    for i in range(1, 5)) + '\n## 风险与回退'))
            p = self.root / '06-test-report.md'
            p.write_text(p.read_text().replace('\n\n## 未覆盖与风险', '\n' + ''.join(
                f'| {name}#AC-{i} | 是 | {name}#T-{i} |\n' for i in range(1, 5)) + '\n## 未覆盖与风险'))
        self.root.joinpath('07-delivery.md').write_text(self.root.joinpath('07-delivery.md').read_text() +
            '\n### 模块交付清单\n\n| 模块 | 测试修订 | 评审修订 |\n|---|---|---|\n' +
            ''.join(f'| {name} | 2 | 1 |\n' for name in self.names))

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        (self.root / 'modules.json').write_text(json.dumps(self.manifest, ensure_ascii=False))

    def edit(self, relative, old, new):
        p = self.root / relative
        self.assertIn(old, p.read_text())
        p.write_text(p.read_text().replace(old, new, 1))

    def gate(self, *args):
        return fixtures.run_gate(self.root, *args)

    def passed(self, *args):
        code, output = self.gate(*args)
        self.assertEqual(code, 0, output)

    def blocked(self, *args, contains=None):
        code, output = self.gate(*args)
        self.assertEqual(code, 1, output)
        if contains:
            self.assertIn(contains, output)

    def test_complete_nested_tree(self):
        self.passed('--all')
        self.passed('--delivery')
        self.passed('--next')

    def test_module_error_has_full_path(self):
        self.edit('modules/users/access/01-requirements.md', 'Then', '缺失结果')
        self.blocked('--stage', '01', contains='modules/users/access/01-requirements.md')

    def test_module_functional_requirement_ids_are_unique(self):
        self.edit('modules/users/access/01-requirements.md', '### FR-2 ', '### FR-1 ')
        self.blocked('--stage', '01', contains='功能需求编号重复')

    def test_missing_module_file_is_not_ignored(self):
        (self.root / 'modules/users/access/05-implementation.md').unlink()
        self.blocked('--delivery', contains='modules/users/access/05-implementation.md')

    def test_undeclared_artifact_is_blocked(self):
        folder = self.root / 'modules/forgotten'
        folder.mkdir()
        shutil.copyfile(fixtures.SAMPLE / '01-requirements.md', folder / '01-requirements.md')
        self.blocked('--all', contains='未登记')

    def test_missing_manifest_is_blocked_if_modules_exist(self):
        (self.root / 'modules.json').unlink()
        self.blocked('--delivery', contains='modules.json')

    def test_duplicate_unknown_and_unsafe_modules(self):
        original = json.loads(json.dumps(self.manifest))
        variants = [[], [self.manifest['modules'][0]] * 2,
            [{'path': '../outside', 'baseline': {'01': 1, '02': 1, '03': 1}}],
            [{'path': '/absolute', 'baseline': {'01': 1, '02': 1, '03': 1}}]]
        for value in variants:
            with self.subTest(value=value):
                self.manifest = {'version': 1, 'modules': value}
                self.save()
                self.blocked('--stage', '01', contains='modules.json')
        self.manifest = original

    def test_unknown_dependency(self):
        self.manifest['modules'][0]['depends_on'] = ['unknown']
        self.save()
        self.blocked('--stage', '01', contains='unknown')

    def test_dependency_cycle(self):
        self.manifest['modules'][0]['depends_on'] = [self.names[1]]
        self.manifest['modules'][1]['depends_on'] = [self.names[0]]
        self.save()
        self.blocked('--stage', '01', contains='循环')

    def test_manifest_json_errors_are_diagnostic(self):
        for raw in ('{', '[]', '{"version":1,"version":1,"modules":[]}'):
            (self.root / 'modules.json').write_text(raw)
            self.blocked('--stage', '01', contains='modules.json')

    def test_symlink_escape(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        (self.root / 'modules/external').symlink_to(outside, target_is_directory=True)
        self.manifest['modules'].append({'path': 'external', 'baseline': {'01': 1, '02': 1, '03': 1}})
        self.save()
        self.blocked('--stage', '01', contains='路径')

    def test_two_names_cannot_alias_one_module(self):
        (self.root / 'modules/alias').symlink_to(self.root / 'modules/users/access', target_is_directory=True)
        self.manifest['modules'].append({'path': 'alias', 'baseline': {'01': 1, '02': 1, '03': 1}})
        self.save()
        self.blocked('--stage', '01', contains='同一目录')

    def test_changed_common_revision_requires_review(self):
        self.edit('02-design.md', '修订: 1', '修订: 2')
        self.blocked('--stage', '05', contains='基线')

    def test_unfrozen_common_design_blocks_module(self):
        self.edit('02-design.md', '状态: 已冻结', '状态: 待签收')
        self.blocked('--module', 'users/access', '--stage', '04', contains='冻结')

    def test_dependency_same_stage_must_be_frozen(self):
        self.manifest['modules'][1]['depends_on'] = [self.names[0]]
        self.save()
        self.edit('modules/users/access/05-implementation.md', '状态: 已冻结', '状态: 草稿')
        self.blocked('--module', 'orders/refund', '--stage', '05', contains='依赖模块')

    def test_module_selector_and_unrelated_future_draft(self):
        self.edit('modules/orders/refund/08-retro.md', '---', '坏的未来草稿')
        self.passed('--module', 'users', '--stage', '06')

    def test_module_selector_includes_dependencies(self):
        self.manifest['modules'][1]['depends_on'] = [self.names[0]]
        self.save()
        self.edit('modules/users/access/05-implementation.md', 'GREEN 证据', '没有证据')
        self.blocked('--module', 'orders/refund', '--stage', '06', contains='users/access')

    def test_unknown_module_selector(self):
        self.blocked('--module', 'unknown', '--stage', '01', contains='unknown')

    def test_root_matrix_must_include_module_acceptance(self):
        self.edit('06-test-report.md', '| users/access#AC-4 | 是 | users/access#T-4 |\n', '')
        self.blocked('--stage', '06', contains='users/access#AC-4')

    def test_root_matrix_cannot_borrow_wrong_module_case(self):
        self.edit('06-test-report.md', '| users/access#AC-4 | 是 | users/access#T-4 |',
                  '| users/access#AC-4 | 是 | orders/refund#T-4 |')
        self.blocked('--stage', '06', contains='users/access#AC-4')

    def test_root_plan_must_include_module_acceptance(self):
        self.edit('04-tasks.md', '| users/access 验收 4 | users/access#任务 1 | 单元 | users/access#AC-4 |\n', '')
        self.blocked('--stage', '04', contains='users/access#AC-4')

    def test_root_plan_task_reference_must_exist(self):
        self.edit('04-tasks.md', 'users/access#任务 1', 'users/access#任务 999')
        self.blocked('--stage', '04', contains='任务 999')

    def test_delivery_snapshot_must_match(self):
        self.edit('07-delivery.md', '| users/access | 2 | 1 |', '| users/access | 1 | 1 |')
        self.blocked('--delivery', contains='修订')

    def test_delivery_missing_module_snapshot(self):
        self.edit('07-delivery.md', '| users/access | 2 | 1 |\n', '')
        self.blocked('--delivery', contains='users/access')

    def test_draft_module_report_blocks_delivery(self):
        self.edit('modules/users/access/06-review-report.md', '状态: 已冻结', '状态: 草稿')
        self.blocked('--delivery', contains='modules/users/access/06-review-report.md')

    def test_module_review_rejection_blocks_release(self):
        self.edit('modules/users/access/06-review-report.md', '结论：可合并', '结论：需修改')
        self.blocked('--delivery', contains='users/access')

    def test_archive_requires_module_retro_but_delivery_does_not(self):
        self.edit('modules/users/access/08-retro.md', '状态: 已冻结', '状态: 草稿')
        self.passed('--delivery')
        self.blocked('--all', contains='modules/users/access/08-retro.md')

    def test_module_retro_requires_root_delivery(self):
        self.edit('07-delivery.md', '状态: 已冻结', '状态: 待签收')
        self.blocked('--module', 'users/access', '--stage', '08', contains='冻结')

    def test_module_retro_checks_release_snapshot(self):
        self.edit('07-delivery.md', '| users/access | 2 | 1 |', '| users/access | 1 | 1 |')
        self.blocked('--module', 'users/access', '--stage', '08', contains='修订')

    def test_na_root_still_checks_module_acceptance(self):
        import re
        self.edit('01-requirements.md', '不适用: -', '不适用: 根仅组织模块，本次无新增系统级需求')
        p = self.root / '04-tasks.md'
        p.write_text(re.sub(r'^\|.*\| AC-[^\n]*\|\n', '', p.read_text(), flags=re.M))
        p = self.root / '06-test-report.md'
        p.write_text(re.sub(r'^\| AC-\d+ \| 是 \|[^\n]*\n', '', p.read_text(), flags=re.M))
        self.passed('--stage', '06')
        self.edit('06-test-report.md', '| users/access#AC-4 | 是 | users/access#T-4 |\n', '')
        self.blocked('--stage', '06', contains='users/access#AC-4')

    def test_next_rejects_bad_frozen_module(self):
        self.edit('modules/users/access/05-implementation.md', 'GREEN 证据', '没有证据')
        self.blocked('--next', contains='users/access')

    def test_future_module_artifact_does_not_block_early_stage(self):
        (self.root / 'modules/users/access/08-retro.md').write_text('broken')
        self.passed('--stage', '01')


class ModuleScaffoldTest(unittest.TestCase):
    def test_deep_module_and_declared_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            shutil.copytree(fixtures.SAMPLE, root)
            cmd = [sys.executable, str(fixtures.ROOT / 'scripts/init-module.py'), str(root)]
            first = subprocess.run(cmd + ['users/access'], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = subprocess.run(cmd + ['orders/refund/status', '--depends-on', 'users/access'], capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            data = json.loads((root / 'modules.json').read_text())
            self.assertEqual(data['modules'][1]['depends_on'], ['users/access'])
            retro = root / 'modules/orders/refund/status/08-retro.md'
            self.assertIn('依据: ../../../../07-delivery.md', retro.read_text())

    def test_unknown_dependency_preserves_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            shutil.copytree(fixtures.SAMPLE, root)
            cmd = [sys.executable, str(fixtures.ROOT / 'scripts/init-module.py'), str(root)]
            subprocess.run(cmd + ['users/access'], capture_output=True, check=True)
            original = (root / 'modules.json').read_text()
            result = subprocess.run(cmd + ['orders/refund', '--depends-on', 'unknown'], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((root / 'modules.json').read_text(), original)
            self.assertFalse((root / 'modules/orders/refund').exists())

    def test_initialize_nested_module_and_preserve_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            shutil.copytree(fixtures.SAMPLE, root)
            cmd = [sys.executable, str(fixtures.ROOT / 'scripts/init-module.py'), str(root), 'users/access']
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            folder = root / 'modules/users/access'
            self.assertTrue((folder / '01-requirements.md').is_file())
            self.assertTrue((folder / '08-retro.md').is_file())
            self.assertFalse((folder / '07-delivery.md').exists())
            text = (folder / '01-requirements.md').read_text()
            manifest = (root / 'modules.json').read_text()
            again = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual((folder / '01-requirements.md').read_text(), text)
            self.assertEqual((root / 'modules.json').read_text(), manifest)
            self.assertIn('users/access', (root / 'modules/README.md').read_text())

    def test_invalid_path_has_no_side_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            shutil.copytree(fixtures.SAMPLE, root)
            result = subprocess.run([sys.executable, str(fixtures.ROOT / 'scripts/init-module.py'),
                str(root), '../escape'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'modules.json').exists())
