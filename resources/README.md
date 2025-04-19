# 创建 macOS 图标

要为应用程序创建 `.icns` 格式的图标，请按照以下步骤操作：

1. 创建一个 1024x1024 像素的 PNG 图像作为你的图标
2. 将该图像命名为 `icon.png` 并保存在此目录
3. 在终端中运行以下命令：

```bash
# 创建 iconset 目录
mkdir icon.iconset

# 生成不同尺寸的图标
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# 将 iconset 转换为 icns 文件
iconutil -c icns icon.iconset

# 清理
rm -rf icon.iconset
```

4. 确认 `icon.icns` 文件已生成
