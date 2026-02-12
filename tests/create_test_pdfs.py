import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(filename, text_content):
    """
    Creates a simple PDF for testing purposes.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, text_content)
    c.showPage()
    c.save()

def setup_test_files():
    """
    Creates a set of test PDFs.
    """
    if not os.path.exists("tests/test_pdfs"):
        os.makedirs("tests/test_pdfs")

    # Create two identical PDFs
    create_test_pdf("tests/test_pdfs/test1_original.pdf", "This is a test.")
    create_test_pdf("tests/test_pdfs/test1_identical.pdf", "This is a test.")

    # Create a PDF with a different text
    create_test_pdf("tests/test_pdfs/test2_different_text.pdf", "This is a different test.")

    # Create a PDF with a different number of pages (but first page is identical to test1_original)
    c = canvas.Canvas("tests/test_pdfs/test3_different_pages.pdf", pagesize=letter)
    c.drawString(100, 750, "This is a test.")
    c.showPage()
    c.drawString(100, 750, "Page 2")
    c.showPage()
    c.save()

if __name__ == "__main__":
    setup_test_files()
    print("Test PDF files created in tests/test_pdfs/")
