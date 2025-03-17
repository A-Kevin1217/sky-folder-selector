from PIL import Image
import os

def create_ico(input_path, output_path):
    """创建 Windows 图标文件"""
    img = Image.open(input_path)
    # 创建多个尺寸的图标
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(output_path, format='ICO', sizes=sizes)

def create_icns(input_path, output_path):
    """创建 macOS 图标文件"""
    img = Image.open(input_path)
    if not os.path.exists('icon.iconset'):
        os.makedirs('icon.iconset')
    
    # 创建不同尺寸的图标
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        # 普通分辨率
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'icon.iconset/icon_{size}x{size}.png')
        # 高分辨率 (@2x)
        if size * 2 <= 1024:
            resized = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
            resized.save(f'icon.iconset/icon_{size}x{size}@2x.png')

    # 使用 iconutil 创建 .icns 文件 (仅在 macOS 上可用)
    os.system(f'iconutil -c icns icon.iconset -o {output_path}')
    # 清理临时文件
    os.system('rm -rf icon.iconset')

if __name__ == '__main__':
    # 确保目录存在
    if not os.path.exists('assets/icons'):
        os.makedirs('assets/icons')
    
    # 生成图标
    create_ico('assets/icons/icon.png', 'assets/icons/icon.ico')
    create_icns('assets/icons/icon.png', 'assets/icons/icon.icns') 