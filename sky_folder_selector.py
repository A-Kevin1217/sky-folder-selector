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
        self.root.title("Sky·光遇 电脑版目录选择器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 设置窗口图标
        try:
            if platform.system() == 'Windows':
                icon_path = "assets/icons/icon.ico"
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            elif platform.system() == 'Darwin':  # macOS
                icon_path = "assets/icons/icon.icns"
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"无法加载图标：{str(e)}")
        
        # 设置暗色主题
        self.style = ttk.Style()
        
        # 配置按钮样式
        self.style.configure("Dark.TButton",
                           padding=10,
                           relief="flat",
                           background="#4A4A4A",
                           foreground="#FFFFFF",
                           font=("SF Pro Text", 13))
        
        # 配置标签样式
        self.style.configure("Dark.TLabel",
                           padding=5,
                           font=("SF Pro Text", 13),
                           foreground="#FFFFFF")
        
        # 配置标题样式
        self.style.configure("DarkTitle.TLabel",
                           font=("SF Pro Display", 24, "bold"),
                           foreground="#FFFFFF")
        
        # 配置副标题样式
        self.style.configure("DarkSubTitle.TLabel",
                           font=("SF Pro Text", 13),
                           foreground="#AAAAAA")
        
        # 配置信息标签样式
        self.style.configure("DarkInfo.TLabel",
                           font=("SF Pro Text", 10),
                           foreground="#888888")
        
        # 配置框架样式
        self.style.configure("Dark.TFrame",
                           background="#2A2A2A")
        
        # 设置窗口背景色
        self.root.configure(bg="#2A2A2A")
        
        # 获取用户目录
        self.user_home = str(Path.home())
        self.settings_file = os.path.join(self.user_home, '.sky_folder_selector', 'settings.json')
        
        # 确保设置目录存在
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # 初始化设置
        self.settings = {}
        
        self.create_widgets()
        self.load_settings()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # 标题
        ttk.Label(main_frame, text="Sky·光遇", 
                 style="DarkTitle.TLabel").pack(pady=(30, 5))
        ttk.Label(main_frame, text="电脑版目录选择器", 
                 style="DarkSubTitle.TLabel").pack(pady=(0, 40))
        
        # 创建按钮框架
        button_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        button_frame.pack(fill="x", padx=50)
        
        # 前两个按钮并排显示
        ttk.Button(button_frame, text="打开截图目录", 
                  command=self.open_images,
                  style="Dark.TButton").pack(side="left", expand=True, padx=5)
        ttk.Button(button_frame, text="打开录屏目录", 
                  command=self.open_record,
                  style="Dark.TButton").pack(side="left", expand=True, padx=5)
        
        # 第三个按钮
        ttk.Button(main_frame, text="同时打开两个目录", 
                  command=self.open_both,
                  style="Dark.TButton").pack(fill="x", padx=50, pady=20)
        
        # 设置按钮
        ttk.Button(main_frame, text="设置", 
                  command=self.show_settings,
                  style="Dark.TButton").pack(pady=10)
        
        # 底部署名
        ttk.Label(main_frame, text="Powered By 星川尘心", 
                 style="DarkInfo.TLabel").pack(side="bottom", pady=(0, 5))
        ttk.Label(main_frame, text="Programmed By 小丞", 
                 style="DarkInfo.TLabel").pack(side="bottom", pady=(0, 5))
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                # 设置默认路径
                base_path = get_default_sky_path()
                if base_path:
                    self.settings = {
                        "images_path": os.path.join(base_path, "images"),
                        "record_path": os.path.join(base_path, "Record")
                    }
                    self.save_settings()
        except Exception as e:
            messagebox.showerror("错误", f"加载设置时出错：{str(e)}")
            self.settings = {}
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存设置时出错：{str(e)}")
    
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
    
    def open_images(self):
        self.open_folder(self.get_folder_path("images_path"))
    
    def open_record(self):
        self.open_folder(self.get_folder_path("record_path"))
    
    def open_both(self):
        self.open_images()
        self.open_record()
    
    def run(self):
        self.root.mainloop()

def main():
    app = SkyFolderSelector()
    app.run()

if __name__ == "__main__":
    main() 