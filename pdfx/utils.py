"""
Utility functions for the PdfX package
"""
import os
import colorama
from colorama import Fore, Style
from tabulate import tabulate

# Initialize colorama
colorama.init()

def list_files_in_directory(directory, extensions=None):
    """
    List files in a directory with optional extension filtering
    
    Args:
        directory: Directory to search
        extensions: List of extensions to filter by (e.g., ['.txt', '.jpg'])
    
    Returns:
        List of filenames
    """
    files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            if extensions:
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    files.append(file)
            else:
                files.append(file)
    return files

def display_files(files, title="Files in current directory"):
    """Display a list of files in a retro hacker style table"""
    if not files:
        print(f"{Fore.RED}[!] No files found.{Style.RESET_ALL}")
        return
    
    file_data = []
    for idx, file in enumerate(files, 1):
        # Get file extension
        ext = os.path.splitext(file)[1].lower()
        
        # Get file size
        size = os.path.getsize(os.path.join(os.getcwd(), file))
        size_str = format_size(size)
        
        file_data.append([
            f"{Fore.WHITE}[{Fore.GREEN}{idx}{Fore.WHITE}]{Style.RESET_ALL}",
            f"{Fore.GREEN}{file}{Style.RESET_ALL}",
            f"{Fore.WHITE}{ext}{Style.RESET_ALL}",
            f"{Fore.GREEN}{size_str}{Style.RESET_ALL}"
        ])
    
    print(f"\n{Fore.GREEN}╔═══════ {Fore.WHITE}[ {Fore.GREEN}{title} {Fore.WHITE}]{Fore.GREEN} ═══════╗{Style.RESET_ALL}")
    print(tabulate(file_data, headers=[f"{Fore.WHITE}#", f"Filename", f"Type", f"Size{Style.RESET_ALL}"], 
                  tablefmt="plain"))

def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def print_banner():
    """Print the PdfX banner (retro hacking style)"""
    banner = f"""
{Fore.GREEN}╔═══════════════════════════════════════════╗
{Fore.GREEN}║                                           ║
{Fore.GREEN}║  {Style.BRIGHT}██████╗ ██████╗ ███████╗██╗  ██╗{Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║  {Style.BRIGHT}██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝{Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║  {Style.BRIGHT}██████╔╝██║  ██║█████╗   ╚███╔╝ {Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║  {Style.BRIGHT}██╔═══╝ ██║  ██║██╔══╝   ██╔██╗ {Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║  {Style.BRIGHT}██║     ██████╔╝██║     ██╔╝ ██╗{Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║  {Style.BRIGHT}╚═╝     ╚═════╝ ╚═╝     ╚═╝  ╚═╝{Style.RESET_ALL}{Fore.GREEN}        ║
{Fore.GREEN}║                                           ║
{Fore.GREEN}║      {Fore.WHITE}A Powerful PDF Converter Tool{Fore.GREEN}       ║
{Fore.GREEN}║      {Fore.RED}by Dinesh{Fore.WHITE} - {Fore.GREEN}github.com/Dinesh210805{Fore.GREEN}  ║
{Fore.GREEN}╚═══════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_menu():
    """Print the main menu options (retro hacking style)"""
    print(f"{Fore.GREEN}╔═════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.WHITE}[{Fore.GREEN}MENU{Fore.WHITE}]{Fore.GREEN}                          ║")
    print(f"{Fore.GREEN}╠═════════════════════════════════════╣")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}]{Fore.GREEN} Convert TXT to PDF         ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}2{Fore.WHITE}]{Fore.GREEN} Convert JPG/PNG to PDF     ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}3{Fore.WHITE}]{Fore.GREEN} Convert PPT to PDF         ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}4{Fore.WHITE}]{Fore.GREEN} Convert DOCX to PDF        ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}5{Fore.WHITE}]{Fore.GREEN} Convert HTML to PDF        ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}6{Fore.WHITE}]{Fore.GREEN} Merge PDFs                 ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}7{Fore.WHITE}]{Fore.GREEN} Split PDF                  ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}8{Fore.WHITE}]{Fore.GREEN} Extract Text from PDF      ║")
    print(f"{Fore.GREEN}║  {Fore.WHITE}[{Fore.GREEN}9{Fore.WHITE}]{Fore.GREEN} {Fore.RED}Exit                      {Fore.GREEN}║")
    print(f"{Fore.GREEN}╚═════════════════════════════════════╝{Style.RESET_ALL}")

def get_input_files(directory, extensions=None, allow_multiple=False):
    """
    Get selected input files from the user
    
    Args:
        directory: Directory to list files from
        extensions: List of extensions to filter files by
        allow_multiple: Whether to allow selecting multiple files
    
    Returns:
        A single file path or list of file paths
    """
    files = list_files_in_directory(directory, extensions)
    display_files(files)
    
    if not files:
        print(f"{Fore.YELLOW}No matching files found in the current directory.{Style.RESET_ALL}")
        custom_path = input(f"\n{Fore.CYAN}Enter custom file path: {Style.RESET_ALL}")
        if os.path.isfile(custom_path):
            return [custom_path] if allow_multiple else custom_path
        else:
            print(f"{Fore.RED}Invalid file path. Operation canceled.{Style.RESET_ALL}")
            return None
      # Check if user wants all files
    if allow_multiple:
        prompt = f"{Fore.GREEN}Select files {Fore.WHITE}[{Fore.GREEN}comma-separated numbers{Fore.WHITE}, {Fore.GREEN}'all'{Fore.WHITE}, or {Fore.GREEN}'c'{Fore.WHITE} for custom path{Fore.WHITE}]: {Style.RESET_ALL}"
    else:
        prompt = f"{Fore.GREEN}Select file {Fore.WHITE}[{Fore.GREEN}number{Fore.WHITE}, {Fore.GREEN}'all'{Fore.WHITE}, or {Fore.GREEN}'c'{Fore.WHITE} for custom path{Fore.WHITE}]: {Style.RESET_ALL}"
    
    selection = input(prompt)
    
    # Handle custom path
    if selection.lower() == 'c':
        custom_path = input(f"{Fore.CYAN}Enter custom file path: {Style.RESET_ALL}")
        if os.path.isfile(custom_path):
            return [custom_path] if allow_multiple else custom_path
        else:
            print(f"{Fore.RED}Invalid file path. Operation canceled.{Style.RESET_ALL}")
            return None
      # Handle 'all' for any selection type
    if selection.lower() == 'all':
        if allow_multiple:
            return [os.path.join(directory, file) for file in files]
        else:
            # For single file selection mode, just return the first matching file
            if files:
                print(f"{Fore.GREEN}Converting all files is enabled for batch mode only. Using first file: {files[0]}{Style.RESET_ALL}")
                return os.path.join(directory, files[0])
            return None
    
    # Handle numeric selections
    try:
        if allow_multiple:
            # Handle comma-separated selections
            indices = [int(idx.strip()) for idx in selection.split(',')]
            selected_files = []
            for idx in indices:
                if 1 <= idx <= len(files):
                    selected_files.append(os.path.join(directory, files[idx-1]))
                else:
                    print(f"{Fore.RED}Invalid selection: {idx}. Skipping.{Style.RESET_ALL}")
            return selected_files if selected_files else None
        else:
            # Handle single selection
            idx = int(selection)
            if 1 <= idx <= len(files):
                return os.path.join(directory, files[idx-1])
            else:
                print(f"{Fore.RED}Invalid selection. Operation canceled.{Style.RESET_ALL}")
                return None
    except ValueError:
        print(f"{Fore.RED}Invalid input. Operation canceled.{Style.RESET_ALL}")
        return None
