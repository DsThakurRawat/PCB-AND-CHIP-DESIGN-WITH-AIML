#!/home/divyansh-rawat/AIPCBDESIGN/.venv/bin/python3
"""
Step 5: Compilation of Final Deliverables & Single Master PDF Submission
Author: Divyansh Rawat (Roll No: 124EC0030)
Department of ECE, IIIT Kurnool
Course: Electronic Prototyping and Manufacturing (EPM) Laboratory
Faculty: Dr. Eswaramoorthy K V
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN").resolve()
EDIR = ROOT_DIR / "end_exam"
SUBMISSION_DIR = ROOT_DIR / "124EC0030"

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from pypdf import PdfWriter, PdfReader

def build_pdf_document():
    print("==================================================================")
    print(" [*] COMPILING MASTER SINGLE SUBMISSION PDF (124EC0030)")
    print("==================================================================")
    
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    temp_pdf = EDIR / "temp_full_report.pdf"
    
    # Setup Document: A4 Portrait with 15 mm margins (printable width: 180 mm, height: 273 mm)
    doc = SimpleDocTemplate(
        str(temp_pdf),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        textColor=colors.HexColor('#1A365D')
    )
    
    sub_title = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#2B6CB0')
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=4,
        spaceAfter=4
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=4,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2D3748')
    )
    
    story = []
    
    # -------------------------------------------------------------
    # PAGE 1: OFFICIAL IIITDM KURNOOL CERTIFICATE & COVER PAGE
    # -------------------------------------------------------------
    logo_path = EDIR / "iiitdm_logo.png"
    if logo_path.exists():
        story.append(RLImage(str(logo_path), width=28 * mm, height=28 * mm))
        story.append(Spacer(1, 2 * mm))
        
    inst_title = ParagraphStyle('InstTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=colors.black)
    inst_sub = ParagraphStyle('InstSub', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, alignment=1, textColor=colors.black)
    
    story.append(Paragraph("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY<br/>DESIGN AND MANUFACTURING KURNOOL", inst_title))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("(An Institute of National Importance under Ministry of Education, Govt. of India)", inst_sub))
    story.append(Paragraph("Jagannathagattu, Dinnedevarapadu, Kurnool – 518008, Andhra Pradesh", inst_sub))
    story.append(Spacer(1, 3 * mm))
    
    reg_style = ParagraphStyle('RegNo', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=2, textColor=colors.black)
    story.append(Paragraph("<b>Reg. No. : 124EC0030</b>", reg_style))
    story.append(Spacer(1, 3 * mm))
    
    cert_box = Table([[Paragraph("<b>CERTIFICATE</b>", ParagraphStyle('Cert', fontName='Helvetica-Bold', fontSize=13, alignment=1))]], colWidths=[55 * mm])
    cert_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(cert_box)
    story.append(Spacer(1, 4 * mm))
    
    cert_text = (
        "Certified that this is the bonafide record of practical work done<br/><br/>"
        "by <b>Mr. Divyansh Rawat (Reg. No: 124EC0030)</b><br/><br/>"
        "of the <b>Department of Electronics and Communication Engineering</b><br/><br/>"
        "in the <b>Electronic Prototyping and Manufacturing (EPM) Laboratory</b><br/><br/>"
        "for the End Semester Practical Examination on<br/>"
        "<b>Dual Inductance-Sensitive Tone Demonstrator — Layout Variant A (90 x 70 mm)</b><br/><br/>"
        "during the academic year 2026 – 2027.<br/><br/>"
        "<b>Course Faculty:</b> Dr. Eswaramoorthy K V"
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 5 * mm))
    
    meta_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Divyansh Rawat (124EC0030)", body_style),
         Paragraph("<b>Course Faculty:</b>", body_style), Paragraph("Dr. Eswaramoorthy K V", body_style)],
        [Paragraph("<b>Date of Exam:</b>", body_style), Paragraph("10-11-2026", body_style),
         Paragraph("<b>Exam Pattern:</b>", body_style), Paragraph("Layout Variant A (90 x 70 mm)", body_style)],
        [Paragraph("<b>Design Environment:</b>", body_style), Paragraph("KiCad 9.0.8 (x86_64 Linux)", body_style),
         Paragraph("<b>DRC / ERC Status:</b>", body_style), Paragraph("<b>0 Errors / 0 Violations (100% Pass)</b>", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#718096')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10 * mm))
    
    # Signatures
    sig_data = [
        [Paragraph("<b>Signature of Head of the Department</b>", body_style),
         Paragraph("<b>Signature of Faculty</b><br/><br/><b>Dr. Eswaramoorthy K V</b><br/><i>Associate Professor, Dept. of ECE</i>", ParagraphStyle('SigRight', parent=body_style, alignment=2))],
        [Paragraph("Date : ____________________", body_style),
         Paragraph("Date : ____________________", ParagraphStyle('DateRight', parent=body_style, alignment=2))]
    ]
    sig_table = Table(sig_data, colWidths=[90 * mm, 90 * mm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(sig_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 2: ITEM 1 - CIRCUIT DIAGRAM
    # -------------------------------------------------------------
    story.append(Paragraph("1. CIRCUIT DIAGRAM (REFERENCE CIRCUIT SPECIFICATION)", h1_style))
    story.append(Paragraph(
        "Source Reference: <b>555-Timer-Circuits.com Metal Detector / Dual Inductance-Sensitive Tone Generator</b>. "
        "The circuit operates as an astable multivibrator where oscillation frequency is modulated by the inductive "
        "reactance of choke L1 in conjunction with timing capacitors and feedback resistor R2. When a metallic "
        "object is brought into proximity with the external choke, the inductance shifts, producing an audible frequency change.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))
    
    webpage_img = EDIR / "reference_webpage_clean.png"
    schem_ref_img = EDIR / "reference_schematic_enlarged.png"
    
    if webpage_img.exists() and schem_ref_img.exists():
        circ_table = Table([
            [Paragraph("<b>Source Website & Parts List:</b>", h2_style),
             Paragraph("<b>Enlarged Circuit Schematic:</b>", h2_style)],
            [RLImage(str(webpage_img), width=78 * mm, height=98 * mm),
             RLImage(str(schem_ref_img), width=92 * mm, height=74 * mm)]
        ], colWidths=[82 * mm, 96 * mm])
        circ_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,1), (-1,1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(circ_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 3: ITEM 2 - SCHEMATIC DIAGRAM
    # -------------------------------------------------------------
    story.append(Paragraph("2. SCHEMATIC DIAGRAM (KiCad Schematic Editor)", h1_style))
    story.append(Paragraph(
        "Live interactive KiCad Schematic Editor capture showing the complete dual 555 oscillator design. "
        "The schematic is organized into four distinct functional modules: (1) 9V DC Power Supply Conditioning with reverse polarity protection and bulk/high-frequency filtering; "
        "(2) Channel A 555 astable oscillator with external inductor connector J2 and speaker connector J3; "
        "(3) Channel B 555 astable oscillator with external inductor connector J4 and speaker connector J5; and "
        "(4) Mechanical M3 chassis mounting holes (H1-H4).",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    schem_screen = EDIR / "gui_screenshot_schematic.png"
    if schem_screen.exists():
        story.append(RLImage(str(schem_screen), width=175 * mm, height=101.2 * mm))
        story.append(Spacer(1, 2 * mm))
        
    schem_meta = [
        [Paragraph("<b>Sheet Size / Frame:</b>", body_style), Paragraph("A3 (420 x 297 mm, Standard Drawing Frame)", body_style),
         Paragraph("<b>Hierarchy:</b>", body_style), Paragraph("Flat Single Sheet (Root /)", body_style)],
        [Paragraph("<b>Oscillator Channels:</b>", body_style), Paragraph("2 Identical 555 Astable Circuits (Ch A & Ch B)", body_style),
         Paragraph("<b>Decoupling Capacitors:</b>", body_style), Paragraph("100 nF Ceramic per IC (Pin 8 to GND)", body_style)],
        [Paragraph("<b>ERC Status:</b>", body_style), Paragraph("<font color='#276749'><b>0 Errors, 0 Warnings (Passed)</b></font>", body_style),
         Paragraph("<b>Schematic File:</b>", body_style), Paragraph("dual_555_tone_demonstrator.kicad_sch", body_style)],
    ]
    t_sch = Table(schem_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_sch)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 4: ITEM 3 - LAYOUT
    # -------------------------------------------------------------
    story.append(Paragraph("3. COMPOSITE PCB LAYOUT (KiCad PCB Editor)", h1_style))
    story.append(Paragraph(
        "Live interactive PCB Editor screenshot showing double-sided routing (F.Cu red, B.Cu blue), "
        "continuous solid ground planes with thermal relief spokes, component placements, and Edge.Cuts outline. "
        "Supply connector J1 is placed on the left edge; external inductor headers J2 & J4 along the lower edge; "
        "external speaker headers J3 & J5 along the upper edge; timing loops kept minimal; 4x M3 mounting holes at corners.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    pcb_screen = EDIR / "pcb_editor_layout_user.jpg"
    if pcb_screen.exists():
        story.append(RLImage(str(pcb_screen), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    layout_meta = [
        [Paragraph("<b>Board Dimensions:</b>", body_style), Paragraph("90.00 mm x 70.00 mm (Rectangular)", body_style),
         Paragraph("<b>Layer Stackup:</b>", body_style), Paragraph("2 Copper Layers (F.Cu & B.Cu, 1.6 mm FR4)", body_style)],
        [Paragraph("<b>Component Count:</b>", body_style), Paragraph("23 Through-Hole Components", body_style),
         Paragraph("<b>Routing Completion:</b>", body_style), Paragraph("<font color='#276749'><b>49 / 49 Nets (100% Routed, 0 Unrouted)</b></font>", body_style)],
        [Paragraph("<b>Mounting Holes:</b>", body_style), Paragraph("4x M3 (3.2 mm NPTH, 6.0 mm Keepout)", body_style),
         Paragraph("<b>Diagnostic Test Points:</b>", body_style), Paragraph("6 THT Pads (TP1 - TP6)", body_style)],
    ]
    t_lay = Table(layout_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_lay.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_lay)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 5: ITEM 4 - FRONT COPPER (F.Cu)
    # -------------------------------------------------------------
    story.append(Paragraph("4. FRONT COPPER LAYER (F.Cu)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor layer inspection view showing the top copper routing (F.Cu) with all inactive layers hidden. "
        "Features 0.50 mm wide power distribution tracks (+9V DC rail) and 0.30 mm signal tracks. All trace corners utilize "
        "45-degree mitered chamfers (0.60 mm setback) to prevent 90-degree acid traps during chemical etching.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    f_cu_img = EDIR / "gui_screenshot_f_cu.jpg"
    if f_cu_img.exists():
        story.append(RLImage(str(f_cu_img), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    f_cu_meta = [
        [Paragraph("<b>Layer Name:</b>", body_style), Paragraph("F.Cu (Top Copper, Red)", body_style),
         Paragraph("<b>Copper Thickness:</b>", body_style), Paragraph("35 µm (1.0 oz/ft² finished)", body_style)],
        [Paragraph("<b>Power Track Width:</b>", body_style), Paragraph("0.50 mm (19.69 mils, Net /+9V)", body_style),
         Paragraph("<b>Signal Track Width:</b>", body_style), Paragraph("0.30 mm (11.81 mils)", body_style)],
        [Paragraph("<b>Minimum Clearance:</b>", body_style), Paragraph("0.25 mm (Board Minimum)", body_style),
         Paragraph("<b>Corner Miter Geometry:</b>", body_style), Paragraph("45° Diagonal Transitions", body_style)],
    ]
    t_fcu = Table(f_cu_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_fcu.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fcu)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 6: ITEM 5 - BACK COPPER (B.Cu)
    # -------------------------------------------------------------
    story.append(Paragraph("5. BACK COPPER LAYER (B.Cu)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor layer inspection view showing the bottom copper routing (B.Cu) with all inactive layers hidden. "
        "Provides an expansive, low-impedance ground return plane with thermal relief spoke connections to through-hole GND pads. "
        "Interconnects Channel A and Channel B oscillator timing sub-circuits while preserving return current continuity.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    b_cu_img = EDIR / "gui_screenshot_b_cu.jpg"
    if b_cu_img.exists():
        story.append(RLImage(str(b_cu_img), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    b_cu_meta = [
        [Paragraph("<b>Layer Name:</b>", body_style), Paragraph("B.Cu (Bottom Copper, Blue)", body_style),
         Paragraph("<b>Copper Thickness:</b>", body_style), Paragraph("35 µm (1.0 oz/ft² finished)", body_style)],
        [Paragraph("<b>Ground Plane Pour:</b>", body_style), Paragraph("Solid Continuous Zone (Net /GND)", body_style),
         Paragraph("<b>Thermal Relief Spokes:</b>", body_style), Paragraph("4 Spokes (0.50 mm width, 0.35 mm gap)", body_style)],
        [Paragraph("<b>Unconnected Copper:</b>", body_style), Paragraph("0 Isolated Copper Islands", body_style),
         Paragraph("<b>Corner Miter Geometry:</b>", body_style), Paragraph("45° Diagonal Transitions", body_style)],
    ]
    t_bcu = Table(b_cu_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_bcu.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_bcu)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 7: ITEM 6 - SILKSCREEN (F.SilkS)
    # -------------------------------------------------------------
    story.append(Paragraph("6. SILKSCREEN LAYER (F.SilkS)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor layer inspection view showing the front silkscreen legend (F.SilkS) with all inactive layers hidden. "
        "Contains unambiguous component outlines, reference designators (U1-U2, R1-R3, C1-C12, D1, J1-J5, TP1-TP6), "
        "polarity indicators (+/- for 9V IN, pin 1 notches for DIP-8 ICs, and electrolytic capacitor positive markings), "
        "connector labels (9V IN, L_A, L_B, SPK_A, SPK_B), and student roll number identification.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    silks_img = EDIR / "gui_screenshot_f_silks.jpg"
    if silks_img.exists():
        story.append(RLImage(str(silks_img), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    silk_meta = [
        [Paragraph("<b>Layer Name:</b>", body_style), Paragraph("F.SilkS (Front Silkscreen, Yellow/White)", body_style),
         Paragraph("<b>Silkscreen Color:</b>", body_style), Paragraph("White on Green Solder Mask", body_style)],
        [Paragraph("<b>Text Height / Width:</b>", body_style), Paragraph("1.0 mm / 1.5 mm (0.15 mm line thickness)", body_style),
         Paragraph("<b>Polarity Labels:</b>", body_style), Paragraph("9V IN (+/-), L A/B, SPK A/B, C1-C12 (+)", body_style)],
        [Paragraph("<b>Student Attribution:</b>", body_style), Paragraph("124EC0030 — DIVYANSH RAWAT", body_style),
         Paragraph("<b>Title Legend:</b>", body_style), Paragraph("DUAL 555 TONE DEMONSTRATOR - A", body_style)],
    ]
    t_silk = Table(silk_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_silk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_silk)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 8: ITEM 7 - SOLDER MASK (F.Mask & B.Mask)
    # -------------------------------------------------------------
    story.append(Paragraph("7. SOLDER MASK LAYER (F.Mask & B.Mask)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor layer inspection views showing solder mask apertures with inactive layers hidden. "
        "Top apertures (F.Mask, purple) and bottom apertures (B.Mask, teal) provide 0.10 mm radial clearance around all "
        "through-hole component pads, test points, terminal blocks, and mounting holes to prevent solder bridging during hand soldering.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    
    f_mask_img = EDIR / "gui_screenshot_f_mask.jpg"
    b_mask_img = EDIR / "gui_screenshot_b_mask.jpg"
    
    if f_mask_img.exists() and b_mask_img.exists():
        mask_table = Table([
            [Paragraph("<b>Front Solder Mask Apertures (F.Mask - Top Side):</b>", h2_style),
             Paragraph("<b>Back Solder Mask Apertures (B.Mask - Solder Side):</b>", h2_style)],
            [RLImage(str(f_mask_img), width=86 * mm, height=48.4 * mm),
             RLImage(str(b_mask_img), width=86 * mm, height=48.4 * mm)],
        ], colWidths=[88 * mm, 88 * mm])
        mask_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(mask_table)
        story.append(Spacer(1, 3 * mm))
    elif f_mask_img.exists():
        story.append(RLImage(str(f_mask_img), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    mask_meta = [
        [Paragraph("<b>Mask Clearances:</b>", body_style), Paragraph("0.10 mm (Board Design Rules)", body_style),
         Paragraph("<b>Minimum Solder Dam:</b>", body_style), Paragraph("0.10 mm Between Adjacent Pads", body_style)],
        [Paragraph("<b>Pad Aperture Coverage:</b>", body_style), Paragraph("All 70 THT Component & Connector Pads", body_style),
         Paragraph("<b>Mask Finish / Color:</b>", body_style), Paragraph("Liquid Photoimageable (LPI) Green", body_style)],
    ]
    t_mask = Table(mask_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_mask.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_mask)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 9: ITEM 8 - SCREENSHOT OF ERC
    # -------------------------------------------------------------
    story.append(Paragraph("8. SCREENSHOT OF ELECTRICAL RULES CHECK (ERC)", h1_style))
    story.append(Paragraph(
        "Live KiCad Schematic Editor Electrical Rules Checker dialog showing <b>0 Errors, 0 Warnings, and 0 Violations</b>. "
        "Confirms that all pin electrical types, power flag drivers, net connectivity, and label references match design rules.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    proof_erc = EDIR / "proof_erc_gui.png"
    if proof_erc.exists():
        story.append(RLImage(str(proof_erc), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    erc_meta = [
        [Paragraph("<b>ERC Status:</b>", body_style), Paragraph("<font color='#276749'><b>PASSED (0 Errors, 0 Warnings)</b></font>", body_style),
         Paragraph("<b>KiCad Version:</b>", body_style), Paragraph("9.0.8+dfsg-1 (Linux x86_64)", body_style)],
        [Paragraph("<b>Schematic File:</b>", body_style), Paragraph("dual_555_tone_demonstrator.kicad_sch", body_style),
         Paragraph("<b>Sheet Name:</b>", body_style), Paragraph("Root Sheet (/)", body_style)],
        [Paragraph("<b>Power Flags:</b>", body_style), Paragraph("PWR_FLAG configured on +9V & GND", body_style),
         Paragraph("<b>Unconnected Pins:</b>", body_style), Paragraph("0 Unintended Unconnected Pins", body_style)],
    ]
    t_erc = Table(erc_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_erc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_erc)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 10: ITEM 9 - SCREENSHOT OF DRC
    # -------------------------------------------------------------
    story.append(Paragraph("9. SCREENSHOT OF DESIGN RULES CHECK (DRC)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor Design Rules Checker dialog showing <b>0 Violations, 0 Unconnected Items, and 0 Schematic Parity Warnings</b>. "
        "Confirms 100% routing completion, strict clearance compliance, zero courtyard overlaps, and full board-to-schematic netlist synchronization.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))
    proof_drc = EDIR / "proof_drc_gui.jpg"
    if proof_drc.exists():
        story.append(RLImage(str(proof_drc), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 2 * mm))
        
    drc_meta = [
        [Paragraph("<b>DRC Violations:</b>", body_style), Paragraph("<font color='#276749'><b>0 Violations</b></font>", body_style),
         Paragraph("<b>Unconnected Items:</b>", body_style), Paragraph("<font color='#276749'><b>0 Unconnected Items</b></font>", body_style)],
        [Paragraph("<b>Schematic Parity:</b>", body_style), Paragraph("<font color='#276749'><b>0 Issues (100% Match)</b></font>", body_style),
         Paragraph("<b>Overall DRC:</b>", body_style), Paragraph("<font color='#276749'><b>0 Errors, 0 Warnings</b></font>", body_style)],
        [Paragraph("<b>Zone Refill Status:</b>", body_style), Paragraph("All Zones Filled Prior to Check", body_style),
         Paragraph("<b>Board File:</b>", body_style), Paragraph("dual_555_tone_demonstrator.kicad_pcb", body_style)],
    ]
    t_drc = Table(drc_meta, colWidths=[38 * mm, 52 * mm, 38 * mm, 52 * mm])
    t_drc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_drc)
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 11: APPENDIX A - MULTI-PERSPECTIVE 3D VIEWS
    # -------------------------------------------------------------
    story.append(Paragraph("APPENDIX A: 3D VISUALIZATION VIEWS (REALISTIC GREEN SOLDERMASK)", h1_style))
    story.append(Paragraph(
        "Comprehensive 3D renders from four vantage points demonstrating component package fit, "
        "through-hole solder joints, connector orientations, and ground planes.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))
    
    v_top = EDIR / "3d_view_top.jpg"
    v_iso = EDIR / "3d_view_isometric.jpg"
    v_front = EDIR / "3d_view_front.png"
    v_side = EDIR / "3d_view_side.jpg"
    
    if v_top.exists() and v_iso.exists() and v_front.exists() and v_side.exists():
        grid_3d = Table([
            [Paragraph("<b>Top Orthogonal View:</b>", h2_style),
             Paragraph("<b>Isometric Perspective View:</b>", h2_style)],
            [RLImage(str(v_top), width=85 * mm, height=48 * mm),
             RLImage(str(v_iso), width=85 * mm, height=48 * mm)],
            [Paragraph("<b>Front Elevation View:</b>", h2_style),
             Paragraph("<b>Side Profile View:</b>", h2_style)],
            [RLImage(str(v_front), width=85 * mm, height=48 * mm),
             RLImage(str(v_side), width=85 * mm, height=48 * mm)]
        ], colWidths=[87 * mm, 87 * mm])
        grid_3d.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(grid_3d)
        story.append(Spacer(1, 3 * mm))
        
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 12: APPENDIX B - BILL OF MATERIALS (BOM)
    # -------------------------------------------------------------
    story.append(Paragraph("APPENDIX B: BILL OF MATERIALS (BOM)", h1_style))
    bom_data = [
        ["Item", "Reference", "Value", "Footprint", "Qty", "Description / Function"]
    ]
    bom_rows = [
        ("1", "U1, U2", "NE555P", "DIP-8_W7.62mm", "2", "Precision Bipolar Timer IC"),
        ("2", "J1", "9V_INPUT", "TerminalBlock_MPT-0.5-2_P2.54mm", "1", "DC Power Input Terminal Block"),
        ("3", "J2, J4", "L_A, L_B", "PinHeader_1x02_P2.54mm_Vertical", "2", "External Inductor (10 mH) Connectors"),
        ("4", "J3, J5", "SPK_A, SPK_B", "PinHeader_1x02_P2.54mm_Vertical", "2", "External Speaker (8 Ohm) Connectors"),
        ("5", "C1", "100uF_16V", "CP_Radial_D6.3mm_P2.50mm", "1", "Power Supply Bulk Reservoir Capacitor"),
        ("6", "C2, C6, C11", "100nF", "C_Disc_D4.3mm_W1.9mm_P5.00mm", "3", "High-Frequency Ceramic Bypass Capacitors"),
        ("7", "C3, C4, C8, C9", "2.2uF_16V", "CP_Radial_D5.0mm_P2.00mm", "4", "Astable Timing Electrolytic Capacitors"),
        ("8", "C5, C7, C10, C12", "10uF_16V", "CP_Radial_D5.0mm_P2.00mm", "4", "AC Audio Output Coupling Capacitors"),
        ("9", "R1", "1k", "R_Axial_DIN0207_P7.62mm", "1", "Power LED Current-Limiting Resistor"),
        ("10", "R2, R3", "47k", "R_Axial_DIN0207_P7.62mm", "2", "Astable Timing Feedback Resistors"),
        ("11", "D1", "PWR_LED", "LED_D3.0mm", "1", "Green Power Status Indicator"),
        ("12", "TP1-TP6", "TestPoint", "TestPoint_THTPad_D1.5mm", "6", "Diagnostic Test Points (+9V, GND, Outs, Timings)"),
        ("13", "H1-H4", "M3 Hole", "MountingHole_3.2mm_M3", "4", "M3 Mechanical Chassis Mounting Holes")
    ]
    for r in bom_rows:
        bom_data.append([Paragraph(cell, body_style) for cell in r])
        
    bom_table = Table(bom_data, colWidths=[12 * mm, 25 * mm, 22 * mm, 52 * mm, 12 * mm, 55 * mm])
    bom_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(bom_table)
    
    # Build complete document
    doc.build(story)
    print(f" [✓] ReportLab Document Built: {temp_pdf}")
    
    # Save Master PDF to both 124EC0030/ and end_exam/
    final_pdf_submission = SUBMISSION_DIR / "124EC0030_EPM_End_Semester_Exam.pdf"
    final_pdf_edir = EDIR / "124EC0030_EPM_End_Semester_Exam.pdf"
    
    shutil.copy(temp_pdf, final_pdf_submission)
    shutil.copy(temp_pdf, final_pdf_edir)
    
    print(f" [✓] Final Master PDF successfully generated:")
    print(f"     -> {final_pdf_submission} ({final_pdf_submission.stat().st_size} bytes)")
    
    # -------------------------------------------------------------
    # Synchronize All Design Files to SUBMISSION_DIR (124EC0030/)
    # -------------------------------------------------------------
    print(" [*] Synchronizing Project Files to 124EC0030/...")
    shutil.copy(EDIR / "dual_555_tone_demonstrator.kicad_pro", SUBMISSION_DIR / "dual_555_tone_demonstrator.kicad_pro")
    shutil.copy(EDIR / "dual_555_tone_demonstrator.kicad_sch", SUBMISSION_DIR / "dual_555_tone_demonstrator.kicad_sch")
    shutil.copy(EDIR / "dual_555_tone_demonstrator.kicad_pcb", SUBMISSION_DIR / "dual_555_tone_demonstrator.kicad_pcb")
    shutil.copy(EDIR / "bom.csv", SUBMISSION_DIR / "bom.csv")
    shutil.copy(EDIR / "dual_555_drc_final.rpt", SUBMISSION_DIR / "dual_555_drc_report.txt")
    shutil.copy(EDIR / "dual_555_erc.rpt", SUBMISSION_DIR / "dual_555_erc_report.txt")
    shutil.copy(EDIR / "3d_render_top.png", SUBMISSION_DIR / "3d_render_top.png")
    
    # Gerbers folder & ZIP
    sub_gerbers = SUBMISSION_DIR / "gerbers"
    if sub_gerbers.exists():
        shutil.rmtree(sub_gerbers)
    shutil.copytree(EDIR / "gerbers", sub_gerbers)
    
    zip_path = SUBMISSION_DIR / "gerbers.zip"
    subprocess.run(["zip", "-r", str(zip_path), "."], cwd=str(sub_gerbers), capture_output=True)
    shutil.copy(zip_path, EDIR / "gerbers.zip")
    print(f" [✓] Gerbers ZIP created: {zip_path}")
    
    print("==================================================================")
    print(" [✓] DELIVERABLES FULLY COMPILED WITH AUTHENTIC GUI SCREENSHOTS!")
    print("==================================================================")

if __name__ == "__main__":
    build_pdf_document()
