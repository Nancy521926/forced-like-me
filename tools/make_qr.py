# -*- coding: utf-8 -*-
"""把网页链接生成二维码 PNG（微信扫码玩）。

用法：python3 tools/make_qr.py "https://你的链接"
输出：web/qrcode.png
"""
import os
import sys

import qrcode
from qrcode.image.pil import PilImage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    if len(sys.argv) < 2:
        print('用法：python3 tools/make_qr.py "https://链接"')
        return
    url = sys.argv[1].strip()
    qr = qrcode.QRCode(
        version=None,               # 自动选版本
        error_correction=qrcode.constants.ERROR_CORRECT_M,   # 中等纠错，微信好扫
        box_size=12,                # 每格像素：二维码约 400~450px，转发后仍清晰
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=PilImage, fill_color="#1b1035",
                        back_color="#fff4f9").convert("RGB")
    out = os.path.join(ROOT, "web", "qrcode.png")
    img.save(out)
    print("已生成 %s (%dx%d)" % (out, img.size[0], img.size[1]))
    print("链接：%s" % url)


if __name__ == "__main__":
    main()
