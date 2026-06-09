from io import BytesIO
from pathlib import Path

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas

FONT_NAME_DEVANAGARI = "NotoSansDevanagari"
FONT_FILE = "NotoSansDevanagari-Regular.ttf"
FONT_PATH = Path(settings.BASE_DIR) / "main" / "fonts" / FONT_FILE

FONT_REGISTERED = False


def register_fonts():
    global FONT_REGISTERED
    if FONT_REGISTERED:
        return FONT_NAME_DEVANAGARI
    
    try:
        if FONT_PATH.exists():
            pdfmetrics.registerFont(TTFont(FONT_NAME_DEVANAGARI, str(FONT_PATH)))
            FONT_REGISTERED = True
            return FONT_NAME_DEVANAGARI
    except Exception:
        pass
    
    return "Helvetica"


def _format_gender(value):
    if not value:
        return ""
    return {
        "Male": "पुरुष / Male",
        "Female": "स्त्री / Female"
    }.get(value, value)


def build_member_pdf(member):
    buffer = BytesIO()
    font_name = register_fonts()

    styles = getSampleStyleSheet()
    
    # Professional header style
    header_deco_style = ParagraphStyle(
        "HeaderDeco",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=colors.HexColor("#1a1a1a"),
    )
    
    # Organization line - clear and simple
    org_line1_style = ParagraphStyle(
        "OrgLine1",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#000000"),
    )
    
    # Main organization name
    org_name_style = ParagraphStyle(
        "OrgName",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#000000"),
    )
    
    # Form title - prominent
    form_title_style = ParagraphStyle(
        "FormTitle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#000000"),
        spaceAfter=6,
    )
    
    # Field label style
    label_style = ParagraphStyle(
        "LabelStyle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=8,
        leading=10,
        alignment=0,
        textColor=colors.HexColor("#000000"),
    )
    
    # Field value style
    value_style = ParagraphStyle(
        "ValueStyle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=8,
        leading=10,
        alignment=0,
        textColor=colors.HexColor("#333333"),
    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=10,
        leftMargin=10,
        topMargin=10,
        bottomMargin=10,
    )

    elements = []
    
    # Professional header - clean and simple
    elements.append(
        Paragraph(
            "॥   मांगीरबाबा प्रसन्न   ॥   जय लहुजी   ॥   जय महाराष्ट्र   ॥",
            header_deco_style,
        )
    )
    elements.append(Spacer(5, 3))
    
    elements.append(
        Paragraph(
            "विश्वभूषण अण्णाभाऊ साठे फाउंडेशन नाशिक (नोंदणी क्रमांकः महा / 527 / वा / 2017) संचालित",
            org_line1_style,
        )
    )
    elements.append(Spacer(1, 2))
    
    # Main organization title
    elements.append(
        Paragraph(
            "मातंग समाज वधुवर व पालक परिचय मंडळ नाशिक",
            org_name_style,
        )
    )
    elements.append(Spacer(1, 1))
    
    # Form title
    elements.append(
        Paragraph(
            "वधुवर मेळावा नोंदणी अर्ज (वर्ष ९ वे)",
            form_title_style,
        )
    )
    elements.append(Spacer(1, 4))

    # Photo box - professional look
    image_cell = Paragraph("<i>फोटो / Photo</i>", value_style)
    if member.photo and getattr(member.photo, "path", None):
        try:
            image = Image(member.photo.path, width=1.0 * inch, height=1.2 * inch)
            image_cell = image
        except Exception:
            pass

    photo_box = Table(
        [
            [Paragraph("<b>फोटो / Photo</b>", label_style)],
            [image_cell],
        ],
        colWidths=[105],
        rowHeights=[16, 95],
    )
    photo_box.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ]
        )
    )

    # Build form data with all fields
    form_fields = [
        ("१. नाव / सरनेव नाव", member.full_name or ""),
        ("२. लिंग", _format_gender(member.gender)),
        ("३. शिक्षण", member.education or ""),
        ("४. जन्म तारीख", str(member.birth_date)),
        ("५. वय", str(member.age)),
        ("६. उंची", member.height or ""),
        ("७. रंग", member.complexion or ""),
        ("८. व्यवसाय", member.occupation or ""),
        ("९. वार्षिक उत्पन्न", member.annual_income or ""),
        ("१०. मोबाईल", member.mobile or ""),
        ("११. ई-मेल", member.email or ""),
        ("१२. पत्ता", member.address or ""),
        ("१३. मूळ ठिकाण", member.native_place or ""),
        ("१४. वडिलांचे नाव", member.father_name or ""),
        ("१५. वडिलांचे व्यवसाय", member.father_occupation or ""),
        ("१६. आईचे नाव", member.mother_name or ""),
        ("१७. जात", member.caste or ""),
        ("१८. उपजात", member.sub_caste or ""),
        ("१९. गोत्र", member.gotra or ""),
        ("२०. रक्तगट", member.blood_group or ""),
        ("२१. भाऊ", str(member.brothers)),
        ("२२. बहिणी", str(member.sisters)),
    ]

    data = []
    for i, (label, value) in enumerate(form_fields):
        if i == 0:
            # First row with photo box
            data.append([
                Paragraph(f"<b>{label}</b>", label_style),
                Paragraph(value or "", value_style),
                photo_box
            ])
        else:
            # Regular rows
            data.append([
                Paragraph(f"<b>{label}</b>", label_style),
                Paragraph(value or "", value_style),
                ""
            ])

    # Main data table with proper spacing
    table = Table(data, colWidths=[130, 260, 110], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f0f0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWHEIGHTS", (0, 0), (-1, -1), 16),
                ("ALIGN", (2, 0), (2, 0), "CENTER"),
                ("VALIGN", (2, 0), (2, 0), "TOP"),
            ]
        )
    )
    
    elements.append(table)
    elements.append(Spacer(1, 8))

    # Expectations section
    if member.expectations:
        elements.append(
            Paragraph(
                f"<b>अपेक्षा:</b> {member.expectations}",
                value_style,
            )
        )
        elements.append(Spacer(1, 4))

    # Relative info if available
    if member.relative_info:
        elements.append(
            Paragraph(
                f"<b>नातेवाईक माहिती:</b> {member.relative_info}",
                value_style,
            )
        )
        elements.append(Spacer(1, 4))
    
    elements.append(Spacer(1, 8))
    
    # Signature sections - professional layout
    sig_table_data = [
        [
            Paragraph("<b>सदस्य सही / Member Signature</b>", label_style),
            "",
            Paragraph("<b>नोंदणीकर्ता साक्ष्य / Registrar Sign</b>", label_style)
        ]
    ]
    
    sig_table = Table(sig_table_data, colWidths=[130, 260, 110])
    sig_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("TOPPADDING", (0, 0), (-1, -1), 20),
            ]
        )
    )
    elements.append(sig_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


