"""
Utility functions for PdfIt
"""
import os
import sys
import platform
from colorama import Fore, Style, Back

def print_banner():
    """Print an ASCII art header for PdfIt"""
    
    # Define the ASCII art banner
    banner = f"""
{Fore.CYAN}
    ______     _____   _____ __  
   / __ \\_____/ _/ /  / __(_) /_ 
  / /_/ / ___/ // /  / /_/ / __/ 
 / ____/ /  _/ // /___/ __/ / /_  
/_/   /_/  /___/_____/_/ /_/\\__/  
{Style.RESET_ALL}
"""
    
    # Print the banner
    print(banner)
    print(f"{Fore.GREEN}PDF Conversion & Manipulation Tool{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Version: 0.1.0{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}")

def print_menu():
    """Print the main menu options"""
    print(f"\n{Fore.CYAN}==== MAIN MENU ===={Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}CONVERT TO PDF:{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 1. {Fore.YELLOW}Convert TXT to PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 2. {Fore.YELLOW}Convert Image to PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 3. {Fore.YELLOW}Convert DOCX to PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 4. {Fore.YELLOW}Convert HTML to PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 5. {Fore.YELLOW}Convert PowerPoint to PDF{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}MANIPULATE PDF:{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 6. {Fore.GREEN}Merge PDF Files{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 7. {Fore.GREEN}Split PDF into Pages{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 8. {Fore.GREEN}Extract Text from PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE} 9. {Fore.GREEN}Add Password Protection{Style.RESET_ALL}")
    print(f"{Fore.WHITE}10. {Fore.GREEN}Remove Password Protection{Style.RESET_ALL}")
    print(f"{Fore.WHITE}11. {Fore.GREEN}Compress PDF{Style.RESET_ALL}")
    print(f"{Fore.WHITE}12. {Fore.GREEN}Rotate PDF Pages{Style.RESET_ALL}")
    print(f"{Fore.WHITE}13. {Fore.GREEN}Reorder PDF Pages{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Type 'q' to quit{Style.RESET_ALL}")

def list_files_in_directory(directory_path='.', extension=None):
    """List all files in a directory with an optional extension filter"""
    files = []
    try:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path) and (extension is None or file.lower().endswith(extension)):
                files.append(file_path)
    except Exception as e:
        print(f"\n{Fore.RED}Error listing files: {str(e)}{Style.RESET_ALL}")
    return files

def display_files(files):
    """Display a list of files with numbering"""
    print(f"\n{Fore.WHITE}Available files:{Style.RESET_ALL}")
    if not files:
        print(f"{Fore.YELLOW}No files found.{Style.RESET_ALL}")
        return
        
    for i, file in enumerate(files, 1):
        file_size = os.path.getsize(file) / 1024  # convert to KB
        print(f"{Fore.WHITE}{i}. {Fore.CYAN}{file}{Style.RESET_ALL} ({file_size:.1f} KB)")

def get_input_files(message, directory_path='.', extension=None):
    """Get input files from the user"""
    files = list_files_in_directory(directory_path, extension)
    
    if not files:
        print(f"{Fore.RED}No{extension if extension else ''} files found in this directory.{Style.RESET_ALL}")
        return None
        
    display_files(files)
    
    print(f"\n{Fore.CYAN}{message}{Style.RESET_ALL}")
    selection = input(f"{Fore.WHITE}Enter your choice (or 'q' to return to menu): {Style.RESET_ALL}")
    
    if selection.lower() == 'q':
        return None
        
    try:
        selection = int(selection)
        if selection < 1 or selection > len(files):
            print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            return None
            
        return files[selection - 1]
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        return None
