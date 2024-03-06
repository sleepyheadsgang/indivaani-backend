import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def extract_text_with_format(pdf_path):
    doc = fitz.open(pdf_path)
    text_with_format = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text_with_format.append({
                            "text": s["text"],
                            "font_size": s["size"],
                            "font_color": s["color"],
                            "font_bold": bool(s["flags"] & 2),
                            "font_italic": bool(s["flags"] & 1)
                        })
            elif b['type'] == 1:
                # Image type, you can handle images as well if needed
                pass

    doc.close()
    return text_with_format

def create_pdf_from_text_with_format(output_path, text_with_format):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(output_path, pagesize=letter)

    # Create a list to hold the flowables
    flowables = []

    # Define custom styles for bold and italic text
    custom_styles = {
        "bold": ParagraphStyle("Bold", parent=styles["Normal"], fontName="Helvetica-Bold"),
        "italic": ParagraphStyle("Italic", parent=styles["Normal"], fontName="Helvetica-Oblique"),
        "normal": styles["Normal"]
    }

    # Add paragraphs with formatting
    for item in text_with_format:
        text = item["text"]
        font_size = item["font_size"]
        font_color = item["font_color"]
        font_bold = item["font_bold"]
        font_italic = item["font_italic"]

        style = custom_styles["normal"]
        if font_bold and font_italic:
            style = custom_styles["bold"]
        elif font_bold:
            style = custom_styles["bold"]
        elif font_italic:
            style = custom_styles["italic"]

        p = Paragraph(text, style)
        flowables.append(p)
        flowables.append(Spacer(1, 12))  # Adjust the spacing as needed

    # Build the PDF document
    pdf.build(flowables)

if __name__ == "__main__":
    input_pdf_path = "input.pdf"
    output_pdf_path = "output.pdf"

    text_with_format = extract_text_with_format(input_pdf_path)
    create_pdf_from_text_with_format(output_pdf_path, text_with_format)
