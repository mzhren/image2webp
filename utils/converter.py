import os
import subprocess
import shutil
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PIL import Image

class ConversionWorker(QThread):
    """在单独线程中执行图片转换的工作线程"""
    
    progress_updated = pyqtSignal(int, int, str)  # 当前进度, 总数, 文件名
    finished = pyqtSignal(int, int)  # 成功数量, 失败数量
    
    def __init__(self, image_files, output_dir, settings):
        super().__init__()
        self.image_files = image_files
        self.output_dir = output_dir
        self.settings = settings
        self.success_count = 0
        self.fail_count = 0
        
    def run(self):
        total = len(self.image_files)
        
        for i, file_path in enumerate(self.image_files, 1):
            try:
                self.progress_updated.emit(i, total, file_path)
                self.convert_image(file_path)
                self.success_count += 1
            except Exception as e:
                print(f"转换失败: {file_path}, 错误: {str(e)}")
                self.fail_count += 1
                
        self.finished.emit(self.success_count, self.fail_count)
        
    def convert_image(self, file_path):
        """转换单个图像文件"""
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_file = os.path.join(self.output_dir, name_without_ext + ".webp")
        
        # 检查是否需要预处理（如调整大小）
        if self.settings["resize"]:
            # 使用PIL进行图像大小调整
            img = Image.open(file_path)
            
            if self.settings["maintain_aspect"]:
                # 计算维持宽高比的新尺寸
                width, height = img.size
                target_width = self.settings["width"]
                target_height = self.settings["height"]
                
                ratio = min(target_width / width, target_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
            else:
                img = img.resize(
                    (self.settings["width"], self.settings["height"]),
                    Image.LANCZOS
                )
                
            # 保存临时文件
            temp_file = os.path.join(self.output_dir, "temp_" + filename)
            img.save(temp_file)
            file_path = temp_file
            
        # 检查cwebp是否可用
        if shutil.which('cwebp'):
            # 构建cwebp命令
            cmd = ['cwebp']
            
            if self.settings["lossless"]:
                cmd.append('-lossless')
            else:
                cmd.extend(['-q', str(self.settings["quality"])])
                
            # 使用固定的方法 (默认值4)
            cmd.extend(['-m', '4'])
            cmd.extend([file_path, '-o', output_file])
            
            # 执行命令
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"cwebp 转换失败: {result.stderr}")
        else:
            # 如果cwebp不可用，回退到PIL
            img = Image.open(file_path)
            img.save(output_file, 'webp', 
                     quality=self.settings["quality"], 
                     lossless=self.settings["lossless"],
                     method=4)  # 使用固定的方法 (默认值4)
            
        # 清理临时文件
        if self.settings["resize"] and file_path.startswith(os.path.join(self.output_dir, "temp_")):
            try:
                os.remove(file_path)
            except:
                pass

class WebPConverter(QObject):
    """WebP 图片转换器"""
    
    progress_updated = pyqtSignal(int, int, str)  # 当前进度, 总数, 文件名
    conversion_finished = pyqtSignal(int, int)  # 成功数量, 失败数量
    
    def __init__(self):
        super().__init__()
        self.worker = None
        
    def convert_images(self, image_files, output_dir, settings):
        """
        开始图片转换
        
        Args:
            image_files: 图片文件路径列表
            output_dir: 输出目录
            settings: 转换参数设置
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建并启动工作线程
        self.worker = ConversionWorker(image_files, output_dir, settings)
        self.worker.progress_updated.connect(self.progress_updated)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.start()
