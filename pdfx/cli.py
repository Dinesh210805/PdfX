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
    extract_text_from_pdf
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
        elif choice == '9':            # Exit animation in retro hacker style
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
            print(f"\n{Fore.RED}Invalid choice. Please enter a number between 1 and 9.{Style.RESET_ALL}")
        
        # Pause before showing the menu again
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
