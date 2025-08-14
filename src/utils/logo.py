"""
QuantumKit Logo Module
Simplified logo and visual elements for the toolkit
"""

from colorama import Fore, Style, Back
import random

class QuantumKitLogo:
    """Класс для отображения логотипов QuantumKit"""
    
    @staticmethod
    def get_main_logo():
        """Основной логотип QuantumKit с оригинальным артом"""
        return f"""
{Fore.MAGENTA}   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓
{Fore.MAGENTA} ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒
{Fore.MAGENTA} ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░
{Fore.MAGENTA} ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ 
{Fore.MAGENTA} ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒
{Fore.MAGENTA} ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
{Fore.MAGENTA}  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░
{Fore.MAGENTA}    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   
{Fore.MAGENTA}     ░       ░           ░  ░         ░             ░            ░   
{Fore.WHITE}                                {Fore.YELLOW}by Sqrilizz{Fore.RESET}

{Fore.MAGENTA}                    QUANTUMKIT v6.2 - ADVANCED SECURITY TOOLKIT{Fore.RESET}
"""
    
    @staticmethod
    def get_simple_logo():
        """Простой логотип"""
        return f"""
{Fore.MAGENTA}                    QUANTUMKIT v6.2 - ADVANCED SECURITY TOOLKIT{Fore.RESET}
{Fore.WHITE}                                by Sqrilizz{Fore.RESET}
"""

class CategoryIcons:
    """Иконки для категорий инструментов"""
    
    @staticmethod
    def discord():
        return f"{Fore.BLUE}🔥 Discord Tools"
    
    @staticmethod
    def network():
        return f"{Fore.GREEN}🌐 Network Tools"
    
    @staticmethod
    def security():
        return f"{Fore.RED}🔐 Security Tools"
    
    @staticmethod
    def utility():
        return f"{Fore.YELLOW}⚙️ Utility Tools"

class StatusIcons:
    """Иконки статуса"""
    
    @staticmethod
    def success():
        return f"{Fore.GREEN}✓"
    
    @staticmethod
    def error():
        return f"{Fore.RED}✗"
    
    @staticmethod
    def warning():
        return f"{Fore.YELLOW}⚠"
    
    @staticmethod
    def info():
        return f"{Fore.CYAN}ℹ"
    
    @staticmethod
    def loading():
        return f"{Fore.MAGENTA}⟳"

class ProgressBars:
    """Упрощенные прогресс-бары"""
    
    @staticmethod
    def get_bar(progress, width=40):
        """Создать прогресс-бар"""
        filled = int((progress / 100) * width)
        bar = f"{Fore.MAGENTA}{'█' * filled}{Fore.WHITE}{'░' * (width - filled)}"
        return f"[{bar}] {progress:.1f}%"

class LoadingAnimations:
    """Анимации загрузки"""
    
    @staticmethod
    def spinner():
        """Спиннер"""
        return ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    @staticmethod
    def dots():
        """Точки"""
        return ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

class ColorSchemes:
    """Цветовые схемы"""
    
    @staticmethod
    def cyberpunk():
        """Киберпанк схема"""
        return {
            'primary': Fore.MAGENTA,
            'secondary': Fore.CYAN,
            'accent': Fore.YELLOW,
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'info': Fore.BLUE
        }
    
    @staticmethod
    def matrix():
        """Матрица схема"""
        return {
            'primary': Fore.GREEN,
            'secondary': Fore.WHITE,
            'accent': Fore.CYAN,
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'info': Fore.CYAN
        }

def create_banner(title, subtitle="", style="main"):
    """Создать баннер с заголовком"""
    if style == "main":
        logo = QuantumKitLogo.get_main_logo()
    else:
        logo = QuantumKitLogo.get_simple_logo()
    
    if title:
        title_line = f"{Fore.CYAN}║{Fore.WHITE}{title.center(78)}{Fore.CYAN}║"
        logo = logo.replace("║                    QUANTUMKIT v6.2 - ADVANCED SECURITY TOOLKIT                  ║", title_line)
    
    if subtitle:
        subtitle_line = f"{Fore.CYAN}║{Fore.YELLOW}{subtitle.center(78)}{Fore.CYAN}║"
        logo = logo.replace("║                                by Sqrilizz                                    ║", subtitle_line)
    
    return logo
