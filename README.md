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
- Local persistence (deals, messages, settings) via a storage bridge into
  `%LOCALAPPDATA%\Greyola CRM\`

## Repository layout
| Path | Purpose |
|------|---------|
| `Greyola CRM.html` | The entire app (HTML + CSS + JS). This is the source of truth. |
| `launcher.py` | pywebview wrapper that loads the HTML in a native window |
| `build.spec` | PyInstaller single-file, windowed build spec |
| `make_icon.py` | Generates `greyola.ico` |
| `installer/` | iexpress-based installer (Start Menu + desktop shortcut + uninstaller) |
| `assets/crm.html` | Copy of the source, bundled into the `.exe` at build time |

## Building the Windows app
```bash
pip install pywebview pyinstaller pillow
cp "Greyola CRM.html" assets/crm.html
python -m PyInstaller build.spec --noconfirm --clean
# result: dist/Greyola CRM.exe
```

## Building the installer
```bash
cp dist/"Greyola CRM.exe" installer/payload/
iexpress.exe /N installer/GreyolaCRM.sed
# result: Greyola CRM Setup.exe on the Desktop
```

## License
MIT
