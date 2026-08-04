#!/usr/bin/env python3
"""Apply the two standing production patches to a fresh TextMaxx delivery.

Patches:
  1. Tabler Icons <link> in <head> — needed because the client's HTML uses 40
     `ti ti-*` icon classes but doesn't link the Tabler webfont. Without this
     link, all 40 icons render as blank rectangles.
  2. Phone field on the Request Demo form + `phone:` in the JS payload — added
     2026-07-07 per Chris and Dave (Head of Sales). The client's HTML keeps
     shipping without it.

Idempotent: if a patch is already present, that patch is skipped. Safe to run
multiple times.

Fails loud (non-zero exit) if an expected anchor pattern isn't found, so we
notice immediately if the client's HTML template shifts.

Usage:
  python3 apply-patches.py               # patches ./index.html in place
  python3 apply-patches.py path/to.html  # patches that file in place
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patch 1 — Tabler Icons <link>
# ---------------------------------------------------------------------------
GOOGLE_FONTS_LINE = (
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:'
    'wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap"'
    ' rel="stylesheet">'
)
TABLER_LINK_LINE = (
    '<link href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3/dist/'
    'tabler-icons.min.css" rel="stylesheet">'
)
TABLER_SENTINEL = "tabler-icons.min.css"

# ---------------------------------------------------------------------------
# Patch 2 — Phone <input> in the demo form
# The client's form has fields in order: Name, Email, Company, Message.
# We insert Phone as a new <div> block after Company's closing </div>.
# ---------------------------------------------------------------------------
COMPANY_BLOCK_END = (
    '<input type="text" id="tf-company" name="company" '
    'style="width:100%; padding:12px 14px; border:1px solid var(--gray-mid); '
    "border-radius: var(--radius); font-family:'Source Sans 3', sans-serif; "
    'font-size:15px;">'
)
PHONE_BLOCK = """
      </div>
      <div>
        <label style="display:block; font-size:13px; font-weight:600; margin-bottom:6px; color: var(--ink);">Phone</label>
        <input type="tel" id="tf-phone" name="phone" required style="width:100%; padding:12px 14px; border:1px solid var(--gray-mid); border-radius: var(--radius); font-family:'Source Sans 3', sans-serif; font-size:15px;">"""
PHONE_FIELD_SENTINEL = 'id="tf-phone"'

# ---------------------------------------------------------------------------
# Patch 3 — Phone entry in the JS submit payload
# Existing payload lines are name/email/company/message; we insert phone
# between company and message so the JSON key order stays intuitive.
# ---------------------------------------------------------------------------
COMPANY_PAYLOAD_LINE = (
    "            company: document.getElementById('tf-company').value,"
)
PHONE_PAYLOAD_LINE = (
    "            phone: document.getElementById('tf-phone').value,"
)
PHONE_PAYLOAD_SENTINEL = "phone: document.getElementById('tf-phone')"


def replace_once(text: str, needle: str, replacement: str, label: str) -> str:
    """Replace `needle` with `replacement` — must occur exactly once."""
    count = text.count(needle)
    if count == 0:
        print(f"  [FAIL] {label}: anchor pattern not found in file", file=sys.stderr)
        print(f"         anchor was: {needle[:80]!r}...", file=sys.stderr)
        sys.exit(2)
    if count > 1:
        print(f"  [FAIL] {label}: anchor pattern found {count} times, expected 1", file=sys.stderr)
        sys.exit(2)
    return text.replace(needle, replacement)


def apply_patches(html: str) -> tuple[str, list[str]]:
    changed: list[str] = []

    # Patch 1 — Tabler <link>
    if TABLER_SENTINEL in html:
        print("  [skip] Tabler <link> already present")
    else:
        html = replace_once(
            html,
            GOOGLE_FONTS_LINE,
            GOOGLE_FONTS_LINE + "\n" + TABLER_LINK_LINE,
            label="Tabler <link>",
        )
        changed.append("Tabler <link>")
        print("  [added] Tabler <link> inserted after Google Fonts")

    # Patch 2 — Phone field
    if PHONE_FIELD_SENTINEL in html:
        print("  [skip] Phone field already present")
    else:
        html = replace_once(
            html,
            COMPANY_BLOCK_END,
            COMPANY_BLOCK_END + PHONE_BLOCK,
            label="Phone <div>",
        )
        changed.append("Phone field")
        print("  [added] Phone <div> inserted after Company field")

    # Patch 3 — Phone in JS payload
    if PHONE_PAYLOAD_SENTINEL in html:
        print("  [skip] phone in JS payload already present")
    else:
        html = replace_once(
            html,
            COMPANY_PAYLOAD_LINE,
            COMPANY_PAYLOAD_LINE + "\n" + PHONE_PAYLOAD_LINE,
            label="phone: in JS payload",
        )
        changed.append("Phone payload")
        print("  [added] phone: inserted into JS payload")

    return html, changed


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    if not target.exists():
        print(f"[FAIL] file not found: {target}", file=sys.stderr)
        sys.exit(1)

    print(f"Patching {target}...")
    original = target.read_text(encoding="utf-8")
    patched, changed = apply_patches(original)

    if patched == original:
        print("No changes — all patches already applied.")
        return

    target.write_text(patched, encoding="utf-8")
    print(f"Patched {target}: {', '.join(changed)}")


if __name__ == "__main__":
    main()
