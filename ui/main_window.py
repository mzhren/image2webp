import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QFileDialog, 
                            QProgressBar, QMessageBox, QGroupBox, QListWidget,
                            QSizePolicy)
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QCursor
from ui.settings_widget import SettingsWidget
from utils.converter import WebPConverter

class FileDropArea(QWidget):
    """支持拖放文件的控件，同时可点击选择文件"""
    
    filesDropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("拖放或点击此处选择图片文件", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(100)
        self.setStyleSheet("border: 2px dashed #aaa; border-radius: 5px;")
        layout.addWidget(self.label)
        # 设置光标为手型，提示可点击
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border: 2px dashed #3daee9; border-radius: 5px;")
            
    def dragLeaveEvent(self, event):
        self.setStyleSheet("border: 2px dashed #aaa; border-radius: 5px;")
        
    def dropEvent(self, event: QDropEvent):
        file_paths = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                file_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
                if any(path.lower().endswith(ext) for ext in file_extensions):
                    file_paths.append(path)
                    
        if file_paths:
            self.filesDropped.emit(file_paths)
            
        self.setStyleSheet("border: 2px dashed #aaa; border-radius: 5px;")
         
    def mousePressEvent(self, event):
        """点击区域时打开文件选择对话框"""
        if event.button() == Qt.LeftButton:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "选择图片文件",
                "",
                "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif *.tiff)"
            )
            
            if files:
                self.filesDropped.emit(files)

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.converter = WebPConverter()
        self.file_list = []
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        self.setWindowTitle("图片转WebP工具")
        self.setMinimumSize(800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # 添加文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout(file_group)
        
        # 拖放区域
        self.drop_area = FileDropArea()
        file_layout.addWidget(self.drop_area)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        self.btn_add_files = QPushButton("添加文件")
        self.btn_add_folder = QPushButton("添加文件夹")
        self.btn_clear = QPushButton("清空列表")
        btn_layout.addWidget(self.btn_add_files)
        btn_layout.addWidget(self.btn_add_folder)
        btn_layout.addWidget(self.btn_clear)
        file_layout.addLayout(btn_layout)
        
        # 文件列表 - 减少高度
        self.list_widget = QListWidget()
        # 设置尺寸策略，使列表高度减少10%
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # 设置最大高度为默认高度的90%（减少10%）
        self.list_widget.setMaximumHeight(200)  # 设置一个合理的高度上限
        file_layout.addWidget(self.list_widget)
        
        # 在文件组内添加伸缩因子，以减少文件列表的相对高度
        file_layout.setStretch(0, 1)  # 拖放区域
        file_layout.setStretch(1, 0)  # 按钮区域
        file_layout.setStretch(2, 2)  # 文件列表
        
        main_layout.addWidget(file_group)
        
        # 设置区域
        self.settings_widget = SettingsWidget()
        main_layout.addWidget(self.settings_widget)
        
        # 输出选择和转换按钮一行显示
        output_convert_layout = QHBoxLayout()
        
        # 输出选择部分
        output_layout = QHBoxLayout()
        self.output_label = QLabel("输出目录：")
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        self.btn_output = QPushButton("选择目录")
        
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path, 1)  # 给输出路径更多空间
        output_layout.addWidget(self.btn_output)
        
        # 转换按钮
        self.btn_convert = QPushButton("开始转换")
        self.btn_convert.setMinimumHeight(30)
        self.btn_convert.setMinimumWidth(120)
        
        # 添加到同一行布局
        output_convert_layout.addLayout(output_layout, 3)  # 输出路径部分占用更多空间
        output_convert_layout.addWidget(self.btn_convert, 1)
        
        main_layout.addLayout(output_convert_layout)
        
        # 转换进度
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("准备就绪")
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(progress_layout)
        
        # 设置布局的伸缩因子，控制各部分的比例
        main_layout.setStretch(0, 2)  # 文件选择区域
        main_layout.setStretch(1, 0)  # 设置区域
        main_layout.setStretch(2, 0)  # 输出和转换按钮区域
        main_layout.setStretch(3, 0)  # 进度区域
        
        self.setCentralWidget(central_widget)
        
    def connect_signals(self):
        self.drop_area.filesDropped.connect(self.add_files)
        self.btn_add_files.clicked.connect(self.select_files)
        self.btn_add_folder.clicked.connect(self.select_folder)
        self.btn_clear.clicked.connect(self.clear_files)
        self.btn_output.clicked.connect(self.select_output_dir)
        self.btn_convert.clicked.connect(self.start_conversion)
        self.converter.progress_updated.connect(self.update_progress)
        self.converter.conversion_finished.connect(self.conversion_finished)
        
    def add_files(self, file_paths):
        for path in file_paths:
            if path not in self.file_list:
                self.file_list.append(path)
                self.list_widget.addItem(path)
        
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif *.tiff)"
        )
        self.add_files(files)
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择图片文件夹"
        )
        if folder:
            import glob
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']:
                image_files.extend(glob.glob(os.path.join(folder, ext)))
                image_files.extend(glob.glob(os.path.join(folder, ext.upper())))
            
            self.add_files(image_files)
        
    def clear_files(self):
        self.file_list.clear()
        self.list_widget.clear()
        
    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录"
        )
        if directory:
            self.output_path.setText(directory)
            
    def start_conversion(self):
        if not self.file_list:
            QMessageBox.warning(self, "警告", "请先添加图片文件")
            return
            
        if not self.output_path.text():
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
            
        # 获取设置参数
        settings = self.settings_widget.get_settings()
        
        # 开始转换
        self.progress_bar.setMaximum(len(self.file_list))
        self.progress_bar.setValue(0)
        self.progress_label.setText("开始转换...")
        
        # 禁用按钮
        self.btn_convert.setEnabled(False)
        
        # 开始转换
        self.converter.convert_images(
            self.file_list,
            self.output_path.text(),
            settings
        )
        
    def update_progress(self, current, total, filename):
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"正在转换: {os.path.basename(filename)}... ({current}/{total})")
        
    def conversion_finished(self, success_count, fail_count):
        self.progress_label.setText(f"转换完成: 成功 {success_count} 个，失败 {fail_count} 个")
        self.btn_convert.setEnabled(True)
        
        QMessageBox.information(
            self,
            "转换完成",
            f"图片转换完成\n成功: {success_count} 个\n失败: {fail_count} 个"
        )
