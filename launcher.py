"""Greyola CRM — native Windows app launcher.

Hosts the CRM (self-contained HTML/JS) inside a native Edge WebView2 window
via pywebview. Data persists to  %LOCALAPPDATA%\\Greyola CRM\\  so the app keeps
your deals/contacts/messages across restarts and updates.
"""

import os
import json
import shutil
import webview

# ---------------------------------------------------------------------------
# Embed the CRM front-end (read from the source file at build time).
# ---------------------------------------------------------------------------
def _read_html():
    """Locate the CRM interface file in both dev and PyInstaller-bundled runs."""
    here = os.path.dirname(os.path.abspath(__file__))
    # 1) PyInstaller bundles data next to the frozen exe / in _MEIPASS.
    if getattr(sys, 'frozen', False):
        candidates = [
            os.path.join(getattr(sys, '_MEIPASS', ''), 'assets', 'crm.html'),
            os.path.join(here, 'assets', 'crm.html'),
        ]
    else:
        # 2) Dev: look in app/assets then repo root.
        candidates = [
            os.path.join(here, 'assets', 'crm.html'),
            os.path.join(here, '..', 'Greyola CRM.html'),
            os.path.join(here, 'Greyola CRM.html'),
        ]
    for c in candidates:
        try:
            with open(c, 'r', encoding='utf-8') as _f:
                return _f.read()
        except (FileNotFoundError, OSError):
            continue
    return ("<h1 style='font-family:sans-serif;padding:2rem'>"
            "Greyola CRM could not find its interface file.</h1>")


import sys
HTML = _read_html()


# ---------------------------------------------------------------------------
# JS bridge: real on-disk persistence in %LOCALAPPDATA%\Greyola CRM\
# ---------------------------------------------------------------------------
class StorageBridge:
    def __init__(self):
        self.dir = os.path.join(os.environ.get('LOCALAPPDATA',
                                               os.path.expanduser('~')),
                                'Greyola CRM')
        os.makedirs(self.dir, exist_ok=True)
        self._cache = {}

    def _path(self, key):
        return os.path.join(self.dir, key.replace('/', '_') + '.json')

    def load(self, key):
        p = self._path(key)
        if key in self._cache:
            return self._cache[key]
        if not os.path.exists(p):
            return None
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = f.read()
            self._cache[key] = data
            return data
        except Exception:
            return None

    def save(self, key, value):
        p = self._path(key)
        try:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(value)
            self._cache[key] = value
            return True
        except Exception:
            return False

    def remove(self, key):
        p = self._path(key)
        self._cache.pop(key, None)
        try:
            if os.path.exists(p):
                os.remove(p)
            return True
        except Exception:
            return False


def main():
    bridge = StorageBridge()
    window = webview.create_window(
        'Greyola CRM',
        html=HTML,
        js_api=bridge,
        width=1280,
        height=820,
        min_size=(900, 620),
        text_select=True,
        confirm_close=False,
    )
    # Native window icon is set via the build; nothing else needed here.
    webview.start(debug=False, gui='edgechromium')


if __name__ == '__main__':
    main()
