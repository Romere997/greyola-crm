"""Smoke test for the Greyola CRM front-end.

- Reads ``Greyola CRM.html`` from the repository root.
- Extracts every ``<script>`` block and runs ``node --check`` on each to catch
  syntax errors in the bundled JavaScript.
- Asserts the HTML contains the required navigation view ids.

``node`` must be on PATH (it is on the Windows build machine and in CI).
"""

import os
import re
import subprocess
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(REPO_ROOT, "Greyola CRM.html")

REQUIRED_VIEW_IDS = [
    "view-overview",
    "view-contacts",
    "view-deals",
    "view-analytics",
    "view-messages",
    "view-calendar",
    "view-settings",
]


def _read_html():
    with open(HTML_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


def _extract_script_blocks(html):
    """Return a list of inline <script> bodies (no src attribute)."""
    blocks = []
    # Match <script ...>...</script>, non-greedy, dotall. Skip <script src=...>.
    for m in re.finditer(
        r"<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.DOTALL | re.IGNORECASE
    ):
        blocks.append(m.group(1))
    return blocks


def test_html_exists():
    assert os.path.isfile(HTML_PATH), f"Missing front-end HTML at {HTML_PATH}"


def test_required_view_ids_present():
    html = _read_html()
    missing = [vid for vid in REQUIRED_VIEW_IDS if vid not in html]
    assert not missing, f"Missing required view ids: {missing}"


def test_script_blocks_pass_node_check():
    html = _read_html()
    blocks = _extract_script_blocks(html)
    assert blocks, "No inline <script> blocks found in front-end HTML"

    # Ensure node is available.
    try:
        subprocess.run(
            ["node", "--version"], check=True, capture_output=True, text=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"node not available on PATH: {exc}")

    failed = []
    with tempfile.TemporaryDirectory() as tmp:
        for idx, block in enumerate(blocks):
            js_path = os.path.join(tmp, f"block_{idx}.js")
            with open(js_path, "w", encoding="utf-8") as fh:
                fh.write(block)
            result = subprocess.run(
                ["node", "--check", js_path],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                failed.append((idx, result.stderr.strip()))

    assert not failed, (
        "JavaScript syntax errors in front-end:\n"
        + "\n".join(f"[block {i}] {err}" for i, err in failed)
    )
