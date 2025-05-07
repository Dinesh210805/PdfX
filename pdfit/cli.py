"""
Command Line Interface for PdfIt
"""
import os
import sys
import time
import threading
import itertools
import colorama
from colorama import Fore, Style, Back
from PyPDF2 import PdfReader

from pdfit.utils import (
    print_banner, 
    print_menu, 
    get_input_files,
    list_files_in_directory, 
    display_files
)
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

# Initialize colorama
colorama.init()

def spinner_animation(done_event, message="Processing"):
    """Display a retro hacker-style animation while a task is running"""
    spinners = ['|', '/', '-', '\\']
    progress_chars = ['.'] * 10
    progress_idx = 0
    i = 0
    
    while not done_event.is_set():
        # Update progress display
        if progress_idx < len(progress_chars):
            progress_chars[progress_idx] = '█'
            progress_idx = (progress_idx + 1) % len(progress_chars)
            
        spinner = spinners[i % len(spinners)]
        progress_bar = ''.join(progress_chars)
        sys.stdout.write(f"\r{Fore.CYAN}{message} {spinner} [{progress_bar}]{Style.RESET_ALL}")
        sys.stdout.flush()
        
        # Reset progress bar if all filled
        if progress_idx == 0:
            progress_chars = ['.'] * 10
            
        time.sleep(0.1)
        i += 1
    
    # Clear the animation line
    sys.stdout.write("\r" + " " * (len(message) + 20) + "\r")
    sys.stdout.flush()

def startup_animation():
    """Display a cool retro-style boot-up animation"""
    colorama.init()  # Initialize colorama
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    
    lines = [
        f"{Fore.CYAN}Initializing PdfIt Conversion System...{Style.RESET_ALL}",
        f"{Fore.CYAN}Loading conversion modules...{Style.RESET_ALL}",
        f"{Fore.CYAN}Checking system compatibility...{Style.RESET_ALL}",
        f"{Fore.CYAN}Starting user interface...{Style.RESET_ALL}"
    ]
    
    for line in lines:
        print(line)
        time.sleep(0.3)
        
    print(f"{Fore.GREEN}System ready.{Style.RESET_ALL}")
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal again

def run_with_spinner(func, message="Processing", *args, **kwargs):
    """Run a function with a spinner animation"""
    done_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(done_event, message))
    spinner_thread.start()
    
    try:
        result = func(*args, **kwargs)
    finally:
        done_event.set()
        spinner_thread.join()
    
    return result

def run_pdfit():
    """Main function for the PdfIt CLI"""
    startup_animation()
    while True:
        print_banner()
        print_menu()
        
        choice = input(f"\n{Fore.CYAN}Please enter your choice (1-13, or q to quit): {Style.RESET_ALL}")
        
        if choice.lower() == 'q':
            print(f"\n{Fore.GREEN}Thank you for using PdfIt! Goodbye!{Style.RESET_ALL}")
            break
            
        try:
            choice = int(choice)
            if choice < 1 or choice > 13:
                print(f"\n{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                time.sleep(1.5)
                continue
        except ValueError:
            print(f"\n{Fore.RED}Invalid input. Please enter a number between 1-13 or 'q'.{Style.RESET_ALL}")
            time.sleep(1.5)
            continue
            
        # Process user choice
        if choice == 1:  # TXT to PDF
            print(f"\n{Fore.YELLOW}=== Convert Text to PDF ==={Style.RESET_ALL}")
            
            # Get text files in current directory
            files = list_files_in_directory('.', '.txt')
            if not files:
                print(f"{Fore.RED}No text files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a text file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Convert the file
                success = run_with_spinner(convert_txt_to_pdf, "Converting text to PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}Text file converted successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to convert text file.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 2:  # Image to PDF
            print(f"\n{Fore.YELLOW}=== Convert Image to PDF ==={Style.RESET_ALL}")
            
            # Get image files in current directory
            image_exts = ['.jpg', '.jpeg', '.png', '.bmp']
            files = []
            for ext in image_exts:
                files.extend(list_files_in_directory('.', ext))
                
            if not files:
                print(f"{Fore.RED}No image files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to an image file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Convert the file
                success = run_with_spinner(convert_jpg_to_pdf, "Converting image to PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}Image converted successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to convert image.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
        elif choice == 3:  # DOCX to PDF
            print(f"\n{Fore.YELLOW}=== Convert Word Document to PDF ==={Style.RESET_ALL}")
            
            # Get document files in current directory
            doc_exts = ['.docx', '.doc']
            files = []
            for ext in doc_exts:
                files.extend(list_files_in_directory('.', ext))
                
            if not files:
                print(f"{Fore.RED}No Word documents found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a Word document: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Convert the file
                success = run_with_spinner(convert_docx_to_pdf, "Converting Word document to PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}Document converted successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to convert document.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 4:  # HTML to PDF
            print(f"\n{Fore.YELLOW}=== Convert HTML to PDF ==={Style.RESET_ALL}")
            
            # Get HTML files in current directory
            html_exts = ['.html', '.htm']
            files = []
            for ext in html_exts:
                files.extend(list_files_in_directory('.', ext))
                
            if not files:
                print(f"{Fore.RED}No HTML files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to an HTML file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Convert the file
                success = run_with_spinner(convert_html_to_pdf, "Converting HTML to PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}HTML converted successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to convert HTML.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 5:  # PPT to PDF
            print(f"\n{Fore.YELLOW}=== Convert PowerPoint to PDF ==={Style.RESET_ALL}")
            
            # Get presentation files in current directory
            ppt_exts = ['.pptx', '.ppt']
            files = []
            for ext in ppt_exts:
                files.extend(list_files_in_directory('.', ext))
                
            if not files:
                print(f"{Fore.RED}No PowerPoint presentations found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PowerPoint presentation: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Convert the file
                success = run_with_spinner(convert_ppt_to_pdf, "Converting PowerPoint to PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}Presentation converted successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to convert presentation.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 6:  # Merge PDFs
            print(f"\n{Fore.YELLOW}=== Merge PDF Files ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if len(files) < 2:
                print(f"{Fore.RED}Not enough PDF files found in the current directory (need at least 2).{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selections
            selection = input(f"\n{Fore.CYAN}Enter file numbers separated by commas (e.g., 1,3,5), or 'all' for all files: {Style.RESET_ALL}")
            
            try:
                # Process selection
                if selection.lower() == 'all':
                    selected_files = files
                else:
                    try:
                        indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
                        selected_files = [files[idx] for idx in indices if 0 <= idx < len(files)]
                    except (ValueError, IndexError):
                        print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                
                if len(selected_files) < 2:
                    print(f"{Fore.RED}Please select at least 2 PDF files to merge.{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get output file path
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for merged.pdf): {Style.RESET_ALL}")
                if not output_file:
                    output_file = 'merged.pdf'
                
                # Convert the file
                input_paths = [os.path.abspath(f) for f in selected_files]
                success = run_with_spinner(merge_pdfs, "Merging PDF files", input_paths, output_file)
                
                if success:
                    print(f"{Fore.GREEN}PDFs merged successfully! Output saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to merge PDFs.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
        elif choice == 7:  # Split PDF
            print(f"\n{Fore.YELLOW}=== Split PDF into Pages ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get page count
                try:
                    reader = PdfReader(input_file)
                    page_count = len(reader.pages)
                    print(f"{Fore.CYAN}The PDF has {page_count} pages.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error reading PDF: {str(e)}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output directory
                output_dir = input(f"{Fore.CYAN}Enter output directory (or press Enter for current directory): {Style.RESET_ALL}")
                if not output_dir:
                    output_dir = os.path.dirname(os.path.abspath(input_file))
                elif not os.path.exists(output_dir):
                    try:
                        os.makedirs(output_dir)
                    except Exception as e:
                        print(f"{Fore.RED}Error creating directory: {str(e)}{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                
                # Split the PDF
                success = run_with_spinner(split_pdf, "Splitting PDF", input_file, output_dir)
                
                if success:
                    print(f"{Fore.GREEN}PDF split successfully! Pages saved to: {output_dir}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to split PDF.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 8:  # Extract Text
            print(f"\n{Fore.YELLOW}=== Extract Text from PDF ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '.txt'
                output_file = input(f"{Fore.CYAN}Enter output text file path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Extract text
                success = run_with_spinner(extract_text_from_pdf, "Extracting text from PDF", input_file, output_file)
                
                if success:
                    print(f"{Fore.GREEN}Text extracted successfully! Saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to extract text.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        # Add Password Protection
        elif choice == 9:  # Password Protection
            print(f"\n{Fore.YELLOW}=== Add Password Protection to PDF ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get password
                password = input(f"{Fore.CYAN}Enter password for protection: {Style.RESET_ALL}")
                if not password:
                    print(f"{Fore.RED}Password cannot be empty.{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get owner password (optional)
                owner_pw = input(f"{Fore.CYAN}Enter owner password (or press Enter to use the same password): {Style.RESET_ALL}")
                if not owner_pw:
                    owner_pw = None
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '_protected.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Add password protection
                success = run_with_spinner(
                    password_protect_pdf, 
                    "Adding password protection", 
                    input_file, output_file, password, owner_pw
                )
                
                if success:
                    print(f"{Fore.GREEN}Password protection added successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to add password protection.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
        # Remove Password Protection
        elif choice == 10:  # Remove Password Protection
            print(f"\n{Fore.YELLOW}=== Remove Password Protection from PDF ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a password-protected PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Check if the PDF is encrypted
                try:
                    reader = PdfReader(input_file)
                    if not reader.is_encrypted:
                        print(f"{Fore.YELLOW}The selected PDF is not encrypted.{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                except Exception:
                    # If we get an exception here, it might be because the PDF is encrypted
                    pass
                
                # Get password
                password = input(f"{Fore.CYAN}Enter the PDF password: {Style.RESET_ALL}")
                if not password:
                    print(f"{Fore.RED}Password cannot be empty.{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '_decrypted.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Remove password protection
                success = run_with_spinner(
                    remove_password_from_pdf, 
                    "Removing password protection", 
                    input_file, output_file, password
                )
                
                if success:
                    print(f"{Fore.GREEN}Password protection removed successfully! PDF saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to remove password protection. Is the password correct?{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
        elif choice == 11:  # Compress PDF
            print(f"\n{Fore.YELLOW}=== Compress PDF File ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file to compress: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get compression level
                print(f"\n{Fore.CYAN}Compression quality levels:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}1. Low compression (better quality){Style.RESET_ALL}")
                print(f"{Fore.WHITE}2. Medium compression (balanced){Style.RESET_ALL}")
                print(f"{Fore.WHITE}3. High compression (smaller file size){Style.RESET_ALL}")
                
                quality_choice = input(f"{Fore.CYAN}Select compression quality (1-3, default is 2): {Style.RESET_ALL}")
                
                # Map user choice to quality setting
                quality_map = {
                    '1': 'low',
                    '2': 'medium',
                    '3': 'high'
                }
                
                quality = quality_map.get(quality_choice, 'medium')
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '_compressed.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Compress PDF
                success = run_with_spinner(
                    compress_pdf, 
                    "Compressing PDF", 
                    input_file, output_file, quality
                )
                
                if success:
                    original_size = os.path.getsize(input_file)
                    compressed_size = os.path.getsize(output_file)
                    
                    print(f"{Fore.GREEN}PDF compressed successfully! Saved to: {output_file}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Original size: {original_size / 1024:.1f} KB{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Compressed size: {compressed_size / 1024:.1f} KB{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Reduction: {(1 - compressed_size / original_size) * 100:.1f}%{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to compress PDF.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
        elif choice == 12:  # Rotate PDF Pages
            print(f"\n{Fore.YELLOW}=== Rotate PDF Pages ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get page count
                try:
                    reader = PdfReader(input_file)
                    page_count = len(reader.pages)
                    print(f"{Fore.CYAN}The PDF has {page_count} pages.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error reading PDF: {str(e)}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get pages to rotate
                pages_input = input(f"{Fore.CYAN}Enter pages to rotate (e.g., 1,3-5,7 or 'all' for all pages): {Style.RESET_ALL}")
                
                if pages_input.lower() == 'all':
                    pages = None  # Will rotate all pages
                else:
                    pages = pages_input
                
                # Get rotation angle
                print(f"\n{Fore.CYAN}Rotation angles:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}1. 90° clockwise{Style.RESET_ALL}")
                print(f"{Fore.WHITE}2. 180° (upside down){Style.RESET_ALL}")
                print(f"{Fore.WHITE}3. 270° clockwise (90° counter-clockwise){Style.RESET_ALL}")
                
                angle_choice = input(f"{Fore.CYAN}Select rotation angle (1-3, default is 1): {Style.RESET_ALL}")
                
                # Map user choice to angle
                angle_map = {
                    '1': 90,
                    '2': 180,
                    '3': 270
                }
                
                angle = angle_map.get(angle_choice, 90)
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '_rotated.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Rotate pages
                success = run_with_spinner(
                    rotate_pdf_pages, 
                    "Rotating PDF pages", 
                    input_file, output_file, pages, angle
                )
                
                if success:
                    print(f"{Fore.GREEN}PDF pages rotated successfully! Saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to rotate PDF pages.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == 13:  # Reorder PDF Pages
            print(f"\n{Fore.YELLOW}=== Reorder PDF Pages ==={Style.RESET_ALL}")
            
            # Get PDF files in current directory
            files = list_files_in_directory('.', '.pdf')
            
            if not files:
                print(f"{Fore.RED}No PDF files found in the current directory.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                continue
                
            # Display files
            display_files(files)
            
            # Get user selection
            selection = input(f"\n{Fore.CYAN}Enter file number, or path to a PDF file: {Style.RESET_ALL}")
            
            try:
                if selection.isdigit() and int(selection) <= len(files):
                    input_file = files[int(selection)-1]
                else:
                    input_file = selection
                
                if not os.path.exists(input_file):
                    print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get page count
                try:
                    reader = PdfReader(input_file)
                    page_count = len(reader.pages)
                    print(f"{Fore.CYAN}The PDF has {page_count} pages.{Style.RESET_ALL}")
                    
                    # Print current page order
                    print(f"{Fore.CYAN}Current page order: {','.join([str(i+1) for i in range(page_count)])}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error reading PDF: {str(e)}{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                    
                # Get new page order
                page_order = input(f"{Fore.CYAN}Enter new page order (e.g., 3,1,2 for a 3-page document): {Style.RESET_ALL}")
                
                # Validate page order
                try:
                    page_numbers = [int(p) for p in page_order.split(',')]
                    if len(page_numbers) != page_count:
                        print(f"{Fore.RED}Error: You must specify exactly {page_count} pages.{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                        
                    for p in page_numbers:
                        if p < 1 or p > page_count:
                            print(f"{Fore.RED}Error: Page number {p} out of range (1-{page_count}).{Style.RESET_ALL}")
                            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                            continue
                except ValueError:
                    print(f"{Fore.RED}Error: Invalid page numbers.{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    continue
                
                # Get output file path
                default_output = os.path.splitext(input_file)[0] + '_reordered.pdf'
                output_file = input(f"{Fore.CYAN}Enter output PDF path (or press Enter for {default_output}): {Style.RESET_ALL}")
                if not output_file:
                    output_file = default_output
                
                # Reorder pages
                success = run_with_spinner(
                    reorder_pdf_pages, 
                    "Reordering PDF pages", 
                    input_file, output_file, page_order
                )
                
                if success:
                    print(f"{Fore.GREEN}PDF pages reordered successfully! Saved to: {output_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to reorder PDF pages.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    run_pdfit()
