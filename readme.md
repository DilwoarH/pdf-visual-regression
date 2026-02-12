# PDF Visual Regression Tester

This project provides a Python script for performing visual regression testing on PDF files. It compares two PDFs page by page and generates images that highlight any visual differences found.

## Features

-   **Page-by-Page Comparison**: Compares each corresponding page of two PDF files.
-   **Difference Highlighting**: Generates "diff" images that visually mark the areas where differences were detected.
-   **Command-Line Interface**: Easy to use from the terminal with simple arguments.
-   **Handles Page Count Mismatches**: Provides a warning if the PDFs have a different number of pages and compares up to the length of the shorter document.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd pdf-visual-regression
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

The main script is `pdf_visual_diff.py`. You can run it from the command line, providing the paths to the two PDF files you want to compare.

### Command

```bash
python pdf_visual_diff.py <path/to/pdf1.pdf> <path/to/pdf2.pdf> [options]
```

### Arguments

-   `pdf1`: The path to the first PDF file (e.g., the original or expected version).
-   `pdf2`: The path to the second PDF file (e.g., the new or actual version).
-   `--output` (optional): The directory where the generated diff images will be saved. Defaults to `diff_output`.

### Example

```bash
python pdf_visual_diff.py documents/original.pdf documents/modified.pdf --output diffs
```

If differences are found, the script will print a summary to the console and save the highlighted images in the specified output directory.

## Testing

This project includes a test suite to verify the functionality of the comparison script. A `Makefile` is provided to simplify the testing process.

-   **Run tests:**
    This command will first set up the necessary test PDFs and then execute the unit tests.
    ```bash
    make test
    ```

-   **Clean up:**
    This command will remove all generated files, including test PDFs, test outputs, and cache files.
    ```bash
    make clean
    ```

## How It Works

The script leverages several powerful Python libraries:

-   **PyMuPDF (`fitz`)**: Used for its high-performance rendering of PDF pages into images (pixmaps).
-   **scikit-image**: Provides the `structural_similarity` function, which offers a more robust method for comparing images than simple pixel-by-pixel checks. This helps in reducing false positives from minor, imperceptible rendering variations.
-   **Pillow (PIL)**: Used for image manipulation, such as creating the highlighted diff images and saving them to a file.
-   **ReportLab**: Used in the test suite to programmatically generate PDF files for testing purposes.

## Dependencies

-   `PyMuPDF`
-   `scikit-image`
-   `Pillow`
-   `numpy`
-   `reportlab`
