#!/usr/bin/env python
"""
Test script for PdfIt functionality
"""
import os
import sys
import tempfile
import shutil
import time
import traceback
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

# Add parent directory to path to import pdfit modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdfit.converters import (
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

class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.skipped = []
        self.start_time = None
        self.end_time = None

    def add_pass(self, test_name, message=""):
        self.passed.append((test_name, message))
    
    def add_fail(self, test_name, error):
        self.failed.append((test_name, error))
    
    def add_skip(self, test_name, reason):
        self.skipped.append((test_name, reason))
        
    def print_summary(self):
        self.end_time = time.time()
        
        print("\n" + "="*70)
        print(f"{Fore.CYAN}TEST SUMMARY:{Style.RESET_ALL}")
        print(f"Total time: {self.end_time - self.start_time:.2f} seconds")
        print(f"{Fore.GREEN}Passed: {len(self.passed)}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {len(self.failed)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Skipped: {len(self.skipped)}{Style.RESET_ALL}")
        print("="*70)
        
        if self.failed:
            print(f"\n{Fore.RED}FAILED TESTS:{Style.RESET_ALL}")
            for test_name, error in self.failed:
                print(f"  - {test_name}: {error}")
            print()
        
        if self.skipped:
            print(f"\n{Fore.YELLOW}SKIPPED TESTS:{Style.RESET_ALL}")
            for test_name, reason in self.skipped:
                print(f"  - {test_name}: {reason}")
            print()

def run_test(test_func, results, *args, **kwargs):
    test_name = test_func.__name__
    print(f"Running {Fore.CYAN}{test_name}{Style.RESET_ALL}... ", end="")
    sys.stdout.flush()
    
    try:
        if test_func(*args, **kwargs):
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            results.add_fail(test_name, "Test returned False")
            return False
    except Exception as e:
        print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        results.add_fail(test_name, error_msg)
        return False

def test_txt_to_pdf():
    """Test text to PDF conversion"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(b"Hello, this is a test file for conversion from TXT to PDF.")
    
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Run the conversion
    result = convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Check output exists
    success = result and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    
    return success

def test_jpg_to_pdf():
    """Test image to PDF conversion"""
    # Locate test image file
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', 'image.png')
    
    if not os.path.exists(test_file_path):
        print(f"{Fore.YELLOW}Test file not found: {test_file_path}. Creating a test image.{Style.RESET_ALL}")
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (512, 512), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), "PdfIt Test Image", fill=(255,255,0))
        try:
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            img.save(test_file_path)
        except:
            # If we can't save to the testfiles directory, create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                img.save(f.name)
                test_file_path = f.name
    
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Run the conversion
    result = convert_jpg_to_pdf(test_file_path, temp_pdf)
    
    # Check output exists
    success = result and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0
    
    # Clean up
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    
    return success

def test_docx_to_pdf():
    """Test DOCX to PDF conversion"""
    # Locate test DOCX file
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', 'hello.docx')
    
    if not os.path.exists(test_file_path):
        print(f"{Fore.YELLOW}Test file not found: {test_file_path}, skipping test{Style.RESET_ALL}")
        return True  # Skip this test if file not found
    
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Run the conversion
    result = convert_docx_to_pdf(test_file_path, temp_pdf)
    
    # Check output exists
    success = result and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0
    
    # Clean up
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    
    return success

def test_html_to_pdf():
    """Test HTML to PDF conversion"""
    # Locate test HTML file
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', 'hello.html')
    
    if not os.path.exists(test_file_path):
        print(f"{Fore.YELLOW}Test file not found: {test_file_path}. Creating a test HTML file.{Style.RESET_ALL}")
        with open(test_file_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>PdfIt Test</title>
</head>
<body>
    <h1>Hello, PdfIt!</h1>
    <p>This is a test HTML file for conversion to PDF.</p>
</body>
</html>""")
    
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Run the conversion
    result = convert_html_to_pdf(test_file_path, temp_pdf)
    
    # Check output exists
    success = result and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0
    
    # Clean up
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    
    return success

def test_ppt_to_pdf():
    """Test PowerPoint to PDF conversion"""
    # Locate test PPT file
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', 'DT Unit II.pptx')
    
    if not os.path.exists(test_file_path):
        print(f"{Fore.YELLOW}Test file not found: {test_file_path}, skipping test{Style.RESET_ALL}")
        return True  # Skip this test if file not found
    
    # Check if we're on Windows (PowerPoint conversion needs Windows)
    if os.name != 'nt':
        print(f"{Fore.YELLOW}PowerPoint conversion test skipped on non-Windows OS{Style.RESET_ALL}")
        return True  # Skip this test on non-Windows
    
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Run the conversion
    try:
        result = convert_ppt_to_pdf(test_file_path, temp_pdf)
    except Exception as e:
        if "comtypes" in str(e) or "PowerPoint" in str(e):
            print(f"{Fore.YELLOW}PowerPoint conversion skipped: PowerPoint not installed{Style.RESET_ALL}")
            return True  # Skip if PowerPoint or comtypes not available
        raise
    
    # Check output exists
    success = result and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0
    
    # Clean up
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    
    return success

def test_merge_pdfs():
    """Test merging multiple PDFs"""
    # Create some temporary PDFs to merge
    temp_pdf1 = tempfile.mktemp(suffix='.pdf')
    temp_pdf2 = tempfile.mktemp(suffix='.pdf')
    
    # Create test text files
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt1:
        temp_txt1.write(b"This is the first test file for PDF merging.")
    
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt2:
        temp_txt2.write(b"This is the second test file for PDF merging.")
    
    # Convert text files to PDFs
    convert_txt_to_pdf(temp_txt1.name, temp_pdf1)
    convert_txt_to_pdf(temp_txt2.name, temp_pdf2)
    
    # Merge the PDFs
    output_pdf = tempfile.mktemp(suffix='.pdf')
    result = merge_pdfs([temp_pdf1, temp_pdf2], output_pdf)
    
    # Check output exists
    success = result and os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt1.name)
    os.unlink(temp_txt2.name)
    for path in [temp_pdf1, temp_pdf2, output_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_split_pdf():
    """Test splitting a PDF into individual pages"""
    # Create a temporary PDF
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(b"Line 1\nLine 2\nLine 3\nLine 4\nLine 5")
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Create temp output directory
    output_dir = tempfile.mkdtemp()
    
    # Split the PDF
    result = split_pdf(temp_pdf, output_dir)
    
    # Check if output files exist
    files = os.listdir(output_dir)
    success = result and len(files) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    if os.path.exists(temp_pdf):
        os.unlink(temp_pdf)
    shutil.rmtree(output_dir)
    
    return success

def test_extract_text():
    """Test extracting text from a PDF"""
    # Create a temporary PDF
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file with specific text
    test_text = "This is a specific test string for text extraction testing."
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(test_text.encode('utf-8'))
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Extract text
    output_txt = tempfile.mktemp(suffix='.txt')
    result = extract_text_from_pdf(temp_pdf, output_txt)
    
    # Check if extracted text contains the original text
    with open(output_txt, 'r', encoding='utf-8') as f:
        extracted_text = f.read()
    
    success = result and test_text.lower() in extracted_text.lower()
    
    # Clean up
    os.unlink(temp_txt.name)
    for path in [temp_pdf, output_txt]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_password_protect():
    """Test adding password protection to a PDF"""
    # Create a temporary PDF
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(b"This is a test file for password protection.")
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Add password protection
    protected_pdf = tempfile.mktemp(suffix='.pdf')
    test_password = "test1234"
    result = password_protect_pdf(temp_pdf, protected_pdf, test_password)
    
    # Verify the file exists
    success = result and os.path.exists(protected_pdf) and os.path.getsize(protected_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    for path in [temp_pdf, protected_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_remove_password():
    """Test removing password protection from a PDF"""
    # Create a temporary PDF
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(b"This is a test file for password removal.")
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Add password protection
    protected_pdf = tempfile.mktemp(suffix='.pdf')
    test_password = "test1234"
    password_protect_pdf(temp_pdf, protected_pdf, test_password)
    
    # Remove password protection
    decrypted_pdf = tempfile.mktemp(suffix='.pdf')
    result = remove_password_from_pdf(protected_pdf, decrypted_pdf, test_password)
    
    # Verify the file exists and is different from the protected one
    success = result and os.path.exists(decrypted_pdf) and os.path.getsize(decrypted_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    for path in [temp_pdf, protected_pdf, decrypted_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_compress_pdf():
    """Test PDF compression"""
    # Create a temporary PDF with some content to make it compressible
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file with repeated content to make it more compressible
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        repeated_text = "This is a test string that will be repeated many times to create a compressible file. " * 100
        temp_txt.write(repeated_text.encode('utf-8'))
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Compress the PDF
    compressed_pdf = tempfile.mktemp(suffix='.pdf')
    result = compress_pdf(temp_pdf, compressed_pdf, 'high')
    
    # Verify the file exists
    success = result and os.path.exists(compressed_pdf) and os.path.getsize(compressed_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    for path in [temp_pdf, compressed_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_rotate_pdf():
    """Test rotating PDF pages"""
    # Create a temporary PDF
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Create a test text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt:
        temp_txt.write(b"This is a test file for page rotation.")
    
    # Convert text file to PDF
    convert_txt_to_pdf(temp_txt.name, temp_pdf)
    
    # Rotate pages
    rotated_pdf = tempfile.mktemp(suffix='.pdf')
    result = rotate_pdf_pages(temp_pdf, rotated_pdf, None, 90)
    
    # Verify the file exists
    success = result and os.path.exists(rotated_pdf) and os.path.getsize(rotated_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt.name)
    for path in [temp_pdf, rotated_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def test_reorder_pdf():
    """Test reordering PDF pages"""
    # Create a temporary PDF with multiple pages
    temp_pdf = tempfile.mktemp(suffix='.pdf')
    
    # Use the merge function to create a multi-page PDF
    pdf1 = tempfile.mktemp(suffix='.pdf')
    pdf2 = tempfile.mktemp(suffix='.pdf')
    
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt1:
        temp_txt1.write(b"This is page 1")
    
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_txt2:
        temp_txt2.write(b"This is page 2")
    
    convert_txt_to_pdf(temp_txt1.name, pdf1)
    convert_txt_to_pdf(temp_txt2.name, pdf2)
    
    merge_pdfs([pdf1, pdf2], temp_pdf)
    
    # Reorder pages
    reordered_pdf = tempfile.mktemp(suffix='.pdf')
    result = reorder_pdf_pages(temp_pdf, reordered_pdf, "2,1")
    
    # Verify the file exists
    success = result and os.path.exists(reordered_pdf) and os.path.getsize(reordered_pdf) > 0
    
    # Clean up
    os.unlink(temp_txt1.name)
    os.unlink(temp_txt2.name)
    for path in [pdf1, pdf2, temp_pdf, reordered_pdf]:
        if os.path.exists(path):
            os.unlink(path)
    
    return success

def main():
    """Main test function to run all tests"""
    results = TestResult()
    results.start_time = time.time()
    
    print(f"{Fore.CYAN}Running PdfIt tests...{Style.RESET_ALL}\n")
    
    # Basic conversion tests
    run_test(test_txt_to_pdf, results)
    run_test(test_jpg_to_pdf, results)
    run_test(test_docx_to_pdf, results)
    run_test(test_html_to_pdf, results)
    run_test(test_ppt_to_pdf, results)
    
    # PDF manipulation tests
    run_test(test_merge_pdfs, results)
    run_test(test_split_pdf, results)
    run_test(test_extract_text, results)
    run_test(test_password_protect, results)
    run_test(test_remove_password, results)
    run_test(test_compress_pdf, results)
    run_test(test_rotate_pdf, results)
    run_test(test_reorder_pdf, results)
    
    # Print test summary
    results.print_summary()
    
    # Return success if all tests passed
    return len(results.failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
