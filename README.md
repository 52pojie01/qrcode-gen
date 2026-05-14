# 📱 QR Code Generator

纯 Python 二维码生成器，输出 SVG 格式，零依赖。

## 使用

```bash
python3 qr_gen.py "Hello World"              # 输出 SVG 到终端
python3 qr_gen.py "https://example.com" -o qr.svg  # 保存为文件
python3 qr_gen.py "你好" -s 400              # 指定尺寸
```
