Dim wshShell, fso, loc, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
if WScript.Arguments.Count = 0 then
    loc = fso.GetAbsolutePathName(".")
else
    loc = WScript.Arguments(0)
end if
WScript.Echo loc

cmd = "C:\Users\richi\AppData\Local\Microsoft\WindowsApps\python3.exe " + loc + "\main.py 192.168.1.233 LenovoYoga homeassistant hello"
WScript.Echo cmd

Set wshShell = CreateObject("WScript.Shell")
wshShell.Run cmd