"""门禁自测：样例必须全绿，故意违规必须被拦住。

运行：python3 -m unittest discover gates/tests
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATES = ROOT / "gates"
SAMPLE = ROOT / "examples" / "sample-run"
sys.path.insert(0, str(GATES))

import run as gate_run  # noqa: E402


def run_gate(path: Path, *args: str) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = gate_run.main([str(path), *args])
    return code, buffer.getvalue()


class RunFixture:
    """把 examples/sample-run 复制到临时目录，供每条用例独立修改。"""

    def __init__(self, tmp: Path):
        self.dir = tmp / "run"
        shutil.copytree(SAMPLE, self.dir)

    def replace(self, name: str, old: str, new: str) -> None:
        path = self.dir / name
        text = path.read_text(encoding="utf-8")
        assert old in text, f"{name} 中找不到待替换文本：{old[:40]}"
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def write(self, name: str, text: str) -> None:
        (self.dir / name).write_text(text, encoding="utf-8")

    def unlink(self, name: str) -> None:
        (self.dir / name).unlink()


class GateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture = RunFixture(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # ---------- 正向 ----------
    def test_sample_run_passes(self) -> None:
        code, output = run_gate(self.fixture.dir, "--all")
        self.assertEqual(code, 0, output)
        self.assertIn("全链通过", output)

    def test_next_reports_complete(self) -> None:
        code, output = run_gate(self.fixture.dir, "--next")
        self.assertEqual(code, 0, output)
        self.assertIn("全部冻结", output)

    def test_na_artifact_is_allowed_for_ui_stage(self) -> None:
        self.fixture.write(
            "03-ui-design.md",
            "\n".join(
                [
                    "---",
                    "产物: ui-design",
                    "阶段: 03-UI/UX设计",
                    "编号: UIX-0001",
                    "状态: 已冻结",
                    "签收: 陈若南",
                    "签收时间: 2026-10-31",
                    "依据: 02-design.md",
                    "修订: 1",
                    "不适用: 本需求为纯后端接口，没有用户界面变更",
                    "---",
                    "",
                    "# UI/UX 设计：不适用",
                    "",
                    "本需求不涉及界面。",
                    "",
                ]
            ),
        )
        code, output = run_gate(self.fixture.dir, "--all")
        self.assertEqual(code, 0, output)

    # ---------- 结构违规 ----------
    def test_missing_artifact_is_blocked(self) -> None:
        self.fixture.unlink("06-review-report.md")
        code, output = run_gate(self.fixture.dir, "--all")
        self.assertEqual(code, 1)
        self.assertIn("缺少产物文件", output)

    def test_missing_acceptance_criterion_is_blocked(self) -> None:
        self.fixture.replace("01-requirements.md", "  - Then 2 秒内返回预览结果", "  - 结果 2 秒内返回预览结果")
        code, output = run_gate(self.fixture.dir, "--stage", "01")
        self.assertEqual(code, 1, output)
        self.assertIn("Then", output)

    def test_unfrozen_artifact_blocks_chain(self) -> None:
        self.fixture.replace("02-design.md", "状态: 已冻结", "状态: 草稿")
        code, output = run_gate(self.fixture.dir, "--all")
        self.assertEqual(code, 1)
        self.assertIn("尚未冻结", output)
        self.assertIn("依赖的产物未冻结", output)

    # ---------- 签收违规 ----------
    def test_machine_signoff_rejected_on_human_stage(self) -> None:
        self.fixture.replace("02-design.md", "签收: 陈若南", "签收: 机器门禁")
        code, output = run_gate(self.fixture.dir, "--stage", "02")
        self.assertEqual(code, 1)
        self.assertIn("必须由人签收", output)

    def test_human_stage_without_signature_is_blocked(self) -> None:
        self.fixture.replace("07-delivery.md", "签收: 陈若南", "签收: -")
        code, output = run_gate(self.fixture.dir, "--stage", "07")
        self.assertEqual(code, 1)
        self.assertIn("必须填写签收人", output)

    # ---------- 证据违规 ----------
    def test_implementation_without_green_evidence_is_blocked(self) -> None:
        self.fixture.replace("05-implementation.md", "### 任务 2：CSV 解析与逐行校验", "### 任务 2：CSV 解析与逐行校验\n\n- 未写证据")
        self.fixture.replace("05-implementation.md", "- GREEN 证据：\n  - 命令：`go test ./internal/coupon/import/... -run TestValidate`\n  - 输出摘要：`ok internal/coupon/import 0.412s — 7 passed`\n", "")
        code, output = run_gate(self.fixture.dir, "--stage", "05")
        self.assertEqual(code, 1, output)
        self.assertIn("GREEN 证据", output)

    def test_publish_with_failing_case_is_blocked(self) -> None:
        self.fixture.replace(
            "06-test-report.md",
            "| T-4 | AC-4 | 集成 | `go test ./internal/coupon/handler/... -run TestImportCommitIdempotent` | 通过 |",
            "| T-4 | AC-4 | 集成 | `go test ./internal/coupon/handler/... -run TestImportCommitIdempotent` | 失败 |",
        )
        code, output = run_gate(self.fixture.dir, "--stage", "06")
        self.assertEqual(code, 1, output)
        self.assertIn("不能判定为可发布", output)

    def test_matrix_audit_missing_criterion_is_blocked(self) -> None:
        self.fixture.replace("06-test-report.md", "| AC-4 | 是 | T-4 |\n", "")
        code, output = run_gate(self.fixture.dir, "--stage", "06")
        self.assertEqual(code, 1, output)
        self.assertIn("矩阵审计缺少验收标准 AC-4", output)

    def test_review_with_blocker_cannot_be_merged(self) -> None:
        self.fixture.replace(
            "06-review-report.md",
            "### 严重（必须修）\n\n无",
            "### 严重（必须修）\n\n- `internal/coupon/import/parser.go:51` — 事务外调用发放服务，失败会留下半批数据 — 数据不一致 — 移入事务或用补偿",
        )
        code, output = run_gate(self.fixture.dir, "--stage", "06")
        self.assertEqual(code, 1, output)
        self.assertIn("不能判定为可合并", output)

    # ---------- 设计违规 ----------
    def test_design_with_single_alternative_is_blocked(self) -> None:
        self.fixture.replace("02-design.md", "### 方案 B：前端解析后逐条调单张接口", "### 附注 B：前端解析")
        self.fixture.replace("02-design.md", "### 方案 C：数据库 LOAD DATA 直灌", "### 附注 C：数据库直灌")
        code, output = run_gate(self.fixture.dir, "--stage", "02")
        self.assertEqual(code, 1, output)
        self.assertIn("备选方案至少两个", output)

    def test_schema_change_without_migration_is_blocked(self) -> None:
        self.fixture.replace(
            "02-design.md",
            "## 数据模型与迁移\n\n- 数据结构：",
            "## 数据模型与迁移\n\n不适用：字段都可以从券名推断\n\n- 数据结构：",
        )
        code, output = run_gate(self.fixture.dir, "--stage", "02")
        self.assertEqual(code, 1, output)
        self.assertIn("不允许写不适用", output)

    # ---------- 交付违规 ----------
    def test_delivery_missing_ai_row_is_blocked(self) -> None:
        self.fixture.replace(
            "07-delivery.md",
            "| 评审处理 | 人工把关 | AI 处理评审意见并给出结论，人工确认两条轻微问题延后 |\n",
            "",
        )
        code, output = run_gate(self.fixture.dir, "--stage", "07")
        self.assertEqual(code, 1, output)
        self.assertIn("AI 参与度", output)

    def test_delivery_without_rollback_is_blocked(self) -> None:
        self.fixture.replace("07-delivery.md", "- 触发条件：导入失败率连续 5 分钟 > 10%，或出现批次数据不一致，或前端白屏。", "- 相关情况：见部署方案。")
        self.fixture.replace("07-delivery.md", "- 预估耗时：10 分钟。", "- 其他：见部署方案。")
        self.fixture.replace("07-delivery.md", "- 数据回滚：新列与新表可整体删除；已导入的券保留为普通券，不做自动失效（需运营人工确认）。", "")
        self.fixture.replace("07-delivery.md", "- 步骤：1) 回滚应用版本到上一个镜像；2) 删除 `idx_coupon_batch` 索引与 `import_batch_id` 列；3) 删除 `coupon_import_batch` 表；4) 回收两个权限点。", "")
        code, output = run_gate(self.fixture.dir, "--stage", "07")
        self.assertEqual(code, 1, output)
        self.assertIn("回滚方案缺少", output)

    # ---------- 复盘违规 ----------
    def test_retro_improvement_must_point_into_repo(self) -> None:
        self.fixture.replace("08-retro.md", "| `skills/org-design/SKILL.md` |", "| 某个项目的 README |")
        code, output = run_gate(self.fixture.dir, "--stage", "08")
        self.assertEqual(code, 1, output)
        self.assertIn("目标文件必须指向本仓库内的路径", output)


if __name__ == "__main__":
    unittest.main()
