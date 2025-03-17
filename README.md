# Sky光遇文件夹选择器

一个简单的工具，用于快速打开 Sky光遇 游戏的截图和录屏文件夹。

## 功能特点

- 支持 Windows 和 macOS 双平台
- 快速打开截图文件夹
- 快速打开录屏文件夹
- 支持自定义文件夹路径
- 简洁美观的界面

## 使用方法

1. 下载对应平台的可执行文件
2. 直接运行程序
3. 点击按钮打开对应文件夹
4. 可以通过设置按钮自定义文件夹路径

## 开发环境

- Python 3.9+
- PyQt6
- pyinstaller

## 构建方法

```bash
# 安装依赖
pip install PyQt6
pip install pyinstaller

# 构建程序
pyinstaller --onefile --windowed --name "Sky光遇文件夹选择器" sky_folder_selector.py
```

## 默认路径

- Windows: `%APPDATA%\ThatGameCompany\com.netease.sky`
- macOS: `~/Library/Containers/com.tgc.sky.macos/Data/Documents`

## 作者

星川尘心 