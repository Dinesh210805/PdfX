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

## Installation

You can install PdfX using pip:

```bash
pip install pdfx
```

### Dependencies

PdfX depends on the following packages, which are automatically installed:

- fpdf (for text to PDF conversion)
- Pillow (for image handling)
- python-docx (for Word document processing)
- reportlab (for PDF generation)
- PyPDF2 (for PDF manipulation)
- pdfkit (for HTML to PDF conversion)
- colorama (for colored terminal output)
- tabulate (for formatted table display)
- comtypes (for PowerPoint conversion, Windows only)

### Additional Requirements

For HTML to PDF conversion, you'll need wkhtmltopdf installed on your system:

- Windows: Download from [wkhtmltopdf website](https://wkhtmltopdf.org/downloads.html)
- macOS: `brew install wkhtmltopdf`
- Linux: `sudo apt-get install wkhtmltopdf` (Ubuntu/Debian) or equivalent for your distro

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
