"""
PdfIt - A powerful PDF converter for multiple file types

This package provides tools for converting various file formats to PDF,
as well as manipulating existing PDF files.
"""
__version__ = '0.1.0'

# Import main functions for easier access
from .converters import (
    convert_txt_to_pdf,
    convert_jpg_to_pdf,
    convert_docx_to_pdf,
    convert_html_to_pdf,
    convert_ppt_to_pdf,
    merge_pdfs,
    split_pdf,
    extract_text_from_pdf,
    password_protect_pdf,
    remove_password_from_pdf,
    compress_pdf,
    rotate_pdf_pages,
    reorder_pdf_pages
)

# CLI entry point
from .cli import run_pdfit
