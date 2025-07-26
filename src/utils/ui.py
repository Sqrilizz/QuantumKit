"""
QuantumKit User Interface
"""
import os
import sys
import time
import threading
from typing import List, Dict, Optional, Callable
from datetime import datetime

from colorama import Fore, Style, init
from src.config.settings import COLORS, APP_NAME, APP_VERSION, APP_AUTHOR
from src.utils.logger import get_logger

# Initialize colorama
init(autoreset=True)

class ProgressBar:
    """Animated progress bar"""
    
    def __init__(self, total: int, description: str = "Progress", width: int = 50):
        self.total = total
        self.current = 0
        self.description = description
        self.width = width
        self.start_time = time.time()
        self.logger = get_logger("progress_bar")
    
    def update(self, value: int = None, increment: int = 1):
        """Update progress bar"""
        if value is not None:
            self.current = value
        else:
            self.current += increment
        
        self.current = min(self.current, self.total)
        self._display()
    
    def _display(self):
        """Display the progress bar"""
        percentage = (self.current / self.total) * 100
        filled_width = int((self.current / self.total) * self.width)
        
        bar = "█" * filled_width + "░" * (self.width - filled_width)
        
        elapsed_time = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed_time / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
        
        sys.stdout.write(f"\r{Fore.CYAN}{self.description}: [{bar}] {percentage:.1f}% ({self.current}/{self.total}) {eta_str}")
        sys.stdout.flush()
    
    def finish(self):
        """Finish the progress bar"""
        self.current = self.total
        self._display()
        print()  # New line after progress bar
        elapsed_time = time.time() - self.start_time
        self.logger.success(f"Completed in {elapsed_time:.2f} seconds")

class Spinner:
    """Loading spinner"""
    
    def __init__(self, message: str = "Loading"):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_char = 0
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the spinner"""
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the spinner"""
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()
    
    def _spin(self):
        """Spin animation"""
        while self.running:
            char = self.spinner_chars[self.current_char]
            sys.stdout.write(f"\r{Fore.CYAN}{char} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
            self.current_char = (self.current_char + 1) % len(self.spinner_chars)

class Menu:
    """Interactive menu system"""
    
    def __init__(self, title: str = "Menu"):
        self.title = title
        self.options: List[Dict] = []
        self.logger = get_logger("menu")
    
    def add_option(self, key: str, label: str, action: Callable, description: str = ""):
        """Add menu option"""
        self.options.append({
            "key": key,
            "label": label,
            "action": action,
            "description": description
        })
    
    def display(self):
        """Display the menu"""
        while True:
            self._clear_screen()
            self._print_banner()
            self._print_title()
            self._print_options()
            
            try:
                choice = input(f"\n{Fore.MAGENTA}Enter your choice: ").strip().upper()
                
                if choice == "0" or choice == "EXIT":
                    self.logger.info("Exiting menu")
                    break
                
                # Find and execute the selected option
                for option in self.options:
                    if option["key"].upper() == choice:
                        try:
                            option["action"]()
                        except KeyboardInterrupt:
                            self.logger.info("Operation cancelled by user")
                        except Exception as e:
                            self.logger.error(f"Error executing option: {str(e)}")
                        break
                else:
                    self.logger.warning(f"Invalid choice: {choice}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                self.logger.info("Exiting menu")
                break
            except EOFError:
                self.logger.info("Exiting menu")
                break
    
    def _clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _print_banner(self):
        """Print QuantumKit banner"""
        banner = [
            "   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓",
            " ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒",
            " ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░",
            " ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ ",
            " ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒",
            " ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░",
            "  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░",
            "    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   ",
            "     ░       ░           ░  ░         ░             ░            ░   ",
            "",
            f"                                by {APP_AUTHOR}"
        ]
        
        for line in banner:
            print(f"{Fore.MAGENTA}{line}")
    
    def _print_title(self):
        """Print menu title"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║{Fore.WHITE} {self.title:^76} {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    def _print_options(self):
        """Print menu options"""
        for i, option in enumerate(self.options, 1):
            key = option["key"]
            label = option["label"]
            description = option["description"]
            
            if description:
                print(f"{Fore.MAGENTA}{key}. {Fore.WHITE}{label} - {Fore.YELLOW}{description}")
            else:
                print(f"{Fore.MAGENTA}{key}. {Fore.WHITE}{label}")
        
        print(f"\n{Fore.MAGENTA}0. {Fore.WHITE}Exit")

class Table:
    """Display data in table format"""
    
    def __init__(self, headers: List[str]):
        self.headers = headers
        self.rows: List[List[str]] = []
    
    def add_row(self, row: List[str]):
        """Add a row to the table"""
        self.rows.append(row)
    
    def display(self):
        """Display the table"""
        if not self.rows:
            return
        
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(self.headers):
            max_width = len(header)
            for row in self.rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width)
        
        # Print header
        header_line = "│"
        separator_line = "├"
        for i, header in enumerate(self.headers):
            header_line += f" {header:<{col_widths[i]}} │"
            separator_line += "─" * (col_widths[i] + 2) + "┼"
        separator_line = separator_line[:-1] + "┤"
        
        print(f"{Fore.CYAN}┌{separator_line[1:-1].replace('┼', '┬')}┐")
        print(f"{Fore.CYAN}│{Fore.WHITE}{header_line[1:]}")
        print(f"{Fore.CYAN}{separator_line}")
        
        # Print rows
        for row in self.rows:
            row_line = "│"
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_line += f" {str(cell):<{col_widths[i]}} │"
            print(f"{Fore.CYAN}│{Fore.WHITE}{row_line[1:]}")
        
        print(f"{Fore.CYAN}└{separator_line[1:-1].replace('┼', '┴')}┘")

def print_status(message: str, status: str = "info"):
    """Print status message with color"""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    
    icons = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✗"
    }
    
    color = colors.get(status, Fore.WHITE)
    icon = icons.get(status, "•")
    
    print(f"{color}{icon} {message}{Style.RESET_ALL}")

def print_header(title: str, subtitle: str = ""):
    """Print section header"""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.WHITE} {title:^76} {Fore.CYAN}║")
    if subtitle:
        print(f"{Fore.CYAN}║{Fore.YELLOW} {subtitle:^76} {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

def confirm_action(message: str = "Are you sure?") -> bool:
    """Ask for user confirmation"""
    while True:
        response = input(f"{Fore.YELLOW}{message} (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print(f"{Fore.RED}Please enter 'y' or 'n'") 