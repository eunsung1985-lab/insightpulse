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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(base_dir, 'static', 'fonts', 'NanumGothic.ttf')
        
        # Debugging: List files to check if font uploaded
        print(f"[PDF] Current working dir: {os.getcwd()}")
        font_dir = os.path.join(base_dir, 'static', 'fonts')
        if os.path.exists(font_dir):
            print(f"[PDF] Files in static/fonts: {os.listdir(font_dir)}")
        else:
            print(f"[PDF] static/fonts dir NOT FOUND at {font_dir}")

        if os.path.exists(font_path):
            pdf.add_font('NanumGothic', '', font_path)
            pdf.set_font('NanumGothic', size=12)
            print("[PDF] Loaded NanumGothic successfully.")
        else:
            print("[PDF] FONT FILE MISSING! Fallback to Helvetica.") 
            pdf.set_font("Helvetica", size=12) # Standard FPDF font
            print("Warning: Korean font not found. Text may appear broken.")

        # Title
        pdf.cell(200, 10, txt=f"InsightPulse Report: {ticker}", ln=True, align='C')
        
        # Body
        if 'NanumGothic' in pdf.fonts:
             pdf.set_font("NanumGothic", size=10)
        else:
             pdf.set_font("Helvetica", size=10)
            
        pdf.multi_cell(0, 10, txt=str(analysis_data))
        
        filename = f"{ticker}_report.pdf"
        output_path = os.path.join("services", filename) 
        pdf.output(output_path)
        
        return output_path

pdf_service = PDFService()
