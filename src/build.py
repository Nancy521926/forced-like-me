# -*- coding: utf-8 -*-
"""把贴图/表情打成单文件网页 docs/index.html（零外部依赖，方便托管 + 生成二维码）。

用法：python3 src/build.py
"""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PET_DIR = os.path.join(ROOT, "assets", "pet")
STICKER_DIR = os.path.join(ROOT, "assets", "sticker")
TEMPLATE = os.path.join(HERE, "template.html")
OUT = os.path.join(ROOT, "docs", "index.html")

# ----------------------------- 可调参数 -----------------------------
# 主角表情：点一次「不喜欢」往后翻一张，台词跟着换；翻到最后一张就到底了
PET_FILES = [
    "pet_10.gif",   # 小猫咪「嘿嘿嘿」（开场）
    "pet_01.gif",   # 白熊大哭
    "pet_06.gif",   # 扁扁地走开
    "pet_04.gif",   # 白团子抱抱
    "pet_00.gif",   # 粉猪捂脸
    "pet_08.gif",   # 门口灰猫（压轴）
]
DISLIKE_TEXTS = [
    "呜呜呜…你不喜欢我",
    "再也不理你了！坏蛋！！",
    "宝宝，喜欢我好不好",
    "呜…人家都哭了",
    "求求你啦，喜欢人家嘛~",
]
MOOD_EMOJI = ["😼", "😭", "🥺", "🫂", "😢", "🥹"]
# 这三张不进「不喜欢」翻牌序列，只在点「喜欢」之后的烟花页一朵朵炸出来
FIREWORK_STICKERS = ["stk_05.png", "stk_07.png", "stk_09.png"]
COUNTDOWN_FROM = 5     # 烟花页「敌军还有 N 秒到达战场」从几开始倒数


def data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {"gif": "image/gif", "png": "image/png"}[ext[1:]]
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


def main():
    assets = {}

    # 问询页主角
    for name in PET_FILES:
        assets[name] = data_url(os.path.join(PET_DIR, name))

    # 烟花页表情：有对应动图用动图，没有退回贴纸
    fire = []
    for stk in FIREWORK_STICKERS:
        pet = stk.replace("stk_", "pet_").replace(".png", ".gif")
        pet_path = os.path.join(PET_DIR, pet)
        stk_path = os.path.join(STICKER_DIR, stk)
        if os.path.isfile(pet_path):
            assets[pet] = data_url(pet_path)
            fire.append({"pet": pet, "stk": stk})
        elif os.path.isfile(stk_path):
            assets[stk] = data_url(stk_path)
            fire.append({"pet": "", "stk": stk})

    # 问询页上飘的贴纸
    floats = []
    for name in sorted(os.listdir(STICKER_DIR)):
        if not name.lower().endswith(".png"):
            continue
        if name in FIREWORK_STICKERS or name == "stk_10.png":
            continue
        assets[name] = data_url(os.path.join(STICKER_DIR, name))
        floats.append(name)

    config = {
        "petFiles": PET_FILES,
        "dislikeTexts": DISLIKE_TEXTS,
        "moodEmoji": MOOD_EMOJI,
        "countdownFrom": COUNTDOWN_FROM,
        "floats": floats,
        "fire": fire,
        "assets": assets,
    }

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__CONFIG__", json.dumps(config, ensure_ascii=False))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(html)

    print("生成 %s (%.0f KB)" % (OUT, os.path.getsize(OUT) / 1024.0))
    print("  主角动图 %d 张 / 上飘贴纸 %d 张 / 烟花表情 %d 组"
          % (len(PET_FILES), len(floats), len(fire)))


if __name__ == "__main__":
    main()
