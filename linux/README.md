# Greyola CRM — Linux

A native Linux build of the Greyola CRM desktop app, using
[pywebview](https://pywebview.flowrl.com/) with the **GTK / WebKit2** backend
(no bundled browser — it uses the system's WebKitGTK).

## System dependencies (install once)

pywebview on Linux needs the WebKit2 GTK libraries:

```bash
# Debian / Ubuntu
sudo apt update
sudo apt install -y python3-pip python3-venv \
     libwebkit2gtk-4.1-dev libgtk-3-dev gir1.2-webkit2-4.1

# Fedora
sudo dnf install -y python3-pip gtk3-devel webkit2gtk4.1-devel

# Arch
sudo pacman -Syu python-pip gtk3 webkit2gtk-4.1
```

> Use `webkit2gtk-4.1` (GTK 3) — it matches the pywebview GTK backend.

## Build the executable

```bash
cd linux
bash build_linux.sh
# -> dist/greyola-crm   (single Linux binary, no console window)
```

Or manually:

```bash
cd linux
cp "../Greyola CRM.html" assets/crm.html
pip install -r requirements.txt
pyinstaller build_linux.spec --noconfirm --clean
```

## Run (from source, no build)

```bash
cd linux
pip install -r requirements.txt
cp "../Greyola CRM.html" assets/crm.html
python linux_launcher.py
```

## Packaging as an AppImage (optional)

The one-file binary from PyInstaller works standalone, but to ship a
distro-agnostic AppImage:

```bash
# install appimage tooling
pip install appimage-builder  # or use linuxdeploy + AppImageKit

# example appimage-builder.yml (summary)
# app: greyola-crm
#   bins: [dist/greyola-crm]
#   apt: [libwebkit2gtk-4.1-0, libgtk-3-0]
# then: appimage-builder --recipe AppImageBuilder.yml
```

A ready `AppImageBuilder.yml` can be added on request.

## Data & persistence

Your deals, messages, and settings are stored under:

```
$XDG_DATA_HOME/Greyola CRM/      (usually ~/.local/share/Greyola CRM/)
```

This keeps your data separate from the app and safe across updates.

## Notes

- `linux_launcher.py` mirrors the Windows `launcher.py` but uses the GTK backend
  and XDG data directories instead of Edge WebView2 / `%LOCALAPPDATA%`.
- The front-end (`Greyola CRM.html`) is shared with the Windows build — the same
  single source of truth lives in the repo root.
