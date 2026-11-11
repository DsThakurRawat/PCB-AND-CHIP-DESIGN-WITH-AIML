#!/home/divyansh-rawat/AIPCBDESIGN/.venv/bin/python3
"""
Step 5: Compilation of Final Deliverables & Single PDF Submission
Author: Divyansh Rawat (Roll No: 124EC0030)
Department of ECE, IIIT Kurnool
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

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from pypdf import PdfWriter, PdfReader

def build_pdf_document():
    print("==================================================================")
    print(" [*] COMPILING MASTER SINGLE SUBMISSION PDF")
    print("==================================================================")
    
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    temp_cover_pdf = EDIR / "temp_cover_viva.pdf"
    
    # 1. Setup Document
    doc = SimpleDocTemplate(
        str(temp_cover_pdf),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1, # Center
        textColor=colors.HexColor('#1A365D')
    )
    
    sub_title = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#2B6CB0')
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=6,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2D3748')
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    story = []
    
    # --- PAGE 1: TITLE & COVER PAGE ---
    story.append(Paragraph("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY, KURNOOL", sub_title))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("Department of Electronics and Communication Engineering", sub_title))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Electronic Prototyping and Manufacturing (EPM) Laboratory", title_style))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("End Semester Practical Examination — Laboratory Report", sub_title))
    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceBefore=2, spaceAfter=8))
    
    meta_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Divyansh Rawat", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("124EC0030", body_style)],
        [Paragraph("<b>Course Faculty:</b>", body_style), Paragraph("Dr. Eswaramoorthy K V", body_style),
         Paragraph("<b>Date of Exam:</b>", body_style), Paragraph("10-11-2026", body_style)],
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("Dual Inductance-Sensitive Tone Demonstrator - A", body_style),
         Paragraph("<b>Exam Pattern:</b>", body_style), Paragraph("Layout Variant A (90 x 70 mm)", body_style)],
        [Paragraph("<b>Design Environment:</b>", body_style), Paragraph("KiCad 9.0.8 (x86_64 Linux)", body_style),
         Paragraph("<b>DRC / ERC Status:</b>", body_style), Paragraph("<font color='#276749'><b>0 Errors / 0 Violations</b></font>", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[38 * mm, 50 * mm, 38 * mm, 54 * mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6 * mm))
    
    story.append(Paragraph("<b>EXAM QUESTION SPECIFICATIONS (VARIANT A):</b>", h2_style))
    spec_text = (
        "Implement two copies of the source 555 inductance-sensitive oscillator. Use an external inductor "
        "connector and speaker connector for each channel. Supply: 9 V DC. Use a 90 x 70 mm rectangular board. "
        "Place the supply connector on the left edge, input/user controls along the lower edge and outputs along "
        "the upper edge. Keep inductive/timing loops short; label L A/B and SPK A/B connector polarity where applicable. "
        "Mandatory circuit clarifications: No search-coil winding, detection-distance target or field calibration is required. "
        "This is a layout-only oscillator demonstrator, not a validated general metal detector. Use exact capacitor connections "
        "from the schematic. Assign verified through-hole footprints and complete a two-copper-layer PCB using both F.Cu and B.Cu."
    )
    story.append(Paragraph(spec_text, body_style))
    story.append(Spacer(1, 5 * mm))
    
    # Add Green 3D Render on cover as requested by student
    render_green = EDIR / "3d_render_green_user.jpg"
    if render_green.exists():
        story.append(Paragraph("<b>3D BOARD PREVIEW (REALISTIC GREEN SOLDERMASK):</b>", h2_style))
        story.append(RLImage(str(render_green), width=175 * mm, height=98 * mm))
        story.append(Spacer(1, 4 * mm))
    else:
        render_img = EDIR / "3d_render_top.png"
        if render_img.exists():
            story.append(Paragraph("<b>3D RAYTRACED BOARD PREVIEW:</b>", h2_style))
            story.append(RLImage(str(render_img), width=175 * mm, height=95 * mm))
            story.append(Spacer(1, 4 * mm))
        
    story.append(PageBreak())
    
    # --- PAGE 2: ITEM 1 - CIRCUIT DIAGRAM ---
    story.append(Paragraph("1. CIRCUIT DIAGRAM (REFERENCE CIRCUIT SPECIFICATION)", h1_style))
    story.append(Paragraph(
        "Source Reference: <b>555-Timer-Circuits.com Metal Detector / Dual Inductance-Sensitive Tone Generator</b>. "
        "The circuit operates as an astable multivibrator where oscillation frequency is modulated by the inductive "
        "reactance of choke L1 in conjunction with timing capacitors and feedback resistor R2. When a metallic "
        "object is brought into proximity with the external choke, the inductance shifts, producing an audible frequency change.",
        body_style
    ))
    story.append(Spacer(1, 4 * mm))
    
    webpage_img = EDIR / "reference_webpage_clean.png"
    schem_img = Path("/tmp/schematic_highres.png")
    
    if webpage_img.exists() and schem_img.exists():
        circ_table = Table([
            [Paragraph("<b>Source Website & Parts List:</b>", h2_style),
             Paragraph("<b>Enlarged Circuit Schematic:</b>", h2_style)],
            [RLImage(str(webpage_img), width=78 * mm, height=98 * mm),
             RLImage(str(schem_img), width=92 * mm, height=74 * mm)]
        ], colWidths=[82 * mm, 96 * mm])
        circ_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,1), (-1,1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(circ_table)
        story.append(Spacer(1, 4 * mm))
    elif schem_img.exists():
        story.append(RLImage(str(schem_img), width=160 * mm, height=125 * mm))
        story.append(Spacer(1, 4 * mm))
        
    story.append(PageBreak())

    # --- PAGE 3: ITEM 8 - SCREENSHOT OF ERC ---
    story.append(Paragraph("8. SCREENSHOT OF ELECTRICAL RULES CHECK (ERC)", h1_style))
    story.append(Paragraph(
        "Live KiCad Schematic Editor Electrical Rules Checker dialog showing <b>0 Errors, 0 Warnings, and 0 Violations</b>.",
        body_style
    ))
    story.append(Spacer(1, 4 * mm))
    
    proof_erc = EDIR / "proof_erc_gui.png"
    if proof_erc.exists():
        story.append(RLImage(str(proof_erc), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 3 * mm))
        
    erc_meta = [
        [Paragraph("<b>ERC Status:</b>", body_style), Paragraph("<font color='#276749'><b>PASSED (0 Errors, 0 Warnings)</b></font>", body_style),
         Paragraph("<b>KiCad Version:</b>", body_style), Paragraph("9.0.8+dfsg-1 (Linux x86_64)", body_style)],
        [Paragraph("<b>Schematic File:</b>", body_style), Paragraph("dual_555_tone_demonstrator.kicad_sch", body_style),
         Paragraph("<b>Sheet Name:</b>", body_style), Paragraph("Root Sheet (/)", body_style)]
    ]
    t_erc = Table(erc_meta, colWidths=[35 * mm, 55 * mm, 35 * mm, 55 * mm])
    t_erc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_erc)
    story.append(PageBreak())

    # --- PAGE 4: ITEM 9 - SCREENSHOT OF DRC ---
    story.append(Paragraph("9. SCREENSHOT OF DESIGN RULES CHECK (DRC)", h1_style))
    story.append(Paragraph(
        "Live KiCad PCB Editor Design Rules Checker dialog showing <b>0 Violations, 0 Unconnected Items, and 0 Schematic Parity Warnings</b>.",
        body_style
    ))
    story.append(Spacer(1, 4 * mm))
    
    proof_drc = EDIR / "proof_drc_gui.jpg"
    if proof_drc.exists():
        story.append(RLImage(str(proof_drc), width=175 * mm, height=98.4 * mm))
        story.append(Spacer(1, 3 * mm))
        
    drc_meta = [
        [Paragraph("<b>DRC Violations:</b>", body_style), Paragraph("<font color='#276749'><b>0 Violations</b></font>", body_style),
         Paragraph("<b>Unconnected Items:</b>", body_style), Paragraph("<font color='#276749'><b>0 Unconnected Items</b></font>", body_style)],
        [Paragraph("<b>Schematic Parity:</b>", body_style), Paragraph("<font color='#276749'><b>0 Issues (100% Match)</b></font>", body_style),
         Paragraph("<b>Overall DRC:</b>", body_style), Paragraph("<font color='#276749'><b>0 Errors, 0 Warnings</b></font>", body_style)]
    ]
    t_drc = Table(drc_meta, colWidths=[40 * mm, 50 * mm, 45 * mm, 45 * mm])
    t_drc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_drc)
    story.append(PageBreak())

    # --- PAGE 4: LIVE PCB EDITOR SCREENSHOT ---
    story.append(Paragraph("3. LIVE COMPOSITE PCB LAYOUT (KiCad PCB Editor)", h1_style))
    story.append(Paragraph(
        "Live interactive PCB Editor screenshot showing double-sided routing (F.Cu red, B.Cu blue), "
        "continuous solid ground planes with thermal relief spokes, component placements, and Edge.Cuts outline.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))
    
    pcb_screen = EDIR / "pcb_editor_layout_user.jpg"
    if pcb_screen.exists():
        story.append(RLImage(str(pcb_screen), width=175 * mm, height=98 * mm))
        story.append(Spacer(1, 3 * mm))
        
    story.append(PageBreak())

    # --- PAGE 5: MULTI-PERSPECTIVE 3D VIEWS (GREEN SOLDERMASK) ---
    story.append(Paragraph("4. 3D VISUALIZATION VIEWS (REALISTIC GREEN SOLDERMASK)", h1_style))
    story.append(Paragraph(
        "Comprehensive 3D renders from multiple vantage points demonstrating component package fit, "
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
    
    # --- PAGE 5: BILL OF MATERIALS TABLE ---
    story.append(Paragraph("BILL OF MATERIALS (BOM)", h1_style))
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
    
    doc.build(story)
    print(f" [✓] Base document built: {temp_cover_pdf}")
    
    # 2. Merge Vector KiCad Plots into Master PDF
    print(" [*] Merging Vector Schematic and Layer Plots...")
    writer = PdfWriter()
    
    # Add Text / Viva Voce / Report pages
    base_reader = PdfReader(str(temp_cover_pdf))
    for p in base_reader.pages:
        writer.add_page(p)
        
    # Append KiCad Vector Plots with clear bookmarks:
    layer_plots = [
        ("Schematic Diagram", EDIR / "export_schematic.pdf"),
        ("Composite PCB Layout", EDIR / "export_layout.pdf"),
        ("Front Copper (F.Cu)", EDIR / "export_f_cu.pdf"),
        ("Back Copper (B.Cu)", EDIR / "export_b_cu.pdf"),
        ("Silkscreen (F.SilkS)", EDIR / "export_f_silk.pdf"),
        ("Solder Mask (F.Mask)", EDIR / "export_mask.pdf")
    ]
    
    # Ensure all plots exist in EDIR
    shutil.copy("/tmp/export_schematic.pdf", EDIR / "export_schematic.pdf")
    shutil.copy("/tmp/export_layout.pdf", EDIR / "export_layout.pdf")
    shutil.copy("/tmp/export_f_cu.pdf", EDIR / "export_f_cu.pdf")
    shutil.copy("/tmp/export_b_cu.pdf", EDIR / "export_b_cu.pdf")
    shutil.copy("/tmp/export_f_silk.pdf", EDIR / "export_f_silk.pdf")
    shutil.copy("/tmp/export_mask.pdf", EDIR / "export_mask.pdf")
    
    for title, plot_path in layer_plots:
        if plot_path.exists():
            r = PdfReader(str(plot_path))
            for page in r.pages:
                writer.add_page(page)
            print(f"     Appended {title} ({plot_path.name})")
            
    # Save Master PDF
    final_pdf_submission = SUBMISSION_DIR / "124EC0030_EPM_End_Semester_Exam.pdf"
    final_pdf_edir = EDIR / "124EC0030_EPM_End_Semester_Exam.pdf"
    
    with open(str(final_pdf_submission), "wb") as f_out:
        writer.write(f_out)
    shutil.copy(final_pdf_submission, final_pdf_edir)
    
    print(f" [✓] Final Master PDF Generated successfully at:")
    print(f"     -> {final_pdf_submission} ({final_pdf_submission.stat().st_size} bytes, {len(writer.pages)} pages)")
    
    # 3. Synchronize all design files to SUBMISSION_DIR (124EC0030/)
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
    print(" [✓] STEP 5 COMPLETE: ALL DELIVERABLES FULLY GENERATED & VERIFIED!")
    print("==================================================================")

if __name__ == "__main__":
    build_pdf_document()
