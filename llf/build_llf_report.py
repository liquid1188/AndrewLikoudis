#!/usr/bin/env python3
"""
Likoudis Legacy Foundation — Lifetime Giving Report
Generated for patron recognition purposes.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.platypus import PageBreak

OUTPUT = "/mnt/user-data/outputs/LLF_Lifetime_Giving_Report.pdf"

# Brand colors
NAVY   = colors.HexColor("#1B2B5E")
GOLD   = colors.HexColor("#C9A84C")
IVORY  = colors.HexColor("#F8F5EE")
GRAY   = colors.HexColor("#6B7280")
LIGHT  = colors.HexColor("#EDE8DC")

def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontName="Times-Bold",
        fontSize=28,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=34,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        fontName="Times-Italic",
        fontSize=14,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="FounderLetter",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_JUSTIFY,
        spaceAfter=7,
        leading=15,
        leftIndent=0,
        rightIndent=0,
    ))
    styles.add(ParagraphStyle(
        name="SectionHead",
        fontName="Times-Bold",
        fontSize=12,
        textColor=NAVY,
        spaceAfter=4,
        spaceBefore=8,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="SubHead",
        fontName="Times-Bold",
        fontSize=10,
        textColor=GOLD,
        spaceAfter=4,
        spaceBefore=6,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="LLFBodyText",
        fontName="Times-Roman",
        fontSize=10.5,
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name="Caption",
        fontName="Times-Italic",
        fontSize=9,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="PatronName",
        fontName="Times-Bold",
        fontSize=10,
        textColor=NAVY,
        spaceAfter=1,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="PatronTier",
        fontName="Times-Italic",
        fontSize=10,
        textColor=GOLD,
        spaceAfter=8,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="FooterText",
        fontName="Times-Italic",
        fontSize=9,
        textColor=GRAY,
        alignment=TA_CENTER,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Salutation",
        fontName="Times-Bold",
        fontSize=12,
        textColor=NAVY,
        spaceAfter=10,
        leading=16,
    ))
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter

    # Top rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.5)
    canvas.line(0.65*inch, h - 0.55*inch, w - 0.65*inch, h - 0.55*inch)

    # Header text
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.65*inch, h - 0.45*inch, "Likoudis Legacy Foundation")
    canvas.drawRightString(w - 0.65*inch, h - 0.45*inch, "Lifetime Giving Report")

    # Bottom rule
    canvas.setStrokeColor(GOLD)
    canvas.line(0.65*inch, 0.65*inch, w - 0.65*inch, 0.65*inch)

    # Page number
    canvas.setFont("Times-Roman", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(w / 2, 0.45*inch, str(doc.page))

    canvas.restoreState()



def compact_header(styles):
    story = []
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=8))
    story.append(Paragraph("LIKOUDIS LEGACY FOUNDATION", styles["ReportTitle"]))
    story.append(Paragraph(
        "Lifetime Giving Report — Patron Recognition &amp; Foundation Highlights",
        styles["ReportSubtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))
    return story

def cover_page(styles):
    story = []

    story.append(Spacer(1, 0.5*inch))

    # Gold rule
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=24))

    story.append(Paragraph("LIKOUDIS LEGACY FOUNDATION", styles["ReportTitle"]))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Lifetime Giving Report", styles["ReportSubtitle"]))
    story.append(Paragraph("Patron Recognition &amp; Foundation Highlights", styles["ReportSubtitle"]))

    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=28))

    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph(
        "Ecumenical scholarship. Catholic formation.<br/>"
        "Building on the intellectual legacy of James Likoudis.",
        ParagraphStyle(
            name="CoverTagline",
            fontName="Times-Italic",
            fontSize=13,
            textColor=NAVY,
            alignment=TA_CENTER,
            leading=22,
            spaceAfter=0,
        )
    ))

    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(
        "The Likoudis Legacy Foundation is a 501(c)(3) research institute dedicated to "
        "ecumenical scholarship, Catholic formation, and building on the intellectual legacy of "
        "James Likoudis—theologian, apologist, and lay Catholic who devoted more than "
        "seventy years to the reunion of East and West. The Foundation advances that work "
        "through education, publication, and service to dioceses and the wider Church.",
        ParagraphStyle(
            name="CoverDesc",
            fontName="Times-Roman",
            fontSize=10.5,
            textColor=colors.HexColor("#2a2a2a"),
            alignment=TA_CENTER,
            leading=17,
            spaceAfter=0,
            leftIndent=0.4*inch,
            rightIndent=0.4*inch,
        )
    ))

    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph(
        "Prepared for the Foundation's patrons and friends<br/>"
        "in gratitude for their generosity and partnership.",
        ParagraphStyle(
            name="CoverNote",
            fontName="Times-Roman",
            fontSize=10,
            textColor=GRAY,
            alignment=TA_CENTER,
            leading=16,
            spaceAfter=0,
        )
    ))

    story.append(PageBreak())
    return story


def letter_from_andrew(styles):
    story = []

    story.append(Paragraph("A Letter from the Founder", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LIGHT, spaceAfter=14))

    story.append(Paragraph("Dear Friends,", styles["Salutation"]))


    story.append(Paragraph(
        "Three years in: a journal taking shape, a conference coming in July, "
        "grant applications submitted, a Substack past 1,200 readers. It seemed "
        "like the right time to put something on paper for the people who made it "
        "possible. My grandfather James Likoudis, whose name the Foundation carries, "
        "spent seventy years working toward the reunion of East and West. "
        "He never saw the full reunion. We hope to. The 1000th anniversary of the "
        "Great Schism falls in 2054 — that is the horizon we are working toward.",
        styles["FounderLetter"]
    ))


    story.append(Paragraph(
        "<i>Faith in Crisis</i> is out: a forty-chapter volume, with a foreword by Rocco "
        "Buttiglione and an essay by Cardinal Robert Sarah, that takes the polarization "
        "dividing Catholics head-on without flinching into either camp. "
        "<i>Ending the Byzantine Greek Schism</i>, revised and with a foreword by Scott "
        "Hahn, is forthcoming. Tradition &amp; Renewal has grown "
        "past 1,200 subscribers. The Book Club is running its first reading under Liz "
        "Moncada Sandoval, opening with James Likoudis's own <i>Divine Primacy</i>. The "
        "Kydones Review has received its first round of submissions and is being prepared "
        "for a Fall 2026 launch. The Foundation's website has been rebuilt from the ground "
        "up: separate pages for every program, a fellows section, diocesan consulting, "
        "press archive, and the full journal infrastructure for the Kydones Review. It "
        "reflects what the Foundation has actually become. The Orientale Lumen conference "
        "convenes this July, the 30th in the annual series founded by Jack Figel, "
        "hosted in partnership with his Orientale Lumen Foundation. "
        "Archbishop Flavio Pace (Secretary, Dicastery for Promoting Christian Unity) "
        "and Cardinal O'Malley are confirmed speakers. Bishop Madden will attend.",
        styles["FounderLetter"]
    ))

    story.append(Paragraph(
        "We have also submitted a Letter of Intent to the Lilly Endowment's Exploring "
        "Christian Practices Initiative, a proposal centered on pilgrimage to the five "
        "ancient patriarchal sees, and prepared an application to the John Templeton Foundation "
        "for this year's grant cycle. These are "
        "the first real institutional funding efforts the Foundation has made. The full Lilly "
        "proposal is due in May.",
        styles["FounderLetter"]
    ))

    story.append(Paragraph(
        "None of this would be moving without you. This report is a straightforward account "
        "of what your support has made possible. I am grateful for it. If you feel moved "
        "to give again, the link at the bottom of this document will take you there.",
        styles["FounderLetter"]
    ))

    story.append(Paragraph(
        "With gratitude and in communion,",
        ParagraphStyle(
            name="Closing",
            fontName="Times-Italic",
            fontSize=11,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=4,
            leading=16,
        )
    ))

    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(
        "Andrew Likoudis",
        ParagraphStyle(
            name="Sig",
            fontName="Times-Bold",
            fontSize=12,
            textColor=NAVY,
            spaceAfter=2,
            leading=16,
        )
    ))
    story.append(Paragraph(
        "Founder &amp; Chairman, Likoudis Legacy Foundation",
        ParagraphStyle(
            name="SigTitle",
            fontName="Times-Roman",
            fontSize=10,
            textColor=GRAY,
            spaceAfter=0,
            leading=14,
        )
    ))

    story.append(Spacer(1, 0.15*inch))
    return story


def highlights_section(styles):
    story = []

    story.append(Paragraph("Foundation Highlights", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LIGHT, spaceAfter=14))

    highlights = [
        (
            "Ending the Byzantine Greek Schism — Revised Edition",
            "A revised third edition of James Likoudis's <i>Ending the Byzantine Greek "
            "Schism</i>, one of the most thorough lay Catholic treatments of the "
            "Catholic-Orthodox divide, is forthcoming with a foreword by Scott Hahn."
        ),
        (
            "Tradition &amp; Renewal — Over 1,200 Subscribers",
            "<link href=\"https://traditionandrenewal.com\">Tradition &amp; Renewal</link> "
            "covers ten thematic sections, from magisterial commentary to ecumenism,"
            "and has grown to over 1,200 subscribers."
        ),
        (
            "Orientale Lumen Conference — July 13-15, 2026",
            "The LLF's inaugural conference, hosted in partnership with Jack Figel's "
            "Orientale Lumen Foundation, marking the 30th year of OLF's annual series. "
            "Archbishop Flavio Pace (Secretary, Dicastery for Promoting Christian Unity) "
            "and Cardinal Sean O'Malley are confirmed speakers. Bishop Madden will attend."
        ),
        (
            "Book Club",
            "The Foundation's Book Club has received a number of signups and launches at the end of May, led by Liz Moncada Sandoval. The inaugural reading is <i>Divine Primacy</i> by James Likoudis."
        ),
        (
            "The Kydones Review",
            "The Foundation's peer-reviewed journal has received a number of submissions and is being prepared for its first volume, due out in Fall 2026, on the theme <i>Christian Unity in a Fragmented Age</i>. The journal has added three members to its editorial board: Vladan Stankovic, PhD; Fabio Salgado, PhD; Luke DeWeese, JD; and Liz Moncada Sandoval."
        ),
        (
            "Recent Writing — Communion Posture Series",
            "A two-part series at <i>Where Peter Is</i> on the theology of posture at Communion. "
            "Part I: <link href=\"https://wherepeteris.com/the-case-for-standing-to-receive-communion/\">"
            "The historical and liturgical case</link>. "
            "Part II: <link href=\"https://wherepeteris.com/standing-to-receive-communion-part-ii-the-anthropological-question/\">"
            "The anthropological question</link>."
        ),
        (
            "Institutional Funding — Lilly Endowment &amp; Templeton Foundation",
            "The Foundation has submitted a Letter of Intent to the Lilly Endowment's "
            "Exploring Christian Practices Initiative (full proposal due May 2026) and "
            "prepared an application to the John Templeton Foundation for this year's grant cycle, the Foundation's first major "
            "institutional funding efforts."
        ),
    ]

    for title, body in highlights:
        story.append(KeepTogether([
            Paragraph(title, styles["SubHead"]),
            Paragraph(body, styles["LLFBodyText"]),
        ]))

    story.append(Spacer(1, 0.1*inch))
    return story


def giving_summary(styles):
    story = []

    story.append(Paragraph("Lifetime Giving", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LIGHT, spaceAfter=10))

    story.append(Paragraph(
        "The following recognizes all those who have given to the Likoudis Legacy Foundation "
        "since its founding. As the Foundation is in its early years, this report covers "
        "lifetime giving in full. Future reports will transition to annual cycles.",
        styles["LLFBodyText"]
    ))
    story.append(Spacer(1, 0.1*inch))
    return story


def patron_recognition(styles):
    story = []

    story.append(Paragraph("Patron Recognition", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LIGHT, spaceAfter=8))

    # Build a two-column recognition table
    tier_style = ParagraphStyle(name="TierHead", fontName="Times-Bold", fontSize=10,
                                textColor=GOLD, spaceAfter=2, leading=13)
    tier_desc = ParagraphStyle(name="TierSub", fontName="Times-Italic", fontSize=8,
                               textColor=GRAY, spaceAfter=2, leading=10)
    name_style = ParagraphStyle(name="PName", fontName="Times-Roman", fontSize=10,
                                textColor=NAVY, spaceAfter=0, leading=12)

    col1 = []
    col1.append(Paragraph("Founders Circle", tier_style))
    col1.append(Paragraph("Gifts of $1,000 or more", tier_desc))
    for n in ["Alice Grayson", "Elizabeth A. Zilbauer"]:
        col1.append(Paragraph(n, name_style))
    col1.append(Spacer(1, 4))
    col1.append(Paragraph("Benefactors", tier_style))
    col1.append(Paragraph("Gifts of $100 to $499", tier_desc))
    for n in ["Philip Blosser", "Pauline Parker", "Joseph F. Caskey",
              "Will Deatherage", "Todd Voss"]:
        col1.append(Paragraph(n, name_style))

    col2 = []
    col2.append(Paragraph("Patrons", tier_style))
    col2.append(Paragraph("Gifts of $500 to $999", tier_desc))
    for n in ["Cardinal Raymond Leo Burke", "Ben Fraser"]:
        col2.append(Paragraph(n, name_style))
    col2.append(Spacer(1, 4))
    col2.append(Paragraph("Supporters", tier_style))
    col2.append(Paragraph("All gifts up to $99", tier_desc))
    for n in ["Colin Miller", "Jon Jacobsen", "Robert Fastiggi",
              "Anonymous Friends of the Foundation (5)"]:
        col2.append(Paragraph(n, name_style))

    from reportlab.platypus import Frame, PageTemplate
    from reportlab.lib.units import inch

    # Use a two-column table to simulate columns
    data = [[col1, col2]]
    col_table = Table(data, colWidths=[3.3*inch, 3.3*inch])
    col_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(col_table)
    story.append(Spacer(1, 0.1*inch))
    return story


def closing_section(styles):
    story = []

    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=4))

    story.append(Paragraph(
        "The Likoudis Legacy Foundation is a 501(c)(3) tax-exempt organization. "
        "All gifts are tax-deductible to the extent permitted by law. "
        "We intend to list patron names on our website. If you prefer not to be "
        "listed, please let us know at alikoudis@likoudislegacy.com.",
        ParagraphStyle(
            name="Legal",
            fontName="Times-Roman",
            fontSize=9,
            textColor=GRAY,
            alignment=TA_CENTER,
            leading=12,
            spaceAfter=4,
        )
    ))

    story.append(Paragraph(
        "<link href=\"https://donate.stripe.com/8x200beyMgHugS84Xla3u00\">Make a gift →</link>",
        ParagraphStyle(
            name="GiftLink",
            fontName="Times-Bold",
            fontSize=10,
            textColor=GOLD,
            alignment=TA_CENTER,
            leading=14,
            spaceAfter=4,
        )
    ))

    story.append(Paragraph(
        "<link href=\"https://likoudislegacy.com\">likoudislegacy.com</link>",
        ParagraphStyle(
            name="Website",
            fontName="Times-Bold",
            fontSize=10,
            textColor=NAVY,
            alignment=TA_CENTER,
            leading=14,
            spaceAfter=0,
        )
    ))

    return story


def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.65*inch,
        bottomMargin=0.55*inch,
        title="LLF Lifetime Giving Report",
        author="Likoudis Legacy Foundation",
    )

    styles = build_styles()

    story = []
    story += cover_page(styles)
    story += letter_from_andrew(styles)
    story += highlights_section(styles)
    story += giving_summary(styles)
    story += patron_recognition(styles)
    story += closing_section(styles)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF built:", OUTPUT)


if __name__ == "__main__":
    main()
