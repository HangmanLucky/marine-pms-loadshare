# -*- coding: utf-8 -*-
"""
Ebook generator - Marine Automation Portfolio series
Project 3: Autonomous Marine Power Management System (PMS)
Author: Sipho Lucky Sibanda
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Oblique", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Cond-Bold", FD + "DejaVuSansCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cond", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "DejaVuSansMono-Bold.ttf"))

# ---------------------------------------------------------------------------
# Palette - blue/amber "switchboard" identity for this project
# ---------------------------------------------------------------------------
BASE      = colors.HexColor("#08121F")
BASE2     = colors.HexColor("#0E1B2E")
BASE_LINE = colors.HexColor("#14304F")
BLUEACC   = colors.HexColor("#7FB3F0")
BLUEACC_LT= colors.HexColor("#CFE3FB")
DEEPBLUE  = colors.HexColor("#1D4E89")
TEAL      = colors.HexColor("#2FBE96")
AMBER     = colors.HexColor("#F5A623")
RED       = colors.HexColor("#E0503E")
BLUE      = colors.HexColor("#4F8EF7")
INK       = colors.HexColor("#101E30")
MUTED     = colors.HexColor("#5C7290")
MUTED_LT  = colors.HexColor("#AFC8E8")
PANEL     = colors.HexColor("#EDF3FB")
ROWBAND   = colors.HexColor("#F5F9FD")
GRIDLINE  = colors.HexColor("#D7E2F0")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 22 * mm, 20 * mm
MARGIN_TOP, MARGIN_BOT = 26 * mm, 24 * mm
AVAIL_W = PAGE_W - MARGIN_L - MARGIN_R

DOC_TITLE = "MARINE POWER MANAGEMENT SYSTEM (PMS)"
AUTHOR = "Sipho Lucky Sibanda"
OUTFILE = "/home/claude/marine-pms-loadshare/ebook/PMS_Technical_Manual.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
body = ParagraphStyle("body", fontName="Sans", fontSize=10.2, leading=15,
                       textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY)
body_l = ParagraphStyle("body_l", parent=body, alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=12.5, leading=18, textColor=DEEPBLUE,
                       spaceAfter=10)
kicker = ParagraphStyle("kicker", fontName="Mono", fontSize=8.5, leading=11,
                         textColor=DEEPBLUE, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Cond-Bold", fontSize=19, leading=22,
                     textColor=colors.HexColor("#14304F"), spaceAfter=2)
h2 = ParagraphStyle("h2", fontName="Cond-Bold", fontSize=13.5, leading=16,
                     textColor=colors.HexColor("#14304F"), spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.6, leading=13,
                     textColor=colors.HexColor("#14304F"), spaceBefore=8, spaceAfter=4)
caption = ParagraphStyle("caption", fontName="Sans-Oblique", fontSize=8.3, leading=11,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
bullet = ParagraphStyle("bullet", parent=body, alignment=TA_LEFT, leftIndent=12,
                         bulletIndent=0, spaceAfter=5)
chip_num = ParagraphStyle("chip_num", fontName="Cond-Bold", fontSize=17, leading=20,
                           textColor=colors.white, alignment=TA_CENTER)
toc_entry = ParagraphStyle("toc_entry", fontName="Sans", fontSize=10.5, leading=16,
                            textColor=INK)
toc_num = ParagraphStyle("toc_num", fontName="Mono-Bold", fontSize=10.5, leading=16,
                          textColor=DEEPBLUE)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Sans-Bold", fontSize=8.6, leading=11,
                           textColor=colors.white)
cell_txt = ParagraphStyle("cell_txt", fontName="Sans", fontSize=8.6, leading=12,
                           textColor=INK)
code_style = ParagraphStyle("code", fontName="Mono", fontSize=7.6, leading=11.2,
                             textColor=BLUEACC_LT)
callout_title = lambda c: ParagraphStyle("ct", fontName="Sans-Bold", fontSize=9.6,
                                          leading=12, textColor=c, spaceAfter=3)
callout_body = ParagraphStyle("cb", fontName="Sans", fontSize=9.4, leading=13.4,
                               textColor=INK)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def P(text, style=body):
    return Paragraph(text, style)

def chapter_head(num, title, kicker_text="PMS POWER MANAGEMENT"):
    chip = Table([[Paragraph(str(num).zfill(2), chip_num)]],
                 colWidths=[17 * mm], rowHeights=[17 * mm])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEPBLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    title_block = [P(kicker_text, kicker), P(title, h1)]
    row = Table([[chip, title_block]], colWidths=[22 * mm, AVAIL_W - 22 * mm])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    rule = HRFlowable(width="100%", thickness=1.3, color=BLUEACC, spaceBefore=8, spaceAfter=16)
    return [row, rule]

def subhead(text):
    return P(text, h2)

def bullets(items):
    out = []
    for it in items:
        out.append(P("&#8226;&nbsp;&nbsp;" + it, bullet))
    return out

def code_block(code_text, cap=None):
    lines = code_text.strip("\n").split("\n")
    esc_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        n = len(ln) - len(stripped)
        esc_lines.append("&nbsp;" * n + esc(stripped) if stripped else "&nbsp;")
    para = Paragraph("<br/>".join(esc_lines), code_style)
    cell = Table([[para]], colWidths=[AVAIL_W])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BASE2),
        ("BOX", (0, 0), (-1, -1), 0.75, BASE_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    out = [cell]
    if cap:
        out.append(P(cap, caption))
    else:
        out.append(Spacer(1, 10))
    return out

def data_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, cell_hdr) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cell_txt) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14304F")),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIDLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBAND))
    t.setStyle(TableStyle(style))
    return t

def callout(title, text, kind="info"):
    color = {"info": BLUE, "warning": AMBER, "critical": RED, "ok": TEAL}[kind]
    label = {"info": "NOTE", "warning": "ENGINEERING NOTE", "critical": "SAFETY CRITICAL",
             "ok": "DESIGN NOTE"}[kind]
    content = [P("%s &mdash; %s" % (label, title), callout_title(color)), P(text, callout_body)]
    inner = Table([[content]], colWidths=[AVAIL_W - 16])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([["", inner]], colWidths=[5, AVAIL_W - 5])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), PANEL),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [outer, Spacer(1, 10)]

def full_image(path, cap, max_h_mm=95):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / float(iw)
    w = AVAIL_W
    h = w * ratio
    max_h = max_h_mm * mm
    if h > max_h:
        h = max_h
        w = h / ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    return [img, P(cap, caption)]


# ---------------------------------------------------------------------------
# Page backgrounds
# ---------------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.4)
    step = 12 * mm
    x = 0
    while x < PAGE_W:
        c.line(x, 0, x, PAGE_H); x += step
    y = 0
    while y < PAGE_H:
        c.line(0, y, PAGE_W, y); y += step

    c.setStrokeColor(BLUEACC)
    c.setLineWidth(1.1)
    c.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, fill=0, stroke=1)

    # Decorative synchroscope glyph, bottom right
    c.setStrokeColor(BLUEACC)
    c.setLineWidth(1.2)
    cx, cy, r = PAGE_W - 46 * mm, 52 * mm, 16 * mm
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setLineWidth(1.6)
    c.setStrokeColor(AMBER)
    import math
    ang = math.radians(35)
    c.line(cx, cy, cx + r*0.75*math.sin(ang), cy + r*0.75*math.cos(ang))
    c.setFillColor(AMBER)
    c.circle(cx, cy, 1.6*mm, fill=1, stroke=0)
    c.setFillColor(BLUEACC)
    c.setFont("Mono-Bold", 7)
    c.drawCentredString(cx, cy - r - 7*mm, "SYNC")

    c.setFillColor(BLUEACC)
    c.setFont("Mono", 10.5)
    c.drawString(24 * mm, PAGE_H - 42 * mm, "MARINE AUTOMATION PORTFOLIO   ·   PROJECT 03")

    c.setFillColor(colors.white)
    c.setFont("Cond-Bold", 27)
    for i, line in enumerate(["AUTONOMOUS MARINE POWER", "MANAGEMENT SYSTEM (PMS)"]):
        c.drawString(24 * mm, PAGE_H - 62 * mm - i * 11.5 * mm, line)

    c.setFont("Cond", 13.5)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, PAGE_H - 90 * mm, "Intelligent Load-Shedding, Auto-Synchronising")
    c.drawString(24 * mm, PAGE_H - 97 * mm, "and Blackout Recovery")

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.8)
    c.line(24 * mm, 46 * mm, PAGE_W - 24 * mm, 46 * mm)

    c.setFont("Mono", 9.5)
    c.setFillColor(AMBER)
    c.drawString(24 * mm, 38 * mm, "TECHNICAL PROJECT MANUAL  ·  REV. A")
    c.setFont("Sans-Bold", 13)
    c.setFillColor(colors.white)
    c.drawString(24 * mm, 31 * mm, "By " + AUTHOR)
    c.setFont("Sans", 8.6)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, 25.5 * mm, "PLC Platform: Siemens S7-1500 (SCL) / CODESYS-portable Structured Text")
    c.drawString(24 * mm, 21 * mm, "Simulation & Portfolio Engineering Build  ·  Not for Shipboard Deployment")
    c.restoreState()

def draw_body(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    c.setFillColor(BLUEACC)
    c.setFont("Mono", 7.6)
    c.drawString(MARGIN_L, PAGE_H - 9.5 * mm, DOC_TITLE)
    c.setFillColor(colors.white)
    c.setFont("Sans", 7.4)
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9.5 * mm, "By " + AUTHOR)
    c.setStrokeColor(BLUEACC)
    c.setLineWidth(0.8)
    c.line(0, PAGE_H - 15 * mm, PAGE_W, PAGE_H - 15 * mm)

    c.setFillColor(MUTED)
    c.setFont("Mono", 7.8)
    c.drawString(MARGIN_L, 13 * mm, "PMS-POWER-MGMT")
    c.drawCentredString(PAGE_W / 2, 13 * mm, "Page %d" % c.getPageNumber())
    c.drawRightString(PAGE_W - MARGIN_R, 13 * mm, "Simulation / Portfolio Build")
    c.setStrokeColor(BLUEACC)
    c.setLineWidth(1)
    c.line(PAGE_W - MARGIN_R, 17 * mm, PAGE_W - MARGIN_R, 21 * mm)
    c.line(PAGE_W - MARGIN_R - 4 * mm, 17 * mm, PAGE_W - MARGIN_R, 17 * mm)
    c.restoreState()


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = [PageBreak()]

# ---- Document control / disclaimer ------------------------------------------------
story += chapter_head("i", "Document Control &amp; Disclaimer", "FRONT MATTER")
story.append(P(
    "This document is a self-authored technical project manual produced as part of a "
    "personal engineering portfolio. It describes the design, control philosophy, and "
    "simulated validation of a marine Power Management System (PMS) covering fast load "
    "shedding, auto-synchronising, and blackout recovery, built to demonstrate electrical "
    "sequencing logic, state-machine design, and marine regulatory awareness for "
    "automation, controls, and marine electrical engineering roles.", body))
story.append(P(
    "The system described here was developed and tested in simulation only (PLCSIM-style "
    "forcing of inputs and desktop review), using publicly available regulatory references "
    "for realism. No part of this project has been installed, commissioned, or verified on "
    "physical shipboard hardware, and it must not be treated as a certified or classed "
    "Power Management System.", body))

story += callout(
    "Portfolio project, not a certified PMS",
    "A real shipboard PMS requires generator and governor/AVR characterisation specific to "
    "the actual machinery installed, full load-sharing (droop) control, protection "
    "coordination studies, and class society approval before any of this logic could be "
    "considered for actual use. Figures, thresholds, and I/O in this manual are "
    "engineering-realistic but illustrative.", "critical")

data = [
    ["Document Title", "Autonomous Marine PMS \u2014 Technical Manual"],
    ["Author", AUTHOR],
    ["Revision", "A"],
    ["Document Type", "Portfolio Technical Manual (Simulation)"],
    ["Target PLC Platform", "Siemens S7-1500 (TIA Portal / SCL) \u2014 CODESYS-portable"],
    ["Related Repository", "marine-pms-loadshare"],
    ["Series", "Marine Automation Portfolio \u2014 Project 03"],
]
t = Table(data, colWidths=[45 * mm, AVAIL_W - 45 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Sans-Bold"), ("FONTNAME", (1, 0), (1, -1), "Sans"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.4), ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#14304F")),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, GRIDLINE),
    ("BACKGROUND", (0, 0), (0, -1), PANEL),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(t)
story.append(PageBreak())

# ---- Contents ------------------------------------------------------------
story += chapter_head("ii", "Contents", "FRONT MATTER")
toc = [
    ("01", "Regulatory &amp; Marine Context"),
    ("02", "System Architecture &amp; Process Overview"),
    ("03", "Hardware &amp; Instrumentation Specification"),
    ("04", "I/O List"),
    ("05", "Control Philosophy: Three Linked Problems"),
    ("06", "PLC Logic Walkthrough"),
    ("07", "HMI Design &amp; the Live Synchroscope"),
    ("08", "Alarm Philosophy &amp; Fail-Safe Design"),
    ("09", "Testing, Commissioning &amp; FAT Procedures"),
    ("10", "Limitations, Real-World Deltas &amp; Future Work"),
    ("A", "Appendix A &mdash; I/O Quick Reference"),
    ("B", "Appendix B &mdash; Full Structured Text Listing"),
    ("C", "Appendix C &mdash; Glossary"),
    ("&mdash;", "About the Author"),
]
rows = []
for num, title in toc:
    rows.append([P(num, toc_num), P(title, toc_entry)])
tt = Table(rows, colWidths=[14 * mm, AVAIL_W - 14 * mm])
tt.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, GRIDLINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tt)
story.append(PageBreak())

# ---- Executive Summary ----------------------------------------------------
story += chapter_head("iii", "Executive Summary", "FRONT MATTER")
story.append(P(
    "A ship that loses all electrical power isn't just inconvenienced &mdash; it's adrift, "
    "unable to steer, and at risk of collision or grounding until power is restored. This "
    "project simulates the PLC-side logic of a marine Power Management System, the software "
    "layer whose entire job is to make sure that scenario either never happens, or resolves "
    "itself in a matter of seconds rather than minutes.", lead))
story.append(P(
    "Three distinct problems are covered, and the manual is deliberately structured around "
    "keeping them separate, because conflating them is where real PMS bugs come from. "
    "<b>Fast load shedding</b> reacts to a generator suddenly tripping, shedding pre-defined "
    "load blocks in the time it takes to open a contactor &mdash; there's no time for a "
    "clever calculation. <b>Auto-synchronising</b> is the opposite kind of problem: patient, "
    "state-machine-driven, bringing a second generator's speed, voltage, and phase into "
    "alignment with a live bus before ever closing a breaker onto it. <b>Blackout recovery</b> "
    "is a third problem again &mdash; starting from nothing, with a bus that's genuinely dead "
    "rather than live and needing synchronisation.", body))
story.append(P(
    "The function block that ties these together, <b>FB_PMS_PowerManagement</b>, deliberately "
    "keeps a dead-bus reclose (no phase matching needed, because there's nothing to phase-match "
    "against) as a completely separate code path from a live synchronising sequence &mdash; "
    "closing a breaker onto a live bus without verifying phase alignment first is precisely "
    "the kind of mistake that damages generators, and the two paths are structured so that "
    "mistake isn't possible to make by accident.", body))
story.append(P(
    "What follows documents the regulatory basis, architecture, hardware assumptions, full "
    "I/O list, control philosophy, complete annotated code, HMI design (including a working "
    "synchroscope), alarm philosophy, and the functional test procedure used to validate the "
    "logic in simulation.", body))
story.append(PageBreak())

# ---- Chapter 1: Regulatory context ----------------------------------------
story += chapter_head(1, "Regulatory &amp; Marine Context")
story.append(P(
    "<b>SOLAS Chapter II-1</b> is the backbone regulation behind why this project exists at "
    "all. Regulations 42 and 43 require passenger and cargo ships respectively to carry a "
    "self-contained <b>emergency source of electrical power</b>, independent of the main "
    "generating plant, capable of supplying defined essential services &mdash; steering gear, "
    "navigation lights, emergency lighting, and fire-fighting equipment among them &mdash; "
    "within a strict time limit after a blackout. For most vessel types, that limit is "
    "<b>45 seconds</b>.", body))
story.append(P(
    "That single number &mdash; 45 seconds &mdash; is why blackout recovery in this project "
    "is automated rather than left to a duty engineer to run manually from a switchboard. A "
    "human being locating the right breaker, confirming conditions, and closing it by hand "
    "inside 45 seconds of a blackout, at night, possibly in heavy weather, is not a plan a "
    "class society will accept as the primary defence.", body))
story.append(subhead("Beyond the emergency generator: getting the main plant back"))
story.append(P(
    "SOLAS's 45-second requirement covers the emergency generator specifically. It says "
    "nothing about how quickly the <i>main</i> generating plant needs to be back online and "
    "carrying propulsion and normal ship's load &mdash; that's where classification society "
    "PMS notations and guidance (e.g. DNV's power management system requirements) come in, "
    "expecting a documented, largely automatic sequence for black-starting the main plant "
    "once the emergency source has stabilised the situation.", body))
story += callout(
    "Why load shedding gets its own regulatory attention",
    "IACS and class society rules also expect a generating plant to survive the loss of its "
    "largest single generator without a full blackout, provided load shedding acts fast "
    "enough. That single requirement is effectively the specification for this project's "
    "fast load-shedding logic (Chapter 5) &mdash; it isn't a nice-to-have feature, it's the "
    "mechanism that's supposed to prevent a single generator trip from cascading into the "
    "exact blackout scenario Chapter II-1 exists to recover from.", "info")
story.append(subhead("Standards referenced"))
story += bullets([
    "<b>SOLAS Chapter II-1, Regulations 42/43</b> &mdash; emergency source of electrical "
    "power and its distribution.",
    "<b>IEC 61892-1 / IEC 60092 series</b> &mdash; electrical installations on ships and "
    "offshore units.",
    "<b>Class society PMS guidance</b> &mdash; e.g. DNV-RU-SHIP Pt.4 Ch.8 on power "
    "management systems, covering load-dependent start/stop, load sharing, and blackout "
    "recovery expectations.",
])
story.append(PageBreak())

# ---- Chapter 2: Architecture ----------------------------------------------
story += chapter_head(2, "System Architecture &amp; Process Overview")
story.append(P(
    "Two main generators feed a common busbar through breakers, supervised by a "
    "synchronising relay that reports frequency, voltage, and phase angle whenever a "
    "paralleling attempt is in progress. An emergency generator sits on its own independent "
    "branch, exactly as SOLAS requires. Essential loads are wired to a section of the "
    "switchboard that no load-shed output can ever touch.", body))
story += full_image("../images/architecture_diagram.png",
    "Figure 2.1 &mdash; Simplified single-line diagram. Solid lines represent power "
    "distribution; dashed lines represent PMS controller signal paths.", max_h_mm=100)
story.append(subhead("Control hierarchy"))
story += bullets([
    "<b>Field layer</b> &mdash; generator power meters (kW), synchronising relay "
    "(frequency/voltage/phase), breaker auxiliary contacts, governor and AVR bias inputs.",
    "<b>Control layer</b> &mdash; a single PLC function block, "
    "<b>FB_PMS_PowerManagement</b>, hosted on a Siemens S7-1500 (or CODESYS-based marine "
    "PMS controller), running load monitoring, the sync state machine, and blackout recovery.",
    "<b>Supervisory / HMI layer</b> &mdash; a switchboard console giving the watch-keeping "
    "engineer a single-line diagram view, a live synchroscope, and load-vs-capacity trending.",
])
story.append(subhead("Why the PMS controller has to survive the blackout it's recovering from"))
story.append(P(
    "It's worth stating explicitly: the PLC running this logic has to be on UPS or "
    "battery-backed power, independent of the main generating plant it's managing. A "
    "controller that itself goes dead in a blackout can't run a blackout recovery sequence. "
    "This is a hardware/power-architecture requirement that sits outside the Structured Text "
    "itself, but it's a precondition for any of Chapter 6's blackout logic to mean anything.", body))
story.append(PageBreak())

# ---- Chapter 3: Hardware ----------------------------------------------------
story += chapter_head(3, "Hardware &amp; Instrumentation Specification")
story.append(P(
    "As with the other two projects in this series, this logic is platform-portable but "
    "written against a concrete reference platform so thresholds and timing are grounded.", body))
story.append(data_table(
    ["Component", "Representative Spec", "Role"],
    [
        ["PMS Controller CPU", "Siemens SIMATIC S7-1500, UPS/battery-backed supply", "Executes FB_PMS_PowerManagement"],
        ["Generator Power Meter", "CT/PT-derived, 4&ndash;20mA or digital bus, per generator", "Active power (kW) feedback"],
        ["Synchronising Relay", "Freq/volt/phase, dedicated sync relay per incoming breaker", "Live-sync supervision"],
        ["Governor Interface", "4&ndash;20mA speed bias, -100 to +100%", "Speed trim during synchronising"],
        ["AVR Interface", "4&ndash;20mA voltage bias, -100 to +100%", "Voltage trim during synchronising"],
        ["Generator Breaker", "Motorised, 24VDC close/trip, auxiliary contact feedback", "Isolation and paralleling"],
        ["Emergency Generator", "Self-contained start (battery/air), independent fuel supply", "SOLAS emergency source"],
        ["Load Contactors", "24VDC, one per load-shed stage group", "Non-essential load isolation"],
    ],
    col_widths=[42 * mm, 70 * mm, AVAIL_W - 42 * mm - 70 * mm]))
story.append(Spacer(1, 8))
story += callout(
    "Why governor/AVR bias, not a direct setpoint",
    "The synchronising logic in this project trims the incoming generator's governor and AVR "
    "with a bias signal layered on top of the generator's own local control, rather than "
    "overriding it outright. This mirrors real practice: the generator's own governor and AVR "
    "always retain their own protective limits, and the PMS is a supervisory trim on top, not "
    "a replacement for them.", "ok")
story.append(PageBreak())

# ---- Chapter 4: I/O List ----------------------------------------------------
story += chapter_head(4, "I/O List")
story.append(P(
    "The table below is the working I/O list for FB_PMS_PowerManagement (see also "
    "<b>docs/IO_List.md</b> in the repository, and Appendix A of this manual).", body))
story.append(subhead("Inputs"))
story.append(data_table(
    ["Tag", "Description", "Signal", "Range / Units"],
    [
        ["AI_Gen1_Load_kW", "Gen1 active power", "4&ndash;20mA", "0&ndash;2200 kW"],
        ["AI_Gen2_Load_kW", "Gen2 active power", "4&ndash;20mA", "0&ndash;2200 kW"],
        ["AI_Gen2_Freq_Hz", "Gen2 (incoming set) frequency", "Sync relay", "45&ndash;65 Hz"],
        ["AI_BusFreq_Hz", "Main busbar frequency", "Freq. relay", "45&ndash;65 Hz"],
        ["AI_Gen2_Voltage_V", "Gen2 terminal voltage", "Sync relay", "0&ndash;500 V"],
        ["AI_BusVoltage_V", "Main busbar voltage", "PT / volt. relay", "0&ndash;500 V"],
        ["AI_PhaseAngle_Deg", "Gen2 vs Bus phase angle", "Sync relay", "-180 to +180&deg;"],
        ["DI_Gen1_Running / DI_Gen2_Running", "Engine running feedback", "24VDC digital", "0/1"],
        ["DI_Gen1_Breaker_Closed / DI_Gen2_Breaker_Closed", "Breaker aux. contacts", "24VDC digital", "0/1"],
        ["DI_EmergencyGen_Running", "Emergency generator feedback", "24VDC digital", "0/1"],
        ["DI_ManualSyncRequest", "Operator sync request pushbutton", "24VDC digital", "0/1"],
        ["DI_System_Enable", "Master enable", "24VDC digital", "0/1"],
    ],
    col_widths=[62 * mm, 46 * mm, 28 * mm, AVAIL_W - 62 * mm - 46 * mm - 28 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Outputs"))
story.append(data_table(
    ["Tag", "Description", "Signal"],
    [
        ["DO_Gen1_Start / DO_Gen2_Start", "Generator start commands", "24VDC digital"],
        ["DO_Gen1_Breaker_Close", "Dead-bus reclose (blackout recovery only)", "24VDC digital"],
        ["DO_Gen2_Breaker_Close", "Live-sync breaker close (pulsed)", "24VDC digital"],
        ["AO_Gen2_GovernorBias_Pct / AO_Gen2_AVRBias_Pct", "Speed/voltage trim during sync", "4&ndash;20mA, &plusmn;100%"],
        ["DO_LoadShed_Stage1/2/3", "Non-essential load group trips", "24VDC digital &times;3"],
        ["DO_EmergencyGen_Start", "Emergency generator start command", "24VDC digital"],
        ["Alarm_Overload / Alarm_Blackout / Alarm_SyncTimeout", "Alarms", "24VDC digital &times;3"],
        ["PMS_State / SystemStatus", "State machine state / status text", "Internal / HMI tag"],
    ],
    col_widths=[68 * mm, 66 * mm, AVAIL_W - 68 * mm - 66 * mm]))
story.append(PageBreak())


# ---- Chapter 5: Control Philosophy -----------------------------------------
story += chapter_head(5, "Control Philosophy: Three Linked Problems")
story.append(P(
    "This project's logic makes more sense once the three problems it solves are seen as "
    "genuinely different in character, not three variations on the same theme.", body))
story.append(subhead("5.1 &nbsp; Fast load shedding: no time to calculate"))
story.append(P(
    "When Gen1 trips unexpectedly while carrying most of the plant's load, the remaining "
    "capacity drops instantly, but the load doesn't &mdash; whatever's still running is still "
    "drawing the same power. If nothing intervenes within a very short window (the "
    "manufacturer's overload trip curve, typically low single-digit seconds at high overload), "
    "the surviving generator's own protection trips it too, and the plant blacks out anyway. "
    "There's no time to compute an optimal shedding amount; the logic sheds pre-sized load "
    "blocks (Chapter 3's load contactor groups) in a fixed, predictable order, decided in "
    "advance rather than in the moment.", body))
story.append(subhead("5.2 &nbsp; Auto-synchronising: a patient, verified state machine"))
story.append(P(
    "Bringing a second generator onto a live bus is the opposite problem: there's no "
    "emergency, and rushing it is actively dangerous. Closing a breaker while the incoming "
    "generator's phase is misaligned with the bus can produce a current transient large "
    "enough to damage the generator, its prime mover, or the switchgear. The sequence in this "
    "project (Chapter 6) verifies speed, then voltage, then phase &mdash; each with its own "
    "tolerance and its own timeout &mdash; and only ever closes the breaker from the one state "
    "where every condition has just been confirmed true in that scan.", body))
story += callout(
    "The incoming generator runs deliberately fast",
    "During speed matching, the target isn't to match the bus frequency exactly &mdash; it's "
    "to run marginally faster (a small deliberate lead, implemented as the +0.05Hz bias in "
    "Chapter 6). A generator held at exactly the bus frequency has a phase angle that drifts "
    "unpredictably; one running slightly fast has a phase angle that advances steadily and "
    "predictably toward the closing window, which is what actually makes a bounded-time "
    "closing decision possible.", "ok")
story.append(subhead("5.3 &nbsp; Blackout recovery: starting from zero, not from a fault"))
story.append(P(
    "Blackout recovery isn't \"auto-sync, but urgent\" &mdash; it's a different problem "
    "because there's nothing left to synchronise against. Once every generator is confirmed "
    "down and bus voltage has genuinely collapsed, the correct action for the first generator "
    "back online is a direct <b>dead-bus close</b>: no phase matching, because there's no "
    "second live source to match against. Attempting to run the live-sync state machine "
    "against a dead bus would simply never satisfy the phase-window condition and stall "
    "recovery for no reason.", body))
story += callout(
    "Dead-bus close and live sync must never share a code path",
    "This is the single most important design decision in this project. If a generator ever "
    "closes onto a bus that turns out to still be live &mdash; because the dead-bus check was "
    "wrong, or shared logic with the live-sync path introduced a subtle bug &mdash; the result "
    "is an out-of-phase closure with no supervision at all. Section 3 of the code (Chapter 6) "
    "keeps these as two structurally separate branches specifically so a bug in one can't "
    "silently borrow the other's closing permissive.", "critical")
story.append(subhead("5.4 &nbsp; Why restoration is staged, not instant"))
story.append(P(
    "Once the main bus is back, dumping all previously-shed load back on at once risks "
    "re-tripping a generator that's only just stabilised. Load is restored in the exact "
    "reverse of the order it was shed &mdash; last shed, first back &mdash; with a timed gap "
    "between each stage, giving the generator's governor and AVR room to settle before the "
    "next block lands.", body))
story.append(PageBreak())

# ---- Chapter 6: PLC Logic Walkthrough --------------------------------------
story += chapter_head(6, "PLC Logic Walkthrough")
story.append(P(
    "This chapter walks through <b>FB_PMS_PowerManagement</b> section by section. The full, "
    "unbroken listing is reproduced in Appendix B.", body))

story.append(subhead("6.1 &nbsp; Bus and generator status"))
story.append(P(
    "Every other section depends on three derived values computed here first: how many "
    "generators are actually contributing to the bus, what the plant's total load is, and "
    "whether the bus is genuinely dead (not just low, but below a defined threshold).", body))
story += code_block(
"""RunningGenCount := 0;
IF DI_Gen1_Running AND DI_Gen1_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF
IF DI_Gen2_Running AND DI_Gen2_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF

AvailableCapacity_kW := INT_TO_REAL(RunningGenCount) * Gen_Rated_kW;
BusIsDead              := AI_BusVoltage_V < DeadBus_Threshold_V;
BlackoutDetected        := DI_System_Enable AND BusIsDead
                            AND (NOT DI_Gen1_Running) AND (NOT DI_Gen2_Running);""",
    "Listing 6.1 &mdash; Bus and generator status, computed once per scan.")

story.append(subhead("6.2 &nbsp; Fast load shedding"))
story.append(P(
    "An edge-detected trip, or simply exceeding the overload margin, sheds stages "
    "immediately &mdash; note there's no PID, no ramp, just direct comparisons against "
    "pre-sized blocks. This section is explicitly skipped while a blackout recovery is in "
    "progress, so it can't fight with the forced-shed state Section 6.3 sets.", body))
story += code_block(
"""Gen1_TripEdge     := Gen1_Was_Running AND (NOT DI_Gen1_Breaker_Closed) AND (NOT BlackoutDetected);
Gen1_Was_Running  := DI_Gen1_Breaker_Closed;

IF Gen1_TripEdge OR (TotalLoad_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0)) THEN
    DO_LoadShed_Stage1 := TRUE;
    IF TotalLoad_kW - LoadShed_Stage1_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
        DO_LoadShed_Stage2 := TRUE;
    END_IF
    IF TotalLoad_kW - LoadShed_Stage1_kW - LoadShed_Stage2_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
        DO_LoadShed_Stage3 := TRUE;
    END_IF
    Alarm_Overload := TRUE;
ELSIF TotalLoad_kW < AvailableCapacity_kW * 0.6 THEN
    DO_LoadShed_Stage1 := FALSE; DO_LoadShed_Stage2 := FALSE; DO_LoadShed_Stage3 := FALSE;
    Alarm_Overload      := FALSE;
END_IF""", "Listing 6.2 &mdash; Fast, block-based load shedding.")

story.append(subhead("6.3 &nbsp; Blackout pre-empts everything else"))
story.append(P(
    "This is a short section doing something structurally important: it forces every "
    "sheddable load OFF the instant a blackout is confirmed, before power even returns, so "
    "nothing re-energises in an uncontrolled rush the moment the bus comes back.", body))
story += code_block(
"""IF BlackoutDetected AND (PMS_State <> ST_BLACKOUT_EMERGENCY)
   AND (PMS_State <> ST_BLACKOUT_BLACKSTART) AND (PMS_State <> ST_BLACKOUT_RESTORE) THEN
    PMS_State           := ST_BLACKOUT_EMERGENCY;
    DO_LoadShed_Stage1  := TRUE;
    DO_LoadShed_Stage2  := TRUE;
    DO_LoadShed_Stage3  := TRUE;
    DO_Gen2_Start        := FALSE;
    RestoreStageIndex     := 0;
END_IF""", "Listing 6.3 &mdash; Blackout detection forces a safe, fully-shed starting point.")

story.append(subhead("6.4 &nbsp; The live-sync state machine (condensed)"))
story.append(P(
    "The full sequence runs through eight states; the two decision points worth seeing "
    "directly are the phase-window check and the breaker-close confirmation, since those are "
    "where a synchronising sequence actually earns its trust.", body))
story += code_block(
"""ST_PHASE_MATCH:
    T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
    // ... governor bias kept live here (Listing continues in Appendix B) ...
    IF (AI_PhaseAngle_Deg <= 0.0) AND (AI_PhaseAngle_Deg > -PhaseClose_Window_Deg) THEN
        PMS_State := ST_CLOSE_BREAKER;
        T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
    END_IF
    IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

ST_CLOSE_BREAKER:
    DO_Gen2_Breaker_Close := TRUE;
    T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
    IF DI_Gen2_Breaker_Closed THEN
        DO_Gen2_Breaker_Close := FALSE;
        PMS_State := ST_RUNNING_PARALLEL;
    ELSIF T_BreakerConfirm.Q THEN
        DO_Gen2_Breaker_Close := FALSE;
        PMS_State := ST_SYNC_FAILED;
    END_IF""", "Listing 6.4 &mdash; The phase-window check and breaker-close confirmation.")
story += callout(
    "Every path through this state machine ends in a verified state",
    "Look at the two exits from ST_CLOSE_BREAKER: the breaker only ever registers as "
    "successfully closed via confirmed feedback (<code>DI_Gen2_Breaker_Closed</code>), never "
    "by assuming the close command worked. If confirmation doesn't arrive before "
    "<code>T_BreakerConfirm_PT</code> elapses, the sequence fails safe rather than proceeding "
    "on faith.", "ok")

story.append(subhead("6.5 &nbsp; Blackout black-start: the dead-bus path"))
story.append(P(
    "Compare this directly against Listing 6.4. There is no frequency check, no voltage "
    "check, no phase check &mdash; because <code>BusIsDead</code> was already confirmed in "
    "Section 6.1, closing directly is the correct action, not a shortcut.", body))
story += code_block(
"""ST_BLACKOUT_BLACKSTART:
    DO_Gen1_Start := TRUE;
    T_Warmup(IN := TRUE, PT := T_Warmup_PT);
    IF DI_Gen1_Running AND T_Warmup.Q AND BusIsDead THEN
        DO_Gen1_Breaker_Close := TRUE;   // Dead-bus close - no sync check needed,
    END_IF                                // the bus is confirmed dead, not live.
    IF DI_Gen1_Breaker_Closed THEN
        DO_Gen1_Breaker_Close := FALSE;
        PMS_State := ST_BLACKOUT_RESTORE;
    END_IF""", "Listing 6.5 &mdash; Dead-bus close: structurally separate from live synchronising.")
story.append(PageBreak())


# ---- Chapter 7: HMI ---------------------------------------------------------
story += chapter_head(7, "HMI Design &amp; the Live Synchroscope")
story.append(P(
    "The HMI mockup (<b>hmi/index.html</b> in the repository) centres on a single-line "
    "diagram &mdash; the standard way electrical engineers read a switchboard at a glance "
    "&mdash; paired with a live synchroscope, the classic rotating-needle dial real "
    "synchronising panels have used for decades. It runs a full scripted demo on a loop: "
    "rising load, auto-sync, parallel running, a full blackout, emergency generator start, "
    "black-start, and staged restoration.", body))
story += full_image("../images/hmi-dashboard.png",
    "Figure 7.1 &mdash; Switchboard console mid-synchronising: Gen2 breaker still open on "
    "the single-line diagram, synchroscope needle approaching the 12 o'clock closing "
    "position, governor/AVR bias bars active.", max_h_mm=115)
story.append(subhead("Design decisions"))
story += bullets([
    "<b>The single-line diagram is the primary view, not a supporting chart</b> &mdash; "
    "breaker colour (green closed, red/grey open), generator circle colour, and bus-line "
    "colour all update live, exactly what a real switchboard mimic panel shows.",
    "<b>The synchroscope is a real instrument, not decoration</b> &mdash; its needle "
    "position is driven directly by the same phase-angle value the PLC's "
    "<code>AI_PhaseAngle_Deg</code> input represents, rotating toward the 12 o'clock "
    "position as the sequence approaches the closing window.",
    "<b>Blue/amber switchboard palette</b> &mdash; a third distinct identity in the "
    "portfolio series (after Project 01's teal compliance theme and Project 02's red safety "
    "theme), chosen because blue-dominant panels are how electrical distribution equipment "
    "is conventionally rendered, distinct from a process or safety console.",
    "<b>Flexbox over CSS Grid</b> &mdash; the three-column detail panel below the SLD was "
    "originally built with CSS Grid, which turned out to silently fail to lay out columns "
    "at all on an older rendering engine used during screenshot generation. Rebuilt in "
    "flexbox, which behaved correctly everywhere it was tested.",
])
story += callout(
    "A second compatibility bug, a second real lesson",
    "This is the second rendering-engine compatibility issue found across the portfolio "
    "series (the first was Project 01's CSS conic-gradient/ES6 failure). The pattern is "
    "consistent: features that are perfectly standard in a modern desktop browser "
    "(<code>conic-gradient</code>, template literals, CSS Grid) are not universally "
    "supported by the older embedded browser engines that panel PCs and screenshot/report "
    "tooling often still run. Treating that as a real defect class, not an edge case, is "
    "itself part of what this portfolio is meant to demonstrate.", "ok")
story.append(PageBreak())

# ---- Chapter 8: Alarm Philosophy -------------------------------------------
story += chapter_head(8, "Alarm Philosophy &amp; Fail-Safe Design")
story.append(P(
    "As with the other two projects, every alarm here maps to a specific expected operator "
    "response rather than a generic warning light.", body))
story.append(data_table(
    ["Condition", "Meaning", "Expected Operator Response"],
    [
        ["Alarm_Overload", "Load shed stage(s) active", "Confirm shed loads are non-essential; investigate cause of high load"],
        ["Alarm_Blackout", "Blackout recovery in progress", "Monitor recovery sequence; do not manually intervene unless it stalls"],
        ["Alarm_SyncTimeout", "Auto-sync sequence failed to complete", "Investigate generator/governor/AVR fault before re-requesting sync"],
    ],
    col_widths=[38 * mm, 56 * mm, AVAIL_W - 38 * mm - 56 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Fail-safe defaults, summarised"))
story += bullets([
    "Any generator trip while carrying significant load &rarr; load sheds within one scan, "
    "no waiting for confirmation of cause.",
    "Any sync stage timeout &rarr; sequence aborts to SYNC_FAILED; breaker is never closed "
    "on an unverified condition.",
    "Blackout confirmed &rarr; every sheddable load forced off before any recovery action "
    "begins.",
    "Sync retry requires the operator to drop and re-raise the request &mdash; no silent, "
    "unattended retry loop against a fault that hasn't been investigated.",
])
story.append(PageBreak())

# ---- Chapter 9: Testing -----------------------------------------------------
story += chapter_head(9, "Testing, Commissioning &amp; FAT Procedures")
story.append(P(
    "The function block was validated against twelve functional test cases spanning normal "
    "operation, the full auto-sync sequence (including two deliberate failure paths), and "
    "the complete blackout-to-recovery chain. The full procedure is in "
    "<b>docs/Testing_Procedures.md</b>; the matrix is reproduced below.", body))
story.append(data_table(
    ["#", "Test Case", "Expected Result"],
    [
        ["1", "Normal single-generator operation", "Status NORMAL; no shed stages active"],
        ["2", "Fast load shed on unexpected trip", "Stages shed within one scan; Alarm_Overload raised"],
        ["3", "Load-dependent auto-start", "Gen2 start command energises above 85% single-gen load"],
        ["4", "Full auto-sync sequence", "Reaches RUNNING_PARALLEL; breaker confirmed closed"],
        ["5", "Sync timeout - frequency never matches", "SYNC_FAILED; breaker never commanded closed"],
        ["6", "Sync retry requires a fresh request", "No silent auto-retry after a failure"],
        ["7", "Breaker close confirmation failure", "SYNC_FAILED; close command drops"],
        ["8", "Full blackout detection", "BLACKOUT_EMERGENCY within one scan"],
        ["9", "Emergency generator auto-start", "Start command energises; all shed stages forced TRUE"],
        ["10", "Black-start dead-bus close", "Direct close &mdash; no synchronising states entered"],
        ["11", "Staged load restoration", "Reverse-order restore, each stage timer-gated"],
        ["12", "Blackout recovery completes to normal", "Returns to IDLE; Alarm_Blackout clears"],
    ],
    col_widths=[10 * mm, 68 * mm, AVAIL_W - 10 * mm - 68 * mm]))
story.append(Spacer(1, 10))
story += callout(
    "Tests 5&ndash;7 matter as much as Test 4",
    "A synchroniser that completes a clean sync (Test 4) but can't fail safely is worse than "
    "no automation at all. Tests 5 through 7 exist specifically to prove the sequence aborts "
    "cleanly under a frequency fault, a stalled attempt, and a breaker that fails to confirm "
    "&mdash; and that in every one of those cases, the breaker-close command is never left "
    "asserted against an unverified condition.", "warning")
story.append(subhead("9.1 &nbsp; Commissioning sequence (SAT-style, for reference)"))
story.append(data_table(
    ["Step", "Activity", "Exit Criteria"],
    [
        ["1", "Cold loop checks", "Every I/O point traced; breaker aux. contacts verified against actual position"],
        ["2", "Governor/AVR bias calibration", "Bias signal range matched to the actual generator's droop characteristic"],
        ["3", "Load shed contactor test", "Each stage group trips and restores correctly, independent of the others"],
        ["4", "Live sync proving (no load)", "Full sequence run and breaker closed with both gensets lightly loaded"],
        ["5", "Fast shed proving", "Duty generator deliberately tripped under real load; shed timing measured against the class overload trip curve"],
        ["6", "Blackout drill", "Full plant blackout simulated; emergency gen, black-start, and restoration timed end-to-end"],
        ["7", "Sign-off", "Class surveyor and shipowner's engineer countersign the FAT/SAT record"],
    ],
    col_widths=[14 * mm, 56 * mm, AVAIL_W - 14 * mm - 56 * mm]))
story.append(PageBreak())

# ---- Chapter 10: Limitations -------------------------------------------------
story += chapter_head(10, "Limitations, Real-World Deltas &amp; Future Work")
story.append(P(
    "Naming the gap between a strong simulation and a certifiable Power Management System "
    "is part of the engineering, consistent with the other two projects in this series.", body))
story.append(subhead("What a real installation would add"))
story += bullets([
    "<b>Load sharing (droop) control</b> &mdash; once generators are in parallel, this "
    "function block hands off governor/AVR control entirely; a real PMS actively balances "
    "kW and kVAR sharing between running generators on an ongoing basis.",
    "<b>Reverse-power and other protection coordination</b> &mdash; a real system "
    "coordinates this logic with generator protection relays (reverse power, overcurrent, "
    "loss of excitation) rather than treating them as independent.",
    "<b>Auto-stop / de-load sequencing</b> &mdash; stopping Gen2 once it's no longer needed "
    "is explicitly left as an operator decision in this design (Chapter 6.4) rather than "
    "modelled.",
    "<b>Class society approval</b> &mdash; DNV, ABS, or Lloyd's Register review against their "
    "specific PMS notation requirements, including a documented FMEA.",
])
story.append(subhead("10.1 &nbsp; Hazard &amp; safeguard register (HAZOP-style)"))
story.append(data_table(
    ["Hazard", "Cause", "Safeguard in This Design"],
    [
        ["Out-of-phase breaker closure", "Sync logic closes before phase genuinely aligned",
         "Phase window checked in the same scan as closure; dead-bus and live-sync paths structurally separate"],
        ["Cascading blackout from single trip", "Load shed too slow or wrong amount",
         "Pre-sized blocks, no iterative calculation, edge-triggered within one scan"],
        ["Uncontrolled load rush on recovery", "All load restored simultaneously after blackout",
         "Reverse-order, timer-gated staged restoration (Chapter 5.4)"],
        ["Silent, repeated failed sync attempts", "Automatic retry against an unresolved fault",
         "Retry requires the operator to drop and re-raise the request"],
    ],
    col_widths=[46 * mm, 48 * mm, AVAIL_W - 46 * mm - 48 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("Where this project could go next"))
story += bullets([
    "Add basic kW droop-based load sharing once both generators are confirmed parallel.",
    "Model a third generator to demonstrate the state machine scaling beyond a two-set plant.",
    "Add a data-logged timing report per blackout event, comparing actual recovery time "
    "against the SOLAS 45-second and class-society expectations documented in Chapter 1.",
])
story.append(PageBreak())


# ---- Appendix A: I/O Quick Reference ---------------------------------------
story += chapter_head("A", "Appendix A &mdash; I/O Quick Reference", "APPENDIX")
story.append(data_table(
    ["Tag", "Dir.", "Type", "Notes"],
    [
        ["AI_Gen1_Load_kW / AI_Gen2_Load_kW", "IN", "REAL x2", "0-2200 kW"],
        ["AI_Gen2_Freq_Hz / AI_BusFreq_Hz", "IN", "REAL x2", "Tolerance 0.10 Hz"],
        ["AI_Gen2_Voltage_V / AI_BusVoltage_V", "IN", "REAL x2", "Tolerance 2.0%"],
        ["AI_PhaseAngle_Deg", "IN", "REAL", "Close window -8 to 0 deg"],
        ["DI_Gen1/2_Running", "IN", "BOOL x2", "Engine feedback"],
        ["DI_Gen1/2_Breaker_Closed", "IN", "BOOL x2", "Aux. contact"],
        ["DI_EmergencyGen_Running", "IN", "BOOL", "SOLAS emergency source"],
        ["DI_ManualSyncRequest", "IN", "BOOL", "Must re-raise after a failure"],
        ["DI_System_Enable", "IN", "BOOL", "Master enable"],
        ["DO_Gen1_Start / DO_Gen2_Start", "OUT", "BOOL x2", "Start commands"],
        ["DO_Gen1_Breaker_Close", "OUT", "BOOL", "Dead-bus only"],
        ["DO_Gen2_Breaker_Close", "OUT", "BOOL", "Live-sync only, pulsed"],
        ["AO_Gen2_GovernorBias_Pct / AVRBias_Pct", "OUT", "REAL x2", "-100..100%"],
        ["DO_LoadShed_Stage1/2/3", "OUT", "BOOL x3", "Reverse-order restore"],
        ["DO_EmergencyGen_Start", "OUT", "BOOL", "SOLAS 45s target"],
        ["PMS_State", "OUT", "ENUM", "12-state machine"],
    ],
    col_widths=[64 * mm, 14 * mm, 22 * mm, AVAIL_W - 64 * mm - 14 * mm - 22 * mm]))
story.append(PageBreak())

# ---- Appendix B: Full ST Listing -------------------------------------------
story += chapter_head("B", "Appendix B &mdash; Full Structured Text Listing", "APPENDIX")
story.append(P("Complete, unedited listing of <b>src/PMS_PowerManagement.st</b>.", body))

story += code_block(
"""(*
====================================================================================
  PROJECT   : Autonomous Marine Power Management System (PMS)
              Intelligent Load-Shedding & Blackout Recovery
  MODULE    : FB_PMS_PowerManagement
  PLATFORM  : IEC 61131-3 Structured Text (Siemens SCL / CODESYS-portable)
  AUTHOR    : Sipho Lucky Sibanda
  REGULATORY BASIS (simulated against, for realism only):
    - SOLAS Ch. II-1, Reg 42/43 - Emergency source, 45-second start
    - IEC 61892-1 / IEC 60092  - Electrical installations on ships
====================================================================================
*)

TYPE E_PMS_State :
(
    ST_IDLE, ST_STARTING, ST_WARMUP, ST_SPEED_MATCH, ST_VOLTAGE_MATCH,
    ST_PHASE_MATCH, ST_CLOSE_BREAKER, ST_RUNNING_PARALLEL, ST_SYNC_FAILED,
    ST_BLACKOUT_EMERGENCY, ST_BLACKOUT_BLACKSTART, ST_BLACKOUT_RESTORE
);
END_TYPE

FUNCTION_BLOCK FB_PMS_PowerManagement
VAR_INPUT
    AI_Gen1_Load_kW : REAL;          AI_Gen2_Load_kW : REAL;
    AI_Gen2_Freq_Hz : REAL;           AI_BusFreq_Hz : REAL;
    AI_Gen2_Voltage_V : REAL;          AI_BusVoltage_V : REAL;
    AI_PhaseAngle_Deg : REAL;
    DI_Gen1_Running : BOOL;             DI_Gen2_Running : BOOL;
    DI_Gen1_Breaker_Closed : BOOL;       DI_Gen2_Breaker_Closed : BOOL;
    DI_EmergencyGen_Running : BOOL;
    DI_ManualSyncRequest : BOOL;
    DI_System_Enable : BOOL;
END_VAR""")

story += code_block(
"""VAR_OUTPUT
    DO_Gen1_Start : BOOL := FALSE;              DO_Gen2_Start : BOOL := FALSE;
    DO_Gen1_Breaker_Close : BOOL := FALSE;        DO_Gen2_Breaker_Close : BOOL := FALSE;
    AO_Gen2_GovernorBias_Pct : REAL := 0.0;        AO_Gen2_AVRBias_Pct : REAL := 0.0;
    DO_LoadShed_Stage1 : BOOL := FALSE;
    DO_LoadShed_Stage2 : BOOL := FALSE;
    DO_LoadShed_Stage3 : BOOL := FALSE;
    DO_EmergencyGen_Start : BOOL := FALSE;
    Alarm_Overload : BOOL := FALSE;
    Alarm_Blackout : BOOL := FALSE;
    Alarm_SyncTimeout : BOOL := FALSE;
    PMS_State : E_PMS_State := ST_IDLE;
    SystemStatus : STRING[24] := 'STANDBY';
END_VAR

VAR
    Gen_Rated_kW : REAL := 2000.0;
    LoadShed_Stage1_kW : REAL := 150.0;  LoadShed_Stage2_kW : REAL := 300.0;
    LoadShed_Stage3_kW : REAL := 200.0;
    Overload_Margin_Pct : REAL := 90.0;
    Freq_Tolerance_Hz : REAL := 0.10;     Volt_Tolerance_Pct : REAL := 2.0;
    PhaseClose_Window_Deg : REAL := 8.0;   DeadBus_Threshold_V : REAL := 50.0;

    RunningGenCount : INT;    TotalLoad_kW : REAL;    AvailableCapacity_kW : REAL;
    BusIsDead : BOOL;          BlackoutDetected : BOOL;
    TempBias : REAL;            VoltErrPct : REAL;
    Gen1_Was_Running : BOOL;     Gen1_TripEdge : BOOL;

    T_Start : TON;  T_Start_PT : TIME := T#20S;
    T_Warmup : TON;  T_Warmup_PT : TIME := T#30S;
    T_SyncWindow : TON;  T_SyncWindow_PT : TIME := T#60S;
    T_BreakerConfirm : TON;  T_BreakerConfirm_PT : TIME := T#500MS;
    T_RestoreStage : TON;  T_RestoreStage_PT : TIME := T#15S;
    RestoreStageIndex : INT := 0;
END_VAR""")

story += code_block(
"""// 1. BUS & GENERATOR STATUS
RunningGenCount := 0;
IF DI_Gen1_Running AND DI_Gen1_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF
IF DI_Gen2_Running AND DI_Gen2_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF

TotalLoad_kW := 0.0;
IF DI_Gen1_Breaker_Closed THEN TotalLoad_kW := TotalLoad_kW + AI_Gen1_Load_kW; END_IF
IF DI_Gen2_Breaker_Closed THEN TotalLoad_kW := TotalLoad_kW + AI_Gen2_Load_kW; END_IF

AvailableCapacity_kW := INT_TO_REAL(RunningGenCount) * Gen_Rated_kW;
BusIsDead              := AI_BusVoltage_V < DeadBus_Threshold_V;
BlackoutDetected        := DI_System_Enable AND BusIsDead
                            AND (NOT DI_Gen1_Running) AND (NOT DI_Gen2_Running);

// 2. FAST LOAD SHEDDING
Gen1_TripEdge     := Gen1_Was_Running AND (NOT DI_Gen1_Breaker_Closed) AND (NOT BlackoutDetected);
Gen1_Was_Running  := DI_Gen1_Breaker_Closed;

IF (PMS_State <> ST_BLACKOUT_EMERGENCY) AND (PMS_State <> ST_BLACKOUT_BLACKSTART)
   AND (PMS_State <> ST_BLACKOUT_RESTORE) THEN
    IF Gen1_TripEdge OR (TotalLoad_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0)) THEN
        DO_LoadShed_Stage1 := TRUE;
        IF TotalLoad_kW - LoadShed_Stage1_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
            DO_LoadShed_Stage2 := TRUE;
        END_IF
        IF TotalLoad_kW - LoadShed_Stage1_kW - LoadShed_Stage2_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
            DO_LoadShed_Stage3 := TRUE;
        END_IF
        Alarm_Overload := TRUE;
    ELSIF TotalLoad_kW < AvailableCapacity_kW * 0.6 THEN
        DO_LoadShed_Stage1 := FALSE; DO_LoadShed_Stage2 := FALSE; DO_LoadShed_Stage3 := FALSE;
        Alarm_Overload      := FALSE;
    END_IF
END_IF""")

story += code_block(
"""// 3. BLACKOUT PRE-EMPTS EVERYTHING ELSE
IF BlackoutDetected AND (PMS_State <> ST_BLACKOUT_EMERGENCY)
   AND (PMS_State <> ST_BLACKOUT_BLACKSTART) AND (PMS_State <> ST_BLACKOUT_RESTORE) THEN
    PMS_State           := ST_BLACKOUT_EMERGENCY;
    DO_LoadShed_Stage1  := TRUE;  DO_LoadShed_Stage2 := TRUE;  DO_LoadShed_Stage3 := TRUE;
    DO_Gen2_Start        := FALSE;
    RestoreStageIndex     := 0;
END_IF

// 4. LOAD-DEPENDENT AUTO-START TRIGGER
IF DI_System_Enable AND (NOT BlackoutDetected) AND (PMS_State = ST_IDLE)
   AND ((TotalLoad_kW > Gen_Rated_kW * 0.85) OR DI_ManualSyncRequest)
   AND (NOT DI_Gen2_Breaker_Closed) THEN
    PMS_State := ST_STARTING;
END_IF

// 5. AUTO-SYNCHRONISING STATE MACHINE (Gen2 onto a LIVE bus)
CASE PMS_State OF
    ST_STARTING:
        DO_Gen2_Start := TRUE;
        T_Start(IN := TRUE, PT := T_Start_PT);
        IF DI_Gen2_Running THEN
            T_Start(IN := FALSE); T_Warmup(IN := TRUE, PT := T_Warmup_PT);
            PMS_State := ST_WARMUP;
        ELSIF T_Start.Q THEN
            PMS_State := ST_SYNC_FAILED;
        END_IF

    ST_WARMUP:
        T_Warmup(IN := TRUE, PT := T_Warmup_PT);
        IF T_Warmup.Q THEN
            T_Warmup(IN := FALSE); T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
            PMS_State := ST_SPEED_MATCH;
        END_IF""")

story += code_block(
"""    ST_SPEED_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        TempBias := (AI_BusFreq_Hz + 0.05 - AI_Gen2_Freq_Hz) * 50.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_GovernorBias_Pct := TempBias;
        IF ABS(AI_BusFreq_Hz - AI_Gen2_Freq_Hz) <= Freq_Tolerance_Hz THEN
            PMS_State := ST_VOLTAGE_MATCH;
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_VOLTAGE_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        VoltErrPct := ((AI_BusVoltage_V - AI_Gen2_Voltage_V) / AI_BusVoltage_V) * 100.0;
        TempBias    := VoltErrPct * 20.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_AVRBias_Pct := TempBias;
        IF ABS(VoltErrPct) <= Volt_Tolerance_Pct THEN
            PMS_State := ST_PHASE_MATCH;
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_PHASE_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        TempBias := (AI_BusFreq_Hz + 0.05 - AI_Gen2_Freq_Hz) * 50.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_GovernorBias_Pct := TempBias;
        IF (AI_PhaseAngle_Deg <= 0.0) AND (AI_PhaseAngle_Deg > -PhaseClose_Window_Deg) THEN
            PMS_State := ST_CLOSE_BREAKER;
            T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_CLOSE_BREAKER:
        DO_Gen2_Breaker_Close := TRUE;
        T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
        IF DI_Gen2_Breaker_Closed THEN
            DO_Gen2_Breaker_Close := FALSE; T_BreakerConfirm(IN := FALSE); T_SyncWindow(IN := FALSE);
            AO_Gen2_GovernorBias_Pct := 0.0; AO_Gen2_AVRBias_Pct := 0.0;
            PMS_State := ST_RUNNING_PARALLEL;
        ELSIF T_BreakerConfirm.Q THEN
            DO_Gen2_Breaker_Close := FALSE; PMS_State := ST_SYNC_FAILED;
        END_IF

    ST_RUNNING_PARALLEL:
        IF NOT DI_Gen2_Breaker_Closed THEN PMS_State := ST_IDLE; END_IF

    ST_SYNC_FAILED:
        DO_Gen2_Start := FALSE; Alarm_SyncTimeout := TRUE;
        AO_Gen2_GovernorBias_Pct := 0.0; AO_Gen2_AVRBias_Pct := 0.0;
        IF NOT DI_ManualSyncRequest THEN
            Alarm_SyncTimeout := FALSE; PMS_State := ST_IDLE;
        END_IF""")

story += code_block(
"""    ST_BLACKOUT_EMERGENCY:
        DO_EmergencyGen_Start := TRUE;
        Alarm_Blackout          := TRUE;
        IF DI_EmergencyGen_Running THEN
            T_Warmup(IN := TRUE, PT := T_Warmup_PT);
            PMS_State := ST_BLACKOUT_BLACKSTART;
        END_IF

    ST_BLACKOUT_BLACKSTART:
        DO_Gen1_Start := TRUE;
        T_Warmup(IN := TRUE, PT := T_Warmup_PT);
        IF DI_Gen1_Running AND T_Warmup.Q AND BusIsDead THEN
            DO_Gen1_Breaker_Close := TRUE;
        END_IF
        IF DI_Gen1_Breaker_Closed THEN
            DO_Gen1_Breaker_Close := FALSE; T_Warmup(IN := FALSE);
            T_RestoreStage(IN := TRUE, PT := T_RestoreStage_PT);
            PMS_State := ST_BLACKOUT_RESTORE;
        END_IF

    ST_BLACKOUT_RESTORE:
        T_RestoreStage(IN := TRUE, PT := T_RestoreStage_PT);
        CASE RestoreStageIndex OF
            0: IF T_RestoreStage.Q THEN
                   DO_LoadShed_Stage3 := FALSE; T_RestoreStage(IN := FALSE); RestoreStageIndex := 1;
               END_IF
            1: IF T_RestoreStage.Q THEN
                   DO_LoadShed_Stage2 := FALSE; T_RestoreStage(IN := FALSE); RestoreStageIndex := 2;
               END_IF
            2: IF T_RestoreStage.Q THEN
                   DO_LoadShed_Stage1 := FALSE; T_RestoreStage(IN := FALSE); RestoreStageIndex := 3;
               END_IF
            3: Alarm_Blackout := FALSE; RestoreStageIndex := 0; PMS_State := ST_IDLE;
        END_CASE

    ELSE
        ; // ST_IDLE
END_CASE

// 6. STATUS TEXT
IF NOT DI_System_Enable THEN SystemStatus := 'STANDBY';
ELSIF BlackoutDetected OR (PMS_State = ST_BLACKOUT_EMERGENCY)
      OR (PMS_State = ST_BLACKOUT_BLACKSTART) OR (PMS_State = ST_BLACKOUT_RESTORE) THEN
    SystemStatus := 'BLACKOUT RECOVERY';
ELSIF PMS_State = ST_RUNNING_PARALLEL THEN SystemStatus := 'GENS PARALLEL';
ELSIF PMS_State = ST_SYNC_FAILED THEN SystemStatus := 'SYNC FAILED';
ELSIF (PMS_State <> ST_IDLE) THEN SystemStatus := 'SYNCHRONISING';
ELSIF Alarm_Overload THEN SystemStatus := 'LOAD SHED ACTIVE';
ELSE SystemStatus := 'NORMAL - GEN1 DUTY';
END_IF

END_FUNCTION_BLOCK""", "Listing B.1 &mdash; Complete FB_PMS_PowerManagement source.")
story.append(PageBreak())

# ---- Appendix C: Glossary --------------------------------------------------
story += chapter_head("C", "Appendix C &mdash; Glossary", "APPENDIX")
story.append(data_table(
    ["Term", "Meaning"],
    [
        ["PMS", "Power Management System &mdash; supervises generators, load sharing, and shutdown/start sequencing"],
        ["SOLAS", "Safety of Life at Sea &mdash; the IMO convention setting the 45-second emergency power requirement"],
        ["Blackout", "Total loss of electrical power across the main switchboard"],
        ["Black start", "Starting and energising a generator/bus with no external power source available"],
        ["Dead-bus close", "Closing a breaker onto a confirmed de-energised bus &mdash; no synchronising required"],
        ["Synchronising", "Matching an incoming generator's speed, voltage, and phase to a live bus before closing its breaker"],
        ["Synchroscope", "An instrument (physical or, here, simulated) showing phase alignment between two AC sources"],
        ["Droop", "A governor/AVR control method that shares load proportionally between parallel generators"],
        ["Load shedding", "Automatically disconnecting non-essential loads to protect remaining generation capacity"],
        ["AVR", "Automatic Voltage Regulator &mdash; controls a generator's terminal voltage"],
        ["Governor", "Controls a generator's prime mover speed, and therefore frequency"],
        ["HAZOP", "Hazard and Operability study &mdash; a structured method for identifying process risks"],
    ],
    col_widths=[34 * mm, AVAIL_W - 34 * mm]))
story.append(PageBreak())

# ---- About the Author -------------------------------------------------------
story += chapter_head("&mdash;", "About the Author", "CLOSING")
story.append(P(
    "<b>Sipho Lucky Sibanda</b> is an automation and controls engineer building a "
    "multi-disciplinary portfolio spanning marine systems, industrial automation, biotech, "
    "and applied AI/PLC integration. This manual is the third in the "
    "<b>Marine Automation Portfolio</b> series, following the same documentation standard "
    "as Projects 01 and 02: full PLC logic, I/O documentation, a live HMI, functional test "
    "procedures, and an honest account of what separates a strong simulation from a "
    "certifiable production system.", lead))
story.append(P("Repository: <b>marine-pms-loadshare</b>", body))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=1, color=BLUEACC))
story.append(Spacer(1, 6))
story.append(P("End of document.", caption))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUTFILE, pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOT,
    title="Autonomous Marine Power Management System (PMS) - Technical Manual",
    author=AUTHOR,
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_body)
print("Built:", OUTFILE)
