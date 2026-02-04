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
            # DEBUG: Raise error immediately to show user where we looked
            error_msg = f"FONT FILE NOT FOUND. Checked path: {font_path}. Files depends on: {base_dir}"
            print(error_msg)
            # Check what IS there
            try:
                static_fonts = os.path.join(base_dir, 'static', 'fonts')
                files = os.listdir(static_fonts)
                error_msg += f" | Existing files in {static_fonts}: {files}"
            except Exception as e:
                error_msg += f" | Could not list dir: {e}"
            
            raise FileNotFoundError(error_msg)

        # Title
        pdf.cell(200, 10, txt=f"InsightPulse Report: {ticker}", ln=True, align='C')
        
        # Body
        pdf.set_font("NanumGothic", size=10)
        pdf.multi_cell(0, 10, txt=str(analysis_data))
        
        filename = f"{ticker}_report.pdf"
        output_path = os.path.join("services", filename) 
        pdf.output(output_path)
        
        return output_path

pdf_service = PDFService()
