#!/usr/bin/env python
"""
Test script for PdfX functionality
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

# Add parent directory to path to import pdfx modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdfx.converters import (
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
    
    def start(self):
        self.start_time = time.time()
    
    def finish(self):
        self.end_time = time.time()
    
    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def print_summary(self):
        print("\n" + "="*80)
        print(f"{Fore.CYAN}TEST RESULTS SUMMARY{Style.RESET_ALL}")
        print("="*80)
        
        total = len(self.passed) + len(self.failed) + len(self.skipped)
        print(f"Total tests: {total}")
        print(f"{Fore.GREEN}Passed: {len(self.passed)}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {len(self.failed)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Skipped: {len(self.skipped)}{Style.RESET_ALL}")
        print(f"Time elapsed: {self.get_duration():.2f} seconds")
        
        if self.failed:
            print("\n" + "="*80)
            print(f"{Fore.RED}FAILED TESTS:{Style.RESET_ALL}")
            print("="*80)
            for i, (test_name, error) in enumerate(self.failed, 1):
                print(f"{i}. {Fore.RED}{test_name}{Style.RESET_ALL}")
                print(f"   Error: {error}")
                print()


def test_convert_txt_to_pdf(results):
    """Test converting text file to PDF"""
    test_name = "TXT to PDF conversion"
    print(f"\n== Testing {test_name} ==")
    
    try:
        input_path = "test.txt"
        if not os.path.exists(input_path):
            with open(input_path, "w") as f:
                f.write("This is a test text file\nWith multiple lines\nFor testing PdfX functionality")
        
        output_path = "test_output.pdf"
        result = convert_txt_to_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Converted text to PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Conversion failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_convert_jpg_to_pdf(results):
    """Test converting image to PDF"""
    test_name = "Image to PDF conversion"
    print(f"\n== Testing {test_name} ==")
    
    try:
        input_path = "image.png"
        if not os.path.exists(input_path):
            print(f"{Fore.YELLOW}⚠ Test file {input_path} not found, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, f"Test file {input_path} not found")
            return None
            
        output_path = "image_output.pdf"
        result = convert_jpg_to_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Converted image to PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Conversion failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_convert_docx_to_pdf(results):
    """Test converting DOCX to PDF"""
    test_name = "DOCX to PDF conversion"
    print(f"\n== Testing {test_name} ==")
    
    try:
        input_path = "sample.docx"
        if not os.path.exists(input_path):
            print(f"{Fore.YELLOW}⚠ Test file {input_path} not found, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, f"Test file {input_path} not found")
            return None
            
        output_path = "docx_output.pdf"
        result = convert_docx_to_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Converted DOCX to PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Conversion failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_convert_html_to_pdf(results):
    """Test converting HTML to PDF"""
    test_name = "HTML to PDF conversion"
    print(f"\n== Testing {test_name} ==")
    
    try:
        input_path = "hello.html"
        if not os.path.exists(input_path):
            print(f"{Fore.YELLOW}⚠ Test file {input_path} not found, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, f"Test file {input_path} not found")
            return None
            
        output_path = "html_output.pdf"
        result = convert_html_to_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Converted HTML to PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Conversion failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_convert_ppt_to_pdf(results):
    """Test converting PPT to PDF"""
    test_name = "PPT to PDF conversion"
    print(f"\n== Testing {test_name} ==")
    
    try:
        input_path = "DT Unit II.pptx"
        if not os.path.exists(input_path):
            print(f"{Fore.YELLOW}⚠ Test file {input_path} not found, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, f"Test file {input_path} not found")
            return None
            
        output_path = "ppt_output.pdf"
        result = convert_ppt_to_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Converted PPT to PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Conversion failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_merge_pdfs(results):
    """Test merging PDFs"""
    test_name = "PDF merging"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if len(pdf_files) < 2:
            print(f"{Fore.YELLOW}⚠ Not enough PDF files for testing merge, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "Not enough PDF files for testing merge")
            return None
        
        input_paths = [os.path.abspath(pdf_files[0]), os.path.abspath(pdf_files[1])]
        output_path = "merged_test.pdf"
        result = merge_pdfs(input_paths, output_path)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Merged PDFs{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Merge failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_split_pdf(results):
    """Test splitting a PDF into pages"""
    test_name = "PDF splitting"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing split, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        input_path = os.path.abspath(pdf_files[0])
        output_dir = tempfile.mkdtemp()
        result = split_pdf(input_path, output_dir)
        
        file_count = len([f for f in os.listdir(output_dir) if f.endswith('.pdf')])
        if result and file_count > 0:
            print(f"{Fore.GREEN}✓ Success: Split PDF into {file_count} files{Style.RESET_ALL}")
            results.add_pass(test_name, f"Created {file_count} files")
            shutil.rmtree(output_dir)
            return True
        else:
            shutil.rmtree(output_dir)
            error = "Split failed or no output files created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_extract_text(results):
    """Test extracting text from PDF"""
    test_name = "Text extraction from PDF"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing text extraction, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        input_path = os.path.abspath(pdf_files[0])
        output_path = "extracted_text.txt"
        result = extract_text_from_pdf(input_path, output_path)
        
        if result and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"{Fore.GREEN}✓ Success: Extracted text from PDF{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Text extraction failed or output file empty"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_password_protection(results):
    """Test password protection and removal"""
    test_name = "PDF password protection"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and not f.endswith('_protected.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing password protection, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        input_path = os.path.abspath(pdf_files[0])
        protected_path = "test_protected.pdf"
        decrypted_path = "test_decrypted.pdf"
        password = "testpassword123"
        
        # Add password
        protect_result = password_protect_pdf(input_path, protected_path, password)
        
        if not protect_result or not os.path.exists(protected_path):
            error = "Failed to apply password protection"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
        
        # Remove password
        decrypt_result = remove_password_from_pdf(protected_path, decrypted_path, password)
        
        if decrypt_result and os.path.exists(decrypted_path):
            print(f"{Fore.GREEN}✓ Success: Added and removed password{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Failed to remove password"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_rotate_pages(results):
    """Test rotating PDF pages"""
    test_name = "PDF page rotation"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing page rotation, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        input_path = os.path.abspath(pdf_files[0])
        output_path = "test_rotated.pdf"
        result = rotate_pdf_pages(input_path, output_path, pages="1", angle=90)
        
        if result and os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Success: Rotated PDF pages{Style.RESET_ALL}")
            results.add_pass(test_name)
            return True
        else:
            error = "Page rotation failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_reorder_pages(results):
    """Test reordering PDF pages"""
    test_name = "PDF page reordering"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and not f.endswith('_protected.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing page reordering, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        from PyPDF2 import PdfReader
        
        # Find a PDF with at least 2 pages
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                
                # Check if file is encrypted
                if reader.is_encrypted:
                    continue
                    
                if len(reader.pages) >= 2:
                    input_path = os.path.abspath(pdf_file)
                    output_path = "test_reordered.pdf"
                    # Reverse page order
                    page_order = ",".join([str(i) for i in range(len(reader.pages), 0, -1)])
                    result = reorder_pdf_pages(input_path, output_path, page_order)
                    
                    if result and os.path.exists(output_path):
                        print(f"{Fore.GREEN}✓ Success: Reordered PDF pages{Style.RESET_ALL}")
                        results.add_pass(test_name)
                        return True
                    else:
                        error = "Page reordering failed or output file not created"
                        print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
                        results.add_fail(test_name, error)
                        return False
            except Exception:
                continue
                
        print(f"{Fore.YELLOW}⚠ No suitable multi-page PDF files for testing page reordering, skipping test{Style.RESET_ALL}")
        results.add_skip(test_name, "No suitable multi-page PDF files available")
        return None
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def test_compress_pdf(results):
    """Test PDF compression"""
    test_name = "PDF compression"
    print(f"\n== Testing {test_name} ==")
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and not f.endswith('_compressed.pdf')]
        if not pdf_files:
            print(f"{Fore.YELLOW}⚠ No PDF files for testing compression, skipping test{Style.RESET_ALL}")
            results.add_skip(test_name, "No PDF files available")
            return None
            
        input_path = os.path.abspath(pdf_files[0])
        output_path = "test_compressed.pdf"
        result = compress_pdf(input_path, output_path, quality='medium')
        
        if result and os.path.exists(output_path):
            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_path)
            print(f"{Fore.GREEN}✓ Success: Compressed PDF{Style.RESET_ALL}")
            print(f"  Original size: {input_size / 1024:.1f} KB, Compressed size: {output_size / 1024:.1f} KB")
            results.add_pass(test_name, f"Reduced from {input_size / 1024:.1f} KB to {output_size / 1024:.1f} KB")
            return True
        else:
            error = "Compression failed or output file not created"
            print(f"{Fore.RED}✗ Failed: {error}{Style.RESET_ALL}")
            results.add_fail(test_name, error)
            return False
    except Exception as e:
        error = str(e)
        print(f"{Fore.RED}✗ Exception: {error}{Style.RESET_ALL}")
        results.add_fail(test_name, f"Exception: {error}\n{traceback.format_exc()}")
        return False


def run_all_tests():
    """Run all available tests"""
    print(f"{Fore.CYAN}========== Running PdfX Functionality Tests =========={Style.RESET_ALL}")
    
    results = TestResult()
    results.start()
    
    # Run tests
    test_convert_txt_to_pdf(results)
    test_convert_jpg_to_pdf(results)
    test_convert_docx_to_pdf(results)
    test_convert_html_to_pdf(results)
    test_convert_ppt_to_pdf(results)
    test_merge_pdfs(results)
    test_split_pdf(results)
    test_extract_text(results)
    test_password_protection(results)
    test_rotate_pages(results)
    test_reorder_pages(results)
    test_compress_pdf(results)
    
    results.finish()
    results.print_summary()

if __name__ == "__main__":
    run_all_tests()
