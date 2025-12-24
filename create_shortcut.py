import os
import win32com.client

# 创建快捷方式的函数
def create_shortcut():
    try:
        # 获取桌面路径
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_path = os.path.join(desktop_path, 'Personal RAG 应用.lnk')
        
        # 创建WScript Shell对象
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        
        # 设置快捷方式属性
        shortcut.TargetPath = 'powershell.exe'
        shortcut.Arguments = '-ExecutionPolicy Bypass -NoExit -Command "cd D:\\pycharm\\project\\personal\\personal_RAG; streamlit run app.py"'
        shortcut.WorkingDirectory = 'D:\\pycharm\\project\\personal\\personal_RAG'
        shortcut.Description = '启动Personal RAG知识库问答系统'
        
        # 保存快捷方式
        shortcut.Save()
        
        print(f"快捷方式已成功创建到桌面: {shortcut_path}")
        return True
    except Exception as e:
        print(f"创建快捷方式时出错: {str(e)}")
        # 如果win32com不可用，提供备用方法
        print("\n备选方法：请手动创建快捷方式")
        print("1. 右键点击桌面 -> 新建 -> 快捷方式")
        print("2. 输入以下内容作为位置:")
        print('   powershell.exe -ExecutionPolicy Bypass -NoExit -Command "cd D:\\pycharm\\project\\personal\\personal_RAG; streamlit run app.py"')
        print("3. 点击下一步，输入名称'Personal RAG 应用'")
        print("4. 点击完成")
        return False

# 主程序
if __name__ == "__main__":
    print("开始创建Personal RAG应用的桌面快捷方式...")
    create_shortcut()
    print("\n按任意键退出...")
    input()