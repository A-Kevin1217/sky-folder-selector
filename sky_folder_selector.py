import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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
        
        # 加载设置
        self.load_settings()
        
        # 设置样式
        style = ttk.Style()
        style.configure("TButton", padding=10)
        style.configure("TLabel", padding=5)
        
        # 标题
        ttk.Label(self.root, text="Sky·光遇 电脑版目录选择器", 
                 font=("", 16, "bold")).pack(pady=20)
        
        # 平台信息
        platform_text = "Windows版本" if sys.platform == 'win32' else "macOS版本" if sys.platform == 'darwin' else "其他平台"
        ttk.Label(self.root, text=platform_text).pack()
        
        # 按钮
        ttk.Button(self.root, text="打开 光遇截图(images) 目录", 
                  command=self.open_images).pack(fill="x", padx=30, pady=10)
        ttk.Button(self.root, text="打开 光遇录屏(Record) 目录", 
                  command=self.open_record).pack(fill="x", padx=30, pady=10)
        ttk.Button(self.root, text="同时打开录屏和截图两个目录", 
                  command=self.open_both).pack(fill="x", padx=30, pady=10)
        
        # 设置按钮
        ttk.Button(self.root, text="设置", 
                  command=self.show_settings).pack(pady=10)
        
        # 底部署名
        ttk.Label(self.root, text="Powered By 星川尘心", 
                 font=("", 9)).pack(side="bottom", pady=(0, 5))
        ttk.Label(self.root, text="Programmed By 小丞", 
                 font=("", 9)).pack(side="bottom", pady=(0, 5))
    
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