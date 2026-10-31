#!/usr/bin/env bash
# 为一个需求创建运行目录，并铺好 9 份产物模板。
# 用法：./scripts/init-docs.sh <需求slug>
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
slug="${1:-}"

if [ -z "$slug" ]; then
  echo "用法: $0 <需求slug，kebab-case，例如 coupon-import>" >&2
  exit 2
fi

if [[ ! "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "slug 必须是 kebab-case（小写字母、数字、连字符），当前为：$slug" >&2
  exit 2
fi

project_root="$(pwd)"
target="$project_root/docs/engineering/$slug"

if [ -e "$target" ]; then
  echo "运行目录已存在：$target" >&2
  echo "如需重开，请先移除或换一个 slug。" >&2
  exit 1
fi

mkdir -p "$target"

copy_template() {
  local src="$1" dst="$2"
  if [ ! -f "$REPO_ROOT/templates/$src" ]; then
    echo "模板缺失：templates/$src" >&2
    exit 1
  fi
  cp "$REPO_ROOT/templates/$src" "$target/$dst"
}

copy_template 01-requirements.md   01-requirements.md
copy_template 02-design.md          02-design.md
copy_template 03-ui-design.md       03-ui-design.md
copy_template 04-tasks.md           04-tasks.md
copy_template 05-implementation.md  05-implementation.md
copy_template 06-test-report.md     06-test-report.md
copy_template 06-review-report.md   06-review-report.md
copy_template 07-delivery.md        07-delivery.md
copy_template 08-retro.md           08-retro.md

python3 - "$project_root" "$slug" <<'PY'
import datetime
import pathlib
import sys

project_root = pathlib.Path(sys.argv[1])
slug = sys.argv[2]
index = project_root / "docs" / "engineering" / "README.md"
today = datetime.date.today().isoformat()

header = (
    "# 需求运行目录\n\n"
    "每个需求一个目录，产物由 `gates/run.py` 校验。新增目录用 "
    "`scripts/init-docs.sh <slug>`。\n\n"
    "| 需求 | 状态 | 创建时间 | 备注 |\n|---|---|---|---|\n"
)

if index.exists():
    text = index.read_text(encoding="utf-8")
    if slug not in text:
        text = text.rstrip("\n") + f"\n| {slug} | 进行中 | {today} |  |\n"
        index.write_text(text, encoding="utf-8")
else:
    index.write_text(header + f"| {slug} | 进行中 | {today} |  |\n", encoding="utf-8")
PY

echo "已创建：$target"
echo
echo "下一步："
echo "  1) 在 agent 里说：用 org-requirements 开始处理 $slug"
echo "  2) 写完一段就跑：python3 gates/run.py docs/engineering/$slug --stage 01"
echo "  3) 全部完成后跑：python3 gates/run.py docs/engineering/$slug --all"
