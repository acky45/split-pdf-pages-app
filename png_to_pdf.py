import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

# 入力フォルダ（結合したいPNGを置く）・出力フォルダ
INPUT_DIR = Path(__file__).parent / "png_input"
OUTPUT_DIR = Path(__file__).parent / "output"

# 出力ファイル名
OUTPUT_FILENAME = "merged.pdf"

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

png_files = sorted(INPUT_DIR.glob("*.png"))

if not png_files:
    print(f"⚠️ {INPUT_DIR} にPNGファイルが見つかりません")
else:
    images = [Image.open(p).convert("RGB") for p in png_files]
    output_path = OUTPUT_DIR / OUTPUT_FILENAME
    images[0].save(output_path, save_all=True, append_images=images[1:])
    print(f"✅ {len(images)}枚のPNGを結合しました → {output_path}")
