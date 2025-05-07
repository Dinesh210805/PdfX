"""
PdfX - A powerful PDF converter for multiple file types

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

# Check for external dependencies and print informative messages at import time
import importlib.util
import os
import sys
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init()

def _check_external_dependency(name, install_message):
    """Check if an external dependency exists and print message if not"""
    if name in ('wkhtmltopdf', 'gs', 'gswin64c', 'gswin32c'):
        # Check executables in PATH
        executables = [name]
        if name == 'gs' and os.name == 'nt':
            executables = ['gswin64c', 'gswin32c']
            
        for exe in executables:
            if shutil.which(exe) is not None:
                return True
                
        print(f"{Fore.YELLOW}Note: {name} not found. {install_message}{Style.RESET_ALL}")
        return False
    return True

# Check for wkhtmltopdf (needed for HTML conversion)
_check_external_dependency('wkhtmltopdf', 
    "For optimal HTML to PDF conversion, install wkhtmltopdf or use 'pip install \"pdfx[html]\"'")

# Check for Ghostscript (needed for PDF compression)
_check_external_dependency('gs' if os.name != 'nt' else 'gswin64c',
    "For better PDF compression, install Ghostscript")
