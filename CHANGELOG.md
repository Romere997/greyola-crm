# Changelog

All notable changes to the Greyola CRM desktop app are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - 2026-07-22

### Added
- **Deal actions**: Edit, Call, and Email actions directly from deal rows so reps
  can act on a deal without opening a separate screen.
- **Dark mode**: a light/dark theme toggle that persists across restarts.
- **Global search**: a command-palette-style search across deals, contacts, and
  messages (Ctrl/Cmd+K).
- **Won / Lost quick actions**: one-click buttons on each deal to mark it won or
  lost and update the pipeline instantly.
- **Windows + Linux CI**: automated build pipelines producing the Windows
  (`.exe`) and Linux (`greyola-crm`) artifacts.
- **pytest smoke test**: a headless smoke test that verifies the launcher boots
  and the storage bridge loads/saves without errors.
- **Installer hardening**: the Windows installer now verifies the Microsoft Edge
  WebView2 runtime is present (and links to the download if missing), tracks the
  exact Start Menu and desktop shortcut paths for clean removal, and writes the
  install location and explicit version into the Windows Uninstall registry key.

### Changed
- Bumped app version to **1.1.0** (Windows and Linux launchers, build specs, and
  the Windows executable version resource).

[1.1.0]: https://github.com/greyola/greyola-crm/releases/tag/v1.1.0
