"""脚手架名称、索引和 CI 目录选择的一致性回归。"""

from pathlib import Path
import subprocess
import tempfile
import unittest

import test_gates as fixtures
from changed_runs import select_runs


class ScaffoldTest(unittest.TestCase):
    def initialize(self, root, slug):
        return subprocess.run(
            ['bash', str(fixtures.ROOT / 'scripts/init-docs.sh'), slug],
            cwd=root, capture_output=True, text=True,
        )

    def test_invalid_slug_has_no_side_effect(self):
        for slug in ('coupon--import', 'coupon-import-', '-coupon', 'Coupon', 'coupon_import'):
            with self.subTest(slug=slug), tempfile.TemporaryDirectory() as tmp:
                result = self.initialize(tmp, slug)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse((Path(tmp) / 'docs').exists())

    def test_valid_slugs_are_detected_by_ci(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for slug in ('coupon', 'coupon-import', 'v2-export'):
                result = self.initialize(root, slug)
                self.assertEqual(result.returncode, 0, result.stderr)
                relative = f'docs/engineering/{slug}'
                self.assertEqual(select_runs(root, [relative + '/01-requirements.md']), [relative])
                self.assertEqual(len(list((root / relative).glob('*.md'))), 9)

    def test_index_keeps_shorter_name_and_existing_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.initialize(root, 'coupon-import').returncode, 0)
            index = root / 'docs/engineering/README.md'
            index.write_text(index.read_text() + '\n保留团队备注。\n', encoding='utf-8')
            self.assertEqual(self.initialize(root, 'coupon').returncode, 0)
            content = index.read_text(encoding='utf-8')
            for slug in ('coupon-import', 'coupon'):
                self.assertEqual(sum(line.startswith(f'| {slug} |') for line in content.splitlines()), 1)
            self.assertIn('保留团队备注。', content)
            self.assertLess(content.index('| coupon |'), content.index('保留团队备注。'))

    def test_existing_run_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.initialize(root, 'coupon').returncode, 0)
            path = root / 'docs/engineering/coupon/01-requirements.md'
            path.write_text('保留需求内容。', encoding='utf-8')
            index = root / 'docs/engineering/README.md'
            original = index.read_bytes()
            self.assertEqual(self.initialize(root, 'coupon').returncode, 1)
            self.assertEqual(path.read_text(encoding='utf-8'), '保留需求内容。')
            self.assertEqual(index.read_bytes(), original)

    def test_custom_index_formats_are_preserved(self):
        examples = (
            '# 团队需求\n\n保留说明。',
            '| 需求 | 状态 | 创建时间 | 备注 |\n|---|---|---|---|\n| old | 完成 | 2026-01-01 | |',
            '| 其他清单 | 备注 |\n|---|---|\n| coupon | 示例文字，不是需求索引 |\n',
        )
        for content in examples:
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                index = root / 'docs/engineering/README.md'
                index.parent.mkdir(parents=True)
                index.write_text(content, encoding='utf-8')
                result = self.initialize(root, 'coupon')
                self.assertEqual(result.returncode, 0, result.stderr)
                updated = index.read_text(encoding='utf-8')
                self.assertTrue(updated.startswith(content))
                self.assertIn('| 需求 | 状态 | 创建时间 | 备注 |', updated)
                self.assertIn('| coupon | 进行中 |', updated)
