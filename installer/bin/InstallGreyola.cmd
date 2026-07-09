@ECHO OFF
REM ============================================================================
REM  Greyola CRM — silent installer
REM  Installs the app to %ProgramFiles%\Greyola CRM, adds a Start Menu entry,
REM  a desktop shortcut and an uninstaller. Runs automatically from the
REM  self-extracting package; no user interaction required.
REM ============================================================================

SET "SRC=%~dp0"
SET "APPNAME=Greyola CRM"
SET "INSTALLDIR=%ProgramFiles%\%APPNAME%"
SET "STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\%APPNAME%"

ECHO Installing %APPNAME% to %INSTALLDIR% ...

REM --- create directories ---------------------------------------------------
IF NOT EXIST "%INSTALLDIR%" MKDIR "%INSTALLDIR%"
IF NOT EXIST "%STARTMENU%"   MKDIR "%STARTMENU%"

REM --- copy application -----------------------------------------------------
COPY /Y "%SRC%Greyola CRM.exe" "%INSTALLDIR%\" >NUL
COPY /Y "%SRC%greyola.ico"    "%INSTALLDIR%\" >NUL

REM --- build uninstaller (self-contained batch) -----------------------------
(
  ECHO @ECHO OFF
  ECHO ECHO Uninstalling %APPNAME% ...
  ECHO TASKKILL /F /IM "Greyola CRM.exe" ^>NUL 2^>^&1
  ECHO IF EXIST "%ProgramFiles%\%APPNAME%" RMDIR /S /Q "%ProgramFiles%\%APPNAME%"
  ECHO IF EXIST "%STARTMENU%" RMDIR /S /Q "%STARTMENU%"
  ECHO DEL /F /Q "%%PUBLIC%%\Desktop\%APPNAME%.lnk" 2^>NUL
  ECHO REG DELETE "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /F ^>NUL 2^>^&1
  ECHO ECHO Done.
) > "%INSTALLDIR%\Uninstall.cmd"

REM --- shortcuts ------------------------------------------------------------
SET "WSH=%SystemRoot%\System32\wscript.exe"
CSCRIPT //NoLogo //E:JScript "%SRC%MakeLnk.js" "%INSTALLDIR%\Greyola CRM.exe" "%STARTMENU%\%APPNAME%.lnk" "%INSTALLDIR%\greyola.ico,0" "%INSTALLDIR%"
CSCRIPT //NoLogo //E:JScript "%SRC%MakeLnk.js" "%INSTALLDIR%\Greyola CRM.exe" "%PUBLIC%\Desktop\%APPNAME%.lnk" "%INSTALLDIR%\greyola.ico,0" "%INSTALLDIR%"

REM --- Add/Remove Programs registration -------------------------------------
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "DisplayName"    /T REG_SZ /D "%APPNAME%" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "UninstallString" /T REG_SZ /D "\"%INSTALLDIR%\Uninstall.cmd\"" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "DisplayIcon"    /T REG_SZ /D "\"%INSTALLDIR%\greyola.ico,0\"" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "Publisher"      /T REG_SZ /D "Greyola" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "InstallLocation" /T REG_SZ /D "%INSTALLDIR%" /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "NoModify"       /T REG_DWORD /D 1 /F >NUL
REG ADD "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\%APPNAME%" /V "NoRepair"       /T REG_DWORD /D 1 /F >NUL

ECHO Installation complete.
