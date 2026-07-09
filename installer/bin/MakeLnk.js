// MakeLnk.js — creates a Windows shortcut (.lnk).
// Usage: cscript //NoLogo //E:JScript MakeLnk.js "<target>" "<lnkPath>" "<icon>" "<workdir>"
var args = WScript.Arguments;
if (args.Length < 2) { WScript.Quit(1); }
var target  = args(0);
var lnkPath = args(1);
var icon    = (args.Length > 2) ? args(2) : "";
var workdir = (args.Length > 3) ? args(3) : "";

var WshShell = new ActiveXObject("WScript.Shell");
var lnk = WshShell.CreateShortcut(lnkPath);
lnk.TargetPath = target;
if (workdir !== "") lnk.WorkingDirectory = workdir;
if (icon !== "")   lnk.IconLocation = icon;
lnk.Description = "Greyola CRM";
lnk.Save();
WScript.Quit(0);
