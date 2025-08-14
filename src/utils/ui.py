import os
import time
import sys
from typing import List, Optional, Callable
from colorama import Fore, Style, Back, init
import threading

# Инициализация colorama
init(autoreset=True)

# Упрощенные цветовые константы
COLOR_SUCCESS = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_WARNING = Fore.YELLOW
COLOR_INFO = Fore.CYAN
COLOR_PRIMARY = Fore.MAGENTA
COLOR_SECONDARY = Fore.BLUE
COLOR_RESET = Style.RESET_ALL
COLOR_HIGHLIGHT = Fore.WHITE + Style.BRIGHT

# Минималистичные символы
SYMBOLS = {
    'check': '✓',
    'cross': '✗',
    'arrow': '→',
    'star': '★',
    'line': '─',
    'corner_tl': '┌',
    'corner_tr': '┐',
    'corner_bl': '└',
    'corner_br': '┘',
    'line_v': '│',
    'line_h': '─',
    'cross_t': '├',
    'cross_b': '┤'
}

class ProgressBar:
    """Упрощенная прогресс-бар"""
    
    def __init__(self, total: int, width: int = 40, title: str = ""):
        self.total = total
        self.width = width
        self.title = title
        self.current = 0
    
    def update(self, value: int):
        """Обновить прогресс"""
        self.current = value
        percentage = (self.current / self.total) * 100
        filled = int((self.current / self.total) * self.width)
        
        bar = f"{COLOR_PRIMARY}{'█' * filled}{Fore.WHITE}{'░' * (self.width - filled)}"
        print(f"\r{self.title} {bar} {percentage:5.1f}%", end='', flush=True)
    
    def finish(self):
        """Завершить прогресс-бар"""
        self.update(self.total)
        print()

class Spinner:
    """Упрощенный спиннер"""
    
    def __init__(self, text: str = "Loading..."):
        self.text = text
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread = None
    
    def start(self):
        """Запустить спиннер"""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Остановить спиннер"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * (len(self.text) + 10) + "\r", end='', flush=True)
    
    def _spin(self):
        """Внутренний метод для анимации"""
        i = 0
        while self.running:
            char = self.spinner_chars[i % len(self.spinner_chars)]
            print(f"\r{COLOR_PRIMARY}{char} {self.text}", end='', flush=True)
            time.sleep(0.1)
            i += 1

class Notification:
    """Упрощенные уведомления"""
    
    @staticmethod
    def success(message: str):
        """Успешное уведомление"""
        print(f"{COLOR_SUCCESS}{SYMBOLS['check']} {message}")
    
    @staticmethod
    def error(message: str):
        """Уведомление об ошибке"""
        print(f"{COLOR_ERROR}{SYMBOLS['cross']} {message}")
    
    @staticmethod
    def warning(message: str):
        """Предупреждение"""
        print(f"{COLOR_WARNING}⚠ {message}")
    
    @staticmethod
    def info(message: str):
        """Информационное уведомление"""
        print(f"{COLOR_INFO}ℹ {message}")

def print_banner():
    """Красивый баннер QuantumKit с оригинальным артом"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{COLOR_PRIMARY}   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓
{COLOR_PRIMARY} ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒
{COLOR_PRIMARY} ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░
{COLOR_PRIMARY} ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ 
{COLOR_PRIMARY} ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒
{COLOR_PRIMARY} ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
{COLOR_PRIMARY}  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░
{COLOR_PRIMARY}    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   
{COLOR_PRIMARY}     ░       ░           ░  ░         ░             ░            ░   
{Fore.WHITE}                                {COLOR_WARNING}by Sqrilizz{COLOR_RESET}

{COLOR_PRIMARY}                    QUANTUMKIT v6.2 - ADVANCED SECURITY TOOLKIT{COLOR_RESET}
"""
    print(banner)

def print_header(title: str):
    """Упрощенный заголовок"""
    width = 50
    print(f"\n{COLOR_PRIMARY}{SYMBOLS['line_h'] * width}")
    print(f"{COLOR_PRIMARY}{title.center(width)}")
    print(f"{COLOR_PRIMARY}{SYMBOLS['line_h'] * width}\n")

def print_separator():
    """Простой разделитель"""
    print(f"{COLOR_PRIMARY}{SYMBOLS['line_h'] * 50}")

def print_success(message: str):
    """Успешное сообщение"""
    print(f"{COLOR_SUCCESS}{SYMBOLS['check']} {message}")

def print_error(message: str):
    """Сообщение об ошибке"""
    print(f"{COLOR_ERROR}{SYMBOLS['cross']} {message}")

def print_warning(message: str):
    """Предупреждение"""
    print(f"{COLOR_WARNING}⚠ {message}")

def print_info(message: str):
    """Информационное сообщение"""
    print(f"{COLOR_INFO}ℹ {message}")

def confirm_action(message: str) -> bool:
    """Подтверждение действия"""
    while True:
        response = input(f"{COLOR_WARNING}{message} (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print(f"{COLOR_ERROR}Please enter 'y' or 'n'")

class Menu:
    """Меню с пагинацией по категориям"""
    
    def __init__(self, title: str):
        self.title = title
        self.options = []
        self.current_page = 1
        self.items_per_page = 8  # Количество элементов на странице
    
    def add_option(self, key: str, label: str, action: Callable, description: str = "", category: str = ""):
        """Добавить опцию в меню"""
        self.options.append({
            'key': key,
            'label': label,
            'action': action,
            'description': description,
            'category': category
        })
    
    def display(self):
        """Отобразить меню с пагинацией"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            print_header(self.title)
            
            # Разбить опции на страницы
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_options = self.options[start_idx:end_idx]
            
            # Отобразить опции текущей страницы
            for option in page_options:
                key = option['key']
                label = option['label']
                desc = option.get('description', '')
                category = option.get('category', '')
                
                # Добавить иконку категории
                category_icon = self._get_category_icon(category)
                display_label = f"{category_icon} {label}" if category_icon else label
                
                print(f"{COLOR_PRIMARY}{key:>2}. {Fore.WHITE}{display_label}")
                if desc:
                    print(f"{Style.DIM}    {desc}")
                print()
            
            # Навигация между страницами
            total_pages = (len(self.options) + self.items_per_page - 1) // self.items_per_page
            
            if total_pages > 1:
                nav_text = f"{COLOR_WARNING}Страница {self.current_page}/{total_pages}"
                if self.current_page > 1:
                    nav_text += f" {COLOR_PRIMARY}[P] Предыдущая"
                if self.current_page < total_pages:
                    nav_text += f" {COLOR_PRIMARY}[N] Следующая"
                print(f"{nav_text}\n")
            
            print(f"{COLOR_PRIMARY}0. {COLOR_ERROR}Выход")
            print_separator()
            
            choice = input(f"{COLOR_SUCCESS}>>> ").strip().upper()
            
            if choice == "0":
                break
            elif choice == "P" and self.current_page > 1:
                self.current_page -= 1
            elif choice == "N" and self.current_page < total_pages:
                self.current_page += 1
            else:
                # Найти и выполнить действие
                for option in page_options:
                    if option['key'].upper() == choice:
                        try:
                            option['action']()
                            input(f"\n{COLOR_WARNING}Нажмите Enter для продолжения...")
                        except Exception as e:
                            print_error(f"Ошибка выполнения {option['label']}: {str(e)}")
                            input(f"\n{COLOR_WARNING}Нажмите Enter для продолжения...")
                        break
    
    def _get_category_icon(self, category: str) -> str:
        """Получить иконку для категории"""
        icons = {
            "discord": "🔥",
            "network": "🌐", 
            "security": "🔐",
            "utility": "⚙️",
            "reporting": "📊",
            "system": "💻"
        }
        return icons.get(category.lower(), "")

def create_table(headers: List[str], rows: List[List[str]], title: str = "") -> str:
    """Упрощенная таблица"""
    if not rows:
        return ""
    
    # Определить ширину колонок
    col_widths = []
    for i in range(len(headers)):
        max_width = len(headers[i])
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(row[i]))
        col_widths.append(max_width + 2)
    
    # Создать таблицу
    table = ""
    if title:
        table += f"{COLOR_PRIMARY}{title}\n"
    
    # Заголовок
    table += f"{COLOR_PRIMARY}{SYMBOLS['corner_tl']}"
    for i, header in enumerate(headers):
        table += f"{SYMBOLS['line_h'] * col_widths[i]}{SYMBOLS['cross_t'] if i < len(headers) - 1 else SYMBOLS['corner_tr']}"
    table += "\n"
    
    table += f"{COLOR_PRIMARY}{SYMBOLS['line_v']}"
    for i, header in enumerate(headers):
        table += f"{Fore.WHITE}{header.center(col_widths[i])}{COLOR_PRIMARY}{SYMBOLS['line_v']}"
    table += "\n"
    
    # Разделитель
    table += f"{COLOR_PRIMARY}{SYMBOLS['cross_t']}"
    for i in range(len(headers)):
        table += f"{SYMBOLS['line_h'] * col_widths[i]}{SYMBOLS['cross_t'] if i < len(headers) - 1 else SYMBOLS['cross_b']}"
    table += "\n"
    
    # Строки данных
    for row in rows:
        table += f"{COLOR_PRIMARY}{SYMBOLS['line_v']}"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                table += f"{Fore.WHITE}{cell.center(col_widths[i])}{COLOR_PRIMARY}{SYMBOLS['line_v']}"
        table += "\n"
    
    # Нижняя граница
    table += f"{COLOR_PRIMARY}{SYMBOLS['corner_bl']}"
    for i in range(len(headers)):
        table += f"{SYMBOLS['line_h'] * col_widths[i]}{SYMBOLS['cross_b'] if i < len(headers) - 1 else SYMBOLS['corner_br']}"
    
    return table

def animate_loading(text: str, duration: float = 2.0):
    """Анимация загрузки"""
    spinner = Spinner(text)
    spinner.start()
    time.sleep(duration)
    spinner.stop()
