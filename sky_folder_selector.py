import sys
import os
import json
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

def get_default_sky_path():
    """获取不同平台下Sky的默认路径"""
    if sys.platform == 'win32':  # Windows
        base = os.path.join(os.getenv('APPDATA'), "ThatGameCompany", "com.netease.sky")
    elif sys.platform == 'darwin':  # macOS
        base = os.path.expanduser("~/Library/Containers/com.tgc.sky.macos/Data/Documents")
    else:  # 其他平台
        base = ""
    return base

class SettingsDialog:
    def __init__(self, parent, settings):
        self.result = None
        self.settings = settings or {}
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("设置")
        self.dialog.geometry("500x250")
        self.dialog.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=5)
        style.configure("TEntry", padding=5)
        
        # 显示当前平台
        platform_text = "当前平台：Windows" if sys.platform == 'win32' else "当前平台：macOS" if sys.platform == 'darwin' else "当前平台：其他"
        ttk.Label(self.dialog, text=platform_text, font=("", 10, "bold")).pack(pady=5)
        
        # 默认路径提示
        default_path = get_default_sky_path()
        ttk.Label(self.dialog, text=f"默认路径：{default_path}", font=("", 9)).pack(pady=5)
        
        # 创建输入框框架
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="x", padx=20, pady=10)
        
        # 图片目录设置
        ttk.Label(frame, text="截图目录：").grid(row=0, column=0, sticky="w")
        self.images_path = ttk.Entry(frame, width=40)
        self.images_path.insert(0, self.settings.get("images_path", ""))
        self.images_path.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览", command=lambda: self.browse_folder(self.images_path)).grid(row=0, column=2)
        
        # 录屏目录设置
        ttk.Label(frame, text="录屏目录：").grid(row=1, column=0, sticky="w", pady=10)
        self.record_path = ttk.Entry(frame, width=40)
        self.record_path.insert(0, self.settings.get("record_path", ""))
        self.record_path.grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(frame, text="浏览", command=lambda: self.browse_folder(self.record_path)).grid(row=1, column=2, pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(button_frame, text="恢复默认", command=self.reset_to_default).pack(side="left", padx=5)
        ttk.Button(button_frame, text="保存", command=self.save).pack(side="right", padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side="right", padx=5)
        
        # 设置模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)
    
    def browse_folder(self, entry):
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)
    
    def reset_to_default(self):
        base_path = get_default_sky_path()
        if base_path:
            self.images_path.delete(0, tk.END)
            self.images_path.insert(0, os.path.join(base_path, "images"))
            self.record_path.delete(0, tk.END)
            self.record_path.insert(0, os.path.join(base_path, "Record"))
        else:
            messagebox.showwarning("错误", "无法确定默认路径，请手动选择目录。")
    
    def save(self):
        self.result = {
            "images_path": self.images_path.get(),
            "record_path": self.record_path.get()
        }
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

class SkyFolderSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sky Folder Selector")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # 设置窗口图标
        if platform.system() == 'Windows':
            self.root.iconbitmap("assets/icons/icon.ico")
        elif platform.system() == 'Darwin':  # macOS
            self.root.iconbitmap("assets/icons/icon.icns")
        
        # 设置主题色
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        self.style.configure("TLabel", padding=5)
        self.style.configure("TFrame", background="#f0f0f0")
        
        # 获取用户目录
        self.user_home = str(Path.home())
        self.settings_file = os.path.join(self.user_home, '.sky_folder_selector', 'settings.json')
        
        # 确保设置目录存在
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # 默认路径
        self.default_paths = {
            'Windows': os.path.join(os.getenv('APPDATA', ''), 'ThatGameCompany', 'com.netease.sky'),
            'Darwin': os.path.join(self.user_home, 'Library', 'Containers', 'com.tgc.sky.macos', 'Data', 'Documents')
        }
        
        self.create_widgets()
        self.load_settings()
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="Sky Folder Selector", 
                              font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 平台选择框架
        platform_frame = ttk.LabelFrame(main_frame, text="平台设置", padding="10")
        platform_frame.pack(fill="x", pady=(0, 20))
        
        # 平台选择
        self.platform_var = tk.StringVar(value=platform.system())
        ttk.Label(platform_frame, text="选择平台：").pack(side="left", padx=5)
        platform_menu = ttk.OptionMenu(platform_frame, self.platform_var, 
                                     platform.system(), "Windows", "Darwin")
        platform_menu.pack(side="left", padx=5)
        
        # 默认路径提示
        default_path = self.default_paths.get(platform.system(), "")
        path_label = ttk.Label(platform_frame, text=f"默认路径：{default_path}", 
                             font=("", 9), wraplength=400)
        path_label.pack(side="left", padx=5)
        
        # 按钮框架
        button_frame = ttk.LabelFrame(main_frame, text="操作", padding="10")
        button_frame.pack(fill="x", pady=(0, 20))
        
        # 创建按钮网格
        for i, (text, command) in enumerate([
            ("打开截图文件夹", self.open_screenshots),
            ("打开录屏文件夹", self.open_recordings),
            ("设置自定义路径", self.set_custom_path),
            ("重置为默认路径", self.reset_paths)
        ]):
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
        
        # 设置按钮列权重
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # 当前路径显示
        path_frame = ttk.LabelFrame(main_frame, text="当前路径", padding="10")
        path_frame.pack(fill="x", pady=(0, 20))
        
        self.screenshots_path_var = tk.StringVar()
        self.recordings_path_var = tk.StringVar()
        
        ttk.Label(path_frame, text="截图文件夹：").pack(anchor="w")
        ttk.Label(path_frame, textvariable=self.screenshots_path_var, 
                 wraplength=400).pack(anchor="w", pady=(0, 10))
        
        ttk.Label(path_frame, text="录屏文件夹：").pack(anchor="w")
        ttk.Label(path_frame, textvariable=self.recordings_path_var, 
                 wraplength=400).pack(anchor="w")
        
        # 底部署名
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Label(footer_frame, text="Powered By 星川尘心", 
                 font=("", 9)).pack(side="bottom", pady=(0, 5))
        ttk.Label(footer_frame, text="Programmed By 小丞", 
                 font=("", 9)).pack(side="bottom", pady=(0, 5))
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.screenshots_path_var.set(settings.get('screenshots_path', ''))
                    self.recordings_path_var.set(settings.get('recordings_path', ''))
            else:
                self.screenshots_path_var.set(self.default_paths.get(platform.system(), ''))
                self.recordings_path_var.set(self.default_paths.get(platform.system(), ''))
        except Exception as e:
            messagebox.showerror("错误", f"加载设置时出错：{str(e)}")
            self.screenshots_path_var.set(self.default_paths.get(platform.system(), ''))
            self.recordings_path_var.set(self.default_paths.get(platform.system(), ''))
    
    def show_settings(self):
        dialog = SettingsDialog(self.root, self.settings)
        if dialog.result:
            self.settings = dialog.result
            self.save_settings()
    
    def get_folder_path(self, folder_type):
        if folder_type in self.settings and self.settings[folder_type]:
            return self.settings[folder_type]
        # 默认路径
        base_path = get_default_sky_path()
        if not base_path:
            messagebox.showwarning("错误", "无法确定默认路径，请在设置中手动设置目录。")
            return None
        return os.path.join(base_path, "images" if folder_type == "images_path" else "Record")
    
    def open_folder(self, path):
        if not path:
            return
            
        if not os.path.exists(path):
            messagebox.showwarning("错误", 
                f"您指定的目录 '{path}' 不存在。如果您没有手动设置该目录，"
                f"可能是程序的默认目录未能找到。请检查路径是否正确，或在设置中手动选择目录。")
            return
        
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{path}"')
            elif sys.platform == 'win32':  # Windows
                os.startfile(path)
            else:  # Linux
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("错误", f"打开目录时出错：{str(e)}")
    
    def open_screenshots(self):
        self.open_folder(self.get_folder_path("images_path"))
    
    def open_recordings(self):
        self.open_folder(self.get_folder_path("record_path"))
    
    def set_custom_path(self):
        self.show_settings()
    
    def reset_paths(self):
        self.reset_to_default()
    
    def run(self):
        self.root.mainloop()

def main():
    app = SkyFolderSelector()
    app.run()

if __name__ == "__main__":
    main() 