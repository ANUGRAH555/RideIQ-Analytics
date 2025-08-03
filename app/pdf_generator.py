from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "RideIQ Rides Data Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def sanitize_text(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '₹': 'Rs.',
        '–': '-', '—': '-',
        '“': '"', '”': '"',
        '‘': "'", '’': "'",
        '…': '...',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # encode to latin-1 ignoring unsupported chars and decode back
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf_report(analysis, insights, plot_paths, output_path="RideIQ_Report.pdf"):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Section 1: KPIs
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Key Metrics", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, sanitize_text(f"Total Rides: {analysis.get('total_rides', 'N/A')}"), ln=True)
    pdf.cell(0, 8, sanitize_text(f"Average Fare: Rs.{analysis.get('avg_fare', 0):.2f}"), ln=True)
    pdf.cell(0, 8, sanitize_text(f"Total Revenue: Rs.{analysis.get('total_revenue', 0):.2f}"), ln=True)
    pdf.cell(0, 8, sanitize_text(f"Peak Hour: {analysis.get('peak_hour', 'N/A')}:00"), ln=True)

    # Section 2: Insights
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Auto-Generated Insights", ln=True)
    pdf.set_font("Arial", "", 11)
    for line in insights:
        clean_line = sanitize_text(line)
        pdf.cell(0, 8, clean_line, ln=True)

    # Section 3: Plots
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Visualizations", ln=True)

    max_image_height = 120  # mm, adjust if needed

    for path in plot_paths:
        if os.path.exists(path):
            current_y = pdf.get_y()
            page_height = pdf.h - pdf.b_margin
            space_left = page_height - current_y

            if space_left < max_image_height:
                pdf.add_page()

            pdf.image(path, w=180)
            pdf.ln(5)

    try:
        pdf.output(output_path)
        print(f"✅ PDF generated: {output_path}")
    except UnicodeEncodeError as e:
        print("❌ UnicodeEncodeError during PDF generation.")
        print("Check if any string still contains non-Latin-1 characters.")
        print("Error:", e)
