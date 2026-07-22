@ECHO OFF
REM ============================================================================
REM  Greyola CRM v1.1.0 — silent installer
REM  Installs the app to %ProgramFiles%\Greyola CRM, adds a Start Menu entry,
REM  a desktop shortcut and an uninstaller. Runs automatically from the
REM  self-extracting package; no user interaction required.
REM ============================================================================

SET "SRC=%~dp0"
SET "APPNAME=Greyola CRM"
SET "VERSION=1.1.0"
SET "INSTALLDIR=%ProgramFiles%\%APPNAME%"
SET "STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\%APPNAME%"
SET "DESKTOPLNK=%PUBLIC%\Desktop\%APPNAME%.lnk"
SET "STARTMENULNK=%STARTMENU%\%APPNAME%.lnk"

ECHO Installing %APPNAME% %VERSION% to %INSTALLDIR% ...

REM --- WebView2 runtime check ------------------------------------------------
REM  Greyola CRM uses the Edge WebView2 control. If it is missing the app will
REM  fail to launch, so warn the user (and the admin log) up front.
SET "WEBVIEW2_OK=0"
REG QUERY "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A08C11}" >NUL 2>&1 && SET "WEBVIEW2_OK=1"
REG QUERY "HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A08C11}" >NUL 2>&1 && SET "WEBVIEW2_OK=1"
REG QUERY "HKCU\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A08C11}" >NUL 2>&1 && SET "WEBVIEW2_OK=1"
IF "%WEBVIEW2_OK%"=="0" (
    ECHO.
    ECHO [WARNING] The Microsoft Edge WebView2 runtime was not detected.
    ECHO           Greyola CRM needs it to run. Please install the "Evergreen
    ECHO           Bootstrapper" from:
    ECHO.
    ECHO           https://developer.microsoft.com/microsoft-edge/webview2/
    ECHO.
    ECHO           Continuing the installation, but the app will not start until
    ECHO           WebView2 is present.
    ECHO.
)

REM --- create directories ---------------------------------------------------
IF NOT EXIST "%INSTALLDIR%" MKDIR "%INSTALLDIR%"
IF NOT EXIST "%STARTMENU%"   MKDIR "%STARTMENU%"

REM --- copy application -----------------------------------------------------
COPY /Y "%SRC%Greyola CRM.exe" "%INSTALLDIR%\" >NUL
COPY /Y "%SRC%greyola.ico"    "%INSTALLDIR%\" >NUL

REM --- build uninstaller (self-contained batch) -----------------------------
REM  Paths to created artifacts are written into the uninstaller so removal is
REM  explicit and tracks exactly what we installed.
(
  ECHO @ECHO OFF
  ECHO SET "APPNAME=%APPNAME%"
  ECHO SET "INSTALLDIR=%ProgramFiles%\%APPNAME%"
  ECHO SET "STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\%APPNAME%"
  ECHO SET "DESKTOPLNK=%PUBLIC%\Desktop\%APPNAME%.lnk"
  ECHO SET "STARTMENULNK=%%STARTMENU%%\%APPNAME%.lnk"
  ECHO ECHO Uninstalling %%APPNAME%% ...
  ECHO TASKKILL /F /IM "Greyola CRM.exe" ^>NUL 2^>^&1
  ECHO DEL /F /Q "%%DESKTOPLNK%%" 2^>NUL
  ECHO DEL /F /Q "%%STARTMENULNK%%" 2^>NUL
  ECHO IF EXIST "%%STARTMENU%%" RMDIR /S /Q "%%STARTMENU%%"
  ECHO IF EXIST "%%INSTALLDIR%%" RMDIR /S /Q "%%INSTALLDIR%%"
  ECHO REG DELETE "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /F ^>NUL 2^>^&1
  ECHO ECHO Done.
) > "%INSTALLDIR%\Uninstall.cmd"

REM --- shortcuts ------------------------------------------------------------
SET "WSH=%SystemRoot%\System32\wscript.exe"
CSCRIPT //NoLogo //E:JScript "%SRC%MakeLnk.js" "%INSTALLDIR%\Greyola CRM.exe" "%STARTMENULNK%" "%INSTALLDIR%\greyola.ico,0" "%INSTALLDIR%"
CSCRIPT //NoLogo //E:JScript "%SRC%MakeLnk.js" "%INSTALLDIR%\Greyola CRM.exe" "%DESKTOPLNK%" "%INSTALLDIR%\greyola.ico,0" "%INSTALLDIR%"

REM --- Add/Remove Programs registration -------------------------------------
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "DisplayName"    /T REG_SZ /D "%APPNAME%" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "DisplayVersion" /T REG_SZ /D "%VERSION%" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "Version"       /T REG_DWORD /D 0x1010000 /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "UninstallString" /T REG_SZ /D "\"%INSTALLDIR%\Uninstall.cmd\"" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "QuietUninstallString" /T REG_SZ /D "\"%INSTALLDIR%\Uninstall.cmd\"" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "DisplayIcon"    /T REG_SZ /D "\"%INSTALLDIR%\greyola.ico,0\"" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "Publisher"      /T REG_SZ /D "Greyola" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "InstallLocation" /T REG_SZ /D "%INSTALLDIR%" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "NoModify"       /T REG_DWORD /D 1 /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "NoRepair"       /T REG_DWORD /D 1 /F >NUL

ECHO Installation complete.
