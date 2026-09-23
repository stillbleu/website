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
BODY = ParagraphStyle("flyer-body", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=10.8, leading=15, textColor=INK)
SMALL = ParagraphStyle("flyer-small", parent=BODY, fontSize=8.7, leading=11.2, textColor=INK)
THERAPY = ParagraphStyle("flyer-therapy", parent=BODY, fontName="NorthwellAlt", fontSize=12.5, leading=14, textColor=INK)
HEADLINE = ParagraphStyle("flyer-headline", parent=BODY, fontName="DejaVuSerif", fontSize=25, leading=31, textColor=WHITE)
INTRO = ParagraphStyle("flyer-intro", parent=BODY, fontSize=12, leading=17, textColor=HexColor("#D7E6F2"))
BOOKING = ParagraphStyle("flyer-booking", parent=BODY, fontName="DejaVuSans-Bold", fontSize=11, leading=13, textColor=WHITE)
SECTION = ParagraphStyle("flyer-section", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8, leading=10, alignment=1, textColor=BLUE)
SUBSECTION = ParagraphStyle("flyer-subsection", parent=BODY, fontName="DejaVuSerif", fontSize=15, leading=18, alignment=1, textColor=NAVY)
CORE_LABEL = ParagraphStyle("flyer-core-label", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8.5, leading=10, alignment=1, textColor=HexColor("#B7CEE0"))
CORE_NAME = ParagraphStyle("flyer-core-name", parent=BODY, fontName="NorthwellAlt", fontSize=22, leading=25, alignment=1, textColor=WHITE)
CORE_DESC = ParagraphStyle("flyer-core-desc", parent=BODY, fontSize=10.5, leading=14, alignment=1, textColor=HexColor("#D7E6F2"))
CORE_INVITE = ParagraphStyle("flyer-core-invite", parent=BODY, fontName="DejaVuSans-Bold", fontSize=9.5, leading=12, alignment=1, textColor=WHITE)
NOTE = ParagraphStyle("flyer-note", parent=BODY, fontName="DejaVuSerif", fontSize=9.5, leading=12, alignment=1, textColor=NAVY)
MAP_LABEL = ParagraphStyle("flyer-map-label", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8.2, leading=9.5, alignment=1, textColor=NAVY)
MAP_CORE = ParagraphStyle("flyer-map-core", parent=BODY, fontName="DejaVuSerif-Bold", fontSize=11.5, leading=13, alignment=1, textColor=NAVY)
MIDDLE_LABEL = ParagraphStyle("flyer-middle-label", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8.5, leading=10, alignment=1, textColor=BLUE)
PANEL_INTRO = ParagraphStyle("flyer-panel-intro", parent=BODY, fontSize=9.2, leading=12, alignment=1, textColor=MUTE)
FRESH_HEADLINE = ParagraphStyle("fresh-headline", parent=BODY, fontName="DejaVuSerif", fontSize=27, leading=31, textColor=WHITE)
FRESH_INTRO = ParagraphStyle("fresh-intro", parent=BODY, fontSize=11.2, leading=15, textColor=HexColor("#D7E6F2"))
FRESH_SECTION = ParagraphStyle("fresh-section", parent=BODY, fontName="DejaVuSans-Bold", fontSize=8, leading=10, textColor=BLUE)
FRESH_LIST_TITLE = ParagraphStyle("fresh-list-title", parent=BODY, fontName="NorthwellAlt", fontSize=12.5, leading=14, textColor=INK)
FRESH_LIST_DESC = ParagraphStyle("fresh-list-desc", parent=BODY, fontSize=8, leading=10, textColor=MUTE)
FRESH_CORE_LABEL = ParagraphStyle("fresh-core-label", parent=BODY, fontName="DejaVuSans-Bold", fontSize=7.5, leading=9, textColor=HexColor("#B7CEE0"))
FRESH_CORE_NAME = ParagraphStyle("fresh-core-name", parent=BODY, fontName="NorthwellAlt", fontSize=20, leading=23, textColor=WHITE)
FRESH_CORE_DESC = ParagraphStyle("fresh-core-desc", parent=BODY, fontSize=9.2, leading=12, textColor=HexColor("#D7E6F2"))
FRESH_CTA = ParagraphStyle("fresh-cta", parent=BODY, fontName="DejaVuSans-Bold", fontSize=10.5, leading=13, textColor=WHITE)


COPY = {
    "en": {
        "lang": "ENGLISH",
        "strap": "ANTHROPOSOPHIC & INTEGRATIVE MEDICINE",
        "title": "Integrative care, time to listen.",
        "intro": "Gentle medical care for health, vitality and balance.",
        "middle_label": "A THOUGHTFUL WAY TO CARE",
        "place": "At L'Aubier, Montézillon",
        "core_label": "THE CORE PRACTICE",
        "core_name": "Anthroposophic external therapies",
        "core_desc": "A gentle, rhythmic approach using massage, warmth, oils, wraps and movement to support the body's own regulation.",
        "core_invite": "Begin with a first consultation: time to listen, understand and find your path.",
        "complementary": "COMPLEMENTARY THERAPIES",
        "complementary_intro": "Other therapies are added gently, tailored to your individual needs.",
        "note": "Thoughtful care for the whole person, never just the symptom.",
        "book": "Book an integrative medical consultation",
        "book_small": "Scan the QR code to choose a time online",
        "visit": "L'Aubier, Montézillon (NE), Switzerland",
        "contact": "+41 76 409 62 42  ·  info@stillbleu.ch",
        "footer": "Science, wisdom and compassion for conscious care.",
        "map_therapies": [
            "Acupuncture",
            "Yoga + breath",
            "Sound",
            "Qi therapies",
            "Integrative guidance",
        ],
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
        "intro": "Une médecine douce pour la santé, la vitalité et l'équilibre.",
        "middle_label": "UNE MANIÈRE ATTENTIVE DE SOIGNER",
        "place": "À L'Aubier, Montézillon",
        "core_label": "LE SOIN CENTRAL",
        "core_name": "Thérapies externes anthroposophiques",
        "core_desc": "Une approche douce et rythmique par le massage, la chaleur, les huiles, les enveloppements et le mouvement, pour soutenir la régulation du corps.",
        "core_invite": "Commencez par une première consultation : un temps pour vous écouter et trouver votre chemin.",
        "complementary": "THÉRAPIES COMPLÉMENTAIRES",
        "complementary_intro": "D'autres thérapies sont ajoutées avec douceur, selon vos besoins.",
        "note": "Un soin attentif pour la personne entière, jamais pour le seul symptôme.",
        "book": "Réserver une consultation médicale intégrative",
        "book_small": "Scannez le QR code pour choisir un horaire",
        "visit": "L'Aubier, Montézillon (NE), Suisse",
        "contact": "+41 76 409 62 42  ·  info@stillbleu.ch",
        "footer": "Science, sagesse et compassion pour un soin conscient.",
        "map_therapies": [
            "Acupuncture",
            "Yoga + souffle",
            "Son",
            "Soins du Qi",
            "Accompagnement",
        ],
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


def draw_map_label(pdf, text, x, y, width, height, style=MAP_LABEL):
    paragraph = Paragraph(text, style)
    _, paragraph_height = paragraph.wrap(width, height)
    paragraph.drawOn(pdf, x - width / 2, y - paragraph_height / 2)


def draw_flyer(language):
    copy = COPY[language]
    output = os.path.join(OUTPUT_DIR, f"stillbleu-flyer-{language}.pdf")
    width, height = A4
    margin = 18 * mm
    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(NAVY)
    pdf.rect(0, height - 96 * mm, width, 96 * mm, fill=1, stroke=0)
    pdf.setFillColor(BLUE)
    pdf.rect(0, height - 4 * mm, width, 4 * mm, fill=1, stroke=0)

    pdf.setFillColor(WHITE)
    pdf.setFont("NorthwellAlt", 34)
    pdf.drawString(margin, height - 13 * mm, "StillBleu")
    pdf.setFillColor(HexColor("#D7E6F2"))
    pdf.setFont("DejaVuSerif", 9.5)
    pdf.drawString(margin, height - 23 * mm, copy["strap"])
    pdf.setFillColor(HexColor("#D7E6F2"))
    pdf.setFont("DejaVuSans", 7.5)
    pdf.drawRightString(width - margin, height - 14 * mm, copy["lang"])
    logo_x = width - margin - 28 * mm
    logo_y = height - 55 * mm
    draw_logo(pdf, logo_x, logo_y, 27 * mm)

    title_top = height - 39 * mm
    title_height = draw_paragraph(pdf, copy["title"], HEADLINE, margin, title_top, 130 * mm)
    intro_top = title_top - title_height - 5 * mm
    intro_height = draw_paragraph(pdf, copy["intro"], INTRO, margin, intro_top, 130 * mm)
    pdf.setStrokeColor(HexColor("#B7CEE0"))
    pdf.setLineWidth(2.2)
    pdf.line(margin, intro_top - intro_height - 4 * mm, margin + 30 * mm, intro_top - intro_height - 4 * mm)
    pdf.setFillColor(HexColor("#D7E6F2"))
    pdf.setFont("DejaVuSans-Bold", 8.5)
    pdf.drawString(margin, intro_top - intro_height - 11 * mm, copy["place"])

    middle_top = 184 * mm
    draw_paragraph(pdf, copy["middle_label"], MIDDLE_LABEL, margin, middle_top, width - 2 * margin)

    core_top = 174 * mm
    core_bottom = 130 * mm
    pdf.setFillColor(NAVY)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(.7)
    pdf.roundRect(margin, core_bottom, width - 2 * margin, core_top - core_bottom, 3 * mm, fill=1, stroke=0)
    draw_paragraph(pdf, copy["core_label"], CORE_LABEL, margin + 8 * mm, core_top - 5 * mm, width - 2 * margin - 16 * mm)
    draw_paragraph(pdf, copy["core_name"], CORE_NAME, margin + 12 * mm, core_top - 12 * mm, width - 2 * margin - 24 * mm)
    core_desc_top = core_top - 23 * mm
    core_desc_height = draw_paragraph(pdf, copy["core_desc"], CORE_DESC, margin + 22 * mm, core_desc_top, width - 2 * margin - 44 * mm)
    invite_top = core_desc_top - core_desc_height - 2 * mm
    draw_paragraph(pdf, copy["core_invite"], CORE_INVITE, margin + 20 * mm, invite_top, width - 2 * margin - 40 * mm)

    complementary_top = 122 * mm
    complementary_bottom = 65 * mm
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(margin, complementary_bottom, width - 2 * margin, complementary_top - complementary_bottom, 3 * mm, fill=1, stroke=1)
    draw_paragraph(pdf, copy["complementary"], SUBSECTION, margin + 8 * mm, complementary_top - 5 * mm, width - 2 * margin - 16 * mm)
    draw_paragraph(pdf, copy["complementary_intro"], PANEL_INTRO, margin + 12 * mm, complementary_top - 14 * mm, width - 2 * margin - 24 * mm)

    list_top = complementary_top - 27 * mm
    column_width = 75 * mm
    column_gap = 10 * mm
    for index, (name, _) in enumerate(copy["therapies"]):
        row_index = index // 2
        column_index = index % 2
        x = margin + 8 * mm + column_index * (column_width + column_gap)
        y = list_top - row_index * 13 * mm
        pdf.setFillColor(BLUE)
        pdf.circle(x + 2 * mm, y - 3 * mm, 1.1 * mm, fill=1, stroke=0)
        draw_paragraph(pdf, name, THERAPY, x + 7 * mm, y, column_width - 7 * mm)

    footer_y = 10 * mm
    footer_height = 42 * mm
    pdf.setFillColor(NAVY)
    pdf.roundRect(margin, footer_y, width - 2 * margin, footer_height, 3 * mm, fill=1, stroke=0)
    draw_paragraph(pdf, copy["book"], BOOKING, margin + 8 * mm, footer_y + 33 * mm, 112 * mm)
    pdf.setFillColor(HexColor("#C9DCE9"))
    pdf.setFont("DejaVuSans", 8.5)
    pdf.drawString(margin + 8 * mm, footer_y + 25 * mm, copy["book_small"])
    pdf.setFont("DejaVuSans-Bold", 9)
    pdf.drawString(margin + 8 * mm, footer_y + 12 * mm, copy["visit"])
    pdf.setFont("DejaVuSans", 8.2)
    pdf.drawString(margin + 8 * mm, footer_y + 6 * mm, copy["contact"])

    code = qr.QrCodeWidget(BOOKING_URLS[language])
    code.barFillColor = HexColor("#000000")
    code.barStrokeColor = HexColor("#000000")
    size = 29 * mm
    code.barWidth = size
    code.barHeight = size
    drawing = Drawing(size, size)
    drawing.add(code)
    qr_x = width - margin - size - 8 * mm
    qr_y = footer_y + 6 * mm
    pdf.setFillColor(WHITE)
    pdf.rect(qr_x - 2 * mm, qr_y - 2 * mm, size + 4 * mm, size + 4 * mm, fill=1, stroke=0)
    renderPDF.draw(drawing, pdf, qr_x, qr_y)

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Italic", 8.5)
    pdf.drawCentredString(width / 2, 10 * mm, copy["footer"])
    pdf.save()
    print(f"Generated PDF: {output}")


def draw_flyer_fresh(language):
    copy = COPY[language]
    output = os.path.join(OUTPUT_DIR, f"stillbleu-flyer-{language}.pdf")
    width, height = A4
    margin = 16 * mm
    content_width = width - 2 * margin
    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(NAVY)
    pdf.rect(0, height - 108 * mm, width, 108 * mm, fill=1, stroke=0)
    pdf.setFillColor(BLUE)
    pdf.rect(0, height - 4 * mm, width, 4 * mm, fill=1, stroke=0)

    logo_size = 23 * mm
    logo_x = margin
    logo_y = height - 34 * mm
    pdf.setFillColor(WHITE)
    pdf.circle(logo_x + logo_size / 2, logo_y + logo_size / 2, logo_size / 2 + 3 * mm, fill=1, stroke=0)
    draw_logo(pdf, logo_x, logo_y, logo_size)
    pdf.setFillColor(WHITE)
    pdf.setFont("NorthwellAlt", 25)
    pdf.drawString(logo_x + 29 * mm, height - 18 * mm, "StillBleu")
    pdf.setFillColor(HexColor("#B7CEE0"))
    pdf.setFont("DejaVuSerif", 8.5)
    pdf.drawString(logo_x + 29 * mm, height - 25 * mm, copy["strap"])

    title_top = height - 47 * mm
    title_height = draw_paragraph(pdf, copy["title"], FRESH_HEADLINE, margin, title_top, 112 * mm)
    intro_top = title_top - title_height - 5 * mm
    intro_height = draw_paragraph(pdf, copy["intro"], FRESH_INTRO, margin, intro_top, 105 * mm)
    pdf.setStrokeColor(HexColor("#B7CEE0"))
    pdf.setLineWidth(1.5)
    pdf.line(margin, intro_top - intro_height - 5 * mm, margin + 25 * mm, intro_top - intro_height - 5 * mm)
    pdf.setFillColor(HexColor("#D7E6F2"))
    pdf.setFont("DejaVuSans-Bold", 8)
    pdf.drawString(margin, intro_top - intro_height - 12 * mm, copy["place"])

    middle_top = height - 119 * mm
    draw_paragraph(pdf, copy["middle_label"], FRESH_SECTION, margin, middle_top, content_width)

    core_top = height - 128 * mm
    core_bottom = height - 174 * mm
    pdf.setFillColor(NAVY)
    pdf.setStrokeColor(NAVY)
    pdf.roundRect(margin, core_bottom, content_width, core_top - core_bottom, 3 * mm, fill=1, stroke=0)
    draw_paragraph(pdf, copy["core_label"], FRESH_CORE_LABEL, margin + 8 * mm, core_top - 6 * mm, content_width - 16 * mm)
    draw_paragraph(pdf, copy["core_name"], FRESH_CORE_NAME, margin + 8 * mm, core_top - 13 * mm, content_width - 16 * mm)
    draw_paragraph(pdf, copy["core_desc"], FRESH_CORE_DESC, margin + 8 * mm, core_top - 27 * mm, content_width - 16 * mm)

    complement_top = height - 181 * mm
    draw_paragraph(pdf, copy["complementary"], FRESH_SECTION, margin, complement_top, content_width)
    draw_paragraph(pdf, copy["complementary_intro"], PANEL_INTRO, margin, complement_top - 6 * mm, content_width)

    list_top = height - 198 * mm
    column_width = 80 * mm
    column_gap = 10 * mm
    for index, (name, description) in enumerate(copy["therapies"]):
        row_index = index // 2
        column_index = index % 2
        x = margin + column_index * (column_width + column_gap)
        y = list_top - row_index * 15 * mm
        pdf.setFillColor(BLUE)
        pdf.circle(x + 2 * mm, y - 3 * mm, 1.1 * mm, fill=1, stroke=0)
        name_height = draw_paragraph(pdf, name, FRESH_LIST_TITLE, x + 7 * mm, y, column_width - 7 * mm)
        draw_paragraph(pdf, description, FRESH_LIST_DESC, x + 7 * mm, y - name_height - 1 * mm, column_width - 7 * mm)

    note_top = height - 253 * mm
    draw_paragraph(pdf, copy["note"], NOTE, margin, note_top, content_width)

    footer_y = 10 * mm
    footer_height = 39 * mm
    pdf.setFillColor(NAVY)
    pdf.roundRect(margin, footer_y, content_width, footer_height, 3 * mm, fill=1, stroke=0)
    draw_paragraph(pdf, copy["book"], FRESH_CTA, margin + 7 * mm, footer_y + 31 * mm, 100 * mm)
    pdf.setFillColor(HexColor("#C9DCE9"))
    pdf.setFont("DejaVuSans", 8)
    pdf.drawString(margin + 7 * mm, footer_y + 22 * mm, copy["book_small"])
    pdf.setFont("DejaVuSans-Bold", 8.5)
    pdf.drawString(margin + 7 * mm, footer_y + 11 * mm, copy["visit"])
    pdf.setFont("DejaVuSans", 8)
    pdf.drawString(margin + 7 * mm, footer_y + 5 * mm, copy["contact"])

    code = qr.QrCodeWidget(BOOKING_URLS[language])
    code.barFillColor = HexColor("#000000")
    code.barStrokeColor = HexColor("#000000")
    size = 25 * mm
    code.barWidth = size
    code.barHeight = size
    drawing = Drawing(size, size)
    drawing.add(code)
    qr_x = width - margin - size - 7 * mm
    qr_y = footer_y + 7 * mm
    pdf.setFillColor(WHITE)
    pdf.rect(qr_x - 2 * mm, qr_y - 2 * mm, size + 4 * mm, size + 4 * mm, fill=1, stroke=0)
    renderPDF.draw(drawing, pdf, qr_x, qr_y)

    pdf.setFillColor(NAVY)
    pdf.setFont("DejaVuSerif", 8)
    pdf.drawCentredString(width / 2, 5 * mm, copy["footer"])
    pdf.save()
    print(f"Generated PDF: {output}")


os.makedirs(OUTPUT_DIR, exist_ok=True)
for language in ("en", "fr"):
    draw_flyer_fresh(language)
