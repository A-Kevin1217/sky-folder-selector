# Sky Folder Selector

Sky Folder Selector 是一个简单易用的文件夹选择工具，基于 tkinter 开发，支持 Windows 和 macOS 平台。

## 功能特点

- 简洁的图形界面
- 支持文件夹选择
- 跨平台支持（Windows/macOS）

## 系统要求

- Python 3.10 或更高版本
- Windows 10 或更高版本
- macOS 10.13 或更高版本

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python sky_folder_selector.py
```

## 构建可执行文件

使用 PyInstaller 构建可执行文件：

```bash
# Windows
pyinstaller --name "Sky Folder Selector" --windowed --onefile --icon "assets/icons/icon.ico" sky_folder_selector.py

# macOS
pyinstaller --name "Sky Folder Selector" --windowed --onefile --icon "assets/icons/icon.icns" sky_folder_selector.py
```

## 使用说明

1. 下载对应平台的安装包
2. 运行程序
3. 选择需要处理的文件夹

## 更新日志

### v1.0.0
- 初始版本发布
- 支持 Windows 和 macOS 平台
- 优化了构建配置，确保所有依赖正确打包
- 添加了必要的系统权限配置
- 添加了应用程序图标
