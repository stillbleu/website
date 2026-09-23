"""Generate the downloadable StillBleu therapy flyers."""

import os

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "assets", "flyers")
BOOKING_URL = "https://stillbleu.ch/booking.html"
BOOKING_URLS = {
    "en": f"{BOOKING_URL}?lang=en",
    "fr": f"{BOOKING_URL}?lang=fr",
}

INK = HexColor("#1B2B3A")
NAVY = HexColor("#1D3A52")
BLUE = HexColor("#35688E")
MUTE = HexColor("#5F7688")
PALE = HexColor("#F2F7FB")
LINE = HexColor("#D6E4ED")
GOLD = HexColor("#4F87B0")
WHITE = HexColor("#FFFFFF")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
NORTHWELL_FONT = os.path.join(ROOT, "assets", "fonts", "NorthwellAlt.ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSerif", os.path.join(FONT_DIR, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("NorthwellAlt", NORTHWELL_FONT))

styles = getSampleStyleSheet()
BODY = ParagraphStyle("flyer-body", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=10, leading=14, textColor=INK)
SMALL = ParagraphStyle("flyer-small", parent=BODY, fontSize=8.2, leading=10.5, textColor=INK)
THERAPY = ParagraphStyle("flyer-therapy", parent=BODY, fontName="DejaVuSans-Bold", fontSize=9.8, leading=12, textColor=NAVY)
HEADLINE = ParagraphStyle("flyer-headline", parent=BODY, fontName="NorthwellAlt", fontSize=25, leading=32, textColor=NAVY)
INTRO = ParagraphStyle("flyer-intro", parent=BODY, fontSize=10.5, leading=15, textColor=MUTE)
BOOKING = ParagraphStyle("flyer-booking", parent=BODY, fontName="DejaVuSans-Bold", fontSize=11, leading=13, textColor=WHITE)
SECTION = ParagraphStyle("flyer-section", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8, leading=10, alignment=1, textColor=BLUE)
SUBSECTION = ParagraphStyle("flyer-subsection", parent=BODY, fontName="NorthwellAlt", fontSize=14, leading=16, alignment=1, textColor=NAVY)
CORE_LABEL = ParagraphStyle("flyer-core-label", parent=BODY, fontName="DejaVuSans-Bold", fontSize=7.5, leading=9, alignment=1, textColor=BLUE)
CORE_NAME = ParagraphStyle("flyer-core-name", parent=BODY, fontName="NorthwellAlt", fontSize=18, leading=21, alignment=1, textColor=NAVY)
CORE_DESC = ParagraphStyle("flyer-core-desc", parent=BODY, fontSize=8.8, leading=11, alignment=1, textColor=INK)
NOTE = ParagraphStyle("flyer-note", parent=BODY, fontName="Times-Italic", fontSize=9.2, leading=11.5, alignment=1, textColor=NAVY)


COPY = {
    "en": {
        "lang": "ENGLISH",
        "strap": "ANTHROPOSOPHIC & INTEGRATIVE MEDICINE",
        "title": "Integrative care, with time to listen.",
        "intro": "A thoughtful medical practice offering gentle therapies for health, vitality and inner balance.",
        "place": "At L'Aubier, Montézillon",
        "core_label": "THE CORE PRACTICE",
        "core_name": "Anthroposophic external therapies",
        "core_desc": "The heart of StillBleu: rhythmic massage, touch, warmth, oils, compresses, wraps and therapeutic movement, chosen to support the body's own regulation.",
        "complementary": "COMPLEMENTARY APPROACHES",
        "complementary_intro": "Added only where appropriate, after individual assessment, to complement the core work.",
        "note": "Every consultation begins with listening. Together, we find a thoughtful path for the whole person, never just the symptom.",
        "book": "Book an integrative medical consultation",
        "book_small": "Scan the QR code to choose a time online",
        "visit": "L'Aubier, Montézillon (NE), Switzerland",
        "contact": "+41 76 409 62 42  ·  info@stillbleu.ch",
        "footer": "Integrating science, wisdom and compassion for conscious care.",
        "therapies": [
            ("Acupuncture", "Individual support for regulation and energetic balance."),
            ("Yoga and breath awareness", "Conscious breathing, stability and inner calm."),
            ("Sound-based therapies", "Sound and attentive listening for rest and awareness."),
            ("Qi-based therapies", "Reiki and Pranic Healing with light touch and attention."),
            ("Integrative guidance", "Lifestyle, rhythm, rest and movement for well-being."),
        ],
    },
    "fr": {
        "lang": "FRANÇAIS",
        "strap": "MÉDECINE ANTHROPOSOPHIQUE & INTÉGRATIVE",
        "title": "Une médecine intégrative, le temps d'écouter.",
        "intro": "Une pratique médicale attentive proposant des thérapies douces pour la santé, la vitalité et l'équilibre intérieur.",
        "place": "À L'Aubier, Montézillon",
        "core_label": "LE SOIN CENTRAL",
        "core_name": "Thérapies externes anthroposophiques",
        "core_desc": "Le cœur de StillBleu : massage rythmique, toucher, chaleur, huiles, compresses, enveloppements et mouvement thérapeutique, choisis pour soutenir la régulation propre du corps.",
        "complementary": "APPROCHES COMPLÉMENTAIRES",
        "complementary_intro": "Proposées uniquement si elles sont appropriées, après une évaluation individuelle, en complément du travail central.",
        "note": "Chaque consultation commence par l'écoute. Ensemble, nous cherchons un chemin attentif pour la personne dans sa globalité, jamais pour le seul symptôme.",
        "book": "Réserver une consultation médicale intégrative",
        "book_small": "Scannez le QR code pour choisir un horaire",
        "visit": "L'Aubier, Montézillon (NE), Suisse",
        "contact": "+41 76 409 62 42  ·  info@stillbleu.ch",
        "footer": "Science, sagesse et compassion réunies pour un soin conscient.",
        "therapies": [
            ("Acupuncture", "Un soutien personnalisé pour la régulation et l'équilibre énergétique."),
            ("Yoga et conscience du souffle", "Respiration consciente, stabilité et calme intérieur."),
            ("Thérapies par le son", "Le son et l'écoute attentive pour la détente et la conscience de soi."),
            ("Thérapies fondées sur le Qi", "Reiki et Pranic Healing par un toucher léger et une attention soutenue."),
            ("Accompagnement intégratif", "Mode de vie, rythme, repos et mouvement pour le bien-être."),
        ],
    },
}


def draw_paragraph(pdf, text, style, x, y, width):
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, 200 * mm)
    paragraph.drawOn(pdf, x, y - height)
    return height


def draw_logo(pdf, x, y, width):
    path = os.path.join(ROOT, "assets", "img", "logo-mark.png")
    pdf.drawImage(path, x, y, width=width, height=width, mask="auto", preserveAspectRatio=True)


def draw_flyer(language):
    copy = COPY[language]
    output = os.path.join(OUTPUT_DIR, f"stillbleu-flyer-{language}.pdf")
    width, height = A4
    margin = 18 * mm
    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(PALE)
    pdf.rect(0, height - 100 * mm, width, 100 * mm, fill=1, stroke=0)
    pdf.setFillColor(BLUE)
    pdf.rect(0, height - 4 * mm, width, 4 * mm, fill=1, stroke=0)

    pdf.setFillColor(NAVY)
    pdf.setFont("DejaVuSans", 7.5)
    pdf.drawString(margin, height - 14 * mm, copy["strap"])
    pdf.drawRightString(width - margin, height - 14 * mm, copy["lang"])
    logo_x = width - margin - 28 * mm
    logo_y = height - 67 * mm
    draw_logo(pdf, logo_x, logo_y, 27 * mm)
    pdf.setFillColor(NAVY)
    pdf.setFont("NorthwellAlt", 15)
    pdf.drawCentredString(logo_x + 13.5 * mm, logo_y - 5 * mm, "StillBleu")

    title_top = height - 43 * mm
    title_height = draw_paragraph(pdf, copy["title"], HEADLINE, margin, title_top, 130 * mm)
    intro_top = title_top - title_height - 5 * mm
    intro_height = draw_paragraph(pdf, copy["intro"], INTRO, margin, intro_top, 130 * mm)
    pdf.setStrokeColor(BLUE)
    pdf.setLineWidth(2.2)
    pdf.line(margin, intro_top - intro_height - 4 * mm, margin + 30 * mm, intro_top - intro_height - 4 * mm)
    pdf.setFillColor(BLUE)
    pdf.setFont("DejaVuSans-Bold", 8.5)
    pdf.drawString(margin, intro_top - intro_height - 11 * mm, copy["place"])

    core_top = height - 119 * mm
    draw_paragraph(pdf, copy["core_label"], CORE_LABEL, margin, core_top, width - 2 * margin)
    draw_paragraph(pdf, copy["core_name"], CORE_NAME, margin, core_top - 7 * mm, width - 2 * margin)
    draw_paragraph(pdf, copy["core_desc"], CORE_DESC, margin + 16 * mm, core_top - 18 * mm, width - 2 * margin - 32 * mm)
    pdf.setStrokeColor(BLUE)
    pdf.setLineWidth(1)
    pdf.line(margin + 42 * mm, core_top - 32 * mm, width - margin - 42 * mm, core_top - 32 * mm)
    pdf.setFillColor(BLUE)
    pdf.circle(width / 2, core_top - 32 * mm, 1.5 * mm, fill=1, stroke=0)

    complementary_top = core_top - 42 * mm
    draw_paragraph(pdf, copy["complementary"], SUBSECTION, margin, complementary_top, width - 2 * margin)
    draw_paragraph(pdf, copy["complementary_intro"], NOTE, margin + 8 * mm, complementary_top - 7 * mm, width - 2 * margin - 16 * mm)

    column_width = 82 * mm
    row_y = complementary_top - 18 * mm
    for index, (name, description) in enumerate(copy["therapies"]):
        x = margin if index % 2 == 0 else 111 * mm
        y = row_y - (index // 2) * 24 * mm
        pdf.setStrokeColor(LINE)
        pdf.setLineWidth(.5)
        pdf.line(x, y - 17 * mm, x + column_width, y - 17 * mm)
        pdf.setStrokeColor(LINE)
        pdf.setFillColor(BLUE)
        pdf.circle(x + 3 * mm, y - 3 * mm, 1.2 * mm, fill=1, stroke=0)
        draw_paragraph(pdf, name, THERAPY, x + 8 * mm, y, column_width - 8 * mm)
        draw_paragraph(pdf, description, SMALL, x + 8 * mm, y - 7 * mm, column_width - 8 * mm)

    note_y = 89 * mm
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(margin, note_y - 24 * mm, width - 2 * margin, 24 * mm, 2 * mm, fill=1, stroke=1)
    draw_paragraph(pdf, copy["note"], NOTE, margin + 7 * mm, note_y - 5 * mm, width - 2 * margin - 14 * mm)

    footer_y = 18 * mm
    footer_height = 47 * mm
    pdf.setFillColor(NAVY)
    pdf.roundRect(margin, footer_y, width - 2 * margin, footer_height, 3 * mm, fill=1, stroke=0)
    draw_paragraph(pdf, copy["book"], BOOKING, margin + 8 * mm, footer_y + 37 * mm, 112 * mm)
    pdf.setFillColor(HexColor("#C9DCE9"))
    pdf.setFont("DejaVuSans", 8.5)
    pdf.drawString(margin + 8 * mm, footer_y + 29 * mm, copy["book_small"])
    pdf.setFont("DejaVuSans-Bold", 9)
    pdf.drawString(margin + 8 * mm, footer_y + 15 * mm, copy["visit"])
    pdf.setFont("DejaVuSans", 8.2)
    pdf.drawString(margin + 8 * mm, footer_y + 9 * mm, copy["contact"])

    code = qr.QrCodeWidget(BOOKING_URLS[language])
    code.barFillColor = HexColor("#000000")
    code.barStrokeColor = HexColor("#000000")
    size = 29 * mm
    code.barWidth = size
    code.barHeight = size
    drawing = Drawing(size, size)
    drawing.add(code)
    qr_x = width - margin - size - 8 * mm
    qr_y = footer_y + 7 * mm
    pdf.setFillColor(WHITE)
    pdf.rect(qr_x - 2 * mm, qr_y - 2 * mm, size + 4 * mm, size + 4 * mm, fill=1, stroke=0)
    renderPDF.draw(drawing, pdf, qr_x, qr_y)

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Italic", 8.5)
    pdf.drawCentredString(width / 2, 10 * mm, copy["footer"])
    pdf.save()
    print(f"Generated PDF: {output}")


os.makedirs(OUTPUT_DIR, exist_ok=True)
for language in ("en", "fr"):
    draw_flyer(language)
