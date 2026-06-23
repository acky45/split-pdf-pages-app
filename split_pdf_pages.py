import sys
from pathlib import Path

import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

sys.stdout.reconfigure(encoding="utf-8")

# 出力形式: "pdf" または "png"
OUTPUT_FORMAT = "pdf"

# PNG変換時の解像度（高いほど鮮明・容量大）
PNG_DPI = 150

# 入力フォルダ・出力フォルダ
INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

if not pdf_files:
    print(f"⚠️ {INPUT_DIR} にPDFファイルが見つかりません")

for pdf_path in pdf_files:
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    # PDFごとにサブフォルダを作成
    pdf_output_dir = OUTPUT_DIR / pdf_path.stem
    pdf_output_dir.mkdir(exist_ok=True)

    if OUTPUT_FORMAT == "png":
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=PNG_DPI)
            output_path = pdf_output_dir / f"page_{i + 1}.png"
            pix.save(output_path)
            print(f"✅ {pdf_path.name} ページ {i + 1} を保存しました → {output_path}")
        doc.close()
    else:
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            output_path = pdf_output_dir / f"page_{i + 1}.pdf"
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            print(f"✅ {pdf_path.name} ページ {i + 1} を保存しました → {output_path}")
