from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QSlider, QSpinBox, QCheckBox, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt

class SettingsWidget(QWidget):
    """WebP 转换参数设置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)  # 减少边距
        
        # 创建单行参数设置布局
        settings_layout = QHBoxLayout()
        
        # 质量设置
        quality_label = QLabel("质量:")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(80)
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(0, 100)
        self.quality_spin.setValue(80)
        
        # 无损压缩选项
        self.lossless_check = QCheckBox("无损压缩")
        
        # 尺寸控制选项
        self.resize_check = QCheckBox("调整尺寸")
        
        width_label = QLabel("宽度:")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(800)
        self.width_spin.setEnabled(False)
        
        height_label = QLabel("高度:")
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(600)
        self.height_spin.setEnabled(False)
        
        self.maintain_aspect = QCheckBox("保持比例")
        self.maintain_aspect.setChecked(True)
        self.maintain_aspect.setEnabled(False)
        
        # 添加所有组件到单行布局
        settings_layout.addWidget(quality_label)
        settings_layout.addWidget(self.quality_slider)
        settings_layout.addWidget(self.quality_spin)
        settings_layout.addWidget(self.lossless_check)
        settings_layout.addSpacing(10)
        settings_layout.addWidget(self.resize_check)
        settings_layout.addWidget(width_label)
        settings_layout.addWidget(self.width_spin)
        settings_layout.addWidget(height_label)
        settings_layout.addWidget(self.height_spin)
        settings_layout.addWidget(self.maintain_aspect)
        
        main_layout.addLayout(settings_layout)
        
        # 连接信号
        self.quality_slider.valueChanged.connect(self.quality_spin.setValue)
        self.quality_spin.valueChanged.connect(self.quality_slider.setValue)
        self.lossless_check.toggled.connect(self.toggle_quality_controls)
        self.resize_check.toggled.connect(self.toggle_resize_controls)
        
    def toggle_quality_controls(self, checked):
        self.quality_slider.setEnabled(not checked)
        self.quality_spin.setEnabled(not checked)
        
    def toggle_resize_controls(self, checked):
        self.width_spin.setEnabled(checked)
        self.height_spin.setEnabled(checked)
        self.maintain_aspect.setEnabled(checked)
        
    def get_settings(self):
        """返回当前设置参数"""
        settings = {
            "quality": self.quality_spin.value(),
            "lossless": self.lossless_check.isChecked(),
            "method": 4,  # 使用默认的方法 4
            "resize": self.resize_check.isChecked(),
            "width": self.width_spin.value() if self.resize_check.isChecked() else None,
            "height": self.height_spin.value() if self.resize_check.isChecked() else None,
            "maintain_aspect": self.maintain_aspect.isChecked()
        }
        return settings
