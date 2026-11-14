# -*- coding: utf-8 -*-
"""把二维码「融合」进一张图：底部居中放奶油色圆角卡 + 深棕二维码（颜色取自底图）。

用法：python3 tools/make_qr_merged.py "链接" "底图路径"
输出：web/qrcode_merged.png
"""
import os
import sys

import qrcode
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "web", "qrcode_merged.png")

DARK = (77, 59, 47)        # 深暖棕（二维码块，取底图深色）
CARD = (253, 250, 243)     # 奶油色卡片底（取底图亮色）


def main():
    if len(sys.argv) < 3:
        print('用法：python3 tools/make_qr_merged.py "链接" "底图路径"')
        return
    url, bg_path = sys.argv[1], sys.argv[2]

    # —— 二维码矩阵（纠错 M，好扫） ——
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)                       # 模块数（不含静区）

    # —— 底图 ——
    bg = Image.open(bg_path).convert("RGB")
    target_w = 900
    scale = target_w / bg.width
    bg = bg.resize((target_w, int(bg.height * scale)), Image.LANCZOS)
    W, H = bg.size

    # —— 布局：底部居中 ——
    qr_px = int(W * 0.34)            # 二维码边长
    pad = int(qr_px * 0.10)          # 卡片内边距
    quiet = int(qr_px * 0.045)       # 静区（扫描需要）
    card_w = qr_px + pad * 2
    card_h = qr_px + pad * 2
    cx, cy = W // 2, int(H * 0.80)
    x0, y0 = cx - card_w // 2, cy - card_h // 2

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h],
                        radius=int(card_w * 0.14), fill=CARD + (235,),
                        outline=DARK + (90,), width=3)

    # 二维码逐模块画（深棕块，带一点圆角感：用整格方块即可，扫描最稳）
    step = qr_px / n
    qx0 = cx - qr_px / 2 + quiet
    qy0 = cy - qr_px / 2 + quiet
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                d.rectangle([qx0 + c * step, qy0 + r * step,
                             qx0 + (c + 1) * step + 0.5, qy0 + (r + 1) * step + 0.5],
                            fill=DARK + (255,))

    merged = bg.convert("RGBA")
    merged = Image.alpha_composite(merged, layer).convert("RGB")
    merged.save(OUT, quality=95)
    print("已生成 %s (%dx%d)" % (OUT, W, H))


if __name__ == "__main__":
    main()
