"""真实违规输入的回归：证据、依赖、范围和 CI 目录筛选。"""

import subprocess
import sys
import unittest
from pathlib import Path

import test_gates as fixtures

ROOT = fixtures.ROOT
run_gate = fixtures.run_gate


class RegressionTest(unittest.TestCase):
    setUp = fixtures.GateTest.setUp
    tearDown = fixtures.GateTest.tearDown
    def edit(self, name, transform):
        path = self.fixture.dir / name
        path.write_text(transform(path.read_text(encoding="utf-8")), encoding="utf-8")

    def assert_blocked(self, *args, message=None):
        code, output = run_gate(self.fixture.dir, *args)
        self.assertEqual(code, 1, output)
        if message:
            self.assertIn(message, output)

    def test_next_reads_and_validates_each_artifact_once(self):
        from collections import Counter
        from unittest.mock import patch
        import _lib

        with patch.object(_lib, 'Artifact', wraps=_lib.Artifact) as read, patch.object(
            fixtures.gate_run, 'validate_artifact', wraps=fixtures.gate_run.validate_artifact
        ) as validate:
            code, output = run_gate(self.fixture.dir, '--next')
        self.assertEqual(code, 0, output)
        counts = Counter(call.args[0].name for call in read.call_args_list)
        self.assertEqual(counts, {entry['file']: 1 for entry in fixtures.gate_run.spec.ARTIFACTS})
        self.assertEqual(validate.call_count, 9)

    def test_next_rechecks_changes_between_calls(self):
        code, output = run_gate(self.fixture.dir, '--next')
        self.assertEqual(code, 0, output)
        self.fixture.replace('01-requirements.md', '签收: 陈若南', '签收: -')
        self.assert_blocked('--next', message='签收')

    def test_red_cannot_borrow_green_fields(self):
        import re
        self.edit("05-implementation.md", lambda t: re.sub(
            r"(- RED 证据：\n).*?(?=- GREEN 证据：)", r"\1", t, flags=re.S))
        self.assert_blocked("--stage", "05", message="RED")

    def test_evidence_values_cannot_be_empty(self):
        import re
        for field in ("命令", "输出摘要"):
            with self.subTest(field=field):
                path = self.fixture.dir / "05-implementation.md"
                original = path.read_text()
                self.edit(path.name, lambda t: re.sub(
                    rf"^  - {field}：.*$", f"  - {field}：", t, flags=re.M))
                self.assert_blocked("--stage", "05", message=field)
                path.write_text(original)

    def test_empty_test_command_cannot_borrow_next_line(self):
        import re
        self.edit("05-implementation.md", lambda t: re.sub(
            r"^- 测试命令：.*$", "- 测试命令：", t, flags=re.M))
        self.assert_blocked("--stage", "05", message="测试命令")

    def test_missing_matrix_case_is_blocked(self):
        import re
        self.edit("06-test-report.md", lambda t: re.sub(r"^\| T-4 .*\n", "", t, flags=re.M))
        self.assert_blocked("--stage", "06", message="T-4")

    def test_matrix_case_must_cover_the_same_ac(self):
        self.fixture.replace("06-test-report.md", "| T-4 | AC-4 |", "| T-4 | AC-1 |")
        self.assert_blocked("--stage", "06", message="AC-4")

    def test_duplicate_case_id_is_blocked(self):
        self.fixture.replace("06-test-report.md", "| T-4 | AC-4 |", "| T-1 | AC-4 |")
        self.assert_blocked("--stage", "06", message="重复")

    def test_missing_matrix_columns_do_not_crash(self):
        self.fixture.replace("06-test-report.md", "| 验收标准 | 是否有已执行用例 | 依据用例 |", "| 其他 | 状态 | 依据 |")
        self.assert_blocked("--stage", "06", message="缺少列")

    def test_missing_failure_columns_do_not_crash(self):
        self.edit("06-test-report.md", lambda t: t.replace("| 通过 | 连续两次确认", "| 失败 | 连续两次确认").replace(
            "无失败用例", "| 用例 | 失败原因 | 修复方式 |\n|---|---|---|\n| T-4 | 未修复 | 补测试 |"))
        self.assert_blocked("--stage", "06", message="复验结果")

    def test_empty_reference_list_is_not_coverage(self):
        self.fixture.replace("06-test-report.md", "| AC-4 | 是 | T-4 |", "| AC-4 | 是 | ` ` |")
        self.assert_blocked("--stage", "06", message="依据用例")

    def test_na_retro_cannot_be_machine_approved(self):
        self.fixture.replace("08-retro.md", "不适用: -", "不适用: 本次为机械修改，不需要复盘")
        self.fixture.replace("08-retro.md", "签收: 陈若南", "签收: 机器门禁")
        self.assert_blocked("--all", message="人签收")

    def test_engineering_failure_prevents_delivery(self):
        self.fixture.replace("07-delivery.md", "| 安全扫描 | 通过 |", "| 安全扫描 | 失败 |")
        self.assert_blocked("--all", message="安全扫描")

    def test_missing_engineering_check_prevents_delivery(self):
        import re
        self.edit("07-delivery.md", lambda t: re.sub(r"^\| 构建 .*\n", "", t, flags=re.M))
        self.assert_blocked("--stage", "07", message="构建")

    def test_unexplained_skip_prevents_delivery(self):
        self.fixture.replace("07-delivery.md", "| 构建 | 通过 |", "| 构建 | 跳过 |")
        self.assert_blocked("--stage", "07", message="不适用")

    def test_explained_build_skip_is_allowed(self):
        self.fixture.replace("07-delivery.md", "| 构建 | 通过 | `pnpm build` 与 `go build ./...` 均成功 |",
                             "| 构建 | 跳过 | 不适用：本次为纯文档项目，无编译产物 |")
        code, output = run_gate(self.fixture.dir, "--stage", "07")
        self.assertEqual(code, 0, output)

    def test_gate_cannot_be_skipped_even_with_reason(self):
        self.fixture.replace("07-delivery.md", "| 标准门禁 | 通过 |", "| 标准门禁 | 跳过 | 不适用：临时例外；")
        self.assert_blocked("--stage", "07", message="标准门禁")

    def test_unfrozen_review_prevents_delivery(self):
        self.fixture.replace("06-review-report.md", "状态: 已冻结", "状态: 草稿")
        self.assert_blocked("--stage", "07", message="06-review-report.md")

    def test_missing_review_verdict_prevents_delivery(self):
        self.fixture.replace("06-review-report.md", "结论：可合并", "结论：稍后讨论")
        self.assert_blocked("--stage", "07", message="结论")

    def test_invalid_ancestor_signoff_prevents_stage(self):
        self.fixture.replace("01-requirements.md", "签收: 陈若南", "签收: -")
        self.assert_blocked("--stage", "05", message="签收")

    def test_frontmatter_errors_are_diagnostics(self):
        path = self.fixture.dir / "01-requirements.md"
        original = path.read_text()
        malformed = ["", original.removeprefix("---\n"), "---\n产物: requirements\n",
                     original.replace("修订: 1", "修订没有冒号"),
                     original.replace("修订: 1", "修订: 1\n修订: 2")]
        for text in malformed:
            with self.subTest(text=text[:30]):
                path.write_text(text)
                self.assert_blocked("--stage", "01", message="frontmatter")
        path.write_text(original)

    def test_invalid_utf8_is_diagnostic(self):
        (self.fixture.dir / "01-requirements.md").write_bytes(b"\xff")
        self.assert_blocked("--all", message="读取")

    def test_next_rejects_invalid_frozen_signature(self):
        self.fixture.replace("01-requirements.md", "签收: 陈若南", "签收: -")
        self.assert_blocked("--next", message="签收")

    def test_next_rejects_broken_frozen_content(self):
        self.fixture.replace("05-implementation.md", "GREEN 证据", "未记录")
        self.assert_blocked("--next", message="GREEN")

    def test_stage_does_not_require_future_artifacts(self):
        for path in self.fixture.dir.iterdir():
            if path.name != "01-requirements.md":
                path.unlink()
        code, output = run_gate(self.fixture.dir, "--stage", "01")
        self.assertEqual(code, 0, output)

    def test_future_malformed_artifact_does_not_block_stage(self):
        self.fixture.write("08-retro.md", "broken future draft")
        code, output = run_gate(self.fixture.dir, "--stage", "01")
        self.assertEqual(code, 0, output)

    def test_delivery_scope_does_not_require_retro(self):
        self.fixture.unlink("08-retro.md")
        code, output = run_gate(self.fixture.dir, "--delivery")
        self.assertEqual(code, 0, output)
        self.assert_blocked("--all", message="08-retro.md")

    def test_delivery_scope_accepts_draft_retro(self):
        self.fixture.replace("08-retro.md", "状态: 已冻结", "状态: 草稿")
        code, output = run_gate(self.fixture.dir, "--delivery")
        self.assertEqual(code, 0, output)
        self.assert_blocked("--all", message="尚未冻结")

    def test_delivery_scope_requires_final_signoff(self):
        self.fixture.replace("07-delivery.md", "状态: 已冻结", "状态: 待签收")
        self.assert_blocked("--delivery", message="尚未冻结")

    def test_pending_delivery_can_be_content_checked_without_fake_acceptance(self):
        self.fixture.replace("07-delivery.md", "状态: 已冻结", "状态: 待签收")
        self.fixture.replace("07-delivery.md", "- 验收人：陈若南", "- 验收人：-")
        self.fixture.replace("07-delivery.md", "- 确认时间：2026-11-04", "- 确认时间：-")
        code, output = run_gate(self.fixture.dir, "--stage", "07")
        self.assertEqual(code, 0, output)
        self.assert_blocked("--delivery", message="尚未冻结")

    def test_unselected_template_verdict_is_not_a_decision(self):
        self.fixture.replace("06-test-report.md", "结论：可发布", "结论：可发布 / 不可发布")
        self.assert_blocked("--stage", "06", message="结论")

    def test_unknown_compliance_cannot_be_approved(self):
        self.fixture.replace("06-review-report.md", "结论：符合", "结论：无法判定")
        self.assert_blocked("--stage", "06", message="无法判定")


class ChangedRunsTest(unittest.TestCase):
    def test_real_paths_only_and_deleted_paths_are_ignored(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/engineering/real-run").mkdir(parents=True)
            (root / "docs/engineering/_custom/roles").mkdir(parents=True)
            data = "\0".join([
                "docs/engineering/README.md", "docs/engineering/_custom/roles/dev.toml",
                "docs/engineering/real-run/01-requirements.md",
                "docs/engineering/real-run/04-tasks.md", "docs/engineering/deleted/01-requirements.md",
                "docs/engineering/../../outside/01-requirements.md", "README.md", "",
            ])
            result = subprocess.run([sys.executable, str(ROOT / "gates/changed_runs.py"), str(root)],
                                    input=data, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.splitlines(), ["docs/engineering/real-run"])
