@echo off
setlocal

:: 创建WSH脚本内容
set "JSCRIPT=%TEMP%\CreateShortcut.js"

echo var WshShell = WScript.CreateObject("WScript.Shell"); > %JSCRIPT%
echo var Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") + "\\Personal RAG 应用.lnk"); >> %JSCRIPT%
echo Shortcut.TargetPath = "powershell.exe"; >> %JSCRIPT%
echo Shortcut.Arguments = "-ExecutionPolicy Bypass -NoExit -Command \"cd D:\\pycharm\\project\\personal\\personal_RAG; streamlit run app.py\""; >> %JSCRIPT%
echo Shortcut.WorkingDirectory = "D:\\pycharm\\project\\personal\\personal_RAG"; >> %JSCRIPT%
echo Shortcut.Description = "启动Personal RAG知识库问答系统"; >> %JSCRIPT%
echo Shortcut.Save(); >> %JSCRIPT%
echo WScript.Echo("快捷方式已创建到桌面"); >> %JSCRIPT%

:: 执行JScript创建快捷方式
cscript.exe /nologo %JSCRIPT%

:: 清理临时文件
del %JSCRIPT%

echo 操作完成。快捷方式应该已创建在桌面上。
pause