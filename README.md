# Greyola CRM

A self-contained sales / deal-pipeline CRM that runs as a **native Windows desktop app**
(no browser, no console window) — built from a single HTML/JS front-end wrapped with
[pywebview](https://pywebview.flowrl.com/) (Edge WebView2) and packaged with PyInstaller.

## Features
- **Overview** dashboard — KPIs, portfolio breakdown, transaction volume chart
- **Contacts** — searchable customer list
- **Deals** — pipeline table with stages, values, close dates, win %, and an "Add Deal" modal
- **Analytics** — performance breakdown and sparklines
- **Messages** — conversation inbox with unread counts
- **Calendar** — month view plotting each deal's close date as a colored chip, with an
  upcoming-closings side panel
- **Settings** — editable profile, accent-color theming, reduce-motion / compact-density
  toggles, landing-view selection, and data export / clear
- **Dark mode** — automatic / manual theme switching
- **Search** — global search across contacts and deals
- **Cross-platform** — native Windows (Edge WebView2) and Linux (GTK/WebKit2) builds
- Local persistence (deals, messages, settings) via a storage bridge into
  `%LOCALAPPDATA%\Greyola CRM\` (Windows) or `~/.local/share/Greyola CRM/` (Linux)

## Repository layout
| Path | Purpose |
|------|---------|
| `Greyola CRM.html` | The entire app (HTML + CSS + JS). This is the source of truth. |
| `launcher.py` | pywebview wrapper that loads the HTML in a native window |
| `build.spec` | PyInstaller single-file, windowed build spec |
| `make_icon.py` | Generates `greyola.ico` |
| `installer/` | iexpress-based installer (Start Menu + desktop shortcut + uninstaller) |
| `assets/crm.html` | Copy of the source, bundled into the `.exe` at build time |
| `linux/` | Native **Linux** build (GTK/WebKit2 backend) — `linux_launcher.py`, `build_linux.spec`, `build_linux.sh` |

## Building the Windows app
```bash
pip install pywebview pyinstaller pillow
cp "Greyola CRM.html" assets/crm.html
python -m PyInstaller build.spec --noconfirm --clean
# result: dist/Greyola CRM.exe
```

## Building the Linux app
```bash
cd linux
# install system WebKitGTK deps first (see linux/README.md)
bash build_linux.sh
# result: dist/greyola-crm  (single Linux binary)
```
See [linux/README.md](linux/README.md) for distro-specific WebKit2 GTK packages.

## Building the installer
```bash
cp dist/"Greyola CRM.exe" installer/payload/
iexpress.exe /N installer/GreyolaCRM.sed
# result: Greyola CRM Setup.exe on the Desktop
```

## Architecture
Greyola CRM is a **single HTML front-end** (`Greyola CRM.html` — the entire app's
HTML + CSS + JS) wrapped by [pywebview](https://pywebview.flowrl.com/) in a native
desktop window. There is no separate backend server; the page talks to Python through
a small storage bridge for local persistence.

- **Windows** — pywebview uses the **Edge WebView2** (Chromium) backend.
- **Linux** — pywebview uses the **GTK / WebKit2** backend.

Application data (deals, messages, settings) is stored locally:
- Windows: `%LOCALAPPDATA%\Greyola CRM\`
- Linux: `~/.local/share/Greyola CRM/`

The HTML is copied to `assets/crm.html` at build time and bundled into the executable
by PyInstaller (`build.spec` on Windows, `linux/build_linux.spec` on Linux).

## Testing / CI
Two GitHub Actions workflows build and smoke-test the app on every push, PR, and release:

- **`.github/workflows/build-linux.yml`** — builds the one-file `greyola-crm` Linux
  binary (plus an AppImage) on `ubuntu-22.04`.
- **`.github/workflows/build-windows.yml`** — builds `dist/Greyola CRM.exe` on
  `windows-latest`, verifies the binary exists and the bundled HTML contains the
  Calendar view, and attaches the artifact to releases.

A lightweight pytest smoke test lives in `tests/`:

```bash
pytest tests/
```

It extracts the inline `<script>` blocks from `Greyola CRM.html`, runs `node --check`
on each (requires `node` on PATH), and asserts all required view ids
(`view-overview`, `view-contacts`, `view-deals`, `view-analytics`, `view-messages`,
`view-calendar`, `view-settings`) are present.

## License
MIT
