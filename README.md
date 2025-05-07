# PdfX - A Powerful PDF Converter Tool

PdfX is a versatile command-line tool that allows you to convert various file formats to PDF, merge PDFs, split PDFs into separate pages, and extract text from PDFs. With a user-friendly interface, PdfX makes working with PDF files easier than ever.

## Features

- **Convert various formats to PDF:**

  - Text files (.txt)
  - Images (.jpg, .jpeg, .png)
  - PowerPoint presentations (.ppt, .pptx)
  - Word documents (.doc, .docx)
  - HTML files (.html, .htm)

- **PDF operations:**
  - Merge multiple PDF files into one
  - Split PDF into individual pages
  - Extract text content from PDFs
  - Password protect PDFs
  - Remove password protection
  - Compress PDFs to reduce file size
  - Rotate pages in PDFs
  - Reorder pages in PDFs

## Installation

You can install PdfX using pip:

```bash
pip install pdfx
```

This will automatically install all required Python dependencies.

### Dependencies

PdfX automatically installs the following Python packages:

- fpdf>=1.7.2 (for text to PDF conversion)
- Pillow>=10.0.0 (for image handling)
- python-docx>=0.8.11 (for Word document processing)
- reportlab>=3.6.13 (for PDF generation)
- PyPDF2>=3.0.0 (for PDF manipulation)
- pdfkit>=1.0.0 (for HTML to PDF conversion)
- colorama>=0.4.6 (for colored terminal output)
- tabulate>=0.9.0 (for formatted table display)
- comtypes>=1.1.14 (for PowerPoint conversion, Windows only)
- docx2pdf>=0.1.8 (for better DOCX conversion)

### Optional Dependencies

For optimal performance with certain features, you may need to install some external tools:

#### For HTML to PDF conversion:

Install wkhtmltopdf:
- Windows: Download from [wkhtmltopdf website](https://wkhtmltopdf.org/downloads.html)
- Linux: `sudo apt-get install wkhtmltopdf`
- macOS: `brew install wkhtmltopdf`

Or install the Python package with bundled binary:
```bash
pip install "pdfx[html]"
```

#### For PDF compression:

Install Ghostscript:
- Windows: Download from [Ghostscript website](https://ghostscript.com/releases/)
- Linux: `sudo apt-get install ghostscript`
- macOS: `brew install ghostscript`
- macOS: `brew install wkhtmltopdf`
- Linux: `sudo apt-get install wkhtmltopdf` (Ubuntu/Debian) or equivalent for your distro

For PDF compression, you'll need Ghostscript installed:

- Windows: Download from [Ghostscript website](https://ghostscript.com/releases/)
- macOS: `brew install ghostscript`
- Linux: `sudo apt-get install ghostscript` (Ubuntu/Debian) or equivalent for your distro

## Usage

After installation, you can run PdfX from the command line:

```bash
pdfx
```

This will launch the interactive menu where you can choose your desired operation.

## Examples

### Converting a text file to PDF

1. Run `pdfx`
2. Choose option `1` (Convert TXT to PDF)
3. Select your text file from the list or enter a custom path
4. Choose the output path or use the default

### Merging multiple PDFs

1. Run `pdfx`
2. Choose option `6` (Merge PDFs)
3. Select multiple PDF files by entering comma-separated numbers (e.g., `1,3,5`), or `all` for all PDFs
4. Specify the output file or use the default `merged.pdf`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
