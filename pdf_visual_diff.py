import argparse
import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageChops
from skimage.metrics import structural_similarity as ssim
import os

def compare_pdfs(pdf1_path, pdf2_path, output_dir, threshold=0.999):
    """
    Compares two PDFs page by page for visual differences.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf1 = fitz.open(pdf1_path)
    pdf2 = fitz.open(pdf2_path)

    diff_pages = []
    has_printed_warning = False

    if len(pdf1) != len(pdf2):
        print(f"Warning: PDFs have different page counts. PDF1: {len(pdf1)} pages, PDF2: {len(pdf2)} pages.")
        print("Comparing up to the lower page count.")
        has_printed_warning = True

    page_count = min(len(pdf1), len(pdf2))

    for i in range(page_count):
        page1 = pdf1.load_page(i)
        page2 = pdf2.load_page(i)

        # To ensure consistent rendering, let's use a standard DPI
        zoom = 2  # DPI = 144
        mat = fitz.Matrix(zoom, zoom)
        img1 = page1.get_pixmap(matrix=mat)
        img2 = page2.get_pixmap(matrix=mat)

        # Convert to PIL images
        pil_img1 = Image.frombytes("RGB", [img1.width, img1.height], img1.samples)
        pil_img2 = Image.frombytes("RGB", [img2.width, img2.height], img2.samples)

        if pil_img1.size != pil_img2.size:
            # Resize images to be the same size for comparison
            pil_img2 = pil_img2.resize(pil_img1.size, Image.LANCZOS)

        # Convert to numpy arrays for ssim
        np_img1 = np.array(pil_img1)
        np_img2 = np.array(pil_img2)

        # Compute SSIM (channel_axis=-1 for color images, replaces deprecated multichannel parameter)
        similarity = ssim(np_img1, np_img2, channel_axis=-1, data_range=255)

        if similarity < threshold:
            diff_pages.append(i + 1)

            # Use ImageChops to find the difference
            diff = ImageChops.difference(pil_img1, pil_img2)

            # Threshold to make the diff more visible
            thresholded_diff = diff.point(lambda p: 255 if p > 20 else 0)

            if thresholded_diff.getbbox():
                drawing_layer = Image.new("RGBA", pil_img1.size, (0,0,0,0))
                drawing_layer.paste((255,0,0,128), mask=thresholded_diff.convert('L'))
                highlighted_img = Image.alpha_composite(pil_img1.convert("RGBA"), drawing_layer)
                highlighted_img.convert("RGB").save(os.path.join(output_dir, f"diff_page_{i+1}.png"))

    pdf1.close()
    pdf2.close()

    if not diff_pages:
        # If a warning was printed and no diffs were found, the identical message should still be printed
        # for the pages that were compared.
        print("All pages are visually identical.")
    else:
        print(f"Visual differences found on pages: {', '.join(map(str, diff_pages))}")

def main():
    parser = argparse.ArgumentParser(description="Compare two PDFs for visual differences.")
    parser.add_argument("pdf1", help="Path to the first PDF file.")
    parser.add_argument("pdf2", help="Path to the second PDF file.")
    parser.add_argument("--output", default="diff_output", help="Directory to save difference images.")
    parser.add_argument("--threshold", type=float, default=0.999, help="Similarity threshold for SSIM (0.0 to 1.0).")
    args = parser.parse_args()

    compare_pdfs(args.pdf1, args.pdf2, args.output, args.threshold)

if __name__ == "__main__":
    main()
