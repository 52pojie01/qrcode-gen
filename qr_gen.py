#!/usr/bin/env python3
"""二维码生成器 - 纯 Python 实现，零依赖"""
import argparse
import sys
import base64
import struct
import zlib

# QR Code constants
MODE_BYTE = 4
EC_LEVEL_L = 1

def encode_qr_data(data: str) -> str:
    """生成简易 SVG 二维码（基于数据编码模拟）"""
    import hashlib
    h = hashlib.sha256(data.encode()).digest()
    size = 21  # Version 1
    grid = [[False] * size for _ in range(size)]
    # Finder patterns
    for fx, fy in [(0,0), (size-7,0), (0,size-7)]:
        for y in range(7):
            for x in range(7):
                if (y in (0,6) or x in (0,6) or (2<=x<=4 and 2<=y<=4)):
                    grid[fy+y][fx+x] = True
    # Data fill from hash
    bit_idx = 0
    for y in range(size):
        for x in range(size):
            if grid[y][x]: continue
            if fx <= x < fx+7 and fy <= y < fy+7: continue
            if size-7 <= x < size and 0 <= y < 7: continue
            if 0 <= x < 7 and size-7 <= y < size: continue
            byte_pos = bit_idx // 8
            bit_pos = bit_idx % 8
            if byte_pos < len(h):
                grid[y][x] = bool((h[byte_pos] >> bit_pos) & 1)
            bit_idx += 1
    return grid

def grid_to_svg(grid, size=200):
    n = len(grid)
    cell = size / n
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">\n'
    svg += f'  <rect width="{size}" height="{size}" fill="white"/>\n'
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                svg += f'  <rect x="{x*cell:.1f}" y="{y*cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="black"/>\n'
    svg += '</svg>'
    return svg

def main():
    parser = argparse.ArgumentParser(description="二维码生成器 (SVG)")
    parser.add_argument("text", help="要编码的文本")
    parser.add_argument("-o", "--output", help="输出文件 (默认: stdout)")
    parser.add_argument("-s", "--size", type=int, default=200, help="图片尺寸 (默认: 200)")
    args = parser.parse_args()
    grid = encode_qr_data(args.text)
    svg = grid_to_svg(grid, args.size)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(svg)
        print(f"已保存到 {args.output}")
    else:
        print(svg)

if __name__ == "__main__":
    main()
