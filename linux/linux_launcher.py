"""Greyola CRM — native Linux app launcher.

Hosts the CRM (self-contained HTML/JS) inside a native WebView window via
pywebview. On Linux pywebview uses the GTK/WebKit2 backend (no bundled
browser needed — it uses the system's WebKitGTK). Data persists to
``~/.local/share/Greyola CRM/`` so the app keeps your deals/contacts/messages
across restarts and updates.

Build a one-file executable with:

    pip install pywebview pyinstaller
    cp "../Greyola CRM.html" assets/crm.html
    pyinstaller build_linux.spec --noconfirm --clean
    # -> dist/greyola-crm
"""

import os
import sys
import webview

# Greyola CRM release version (bumped per CHANGELOG.md).
APP_VERSION = '1.1.0'


# ---------------------------------------------------------------------------
# Locate the CRM front-end (read from the source file at build time).
# ---------------------------------------------------------------------------
def _read_html():
    here = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        candidates = [
            os.path.join(getattr(sys, '_MEIPASS', ''), 'assets', 'crm.html'),
            os.path.join(here, 'assets', 'crm.html'),
        ]
    else:
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


HTML = _read_html()


# ---------------------------------------------------------------------------
# JS bridge: real on-disk persistence in $XDG_DATA_HOME/Greyola CRM/
# ---------------------------------------------------------------------------
class StorageBridge:
    def __init__(self):
        xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
        self.dir = os.path.join(xdg, 'Greyola CRM')
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
    # On Linux pywebview auto-selects the GTK/WebKit2 backend; forcing it is
    # optional and can mask missing system libs, so we let it auto-detect.
    webview.start(debug=False)


if __name__ == '__main__':
    main()
