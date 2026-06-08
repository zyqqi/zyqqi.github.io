"""
图片批量压缩脚本
用法：把这个文件放到你的作品集文件夹里，双击运行（或在终端执行 python compress_images.py）
需要先安装 Pillow：在终端/cmd 输入 pip install Pillow
"""

from PIL import Image
import os
import shutil

# ============ 配置区（可以改这里）============
FOLDER = "."             # "." 表示脚本所在的文件夹，也可以改成绝对路径如 r"C:\Users\你的名字\作品集"
QUALITY = 75             # 压缩质量，建议 70-85，越低文件越小但画质越差
MAX_WIDTH = 1920         # 最大宽度（像素），超过这个宽度会自动缩小，设 0 则不限制
BACKUP = True            # True = 压缩前备份原图到 _backup 文件夹；False = 直接覆盖
INCLUDE_SUBFOLDERS = True  # True = 同时处理子文件夹里的图片
# ============================================

SUPPORTED = (".jpg", ".jpeg", ".png")

def compress_images(folder, quality, max_width, backup, include_sub):
    folder = os.path.abspath(folder)
    backup_dir = os.path.join(folder, "_backup")

    # 收集所有图片路径
    image_paths = []
    if include_sub:
        for root, dirs, files in os.walk(folder):
            # 跳过备份文件夹
            dirs[:] = [d for d in dirs if d != "_backup"]
            for f in files:
                if f.lower().endswith(SUPPORTED):
                    image_paths.append(os.path.join(root, f))
    else:
        for f in os.listdir(folder):
            if f.lower().endswith(SUPPORTED):
                image_paths.append(os.path.join(folder, f))

    if not image_paths:
        print("❌ 没有找到任何 JPG/PNG 图片，请确认文件夹路径。")
        return

    print(f"📂 文件夹：{folder}")
    print(f"🖼  找到 {len(image_paths)} 张图片，开始压缩...\n")

    total_before = 0
    total_after = 0

    for path in image_paths:
        try:
            size_before = os.path.getsize(path)
            total_before += size_before

            # 备份原图
            if backup:
                rel = os.path.relpath(path, folder)
                bak_path = os.path.join(backup_dir, rel)
                os.makedirs(os.path.dirname(bak_path), exist_ok=True)
                shutil.copy2(path, bak_path)

            # 打开并处理图片
            with Image.open(path) as img:
                # 转换模式（PNG 带透明通道处理）
                ext = os.path.splitext(path)[1].lower()
                if ext == ".png":
                    # PNG 保留透明度，不转换
                    save_format = "PNG"
                    save_kwargs = {"optimize": True}
                else:
                    # JPG 转为 RGB（防止 RGBA 报错）
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    save_format = "JPEG"
                    save_kwargs = {"quality": quality, "optimize": True}

                # 限制最大宽度
                if max_width and img.width > max_width:
                    ratio = max_width / img.width
                    new_size = (max_width, int(img.height * ratio))
                    img = img.resize(new_size, Image.LANCZOS)

                img.save(path, save_format, **save_kwargs)

            size_after = os.path.getsize(path)
            total_after += size_after
            ratio = (1 - size_after / size_before) * 100 if size_before else 0
            filename = os.path.relpath(path, folder)
            print(f"  ✅ {filename}")
            print(f"     {_fmt(size_before)} → {_fmt(size_after)}  (-{ratio:.1f}%)")

        except Exception as e:
            print(f"  ⚠️  跳过 {os.path.basename(path)}：{e}")

    print(f"\n{'='*50}")
    print(f"✨ 完成！共处理 {len(image_paths)} 张图片")
    print(f"   压缩前总大小：{_fmt(total_before)}")
    print(f"   压缩后总大小：{_fmt(total_after)}")
    print(f"   节省空间：{_fmt(total_before - total_after)}  (-{(1 - total_after/total_before)*100:.1f}%)")
    if backup:
        print(f"   原图备份在：{backup_dir}")

def _fmt(size_bytes):
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"

if __name__ == "__main__":
    compress_images(FOLDER, QUALITY, MAX_WIDTH, BACKUP, INCLUDE_SUBFOLDERS)
    input("\n按回车键退出...")
