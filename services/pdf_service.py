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
        
        # Use Bundled Font (NanumGothic) for Cross-Platform Korean support
        font_path = os.path.join(os.getcwd(), 'static', 'fonts', 'NanumGothic.ttf')
        
        if os.path.exists(font_path):
            pdf.add_font('NanumGothic', '', font_path)
            pdf.set_font('NanumGothic', size=12)
        else:
            # Fallback if bundled font not found (no longer trying system fonts)
            pdf.set_font("Helvetica", size=12) # Standard FPDF font
            print("Warning: Korean font (NanumGothic) not found. Text may appear broken.")

        # Title
        pdf.cell(200, 10, txt=f"InsightPulse Report: {ticker}", ln=True, align='C')
        
        # Body
        if 'NanumGothic' in pdf.fonts:
             pdf.set_font("NanumGothic", size=10)
        else: # Fallback to Helvetica if NanumGothic wasn't loaded
             pdf.set_font("Helvetica", size=10)
            
        pdf.multi_cell(0, 10, txt=str(analysis_data))
        
        filename = f"{ticker}_report.pdf"
        output_path = os.path.join("services", filename) 
        pdf.output(output_path)
        
        return output_path

pdf_service = PDFService()
