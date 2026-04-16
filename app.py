from flask import Flask, render_template, request, send_file
import os
import zipfile
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter, Transformation
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MARGEM_X = 40
MARGEM_Y = 40
LARGURA_ASSINATURA = 160


def criar_assinatura_pdf(img_path, w, h):
    temp = "temp.pdf"

    img = Image.open(img_path)
    proporcao = img.height / img.width
    altura = LARGURA_ASSINATURA * proporcao

    c = canvas.Canvas(temp, pagesize=(w, h))
    c.drawImage(img_path, w - LARGURA_ASSINATURA - MARGEM_X, MARGEM_Y,
                width=LARGURA_ASSINATURA, height=altura, mask="auto")
    c.save()

    return temp


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/assinar", methods=["POST"])
def assinar():

    assinatura = request.files["assinatura"]
    pdfs = request.files.getlist("pdfs")

    assinatura_path = os.path.join(UPLOAD_FOLDER, assinatura.filename)
    assinatura.save(assinatura_path)

    saida_files = []

    for pdf in pdfs:

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        first = reader.pages[0]
        w = float(first.mediabox.width)
        h = float(first.mediabox.height)

        sig_pdf = criar_assinatura_pdf(assinatura_path, w, h)
        sig_page = PdfReader(sig_pdf).pages[0]

        for p in reader.pages:
            p.merge_transformed_page(sig_page, Transformation())
            writer.add_page(p)

        out_path = os.path.join(OUTPUT_FOLDER, pdf.filename)

        with open(out_path, "wb") as f:
            writer.write(f)

        saida_files.append(out_path)

    zip_path = os.path.join(OUTPUT_FOLDER, "resultado.zip")

    with zipfile.ZipFile(zip_path, "w") as z:
        for f in saida_files:
            z.write(f, os.path.basename(f))

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)