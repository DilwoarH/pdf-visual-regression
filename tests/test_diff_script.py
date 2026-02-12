import unittest
import os
import subprocess

class TestPdfVisualDiff(unittest.TestCase):

    def setUp(self):
        """
        Set up test files before each test.
        """
        if not os.path.exists("tests/test_pdfs"):
            subprocess.run(["python", "tests/create_test_pdfs.py"], capture_output=True, text=True)

    def test_identical_pdfs(self):
        """
        Test that identical PDFs produce no differences.
        """
        pdf1 = "tests/test_pdfs/test1_original.pdf"
        pdf2 = "tests/test_pdfs/test1_identical.pdf"
        output_dir = "tests/test_output/identical"
        
        result = subprocess.run(["python", "pdf_visual_diff.py", pdf1, pdf2, "--output", output_dir], capture_output=True, text=True)
        
        self.assertIn("All pages are visually identical.", result.stdout)
        self.assertFalse(os.path.exists(output_dir) and os.listdir(output_dir))

    def test_different_text_pdfs(self):
        """
        Test that PDFs with different text produce differences.
        """
        pdf1 = "tests/test_pdfs/test1_original.pdf"
        pdf2 = "tests/test_pdfs/test2_different_text.pdf"
        output_dir = "tests/test_output/different_text"

        result = subprocess.run(["python", "pdf_visual_diff.py", pdf1, pdf2, "--output", output_dir], capture_output=True, text=True)

        self.assertIn("Visual differences found on pages: 1", result.stdout)
        self.assertTrue(os.path.exists(os.path.join(output_dir, "diff_page_1.png")))

    def test_different_page_count_pdfs(self):
        """
        Test that PDFs with different page counts are handled correctly.
        """
        pdf1 = "tests/test_pdfs/test1_original.pdf"
        pdf2 = "tests/test_pdfs/test3_different_pages.pdf"
        output_dir = "tests/test_output/different_pages"

        result = subprocess.run(["python", "pdf_visual_diff.py", pdf1, pdf2, "--output", output_dir], capture_output=True, text=True)

        self.assertIn("Warning: PDFs have different page counts.", result.stdout)
        # No diffs should be reported as we only compare up to the shortest PDF
        self.assertIn("All pages are visually identical.", result.stdout)
        self.assertFalse(os.path.exists(output_dir) and os.listdir(output_dir))

if __name__ == '__main__':
    unittest.main()
