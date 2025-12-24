# 创建桌面快捷方式脚本
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Personal RAG 应用.lnk')
$Shortcut.TargetPath = 'powershell.exe'
$Shortcut.Arguments = '-ExecutionPolicy Bypass -NoExit -Command "cd D:\pycharm\project\personal\personal_RAG; streamlit run app.py"'
$Shortcut.WorkingDirectory = 'D:\pycharm\project\personal\personal_RAG'
$Shortcut.Description = '启动Personal RAG知识库问答系统'
$Shortcut.Save()
Write-Host 'Shortcut created.'