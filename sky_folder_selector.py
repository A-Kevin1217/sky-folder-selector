import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QDialog, QGridLayout,
                           QLineEdit, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

def get_default_sky_path():
    """获取不同平台下Sky的默认路径"""
    if sys.platform == 'win32':  # Windows
        base = os.path.join(os.getenv('APPDATA'), "ThatGameCompany", "com.netease.sky")
    elif sys.platform == 'darwin':  # macOS
        base = os.path.expanduser("~/Library/Containers/com.tgc.sky.macos/Data/Documents")
    else:  # 其他平台
        base = ""
    return base

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.setWindowTitle("设置")
        self.setFixedSize(500, 250)  # 增加高度以容纳平台信息
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F3FF;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                color: #000000;
                background-color: white;
                padding: 5px;
                border: 1px solid #BDC3C7;
                border-radius: 3px;
            }
        """)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        # 显示当前平台
        platform_text = "当前平台：Windows" if sys.platform == 'win32' else "当前平台：macOS" if sys.platform == 'darwin' else "当前平台：其他"
        platform_label = QLabel(platform_text)
        platform_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(platform_label, 0, 0, 1, 3)
        
        # 默认路径提示
        default_path = get_default_sky_path()
        default_label = QLabel(f"默认路径：{default_path}")
        default_label.setStyleSheet("color: #7F8C8D; font-size: 10px;")
        layout.addWidget(default_label, 1, 0, 1, 3)
        
        # 图片目录设置
        images_label = QLabel("截图目录：")
        images_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(images_label, 2, 0)
        self.images_path = QLineEdit(self.settings.get("images_path", ""))
        layout.addWidget(self.images_path, 2, 1)
        browse_images = QPushButton("浏览")
        browse_images.clicked.connect(lambda: self.browse_folder(self.images_path))
        layout.addWidget(browse_images, 2, 2)
        
        # 录屏目录设置
        record_label = QLabel("录屏目录：")
        record_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(record_label, 3, 0)
        self.record_path = QLineEdit(self.settings.get("record_path", ""))
        layout.addWidget(self.record_path, 3, 1)
        browse_record = QPushButton("浏览")
        browse_record.clicked.connect(lambda: self.browse_folder(self.record_path))
        layout.addWidget(browse_record, 3, 2)
        
        # 重置按钮
        reset_btn = QPushButton("恢复默认")
        reset_btn.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_btn, 4, 0)
        
        # 确定和取消按钮
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(save_btn, 4, 1)
        layout.addWidget(cancel_btn, 4, 2)
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """
        for btn in [browse_images, browse_record, reset_btn, save_btn, cancel_btn]:
            btn.setStyleSheet(button_style)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            line_edit.setText(folder)
    
    def reset_to_default(self):
        base_path = get_default_sky_path()
        if base_path:
            self.images_path.setText(os.path.join(base_path, "images"))
            self.record_path.setText(os.path.join(base_path, "Record"))
        else:
            QMessageBox.warning(self, "错误", "无法确定默认路径，请手动选择目录。")
    
    def get_settings(self):
        return {
            "images_path": self.images_path.text(),
            "record_path": self.record_path.text()
        }

class SkyFolderSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sky·光遇 电脑版目录选择器")
        self.setFixedSize(500, 400)
        self.load_settings()
        
        # 设置窗口背景色
        self.setStyleSheet("background-color: #E6F3FF;")
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("Sky·光遇 电脑版目录选择器")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)
        
        # 平台信息
        platform_text = "Windows版本" if sys.platform == 'win32' else "macOS版本" if sys.platform == 'darwin' else "其他平台"
        platform_label = QLabel(platform_text)
        platform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        platform_label.setStyleSheet("color: #7F8C8D;")
        layout.addWidget(platform_label)
        
        # 按钮样式
        button_style = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #2574A9;
            }
        """
        
        # 创建按钮
        self.create_button("打开 光遇截图(images) 目录", self.open_images, layout, button_style)
        self.create_button("打开 光遇录屏(Record) 目录", self.open_record, layout, button_style)
        self.create_button("同时打开录屏和截图两个目录", self.open_both, layout, button_style)
        
        # 添加设置按钮
        settings_button = QPushButton("设置")
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
                font-family: 'Microsoft YaHei';
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_button.clicked.connect(self.show_settings)
        layout.addWidget(settings_button)
        
        # 添加底部署名
        signature = QLabel("Powered By 星川尘心")
        signature.setAlignment(Qt.AlignmentFlag.AlignRight)
        signature.setFont(QFont("Microsoft YaHei", 9))
        signature.setStyleSheet("color: #7F8C8D;")
        layout.addWidget(signature)
    
    def load_settings(self):
        self.settings_file = "sky_settings.json"
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = {}
                # 设置默认路径
                base_path = get_default_sky_path()
                if base_path:
                    self.settings = {
                        "images_path": os.path.join(base_path, "images"),
                        "record_path": os.path.join(base_path, "Record")
                    }
                    self.save_settings()
        except Exception:
            self.settings = {}
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存设置时出错：{str(e)}")
    
    def create_button(self, text, slot, layout, style):
        button = QPushButton(text)
        button.setStyleSheet(style)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(slot)
        layout.addWidget(button)
    
    def show_settings(self):
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings = dialog.get_settings()
            self.save_settings()
    
    def get_folder_path(self, folder_type):
        if folder_type in self.settings and self.settings[folder_type]:
            return self.settings[folder_type]
        # 默认路径
        base_path = get_default_sky_path()
        if not base_path:
            QMessageBox.warning(self, "错误", "无法确定默认路径，请在设置中手动设置目录。")
            return None
        return os.path.join(base_path, "images" if folder_type == "images_path" else "Record")
    
    def open_folder(self, path):
        if not path:
            return
            
        if not os.path.exists(path):
            QMessageBox.warning(self, "错误", f"您指定的目录 '{path}' 不存在。如果您没有手动设置该目录，可能是程序的默认目录未能找到。请检查路径是否正确，或在设置中手动选择目录。")
            return
        
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{path}"')
            elif sys.platform == 'win32':  # Windows
                os.startfile(path)
            else:  # Linux
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开目录时出错：{str(e)}")
    
    def open_images(self):
        self.open_folder(self.get_folder_path("images_path"))
    
    def open_record(self):
        self.open_folder(self.get_folder_path("record_path"))
    
    def open_both(self):
        self.open_images()
        self.open_record()

def main():
    folder_path = "your_directory_path"  # 替换为实际的目录路径

    # 检查目录是否存在
    if not os.path.exists(folder_path):
        print(f"提示：您指定的目录 '{folder_path}' 不存在。"
              f"如果您没有手动设置该目录，可能是程序的默认目录未能找到。"
              f"请检查路径是否正确，或在设置中手动选择目录。")
        sys.exit(1)

    # 继续执行程序的其他部分
    app = QApplication(sys.argv)
    window = SkyFolderSelector()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 