#!/usr/bin/env python3
"""
打包 Image2WebP 为 macOS 应用程序
"""
import os
import subprocess
import shutil
import platform

def main():
    print("开始打包 Image2WebP 应用...")
    
    # 确保在 macOS 上运行
    if platform.system() != "Darwin":
        print("错误: 此脚本只能在 macOS 上运行")
        return
    
    # 安装依赖
    print("安装必要依赖...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    subprocess.run(["pip", "install", "pyinstaller"])
    
    # 创建打包目录
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # 准备图标
    icon_path = "resources/icon.icns"
    if not os.path.exists(icon_path):
        print("警告: 未找到图标文件, 将使用默认图标")
        icon_path = None
    
    # 构建 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--name=Image2WebP",
        "--windowed",  # 无控制台窗口
        "--onefile",  # 打包成单个文件
        "--noconfirm",  # 覆盖已存在的输出目录
        "--clean",  # 清理临时文件
    ]
    
    # 添加图标(如果存在)
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    # 添加主脚本和额外数据
    cmd.extend([
        "--add-data=resources:resources",
        "main.py"
    ])
    
    # 执行打包
    print("执行打包命令...")
    subprocess.run(cmd)
    
    # 检查打包结果
    app_path = "dist/Image2WebP.app"
    if os.path.exists(app_path):
        print(f"打包成功! 应用位于: {os.path.abspath(app_path)}")
        print("您可以将此应用复制到 Applications 文件夹或者直接运行。")
    else:
        print("打包失败，请检查错误信息。")

if __name__ == "__main__":
    main()
