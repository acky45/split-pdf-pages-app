import io
import zipfile
from pathlib import Path

import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from werkzeug.utils import secure_filename

app = Flask(__name__)


def split_pdf(pdf_bytes: bytes, output_format: str, png_dpi: int = 150) -> bytes:
    """PDFをページごとに分割し、zip化したバイト列を返す"""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    total_pages = len(reader.pages)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        if output_format == "png":
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=png_dpi)
                zf.writestr(f"page_{i + 1}.png", pix.tobytes("png"))
            doc.close()
        else:
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                page_buffer = io.BytesIO()
                writer.write(page_buffer)
                zf.writestr(f"page_{i + 1}.pdf", page_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def merge_png_to_pdf(files) -> bytes:
    """複数のPNGファイルを1つのPDFに結合したバイト列を返す"""
    images = [Image.open(f).convert("RGB") for f in files]
    output_buffer = io.BytesIO()
    images[0].save(output_buffer, format="PDF", save_all=True, append_images=images[1:])
    output_buffer.seek(0)
    return output_buffer.getvalue()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/split", methods=["POST"])
def split():
    uploaded_file = request.files.get("pdf_file")
    output_format = request.form.get("output_format", "pdf")

    if not uploaded_file or uploaded_file.filename == "":
        return "PDFファイルが選択されていません", 400

    filename = secure_filename(uploaded_file.filename)
    stem = Path(filename).stem or "output"

    zip_bytes = split_pdf(uploaded_file.read(), output_format)

    return send_file(
        io.BytesIO(zip_bytes),
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{stem}_pages.zip",
    )


@app.route("/merge", methods=["POST"])
def merge():
    uploaded_files = request.files.getlist("png_files")
    uploaded_files = [f for f in uploaded_files if f and f.filename]

    if not uploaded_files:
        return "PNGファイルが選択されていません", 400

    uploaded_files.sort(key=lambda f: f.filename)
    pdf_bytes = merge_png_to_pdf(uploaded_files)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="merged.pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
