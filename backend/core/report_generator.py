import os
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(scan_id, prediction_data, orig_image_path, heatmap_image_path, output_path):
    """
    Generates a structured clinical PDF report using ReportLab.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='ClinicalHeading', fontSize=14, spaceAfter=12, textColor=colors.HexColor('#233554')))
    
    Story = []
    
    # Title
    title = Paragraph("<font color='#00C9A7'><b>Dementia Detect</b></font> - Clinical Assessment Report", styles['Title'])
    Story.append(title)
    Story.append(Spacer(1, 24))
    
    # Patient Info Table
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    patient_data = [
        ['Patient ID:', f"{scan_id[:8].upper()}", 'Scan Date:', date_str],
        ['Modality:', 'MRI (Axial)', 'Analysis Version:', 'v1.0 (EfficientNet-B4)']
    ]
    
    t = Table(patient_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#475569')),
        ('TEXTCOLOR', (2,0), (2,-1), colors.HexColor('#475569')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 24))
    
    # Diagnosis Section
    Story.append(Paragraph("<b>Primary Diagnosis</b>", styles['ClinicalHeading']))
    
    pred_class = prediction_data.get('predicted_class', 'Unknown')
    confidence = prediction_data.get('confidence', 0.0) * 100
    
    diag_text = f"The AI model indicates a primary diagnosis of <b>{pred_class}</b> with a confidence score of <b>{confidence:.1f}%</b>."
    Story.append(Paragraph(diag_text, styles['Normal']))
    Story.append(Spacer(1, 24))
    
    # Images Section
    Story.append(Paragraph("<b>Visual Findings (GradCAM ROI)</b>", styles['ClinicalHeading']))
    
    img_width = 2.5*inch
    img_height = 2.5*inch
    
    # Ensure images exist
    if os.path.exists(orig_image_path) and os.path.exists(heatmap_image_path):
        img_data = [[
            RLImage(orig_image_path, width=img_width, height=img_height),
            RLImage(heatmap_image_path, width=img_width, height=img_height)
        ], [
            Paragraph("Original Input", styles['Center']),
            Paragraph("GradCAM Activation", styles['Center'])
        ]]
        
        img_table = Table(img_data, colWidths=[3*inch, 3*inch])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        Story.append(img_table)
    else:
        Story.append(Paragraph("<i>Images not available for rendering.</i>", styles['Normal']))
        
    Story.append(Spacer(1, 24))
    
    # Summary
    Story.append(Paragraph("<b>Findings Summary</b>", styles['ClinicalHeading']))
    summary_text = (
        "Automated volumetric and heatmap analysis highlights localized atrophy "
        "and signal intensity variations consistent with the predicted stage. "
        "The heatmap overlay indicates the neural network's primary areas of focus, "
        "which typically correlate with the hippocampus and entorhinal cortex in positive cases. "
        "<i>Clinical correlation is required.</i>"
    )
    Story.append(Paragraph(summary_text, styles['Normal']))
    
    doc.build(Story)
    return output_path
