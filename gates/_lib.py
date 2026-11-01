"""门禁公共库：frontmatter / 标题锚点 / 表格 / 签收 / 不适用。

约束：只使用 Python 3 标准库（AGENTS.md §8）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import spec

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SIGN_OFF_NA = "-"


@dataclass
class Issue:
    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}"


@dataclass
class Row:
    line: int
    cells: list[str]


@dataclass
class Table:
    header: list[str]
    rows: list[Row]
    line: int

    def column(self, name: str) -> int:
        try:
            return self.header.index(name)
        except ValueError:
            raise KeyError(name)

    def cell(self, row: Row, name: str) -> str:
        if name not in self.header:
            return ""
        idx = self.column(name)
        if idx >= len(row.cells):
            return ""
        return row.cells[idx].strip()


class Section:
    def __init__(self, anchor: str, line: int, lines: list[tuple[int, str]]):
        self.anchor = anchor
        self.line = line
        self.lines = lines

    @property
    def text(self) -> str:
        return "\n".join(t for _, t in self.lines).strip()

    @property
    def empty(self) -> bool:
        return not self.text

    def first_line(self) -> int:
        for lineno, text in self.lines:
            if text.strip():
                return lineno
        return self.line

    def blocks(self, prefix: str) -> list[tuple[int, str, list[tuple[int, str]]]]:
        """按 `### ` 切块，返回 (行号, 标题, 内容行)。"""
        result: list[tuple[int, str, list[tuple[int, str]]]] = []
        current: tuple[int, str, list[tuple[int, str]]] | None = None
        for lineno, text in self.lines:
            if text.startswith("### "):
                if current is not None:
                    result.append(current)
                current = (lineno, text[4:].strip(), [])
            elif current is not None:
                current[2].append((lineno, text))
        if current is not None:
            result.append(current)
        return result

    def tables(self) -> list[Table]:
        tables: list[Table] = []
        i = 0
        lines = self.lines
        while i < len(lines):
            lineno, text = lines[i]
            if text.lstrip().startswith("|") and i + 1 < len(lines) and re.match(
                r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1][1]
            ):
                header = _split_row(text)
                rows: list[Row] = []
                j = i + 2
                while j < len(lines) and lines[j][1].lstrip().startswith("|"):
                    rows.append(Row(lines[j][0], _split_row(lines[j][1])))
                    j += 1
                tables.append(Table(header, rows, lineno))
                i = j
            else:
                i += 1
        return tables

    def checkboxes(self) -> list[tuple[int, str, bool]]:
        result = []
        for lineno, text in self.lines:
            m = re.match(r"^\s*-\s*\[( |x|X)\]\s*(.+)$", text)
            if m:
                result.append((lineno, m.group(2).strip(), m.group(1).lower() == "x"))
        return result


def _split_row(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


class Artifact:
    def __init__(self, path: Path, entry: dict):
        self.path = path
        self.spec = entry
        self.name = path.name
        raw = path.read_text(encoding="utf-8")
        self.raw = raw
        self.lines = raw.splitlines()
        self.fm: dict[str, str] = {}
        self.fm_lines: dict[str, int] = {}
        self.fm_error: tuple[int, str] | None = None
        self.sections: dict[str, Section] = {}
        self.duplicate_sections: list[tuple[int, str]] = []
        self.body_start = len(self.lines) + 1
        self._parse_frontmatter()
        if self.fm_error is None:
            self._parse_sections()

    # ---------- 解析 ----------
    def _parse_frontmatter(self) -> None:
        if not self.lines or self.lines[0].strip() != "---":
            self.fm_error = (1, "缺少 frontmatter：文件首行必须是 ---")
            return
        end = None
        for i in range(1, len(self.lines)):
            if self.lines[i].strip() == "---":
                end = i
                break
        if end is None:
            self.fm_error = (1, "frontmatter 未闭合：缺少结束的 ---")
            return
        for i in range(1, end):
            text = self.lines[i]
            if not text.strip() or text.lstrip().startswith("#"):
                continue
            if ":" not in text:
                self.fm_error = (i + 1, f"frontmatter 行格式错误（缺少冒号）：{text.strip()}")
                return
            key, value = text.split(":", 1)
            if not key.strip() or key.strip() in self.fm:
                self.fm_error = (i + 1, f"frontmatter 字段为空或重复：{key.strip()}")
                return
            self.fm[key.strip()] = value.strip()
            self.fm_lines[key.strip()] = i + 1
        self.body_start = end + 2

    def _parse_sections(self) -> None:
        current: tuple[int, str, list[tuple[int, str]]] | None = None
        end_of_body = len(self.lines) + 1
        for i in range(self.body_start - 1, len(self.lines)):
            text = self.lines[i]
            lineno = i + 1
            if text.startswith("## "):
                if current is not None:
                    anchor, line, collected = current
                    if anchor in self.sections:
                        self.duplicate_sections.append((line, anchor))
                    else:
                        self.sections[anchor] = Section(anchor, line, collected)
                current = (text[3:].strip(), lineno, [])
            elif current is not None:
                current[2].append((lineno, text))
        if current is not None:
            anchor, line, collected = current
            if anchor in self.sections:
                self.duplicate_sections.append((line, anchor))
            else:
                self.sections[anchor] = Section(anchor, line, collected)

    # ---------- 查询 ----------
    def line_of(self, key: str, default: int = 1) -> int:
        return self.fm_lines.get(key, default)

    def section(self, anchor: str) -> Section | None:
        return self.sections.get(anchor)

    def status(self) -> str:
        return self.fm.get("状态", "")

    def na_reason(self) -> str:
        return self.fm.get("不适用", "-")

    def is_na(self) -> bool:
        reason = self.na_reason()
        return reason not in ("-", "", "无")

    def signoff(self) -> str:
        return self.fm.get("签收", "-")


# --------------------------------------------------------------------------
# 通用判据
# --------------------------------------------------------------------------

def issue(issues: list[Issue], art: Artifact, line: int, message: str) -> None:
    issues.append(Issue(art.name, line, message))


def check_file(issues: list[Issue], run_dir: Path, entry: dict) -> Artifact | None:
    path = run_dir / entry["file"]
    if not path.is_file():
        issues.append(Issue(entry["file"], 0, f"缺少产物文件（阶段 {entry['code']}）"))
        return None
    try:
        return Artifact(path, entry)
    except (OSError, UnicodeError) as exc:
        issues.append(Issue(entry["file"], 1, f"无法读取产物：{exc}"))
        return None


def check_frontmatter(issues: list[Issue], art: Artifact) -> None:
    if art.fm_error:
        line, message = art.fm_error
        issues.append(Issue(art.name, line, message))
        return
    required = ["产物", "阶段", "编号", "状态", "签收", "签收时间", "依据", "修订", "不适用"]
    for key in required:
        if key not in art.fm:
            issue(issues, art, art.line_of("修订", 1), f"frontmatter 缺少字段：{key}")

    if art.fm.get("产物") != art.spec["product"]:
        issue(issues, art, art.line_of("产物"), f"产物字段应为 `{art.spec['product']}`")
    expected_stage = f"{art.spec['code']}-{spec.STAGE_TITLES[art.spec['code']]}"
    if art.fm.get("阶段") != expected_stage:
        issue(issues, art, art.line_of("阶段"), f"阶段字段应为 `{expected_stage}`")

    number = art.fm.get("编号", "")
    if not re.match(rf"^{art.spec['prefix']}-\d{{4}}$", number):
        issue(issues, art, art.line_of("编号"), f"编号应为 `{art.spec['prefix']}-0001` 形式，当前为 `{number}`")

    status = art.fm.get("状态", "")
    if status not in spec.STATUSES:
        issue(issues, art, art.line_of("状态"), f"状态取值非法：`{status}`，允许 {list(spec.STATUSES)}")

    revised = art.fm.get("修订", "")
    if not revised.isdigit() or int(revised) < 1:
        issue(issues, art, art.line_of("修订"), f"修订必须是从 1 开始的整数，当前为 `{revised}`")

    depends = art.fm.get("依据", "")
    expected = art.spec["depends"] or "-"
    if depends != expected:
        issue(issues, art, art.line_of("依据"), f"依据应为 `{expected}`（阶段顺序不可跳）")


def check_anchors(issues: list[Issue], art: Artifact) -> None:
    for anchor in spec.ANCHORS[art.spec["product"]]:
        if anchor not in art.sections:
            issue(issues, art, 1, f"缺少固定标题：## {anchor}")
    for line, anchor in art.duplicate_sections:
        issue(issues, art, line, f"重复的固定标题：## {anchor}")


def check_dependency(issues: list[Issue], run_dir: Path, entry: dict, loaded: dict[str, Artifact]) -> None:
    for depends in spec.dependencies(entry):
        art = loaded.get(depends)
        if art is None:
            issues.append(Issue(entry["file"], 1, f"依赖的产物不存在或无法读取：{depends}"))
        elif art.status() != "已冻结":
            issues.append(Issue(entry["file"], 1,
                                f"依赖的产物未冻结：{depends} 当前状态 `{art.status() or '未知'}`"))


def check_status(issues: list[Issue], art: Artifact, human_required: bool | None) -> None:
    status = art.status()
    if status == "已废弃":
        if not re.search(r"^废弃理由[:：]\s*\S", art.raw, re.M):
            issue(issues, art, art.line_of("状态"), "已废弃的产物必须补一行 `废弃理由: <原因>`")
        return
    if status != "已冻结":
        return

    sign = art.signoff()
    if sign in ("", SIGN_OFF_NA):
        issue(issues, art, art.line_of("签收"), "已冻结的产物必须填写签收人")
    elif human_required is True and sign == spec.SIGNOFF_MACHINE:
        issue(issues, art, art.line_of("签收"), "本阶段必须由人签收，不能填 `机器门禁`")

    date = art.fm.get("签收时间", "")
    if not DATE_RE.match(date):
        issue(issues, art, art.line_of("签收时间"), f"签收时间必须是 YYYY-MM-DD，当前为 `{date}`")


def na_check(issues: list[Issue], art: Artifact) -> bool:
    """整份不适用的校验；返回 True 表示可跳过内容检查。"""
    if not art.is_na():
        return False
    if not art.spec["na_allowed"]:
        issue(issues, art, art.line_of("不适用"), f"阶段 {art.spec['code']} 不允许整份不适用")
        return False
    reason = art.na_reason()
    if len(reason) < 4:
        issue(issues, art, art.line_of("不适用"), f"不适用必须写清理由（至少 4 个字），当前为 `{reason}`")
        return False
    if art.status() != "已冻结":
        issue(issues, art, art.line_of("状态"), "整份不适用的产物也必须冻结后才能进入下一阶段")
        return False
    if art.signoff() in ("", SIGN_OFF_NA, spec.SIGNOFF_MACHINE):
        issue(issues, art, art.line_of("签收"), "整份不适用必须有人签收确认")
    return True


def section_ok(issues: list[Issue], art: Artifact, anchor: str) -> Section | None:
    """取锚点并要求非空（允许节内写 `不适用：理由`）。"""
    sec = art.section(anchor)
    if sec is None:
        return None
    if sec.empty:
        issue(issues, art, sec.line, f"## {anchor} 内容为空；不适用时写 `不适用：<理由>`")
        return None
    stripped = sec.text.strip()
    if stripped.startswith("不适用"):
        reason = stripped.split("不适用", 1)[1].strip(" ：:-—")
        if len(reason) < 3:
            issue(issues, art, sec.first_line(), f"## {anchor} 写了不适用但没有理由")
    return sec


def is_section_na(sec: Section | None) -> bool:
    return sec is not None and sec.text.strip().startswith("不适用") and "不适用" in sec.text


def need_table(issues: list[Issue], art: Artifact, sec: Section, anchor: str,
               min_rows: int = 1) -> Table | None:
    tables = sec.tables()
    if not tables:
        issue(issues, art, sec.line, f"## {anchor} 缺少表格（表头行 + 分隔行 + 数据行）")
        return None
    table = tables[0]
    if len(table.rows) < min_rows:
        issue(issues, art, table.line, f"## {anchor} 表格至少需要 {min_rows} 行数据，当前 {len(table.rows)} 行")
        return None
    return table


def rows_where_filled(issues: list[Issue], art: Artifact, table: Table, columns: list[str],
                      anchor: str) -> list[Row]:
    """返回所有指定列都非空的表格行；缺列的列报错一次。"""
    for col in columns:
        if col not in table.header:
            issue(issues, art, table.line, f"## {anchor} 表格缺少列：`{col}`（现有列：{table.header}）")
            return []
    filled = []
    for row in table.rows:
        missing = [c for c in columns if not table.cell(row, c) or table.cell(row, c) in ("-", "")]
        if missing:
            issue(issues, art, row.line, f"表格行缺少取值：{missing}")
            continue
        filled.append(row)
    return filled


def heading_level3_titles(sec: Section) -> list[str]:
    return [text[4:].strip() for _, text, _ in sec.blocks("")]


def find_heading(art: Artifact, anchor: str) -> Section | None:
    return art.section(anchor)


def count_h3(sec: Section) -> int:
    return sum(1 for _, text in sec.lines if text.startswith("### "))


def freeze_required_human(art: Artifact) -> bool | None:
    """返回 True/False 表示是否需要人签收；None 表示由调用方决定。"""
    if art.spec["signoff"] == "human":
        return True
    return None


def require_h3(issues: list[Issue], art: Artifact, sec: Section, titles: list[str]) -> dict[str, list[tuple[int, str]]]:
    """要求节内存在指定三级标题，且正文非空。返回 title -> 内容行。"""
    found = {title: lines for _, title, lines in sec.blocks("")}
    result: dict[str, list[tuple[int, str]]] = {}
    for title in titles:
        if title not in found:
            issue(issues, art, sec.line, f"## {sec.anchor} 缺少三级标题：### {title}")
            continue
        lines = found[title]
        content = "\n".join(t for _, t in lines).strip()
        if not content:
            issue(issues, art, sec.line, f"### {title} 内容为空")
            continue
        result[title] = lines
    return result


def only_none(text: str) -> bool:
    """判断内容是否为「无 / 无：理由」这类空结论。"""
    stripped = text.strip()
    if not stripped:
        return True
    first = stripped.splitlines()[0].strip()
    return first == "无" or first.startswith("无：") or first.startswith("无:")


def block_text(lines: list[tuple[int, str]]) -> str:
    return "\n".join(t for _, t in lines).strip()


def verdict(art: Artifact, anchor: str, choices: tuple[str, ...]) -> str | None:
    """只接受整行明确选定的结论，拒绝未选择的模板和多重结论。"""
    sec = art.section(anchor)
    if sec is None:
        return None
    values = re.findall(r"^\s*(?:-\s*)?结论[:：]\s*(.*?)\s*$", sec.text, re.M)
    return values[0] if len(values) == 1 and values[0] in choices else None


def section_missing_in(issues: list[Issue], art: Artifact, anchor: str) -> None:
    issue(issues, art, 1, f"缺少固定标题：## {anchor}")

