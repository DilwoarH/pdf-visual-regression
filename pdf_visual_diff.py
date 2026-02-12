import argparse
import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageChops
from skimage.metrics import structural_similarity as ssim
import os

def compare_pdfs(pdf1_path, pdf2_path, output_dir):
    """
    Compares two PDFs page by page for visual differences.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf1 = fitz.open(pdf1_path)
    pdf2 = fitz.open(pdf2_path)

    diff_pages = []

    if len(pdf1) != len(pdf2):
        print(f"Warning: PDFs have different page counts. PDF1: {len(pdf1)} pages, PDF2: {len(pdf2)} pages.")
        print("Comparing up to the lower page count.")

    page_count = min(len(pdf1), len(pdf2))

    for i in range(page_count):
        page1 = pdf1.load_page(i)
        page2 = pdf2.load_page(i)

        img1 = page1.get_pixmap()
        img2 = page2.get_pixmap()

        # Convert to PIL images
        pil_img1 = Image.frombytes("RGB", [img1.width, img1.height], img1.samples)
        pil_img2 = Image.frombytes("RGB", [img2.width, img2.height], img2.samples)

        # Convert to numpy arrays for ssim
        np_img1 = np.array(pil_img1)
        np_img2 = np.array(pil_img2)

        # Compute SSIM
        similarity, diff_img = ssim(np_img1, np_img2, full=True, multichannel=True)

        if similarity < 1.0:
            diff_pages.append(i + 1)
            
            # Create a visual diff image
            diff_img = (diff_img * 255).astype("uint8")
            diff_pil = Image.fromarray(diff_img)
            
            # To make differences more visible, we can create a blended image
            # Create an image with the differences highlighted in red
            diff_highlight = Image.new("RGB", pil_img1.size, (0, 0, 0))
            
            # Use ImageChops to find the difference
            diff = ImageChops.difference(pil_img1, pil_img2)
            
            # To make the diff more visible, we can threshold it
            # This will make small differences more pronounced
            thresholded_diff = diff.point(lambda p: 255 if p > 20 else 0)
            
            # We need to get the bounding box of the differences
            bbox = thresholded_diff.getbbox()
            
            if bbox:
                # Create a red transparent overlay for the differences
                overlay = Image.new("RGBA", pil_img1.size, (255, 0, 0, 0))
                drawing_layer = Image.new("RGBA", pil_img1.size, (0,0,0,0))
                
                # Paste the thresholded difference onto the drawing layer
                drawing_layer.paste((255,0,0,128), mask=thresholded_diff.convert('L'))
                
                # Composite the drawing layer onto the first image
                highlighted_img = Image.alpha_composite(pil_img1.convert("RGBA"), drawing_layer)
                
                # Save the highlighted image
                highlighted_img.convert("RGB").save(os.path.join(output_dir, f"diff_page_{i+1}.png"))


    pdf1.close()
    pdf2.close()

    if not diff_pages:
        print("All pages are visually identical.")
    else:
        print(f"Visual differences found on pages: {', '.join(map(str, diff_pages))}")

def main():
    parser = argparse.ArgumentParser(description="Compare two PDFs for visual differences.")
    parser.add_argument("pdf1", help="Path to the first PDF file.")
    parser.add_argument("pdf2", help="Path to the second PDF file.")
    parser.add_argument("--output", default="diff_output", help="Directory to save difference images.")
    args = parser.parse_args()

    compare_pdfs(args.pdf1, args.pdf2, args.output)

if __name__ == "__main__":
    main()
