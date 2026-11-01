"""维护文档与门禁之间的可执行契约，不判定文案质量。"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gates"))
import _lib
import spec


class DocumentContractTest(unittest.TestCase):
    def test_requirements_tree_example_is_valid_without_future_stages(self):
        from test_gates import run_gate

        example = ROOT / "examples" / "requirements-tree"
        code, output = run_gate(example, "--stage", "01")
        self.assertEqual(code, 0, output)
        # 草稿示例只用于讨论和内容自检，不能被当成已交付。
        code, output = run_gate(example, "--delivery")
        self.assertEqual(code, 1, output)

    def test_templates_match_registered_metadata_and_anchors(self):
        for entry in spec.ARTIFACTS:
            with self.subTest(file=entry["file"]):
                art = _lib.Artifact(ROOT / "templates" / entry["file"], entry)
                issues = []
                _lib.check_frontmatter(issues, art)
                _lib.check_anchors(issues, art)
                self.assertEqual(issues, [])

    def test_policy_references_resolve(self):
        paths = list(ROOT.glob("*.md"))
        for folder in ("policies", "skills", "templates", "adapters", "examples"):
            paths.extend((ROOT / folder).rglob("*.md"))
        for path in paths:
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative:
                    with self.subTest(source=str(path.relative_to(ROOT)), target=target):
                        self.assertTrue((path.parent / relative).exists())

    def test_lifecycle_guides_ship_with_the_standard(self):
        for name in ("project-context.md", "lifecycle.md", "workflow-evaluation.md"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / "policies" / name).is_file())
