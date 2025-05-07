"""
Command Line Interface for PdfX
"""
import os
import sys
import time
import threading
import itertools
import colorama
from colorama import Fore, Style, Back
from PyPDF2 import PdfReader

from pdfx.utils import (
    print_banner, 
    print_menu, 
    get_input_files,
    list_files_in_directory, 
    display_files
)
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
        
        # Create progress bar
        progress_bar = ''.join(progress_chars)
        
        # Update spinner
        i = (i + 1) % len(spinners)
        
        # Create output with retro hacker style
        output = f"\r{Fore.WHITE}[{Fore.GREEN}{spinners[i]}{Fore.WHITE}] {Fore.GREEN}{message} {Fore.WHITE}[{Fore.GREEN}{progress_bar}{Fore.WHITE}]{Style.RESET_ALL}"
        
        sys.stdout.write(output)
        sys.stdout.flush()
        time.sleep(0.1)
        
        # Reset progress chars
        if progress_idx == 0:
            progress_chars = ['.'] * 10
    
    # Clear the line when done
    sys.stdout.write("\r" + " " * (len(message) + 30) + "\r")
    sys.stdout.flush()

def progress_bar(progress, total, text="", length=30):
    """Display a retro hacker-style progress bar"""
    filled_len = int(length * progress / total)
    bar = f"{Fore.GREEN}{'█' * filled_len}{Fore.WHITE}{' ' * (length - filled_len)}{Style.RESET_ALL}"
    percentage = progress / total * 100
    sys.stdout.write(f"\r{Fore.WHITE}[{Fore.GREEN}*{Fore.WHITE}] {Fore.GREEN}{text} {Fore.WHITE}[{bar}{Fore.WHITE}] {Fore.GREEN}{percentage:.1f}%{Style.RESET_ALL}")
    sys.stdout.flush()

def with_loading_animation(func, message="Processing"):
    """Run a function with a loading animation"""
    done_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(done_event, message))
    spinner_thread.start()
    
    try:
        result = func()
    finally:
        done_event.set()
        spinner_thread.join()
    
    return result

def get_output_path(default_filename):
    """Get output path from user or use default"""
    use_default = input(f"{Fore.WHITE}[{Fore.GREEN}?{Fore.WHITE}] Use default output path? {Fore.GREEN}({default_filename}) {Fore.WHITE}[Y/n]: {Style.RESET_ALL}").lower() != 'n'
    if use_default:
        return default_filename
    else:
        return input(f"{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter output file path: {Style.RESET_ALL}")

def handle_txt_to_pdf():
    """Handle conversion from TXT to PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Convert TXT to PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.txt'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.pdf')
        
        def convert():
            print(f"\n{Fore.YELLOW}Converting {os.path.basename(input_file)} to PDF...{Style.RESET_ALL}")
            convert_txt_to_pdf(input_file, output_path)
        
        with_loading_animation(convert, message=f"Converting {os.path.basename(input_file)}")

def handle_img_to_pdf():
    """Handle conversion from JPG/PNG to PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Convert Image to PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.jpg', '.jpeg', '.png'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.pdf')
        
        def convert():
            print(f"\n{Fore.YELLOW}Converting {os.path.basename(input_file)} to PDF...{Style.RESET_ALL}")
            convert_jpg_to_pdf(input_file, output_path)
            
        with_loading_animation(convert, message=f"Converting {os.path.basename(input_file)}")

def handle_ppt_to_pdf():
    """Handle conversion from PPT to PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Convert PowerPoint to PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.ppt', '.pptx'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.pdf')
        
        def convert():
            print(f"\n{Fore.YELLOW}Converting {os.path.basename(input_file)} to PDF...{Style.RESET_ALL}")
            convert_ppt_to_pdf(input_file, output_path)
            
        with_loading_animation(convert, message=f"Converting {os.path.basename(input_file)}")

def handle_docx_to_pdf():
    """Handle conversion from DOCX to PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Convert Word Document to PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.doc', '.docx'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.pdf')
        
        def convert():
            print(f"\n{Fore.YELLOW}Converting {os.path.basename(input_file)} to PDF...{Style.RESET_ALL}")
            convert_docx_to_pdf(input_file, output_path)
            
        with_loading_animation(convert, message=f"Converting {os.path.basename(input_file)}")

def handle_html_to_pdf():
    """Handle conversion from HTML to PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Convert HTML to PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.html', '.htm'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.pdf')
        
        def convert():
            print(f"\n{Fore.YELLOW}Converting {os.path.basename(input_file)} to PDF...{Style.RESET_ALL}")
            convert_html_to_pdf(input_file, output_path)
            
        with_loading_animation(convert, message=f"Converting {os.path.basename(input_file)}")

def handle_merge_pdfs():
    """Handle merging multiple PDFs"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Merge PDFs {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_files = get_input_files(os.getcwd(), extensions=['.pdf'], allow_multiple=True)
    if input_files:
        output_path = get_output_path('merged.pdf')
        
        def merge():
            print(f"\n{Fore.YELLOW}Merging {len(input_files)} PDF files to {output_path}...{Style.RESET_ALL}")
            merge_pdfs(input_files, output_path)
            
        with_loading_animation(merge, message=f"Merging {len(input_files)} PDF files")

def handle_split_pdf():
    """Handle splitting a PDF into pages"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Split PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_dir = input(f"{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter output directory {Fore.GREEN}(leave blank for current directory){Fore.WHITE}: {Style.RESET_ALL}").strip()
        if not output_dir:
            output_dir = os.getcwd()
        if not os.path.exists(output_dir):
            create_dir = input(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Directory doesn't exist. Create it? {Fore.WHITE}[Y/n]: {Style.RESET_ALL}").lower() != 'n'
            if create_dir:
                os.makedirs(output_dir)
            else:
                print(f"{Fore.RED}Operation canceled.{Style.RESET_ALL}")
                return
                
        def split():
            print(f"\n{Fore.YELLOW}Splitting {os.path.basename(input_file)} into pages...{Style.RESET_ALL}")
            split_pdf(input_file, output_dir)
            
        with_loading_animation(split, message=f"Splitting {os.path.basename(input_file)}")

def handle_extract_text():
    """Handle extracting text from PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Extract Text from PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '.txt')
        
        def extract():
            print(f"\n{Fore.YELLOW}Extracting text from {os.path.basename(input_file)} to {output_path}...{Style.RESET_ALL}")
            extract_text_from_pdf(input_file, output_path)
            
        with_loading_animation(extract, message=f"Extracting text from {os.path.basename(input_file)}")

def handle_password_protect_pdf():
    """Handle adding password protection to a PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Password-Protect PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '_protected.pdf')
        
        password = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter password to encrypt PDF: {Style.RESET_ALL}")
        if not password:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.RED}Password cannot be empty.{Style.RESET_ALL}")
            return
            
        confirm_pwd = input(f"{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Confirm password: {Style.RESET_ALL}")
        if password != confirm_pwd:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.RED}Passwords do not match.{Style.RESET_ALL}")
            return
            
        # Ask for owner password (optional)
        use_owner_pw = input(f"\n{Fore.WHITE}[{Fore.GREEN}?{Fore.WHITE}] Set different owner password? {Fore.WHITE}[y/N]: {Style.RESET_ALL}").lower() == 'y'
        owner_pw = None
        if use_owner_pw:
            owner_pw = input(f"{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter owner password: {Style.RESET_ALL}")
        
        def protect():
            print(f"\n{Fore.YELLOW}Adding password protection to {os.path.basename(input_file)}...{Style.RESET_ALL}")
            password_protect_pdf(input_file, output_path, password, owner_pw)
            
        with_loading_animation(protect, message=f"Encrypting {os.path.basename(input_file)}")

def handle_remove_password_from_pdf():
    """Handle removing password protection from a PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Remove Password from PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '_decrypted.pdf')
        
        password = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter the PDF password: {Style.RESET_ALL}")
        if not password:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.RED}Password cannot be empty.{Style.RESET_ALL}")
            return
        
        def decrypt():
            print(f"\n{Fore.YELLOW}Removing password from {os.path.basename(input_file)}...{Style.RESET_ALL}")
            remove_password_from_pdf(input_file, output_path, password)
            
        with_loading_animation(decrypt, message=f"Decrypting {os.path.basename(input_file)}")

def handle_compress_pdf():
    """Handle compressing a PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Compress PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '_compressed.pdf')
        
        print(f"\n{Fore.WHITE}[{Fore.GREEN}i{Fore.WHITE}] {Fore.CYAN}Select compression quality:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] Low compression (better quality){Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}2{Fore.WHITE}] Medium compression (balanced){Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}3{Fore.WHITE}] High compression (smaller file){Style.RESET_ALL}")
        
        quality_choice = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Select quality (1-3): {Style.RESET_ALL}")
        quality_map = {'1': 'low', '2': 'medium', '3': 'high'}
        quality = quality_map.get(quality_choice, 'medium')
        
        def compress():
            print(f"\n{Fore.YELLOW}Compressing {os.path.basename(input_file)}...{Style.RESET_ALL}")
            compress_pdf(input_file, output_path, quality)
            
        with_loading_animation(compress, message=f"Compressing {os.path.basename(input_file)}")

def handle_rotate_pdf_pages():
    """Handle rotating pages in a PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Rotate Pages in PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '_rotated.pdf')
        
        # Show total page count
        try:
            reader = PdfReader(input_file)
            print(f"\n{Fore.WHITE}[{Fore.GREEN}i{Fore.WHITE}] {Fore.CYAN}PDF has {len(reader.pages)} pages total.{Style.RESET_ALL}")
        except:
            pass
            
        pages = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter pages to rotate (e.g., 1,3-5,7 or 'all'): {Style.RESET_ALL}")
        if pages.lower() == 'all':
            pages = None
        
        print(f"\n{Fore.WHITE}[{Fore.GREEN}i{Fore.WHITE}] {Fore.CYAN}Select rotation angle:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] 90° clockwise{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}2{Fore.WHITE}] 180° (upside down){Style.RESET_ALL}")
        print(f"{Fore.WHITE}[{Fore.GREEN}3{Fore.WHITE}] 270° clockwise (90° counterclockwise){Style.RESET_ALL}")
        
        angle_choice = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Select angle (1-3): {Style.RESET_ALL}")
        angle_map = {'1': 90, '2': 180, '3': 270}
        angle = angle_map.get(angle_choice, 90)
        
        def rotate():
            print(f"\n{Fore.YELLOW}Rotating pages in {os.path.basename(input_file)}...{Style.RESET_ALL}")
            rotate_pdf_pages(input_file, output_path, pages, angle)
            
        with_loading_animation(rotate, message=f"Rotating pages in {os.path.basename(input_file)}")

def handle_reorder_pdf_pages():
    """Handle reordering pages in a PDF"""
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}Reorder Pages in PDF {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    input_file = get_input_files(os.getcwd(), extensions=['.pdf'])
    if input_file:
        output_path = get_output_path(os.path.splitext(input_file)[0] + '_reordered.pdf')
        
        # Show page count and current order
        try:
            reader = PdfReader(input_file)
            num_pages = len(reader.pages)
            print(f"\n{Fore.WHITE}[{Fore.GREEN}i{Fore.WHITE}] {Fore.CYAN}The PDF has {num_pages} pages.{Style.RESET_ALL}")
            print(f"{Fore.WHITE}[{Fore.GREEN}i{Fore.WHITE}] {Fore.CYAN}Current order: {','.join([str(i+1) for i in range(num_pages)])}{Style.RESET_ALL}")
        except:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.RED}Could not read PDF file.{Style.RESET_ALL}")
            return
        
        page_order = input(f"\n{Fore.WHITE}[{Fore.GREEN}>{Fore.WHITE}] Enter new page order (e.g., 3,1,2): {Style.RESET_ALL}")
        if not page_order:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.RED}No page order specified.{Style.RESET_ALL}")
            return
        
        def reorder():
            print(f"\n{Fore.YELLOW}Reordering pages in {os.path.basename(input_file)}...{Style.RESET_ALL}")
            reorder_pdf_pages(input_file, output_path, page_order)
            
        with_loading_animation(reorder, message=f"Reordering pages in {os.path.basename(input_file)}")

def startup_animation():
    """Show a startup animation in retro hacker style"""
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Hacker-style loading text
    texts = [
        "Initializing system...",
        "Checking dependencies...",
        "Loading PDF libraries...",
        "Starting PdfX engine...",
        "Establishing secure connection...",
        "Setting up conversion modules...",
        "Calibrating PDF algorithms...",
        "PdfX ready!"
    ]
    
    print(f"{Fore.GREEN}")
    for text in texts:
        sys.stdout.write("\r" + " " * 50)  # Clear the line
        sys.stdout.write("\r> " + text)
        sys.stdout.flush()
        time.sleep(0.4)
        
        # Show a quick "working" effect
        for _ in range(3):
            sys.stdout.write(f"{Fore.WHITE}.{Fore.GREEN}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    print(f"\n\n{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}PdfX v0.1.0 loaded successfully!{Style.RESET_ALL}")
    time.sleep(0.5)

def main():
    """Main entry point for the CLI"""
    # Show startup animation
    startup_animation()
    
    while True:
        # Clear the terminal (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner()
        print_menu()
        
        choice = input(f"\n{Fore.WHITE}[{Fore.GREEN}root@pdfx{Fore.WHITE}]~$ {Style.RESET_ALL}")
        
        if choice == '1':
            handle_txt_to_pdf()
        elif choice == '2':
            handle_img_to_pdf()
        elif choice == '3':
            handle_ppt_to_pdf()
        elif choice == '4':
            handle_docx_to_pdf()
        elif choice == '5':
            handle_html_to_pdf()
        elif choice == '6':
            handle_merge_pdfs()
        elif choice == '7':
            handle_split_pdf()
        elif choice == '8':
            handle_extract_text()
        elif choice == '9':
            handle_password_protect_pdf()
        elif choice == '10':
            handle_remove_password_from_pdf()
        elif choice == '11':
            handle_compress_pdf()
        elif choice == '12':
            handle_rotate_pdf_pages()
        elif choice == '13':
            handle_reorder_pdf_pages()
        elif choice == '0':
            # Exit animation in retro hacker style
            print(f"\n{Fore.GREEN}╔═════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║                                         ║")
            print(f"{Fore.GREEN}║   {Fore.WHITE}Thank you for using PdfX! Goodbye!   {Fore.GREEN}║")
            print(f"{Fore.GREEN}║                                         ║")
            print(f"{Fore.GREEN}╚═════════════════════════════════════════╝{Style.RESET_ALL}")
            
            terminateText = "TERMINATING SESSION"
            sys.stdout.write(f"\n{Fore.WHITE}[{Fore.GREEN}*{Fore.WHITE}] {Fore.GREEN}{terminateText}")
            sys.stdout.flush()
            
            for i in range(10):
                sys.stdout.write(f"{Fore.GREEN}.")
                sys.stdout.flush()
                time.sleep(0.15)
                
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.GREEN}CONNECTION CLOSED{Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.RED}Invalid choice. Please enter a number between 0 and 13.{Style.RESET_ALL}")
        
        # Pause before showing the menu again
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def run_pdfx():
    """
    Entry point function for the console script.
    This function catches any errors that might occur during startup.
    """
    try:
        main()
    except Exception as e:
        # Print error information to help diagnose issues
        import traceback
        print(f"\n{Fore.RED}Error starting PdfX: {str(e)}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Detailed error information:{Style.RESET_ALL}")
        traceback.print_exc()
        print(f"\n{Fore.YELLOW}If you continue to experience issues, please report this bug.{Style.RESET_ALL}")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(run_pdfx())
