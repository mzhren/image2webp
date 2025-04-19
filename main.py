import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和打包后的环境"""
    try:
        # PyInstaller创建临时文件夹并将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序名称和组织名称（用于QSettings）
    app.setApplicationName("Image2WebP")
    app.setOrganizationName("YourOrganizationName")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
