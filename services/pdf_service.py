from fpdf import FPDF
import os

class PDFService:
    def create_report(self, ticker, analysis_data):
        """
        Generates a PDF report for the given ticker and analysis data.
        Returns the file path of the generated PDF.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Use Windows System Font (Malgun Gothic) for Korean support
        font_path = "C:/Windows/Fonts/malgun.ttf"
        if os.path.exists(font_path):
            pdf.add_font('Malgun', '', font_path) # Removed unique=True
            pdf.set_font('Malgun', size=12)
        else:
            # Fallback if font missing (unlikely on Windows)
            pdf.set_font("Arial", size=12)
            print("Warning: Malgun font not found. Korean may not render.")

        pdf.cell(200, 10, txt=f"InsightPulse Report: {ticker}", ln=True, align='C')
        
        if os.path.exists(font_path):
            pdf.set_font("Malgun", size=10)
        else:
            pdf.set_font("Arial", size=10)
            
        pdf.multi_cell(0, 10, txt=str(analysis_data))
        
        filename = f"{ticker}_report.pdf"
        output_path = os.path.join("services", filename) 
        pdf.output(output_path)
        
        return output_path

pdf_service = PDFService()
